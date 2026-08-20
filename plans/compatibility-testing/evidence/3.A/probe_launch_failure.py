#!/usr/bin/env python3
"""Phase 3.A item 1 (G21) probe: authentic launch-failure event on a live lane.

Launches ONE lane through the real ``launch_lane_controller`` path whose provider
command is a stand-in binary that exits immediately WITHOUT emitting a
session-initialization record — the generic "provider failed at startup" case.
Per lane_controller.py:3117-3131 the harness then classifies this as
``LAUNCH_FAILED`` and appends that event to ``LANE_EVENTS.jsonl``.

Design note (why NOT a dead HTTP endpoint): the real ``claude`` binary prints a
client-side ``system/init`` line carrying a generated ``session_id`` BEFORE it
makes any network call, so pointing it at a closed port yields ``RUNNING_PROVIDER``
(a session was recorded) and leaves the binary hanging on retries — it never
reaches the LAUNCH_FAILED branch, which requires *no* session id. The faithful
way to exercise G21's launch-failure classification is a provider child that
exits before any session line. G21 is a provider-NEUTRAL harness classification
(``notifications.py`` groups LAUNCH_FAILED/CONTROLLER_FAILED/CONTROLLER_INTERRUPTED
independent of which provider), so a stand-in provider that fails at startup is
the correct authentic trigger: real controller, real child process, real
event-log append — not a fabricated status file. It also re-confirms the phase-0
argv fix: the failure is the child's own exit, not the pre-fix --verbose flag
error.

Quota-free by construction: the provider stub exits before executing any network
call, so no Ollama/Anthropic endpoint is ever contacted.

Pass = a LAUNCH_FAILED (or CONTROLLER_FAILED) event for the lane appears in
LANE_EVENTS.jsonl and the controller status terminal state is that failure
state, with provider_session_id null (proving it never initialized a session).

Run:  python probe_launch_failure.py [--keep DIR]
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.processes import WINDOWS_CREATE_NO_WINDOW  # noqa: E402
from orchestrator_harness.profile import RuntimeProfile  # noqa: E402
from orchestrator_harness.prompt_bundle import (  # noqa: E402
    prompt_bundle_record_from_paths,
)
from orchestrator_harness.provider import claude_config_override_env  # noqa: E402
from orchestrator_harness.public_launch import launch_lane_controller  # noqa: E402

CLAUDE_MODEL = "deepseek-v4-flash:0731-cloud"
ANTHROPIC_KEYS = ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY")
TOOLS = ["Read", "Bash", "Write", "Edit", "Glob", "Grep"]

# A provider stand-in that exits immediately (code 3) without printing a
# session-init line. The claude adapter appends its flags AFTER spec.command
# (provider.py:593 `argv = [*spec.command, "--print", ...]`); python's -c runs
# this and treats the appended flags as sys.argv, so it exits at once, emits no
# stream-json, and the controller sees action=start with no provider_session_id
# -> LAUNCH_FAILED. It never touches the network, so it is quota-free.
STUB_COMMAND = [sys.executable, "-c", "import sys; sys.exit(3)"]
# Harmless redirect entry to mirror a realistic invocation's env channel; the
# stub exits before reading it, so it is never contacted.
DEAD_OVERRIDES = [
    'ANTHROPIC_BASE_URL="http://127.0.0.1:9"',
    'ANTHROPIC_AUTH_TOKEN="dead"',
    "ANTHROPIC_API_KEY=",
]

TERMINAL_TIMEOUT = 90.0


class ProbeError(RuntimeError):
    pass


def _run(argv: Sequence[str], *, cwd: Path, expected=(0,), timeout=60) -> str:
    completed = subprocess.run(
        list(argv),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        shell=False,
        stdin=subprocess.DEVNULL,
        creationflags=WINDOWS_CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    if completed.returncode not in expected:
        raise ProbeError(
            f"command failed ({completed.returncode}): {list(argv)!r}\n"
            f"stderr: {completed.stderr[-1500:]}"
        )
    return completed.stdout.strip()


def _git(cwd: Path, *args: str) -> str:
    return _run(("git", *args), cwd=cwd)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _strip_anthropic() -> list[str]:
    removed = sorted(k for k in ANTHROPIC_KEYS if k in os.environ)
    for k in removed:
        del os.environ[k]
    return removed


def _invocation(*, lane: str, worktree: Path, common_dir: Path,
                base_commit: str, runtime: Path) -> Path:
    workspace = worktree / ".agent-workspace"
    workspace.mkdir(exist_ok=True)
    prompt = workspace / "worker-prompt.md"
    prompt.write_text("Create g21-artifact.txt and commit it.\n", encoding="utf-8")
    branch = _git(worktree, "branch", "--show-current")
    worker_id = f"{lane}-001"
    card = {
        "schema": "orchestrator-task-card/v1",
        "card_id": f"card-{lane}",
        "lane_id": lane,
        "stage_cohort_id": f"cohort-{lane}",
        "worker_invocation_id": worker_id,
        "objective": "Create g21-artifact.txt and commit it",
        "revision": "r1",
    }
    profile = RuntimeProfile(
        f"profile-{lane}", "implementer", "claude-code", CLAUDE_MODEL,
        tuple(TOOLS), ("repo",), (), ("CLAUDE_CONFIG_DIR", "HOME"),
    )
    bundle = prompt_bundle_record_from_paths(
        workflow_id="probe-3A-g21",
        task_card_id=card["card_id"],
        profile_id=f"profile-{lane}",
        paths=(("instructions", prompt),),
        run_root=worktree,
    )
    invocation = {
        "schema": "orchestrator-worker-invocation/v1",
        "action": "start",
        "run_root": str(worktree),
        "runtime_root": str(runtime),
        "lane_id": lane,
        "worker_invocation_id": worker_id,
        "cohort_id": f"cohort-{lane}",
        "workflow": {"id": "probe-3A-g21", "version": "1"},
        "task_card": {
            "id": card["card_id"],
            "revision": card["revision"],
            "sha256": hashlib.sha256(
                json.dumps(card, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
        },
        "role": "implementer",
        "provider": {
            "id": "claude-code",
            "model": CLAUDE_MODEL,
            "command": STUB_COMMAND,
            "allowed_tools": TOOLS,
            "config_overrides": DEAD_OVERRIDES,
        },
        "profile": profile.to_record(),
        "prompt_bundle": bundle,
        "output_paths": {
            "status": str(workspace / "worker.status.json"),
            "jsonl": str(workspace / "worker.jsonl"),
            "stderr": str(workspace / "worker.stderr.log"),
            "last_message": str(workspace / "worker_last_message.txt"),
        },
        "event_log_path": str(runtime / "LANE_EVENTS.jsonl"),
        "resources": [],
        "repository": {
            "common_dir": str(common_dir),
            "worktree_root": str(worktree),
            "branch": branch,
            "base_commit": base_commit,
        },
    }
    path = workspace / "invocation.json"
    _write_json(path, invocation)
    return path


def _lane_events(runtime: Path) -> list[dict[str, Any]]:
    path = runtime / "LANE_EVENTS.jsonl"
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


FAILURE_TYPES = {"LAUNCH_FAILED", "CONTROLLER_FAILED", "CONTROLLER_INTERRUPTED"}


def _event_kind(e: Mapping[str, Any]) -> Any:
    # LANE_EVENTS.jsonl rows carry the event name under "event"; some other
    # event surfaces use "type". Accept either so the check is robust.
    return e.get("event", e.get("type"))


def _wait_for_failure_event(
    runtime: Path, status_path: Path, timeout: float
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Poll until a launch-failure EVENT is appended to LANE_EVENTS.jsonl.

    The status file's *initial* default state is also 'LAUNCH_FAILED' (written
    before the child is spawned), so the authoritative signal is the appended
    event, not the status state. Return the last status read and the events.
    """
    deadline = time.monotonic() + timeout
    last: dict[str, Any] = {}
    while time.monotonic() < deadline:
        events = _lane_events(runtime)
        if any(_event_kind(e) in FAILURE_TYPES for e in events):
            try:
                last = json.loads(status_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                last = {}
            return last, events
        time.sleep(0.2)
    try:
        last = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        last = {}
    return last, _lane_events(runtime)


def run_probe(root: Path) -> dict[str, Any]:
    root = root.resolve()
    project = root / "project"
    worktrees = root / "worktrees"
    runtime = root / "runtime"
    for d in (project, worktrees, runtime):
        d.mkdir(parents=True)

    removed = _strip_anthropic()
    ccd = root / "claude-config-dir"
    ccd.mkdir(exist_ok=True)
    os.environ["CLAUDE_CONFIG_DIR"] = str(ccd)
    assert not any(k in os.environ for k in ANTHROPIC_KEYS)
    expansion = {}
    for ov in DEAD_OVERRIDES:
        expansion.update(claude_config_override_env(ov))

    _git(project, "init", "-b", "main")
    _git(project, "config", "user.email", "probe@example.invalid")
    _git(project, "config", "user.name", "Phase 3A Probe")
    (project / "README.md").write_text("# G21 probe\n", encoding="utf-8")
    (project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
    _git(project, "add", "README.md", ".gitignore")
    _git(project, "commit", "-m", "init")
    base_commit = _git(project, "rev-parse", "HEAD")
    common_dir = str((project / ".git").resolve())
    lane_wt = worktrees / "lane-g21"
    _git(project, "worktree", "add", "-b", "lane/g21", str(lane_wt), base_commit)

    inv = _invocation(
        lane="lane-g21", worktree=lane_wt, common_dir=Path(common_dir),
        base_commit=base_commit, runtime=runtime,
    )
    status_path = lane_wt / ".agent-workspace" / "worker.status.json"

    started = time.monotonic()
    launch_lane_controller(
        inv, receipt=inv.parent / "launch_receipt.json",
        cwd=HARNESS_ROOT, expected_state_path=status_path,
    )
    status, events = _wait_for_failure_event(runtime, status_path, TERMINAL_TIMEOUT)
    elapsed = round(time.monotonic() - started, 1)

    event_types = [_event_kind(e) for e in events]
    failure_events = [e for e in events if _event_kind(e) in FAILURE_TYPES]
    terminal_state = status.get("state")
    session_id = status.get("provider_session_id")

    verdict_pass = (
        bool(failure_events)
        and terminal_state in FAILURE_TYPES
        and not session_id  # never initialized a real session
    )

    return {
        "probe": "3.A/G21 authentic launch-failure",
        "clone_root": str(HARNESS_ROOT),
        "removed_ambient_anthropic": removed,
        "override_expansion": expansion,
        "elapsed_s": elapsed,
        "terminal_state": terminal_state,
        "provider_session_id": session_id,
        "controller_error": status.get("error"),
        "event_types": event_types,
        "failure_event_types": [_event_kind(e) for e in failure_events],
        "failure_event_errors": [e.get("error") for e in failure_events],
        "verdict": "PASS" if verdict_pass else "FAIL",
    }


def main() -> int:
    args = sys.argv[1:]
    keep = None
    if args:
        if len(args) != 2 or args[0] != "--keep":
            print("usage: probe_launch_failure.py [--keep DIR]", file=sys.stderr)
            return 2
        keep = Path(args[1]).resolve()
        if keep.exists():
            print("--keep DIR must not exist", file=sys.stderr)
            return 2
        keep.mkdir(parents=True)
    try:
        if keep is not None:
            result = run_probe(keep)
        else:
            with tempfile.TemporaryDirectory(prefix="probe-3A-") as tmp:
                result = run_probe(Path(tmp))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["verdict"] == "PASS" else 1
    except (ProbeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"probe failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
