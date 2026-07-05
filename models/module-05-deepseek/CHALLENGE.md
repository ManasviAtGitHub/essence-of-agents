# By hand - weigh MLA, and name the resource

## 1. MLA cache
DeepSeek-V3: 61 layers, MLA latent d_c = 512, decoupled RoPE key d_h^R = 64,
fp16 (2 bytes).
- Elements cached per token per layer? (d_c + d_h^R)
- Bytes per token for the whole model? (x 2 bytes x 61 layers)
- At 128k tokens (131,072), how many GB of cache? (1 GB = 1e9 bytes)

## 2. The comparison
Standard MHA for the same model would cache 2 x n_heads x head_dim per token
per layer, with 128 heads and head_dim 128.
- Elements per token per layer for MHA?
- MHA / MLA ratio? What percent reduction is that?
- The paper reports 93.3% for DeepSeek-V2 vs a 67B dense model. Why might your
  computed percentage differ from the reported one? (Think: different config.)

## 3. Why the extra 64?
MLA caches d_c + d_h^R, not just d_c. In one sentence: why can't the position
(RoPE) information be folded into the compressed latent, forcing a separate
small position key?

## 4. Name the resource
For each trick, name the ONE resource it primarily attacks (memory / compute /
decode-speed) and the module that taught it:
GQA, MLA, MoE, MTP, quantization, KV-cache eviction.

## 5. MTP arithmetic
An MTP head drafts the next token; the main model verifies it in the same pass.
- If the draft is accepted 90% of the time, and each accepted draft saves one
  full forward pass, roughly what is the average number of tokens committed per
  pass? (Rough is fine.)
- Why does exact verification mean MTP costs NO quality, only adds speed?

## Stretch
- MLA's up-projections (latent -> per-head K,V) can be "absorbed" into the
  query and output matrices at inference. Why does that make decompression
  nearly free, and why does it NOT help at training time?
- You have now seen four memory/compute tricks (GQA, MLA, MoE, MTP). Design a
  hypothetical fifth that attacks a resource none of them target. What would it
  trade away?
