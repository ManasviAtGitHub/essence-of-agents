# Harness Maintenance Policy (snip)

> How to keep CLAUDE.md lean and docs/harness/ usable. The harness is only worth
> reading if it stays small and true -- these rules are what keep it that way.

## CLAUDE.md (~140-line cap)

Only content needed **regardless of which subsystem you're in**:

- **Run it** -- the commands you type every session.
- **Map** -- pipeline + module list. Enough to orient, not to implement.
- **Non-negotiables + Do/Don't** -- short rules, no explanations.
- **Baseline** -- a pointer, not the numbers.
- **Deep-dive index** -- the table linking `docs/harness/*.md`.

The cap is the point: it forces you to push detail down into a deep-dive instead of
letting the front door rot into a dump.

## docs/harness/*.md

Subsystem detail only useful when actively working that area: how it works internally,
the design rationale (the *why*), the bugs and lessons, debug/regression workflows.

## When you add something

1. **"Does every session need this?"** Yes -> a short line in CLAUDE.md. No -> a deep-dive.
2. **A durable lesson?** One-line rule in CLAUDE.md's Do/Don't; the *why* goes in
   `decisions.md`, the *bug that taught it* goes in `lessons.md`.
3. **A new subsystem?** New `docs/harness/<name>.md` + one row in the index. Never inline
   50 lines of subsystem detail into the front door.
4. **One concern per file.** Never combine two topics (`decisions_and_lessons.md`) --
   split early, cross-link.

## The truth hierarchy

When they disagree: **running code + tests > harness docs > historical notes.** Trust
what you observe now, and fix the stale doc in the same change.

## Log before code

Every substantive decision or direction change gets a dated entry in `docs/log/` (what
was asked, what was decided, why) before or with the code it produced. The log is the
raw history; CLAUDE.md and the deep-dives are the compressed, current view of it.
