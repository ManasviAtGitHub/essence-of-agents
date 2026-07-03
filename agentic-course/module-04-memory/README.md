# Module 4 - Memory & retrieval (deriving RAG)

The context is finite and the past falls off the edge. How does an agent remember?

## Question
You can only fit so much in the context window, and the model forgets everything
between calls (Module 0). So how does an agent "know" things it was never handed?

## Principle
Retrieval doesn't give the agent a memory -- it silently swaps *which agent you're
running* on this call. Memory is a **retrieve-and-insert** decision, not storage: you're
the librarian, choosing on each call which notes to put back on the desk (the context).
Retrieve + insert = RAG.

## See it (no key)
- `widgets/librarian/index.html` - a tiny knowledge base and a question. Toggle
  retrieval OFF/ON and press Run. OFF: the model has never heard of Project Heron and
  says so. ON: the relevant note lands on the desk and the answer becomes grounded and
  correct. **Same model, same question** - only the notes changed.
- `rag_offline.py` - the same idea in code, keyless: *real* keyword retrieval over a
  small KB, then a (scripted) answer from the retrieved notes.

## The aha
Toggle retrieval off and the same model becomes a different, ignorant agent; toggle it
on and it's "the agent that just read the launch plan." The model never changed -- only
the notes on the desk did, and that decided who answered.

## Honest note
The widget and `rag_offline.py` retrieve by **keyword overlap** - a stand-in for real
RAG, which uses embeddings (semantic similarity). The shape is identical: score docs
against the query, take the top-k, paste them in. `CHALLENGE.md` swaps in embeddings.

## Run
```
open widgets/librarian/index.html in a browser
python agentic-course/module-04-memory/rag_offline.py
```
