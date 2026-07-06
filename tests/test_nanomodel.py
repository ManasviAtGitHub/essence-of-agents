"""Smoke test for models/nanomodel - the from-scratch transformer.

Verifies the tokenizer round-trips, the forward+backward wiring works, and a
short training run actually reduces the loss. Fast (a few seconds). Run:

    python tests/test_nanomodel.py
    pytest tests/test_nanomodel.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "models", "nanomodel"))

import bpe          # noqa: E402
from autograd import Value, cross_entropy   # noqa: E402
from model import NanoModel                 # noqa: E402


def test_autograd_gradient():
    # c = a*b + a  ->  dc/da = b + 1,  dc/db = a
    a, b = Value(2.0), Value(-3.0)
    c = a * b + a
    c.backward()
    assert abs(a.grad - (-3.0 + 1.0)) < 1e-9
    assert abs(b.grad - 2.0) < 1e-9


def test_bpe_matches_widget():
    merges = bpe.train(num_merges=5)
    assert merges[0] == ("s", "t")               # most frequent pair first
    assert bpe.encode("lowest", merges) == ["low", "est"]
    assert bpe.decode(bpe.encode("newest", merges)) == "newest"


def test_forward_and_backward():
    m = NanoModel(vocab=8, block_size=4, d=8, hidden=16, seed=1)
    logits = m.forward([1, 2, 3, 0])
    assert len(logits) == 4 and len(logits[0]) == 8      # a logit per position, per vocab token
    loss = cross_entropy(logits[-1], 2)
    for p in m.params():
        p.grad = 0.0
    loss.backward()
    assert any(p.grad != 0.0 for p in m.params())        # gradients actually flowed


def test_training_reduces_loss():
    # run a short training loop and check the loss trends DOWN (early avg vs late avg,
    # which is robust to the single-window SGD noise the real train.py smooths with an EMA)
    import random
    from train import DATA, CHARS
    block = 6
    m = NanoModel(vocab=len(CHARS), block_size=block, d=8, hidden=16, seed=1337)
    params = m.params()
    rnd = random.Random(1337)
    losses = []
    for _ in range(90):
        i = rnd.randint(0, len(DATA) - block - 1)
        xs, ys = DATA[i:i + block], DATA[i + 1:i + block + 1]
        lo = m.forward(xs)
        loss = cross_entropy(lo[0], ys[0])
        for t in range(1, block):
            loss = loss + cross_entropy(lo[t], ys[t])
        loss = loss * (1.0 / block)
        for p in params:
            p.grad = 0.0
        loss.backward()
        for p in params:
            p.data -= 0.4 * p.grad
        losses.append(loss.data)
    early = sum(losses[:20]) / 20
    late = sum(losses[-20:]) / 20
    assert late < early * 0.85, f"loss did not drop enough: {early:.3f} -> {late:.3f}"


if __name__ == "__main__":
    test_autograd_gradient(); print("ok - autograd gradient")
    test_bpe_matches_widget(); print("ok - bpe matches widget")
    test_forward_and_backward(); print("ok - forward + backward")
    test_training_reduces_loss(); print("ok - training reduces loss")
    print("ALL NANOMODEL CHECKS PASSED")
