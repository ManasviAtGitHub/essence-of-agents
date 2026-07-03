"""A small library of ready-made tools.

These are intentionally tiny and safe. Real harnesses promote actions to dedicated
tools when they need to gate, sandbox, or audit them - see the course's Module 9.
"""
from __future__ import annotations

import ast
import operator as op
import os

from .tools import tool


@tool
def read_file(path: str) -> str:
    """Read a UTF-8 text file and return its contents.

    Args:
        path: Path to the file.
    """
    with open(path, encoding="utf-8") as f:
        return f.read()


@tool
def list_dir(path: str = ".") -> str:
    """List the entries in a directory, one per line.

    Args:
        path: Directory path (defaults to the current directory).
    """
    return "\n".join(sorted(os.listdir(path)))


_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


@tool
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression exactly. Supports + - * / ** %.

    Args:
        expression: e.g. "2**100 + 17*365*24*3600".
    """
    return str(_eval(ast.parse(expression, mode="eval").body))
