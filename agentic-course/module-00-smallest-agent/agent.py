# agent.py - the smallest agent that could (built from scratch, on purpose)
#
# Three lines carry the whole module:
#   while True      -> the loop is the agency
#   messages        -> this list is the memory
#   run_tool(...)   -> your code is the runtime; the model only *asks*
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

TOOLS = [
    {
        "name": "read_file",
        "description": "Read a UTF-8 text file from disk and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Path to the file"}},
            "required": ["path"],
        },
    }
]


def run_tool(name, args):  # YOUR code is the runtime
    if name == "read_file":
        with open(args["path"], encoding="utf-8") as f:
            return f.read()
    return f"Unknown tool: {name}"


def agent(task):
    messages = [{"role": "user", "content": task}]  # this list IS the memory
    while True:                                      # this loop IS the agency
        reply = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2048,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": reply.content})

        if reply.stop_reason != "tool_use":          # nothing left to do -> done
            return "".join(b.text for b in reply.content if b.type == "text")

        results = []
        for b in reply.content:
            if b.type == "tool_use":                 # the model asked; we act
                out = run_tool(b.name, b.input)
                results.append(
                    {"type": "tool_result", "tool_use_id": b.id, "content": out}
                )
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    print(
        agent(
            "Read your own source file agent.py and explain, in two sentences, "
            "how you work."
        )
    )
