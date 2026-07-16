# B2 - The verifier (build it first; whoever writes the best one wins)

*Bonus track. Real (BYO-key) + a keyless `--dry-run`. Verified as of 2026-07.*

## The pattern (one sentence)
**An agent is exactly as good as its verifier** - so the verifier is the artifact
worth your best effort, not an afterthought. B1's loop *stops* on it; B3's loop
*climbs* it. Get the verifier right and everything downstream is just search.

## Four kinds, composable (this is the whole file)
1. **Verifiable** - a deterministic check (a test, a schema, a keyword). Cheap and
   **un-gameable**. Weight it highest. If you can make a check verifiable, do.
2. **LLM-judge** - a model scores an output against a written **rubric**, for the
   fuzzy quality a test can't capture (tone, completeness). Gameable - keep it a
   minority of the score.
3. **Self-consistency** - sample the system N times, take the majority. Reliability
   for ~free; the cost is Nx calls.
4. **Gate** - block a change if its score dropped vs a saved **baseline**. This is
   the one you wire into CI. A regression fails the build, like any other test.

## Run it
```bash
python3 evals.py --dry-run              # keyless: FakeJudge; catches a planted regression
ANTHROPIC_API_KEY=... python3 evals.py  # real LLM-judge (claude-sonnet-5)
```
The `--dry-run` (committed in `recorded-run.log`) scores a good system, saves it as
the baseline, then proves the gate **BLOCKs a regression** and **PASSes a real
improvement** - and exits non-zero if it ever misjudges (the verifier self-tests):
```
1) good system     -> score 0.96   gate: PASS (saved as baseline)
2) regressed       -> score 0.653  gate: BLOCK - REGRESSION: 0.653 < 0.96
3) improved        -> score 0.96   gate: PASS - held at ~0.96
```

## Make it yours (the only 3 things you change)
- `CASES` - your inputs + the deterministic check for each (the un-gameable core).
- `RUBRIC` - your quality bar, in one sentence, for the LLM-judge.
- `system(q)` - call **your** agent/model instead of the demo's lookup table.

Then `gate(score, "baseline.json")` in CI, and commit `baseline.json`. That's it.

## Why this shape
Verifiable-weighted-higher is deliberate: a model asked to judge itself can be
flattered, but it cannot make a failing test pass. The judge fills the gap the
test leaves; the gate turns "we think it's better" into a number a machine can
enforce. Every serious eval harness is a fancier version of these four functions.

## Honest limits
`FakeJudge` is a deterministic stand-in (short+direct scores high; hedging scores
low) so the whole thing runs keyless in CI - a *real* judge needs a key and a real
model. Self-consistency here is wired but the demo systems are deterministic, so
N=1; it earns its keep only against a sampling model. The idea is real; the demo
is a fixture.
