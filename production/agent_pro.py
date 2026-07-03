"""agent_pro -- the production tier of the agent loop.

Same loop as claude_harness/agent.py (Module 0), wrapped in the things production needs
and the course deliberately left out: retries+backoff, streaming, cost/usage accounting,
a tool permission policy with an approval gate, an input guardrail on untrusted tool
output, a spend budget, and structured events for observability.

It stays offline-testable: pass a FakeClient (no .stream attr) and it uses .create();
in production it streams. The real Anthropic client is imported lazily, so the offline
path needs neither the SDK nor a key. See production/README.md.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from claude_harness.tools import Tool  # reuse the teaching tool registry

DEFAULT_MODEL = "claude-opus-4-8"
# USD per 1M tokens (input, output) -- see the claude-api reference.
PRICES = {
    "claude-opus-4-8": (5.0, 25.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}

log = logging.getLogger("agent_pro")


def _default_client():
    import anthropic
    return anthropic.Anthropic()


def injection_guardrail(text: str):
    """Default input guardrail: neutralize instruction-like text in untrusted tool
    output before it enters the context. Returns (clean_text, flagged)."""
    triggers = ["ignore", "instead", "disregard", "you must", "system:", "reveal", "api key"]
    low = text.lower()
    if any(t in low for t in triggers):
        return ("[guardrail: instruction-like content removed from untrusted output]\n"
                + " ".join(w for w in text.split() if not any(t in w.lower() for t in triggers))), True
    return text, False


def _default_compactor(messages, keep=4):
    """A simple local compactor: keep the first turn and the last `keep`, drop the middle.
    Real deployments use the server-side compaction beta; this keeps it keyless."""
    if len(messages) <= keep + 1:
        return messages
    note = {"role": "user", "content": "[older turns summarized to save context]"}
    return messages[:1] + [note] + messages[-keep:]


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cost_usd: float = 0.0
    steps: int = 0

    def add(self, model: str, u) -> None:
        i = getattr(u, "input_tokens", 0) or 0
        o = getattr(u, "output_tokens", 0) or 0
        self.input_tokens += i
        self.output_tokens += o
        self.cache_read += getattr(u, "cache_read_input_tokens", 0) or 0
        pin, pout = PRICES.get(model, (0.0, 0.0))
        self.cost_usd += i * pin / 1e6 + o * pout / 1e6


@dataclass
class Policy:
    """Per-tool permission: 'allow' | 'ask' | 'deny'."""
    default: str = "allow"
    rules: dict = field(default_factory=dict)

    def decision(self, name: str) -> str:
        return self.rules.get(name, self.default)


@dataclass
class Result:
    text: str
    usage: Usage
    stop_reason: str
    events: list


_RETRYABLE_NAMES = {"RateLimitError", "APIConnectionError", "APITimeoutError",
                    "InternalServerError", "OverloadedError"}


class ProAgent:
    def __init__(self, tools=(), model=DEFAULT_MODEL, system=None, client=None,
                 max_steps=20, max_tokens=4096, thinking=False, stream=True,
                 policy: Optional[Policy] = None,
                 approve: Optional[Callable[[str, dict], bool]] = None,
                 guardrail: Optional[Callable[[str], Any]] = injection_guardrail,
                 budget_usd: Optional[float] = None,
                 cache_system=False, compactor=None, compact_after=None,
                 max_retries=3, retry_base=0.5):
        self.tools = list(tools)
        self.model = model
        self.system = system
        self.client = client if client is not None else _default_client()
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.thinking = thinking
        self.stream = stream
        self.policy = policy or Policy()
        self.approve = approve
        self.guardrail = guardrail
        self.budget_usd = budget_usd
        self.cache_system = cache_system
        self.compactor = compactor
        self.compact_after = compact_after
        self.max_retries = max_retries
        self.retry_base = retry_base

    def _tool(self, name):
        return next((t for t in self.tools if t.name == name), None)

    def _retryable(self, e) -> bool:
        return type(e).__name__ in _RETRYABLE_NAMES or isinstance(e, (ConnectionError, TimeoutError))

    def _call(self, messages):
        kwargs: dict = dict(model=self.model, max_tokens=self.max_tokens, messages=messages)
        if self.system:
            if self.cache_system:  # cache the stable system prefix (Anthropic prompt caching)
                kwargs["system"] = [{"type": "text", "text": self.system,
                                     "cache_control": {"type": "ephemeral"}}]
            else:
                kwargs["system"] = self.system
        if self.tools:
            kwargs["tools"] = [t.spec() for t in self.tools]
        if self.thinking:
            kwargs["thinking"] = {"type": "adaptive"}

        last = None
        for attempt in range(self.max_retries + 1):
            try:
                if self.stream and hasattr(self.client.messages, "stream"):
                    with self.client.messages.stream(**kwargs) as s:
                        return s.get_final_message()
                return self.client.messages.create(**kwargs)
            except Exception as e:
                if not self._retryable(e) or attempt == self.max_retries:
                    raise
                last = e
                log.warning("retryable error (attempt %d): %s", attempt + 1, e)
                time.sleep(self.retry_base * (2 ** attempt))
        raise last  # pragma: no cover

    def run(self, task: str, on_event: Optional[Callable[[dict], None]] = None) -> Result:
        usage = Usage()
        events: list = []
        t0 = time.perf_counter()

        def emit(kind, **data):
            ev = {"kind": kind, "t_ms": int((time.perf_counter() - t0) * 1000), **data}
            events.append(ev)
            if on_event:
                on_event(ev)

        messages = [{"role": "user", "content": task}]
        for _ in range(self.max_steps):
            if self.budget_usd is not None and usage.cost_usd >= self.budget_usd:
                emit("budget_exceeded", cost_usd=round(usage.cost_usd, 4))
                return Result("[stopped: spend budget exceeded]", usage, "budget", events)

            if self.compact_after and len(messages) > self.compact_after:
                messages = (self.compactor or _default_compactor)(messages)
                emit("compacted", messages=len(messages))

            reply = self._call(messages)
            u = getattr(reply, "usage", None)
            if u:
                usage.add(self.model, u)
            usage.steps += 1
            emit("model_reply", stop_reason=reply.stop_reason, cost_usd=round(usage.cost_usd, 4))
            messages.append({"role": "assistant", "content": reply.content})

            if reply.stop_reason == "pause_turn":
                continue
            if reply.stop_reason != "tool_use":
                text = "".join(b.text for b in reply.content if b.type == "text")
                emit("final")
                return Result(text, usage, reply.stop_reason, events)

            results = []
            for b in reply.content:
                if b.type != "tool_use":
                    continue
                decision = self.policy.decision(b.name)
                allowed = decision == "allow" or (
                    decision == "ask" and self.approve is not None and self.approve(b.name, b.input))
                if not allowed:
                    emit("tool_blocked", tool=b.name, decision=decision)
                    results.append({"type": "tool_result", "tool_use_id": b.id,
                                    "content": f"Blocked by policy ({decision}).", "is_error": True})
                    continue

                emit("tool_use", tool=b.name, args=b.input)
                tool = self._tool(b.name)
                try:
                    out, err = (tool(b.input), False) if tool else (f"Unknown tool: {b.name}", True)
                except Exception as e:
                    out, err = f"{type(e).__name__}: {e}", True

                if self.guardrail and not err:
                    out, flagged = self.guardrail(str(out))
                    if flagged:
                        emit("guardrail_flag", tool=b.name)

                emit("tool_result", tool=b.name, is_error=err)
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": str(out), "is_error": err})
            messages.append({"role": "user", "content": results})

        emit("max_steps")
        return Result("[stopped: max_steps reached]", usage, "max_steps", events)
