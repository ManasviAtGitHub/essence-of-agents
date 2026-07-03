# Coding Challenge - supervisor + specialists, then prove the tax

## Build a fan-out
1. A supervisor agent splits a task into independent subtasks.
2. Spawn one worker agent per subtask (each with its own fresh context).
3. Collect the results and synthesize a final answer.

```python
from claude_harness import Agent
supervisor = Agent(system="Split the task into independent subtasks, one per line.")
def worker(subtask): return Agent(tools=[...]).run(subtask)

subtasks = supervisor.run(task).splitlines()
results = [worker(s) for s in subtasks]      # parallelize for real with threads/async
final = Agent().run("Synthesize:\n" + "\n".join(results))
```

## Now prove the tax
Run a *sequential* task (one tricky bug) two ways: a single agent, and a 5-agent team.
Measure tokens, wall-clock, and whether each finishes correctly. The single agent should
win - that's the lesson made quantitative.

## Context isolation is the real prize
Give workers a task too big for one context window (e.g. audit 20 files). The single
agent overflows or loses detail; the team - each worker on a slice - doesn't. *That's*
when many beats one.

## Offline
Stub each agent with a `FakeClient`; you can build and test the fan-out / synthesis
control flow with no key. The accuracy differences need real models.
