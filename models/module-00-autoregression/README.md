# Module 0 - Autoregression: the loop inside

Course 1 wrapped a while-loop AROUND the model. This track opens the model, and
the first thing inside is... another loop.

## Question
You have watched answers stream in word by word. What is actually looping?

## Principle
Generation is a loop: **context -> stack -> distribution -> sample -> append ->
repeat.** One forward pass produces one distribution over the entire vocabulary;
one token is drawn from it; the drawn token is appended to the context and the
model runs again - on its own output. There is no plan and no sentence-level
choice. There is only the next token, chosen ~40 times per sentence.

## See it (no key)
`widgets/next-token-loop/index.html` - two passes over one stage:
- **intuition (8 steps):** the story. "The capital of France is" -> ` Paris` ->
  `.` -> `<end>`, one drawn token at a time, with the append edge - the loop -
  lit up every time output becomes input.
- **mechanism (20 steps, 3 acts):** the machinery. Act 1: tokens -> IDs ->
  embeddings -> 32 layers -> logits -> softmax, with the arithmetic in a live
  table. Act 2: temperature and top-p as real knobs - drag T and every number
  recomputes from `p_i = e^(z_i/T) / sum_j e^(z_j/T)`. Act 3: why identical
  prompts diverge (two draws, one fork, compounding contexts), then break it on
  purpose: greedy decoding walks a repetition cycle ("and so on and so on and")
  and a little temperature breaks the spell.

## The aha
The model never chooses a sentence. It chooses ONE token, again and again - and
because each chosen token feeds back into the context, one lucky or unlucky draw
changes every distribution after it. Course 1's "run it twice, get two answers"
widget is this mechanism, seen from outside.

## Honest note
The six candidate logits on screen are hand-authored (running a real model needs
a real model - this track stays keyless). Everything DOWNSTREAM of them is
computed live in the page: the softmax, the temperature scaling, the top-p cut,
the renormalization, the draw. Check any row with a calculator - that is the
point.

## Done when (the bar for this module)
Given five logits and a temperature, you can compute the sampling distribution
by hand. `CHALLENGE.md` is exactly that exercise.

## Next
Module 1 asks what those "tokens" actually are - and why the model cannot see
the letters inside them.
