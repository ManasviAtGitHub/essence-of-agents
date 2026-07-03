# Coding Challenge - solder on the feedback edge

## Wire failures back into evals
1. The harness already emits traces (`claude_harness/trace.py`). On a failure (an
   exception, a user thumbs-down, a guardrail trip), save the trace.
2. Turn that trace into an eval case: input + the expected (correct) behavior.
3. Append it to your eval set (as in `close_loop.py`).
4. Make CI re-run the eval set on every change and block regressions.

```python
from claude_harness import Agent, Trace
t = Trace()
try:
    out = Agent(tools=[...]).run(user_input, trace=t)
    if not ok(out):
        capture_failure({"input": user_input, "expected": "...", "trace": t.events})
except Exception:
    t.save("incident.trace.json")     # an incident is a future test
```

## The supporting details (pick one and add it)
- **Cost budget** - cap tokens per run; log spend per request.
- **Prompt caching** - keep the stable prefix first so it caches; measure the hit rate.
- **Streaming** - stream long outputs so requests don't time out.
- **Retries** - backoff on transient errors (the SDK already does some of this).

## The point
You've now built the loop in Module 0, and here you've closed it: users -> agent ->
traces -> evals -> fixes -> users. Everything else is tuning. Ship, watch, fold failures
back in.

## Offline
`close_loop.py` and the trace capture both run keyless. The only piece needing a real
model is the agent actually answering - everything around it you can build and test now.
