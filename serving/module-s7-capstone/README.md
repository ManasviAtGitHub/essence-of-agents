# S7 - CAPSTONE: Host it yourself

*Verified as of 2026-07. Read it, make it fast, ship it, run it, rack it.*

The whole track, in one console. You designed nothing until now - you watched.
Here you make the choices: pick a model, a quantization, a backend, a
deployment; run a real model on your own machine; and scale your design to a
fleet whose cost is projected from the track's formulas (the single-instance run
itself is really measured). Your setup settles beside a
real 2026 serving stack.

## Question
Can you take one design all the way - a real model actually running, and a fleet
priced from what it really does - and say which real-world stack you just built?

## Principle
**The track is a loop: read it (S1) -> make it fast (S2) -> ship it (S3) -> run
it (S4) -> rack it (S5-S6) -> price it.** The console runs that loop:
- **Design.** The dials are the levers you learned: model size and bits (S2's
  pile), backend (S2/S4's kernel - WebGPU or WASM), deployment (S5's single
  stream vs batched fleet). Each recomputes the pile (S0/S2), the single-stream
  tok/s (S0's clock), the served throughput (S5's batching), the $/1M tokens
  (S6), and whether it fits in a browser tab (S4).
- **Run (real).** One button runs the course's own nanomodel - a real
  transformer (S1) - live and TIMED, and reports the tokens/sec YOUR machine
  actually did. That is the honest single-instance measurement (rule 13); the
  projection is built on that same idea, scaled to your chosen tier.
- **Scale.** Pick a user count; the console projects tokens/day, GPUs needed, and
  cost/day from the served throughput (S6's arithmetic).
- **Settle.** Your dial choices name the real 2026 stack you just described -
  WebLLM/transformers.js (S4), llamafile (S3), or vLLM/TensorRT-LLM (S5-S6).

## See it (no key)
`widgets/host-it-yourself/index.html`. Turn the dials and watch every number
recompute; press "run the real engine" to generate real tokens and read your
machine's real tok/s; set a user count and see the fleet's daily cost; and read
which real stack your design resembles. The single-instance run is real
(measured); the tier and fleet numbers are illustrative projections built from
the track's own formulas (labeled).

## The aha
You read an engine, made it fast, shipped it, ran it for real, and priced a
fleet from your own machine. Hosting a model is not magic - it is a pile of
bytes, a doorway, a kernel, a batch, and a bill, and you now hold all five.

## Done when
The learner can run a real model, read its true tok/s, turn the dials to hit a
target ($/1M tokens or "fits in a tab" or "serves 10k users"), and explain which
real serving stack their design corresponds to and why.

## Honest notes
- The RUN is genuinely real and measured (the nanomodel, S1, on your hardware).
  The tier tok/s, $/1M tokens, GPU counts, and daily costs are illustrative
  projections computed live from the track's formulas (S0/S2/S5/S6) with round
  inputs (rule 11) - the shapes and ratios are honest, the absolute dollars are
  not a quote.
- For a bigger real model running in the browser, see S4's WebGPU panel; this
  capstone keeps the always-works nanomodel as its real measurement so it runs
  offline, anywhere, every time.
