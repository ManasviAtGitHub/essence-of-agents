# Module 8 - Many agents

When does one mind need to become several?

## Question
Multi-agent setups are everywhere. When do they actually help, and when are they just
one good agent wearing a trenchcoat?

## Principle
Multi-agent earns its cost when it buys **context isolation** (each agent gets a clean,
focused context), **specialization**, or **parallelism**. When the task has none of
those - it's sequential and fits one context - extra agents only add coordination
overhead. The shape of the team should match the shape of the task.

## See it (no key)
- `widgets/team-flow/index.html` - pick a task and a team. A parallel, isolatable audit
  is won by a supervisor + specialists; a single sequential bug is won by one focused
  agent (the team just adds tax). Same two levers, opposite winners.

## The aha
The 5-agent build loses to one good agent when you've paid the coordination tax for
nothing. It wins only when each agent gets a context the others couldn't hold. It's
divide-and-conquer over *context*, not magic.

## Honest note
Most multi-agent systems in the wild are over-built. Default to one good agent; reach
for many when you can name the isolation/specialization/parallelism it buys.

## Mechanically
Each sub-agent is the same loop (Module 0) with its own scroll of context (Module 3).
Multi-agent is just several scrolls plus a protocol for passing messages between them.

## Build it (no key)
`python agentic-course/module-08-multi-agent/fanout_offline.py` -- a supervisor fan-out
where each worker is a real Agent with its own isolated context, then a synthesis step.

## Run
Open `widgets/team-flow/index.html`. `CHALLENGE.md` builds a real supervisor + workers.
The production track's "Scale it" chapter simulates the operational side: per-worker
budgets, retrying a failed worker alone, and merging summaries - never contexts.
