# Essence of Agents -- architecture

One project, two tracks, one shared design system. Everything is a **keyless simulation** by
default; the real agent harness is real code you can opt into.

## Layout

```
index.html                 root launcher: two doors (Course / Production) + the cast
assets/                    THE shared library (used by launcher, course, production)
  theme.css                dark palette + cast + scrubber components
  cast.js                  window.Cast -- Cortex & Bit (the ONLY character definition)
  anim.js                  window.Anim -- Timeline + scrubber (scrubbable scenes)
  README.md                library API + how to author a scene
  scene-template.html      copy-paste starting point for a new animated widget

agentic-course/            THE COURSE (learn the agent loop, module by module)
  index.html               hub: sidebar + iframe + a linear pager (About -> ... -> Capstone -> Production)
  about.html               landing + the cast's origin story
  module-XX-*/             each module: README.md, CHALLENGE.md, a keyless widget, often a Python demo
    widgets/NAME/index.html   a self-contained interactive/animated widget

production/                THE PRODUCTION TRACK (harden that loop; the sequel)
  index.html               hub: the "break it on purpose" failure->fix story
  web/index.html           the stage: Cortex runs the loop on stage (SIMULATION by default)
  agent_pro.py             the real production agent (retries, budgets, guardrails, tracing, compaction)
  providers/nvidia.py      OpenAI-compatible adapter (the opt-in live provider)
  server.py                HTTP + SSE server + /assets static route  (OPT-IN "run for real")
  vectorstore.py sandbox.py observability.py persistence.py router.py eval_gate.py run_agent.py
  README.md, test_*.py

models/                    THE MODELS TRACK (inside the model; M0-M9 + capstone - see models/docs/00-pedagogy.md)
  module-XX-*/             README.md, CHALLENGE.md, keyless widget(s) per mechanism
  nanomodel/               the track, RUNNING: from-scratch autograd + tiny transformer + BPE
    autograd.py model.py train.py bpe.py README.md   (models-track counterpart of claude_harness)

claude_harness/            reusable agent library (agent loop + tools + tracing + FakeClient)
tools/                     dev harness (see below)
tests/                     test_modules.py, test_offline_loop.py, test_structure.py, test_nanomodel.py
```

## Principles (enforced by tests/test_structure.py)

1. **One source of truth.** Characters live only in `assets/cast.js`; theme + scrubber only in
   `assets/theme.css`. Never re-inline them.
2. **Simulation-first.** No default surface calls a model. The stage steps through a scripted
   loop; the course widgets replay scripted/recorded data. Deterministic, keyless, scrubbable.
3. **Real underneath, opt-in.** `claude_harness` / `agent_pro` / `providers` are real. To run
   the agent against a real model: `python production/server.py` then open
   `http://127.0.0.1:8088/?live` (uses your own key from a gitignored `.env`). Nothing else needs it.
   The models track has its own real-code counterpart: `models/nanomodel/` is a from-scratch,
   keyless tiny transformer (`python models/nanomodel/train.py`) - the widgets' math, running.
4. **ASCII only** for course + assets + launcher (enforced). Use `-`, `&mdash;`, `&rarr;`.

## Add an animated widget

1. Copy `assets/scene-template.html` -> `agentic-course/module-XX/.../widgets/NAME/index.html`.
2. Fill in `STEPS` + `renderStep(i, dir)` (see `assets/README.md`).
3. Add it to the `NAV` array in `agentic-course/index.html`.
4. Verify (below).

## Verify (the harness)

```
node tools/gallery.mjs        # contact sheet of EVERY page/widget -> tools/gallery/_contact.png
node tools/shoot.mjs <file> <out.png> [click-selectors...]   # one widget, drive a state
python tests/test_modules.py  # widgets well-formed + keyless demos run + ASCII
python tests/test_structure.py# single-source + simulation-first invariants
```

`tools/` also has: `stage_shot.mjs` (drive the served stage), `probe.mjs` (computed styles +
element crops), `scrollshot.mjs` (below-fold sidebar), `asciify.py` (repair non-ASCII).
Throwaway screenshots land in `tools/shot-*.png` and `tools/gallery/` (gitignored).
