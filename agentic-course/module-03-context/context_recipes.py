"""Module 3 -- a REPRODUCIBLE measurement of context quality (keyless, no model).

We proxy "better prompt" with "better extractor": each recipe is a regex of increasing
quality, scored against a real dataset. The pass-rate climbs -- and you can re-run it
and get the same numbers, every time. (With a real model the recipe IS the prompt; same
shape, real numbers -- see CHALLENGE.md.)

    python agentic-course/module-03-context/context_recipes.py
"""
import re

# (email text, the order id we should extract -- or None if there isn't one)
DATASET = [
    ("my order 88231 is late", "88231"),
    ("Re: order #A1024", "A1024"),
    ("ref ZX-9 please", "ZX-9"),
    ("order: 77 thanks", "77"),
    ("where is my package", None),
    ("invoice 2024 for order 88231", "88231"),
]

RECIPES = [
    ("naive: first digits",      r"(\d+)"),
    ("alnum token",              r"#?([A-Z]{0,3}-?\d+)"),
    ("anchored on order/ref",    r"(?:order|ref)[\s:#]*([A-Z]{0,3}-?\d+)"),
]


def extract(pattern, text):
    m = re.search(pattern, text)
    return m.group(1) if m else None


print("Same dataset, same scorer. Only the 'context recipe' changes:\n")
for name, pattern in RECIPES:
    hits = sum(extract(pattern, text) == expected for text, expected in DATASET)
    pct = round(100 * hits / len(DATASET))
    bar = "#" * (pct // 10)
    print(f"  {name:24} {hits}/{len(DATASET)}  {pct:3}%  {bar}")

print("\nThe model never changed -- only the context did. That is the whole thesis,")
print("and unlike a hand-authored claim, you can re-run this and reproduce the numbers.")
