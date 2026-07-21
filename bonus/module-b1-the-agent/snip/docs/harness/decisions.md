# Design Decisions (snip)

> Read when weighing a design change, so you don't undo a choice that was made for a
> reason you can't see from the code alone.

---

## Why random codes, not sequential

Sequential codes (the row id in base62: `1->b, 2->c`) make every link enumerable --
scrape one, walk the alphabet, get them all. We generate a **random** code and check
the store for a collision. Cost: one extra store read per `create`; cheap, and the
retry loop almost never fires. The incident that forced this is [`lessons.md`](lessons.md) #1;
the rule is CLAUDE.md non-negotiable #1.

## Why 7 characters

With a 57-char alphabet, `57^7 ~ 1.9e12`. At a million live links the
birthday-collision probability per create is ~`1e-6`, so the retry loop is effectively
never hit. 6 chars (`57^6 ~ 3.4e10`) collides often enough to matter at scale; 8 is
longer for no benefit. If live-link count ever approaches `1e9`, revisit -- bump to 8,
don't shrink the alphabet.

## Why base57 (base62 minus look-alikes)

We dropped `0 O 1 l I` from the alphabet so a code is unambiguous read aloud, copied
off a printed page, or dictated over the phone. 62 -> 57 characters; length stays 7
(the math above uses 57). The alphabet lives in one place, `codec.ALPHABET` -- never
inline a different one.

## Why a single JSON file store (for now)

Walking-skeleton: one file (`runtime/snip.json`) is enough to prove create/resolve/stats
end to end and to ship the first version. The **interface** -- `store.put/get/hits` -- is
the contract; the backend is not. Swap in SQLite behind that interface the day write
volume needs it, without touching `codec` or `api`. Don't add a database before the file
store actually hurts.

## Why hits are eventually-consistent

`stats` is a soft number -- it's fine for it to lag or drop the occasional increment.
That's the price of keeping `resolve` off the disk-write path (non-negotiable #4). If
you ever need exact hit accounting, that's a real feature with its own storage, not a
tweak to `resolve`.
