# Module 1 - Hands (tools)

The model can only emit text. So how does text become a real action?

## Question
In Module 0 we hard-coded one tool. How does the model actually *request* an action,
and how do we give it a whole menu without changing the loop?

## Principle
You describe tools **in the context** - each as a name, a description, and a JSON
schema. The model emits a structured *request* to use one. **Your code is the
runtime** that executes it. The model never acts; it asks.

## Build (offline-friendly)
- `schema_demo.py` - **no key needed.** Shows how the `@tool` decorator turns a plain
  Python function into the exact JSON spec the model receives. This is "tools are just
  text in the context," made concrete.
- `hands.py` - a multi-handed agent (read_file, list_dir, calculate, reverse). Run it
  with `ANTHROPIC_API_KEY` set to watch a real model pick tools.
- `offline_demo.py` - **no key needed.** Runs the same toolset under a scripted
  `FakeClient`: the loop, dispatch, and real tool execution all happen offline.

## The aha (needs a real model to *feel*)
We added four tools and a custom one - and never touched the model or the loop. The
competence to use a tool was already latent in the model; we just granted permission
and a parser. Offline, the FakeClient can show the *plumbing* but not the *choosing* -
run `hands.py` with a key (or the future Ollama adapter) to feel the model do the
deciding.

## Structured output (related)
Tool schemas make the model's *request* parseable. The same idea makes the model's
*answer* parseable: with the real API you can pass `output_config={"format": {...}}`
(or `strict: true` on a tool) to force valid JSON. We'll wire this into the harness
when we move past the FakeClient.

## Beyond hand-written menus (MCP)
Here you write every tool yourself. In the wild there's a standard for this: **MCP**
(Model Context Protocol) lets external *servers* publish tool menus that agents
discover at runtime - same physics (descriptions in the context, a runtime executing
the call), standardized plug. The production track's "Scale it" chapter has a keyless
simulation of it.

## Security seed (paid off in Module 9)
`hands.py` lets the model read files off your disk and act on whatever text comes
back. Hold that thought: the model can't reliably tell *instructions* from *data* -
both are just tokens - so a file (or web page) it reads can try to steer it. That's
prompt injection, and it's the whole of Module 9.

## Graduating to the harness
You wrote the loop by hand in Module 0. From here the same loop lives in
`claude_harness/agent.py` -- read the two side by side. The harness adds a tool registry,
error handling (it returns `is_error` instead of crashing), `pause_turn` / iteration
limits, and tracing -- but it is the *same* observe-act loop. The offline demos and the
capstone build on it, so this is where you switch from writing the loop to using it.

## Run
```bash
python agentic-course/module-01-hands/schema_demo.py     # no key
python agentic-course/module-01-hands/offline_demo.py     # no key
python agentic-course/module-01-hands/hands.py            # needs ANTHROPIC_API_KEY
```
