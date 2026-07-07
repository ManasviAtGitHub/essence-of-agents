# Essence of Models - pedagogy & design (v1)

The third track. Course 1 (Essence of Agents) built the loop AROUND the model.
Production hardened it. This track opens the model itself: Bit finally looks
inside Cortex. Same engine (assets/ Cast + Anim), same house rules (keyless,
scrubbable, ASCII, honest) - but a different depth contract (below).

## The bridge

Course 1's Module 3 widget ("Why the answer changes") ends at a probability
distribution over the next token. That distribution is the front door of this
track: Module 0 here starts from that exact picture and asks "where did those
bars come from?" One curriculum, one seam.

## The thesis (the one sentence this track defends)

> A language model is a next-token machine. Everything it does - chatting,
> reasoning, refusing - is one distribution over the next token, computed by a
> stack of layers. Architecture decides how much of the machine wakes up per
> token; training decides what the distribution prefers.

## The recurring primitive

**A token flowing through a stack of layers, ending in a distribution.**
Every module is that picture recomposed - never a new diagram:

- tokenization = what enters the stack
- attention = how positions in the stack talk
- KV cache = what the stack remembers between tokens
- MoE = which parts of a layer wake up
- training = what bends the final distribution
- reasoning = spending more trips through the stack before committing

This mirrors course 1 exactly: the agent track's primitive was a while-loop
OUTSIDE the model; this track's is a for-loop INSIDE it.

## THE DEPTH CONTRACT (what "extensive" means - user directive)

This track is a technical deep-dive. The animations themselves carry the
explanation, not just the aha. Concretely, every scene must have:

1. **Two passes, one scene.** A mode pill `intuition / mechanism` on every
   widget. The intuition pass is the course-1-style story (5-9 steps). The
   mechanism pass reuses the same stage but shows the real machinery: tensor
   shapes, the actual equation, real dimension numbers, per-step cost. Same
   diagram, two altitudes - never two diagrams.
2. **Act-structured timelines.** Mechanism passes run 15-30 steps, grouped
   into labeled acts (the scrubber count reads "act 2 . step 4/7"). Long is
   fine; shallow is not. anim.js may need an `acts` option - build it once.
3. **Real arithmetic, computed live.** Any number a learner could check
   (KV-cache bytes, FLOPs per token, active-vs-total params, tokens/param
   ratios) is COMPUTED in JS from stated inputs, with the formula visible -
   never a hand-authored total. The "illustrative" chip is only for what
   genuinely cannot be computed (quality scores, loss curves).
4. **Real architectures as named exhibits.** Each module pins its principle,
   then instantiates it with a real model's published numbers (labeled with
   the source paper, marked VERIFY-AT-BUILD in this doc). Named models are
   dated examples of a principle, so the track survives the field moving.
5. **Done-when per module.** Each module ends with something the learner can
   now compute or predict BY HAND. That criterion is listed below and is the
   review bar for the scene.
6. **The worked example.** One fixed prompt runs through the whole track (see
   next section), so every mechanism operates on the same tokens the learner
   has already memorized.
7. **The story of everything (user rule, 2026-07-05).** No object may appear
   on screen without its ORIGIN STORY: who computes it, where it lives (inside
   the network? in the sampler code? on whose machine?), and why it must
   exist. A legend DEFINES a symbol; the story EXPLAINS it - both are
   required. Litmus test: for every symbol in a caption, a reader arriving at
   that step cold can answer "where did this come from?" without scrubbing
   back. (Found via r in M0: the draw was defined but its story - the network
   only ranks, so a plain RNG outside the network must choose - was missing.)
8. **The visual carries the claim; the cast tracks the knowledge state (user
   rule, 2026-07-05).** If a caption asserts something, the stage must SHOW it
   - a number must be countable/derivable from visible elements, or explicitly
   tagged IMPORTED (with where it comes from). Text-only steps are a defect:
   if the visualization is not doing the explaining, redesign the step, do not
   lengthen the caption. And the cast are the learner's epistemic proxies:
   Cortex/Bit know exactly what has been derived on screen so far - when
   something arrives from out of the box they either derive it, flag it as
   imported, or are visibly confused BY it (never breezily aware of it).
   (Found via M1 act 2: "~4.0 chars/token" chips that nothing on screen
   supported, and react lines that quipped instead of tracking knowledge.)
