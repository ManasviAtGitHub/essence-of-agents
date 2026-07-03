"""Offline tests for the production modules (no key, no network). Run:

    python production/test_production.py
    pytest production
"""
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # repo root -> claude_harness
sys.path.insert(0, _HERE)                    # production

import eval_gate
from agent_pro import ProAgent
from claude_harness import tool
from claude_harness.testing import FakeClient, reply, text_block, tool_use_block
from observability import spans, summarize
from persistence import SessionStore
from router import Router


@tool
def calc(a: int, b: int) -> str:
    """Add two integers.

    Args:
        a: first
        b: second
    """
    return str(a + b)


def _run_with_tool():
    client = FakeClient([reply(tool_use_block("calc", {"a": 2, "b": 3}, id="t1")),
                         reply(text_block("5"))])
    return ProAgent(tools=[calc], client=client).run("add 2 and 3")


def test_observability_summary():
    r = _run_with_tool()
    s = summarize(r)
    assert s["tool_calls"] == 1 and s["steps"] >= 2 and s["stop_reason"] == "end_turn"
    assert len(spans(r)) == len(r.events)


def test_persistence_roundtrip():
    d = tempfile.mkdtemp()
    try:
        store = SessionStore(d)
        r = _run_with_tool()
        store.save("s1", r)
        loaded = store.load("s1")
        assert loaded["text"] == r.text
        assert loaded["usage"]["steps"] == r.usage.steps
        assert "s1" in store.list()
    finally:
        shutil.rmtree(d)


def test_router_falls_back_on_refusal():
    refuse = FakeClient([reply(text_block("no"), stop_reason="refusal")])
    ok = FakeClient([reply(text_block("yes"))])
    router = Router([{"name": "primary", "client": refuse, "model": "m1"},
                     {"name": "backup", "client": ok, "model": "m2"}])
    name, result = router.run("x")
    assert name == "backup" and result.text == "yes"


def test_eval_gate_no_regression():
    assert eval_gate.run_eval() >= eval_gate.BASELINE - 1e-9


if __name__ == "__main__":
    test_observability_summary()
    test_persistence_roundtrip()
    test_router_falls_back_on_refusal()
    test_eval_gate_no_regression()
    print("ok - 4 production-module tests passed")
