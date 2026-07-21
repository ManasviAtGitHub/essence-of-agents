# codec -- short-code generation

> Read when working on how codes are made or validated. The security model lives here.

## What it does

`make_code(exists)` returns a fresh code; `is_valid_code(code)` checks the *shape* (not
existence). A code is `CODE_LEN` (7) random characters from `ALPHABET`.

## The alphabet (base57)

`ALPHABET` is base62 minus the five look-alikes `0 O 1 l I` -> 57 characters, so a code is
unambiguous read aloud or off a printed page. It lives in exactly one place; never inline a
different alphabet (see `decisions.md`).

## The length math

`57 ** 7 ~ 1.9e12`. At ~1M live links the birthday-collision probability per `create` is
~`1e-6`, so the collision-retry loop in `make_code` is effectively never taken. If the live
count ever approaches `1e9`, bump `CODE_LEN` to 8 -- never shrink the alphabet.

## Collision handling

`make_code` draws a candidate and calls `exists(code)` (the store's membership check,
dependency-injected so codec stays pure and testable). On the rare hit it just draws again.

## The one rule that must not regress

`make_code` takes **no** id / seed / timestamp / URL -- only the `exists` callback. Deriving
a code from any of those is what made codes enumerable (`lessons.md` #1). `test_codec.py`
pins the signature so the regression fails a test, not a user.
