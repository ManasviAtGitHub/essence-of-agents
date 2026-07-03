# Module 9 - Reliability & security

Your agent reads untrusted text (Module 1) and takes real actions. What goes wrong?

## Question
We've spent eight modules letting the agent read files and web pages and act on them.
What happens when that text is hostile?

## Principle
The model **doesn't reliably preserve the boundary between instructions and data** -
to it, both are just tokens. So text the agent *reads* (a web page, a file, a tool
result) can carry instructions that hijack it. That's **prompt injection**, and the
same flexibility that makes agents useful makes them exploitable.

## See it (no key)
- `widgets/injection-flow/index.html` - the guided version: step through the document
  flowing into the context and watch the hidden line hijack the agent; flip the
  guardrail **ON** and step again to watch it caught at the door.
- `widgets/prompt-injection/index.html` - the sandbox: same setup, but the document is
  **editable**. Run with the guardrail OFF and the agent gets hijacked; toggle it ON
  and the guardrail flags the instruction inside the data. Try your own injection.
- `injection_offline.py` - the same guardrail in code: inspect untrusted text before it
  enters the context.

## The aha
The exploit wasn't a bug in your code - it was the feature (the agent reads and acts on
text) working exactly as designed. Defense isn't a patch; it's a discipline: control
**what enters the context** and **what actions are permitted**.

## The toolbox (full treatment)
Input/output guardrails, sandboxing untrusted tool output, **least-privilege tools**
(promote dangerous actions to gated tools - Module 1 / agent-design), and a
**human-in-the-loop approval gate** for irreversible actions.

## Honest note
The widget's keyword guardrail is a toy - real injection defense is layered and
imperfect. The durable lesson is the *threat model*, not the regex.

## Run
```
python agentic-course/module-09-security/injection_offline.py
```
or open `widgets/prompt-injection/index.html` and toggle the guardrail.
