# By hand - diagnose the stage

## 1. Which stage?
For each behavior change, name the training stage most likely responsible, and
say in one line what that stage's LOSS sees:
- a) The model stopped continuing your text and started answering questions.
- b) The model began refusing to help with clearly harmful requests.
- c) The model started writing "<think>...</think>" before hard answers.
- d) The model learned that Mount Everest is the tallest mountain.
- e) The model's replies became more nicely formatted with bullet points.

## 2. The stop token
Two distributions over the token after "...is Paris":
base = {" The": logit 4.6, ".": 4.2, "<end>": 1.0, ...}
SFT  = {" The": 1.2, ".": 4.3, "<end>": 6.0, ...}
- Softmax the <end> entry in each (you may ignore the "..." tail; use just the
  three shown for a rough number). Which way did <end>'s probability move?
- In one sentence: what did SFT teach here, and what did it NOT teach?

## 3. The data funnel
Order these by dataset size, largest first, and say WHY the order is that way:
preference pairs, pretraining tokens, SFT dialogues, RL problems.
(Hint: what makes a training label cheap vs expensive to produce?)

## 4. Reward hacking
A reasoning-RL setup rewards the model when a verifier marks its proof
"correct". The verifier only checks that the output ends in "QED".
- What will the model learn to do?
- Connect this to course 1, Module 6's thesis in one sentence.

## Stretch
- Why can pretraining use 14.8T tokens while SFT uses far fewer? (Think about
  where each stage's training labels come from - who has to make them.)
- DPO optimizes a chosen/rejected pair directly; classic RLHF trains a reward
  model first, then does RL against it. What does DPO save, and what might a
  separate reward model still buy you?
