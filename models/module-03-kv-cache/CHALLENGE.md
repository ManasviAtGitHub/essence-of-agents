# By hand - weigh the cache

The formula, once more:
`cache bytes = 2 x layers x kv_heads x head_dim x bytes x tokens`

## 1. Bytes per token
Compute KV cache bytes per token for each:
- a) Llama-3-70B: 80 layers, 8 KV heads, head_dim 128, fp16 (2 bytes).
- b) A 7B model: 32 layers, 8 KV heads, head_dim 128, fp16.
- c) The 70B WITHOUT GQA: 64 KV heads (else same). How many times bigger
  than (a)?

## 2. A whole context
Using (1a), what is the total cache for:
- 4,096 tokens?  - 128,000 tokens?
Express each in GB (1 GB = 1e9 bytes).

## 3. Does it fit?
The 70B weights are 70e9 x 2 bytes = 140 GB. An 80 GB GPU obviously cannot
even hold the weights alone at fp16 - so it is sharded across cards. On a node
with 320 GB total, how much room is left for KV cache after the weights, and
roughly how many tokens of context does that allow (using 1a)?

## 4. The GQA question
GQA shares KV heads across query heads. Llama-3-70B has 64 query heads and 8
KV heads.
- By what factor does GQA shrink the cache versus one-KV-head-per-query-head?
- Queries are NOT cached, only K and V. Why does that make GQA a memory win
  specifically (not a compute win)?

## 5. Prompt caching
Two API requests start with the same 2,000-token system prompt, then differ.
- Which tokens' K,V can be reused between them, and which must be recomputed?
- If you put a changing timestamp at the START of the system prompt instead of
  the end, what happens to the cache hit, and why? (This is the production
  track's caching chapter, from the inside.)

## Stretch
- Derive why decode is "memory-bound": count the new FLOPs per decode step
  versus the bytes read from the cache, at 100k tokens of context.
- Sketch how you would EVICT tokens when the cache is full (which to drop,
  and what the model loses). Real systems call this KV-cache eviction /
  windowed attention.
