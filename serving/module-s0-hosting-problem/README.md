# S0 - The hosting problem

*Verified as of 2026-07. Bandwidth is the clock.*

You read the engine in S1 - a forward pass, in C. Now the first question of
hosting: why is running it slow, and why does it cost what it costs? Your
Track-1 agent called a model thousands of times without ever asking. The answer
is not the math. It is moving the weights.

## Question
To produce one token, what actually takes the time? And why can the same model
feel instant in a datacenter, sluggish on a laptop, and impossible on a phone?

## Principle
**A forward pass must read every weight from memory into compute - so speed is
set by the memory doorway (bandwidth), not the math.** Picture it: MEMORY holds
the weights; a COMPUTE unit does the arithmetic; between them is one doorway,
the memory bus. To make a single token, the whole model streams through that
doorway. The compute unit finishes the instant the bytes arrive and then sits
IDLE, waiting for the next load. This is being **memory-bound**, and nearly all
decoding is.

Two lines are the whole track's spine:
- **bytes per token = params x bits / 8.** A 1B model at 16 bits is 2 GB, read
  every token.
- **tokens/sec = bandwidth / bytes.** On a 900 GB/s GPU that is ~450 tok/s (a
  ceiling; real is lower). The only two ways to go faster are a smaller pile
  (quantize, S2) or a wider / better-used doorway (S2) - or reading the pile
  once and serving many users from it (batching, S5).

And it decides WHERE a model can live: the doorway comes in sizes (datacenter
GPU >> laptop > phone ~ browser tab), and a model runs only where its pile
clears the door fast enough.

## Dated exhibits (rule 10, illustrative - rule 11)
- Memory bandwidths, round 2026 figures: datacenter GPU ~3.3 TB/s, gaming GPU
  ~0.9 TB/s, laptop unified memory ~0.2 TB/s, phone ~60 GB/s. Model sizes:
  1B @ int4 ~0.5 GB, 7B @ fp16 ~14 GB, a frontier model, hundreds of GB.
- The decode-is-memory-bound fact (arithmetic intensity ~2 FLOP/byte, far below
  any modern accelerator's compute:bandwidth ratio) - the reason the doorway,
  not the FLOPs, sets the pace.

## See it (no key)
`widgets/hosting-problem/index.html`. **The machine:** watch a token get made -
the whole weight-pile streams through the doorway while the compute unit sits
idle (the memory-bound punchline). Make the model bigger (slower), quantize it
(smaller boxes, faster), and slide from cloud to browser (the doorway narrows).
**The clock:** the arithmetic - bytes = params x bits/8, tok/s = bandwidth /
bytes - computed live, plus the roofline that explains why decode waits on bytes
and prefill waits on math (M3's two phases, at the hardware level).

## The aha
Hosting is moving bytes fast enough. Bandwidth is the clock, and every trick in
this track is one move on this single picture.

## Done when
Given a model's parameters, its bits-per-weight, and a device's bandwidth, the
learner can compute bytes-per-token and the tok/s ceiling, and say whether the
model is memory-bound (it almost always is) and where it can run.

## Honest notes
- All bandwidths and sizes are round, illustrative figures (rule 11); tok/s here
  is the memory-bound CEILING (bandwidth / bytes) - real throughput is lower
  (overheads, imperfect utilization).
- "Reads every weight per token" is the decode picture. Prefill and mixture-of-
  experts models read a subset per token, but the framing holds: cost is bytes
  moved, and bandwidth is the clock.
