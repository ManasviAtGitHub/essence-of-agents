"""codec.py -- short-code generation for snip.

A code is a random string over ALPHABET (base62 minus the look-alike characters).
It is NEVER derived from the row id, the URL, or the time -- that randomness IS the
security model. See docs/harness/lessons.md #1 (the enumeration incident) and
docs/harness/decisions.md (why random, why base57, why 7 chars).
"""
import secrets

# base62 minus 0 O 1 l I -- 57 chars, unambiguous read-aloud / on paper (decisions.md).
ALPHABET = "23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
CODE_LEN = 7                                   # 57**7 ~ 1.9e12 (decisions.md: "why 7")


def make_code(exists):
    """Return a fresh random code that is not already in the store.

    `exists(code) -> bool` is the store's membership check, injected so this stays
    pure and testable. The retry loop almost never fires (see decisions.md).

    Note there is NO id/url/time argument, and there must never be one again -- that
    was the regression that made codes enumerable (lessons.md #1).
    """
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))
        if not exists(code):
            return code


def is_valid_code(code):
    """True if `code` has the shape make_code() produces (not an existence check)."""
    return (isinstance(code, str) and len(code) == CODE_LEN
            and all(c in ALPHABET for c in code))
