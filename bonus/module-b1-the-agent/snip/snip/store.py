"""store.py -- JSON-file persistence for snip. The source of truth for code -> url.

Every mutation goes write-temp-then-os.replace (atomic on POSIX + Windows) under a
process lock -- that's the fix for the lost-writes incident (docs/harness/lessons.md #2).
The put / get / hits / bump interface is the contract; the JSON backend is swappable
for SQLite behind it (docs/harness/decisions.md).
"""
import json
import os
import tempfile
import threading

_LOCK = threading.Lock()


class Store:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def _load(self):
        if not os.path.isfile(self.path):
            return {}
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        # atomic: write a temp file in the same dir, then replace (lessons.md #2).
        d = os.path.dirname(self.path) or "."
        fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, self.path)

    def exists(self, code):
        return code in self._load()

    def put(self, code, url):
        with _LOCK:
            data = self._load()
            if code in data and data[code]["url"] != url:
                raise ValueError("codes are permanent (rule #2): " + code)
            if code not in data:
                data[code] = {"url": url, "hits": 0}
            self._save(data)

    def get(self, code):
        rec = self._load().get(code)
        return rec["url"] if rec else None

    def hits(self, code):
        rec = self._load().get(code)
        return rec["hits"] if rec else None

    def bump(self, code):
        with _LOCK:
            data = self._load()
            if code in data:
                data[code]["hits"] += 1
                self._save(data)
