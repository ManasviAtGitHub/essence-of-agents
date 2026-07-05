# By hand - be the accountant for an MoE

The module is "done" when you can price a mixture-of-experts model yourself.

## 1. One expert
An expert FFN has three matrices (gate, up, down), each `d x m`.
With d = 4096 and m = 1024, how many parameters is one expert?
(Check: 3 x 4096 x 1024 = 12.58M.)

## 2. A whole model
A model has 32 layers, all MoE, each layer with 64 routed experts + 1 shared,
top-2 routing, and the expert size from question 1. Attention + embeddings add
a flat 2.0B that always runs.
- Total parameters?
- Active parameters per token?
- What fraction of the model does one token touch?

## 3. The DeepSeek check
Redo the arithmetic with the real DeepSeek-V3 shape: d = 7168, m = 2048,
256 routed + 1 shared, top-8, 58 MoE layers, and derive the always-on rest
from the reported 671B total. You should land within rounding of the reported
37B active. (The widget's mechanism act 2 does this on screen - do it on paper
first, then compare.)

## 4. The router
Router logits for 4 experts: [2.0, 5.0, 4.4, 1.0], top-2 routing.
- Softmax all four (Module 0's formula).
- Which two survive? Renormalize their probabilities into gates g1, g2.
- Write the layer's output as a weighted blend.

## Stretch
- C(64,2) vs C(8,2): how many possible "teams" does fine-grained slicing buy,
  at the same active compute? Why might more teams mean better specialization?
- Explain in three sentences why router collapse is invisible on the loss
  curve while it happens, and what DeepSeek-V3's bias method changes about
  the top-k selection without touching gradients.
