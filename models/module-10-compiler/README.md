# Capstone - The compiler you can talk to

If natural language is how we now drive computers, the honest question is: can a
stochastic model behave like a **compiler** - turn a spec into something that
runs, exactly and repeatably, and fail loudly when it can't? This capstone
builds one, and in doing so uses every module in the track.

## Question
A compiler is deterministic, type-checked, and errors out on bad input. An LLM
is stochastic and speaks fuzzy English. How do you get compiler behavior out of
it - and does everything you learned actually lead here?

## Principle
An "LLM compiler" is not one magic model. It is a **stochastic front-end** (the
model, lowering natural language into a typed plan) bolted to a **deterministic,
verified backend**, with a repair loop closing the gap:

- **Front-end = constrained decoding.** At each step the model produces a
  distribution over next tokens (Module 0). A **grammar** masks every token that
  would make the plan invalid, and the model samples from the *renormalized
  legal set*. It literally cannot emit a wrong tool name, an unknown arg, or a
  reference to a result that does not exist - the check happens at the sampler,
  before the token is chosen.
- **IR = a typed tool-call plan (DAG).** The same agent loop you hand-built in
  course 1 - now the *output* of compiling a sentence. Deterministic,
  inspectable, re-runnable.
- **Backend = a verifier.** The finished plan is type-checked (tools exist, args
  match the schema, refs resolve, graph acyclic) and **fails loudly** - a
  compile error, not a plausible wrong answer that runs and misbehaves. On
  failure the compiler loops and re-decodes. This is Module 7's lesson: the
  system is only as good as its verifier.
- **Determinism.** Temperature 0 makes the front-end take the argmax of the
  legal set, so the same sentence lowers to the same plan, byte-identical.

## See it (no key)
`widgets/compile-live/index.html` - the INTERACTIVE view (built on p5). A
"meet the pieces" beat introduces reader / rules / plan / checker in plain
words, then: click a request and watch it compile live - candidate words fly
at the rules gate, disallowed ones bounce off, the winner snaps into a plan
graph, the checker confirms it, and a cost ledger prices the compile (driver
size computed from params x bits/8, KV cache, experts - Modules 8/3/4). Then
BREAK it, one lever per prior module: rules off (invalid plan - M0's unmasked
sampler), temperature up (same sentence, two different compiles - M0), checker
weak (a wrong plan ships silently - M7), untrained reader (legal syntax,
nonsense plan - M6). Run the verified plan and watch it execute.

`widgets/architecture/index.html` - the WIRING diagram (built on p5): the same
pieces as an architecture graph - click any piece to light up its connections,
and open the reader to see the entire models track inside it (tokens -> layers
-> logits -> the sampler, where the rules plug in). Surfaces the two structural
ahas the process view hides: one tool catalog defines BOTH the rules and the
checker (front and back, same schema), and the checker wires back to the reader
to repair.

## The aha
The whole course was building the front-end. A compiler is what you do with it:
constrain the sampler with a grammar, check the output with a verifier, pin the
temperature - and a stochastic model becomes a machine that compiles language
into verified, runnable plans.

## The genuine-capstone test
Every break-toggle is powered by an earlier module - if you can break it along
each module's axis, the course genuinely led here: grammar/determinism = Module
0's sampler; tokens = Module 1; the front-end follows a spec at all because of
Module 6's instruction-tuning; it runs locally because it is small and quantized
(Module 8); its running cost is Modules 3/4; the verifier is Module 7.

## Honest notes
- The grammar mask and the renormalization over the legal set are **computed
  live** from a real tool schema; the verifier runs **real** static checks. The
  raw per-token logits are illustrative (keyless), exactly the split used in
  Module 0.
- The grammar guarantees valid **structure, not correct meaning** - a small
  model can compile a sentence into something syntactically perfect but
  semantically off. Honest-toy quality.

## Done when (the bar for this module)
Given a tool schema and a partial plan, you can list which next tokens are legal
(and why the rest are masked), and hand-run the verifier on a small plan.
`CHALLENGE.md` is that exercise.

## Run it in code
`compiler.py` is the whole pipeline, real and runnable:
```bash
python models/module-10-compiler/compiler.py
python models/module-10-compiler/compiler.py "search for umbrellas and email me"
```
The **grammar** (legal-option computation) and the **verifier** (static checks)
are real; the front-end model is a swappable **driver**. The default drivers are
keyless and deterministic - a scripted stand-in and a tiny keyword parser, the
FakeClient analog - so it runs in CI with no download (`tests/test_compiler.py`).
The demo prints the compiled plan, then the thesis in one line: grammar ON
(constrained) always verifies; grammar OFF (adversarial) produces a plan the
verifier catches.

**Run it with a real model (opt-in).** Plug in `LlamaDriver` - a quantized
small-instruct GGUF (MiniCPM-class) via `llama-cpp-python`. The grammar
guarantees valid structure even from a ~1B model, which is exactly why a tiny
local model is enough. `grammar.gbnf` is the same grammar in llama.cpp's native
GBNF format for full token-level constraint. (The keyword parser is honest-toy
quality - it turns simple sentences into plans; a real model understands
language properly.)

**Bake a real trace.** `bake_trace.py` runs the real grammar-constrained model on
the worked sentence and writes `widgets/talk-to-compile/data/real-run.json` - a
measured trace beside the widget's illustrative default:
```bash
python models/module-10-compiler/bake_trace.py --model MiniCPM5-1B-Q4_K_M.gguf
python models/module-10-compiler/bake_trace.py --dry-run   # no model, just the plan of action
```
The GitHub Actions job `.github/workflows/bake-trace.yml` (manual dispatch) does
this on a runner - installs the CPU wheel, downloads a MiniCPM GGUF, runs
`bake_trace.py`, and uploads the trace as an artifact. Note: the prebuilt
llama.cpp CPU wheel needs a CPU with AVX2 (fine on GitHub runners and modern
machines; an older/virtualized CPU may raise an illegal-instruction error on
model load - rebuild the wheel from source for that CPU if so).

Phase next: wire the widget to show the baked "measured" trace beside the
illustrative one, plus an opt-in live mode.
