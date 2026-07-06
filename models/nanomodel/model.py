"""A tiny transformer, from scratch, on the autograd engine - the models track in code.

Every piece here is a module of the course, made runnable:
  - embed()      tokens -> vectors h            (Module 1)
  - Attention    positions exchange info        (Module 2, with the causal mask)
  - MLP          each position thinks alone      (Module 4's FFN, un-sliced)
  - forward()    h -> logits over the vocab      (Module 0)
  - generate()   sample + append + repeat        (Module 0's loop)

It is deliberately tiny (a handful of dims, one head, one block) so it runs in
pure Python in seconds. Real models are this exact math, scaled up.
"""
from __future__ import annotations

import math
import random

from autograd import Value, softmax


def _rng(seed):
    r = random.Random(seed)
    return lambda: r.uniform(-1, 1)


class Linear:
    """y = W x + b. The building block of every projection in a transformer."""

    def __init__(self, n_in, n_out, rnd):
        s = 1.0 / math.sqrt(n_in)                          # small init
        self.W = [[Value(rnd() * s) for _ in range(n_in)] for _ in range(n_out)]
        self.b = [Value(0.0) for _ in range(n_out)]

    def __call__(self, x):                                  # x: list[Value] length n_in
        out = []
        for wrow, bias in zip(self.W, self.b):
            acc = bias
            for wij, xj in zip(wrow, x):
                acc = acc + wij * xj
            out.append(acc)
        return out

    def params(self):
        return [w for row in self.W for w in row] + self.b


class Attention:
    """One causal self-attention head: softmax(q.k / sqrt(d)) . v over the PAST."""

    def __init__(self, d, rnd):
        self.d = d
        self.q, self.k, self.v = Linear(d, d, rnd), Linear(d, d, rnd), Linear(d, d, rnd)
        self.proj = Linear(d, d, rnd)

    def __call__(self, hs):                                 # hs: list of per-position vectors
        T = len(hs)
        Q = [self.q(h) for h in hs]
        K = [self.k(h) for h in hs]
        V = [self.v(h) for h in hs]
        scale = 1.0 / math.sqrt(self.d)
        out = []
        for t in range(T):
            scores = []
            for s in range(t + 1):                          # causal: only 0..t (Module 2's mask)
                dot = Value(0.0)
                for a, b in zip(Q[t], K[s]):
                    dot = dot + a * b
                scores.append(dot * scale)
            w = softmax(scores)                             # attention weights (computed)
            blended = [Value(0.0) for _ in range(self.d)]
            for s in range(t + 1):
                for j in range(self.d):
                    blended[j] = blended[j] + w[s] * V[s][j]
            out.append(self.proj(blended))
        return out

    def params(self):
        return self.q.params() + self.k.params() + self.v.params() + self.proj.params()


class MLP:
    """Each position thinks alone: Linear -> tanh -> Linear. (Module 4's FFN.)"""

    def __init__(self, d, hidden, rnd):
        self.fc = Linear(d, hidden, rnd)
        self.proj = Linear(hidden, d, rnd)

    def __call__(self, h):
        return self.proj([x.tanh() for x in self.fc(h)])

    def params(self):
        return self.fc.params() + self.proj.params()


class NanoModel:
    """tokens -> embed -> (attention + MLP) -> logits. A whole transformer, tiny."""

    def __init__(self, vocab, block_size, d=16, hidden=32, seed=1337):
        rnd = _rng(seed)
        self.vocab, self.block_size, self.d = vocab, block_size, d
        self.tok_emb = [[Value(rnd() * 0.1) for _ in range(d)] for _ in range(vocab)]
        self.pos_emb = [[Value(rnd() * 0.1) for _ in range(d)] for _ in range(block_size)]
        self.attn = Attention(d, rnd)
        self.mlp = MLP(d, hidden, rnd)
        self.head = Linear(d, vocab, rnd)                   # unembed -> logits (Module 0)

    def forward(self, idx):                                 # idx: list[int], length <= block_size
        hs = [[te + pe for te, pe in zip(self.tok_emb[t], self.pos_emb[p])]
              for p, t in enumerate(idx)]                   # embed = token + position (Module 1)
        a = self.attn(hs)                                   # beat 1: attention (residual add)
        hs = [[x + y for x, y in zip(h, ai)] for h, ai in zip(hs, a)]
        m = [self.mlp(h) for h in hs]                       # beat 2: MLP (residual add)
        hs = [[x + y for x, y in zip(h, mi)] for h, mi in zip(hs, m)]
        return [self.head(h) for h in hs]                   # logits per position

    def params(self):
        return ([w for row in self.tok_emb for w in row] +
                [w for row in self.pos_emb for w in row] +
                self.attn.params() + self.mlp.params() + self.head.params())

    def generate(self, idx, n, temperature=1.0, seed=0):
        """Module 0's loop: forward -> distribution -> sample -> append -> repeat."""
        r = random.Random(seed)
        for _ in range(n):
            window = idx[-self.block_size:]
            logits = self.forward(window)[-1]              # only the last position matters
            probs = softmax([l * (1.0 / temperature) for l in logits])
            draw, cum, pick = r.random(), 0.0, len(probs) - 1
            for i, p in enumerate(probs):                   # the dice roll (Module 0)
                cum += p.data
                if draw < cum:
                    pick = i
                    break
            idx = idx + [pick]
        return idx
