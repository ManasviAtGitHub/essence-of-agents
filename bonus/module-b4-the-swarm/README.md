# B4 - The swarm (fan-out for recall, adversarial-verify for precision)

*Bonus track. Real (BYO-key) + a keyless `--dry-run`. Verified as of 2026-07.*

## The pattern (one sentence)
**A swarm isn't "more agents" - it's two moves that trade breadth for precision:**
fan out over diverse lenses to find everything, then make every finding survive a
squad of skeptics whose job is to *refute* it. Recall, then precision.

## The two moves (the whole file)
1. **Fan-out** - N reviewers, each a *different* lens (correctness / security /
   performance), run in parallel. Each lens catches what the others are blind to.
   Union + dedup. High recall, all unverified.
2. **Adversarial verify** - every candidate faces **K skeptics** who each try to
   *refute* it against the code. It survives only if a majority *fail* to refute
   (a consensus vote folded in). This is the move that kills plausible-but-wrong
   findings - the failure mode of any single reviewer.

Fan-out alone is a pile of maybes; verify alone has nothing to check. Together
they're how *this course* was reviewed: 8 agents across the modules, each finding
checked against the code before a single fix landed.

## Run it
```bash
python3 orchestrate.py --dry-run              # keyless: scripted swarm reviews a buggy snippet
ANTHROPIC_API_KEY=... python3 orchestrate.py  # real, parallel model calls
```
The `--dry-run` (in `recorded-run.log`) reviews a function with a real off-by-one.
Five candidates come out of fan-out; the skeptics **kill the two that aren't in the
code** and confirm the three that are:
```
[correctness] off-by-one: range(n+1) yields n+1 items      0/3 refute -> SURVIVES
[security]    no input validation (unvalidated dict...)    3/3 refute -> killed
[performance] recomputes price on every compare (imagined) 3/3 refute -> killed
CONFIRMED (3, ranked by severity): the two real bugs + one real perf note
```

## Make it yours
- **`LENSES`** - your review dimensions (the angles to fan out over).
- **`TARGET`** - what you're judging: a diff, a design doc, a model's answer.
- **`k`** - how many skeptics must fail to refute for a finding to survive. Higher
  k = higher precision, more cost. 3 is a good default.

## Why adversarial, not just "review again"
Asking a second agent to *review* repeats the first agent's blind spots. Asking it
to *refute a specific claim against the code* is a different, harder task - it has
to find evidence the claim is false. That asymmetry is the point: generation is
cheap and optimistic, refutation is where the rigor lives. Put your compute there.

## Honest limits
The keyless swarm is scripted (two lenses surface real bugs, two claims are planted
bogus so you can watch them die) - a real swarm's findings and refutations come
from parallel model calls. Dedup here is a prefix match; real use wants semantic
dedup. The idea and the control flow are exactly real; the verdicts in the demo are
a fixture.
