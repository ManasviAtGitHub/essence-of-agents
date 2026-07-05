# By hand - one attention head on paper

d_head = 2 (even smaller than the widget). Three tokens with:

| token | k        | v        |
|-------|----------|----------|
| A     | [1, 0]   | [2, 0]   |
| B     | [0, 1]   | [0, 2]   |
| C (query) | q = [2, 1] | -    |

## 1. Scores
Compute q.k for A and B. (C attends over its past: A and B only.)

## 2. Scale
Divide by sqrt(2) ~ 1.41.

## 3. Softmax
Turn the two scaled scores into weights (Module 0's formula). Check they
sum to 1. Which token wins, and by roughly how much?

## 4. Blend
output = w_A x v_A + w_B x v_B. Compute both components.

## 5. The mask
Suppose there were a token D after C. What score does C's row give D, and
what weight does softmax hand it? Why is that non-negotiable for a model
trained to predict the NEXT token?

## 6. The bill (bridge to Module 3)
Llama-3-70B: 80 layers, 8 KV heads (GQA), head_dim 128, fp16 (2 bytes).
Per token, the cache must keep k AND v in every layer and KV head:
2 x 80 x 8 x 128 x 2 bytes. Compute it. Then multiply by a 128k-token
context. (You have just done Module 3's homework early.)

## Stretch
- Why divide by sqrt(d_head) at all? Try your computation again with
  q = [20, 10] and watch what softmax does without scaling.
- GQA shares 8 KV heads across 64 query heads. What does that change in
  your step-6 arithmetic, and what does it NOT change (hint: n^2)?
