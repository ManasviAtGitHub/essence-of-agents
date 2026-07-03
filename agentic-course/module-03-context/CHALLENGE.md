# Coding Challenge - turn the lever and measure it

The widget shows the *shape* of the effect. Now get the real numbers.

## With a real model (key or Ollama)
1. Pick one task with a checkable answer (e.g. "extract `order_id` as JSON").
2. Write 4 context recipes: naive -> + clear instruction -> + few-shot examples ->
   + reordered / format-last.
3. Run each recipe over ~20 inputs with the harness (same model), score pass/fail,
   and compare the four pass-rates.

```python
from claude_harness import Agent

agent = Agent()                      # model FIXED - only the context changes

def build_context(recipe, email):    # returns the full prompt for this recipe
    ...

def passes(output, expected):        # e.g. json.loads(output)["order_id"] == expected
    ...

for recipe in RECIPES:
    hits = sum(passes(agent.run(build_context(recipe, e)), ans)
               for e, ans in dataset)
    print(recipe, hits / len(dataset))
```

Same model every time. The only variable is the context - that *is* the thesis, proven
with numbers. You've also just built the eval Module 10 formalizes.

## Offline (no key)
Stub `Agent` with a `FakeClient` to wire up the scoring loop and prove the harness
works; the real pass-rate *differences* need a real model.

## Going deeper - context order is also cost
Put `datetime.now()` in your system prompt and watch your prompt cache stop hitting
(the prefix changes every request). Context isn't only about quality; its *order*
decides what can be cached. That thread returns in Module 11.
