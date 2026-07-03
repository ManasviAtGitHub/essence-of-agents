# Coding Challenge - give the agent a reader

`verify_offline.py` fakes the writer and runs a real verifier. Now make the writer real.

## With a real model
1. Ask the model to write a function for a spec.
2. Run it against tests (or a type check / linter).
3. On failure, feed the **exact error** back and ask for a fix. Loop until green or a
   retry budget is hit.

```python
from claude_harness import Agent
coder = Agent(system="Return only Python code, no prose.")
code = coder.run(spec)
while (err := verify(code)) is not None:
    code = coder.run(f"That failed:\n{err}\nFix it. Return only the code.")
```

Measure: how many attempts to green? How often does it converge at all? That number is
your agent's quality - and it's set mostly by the verifier, not the model.

## Strengthen the verifier
Swap the test for: a stricter test set, a type checker, a property-based test, or an
LLM-as-judge. Watch the convergence change. The lesson: **a better verifier beats a
better generator** for most tasks.

## Safety note
Running model-written code requires a sandbox (Module 9). `verify_offline.py` only
`exec`s our own trusted strings - never `exec` untrusted model output unsandboxed.

## Going deeper
Spawn N independent verifiers, each prompted to *refute* the answer, and require a
majority to accept (adversarial verification). When is one verifier not enough?
