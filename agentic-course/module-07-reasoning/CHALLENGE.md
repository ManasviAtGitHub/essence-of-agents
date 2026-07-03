# Coding Challenge - the three-way bake-off

The widget asserts the effect. Measure it.

## Run the same tasks three ways (real models)
1. **Cheap model + heavy scaffold** - a small model with an explicit step-by-step loop.
2. **Reasoning model + thin loop** - let the model deliberate internally.
3. **The wrong pairing** - reasoning model *and* heavy scaffold (often overthinks).

Across a deliberation-bound set (puzzles) and an information-bound set (questions whose
answers need a tool), record **accuracy, latency, and tokens** for each.

```python
from claude_harness import Agent
deliberate = Agent(thinking=True)             # reasoning inside
scaffold   = Agent(thinking=False, tools=[...])  # steps outside
```

What you should find:
- Puzzles: reasoning-inside wins; the external scaffold adds cost, not accuracy.
- Fact lookups: the tool step wins; reasoning-inside is confidently wrong.
- The wrong pairing: most expensive, rarely the most accurate.

That table is your guide to where to spend compute - and it's an eval (Module 10).

## Offline
You can't fake the accuracy *differences* (they're real model behavior), but you can
build the timing/token harness with a `FakeClient` and plug a real model in later.

## Going deeper
Add a budget: cap tokens per task (the harness can carry a budget) and see which
approach degrades gracefully. When compute is scarce, which lever do you cut first?
