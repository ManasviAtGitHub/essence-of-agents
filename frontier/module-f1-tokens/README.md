# F1 - Everything becomes a token

*Verified as of 2026-07. Exhibits age; the principle does not.*

Track 3, Module 1 taught that the model never sees letters - only menu
entries. Then how is it suddenly looking at photos, hearing speech, and
answering with pictures? Because the menu grew.

## Question
The model only ever reads tokens. What actually happens to a photo - pixel
by pixel - so that the same transformer you opened in track 3 can attend
over it next to words?

## Principle
**The menu grows - through two different doors.**
- **The input door (continuous):** an image is cut into square PATCHES; each
  patch's pixel values are flattened into a vector and pushed through a
  learned linear layer (the PROJECTOR) into the same space as word
  embeddings. It is not a vocabulary lookup - it is a projection - but the
  result is an h like any other, and M2's attention treats it identically.
- **The output door (discrete):** to EMIT an image or speech, the menu
  literally grows - a learned CODEBOOK of image/audio tokens the model
  predicts autoregressively, exactly like words (M0's loop, unchanged).
  Speech is the special case: the Omni recipe runs INPUT audio through the
  same codebook - one audio menu, used in both directions.
One transformer, one stream; "multimodal" is new entrances, not a new brain.

## Dated exhibits (rule 10)
- Qwen3-VL (Oct 2025) / InternVL3 (Apr 2025): the patches -> projector ->
  LLM recipe at its ceiling - native resolution, GUI control.
- Qwen3.5 (Feb 2026): the flagship open model is natively vision-language -
  "VLM" as a separate model class is dissolving.
- Qwen3.5-Omni (Mar 2026): speech as codebook tokens, BOTH directions.
- Nano Banana Pro (Nov 2025): the consensus-best image generator is
  AUTOREGRESSIVE (~1,290 image tokens per image) - tokens beat diffusion at
  its own game. The reverse-attack exhibit.

## See it (no key)
`widgets/patch-stream/index.html` - two passes on one p5 stage + a D3 menu
chart:
- **intuition (8 steps):** a question about a photo; the photo SHATTERS into
  patches; the patches fly into the token stream beside the words; attention
  arcs treat both alike; then the other doors - speech in, images out - and
  the growing menu.
- **mechanism (21 steps, 4 acts):** act 1 computes one patch end to end on a
  toy 4x4 grayscale image - pixels -> flatten -> the projector's arithmetic,
  every number on screen. Act 2 is the real bill: tokens = (H/p) x (W/p),
  computed live with size/patch controls, and what one screenshot costs the
  KV cache (M3's meter returns). Act 3 is the output door - the image
  codebook (now it IS a menu), then SPEECH computed properly: quantization
  (a frame vector snapped to its nearest codebook entry, distances computed
  live), stacked residual codebooks, and the way back out (Omni's
  Thinker/Talker). Act 4 names the family: ViT (2020) -> CLIP (2021, where
  "image and text in one space" was born) -> the VLM recipe (LLaVA 2023:
  eye -> projector -> LLM; honesty note - act 1 skipped the eye) -> native
  multimodal (the seam removed, Feb 2026) -> VLA (add an action head;
  RT-2 Jul 2023, F5 opens the box).

## The aha
"Multimodal" is not a new kind of intelligence bolted on. It is M1's menu
with more entrances (projected patches in) and more entries (codebooks out) -
and everything downstream, from attention to the KV bill, follows unchanged.

## Honest notes
- The toy image, its pixel values, and the tiny projector matrix are
  hand-authored (labeled); every projection, token count, and cache figure
  derived from them is computed live on screen.
- Token-count arithmetic uses primary recipes: ViT's 16x16 patches (224x224
  -> 196 tokens) and the Qwen-VL 28px merged-patch recipe. Nano Banana Pro's
  ~1,290 tokens/image appears as a labeled exhibit stat, not in arithmetic
  (rule 11 - secondary-sourced).
- Codebook sizes in the menu chart are labeled illustrative.

## Done when (the bar for this module)
Given an image size and a patch size, you can compute how many tokens the
image costs, and say which door it entered through - projection (in) or
codebook (out). `CHALLENGE.md` is that exercise.

## Next
F2: the 2026 flagships refuse to pay M2's n^2 and M3's KV bill - sparse
indexes, linear states, and one very public retreat.
