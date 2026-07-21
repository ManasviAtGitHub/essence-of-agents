"""snip -- a tiny URL shortener (the worked example for the B1 harness).

Public surface: the three verbs the CLI exposes, plus the codec primitives.
Read CLAUDE.md first; each module has a deep-dive under docs/harness/.
"""
from .codec import make_code, is_valid_code, ALPHABET, CODE_LEN
from .store import Store
from .api import create, resolve, stats

__all__ = ["make_code", "is_valid_code", "ALPHABET", "CODE_LEN", "Store", "create", "resolve", "stats"]
