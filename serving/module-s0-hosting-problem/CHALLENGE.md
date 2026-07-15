# S0 Challenge - The hosting problem

The doorway is the whole model. Prove you can read the clock.

## Read the clock (do the arithmetic)
1. A 3B model at 8 bits. How many bytes must be read per token? On a laptop at
   200 GB/s, what is the tok/s ceiling? Show both steps.
2. You quantize the same model from 8 bits to 4 bits. Without changing anything
   else, what happens to the tok/s ceiling, and why - in terms of the doorway?
3. A 70B model at fp16 is ~140 GB. Name every device from the widget's spectrum
   on which it will NOT even fit, and the one on which it clears the doorway
   fast enough to be interactive.

## The idea (say it in your own words)
4. "Decode is memory-bound." Explain what that means using the doorway and the
   idle compute unit - no jargon. Then: why is PREFILL (the first token, over
   the whole prompt at once) the opposite - compute-bound? (Callback: M3.)
5. Two teams both want their model twice as fast. Team A buys a GPU with double
   the bandwidth; Team B quantizes from 8-bit to 4-bit. Using tok/s =
   bandwidth / bytes, show that BOTH get ~2x - and name one real cost each pays
   that the equation hides.

## Look ahead (place the track)
6. The equation has exactly three levers: shrink the pile, widen/better-use the
   doorway, or serve more tokens per trip. Match each lever to the module that
   pulls it (S2 quantize, S2 kernels, S5 batching). Which lever does NOT make a
   single token faster, only the whole SERVER faster - and why is that still a
   win?

## Done when
You can take any (params, bits, bandwidth), compute the tok/s ceiling out loud,
say why the number is a ceiling and not the real rate, and point to which lever
of the equation each later module pulls.
