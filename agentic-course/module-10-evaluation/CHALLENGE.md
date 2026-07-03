# Coding Challenge - build the eval you've been needing since Module 3

## A real eval harness
1. Collect ~20 cases with checkable answers (reuse the Module 3 extraction task, or the
   Module 6 code task).
2. Write a scorer: exact match, JSON-field match, "tests pass", or an LLM-as-judge for
   fuzzy outputs.
3. Run version A and version B over the set; print both pass-rates and the per-case diff.

```python
from claude_harness import Agent

def evaluate(agent, dataset, scorer):
    return sum(scorer(agent.run(x), expected) for x, expected in dataset) / len(dataset)

a, b = Agent(system=PROMPT_A), Agent(system=PROMPT_B)
print(evaluate(a, data, check), evaluate(b, data, check))
```

## Make it a regression gate
Save the dataset. Every time you change a prompt or a tool, re-run it. Block the change
if the score drops. That single habit turns prompt-tuning from alchemy into engineering.

## LLM-as-judge (soft verifier)
For outputs with no exact answer (summaries, plans), have a model score each output
against a rubric. Note its limits: judges are biased and gameable - calibrate against a
few human-labeled cases.

## Offline
The whole harness - dataset, scorer, comparison - runs keyless with `FakeClient`
stand-ins (as in `eval_offline.py`). Only the LLM-as-judge needs a real model.
