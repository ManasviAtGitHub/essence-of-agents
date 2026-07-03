"""CI eval-gate -- block deploys that regress the eval set (Module 10, productionized).

Runs a deterministic eval (a classifier over a fixed dataset, so it needs no key and is
reproducible) and exits non-zero if the pass-rate drops below the baseline. Wire it into
CI (see .github/workflows/ci.yml). In a real system the candidate is your agent over a
real eval set scored by exact-match / tests / an LLM-judge -- the gate logic is identical.

    python production/eval_gate.py
"""
import re
import sys

DATASET = [
    ("this product is great, i love it", "positive"),
    ("terrible experience, would not recommend", "negative"),
    ("it works as described", "neutral"),
    ("absolutely fantastic and wonderful", "positive"),
    ("broken on arrival, awful", "negative"),
    ("the package arrived on tuesday", "neutral"),
]
POSITIVE = {"great", "love", "fantastic", "wonderful", "excellent", "amazing", "good"}
NEGATIVE = {"terrible", "awful", "broken", "bad", "worst", "hate", "horrible"}
BASELINE = 1.0  # the current candidate classifies the whole set correctly


def classify(text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    if words & POSITIVE:
        return "positive"
    if words & NEGATIVE:
        return "negative"
    return "neutral"


def run_eval() -> float:
    hits = sum(classify(t) == label for t, label in DATASET)
    return hits / len(DATASET)


def main():
    rate = run_eval()
    print(f"eval pass-rate: {rate:.1%}  (baseline {BASELINE:.1%})")
    if rate + 1e-9 < BASELINE:
        print("REGRESSION -- blocking the deploy.")
        sys.exit(1)
    print("OK -- no regression.")
    sys.exit(0)


if __name__ == "__main__":
    main()
