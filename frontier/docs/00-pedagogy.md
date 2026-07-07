# Essence of the Frontier - pedagogy

Track 4. Factual basis: `frontier-scan-2026-07.md` (four verified research
passes, July 2026). Read this doc before building any module.

## The bridge

Track 1 built a loop around a model. Track 2 hardened it. Track 3 opened the
model. This track answers the question every learner has at the end: "okay,
but what is happening OUT THERE right now?" - without becoming a news feed.

## The thesis (the one sentence this track defends)

**Every frontier headline is an attack on a principle you already own.**
Sparse attention attacks M2's n^2. Linear attention attacks M3's KV formula.
Agentic RL attacks the scripted loop of course 1. World models attack M0
itself. The exhibits age; the mapping does not - and a learner who holds the
mapping can read NEXT year's frontier without us.

## The recurring primitive

The **attack map**: a principle from tracks 1-3 on one side, a dated exhibit
on the other, an edge labeled with WHAT the attack changes. Every module
opens by placing itself on this map ("you already know the principle; here is
this year's attack on it") and closes by returning to it. The capstone is the
map made playable.

## Depth contract - inherited + frontier rules

Rules 1-9 of the models track apply unchanged (intuition+mechanism passes,
act structure, live-computed arithmetic, verified numbers, done-when bar, one
worked example, origin story for every object, the visual carries the claim +
cast as epistemic proxies, one thread with park/resume). Three NEW rules:

10. **Date-stamp everything.** Every exhibit carries month/year on screen.
    Every module header carries "verified as of 2026-07". The track states
    openly: exhibits age, principles do not.
11. **Secondary-sourced numbers never enter widget arithmetic.** Benchmarks,
    market shares, and leak-reported claims are narrative color at most,
    labeled. Widget math uses only primary-source numbers (papers, official
    tech reports) - or is labeled illustrative, exactly as in track 3.
12. **Teach arguments, not winners.** Where the field disagrees (linear vs
    sparse vs full attention; tokens vs world models), the module presents
    the live argument with the evidence on each side - MiniMax M2's retreat
    gets equal billing with Qwen3.5's bet. No module declares a winner the
    field has not declared.

Read-order rule applies (see memory/read-order-not-build-order): modules
reference only F-modules before them + tracks 1-3 (all backward by
construction). Forward references are fenced teasers.

## Visual grammar - the three-layer stack (NEW, first-class)

Learned from the track-3 capstone: motion earns the wow, but data needs
vector text. Every F-widget composes three vendored layers (assets/vendor/,
offline, no CDN at runtime):

- **p5 (p5.min.js)** - the MOTION layer: stages, particles, choreography
  (tokens flying, patches shattering, worlds unfolding). Canvas. MUST use the
  crispness pattern (density = max(2, devicePixelRatio), polled per frame -
  see memory/canvas-widgets-render-crisp).
- **D3 (d3.min.js)** - the DATA-TRUTH layer: SVG meters, tradeoff charts,
  sankeys, force graphs, and the design-space constellation. Vector text -
  crisp at any zoom by construction. Anything a learner should READ or that
  carries computed numbers prefers D3/SVG over canvas.
- **Rough.js (rough.min.js)** - the BLUEPRINT layer: hand-sketched rendering
  for anything being DESIGNED but not yet committed. Sketch -> ink is the
  visual language of decision-making (capstone especially).

DOM keeps captions, trace panels, cast, and controls (crisp, accessible),
exactly as in compile-live. Widgets link shared theme.css + cast.js as
always; structure tests apply.

## Cast (single-source in assets/cast.js, as always)

- **Bit's arc completes: the architect.** Course 1 Bit built a loop around
  Cortex; track 3 Bit opened Cortex up; here Bit DESIGNS models. In the
  capstone Bit stands at the drafting table.
- **Cortex: remixed, embodied, then challenged.** F2-F4 rewire Cortex's
  insides (it reacts to each operation); F5 gives Cortex a BODY (the chip
  slots into a small robot torso - an outfit/variant, not a new character);
  F6 confronts Cortex with a rival way of thinking.
- **Cortex's cousins (cast.js VARIANTS, not new characters):** the rival
  designs. Same chip DNA, different builds - a sparse cousin (goggles: looks
  at only a few things), a linear cousin (streamlined; a small fixed-size
  backpack instead of a growing KV sack), a blurry diffusion cousin that
  sharpens as it thinks. The capstone reveal = your design walking up to
  stand beside its nearest cousin. Mini-Cortex swarms (M4 precedent) return
  for PARL.
- **SOMNI - the one new character (debuts F6).** From Latin somnium, dream
  (nod to the Dreamer world-model papers). Cloud-soft body, eyes closed.
  DESIGN RULE: Somni never uses a speech bubble - it shows a small WORLD in
  a thought bubble (a tree, rain starting, a ball mid-roll). Cortex speaks in
  tokens; Somni imagines outcomes. Their F6 confrontation is the tokens-vs-
  worlds debate as a character scene. Somni only knows what its bubble has
  shown - epistemic proxy rule applies.

## Module breakdown (each: Q / principle / exhibits / build / aha / done-when)

### F1 - Everything becomes a token (extends M1, M0)
- Q: The model only ever reads tokens. So how is it suddenly looking at
  photos, hearing speech, and moving robot arms?
- P: The menu grows. An image is cut into PATCHES, each projected into the
  same vector space as word tokens; speech becomes codebook tokens; even
  outputs (images, audio) can be token streams. One transformer, one stream,
  new entries in M1's vocabulary.
- Exhibits (dated): Qwen3-VL / InternVL3 (2025 - the patches -> projector ->
  LLM recipe at its ceiling), Qwen3.5 (Feb 2026 - natively multimodal
  flagship; "VLM" dissolving as a category), Qwen3.5-Omni (Mar 2026 - speech
  codebook tokens, both directions), Nano Banana Pro (Nov 2025 - the best
  image GENERATOR is autoregressive; tokens beat diffusion at its own game).
- Build: intuition = a photo shatters into patches that fly into the token
  stream beside words (p5); mechanism act 1 = patch -> vector -> the same
  attention you know (live arithmetic on a toy 4x4 patch grid); act 2 =
  the projector (the translation layer, computed); act 3 = the reverse trip
  (image OUT as tokens) + the omni menu. D3 for the growing-vocabulary chart.
- Aha: "multimodal" is not a new brain - it is a bigger menu. M1 was the
  whole story all along.
- Done when: given a patch size and image size, the learner can compute how
  many tokens an image costs and say where they enter the stream.

### F2 - Attention unchained (attacks M2's n^2, M3's KV formula)
- Q: Track 3 said attention must look at everything and remember everything.
  The 2026 flagships refuse both. How - and what does it cost?
- P: Two escape routes. SPARSE: a cheap learned index picks the few past
  tokens worth exact attention (NSA Feb 2025 -> DSA lightning indexer Sep
  2025 -> V4's CSA+HCA 2026; adopted by GLM-5, MiniMax M3). LINEAR: replace
  the growing KV entirely with a fixed-size recurrent state (Gated DeltaNet
  Sep 2025 -> Kimi KDA Oct 2025 -> Qwen3.5 flagship Feb 2026). THE DISSENT:
  MiniMax M2 (Oct 2025) went BACK to full attention - hybrids degraded
  multi-hop reasoning at scale. Teach the argument (rule 12).
- Build: the M3 cache visual returns; sparse = a spotlight index sweeping
  the past (p5), the indexer's own cost as the new bottleneck (IndexShare);
  linear = the KV sack replaced by a fixed backpack (cousin variant debuts);
  D3 chart: KV bytes vs context for full/sparse/linear, computed from
  primary numbers (V4: ~10% of V3.2's KV; KDA: 75% reduction). Act 3 = the
  M2 retreat, presented straight.
- Aha: the n^2 wall and the KV bill were never laws - they were choices, and
  2026 is the year the field split three ways on them.
- Done when: given context length and a design (full/sparse-k/linear), the
  learner can rank their KV memory and name each design's failure risk.

### F3 - RL eats the pipeline (attacks M6's stages, extends M7)
- Q: M6 taught four manners in a row. The 2026 pipeline has RL at the START,
  the MIDDLE, the END - and even at TEST TIME. What happened?
- P: The reward signal escaped its stage. RLP (Oct 2025): thought-before-
  token rewarded by information gain, inside pretraining. Agentic
  mid-training (Tongyi, Oct 2025): a new stage. TTRL (2025->): majority-vote
  pseudo-rewards at inference. The GRPO zoo, each fixing one flaw (DAPO
  entropy, GSPO sequence-level for MoE, Dr.GRPO length bias, VAPO the critic
  returns, CISPO fork tokens). Rubrics as rewards escape math/code. The
  twist: DeepSeek-V4 (Jun 2026) - GRPO trains SPECIALISTS, on-policy
  distillation fuses them ("RL makes the teachers, distillation makes the
  model" - M7+M8 merged).
- Build: M6's four-stage pipeline diagram returns, then gets INVADED - RL
  seeps left and right (p5 flow); D3 sankey of the V4 pipeline (specialists
  -> distill fusion) with primary token counts; GRPO-zoo table with the flaw
  each fixes (live toy advantage computation extended from M7's widget).
- Aha: "post-training" is dying as a phrase - reward is becoming an
  ingredient, not a stage.
- Done when: the learner can place RLP / mid-training / GRPO / TTRL on a
  pipeline diagram and say what signal rewards each.

### F4 - The loop learns itself (attacks course 1's scripted loop + M8)
- Q: You HAND-WROTE the agent loop in course 1. The 2026 labs do not. What
  replaced your while loop?
- P: Orchestration moved from prompts into weights. Tongyi DeepResearch
  (Sep 2025): the whole search/read/reason loop trained end-to-end, no human
  labels. Cursor Composer (Oct 2025): running tests EMERGED from reward.
  Kimi K2.5 PARL (Jan 2026): the ORCHESTRATOR is trained - when to spawn up
  to ~100 sub-agents, what to delegate ("serial collapse" as the named
  failure). Plumbing standardized underneath: MCP -> Agentic AI Foundation
  (Dec 2025), A2A v1.0 signed agent identity (Apr 2026).
- Build: course 1's loop-cycle visual returns, then the script FADES and the
  same choreography re-emerges from a reward signal (p5); PARL = mini-Cortex
  swarm spawning (D3 force graph of orchestrator + workers, live task
  decomposition); act 3 = serial collapse, shown then fixed.
- Aha: the loop you built by hand is now a thing models LEARN - your course-1
  code was the curriculum.
- Done when: the learner can say what is trained vs scripted in a 2026 agent
  stack and name the failure PARL's reward shaping prevents.

### F5 - The loop gets a body (extends course 1's loop; tools = motors)
- Q: An agent's tools were functions. What happens when the tools are motors
  and the observations are a camera?
- P: A VLA = a VLM whose output tokens ARE actions. pi-0.5 -> pi-0.7 (Apr
  2026) + FAST: motor trajectories DCT-compressed and BPE-TOKENIZED (M1's
  algorithm driving an arm), plus a flow-matching action head for continuous
  50Hz control. THE COUNTER (rule 12): Figure Helix - tokens think at 7-9Hz,
  a continuous 200Hz policy moves; actions-as-tokens has limits. Gemini
  Robotics ER (Sep 2025): planner VLM with web search hands to a VLA
  executor - the agent loop, embodied. Bridge exhibit: GR00T N2
  "world-action models" (2026) - pretrained to imagine, fine-tuned to act.
- Build: Cortex gets a BODY (variant debuts, p5 stage: see -> think -> move
  -> observe as one loop); FAST tokenization shown mechanically (a wave ->
  DCT bars -> BPE chips - M1's widget grammar reused verbatim); Helix
  two-speed split as a clock visual (7Hz bubble vs 200Hz blur). D3: the
  action-token vocabulary growing out of M1's menu.
- Aha: course 1 and track 3 converge in a robot - the loop is the body's
  mind, and actions were tokens all along (until they are not - Helix).
- Done when: the learner can trace one camera frame to one motor command
  through the VLA stack and say where tokens end and continuous control
  begins.

### F6 - The dissent: the war on next-token (attacks M0; SOMNI debuts)
- Q: Everything so far still predicts the next token. Two billion dollars of
  new labs say that is the wrong foundation. What do they know?
- P: Three escapes from left-to-right token prediction. (1) Diffusion LLMs -
  denoise the whole text in parallel (LLaDA 2.0 Dec 2025, 100B, CONVERTED
  from an AR model; Mercury 2 Feb 2026, >1000 tok/s in production). (2)
  World models - predict the world, not the word (Genie 3 -> consumer
  product Jan 2026; Cosmos 3 Jun 2026 unifies sim+reason+act; Sora 2; GAIA-3
  and Oasis 3 in AV safety pipelines). (3) JEPA - predict in REPRESENTATION
  space, generate nothing (V-JEPA 2 Jun 2025; LeCun exits Meta Nov 2025 ->
  AMI Labs $1.03B Mar 2026; World Labs $1B - the world as a persistent 3D
  structure). THE COUNTERPOINT: this same year, actions, speech and images
  all became tokens (F1/F5). State the live question; declare no winner.
- Build: act 1 = diffusion vs autoregression on the SAME sentence (p5: one
  writes left to right, one sharpens from noise - the M0 loop vs its rival,
  side by side); act 2 = Genie-style playable world (p5 stage the learner
  steers, honest "toy cartoon of the idea" label); act 3 = SOMNI debuts -
  Cortex predicts the next token of a falling-ball sentence, Somni's bubble
  just shows the ball landing; the debate scene, evidence on both sides,
  ends on the open question. D3 timeline of the $2B dissent.
- Aha: M0 is not physics - it is a bet, currently winning, seriously
  contested for the first time. You now know both sides' actual arguments.
- Done when: the learner can name the three escapes, what each predicts
  instead of the next token, and the strongest argument FOR tokens.

### F7 - The dated atlas
Same grammar as M9: every exhibit a pin (name, month/year, principle
attacked, source), filterable by principle and by lane; "verified as of
2026-07" stamped in the header; UNVERIFIED items visibly flagged. The page
that ages, pointing at the mapping that does not. Pins include the tail the
modules skip (A2A, Agent 365, memory vendors, sandboxing, Behemoth shelving,
Antigravity, Cowork, benchmark numbers - all labeled per rule 11).

### F8 - CAPSTONE: The drafting room (design the next frontier model)
- Q: You have watched every lab make its choices. Can you make yours - and
  do you understand what each one costs?
- P: The frontier is a small set of DIALS, and every famous model is one
  path through them. Constructive mirror of the track-3 capstone: there you
  proved the modules by BREAKING one per lever; here you prove them by
  BUILDING - one dial per module. Dials: attention (F2: full/sparse/linear
  hybrid), modality (F1/F5: text/VL/omni/+actions), training pipeline (F3:
  stages, GRPO variant, rubric rewards, distill-fusion), deployment (F4:
  single agent / trained swarm), foundation (F6: AR tokens / diffusion /
  world-model bet - the boldest dial).
- Build (the three-layer stack in full): Rough.js blueprint table - the
  model starts as pencil sketch, each committed dial INKS that subsystem in;
  each dial choice fires a short p5 choreography of the mechanism chosen;
  D3 meters (cost / speed / context / capability risk) recompute live from
  PRIMARY numbers only (V4 27% FLOPs, KDA 6x decode, PARL 4.5x wall-clock,
  MSA 1/20 compute at 1M - each cited on hover); and the D3 CONSTELLATION:
  real 2026 models as labeled stars in design space, your design a glowing
  dot that drifts as you turn dials. THE REVEAL: your dot settles beside its
  nearest star - "you just designed ~Qwen3.5" - with the real model card
  cited, and the matching cousin walks on stage. Warnings are exhibits: pick
  linear attention and the M2-retreat card appears; pick rubric rewards and
  the reward-hacking card appears (rule 12 as gameplay).
- Two closing beats: (1) THE SERVING BILL - your design's KV-per-user and
  batch economics, computed from YOUR dial choices, with the door: "paying
  this bill is Track 5." (2) READ THE FRONTIER WITHOUT US - three fresh
  headlines drop (from the atlas feed); the learner drags each onto the
  attack map. Pass = the track achieved its purpose.
- Aha: you can rebuild the frontier from principles - which means next
  year's frontier is already readable.
- Done when: the learner can defend their design's tradeoffs against a
  cousin's design, and correctly place an unseen headline on the attack map.
- Cast: Bit at the drafting table (the architect arc completes); Cortex as
  the model being designed, reacting to each dial; cousins as rivals; Somni
  waiting at the foundation dial.

## Layout & build order

```
frontier/                    this track (sibling of models/, production/)
  docs/00-pedagogy.md        this file
  docs/frontier-scan-2026-07.md   the verified factual basis
  module-f1-tokens/ ...      same shape as track-3 modules:
  module-f8-capstone/        README.md + CHALLENGE.md + widgets/NAME/
  index.html                 hub (track-3 hub pattern, own NAV)
```

Build order: F1 first (proof-slice of the three-layer stack; easiest bridge
from M1; feeds F5 and F6). Then F2 (richest mechanism) -> F5 -> F4 -> F3 ->
F6 (Somni debuts; add Somni to cast.js HERE, single-source) -> F7 atlas ->
F8 capstone last (it needs every module's dial). Launcher gets door 4 when
F1 + hub exist. Wire each module into hub NAV + gallery + gates as built.
Track 5 (serving/infra) comes after this track; F8's serving bill is its
doorway.

## Honesty rules (in addition to rules 10-12)

1. Genie-style playable moments are labeled "a toy cartoon of the idea" -
   we simulate the CONCEPT, never claim to run the real system.
2. The constellation's axes and distances are design abstractions - labeled
   illustrative; the NUMBERS on meters are primary-sourced or absent.
3. Where a 2026 event is known only from secondary sources it appears with
   an UNVERIFIED tag on screen, exactly as in the scan doc.
4. This track will age. The header of every module says so, with its
   verified-as-of date. Aging exhibits are a feature: they become history
   the attack map explains.
