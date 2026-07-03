"""Module 8 -- supervisor fan-out, built on the harness (keyless).

Each worker is a real Agent with its OWN context (its own FakeClient) -- that is the
context isolation multi-agent buys. Generation is scripted so it runs with no key.

    python agentic-course/module-08-multi-agent/fanout_offline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import Agent
from claude_harness.testing import FakeClient, reply, text_block


def worker(subtask, finding):
    """A specialist agent with its own clean context."""
    agent = Agent(client=FakeClient([reply(text_block(finding))]))
    return agent.run(subtask)


# Parallel, isolatable task -> fan out. Each worker sees only its own file.
subtasks = ["audit auth.py", "audit db.py", "audit api.py"]
findings = [worker(s, f"{s}: 0 critical issues") for s in subtasks]
for f in findings:
    print("  worker:", f)

supervisor = Agent(client=FakeClient([reply(text_block("3 files audited in parallel, 0 critical issues."))]))
print("\n  supervisor:", supervisor.run("Synthesize the workers' findings."))

print("\nEach worker had its own clean context (isolation). Here they run one after")
print("another; in production you'd run them concurrently (parallelism).")
print("For a single sequential bug, skip all this -- one focused agent wins; the team is")
print("pure coordination tax. Match the team shape to the task shape.")
