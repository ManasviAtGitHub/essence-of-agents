"""A multi-handed agent: several tools, one unchanged loop.

We never change the model or the loop - we just hand it more tools. Run this with
ANTHROPIC_API_KEY set; for the keyless version see offline_demo.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import Agent, tool
from claude_harness.builtins import calculate, list_dir, read_file


@tool
def reverse(text: str) -> str:
    """Reverse a string.

    Args:
        text: The text to reverse.
    """
    return text[::-1]


TOOLS = [read_file, list_dir, calculate, reverse]


def build_agent(client=None):
    """Build the multi-tool agent. Pass a client (e.g. a FakeClient) to run offline;
    omit it to use the real Anthropic client (needs a key)."""
    kwargs = {"tools": TOOLS}
    if client is not None:
        kwargs["client"] = client
    return Agent(**kwargs)


if __name__ == "__main__":
    agent = build_agent()  # real client - needs ANTHROPIC_API_KEY
    print(
        agent.run(
            "List the files in this folder, reverse the text 'README.md', "
            "and tell me what 13 * 17 is."
        )
    )
