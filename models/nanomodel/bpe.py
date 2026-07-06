"""Byte-pair encoding - the real tokenizer, from scratch (Module 1, in code).

This is exactly the algorithm the Module 1 widget animates, now runnable:
train a vocabulary by repeatedly merging the most frequent adjacent pair, then
encode any text by replaying those merges in order.

    python bpe.py        # trains on a toy corpus, prints the merges, encodes a word

train.py uses a char-level tokenizer for speed; this is the subword tokenizer
real models use. Same idea at 100,000+ merges over web-scale text.
"""
from __future__ import annotations

from collections import Counter

# the classic BPE teaching corpus (word -> count), same as the widget
CORPUS = {"low": 5, "lower": 2, "newest": 6, "widest": 3}


def _pairs(words):
    """count every adjacent symbol pair across the (weighted) corpus."""
    c = Counter()
    for syms, n in words:
        for a, b in zip(syms, syms[1:]):
            c[(a, b)] += n
    return c


def train(corpus=CORPUS, num_merges=10):
    """learn a merge list by greedily fusing the most frequent pair."""
    words = [([*w], n) for w, n in corpus.items()]      # start from characters
    merges = []
    for _ in range(num_merges):
        pairs = _pairs(words)
        if not pairs:
            break
        (a, b), _ = max(pairs.items(), key=lambda kv: (kv[1], kv[0]))
        merges.append((a, b))
        words = [([_merge(syms, a, b)][0], n) for syms, n in words]  # apply everywhere
    return merges


def _merge(syms, a, b):
    out, i = [], 0
    while i < len(syms):
        if i < len(syms) - 1 and syms[i] == a and syms[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(syms[i])
            i += 1
    return out


def encode(word, merges):
    """split a word to chars, then replay the learned merges in training order."""
    syms = [*word]
    for a, b in merges:
        syms = _merge(syms, a, b)
    return syms


def decode(tokens):
    return "".join(tokens)


if __name__ == "__main__":
    merges = train(num_merges=5)
    print("learned merges (in order):")
    for i, (a, b) in enumerate(merges, 1):
        print(f"  {i}. {a!r} + {b!r} -> {a + b!r}")
    for w in ("lowest", "newest", "widest"):
        print(f"encode({w!r}) = {encode(w, merges)}")
    print("\n(same algorithm as the Module 1 widget - real vocabs run it ~100k+ times.)")
