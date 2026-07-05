# Module 7 - Reasoning RL: the verifier becomes the teacher

Module 6's fourth stage rewarded verified attempts. Here it is in full - the
inference-time-compute idea and the training loop (GRPO) that produce reasoning
models.

## Question
What, physically, is "thinking harder"? And where did DeepSeek-R1's long, self-
correcting chains of thought come from - nobody wrote them?

## Principle
Two ideas. (1) Reasoning is **serial compute at inference**: more chain-of-
thought tokens = more forward passes (Module 0) spent before committing an
answer - traded for accuracy on deliberation-bound problems. (2) Long chains
are **trained by a verifier**: sample many attempts, score each with a checker
(course 1's Module 6, now the reward), and reinforce the winners with **GRPO** -
which uses the group's own average as the baseline instead of a separate value
model. Careful reasoning EMERGES because it scores.

## See it (no key)
`widgets/verifier-teacher/index.html` - two passes:
- **intuition (9 steps):** short chain (blurts, wrong) vs long chain (works it
  out, right) with a compute-vs-accuracy meter; then the RL loop - sample
  attempts, a verifier scores them, reinforce above the group average; the
  R1-Zero "aha moment" (self-correction from pure RL); the limit (only where a
  cheap verifier exists).
- **mechanism (18 steps, 3 acts):** act 1 is inference-time compute (accuracy
  scales with thinking budget - but only on deliberation-bound tasks). Act 2 is
  GRPO computed live: sample a group of 8, verifier rewards [1,0,1,...], group
  mean/std as the baseline, advantage = (reward-mean)/std, reinforce - and why
  dropping PPO's value model saves ~40-60% memory. Act 3: R1-Zero's emergence,
  R1's SFT cold-start, the verifier limit (math/code yes, poetry no), and the
  distillation bridge to Module 8.

## The aha
Reasoning was never programmed in - it was SELECTED FOR by a verifier,
generation after generation. Which is also its limit: it works where a cheap,
exact verifier exists (math, code), and barely where one does not.

## Honest notes
- Verified against DeepSeek-R1 / DeepSeekMath: GRPO uses no value model, a
  group-relative advantage, and rule-based verifiable rewards; ~40-60% memory
  saving vs PPO; R1-Zero showed emergent self-correction; R1 added an SFT cold
  start. The problem, attempts, and accuracy figures are illustrative; the GRPO
  advantage arithmetic (mean, std, advantages) is computed live.

## Done when (the bar for this module)
Given a group of attempt-rewards, you can compute each attempt's group-relative
advantage by hand, and say why reasoning RL works on math but not on "write a
good poem". `CHALLENGE.md`.

## Next
Module 8: shrinking these giants - and R1's reasoning chains become premium
distillation data for small models.
