# Challenge - give the headline a home

Four headlines drop that are not named in the atlas. For each, say **which
principle it attacks** (one of the seven), **which lane** it belongs in, and
whether it is an **attack or a counter**.

1. A startup ships a chat model that writes its entire 300-token answer in ~10
   model passes by denoising all positions at once, not left to right.
2. A humanoid robot is driven by one transformer that reads camera patches and
   emits joint-angle tokens - but a separate fast controller does the actual
   smooth motion at 200 Hz.
3. A lab folds the reward signal directly into pretraining: the model thinks a
   short private thought before each token and is rewarded when it helps.
4. A frontier lab's new flagship quietly drops its linear-attention layers and
   goes back to full attention, citing lost accuracy on multi-hop questions.

<details><summary>answer</summary>

1. Attacks **"predict the next token, left to right"** (F6 / Foundation lane).
   An **attack** - it is a diffusion LLM (escape 1: change the order). Still
   tokens, though; the target did not move.
2. Attacks **"an agent acts through software & senses text"** (F5 / Body lane) -
   actions became tokens. But the 200 Hz controller is the **counter**: tokens
   are too slow for smooth motion (the Figure Helix argument). One headline,
   both an attack and its counter.
3. Attacks **"training is a fixed row of stages"** (F3 / Training lane) - an
   **attack**: RL leaks out of the final polish step into pretraining itself
   (the RLP move).
4. Attacks **"attention must compare against & remember everything"** (F2 /
   Attention lane) - but as a **counter**: it defends full attention against the
   sparse/linear escapes, exactly like MiniMax M2's revert. A negative result is
   an exhibit too.

</details>

## The point
A headline you have never seen is not new physics - it is a dated move against a
principle you already hold. Name the principle and the lane, decide attack or
counter, and you have filed it. That is the whole skill the track was for.
