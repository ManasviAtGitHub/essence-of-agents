# Pedagogy & course design (v2)

## The teaching DNA

**3Blue1Brown:** never start with a definition - start with a question you feel.
Build the intuition before any formalism. Engineer one click per unit. Be honest
about what's hand-wavy.

**The Coding Train:** build it from scratch, live, mistakes and all. Debugging is
the lesson. Every session ends in something that runs and that you can see.

**The synthesis (the whole pedagogy):** derive the concept from a question, then
immediately build the smallest runnable version of it from scratch, then watch it
work and break it on purpose. No frameworks until you've re-derived what the
framework does by hand.

## The spine

One artifact, ~twelve transformations. The agent starts as ~30 lines and grows
hands, a loop, memory, a planner, a critic, copies of itself, then evals and a
deploy. It is never thrown away.

## The recurring primitive (narrowed, honest claim)

A creature whose only world is its scroll of context. It is **literal** through
Module 6. After that the same primitive is visibly recomposed: multi-agent = many
scrolls; security = a gate on the scroll; eval = the loop scored; production = the
loop around the loop. Not "one diagram explains everything" - one primitive,
recomposed.

## Per-module shape

Each module: **Question -> Principle -> Build -> Aha**, where the Aha is what the
*build* surfaced, not the principle restated.

### 0 - The smallest agent that could
- Q: What's the least you can add so a chat model *does* something, not just says it?
- P: Agency isn't in the model; it's the loop and the clock you wrap around it.
- B: ~30 lines - loop, one model call, one real tool. Plant two observations:
  it forgot the earlier turn (no memory), it answered differently on a rerun (sampling).
- Aha: You added zero intelligence. The same model takes an action because it has a
  body and a turn-counter.

### 1 - Hands (tools)
- Q: The model only emits text. How does text become a real action?
- P: You describe tools in the context; the model emits a structured request; your
  code is the runtime.
- B: Add a calculator, file read, web fetch; structured output. One-paragraph
  security seed (we just let it act on text from the open web - remember for M9).
- Aha: We added a calculator and never touched the model - competence was latent;
  we granted permission and a parser.

### 2 - The loop (Reason + Act)
- Q: Why interleave thinking and doing instead of planning once?
- P: The model can't see the future; reasoning is tokens that buy a better next action.
- B: Build observe->think->act with a scratchpad. Then delete the think step and
  watch accuracy collapse.
- Aha: "Thinking" isn't decoration - we measured it paying rent.

### 3 - Context is the only lever (prompting lives here)
- Q: You've felt the agent be flaky. What can you actually turn to fix it?
- P: Only one thing: what's in the context. Skills: tokens, the context window,
  in-context learning, system prompts, few-shot, ordering, sampling/temperature.
- B: Take a task the agent fails ~40% of the time to ~90% without changing the model.
- Aha: You're programming in English, and word order is syntax.

### 4 - Memory & retrieval
- Q: The context is finite and the past falls off the edge. How does it remember?
- P: You are the librarian deciding what to put back on the desk. Memory is
  retrieval-and-insertion, not storage.
- B: Summarization -> a vector store, deriving RAG. Semantic vs episodic.
- Aha: Retrieval doesn't give the agent memory; it silently swaps which agent you're
  running on this call.

### 5 - Planning & decomposition
- Q: What about a task too big for one loop?
- P: Planning spends cheap compute to make expensive actions less likely to be wrong;
  branching is one form of deliberate search (not a grand unified theory).
- B: Plan-and-execute over a task list; re-plan when reality diverges.
- Aha: The plan was wrong by step 3 - and that was fine: re-planning beat a stale
  perfect-looking plan.

### 6 - Verification & self-correction (the center)
- Q: The agent is confidently wrong. How does it catch itself?
- P: Generation is cheap; verification is the bottleneck. An agent is about as good
  as its feedback signal.
- B: It writes code, runs it, reads the real error, fixes it; then a critic pass.
- Aha: The writer barely got smarter; we gave it a harsher reader and quality jumped.

### 7 - Reasoning models & inference-time compute (rebuilt)
- Q: When is a token spent inside the model worth more than a step taken outside it?
- P: Some scaffolding moved inside the model - but internal reasoning doesn't replace
  external scaffolding when the missing ingredient is information or action.
- B: Run the same task three ways (cheap+heavy loop, reasoning+thin loop, wrong pairing);
  chart cost/latency/accuracy.
- Aha: Better-model and better-harness are sometimes substitutes, sometimes
  complements; the experiment tells you which.

### 8 - Many agents
- Q: When does one mind need to become several?
- P: Multi-agent earns its cost when it buys context isolation, specialization, or
  parallelism - and costs coordination overhead when it doesn't.
- B: A supervisor fanning out to specialists; then a deliberately bad 5-agent version
  a single good agent beats.
- Aha: The 5-agent build lost - coordination tax for nothing. It won only once each
  agent got a context the others couldn't hold.

### 9 - Reliability & security (seeded in Module 1)
- Q: Your agent reads untrusted text and takes real actions. What goes wrong?
- P: The model doesn't reliably preserve the boundary between instructions and data
  unless you design for it.
- B: Inject a hostile sentence into a page the agent reads, watch the hijack, then add
  guardrails, sandboxing, least-privilege tools, a human approval gate.
- Aha: The exploit wasn't a bug in our code - the feature working as designed.

### 10 - Evaluation
- Q: You changed a prompt. Is it better, or do you just feel that way?
- P: You can't improve what you can't measure; evals are the experimental method.
- B: Traces -> dataset -> LLM-as-judge -> regression eval -> change/measure/keep-or-revert.
- Aha: Two "obvious improvements" scored worse. We'd been shipping vibes. (Evals are
  the telescope - without one you're staring at the sky.)

### 11 - Shipping: close the loop (one spine)
- Q: What's the gap between "works on my machine" and "people depend on it"?
- P: Production is the dev loop plus one edge: every failure in the wild becomes a row
  in your Module 10 eval set. Cost/caching/streaming/retries/tracing hang off that.
- B: Wire traces -> failure capture -> eval set -> fix -> redeploy, with budgets as guardrails.
- Aha: A production agent is the Module 0 loop with a feedback edge soldered on.

### Capstone - the choice is the lesson
Build one agent end-to-end. Each option stresses a different part of the course:
- **Coding agent** - verification is free and brutal (compiler/tests). Leans on M6.
- **Research agent** - no ground truth, so verification is the hard part. Leans on
  M10 and M4, drowning in untrusted text (M9).
- **Computer-use / browser agent** - the environment is the bottleneck. Leans on the
  M2 loop, retries, real-world danger (M9).

Acceptance for all three: an eval score, plus a trace of the agent recovering from a
failure.

## Honesty notes
- The "one agent" spine is the *narrative*. In the repo, each module ships a
  self-contained keyless widget + demo rather than one evolving codebase; the
  harness is the grown-up form the loop settles into.
- The trace visualizer is aspirational, not a dependency. The course ships on
  dead-simple text/HTML trace dumps; a polished visualizer is a stretch goal. The
  widgets replay their own scripted/recorded data - they are not wired to the
  harness's trace format.
- The recurring visual is a primitive, not a magic diagram (see above).
- The thesis covers Modules 0-6 literally and generalizes after; we don't pretend
  everything is literally context-shaping.
