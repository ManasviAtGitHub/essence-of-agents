# B1 - The agent (a coding harness that is really a context manager)

*Bonus track. Real (BYO-key) + a keyless `--dry-run`. Verified as of 2026-07.*

## The pattern (one sentence)
**A coding agent is not the model - it is the CONTEXT MANAGER around it.** The
tools *fetch* information; context engineering decides what the model actually
*sees* each turn. Nail that and a small model does big work; botch it and a big
model flails.

## The five context moves (this is the whole harness)
1. **Working set** - curate what's in context (system + task + memory + the files
   you actually need + recent results), not an ever-growing transcript.
2. **Just-in-time** - tools pull files on demand; never front-load the repo.
3. **Compaction** - over the token budget, summarize old turns, keep task +
   decisions + current state. (What lets it run for hours.)
4. **Memory** - read a memory file at start, append durable facts (survives runs).
5. **Budget** - track tokens every turn (Track 5's lesson, applied).

...wrapped around a plain tool-use loop whose **stop condition is a VERIFIER**
(the tests pass), never the model's say-so.

## Run it
```bash
python3 harness.py --dry-run          # keyless: fakes the model, fixes a planted bug, CI-safe
ANTHROPIC_API_KEY=... python3 harness.py \
    --repo ./yourproject --task "make the failing tests pass" --test "pytest -q"
```
The `--dry-run` output is committed in `recorded-run.log` - the loop reads the
repo, sees the test fail, edits the code, re-runs, and stops when the **verifier
agrees**:
```
[step 1]  context ~66 tok / 12000 budget
  tool run_bash(...) -> test fails (add subtracts)
[step 3]  model: The bug: add() subtracts. Fixing it.  ->  write_file mathlib.py
[step 5]  model: DONE   [verifier] exit 0
[done] model said DONE and the verifier agrees.
```

## The architecture (read `harness.py` top to bottom - ~260 lines)
- **TOOLS** (`read / write / list / bash`) - they fetch; context decides what's seen.
- **`class Context`** - the star. The working set, `compact()`, `remember()`,
  `used()`/budget, `render()` (what actually goes to the model each turn).
- **`run()`** - the loop; ends on `verify()`, not on the model.
- **RealClient / FakeClient** - real Anthropic API, or a scripted model for the
  keyless demo (the `production/` FakeClient pattern).

## Make it yours (the only 3 lines you change)
- `--repo` - your project (also the **sandbox**: the agent only touches this).
- `--task` - what you want, in plain English.
- `--test` - the verifier command (`exit 0` == done).

Everything else - more tools, MCP, sub-agents, plan-mode - is *additions to this
core*. That's the production leap; the essence is here.

## Safety (rule 18)
The agent runs bash and edits files, but only inside `--repo` (a throwaway scratch
copy in `--dry-run`); `run_bash` is gated by a read-only-ish allowlist. Widen it
deliberately, never blindly - this is course-1's Module 9 (the sandbox) applied
to your own machine.

## Honest limits
The dry-run's "model" is scripted (deterministic, so CI can run it and you can
read the whole flow keyless). The real run needs a key and a real model; the
`compact()`/`summarize()` path only triggers on long runs. The idea is real; the
demo is a fixture.
