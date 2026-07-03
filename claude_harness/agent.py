"""The agent loop - the same shape as module-00's teaching agent, made reusable.

Agency is not in the model. It is the loop you wrap around it. This module is that
loop: call the model, run any tool it requests, feed the result back, repeat until
the model has a final answer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .tools import Tool
from .trace import Trace

DEFAULT_MODEL = "claude-opus-4-8"


def _default_client():
    """Create the real Anthropic client lazily, so the offline / fake path needs
    neither the SDK nor an API key. See claude_harness.testing.FakeClient."""
    import anthropic

    return anthropic.Anthropic()


@dataclass
class Agent:
    """A minimal, reusable agent over the Claude Messages API.

    Attributes:
        tools:      Tools the model may call (see claude_harness.tools.tool).
        model:      Claude model id. Defaults to claude-opus-4-8.
        system:     Optional system prompt.
        max_tokens: Per-response output cap.
        max_iters:  Safety bound on loop iterations.
        thinking:   If True, enable adaptive thinking.
        client:     An anthropic.Anthropic client (created from env by default).
    """

    tools: list[Tool] = field(default_factory=list)
    model: str = DEFAULT_MODEL
    system: str | None = None
    max_tokens: int = 4096
    max_iters: int = 25
    thinking: bool = False
    client: Any = field(default_factory=_default_client)

    # --- internals ---------------------------------------------------------
    def _tool_specs(self) -> list[dict]:
        return [t.spec() for t in self.tools]

    def _dispatch(self, name: str, args: dict):
        for t in self.tools:
            if t.name == name:
                return t(args)
        raise KeyError(f"Unknown tool: {name}")

    # --- the loop ----------------------------------------------------------
    def run(self, task: str, *, trace: Trace | None = None) -> str:
        """Run the agent on a task and return its final text answer.

        Pass a Trace to record every model reply, tool call, and result as a
        replayable JSON log of the run.
        """
        messages: list[dict] = [{"role": "user", "content": task}]

        for _ in range(self.max_iters):
            kwargs: dict = dict(
                model=self.model, max_tokens=self.max_tokens, messages=messages
            )
            if self.system:
                kwargs["system"] = self.system
            if self.tools:
                kwargs["tools"] = self._tool_specs()
            if self.thinking:
                kwargs["thinking"] = {"type": "adaptive"}

            reply = self.client.messages.create(**kwargs)
            if trace:
                trace.model(reply)

            # Always append the FULL assistant content (text + any thinking/tool
            # blocks). The model has no memory of its own - this list is it.
            messages.append({"role": "assistant", "content": reply.content})

            # Server-side tools can pause; re-send and let the server resume.
            if reply.stop_reason == "pause_turn":
                continue

            # No tool requested -> we have a final answer.
            if reply.stop_reason != "tool_use":
                text = "".join(b.text for b in reply.content if b.type == "text")
                if trace:
                    trace.final(text)
                return text

            # The model asked for tools. WE run them; the model never acts.
            results = []
            for b in reply.content:
                if b.type == "tool_use":
                    if trace:
                        trace.tool_use(b.name, b.input, b.id)
                    try:
                        out, err = self._dispatch(b.name, b.input), False
                    except Exception as e:  # surface the error back to the model
                        out, err = f"{type(e).__name__}: {e}", True
                    if trace:
                        trace.tool_result(b.id, out, err)
                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": b.id,
                            "content": str(out),
                            "is_error": err,
                        }
                    )
            messages.append({"role": "user", "content": results})

        raise RuntimeError(f"agent exceeded max_iters={self.max_iters}")
