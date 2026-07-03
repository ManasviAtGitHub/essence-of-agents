# Capstone rubric

Acceptance is the same for all three projects. Aim for evidence, not vibes.

## Required (must pass)
- [ ] **Runs on the harness.** Built on `claude_harness` (or your own equivalent loop),
      with at least two real tools.
- [ ] **Eval set + score.** >= 15 cases with a scorer (exact match / tests-pass /
      LLM-judge). A recorded pass-rate, not a single demo run. (Module 10)
- [ ] **Recovery trace.** A saved `Trace` (or equivalent log) showing the agent hit a
      real failure - a tool error, a wrong answer caught by a verifier, a re-plan - and
      recovered. (Modules 6, 5)
- [ ] **A guardrail.** At least one: least-privilege tools, an approval gate on
      irreversible actions, or an input guardrail on untrusted text. (Module 9)

## Strong (aim here)
- [ ] **Re-plan on failure**, not just retry the same step. (Module 5)
- [ ] **Context discipline** - you can name what's in the context and why; nothing
      volatile bloats it. (Modules 3, 4)
- [ ] **Eval-driven changes** - your commit history shows change -> measure -> keep/revert.
      (Module 10)
- [ ] **A cost or latency number** per run, and one deliberate optimization. (Module 11)

## Honest self-review (answer in your writeup)
- Where is your verifier weakest, and what would a hostile input do? (Modules 6, 9)
- Is your multi-agent structure (if any) earning its coordination cost? (Module 8)
- Are you spending tokens inside the model or outside it - and is that the right call for
  this task? (Module 7)

The grade is the eval number and the recovery trace. Everything else is how you got there.
