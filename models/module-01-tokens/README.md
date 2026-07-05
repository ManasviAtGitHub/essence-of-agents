# Module 1 - Tokens: what the model actually sees

Ask a model to count the r's in "strawberry" and it often fails. Not because it
is stupid - because it never saw the letters.

## Question
What does the model actually receive when you type - and why do its strangest
failures trace back to that step?

## Principle
Text is chopped into **tokens** from a fixed menu (the vocabulary, ~100k-128k
entries) learned by **byte-pair encoding**: start from characters, repeatedly
merge the most frequent adjacent pair. Common words become single atoms (their
letters invisible); rare words split into subword pieces; the cost is uneven
(prose ~4 chars/token, digits and rare scripts far worse). Each token is then
an integer ID - and an **embedding matrix** turns that ID into a vector of
thousands of learned numbers. That vector is **h**, the thing every later
module operates on.

## See it (no key)
`widgets/token-lens/index.html` - two passes:
- **intuition (9 steps):** the strawberry puzzle, tokens-with-IDs, atoms vs
  subword pieces, why the menu design won, the uneven tax, and the family of
  "dumb" failures that are really tokenizer failures.
- **mechanism (19 steps, 3 acts):** act 1 TRAINS a real BPE vocabulary on
  screen - pair counts computed live over a toy corpus, five merge rounds,
  vocabulary growing. Act 2 encodes new words with the learned merges (and a
  sandbox tokenizes anything you type), then the tax: digits shattering,
  9.11-vs-9.9. Act 3 is the bridge: ID -> embedding row -> a vector where
  direction = meaning - the birth of h (and 0.92B of "always-on" parameters,
  computed).

## The aha
The model is brilliant in a language whose letters it cannot see. And its real
input was never words - it was a short list of learned coordinates.

## Honest notes
- The BPE trainer and sandbox are REAL - counts and merges computed live on a
  toy corpus. Real tokenizers run the same loop ~100k+ times on web-scale text.
- Real-tokenizer splits quoted for big vocabs ("strawberry" as one token,
  digit chunking) are typical behavior, labeled illustrative.
- The 2D embedding scatter is a shadow of thousands of dimensions.

## Done when (the bar for this module)
You can run three BPE merge rounds by hand on a toy corpus and predict how a
new word will encode. `CHALLENGE.md` is that exercise.

## Next
Module 2: the vectors are born, but they are islands - attention is how
meaning moves between them.
