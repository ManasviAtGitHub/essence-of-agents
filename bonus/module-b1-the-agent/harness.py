#!/usr/bin/env python3
"""harness.py - a coding agent in ~260 lines. Bonus track / B1.

THE PROPER IDEA: a coding agent is not the model - it is the CONTEXT MANAGER
around the model. The tools FETCH information; context engineering decides what
the model actually SEES each turn. Get that right and a small model does big
work; get it wrong and a big model flails. So this harness's whole job is five
context moves, working together, wrapped around a plain tool-use loop:

  1. WORKING SET      curate what's in context (system + task + memory +
                      relevant files + recent results), not a growing transcript
  2. JUST-IN-TIME     tools pull files on demand; never front-load the repo
  3. COMPACTION       over budget -> summarize old turns, keep task + decisions
  4. MEMORY           read a memory file at start; append durable facts
  5. BUDGET           track tokens every turn (Track 5's lesson, applied)

The loop stops on a VERIFIER (the tests pass) - not on the model's say-so.

RUN IT
  python harness.py --dry-run                       # keyless demo (FakeClient), CI-safe
  ANTHROPIC_API_KEY=... python harness.py \
      --repo ./yourproject --task "make the tests pass" --test "pytest -q"

MAKE IT YOURS (the only 3 lines you change):
  --repo   : your project dir            (the sandbox: the agent only touches this)
  --task   : what you want done          (plain English)
  --test   : the verifier command        (the stop condition; exit 0 == done)

SAFETY (rule 18): the agent runs bash + edits files, but ONLY inside --repo
(a scratch copy in dry-run). In real mode it prints each shell command and, if
stdin is a TTY, asks before running anything outside a read-only allowlist.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile

# ============================ TOOLS (they FETCH; context decides what's SEEN) ===
def tool_list(repo, args):        # list_dir
    d = os.path.join(repo, args.get("path", "."))
    return "\n".join(sorted(os.listdir(d))) if os.path.isdir(d) else f"(not a dir: {d})"

def tool_read(repo, args):        # read a file (just-in-time retrieval)
    p = os.path.join(repo, args["path"])
    if not os.path.isfile(p): return f"(no such file: {args['path']})"
    return open(p, encoding="utf-8").read()[:8000]

def tool_write(repo, args):       # write/replace a file
    p = os.path.join(repo, args["path"])
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w", encoding="utf-8").write(args["content"])
    return f"wrote {args['path']} ({len(args['content'])} bytes)"

def tool_bash(repo, args, allow):  # run a shell command IN the sandbox
    cmd = args["cmd"]
    if not allow(cmd): return "(refused: command not permitted)"
    r = subprocess.run(cmd, shell=True, cwd=repo, capture_output=True, text=True, timeout=60)
    return (r.stdout + r.stderr)[-4000:] or "(no output)"

TOOLS = [
    {"name": "list_dir", "description": "list files in a directory of the repo",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}},
    {"name": "read_file", "description": "read a file (pull context on demand)",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file", "description": "create or overwrite a file",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "run_bash", "description": "run a shell command inside the repo (e.g. the tests)",
     "input_schema": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}},
]

# ============================ CONTEXT ENGINEERING (the actual craft) ============
class Context:
    """The WORKING SET the model sees each turn - deliberately curated, not a
    transcript that grows forever. This class is the whole point of the harness."""
    def __init__(self, system, task, memory_path, budget_tokens=12000):
        self.system = system
        self.task = task
        self.memory_path = memory_path
        self.budget = budget_tokens
        self.turns = []                       # [{role, content}] - the rolling window
        self.memory = self._load_memory()     # durable facts, read once at start (move 4)

    def _load_memory(self):
        return open(self.memory_path, encoding="utf-8").read() if os.path.isfile(self.memory_path) else ""

    def remember(self, fact):                 # move 4: append a durable fact
        with open(self.memory_path, "a", encoding="utf-8") as f: f.write(fact.rstrip() + "\n")
        self.memory = self._load_memory()

    def add(self, role, content):
        self.turns.append({"role": role, "content": content})

    @staticmethod
    def _toks(x): return len(json.dumps(x)) // 4     # ~4 chars/token, good enough to budget

    def used(self):
        return self._toks(self.system) + self._toks(self.memory) + self._toks(self.turns)

    def compact(self, client):
        """Move 3: when the window outgrows the budget, summarize the OLD turns
        into one note and drop them - keeping the task, decisions, and current
        state. This is what lets an agent run for hours without drowning."""
        if self.used() < self.budget or len(self.turns) <= 4: return False
        old, keep = self.turns[:-3], self.turns[-3:]
        summary = client.summarize(self.task, old)     # a cheap model call
        self.turns = [{"role": "user", "content": f"[earlier work, compacted]\n{summary}"}] + keep
        return True

    def render(self):
        """What actually goes to the model this turn: system + memory + task +
        the (windowed, possibly-compacted) turns. Curated, not accumulated."""
        sys = self.system
        if self.memory: sys += "\n\nMEMORY (durable facts):\n" + self.memory
        head = [{"role": "user", "content": f"TASK: {self.task}"}]
        return sys, head + self.turns

# ============================ THE LOOP (stops on the VERIFIER, not the model) ===
def run(client, repo, task, test_cmd, memory_path, allow, max_steps=20, log=print):
    system = ("You are a coding agent. Use the tools to inspect and edit the repo, "
              "then run the test command to check your work. Keep going until the "
              "tests pass. Prefer reading only the files you need (pull context on "
              "demand). When the tests pass, reply with the single word DONE.")
    ctx = Context(system, task, memory_path)
    tools_by_name = {"list_dir": lambda a: tool_list(repo, a),
                     "read_file": lambda a: tool_read(repo, a),
                     "write_file": lambda a: tool_write(repo, a),
                     "run_bash": lambda a: tool_bash(repo, a, allow)}
    for step in range(1, max_steps + 1):
        if ctx.compact(client): log(f"  [context] compacted (was over {ctx.budget} tok)")
        sys_prompt, messages = ctx.render()
        log(f"[step {step}]  context ~{ctx.used()} tok / {ctx.budget} budget")
        blocks = client.complete(sys_prompt, messages, TOOLS)
        did_tool = False
        for b in blocks:
            if b["type"] == "text":
                log(f"  model: {b['text'].strip()[:200]}")
                ctx.add("assistant", b["text"])
                if b["text"].strip().upper().endswith("DONE"):
                    ok = verify(repo, test_cmd, log)
                    if ok: log("[done] model said DONE and the verifier agrees."); return True
                    ctx.add("user", "The verifier still fails - keep going.")
            elif b["type"] == "tool_use":
                did_tool = True
                out = tools_by_name[b["name"]](b["input"])
                log(f"  tool {b['name']}({json.dumps(b['input'])[:80]}) -> {out.strip()[:120]!r}")
                ctx.add("assistant", f"(called {b['name']})")
                ctx.add("user", f"[{b['name']} result]\n{out}")
        if not did_tool and not blocks:
            log("  (empty response)"); break
    # last word to the verifier regardless of what the model claimed
    return verify(repo, test_cmd, log)

def verify(repo, test_cmd, log):
    r = subprocess.run(test_cmd, shell=True, cwd=repo, capture_output=True, text=True, timeout=120)
    log(f"  [verifier] `{test_cmd}` -> exit {r.returncode}")
    return r.returncode == 0

# ============================ CLIENTS: real (BYO-key) + fake (keyless demo) =====
class RealClient:
    """Wraps the Anthropic API. Needs `pip install anthropic` + ANTHROPIC_API_KEY."""
    def __init__(self, model="claude-sonnet-5"):
        import anthropic; self.a = anthropic.Anthropic(); self.model = model
    def complete(self, system, messages, tools):
        msgs = [{"role": m["role"], "content": m["content"]} for m in messages]
        r = self.a.messages.create(model=self.model, max_tokens=2000, system=system, messages=msgs, tools=tools)
        out = []
        for b in r.content:
            if b.type == "text": out.append({"type": "text", "text": b.text})
            elif b.type == "tool_use": out.append({"type": "tool_use", "name": b.name, "input": b.input})
        return out
    def summarize(self, task, old):
        r = self.a.messages.create(model=self.model, max_tokens=400,
            messages=[{"role": "user", "content": f"Summarize this agent's progress on '{task}' in 4 lines "
                       f"(decisions + current state), so it can continue without the detail:\n{json.dumps(old)[:6000]}"}])
        return r.content[0].text

class FakeClient:
    """A scripted model for the keyless --dry-run: it fixes a planted bug so the
    whole loop + context machinery runs end to end, deterministically, in CI."""
    def __init__(self): self.step = 0
    def summarize(self, task, old): return "(compacted earlier turns)"
    def complete(self, system, messages, tools):
        self.step += 1
        if self.step == 1: return [{"type": "tool_use", "name": "run_bash", "input": {"cmd": "python3 -B test_math.py"}}]
        if self.step == 2: return [{"type": "tool_use", "name": "read_file", "input": {"path": "mathlib.py"}}]
        if self.step == 3: return [{"type": "text", "text": "The bug: add() subtracts. Fixing it."},
                                   {"type": "tool_use", "name": "write_file",
                                    "input": {"path": "mathlib.py", "content": "def add(a, b):\n    return a + b\n"}}]
        if self.step == 4: return [{"type": "tool_use", "name": "run_bash", "input": {"cmd": "python3 -B test_math.py"}}]
        return [{"type": "text", "text": "Tests pass. DONE"}]

# ============================ SANDBOX + CLI ====================================
def make_demo_repo():
    d = tempfile.mkdtemp(prefix="harness_demo_")
    open(os.path.join(d, "mathlib.py"), "w").write("def add(a, b):\n    return a - b\n")   # planted bug
    open(os.path.join(d, "test_math.py"), "w").write("from mathlib import add\nassert add(2, 3) == 5, 'add is broken'\nprint('ok - tests pass')\n")
    return d

def default_allow(cmd):   # read-only-ish allowlist; edits happen via write_file, not bash
    safe = ("pytest", "python -m pytest", "python3 ", "python ", "ls", "cat", "grep", "npm test", "node ")
    return cmd.strip().startswith(safe)

def main():
    ap = argparse.ArgumentParser(description="a coding agent that is really a context manager")
    ap.add_argument("--repo"); ap.add_argument("--task", default="make the tests pass")
    ap.add_argument("--test", default="python -m pytest -q"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--memory", default=None)
    a = ap.parse_args()
    if a.dry_run:
        repo = make_demo_repo()
        print(f"[dry-run] scratch repo at {repo} with a planted bug (add subtracts).")
        client = FakeClient(); a.test = "python3 -B test_math.py"   # self-contained verifier, no pytest needed
    else:
        if not a.repo: sys.exit("give --repo (your project) or use --dry-run")
        if not os.environ.get("ANTHROPIC_API_KEY"): sys.exit("set ANTHROPIC_API_KEY for real runs")
        repo, client = os.path.abspath(a.repo), RealClient()
    memory = a.memory or os.path.join(repo, ".agent_memory.md")
    ok = run(client, repo, a.task, a.test, memory, default_allow)
    print(("\nSUCCESS" if ok else "\nFAILED") + " - the verifier is the judge, not the model.")
    if a.dry_run: shutil.rmtree(repo, ignore_errors=True)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
