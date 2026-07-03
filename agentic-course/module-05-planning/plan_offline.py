"""Module 5 -- plan, execute, and re-plan, built by hand (keyless).

The control flow is real; the plans are scripted so it runs with no key. Toggle
re-planning to feel the difference (the "break it on purpose" beat).

    python agentic-course/module-05-planning/plan_offline.py
"""

TASK = "Add a /health endpoint and get the tests passing."
RIGID = [
    {"step": "Add the /health route", "ok": True},
    {"step": "Run the tests", "ok": False, "err": "ImportError: app not found"},
]
REPLAN = [
    {"step": "Read the project layout", "ok": True},
    {"step": "Fix the import path", "ok": True},
    {"step": "Run the tests", "ok": True},
]


def execute(plan):
    """Run steps in order; return the first failing step (or None if all pass)."""
    for s in plan:
        print(("  [ok] " if s["ok"] else "  [x]  ") + s["step"])
        if not s["ok"]:
            return s
    return None


def run(replan):
    print(f"task: {TASK}   (re-plan on fail: {'ON' if replan else 'OFF'})")
    failed = execute(RIGID)
    if failed and replan:
        print(f"  -> re-planning from the error: {failed['err']}")
        execute(REPLAN)
        print("  result: done -- re-planned around the failure.\n")
    elif failed:
        print(f"  result: STUCK -- {failed['err']} (the stale plan didn't survive reality)\n")


run(replan=True)
run(replan=False)   # break it on purpose: watch the rigid plan die on the first surprise
print("Plans are disposable. The ability to re-plan from the new state is the asset.")
