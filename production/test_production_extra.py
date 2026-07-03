"""Offline tests for the final production pieces: vector store, sandbox, HTTP handler,
prompt-caching wiring, and compaction. No key, no network (besides local subprocess). Run:

    python production/test_production_extra.py
    pytest production
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # repo root -> claude_harness
sys.path.insert(0, _HERE)                    # production

import server
from agent_pro import ProAgent
from claude_harness import tool
from claude_harness.builtins import calculate
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block
from sandbox import run_python
from vectorstore import VectorStore


@tool
def add(a: int, b: int) -> str:
    """Add two integers.

    Args:
        a: first
        b: second
    """
    return str(a + b)


class _U:
    input_tokens = 0
    output_tokens = 0
    cache_read_input_tokens = 0


class _R:
    def __init__(self, blocks, stop):
        self.content, self.stop_reason, self.usage = blocks, stop, _U()


class LoopClient:
    def __init__(self):
        self.messages = self

    def create(self, **_kw):
        return _R([tool_use_block("add", {"a": 1, "b": 1}, id="t")], "tool_use")


class SpyClient:
    def __init__(self, replies):
        self.captured, self._r, self.messages = [], list(replies), self

    def create(self, **kw):
        self.captured.append(kw)
        return self._r.pop(0)


def test_vectorstore_ranks_relevant_doc_first():
    vs = VectorStore()
    vs.add("Project Heron's launch date is March 3, 2027.")
    vs.add("Dana Okafor leads Project Heron.")
    vs.add("Tuesday's lunch special is mushroom risotto.")
    hits = vs.search("when does heron launch", k=1)
    assert "launch" in hits[0]["text"].lower()


def test_sandbox_runs_and_reports_errors():
    ok = run_python("print(2 + 2)")
    assert ok["returncode"] == 0 and ok["stdout"].strip() == "4"
    bad = run_python("1 / 0")
    assert bad["returncode"] != 0 and "ZeroDivisionError" in bad["stderr"]


def test_server_handle():
    def factory():
        client = FakeClient([reply(tool_use_block("calculate", {"expression": "6*7"}, id="t")),
                             reply(text_block("42"))])
        return ProAgent(tools=[calculate], client=client)
    out = server.handle("what is 6*7?", factory)
    assert out["answer"] == "42" and out["metrics"]["tool_calls"] == 1


def test_prompt_caching_wiring():
    spy = SpyClient([reply(text_block("ok"))])
    ProAgent(client=spy, system="SYS", cache_system=True).run("x")
    system_arg = spy.captured[0]["system"]
    assert isinstance(system_arg, list) and system_arg[0]["cache_control"] == {"type": "ephemeral"}


def test_compaction_triggers():
    r = ProAgent(tools=[add], client=LoopClient(), compact_after=3, max_steps=6).run("loop")
    assert any(e["kind"] == "compacted" for e in r.events)


def test_chat_ui_served():
    path = os.path.join(_HERE, "web", "index.html")
    html = open(path, encoding="utf-8").read()
    assert "/chat" in html and "<form" in html and ("EventSource" in html or "fetch(" in html)


if __name__ == "__main__":
    test_vectorstore_ranks_relevant_doc_first(); print("ok - vector store")
    test_sandbox_runs_and_reports_errors(); print("ok - code sandbox")
    test_server_handle(); print("ok - HTTP handler")
    test_chat_ui_served(); print("ok - chat UI served")
    test_prompt_caching_wiring(); print("ok - prompt caching wiring")
    test_compaction_triggers(); print("ok - compaction")
    print("ok - 6 extra production tests passed")
