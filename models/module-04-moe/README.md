# Module 4 - Mixture of Experts: parameters are not compute

DeepSeek-V3 has 671 billion parameters. It runs like a 37-billion-parameter
model. This module is the trick - and the receipts.

## Question
How can the biggest models keep getting bigger without every token getting
slower and more expensive?

## Principle
In an MoE layer the FFN is split into many **experts**, and a tiny learned
**router** sends each TOKEN to a few of them (plus one **shared expert** that
always runs). Capacity - what the model can store - decouples from cost - what
one token touches. Routing is per token, per layer: score -> softmax -> top-k ->
renormalized gates -> weighted blend of the chosen experts' outputs.

## See it (no key)
`widgets/expert-router/index.html` - a SIDE-BY-SIDE comparison, two passes:
- **intuition (12 steps):** starts with the anatomy (one transformer layer =
  attention + FFN; the FFN is the fat part), then puts the traditional dense
  FFN and the MoE layer next to each other and runs the SAME tokens through
  both. The dense trap (capacity and cost locked together), the MoE move
  (same capacity, sliced, router in front), ' France' vs ' is' waking
  different experts, per-layer cost chips (11.3B touched vs 0.4B touched),
  the shared expert, the honest price (memory + a new failure mode), and the
  closing comparison: a dense model at V3's per-token cost would be ~37B
  TOTAL - the MoE stores ~18x more at the same price.
- **mechanism (21 steps, 3 acts):** act 1 demystifies the expert itself (a
  small SwiGLU FFN - formula and size computed) before the router (logits ->
  softmax -> top-k -> gates, computed live). Act 2 is the receipts: the page
  DERIVES 671B and 37B from the verified architecture, plus C(256,8) vs
  C(8,2) for why fine-grained slicing wins. Act 3 breaks it: router collapse
  (rich-get-richer until one expert does 74% of the work, silently), then the
  two fixes - the classic auxiliary balance loss and DeepSeek-V3's
  auxiliary-loss-free bias method.

## The aha
Parameters are not compute. The biggest models are mostly asleep on every
token - on purpose - and one tiny linear layer (the router) is what decides
which slice wakes up.

## Honest notes
- Architecture numbers are from the DeepSeek-V3 technical report
  (arXiv 2412.19437): 61 layers (first 3 dense), d = 7168, 256 routed experts
  + 1 shared, top-8, expert intermediate 2048, 671B total / 37B activated.
- The widget draws 8 experts with top-2 routing standing in for 256/top-8 -
  labeled on screen. Router logits are hand-authored; every softmax, gate,
  parameter count, and C(256,8) is computed live in the page.
- Expert "specialties" are emergent and only loosely nameable - the widget
  says so rather than inventing clean labels.

## Done when (the bar for this module)
Given an MoE's shape (experts, top-k, shared, dims, layers), you can compute
its total and active parameter counts by hand. `CHALLENGE.md` is that exercise.

## Run it in code
`models/nanomodel/model.py` runs the DENSE side of this comparison - one plain
`MLP` per layer, capacity and cost locked together. Reading it is how you feel
what MoE unlocks: swap that one FFN for a router plus experts and nothing else
in the forward pass changes.

## Next
Module 5: all 671B must sit in GPU memory even asleep - and the KV cache makes
long context another memory bill. DeepSeek's MLA is how V3 pays it.
