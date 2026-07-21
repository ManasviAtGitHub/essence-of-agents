from snip.codec import make_code, is_valid_code, ALPHABET, CODE_LEN


def test_alphabet_has_no_lookalikes():
    for bad in "0O1lI":
        assert bad not in ALPHABET
    assert len(ALPHABET) == 57


def test_make_code_shape():
    code = make_code(lambda c: False)          # nothing exists -> first draw is returned
    assert len(code) == CODE_LEN
    assert all(ch in ALPHABET for ch in code)


def test_make_code_takes_no_id():
    # the whole point of lessons.md #1: make_code must not accept an id/seed.
    import inspect
    params = list(inspect.signature(make_code).parameters)
    assert params == ["exists"], "make_code must take only the store's exists() -- never an id"


def test_make_code_retries_on_collision():
    calls = {"n": 0}
    def exists(code):                          # first 3 candidates "exist", then free
        calls["n"] += 1
        return calls["n"] <= 3
    code = make_code(exists)
    assert calls["n"] == 4 and is_valid_code(code)


def test_is_valid_code():
    assert is_valid_code("abcdefg")            # right length, all in alphabet
    assert not is_valid_code("abcdef")         # too short
    assert not is_valid_code("abcdefgh")       # too long
    assert not is_valid_code("abcdef0")        # contains a look-alike (0)
