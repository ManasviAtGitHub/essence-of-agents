"""Live smoke test for the NVIDIA adapter: same prompt twice -> two real answers.

Needs NVIDIA_API_KEY in the environment (or a gitignored .env).

    python production/providers/nvidia_smoke.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nvidia import NvidiaClient

client = NvidiaClient()  # default model; override NvidiaClient(model="...")
print("model:", client.model)
for i in (1, 2):
    r = client.messages.create(
        model=client.model, max_tokens=120,
        messages=[{"role": "user", "content": "In one vivid sentence, describe a city at dawn."}],
    )
    print(f"run {i}: " + "".join(b.text for b in r.content if b.type == "text").strip())
    print(f"  tokens: {r.usage.input_tokens} in / {r.usage.output_tokens} out")
