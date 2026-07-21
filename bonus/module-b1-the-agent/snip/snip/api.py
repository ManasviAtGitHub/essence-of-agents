"""api.py -- the CLI for snip (create / resolve / stats).

Thin: it wires codec + store together and nothing else. `resolve` returns the URL
immediately and bumps the hit counter separately -- never on the read path
(CLAUDE.md non-negotiable #4, docs/harness/lessons.md #3).
"""
import os
import sys

from .codec import make_code, is_valid_code
from .store import Store

RUNTIME = os.environ.get("SNIP_DB", "runtime/snip.json")


def _store():
    return Store(RUNTIME)


def create(url):
    s = _store()
    code = make_code(s.exists)        # make_code takes NO id -- never make it guessable
    s.put(code, url)
    return code


def resolve(code):
    if not is_valid_code(code):
        return None
    s = _store()
    url = s.get(code)
    if url is not None:
        s.bump(code)                  # in production this is queued off the hot path
    return url


def stats(code):
    return _store().hits(code)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: snip <create|resolve|stats> ...")
        return 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "create":
        print(create(rest[0]))
        return 0
    if cmd == "resolve":
        url = resolve(rest[0])
        print(url if url else "not found")
        return 0 if url else 1
    if cmd == "stats":
        h = stats(rest[0])
        print(h if h is not None else "not found")
        return 0 if h is not None else 1
    print("unknown command: " + cmd)
    return 2
