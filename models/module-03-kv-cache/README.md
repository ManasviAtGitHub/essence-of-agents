# Module 3 - The KV cache: why context costs memory

The first token takes a beat; the rest stream fast. Long context costs money
even when the text is unchanged. Both facts come from one place: to look back
(Module 2), the model must REMEMBER every past token's keys and values.

## Question
Why is the first token slow and the rest fast? And why does a long context
cost real money, continuously, for the whole conversation?

## Principle
At generation, each new token's attention needs the K and V of every earlier
token. Recomputing them every step is O(n) passes per token - quadratic waste -
so we **cache** them. That splits generation into **prefill** (compute the
prompt's K,V in one parallel pass - compute-bound, the first-token pause) and
**decode** (one token at a time against the cache - memory-bound, the fast
streaming). The cache grows with every token and lives in GPU memory, so the
"context window" is really a **memory budget**.

## See it (no key)
`widgets/kv-cache/index.html` - two passes:
- **intuition (9 steps):** the first-token asymmetry, the naive recompute
  (red flash), the cache fix (blue keys, gold values), prefill vs decode, and
  the cache ballooning to ~43 GB at 128k on top of 140 GB of weights - context
  window = memory budget.
- **mechanism (18 steps, 3 acts):** act 1 contrasts prefill (parallel,
  compute-bound) and decode (one-by-one, memory-bound). Act 2 counts the bytes
  live: `2 x layers x kv_heads x head_dim x bytes x tokens` = 320 KB/token for
  Llama-3-70B, with a clickable context picker (8k/32k/128k) and the shared-vs-
  unshared-heads comparison (8x saving - grouped-query attention, GQA, owned
  here as the memory win). Act 3: reuse a stored prefix cache (met as "prompt
  caching" if you did the other track), serving is memory-bottlenecked, the
  out-of-memory wall is the true context limit, and a later module (DeepSeek's
  MLA) is previewed as the next attack on the formula.

## The aha
A context window is not a text limit - it is a memory limit. Every token you
keep costs GPU memory, forever, for the whole conversation.

## Honest notes
- Every byte figure is computed live from Llama-3-70B's verified shape
  (80 layers, 8 KV heads via GQA, 64 query heads, head_dim 128, fp16): the
  formula and all totals are real arithmetic. The example sentence is
  illustrative.
- GB = 1e9 bytes, KB = 1e3, for clean decimal figures.

## Done when (the bar for this module)
Given a model's layers, KV heads, head_dim, and dtype, you can compute its KV
cache bytes per token by hand - and the total for a given context length.
`CHALLENGE.md`.

## Next
Module 4: MoE - why the biggest models have hundreds of billions of parameters
but only pay for a few billion per token. (Then Module 5's MLA returns to this
module's formula and shrinks the cache itself.)
