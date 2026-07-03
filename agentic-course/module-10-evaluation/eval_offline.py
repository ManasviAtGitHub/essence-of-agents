"""A tiny eval harness, keyless. Run two prompt "versions" over a dataset and score
them - the version that *felt* like an improvement regresses.

Agent outputs are scripted (FakeClient) so it runs with no key; the harness + checker
are real. Swap in a real model and these become genuine evals.

    python agentic-course/module-10-evaluation/eval_offline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import Agent
from claude_harness.testing import FakeClient, reply, text_block

# (input, expected) - a small eval set.
DATASET = [("q1", "A"), ("q2", "B"), ("q3", "C"), ("q4", "D")]

def run_version(outputs):
    client = FakeClient([reply(text_block(o)) for o in outputs])
    agent = Agent(client=client)
    return [agent.run(inp) for inp, _ in DATASET]


def score(outs):
    return sum(o == exp for o, (_, exp) in zip(outs, DATASET))


# v1 gets q1-q3 right, misses q4.  v2 "improves" q4 but breaks q3 AND q1.
V1 = ["A", "B", "C", "x"]   # 3/4
V2 = ["x", "B", "x", "D"]   # 2/4 - fixed q4, broke q1 and q3

v1_out, v2_out = run_version(V1), run_version(V2)
n = len(DATASET)
print(f"v1 (baseline):     {score(v1_out)}/{n}")
print(f"v2 ('improvement'): {score(v2_out)}/{n}")
print()
print("v2 felt cleaner and fixed q4 - but the eval shows it regressed overall.")
print("Vibes said better; the measurement said worse. That's why you eval before you ship.")
