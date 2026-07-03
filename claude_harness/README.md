# claude_harness

A small, reusable Claude agent harness: the agent loop, tools, and tracing. The
loop is written by hand on purpose - it's the thing the course teaches, and it's
the thing you keep.

## Install

```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=...        # PowerShell: $env:ANTHROPIC_API_KEY="..."
```

## Use

```python
from claude_harness import Agent, tool, Trace
from claude_harness.builtins import read_file, list_dir, calculate

agent = Agent(tools=[read_file, list_dir, calculate])
print(agent.run("How many entries are in this directory, and what is 2**64?"))
```

Define your own tool - the schema is built from the signature + docstring:

```python
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: City name, e.g. "Paris".
    """
    return f"Sunny in {city}."

agent = Agent(tools=[get_weather])
```

Record a trace (a step-by-step JSON log of the run):

```python
t = Trace(id="my-run")
agent.run("...", trace=t)
t.save("my-run.trace.json")
```

## No API key? Run offline

The loop doesn't care where replies come from. `claude_harness.testing` provides a
`FakeClient` that returns scripted replies, so you can run the whole loop - tool
dispatch, error handling, tracing - with no key, no network, and not even the
`anthropic` SDK installed (the real client is imported lazily).

```python
from claude_harness import Agent
from claude_harness.builtins import calculate
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block

client = FakeClient([
    reply(tool_use_block("calculate", {"expression": "2**100"})),
    reply(text_block("Done.")),
])
print(Agent(tools=[calculate], client=client).run("compute 2**100"))
```

Try it: `python -m claude_harness.examples.offline_demo`.
Tests: `python tests/test_offline_loop.py`.

## Design notes

- **Default model:** `claude-opus-4-8`. Override with `Agent(model=...)`.
- **The loop is the agency.** `Agent.run` calls the model, runs any requested tool,
  feeds the result back, and repeats until `stop_reason != "tool_use"`.
- **You are the runtime.** The model only emits a structured tool *request*; the
  harness executes it. Tool errors are caught and returned with `is_error: true`
  so the model can recover.
- **Adaptive thinking:** `Agent(thinking=True)`.
- **Server-tool pauses** (`pause_turn`) are handled by re-sending and resuming.

## Relationship to the course

`agentic-course/module-00-smallest-agent/agent.py` is the ~30-line from-scratch
version of this. This package is what it grows into once you want to reuse it.
