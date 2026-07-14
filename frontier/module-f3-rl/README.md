# F3 - RL eats the pipeline

*Verified as of 2026-07. Exhibits age; the principle does not.*

Track 3's M6 taught four manners in a row: pretrain -> SFT -> preference ->
reasoning RL. The 2026 pipeline has reward signals at the START, in the
MIDDLE, at the END - and at TEST TIME. The stage became an ingredient.

## Question
M6 drew training as a sequence of stages, with RL as the last polish. Where
did the reward signal actually live by mid-2026 - and what happened to the
tidy pipeline?

## Principle
**The reward escaped its stage.**
- Into PRETRAINING: RLP (NVIDIA, Oct 2025) treats a chain of thought as an
  action before predicting the next token, rewarded by information gain -
  verifier-free, dense, on ordinary text.
- A NEW STAGE: agentic mid-training (Tongyi DeepResearch, Oct 2025) between
  pretraining and post-training, on fully synthetic agent-task data.
- At TEST TIME: TTRL (2025 -> a subfield) - majority-vote pseudo-labels on
  unlabeled data become rewards, and the model updates itself at inference.
- The GRPO zoo, each descendant fixing one named flaw: DAPO (entropy
  collapse; clip-higher), GSPO (token-ratio noise kills MoE RL; go
  sequence-level), Dr.GRPO (length bias - long wrong answers punished less
  per token), VAPO (the critic returns), CISPO (keep rare fork-token
  gradients). ScaleRL (Meta, Oct 2025) gave RL its first scaling laws.
- Rewards outgrew verifiable answers: rubric checklists scored by judges
  carry RL into medicine and open-ended work - and invite their own hacking.
- The twist that closes the loop: DeepSeek-V4 (Jun 2026) runs GRPO only on
  domain SPECIALISTS, then fuses them into one student by ON-POLICY
  DISTILLATION (the student samples, the teacher grades every token) -
  "RL makes the teachers, distillation makes the model." M7 + M8, merged.

## See it (no key)
`widgets/reward-everywhere/index.html` - two passes:
- **intuition (7 steps):** a school fable - the robot Cortex learns to talk.
  First it only copies; then a teacher scores the final drills; then the
  scoring spreads - live, at the very start, into a brand-new middle class -
  until every phase of its schooling is graded. That is the aha.
- **mechanism (15 steps, 3 acts):** act 1 computes GRPO's advantage as
  geometry (each answer's distance from the class average, in std-widths),
  then Dr.GRPO's length-bias fix on two wrong answers (-0.020 vs -0.002 per
  word, live) and the zoo of named descendants. Act 2 spreads the score:
  RLP's information-gain reward (log(0.42/0.15), live) and TTRL's majority
  vote -> pseudo-rewards (live), with the school phases mapped to pipeline
  stages on screen. Act 3 computes one on-policy-distillation word grade,
  merges drilled specialists into one student, and closes with rubric
  rewards + the schooling scored throughout. Exhibit stamps date each act.

## The aha
"Post-training" is dying as a phrase. Reward is becoming an ingredient
mixed through the whole pipeline - and the tidy M6 diagram is now a dated
exhibit of how 2024 thought.

## Honest notes
- All toy rewards/probabilities hand-authored (labeled); every mean, std,
  advantage, log-ratio and vote computed live on screen.
- Method attributions primary-sourced (arXiv/tech reports). OpenAI's
  "universal verifiers" is leak-only and appears nowhere here.
- Rubric-reward benchmark deltas are stated qualitatively (rule 11).

## Done when (the bar for this module)
You can place RLP / mid-training / GRPO-family / TTRL on a pipeline diagram,
say what signal rewards each, and explain Dr.GRPO's length-bias fix with the
two-answer arithmetic. `CHALLENGE.md`.

## Next
F4: the loop itself learns - agents trained end to end, orchestration in
the weights.
