# S3 - Ship it

*Verified as of 2026-07. One file, every machine.*

You have a fast engine (S1-S2) and a weights file. Now the least glamorous,
most useful question in hosting: how do you deliver it so a person can actually
run it - no Python, no CUDA install, no setup? The 2026 answer collapses the
whole problem to a single file.

## Question
Running a model normally means assembling an environment: an engine, a
toolchain, drivers, libraries, and gigabytes of weights, each a chance to
break. How do you ship a model so "run it" is one step, on any machine?

## Principle
**Fold the engine and the weights into ONE portable file.** That is llamafile
(Mozilla): the llama.cpp engine (the grown-up descendant of S1's run.c) plus a
GGUF weights file (S2's int4), compiled by **Cosmopolitan Libc** into an **APE -
an Actually Portable Executable**. The same bytes are simultaneously a valid
Windows .exe, a Linux ELF, a macOS Mach-O, and a shell script. Copy it, run it -
that is the whole install - and it uses the GPU (Metal/CUDA) if present or the
CPU (S2's SIMD) if not.

And the part that closes the course: **llamafile serves the Anthropic Messages
API on localhost.** So the harness you built in course 1 - Claude Code, your
agent's loop - can point its base URL at this local file and run fully offline.
The API your agent speaks is now answered by a model on your own disk.

## Dated exhibits (rule 10)
- llamafile 0.10.0 (Mozilla, 2026): one stable APE with Metal (Dec 2025) and
  CUDA (Feb 2026) support, and an Anthropic-Messages-API-compatible local
  server - point Claude Code at it and run offline.
- Cosmopolitan Libc (Justine Tunney): the APE / polyglot-executable technology.
- llama.cpp + GGUF (ggml-org): the engine and weight format inside.

## See it (no key)
`widgets/ship-it/index.html`. **One file, every OS:** the friction of the usual
install; the engine + weights folding into one file; that file fanning out to
Windows / macOS / Linux / phone, each "runs, no install"; then the loop-back -
your Track-1 agent loop unplugging from the cloud API and plugging into the
local file. **What's inside:** the APE anatomy (polyglot header + engine +
mmap'd weights), the run sequence (mmap -> detect GPU -> S2 kernel -> S1 forward
pass), the localhost /v1/messages server, and the honest trade.

## The aha
Hosting does not require a datacenter or even an install - it can be one file
you email or run on a plane, and because it answers the same API, everything
from tracks 1-2 works against it unchanged.

## Done when
The learner can say what an APE is and why it runs everywhere without install,
and explain why a local Anthropic-API server means your existing agent runs
offline against a local model.

## Honest notes
- The file is fat (weights live inside, gigabytes) and a single binary is not as
  tuned as a hand-optimized datacenter stack. The win is zero-install
  portability, offline operation, and privacy - right for edge, demos, and
  privacy; the fleet (S5-S6) is right for serving many users.
- No live arithmetic in this module - it is a shipping/packaging story; the
  facts (Cosmopolitan APE, Anthropic-API server) are real and labeled.
