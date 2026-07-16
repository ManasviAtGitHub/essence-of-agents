# The Workshop - pedagogy (bonus track)

Read this before building any module. This is the bonus track - the "final
gift" - and it is the ONE track that is deliberately REAL, not keyless
simulation. Its job: take a learner who now understands agents (T1), production
(T2), the model (T3), the frontier (T4), and serving (T5), and hand them the
actual machinery to build agentic systems that make them extraordinarily
productive. Factual basis: current 2026 practice (Claude Code / Agent SDK, MCP,
multi-agent orchestration, LLM-as-judge, and Karpathy's `autoresearch`, Mar
2026). Verified as of 2026-07.

## The bridge

Tracks 1-5 answered "what is an agent, how does it work, and how is it run?"
This track answers the only question left: **"so how do I use this to 10x my
own work?"** Every prior track was understanding; this one is leverage. And it
is honest about its own origin - this entire course was BUILT this way (an agent
in a loop, reviewed by agent panels, gated by real tests), so the track can hand
you the exact machinery that produced it.

## The thesis (the one sentence this track defends)

**Extraordinary productivity is not a smarter model - it is a loop around an
agent, and a verifier around that loop.** An agent is a loop around a model
(T1). A force multiplier is a loop around an AGENT that keeps only what a
verifier approves. Give an agent a real task and a cheap, checkable signal of
"better", and it will improve your work while you sleep. The model is the
engine; the verifier and the loop are the whole game.

## The recurring primitive - THE VERIFIER LOOP

Every module in this track is one view of a single machine:

    propose  ->  run  ->  VERIFY  ->  keep if better, roll back if not  ->  repeat

The north star is **Karpathy's `autoresearch`** (Mar 2026): an AI coding agent
in an indefinite loop over a tiny real ML-training repo (a stripped single-GPU
nanochat, ~630 lines). You write research directions in a markdown file, point a
coding agent at the repo, and walk away; overnight it reads the code, proposes a
change, trains for ~5 minutes, MEASURES whether the metric improved, commits if
yes and rolls back if not, and repeats - leaving a git history of validated
improvements by morning. It works for exactly one reason: **the training metric
is a cheap, honest verifier.** That is the whole track's lesson generalized:
put a verifier on ANY work (tests, a linter, an eval score, an LLM-judge
rubric) and you can loop an agent against it. Every module opens and closes on
this loop.

## THE DELIVERABLE IS A TOOLKIT YOU STEAL (read twice)

