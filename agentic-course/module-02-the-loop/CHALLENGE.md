# Coding Challenge - measure what thinking is worth

The widget shows the effect on one problem. Turn the anecdote into evidence.

## With a real model (key or Ollama)
1. Collect ~10 reasoning-trap problems (bat-and-ball variants, simple logic puzzles)
   with known answers.
2. Run each twice with the harness - same model, same prompt, one variable changed:

   ```python
   from claude_harness import Agent
   think = Agent(thinking=True)
   quick = Agent(thinking=False)
   # for each problem p: compare think.run(p) vs quick.run(p) to the known answer
   ```
3. Score correct / incorrect for each setting and compare the two rates.

You just built a **one-variable eval**: change a setting, measure the effect, keep or
revert. That habit is the whole of Module 10.

## Offline (no key)
You can stub the experiment with a `FakeClient` scripted to return a "reasoned" answer
vs a "blurted" one per problem - useful for wiring up the scoring harness. But the real
*signal* (does reasoning actually help?) needs a real model; the stub only exercises
the plumbing.

## Going deeper
Add an explicit text scratchpad to the loop ("Thought: ... Action: ... Observation:
...") instead of relying on the model's built-in thinking, and compare. When does an
*external* scratchpad beat *internal* thinking? That question returns in Module 7.
