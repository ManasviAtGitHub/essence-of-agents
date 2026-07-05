# Module 6 - Training stages: same machine, different manners

A base model, a chat model, and a reasoning model can share the SAME
architecture and even the same starting weights - yet answer nothing alike.
Why? Not knowledge. Manners.

## Question
Base continues, chat answers, reasoning deliberates. If the machine is the
same, what did the different training actually do?

## Principle
Training shapes the **distribution**, not the knowledge. Four stages, each a
different loss bending the same next-token machine from Module 0:
- **Pretraining** - next-token loss on trillions of tokens of web text. Builds
  a completion machine that holds essentially all the knowledge.
- **SFT** - imitate curated user->assistant dialogues (loss masked to the
  assistant's tokens). Installs manners: answer, then STOP.
- **Preference (RLHF / DPO)** - humans rank whole outputs; push probability
  toward the preferred one. Installs tone, helpfulness, formatting, safety.
- **Reasoning RL** - sample K attempts, score with a VERIFIER, reinforce the
  winners. Long chains of thought emerge because they score correct.

## See it (no key)
`widgets/four-manners/index.html` - two passes:
- **intuition (10 steps):** one prompt, four manners. The killer A/B: base
  says "Paris" then rolls on forever (the <end> token's probability is tiny);
  SFT says "Paris." and stops (<end> now dominates) - **same 'Paris' both
  times, only the STOP token's mass moved.** Then preference (center-a-div,
  ranked outputs) and reasoning (course 1's bat-and-ball: SFT blurts $0.10,
  reasoning deliberates to $0.05).
- **mechanism (21 steps, 3 acts):** act 1 shows one training EXAMPLE per stage
  - pretraining's every-position loss, SFT's prompt-masking, DPO's chosen/
  rejected pair, reasoning RL's sample-and-verify. Act 2: what updates, then
  **LoRA and QLoRA** - freeze the giant base, train a low-rank adapter B*A
  (67.1M -> 262K trainable per matrix, a 256x cut, computed live), and QLoRA's
  4-bit frozen base that lets you fine-tune a 65B model on one 48GB GPU - then
  the DATA FUNNEL (14.8T tokens collapsing to a trickle). Act 3 breaks it:
  catastrophic forgetting, the alignment tax, and reward hacking (an RL model
  is exactly as good as its verifier - course 1, Module 6, now inside
  training).

## The aha
Not one stage taught a new fact. The base model already contained Paris,
flexbox, and the algebra. Each stage only bent WHICH completion it prefers -
stop here, phrase it kindly, think first.

## Honest notes
- Per-stage logits are hand-authored (labeled); every softmax and probability
  shift is computed live in the page.
- Verified real numbers: DeepSeek-V3 pretrained on ~14.8T tokens
  (arXiv 2412.19437); LoRA's B*A decomposition (Hu et al. 2021); QLoRA's
  4-bit NF4 base + 65B-on-one-48GB-GPU result (Dettmers et al. 2023). The
  LoRA param counts (67.1M vs 262K, 256x) are computed live from d=8192,
  r=16. The SFT/preference/RL dataset sizes are order-of-magnitude,
  labeled illustrative.
- The bat-and-ball is a deliberate callback to course 1, Module 2.

## Done when (the bar for this module)
Given a described behavior change (it started refusing X; it stopped rambling;
it began showing its work), you can name which training stage most likely
caused it, and say what that stage's loss and data look like. `CHALLENGE.md`.

## Next
Module 7 zooms all the way into stage 4: reasoning models and
inference-time compute, where the verifier becomes the teacher.
