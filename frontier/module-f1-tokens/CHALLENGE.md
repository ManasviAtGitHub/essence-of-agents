# Challenge - price the image, name the door

The two-door rule from this module: images ENTER by projection (continuous
vectors), images and speech LEAVE by codebook (discrete menu entries). Speech
is the special case: the Omni recipe runs INPUT audio through the same
codebook too - one audio menu, both directions.

## Part 1 - count the tokens (be the projector's accountant)
Using the standard recipes from the widget:

1. ViT recipe, 16x16 patches: how many tokens does a 224x224 image cost?
2. Same recipe: a 448x448 image?
3. Qwen-VL recipe (28px merged patches): a 1344x896 screenshot?
4. At Module 3's Llama-3-70B rate (~328 KB of KV cache per token), roughly
   how much cache does that screenshot alone occupy?

<details><summary>answer</summary>

1. (224/16) x (224/16) = 14 x 14 = **196 tokens**.
2. (448/16) x (448/16) = 28 x 28 = **784 tokens** - 4x the pixels, 4x the
   tokens. The bill scales with AREA.
3. (1344/28) x (896/28) = 48 x 32 = **1,536 tokens** - one screenshot costs
   more context than most prompts.
4. 1,536 x ~328 KB = ~**503 MB** of KV cache - for ONE image in ONE
   conversation. (Rates differ per model; the POINT is that M3's memory
   story follows multimodal tokens unchanged.)
</details>

## Part 2 - name the door
For each, say which door it uses - PROJECTION IN (continuous, no new menu
entries) or CODEBOOK OUT (discrete, the menu literally grows) - and why:

- A. The model answers a question about a photo you attached.
- B. The model generates a picture of an umbrella (Nano Banana Pro style).
- C. The model transcribes what you said out loud.
- D. The model replies in spoken audio (Omni style).

<details><summary>answer</summary>

- **A - projection in.** Patches -> flatten -> projector -> h. No vocabulary
  entries involved; attention sees vectors it can attend over.
- **B - codebook out.** To EMIT pixels autoregressively the model needs a
  discrete menu of image tokens to sample from - M0's loop needs a menu.
- **C - codebook in (the Omni recipe).** The wave is sliced into ~20ms
  frames and each frame is SNAPPED to its nearest entry in the learned audio
  menu - the same discrete tokens the model later speaks with. Understanding
  does not REQUIRE sampling, so a projection would also work - but Omni
  shares one audio menu across both directions, and that is what the widget
  computes.
- **D - codebook out.** Speech is emitted as codebook tokens rendered to
  waveform - the dice of M0, rolling over sound.

The rule of thumb: READING can ride a projection; SAYING needs a menu,
because sampling (M0, the loop module) only works over discrete choices.
Speech-in is the exception that proves the rule: Omni snaps input audio onto
the very menu it speaks from.
</details>

## The point
Once you can price an image in tokens and name its door, every multimodal
headline reads mechanically: "native multimodal" = projection trained from
token one; "generates images/speech" = a codebook joined the menu. Same
transformer. Same loop. Bigger menu.
