# S3 Challenge - Ship it

One file that runs everywhere and speaks your agent's API. Prove you get why
that matters.

## The file
1. Name the three things stacked inside a llamafile, and which one is memory-
   mapped (and why mmap makes a 4 GB file start almost instantly).
2. An APE is "a valid Windows .exe AND Linux ELF AND macOS Mach-O at once."
   In one sentence, why does that mean no install step - what work did the usual
   install (toolchain, drivers, package manager) do that the APE avoids?

## The loop-back (the point)
3. Your Track-2 agent runs against the Anthropic API in the cloud. To make it
   run against a local llamafile instead, what is the ONE thing you change - and
   what does NOT change? Why is "speaks the same API" the whole trick?
4. Give two real situations where running the model offline on one machine
   (llamafile) beats calling a cloud API - and one where it clearly loses.

## Place it
5. S1 read the engine, S2 made it fast, S3 shipped it. All three are about ONE
   instance on ONE machine. Which question have we NOT answered yet - and which
   module answers it? (Hint: how many people can this one file serve at once?)
6. llamafile is "fat" because the weights are inside. Using S2, name one thing
   you would do to the weights to make the file smaller before shipping it, and
   what it costs.

## Done when
You can explain, to someone who has never installed a model, why "here is one
file, double-click it" works on any OS - and why pointing your existing agent at
it (same API, base URL -> localhost) gives you an offline assistant.
