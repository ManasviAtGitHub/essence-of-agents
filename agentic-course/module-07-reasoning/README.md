# Module 7 - Reasoning models & inference-time compute

Models now "think" internally. What does that do to everything we just built?

## Question
The sharp version: **when is a token spent *inside* the model (extended reasoning)
worth more than a step taken *outside* it (a tool call, a re-plan)?**

## Principle
Some of the scaffolding from Modules 2 and 5 has moved *inside* the model - it can now
deliberate before answering. But internal reasoning only **substitutes** for external
scaffolding when the missing ingredient is *deliberation*. When the missing ingredient
is *information or action* (a fact, a file, the real world), no amount of thinking helps
- you still need the loop and the tools. There, they're **complements**, not substitutes.

## See it (no key)
- `widgets/inside-outside/index.html` - pick a task and an approach. A logic puzzle is
  solved by thinking *inside*; a question about a fact the model never saw is only solved
  by a step *outside* (a tool). Same two levers, opposite winners.

## The aha
"Better model" and "better harness" are sometimes substitutes and sometimes complements.
Which one you're in depends on the task - and you find out by measuring, not guessing.

## Honest note
Reasoning costs tokens and latency. For deliberation-bound tasks that's worth it; for
information-bound tasks it's pure waste (slower, costlier, still wrong). Match the spend
to the bottleneck.

## Build it (no key)
`python agentic-course/module-07-reasoning/bake_off_offline.py` -- the three-way
bake-off table (more-inside vs more-outside vs both) across both task types. The
numbers are illustrative (hand-authored) - they show the *shape* of the result;
`CHALLENGE.md` is where you measure real ones.

## Run
Open `widgets/inside-outside/index.html`. `CHALLENGE.md` runs the real three-way
bake-off.
