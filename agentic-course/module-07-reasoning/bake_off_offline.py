"""Module 7 -- the three-way bake-off harness (keyless).

The harness (loop over task x approach, score, tabulate) is real; the per-cell outcomes
are scripted so it runs with no key. The shape is the lesson: reasoning INSIDE the model
substitutes for steps OUTSIDE it only when the missing ingredient is deliberation.

    python agentic-course/module-07-reasoning/bake_off_offline.py
"""

TASKS = ["deliberation puzzle", "needs an external fact"]
APPROACHES = ["more inside (reasoning)", "more outside (tool steps)", "both (kitchen sink)"]

# (accuracy, relative_cost) per (task index, approach index). Illustrative outcomes.
RESULTS = {
    (0, 0): (0.92, "high"),  (0, 1): (0.55, "high"),  (0, 2): (0.90, "very high"),
    (1, 0): (0.18, "high"),  (1, 1): (0.90, "low"),   (1, 2): (0.90, "very high"),
}


def best(task_i):
    return max(range(len(APPROACHES)), key=lambda a: RESULTS[(task_i, a)][0])


print(f"{'task':22}{'approach':26}{'acc':>6}  cost")
print("-" * 62)
for ti, task in enumerate(TASKS):
    for ai, approach in enumerate(APPROACHES):
        acc, cost = RESULTS[(ti, ai)]
        star = "  <- best" if ai == best(ti) else ""
        print(f"{task:22}{approach:26}{round(acc*100):>5}%  {cost}{star}")
    print()

print("Puzzle -> reasoning inside wins. Fact -> a tool step outside wins.")
print("Match the spend to the bottleneck: deliberation goes inside, information goes outside.")
print("(Outcomes scripted offline; CHALLENGE.md runs the real bake-off with live models.)")
