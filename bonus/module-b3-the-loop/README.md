# B3 - The loop (autoresearch, generalized: a metric an agent can climb)

*Bonus track. Real (BYO-key) + a keyless `--dry-run`. Verified as of 2026-07.*

## The pattern (one sentence)
**Give an agent a metric and let it hill-climb your code, unattended** - the model
only *proposes*, the verifier (B2) *decides*, and git keeps the history:

```
propose -> apply -> RUN -> measure -> keep-if-better / rollback -> repeat
```

This is B1's loop with one swap: the stop-condition ("until tests pass") becomes a
score-to-maximize ("keep the best you've found"). That swap is the whole idea
behind Karpathy's `autoresearch`, which loops exactly this over nanochat training
runs on a single GPU - propose a code change, train ~5 min, read the metric, keep
or roll back, forever.

## Run it
```bash
python3 autoloop.py --dry-run              # keyless: a deterministic proposer climbs a knob
ANTHROPIC_API_KEY=... python3 autoloop.py  # a real model proposes each step
```
The `--dry-run` (committed in `recorded-run.log`) tunes a knob `K` whose metric has
a hidden peak the loop must find. Note the **rollbacks** - proposals that made it
worse are reverted and never pollute the git log:
```
[seed]    K=0.0   metric=-49.0000
[step 1]  K=4.0   metric=-9.0000   KEEP
[step 2]  K=8.0   metric=-1.0000   KEEP
[step 3]  K=12.0  metric=-25.0000  rollback   <- overshot; reverted
[step 6]  K=7.5   metric=-0.2500   KEEP
[step 7]  K=7.0   metric=-0.0000   KEEP        <- found the peak
BEST: K=7.0    (git log shows ONLY the kept steps - a clean audit trail)
```

## Make it yours (the 3 seams)
- **`apply(repo, cand)`** - how a proposal becomes a change on disk. Here: set a
  knob. In real use: `git apply` a unified diff the model wrote.
- **`measure(repo)`** - run the thing, return ONE number to maximize. Your B2
  score, an eval pass-rate, a training loss (negated), wall-clock - anything.
- **`Proposer.propose`** - the model suggesting the next change from what's worked.

## Why git is load-bearing
Keep = commit, rollback = `git checkout`. So the repo is *always* at the best state
found, every improvement is a reviewable commit, and a bad proposal can never
corrupt your baseline. The audit trail is free, and you can `git bisect` a
regression the agent introduced. Autonomy is only safe because rollback is cheap.

## Honest limits
The keyless proposer is a deterministic hill-climb (reverse-and-halve) so CI can
run it - a real model would propose smarter, non-monotone jumps. The knob is a
stand-in for "a diff to real code"; the loop itself is exactly what you'd run for
real, just with a slower `measure()` (a training step, a full eval) and a model in
the `propose` seat. The idea is real; the demo is a fixture.
