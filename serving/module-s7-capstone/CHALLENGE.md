# S7 Challenge - Host it yourself

The console is yours. These are design tasks - hit each target with the dials,
and be able to say WHY.

## Hit the target
1. **Fits in a browser tab, no server.** Set the dials so the readout says the
   model fits in a tab AND the stack settles as WebLLM/transformers.js. Which
   two dials did the work, and which module (S-number) is that?
2. **Cheapest tokens at scale.** Serve 10k users at the lowest $/1M tokens you
   can reach. Which dials did you move, and which two levers (throughput? the
   fleet?) drove the price down? Name the modules.
3. **A private offline assistant on a laptop, no GPU.** What backend must you
   pick, what does it cost you in tok/s, and which real stack (S3?) does it
   settle to?

## Read the real number
4. Press "run the real engine" and note the measured tok/s on YOUR machine. Is
   it the single-stream number or the served number in the panel? Why is a real
   measurement the honest anchor, and what is a projection (be specific about
   which numbers on screen are which)?
5. Change MODEL from 0.5B to 7B at the same bits. Explain, using S0/S2, why the
   pile grows, the tok/s falls, and the $/1M tokens rises - all from one dial.

## Close the whole track
6. In five short lines - one per verb - trace a token from weights on disk to a
   paid answer: READ (S1), FAST (S2), SHIP (S3), RUN (S4), RACK (S5-S6). For each,
   name the one thing that verb does to the token's cost or speed.

## Done when
You can drive the console to any of three targets (fits-in-a-tab, cheapest-at-
scale, offline-on-a-laptop), point to which reported number is real vs projected,
and narrate the whole read-fast-ship-run-rack loop from memory.
