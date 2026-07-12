# F5 - The loop gets a body

*Verified as of 2026-07. Exhibits age; the principle does not.*

In course 1 an agent's tools were functions and its observations were text. This
module hands Cortex a camera and a motor - and the same chip you have followed
becomes a robot. Its output tokens turn into movements.

## Question
Course 1's loop was think -> call a tool -> read. What happens when the tool is a
MOTOR and the observation is a CAMERA - and how does a token become a movement?

## Principle
**A VLA is a VLM whose output tokens ARE actions.** The camera enters exactly as
F1's patches; the goal enters as words; and the model's next tokens come from a
new part of M1's menu - ACTIONS. To make a smooth motion tokenizable it is
DCT-compressed (keep the big coefficients, drop the tiny ones) and BPE-tokenized -
M1's exact algorithm, now driving a motor. One transformer, one stream, a bigger
vocabulary.

**The honest counter (rule 12):** tokens are slow. Cortex decides token-by-token
at ~7-9 Hz - fine for choosing WHAT to do - but smooth control wants ~200 Hz. So
Figure Helix splits it: slow tokens choose WHAT; a fast continuous policy handles
HOW. Actions-as-tokens has limits.

## Dated exhibits (rule 10)
- pi-0.5 -> pi-0.7 (Physical Intelligence, Apr 2026) + FAST: robot actions
  DCT-compressed and BPE-tokenized, plus a flow-matching head for continuous ~50Hz
  control - M1's principle driving motors.
- Figure Helix (Feb 2025 -> production): the honest counter - tokens think at
  7-9Hz, a continuous 200Hz policy moves.
- Gemini Robotics 1.5 / ER 1.6 (Sep 2025 ->): a planner VLM (with web search)
  hands to a VLA executor - course 1's loop, embodied.
- NVIDIA GR00T N2 / "world-action models" (2026): pretrained to imagine,
  fine-tuned to act - the bridge to F6.

## See it (no key)
`widgets/embodied-loop/index.html` - two passes:
- **intuition (7 steps):** the chip slots into a body; course-1's loop embodied
  (see -> think -> move -> observe); the puzzle (a motor takes angles, not words);
  the reveal (a motion chopped into tokens - M1's tokenizer on a motor); the menu
  grows an ACTIONS row; the two-speed catch; the aha.
- **mechanism (14 steps, 3 acts):** act 1 traces one camera frame -> patch tokens
  -> Cortex + goal -> action tokens -> joint angles -> the arm moves. Act 2
  computes the tokenizer: a 1-second wave -> DCT (keep the big 3) -> ~6 BPE
  tokens, reversibly. Act 3 is the two speeds: Cortex's ~7Hz think-clock vs a
  ~200Hz motion clock, the Helix two-speed stack, and the live argument.

## The aha
Course 1's loop and track 3's tokens converge in a robot: the loop is the body's
mind, and actions were tokens all along - until the fastest motion says otherwise.

## Honest notes
- The toy wave, its DCT coefficients, the ~6-tokens-per-second count, and the
  joint angles are hand-authored (labeled). The Hz figures (7-9, 200) are the
  vendors' own; token counts are illustrative.
- "The eye is just M1's menu" reuses F1's patch recipe; it is not re-derived.
- The two-speed split is Helix's stated design; pi-0.7's single-stream claim is
  the counter-position. No winner is declared (rule 12).

## Done when (the bar for this module)
Given one camera frame and a goal, you can trace it to one motor command through
the VLA stack, and say where tokens end and continuous control begins.
`CHALLENGE.md`.

## Next
F6: the dissent - world models and the war on next-token prediction itself.
