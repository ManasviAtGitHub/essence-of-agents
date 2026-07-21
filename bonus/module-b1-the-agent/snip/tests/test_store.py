import pytest

from snip.store import Store


def test_put_get_roundtrip(tmp_path):
    s = Store(str(tmp_path / "db.json"))
    s.put("abcdefg", "https://example.com/x")
    assert s.get("abcdefg") == "https://example.com/x"
    assert s.get("missing") is None


def test_codes_are_permanent(tmp_path):
    s = Store(str(tmp_path / "db.json"))
    s.put("abcdefg", "https://a.com")
    s.put("abcdefg", "https://a.com")          # same url again is fine (idempotent)
    with pytest.raises(ValueError):
        s.put("abcdefg", "https://b.com")      # reassign to a new url -> rejected (rule #2)


def test_hits_start_zero_and_bump(tmp_path):
    s = Store(str(tmp_path / "db.json"))
    s.put("abcdefg", "https://a.com")
    assert s.hits("abcdefg") == 0
    s.bump("abcdefg")
    s.bump("abcdefg")
    assert s.hits("abcdefg") == 2


def test_write_is_atomic(tmp_path):
    # no .tmp file should survive a completed put (write-temp-then-replace)
    s = Store(str(tmp_path / "db.json"))
    s.put("abcdefg", "https://a.com")
    leftovers = [p for p in tmp_path.iterdir() if p.suffix == ".tmp"]
    assert leftovers == []
