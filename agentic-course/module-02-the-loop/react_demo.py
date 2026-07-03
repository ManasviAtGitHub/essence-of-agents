"""Module 2 -- the Reason+Act loop, built by hand (keyless).

You WRITE the observe -> think -> act loop here; the model's steps are scripted so it
runs with no key. The point is the loop itself, and what the think step buys.

    python agentic-course/module-02-the-loop/react_demo.py
"""

# A tiny tool. (Trusted demo input only -- never eval untrusted text; see Module 9.)
TOOLS = {"calc": lambda expr: str(eval(expr, {"__builtins__": {}}))}

# Two scripted "policies" for the task "12 items at 13 each -- what's the total?".
# WITH a think step the model reasons, then acts correctly.
# WITHOUT it, the model jumps straight to an action and picks the wrong operation.
WITH_THINK = [
    ("think", "12 items at 13 each means multiply, not add."),
    ("act", "calc", "12*13"),
    ("answer", "156"),
]
WITHOUT_THINK = [
    ("act", "calc", "12+13"),   # acted before reasoning -> wrong operation
    ("answer", "25"),
]


def react(transcript):
    """The loop: walk steps, run any tool, return the final answer."""
    scratch = []
    for step in transcript:
        if step[0] == "think":
            scratch.append("THINK: " + step[1])
            print("  think: ", step[1])
        elif step[0] == "act":
            _, tool, arg = step
            result = TOOLS[tool](arg)
            scratch.append(f"ACT {tool}({arg}) -> {result}")
            print(f"  act:   {tool}({arg}) = {result}")
        elif step[0] == "answer":
            print("  answer:", step[1])
            return step[1]


print("WITH the think step:")
a = react(WITH_THINK)
print("\nWITHOUT the think step (deleted):")
b = react(WITHOUT_THINK)
print(f"\nwith-think -> {a} (right)    without-think -> {b} (wrong)")
print("Same loop code. Reasoning is just tokens that condition a better next action.")
print("(Offline the contrast is scripted; CHALLENGE.md measures it with a real model.)")
