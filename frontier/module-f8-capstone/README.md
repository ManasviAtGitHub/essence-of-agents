# F8 - CAPSTONE: The drafting room

*Verified as of 2026-07. Exhibits age; the principle does not.*

Seven modules taught you to *read* the frontier. This one has you *build* one.
Turn a dial per module and design a frontier model - then actually **run the
model you designed**, live in the browser, and watch its costs come true.

## Question
You have watched every lab make its choices. Can you make yours - one dial per
module - and do you understand what each one *costs*?

## Principle
**The frontier is a small set of dials, and every famous 2026 model is one path
through them.** This capstone is the constructive mirror of the track: instead of
reading a headline and naming the principle it attacks, you set the principles
yourself and get the headline back ("you just designed ~Qwen3.5").

Five dials, one per module:
- **Modality** (F1/F5): text / vision-language / omni / +actions
- **Attention** (F2): full / sparse / linear / hybrid
- **Training** (F3): SFT+RLHF / GRPO / rubric rewards / specialists+distill
- **Deployment** (F4): single agent / trained swarm
- **Foundation** (F6): autoregressive / diffusion / world-model

And the capstone's spine is a loop: **design -> predict -> run -> measure.**
- **Design**: each committed dial inks a Rough.js blueprint of your model.
- **Predict**: D3 meters price the choice (cost / speed / context / risk); your
  dot drifts through a sky of real 2026 models and settles beside its nearest
  star, with the real model card and a rule-12 warning card for risky dials.
- **Run**: press *build & train* and a **real ~900-weight transformer** trains
  in the page - `models/nanomodel` ported to JavaScript (scalar autograd, one
  causal attention head, next-token SGD). The **Attention dial swaps genuine
  full / sparse / linear code**, so you run the mechanism you chose.
- **Measure**: the KV-memory curve is computed from the *real* mechanism - Full
  grows with every token, Linear stays flat (F2's "KV cache abolished") - which
  *verifies* the context meter F8 only predicted. The serving bill (KV x context
  x concurrent users) is the doorway to the next track.

## See it (no key)
`widgets/drafting-room/index.html` - one page, three layers (Rough.js blueprint,
D3 sky + meters, a live in-browser trainer). Load a preset (MiniMax M2, Qwen3.5,
DeepSeek V4) or turn the dials yourself; then train with Full attention, switch
to Linear, and compare the two runs' memory curves.

## The aha
You can rebuild the frontier from the principles you own - not just name a model,
but *design* one and watch it run. Which means next year's frontier is already
readable: it will be new dial settings, not new physics.

## Honest notes
- The runnable model is a deliberate **toy** (~900 weights, 6-char context, a
  two-line corpus) so it trains in seconds. Real models are this exact math,
  scaled a trillion-fold.
- **Attention is the real, working bridge** (full/sparse/linear are genuine
  swappable code). Because it is a toy, absolute *speed* differences are tiny -
  which is why the verdict leads with **memory** (the honest, scale-invariant
  win, and exactly F2's point). Foundation/Modality/Deployment ride along as
  design choices (labeled); a text toy cannot truly train on images or a swarm.
- The meter deltas are hand-authored and illustrative (rule 11); the anchor
  figures on hover are the labs' own claims. Warnings are dated exhibits, not
  verdicts (rule 12).

## Done when (the bar for this module)
You can design a model, say what each dial costs, and - from the *running* model -
explain why linear attention changes the memory bill while full attention pays
for every token. `CHALLENGE.md`.

## Next
Track 5 - serving and infrastructure. The serving bill this capstone computes
(KV per user, batch economics) is its doorway: paying that bill at real scale is
the next story.
