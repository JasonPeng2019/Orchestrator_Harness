from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from dev_state import verification_is_current

ROOT = Path(__file__).resolve().parents[2]
VERIFY_CHANGED = ROOT / ".codex" / "scripts" / "verify_changed.py"
BOUNDED_TEST_SUPERVISOR = ROOT / ".codex" / "scripts" / "Invoke-BoundedTest.ps1"
STOP_VERIFY_RESULT = ROOT / ".codex" / "runtime" / "bounded-tests" / "stop-verify.json"
HARNESS_PLAN = ROOT / "plans" / "general-coding-harness" / "FULL-EXECUTION-SPEC_PLAN_2.md"

DESTRUCTIVE_PATTERNS = (
    (
        re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE),
        "git reset --hard is blocked",
    ),
    (
        re.compile(r"\bgit\s+(?:checkout|restore)\s+--\s", re.IGNORECASE),
        "destructive Git restore is blocked",
    ),
    (
        re.compile(r"\bgit\s+clean\s+-[^\s]*f", re.IGNORECASE),
        "git clean with force is blocked",
    ),
    (
        re.compile(r"\brm\s+-[^\s]*r[^\s]*f|\brm\s+-[^\s]*f[^\s]*r", re.IGNORECASE),
        "recursive forced removal is blocked",
    ),
    (
        re.compile(r"\bRemove-Item\b(?=[^\r\n]*(?:-Recurse|-Force))", re.IGNORECASE),
        "recursive or forced Remove-Item is blocked",
    ),
    (
        re.compile(
            r"\b(?:curl|wget)\b[^\r\n|]*\|\s*(?:sh|bash|zsh|pwsh|powershell)\b",
            re.IGNORECASE,
        ),
        "download-to-shell is blocked",
    ),
)


def guard_dangerous(payload: dict[str, Any]) -> dict[str, Any]:
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        return {}
    normalized = " ".join(command.split())
    for pattern, reason in DESTRUCTIVE_PATTERNS:
        if pattern.search(normalized):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
    return {}


def session_start(payload: dict[str, Any]) -> dict[str, Any]:
    handoff = ROOT / "HANDOFF.md"
    context = "Harness development verification is enforced by the project Stop hook."
    if handoff.is_file():
        text = handoff.read_text(encoding="utf-8", errors="replace").strip()
        if text:
            context += f"\n\nProject context from HANDOFF.md:\n{text[:20000]}"
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }


def pre_compact(_payload: dict[str, Any]) -> dict[str, Any]:
    message = (
        "Before compaction, keep a concise HANDOFF.md with status, decisions, files in flight, and the next command."
    )
    if (ROOT / "HANDOFF.md").is_file():
        message = "HANDOFF.md exists; ensure it reflects the current verified state before compaction."
    return {"continue": True, "systemMessage": message}


def verify_on_stop(_payload: dict[str, Any]) -> dict[str, Any]:
    if not HARNESS_PLAN.is_file():
        return {}
    try:
        if verification_is_current(ROOT):
            return {}
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(BOUNDED_TEST_SUPERVISOR),
                "-Command",
                "uv run --project .codex/dev --locked python .codex/scripts/verify_changed.py",
                "-WorkingDirectory",
                str(ROOT),
                "-MaximumLifetimeSeconds",
                "240",
                "-ExpectedUpperBoundSeconds",
                "210",
                "-CleanupAllowanceSeconds",
                "30",
                "-HeartbeatIntervalSeconds",
                "30",
                "-TimeoutBasis",
                ("The Codex Stop hook has a 300-second ceiling; 240 seconds reserves cleanup and response time."),
                "-ResultPath",
                str(STOP_VERIFY_RESULT),
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=290,
        )
    except Exception as exc:
        return {
            "decision": "block",
            "reason": f"Changed-code verification could not run: {exc}",
        }
    if result.returncode == 0:
        return {"systemMessage": "Changed-code verification passed for the current repository state."}
    output = (result.stdout + "\n" + result.stderr).strip()
    return {
        "decision": "block",
        "reason": "Changed-code verification failed. Fix the failures and rerun the gate before finishing.\n\n"
        + output[-6000:],
    }


def _read_payload() -> dict[str, Any]:
    try:
        value = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("hook-runner: expected one event name", file=sys.stderr)
        return 1
    handlers = {
        "guard-dangerous": guard_dangerous,
        "session-start": session_start,
        "pre-compact": pre_compact,
        "verify-on-stop": verify_on_stop,
    }
    handler = handlers.get(args[0])
    if handler is None:
        print(f"hook-runner: unknown event {args[0]}", file=sys.stderr)
        return 1
    try:
        print(json.dumps(handler(_read_payload())))
    except Exception as exc:  # Hooks should fail visibly without crashing Codex.
        print(json.dumps({"systemMessage": f"Harness hook failed: {exc}"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
