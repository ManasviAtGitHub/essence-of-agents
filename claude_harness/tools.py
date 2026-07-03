"""Tools - turn a plain Python function into something the model can request.

A tool is just: a name, a description, an input schema, and your function. The
@tool decorator builds the schema from the function's type hints and docstring so
you don't hand-write JSON Schema.

    @tool
    def read_file(path: str) -> str:
        '''Read a UTF-8 text file and return its contents.

        Args:
            path: Path to the file.
        '''
        ...
"""
from __future__ import annotations

import inspect
import typing
from dataclasses import dataclass
from typing import Any, Callable

_PYTYPE_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    required: list[str]
    fn: Callable[..., Any]

    def spec(self) -> dict:
        """The tool definition the Messages API expects."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": self.parameters,
                "required": self.required,
            },
        }

    def __call__(self, args: dict) -> Any:
        return self.fn(**args)


def _parse_doc(doc: str) -> tuple[str, dict]:
    """Split a Google-style docstring into (summary, {arg: description})."""
    summary, args, in_args = [], {}, False
    for line in doc.splitlines():
        s = line.strip()
        if s.lower().startswith("args:"):
            in_args = True
            continue
        if in_args and ":" in s:
            key, _, val = s.partition(":")
            args[key.strip()] = val.strip()
        elif not in_args and s:
            summary.append(s)
    return " ".join(summary).strip(), args


def tool(fn: Callable[..., Any]) -> Tool:
    """Decorator: build a Tool from a function's signature + docstring."""
    sig = inspect.signature(fn)
    hints = typing.get_type_hints(fn)
    summary, arg_docs = _parse_doc(inspect.getdoc(fn) or "")

    props: dict = {}
    required: list[str] = []
    for name, p in sig.parameters.items():
        props[name] = {"type": _PYTYPE_TO_JSON.get(hints.get(name, str), "string")}
        if name in arg_docs:
            props[name]["description"] = arg_docs[name]
        if p.default is inspect.Parameter.empty:
            required.append(name)

    return Tool(
        name=fn.__name__,
        description=summary,
        parameters=props,
        required=required,
        fn=fn,
    )
