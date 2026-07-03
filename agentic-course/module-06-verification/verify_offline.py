"""The verifier loop, keyless - generation is faked, but the VERIFIER really runs.

A scripted "model" proposes a buggy implementation, then (after seeing the failure) a
fixed one. The verifier executes each candidate against real tests. Generation is the
cheap part; the verifier is the leverage.

    python agentic-course/module-06-verification/verify_offline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import Agent
from claude_harness.testing import FakeClient, reply, text_block

# What the "model" produces: attempt 1 is buggy, attempt 2 is fixed.
ATTEMPTS = [
    "def is_palindrome(s):\n    return s == s[::-1]",
    "def is_palindrome(s):\n    t = ''.join(c.lower() for c in s if c.isalnum())\n    return t == t[::-1]",
]
TESTS = [("Race car", True), ("hello", False), ("RaceCar", True)]


def verify(code):
    """Run the candidate against the tests. Returns None on success, else the failure.
    (exec is fine here - the code is our own trusted teaching string, run locally.)"""
    ns = {}
    exec(code, ns)
    f = ns["is_palindrome"]
    for s, expected in TESTS:
        got = f(s)
        if got != expected:
            return f"is_palindrome({s!r}) -> {got}, expected {expected}"
    return None


client = FakeClient([reply(text_block(ATTEMPTS[0])), reply(text_block(ATTEMPTS[1]))])
agent = Agent(client=client)

for attempt in range(1, 3):
    code = agent.run("Write is_palindrome(s), ignoring case/spaces/punctuation.")
    print(f"--- attempt {attempt} ---\n{code}")
    failure = verify(code)
    if failure is None:
        print("VERIFIER: all tests pass  [ok]\n")
        break
    print(f"VERIFIER: FAIL - {failure}\n")

print("The writer barely changed between attempts. The verifier is what made it correct.")