9. **One thread at a time; park and resume explicitly (user catch, 2026-07-05).**
   A pass tells ONE story. If it needs two threads (a hook/case plus the
   worked example), the switch must be narrated on stage: "the case is
   parked - background first", "back to the case", "case closed". Silent
   ping-pong between exhibits reads as incoherence. (Found via M1's
   intuition: the France sentence appeared unannounced between strawberry
   beats.)

## The worked example (one thread through every module)

Prompt: `The capital of France is`
- M1 tokenizes it (5-6 tokens, VERIFY exact split at build).
- M0 generates ` Paris` from it, token by token.
- M2 shows ` is` attending back to ` capital` and ` France`.
- M3 caches its keys/values and reuses them.
- M4 routes its tokens to different experts.
- M6 shows base/SFT/RLHF/reasoning models continuing it differently
  (base: " Paris. The capital of Spain is..." - the completion trap).
- M7 swaps in a math prompt only where verifiability demands it.

## Module breakdown

### 0 - Autoregression: the loop inside
- Q: You have watched the answer stream in. What is actually looping?
- P: Generation is a loop: context -> stack -> distribution -> sample ->
  append -> repeat. The model eats its own output; there is no plan, only
  the next token.
- Build (acts): (1) one full turn of the loop on the worked example;
  (2) sampling mechanics - logits -> temperature scaling -> softmax -> top-p
  truncation -> the draw, with live bars recomputed as you drag temperature
  (T=0 collapse, T=2 chaos, the softmax formula on screen);
  (3) the consequence - rerun-divergence (course 1's run-again, now explained
  from inside), and why a wrong early token compounds (exposure).
- Aha: the model never chooses a sentence; it chooses ONE token, ~40 times.
- Numbers panel: vocab size, logits vector length, live softmax over the top
  ~10 tokens as sliders move.
- Break it: T=0 + a repetitive prompt -> a repetition loop, on stage.
- Done when: given 5 logits and a temperature, the learner can compute the
  sampling distribution by hand.

### 1 - Tokens: what the model actually sees
- Q: Why does it miscount the r's in strawberry?
- P: The model reads subword tokens, not letters. BPE builds a vocab (~32k-
  128k) by merging frequent pairs; everything you type is spelled in that
  alphabet.
- Build (acts): (1) type-anything tokenizer playground (real BPE merges run
  live on a small demo vocab - the MERGE steps animate); (2) why "strawberry"
  is 1 token and its letters are invisible; (3) the tax table: numbers, code
  indentation, non-English text = more tokens per meaning, computed live.
- Aha: the model is brilliant in a language whose letters it cannot see.
- Done when: learner can run 3 BPE merges by hand on a toy corpus.
- Honesty: the demo vocab is small + trained on a toy corpus; real vocabs
  (VERIFY: GPT-4 cl100k ~100k, Llama-3 128k, DeepSeek-V3 ~129k) behave the
  same way at scale.

### 2 - Attention: retrieval inside the model
- Q: How does token 400 know what token 3 said?
- P: Every token asks a question (Q), every earlier token advertises what it
  holds (K) and carries a payload (V). Attention = softmax(QK^T/sqrt(d))V -
  a soft lookup. Course 1's librarian (M4 retrieval), recomposed INSIDE.
- Build (acts): (1) intuition - click ` is` in the worked example, watch
  attention lines light up ` capital` and ` France`; (2) mechanism - one
  head's Q.K dot products computed live on 4-dim toy vectors, softmaxed,
  then the weighted V sum assembling; the causal mask as a literal wall;
  (3) multi-head - 4 heads with different obsessions (syntax head, name
  head, position head), then the real shape arithmetic: n_heads x head_dim,
  concat, W_O.
- Aha: attention is RAG the model was born with.
- Numbers panel: live QK^T matrix for a 6-token example; per-layer cost
  n^2 x d displayed as n grows (the quadratic wall).
- Done when: learner can compute one attention weight by hand from toy Q/K.
- Honesty: named "heads with obsessions" are a cartoon; real heads are found,
  not designed, and most resist labels.

### 3 - The KV cache: why context costs memory
- Q: Why is the first token slow and the rest fast? Why does long context
  cost money even when you send it twice?
- P: At generation, each new token needs K and V of every earlier token.
  Recomputing them is O(n) model passes per token - so we cache them.
  Prefill = compute the prompt's KV once (parallel, compute-bound);
  decode = one token at a time against the cache (memory-bound).
