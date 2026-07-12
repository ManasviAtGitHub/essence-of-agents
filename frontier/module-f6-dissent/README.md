# F6 - The dissent: tokens versus worlds

*Verified as of 2026-07. Exhibits age; the principle does not.*

Everything so far - reading, talking, looping, moving - Cortex did by predicting
the next token. This module is the first serious bet that the foundation *itself*
is wrong. A new character, **Somni**, predicts the world instead of the word.

## Question
Every skill Cortex learned runs on one move: predict the next token. In 2026,
roughly two billion dollars of new labs bet that foundation is wrong. What are the
escapes - and what does each predict instead of the next token?

## Principle
**Three escapes from "predict the next token, left to right":**

1. **Diffusion (change the ORDER).** Denoise the whole sequence in parallel instead
   of writing it left to right. Still tokens, same target - just not one at a time.
   Fewer, parallel passes -> far faster; the cost is that it must revise and can
   wobble. Escape 1 bends the loop; it does not leave it.
2. **World models (change the TARGET).** Predict the next FRAME of a world, given
   the past frames and your action: `p(frame t+1 | frames so far, action)`. The
   "token" is now a frame - and you can steer it.
3. **JEPA (change the target AND generate nothing).** Encode the world to a gist
   and predict the next gist; the loss lives in representation space, and no pixels
   are ever drawn. Understanding without generating.

**The honest counter (rule 12):** this same year, images, audio and actions all
BECAME tokens (F1, F5); the best image generator is autoregressive (tokens beating
diffusion at its own game); and most diffusion LLMs are converted from token
models. The token loop keeps winning. So next-token prediction is not physics - it
is a **bet**, currently winning, and now seriously contested for the first time.

## Dated exhibits (rule 10)
- **Diffusion went production:** LLaDA 2.0 (Dec 2025, 100B, converted FROM an AR
  model); Mercury 2 (Feb 2026, >1,000 tok/s with reasoning).
- **Playable world models became products:** Genie 3 -> Project Genie (consumer,
  Jan 2026); Cosmos 3 (Jun 2026) unifies simulation + reasoning + action; Sora 2
  (Sep 2025) as a passive world simulator.
- **The institutional bet against tokens:** LeCun exits Meta (Nov 2025) -> AMI
  Labs, $1.03B seed (Mar 2026), V-JEPA lineage, "predict in representation space";
  World Labs Marble + $1B (Feb 2026), the world as a persistent 3D structure.
  Roughly $2B wagered against next-token prediction.
- **The counter-exhibit:** the frontier image generator is autoregressive (~1,290
  image tokens) - tokens beating diffusion at its own game.

## See it (no key)
`widgets/tokens-vs-worlds/index.html` - two passes:
- **intuition (8 steps):** the bet under everything; Somni debuts (a WORD vs a
  WORLD on the same falling ball); escape 1 (diffusion, beside Cortex's
  left-to-right); escape 2 (a playable dream-world you steer); escape 3 (JEPA - the
  gist, generating nothing); the debate; the token bet keeps winning; the aha.
- **mechanism (13 steps, 3 acts):** act 1 writes the same sentence two ways - six
  sequential autoregressive steps vs ~four parallel diffusion refinements, then the
  reminder that diffusion is *still tokens*. Act 2 swaps the target: a world model
  advancing frame by frame, then JEPA's loss in representation space. Act 3 is the
  dated argument: one unified token loop vs a ~$2B world-model bet. No winner.

## The character
**Somni** (from Latin *somnium*, dream) debuts here and is single-sourced into
`assets/cast.js`. Cloud-soft, eyes closed. **Design rule:** Somni never uses a
speech bubble - it shows a small WORLD in a thought bubble. Cortex predicts the
word; Somni predicts the world.

## The aha
Next-token prediction was never physics - it is a bet, currently winning and, for
the first time, seriously contested. You now hold both arguments: one loop that
turns everything into tokens, and a rival that predicts the world itself.

## Honest notes
- The toy sentence, the falling-ball physics, and the 6-vs-4 step counts are
  hand-authored (labeled). Dates, $ amounts and tok/s are the labs' own claims -
  narrative color, never measured here (rule 11).
- The playable world is labeled "a toy cartoon of the idea." A real world model
  dreams the pixels; this fakes them to show the LOOP - every frame predicted from
  the last frame plus your action.
- Diffusion is shown still predicting tokens (escape 1 bends the loop; it does not
  leave it). No camp is declared the winner (rule 12).

## Done when (the bar for this module)
You can name the three escapes, say what each predicts instead of the next token,
and give the strongest argument FOR tokens. `CHALLENGE.md`.

## Next
F7: the dated atlas - every exhibit in this track as a filterable pin - and F8,
the drafting-room capstone, where you design a frontier model one dial at a time.
