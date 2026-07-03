# Production track

The teaching course (../agentic-course) keeps the agent tiny so the ideas stay visible.
This track is the other end of the same loop: the harness *around* the model that a real
deployment needs. Same loop as Module 0 -- wrapped in retries, streaming, cost accounting,
guardrails, budgets, observability, persistence, routing, and a CI gate.

Anthropic stays the canonical provider; NVIDIA is wired in as an optional *live* provider
so the whole thing can run against a real model with no Anthropic key.

## What's here

| File | What it is |
|---|---|
| `agent_pro.py` | Production agent core: retries+backoff, streaming-capable, cost/usage accounting, tool **permission policy + approval gate**, input **guardrail**, spend **budget**, structured events. |
| `providers/nvidia.py` | OpenAI-compatible **NVIDIA adapter** in the harness client shape -- full tool-call translation, so the entire tool-using loop runs live. Key from `.env`/env, never logged. |
| `observability.py` | Event stream -> metrics + OTel-style spans. |
| `persistence.py` | `SessionStore` -- durable JSON session records (the seam for failure-> eval-case). |
| `router.py` | Model **routing + fallback** (cheap vs reasoning; fall back on error/refusal). |
| `run_agent.py` | Reference **deployable CLI** that composes all of the above. |
| `eval_gate.py` | CI **regression gate** -- exits non-zero if the eval pass-rate drops. |
| `server.py` | Deployable **HTTP server** (`POST /chat`, `GET /health`), stdlib only. |
| `vectorstore.py` | Real **vector store** (local n-gram embeddings + cosine) + a `retrieve` tool. |
| `sandbox.py` | Subprocess **code-exec sandbox** (timeout + `-I`) + a `run_python` tool. |
| `test_agent_pro.py`, `test_production.py`, `test_production_extra.py` | Offline tests (no key) for every piece. |
| `../.github/workflows/ci.yml` | Runs all tests + the eval gate on every push. |

## The teaching module -> production mapping

| Module | Production concern (and where it lives here) |
|---|---|
| 0 loop / 2 reason+act | the loop, retries, streaming, step/turn budgets -- `agent_pro` |
| 1 tools | validated tool specs, typed errors, **least privilege** via the permission policy -- `agent_pro` |
| 3 context | token/cost accounting now; prompt caching + compaction are the next add -- `agent_pro` |
| 4 memory | durable records -- `persistence` (vector store is the next add) |
| 5 planning | per-step retries + (next) checkpoint/resume |
| 6 verification | the eval gate + (next) sandboxed code-exec -- `eval_gate` |
| 7 reasoning models | **model routing** cheap<->reasoning -- `router` |
| 8 multi-agent | (next) worker pools / concurrency on top of the loop |
| 9 security | **guardrail** + **approval gate** + secrets in `.env` (gitignored) -- `agent_pro` |
| 10 evaluation | **regression gate** in CI -- `eval_gate` |
| 11 shipping | retries, cost, observability, persistence, **fallback**, the CLI, CI -- all of the above |

## Run it

Offline (no key):
```
python production/run_agent.py --provider fake
python production/test_agent_pro.py
python production/test_production.py
python production/eval_gate.py
```

Live (reads NVIDIA_API_KEY from a gitignored `.env`):
```
python production/providers/tool_live_smoke.py            # full tool loop, live
python production/run_agent.py --provider nvidia --task "What is 17*23? Use the calculator."
```

## Honest notes
- **Keys:** never commit them. `.env` is gitignored. The NVIDIA key used in development was
  pasted into a chat and should be **rotated** at build.nvidia.com.
- **What's real vs next:** the core, the live NVIDIA adapter (text + tools), observability,
  persistence, routing/fallback, the CLI, the CI gate, **prompt-caching wiring, local
  compaction, a vector store, a code-exec sandbox, and the HTTP server** are all built and
  offline-tested. For a *hardened* deployment, still add: true container isolation for the
  sandbox, real embedding-model retrieval (swap `vectorstore.embed`), the server-side
  compaction beta, and auth + rate-limiting on the server.
- **Cost numbers** use Anthropic per-token prices; for NVIDIA models cost shows 0 (no price
  in the table) -- token counts are still real.
