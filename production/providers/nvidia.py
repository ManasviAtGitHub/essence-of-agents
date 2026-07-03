"""NVIDIA provider adapter (OpenAI-compatible) exposed in the harness's client shape.

NVIDIA's API (https://integrate.api.nvidia.com) is OpenAI chat-completions compatible --
a DIFFERENT provider than Anthropic. This adapter translates BOTH directions, including
tool calls, into the small surface the harness/agent_pro use
(`client.messages.create(...)` returning .content / .stop_reason / .usage), so the entire
tool-using agent loop can run live against an NVIDIA-hosted model.

The key is read from NVIDIA_API_KEY (env, or a gitignored .env). It is never logged.

    NvidiaClient(model="meta/llama-3.1-8b-instruct")
"""
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field

NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
_FINISH = {"stop": "end_turn", "length": "max_tokens", "tool_calls": "tool_use",
           "content_filter": "refusal"}


def _load_dotenv():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


@dataclass
class _Text:
    text: str
    type: str = "text"


@dataclass
class _ToolUse:
    name: str
    input: dict
    id: str
    type: str = "tool_use"


@dataclass
class _Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0


@dataclass
class _Reply:
    content: list
    stop_reason: str
    usage: _Usage
    model: str


def _block_attr(b, key, default=None):
    return b.get(key, default) if isinstance(b, dict) else getattr(b, key, default)


def _to_oai_messages(messages, system):
    """Translate harness/Anthropic messages -> OpenAI chat messages (with tool calls)."""
    out = []
    if system:
        out.append({"role": "system", "content": system})
    for m in messages:
        role, content = m["role"], m["content"]
        if isinstance(content, str):
            out.append({"role": role, "content": content})
            continue
        if role == "assistant":
            text_parts, tool_calls = [], []
            for b in content:
                t = _block_attr(b, "type")
                if t == "text":
                    text_parts.append(_block_attr(b, "text", ""))
                elif t == "tool_use":
                    tool_calls.append({
                        "id": _block_attr(b, "id"),
                        "type": "function",
                        "function": {"name": _block_attr(b, "name"),
                                     "arguments": json.dumps(_block_attr(b, "input", {}))},
                    })
            msg = {"role": "assistant", "content": ("\n".join(text_parts) or None)}
            if tool_calls:
                msg["tool_calls"] = tool_calls
            out.append(msg)
        else:  # user turn: tool_result blocks become OpenAI "tool" messages
            text_parts = []
            for b in content:
                t = _block_attr(b, "type")
                if t == "tool_result":
                    body = _block_attr(b, "content", "")
                    if _block_attr(b, "is_error", False):
                        body = "ERROR: " + str(body)
                    out.append({"role": "tool", "tool_call_id": _block_attr(b, "tool_use_id"),
                                "content": str(body)})
                elif t == "text":
                    text_parts.append(_block_attr(b, "text", ""))
            if text_parts:
                out.append({"role": "user", "content": "\n".join(text_parts)})
    return out


def _to_oai_tools(tools):
    """Anthropic tool specs -> OpenAI function-tool specs."""
    return [{"type": "function",
             "function": {"name": t["name"], "description": t.get("description", ""),
                          "parameters": t.get("input_schema", {})}} for t in tools]


class _Messages:
    def __init__(self, outer):
        self._o = outer

    def create(self, model=None, max_tokens=1024, messages=None, system=None,
               tools=None, **_kw):
        return self._o._create(model, max_tokens, messages or [], system, tools)


class NvidiaClient:
    def __init__(self, model="meta/llama-3.1-8b-instruct", api_key=None, timeout=90):
        _load_dotenv()
        self.model = model
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set NVIDIA_API_KEY in the environment (or a gitignored .env).")
        self.timeout = timeout
        self.messages = _Messages(self)

    def _create(self, model, max_tokens, messages, system, tools):
        payload = {"model": model or self.model, "max_tokens": max_tokens,
                   "messages": _to_oai_messages(messages, system)}
        if tools:
            payload["tools"] = _to_oai_tools(tools)
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            NVIDIA_URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"NVIDIA API {e.code}: {e.read().decode()[:400]}") from None

        choice = data["choices"][0]
        msg = choice.get("message", {})
        blocks = []
        if msg.get("content"):
            blocks.append(_Text(msg["content"]))
        for tc in (msg.get("tool_calls") or []):
            fn = tc.get("function", {})
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            blocks.append(_ToolUse(name=fn.get("name"), input=args, id=tc.get("id")))
        if not blocks:
            blocks.append(_Text(""))

        stop = "tool_use" if msg.get("tool_calls") else _FINISH.get(choice.get("finish_reason"), "end_turn")
        u = data.get("usage", {}) or {}
        return _Reply(blocks, stop,
                      _Usage(u.get("prompt_tokens", 0), u.get("completion_tokens", 0)),
                      data.get("model", model or self.model))
