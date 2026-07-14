# F8 - CAPSTONE: The drafting room

*Verified as of 2026-07. Exhibits age; the principle does not.*

Seven modules taught you to *read* the frontier. This one has you *build* one.
Turn a dial per module and design a frontier model - then **simulate what the
model you designed would do and cost**, with every dial live, in the browser.

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
- **Run**: press *run* and a **deterministic simulation** plays the model handling
  one request - and **all five dials** shape it. **Modality** sets what goes in and
  out (text / image+text / +audio+speech / camera+action tokens); **Training** sets
  the reasoning style (direct / GRPO multi-step / rubric-graded / distilled);
  **Foundation** sets the write order (autoregressive / diffusion-parallel /
  world-model rollout); **Attention** sets how context is held; **Deployment** sets
  the serving shape (one loop / orchestrator + workers).
- **Measure**: the cost is *computed from each mechanism* (rule 11), not guessed.
  **Memory** vs context (Attention): Full grows with every token, Linear stays flat
  (F2's "KV cache abolished"). **Passes** vs length (Foundation): autoregressive
  grows one pass per token, diffusion holds ~flat. Plus per-query compute (modality
  x reasoning) and throughput (workers). The serving bill (KV x context x users) is
  the doorway to the next track.

## See it (no key)
`widgets/drafting-room/index.html` - one page, four layers (Rough.js blueprint,
D3 sky + meters, a simulated behavior card, computed cost charts). Load a preset
(any of six real 2026 models - or click its star in the sky) or turn the dials
yourself; then press *run* and watch how the design behaves. Flip any dial and
run again - every one changes what you see.

## The aha
You can rebuild the frontier from the principles you own - not just name a model,
but *design* one and watch how it would behave and what it would cost. Which means
next year's frontier is already readable: it will be new dial settings, not new
physics.

## Honest notes
- The "run" is a **deterministic simulation** (rule 11) - the course's native mode
  - not a trained model. It composes the *expected* behavior of your design from
  the five dials and prices it from each mechanism's formula. It deliberately does
  not train a network: a real frontier model can't be trained in a browser, and a
  from-scratch char toy would only honor two of the five dials - exactly the
  disconnect this simulation avoids, so **every** dial changes the run.
- The two **cost curves are computed, not hand-waved**: memory grows / caps / flats
  with the Attention mechanism (F2); passes grow / flat with the Foundation
  mechanism (F6). Because absolute speed is scale-dependent, each verdict leads with
  the **scale-invariant** win (memory, passes) - the wins that hold a trillion-fold up.
- The behavior samples (a caption, an action trace, a reasoning line) and the
  compute / throughput multipliers are **illustrative** (rule 11) - the *shape* of
  what each design does, not a benchmark. The anchor figures on hover are the labs'
  own claims. Warnings are dated exhibits, not verdicts (rule 12).

## Done when (the bar for this module)
You can design a model, press run, and read back what each of the five dials did
to its behavior *and* its cost - why linear attention flattens the memory bill, why
diffusion writes the whole line at once, why a swarm buys throughput but not a free
lunch - and why each win only shows at scale. `CHALLENGE.md`.

## Next
Track 5 - serving and infrastructure. The serving bill this capstone computes
(KV per user, batch economics) is its doorway: paying that bill at real scale is
the next story.
