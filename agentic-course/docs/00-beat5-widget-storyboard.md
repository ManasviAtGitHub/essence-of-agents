# Storyboard - Beat 5 widget: "Watch it run twice"

The first of the ~6 interactive knobs. It sits on Module 0's non-determinism aha.

**Its one job:** make the learner *feel* that identical input gives different output.
**One knob only** (a Run button); everything else is locked on screen, because the
lesson is "nothing changed but the answer."

## The frames

**Frame 0 - Resting.** Constants pinned with locks; the eye registers "all fixed."

```
+-- Watch it run twice ---------------------------- [ Replay v ] --+
|  (lock) Prompt   "Read your own source and explain how you      |
|                   work, in two sentences."                       |
|  (lock) Model    claude-opus-4-8     (lock) Tools  read_file     |
|  Nothing below changes between runs - except the answer.         |
|                     [   >  Run   ]                               |
|  Runs: -                                                         |
+-----------------------------------------------------------------+
```

**Frame 1 - First run, streaming.** Tokens arrive one at a time; calm cadence.

**Frame 2 - Run 1 settles.** Checkmark; button relabels to "Run again"; the prompt
does NOT clear (learner sees they're sending the same thing).

**Frame 3 - The aha frame.** Run 2 lands beneath Run 1, word-aligned. They agree for
a stretch, then split. Shared prefix renders dim; from the divergence token on, both
brighten. A single caret marks the fork - the only "pop" of motion.

```
Run 1   I read my own source code . then summarized how I work.
Run 2   I read my own source code . then explained the loop I run.
                       shared ----^  diverges at word 7
Same prompt. Same model. Same settings. Two answers.
```

**Frame 4 - The shelf.** Each run stacks as a row; a tiny meter quantifies the split
(a quiet foreshadow of why Module 10 needs evals).

**Frame 5 - The locked door.** A greyed "Why does it split?" affordance - "unlocks in
Module 3." The recomposition promise made visible.

**Frame 6 - Live mode.** Same surface, real call, a cost ticker so the difference from
free replay is honest.

## Interaction & states
- One control (Run). Constants are display-only with lock icons.
- Replay (default): each press pops the next real recorded run, streamed with its
  timing. Works offline. Zero cost. Everyone sees genuine divergence.
- Live: key field appears; same renderer streams from the real API.
- Edge cases: replay exhausted -> reshuffle; live no key -> inline prompt;
  401/rate-limit/refusal -> one calm line + "switch back to Replay."

## The trace-replay engine (the foundation)

A recorded trace is just data: `{ input, runs: [{ run_id, text, chunks: [{t_ms, text}] }] }`.

The one abstraction everything reuses: **replay and live emit the same thing** - an
async stream of `{ index, text }`. Replay yields cached chunks on a timer; live yields
from the API's SSE. The renderer doesn't know which.

```
recorded JSON --\
                 >-- TokenStream --> one renderer (streaming + diff + shelf)
live API (SSE) -/
```

This is the 3B1B "pre-rendered" move applied to agents: the feel of a live run, no
cost, no variance-induced support pain, an offline fallback - and it goes live the
instant someone brings a key.

## The Module 3 upgrade (recomposition)
Same component; clicking the now-unlocked "Why does it split here?" reveals, at the
divergence token, the distribution it was sampled from. The Module 0 observation
becomes the Module 3 mechanism. One primitive, recomposed.

## Build scope
- **Ships cheap (day one):** replay engine + shared renderer + word-aligned diff +
  locked-constants panel. Pure front-end, static JSON, no backend.
- **Stretch - Live:** needs a thin proxy (never ship a key to the browser). Honest
  default is replay; "go live" best in the companion repo/notebook.
- **Stretch - distribution reveal:** the Module 3 upgrade.

## Why this knob is first
Simplest instance of the platform - one button, one stream, one comparison. It forces
us to build the renderer, replay engine, and replay/live duality with minimal surface.
The harder knobs (M2 toggle, M3 context editor, M6 verifier dial, M9 injection box,
M10 eval scatter) are reskins of this chassis.

Implementation lives in `../module-00-smallest-agent/widgets/run-again/`.
