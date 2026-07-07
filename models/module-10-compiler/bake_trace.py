"""Bake a REAL run of the compiler with a live model into a trace the widget can show.

This runs the actual front-end - a quantized small-instruct GGUF (MiniCPM-class)
via llama.cpp, grammar-constrained by grammar.gbnf - on the worked sentence, then
type-checks the result with the real verifier, and writes the outcome to
widgets/talk-to-compile/data/real-run.json (a "measured" trace beside the widget's
illustrative default).

It is OPT-IN and needs `llama-cpp-python` + a GGUF; it is not part of CI's keyless
gates. It runs anywhere with a compatible CPU wheel (e.g. a GitHub Actions
ubuntu-latest runner). Usage:

    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
    python bake_trace.py --model path/to/MiniCPM5-1B-Q4_K_M.gguf
    python bake_trace.py --model ... --sentence "search for umbrellas and email me the top result"
    python bake_trace.py --dry-run       # print the plan of action, load nothing
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from compiler import verify, EXAMPLE  # noqa: E402

OUT = os.path.join(HERE, "widgets", "talk-to-compile", "data", "real-run.json")
GBNF = os.path.join(HERE, "grammar.gbnf")

PROMPT = (
    "You compile a request into a tool-call plan.\n"
    "Tools: get_weather(city)->{{rain,temp}}; add_to_cart(item); search(query)->{{top}}; send_email(to).\n"
    'Example: n1 = get_weather(city="Paris")  then  n2 = if n1.rain: add_to_cart(item="umbrella")\n'
    "Request: {sentence}\n"
    "Plan:\n"
)


def parse_plan(text):
    """Parse the model's grammar-constrained text into IR statements."""
    ir = []
    for line in text.splitlines():
        m = re.match(r'\s*(n\d+)\s*=\s*(if\s+(n\d+)\.(\w+):\s*)?(\w+)\((\w+)="([^"]*)"\)', line)
        if m:
            ir.append({"id": m.group(1), "tool": m.group(5),
                       "args": {m.group(6): '"%s"' % m.group(7)},
                       "cond": [m.group(3), m.group(4)] if m.group(2) else None})
    return ir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", help="path to a GGUF model (quantized small-instruct)")
    ap.add_argument("--sentence", default=EXAMPLE)
    ap.add_argument("--dry-run", action="store_true", help="show the plan of action, load nothing")
    ap.add_argument("--stamp", default="", help="ISO timestamp to record (CI passes this in)")
    args = ap.parse_args()

    if args.dry_run:
        print("would load:", args.model or "<--model required>")
        print("would compile:", args.sentence)
        print("grammar:", GBNF)
        print("would write:", OUT)
        return 0
    if not args.model:
        print("error: --model PATH.gguf is required (or use --dry-run)", file=sys.stderr)
        return 2

    from llama_cpp import Llama, LlamaGrammar  # opt-in dependency
    grammar = LlamaGrammar.from_string(open(GBNF).read())
    llm = Llama(model_path=args.model, n_ctx=1024, n_threads=os.cpu_count() or 4, verbose=False)

    t = time.time()
    out = llm(PROMPT.format(sentence=args.sentence), grammar=grammar, max_tokens=96, temperature=0.0)
    secs = round(time.time() - t, 2)
    text = out["choices"][0]["text"].strip()

    ir = parse_plan(text)
    errs = verify(ir)
    trace = {
        "model": os.path.basename(args.model),
        "sentence": args.sentence,
        "output": text,
        "ir": ir,
        "verify": "PASS" if not errs else errs,
        "seconds": secs,
        "stamp": args.stamp,
        "note": "measured: this plan was produced by a real grammar-constrained model run",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2)
    print("wrote", OUT)
    print(json.dumps(trace, indent=2))
    return 0 if not errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
