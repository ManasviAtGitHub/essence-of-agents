"""Persistence -- durable session records (the seam Module 11 needs).

A SessionStore writes each run (answer, usage, full event trace) to JSON so failures can
become eval cases later and sessions can be inspected/resumed. JSON for simplicity; swap
for sqlite/postgres in real deployments without changing callers.
"""
import json
import os


class SessionStore:
    def __init__(self, root: str):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def _path(self, session_id: str) -> str:
        safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
        return os.path.join(self.root, safe + ".json")

    def save(self, session_id: str, result) -> str:
        data = {
            "id": session_id,
            "text": result.text,
            "stop_reason": result.stop_reason,
            "usage": vars(result.usage),
            "events": result.events,
        }
        path = self._path(session_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path

    def load(self, session_id: str) -> dict:
        with open(self._path(session_id), encoding="utf-8") as f:
            return json.load(f)

    def list(self) -> list:
        return [f[:-5] for f in os.listdir(self.root) if f.endswith(".json")]
