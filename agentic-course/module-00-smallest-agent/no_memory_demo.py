# Beat 5, experiment 1 - the model has no memory between calls.
#
# The API is stateless. The only reason our agent "remembers" anything is that WE
# keep appending to `messages` and resending the whole list. (Held for Module 3.)
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-8"

# Call 1: tell it something. We deliberately throw the reply away.
client.messages.create(
    model=MODEL,
    max_tokens=128,
    messages=[{"role": "user", "content": "My name is Ada. Remember it."}],
)

# Call 2: a brand-new call. We do NOT pass the previous turn.
reply = client.messages.create(
    model=MODEL,
    max_tokens=128,
    messages=[{"role": "user", "content": "What's my name?"}],
)
print("".join(b.text for b in reply.content if b.type == "text"))
# -> it doesn't know. Memory is something we provide, not something the model has.
