# Module 6 - Verification & self-correction (the center of the course)

The agent is confidently wrong sometimes. How does it catch itself?

## Question
Generation is easy - the model always produces *something*. How do we make that
something *correct*?

## Principle
**Generation is cheap; verification is the bottleneck.** An agent is roughly as good as
its feedback signal. The highest-leverage thing you can add to almost any agent is a
good verifier - a test, a compiler, a type checker, a judge, reality.

## See it (no key)
- `widgets/verify-loop/index.html` - same task, a toggle for the verifier. OFF: the
  agent ships its first (buggy) attempt; it looks done and isn't. ON: the tests fail,
  the agent reads the failure, fixes it, tests pass.
- `verify_offline.py` - the loop in code, keyless: generation is faked, but the
  **verifier really runs** (`exec` + real tests). Attempt 1 fails, attempt 2 passes -
  and the *writer* barely changed.

## The aha
The generator barely got smarter between attempts. We just added a reader that can say
"no," and quality jumped. Leverage lives in the verifier, not the writer.

## Honest note
Verifiers vary in strength: a compiler/test is a hard signal; an LLM-as-judge is a soft
one (Module 10). The skill is choosing the strongest verifier the task allows.

## Run
```
python agentic-course/module-06-verification/verify_offline.py
```
or open `widgets/verify-loop/index.html` and toggle the verifier.