- Build (acts): (1) prefill vs decode animated on the worked example - a
  wide parallel sweep, then the one-at-a-time drip; (2) the cache as a
  growing shelf, bytes counted LIVE:
  `2 (K,V) x layers x kv_heads x head_dim x bytes x tokens`
  with a model picker (VERIFY-AT-BUILD: e.g. Llama-3-70B: 80 layers, 8 KV
  heads (GQA), head_dim 128, fp16 -> ~0.66 MB/token -> 128k tokens ~ 84 GB);
  (3) why prompt caching (production track, cost chapter) works: same
  prefix = same cache = skip prefill. The two tracks click together here.
- Aha: "context window" is not a text limit, it is a MEMORY budget.
- Done when: learner can compute a model's KV bytes/token by hand.

### 4 - Mixture of Experts: parameters are not compute
- Q: DeepSeek-V3 has 671B parameters. Why does it run like a 37B model?
- P: In an MoE layer the FFN is split into many experts; a learned router
  sends each TOKEN to a few of them. Capacity (what the model can store)
  decouples from compute (what one token touches).
- Build (acts): (1) intuition - the worked example's tokens flow through a
  dense layer (everything lights up) vs an MoE layer (2 of 64 light up),
  FLOPs meters side by side; (2) mechanism - router logits -> top-k -> the
  chosen experts' outputs weighted-summed; different tokens visibly prefer
  different experts; (3) the DeepSeek recipe (VERIFY-AT-BUILD): 256 small
  routed experts + 1 shared expert, top-8; fine-grained beats few-big;
  total-vs-active param arithmetic computed live; (4) BREAK IT - router
  collapse: all tokens crowd one expert, the rest starve; then balancing
  (aux loss / V3's bias method) restores spread.
- Aha: the biggest models are mostly asleep on every token - on purpose.
- Done when: learner can compute active params of an MoE from expert count,
  expert size, top-k, and shared parts.

### 5 - The DeepSeek moves: MLA and MTP
- Q: Module 3 said long context = a KV memory wall. How did DeepSeek get
  128k context cheaply anyway?
- P: Two moves. MLA (multi-head latent attention): store one small latent
  vector per token instead of full per-head K,V; decompress on use - the
  cache shrinks by an order of magnitude. MTP (multi-token prediction):
  train an extra head to predict token n+2, densifying the training signal
  and enabling speculative decode at inference.
- Build (acts): (1) the same M3 bytes-per-token shelf, now with an
  MHA / GQA / MLA selector - the bar collapses (VERIFY-AT-BUILD: MLA latent
  dim ~512 vs full KV); (2) MTP as a second, cheaper prediction hanging off
  the trunk - accepted when the main model agrees (speculative decode
  animated: draft, verify, accept/reject).
- Aha: architecture headlines are usually about ONE resource; find which
  (here: KV memory, then tokens-per-step).
- Done when: learner can explain why MLA shrinks the cache but not the
  weights, and when speculative decode pays.

### 6 - Training stages: same machine, different manners
- Q: Base, chat, and reasoning models share an architecture. Why do they
  ACT so differently?
- P: Stages shape the distribution, not the knowledge. Pretraining = next-
  token on trillions of tokens (the completion machine). SFT = imitate
  curated dialogues (the assistant shape). Preference tuning (RLHF/DPO) =
  push probability toward answers humans prefer. Each stage is a different
  loss bending the SAME distribution.
- Build (acts): (1) THE flagship scrub - one prompt ("The capital of France
  is" and one risky prompt), four model stages on one stage; scrub across
  base -> SFT -> preference-tuned -> reasoning and watch the same
  distribution reshape: base continues, SFT answers, preference-tuned
  hedges/refuses appropriately, reasoning deliberates first; (2) mechanism
  per stage - what the batch looks like, what the loss compares, what
  updates (all of it vs adapters); (3) the data funnel: web-scale tokens ->
  curated dialogues -> preference pairs -> verifiable problems, sizes to
  scale (VERIFY-AT-BUILD: V3 pretrain ~14.8T tokens).
- Aha: fine-tuning did not teach it facts; it taught it WHICH of its
  completions to prefer.
- Done when: learner can predict how each stage-version answers a novel
  prompt, and say which stage a bad behavior most likely comes from.
- Honesty: stage outputs in the scene are scripted exemplars of documented
  behavior, labeled as such.

### 7 - Reasoning RL: the verifier becomes the teacher
- Q: What physically is "thinking harder"? Where did R1's long chains come
  from?
- P: Chain-of-thought = serial compute at inference: more tokens before the
  answer = more passes through the stack. Reasoning RL (RLVR): sample many
  attempts, score them with a VERIFIER (math checker, tests - course 1's
  Module 6, recomposed as a reward), reinforce what passed. Long, checked
  chains EMERGE; nobody wrote them.
- Build (acts): (1) inference side - same math problem, short vs long chain,
  compute meter running; the chain is workspace, not decoration;
  (2) training side - the RL loop animated: k sampled attempts fan out,
  verifier greens 2 of 8, policy shifts toward them (GRPO-style group
  scoring, VERIFY-AT-BUILD); (3) the R1-Zero story beat - the emergent
  "wait, let me re-check" moment as reward curves rise; then why pure-RL
  models needed an SFT polish (readability, language mixing).
- Aha: reasoning was not programmed in; it was selected for, by a verifier.
- Done when: learner can explain why RLVR works on math/code but not
  directly on "write a nice poem" (no cheap verifier), and connect that to
  course 1 M6.

### 8 - Small models: distillation, quantization, enough
- Q: When is small enough - and how do small models get so good?
- P: Three compressions. Distillation: train the student on the TEACHER'S
  distribution (soft targets carry more signal than one-hot text).
  Quantization: store weights in fewer bits (fp16 -> int8 -> int4); quality
  falls off a cliff only past a point. Data quality: a small model trained
  long on curated tokens beats naive scaling (post-Chinchilla: overtrain
  small models on purpose, because INFERENCE cost dominates).
- Build (acts): (1) scaling-law map - loss vs params/data with the
  Chinchilla ~20 tokens/param ridge drawn, then the inference-optimal
  detour (VERIFY-AT-BUILD: e.g. Llama-3-8B at ~15T tokens = ~1900
  tokens/param); (2) distillation - teacher and student distributions
  overlaid on the worked example, student pulled toward soft targets;
  R1 -> small-model distills as the named exhibit; (3) quantization slider
  with live bytes math (params x bits/8) and an honest quality note per
  stop; (4) capstone echo of course 1 M7: match the model to the task -
  a routing table, not a leaderboard.
- Aha: most of a giant model's behavior fits in a small one - if you copy
  the distribution, not the text.
- Done when: learner can compute a quantized model's disk size by hand and
  say which of the three compressions attacks which cost.

### Capstone - the compiler you can talk to (built 2026-07-07)
- Q: Can a stochastic model behave like a compiler - and does the whole track
  lead here?
- P: An "LLM compiler" = a stochastic FRONT-END (the model lowering natural
  language into a typed tool-call plan / DAG) bolted to a deterministic,
  VERIFIED backend, with a repair loop. Front-end = constrained decoding: a
  grammar masks illegal next-tokens at the sampler (M0) and the model samples
  the renormalized legal set - it cannot emit an invalid plan. Backend = a
  verifier (M7) type-checking the DAG, failing loudly, repairing. Determinism =
  temp 0.
- Build (acts): (1) decode under the grammar - token by token, a different
  static rule masked each step (tool catalog, arg schema, literal type, scope,
  return-type); mask + renorm computed live over illustrative logits. (2) verify
  + repair - four real checks on the DAG, temp-0 determinism, a bad ref failing
  loudly, the repair loop. (3) break it + cost ledger - grammar off / temp up /
  weak verifier / base driver, each toggle a prior module; ledger = M8 driver
  size (computed) + M3/M4 running cost.
- Genuine-capstone test: every break-toggle is powered by an earlier module
  (M0 sampler, M0/temp determinism, M7 verifier, M6 instruction-tuning), so the
  course demonstrably converges here. The IR is course 1's agent loop - the two
  courses meet: natural language COMPILES into the loop you hand-built.
- Driver (the real LLM): pluggable interface; default a quantized small-instruct
  GGUF (MiniCPM-class) grammar-constrained via GBNF - the grammar guarantees
  valid structure even from a ~1B model. Runs local + in CI (never in the
  keyless browser), named only in the Python/README layer. Phase 2: bake real
  traces as a "measured" tab + an opt-in live mode. Honest caveat: grammar
  guarantees valid STRUCTURE, not correct MEANING - honest-toy quality.
- Placement: after M9, as the track's finale. It caps the BEHAVIORAL spine
  (M0/M1/M6/M7/M8 directly power it); the ARCHITECTURE spine (M2-M5) lands as
  the cost-ledger axis. M9 assemble/budget remains the architecture-side
  synthesis. See [[read-order-not-build-order]] (all refs are backward here).

## Widget grammar extensions (build once, in assets/)

- `acts` support in anim.js Timeline + scrubber label ("act 2 . step 4/7").
- An `intuition / mechanism` mode pill convention (same stage, two step
  arrays - the existing OFF/ON pattern generalizes).
- A live-calculator panel component (formula text + inputs + computed
  output) so real arithmetic looks the same in every module.
- A distribution-bars component (logits -> bars with temperature/top-p
  transforms) - used by M0, M6, M8; extract from course 1's distribution
  widget rather than re-inlining.

## Cast notes

Bit finally opens Cortex up: the track's framing scene is Cortex agreeing
to be examined ("be gentle with the residual stream"). Experts in M4 are
mini-Cortexes with specializations; the router is a gold Bit-style
dispatcher. Characters stay single-source in assets/cast.js - add emotes or
variants THERE if needed, never inline.

## Layout & build order

```
models/                      this track (sibling of agentic-course/, production/)
  docs/00-pedagogy.md        this file
  module-00-autoregression/  ...same shape as course 1 modules:
  module-01-tokens/          README.md + widgets/NAME/index.html
  ...                        (+ CHALLENGE.md where a by-hand exercise fits)
  index.html                 hub (clone of course hub pattern, own NAV)
```

Build order (revised 2026-07-05): M0 autoregression -> M4 MoE -> M1 tokens +
M2 attention -> M6 training stages (incl. LoRA/QLoRA/DPO) -> **M3 KV cache ->
M5 DeepSeek -> M7 reasoning RL (GRPO here) -> M8 small models (distill+quant)
-> M9 atlas**. Done: ALL modules M0-M9 built (2026-07-05), plus the CAPSTONE
"the compiler you can talk to" (2026-07-07, module-10-compiler; see the breakdown
above). Rule learned: a module's mechanism pass may only lean on ideas an EXISTING
module has built - check before writing. Cast rule: Cortex/Bit must appear in every widget.

## Closing the asymmetry: nanomodel (2026-07-06)

The agents track graduates from simulation to real code (`claude_harness`); the
models track had none. `models/nanomodel/` closes that: a from-scratch, pure-Python,
keyless tiny transformer (scalar autograd + one attention head + MLP + BPE) that
runs and learns in ~a minute. It is the widgets' math, running - not a new lesson.
Each spine module whose mechanism it implements (M0 loop, M1 BPE, M2 attention,
M4 dense FFN, M6 next-token loss + SGD) ends with a "Run it in code" pointer to
the exact file/function. Guarded by `tests/test_nanomodel.py` (autograd gradient,
BPE matches the M1 widget, forward+backward wiring, training reduces loss). Same
honesty contract: labeled a TOY (char-level, ~1k weights, memorizes not
generalizes); real models are the identical math at scale.

## Coverage decision (user, 2026-07-05): deep spine + atlas

The track is a DEEP SPINE (one mechanism per module, computable by hand), NOT
an encyclopedia. The full method zoo (PPO/DPO/GRPO/KTO, full/LoRA/QLoRA,
quantization/distillation, MoE variants) is exposed two ways: (1) each named
method appears as a dated EXHIBIT of the principle in the module that teaches
its mechanism; (2) a final **Module 9 - "Map of the landscape"** is a pure
atlas: one interactive taxonomy (axes: what it optimizes / what supervision it
needs / what it costs) where every named method is a pin that links back to
the module that explains it. Depth first; coverage as the capstone. Do NOT
turn spine modules into acronym roll-calls - place extra names in the atlas.

## Honesty rules (this track needs them more than the last)

1. Everything computed is computed; everything scripted says so.
2. Named models are dated exhibits of a principle - pin the principle,
   date the exhibit, cite the paper in the module README.
3. All architecture numbers in this doc are from memory and marked
   VERIFY-AT-BUILD: check against the papers (DeepSeek-V2/V3/R1 reports,
   Llama 3 report, Chinchilla) before they appear on screen.
4. No invented benchmark scores, ever. Quality claims stay qualitative
   unless quoting a cited number.
5. Attention/expert visualizations are cartoons of real mechanisms - say so
   on the widget, in the same breath as the mechanism pass.
