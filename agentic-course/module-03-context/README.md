# Module 3 - Context is the only lever (the thesis, operationalized)

This is the module the whole course points at. You've felt the agent be flaky
(Modules 0-2). Now: what can you actually *turn* to fix it?

## Question
You can't retrain the model and you can't change the loop's shape. What's the one
thing you *can* change to make the agent better?

## Principle
Only one thing: **what's in the context.** So every real skill here is a context
skill - tokens and the context window (what fits), system prompts and clear
instructions, in-context learning via few-shot examples, the *order* of all of it, and
the sampling that turns the resulting distribution into words. People call this "prompt
engineering"; the honest name is **context engineering**.

## See it (no key)
- `widgets/context-lever/index.html` - one task, one model (locked). Step through
  better-engineered contexts and watch the pass-rate climb from ~40% to ~90% - without
  ever touching the model. You're programming in English, and word order is syntax.
- `widgets/distribution/index.html` - the Module 0 run-again widget,
  **recomposed**: the "Why does it split?" door now opens to show the probability
  distribution the next token was sampled from. The observation from Module 0 becomes
  the mechanism here. One primitive, recomposed - not a new picture.

## The aha
The same task went from failing often to almost always passing, and the model never
changed. The lever was never the model - it was the context.

## Honest note
Pass-rates and the distribution are illustrative (hand-authored). The point is the
*shape* of the effect; `CHALLENGE.md` shows how to measure the real numbers.

## Reproduce the measurement (no key)
`python agentic-course/module-03-context/context_recipes.py` -- real, reproducible
pass-rates that climb as the context recipe improves. No model, no vibes: re-run it and
get the same numbers.

## Run
Open either file under `widgets/` in a browser.
