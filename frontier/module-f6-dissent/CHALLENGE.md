# Challenge - name the escape

Three 2026 systems land on your desk. Each abandons some part of "predict the next
token, left to right."

1. **System A** writes a 200-token answer in about 8 model passes instead of 200,
   by starting from noise and sharpening all positions together. Which escape is
   it, does it still predict tokens, and what does it trade away for the speed?
2. **System B** takes the last few frames of a driving scene plus a steering
   command and produces the next frame; you can play it. Which escape is it, and
   what is its "token"?
3. **System C** encodes two video frames to a short vector each, predicts the
   second vector from the first, and never renders a pixel. Which escape is it,
   where does its loss live, and what can it still do without generating anything?
4. A colleague says "world models will obviously replace token models - they
   actually understand the world." Give the single strongest counter-argument FOR
   tokens, using something that happened THIS year.

<details><summary>answer</summary>

1. **Diffusion (escape 1 - change the ORDER).** Yes, it still predicts TOKENS -
   same menu, same target, just denoised in parallel instead of left to right
   (LLaDA, Mercury - labeled). The trade: it must revise across steps and can
   wobble; lower quality-per-step is the price of the parallel speed.
2. **A world model (escape 2 - change the TARGET).** Its "token" is a FRAME:
   `p(frame t+1 | past frames, your action)` (Genie, Cosmos - labeled).
3. **JEPA (escape 3 - predict the gist, generate nothing).** The loss lives in
   REPRESENTATION (latent) space, not pixel space. Without generating anything it
   can still PLAN and predict outcomes - e.g. V-JEPA's zero-shot robot planning in
   latent space (labeled).
4. This same year, images, audio and ACTIONS all became tokens (F1, F5); the best
   image generator is autoregressive (tokens beating diffusion at its own game);
   and most diffusion LLMs are converted FROM token models. One loop keeps
   absorbing every new modality - so "the world" may just be another thing tokens
   learn to predict. No winner is declared (rule 12).

</details>

## The point
The 2026 headlines are not three miracles - they are three ways to fill the blank
in "predict the next ___": the word, the word out of order, the world's frame, or
the world's gist. Name the escape and you have read the paper.
