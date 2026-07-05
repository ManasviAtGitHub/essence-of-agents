# By hand - compute the distribution yourself

The module is "done" when you can do the sampler's job with a calculator.

## 1. Softmax by hand
A model produces these logits for the next token (top 5 shown):

| token   | z    |
|---------|------|
| " blue" | 6.0  |
| " red"  | 4.5  |
| " a"    | 3.0  |
| " very" | 2.0  |
| " not"  | 1.0  |

At **T = 1**, compute `p_i = e^(z_i) / sum_j e^(z_j)` for all five.
(Work: e^6.0 = 403.4, e^4.5 = 90.0, e^3.0 = 20.1, e^2.0 = 7.4, e^1.0 = 2.7;
sum = 523.6. Check: " blue" should come out ~0.77.)

## 2. Temperature
Recompute at **T = 0.5** (divide each z by 0.5 first) and at **T = 2**.
Before computing, predict: which way does " blue"'s share move in each case?
Verify your three distributions against the widget's mechanism act 2 - type
nothing, just drag T and compare shapes.

## 3. Top-p
At T = 1, apply **top-p = 0.90**: sort by p, keep the smallest set whose
cumulative probability reaches 0.90, set the rest to zero, renormalize the
kept ones. How many tokens survive? What is " red"'s renormalized p?

## 4. The draw
Using your T = 1, top-p = 0.90 distribution, lay the kept tokens on a number
line from 0 to 1 (cumulative). Which token does r = 0.85 select? r = 0.05?

## Stretch
- Implement `sample(logits, T, top_p)` in any language (~15 lines). Run it
  10,000 times on the logits above and check the empirical frequencies match
  your hand-computed p's.
- Explain in two sentences why T = 0 plus the prompt "and so on" can loop
  forever, and why T = 0.8 eventually escapes. (The widget's mechanism act 3
  is the picture.)
