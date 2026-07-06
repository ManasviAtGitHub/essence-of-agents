"""A tiny reverse-mode autograd engine - the thing that makes training possible.

Every number in the model is a `Value`: it remembers how it was computed, so we
can run backward and get a gradient for every weight. This is the whole of
"how a model learns", written by hand in ~90 lines - no numpy, no framework.
(It is the models-track cousin of writing the agent loop by hand in Module 0.)

    from autograd import Value
    a = Value(2.0); b = Value(-3.0)
    c = a * b + a
    c.backward()
    print(a.grad, b.grad)   # d c / d a, d c / d b
"""
from __future__ import annotations

import math


class Value:
    """A scalar that tracks its own gradient."""

    def __init__(self, data, _children=(), _op=""):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None      # how to push grad to our inputs
        self._prev = set(_children)
        self._op = _op

    # --- the operations the model needs, each with its local derivative ---
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad          # d(a+b)/da = 1
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad   # d(a*b)/da = b
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, p):
        assert isinstance(p, (int, float))
        out = Value(self.data ** p, (self,), f"**{p}")

        def _backward():
            self.grad += (p * self.data ** (p - 1)) * out.grad
        out._backward = _backward
        return out

    def exp(self):
        out = Value(math.exp(self.data), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad     # d(e^x)/dx = e^x
        out._backward = _backward
        return out

    def log(self):
        out = Value(math.log(self.data), (self,), "log")

        def _backward():
            self.grad += (1.0 / self.data) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out

    # --- backprop: topological order, then chain rule from the output back ---
    def backward(self):
        topo, visited = [], set()

        def build(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    # --- conveniences so the model code reads like math ---
    def __neg__(self):        return self * -1
    def __sub__(self, o):     return self + (-o if isinstance(o, Value) else Value(-o))
    def __rsub__(self, o):    return Value(o) + (-self)
    def __radd__(self, o):    return self + o
    def __rmul__(self, o):    return self * o
    def __truediv__(self, o): return self * (o ** -1 if isinstance(o, Value) else Value(1.0 / o))
    def __repr__(self):       return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"


def softmax(logits):
    """logits (list of Value) -> probabilities (list of Value). Module 0's softmax."""
    m = max(v.data for v in logits)                 # subtract max for stability
    exps = [(v - m).exp() for v in logits]
    s = exps[0]
    for e in exps[1:]:
        s = s + e
    return [e / s for e in exps]


def cross_entropy(logits, target_ix):
    """-log p(correct token). The next-token training loss (Module 6)."""
    return -softmax(logits)[target_ix].log()
