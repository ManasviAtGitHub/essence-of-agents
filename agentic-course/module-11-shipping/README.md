# Module 11 - Shipping: close the loop

What's the distance from "works on my machine" to "people depend on it"?

## Question
The agent works in your tests. What's actually left before real users can rely on it -
and what keeps it from rotting once they do?

## Principle
Production is the dev loop **plus one edge**: every failure in the wild becomes a row in
your Module 10 eval set. That single feedback edge is the spine; cost budgets, caching,
streaming, retries, and tracing are all *supporting details* that hang off it.

## See it (no key)
- `widgets/feedback-loop/index.html` - press "Capture a prod failure" and watch it flow:
  user bug -> trace -> new eval case -> fix + green -> redeploy -> back to users. The eval set
  grows by one each time; the agent can never regress on that case again.
- `close_loop.py` - the edge in code: a captured failure is appended to `evalset.json`.
  Run it a few times and watch the regression set grow.

## The aha
A production agent is the Module 0 loop with a feedback edge soldered on: it learns from
its own logs. The circle closes - Module 11 hands you back to Module 0.

## The supporting cast (briefly)
- **Observability** - traces (the harness already emits them) are how you *see* failures.
- **Cost & latency** - budgets, prompt caching (context *order* is cost - Module 3),
  streaming for long outputs.
- **Reliability** - retries/backoff, the guardrails and approval gates from Module 9.

## Honest note
The hard part of shipping isn't any one of these - it's the discipline of routing real
failures back into evals instead of patching them ad hoc. The model is a small part of a
shipped system; this loop -- traces, evals, fixes -- is most of the rest.

## Run
```
python agentic-course/module-11-shipping/close_loop.py
```
or open `widgets/feedback-loop/index.html`.
