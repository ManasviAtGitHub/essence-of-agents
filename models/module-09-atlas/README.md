# Module 9 - Map of the landscape (the atlas)

The whole track, on one map. Modules 0-8 taught each mechanism from first
principles; this module places every one of them - plus a few named cousins -
on a single taxonomy, so any acronym you hear has a home.

## Question
You have met a couple dozen methods - GQA, MLA, MoE, MTP, SFT, DPO, GRPO, LoRA,
QLoRA, distillation, quantization... How do they relate? When someone says a
new one, where does it go?

## Principle
Every method in this track is a factor in some cost formula getting smaller.
So the organizing question is: **what resource does it attack?** - KV/memory,
compute (FLOPs), decode speed, parameter count, data efficiency, or behavior/
quality. Cross that with **what stage it lives in** (architecture, pretraining
& alignment, fine-tuning, inference & serving) and the zoo becomes a map.

## See it (no key)
`widgets/landscape/index.html` - a filterable atlas. Filter methods by stage or
by the resource they attack; click any method for a one-screen summary (what it
is, what it optimizes, what supervision it needs, what it costs, the point, and
the module that explains its mechanism). ~25 methods, each pinned to its home
module (M0-M8) or marked a "cousin" that generalizes from one you already saw
(PPO, KTO/ORPO, KV-cache eviction).

## The aha
The landscape is not a pile of acronyms - it is a small set of resources
(memory, compute, speed, params, data) and a handful of tools attacking each.
Name the resource, and any new method stops being a mystery.

## How this module differs
This is an ATLAS, not a mechanism module - a reference and a synthesis, the
capstone of the deep spine. It does not re-derive anything; it places what the
other nine modules built. Cousins marked "named here" are pointed at the
module whose mechanism they generalize, not re-explained.

## Coverage
- Architecture: autoregression, tokenization, attention, GQA, KV cache, MoE,
  MLA, MTP.
- Pretraining & alignment: pretraining, SFT, RLHF, DPO, reasoning RL, GRPO,
  (PPO, KTO/ORPO as cousins).
- Fine-tuning: full fine-tuning, LoRA, QLoRA, distillation.
- Inference & serving: quantization, overtraining, inference-time compute,
  speculative decoding, prompt caching, (KV-cache eviction as a cousin).

## The whole track, in one sentence
A language model is a next-token machine (M0) reading learned token-vectors
(M1) that talk via attention (M2) within a memory budget (M3), processed by
experts (M4), made affordable by MLA/MTP (M5), and shaped - not filled - by
training (M6) whose reasoning stage (M7) is selected for by a verifier, then
shrunk to fit (M8). This map is all of it at once.
