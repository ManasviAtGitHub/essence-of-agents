"""The compiler you can talk to - the models-track capstone, running.

A natural-language sentence is COMPILED into a typed tool-call plan (the IR),
the same agent loop you hand-built in course 1. The pipeline is:

    NL  --front-end (a model, grammar-constrained)-->  IR  --verifier-->  runnable plan

Two halves, both real here:
  * the GRAMMAR reduces every decode step to the set of LEGAL next options
    (from the tool schema), so the front-end can never emit an invalid plan -
    this is constrained decoding, the mechanism from Module 0's sampler;
  * the VERIFIER type-checks the finished plan and fails LOUDLY - Module 7.

The front-end model is a swappable DRIVER. The default drivers are keyless and
deterministic (a scripted stand-in, and a tiny keyword parser) - the FakeClient
analog, so this runs in CI with no download. Plug in `LlamaDriver` (a quantized
small-instruct GGUF via llama-cpp-python) for the real thing; the grammar
guarantees valid structure even from a ~1B model, which is exactly why a tiny
local model is enough. See grammar.gbnf for llama.cpp's native GBNF path.

Run:
    python compiler.py                 # compile the worked example, keyless
    python compiler.py "search for umbrellas and email me the top result"
"""
from __future__ import annotations

import re
import sys

# ---------------- the backend: the tool catalog ----------------
TOOLS = {
    "get_weather": {"args": ["city"],  "ret": ["rain", "temp"]},
    "add_to_cart": {"args": ["item"],  "ret": []},
    "search":      {"args": ["query"], "ret": ["top"]},
    "send_email":  {"args": ["to"],    "ret": []},
}
TOOL_NAMES = list(TOOLS)


# ---------------- the grammar: legal next options, computed from state ----------------
def legal_starts():
    """A statement may begin a conditional, a tool call, or end the program."""
    return ["<end>", "if"] + TOOL_NAMES


def legal_refs(defined):
    return list(defined)


def legal_fields(ir, ref):
    st = _stmt(ir, ref)
    return list(TOOLS[st["tool"]]["ret"]) if st and st["tool"] in TOOLS else []


def legal_args(tool):
    return list(TOOLS[tool]["args"]) if tool in TOOLS else []


def _stmt(ir, sid):
    for s in ir:
        if s["id"] == sid:
            return s
    return None


# ---------------- the front-end: grammar-constrained decode ----------------
def compile(nl, driver, constrained=True, max_stmts=4):
    """Lower a sentence into an IR, asking the driver to choose within the legal set.

    When `constrained`, the driver is only ever offered grammar-legal options, so
    the resulting IR is syntactically valid by construction. When not, a bogus tool
    and an undefined ref are also offered - so an adversarial driver can produce an
    invalid plan (which the verifier then catches). That contrast is the whole point.
    """
    ir, defined = [], []
    for _ in range(max_stmts):
        starts = legal_starts() + ([] if constrained else ["teleport"])
        head = driver.choose(nl, "start", starts, {"defined": list(defined)})
        if head == "<end>":
            break
        sid = "n%d" % (len(ir) + 1)
        cond, tool = None, head
        if head == "if":
            refs = legal_refs(defined) + ([] if constrained else ["n_undef"])
            ref = driver.choose(nl, "ref", refs, {"defined": list(defined)})
            fields = legal_fields(ir, ref) or ["rain", "temp"]
            field = driver.choose(nl, "field", fields, {"ref": ref})
            cond = [ref, field]
            tools = TOOL_NAMES + ([] if constrained else ["teleport"])
            tool = driver.choose(nl, "tool", tools, {"defined": list(defined)})
        args = {a: driver.value(nl, tool, a) for a in legal_args(tool)}
        ir.append({"id": sid, "tool": tool, "args": args, "cond": cond})
        defined.append(sid)
    return ir


