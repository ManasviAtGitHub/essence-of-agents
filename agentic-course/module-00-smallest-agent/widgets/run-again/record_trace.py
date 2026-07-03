# Record the cached runs the "watch it run twice" widget replays.
#
# Runs the prompt N times, capturing each streamed chunk with its timing, and writes
# trace.m0-nondeterminism.json. No temperature is set (it isn't settable on
# claude-opus-4-8) - the default sampling is exactly what produces the divergence
# the widget teaches.
import datetime
import json
import time

import anthropic

client = anthropic.Anthropic()

MODEL = "claude-opus-4-8"
SYSTEM = "Answer in exactly two sentences. No preamble."
PROMPT = "Read your own source and explain how you work, in two sentences."
N_RUNS = 10


def record_run(run_id):
    chunks, full, t0 = [], [], time.perf_counter()
    with client.messages.stream(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM,
        messages=[{"role": "user", "content": PROMPT}],
    ) as stream:
        for text in stream.text_stream:  # streamed text deltas
            chunks.append(
                {"t_ms": round((time.perf_counter() - t0) * 1000), "text": text}
            )
            full.append(text)
    return {"run_id": run_id, "text": "".join(full), "chunks": chunks}


trace = {
    "id": "m0-nondeterminism",
    "recorded_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "input": {"model": MODEL, "system": SYSTEM, "prompt": PROMPT, "max_tokens": 400},
    "runs": [record_run(i + 1) for i in range(N_RUNS)],
}

with open("trace.m0-nondeterminism.json", "w", encoding="utf-8") as f:
    json.dump(trace, f, ensure_ascii=False, indent=2)

print(f"Recorded {N_RUNS} runs -> trace.m0-nondeterminism.json")
