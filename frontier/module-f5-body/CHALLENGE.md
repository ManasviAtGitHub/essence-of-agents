# Challenge - from a pixel to a motion

A VLA controls a robot arm. One camera frame arrives; the goal is "stack the
block."

1. The camera frame is 224x224. Using F1's ViT recipe (16x16 patches), how many
   PATCH tokens does the frame cost, and where do they enter the stream?
2. The model's next tokens are ACTIONS. Which earlier module's sampling loop
   produces them, and which module's menu do they come from?
3. A 1-second motion of a two-joint arm is DCT-compressed: keep the 3 largest
   coefficients per joint, each snapped to a 256-entry codebook. Roughly how
   many action tokens is that second of motion - and is the step reversible?
4. Cortex emits action tokens at ~8 Hz. A smooth grasp needs ~200 Hz control.
   Name the design that reconciles the two, and say which layer decides WHAT to do
   vs HOW to move.

<details><summary>answer</summary>

1. (224 / 16)^2 = **196** patch tokens. They enter the SAME stream as word
   tokens (each patch projected to the model dimension) - M2's attention treats
   them identically. That is F1's input door.
2. M0's autoregressive loop (sample -> append -> repeat) produces them, from a
   new region of M1's token menu (a learned action codebook) - actions as tokens.
3. ~**6 tokens** (3 kept per joint x 2 joints -> codebook indices -> BPE). It is
   **reversible**: the tokens rebuild the coefficients, the inverse DCT rebuilds
   the wave, and the arm follows it - FAST's round trip.
4. **Figure Helix's two-speed stack**: the slow token model chooses WHAT (~7-9
   Hz); a fast continuous policy handles HOW (~200 Hz). Actions-as-tokens
   (pi-0.7 + FAST) is the opposing bet - no winner declared (rule 12).

</details>

## The point
"How does a language model move a robot?" is now a one-line answer: a camera is
tokens IN, a motor is tokens OUT, and the same transformer predicts both - right
up to the speed where motion stops fitting in tokens.
