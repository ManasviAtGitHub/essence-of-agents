# B5 - A real project (how THIS course was built by an agent)

*Bonus track. The other four modules are patterns; this one is the receipt - the
same four moves, on a real project of 100+ commits and ~70 interactive widgets.*

## The claim
Everything in B1-B4 is not theory. This course - five tracks, ~70 keyless widgets,
a real in-browser transformer, a CI pipeline - was built across a long series of
agent sessions using exactly those four moves. Here's where each one shows up, and
where reality was messier than the pattern card.

## B1 (the agent = a context manager) -> a multi-day, multi-session build
The build outran any single context window. What kept it coherent wasn't a bigger
model, it was the five context moves:
- **Working set / just-in-time**: the agent never held the whole repo. It read the
  file it was editing, the test that gates it, and a memory index - nothing else.
- **Compaction**: this very project's sessions were *summarized and resumed* more
  than once (you're reading a module written after one such compaction). The task,
  the decisions, and the current file state survived; the transcript didn't.
- **Memory**: a `MEMORY.md` index + per-fact files carried the thesis, the craft
  rules, and open threads across sessions - so session N+1 didn't re-litigate N.
- **Budget**: Track 5's own lesson, applied to the agent writing it.

**Messier than the card:** memory rot is real. A memory that named a file which
later moved caused a wrong recommendation once. The fix became a standing rule:
*verify a memory against the code before acting on it.*

## B2 (the verifier) -> the gates that let an agent commit unattended
The course has three verifiers, in ascending cost, and nothing merges until all
three are green:
1. `tests/test_modules.py` - a deterministic invariant (every widget's text is
   pure ASCII). Un-gameable, runs in a second. *The B2 "verifiable" kind.*
2. `tools/check_widgets.mjs` - a Playwright gate that loads all ~70 widgets,
   drives every scrubber and toggle, and fails on any console error or blank
   render. *The verifier that catches what the eye can't.*
3. `tools/build_dist.py` - a build guard asserting every launcher door resolves in
   the shipped `dist/`. (When it was skipped once, the deploy broke - see below.)

**The lesson B2 preaches, learned here the hard way:** the agent is exactly as
good as these gates. Every real bug that shipped got there through a *gap* in them,
and the fix was always to widen the verifier, not to "be more careful."

## B3 (the loop) -> build -> gate -> read failure -> fix -> re-gate
Each widget was hill-climbed against those gates: build it, run `check_widgets`,
read the *specific* failure, fix, re-run - keep when green. Git is the audit trail
(100+ commits, each a kept step). A whole class of bug ("jump-stranding": a
scrubber that renders wrong when you seek backward) was only *findable* because the
loop had a cheap, honest metric - the gate - to climb.

## B4 (the swarm) -> the review that found the bugs the builder missed
Twice, the finished tracks were reviewed by a **fan-out of agents** - one per
module, each calibrated on the hardest existing widget as a quality bar - and every
finding was **verified against the code before any fix**. That pass found the real
defects a single builder-agent had blind spots to: an empty reaction panel, a
climax that collided with an on-screen shelf, a WebGPU fallback that never fired, a
cost readout that contradicted its own GPU count. Recall from the fan-out;
precision from verify-before-fix. Exactly B4.

## The one that got away (a real incident, honestly)
Adding a new track, the agent wired a new door into the launcher **but not into the
build's hardcoded track list**. Every local gate passed - because they run against
the source tree, where the door resolved fine. Only the *deploy* gate
(`build_dist.py`, which runs against `dist/`) caught it, and only in CI, after the
push. **The lesson:** a verifier only protects the surface it actually runs on. The
local gates and the deploy gate tested different trees; the bug lived in the gap.
The fix widened the local build to mirror the deploy - closing the gap, not just
the bug.

## What a real agentic project actually looks like
Not one heroic prompt. A **loop** (B3) around a **context manager** (B1), stopped
by **verifiers** you trust enough to commit on (B2), with a **swarm** (B4) for the
judgment calls one agent gets wrong - and a human setting direction, reading the
diffs, and deciding what "better" means. The models did the typing. The leverage
was in the harness.

## Steal this checklist
- [ ] A cheap, un-gameable verifier exists **before** you point an agent at the task.
- [ ] The agent's context is *curated each turn*, not an ever-growing transcript.
- [ ] Durable facts live in a memory file - and get re-verified before use.
- [ ] Every autonomous step is a git commit, so rollback and bisect are free.
- [ ] Hard judgments get a fan-out + adversarial verify, not a single opinion.
- [ ] Your gates run on the **same surface you ship** - or the gap will bite in CI.
