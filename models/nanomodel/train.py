"""Train the nano transformer and watch the loss drop - the whole track, running.

Next-token training (Module 6): show the model a context, ask it to predict the
next token, compare with the real next token via cross-entropy, backprop, nudge
every weight. Repeat. Then generate (Module 0's loop) and watch it reproduce the
patterns it learned.

    python train.py            # trains ~600 steps (~under a minute), then samples

It is a TOY: char-level tokens, a two-line corpus, one attention head, ~2k
weights. Real models are the identical math at a trillion-x scale.
"""
from __future__ import annotations

import sys

from autograd import cross_entropy
from model import NanoModel

# the track's running example, twice, so there is a pattern to learn
CORPUS = "the capital of france is paris.\nthe capital of spain is madrid.\n"

# char-level tokenizer: the simplest possible (bpe.py has the real subword one)
CHARS = sorted(set(CORPUS))
stoi = {c: i for i, c in enumerate(CHARS)}
itos = {i: c for i, c in enumerate(CHARS)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda ix: "".join(itos[i] for i in ix)
DATA = encode(CORPUS)


def train(steps=500, block_size=6, lr=0.4, log_every=50, seed=1337, verbose=True):
    model = NanoModel(vocab=len(CHARS), block_size=block_size, d=8, hidden=16, seed=seed)
    params = model.params()
    if verbose:
        print(f"nano transformer: vocab={len(CHARS)}, block={block_size}, "
              f"params={len(params)}  (corpus {len(DATA)} tokens)")
    import random
    r = random.Random(seed)
    ema = first = None                                      # smoothed loss (single-window SGD is noisy)
    for step in range(steps):
        i = r.randint(0, len(DATA) - block_size - 1)        # a random window
        xs = DATA[i:i + block_size]
        ys = DATA[i + 1:i + block_size + 1]                 # targets = next token at each position
        logits = model.forward(xs)
        loss = cross_entropy(logits[0], ys[0])
        for t in range(1, block_size):
            loss = loss + cross_entropy(logits[t], ys[t])
        loss = loss * (1.0 / block_size)

        for p in params:                                    # zero grads
            p.grad = 0.0
        loss.backward()                                     # the autograd engine earns its keep
        for p in params:                                    # SGD: step downhill
            p.data -= lr * p.grad

        ema = loss.data if ema is None else 0.95 * ema + 0.05 * loss.data
        if first is None:
            first = ema
        if verbose and (step % log_every == 0 or step == steps - 1):
            print(f"  step {step:4d}   loss (avg) {ema:.3f}")
    if verbose:
        print(f"loss: {first:.3f} -> {ema:.3f}  (it learned)\n")
    return model


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    model = train(steps=steps)
    seed_text = "the capital of "
    out = model.generate(encode(seed_text), n=16, temperature=0.5, seed=0)
    print("prompt:   ", repr(seed_text))
    print("generated:", repr(decode(out)))
    print("\n(temperature 0.5. Trained longer, it reproduces the corpus verbatim - "
          "the exact autoregressive loop Module 0 draws.)")


if __name__ == "__main__":
    main()
