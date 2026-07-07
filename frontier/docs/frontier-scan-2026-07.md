# Frontier scan - July 2026

The factual basis for a possible Track 4 ("The Frontier"). Compiled 2026-07-08
from four parallel web-research passes (architectures / multimodal + world
models / RL + training / agents + applications), primary sources preferred,
anything thinly sourced marked UNVERIFIED. Everything here is a DATED EXHIBIT
of a principle - the honesty rule this track would lean on hardest.

## The unifying frame

Every frontier headline is an attack on (or extension of) a principle the
course already teaches. That mapping is the track's thesis, and it is the part
that does not age:

| 2025-26 headline | attacks / extends |
|---|---|
| sparse + linear attention (NSA, DSA, DeltaNet...) | M2's n^2 wall, M3's KV formula |
| everything-becomes-a-token (vision, speech, actions, images) | M1, M0 |
| RL in pretraining / mid-training / test time | M6's four-stage pipeline |
| GRPO descendant zoo, rubric rewards | M7 |
| specialists + on-policy distillation (V4) | M7 + M8, merged |
| trained orchestration (PARL swarms, DeepResearch) | course 1's loop + M8 team shapes |
| VLA robotics (pi-0.7, Helix) | course 1's loop - tools become motors |
| world models, JEPA, diffusion LLMs | M0 itself - the foundation |

The big meta-stories of the last 12 months, one line each:
1. The attention matrix and its KV cache became the industry's main target;
   LEARNED sparsity (DeepSeek lineage) won round one, linear hybrids reached a
   flagship (Qwen3.5), and MiniMax M2's retreat to full attention is the
   honest dissent.
2. RL stopped being a post-training polish step and dissolved into the whole
   pipeline - pretraining (RLP), mid-training (Tongyi), test time (TTRL),
   environments-as-datasets.
3. Orchestration moved from scripts into weights - labs now TRAIN the agent
   loop, including the decision to spawn and coordinate sub-agent teams.
4. Tokens absorbed everything (actions, speech, images) while ~$2B of new
   labs (LeCun's AMI, Fei-Fei Li's World Labs) bet that predicting tokens is
   the wrong foundation entirely.

## Proposed spine (each module = principle + dated exhibits)

### F1 - Everything becomes a token (extends M1, M0)
The menu keeps growing: patches, codebooks, and action bins are just new
entries in M1's vocabulary.
- Qwen3.5 (Feb 2026): flagship open model NATIVELY vision-language - "VLM" as
  a separate class is dissolving into the base model.
- Qwen3-VL (Oct 2025) / InternVL3 (Apr 2025): the classic patches ->
  projector -> LLM recipe at its ceiling (native resolution, GUI control).
- Qwen3.5-Omni (Mar 2026): speech in AND out as codebook tokens (ARIA rate
  alignment) - audio is in the token stream both directions.
- Nano Banana Pro (Nov 2025): the consensus-best image generator is
  AUTOREGRESSIVE (~1,290 image tokens) - tokens beat diffusion at its own
  game. A reverse-attack exhibit.

### F2 - Attention unchained (attacks M2's n^2, M3's KV formula)
The two escape routes from paying for every past token, and the dissent.
- Sparse lineage: NSA (Feb 2025, ACL best paper) -> DSA lightning indexer
  (V3.2, Sep 2025) -> V4's CSA+HCA two-tier compression (2026: 1.6T/49B
  active, ~10% of V3.2's KV) -> GLM-5 adopts DSA + IndexShare (2026) ->
  MiniMax M3's MSA (Jun 2026, 1M ctx).
- Linear lineage: Gated DeltaNet (Qwen3-Next, Sep 2025) -> Kimi Linear/KDA
  (Oct 2025) -> Qwen3.5 (Feb 2026): 75% linear layers in a true flagship.
  Fixed-size state = the KV cache abolished, not shrunk.
- The dissent: MiniMax M2 (Oct 2025) REVERTED to full attention - hybrids
  degraded multi-hop reasoning at scale. Best-documented negative result;
  then M3 chose sparse over linear. Teach the argument, not a winner.
- Bonus exhibit: mHC (DeepSeek, Dec 2025) - the residual stream itself
  redesigned (n parallel streams, doubly-stochastic mixing), first change to
  that layer since 2015. Shipped in V4.

### F3 - RL eats the pipeline (attacks M6's stages, extends M7)
M6 taught four manners in a row; 2025-26 dissolved the row.
- RLP (NVIDIA, Oct 2025): RL inside PRETRAINING - thought-before-token,
  rewarded by information gain.
- Agentic mid-training (Tongyi DeepResearch, Oct 2025): a new stage between
  pretraining and post-training.
- TTRL (Apr 2025 -> subfield): RL at TEST TIME from majority-vote
  pseudo-rewards.
- The GRPO zoo, each fixing one flaw: DAPO (entropy collapse), GSPO
  (sequence-level for MoE), Dr.GRPO (length bias), VAPO (the critic returns),
  CISPO (keep rare fork-token gradients); ScaleRL (Meta, Oct 2025) gives RL
  its first scaling laws.
- Rubrics as rewards (Jul 2025 ->): RLVR escapes math/code into medicine and
  open-ended work; M7's verifier-limit widget gets a sequel.
- Self-play task generation (Absolute Zero, May 2025): the model proposes its
  own curriculum; environments become the dataset (Prime Intellect
  Environments Hub, INTELLECT-3).
