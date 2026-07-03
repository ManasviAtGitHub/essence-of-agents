"""A small, real vector store -- local n-gram embeddings + cosine similarity.

Keyless and DETERMINISTIC (stable hashing), so it runs with no model. This is genuine
vector retrieval (cosine over embeddings; handles typos/morphology better than exact
keyword match), but it is NOT true semantic search -- that needs an embedding model.
In production you'd swap embed() for a real embedding call and keep everything else.

Upgrades Module 4's keyword retrieval to vectors, still keyless.
"""
import hashlib
import math
import re


def _stable_hash(s: str) -> int:
    # builtin hash() is randomized per process; use a stable digest for reproducibility.
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def embed(text: str, dim: int = 512):
    v = [0.0] * dim
    for tok in re.findall(r"[a-z0-9]+", text.lower()):
        v[_stable_hash(tok) % dim] += 1.0
        for i in range(len(tok) - 2):  # char 3-grams -> robustness to morphology/typos
            v[_stable_hash(tok[i:i + 3]) % dim] += 0.5
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def cosine(a, b) -> float:
    return sum(x * y for x, y in zip(a, b))


class VectorStore:
    def __init__(self, dim: int = 512):
        self.dim = dim
        self.docs = []
        self._vecs = []

    def add(self, text: str, meta=None):
        self.docs.append({"text": text, "meta": meta})
        self._vecs.append(embed(text, self.dim))

    def search(self, query: str, k: int = 3):
        q = embed(query, self.dim)
        ranked = sorted(zip((cosine(q, v) for v in self._vecs), self.docs), key=lambda x: -x[0])
        return [{"score": round(s, 4), **d} for s, d in ranked[:k]]


def retrieve_tool(store: VectorStore, k: int = 2):
    """Wrap a VectorStore as an agent tool (the production version of Module 4's RAG)."""
    from claude_harness.tools import tool

    @tool
    def retrieve(query: str) -> str:
        """Retrieve the most relevant notes for a query.

        Args:
            query: what to search for
        """
        hits = store.search(query, k)
        return "\n".join(f"[{h['score']}] {h['text']}" for h in hits) or "(no matches)"

    return retrieve
