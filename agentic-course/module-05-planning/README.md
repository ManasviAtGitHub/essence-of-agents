# Module 5 - Planning & decomposition

What about a task too big for one loop?

## Question
The Module 2 loop reacts one step at a time. For a multi-step job, should the agent
think the whole thing through up front - and what happens when the world doesn't match
the plan?

## Principle
Planning spends cheap compute (a throwaway draft) to make expensive actions less likely
to be wrong. But a plan is a *prediction*, and predictions break. The move that matters
is **re-planning from the new state**, not clinging to a perfect-looking stale plan.
(Branching search - trying multiple candidate plans - is one richer form of this, not a
grand unified theory.)

## See it (no key)
- `widgets/plan-replan/index.html` - a task with a tidy two-step plan. Run it: step 2
  fails because the plan assumed a layout that wasn't there. With **re-plan ON**, the
  agent reads the actual state and re-plans to success; with it **OFF**, it's stuck.

## The aha
The first plan was wrong by step 2 - and that was fine. Re-planning from the error beat
faithfully executing the stale plan. Plans are disposable; the *ability to re-plan* is
the asset.

## Under the hood
A plan is just more text in the context (Module 3) that conditions the next actions
(Module 2). So "re-planning" is: notice the observation that broke the assumption, and
write a new plan into the context from there.

## Build it (no key)
`python agentic-course/module-05-planning/plan_offline.py` -- the plan / execute /
re-plan loop in code. It runs once with re-plan ON and once OFF, so you watch the stale
plan die on the first surprise (break it on purpose).

## Run
Open `widgets/plan-replan/index.html`, toggle **re-plan on fail**, press Run.
`CHALLENGE.md` builds a real plan-and-execute loop on the harness.
