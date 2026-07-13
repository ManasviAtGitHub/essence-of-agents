# Challenge - design one, then run it

Use the drafting room. Three tasks: a design, a prediction, and a measurement.

1. **Design a long-context model on a budget.** You want the cheapest model that
   can hold a very long context. Which **Attention** dial do you pick, and which
   one do you avoid? Set the other four dials however you like, then read the
   **context** and **cost** meters - do they agree with your reasoning?
2. **Predict, then measure.** Before you press train: with **Full** attention,
   will the KV-memory curve grow or stay flat as context grows? With **Linear**?
   Now train each and read the "your runs" tally - were you right, and what is
   each one's KV at 1,000 tokens?
3. **Read the reveal.** Turn the dials until your dot lands on **~Qwen3.5**. What
   five choices did that take - and which single dial, flipped, would move you
   toward **~DeepSeek V4** instead?

<details><summary>answer</summary>

1. Pick **Linear** (or **Sparse**); avoid **Full**. Linear keeps a *fixed-size*
   state, so context is (nearly) free - the context meter reads high and cost
   low. Full re-reads and stores every past token (n^2 compute, growing KV), so
   its context meter is weak and cost steep. The meters agree because they encode
   exactly F2's lesson.
2. **Full grows** (KV = tokens x d - a rising line, ~8,000 values at 1,000
   tokens); **Linear stays flat** (a fixed d^2 = 64 values, forever). That flat
   line is why Linear's context meter is high - the running model proves the
   prediction.
3. **~Qwen3.5** = Omni . Hybrid . Specialists+distill . Single agent .
   Autoregressive. Flip **Attention** from Hybrid to **Sparse** (and Modality to
   Text) and you slide toward **~DeepSeek V4** - the same design space, one dial
   over.

</details>

## The point
A frontier model is not magic - it is five dial settings, each of which you can
now defend *and run*. Design one, predict its costs, then watch the real
mechanism prove you right. That is the whole track, in your hands: next year's
headline is just a new path through the same dials.
