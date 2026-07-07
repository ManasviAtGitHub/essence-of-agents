# Challenge - place the reward, fix the bias

## Part 1 - place the reward
For each method, name WHERE in the pipeline it lives (pretraining /
mid-training / post-training / test time) and WHAT signal rewards it:
A. RLP   B. Tongyi's agentic mid-training   C. GRPO on math   D. TTRL

<details><summary>answer</summary>
A. PRETRAINING - information gain: how much a sampled thought raises the
   probability of the actual next token (verifier-free, dense).
B. MID-TRAINING (a new stage) - synthetic agent-task trajectories.
C. POST-TRAINING - verifiable rewards (checkable answers), group-relative
   advantage (M7's arithmetic).
D. TEST TIME - majority-vote pseudo-labels over the model's own samples on
   unlabeled data.
</details>

## Part 2 - compute the length bias (be Dr.GRPO)
Two WRONG answers in a GRPO group with advantage -0.4 each:
answer X is 20 tokens long; answer Y is 200 tokens long.
1. Under length-normalized GRPO (advantage spread over tokens), what
   per-token penalty does each answer receive?
2. Which behavior does this accidentally teach, and what is Dr.GRPO's fix?

<details><summary>answer</summary>
1. X: -0.4/20 = -0.02 per token. Y: -0.4/200 = -0.002 per token - the long
   wrong answer is punished 10x LESS per token.
2. Rambling: being wrong at length is cheaper per token than being wrong
   briefly, so responses grow without getting smarter. Dr.GRPO removes the
   length (and std) normalization so a wrong answer costs the same
   regardless of length.
</details>

## Part 3 - the V4 twist
DeepSeek-V4 does not run one big mixed RL stage. Describe its two-step
post-training in one sentence each, and name what grades the student.

<details><summary>answer</summary>
1. Train domain SPECIALISTS (math, code, agents...) independently, each
   with SFT + GRPO and its own reward.
2. Fuse them into ONE student by on-policy distillation: the student
   samples its own trajectories and every token is graded by the teachers'
   probabilities (a per-token log-ratio correction) - "RL makes the
   teachers, distillation makes the model."
</details>
