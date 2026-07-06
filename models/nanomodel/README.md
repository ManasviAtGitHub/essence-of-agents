# nanomodel - the models track, running

The course modules show you how a language model works, mechanism by mechanism.
This is the same thing as **runnable, from-scratch code** - the models-track
counterpart of `claude_harness` in the agents track. No numpy, no framework: a
hand-written autograd engine and a tiny transformer you can read top to bottom
and run in seconds.

> You watched the widgets compute a softmax, an attention weight, a BPE merge.
> Here those exact computations exist as real Python you execute and change.

## Run it

```bash
python bpe.py        # Module 1: train a BPE tokenizer, print the merges
python train.py      # the whole thing: train a tiny transformer, watch loss drop, generate
python train.py 2000 # train longer -> it reproduces the corpus verbatim
```

Everything is keyless and offline. `train.py` finishes in about a minute in pure
Python (it is deliberately tiny); crank the steps up for cleaner output.

## The files, and the modules they are

| File | What it is | Modules |
|------|------------|---------|
| `bpe.py` | byte-pair tokenizer: train / encode / decode | **M1** (tokens) |
| `autograd.py` | a scalar reverse-mode autograd engine (~90 lines) - how gradients work, by hand | the engine behind **M6/M7** |
| `model.py` | a tiny transformer: embed -> attention (causal) -> MLP -> logits -> sample loop | **M0, M1, M2, M4** |
| `train.py` | next-token loss + SGD; watch it learn, then generate | **M6** (training) |

Read them alongside the widgets:
- `NanoModel.forward` in `model.py` is the forward pass the modules draw - embed
  (M1), attention with the causal mask (M2), the MLP/FFN (M4), unembed to logits
  (M0).
- `NanoModel.generate` is Module 0's loop: forward -> softmax -> temperature ->
  the dice -> append -> repeat.
- `autograd.py`'s `backward()` is what makes training possible - the same idea a
  real optimizer uses, written so you can see every derivative.
- `train.py`'s `cross_entropy` + SGD loop is Module 6's "next-token loss", real.

## Honest notes

- It is a **toy**: char-level tokens (bpe.py has the real subword one), ~1k
  weights, one attention head, one block, a two-line corpus. It memorizes rather
  than generalizes - that is the point of a from-scratch sanity check.
- Real models are the **identical math** at a trillion-times scale, on GPUs, in
  numpy/torch for speed. Nothing here is different in kind - only in size.
- Pure Python and a scalar autograd are slow; that is the price of legibility.
  This is `agent.py`, not `claude_harness` - the version you learn from.
