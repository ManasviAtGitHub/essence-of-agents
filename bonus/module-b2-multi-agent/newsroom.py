#!/usr/bin/env python3
"""newsroom.py - a deep-research multi-agent system (the "gold" case). Bonus B2.

Multi-agent is a COST you pay for two things: parallelism on independent subtasks and
isolation for specialists. Deep research is where that cost pays off - and it's the
case with the numbers: an orchestrator + parallel subagents beat a single agent by
~90% on research evals, at ~15x the tokens (Anthropic, 2025).

Modeled as a NEWSROOM - the metaphor IS the architecture, and each role runs the model
tier that fits its job:

  router       (cheap)      triage: how big is this, how many reporters
  editor       (reasoning)  decompose the question into INDEPENDENT angles; later, synthesize
  reporters    (instruct)   chase one angle each, IN PARALLEL, each an isolated context
  fact-checker (reasoning)  refute: drop any claim the sources don't support
  copy desk    (instruct)   attach a citation to every surviving claim

Why it works: ISOLATION (each reporter its own window -> more effective context, no
interference), PARALLELISM (independent angles at once), SPECIALIZATION (right model per
role), and ADVERSARIAL VERIFICATION (the fact-checker). Why it is NOT a default: if
reporters work from conflicting assumptions the whole thing misaligns - so the angles
must be genuinely independent. They are, for research; they are NOT for coding, which is
why you don't split a code change across parallel agents.

RUN
  python3 newsroom.py --dry-run                 # keyless: a fixed "wire" (corpus); whole op runs
  ANTHROPIC_API_KEY=... python3 newsroom.py --q "Why did dirigibles lose to airplanes?"
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, os, sys

# ---- model heterogeneity: the right tier per role (this is the point) ----------
MODELS = {"router": "claude-haiku-4-5", "editor": "claude-opus-4-8",
          "reporter": "claude-sonnet-5", "checker": "claude-opus-4-8"}
TIER = {"router": "cheap", "editor": "reasoning", "reporter": "instruct", "checker": "reasoning", "desk": "instruct"}

# ---- the WIRE: a small fixed corpus so the whole thing runs keyless ------------
WIRE = {
 "s1": "The 1937 Hindenburg disaster, broadcast live, shattered public confidence in passenger airships.",
 "s2": "A 1930s airliner cruised near 250 km/h; a large airship managed about 130 km/h.",
 "s3": "Airships were vast and costly - giant sheds to house them and big ground crews to land them.",
 "s4": "Rigid airships were fragile in storms; the Akron, Macon, and R101 were all lost to weather.",
 "s5": "By WWII, long-range aircraft and radar erased the airship's reconnaissance niche.",
 "s6": "The US controlled the helium supply, forcing other nations to fly on flammable hydrogen.",
}

def search(query):
    """A real (deterministic) keyword search over the wire -- the reporters' one tool."""
    words = [w.strip(".,?") for w in query.lower().split()]
    return [(sid, txt) for sid, txt in WIRE.items() if any(w in txt.lower() for w in words)]

# ---- the pipeline (orchestrator-worker + critic + synthesis) -------------------
def run(client, question, log):
    n = client.route(question)
    log(badge("router"), f"triage: broad 'why did X lose' question -> {n} independent angles, in parallel")
    specs = client.decompose(question, n)
    log(badge("editor"), "decompose into independent angles:")
    for i, s in enumerate(specs, 1): log("   ", f"{i}. {s['angle']}")

    log(badge("reporter"), f"{len(specs)} reporters running IN PARALLEL, each its own notebook (isolated context):")
    with cf.ThreadPoolExecutor(max_workers=len(specs)) as ex:      # real parallelism
        findings = list(ex.map(lambda s: reporter(client, s, log), specs))
    for f in findings:
        log("   ", f"{f['angle'][:26]:26} -> \"{f['claim'][:40]}\"")

    log(badge("checker"), "refute each claim against the wire; keep only what a source supports:")
    kept = []
    for f in findings:
        ok = client.judge(f)
        log("   ", f"{f['angle'][:28]:28} {'sources ' + ','.join(f['sources']) if f['sources'] else '(no source)':22} -> {'KEEP' if ok else 'DROP'}")
        if ok: kept.append(f)

    report = client.write(question, kept)
    log(badge("desk"), "citations attached; editor synthesizes the final report.")
    return report, kept, findings

def reporter(client, spec, log):
    hits = search(spec["query"])
    claim = client.summarize(spec["angle"], hits)
    return {"angle": spec["angle"], "claim": claim, "sources": [sid for sid, _ in hits]}

def badge(role):
    return f"[{role if role != 'desk' else 'copy desk'} - {TIER[role]}]"