This track is NOT a course you sit through - it is a small set of **liftable
patterns**. The whole point (the user's words): someone should be able to pick
up each design and apply it to THEIR OWN work in an afternoon. So the entire
track is built for conciseness and theft:

- **Each module = one pattern, on one page.** A "pattern card": the pattern in a
  sentence, WHEN to use it (and when not), a **minimal template** (~30-60 lines,
  single file, dependency-light, heavily commented), and a **"make it yours"**
  block - the 3 lines you change to point it at your own task.
- **Templates over prose.** The gift is the skeleton the learner forks, not an
  essay. If a module can't be lifted and run in an afternoon, it's too big -
  cut it.
- **Ruthless minimalism.** No module sprawls; no artifact carries a framework.
  `harness.py` is ~200 lines because Claude Code's *essence* is ~200 lines; the
  rest is theirs to add. Small enough to read in full, real enough to use.

Every module below therefore ends in the same shape: *here is the pattern, here
is the ~40-line skeleton, here are the 3 lines you change.*

## THE BIG DEPARTURE - this track is REAL (read twice)

Tracks 1-5 are keyless, offline, deterministic simulation, by rule. This track
breaks that ON PURPOSE, because "a real coding agent" cannot be honestly
simulated - the productivity is in the realness. The resolution, and the new
rules:

- **Rule 16 - the pattern is keyless; the proof is real.** Every module has a
  keyless WIDGET that simulates the pattern (the loop, the swarm, the judge
  panel - animated, zero-setup, deterministic, ships to the site). AND a real,
  runnable ARTIFACT (Python over the Anthropic API / Claude Code) that lives in
  the repo like `production/server.py` - never in the served `dist/`, never
  keyless. The learner reads the pattern for free and runs the real thing with
  their own key.
- **Rule 17 - every real artifact ships a recorded run.** Because most viewers
  will not have a key, every runnable artifact is accompanied by a recorded
  transcript (a committed `.log` / asciinema-style text capture, or annotated
  screenshots) so the real behavior is demonstrable to everyone. Show it
  working; never claim it works.
- **Rule 18 - a real agent is dangerous; sandbox it.** These agents run bash and
  edit files. Every artifact runs in a sandbox / scratch dir, permission-gates
  destructive actions, and is documented with its blast radius. The track TEACHES
  the safety, it does not hand-wave it (this is course-1 M9, applied to your own
  machine).

- **Rule 19 - concise and liftable, or cut.** Each module ships ONE pattern, a
  one-page card, and a minimal fork-me template with a "make it yours" block.
  Anything a reader can't lift into their own project in an afternoon is too big.
  The success test is not "did they learn it" but "did they steal it and use it".

Inherited: the craft contract (intuition-first, the visual carries the claim on
the keyless widgets, live-arithmetic-only), date-stamping (rule 10), and
teach-arguments-not-winners (rule 12) all still apply to the widgets and docs.

## Visual grammar

The keyless pattern widgets use the same stack (p5 for the loop/swarm motion,
D3 for eval curves and tallies, DOM for annotated transcripts/code). The real
artifacts are plain, well-commented Python in the repo, each with a README, a
`--help`, and a recorded run. The recurring on-screen object is the VERIFIER
LOOP diagram - a ring (propose -> run -> verify -> keep/rollback) that every
module lights up a different arc of.

## Cast

- **Bit is now the operator / lead engineer.** Bit built the loop (T1), hardened
  it (T2), opened the model (T3), designed one (T4), served it (T5). Here Bit
  RUNS a fleet of agents - writes the verifier, launches the swarm, reads the
  git history in the morning. Bit is the human-in-the-loop.
- **Cortex is now the WORKER (and there are many).** The agent doing the task.
  In the swarm module there are many Cortexes (M4 / F4 precedent) - finders,
  verifiers, a judge. Cortex proposes; the verifier decides.
- **No new character.** The co-star is the learner's own real repo and key.

## Module breakdown (each is a PATTERN CARD: Q / the pattern in a sentence / a minimal fork-me template + "make it yours" / keyless widget / aha / done-when)

Keep every card to one page. The template is the deliverable; the prose is the
label on it.

### B0 - The force multiplier (the verifier loop)
- Q: everyone has the same model. Why are some people 10x more productive with
  it - and how do you become one?
- P: the leverage is the LOOP + the VERIFIER, not the model. `autoresearch` is
  the proof: an agent + a training metric + an overnight loop = validated
  research while you sleep. The pattern generalizes to any task with a cheap
  checkable signal.
- Real: point the learner at the actual `autoresearch` repo + a recorded run of
  the loop hill-climbing a metric.
- Widget: the verifier-loop ring, animated - propose/run/verify/keep-or-rollback,
  a metric hill-climbing over "nights". Keyless sim of autoresearch's behavior.
- Aha: productivity = (agent) x (verifier) x (loop). Own all three.
- Done when: the learner can state the loop, name the verifier in `autoresearch`,
  and give a verifier for a task of their own.

### B1 - The agent (a coding harness from scratch)
- Q: what IS a coding agent like Claude Code, concretely - and can I build one?
- P: it is T1's loop + real tools (read / edit / bash / grep / glob) + a
  permission gate + a system prompt + context management. ~200 lines over the
  Anthropic tool-use API. The stop condition is a verifier (tests pass).
- Real: `harness.py` - a runnable coding agent. Point it at a repo with a
  failing test and a task; it reads, edits, runs the test, and LOOPS until green.
  Sandboxed, permission-gated, budgeted (rule 18). + a recorded run.
- Widget: the tool-use loop animated (model -> tool call -> result -> model),
  with the permission gate and the test-passes stop condition lit. Keyless.
- Aha: a coding agent is the loop you already built, plus real tools and a
  verifier for a stop condition. The production leap (MCP, subagents, hooks,
  plan-mode) is additions to this core.
- Done when: the learner can run `harness.py` to fix a failing test and name the
  four things that turn the toy loop into Claude Code.

### B2 - The verifier (evaluation, the highest-leverage skill)
- Q: `autoresearch` and `harness.py` both hinge on "is it better?". How do you
  build that judge - and why is it the whole game?
- P: an agent is exactly as good as its verifier (course-1 M6). The kinds:
  VERIFIABLE rewards (tests, compilers, schemas - cheap and un-gameable),
  LLM-AS-JUDGE with a rubric (for fuzzy quality), SELF-CONSISTENCY (majority
  vote over samples), PAIRWISE comparison, and ADVERSARIAL / red-team checks
  (spawn skeptics to refute). And the meta-move: build the verifier FIRST, then
  let the agent loop against it.
- Real: `evals.py` - a small eval suite + an LLM-judge with a rubric + an eval
  GATE (block a change if a score regresses), runnable on a real task. + recorded.
- Widget: a judge panel - N verifiers scoring an output, a gate that blocks a
  regression, an adversarial refuter killing a false positive. Keyless.
- Aha: verification is the bottleneck AND the teacher. Whoever writes the best
  verifier ships the best agent.
- Done when: the learner can pick the right verifier type for a task and write a
  gate that blocks a regression.

### B3 - The loop (autonomous improvement)
- Q: `autoresearch` runs hundreds of experiments overnight. How do you turn ONE
  agent + ONE verifier (B1+B2) into an autonomous overnight improver of YOUR work?
- P: hill-climbing / loop-until-better. Read the artifact, propose a change, run
  the verifier, keep-if-better / roll-back-if-not, log everything, repeat - with
  git as the memory (every kept change is a commit; the log is the research
  trail). Guardrails: a budget, a plateau/stop rule, human checkpoints.
- Real: `autoloop.py` - a generic autoresearch-style loop that improves ANY
  target with a verifier (not just ML: a piece of code against tests, an essay
  against a rubric, a config against a benchmark). BYO-key; sandboxed; git-logged.
  + a recorded overnight-style run showing the metric climbing across "nights".
- Widget: the hill-climb - a metric rising over rounds, branches kept (green
  commits) and rolled back (grey), the git history growing. Keyless sim.
- Aha: `autoresearch` is not about ML - it is a template. Any verifiable task
  becomes an overnight autonomous improvement loop.
- Done when: the learner can wrap a task of their own in `autoloop.py` and read
  the resulting git history as a research log.

### B4 - The swarm (multi-agent orchestration)
- Q: one agent is a worker; how do you get the reliability and reach of MANY?
- P: the real orchestration schemes (each one used to build THIS course):
  FAN-OUT / map-reduce (N agents, one slice each), ORCHESTRATOR-WORKER (a lead
  decomposes -> delegates -> synthesizes), ADVERSARIAL VERIFICATION (skeptics
  refute; majority-vote kills false positives), JUDGE PANEL / debate (N attempts,
  scored, best synthesized), LOOP-UNTIL-DRY (spawn finders until K rounds find
  nothing new), and WORKTREE ISOLATION (parallel agents editing code without
  collision). Plus when NOT to (a single agent is often better).
- Real: `orchestrate.py` - a runnable fan-out-review + adversarial-verify
  workflow that produces a real code review of a real diff (exactly the 8-agent
  pass that reviewed Track 5). + recorded run.
- Widget: the swarm - a lead fanning out to N workers, results flowing back,
  adversarial verifiers voting, a judge synthesizing. Keyless.
- Aha: reliability comes from independent perspectives + adversarial
  verification, not from one bigger agent. Parallelism is a quality tool, not
  just a speed tool.
- Done when: the learner can pick the right scheme for a task and explain why
  adversarial verification beats a single confident agent.

### B5 - A real project, end to end (the case study)
- Q: what does a production agentic project actually LOOK like - all the parts,
  together?
- P: the anatomy: a harness (B1) + a verifier suite and eval gate (B2) + an
  autonomous loop where it pays off (B3) + orchestration for the big passes (B4)
  + observability (tracing, T2), guardrails (T2/M9), a CI loop, and human
  checkpoints (plan-mode, "ask when blocked", durable authorization). And the
  worked example is THIS COURSE: built by a coding agent, reviewed by an 8-agent
  panel, gated by a real test suite + a widget runtime gate + a jump-test tool,
  steered by a persistent memory file, deployed by CI.
- Real: the repo itself - annotated. A `CASE_STUDY.md` walking how the course was
  built (the loops, the panels, the gates, the memory, the tools built to review
  the work), with links to the real commits.
- Widget: the whole machine - all six arcs of the verifier-loop ring lit,
  labeled with which module owns each. The productivity dividend, visualized.
- Aha: the force multiplier is a SYSTEM - agent + verifier + loop + swarm +
  human, wired together - and you have now seen every part built.
- Done when: the learner can sketch the anatomy of an agentic project and name,
  for a goal of their own, the harness / verifier / loop / swarm / checkpoints
  they would build.

## The real artifacts (runnable, BYO-key, sandboxed, recorded)

`bonus/harness.py` (B1), `bonus/evals.py` (B2), `bonus/autoloop.py` (B3),
`bonus/orchestrate.py` (B4), `bonus/CASE_STUDY.md` (B5). Each: a README, a
`--help`, a `--dry-run` (keyless, uses a fake client so it runs in CI like
`production/`'s FakeClient), a recorded real run committed alongside, and a
sandbox / permission gate. The `--dry-run` path is CI-tested; the real path
needs a key. None ship to `dist/` (rule 16) - `build_dist.py` must NOT copy
`bonus/` `.py`, only its keyless widgets + docs.

## Layout & build order

Directory `bonus/`, modules `module-b0-...` through `module-b5-...`, hub
`bonus/index.html`. Build order:
1. **B0 first (the spine)** - the verifier-loop ring + the `autoresearch`
   framing. It sets the identity (real, verifier-first) and the recurring visual.
2. Then B1 (the agent / harness - the first real artifact), B2 (the verifier),
   B3 (the loop - `autoloop.py`, the autoresearch generalization), B4 (the swarm),
   B5 (the case study).
Wire `bonus/` into `build_dist.py`, `check_widgets.mjs`, the root launcher, and
`check_links.py` at the same time (the Track-5 lesson: a new track that is not
added to all four ships a broken deploy).

## Honesty & safety rules (in addition to 10, 12, 16-18)

- **Show, don't claim.** Every "it works" is backed by a committed recorded run
  (rule 17). No screenshots of imagined output.
- **Name the blast radius.** Every real artifact documents what it can touch
  (files, shell) and how it is contained (scratch dir, permission gate, budget).
- **Verifier honesty.** Say plainly when a verifier is gameable (an LLM-judge can
  be flattered; a test can be overfit) - the track is about verification, so its
  own verifiers must be honest about their limits.
- **The keyless/real seam is labeled on screen.** A widget says "pattern
  (simulated)"; a recorded run says "real run, <model>, <date>"; never blur them.
