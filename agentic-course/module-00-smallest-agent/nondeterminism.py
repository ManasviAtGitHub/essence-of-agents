# Beat 5, experiment 2 - the model isn't deterministic.
#
# Same prompt, same model, same settings, run twice -> two different answers.
# (Held for Module 10: this is why you can't eyeball quality. You need evals.)
import anthropic

client = anthropic.Anthropic()
PROMPT = "In one vivid sentence, describe a city at dawn."

for i in (1, 2):
    reply = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=120,
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(f"Run {i}: " + "".join(b.text for b in reply.content if b.type == "text"))
