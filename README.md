# agents

**Open the course:** https://manasviatgithub.github.io/essence-of-agents/
(all four tracks - the agent loop, production, inside the model, the frontier -
run right in the browser, no setup).

Two things live here:

1. **`claude_harness/`** - a small, reusable Claude agent harness (the agent loop +
   tools + tracing) that we keep around as infrastructure for everything else.
2. **`agentic-course/`** - a first-principles agentic-AI course inspired by
   3Blue1Brown (build intuition) and The Coding Train (build it live, from scratch).

The relationship: the course's `module-00-smallest-agent/agent.py` is the
*from-scratch teaching version* of an agent. `claude_harness` is the grown-up,
reusable version that the same ideas distill into. (The course's interactive
widgets are self-contained HTML simulations that replay scripted or recorded
data - they don't call the harness, a server, or any model.)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # PowerShell: $env:ANTHROPIC_API_KEY="..."
```

## Quick start

```bash
python -m claude_harness.examples.self_explain   # the harness reads its own source
```

## Thesis (the one sentence the course defends)

> An LLM is, near enough, a pure function: context in, a distribution over next
> tokens out. It keeps no memory between calls unless you put it there. So most of
> building an agent is two jobs - deciding what goes into the context, and turning
> some of what comes out into actions.

Default model everywhere: `claude-opus-4-8`.
