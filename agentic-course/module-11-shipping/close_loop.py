"""Close the loop, keyless: a production failure becomes a new eval case on disk.

This is the one edge that turns the dev loop into a production loop. Run it a few times
and watch evalset.json grow - each captured failure is a permanent regression test.
An eval set is a *set*: re-capturing a failure you already have adds nothing, so
duplicates are skipped (that's part of the lesson).

    python agentic-course/module-11-shipping/close_loop.py
    (reset evalset.json to [] to start over)
"""
import json
import os

EVAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evalset.json")

# Failures observed "in the wild" - each run of this script captures the next one,
# the way a week of production traffic would surface them one at a time.
PROD_FAILURES = [
    {"input": "user pasted a 50k-token doc and asked for a one-line answer",
     "expected": "summarize, don't error",
     "captured_from": "prod trace"},
    {"input": "web_fetch timed out and the agent retried forever",
     "expected": "give up after 2 retries and say so",
     "captured_from": "prod trace"},
    {"input": "answer quoted a price from a stale cached page",
     "expected": "re-fetch before quoting numbers",
     "captured_from": "user report"},
]


def load():
    return json.load(open(EVAL, encoding="utf-8")) if os.path.exists(EVAL) else []


def capture_failure(case):
    data = load()
    if case in data:  # an eval set is a set - never duplicate a row
        return data, False
    data.append(case)
    with open(EVAL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data, True


# The next real failure observed in production becomes a row in the eval set:
data = load()
new_case = next((c for c in PROD_FAILURES if c not in data), None)

if new_case is None:
    print(f"All {len(PROD_FAILURES)} observed prod failures are already captured "
          f"({len(data)} cases).")
    print("Nothing new this run - but every past failure is a permanent test now.")
else:
    data, added = capture_failure(new_case)
    print(f"Captured a prod failure -> eval set now has {len(data)} case(s).")
    print("Next deploy can't regress on it: it's a permanent test now.")

print("That feedback edge is the whole of 'shipping' - the loop learns from its logs.")