- The capstone twist: DeepSeek-V4 (Jun 2026) trains domain SPECIALISTS with
  GRPO, then fuses them into one student by on-policy distillation - "RL
  makes the teachers, distillation makes the model" (M7 + M8, merged).

### F4 - The loop learns itself (attacks course 1's scripted loop + M8)
Orchestration moved from prompts into weights.
- Tongyi DeepResearch (Sep/Oct 2025): open 30B-A3B deep-research agent, the
  whole search/read/reason loop trained end-to-end (synthetic data, custom
  GRPO) - no human labels.
- Cursor Composer (Oct 2025): lab-independent proof - RL in sandboxed coding
  environments; running tests EMERGED from reward.
- Kimi K2.5 PARL (Jan/Feb 2026): the ORCHESTRATOR is trained - when to spawn
  up to ~100 sub-agents, what to delegate, how to aggregate; names the
  "serial collapse" failure mode. Course 1 M8's team shapes, now learned.
- Kimi K2 (Jul 2025): the open blueprint - ~23k simulated tools generating
  verified trajectories + self-critique rubric reward.
- The plumbing standardized: MCP donated to the Agentic AI Foundation (Dec
  2025; ~97M monthly downloads), A2A v1.0 with signed agent identity (Apr
  2026), sandboxing as table stakes (microVMs), memory layers (Mem0/Letta).

### F5 - The loop gets a body (extends course 1's loop; tools = motors)
- pi-0.5 -> pi-0.7 (Physical Intelligence, Apr 2026) + FAST: robot actions
  DCT-compressed and BPE-TOKENIZED - M1's principle driving motors - plus a
  flow-matching action head for continuous 50Hz control.
- Figure Helix (Feb 2025 -> production): the honest counter - tokens think
  at 7-9Hz, a continuous 200Hz policy moves; actions-as-tokens has limits.
- Gemini Robotics 1.5/ER 1.6 (Sep 2025 -> 2026): planner VLM (with web
  search!) hands to a VLA executor - the agent loop, embodied.
- NVIDIA GR00T N2 / "world-action models" (mid-2026): the world model IS the
  policy - "pretrained to imagine, fine-tuned to act". Bridges to F6.

### F6 - The dissent: world models and the war on next-token (attacks M0)
The finale: three escapes from "predict the next token, left to right" - and
the token camp's answer.
- Diffusion LLMs went production: LLaDA 2.0 (Dec 2025, 100B, converted FROM
  an AR model), Mercury 2 (Feb 2026, >1,000 tok/s with reasoning). Gemini
  Diffusion production status UNVERIFIED.
- Playable world models became products: Genie 3 -> Project Genie (consumer,
  Jan 2026); Waymo world-model variant for robotaxi edge cases; Cosmos 3
  (Jun 2026) unifies simulation + reasoning + action; Sora 2 (Sep 2025) as
  passive world simulator; GAIA-3 / Oasis 3 put generated worlds into AV
  safety pipelines.
- The institutional bet against tokens: LeCun exits Meta (Nov 2025) -> AMI
  Labs, $1.03B seed (Mar 2026) - V-JEPA lineage, predict in REPRESENTATION
  space, "LLMs are a dead end"; World Labs Marble + $1B (Feb 2026) - the
  world as a persistent 3D structure, not re-predicted pixels; V-JEPA 2
  (Jun 2025) is the concrete artifact (zero-shot robot planning in latent
  space).
- The live question, stated honestly: do world models replace next-token
  prediction - or is "the world" just another thing tokens learn to predict?
  (Actions, speech and images all became tokens this same year.)

### F7 - The dated atlas
Every exhibit above as a pin (name, date, principle attacked, source), plus
the tail: Llama 4 / Behemoth shelved + Meta's closed pivot (partly
UNVERIFIED), Nemotron 3 hybrid SSM, Antigravity evidence-artifacts, Claude
Cowork / ChatGPT Agent (agents leave the IDE), Microsoft Agent 365 (agents
managed like employees), Anthropic "Teaching Claude why" (May 2026), K2.6
300-agent swarms (UNVERIFIED), OpenAI universal verifiers (UNVERIFIED).
Stamped "verified as of 2026-07"; the atlas page ages, the mapping does not.

## Sorting: what we can have

- MODULE MATERIAL (deep, animated, mechanism-first): everything under F1-F6
  above. Strongest single candidates if we build only a few: F2 (attention
  unchained - richest mechanism + best evidence story), F4 (the loop learns
  itself - closes the arc with course 1), F6 (the dissent - the finale with
  real stakes).
- ATLAS PINS ONLY (name + one line, no module): protocol/enterprise items
  (A2A, Agent 365, AgentKit->Frontier), memory vendors, sandbox vendors,
  coding-agent market shares, benchmark numbers (secondary-sourced).
- SKIP: product launches with no mechanism to teach (social-app wrappers,
  UNVERIFIED-only items except as flagged asides).

## Honesty notes for the track

- Every exhibit gets a month/year stamp; the track header states its
  "verified as of" date and that exhibits age while principles do not.
- Secondary-only numbers (SWE-bench shares, commit percentages, K2.6,
  AgentKit deprecation, E2B stats) stay OUT of widget arithmetic - narrative
  color at most, labeled.
- The M2-vs-M3 style rule applies: modules own their mechanisms; exhibits are
  dated illustrations, never load-bearing dependencies.
