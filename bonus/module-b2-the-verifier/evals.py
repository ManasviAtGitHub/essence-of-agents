#!/usr/bin/env python3
"""evals.py - the verifier. Bonus track / B2.

THE PATTERN: an agent is exactly as good as its verifier (course-1 M6). So build
the verifier FIRST, then let the agent loop against it (B1 stops on it, B3 climbs
it). This is the single highest-leverage skill in agentic work - whoever writes
the best verifier ships the best agent.

FOUR KINDS, composable:
  1. VERIFIABLE    a deterministic check (test, schema, keyword) - cheap, un-gameable
  2. LLM-JUDGE     a model scores an output against a RUBRIC - for fuzzy quality
  3. SELF-CONSIST  sample N times, majority-vote - reliability for ~free
  4. GATE          block a change if its score regressed vs a saved baseline (CI)

RUN
  python3 evals.py --dry-run             # keyless: FakeJudge; catches a planted regression
  ANTHROPIC_API_KEY=... python3 evals.py # real LLM-judge

MAKE IT YOURS (the 3 things you change):
  CASES    - your inputs + the deterministic check for each
  RUBRIC   - your quality bar for the LLM-judge
  system() - call YOUR agent/model instead of the demo one
Then wire gate() into CI so a regression fails the build.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from collections import Counter

# ---- the eval set: inputs + a deterministic check each (MAKE IT YOURS) --------
CASES = [
    {"q": "What is the capital of France?",        "must_include": "paris"},
    {"q": "What is 2+2?",                          "must_include": "4"},
    {"q": "Name the largest planet.",              "must_include": "jupiter"},
]
RUBRIC = "Score 0-10: is the answer correct, direct, and free of hedging or filler?"

# ---- 1. VERIFIABLE: a cheap, un-gameable check --------------------------------
def verifiable(answer, case):
    return 1.0 if case["must_include"].lower() in answer.lower() else 0.0

# ---- 2. LLM-JUDGE: a model scores against a rubric ----------------------------
def judge(q, answer, rubric, client):
    return client.score(q, answer, rubric)          # 0..1

# ---- 3. SELF-CONSISTENCY: sample N, take the majority -------------------------
def self_consistency(system, q, n):
    if n <= 1: return system(q)
    return Counter(system(q) for _ in range(n)).most_common(1)[0][0]

# ---- the suite: run every case, blend verifiable + judge ----------------------
def suite_score(system, client, samples=1, verbose=False):
    vs, js = [], []
    for c in CASES:
        ans = self_consistency(system, c["q"], samples)
        v = verifiable(ans, c); j = judge(c["q"], ans, RUBRIC, client)
        vs.append(v); js.append(j)
        if verbose: print(f"  {c['q'][:32]:32} -> {ans[:28]:28} verifiable={v:.0f} judge={j:.2f}")
    v_avg, j_avg = sum(vs)/len(vs), sum(js)/len(js)
    score = 0.6*v_avg + 0.4*j_avg               # verifiable weighted higher (it can't be gamed)
    return {"score": round(score, 3), "verifiable": round(v_avg, 3), "judge": round(j_avg, 3)}

# ---- 4. GATE: block a regression vs the saved baseline ------------------------
def gate(new, baseline_path, eps=0.02):
    if not os.path.exists(baseline_path):
        json.dump(new, open(baseline_path, "w")); return True, "no baseline yet - saved this as the baseline"
    base = json.load(open(baseline_path))
    if new["score"] < base["score"] - eps:
        return False, f"REGRESSION: {new['score']} < baseline {base['score']} - eps ({eps})"
    if new["score"] > base["score"] + eps:
        json.dump(new, open(baseline_path, "w")); return True, f"improved {base['score']} -> {new['score']} (baseline updated)"
    return True, f"held at ~{base['score']}"

# ---- clients: real LLM-judge (BYO-key) + a keyless FakeJudge ------------------
class RealJudge:
    def __init__(self, model="claude-sonnet-5"):
        import anthropic; self.a = anthropic.Anthropic(); self.model = model
    def score(self, q, answer, rubric):
        r = self.a.messages.create(model=self.model, max_tokens=16,
            messages=[{"role": "user", "content": f"{rubric}\n\nQ: {q}\nANSWER: {answer}\n\nReply with ONLY an integer 0-10."}])
        m = re.search(r"\d+", r.content[0].text); return (min(10, int(m.group()))/10) if m else 0.0

class FakeJudge:
    """Deterministic stand-in so the whole eval + gate runs keyless in CI:
    rewards a short, direct answer; penalizes hedging/filler."""
    def score(self, q, answer, rubric):
        s = 0.9 if len(answer) < 40 else 0.6
        if any(w in answer.lower() for w in ("i think", "maybe", "as an ai", "it depends")): s -= 0.4
        return round(max(0.0, s), 2)

# ---- the demo: a good system, a regressed one, an improved one ---------------
GOOD  = {"What is the capital of France?": "Paris.", "What is 2+2?": "4.", "Name the largest planet.": "Jupiter."}
REGR  = {"What is the capital of France?": "I think maybe Paris?", "What is 2+2?": "4", "Name the largest planet.": "The Sun, as an AI I'm not sure."}
IMPR  = {**GOOD, "Name the largest planet.": "Jupiter - by far the most massive."}

def main():
    ap = argparse.ArgumentParser(description="the verifier: build it first, gate on it")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--baseline", default=None)
    a = ap.parse_args()
    if not a.dry_run and not os.environ.get("ANTHROPIC_API_KEY"): sys.exit("set ANTHROPIC_API_KEY or use --dry-run")
    client = FakeJudge() if a.dry_run else RealJudge()
    baseline = a.baseline or os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.json")
    if os.path.exists(baseline) and a.dry_run: os.remove(baseline)   # clean demo each run

    print("1) score the good system (and save it as the baseline):")
    good = suite_score(lambda q: GOOD[q], client, verbose=True); print("   ", good)
    ok, why = gate(good, baseline); print(f"   gate: {'PASS' if ok else 'BLOCK'} - {why}\n")

    print("2) a change ships that regressed quality:")
    regr = suite_score(lambda q: REGR[q], client, verbose=True); print("   ", regr)
    caught, why = gate(regr, baseline); caught = not caught   # the gate SHOULD block this
    print(f"   gate: {'BLOCK' if caught else 'PASS'} - {why}\n")

    print("3) a change that improved it:")
    impr = suite_score(lambda q: IMPR[q], client, verbose=True); print("   ", impr)
    ok, why = gate(impr, baseline); print(f"   gate: {'PASS' if ok else 'BLOCK'} - {why}")

    if a.dry_run and os.path.exists(baseline): os.remove(baseline)
    verdict = caught and ok      # regression blocked AND improvement allowed
    print("\nThe gate caught the regression and let the improvement through -", "that is the whole job." if verdict else "(SELF-TEST FAILED)")
    sys.exit(0 if verdict else 1)   # a self-test of the verifier: exit!=0 if it misjudged

if __name__ == "__main__":
    main()
