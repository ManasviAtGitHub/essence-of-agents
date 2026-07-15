# S4 - Run it in the browser

*Verified as of 2026-07. A real model, no server, no key.*

S1 read the engine, S2 made it fast, S3 shipped it as a file - but every step
still ended in "download it and run it". This module removes even that: a real
model runs inside a web page, on your own GPU, with no server and no install.
And because this course IS a web page, you can run one right here.

## Question
Can a real language model run with zero install and zero server - entirely
inside a browser tab? And if so, what does it cost, and what fits?

## Principle
**WebGPU gives the browser real GPU compute, so a real quantized model runs
client-side.** A library (transformers.js or WebLLM) fetches the weights ONCE,
caches them in the browser, and from then on runs the forward pass (S1) on your
GPU via WebGPU - which is S2's warehouse floor, reached from JavaScript - or on
your CPU via WASM (S2's SIMD lanes) if there is no WebGPU: same model, ~5-10x
slower. It is **private** (text never leaves the tab), **offline** (after the
one download), and **keyless**.

Being the most restricted host is what makes it a great teacher: every cost from
S0-S2 becomes something you feel on your own hardware. The download size is
S2's bytes made concrete (135M ~90 MB, 0.5B ~400 MB, 1.7B ~1 GB); the tok/s you
measure is S0's bandwidth clock; and what will even load is S0's "fits and
flows", on the tightest machine there is.

## Dated exhibits (rule 10)
- transformers.js v3 (Hugging Face, WebGPU + WASM, 1200+ ONNX models) and WebLLM
  (mlc-ai) - the two in-browser inference engines.
- WebGPU: solid in Chrome/Edge; Safari and Firefox catching up; WASM as the
  universal fallback.
- Small ONNX models: SmolLM2-135M (~90 MB), Qwen2.5-0.5B (~400 MB), Llama-3.2-1B.

## See it (no key)
`widgets/browser/index.html`. **The teaching** (a deterministic sim): no server
at all, how WebGPU + real weights work, private and keyless, the download-size
tiers, and the payoff. **What it costs:** WebGPU vs WASM, the bandwidth wall
felt as tok/s falls with model/context (S0), what fits in the tab's memory
budget, and where the browser wins vs loses. **Run the real thing** (the panel
below, rules 13-14): click to lazy-load transformers.js from a CDN and run a
real small model on your GPU (WASM fallback) - downloaded once, cached, offline
after, nothing leaving your machine. The measured tok/s is your own hardware's
clock. This panel is the course's ONLY runtime network fetch - opt-in and
skippable; the teaching stands without it.

## The aha
A real language model runs in a browser tab, on your GPU, private and offline -
and the numbers it prints are S0's and S2's costs, measured on your machine.

## Done when
The learner has run a real model in their browser (or understands the panel),
can read its measured tok/s as S0's clock, and can say why WebGPU beats WASM and
why model size decides what fits.

## Honest notes
- The "Run the real thing" panel needs a network for the FIRST download and a
  browser with WebGPU (or it falls back to slower WASM). If offline or the CDN
  is blocked, it degrades gracefully and the teaching still stands (rule 14: the
  one external dependency is quarantined, opt-in, and never load-bearing).
- Real tok/s depends entirely on the viewer's hardware; there are no baked-in
  numbers here - the panel measures what actually happens.
