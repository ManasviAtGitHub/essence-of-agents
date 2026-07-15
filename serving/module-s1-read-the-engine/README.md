# S1 - Read the real engine

*Verified as of 2026-07. An inference engine is a file you can read.*

Tracks 1-4 all did the same thing without ever saying so: they CALLED a model
and got tokens back. This track opens what they called. And the first surprise
is how small it is - an inference engine is a forward pass, about fifteen lines
of C. You already built every line of it, in the models track.

## Question
When your agent sends a prompt and gets a token back, what code actually ran?
Not a diagram of it - the code. And what single thing separates a toy that
generates one token from a system that can serve thousands?

## Principle
**An inference engine is M0's loop + M2's attention + M3's cache, transcribed
to C - and one line turns it from a demo into a server.** `forward(token, pos)`
does exactly what the models track drew: embed the token (M1), project it to a
query/key/value, attend over the past (M2), a residual, an MLP (M4), a residual,
and unembed to a score per vocabulary token (M0). The caller samples, appends,
and calls again - M0's loop.

The one line is the **KV cache**: `cache_k[pos] = k; cache_v[pos] = v;`. Keys
and values depend only on a token and its position, so they never change - store
them once and every future token reuses them as-is. Without it, generating token
n redoes tokens 1..n-1 first: O(n) work per token, quadratic over a sequence.
With it, each token is O(1) new work. That line is the difference between a demo
and something you can serve - which is why this whole track exists.

## Dated exhibits (rule 10)
- **karpathy/llama2.c** (2023, still canonical): Llama inference in ~700 lines
  of pure C (`run.c`) - explicitly for ~100M-1B micro-LLMs on phones, browsers,
  laptops, MCUs. The readable production ancestor of what we run here.
- **llama.cpp / GGUF** (ggml-org, ongoing): the same forward pass grown up -
  quantized weights, `mmap`, Metal/CUDA/Vulkan backends. S2 opens it.

## See it (no key)
`widgets/read-the-engine/index.html`. Two modes over ONE real model - the
course's `nanomodel` (~1,130 weights) trained offline on "the capital of france
is paris" (loss 2.9 -> 0.03), then RUN here live. Every number on screen is
computed by the forward pass, not simulated (rule 13).
- **The walk:** the real C of `forward()` on the left; as a token flows through
  it, the exact lines light up and the vectors (h, q, k, v, scores, weights,
  logits) appear on the right - real values. The KV-cache line gets its own
  beat: watch the shelf gain a column that is reused, never rebuilt.
- **Run it:** the same engine generates "the capital of france is paris." token
  by token. The cache grows; a live chart shows the work you SKIP by caching
  (red, O(n)) against what you pay (green, O(1)).

## The aha
The thing every track called a "model" is a file you can read top to bottom in
an afternoon. Hosting is not magic - it is this forward pass, plus the one line
that lets you reuse the past.

## Done when
The learner can name what `forward()` does in one pass, point to where the KV
cache is written and where it is read, and explain why that one line changes
per-token cost from O(n) to O(1).

## Honest notes
- Our engine is the nanomodel's exact math: one head, one block, a learned
  position embedding, a tanh MLP. Production `run.c`/llama.cpp add RMSNorm, RoPE
  positions, SwiGLU, and dozens of stacked layers - same shape, more of it (S2).
- The cache gives *identical* outputs to full recompute (it is exact reuse, not
  an approximation) - the only thing it changes is the cost.
- Weights are trained offline and embedded (the llama2.c workflow: train in one
  place, run the weights in C). No network, no key - it runs from the file.
