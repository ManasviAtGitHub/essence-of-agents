# Module 2 - Attention: how vectors talk

Module 1 ends with every token as a vector - but a vector ISLAND. ' is' knows
nothing about ' France'. This module is how meaning moves.

## Question
Token 400 needs what token 3 said. Nothing else in the network connects
positions. How does information travel?

## Principle
Every token wears three learned hats: a **query** (what am I looking for?), a
**key** (what do I contain?), a **value** (what will I hand over?). Attention
scores every earlier token by q.k, scales by sqrt(d), masks the future,
softmaxes into weights, and blends the values: **soft retrieval, inside the
model, at every position of every layer**. Then beat two: the FFN transforms
each position alone (the part Module 4 slices into experts), with residuals
carrying h through both beats.

## See it (no key)
`widgets/attention-lens/index.html` - two passes:
- **intuition (9 steps):** ' is' as an empty island; attention arcs with
  computed weights (0.356 to ' France', 0.332 to ' capital'); everyone attends
  backwards at once; the causal wall; the librarian from course 1, recomposed;
  values as payloads; the enriched h; the two-beat layer repeated x80.
- **mechanism (19 steps, 3 acts):** act 1 computes ONE head end to end on toy
  4-dim vectors - dots, sqrt(d) scaling, the mask, softmax, the blended
  output, the residual add - every number checkable with a pocket calculator.
  Act 2 scales to reality (Llama-3-70B, verified: 64 heads x 128 = d 8192,
  80 layers): parameter counts computed live, GQA and why it exists (the KV
  cache), and the n^2 wall computed for 1k/8k/128k contexts. Act 3 zooms out
  to the two-beat layer, the residual stream, and the division of labor:
  attention chooses WHERE, the FFN chooses WHAT, Module 4's router chooses WHO.

## The aha
Attention is RAG the model was born with - and the "magic" is three learned
matrices agreeing on a code, plus one softmax.

## Honest notes
- Toy q/k/v vectors are hand-authored (d_head = 4 for readability); every
  derived number is computed live.
- "Heads with obsessions" (syntax head, entity head) is a useful cartoon;
  real heads are found, not designed, and most defy clean labels.
- Real shapes are Llama-3-70B's, verified against its published config.
  DeepSeek-V3 replaces this exact design with MLA - Module 5's story.

## Done when (the bar for this module)
Given toy q and k vectors, you can compute one attention weight by hand
(dot, scale, softmax) and say what the causal mask zeroes. `CHALLENGE.md`.

## Next
Module 3 prices what this module deferred: keeping every k and v around -
the KV cache. (Module 4, already built, slices the FFN this module located.)
