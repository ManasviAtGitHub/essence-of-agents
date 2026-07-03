# Essence of Agents - Building Minds from a while loop

A first-principles agentic-AI course. Inspired by **3Blue1Brown** (derive the idea,
build the intuition, engineer the click) and **The Coding Train** (build it live,
from scratch, mistakes and all, ending in something that runs).

## The contract

One agent, followed through ~twelve transformations. The *story* starts it at ~30
lines (Module 0) and grows it, module by module, until it can plan, check itself,
spawn helpers, defend itself, and prove it got better. In the repo, each module is
a self-contained stop on that arc - a keyless widget plus a small demo - and
`claude_harness/` is the grown-up form the same loop settles into.

## The thesis (stated up front, mastered in Module 3)

> An LLM is, near enough, a pure function: context in, a distribution over next
> tokens out. It keeps no memory between calls unless you put it there. So most of
> building an agent is two jobs - deciding what goes into the context, and turning
> some of what comes out into actions.

This is the literal story through Module 6; multi-agent and production are about
what surrounds the loop.

## The recurring primitive

A creature whose entire world is the scroll of context it can read and append to.
Every later mechanism is that primitive **recomposed**, not a new picture.

## Format

Video + companion repo, with interactive widgets layered in at the ~6 aha moments.
The widgets are **self-contained, keyless HTML simulations** (open them from
`index.html`) - they are the course's primary surface. The Python demos beside them
are optional deep-dives on the same ideas, not dependencies of the widgets.

## Modules

See `docs/00-pedagogy.md` for the full breakdown. Start with
`module-00-smallest-agent/`.

| #  | Title                                   | The unlock                               |
|----|-----------------------------------------|------------------------------------------|
| 0  | The smallest agent that could           | Agency is the loop, not the model        |
| 1  | Hands (tools)                           | Competence was latent; tools grant access|
| 2  | The loop (Reason + Act)                 | Reasoning pays rent in the next action   |
| 3  | Context is the only lever               | You program in English; order is syntax  |
| 4  | Memory & retrieval                      | Retrieval swaps which agent you're running|
| 5  | Planning & decomposition                | Re-planning beats a perfect stale plan   |
| 6  | Verification & self-correction (center) | Leverage lives in the verifier           |
| 7  | Reasoning models & inference-time compute | Substitute vs complement - measure it  |
| 8  | Many agents                             | Multi-agent buys context isolation       |
| 9  | Reliability & security                  | The exploit is the feature working       |
| 10 | Evaluation                              | You can't improve what you can't measure |
| 11 | Shipping: close the loop                | Prod failures become eval rows           |
|  - | Capstone                                | The choice diagnoses what you'll wrestle |
