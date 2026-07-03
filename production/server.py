"""Deployable HTTP front end for the agent (stdlib only -- no web framework).

    GET  /health        -> {"status": "ok"}
    POST /chat {"task"}  -> {"answer": ..., "metrics": {...}}

Provider via env: AGENT_PROVIDER (fake|nvidia|anthropic), AGENT_MODEL. Run:

    python production/server.py            # serves on 127.0.0.1:8088

The request handler (`handle`) is importable and unit-tested with no socket and no key.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # repo root -> claude_harness
sys.path.insert(0, _HERE)                    # production

from agent_pro import ProAgent
from claude_harness.builtins import calculate, list_dir, read_file
from observability import summarize


def _default_factory():
    from run_agent import _DEFAULT_MODEL, build_client
    provider = os.environ.get("AGENT_PROVIDER", "nvidia")
    model = os.environ.get("AGENT_MODEL") or _DEFAULT_MODEL.get(provider)
    return ProAgent(tools=[calculate, read_file, list_dir], model=model,
                    client=build_client(provider, model))


def handle(task: str, factory=None) -> dict:
    """Core request logic -- build an agent, run the task, return answer + metrics."""
    agent = (factory or _default_factory)()
    result = agent.run(task)
    return {"answer": result.text, "metrics": summarize(result)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send_html()
        if self.path.startswith("/chat/stream"):
            return self._chat_stream()
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        if self.path.startswith("/assets/"):
            return self._send_asset()
        self._send(404, {"error": "not found"})

    def _send_asset(self):
        """Serve the shared library (repo-root /assets/) so the stage can load cast.js/anim.js."""
        name = os.path.basename(urlparse(self.path).path)  # basename only -> no path traversal
        path = os.path.join(os.path.dirname(_HERE), "assets", name)
        ext = name.rsplit(".", 1)[-1].lower()
        ctype = {"js": "application/javascript", "css": "text/css"}.get(ext, "application/octet-stream")
        try:
            with open(path, "rb") as fh:
                body = fh.read()
        except OSError:
            return self._send(404, {"error": "not found"})
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self):
        path = os.path.join(_HERE, "web", "index.html")
        try:
            with open(path, "rb") as fh:
                body = fh.read()
        except FileNotFoundError:
            body = b"<h1>chat UI not found</h1>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _chat_stream(self):
        """Stream the agent's loop live as Server-Sent Events (one frame per loop event)."""
        task = (parse_qs(urlparse(self.path).query).get("task", [""])[0]).strip()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        def emit(ev):
            try:
                self.wfile.write(("data: " + json.dumps(ev) + "\n\n").encode())
                self.wfile.flush()
            except Exception:
                pass

        if not task:
            emit({"kind": "error", "error": "missing task"})
            return emit({"kind": "done"})
        try:
            result = _default_factory().run(task, on_event=emit)  # emits each loop event live
            emit({"kind": "answer", "text": result.text, "metrics": summarize(result)})
        except Exception as e:
            emit({"kind": "error", "error": type(e).__name__})
        emit({"kind": "done"})

    def do_POST(self):
        if self.path != "/chat":
            return self._send(404, {"error": "not found"})
        n = int(self.headers.get("Content-Length", 0) or 0)
        data = json.loads(self.rfile.read(n) or b"{}")
        task = data.get("task", "")
        if not task:
            return self._send(400, {"error": "missing 'task'"})
        try:
            self._send(200, handle(task))
        except Exception as e:  # never leak internals/keys
            self._send(500, {"error": type(e).__name__})


def main(host="127.0.0.1", port=8088):
    print(f"serving on http://{host}:{port}  (POST /chat, GET /health)")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
