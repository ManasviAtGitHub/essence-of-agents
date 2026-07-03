"""Offline tests for the agent loop - no key, no network. Run either:

    python tests/test_offline_loop.py
    pytest
"""
import os
import sys

# Allow running directly from any directory: put the repo root on the path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_harness import Agent
from claude_harness.builtins import calculate
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block


def test_tool_then_final():
    client = FakeClient(
        [
            reply(tool_use_block("calculate", {"expression": "6*7"}, id="x")),
            reply(text_block("The answer is 42.")),
        ]
    )
    assert Agent(tools=[calculate], client=client).run("What is 6*7?") == "The answer is 42."


def test_unknown_tool_is_recoverable():
    # An unknown tool name returns an "Unknown tool" result instead of crashing,
    # so the loop can continue.
    client = FakeClient(
        [
            reply(tool_use_block("nope", {}, id="x")),
            reply(text_block("recovered")),
        ]
    )
    assert Agent(tools=[], client=client).run("do something") == "recovered"


def test_no_tools_just_answers():
    client = FakeClient([reply(text_block("hi"))])
    assert Agent(client=client).run("hi") == "hi"


if __name__ == "__main__":
    test_tool_then_final()
    test_unknown_tool_is_recoverable()
    test_no_tools_just_answers()
    print("ok - 3 passed")
