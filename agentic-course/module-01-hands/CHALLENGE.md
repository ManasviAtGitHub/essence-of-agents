# Coding Challenge - make your own hand (no key required)

1. **Write a tool and inspect its spec.** Add a `@tool` function of your own - say,
   `word_count(text: str) -> str` - and print `word_count.spec()`. Read the JSON: that
   dict is exactly what the model sees. Change the docstring `Args:` line and watch the
   schema's `description` change.

2. **Drive it offline.** Add your tool to a `FakeClient` script and run it through
   `build_agent(client=...)`:

   ```python
   from claude_harness.testing import FakeClient, reply, text_block, tool_use_block
   client = FakeClient([
       reply(tool_use_block("word_count", {"text": "one two three"})),
       reply(text_block("That has 3 words.")),
   ])
   ```

3. **Break a hand on purpose.** Make a tool raise (e.g. divide by zero). Run it and
   read the trace: the harness catches the exception and feeds `is_error: true` back to
   the model instead of crashing. *Why* does the error go back to the model rather than
   to you? (That's the seed of Module 6 - verification and self-correction.)

## The point to feel
Every "hand" is the same three parts: a name, a description, a schema - plus your
function. New capability = new tool, never a new loop and never a new model.

## When you have a real model
Re-run `hands.py` with a key (or the Ollama adapter) and give it a fuzzy task. Watch
*it* pick which hands to use and in what order. That choice - which the FakeClient
can't show - is the whole aha of this module.
