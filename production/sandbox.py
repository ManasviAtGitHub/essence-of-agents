"""Run model-written code in a subprocess with a timeout (Module 6's verifier, safely-ish).

`python -I` isolates from the user's env and site-packages, and the timeout caps runaways.
This is NOT a real sandbox: it does NOT block network or filesystem access. True isolation
needs containers / seccomp / a no-network namespace / a resource-limited user. Use this for
local dev and tests only; in production run untrusted code in a real sandbox.
"""
import subprocess
import sys


def run_python(code: str, timeout: float = 5.0) -> dict:
    try:
        p = subprocess.run([sys.executable, "-I", "-c", code],
                           capture_output=True, text=True, timeout=timeout)
        return {"stdout": p.stdout, "stderr": p.stderr, "returncode": p.returncode}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": f"timeout after {timeout}s", "returncode": -1}


def run_python_tool(timeout: float = 5.0):
    """Wrap the sandbox as an agent tool, so a verifier loop can run code and read errors."""
    from claude_harness.tools import tool

    @tool
    def run_python_code(code: str) -> str:
        """Run a short Python snippet in a sandboxed subprocess and return its output.

        Args:
            code: the Python source to run
        """
        r = run_python(code, timeout)
        return f"exit={r['returncode']}\nstdout:\n{r['stdout']}\nstderr:\n{r['stderr']}"

    return run_python_code
