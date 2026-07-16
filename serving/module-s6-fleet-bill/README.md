# S6 - The fleet & the bill

*Verified as of 2026-07. Throughput vs latency vs cost.*

S5 got one GPU serving many users. But demand is not steady, and a fleet of
GPUs runs a meter every second it is powered on. This is the money module: what
it costs to serve your agent to a crowd, the two latencies users feel, and the
one number the whole course has been circling - dollars per million tokens.

## Question
What does it actually cost to serve your agent to a lot of people - and what are
the knobs that move that cost?

## Principle
**A fleet is replicas behind a queue, priced by GPU-hours, and it reduces to one
triangle.**
- **The meter.** You rent GPUs by the hour; the meter runs whether they are busy
  or idle. Demand spikes and lulls, so fleets AUTOSCALE - add replicas on the
  rise, drop them on the fall - but cold starts lag (a new GPU must load S0's
  pile first), so you scale ahead and carry some idle. RESERVED GPUs are pricey
  but yours; SPOT are cheap but reclaimable.
- **Two latencies.** Users feel TTFT (time to first token = prefill, compute-
  bound, M3/S0 - the wait) and TPOT (time per output token = decode, memory-
  bound - the pace). Because prefill and decode stress opposite hardware, 2025-26
  fleets DISAGGREGATE them into separate pools, each tuned to its bottleneck.
- **The bill.** GPU-hours x price / tokens served = $/1M tokens. Every serving
  trick from this track - quantize (S2), batch and page (S5), right-size the
  hardware (S0) - raises tokens/sec, which pushes that number down. And it all
  trades off in a triangle: throughput vs latency vs cost - you pick your point.

**This is your agent's bill.** Every model call your Track-1 loop makes and
every token your Track-2 service streams is priced by this fleet (closing the
hook S0 opened).

## Dated exhibits (rule 10, illustrative - rule 11)
- Prefill/decode disaggregation (2025-26 serving stacks).
- Autoscaling, spot vs reserved GPU pricing; ~$3/GPU-hour and ~2,500 tok/s are
  round illustrative figures.

## See it (no key)
`widgets/fleet-bill/index.html`. **The fleet:** a live demand curve against the
fleet's capacity line, a GPU rack lighting busy/idle/off as it autoscales, and a
meter ticking dollars every second - watch the queue back up when demand crosses
capacity. **The bill:** TTFT vs TPOT as a wait-then-stream bar; prefill/decode
disaggregation into two pools; the $/1M-tokens arithmetic computed step by step;
and the throughput/latency/cost triangle every module in this track is a lever on.

## The aha
Serving reduces to a triangle - throughput, latency, cost - and the cost corner
is literally your agent's bill. Every trick you learned pushes it down.

## Done when
The learner can name TTFT vs TPOT, explain why prefill and decode get
disaggregated, compute a rough $/1M tokens from users/tokens/tok-s/price, and say
which lever each earlier module pulls on the triangle.

## Honest notes
- All prices, tok/s, and GPU-hour figures are round and illustrative (rule 11);
  the $/1M-token arithmetic is computed live from them so you can see the shape,
  not a quoted price.
- The meter, rack, and demand curve are a simulation of fleet behavior; real
  autoscaling adds SLAs, load balancers, and multi-region routing on top.
