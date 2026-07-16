# S6 Challenge - The fleet & the bill

The meter is running. Prove you can read the bill and the triangle.

## The two latencies
1. Define TTFT and TPOT in your own words, and say which phase (prefill or
   decode) and which bottleneck (compute or memory) each comes from. Which one
   does a user notice as "it's thinking", and which as "it's typing"?
2. Why does it help to run prefill on one kind of machine and decode on another,
   instead of both on one? (Connect to S0: what is each phase bound by?)

## The bill (do the arithmetic)
3. 2,000 users each ask for 800 tokens. Your GPU does ~2,000 tok/s and rents for
   $2.40/hour. Compute the total tokens, the GPU-seconds, the dollars, and the
   $/1M tokens. Show the steps.
4. You switch the model from fp16 to int4 (S2), doubling tok/s. Redo the
   $/1M-tokens number. Which corner of the triangle did you just move, and did
   it cost you anything?
5. Your fleet sits at 30% average utilization because you provision for the 9am
   peak. Name two levers from S5/S6 that would raise utilization (and lower cost)
   without dropping users at peak.

## Close the loop
6. S0 opened with "why is your agent slow and expensive?" Answer it now, in two
   sentences, using the whole track: what makes a call slow (S0-S2), and what
   makes serving your agent to a crowd cost what it costs (S5-S6)?

## Done when
You can compute a $/1M-tokens figure from first inputs, explain the throughput/
latency/cost triangle, and trace your Track-1 agent's per-call cost back to the
fleet - naming which serving trick pushes it down.
