"""Run the multi-tool agent offline (no key) with a scripted FakeClient.

The model's *decisions* are scripted here; the TOOLS really execute. With a key (or
the future Ollama adapter) the same agent runs for real - that's where you feel the
aha that the model, not us, chose the tools.

    python agentic-course/module-01-hands/offline_demo.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # so `import hands` works

from claude_harness import Trace
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block
from hands import build_agent

# Scripted "decisions": use calculate, then reverse, then answer. Two different tools
# in one run - the menu works, and the loop didn't change from Module 0.
client = FakeClient(
    [
        reply(tool_use_block("calculate", {"expression": "13*17"}, id="a")),
        reply(tool_use_block("reverse", {"text": "README.md"}, id="b")),
        reply(text_block("13 * 17 is 221, and 'README.md' reversed is 'dm.EMDAER'.")),
    ]
)

agent = build_agent(client=client)
trace = Trace(id="m1-offline")
print("ANSWER:", agent.run("Do some math and reverse a string.", trace=trace))
print("\nTRACE:")
for e in trace.events:
    print(f"  {e['kind']}: {e['data']}")
