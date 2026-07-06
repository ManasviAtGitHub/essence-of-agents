# Module 5 - DeepSeek's moves: MLA and MTP

Module 3 left a wall: the KV cache is the memory bill for long context, and at
frontier scale it is enormous. DeepSeek-V3 serves 128k context cheaply anyway,
with two targeted moves - each attacking ONE resource.

## Question
Module 3 said long context = a KV-memory wall (hundreds of GB for dense
attention). How did DeepSeek get cheap 128k context regardless?

## Principle
Two independent moves:
- **MLA (Multi-head Latent Attention)** attacks Module 3's KV-cache MEMORY.
  Instead of caching full keys and values per head, compress each token's K,V
  into ONE small latent (dim d_c = 512), plus a tiny decoupled position key
  (64) that RoPE cannot compress. Reconstruct per-head K,V on read via learned
  up-projections. Cache: 576 elements/token/layer vs MHA's 32,768.
- **MTP (Multi-Token Prediction)** attacks Module 0's DECODE speed. A small
  extra head predicts token n+2; at inference it drafts, the main model
  verifies in the same pass (speculative decoding) - two tokens per pass when
  accepted; denser training signal as a bonus.

The meta-lesson: every architecture headline targets one resource - name it.

## See it (no key)
`widgets/mla-mtp/index.html` - two passes:
- **intuition (10 steps):** the M3 wall at V3 scale (~3.8 MB/token dense),
  GQA's partial help, then MLA collapsing per-head K,V boxes into one latent -
  the cache bar shrinking to almost nothing (128k: ~500 GB -> ~9 GB). Then MTP:
  Module 0's one-token-per-pass loop, an extra head drafting n+2, verified for
  free. Aha: two moves, two resources (memory vs passes).
- **mechanism (18 steps, 3 acts):** act 1 computes MLA live - MHA 32,768 elem
  vs MLA 512+64=576, a 56.9x cut (paper reports 93.3% end-to-end), the RoPE
  decoupling, and the up-projection reconstruction. Act 2: MTP training (denser
  signal) and inference (draft -> verify -> accept, ~85-90% reported). Act 3:
  the map - GQA/MLA attack memory, MoE attacks FLOPs, MTP attacks speed - plus
  the honest note that these are trades, not magic.

## The aha
An architecture headline almost always targets ONE bottleneck. MLA shrinks the
KV-cache memory (M3); MTP speeds the decode loop (M0). Meet a new trick, ask:
which resource is it fighting?

## Honest notes
- Every cache figure is computed live from verified config (DeepSeek-V2/V3,
  arXiv 2405.04434 / 2412.19437): 128 heads, head_dim 128, 61 layers, MLA
  d_c=512, decoupled RoPE key 64, fp16. The element counts (32,768 vs 576) and
  the ~57x are computed; the paper's reported 93.3% (V2 vs 67B dense) is a
  different config, labeled as reported.
- MTP depth is 1 (verified); the ~85-90% acceptance rate is model-reported,
  labeled illustrative.
- MLA/MTP are trades (memory-for-compute; speed-for-machinery), not free wins.

## Done when (the bar for this module)
You can compute MLA's cache per token (d_c + d_h^R, times layers, times bytes)
and say what resource each of GQA/MLA/MoE/MTP attacks. `CHALLENGE.md`.

## Next
Module 6: same machine, different manners - how a base, a chat, and a reasoning
model all come from bending the same weights with different training. (Then
Module 7 makes reasoning its whole story - spending MORE decode passes on
purpose, the opposite of MTP's thrift.)
