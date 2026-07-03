"""The harness reads its own source and explains itself - then saves the trace.

Run from the repo root:

    python -m claude_harness.examples.self_explain
"""
from claude_harness import Agent, Trace
from claude_harness.builtins import read_file

agent = Agent(tools=[read_file])
trace = Trace(id="self-explain")

answer = agent.run(
    "Read your own harness source at claude_harness/agent.py and explain, "
    "in two sentences, how the agent loop works.",
    trace=trace,
)

print(answer)
trace.save("self-explain.trace.json")
print("\n(trace saved to self-explain.trace.json)")
