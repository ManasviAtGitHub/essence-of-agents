"""Reference production agent -- a deployable CLI that wires it all together.

    python production/run_agent.py --provider fake            # offline, no key
    python production/run_agent.py --provider nvidia --task "..."   # live (reads .env)
    python production/run_agent.py --provider anthropic --task "..."  # needs ANTHROPIC_API_KEY

Composes agent_pro (guarded tools, budget, retries) + a provider + observability +
optional session persistence.
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # repo root -> claude_harness
sys.path.insert(0, _HERE)                    # production -> agent_pro / observability / providers

from agent_pro import ProAgent
from claude_harness.builtins import calculate, list_dir, read_file
from observability import summarize
from persistence import SessionStore

_DEFAULT_MODEL = {"nvidia": "meta/llama-3.1-8b-instruct", "anthropic": "claude-opus-4-8", "fake": "fake"}


def build_client(provider, model):
    if provider == "nvidia":
        from providers.nvidia import NvidiaClient
        return NvidiaClient(model=model)
    if provider == "anthropic":
        import anthropic
        return anthropic.Anthropic()
    if provider == "fake":  # offline demo: scripted to call the calculator, then answer
        from claude_harness.testing import FakeClient, reply, text_block, tool_use_block
        return FakeClient([
            reply(tool_use_block("calculate", {"expression": "2**10 + 5"}, id="t1")),
            reply(text_block("It is 1029.")),
        ])
    raise SystemExit(f"unknown provider: {provider}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Reference production agent (offline with --provider fake).")
    p.add_argument("--provider", default="fake", choices=["fake", "nvidia", "anthropic"])
    p.add_argument("--model", default=None)
    p.add_argument("--task", default="What is 2**10 + 5? Use the calculator tool, then state the number.")
    p.add_argument("--budget-usd", type=float, default=None)
    p.add_argument("--persist", default=None, help="directory to save the session record")
    p.add_argument("--session", default="session-1")
    a = p.parse_args(argv)

    model = a.model or _DEFAULT_MODEL[a.provider]
    client = build_client(a.provider, model)
    agent = ProAgent(tools=[calculate, read_file, list_dir], model=model, client=client,
                     budget_usd=a.budget_usd)
    result = agent.run(a.task)

    print("ANSWER:", result.text)
    print("metrics:", summarize(result))
    if a.persist:
        path = SessionStore(a.persist).save(a.session, result)
        print("saved ->", path)
    return result


if __name__ == "__main__":
    main()
