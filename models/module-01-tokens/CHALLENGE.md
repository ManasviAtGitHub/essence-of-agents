# By hand - train a tokenizer on paper

## 1. Three merge rounds
Corpus (word x count):

    hug x 10, pug x 5, pun x 12, bun x 4, hugs x 5

Split every word into characters, then:
- Round 1: count all adjacent pairs. Which pair wins? Merge it everywhere.
- Round 2: recount (new pairs exist now). Merge the winner.
- Round 3: once more.
Write the vocabulary you have built (characters + 3 merges).

## 2. Encode a new word
Using YOUR merges, in training order, encode: "hug", "pugs", "bug".
Which one still ends as raw characters, and why?

## 3. Predict the seams
Without a tokenizer in front of you, predict which of these a 128k-vocab
model likely sees as ONE token vs several, and why:
"the", "strawberry", "strawberries", "3.14159", "defenestration",
"    return x" (code with indent).
Check your instincts against the widget's act 2.

## 4. The embedding bill
A model has |V| = 128,000 tokens and d = 7,168.
- How many parameters is the embedding matrix?
- The output head (logits layer) is d x |V| again - unless it is "tied"
  (shared with the embedding). How much does tying save?

## Stretch
- Implement the pair-count + merge loop in any language (~25 lines). Train on
  a paragraph of your own text with a 50-merge budget and inspect the menu it
  invents. Where did it spend the budget?
- Explain in two sentences why "9.11 > 9.9" is a harder question for a model
  than "911 > 99".
