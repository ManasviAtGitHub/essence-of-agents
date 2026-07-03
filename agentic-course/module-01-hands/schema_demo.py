"""How a Python function becomes something the model can request - fully offline.

A tool is just text we put in the context: a name, a description, and a JSON schema.
The @tool decorator builds all of that from your function's signature + docstring.
Run this with NO key to see the exact spec the model receives.

    python agentic-course/module-01-hands/schema_demo.py
"""
import json
import os
import sys

# Put the repo root on the path so `claude_harness` imports when run directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import tool
from claude_harness.builtins import calculate, read_file


@tool
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get the current weather for a city.

    Args:
        city: City name, e.g. "Paris".
        unit: Either "celsius" or "fahrenheit".
    """
    return f"Sunny in {city}."


# get_weather is a Tool (the decorator returned one); read_file/calculate already are.
for t in (get_weather, read_file, calculate):
    print(json.dumps(t.spec(), indent=2))
    print()

print("Notice: `city` is required (no default), `unit` is optional (has a default).")
print("This dict is literally what gets put into the model's context as a tool.")
