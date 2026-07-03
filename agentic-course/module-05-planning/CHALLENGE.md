# Coding Challenge - plan-and-execute, then re-plan

Build a planner on top of the harness.

## Plan-and-execute
1. Ask the model for a numbered plan (a list of steps) for a task.
2. Execute steps one at a time with the agent loop, feeding each step's result back.
3. Stop when the task is done.

```python
from claude_harness import Agent
planner = Agent(system="Output a short numbered plan, one step per line.")
worker  = Agent(tools=[...])
plan = planner.run(task).splitlines()
for step in plan:
    worker.run(step)
```

## Now make it survive reality
Have a step fail (raise, or return an error). Instead of crashing, feed the error back
to the planner and ask for a **revised plan from the current state**. Loop until done or
a retry budget is hit.

The lesson you'll feel: the rigid version dies on the first surprise; the re-planning
version routes around it. Measure how often each completes the task - that's a planning
eval (Module 10).

## Offline
Stub `planner`/`worker` with `FakeClient`s scripted to return a plan, then a failure,
then a revised plan - enough to wire up the re-plan control flow without a key.

## Going deeper
Try **tree-of-thought**: generate 2-3 candidate plans, score them, expand the best.
When is searching over plans worth the extra tokens? (Returns in Module 7.)
