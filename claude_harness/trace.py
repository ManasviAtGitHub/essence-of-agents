"""Run traces - a record of the agent loop, for inspection and for replay.

A Trace timestamps every model reply, tool call, and tool result relative to when
it was created. Saved as JSON, it is a step-by-step log you can inspect or replay
without re-hitting the API. (The course widgets ship with their own scripted or
recorded data; they do not read this format.)
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field


@dataclass
class Trace:
    id: str = "agent-run"
    events: list = field(default_factory=list)
    _t0: float = field(default_factory=time.perf_counter, repr=False)

    def _add(self, kind: str, data: dict) -> None:
        self.events.append(
            {
                "kind": kind,
                "t_ms": int((time.perf_counter() - self._t0) * 1000),
                "data": data,
            }
        )

    # one method per event the loop emits ----------------------------------
    def model(self, reply) -> None:
        self._add(
            "model_reply",
            {
                "stop_reason": reply.stop_reason,
                "text": "".join(b.text for b in reply.content if b.type == "text"),
            },
        )

    def tool_use(self, name: str, args: dict, id: str) -> None:
        self._add("tool_use", {"name": name, "args": args, "id": id})

    def tool_result(self, id: str, output, is_error: bool) -> None:
        self._add(
            "tool_result",
            {"id": id, "output": str(output)[:2000], "is_error": is_error},
        )

    def final(self, text: str) -> None:
        self._add("final", {"text": text})

    # persistence ----------------------------------------------------------
    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"id": self.id, "events": self.events},
                f,
                ensure_ascii=False,
                indent=2,
            )
