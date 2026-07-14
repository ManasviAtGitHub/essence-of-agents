# Challenge - design one, then run it

Use the drafting room. Four tasks: a design, a prediction, a match, and a full run.

1. **Design a long-context model on a budget.** You want the cheapest model that
   can hold a very long context. Which **Attention** dial do you pick, and which
   one do you avoid? Set the other four dials however you like, then read the
   **context** and **cost** meters - do they agree with your reasoning?
2. **Predict, then read the cost.** Before you press **run**: with **Full**
   attention, will the memory curve grow or stay flat as context grows? With
   **Linear**? Now set each and read the cost chart - were you right, and what is
   Full's memory at 1,000 tokens versus Linear's?
3. **Read the reveal.** Turn the dials until your dot lands on **~Qwen3.5**. What
   five choices did that take - and which single dial, flipped, would move you
   toward **~DeepSeek V4** instead?
4. **Run all five.** Set a design - say Omni . Linear . GRPO . Trained swarm .
   Diffusion - and press **run**. Read the simulated behavior: what goes *in* and
   *out*, how does it *reason*, how does it *write*, how is it *served*? Then flip
   **one** dial (Foundation to Autoregressive, or Deployment to Single) and run
   again - what changed in the behavior, and what did it cost?

<details><summary>answer</summary>

1. Pick **Linear** (or **Sparse**); avoid **Full**. Linear keeps a *fixed-size*
   state, so context is (nearly) free - the context meter reads high and cost
   low. Full re-reads and stores every past token (n^2 compute, growing KV), so
   its context meter is weak and cost steep. The meters agree because they encode
   exactly F2's lesson.
2. **Full grows** (KV = tokens x d - a rising line, ~8,000 values at 1,000
   tokens); **Linear stays flat** (a fixed d^2 = 64 values, forever). That flat
   line is why Linear's context meter is high - the computed curve proves the
   prediction.
3. **~Qwen3.5** = Omni . Hybrid . Specialists+distill . Single agent .
   Autoregressive. Flip **Attention** from Hybrid to **Sparse** (and Modality to
   Text) and you slide toward **~DeepSeek V4** - the same design space, one dial
   over.
4. Every stage is set by a different dial: **Modality** decides in/out (Omni ->
   image+audio in, text+speech out), **Attention** how context is held (Linear ->
   a fixed notebook, memory flat), **Training** the reasoning (GRPO -> a multi-step
   trace), **Foundation** the write order (Diffusion -> the whole line at once),
   **Deployment** the serving (swarm -> an orchestrator + workers). Flip Foundation
   to Autoregressive and the write turns left-to-right while the *passes* curve
   tilts from flat to a diagonal; flip Deployment to Single and throughput drops
   from ~Nx to 1x. The point: **all five** dials change the run - your whole design,
   simulated, not a two-knob toy.

</details>

## The point
A frontier model is not magic - it is five dial settings, each of which you can now
defend *and* simulate. Design one, predict its costs, then run it and watch every
dial shape the behavior. That is the whole track, in your hands: next year's
headline is just a new path through the same dials.
