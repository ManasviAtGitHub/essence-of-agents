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
`widgets/expert-router/index.html` - two passes:
- **intuition (8 steps):** a dense layer where everything fires, then the same
  layer split into experts: ' France' wakes E2+E5, ' is' wakes E7+E3, the rest
  sleep. Two meters carry the lesson - params in memory vs params this token
  touches.
- **mechanism (20 steps, 3 acts):** act 1 computes one routing decision live
  (router logits -> softmax -> top-k -> gates). Act 2 is the receipts: the page
  DERIVES 671B and 37B from the verified architecture (44.0M per expert x 257
  experts x 58 layers + the always-on rest) - the headline numbers are computed,
  not quoted. Act 3 breaks it: router collapse (rich-get-richer feedback until
  one expert does 74% of the work, silently), then the two fixes - the classic
  auxiliary balance loss and DeepSeek-V3's auxiliary-loss-free bias method.

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

## Next
Module 5: all 671B must sit in GPU memory even asleep - and the KV cache makes
long context another memory bill. DeepSeek's MLA is how V3 pays it.
