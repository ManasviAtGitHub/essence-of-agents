"""Offline test doubles - run the agent loop with no API key and no network.

The loop doesn't care where replies come from. FakeClient returns scripted replies
so you can exercise the loop, tool dispatch, error handling, and tracing entirely
offline. (It's also the seed of Module 10: a fixture is the simplest possible eval.)

    from claude_harness import Agent
    from claude_harness.builtins import calculate
    from claude_harness.testing import FakeClient, reply, text_block, tool_use_block

    client = FakeClient([
        reply(tool_use_block("calculate", {"expression": "2**100"})),
        reply(text_block("Done.")),
    ])
    Agent(tools=[calculate], client=client).run("compute 2**100")
"""
from __future__ import annotations

from dataclasses import dataclass


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
class _Reply:
    content: list
    stop_reason: str


def text_block(s: str) -> _Text:
    return _Text(s)


def tool_use_block(name: str, input: dict, id: str = "t1") -> _ToolUse:
    return _ToolUse(name=name, input=input, id=id)


def reply(*blocks, stop_reason: str | None = None) -> _Reply:
    """Build one scripted reply. stop_reason defaults to 'tool_use' if any block is
    a tool_use, otherwise 'end_turn'."""
    blocks = list(blocks)
    if stop_reason is None:
        stop_reason = (
            "tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn"
        )
    return _Reply(content=blocks, stop_reason=stop_reason)


class _Messages:
    def __init__(self, replies):
        self._replies = list(replies)
        self._i = 0

    def create(self, **_kwargs):
        if self._i >= len(self._replies):
            raise AssertionError("FakeClient ran out of scripted replies")
        r = self._replies[self._i]
        self._i += 1
        return r


class FakeClient:
    """A drop-in stand-in for anthropic.Anthropic that returns scripted replies in
    order. Pass it as Agent(client=FakeClient([...]))."""

    def __init__(self, replies):
        self.messages = _Messages(replies)
