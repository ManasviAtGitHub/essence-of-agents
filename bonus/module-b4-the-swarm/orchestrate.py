#!/usr/bin/env python3
"""orchestrate.py - the swarm. Bonus track / B4.

THE PATTERN: for hard judgment ("is this code correct? is this finding real?") one
agent is a coin-flip. A swarm isn't "more agents" - it's two moves that trade
breadth for precision:

  1. FAN-OUT      N reviewers, each a DIFFERENT lens (correctness / security / perf).
                  Breadth: each lens sees what the others are blind to. Union +dedup.
  2. ADVERSARIAL  every candidate finding faces K skeptics whose job is to REFUTE it
     VERIFY       against the code. Keep it only if the skeptics can't (majority
                  vote). Precision: this is what kills plausible-but-wrong findings.

Fan-out alone is a pile of maybes; adversarial-verify alone has nothing to check.
Together: high recall, then high precision. (This is exactly the review pattern used
to build this course - 8 agents fanned across modules, each finding verified against
the code before any fix.)

RUN
  python3 orchestrate.py --dry-run              # keyless: scripted swarm reviews a buggy snippet
  ANTHROPIC_API_KEY=... python3 orchestrate.py  # real parallel model calls

MAKE IT YOURS:
  LENSES    - the angles to fan out over (your review dimensions)
  TARGET    - what you're judging (a diff, a doc, an answer)
  k (below) - how many skeptics must fail to refute for a finding to survive
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, json, os, re, sys

LENSES = ["correctness", "security", "performance"]

TARGET = '''\
def take(items, n):
    # return the first n items, cheapest first
    items = sorted(items, key=lambda x: x["price"])
    out = []
    for i in range(n + 1):        # <-- off-by-one: yields n+1 items
        out.append(items[i])      # <-- IndexError when n >= len(items)
    return out
'''

# ============================ move 1: FAN-OUT across lenses =====================
def fan_out(target, lenses, client):
    """Each lens reviews independently (in parallel for the real client). Returns
    the union of candidate findings - high recall, unverified."""
    with cf.ThreadPoolExecutor(max_workers=len(lenses)) as ex:
        batches = list(ex.map(lambda L: client.review(target, L), lenses))
    findings, seen = [], set()
    for batch in batches:
        for f in batch:
            key = f["claim"][:40].lower()
            if key not in seen: seen.add(key); findings.append(f)   # dedup
    return findings

# ============================ move 2: ADVERSARIAL VERIFY (K skeptics vote) ======
def verify(target, finding, client, k=3):
    """K independent skeptics each TRY TO REFUTE the finding against the code.
    Survive only if a majority fail to refute. Precision move + a consensus vote
    folded into one."""
    with cf.ThreadPoolExecutor(max_workers=k) as ex:
        verdicts = list(ex.map(lambda i: client.refute(target, finding, i), range(k)))
    refuted = sum(1 for v in verdicts if v["refuted"])
    return refuted < (k + 1) // 2, refuted, verdicts   # survives if refuters are a minority

def swarm(target, client, k=3, log=print):
    log(f"FAN-OUT over {len(LENSES)} lenses...")
    candidates = fan_out(target, LENSES, client)
    log(f"  {len(candidates)} candidate findings (union, deduped)\n")
    log(f"ADVERSARIAL VERIFY (each faces {k} skeptics)...")
    survivors = []
    for f in candidates:
        ok, refuted, _ = verify(target, f, client, k)
        log(f"  [{f['lens']:11}] {f['claim'][:46]:46} {refuted}/{k} refute -> {'SURVIVES' if ok else 'killed'}")
        if ok: survivors.append(f)
    survivors.sort(key=lambda f: -{"high": 3, "med": 2, "low": 1}.get(f["severity"], 0))
    return survivors

# ============================ clients: real (parallel) + fake (keyless) =========
class RealClient:
    def __init__(self, model="claude-sonnet-5"):
        import anthropic; self.a = anthropic.Anthropic(); self.model = model
    def _json(self, prompt, max_tokens=400):
        r = self.a.messages.create(model=self.model, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}])
        m = re.search(r"[\[{].*[\]}]", r.content[0].text, re.S); return json.loads(m.group()) if m else {}
    def review(self, target, lens):
        got = self._json(f"Review this code through the {lens} lens ONLY. Return a JSON list of findings, "
            f'each {{"claim": str, "severity": "high|med|low"}}. Be specific; [] if none.\n\n{target}')
        return [{"lens": lens, "claim": g["claim"], "severity": g.get("severity", "low")} for g in (got or [])]
    def refute(self, target, finding, i):
        v = self._json(f'A reviewer claims: "{finding["claim"]}". Try to REFUTE it against this code. '
            f'Return {{"refuted": true|false, "why": str}}. Refute if the claim is false, imagined, or not '
            f'supported by the code.\n\n{target}', max_tokens=200)
        return {"refuted": bool(v.get("refuted")), "why": v.get("why", "")}

class FakeClient:
    """Scripted swarm so the whole fan-out + verify runs keyless in CI. Two lenses
    surface real bugs; the rest surface plausible-but-wrong claims the skeptics
    then kill - so you can watch precision happen."""
    FIND = {
        "correctness": [{"claim": "off-by-one: range(n+1) yields n+1 items", "severity": "high"},
                        {"claim": "IndexError when n >= len(items)", "severity": "high"}],
        "security":    [{"claim": "no input validation on items (unvalidated dict access)", "severity": "low"}],
        "performance": [{"claim": "sorts the whole list to take n (O(m log m), could be O(m))", "severity": "med"},
                        {"claim": "recomputes price on every compare (imagined - it does not)", "severity": "med"}],
    }
    def review(self, target, lens):
        return [{"lens": lens, **f} for f in self.FIND.get(lens, [])]
    def refute(self, target, finding, i):
        # skeptics refute the claims that aren't actually in the code
        bogus = ("imagined" in finding["claim"]) or ("no input validation" in finding["claim"])
        return {"refuted": bogus, "why": "not supported by the code" if bogus else "confirmed against the code"}

def main():
    ap = argparse.ArgumentParser(description="a review swarm: fan-out for recall, adversarial-verify for precision")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("-k", type=int, default=3)
    a = ap.parse_args()
    if not a.dry_run and not os.environ.get("ANTHROPIC_API_KEY"): sys.exit("set ANTHROPIC_API_KEY or use --dry-run")
    client = FakeClient() if a.dry_run else RealClient()
    print("TARGET under review:\n" + "".join("  " + l + "\n" for l in TARGET.splitlines()))
    survivors = swarm(TARGET, client, k=a.k)
    print(f"\nCONFIRMED findings ({len(survivors)}, ranked by severity):")
    for f in survivors: print(f"  - [{f['severity']:4}] ({f['lens']}) {f['claim']}")
    print("\nFan-out found everything; the skeptics threw out what wasn't real -", "recall then precision.")

if __name__ == "__main__":
    main()
