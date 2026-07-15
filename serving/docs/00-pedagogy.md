# Essence of Serving - pedagogy

Track 5. Read this doc before building any module. Factual basis: the 2026
local-inference + in-browser landscape (llama2.c, llama.cpp/GGUF, llamafile,
transformers.js v3, WebLLM, vLLM/SGLang), verified as of 2026-07.

## The bridge

Track 1 built a loop around a model. Track 2 hardened it. Track 3 opened the
model. Track 4 read the frontier and designed one. Every one of those tracks
CALLED a model and got tokens back - and never once asked WHERE that call
lands. This track answers it: a model is weights + a loop (you built both),
and hosting it is a systems problem. We open the real engine, make it fast,
ship it as one file, run it in the learner's own browser, and rack a thousand
of them. F8 printed the serving bill; this track pays it.

## The thesis (the one sentence this track defends)

**Every model call your agent makes lands on an engine - and hosting is
making that engine fast, portable, and cheap at scale, which you can read,
ship, and run yourself.**

Track 3 told you what one forward pass computes. Track 5 is the two things
between those weights and a happy user: making one instance fast (read the
engine, quantize it, kernel it) and packing many users onto it (batch, page,
schedule, bill).

## The recurring primitive

**The engine on the workbench -> the server rack.** One real inference engine
sits on the bench (llama2.c - ~700 lines you can read). Each module tunes,
ships, or multiplies it, and the same engine scales from one instance the
learner runs in a tab to a fleet serving thousands. Every module places
itself on that bench-to-rack line ("here is the engine; here is what this
module does to it"); the capstone racks it for real.

## THE NON-OBVIOUS CLAUSE - why visualization carries more here (read twice)

Tracks 1-4 taught ideas with a foothold in intuition: a loop, attention
looking back, a menu of tokens. **Serving has none of that.** "Decode is
memory-bandwidth-bound," "continuous batching," "paged attention," "the
kernel tiles the matmul" - these are invisible systems behaviors with no
everyday analog. A learner cannot picture them, so a CHART of the concept
teaches nothing; it just labels a mystery.

Therefore the load shifts. In this track **the visualization is not an
illustration of the point - it IS the point.** Each non-obvious concept gets
a PHYSICAL, SPATIAL metaphor that makes the invisible thing move on screen,
so the learner's eye discovers the mechanism before the caption names it.
This is rule 15 below, and it is the make-or-break of the whole track. If a
module's central image is a bar chart or a labeled box diagram, it has
failed the clause - go back and find the embodiment.

The per-concept metaphors are fixed here so the track stays coherent:

- **Bandwidth is the clock (S0, S2):** NOT a "bandwidth meter". The weights
  are a physical PILE that must be dragged, whole, through a narrow DOORWAY
  once per token. The GPU's compute is a lightning-fast worker who stands
  IDLE at the far side, starving, because the doorway (bandwidth) can only
  pass so many boxes per second. "Memory-bound" becomes visceral: the fast
  worker waiting on the conveyor. Quantization shrinks the boxes; more pass
  per second; the worker waits less.
- **The engine is readable (S1):** the real C source and the animation are
  SYNCED - as a token flows through run.c, the exact lines light up and the
  KV-cache shelf fills. You read the engine and watch the data at once.
- **The kernel (S2):** a matmul as a floor of workers on a grid of tiles.
  Scalar = one worker filling cells one at a time; SIMD = a ROW of workers
  (lanes) doing 8 cells at once; GPU = the whole warehouse floor at once.
- **Portability (S3):** one file as a shape-shifting key that fits every OS
  lock at once (Win/mac/Linux/phone); then Claude Code's T1 loop unplugs
  from the cloud and plugs into the local file.
- **The browser (S4):** the real model, really running - the download fills
  a tank, then the tab becomes a self-contained engine printing real tokens.
- **Continuous batching (S5):** the GRIDDLE. Static batching = the cook waits
  for the whole batch of patties to finish before starting the next batch
  (empty griddle spots = wasted GPU). Continuous = new patties drop onto
  spots the instant they free - the griddle stays full. GPU utilization is
  griddle-fullness, and you SEE the idle spots in the static case.
- **Paged KV cache (S5/S6):** a LOCKER wall. Naive = each conversation gets
  one long fixed shelf, so short chats leave big empty gaps (fragmentation);
  paged = fixed-size lockers handed out on demand, shared prefixes share a
  locker. Virtual memory made physical.
- **The bill (S6):** a taxi METER running while a load curve lights and dims
  a rack of GPUs; TTFT is the wait for the first bite, TPOT the chewing pace.

If a new concept appears without a metaphor, inventing one is the FIRST build
step, not an afterthought.

## Depth contract - inherited + serving rules

Rules 1-12 apply unchanged (models + frontier contract: intuition+mechanism
passes, act structure, live-computed arithmetic, verified/illustrative-
labeled numbers, done-when bar, one worked example, origin story per object,
the visual carries the claim, cast as epistemic proxies, one thread with
park/resume, date-stamp exhibits, secondary numbers stay narrative color,
teach arguments not winners). THREE new rules, because this is the first
track that touches REAL hardware, a REAL engine, and a REAL model:

13. **Simulate the fleet, run the instance.** Any claim about ONE model -
    tok/s, KV growth, a quantization delta, the WebGPU-vs-WASM cliff - is
    demonstrated on a REAL running model (the llama2.c port or a real
    in-browser model), measured on the learner's own machine. Any claim
    about MANY users - continuous batching, paged attention, fleet economics
    - is DETERMINISTIC SIMULATION, and its inputs are the learner's own
    measured single-instance numbers. Never fake a number you could measure;
    never present a sim as a measurement.

14. **The one external dependency is quarantined.** Real model weights are
    the course's ONLY remote fetch (everything else is vendored offline).
    They are: lazy-loaded on an explicit "run the real thing" click, cached
    forever after first load (Cache API / IndexedDB), WASM-fallback so
    no-WebGPU browsers still work, and never on the critical path of any
    other track or any deterministic sim widget. A learner who never clicks
    "run" still completes the track; the four other tracks load none of it.

15. **The visualization is the explanation (the non-obvious clause).** Every
    central concept is embodied in a physical/spatial metaphor that makes the
    invisible mechanism move on screen (see the fixed list above), so the eye
    discovers it before the caption. A labeled box-diagram or a bare bar
    chart of a non-obvious concept is a failed build. Motion and space do the
    teaching; text confirms.

## Visual grammar - the three-layer stack + the real-inference layer

The frontier three-layer stack carries over (all vendored, offline):
- **p5** - the MOTION/METAPHOR layer, and in THIS track it is primary (rule
  15): the doorway + pile, the griddle, the locker wall, the warehouse floor,
  the token flowing through run.c. Use the crispness pattern (density =
  max(2, devicePixelRatio), polled per frame).
- **D3** - the DATA-TRUTH layer: the roofline, tok/s-vs-context, the fleet
  cost curve. Anything the learner READS or that carries computed numbers.
  In this track D3 confirms what the p5 metaphor already showed - it does not
  lead.
- **Rough.js** - the BLUEPRINT layer: the serving stack being designed in the
  capstone before commit (sketch -> ink).

Plus one NEW, quarantined layer (rule 14):
- **The real-inference layer** - transformers.js / WebLLM, lazy-loaded ONLY
  inside "run the real thing" panels. Two real artifacts use it: the llama2.c
  JS/WASM port (S1) and the in-browser model (S4, S7). The llama2.c source
  walk itself is DOM (annotated, scrollable C), not canvas.

DOM keeps captions, trace panels, cast, the annotated source, and controls.

## Cast

- **Bit becomes the engineer.** Bit built the loop (T1), hardened it (T2),
  opened the model (T3), designed one (T4). Here Bit opens the HOOD - reads
  the real engine, tunes it, ships it, racks it. Bit is at the workbench in
  S1 and at the server rack in S7.
- **Cortex is the engine being hosted.** The chip-brain from tracks 3-4 is
  now the thing on the bench - quantized (fewer bits; it reacts), kernelled,
  packed into a batch beside copies of itself, racked. No new insides; this
  is Cortex being RUN, not rewired. In the doorway metaphor, the pile of
  boxes IS Cortex's weights.
- **No new character.** Frontier added Somni; this track adds none - the
  co-star is the learner's own machine (the real tok/s it produces).

## Module breakdown (each: Q / principle / metaphor / build / aha / done-when)

### S0 - The hosting problem (extends M3; opens the agent hook)
- Q: your agent (T1/T2) fires thousands of model calls. Where does one land,
  and why is it slow and expensive?
- P: a call is a forward pass; a pass is bounded by MEMORY BANDWIDTH, not
  math (M3's decode lesson, at the hardware level). Where it can run - cloud
  GPU / laptop / phone / browser - is set by how many bytes move per token.
  Three questions frame the track: is it FAST (S0-2), PORTABLE (S3-4), does
  it SCALE (S5-6)?
- Metaphor: the doorway + the pile + the idle worker (rule 15).
- Build: intuition = one token = drag the whole weight-pile through the
  bandwidth doorway while the compute-worker waits; a spectrum slider (cloud
  -> browser) rescales the pile and the doorway. Mechanism = the roofline
  (compute vs bandwidth), computed for a real small model. D3 confirms.
- Aha: the model is weights + a loop; hosting is moving bytes fast enough,
  and that decides where it can live.
- Done when: given a model size and a bandwidth, the learner can say whether
  decode is bandwidth- or compute-bound and estimate tok/s to an order.

### S1 - Read the real engine (llama2.c)  [FORMAT-SETTER, REAL]
- Q: what IS an inference engine, concretely - not a diagram, the code?
- P: it is the loop you already know, in ~700 lines of C. run.c is: load
  weights -> for each position, one forward pass (RMSNorm, QKV, attention
  over the KV cache, FFN, logits) -> sample -> append -> repeat (M0's loop,
  M2's attention, M3's KV cache, all real). No framework - the essence of
  hosting is this file.
- Metaphor: source-synced-to-flow (rule 15) - the real C lines light as a
  token flows through them; the KV shelf fills as attention runs.
- Exhibits: karpathy/llama2.c (canonical ~700-line pure-C inference, aimed at
  ~100M-1B micro-LLMs on edge/browser/laptop); GGUF/llama.cpp as the
  production descendant.
- Build: intuition = an annotated scroll of run.c's forward() with each block
  lit as the token passes (DOM code + p5 token). Mechanism = a REAL tiny
  model (the nanomodel weights or a small GGUF) run through a JS/WASM PORT of
  run.c live in the page - the learner watches a real forward pass emit a
  real token and can step it. Rule 13: measured, not simulated.
- Aha: an inference engine is not a black box - it is M0's loop + M2's
  attention + M3's cache, transcribed to C. You can read every line.
- Done when: the learner can name what run.c does in one forward pass and
  point to where the KV cache is stored and reused.

### S2 - Make it fast: quantization + the kernel (builds ON M8)
- Q: M8 showed fewer bits = fewer bytes. WHY does that make it faster, and
  where does the time actually go?
- P: decode is bandwidth-bound (S0), so fewer bits per weight = fewer bytes
  per token = proportionally faster - that is what quantization BUYS at serve
  time (not just smaller disk, which M8 covered). The time lives in ONE
  operation, the matmul; making it fast is the KERNEL story: SIMD lanes on
  the CPU, tiling on the GPU, the same tiling as a WebGPU compute shader.
- Metaphor: the pile shrinks at the doorway (from S0) + the warehouse floor
  of tile-workers (rule 15).
- Exhibits: GGUF k-quants (Q4_K_M...), KV-cache quantization (fp8 KV),
  AWQ/GPTQ; flash-attention as the canonical fused kernel.
- Build: intuition = the same weight matrix at 16/8/4 bits, the doorway
  passing 4x more boxes at int4, live bytes/token + tok/s (builds on M8's
  byte math, adds SPEED). Mechanism = a matmul scalar vs SIMD-row vs
  GPU-floor, animated; the roofline shifting. D3 for precision -> bandwidth
  -> tok/s.
- Aha: quantization is a serving lever, not just a size trick - and all the
  speed lives in one matmul kernel.
- Done when: the learner can explain why int4 decode moves ~4x less memory
  than fp16 and what a kernel tiles.

### S3 - Ship it anywhere: one portable file (llamafile)
- Q: you have a fast engine and a weights file. How do you SHIP it so anyone
  runs it, no install?
- P: fold engine + weights into ONE file that runs on every OS and CPU.
  llamafile = llama.cpp + Cosmopolitan Libc compiled to an APE (Actually
  Portable Executable), one binary valid on Windows/macOS/Linux/BSD at once.
  It speaks the Anthropic Messages API, so the harness from course 1 (Claude
  Code) can point at a LOCAL model and run fully offline.
- Metaphor: the shape-shifting key in every OS lock; then the T1 loop
  unplugging from cloud, plugging into the local file (rule 15).
- Exhibits: llamafile 0.10.0 (2026 - Metal + CUDA in one stable file), its
  Anthropic-API-compatible local server, llama.cpp/GGUF ecosystem.
- Build: intuition = engine + weights merge into one icon that lands on
  Win/mac/Linux/phone tiles. Mechanism = llamafile serving the Anthropic API
  on localhost; Claude Code's loop now hitting it offline - the course eating
  its own tail.
- Aha: hosting can collapse to one file, and a local model is a drop-in for
  the cloud API your agent already speaks.
- Done when: the learner can say what an APE is and why a local
  Anthropic-API server means offline agents.

### S4 - Run it, zero install: the browser  [REAL]
- Q: can a real model run with NO install and NO server - in a web page?
- P: yes - WebGPU gives the browser real GPU compute; transformers.js/WebLLM
  run a real quantized model client-side. Private (weights never leave the
  tab), offline after first load, keyless. The most-restricted host, so it
  makes every serving cost VISIBLE on the learner's own machine.
- Metaphor: the download fills a tank, the tab becomes a self-contained
  engine printing real tokens (rule 15); the bandwidth doorway from S0, now
  the learner's actual GPU.
- Exhibits: transformers.js v3 (WebGPU, 1200+ models), WebLLM (mlc-ai); the
  WebGPU support reality (Chrome/Edge solid, Firefox flag, Safari
  inconsistent -> WASM fallback mandatory).
- Build: intuition = pick a tier (135M / 0.5B / 1.7B), watch it download once
  and generate real tokens, live tok/s + memory. Mechanism = the SAME model
  at different context lengths and backends (WebGPU vs WASM), tok/s measured
  live - the S0 bandwidth wall, felt. Rules 13/14.
- Aha: a real LLM runs in a tab with no server - and the browser's limits
  make the serving story tangible.
- Done when: the learner has run a real model and can report its tok/s and
  why WebGPU beat WASM.

### S5 - Serve many: batching + paged attention (extends M3)
- Q: one tab serves one user. How does a datacenter serve thousands on one
  GPU?
- P: pack them. Static batching wastes the GPU (it waits for the slowest);
  CONTINUOUS (in-flight) batching admits and retires requests every step,
  keeping the GPU full - the single biggest serving win. And the KV cache
  (M3) is PAGED like virtual memory (PagedAttention) so many sequences share
  memory without fragmentation and shared prefixes store once (M3's
  prompt-cache, at fleet scale).
- Metaphor: the GRIDDLE (static vs continuous) + the LOCKER wall (paging),
  rule 15.
- Exhibits: vLLM (PagedAttention), SGLang, TensorRT-LLM; continuous batching
  as the industry default.
- Build: intuition = tickets arriving at random; static (a griddle spot idles
  waiting for the batch) vs continuous (spots refill instantly) - the
  GPU-utilization meter is griddle-fullness. Mechanism = the paged KV lockers
  allocated/freed/shared, throughput computed. Speculative decoding appears
  here as ONE panel callback to M5, not a module.
- Aha: serving is a packing problem - throughput is the product; continuous
  batching + paging are how you pack.
- Done when: the learner can explain why continuous batching beats static and
  what a KV page is.

### S6 - The fleet & the bill (pays F8's bill; closes the agent hook)
- Q: what does it COST to serve your agent to a lot of people, and what are
  the knobs?
- P: the fleet is a queue + replicas. Latency splits into TTFT (prefill) and
  TPOT (decode) - opposite hardware profiles, so labs DISAGGREGATE prefill
  and decode onto different machines. Autoscaling trades cold-starts against
  idle cost; spot vs reserved trades price against reliability; it all rolls
  to $/1M tokens - the number F8 pointed at. This is why your agent costs
  what it costs.
- Metaphor: the taxi meter + the load curve lighting/dimming a GPU rack; the
  first-bite wait (TTFT) vs chewing pace (TPOT), rule 15.
- Exhibits: prefill/decode disaggregation (2025-26), $/1M-token economics,
  autoscaling patterns.
- Build: intuition = a load curve driving replicas up/down, the queue backing
  up when under-provisioned (p5 tickets + D3 latency/cost). Mechanism = the
  bill: QPS x context x tokens -> GPU-hours -> $, computed live, disaggregated
  vs not. Rule 11: numbers illustrative/labeled.
- Aha: serving economics is throughput vs latency vs cost, and every trick in
  this track is a lever on that triangle - which is your agent's bill.
- Done when: the learner can name TTFT vs TPOT and one lever trading latency
  for cost.

### S7 - CAPSTONE: Host it yourself  [REAL instance drives grounded sim]
- Q: can you take one design all the way - a real model running, and a fleet
  priced from what it really did?
- P: the whole track in a loop - CHOOSE (a model tier + backend + quant),
  RUN (a real model in your browser: the single-instance truth), MEASURE
  (your tok/s, TTFT, memory, backend), SCALE (a simulated fleet extrapolates
  1/10/1000 users and $/day FROM your measurement), COMPARE (settle beside a
  real 2026 stack - vLLM / llamafile / WebLLM). The fleet is a sim, but
  grounded in a real number YOU produced - honest per rule 13.
- Metaphor: the workbench becomes the rack; your one real engine multiplied,
  the taxi meter now summing the whole rack.
- Build: a console - model-tier selector (download-size IS the lesson; grab
  two and compare), a live in-browser run with a real dashboard, a D3 fleet
  projection driven by the measured tok/s, a Rough.js blueprint of the chosen
  stack inking on commit, a "you hosted a model like X" settle. The runnable
  counterpart of the track (with S1's llama2.c port).
- Aha: you read an engine, made it fast, shipped it, ran it for real, and
  priced a fleet from your own machine - you can host a model from first
  principles.
- Done when: the learner has run a real model, read its true tok/s, and
  explained what serving 1000 users of it would cost and why.

## Layout & build order

Directory `serving/`, modules `module-s0-...` through `module-s7-capstone`,
hub `serving/index.html` (mirrors the frontier/models hubs). Read-order
applies: each module references only S-modules before it + tracks 1-4.

1. **S1 first (format-setter).** It establishes the track's identity - the
   REAL engine on the bench - and the two hardest patterns: the annotated-C
   code-walk and the real running port under rules 13/14. Everything else
   calibrates to it.
2. Then S0 (the frame + the doorway metaphor), S2 (fast), S4 (the browser -
   second real artifact), S3 (ship), S5-S6 (the fleet), S7 (capstone).

Rationale: S1 and S4 carry the rule-13/14 real-inference machinery; building
S1 first proves the quarantine works before the rest leans on it.

## Honesty rules (in addition to 10-15)

- **Label every number real vs illustrative, on screen.** Measured (S1/S4/S7
  live runs) says "measured on your machine"; simulated (S2/S5/S6) says
  "illustrative" / "simulated". Never blur them - the F8 lesson: a run that
  only honors part of the design reads as fake.
- **Perf numbers age; ratios do not.** Absolute tok/s and $/1M-token figures
  are hardware- and version-specific - lead with SHAPES and RATIOS (int4 is
  ~4x less traffic; continuous batching multiplies throughput) and date-stamp
  any absolute (rule 10).
- **The quarantine is a promise (rule 14).** If the real model ever becomes
  load-bearing for a non-S widget, it is a bug. It is opt-in, cached,
  WASM-fallback, skippable.
- **The metaphor must be honest too (rule 15).** A physical metaphor that
  misleads (implies a wrong mechanism) is worse than a chart. Every metaphor
  is checked against the real behavior before it ships.
