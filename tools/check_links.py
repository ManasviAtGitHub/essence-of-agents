"""Stale-connection checker: resolve every local reference in the UI (static href/src,
plus JS-embedded paths like NAV entries, iframe srcs, gallery manifest, README links) and
report any that point at a file that does not exist.

    python tools/check_links.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# candidate refs: href/src attributes, and any quoted string that looks like a local file path
ATTR = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')
QUOTED = re.compile(r'"([^"\s]+?\.(?:html|md|css|js))"')

SKIP = ("http://", "https://", "//", "#", "data:", "javascript:", "mailto:", "..")


def is_external(p):
    return p.startswith(("http://", "https://", "//", "data:", "javascript:", "mailto:", "#"))


def clean(p):
    p = p.split("#")[0].split("?")[0].strip()
    return p


def refs_in(path):
    txt = open(path, encoding="utf-8").read()
    out = set()
    for m in list(ATTR.findall(txt)) + list(QUOTED.findall(txt)):
        if "${" in m or "+" in m or "'" in m or "*" in m or is_external(m) or not m or m.startswith("/"):
            continue  # skip templated ("${x}" or '"+x+"' concatenation), external, and absolute-root literals
        out.add(clean(m))
    # course + frontier hubs: LESSONS link to each module's README, derived from the widget src
    if path.endswith(os.path.join("agentic-course", "index.html")) or path.endswith(os.path.join("frontier", "index.html")):
        for src in re.findall(r'src:\s*"([^"]+/widgets/[^"]+)"', txt):
            out.add(src.split("/widgets/")[0] + "/README.md")
    return out


def main():
    files = (glob.glob(os.path.join(ROOT, "agentic-course", "**", "*.html"), recursive=True) +
             glob.glob(os.path.join(ROOT, "production", "**", "*.html"), recursive=True) +
             glob.glob(os.path.join(ROOT, "models", "**", "*.html"), recursive=True) +
             glob.glob(os.path.join(ROOT, "frontier", "**", "*.html"), recursive=True) +
             [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "tools", "gallery.mjs")])
    files = [f for f in files if "node_modules" not in f]

    stale = []
    checked = 0
    for f in files:
        base = ROOT if f.endswith("gallery.mjs") else os.path.dirname(f)
        for ref in refs_in(f):
            if not ref or ref.startswith("assets/") is None:
                pass
            target = os.path.normpath(os.path.join(base, ref))
            checked += 1
            if not os.path.exists(target):
                stale.append((os.path.relpath(f, ROOT), ref))

    if stale:
        print("STALE CONNECTIONS FOUND:")
        for src, ref in stale:
            print(f"  {src}  ->  {ref}   (missing)")
        raise SystemExit(1)
    print(f"ok - {checked} local references checked across {len(files)} files, 0 stale")


if __name__ == "__main__":
    main()
