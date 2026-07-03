# Module 0 - The smallest agent that could

The least you can add to a chat model to make it *do* something instead of just
*say* something. We end with a ~30-line agent that reads its own source and explains
itself.

## Run it

```bash
pip install -r ../../requirements.txt
export ANTHROPIC_API_KEY=...          # PowerShell: $env:ANTHROPIC_API_KEY="..."
python agent.py
```

It reads `agent.py` with a `read_file` tool, then explains its own loop.

## The three lines that carry the module
- `while True:` - **the loop is the agency.** Remove it and you have a chatbot.
- `messages` - **this list is the memory.** The model is handed the whole list every
  turn; it has none of its own.
- `run_tool(...)` - **your code is the runtime.** The model never touched your disk.
  It asked you to.

We write the loop by hand on purpose. The SDK has a `tool_runner` that hides it - we
earn the right to use that later, after we've seen what it's hiding. (The reusable,
grown-up version of this is `../../claude_harness/`.)

## The two observations we plant
- `no_memory_demo.py` - the model has no memory between calls (held for Module 3).
- `nondeterminism.py` - same input, different output (held for Module 10).

## The aha (from the build)
We added **zero** intelligence. The exact same model that would hallucinate a file
just read it for real - because we gave it a body (a tool), a clock (the loop), and a
place to keep notes (the message list).

## Break it on purpose
Delete `while True` and run once: the agent emits a tool *request* and then stops,
holding an answer it never got to use. That's exactly the gap Module 2 fills.

## Next
- `CHALLENGE.md` - add a second tool without changing the loop.
- `widgets/run-again/` - the interactive "watch it run twice" widget for the
  non-determinism aha.
