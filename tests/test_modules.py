"""Automated checks for the course: every keyless demo runs, every widget is well-formed,
and all course text is pure ASCII. Run either:

    python tests/test_modules.py
    pytest
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "agentic-course")

KEYLESS_DEMOS = [
    "module-01-hands/schema_demo.py",
    "module-01-hands/offline_demo.py",
    "module-02-the-loop/react_demo.py",
    "module-03-context/context_recipes.py",
    "module-04-memory/rag_offline.py",
    "module-05-planning/plan_offline.py",
    "module-06-verification/verify_offline.py",
    "module-07-reasoning/bake_off_offline.py",
    "module-08-multi-agent/fanout_offline.py",
    "module-09-security/injection_offline.py",
    "module-10-evaluation/eval_offline.py",
    "module-11-shipping/close_loop.py",
]


def test_keyless_demos_run():
    for rel in KEYLESS_DEMOS:
        path = os.path.join(COURSE, rel)
        assert os.path.exists(path), f"missing demo: {rel}"
        r = subprocess.run([sys.executable, path], capture_output=True, text=True)
        assert r.returncode == 0, f"{rel} failed:\n{r.stderr}"


def test_widgets_wellformed():
    widgets = glob.glob(os.path.join(COURSE, "**", "widgets", "**", "index.html"), recursive=True)
    assert len(widgets) >= 12, f"expected >=12 widgets, found {len(widgets)}"
    for w in widgets:
        s = open(w, encoding="utf-8").read()
        assert 'charset="utf-8"' in s, f"no charset in {w}"
        assert "<script>" in s, f"no script in {w}"


def test_course_text_is_ascii():
    files = []
    for base in (COURSE, os.path.join(ROOT, "claude_harness"), os.path.join(ROOT, "assets")):
        for ext in ("md", "html", "py", "css", "js"):
            files += glob.glob(os.path.join(base, "**", f"*.{ext}"), recursive=True)
    files.append(os.path.join(ROOT, "index.html"))  # the root launcher
    for f in files:
        if "node_modules" in f:
            continue
        data = open(f, "rb").read()
        bad = [b for b in data if b > 127]
        assert not bad, f"non-ASCII bytes in {os.path.relpath(f, ROOT)}"


if __name__ == "__main__":
    test_keyless_demos_run()
    print("ok - all keyless demos run")
    test_widgets_wellformed()
    print("ok - all widgets well-formed")
    test_course_text_is_ascii()
    print("ok - all course text is ASCII")
    print("ALL MODULE CHECKS PASSED")
