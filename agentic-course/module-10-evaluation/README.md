# Module 10 - Evaluation

You changed a prompt. Is the agent *better*, or do you just feel that way?

## Question
Every module so far improved the agent "by feel." How do you actually *know* a change
helped - and didn't quietly break three other things?

## Principle
**You can't improve what you can't measure.** Evals are the experimental method for
agents: a dataset of cases with checkable outcomes, a way to score, and a comparison
between versions. Without them, prompt-tuning is alchemy.

## See it (no key)
- `widgets/eval-grid/index.html` - run an 8-case eval on two prompt versions. v2
  *feels* like an improvement and even fixes a case the baseline missed - but the eval
  shows it broke three others. Net: a regression you'd have shipped on vibes.
- `eval_offline.py` - the same as a real harness: run each version over a dataset, score
  against expected answers, compare. Keyless (outputs scripted; harness + checker real).

## The aha
Two "obvious improvements" you were proud of can score *worse*. The eval is the
telescope - without one you're just staring at the sky and guessing.

## Eval-driven development
This is the loop the whole course has been building toward: **change -> measure -> keep
or revert.** Modules 3, 6, 7, and 8 all ended with "measure it" - this is the how.

## Honest note
The grids and scores here are illustrative. Real evals need representative datasets,
and for fuzzy tasks an **LLM-as-judge** (a soft verifier - Module 6) to score outputs.

## Run
```
python agentic-course/module-10-evaluation/eval_offline.py
```
or open `widgets/eval-grid/index.html` and run the eval on both versions.
