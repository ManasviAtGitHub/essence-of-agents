# Coding Challenge - give the agent a second hand

Add a `list_dir(path)` tool to `agent.py` **without changing the loop or the model
call.** Only two edits:

1. Add a tool definition to `TOOLS`:

   ```python
   {
       "name": "list_dir",
       "description": "List the entries in a directory, one per line.",
       "input_schema": {
           "type": "object",
           "properties": {"path": {"type": "string", "description": "Directory path"}},
           "required": ["path"],
       },
   }
   ```

2. Add a branch to `run_tool`:

   ```python
   if name == "list_dir":
       import os
       return "\n".join(sorted(os.listdir(args["path"])))
   ```

Then ask it something that needs both hands:

```python
print(agent("List the files here, then read the smallest .py file and summarize it."))
```

## What you should feel
New capability came from adding a tool and a branch. **The loop didn't change. The
model didn't change.** That experience is the whole point of Module 1: the model was
already capable of using tools - you just granted permission.

## Stretch
- Make a tool fail (read a missing file). Watch the exception. How should the agent
  hear about the error? (Peek at how `claude_harness` returns `is_error: true`.)
- Count how many times the loop runs for a two-tool task. That number is the agent
  "thinking out loud in actions" - the subject of Module 2.
