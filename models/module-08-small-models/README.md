# Module 8 - Small models: distillation, quantization, enough

Not every job needs 671B parameters - and inference cost, paid on every token
forever, usually matters more than training cost. Three ways to get a small
model that punches above its size.

## Question
When is small enough - and how do small models get so good?

## Principle
Three compressions, each attacking a different cost:
- **Overtrain (data).** Chinchilla (2022) says ~20 training tokens per
  parameter is *training*-optimal. But inference is forever, so we overtrain
  small models far past that (Llama-3-8B: ~1,875 tok/param) to get models that
  are cheap to serve.
- **Distill (a mind).** Train a small student to match a big teacher's output
  DISTRIBUTION (soft targets, KL divergence) - copying how it thinks, not just
  its answers. R1's chains distilled into small Qwen/Llama.
- **Quantize (bytes).** Store each weight in fewer bits (fp16 -> int8 -> int4);
  size = params x bits / 8. Quality holds to a precision floor.

## See it (no key)
`widgets/shrink-it/index.html` - two passes:
- **intuition (10 steps):** the Chinchilla ridge and the overtrained-8B point
  above it; distillation (teacher's soft targets -> student, R1 -> Qwen); the
  quantization slider (fp16 -> int2) with live byte math and a quality cliff;
  the aha - copy the distribution, not the size.
- **mechanism (17 steps, 3 acts):** act 1 computes scaling (20 tok/param vs
  Llama-3-8B's ~1,875, and why inference cost flips the optimum). Act 2 is
  distillation - hard label vs soft target, the KL loss, R1 -> Qwen verified,
  and the ceiling (a copy can't beat its teacher). Act 3 is quantization -
  params x bits/8 computed live (7B: 14 GB -> 3.5 GB at int4), the precision
  floor, and how the three tools stack (671B -> 7B distill -> int4 = 3.5 GB).

## The aha
Most of a giant model's BEHAVIOR fits in a small one - if you copy the
distribution, not the parameter count. Match the model to the task; a
leaderboard is not a routing table.

## Honest notes
- Verified: Chinchilla ~20 tok/param (Hoffmann 2022); Llama-3-8B on ~15T tokens
  (~1,875 tok/param, Meta Llama 3); distillation on teacher soft targets (KL);
  DeepSeek-R1 distilled into Qwen 1.5B/7B/32B. Byte math (params x bits/8) is
  computed live; the quality-vs-precision thresholds are illustrative (they
  vary by quantization method).

## Done when (the bar for this module)
Given a parameter count and a bit-width, you can compute a model's disk size by
hand, and say which of the three tools (overtrain / distill / quantize) attacks
which cost. `CHALLENGE.md`.

## Next
Module 9 - the atlas: every method in the whole track (and its named cousins)
on one map, each linking back to where it was explained.
