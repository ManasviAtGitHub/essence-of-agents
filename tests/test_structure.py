"""Structural invariants that keep the codebase from drifting as we add animated
scenes everywhere. Run:

    python tests/test_structure.py
    pytest tests

Enforces: one shared library, no re-inlined character kit, simulation-first UI.
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")


def _html(*roots):
    out = []
    for r in roots:
        out += glob.glob(os.path.join(r, "**", "*.html"), recursive=True)
    return [f for f in out if "node_modules" not in f]


def test_shared_assets_exist():
    for f in ("theme.css", "cast.js", "anim.js"):
        assert os.path.exists(os.path.join(ASSETS, f)), f"missing shared asset: assets/{f}"


def test_widgets_use_shared_library():
    widgets = (glob.glob(os.path.join(ROOT, "agentic-course", "**", "widgets", "**", "index.html"), recursive=True) +
               glob.glob(os.path.join(ROOT, "models", "**", "widgets", "**", "index.html"), recursive=True))
    assert widgets, "no widgets found"
    for w in widgets:
        s = open(w, encoding="utf-8").read()
        rel = os.path.relpath(w, ROOT)
        assert "assets/theme.css" in s, f"{rel} does not link the shared theme.css"
        assert "assets/cast.js" in s, f"{rel} does not link the shared cast.js"


def test_character_kit_is_single_source():
    """Cortex/Bit are defined once (cast.js); nobody re-inlines them."""
    cast = open(os.path.join(ASSETS, "cast.js"), encoding="utf-8").read()
    assert "function cortex(" in cast and "function bit(" in cast, "cast.js should define cortex() and bit()"
    for f in _html(os.path.join(ROOT, "agentic-course"), os.path.join(ROOT, "production"),
                   os.path.join(ROOT, "models")) + [os.path.join(ROOT, "index.html")]:
        s = open(f, encoding="utf-8").read()
        assert "function cortex(" not in s, f"re-inlined character kit in {os.path.relpath(f, ROOT)} -- use cast.js"


def test_stage_is_simulation_by_default():
    """The served stage must default to simulation; live is opt-in via ?live."""
    web = open(os.path.join(ROOT, "production", "web", "index.html"), encoding="utf-8").read()
    assert 'has("live")' in web, "stage should gate live behind ?live"
    assert 'location.protocol.startsWith("http")' not in web, "stage must not default to live when served"


if __name__ == "__main__":
    test_shared_assets_exist(); print("ok - shared assets exist")
    test_widgets_use_shared_library(); print("ok - widgets use shared library")
    test_character_kit_is_single_source(); print("ok - character kit is single-source")
    test_stage_is_simulation_by_default(); print("ok - stage is simulation-first")
    print("ALL STRUCTURE CHECKS PASSED")
