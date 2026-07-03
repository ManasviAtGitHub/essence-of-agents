# Run-again widget - "Watch it run twice"

The Module 0 interactive knob: press Run a few times and watch the same prompt give
different answers, with the divergence point highlighted. Runs on **replay** (cached
data), so it needs **no API key, no server, and no build**.

## See it now (no key, no install)

Open `index.html` in any browser - double-click it, or:

- Windows: `start index.html`
- macOS: `open index.html`

Press **Run** repeatedly. Run 1 renders in full; later runs render dim where they
agree with Run 1 and bright from the word they diverge.

## Files

| File | What it is |
|------|------------|
| `index.html` | **Runnable now.** Self-contained vanilla JS + CSS; replay data embedded. |
| `trace.m0-nondeterminism.json` | The recorded-runs data format. `index.html` embeds a copy. |
| `record_trace.py` | Records real runs into the JSON (needs an API key). The sample data is hand-written until then. |

## Two sources, one renderer
Replay (cached, keyless, offline) and live (real API, needs a key + a proxy) emit the
same stream of text chunks; the renderer doesn't care which. Today `index.html` is
replay-only - the design's "go live" path is the stretch item.

## What it teaches
Non-determinism: identical input, different output. The locked constants on screen
make the point that the *only* thing changing is the model's sampling. ("Why does it
split?" is deliberately locked until Module 3, where the same widget reveals the
probability distribution at the divergence point.)
