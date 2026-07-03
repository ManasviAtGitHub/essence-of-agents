"""claude_harness - a small, reusable Claude agent harness.

    from claude_harness import Agent, tool, Trace
    from claude_harness.builtins import read_file

    agent = Agent(tools=[read_file])
    print(agent.run("Read README.md and summarize it in two sentences."))
"""
from .agent import Agent, DEFAULT_MODEL
from .tools import Tool, tool
from .trace import Trace
from . import builtins

__all__ = ["Agent", "DEFAULT_MODEL", "Tool", "tool", "Trace", "builtins"]
