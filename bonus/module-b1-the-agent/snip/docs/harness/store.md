# store -- persistence

> Read when touching how links are saved. The store is the source of truth for code -> url.

## Format

One JSON object in `runtime/snip.json`: `{ "<code>": {"url": "...", "hits": 0}, ... }`.
Human-readable on purpose -- you can open it and see the whole state.

## The interface (this is the contract)

`Store.put(code, url)` / `get(code)` / `hits(code)` / `bump(code)` / `exists(code)`. Callers
(`api.py`) depend on these four verbs, never on the JSON. Swap in SQLite behind the same
interface the day write volume needs it, without touching codec or api (`decisions.md`).

## Atomic writes

`_save` writes a temp file in the same directory and `os.replace`s it -- atomic on POSIX and
Windows -- under a process lock. That's the fix for the lost-writes incident (`lessons.md`
#2). Never mutate the JSON in place.

## Permanence

`put` refuses to point an existing code at a different URL (raises `ValueError`) -- codes are
permanent (CLAUDE.md non-negotiable #2). Re-putting the *same* url is idempotent.

## Hits are soft

`bump` is called by `resolve` *after* the URL is returned, never before -- a slow redirect is
worse than a dropped increment (`lessons.md` #3). Don't move it onto the read path.
