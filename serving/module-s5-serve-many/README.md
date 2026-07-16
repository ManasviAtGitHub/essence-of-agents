# S5 - Serve many

*Verified as of 2026-07. Keep the GPU full, pack the cache.*

S4 served one user in one tab. A datacenter serves thousands - on the SAME
expensive GPU. That is not a bigger version of one instance; it is a new
problem: packing. Two mechanisms do almost all of the work.

## Question
Reading the weights across S0's doorway costs the same for one user or many. So
how do you serve thousands of users on one GPU without it costing thousands of
times as much?

## Principle
**Batch to amortize the doorway, and pack the KV cache so more requests fit.**
- **Continuous batching (keep the griddle full).** One trip through the doorway
  per step serves the whole batch - so the weight-read cost is split across every
  request. STATIC batching wastes this: it runs a batch to completion, and
  because requests finish at different lengths, finished slots sit IDLE until the
  batch clears. CONTINUOUS (in-flight) batching retires finished requests and
  admits waiting ones every step, so the GPU never idles - the single biggest
  throughput win, and the default in vLLM and SGLang.
- **Paged attention (pack the cache like lockers).** With the griddle full, the
  limit becomes memory: every batched request needs its own KV cache (S1, M3).
  Reserving a max-size contiguous block per request fragments memory - short
  replies leave big empty gaps. PagedAttention breaks the cache into fixed-size
  PAGES handed out on demand (OS virtual memory, applied to attention), so there
  is no waste and far more requests fit. And pages can be SHARED: a common system
  prompt's pages are stored once and pointed at by many requests - Module 3's
  prompt caching, at fleet scale.

## Dated exhibits (rule 10)
- vLLM - PagedAttention and continuous batching, the reference open serving
  engine. SGLang, TensorRT-LLM - the same ideas, production-grade.
- Speculative decoding (M5's draft-and-verify) as a further throughput lever in
  the batched loop.

## See it (no key)
`widgets/serve-many/index.html`. **Keep the griddle full:** the GPU as an
8-slot griddle - static batching leaves finished slots IDLE (utilization drops,
you pay for empty spots); continuous batching refills freed slots every step
(the griddle stays full, utilization high). **Pack the cache:** the naive
reserved-block fragmentation, then fixed-size pages handed out on demand, then a
shared prefix block pointed at by many requests - and the payoff, one GPU
serving many users.

## The aha
Serving many is a packing problem: keep the GPU busy (continuous batching) and
fit as many KV caches as possible (paged, shared). Throughput is the product.

## Done when
The learner can explain why static batching wastes the GPU and continuous
batching does not, what a KV page is and why paging beats reserving a block, and
how a shared prefix saves memory.

## Honest notes
- The griddle and locker wall are metaphors for real vLLM/SGLang mechanisms; the
  8 slots, utilization percentages, and page sizes are illustrative (rule 11).
- Continuous batching + paging genuinely multiply throughput (the real reason a
  frontier model can be served affordably at all); the exact multiple depends on
  request-length distribution and memory.
