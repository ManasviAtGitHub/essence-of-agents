# S1 Challenge - Read the real engine

You have read the forward pass and watched the cache fill. Now prove you can
reason about the engine, not just the picture.

## Warm-up (from the widget)
1. In `forward(token, pos)`, point to the exact line where the KV cache is
   WRITTEN and the line(s) where it is READ. Why can a key/value be cached and
   reused forever without changing the answer?
2. The walk predicts `'p'` after `"the ca"`. Which stage is where the model's
   *decision* actually happens - and which stages just move information toward
   it?

## The cost argument (the point of the module)
3. Generating a 1,000-token answer. With the KV cache, how many key/value pairs
   does the engine compute in total? Without it (recomputing the whole prefix
   each step)? Give both as a function of n, and name the two complexity
   classes.
4. The cache buys speed with memory - it must STORE every k,v. Using Module 3's
   formula (2 x layers x kv_heads x head_dim x bytes x tokens), explain in one
   sentence why the thing that made serving *possible* (S1) becomes the thing
   that *limits* it (the wall you will pack against in S5-S6).

## Go deeper (real engines)
5. Open `karpathy/llama2.c`'s `run.c` (or skim `llama.cpp`). Find its forward
   pass and match three of its steps to three lines of our engine. Name one
   thing it does that ours does not (e.g. RMSNorm, RoPE, SwiGLU, many layers) -
   and say whether that changes the *shape* of the forward pass or just scales
   it.
6. Our model is ~1,130 weights and runs instantly. A 1B model is ~1,000,000x
   bigger. Which line of `forward()` does that 1,000,000x land on hardest, and
   what does that tell you about where all the serving time goes? (That is S0's
   question - carry your answer there.)

## Done when
You can walk a stranger through one forward pass from `token` to `logits`, point
to the cache write and read, and state - with the n and n^2 - why one line is
the difference between a demo and a server.
