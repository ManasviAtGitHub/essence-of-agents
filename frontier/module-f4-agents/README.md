# F4 - The loop learns itself

*Verified as of 2026-07. Exhibits age; the principle does not.*

In course 1 you HAND-WROTE the agent loop: while not done, think, call a
tool, read the result. The 2026 labs do not hand-write it. The loop - and
even the decision to spawn a TEAM - moved from prompts into weights.

## Question
Your course-1 while loop was code you wrote and could read. What replaced
it - and what does "the orchestration is trained" actually mean?

## Principle
**Orchestration moved from scripts into weights.**
- Tongyi DeepResearch (Sep/Oct 2025): an open 30B-A3B model whose whole
  search/read/reason loop is trained end to end - agentic mid-training (F3),
  SFT, then a customized GRPO with a LEAVE-ONE-OUT baseline over full
  trajectories, on fully synthetic data. No human wrote the loop's habits.
- Cursor Composer (Oct 2025): the lab-independent proof - RL inside
  sandboxed coding environments with real tools; running tests and fixing
  lint EMERGED from reward, nobody prompted them.
- Kimi K2.5 PARL (Jan/Feb 2026): the ORCHESTRATOR itself is trained - when
  to spawn up to ~100 sub-agents, what to delegate, how to merge. Sub-agent
  trajectories are treated as environment observations; only the
  orchestrator gets gradients. Names the failure mode: SERIAL COLLAPSE
  (the orchestrator degenerates into doing everything through one worker).
  ~4.5x wall-clock speedup on wide-search tasks (primary).
- Beneath it, the plumbing went neutral: MCP donated to the Agentic AI
  Foundation (Dec 2025; ~97M monthly SDK downloads), A2A v1.0 with signed
  agent identity (Apr 2026). The interfaces standardized while the behavior
  moved into weights.

## See it (no key)
`widgets/trained-loop/index.html` - two passes:
- **intuition (7 steps):** course 1's loop returns as YOUR code; the script
  fades and the same choreography re-emerges from reward; tests emerge in
  Composer; a swarm spawns; serial collapse and its fix; the plumbing.
- **mechanism (14 steps, 3 acts):** act 1 computes Tongyi's leave-one-out
  advantage on a toy trajectory group (each attempt judged against the
  OTHERS' mean, live). Act 2 computes why serial collapse happens and how
  reward shaping fixes it (wall-clock arithmetic, labeled "the mechanism,
  simplified"); the swarm drawn live. Act 3: the plumbing (dated), the
  trained-vs-scripted ledger, and the finale - the trained loop running on
  its own.

## The aha
Your course-1 code was not wasted - it was the CURRICULUM. The loop you
hand-wrote is exactly what these models are now trained to do without you.

## Honest notes
- Toy trajectory rewards hand-authored (labeled); leave-one-out means and
  wall-clock arithmetic computed live.
- PARL's real reward shaping is richer than the toy time-penalty shown; the
  widget labels it "the mechanism, simplified" and keeps the primary claims
  (100 sub-agents, ~1,500 steps, ~4.5x) sourced to the paper.
- K2.6's 300-agent swarms are secondary-sourced and appear nowhere here
  (rule 11).

## Done when (the bar for this module)
You can say what is trained vs scripted in a 2026 agent stack, compute a
leave-one-out advantage for one trajectory, and explain serial collapse and
the kind of reward that prevents it. `CHALLENGE.md`.

## Next
F5: the loop gets a body - actions become tokens, and the counter-argument
(200Hz control) that keeps them continuous.
