"""Offline RAG: real keyword retrieval over a tiny KB + a scripted answer (no key).

Retrieval here is REAL Python. Only the model's final answer is faked (FakeClient),
so the whole retrieve -> assemble-context -> answer loop runs with no key.

    python agentic-course/module-04-memory/rag_offline.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from claude_harness import Agent
from claude_harness.testing import FakeClient, reply, text_block

KB = [
    ("Launch plan", "Project Heron's launch date is March 3, 2027."),
    ("Team roster", "Dana Okafor leads Project Heron."),
    ("Budget memo", "Project Heron's budget is $2.4M for FY27."),
    ("Cafeteria menu", "Tuesday's lunch special is mushroom risotto."),
]
STOP = set("a an the is are of do does what when who whose how to for in on it s much".split())


def toks(s):
    return [w for w in re.sub(r"[^a-z0-9$ ]", " ", s.lower()).split() if w and w not in STOP]


def retrieve(query, k=2):
    """Score each doc by shared (non-stopword) tokens with the query; return top-k."""
    q = set(toks(query))
    scored = []
    for title, text in KB:
        score = len(q & set(toks(title + " " + text)))
        if score:
            scored.append((score, title, text))
    scored.sort(reverse=True)
    return scored[:k]


query = "When does Project Heron launch?"
hits = retrieve(query)

print("RETRIEVED (the librarian's picks):")
for score, title, text in hits:
    print(f"  (match {score}) {title}: {text}")

context = "\n".join(f"[{title}] {text}" for _, title, text in hits)

# The model would now answer FROM the retrieved notes. Faked here so it runs keyless;
# with a real key, drop the client and the harness calls the model for real.
client = FakeClient([reply(text_block("Project Heron launches on March 3, 2027."))])
agent = Agent(client=client)
prompt = f"Use ONLY these notes to answer.\n{context}\n\nQ: {query}"

print("\nANSWER:", agent.run(prompt))
print("\n(Change `query` to a question whose note isn't retrieved, and the grounded "
      "answer disappears - retrieval decided which agent you were running.)")
