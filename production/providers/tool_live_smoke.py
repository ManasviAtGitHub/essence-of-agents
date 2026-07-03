"""Live test of the FULL tool-using loop against NVIDIA (needs NVIDIA_API_KEY in .env).

ProAgent + a real calculate tool + an NVIDIA-hosted model: the model decides to call the
tool, agent_pro runs it, feeds the result back, the model answers. Real tool loop, live.

    python production/providers/tool_live_smoke.py [model]
"""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(_here)))  # repo root -> claude_harness
sys.path.insert(0, os.path.dirname(_here))                   # production -> agent_pro
sys.path.insert(0, _here)                                    # providers -> nvidia

from agent_pro import ProAgent
from claude_harness.builtins import calculate
from nvidia import NvidiaClient

MODEL = sys.argv[1] if len(sys.argv) > 1 else "meta/llama-3.1-8b-instruct"
agent = ProAgent(tools=[calculate], model=MODEL, client=NvidiaClient(model=MODEL), max_steps=6)

result = agent.run("What is 2**10 + 5? Use the calculator tool, then state the number.")

print("model:", MODEL)
print("ANSWER:", result.text)
print(f"steps: {result.usage.steps}  tokens: {result.usage.input_tokens} in / {result.usage.output_tokens} out")
print("trace:")
for e in result.events:
    print("  ", e["kind"], e.get("tool", ""), e.get("args", ""))
