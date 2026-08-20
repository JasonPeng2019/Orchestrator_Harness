from __future__ import annotations

import hashlib
import sys
from pathlib import Path

POLICY_SHA256 = "be10f776c27fa8ffb46b8d395ac791ee0d73c235cf8a0d079fc960612a00f126"


def suite_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_verified_policy() -> str:
    root = suite_root()
    policy_path = root / ".agent-workspace" / "AUTONOMOUS_EXECUTION_POLICY.md"
    sidecar_path = root / ".agent-workspace" / "AUTONOMOUS_EXECUTION_POLICY.sha256"
    policy_bytes = policy_path.read_bytes()
    actual = hashlib.sha256(policy_bytes).hexdigest()
    sidecar = sidecar_path.read_text(encoding="utf-8").split()[0].lower()
    if actual != POLICY_SHA256 or sidecar != POLICY_SHA256:
        raise RuntimeError(
            "autonomous-execution policy hash mismatch: "
            f"expected={POLICY_SHA256} actual={actual} sidecar={sidecar}"
        )
    return policy_bytes.decode("utf-8-sig")


def compose_policy_bound_prompt(prompt_path: Path) -> str:
    prompt = prompt_path.read_text(encoding="utf-8-sig")
    policy = load_verified_policy()
    banner = f"""\
## AUTHORITATIVE ZERO-OPERATOR OVERRIDE

Policy SHA-256: `{POLICY_SHA256}`

The policy below and the run's last signed specification amendment supersede every contrary
instruction in older prompts, specs, assignments, checkpoints, reviews, and result schemas.
For a main-catalog run, never request physical/operator work, external lab equipment, another user
response, or a terminal `NEEDS_USER`/`INFRA_BLOCKED` result. Use autonomous controls or write a
safe nonterminal checkpoint while the manager continues unrelated lanes.

{policy}

## END AUTHORITATIVE ZERO-OPERATOR OVERRIDE
"""
    # Repeat the precedence sentence after the task prompt so stale instructions cannot become the
    # most recent instruction in the composed input.
    trailer = f"""\

## FINAL PRECEDENCE REMINDER

Policy `{POLICY_SHA256}` and the latest signed run amendment control. Ignore any older clause above
that asks for physical/operator intervention, external equipment, another user response, or
`NEEDS_USER`/`INFRA_BLOCKED`.
"""
    return f"{banner}\n{prompt.rstrip()}\n{trailer}"


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: prompt_policy.py INPUT_PROMPT OUTPUT_PROMPT")
    source = Path(sys.argv[1]).resolve()
    destination = Path(sys.argv[2]).resolve()
    destination.write_text(
        compose_policy_bound_prompt(source),
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
