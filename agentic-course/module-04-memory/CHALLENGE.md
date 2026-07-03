# Coding Challenge - from keyword overlap to real retrieval

`rag_offline.py` retrieves by counting shared words. Real RAG scores by *meaning*.

## With embeddings (key or local embedder)
1. Embed each KB document once into a vector; cache it.
2. Embed the query; score docs by cosine similarity; take the top-k.
3. Paste the top-k into the context and let the model answer.

The tell: ask **"Who runs Project Heron?"**. Keyword retrieval misses (no shared word
with the "leads" note); embedding retrieval finds it - because "runs" and "leads" are
*close in meaning*. That gap is the whole reason real RAG uses embeddings.

## Episodic vs semantic
Add a second store: a log of past turns (episodic) alongside the facts (semantic). On
each query, retrieve from both. Which questions need *what happened* vs *what's true*?
That split is the start of real agent-memory design.

## Watch the context window fill
Keep appending retrieved notes turn after turn and you'll blow the window - which is
why summarization and context editing exist. Measure tokens with the harness and find
the turn where you'd need to compact. (That thread continues in Module 11.)

## Offline
Keyword retrieval (as in `rag_offline.py`) needs no key and is enough to wire up the
retrieve -> insert -> answer loop. Embeddings need a model or a local embedder; stub
the answer with a `FakeClient` while you build the scoring.
