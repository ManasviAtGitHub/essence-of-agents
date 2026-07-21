# Lessons (bugs we already paid for)

> Read this before touching the area a lesson names. It's how the harness stops the
> agent (or a new dev) from re-buying a bug the team already paid for.
>
> **Format for every entry:** Symptom -> Root cause -> Fix -> Rule.

---

## 1. Enumerable short-codes (2026-07-05)

- **Symptom:** a user reported that after getting the link `/-/q7Kp2mx`... no -- they got `/-/c`, and then found they could walk `/-/b`, `/-/d`, `/-/e` and land on *other people's* links.
- **Root cause:** `make_code(row_id)` returned `base62(row_id)` -- so the code *was* the auto-increment id. Codes came out `b, c, d, ...`: sequential, and trivially enumerable.
- **Fix:** `codec.make_code()` now takes no id. It draws a random 7-char code from the alphabet and asks the store whether it exists, retrying on the (rare) collision. Existing codes were left as-is (rule #2: codes are permanent); only new ones are random.
- **Rule:** codes must NEVER be guessable (CLAUDE.md non-negotiable #1). Never derive a code from the id, a timestamp, or the URL. If you ever see `make_code(` take an argument again, that's the regression.

## 2. Lost writes under two creates (2026-07-09)

- **Symptom:** two `create`s fired close together; one of the two new links was missing from `runtime/snip.json` afterward.
- **Root cause:** `store.put` did read-modify-write on the whole JSON file with no atomicity -- the second reader loaded the file before the first had written, then overwrote it.
- **Fix:** `put` now writes to a temp file and `os.replace`s it (atomic on POSIX + Windows), under a per-process lock. Full detail in [`store.md`](store.md).
- **Rule:** any whole-file JSON store mutates via write-temp-then-replace, never in place. See the Do list.

## 3. `resolve` slowed down by the hit counter (2026-07-11)

- **Symptom:** redirects got noticeably slower under load; p95 latency tracked the disk, not the lookup.
- **Root cause:** `resolve` was doing a synchronous `store.put` to increment `hits` before returning the URL -- a disk write on the hot read path.
- **Fix:** the URL is returned immediately; the hit increment is queued and flushed in the background. A dropped increment is acceptable; a slow redirect is not.
- **Rule:** resolve must not block on the hit-counter write (CLAUDE.md non-negotiable #4).
