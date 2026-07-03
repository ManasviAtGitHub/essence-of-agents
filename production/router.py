"""Model routing + fallback (Modules 7 + 11 in production).

Pick a (client, model) per task -- e.g. a cheap model by default, a stronger one when the
task needs deliberation -- and fall back to the next option on a hard error or a refusal.
Each option: {name, client, model, when?(task)->bool}. Options whose `when` matches the
task are tried first; ties keep declared order.
"""
from typing import Callable, Optional


class Router:
    def __init__(self, options: list):
        self.options = options

    def _ordered(self, task: str):
        return sorted(self.options, key=lambda o: 0 if (o.get("when") and o["when"](task)) else 1)

    def run(self, task: str, **agent_kw):
        from agent_pro import ProAgent  # local import keeps router importable without it
        last = None
        for opt in self._ordered(task):
            try:
                result = ProAgent(client=opt["client"], model=opt.get("model", "default"),
                                  **agent_kw).run(task)
                if result.stop_reason != "refusal":
                    return opt["name"], result
                last = "refusal"
            except Exception as e:  # transient/hard error -> try the next option
                last = e
        raise RuntimeError(f"all routes failed; last={last}")


def needs_reasoning(task: str) -> bool:
    """A trivial heuristic for the 'when' hook (Module 7's lever, productionized)."""
    t = task.lower()
    return any(w in t for w in ("prove", "step by step", "reason", "puzzle", "why", "plan"))
