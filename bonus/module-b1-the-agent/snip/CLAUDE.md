# snip -- Agent Harness (the front door)

> Read this FIRST in every session. Deep-dive docs are linked below -- open one only
> when you're working that subsystem.
>
> **Design philosophy:** walking skeleton -- the smallest thing that resolves a link,
> hardened one subsystem at a time behind its interface.
>
> **Before editing this file or docs/harness/:** read [`maintenance_policy.md`](docs/harness/maintenance_policy.md). ~140-line cap on this file.

---

## Run it

```bash
python -m snip create https://example.com/some/long/path   # -> prints a short code
python -m snip resolve q7Kp2mx                              # -> the original URL
python -m snip stats   q7Kp2mx                              # -> hit count
python -m snip serve --port 8000                            # optional HTTP (GET /<code> -> 302)

pytest -q                                                   # ~2s, whole suite
pytest -q -k codec                                          # just the short-code tests
```

Data lives in `runtime/snip.json` (gitignored). Delete it to reset.

---

## Map

`create` -> `codec.make_code()` -> `store.put(code, url)`  |  `resolve` -> `store.get(code)`  |  `stats` -> `store.hits(code)`

**Modules** (`snip/`): `codec.py` (short-code generation), `store.py` (JSON persistence, the code->url source of truth), `api.py` (CLI + optional FastAPI). Everything writes under `runtime/`.

---

## Non-negotiables (the golden rules)

1. **Codes must NEVER be guessable.** Random + collision-checked -- never sequential, never derived from the row id / timestamp / URL. This is the whole security model. (Why: [`lessons.md`](docs/harness/lessons.md) #1.)
2. **Codes are permanent.** Once issued, a code always maps to the same URL. Never reassign or recycle a code -- old links must never silently point somewhere new.
3. **The store is the source of truth** for `code -> url`. Never reconstruct a code from a URL, or a URL from a code by any path but the store.
4. **Resolve stays cheap and read-mostly.** It may bump a hit counter; it must not block on that write, and it does nothing else with side effects.

---

## Do / Don't

**Do**
- Validate a code with `is_valid_code()` before touching the store.
- Use the base57 alphabet in `codec.ALPHABET` (base62 minus the look-alikes `0 O 1 l I`). Why: [`decisions.md`](docs/harness/decisions.md).
- Keep `runtime/` out of git (it's user data).

**Don't**
- Use sequential, timestamp-, or id-derived codes (breaks rule #1 -- see the incident in `lessons.md`).
- Log full URLs at INFO level (they can carry tokens/PII); log the code, not the target.
- Widen the alphabet to include look-alikes (breaks read-aloud/print copying).
- Block `resolve` on the hit-counter write (breaks rule #4).

---

## Current baseline

See [`baseline.md`](docs/harness/baseline.md) for code length, alphabet size, collision rate, and test count. Update it there after any material change; no commentary in this file.

---

## Deep-dives (read on demand)

| Doc | When to read |
|-----|-------------|
| [`codec.md`](docs/harness/codec.md) | short-code generation: alphabet, length math, collision handling |
| [`store.md`](docs/harness/store.md) | persistence format, atomic writes, the put/get/hits interface, migration |
| [`decisions.md`](docs/harness/decisions.md) | why random codes, why base57, why a JSON file, why 7 chars |
| [`lessons.md`](docs/harness/lessons.md) | bugs we already paid for -- **read before touching codec or store** |
| [`maintenance_policy.md`](docs/harness/maintenance_policy.md) | how to keep this file + docs/harness/ lean |
| [`log/`](docs/log/) | the dated journal: what was decided, when, and why |
