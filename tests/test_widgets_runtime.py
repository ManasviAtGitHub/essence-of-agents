"""Runtime gate: runs tools/check_widgets.mjs (headless) to catch JS console errors,
uncaught exceptions, blank renders, and scenes whose scrubber/characters did not build --
things the text-only checks cannot see. Skips gracefully if node/playwright are absent.

    python tests/test_widgets_runtime.py
    pytest tests
"""
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_widgets_runtime_clean():
    if not shutil.which("node"):
        print("skip - node not found"); return
    if not os.path.isdir(os.path.join(ROOT, "node_modules", "playwright")):
        print("skip - playwright not installed (run: npm install)"); return
    r = subprocess.run(["node", "tools/check_widgets.mjs"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2500:]); print(r.stderr[-1000:])
    assert r.returncode == 0, "widget runtime gate failed (see output above)"


if __name__ == "__main__":
    test_widgets_runtime_clean()
    print("ok - widget runtime gate")