# ---------------- the backend: the verifier ----------------
def verify(ir):
    """Real static checks over the compiled DAG. Returns a list of compile errors."""
    errs, defined = [], []
    for s in ir:
        if s["tool"] not in TOOLS:
            errs.append("%s: unknown tool '%s'" % (s["id"], s["tool"]))
        else:
            for k in s["args"]:
                if k not in TOOLS[s["tool"]]["args"]:
                    errs.append("%s: '%s' has no arg '%s'" % (s["id"], s["tool"], k))
        c = s.get("cond")
        if c:
            ref, field = c
            if ref not in defined:
                errs.append("%s: ref '%s' used before it is defined" % (s["id"], ref))
            else:
                src = _stmt(ir, ref)
                if src and src["tool"] in TOOLS and field not in TOOLS[src["tool"]]["ret"]:
                    errs.append("%s: '%s' has no field '%s'" % (s["id"], ref, field))
        defined.append(s["id"])
    return errs


def render(ir):
    lines = []
    for s in ir:
        call = "%s(%s)" % (s["tool"], ", ".join("%s=%s" % (k, v) for k, v in s["args"].items()))
        if s.get("cond"):
            lines.append("%s = if %s.%s: %s" % (s["id"], s["cond"][0], s["cond"][1], call))
        else:
            lines.append("%s = %s" % (s["id"], call))
    return "\n".join(lines)


def compile_and_repair(nl, make_driver, tries=3):
    """Compile; if the verifier rejects, re-decode (a real, stochastic driver may
    differ each try). Returns (ir, errors)."""
    ir, errs = [], ["(no attempt)"]
    for _ in range(tries):
        ir = compile(nl, make_driver(), constrained=True)
        errs = verify(ir)
        if not errs:
            return ir, []
    return ir, errs


# ---------------- drivers (the swappable front-end model) ----------------
class ScriptedDriver:
    """Replays a target plan's choices - a deterministic stand-in for a real model
    (the FakeClient analog). Used by tests and the offline demo."""

    def __init__(self, plan):
        self._q, self._vals, self._i = [], {}, 0
        for st in plan:
            if st.get("cond"):
                self._q += [("start", "if"), ("ref", st["cond"][0]),
                            ("field", st["cond"][1]), ("tool", st["tool"])]
            else:
                self._q.append(("start", st["tool"]))
            for a, v in st["args"].items():
                self._vals[(st["tool"], a)] = v
        self._q.append(("start", "<end>"))

    def choose(self, nl, slot, options, ctx):
        _, want = self._q[self._i]
        self._i += 1
        if want not in options:
            raise AssertionError("scripted choice %r not legal at %s: %r" % (want, slot, options))
        return want

    def value(self, nl, tool, arg):
        return self._vals.get((tool, arg), '"?"')


class KeywordDriver(ScriptedDriver):
    """A tiny keyword parser that turns a simple sentence into a plan, then replays
    it. A toy - honest-toy quality, like nanomodel; a real model (LlamaDriver)
    understands language properly. Good enough to demo the pipeline end to end."""

    KW = {"get_weather": ["weather", "forecast", "raining", "rain"],
          "add_to_cart": ["cart", "buy", "add", "umbrella", "order"],
          "search":      ["search", "find", "look up", "top result"],
          "send_email":  ["email", "mail", "send"]}

    def __init__(self, nl):
        super().__init__(self._parse(nl))

    @classmethod
    def _parse(cls, nl):
        s = nl.lower()
        plan, first_id = [], None
        # up to two actions, in the order their keywords first appear
        acts = sorted((min((s.find(k) for k in ws if k in s), default=-1), tool)
                      for tool, ws in cls.KW.items())
        acts = [(pos, tool) for pos, tool in acts if pos >= 0]
        for idx, (pos, tool) in enumerate(acts[:2]):
            arg = TOOLS[tool]["args"][0]
            val = cls._value_for(tool, arg, nl)
            cond = None
            # a later action guarded by "if ... rain" hangs off the first result's .rain
            if idx == 1 and first_id and re.search(r"\bif\b|\bwhen\b", s) and "rain" in s:
                cond = [first_id, "rain"]
            plan.append({"tool": tool, "args": {arg: val}, "cond": cond})
            if idx == 0:
                first_id = "n1"
        return plan

    @staticmethod
    def _value_for(tool, arg, nl):
        if arg == "city":
            m = re.search(r"\bin\s+([A-Z][a-z]+)", nl) or re.search(r"\b([A-Z][a-z]+)\b", nl)
            return '"%s"' % (m.group(1) if m else "there")
        if arg == "item":
            m = re.search(r"\b(umbrella|umbrellas)\b", nl, re.I)
            return '"%s"' % (m.group(1).rstrip("s") if m else "item")
        if arg == "query":
            m = re.search(r"\bfor\s+(?:the\s+)?([a-z]+)", nl, re.I) or re.search(r"\b(umbrella\w*)\b", nl, re.I)
            return '"%s"' % (m.group(1) if m else "query")
        return '"me"'  # send_email 'to'


