"""Convert course text files to pure ASCII so they render correctly in any viewer.

The files are valid UTF-8, but cp1252 viewers (common on Windows) show mojibake for
em dashes, arrows, middots, etc. Pure ASCII sidesteps that everywhere.

    python tools/asciify.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF = os.path.abspath(__file__)
EXTS = {".md", ".html", ".py", ".txt", ".mjs", ".json"}
SKIP_DIRS = {"node_modules", ".git"}

# Keys are unicode escapes so this script stays pure ASCII (and won't rewrite itself).
REPL = {
    "—": "-", "–": "-", "‒": "-", "‐": "-", "‑": "-", "−": "-",
    "→": "->", "←": "<-", "↑": "^", "↓": "v", "↻": "(re)",
    "·": "-", "•": "*", "…": "...",
    "“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", "‚": "'",
    "≈": "~", "≠": "!=", "≤": "<=", "≥": ">=", "×": "x", "÷": "/",
    " ": " ", " ": " ", " ": " ", "​": "", "﻿": "",
    "✓": "[ok]", "✗": "[x]", "✅": "[ok]", "☑": "[x]", "⚠": "[!]",
    "▶": ">", "▸": ">", "▾": "v", "│": "|", "█": "#", "▌": "|",
    "\U0001f512": "[lock]", "\U0001f6e1": "[shield]",
}


def asciify(text):
    out, dropped = [], set()
    for ch in text:
        if ord(ch) < 128:
            out.append(ch)
        elif ch in REPL:
            out.append(REPL[ch])
        else:
            dropped.add(ch)
    return "".join(out), dropped


changed, all_dropped = [], set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for name in filenames:
        if os.path.splitext(name)[1].lower() not in EXTS:
            continue
        path = os.path.join(dirpath, name)
        if os.path.abspath(path) == SELF:
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        new, dropped = asciify(text)
        all_dropped |= dropped
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            changed.append(os.path.relpath(path, ROOT))

print(f"asciified {len(changed)} file(s):")
for c in changed:
    print("  ", c)
print("dropped unmapped non-ASCII:", sorted(repr(c) for c in all_dropped) if all_dropped else "none")
