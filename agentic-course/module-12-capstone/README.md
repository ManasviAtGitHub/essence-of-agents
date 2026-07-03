# Capstone - build a mind from the while loop

Build one agent end to end, on the `claude_harness` you grew across the course. The
deliverable isn't "it ran once" - it's an **eval score** plus a **trace of the agent
recovering from a failure**.

## The choice is the lesson
Pick one. Each option forces a different part of the course to the foreground - so the
choice is really a diagnosis of what you want to wrestle.

- **Coding agent** - verification is free and brutal (compiler, tests, types); the
  environment is deterministic. Leans on **Module 6** (verification), 2, 0. Pick it to go
  deep on self-correction.
- **Research agent** - no ground truth, so verification is the hard part, and every
  source is untrusted. Leans on **Modules 4** (retrieval), **10** (eval + LLM-judge),
  **9** (injection). Pick it if evaluation is your interest.
- **Computer-use / browser agent** - the environment is the bottleneck: partial
  observability, flaky actions, real consequences. Leans on **Module 2** (loop
  robustness), **5** (re-plan), **9** (danger). Pick it for robustness.

See `widgets/capstone-chooser/index.html` for the interactive version, and
`widgets/capstone-sim/index.html` to *watch* each option run end to end - the
characteristic failure, the recovery, and the eval score, as a keyless simulation.
`RUBRIC.md` is how it's judged.

## What "done" requires (all three)
1. It runs on the harness with real tools.
2. A small **eval set** with a scorer, and a recorded pass-rate (Module 10).
3. A saved **trace** (`claude_harness/trace.py`) showing the agent hit a failure and
   recovered (Module 6) - not a happy-path demo.

## The whole course, in one sentence
You started with a while loop around a model (Module 0). You gave it hands, a reason to
think, a lever (context), a memory, a planner, a critic, teammates, a conscience, and a
ruler - then closed the loop so it learns from its own logs. That's an agent.