class AdversarialDriver:
    """Always prefers an illegal option when one is offered (used in tests to show
    that an UNCONSTRAINED decode can produce an invalid plan the verifier catches)."""

    def choose(self, nl, slot, options, ctx):
        for bad in ("teleport", "n_undef"):
            if bad in options:
                return bad
        return options[-1] if slot == "start" else options[0]

    def value(self, nl, tool, arg):
        return '"x"'


class LlamaDriver:
    """The real front-end: a local quantized GGUF model via llama-cpp-python. OPT-IN -
    not needed for CI. Scores each grammar-legal option with the model and takes the
    argmax, so the output is still constrained to the legal set. For full token-level
    constraint, generate with grammar.gbnf via llama.cpp's native GBNF support.

        drv = LlamaDriver("minicpm-1b-sft.Q4_K_M.gguf")
        ir = compile("get the weather in Paris and if raining add an umbrella", drv)
    """

    def __init__(self, model_path, **kw):
        from llama_cpp import Llama  # lazy: only imported on the real path
        kw.setdefault("verbose", False)
        self.llm = Llama(model_path=model_path, logits_all=False, **kw)

    def _score(self, nl, slot, option, ctx):
        prompt = ("Compile the request into tool calls.\nRequest: %s\nSlot: %s\nOption: %s\nGood?"
                  % (nl, slot, option))
        out = self.llm(prompt, max_tokens=1, logprobs=1, temperature=0.0)
        try:
            return out["choices"][0]["logprobs"]["token_logprobs"][0]
        except Exception:
            return 0.0

    def choose(self, nl, slot, options, ctx):
        return max(options, key=lambda o: self._score(nl, slot, o, ctx))

    def value(self, nl, tool, arg):
        out = self.llm("Request: %s\nValue for %s.%s (one quoted word):" % (nl, tool, arg),
                       max_tokens=6, temperature=0.0)
        text = out["choices"][0]["text"].strip().split()
        return '"%s"' % (re.sub(r'\W', "", text[0]) if text else "x")


# ---------------- the worked example + a demo ----------------
EXAMPLE = "get the weather in Paris, and if it is raining add an umbrella to my cart"
EXAMPLE_PLAN = [
    {"tool": "get_weather", "args": {"city": '"Paris"'}, "cond": None},
    {"tool": "add_to_cart", "args": {"item": '"umbrella"'}, "cond": ["n1", "rain"]},
]


def main():
    nl = sys.argv[1] if len(sys.argv) > 1 else EXAMPLE
    print("request: " + nl + "\n")

    ir = compile(nl, KeywordDriver(nl), constrained=True)
    print("compiled plan (IR):\n" + (render(ir) or "  (empty)") + "\n")
    errs = verify(ir)
    print("verify: " + ("compiles - a verified, runnable plan" if not errs else "COMPILE ERROR: " + errs[0]) + "\n")

    # the point: constrained decode is valid by construction; unconstrained can break.
    good = compile(EXAMPLE, ScriptedDriver(EXAMPLE_PLAN), constrained=True)
    bad = compile(EXAMPLE, AdversarialDriver(), constrained=False)
    print("with the grammar ON  (constrained): verify -> %s" % (verify(good) or "PASS"))
    print("with the grammar OFF (adversarial): verify -> %s" % (verify(bad) or "PASS"))


if __name__ == "__main__":
    main()
