#!/usr/bin/env python3
"""autoloop.py - the loop. Bonus track / B3.

THE PATTERN (Karpathy's `autoresearch`, generalized to ~130 lines): give an agent
a METRIC and let it hill-climb your code, unattended.

    propose -> apply -> RUN -> measure -> keep-if-better / rollback -> repeat

Every kept step is a git commit; every worse step is reverted. The metric is the
boss - the model only proposes; the verifier (B2) decides. This is B1's loop with
the stop-condition swapped for a score-to-maximize: instead of "until tests pass,"
it's "keep the best you've found." That single swap is how an agent does research
overnight - autoresearch loops this over nanochat training runs on one GPU.

RUN
  python3 autoloop.py --dry-run              # keyless: a deterministic proposer hill-climbs a knob
  ANTHROPIC_API_KEY=... python3 autoloop.py  # a real model proposes each step

MAKE IT YOURS (the 3 seams):
  apply(repo, cand) - how a proposal becomes a change on disk (here: set a knob;
                      in real use: apply a diff the model wrote)
  measure(repo)     - run the thing, return one number to MAXIMIZE (your B2 score,
                      an eval, a training metric, wall-clock - anything)
  Proposer.propose  - the model that suggests the next change given what's worked
"""
from __future__ import annotations
import argparse, os, re, shutil, subprocess, sys, tempfile

# ============================ the two seams: apply + measure ====================
def apply(repo, cand):
    """Turn a proposal into a change on disk. Here: rewrite the knob `K = <x>`.
    In real use this is `git apply` of a diff the model produced."""
    p = os.path.join(repo, "solution.py")
    src = open(p).read()
    open(p, "w").write(re.sub(r"K = [-\d.]+", f"K = {cand}", src))

def measure(repo):
    """Run the code, return ONE number to maximize. Swap in your eval / B2 score /
    training metric. Here solution.py prints `metric=<float>`."""
    r = subprocess.run([sys.executable, "solution.py"], cwd=repo, capture_output=True, text=True, timeout=30)
    m = re.search(r"metric=([-\d.]+)", r.stdout)
    return float(m.group(1)) if m else float("-inf")

# ============================ the loop (the metric is the boss) =================
def git(repo, *args):
    # scratch-repo identity only - never touches your global git config
    return subprocess.run(["git", "-c", "user.email=agent@localhost", "-c", "user.name=autoloop", *args],
                          cwd=repo, capture_output=True, text=True)

def run(repo, proposer, max_steps=12, eps=1e-6, log=print):
    best = measure(repo)
    git(repo, "add", "-A"); git(repo, "commit", "-m", f"seed metric={best:.4f}")
    best_k = read_k(repo); improved = True
    log(f"[seed] K={best_k}  metric={best:.4f}")
    for step in range(1, max_steps + 1):
        cand = proposer.propose(best_k, best, improved)
        if cand is None: log("  (proposer gave up)"); break
        apply(repo, cand); m = measure(repo)
        if m > best + eps:                       # KEEP: commit it, it's the new best
            git(repo, "commit", "-am", f"step {step}: K={cand} metric={m:.4f} (kept)")
            log(f"[step {step}] K={cand:<7} metric={m:.4f}  KEEP  (was {best:.4f})")
            best, best_k, improved = m, cand, True
        else:                                    # ROLLBACK: git reverts the file
            git(repo, "checkout", "--", "solution.py")
            log(f"[step {step}] K={cand:<7} metric={m:.4f}  rollback (best stays {best:.4f})")
            improved = False
        if proposer.done(): log("  (converged)"); break
    return best_k, best

def read_k(repo):
    return float(re.search(r"K = ([-\d.]+)", open(os.path.join(repo, "solution.py")).read()).group(1))

# ============================ proposers: fake (keyless) + real (BYO-key) ========
class FakeProposer:
    """Deterministic hill-climb so the loop runs keyless in CI: step in one
    direction while it helps; on a worse step, reverse and halve. Converges."""
    def __init__(self): self.step = 4.0
    def propose(self, best_k, best_m, improved):
        if not improved: self.step = -self.step / 2      # overshot -> reverse, smaller
        return round(best_k + self.step, 4)
    def done(self): return abs(self.step) < 0.3

class RealProposer:
    """A real model proposes the next value, given what has and hasn't worked.
    (Generalizes to: 'here is the code + metric, reply with a unified diff.')"""
    def __init__(self, model="claude-sonnet-5"):
        import anthropic; self.a = anthropic.Anthropic(); self.model = model; self._done = False
    def propose(self, best_k, best_m, improved):
        r = self.a.messages.create(model=self.model, max_tokens=16, messages=[{"role": "user", "content":
            f"Tuning a knob K to MAXIMIZE a hidden metric. Best so far: K={best_k} -> metric={best_m:.4f}. "
            f"Your last try {'helped' if improved else 'was worse and was reverted'}. "
            f"Propose the next value of K. Reply with ONLY a number."}])
        m = re.search(r"-?\d+\.?\d*", r.content[0].text)
        return float(m.group()) if m else None
    def done(self): return False

# ============================ sandbox + CLI ====================================
def make_demo():
    d = tempfile.mkdtemp(prefix="autoloop_")
    # a runnable "system" with one knob; its metric peaks at K=7 (the loop doesn't know that)
    open(os.path.join(d, "solution.py"), "w").write(
        "K = 0.0\n"
        "metric = -((K - 7.0) ** 2)   # a hidden peak at K=7; maximize toward 0\n"
        "print(f'metric={metric}')\n")
    git(d, "init", "-q")
    return d

def main():
    ap = argparse.ArgumentParser(description="autoresearch, generalized: propose->run->verify->keep/rollback")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--steps", type=int, default=12)
    a = ap.parse_args()
    if not a.dry_run and not os.environ.get("ANTHROPIC_API_KEY"): sys.exit("set ANTHROPIC_API_KEY or use --dry-run")
    repo = make_demo()
    print(f"[sandbox] scratch git repo at {repo} (a knob K, metric peaks at a value the loop must find)\n")
    proposer = FakeProposer() if a.dry_run else RealProposer()
    best_k, best_m = run(repo, proposer, max_steps=a.steps)
    print(f"\nBEST: K={best_k}  metric={best_m:.4f}   (git log below is the audit trail)")
    print(git(repo, "log", "--oneline").stdout.strip())
    print("\nThe model only proposed; the metric kept score and git kept the history -", "that is the loop.")
    shutil.rmtree(repo, ignore_errors=True)

if __name__ == "__main__":
    main()
