# S2 - Make it fast

*Verified as of 2026-07. Shrink the pile, work the floor.*

S0 gave the clock: tokens/sec = bandwidth / bytes. With the SAME hardware there
are exactly two ways to move it - carry fewer bytes, and do the one operation
that dominates faster. This module is both, and both are things the models track
already half-taught you.

## Question
You cannot always buy a faster GPU. So with fixed hardware, what actually makes
a served model faster - and where does all the time go?

## Principle
**Quantize to shrink the pile; write good kernels to work the floor.**
- **Quantization (the pile).** Store each weight in fewer bits (fp16 -> int8 ->
  int4). Module 8 framed this as smaller storage; at serving time it is directly
  more SPEED, because tok/s = bandwidth / bytes and fewer bits means fewer bytes
  through the doorway. int4 is ~4x smaller and ~4x faster, usually with no
  quality you would notice - the mainstream default. Below ~4 bits, precision
  runs out and quality falls off a cliff (M8's warning). The KV cache (S1) is
  numbers too and can be quantized (fp8 KV), so both piles - fixed weights and
  the growing cache - shrink.
- **The kernel (the floor).** The compute unit's work is almost entirely one
  operation: the matrix multiply (M2, M4). A matmul is a grid of output cells,
  each a dot product. Doing it fast is parallelism: SIMD fills a whole ROW of
  cells per instruction (AVX / NEON / WASM-SIMD - how a CPU keeps up); a GPU
  fills the WHOLE FLOOR of tiles at once (why GPUs win - width, not speed per
  worker); WebGPU brings that floor to a browser tab. Fused kernels like
  flash-attention compute attention tile by tile and never store the giant
  scores matrix - less doorway traffic (back to S0) at full floor.

## Dated exhibits (rule 10)
- GGUF k-quants (Q4_K_M and friends), AWQ, GPTQ - the real int4 formats that
  ship in llama.cpp / vLLM, tuned per-layer. fp8 KV-cache quantization (2024-25).
- flash-attention (v2/v3, ongoing) - the canonical fused attention kernel.
- WebGPU compute shaders (Chrome/Edge stable 2023+) - the GPU floor in the browser (S4).

## See it (no key)
`widgets/fast/index.html`. **Shrink the pile:** a 7B model's weight-cells thin
out as you drop fp16 -> int8 -> int4; the pile (GB) and the tok/s ceiling
recompute live (extends S0/M8), the speedup shows, and a quality bar holds until
int2, where it falls off the cliff. **Work the floor:** the same matmul filled by
one worker (scalar), a row of lanes (SIMD), then the whole floor at once (GPU /
WebGPU), with flash-attention as the fused state of the art.

## The aha
Fast is not magic hardware. It is a smaller pile (quantize) and a fuller floor
(the kernel) - two levers on the one equation from S0.

## Done when
The learner can explain why int4 decode is ~4x faster than fp16 (not just
smaller), name the quality cliff, and say what a kernel tiles and why a GPU
beats a CPU on a matmul (width, not per-worker speed).

## Honest notes
- Speedups are the bandwidth-ceiling ratios (int8 ~2x, int4 ~4x); real gains are
  a bit less, and quantization has a small quality cost that the sweet spot
  (near int4) keeps negligible for most models (rule 11).
- The warehouse-floor is a metaphor for real SIMD/GPU/WebGPU kernels; the ~1000x
  is illustrative of GPU parallelism, not a measured figure.
- MoE models (M4) read only a subset of weights per token - a different way to
  shrink the effective pile, same equation.