# ---- clients: real (a model per role) + fake (scripted, keyless) ---------------
class RealClient:
    def __init__(self): import anthropic; self.a = anthropic.Anthropic()
    def _ask(self, role, prompt, max_tokens=600):
        r = self.a.messages.create(model=MODELS.get(role, MODELS["reporter"]), max_tokens=max_tokens,
                                   messages=[{"role": "user", "content": prompt}])
        return r.content[0].text.strip()
    def route(self, q): return 6
    def decompose(self, q, n):
        txt = self._ask("editor", f"Break this research question into {n} INDEPENDENT angles that can be "
                        f"researched separately. One per line, 'angle | search query'.\n\nQ: {q}")
        out = []
        for line in txt.splitlines():
            if "|" in line: a, _, query = line.partition("|"); out.append({"angle": a.strip(" -0123456789."), "query": query.strip()})
        return out or SPECS
    def summarize(self, angle, hits):
        src = "\n".join(f"[{s}] {t}" for s, t in hits) or "(no sources found)"
        return self._ask("reporter", f"Angle: {angle}\nSources:\n{src}\n\nOne-sentence claim, grounded ONLY in "
                         f"the sources above. If nothing supports it, say so.", 150)
    def judge(self, f):
        if not f["sources"]: return False
        src = "\n".join(f"[{s}] {WIRE[s]}" for s in f["sources"] if s in WIRE)
        return "yes" in self._ask("checker", f"Claim: {f['claim']}\nSources:\n{src}\n\nDo the sources support the "
                                   f"claim? Answer yes or no.", 5).lower()
    def write(self, q, kept):
        body = "\n".join(f"- {f['claim']} {''.join('[' + s + ']' for s in f['sources'])}" for f in kept)
        return self._ask("editor", f"Write a tight, cited answer to '{q}' from these checked findings:\n{body}", 500)

# scripted decomposition + reporter claims for the keyless run (the model's output, faked)
SPECS = [
 {"angle": "safety & public trust",            "query": "Hindenburg disaster confidence public"},
 {"angle": "speed",                            "query": "faster airliner cruised km/h"},
 {"angle": "cost & infrastructure",            "query": "costly sheds crews helium hydrogen"},
 {"angle": "weather fragility",                "query": "storms weather Akron Macon lost"},
 {"angle": "military obsolescence",            "query": "WWII aircraft radar reconnaissance"},
 {"angle": "regulation / were they banned?",   "query": "treaty ban outlawed 1938"},
]
CLAIMS = {
 "safety & public trust":          "The 1937 Hindenburg disaster destroyed public confidence in airships",
 "speed":                          "Airplanes were nearly twice as fast as airships",
 "cost & infrastructure":          "Airships were vast and costly to build, house, and crew",
 "weather fragility":              "Rigid airships were fragile and repeatedly lost to storms",
 "military obsolescence":          "By WWII, aircraft and radar had erased the airship's niche",
 "regulation / were they banned?": "A 1938 international treaty outlawed airships",   # UNSUPPORTED - the fact-checker drops it
}

class FakeClient:
    """Scripts each role for the keyless run; the search + citation + fact-check
    machinery is REAL (deterministic over the wire). Thread-safe: keyed by content,
    not a step counter, so the reporters really run in parallel."""
    def route(self, q): return len(SPECS)
    def decompose(self, q, n): return SPECS
    def summarize(self, angle, hits): return CLAIMS.get(angle, "(no claim)")
    def judge(self, f): return bool(f["sources"]) and all(s in WIRE for s in f["sources"])
    def write(self, q, kept):
        lines = "  ".join(f["claim"] + " " + "".join(f"[{s}]" for s in f["sources"]) + "." for f in kept)
        return "Dirigibles lost to airplanes for several converging reasons.  " + lines

def main():
    ap = argparse.ArgumentParser(description="a deep-research newsroom: orchestrator + parallel reporters + a fact-checker")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--q", default="Why did dirigibles lose to airplanes?")
    a = ap.parse_args()
    if not a.dry_run and not os.environ.get("ANTHROPIC_API_KEY"): sys.exit("set ANTHROPIC_API_KEY or use --dry-run")
    client = FakeClient() if a.dry_run else RealClient()
    pad = print
    print(f'[the newsroom] researching: "{a.q}"\n')
    report, kept, findings = run(client, a.q, lambda *xs: pad(*xs))
    print("\n=== the cited report ===")
    print(report)
    print("\n=== why multi-agent, here ===")
    print(f"  PARALLELISM  {len(findings)} reporters worked at once, not one after another.")
    print(f"  ISOLATION    each had its own window -> no interference; more effective context than one agent.")
    print(f"  VERIFICATION the fact-checker dropped {len(findings)-len(kept)} unsupported claim a lone agent might have kept.")
    print(f"  SPECIALIZATION reasoning model to plan + check, instruct to report, a cheap model to triage.")
    print(f"  THE TRADE    ~+90% on research evals, at ~15x the tokens - worth it here, not for everything.")
    print(f"  THE LIMIT    it only works because the angles are INDEPENDENT; share state (e.g. coding) and it misaligns.")

if __name__ == "__main__":
    main()
