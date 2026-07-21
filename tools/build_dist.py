"""Assemble a clean, deployable static site in dist/ -- only the files a browser needs.
Excludes secrets (.env), dev tooling, tests, node_modules, and all .py source. The real
agent code stays in the repo; the served site is pure HTML + simulations.

    python tools/build_dist.py     ->  dist/   (serve this, entry point index.html)
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}


def copy_tree(src, dst, skip_ext=()):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, src)
        target = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(target, exist_ok=True)
        for f in files:
            if f.lower().endswith(skip_ext):
                continue
            shutil.copy2(os.path.join(root, f), os.path.join(target, f))


if os.path.exists(DIST):
    shutil.rmtree(DIST)
os.makedirs(DIST)

# 1. launcher (entry point)
shutil.copy2(os.path.join(ROOT, "index.html"), os.path.join(DIST, "index.html"))
# 2. shared library (theme + cast + anim; skip the README/template docs is optional -- keep, tiny)
copy_tree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
# 3. the course: HTML widgets + linked READMEs; drop python demos + json artifacts
copy_tree(os.path.join(ROOT, "agentic-course"), os.path.join(DIST, "agentic-course"), skip_ext=(".py", ".json"))
# 3b. the models track (same rules)
copy_tree(os.path.join(ROOT, "models"), os.path.join(DIST, "models"), skip_ext=(".py", ".json"))
# 3c. the frontier track (same rules)
copy_tree(os.path.join(ROOT, "frontier"), os.path.join(DIST, "frontier"), skip_ext=(".py", ".json"))
# 3d. the serving track (Track 5, same rules; keeps weights.js, drops .py/.json)
copy_tree(os.path.join(ROOT, "serving"), os.path.join(DIST, "serving"), skip_ext=(".py", ".json"))
# 3e. the bonus track (the workshop): hub + widgets + worked-example docs; the runnable
# .py source stays repo-only (the hub links it on GitHub), logs/json never ship
copy_tree(os.path.join(ROOT, "bonus"), os.path.join(DIST, "bonus"), skip_ext=(".py", ".json", ".log"))
# 4. production SITE only: hub + scenes + the stage; NO .py source, providers, or tests
pdst = os.path.join(DIST, "production")
os.makedirs(pdst, exist_ok=True)
shutil.copy2(os.path.join(ROOT, "production", "index.html"), os.path.join(pdst, "index.html"))
copy_tree(os.path.join(ROOT, "production", "scenes"), os.path.join(pdst, "scenes"), skip_ext=(".py",))
copy_tree(os.path.join(ROOT, "production", "web"), os.path.join(pdst, "web"), skip_ext=(".py",))

# GitHub Pages: don't run the output through Jekyll (harmless everywhere else)
open(os.path.join(DIST, ".nojekyll"), "w").close()

# safety: make sure nothing secret slipped in
leaked = [p for p in (".env", "node_modules") for _ in [0] if os.path.exists(os.path.join(DIST, p))]
bad = []
for root, _, files in os.walk(DIST):
    for f in files:
        if f == ".env" or f.endswith(".py"):
            bad.append(os.path.relpath(os.path.join(root, f), DIST))
assert not bad, "secret/source leaked into dist: " + ", ".join(bad)

# safety: every door on the launcher must resolve inside dist (a track missing
# here ships as a live 404 -- exactly how the frontier track went missing once)
import re
launcher = open(os.path.join(DIST, "index.html"), encoding="utf-8").read()
for href in sorted(set(re.findall(r'href="([^"#]+\.html)"', launcher))):
    assert os.path.exists(os.path.join(DIST, *href.split("/"))), "launcher door 404s in dist: " + href

n = sum(len(fs) for _, _, fs in os.walk(DIST))
print(f"dist/ built: {n} files, no .env, no .py. Serve dist/ (entry: index.html).")
