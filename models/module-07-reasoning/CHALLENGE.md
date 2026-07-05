# By hand - GRPO advantages, and the verifier's reach

## 1. Group-relative advantage
A prompt is sampled 6 times; the verifier gives rewards:
`[1, 1, 0, 1, 0, 0]`
- Compute the group mean reward.
- Compute the group standard deviation.
- Compute each attempt's advantage = (reward - mean) / std.
- Which attempts get pushed UP, which get pushed DOWN?

## 2. No value model
PPO estimates a baseline with a separate "value model" (a second network the
size of the policy). GRPO uses the group mean instead.
- What does GRPO save by dropping the value model? (The widget says ~40-60%
  of what?)
- Why is the group mean a reasonable baseline?

## 3. Inference-time compute
A reasoning model's answer is a 300-token chain of thought.
- Roughly how many forward passes did that answer cost, versus a 10-token
  direct answer? (Module 0: 1 pass per token.)
- On which of these would a longer chain help, and why:
  (a) "Prove sqrt(2) is irrational."  (b) "What did my coworker email me at
  9am today?"

## 4. The verifier limit
Reasoning RL (RLVR) needs a cheap, exact verifier.
- List two tasks where one exists, and two where one does not.
- Explain in one sentence why R1 is far stronger at competition math than at
  writing emotionally resonant fiction.

## 5. Emergence
R1-Zero used pure RL, no supervised reasoning examples, and self-correction
("wait, let me recheck") appeared anyway.
- In your own words, why would "wait, let me recheck" get REINFORCED by a
  verifier-based reward, even though no human wrote it?

## Stretch
- Reward hacking (Module 6): design a weak verifier for a math task that a
  model could game without actually solving anything. What does GRPO's use of
  VERIFIABLE (rule-based) rewards buy you against your own hack?
- Why does distilling R1's chains into a small model often beat running GRPO
  on the small model directly? (Think about what the small model can and
  cannot discover on its own.)
