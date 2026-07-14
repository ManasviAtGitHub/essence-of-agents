# F2 - Attention unchained

*Verified as of 2026-07. Exhibits age; the principle does not.*

Track 3 taught two bills: attention compares every token to every earlier
token (M2's n^2), and every earlier token's K,V must be remembered (M3's KV
formula). The 2026 flagships refuse to pay - three different ways.

## Question
M2 said: to look back you must compare against EVERYTHING. M3 said: you must
REMEMBER everything. The frontier's flagships do neither. How - and what did
each escape route cost?

## Principle
Three positions in a live argument (rule 12: we teach the argument, not a
winner):
- **SPARSE: learn where to look.** A cheap learned INDEXER scores all past
  tokens; exact attention runs only over the top-k. The reads collapse
  (128k -> ~2k); the cache itself survives until compression joins in.
  Lineage (all DeepSeek until noted): NSA, Native Sparse Attention (Feb
  2025) -> DSA, DeepSeek Sparse Attention - the "lightning indexer"
  (DeepSeek V3.2, Sep 2025) -> DeepSeek V4's CSA+HCA compression stages
  (Jun 2026: ~27% of V3.2's per-token FLOPs, ~10% of its KV) -> adopted by
  GLM-5 (+IndexShare) and MiniMax M3's MSA (2026).
- **LINEAR: stop keeping the list.** Replace the growing KV with a
  FIXED-SIZE state updated as tokens stream past - a small notebook instead
  of a wagon train (the widget draws it as a 4-slot notebook). O(1) memory
  at any context. Lineage: Gated DeltaNet
  (Qwen3-Next, Sep 2025) -> Kimi KDA (Oct 2025: 75% KV cut, ~6x decode at
  1M) -> Qwen3.5 (Feb 2026: ~75% of a FLAGSHIP's layers are linear).
- **THE DISSENT: pay full price.** MiniMax - the linear pioneer - went BACK
  to full attention for M2 (Oct 2025): hybrids matched benchmarks at small
  scale but degraded multi-hop reasoning when scaled. The field's
  best-documented negative result. (Their M3 then chose sparse, not linear.)
Bonus exhibit: mHC (DeepSeek, Dec 2025) - the residual stream itself
redesigned; the first frontier change to that layer in a decade.

## See it (no key)
`widgets/three-escapes/index.html` - two passes:
- **intuition (7 steps):** the two bills return; the spotlight (sparse); the
  notebook (linear); the retreat (dissent); the open argument.
- **mechanism (14 steps, 3 acts):** act 1 computes SPARSE on a toy context -
  a 2-D indexer scores 8 past tokens live, top-3 selected, exact attention
  reads 3 not 8; the lineage dated; the indexer's own cost as the new
  bottleneck (IndexShare). Act 2 computes LINEAR - a 2x2 state updated by
  outer(k,v) across three steps, read by q, every number on screen; the
  state never grows. Act 3 is the argument: a D3 chart of entries READ per
  new token (full n / sparse k / linear constant, computed), the honest
  storage-vs-reads distinction, and the M2 retreat presented straight.

## The aha
The n^2 wall and the KV bill were never laws of nature - they were design
choices, and 2026 is the year the field split three ways on them, in public,
with evidence on every side.

## Honest notes
- Toy vectors are hand-authored (labeled); every indexer score, top-k
  selection, state update and read is computed live.
- SPARSE (NSA/DSA) cuts what attention READS, not what the cache STORES -
  storage falls only when compression joins (V4's CSA/HCA). LINEAR cuts
  storage to a constant. The widget keeps this distinction explicit.
- The toy linear layer omits normalization/gating (KDA's channel-wise gate
  is described, not computed) - labeled.
- All flagship numbers are primary-sourced (tech reports); the M2 retreat is
  the vendor's own engineering account.

## Done when (the bar for this module)
Given a design (full / sparse top-k / linear) and a context length, you can
say how many entries the attention step reads for one new token, what is
stored, and name each design's documented failure risk. `CHALLENGE.md`.

## Next
F3: the reward signal escapes its stage - RL in pretraining, mid-training,
and at test time.
