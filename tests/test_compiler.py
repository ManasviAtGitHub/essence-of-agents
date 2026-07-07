"""Tests for the capstone compiler (models/module-10-compiler/compiler.py).

Keyless and deterministic - the front-end model is a scripted/keyword driver (the
FakeClient analog), so this runs in CI with no download. It exercises the REAL
parts: the grammar's legal-option computation, the verifier's static checks, and
the constrained-vs-unconstrained contrast that is the module's whole point. Run:

    python tests/test_compiler.py
    pytest tests/test_compiler.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "models", "module-10-compiler"))

import compiler  # noqa: E402
from compiler import (  # noqa: E402
    compile, verify, render, legal_fields, legal_args,
    ScriptedDriver, KeywordDriver, AdversarialDriver, EXAMPLE, EXAMPLE_PLAN,
)


def test_grammar_legal_options():
    # be the grammar (CHALLENGE part 1): n1 came from get_weather, whose RETURN
    # schema is {rain, temp} - so only those two fields are legal after n1.
    ir = [{"id": "n1", "tool": "get_weather", "args": {"city": '"Paris"'}, "cond": None}]
    assert legal_fields(ir, "n1") == ["rain", "temp"]
    assert legal_args("add_to_cart") == ["item"]          # exactly one arg
    assert legal_args("get_weather") == ["city"]


def test_verify_cases():
    # be the verifier (CHALLENGE part 2)
    A = [{"id": "n1", "tool": "get_weather", "args": {"city": '"Paris"'}, "cond": None},
         {"id": "n2", "tool": "add_to_cart", "args": {"item": '"umbrella"'}, "cond": ["n1", "rain"]}]
    B = [{"id": "n1", "tool": "get_weather", "args": {"city": '"Paris"'}, "cond": None},
         {"id": "n2", "tool": "add_to_cart", "args": {"item": '"umbrella"'}, "cond": ["n3", "rain"]}]
    C = [{"id": "n1", "tool": "add_to_cart", "args": {"city": '"Paris"'}, "cond": None}]
    D = [{"id": "n1", "tool": "get_weather", "args": {"city": '"Paris"'}, "cond": None},
         {"id": "n2", "tool": "send_email", "args": {"to": '"me"'}, "cond": ["n1", "top"]}]
    assert verify(A) == []                                 # compiles
    assert any("used before it is defined" in e for e in verify(B))
    assert any("has no arg 'city'" in e for e in verify(C))
    assert any("has no field 'top'" in e for e in verify(D))


def test_scripted_compiles_example():
    ir = compile(EXAMPLE, ScriptedDriver(EXAMPLE_PLAN), constrained=True)
    assert verify(ir) == []
    assert render(ir) == ('n1 = get_weather(city="Paris")\n'
                          'n2 = if n1.rain: add_to_cart(item="umbrella")')


def test_keyword_compiles_example():
    # the toy NL parser turns the worked sentence into the right verified plan
    ir = compile(EXAMPLE, KeywordDriver(EXAMPLE), constrained=True)
    assert verify(ir) == []
    tools = [s["tool"] for s in ir]
    assert tools == ["get_weather", "add_to_cart"]
    assert ir[1]["cond"] == ["n1", "rain"]


def test_grammar_is_the_whole_trick():
    # constrained: the adversarial driver is never OFFERED an illegal token, so the
    # plan is valid by construction. unconstrained: it grabs the bogus tool and the
    # verifier catches it. that contrast is the module's thesis.
    good = compile(EXAMPLE, AdversarialDriver(), constrained=True)
    bad = compile(EXAMPLE, AdversarialDriver(), constrained=False)
    assert verify(good) == [], "constrained decode must never yield an invalid plan"
    assert verify(bad) != [], "unconstrained decode must be catchable by the verifier"
    assert any("unknown tool" in e for e in verify(bad))


if __name__ == "__main__":
    test_grammar_legal_options(); print("ok - grammar legal options")
    test_verify_cases(); print("ok - verifier catches the bad plans")
    test_scripted_compiles_example(); print("ok - scripted driver compiles the example")
    test_keyword_compiles_example(); print("ok - keyword driver compiles the example")
    test_grammar_is_the_whole_trick(); print("ok - grammar prevents what the verifier would catch")
    print("ALL COMPILER CHECKS PASSED")
