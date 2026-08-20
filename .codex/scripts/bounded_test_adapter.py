from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUPERVISOR = ROOT / ".codex" / "scripts" / "Invoke-BoundedTest.ps1"
POLICY = ROOT / ".codex" / "policies" / "bounded-tests.md"
LAUNCHERS = ROOT / ".codex" / "policies" / "bounded-launchers.json"
EXCLUSIONS = ROOT / ".codex" / "policies" / "bounded-exclusions.gitignore"
EXPECTED_CATEGORIES = frozenset({"python_script", "powershell_file", "posix_shell"})


class PolicyError(ValueError):
    pass


@dataclass(frozen=True)
class CoveredInvocation:
    script: str | None


def _deny(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _load_launchers(policy_root: Path) -> dict[str, frozenset[str]]:
    path = policy_root / ".codex" / "policies" / "bounded-launchers.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot read valid bounded launcher policy {path}: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "launcher_categories"}:
        raise PolicyError("bounded launcher policy must contain only schema and launcher_categories")
    if value["schema"] != "bounded-launchers/v1":
        raise PolicyError("bounded launcher policy has the wrong schema")
    categories = value["launcher_categories"]
    if not isinstance(categories, dict) or set(categories) != EXPECTED_CATEGORIES:
        raise PolicyError("bounded launcher policy must declare the three supported categories")
    result: dict[str, frozenset[str]] = {}
    for category, raw_names in categories.items():
        if not isinstance(raw_names, list) or any(not isinstance(name, str) or not name.strip() for name in raw_names):
            raise PolicyError(f"bounded launcher category {category} must be a string list")
        result[category] = frozenset(_launcher_name(name) for name in raw_names)
    return result


def _validate_exclusions(policy_root: Path) -> Path:
    path = policy_root / ".codex" / "policies" / "bounded-exclusions.gitignore"
    try:
        path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PolicyError(f"cannot read valid bounded exclusion policy {path}: {exc}") from exc
    return path


def _launcher_name(token: str) -> str:
    name = token.strip("\"'").replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return name[:-4] if name.endswith(".exe") else name


def _tokens(segment: str) -> list[str]:
    try:
        values = shlex.split(segment, posix=False)
    except ValueError:
        return []
    return [value.strip("\"'") for value in values]


def _python_script(arguments: list[str]) -> str | None:
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        lowered = argument.casefold()
        if lowered in {"-c", "-m"} or lowered.startswith(("-c", "-m")):
            return None
        if lowered in {"-w", "-x"}:
            index += 2
            continue
        if lowered == "--":
            return arguments[index + 1] if index + 1 < len(arguments) else None
        if lowered.startswith("-"):
            index += 1
            continue
        return argument
    return None


def _shell_script(arguments: list[str]) -> str | None:
    for argument in arguments:
        lowered = argument.casefold()
        if lowered == "--":
            continue
        if lowered.startswith("-"):
            if "c" in lowered[1:]:
                return None
            continue
        return argument
    return None


def _command_body(values: list[str], command_index: int) -> str:
    if command_index + 1 >= len(values):
        return ""
    body = values[command_index + 1]
    if any(character.isspace() for character in body):
        return body
    return " ".join(values[command_index + 1 :])


def _covered_invocations(
    command: str,
    launchers: dict[str, frozenset[str]],
    *,
    inspect_command_body: bool = True,
) -> list[CoveredInvocation]:
    return [
        invocation
        for segment in _command_segments(command)
        for invocation in _covered_segment(segment, launchers, inspect_command_body=inspect_command_body)
    ]


def _covered_segment(
    segment: str,
    launchers: dict[str, frozenset[str]],
    *,
    inspect_command_body: bool = True,
) -> list[CoveredInvocation]:
    values = _tokens(segment)
    while values and values[0] in {"&", "."}:
        values.pop(0)
    if not values:
        return []

    first_name = _launcher_name(values[0])
    if first_name == "uv" and any(value.casefold() == "run" for value in values[1:]):
        run_index = next(index for index, value in enumerate(values) if value.casefold() == "run")
        for index in range(run_index + 1, len(values)):
            if _launcher_name(values[index]) in launchers["python_script"]:
                return [CoveredInvocation(_python_script(values[index + 1 :]))]

    if first_name in launchers["python_script"]:
        return [CoveredInvocation(_python_script(values[1:]))]

    if first_name in launchers["powershell_file"]:
        for index, value in enumerate(values[1:], start=1):
            if value.casefold() in {"-file", "-f"}:
                script = values[index + 1] if index + 1 < len(values) else None
                return [CoveredInvocation(script)]
            if inspect_command_body and value.casefold() in {"-command", "-c"}:
                return _covered_invocations(
                    _command_body(values, index),
                    launchers,
                    inspect_command_body=False,
                )
        return []

    if values[0].casefold().endswith(".ps1"):
        return [CoveredInvocation(values[0])]

    shell_index = 0
    if first_name == "wsl" and len(values) > 1:
        shell_index = 1
    if _launcher_name(values[shell_index]) in launchers["posix_shell"]:
        return [CoveredInvocation(_shell_script(values[shell_index + 1 :]))]
    return []


def _command_segments(command: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(command):
        character = command[index]
        if quote is not None:
            current.append(character)
            if quote == '"' and character == "`" and index + 1 < len(command):
                index += 1
                current.append(command[index])
            elif character == quote:
                quote = None
            index += 1
            continue
        if character == "`" and index + 1 < len(command):
            current.append(character)
            index += 1
            current.append(command[index])
            if command[index] == "\r" and index + 1 < len(command) and command[index + 1] == "\n":
                index += 1
                current.append(command[index])
            index += 1
            continue
        if character in {"'", '"'}:
            quote = character
            current.append(character)
            index += 1
            continue
        separator_length = 0
        if character in {";", "|", "\r", "\n"}:
            separator_length = 2 if character == "|" and command[index : index + 2] == "||" else 1
        elif command[index : index + 2] == "&&":
            separator_length = 2
        if separator_length:
            if part := "".join(current).strip():
                parts.append(part)
            current = []
            index += separator_length
            continue
        current.append(character)
        index += 1
    if part := "".join(current).strip():
        parts.append(part)
    return parts


def _working_directory(payload: dict[str, Any], policy_root: Path) -> Path:
    tool_input = payload.get("tool_input")
    raw = tool_input.get("workdir") if isinstance(tool_input, dict) else None
    if not isinstance(raw, str) or not raw:
        raw = payload.get("cwd")
    return Path(raw).resolve(strict=False) if isinstance(raw, str) and raw else policy_root


def _is_excluded(script: str, *, cwd: Path, policy_root: Path, exclusions: Path) -> bool:
    candidate = Path(script)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    candidate = candidate.resolve(strict=False)
    try:
        relative = candidate.relative_to(policy_root.resolve(strict=False)).as_posix()
    except ValueError:
        return False
    try:
        completed = subprocess.run(
            [
                "git",
                "-c",
                f"core.excludesFile={exclusions.as_posix()}",
                "-c",
                "core.quotePath=false",
                "check-ignore",
                "--no-index",
                "--verbose",
                relative,
            ],
            cwd=policy_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise PolicyError(f"git could not start to evaluate bounded exclusions: {exc}") from exc
    if completed.returncode not in {0, 1}:
        raise PolicyError(f"git could not evaluate bounded exclusions: {completed.stderr.strip()}")
    if completed.returncode == 1:
        return False
    match = re.match(r"^(.*):(\d+):(.*)\t", completed.stdout.strip())
    if match is None:
        raise PolicyError("git returned an unreadable bounded-exclusion match")
    source = Path(match.group(1).strip("\"'")).resolve(strict=False)
    return source == exclusions.resolve(strict=False) and not match.group(3).startswith("!")


def guard_code_test(payload: dict[str, Any], *, policy_root: Path | None = None) -> dict[str, Any]:
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        return {}
    active_root = (policy_root or ROOT).resolve(strict=False)
    try:
        launchers = _load_launchers(active_root)
        exclusions = _validate_exclusions(active_root)
        cwd = _working_directory(payload, active_root)
        covered = _covered_invocations(command, launchers)
        if not covered:
            return {}
        if all(
            invocation.script is not None
            and _is_excluded(
                invocation.script,
                cwd=cwd,
                policy_root=active_root,
                exclusions=exclusions,
            )
            for invocation in covered
        ):
            return {}
    except PolicyError as exc:
        return _deny(f"BOUNDED-TEST-v1 configuration error: {exc}. Fix the policy before retrying.")

    return _deny(
        "Direct configured Python-script, executed .ps1, and POSIX-shell execution is blocked by "
        "BOUNDED-TEST-v1 unless its resolved script path matches bounded-exclusions.gitignore. "
        f"Run covered work through {SUPERVISOR} with a justified expected upper bound, bounded "
        "cleanup allowance, computed maximum lifetime, heartbeat interval, timeout basis, and "
        "result path."
    )


def session_context() -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "The current ROOT-side orchestration infrastructure enforces BOUNDED-TEST-v1 for "
                "configured Python-script, executed .ps1, and POSIX-shell commands in this session. "
                "Git-ignore-style exclusions apply only to resolved script paths; lane-managed agent "
                "sessions are not test-bounded. "
                f"Read {POLICY} and invoke {SUPERVISOR} for covered work; set the tested product "
                "worktree as -WorkingDirectory. This is a runtime Codex-adapter overlay, not WIP "
                "product code."
            ),
        }
    }


def _payload() -> dict[str, Any]:
    try:
        value = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args == ["pre-tool-use"]:
        output = guard_code_test(_payload())
    elif args == ["session-start"]:
        _payload()
        output = session_context()
    else:
        print(
            "bounded-test-adapter: expected pre-tool-use or session-start",
            file=sys.stderr,
        )
        return 1
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
