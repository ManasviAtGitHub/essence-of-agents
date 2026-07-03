"""Run the agent loop with NO API key and NO network, via a scripted FakeClient.

The "model" is faked, but the calculate TOOL really runs - so you watch a genuine
tool execution flow through the real loop.

    python -m claude_harness.examples.offline_demo
"""
from claude_harness import Agent, Trace
from claude_harness.builtins import calculate
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block

# Script: the "model" first asks for the calculator, then gives a final answer.
client = FakeClient(
    [
        reply(tool_use_block("calculate", {"expression": "2**100"}, id="c1")),
        reply(text_block("2**100 is 1267650600228229401496703205376.")),
    ]
)

agent = Agent(tools=[calculate], client=client)
trace = Trace(id="offline-demo")
answer = agent.run("What is 2 to the 100th power? Use the calculator.", trace=trace)

print("ANSWER:", answer)
print("\nTRACE:")
for e in trace.events:
    print(f"  [{e['t_ms']:>4}ms] {e['kind']}: {e['data']}")
