# Capstone storyboard - the natural-language compiler

The models-track capstone. Thesis: **a compiler you can talk to = a stochastic
front-end (the LLM) bolted to a deterministic, verifiable backend, with a loop
closing the gap.** Spined on constrained decoding - the one inside-the-model
mechanism - so it belongs to the models track, and it unifies both courses:
natural language COMPILES into the agent loop you hand-built in course 1.

## The worked example (one thread)
NL: "get the weather in Paris, and if it's raining add an umbrella to my cart"
Compiles to a typed tool-call DAG (the IR):
```
n1 = get_weather(city="Paris")
n2 = if n1.rain: add_to_cart(item="umbrella")
```
Tool catalog (fixed): get_weather(city)->{rain,temp}, add_to_cart(item),
search(query)->{top}, send_email(to). Grammar allows only known tools, valid
arg keys, resolvable refs. Verifier: tools exist, arg keys in schema, refs
defined-before-use, DAG acyclic.

## The money shot (Act 1)
Token by token, the M0 probability bars appear over the candidates; the GRAMMAR
greys out every illegal next-token and the model samples from the renormalized
legal set. Each decode step enforces a DIFFERENT static rule at decode time:
tool catalog -> arg schema -> literal type -> scope (n1 defined, n2 not) ->
return-field schema -> catalog again. Softmax + masked renormalization are
computed live; the raw logits are illustrative (keyless), same honesty split
as Module 0.

## Acts
- Intuition (~7): naive model is unreliable -> the 3 disciplines (grammar,
  verifier, determinism) -> aha: stochastic front-end + deterministic verified
  backend.
- Act 1 - decode under grammar (money shot; live mask + renorm).
- Act 2 - verify + repair (M7): typecheck the DAG -> PASS; a broken ref -> loud
  FAIL -> repair loop; temp-0 determinism.
- Act 3 - break it + cost ledger: toggles, each firing one prior module.

## The genuine-capstone proof (toggle -> module)
- grammar OFF -> illegal token slips -> invalid IR
- temperature UP -> same sentence, two compiles (M0)
- verifier weak -> wrong-arg IR passes silently (M7)
- base (not instruction-tuned) driver -> valid-but-nonsense IR (M6)
- cost ledger -> KV cache (M3), experts (M4), 4-bit driver size (M8, computed)

## Cast
Cortex = the stochastic front-end (proposes tokens, sometimes wants an illegal
one and the grammar reins it in). Bit = the grammar + verifier (holds the rules,
checks, rejects loud).

## Driver (the real LLM)
Pluggable interface; default a quantized small-instruct GGUF (MiniCPM-class),
grammar-constrained via GBNF - the grammar GUARANTEES valid structure even from
a ~1B model. Runs local + in CI, never in the keyless browser. Named only in
the Python/README layer (de-branding rule). Widget default = live-computed
grammar over illustrative logits; a later phase bakes REAL driver traces as a
"measured" tab, plus an opt-in live mode.

## Honest caveat
The grammar guarantees valid STRUCTURE, not correct MEANING - a small model can
compile a sentence into something syntactically perfect but semantically off.
Honest-toy quality, same framing as nanomodel.
