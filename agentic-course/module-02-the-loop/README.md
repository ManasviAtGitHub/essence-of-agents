# Module 2 - The loop (Reason + Act)

The agent already loops (Module 0). This module asks a sharper question: should the
model *think* before it acts - and does that actually help, or is it decoration?

## Question
Why interleave thinking and doing, instead of deciding everything up front?

## Principle
The model can't see the future. Reasoning is just more tokens - but tokens that
condition the next action. When results can surprise you, a moment of thinking out
loud buys a better next move. (This is Reason + Act, a.k.a. ReAct.)

## See it (no key)
- `widgets/think-toggle/index.html` - a switch: **Reasoning ON / OFF**, on the classic
  bat-and-ball problem. With reasoning OFF the model blurts the intuitive, wrong answer
  ($0.10); with reasoning ON it works the algebra and gets it right ($0.05). Toggle and
  re-run to feel the difference.

This widget **is** the module's "break it on purpose": flipping reasoning off is the
ablation, and the ablation is the lesson.

## The aha
"Thinking" isn't decoration. Flip it off and accuracy falls on a problem where the
intuitive answer is a trap. The reasoning tokens paid rent in the answer that followed.

## Honest note (offline)
The widget replays two recorded answers so you can see the effect with no key. To
*measure* it - across many problems, with a real model - see `CHALLENGE.md`. That's
where the claim stops being a demo and becomes data (the seed of Module 10).

## Build it (no key)
The loop is the lesson, so build it -- don't just toggle a widget:
`python agentic-course/module-02-the-loop/react_demo.py` writes the
observe -> think -> act loop by hand and shows the answer flip when the think step is
deleted.

## Run
Open `widgets/think-toggle/index.html` in a browser. Toggle **Reasoning**, press
**Run**, toggle again, run again.
