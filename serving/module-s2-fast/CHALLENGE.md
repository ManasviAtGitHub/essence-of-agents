# S2 Challenge - Make it fast

Two levers on tok/s = bandwidth / bytes. Show you can pull each.

## The pile (quantization)
1. A 13B model at fp16. Bytes per token? Now at int4? Give the tok/s ratio
   between them on the same GPU, and say why it is exactly that ratio.
2. Someone proposes int2 to go twice as fast again. Using S2's quality cliff,
   say what you would test before shipping it - and why int4 is usually the stop.
3. The KV cache also grows (S1/M3). If you quantize the KV cache from fp16 to
   fp8, what gets cheaper, and for which kind of request does it matter most
   (short chats or long-context ones)? Why?

## The floor (the kernel)
4. A matmul has 4,096 x 4,096 output cells. A scalar loop does one per step.
   SIMD does 8. A GPU does (say) 4,096 at once. Order-of-magnitude, how many
   "steps" does each take? What does that tell you about why the GPU wins - is
   it faster per worker, or something else?
5. flash-attention never writes the full attention-scores matrix to memory.
   Connect that to S0's doorway: which cost does it cut, and why does "compute a
   tile, then forget it" help a MEMORY-bound machine?

## Put it together
6. You have a 7B model and one fixed GPU. List every S2 lever you would pull to
   serve it as fast as possible, and for each, whether it shrinks the PILE or
   works the FLOOR. Then name the one thing S2 does NOT change - the number of
   users you can serve at once (that is S5).

## Done when
You can take a model and a GPU and say - with numbers - how much quantization
buys, what a good kernel buys, where the quality cliff is, and which of the two
levers each real tool (GGUF int4, flash-attention, WebGPU) pulls.
