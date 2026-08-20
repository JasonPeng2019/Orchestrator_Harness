"""Phase 3.A coaching probe — drive a live deepseek-v4-flash claude lane to a
valid committed RESULT.json via orchestrator provider-session coaching, then
author the ROOT completion-review + acceptance to reach the terminal ACCEPTED
state (F15/G32).  Staged so the orchestrator (parent) can inspect between turns
and inject corrective `claude --resume` prompts.

Subcommands (all take --root <disposable-root>):
  build   : create the disposable repo + invocation, write config.json, print the
            turn-1 prompt and identity facts to <root>/state.json. Does NOT launch.
  launch  : run the lane-controller turn (the worker turn) and wait for terminal;
            record session id + controller status into <root>/state.json.
  status  : print current RESULT.json presence/validity + advancement state.
  accept  : author COMPLETION_REVIEW.json + ORCHESTRATOR_ACCEPTANCE.json (ROOT-IM)
            from the on-disk RESULT.json -> advancement ACCEPTED (terminal).

The worker turn inherits os.environ (the invocation sets no child-env isolation),
so the launching process must export the 180k auto-compact recipe + Ollama redirect
scrub; see the driver script.  This probe never sets ANTHROPIC_* itself.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.models import iso_utc
from orchestrator_harness.processes import (
    WINDOWS_CREATE_NO_WINDOW,
    targeted_process_query,
)
from orchestrator_harness.prompt_bundle import prompt_bundle_record_from_paths
from orchestrator_harness.public_launch import launch_lane_controller
from orchestrator_harness.task import (
    COMPLETION_REVIEW_FILENAME,
    ORCHESTRATOR_ACCEPTANCE_FILENAME,
    task_card_from_identity,
    validate_task_result,
    read_task_advancement,
)

CLAUDE_MODEL = "deepseek-v4-flash:0731-cloud"
CLAUDE_OLLAMA_OVERRIDE = 'model_provider="ollama"'
CONTROLLER_COMPLETION_SECONDS = 300
LANE = "claude-hello"
COHORT = "cohort-claude-fixture"


def _run(argv, *, cwd, env=None, expected=(0,), timeout=120):
    completed = subprocess.run(
        list(argv), cwd=cwd, env=env, stdin=subprocess.DEVNULL,
        capture_output=True, check=False, text=True, encoding="utf-8",
        errors="replace", timeout=timeout, shell=False,
        creationflags=WINDOWS_CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    if completed.returncode not in expected:
        raise RuntimeError(
            f"cmd failed ({completed.returncode}): {list(argv)!r}\n"
            f"stdout:{completed.stdout[-1500:]}\nstderr:{completed.stderr[-1500:]}"
        )
    return completed


def _git(cwd, *args):
    return _run(("git", *args), cwd=cwd).stdout.strip()


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _claude() -> list[str]:
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("no claude CLI on PATH")
    return [exe]


def _card_dict() -> dict[str, Any]:
    return {
        "schema": "orchestrator-task-card/v1",
        "card_id": f"card-{LANE}",
        "lane_id": LANE,
        "stage_cohort_id": COHORT,
        "worker_invocation_id": f"{LANE}-001",
        "objective": "Create HELLO.txt, commit it, and write a canonical RESULT.json",
        "revision": "r1",
    }


def _card_sha(card: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(card, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _worker_prompt(card_sha: str) -> str:
    card = _card_dict()
    worker = card["worker_invocation_id"]
    return f"""This is a disposable orchestrator fixture task. Do EXACTLY the following
steps in order, in the current directory (a git worktree). Do not ask questions.

STEP 1 - create the artifact:
  Write a file named HELLO.txt whose entire content is this single line:
    hello from claude

STEP 2 - commit it:
  git add HELLO.txt
  git commit -m "add HELLO.txt"

STEP 3 - capture the commit and branch:
  Run:  git rev-parse HEAD        (call the full 40-hex output <COMMIT>)
  Run:  git branch --show-current (call the output <BRANCH>)

STEP 4 - write the canonical result file to EXACTLY this path:
    .agent-workspace/RESULT.json
  with EXACTLY this JSON (substitute the real <COMMIT> and <BRANCH>; keep all
  other values verbatim; <COMMIT> must be lowercase 40-hex):

{{
  "schema": "orchestrator-task-result/v1",
  "card_id": "{card['card_id']}",
  "lane_id": "{LANE}",
  "worker_invocation_id": "{worker}",
  "cohort_id": "{COHORT}",
  "revision": "r1",
  "task_card_sha256": "{card_sha}",
  "branch": "<BRANCH>",
  "commit": "<COMMIT>",
  "outcome": "PASS",
  "summary": "Created and committed HELLO.txt as specified.",
  "checks": [
    {{"name": "hello-file-committed", "outcome": "PASS", "summary": "HELLO.txt committed"}}
  ],
  "acceptance_state": "PENDING"
}}

Then reply with one short line: the commit hash. Do not modify anything else.
"""


def _invocation(root: Path) -> Path:
    project = root / "project"
    worktrees = root / "worktrees"
    runtime = root / "runtime"
    project.mkdir(parents=True)
    worktrees.mkdir()
    runtime.mkdir()
    _git(project, "init", "-b", "main")
    _git(project, "config", "user.email", "fixture@example.invalid")
    _git(project, "config", "user.name", "Disposable Fixture")
    (project / "README.md").write_text("# Fixture project\n", encoding="utf-8")
    (project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
    _git(project, "add", "README.md", ".gitignore")
    _git(project, "commit", "-m", "Initial fixture project")
    base_commit = _git(project, "rev-parse", "HEAD")
    common_dir = (project / ".git").resolve()
    lane = worktrees / "lane-claude"
    _git(project, "worktree", "add", "-b", "lane/claude-hello", str(lane), base_commit)

    card = _card_dict()
    card_sha = _card_sha(card)
    workspace = lane / ".agent-workspace"
    workspace.mkdir(exist_ok=True)
    prompt = workspace / "worker-prompt.md"
    prompt.write_text(_worker_prompt(card_sha), encoding="utf-8")
    branch = _git(lane, "branch", "--show-current")
    worker_id = card["worker_invocation_id"]
    workflow_id = "disposable-claude-coach"
    profile_id = f"profile-{LANE}"
    tools = ["Read", "Bash", "Write", "Edit", "Glob", "Grep"]
    profile = {
        "schema": "orchestrator-runtime-profile/v1",
        "id": profile_id,
        "role": "implementer",
        "provider": "claude-code",
        "model": CLAUDE_MODEL,
        "tools": tools,
        "capabilities": ["repo"],
        "resources": [],
        "provider_needs": ["CLAUDE_CONFIG_DIR", "HOME"],
    }
    bundle = prompt_bundle_record_from_paths(
        workflow_id=workflow_id,
        task_card_id=card["card_id"],
        profile_id=profile_id,
        paths=(("instructions", prompt),),
        run_root=lane,
    )
    invocation = {
        "schema": "orchestrator-worker-invocation/v1",
        "action": "start",
        "run_root": str(lane),
        "runtime_root": str(runtime),
        "lane_id": LANE,
        "worker_invocation_id": worker_id,
        "cohort_id": COHORT,
        "workflow": {"id": workflow_id, "version": "1"},
        "task_card": {"id": card["card_id"], "revision": card["revision"], "sha256": card_sha},
        "role": "implementer",
        "provider": {
            "id": "claude-code",
            "model": CLAUDE_MODEL,
            "command": _claude(),
            "allowed_tools": tools,
            "config_overrides": [CLAUDE_OLLAMA_OVERRIDE],
        },
        "profile": profile,
        "prompt_bundle": bundle,
        "output_paths": {
            "status": str(workspace / "worker_controller.status.json"),
            "jsonl": str(workspace / "worker_claude.jsonl"),
            "stderr": str(workspace / "worker_claude.stderr.log"),
            "last_message": str(workspace / "worker_last_message.txt"),
        },
        "event_log_path": str(runtime / "LANE_EVENTS.jsonl"),
        "resources": [],
        "repository": {
            "common_dir": str(common_dir),
            "worktree_root": str(lane),
            "branch": branch,
            "base_commit": base_commit,
        },
    }
    path = workspace / "invocation.json"
    _write_json(path, invocation)
    # config.json so `python -m orchestrator_harness scan --config` reconciles the lane.
    _write_json(root / "config.json", {"suite_root": ".", "run_globs": ["worktrees/*"]})
    return path


def _state_path(root: Path) -> Path:
    return root / "state.json"


def cmd_build(root: Path) -> int:
    root = root.resolve()
    invocation = _invocation(root)
    card = _card_dict()
    _write_json(_state_path(root), {
        "invocation": str(invocation),
        "worktree": str(root / "worktrees" / "lane-claude"),
        "workspace": str(root / "worktrees" / "lane-claude" / ".agent-workspace"),
        "runtime": str(root / "runtime"),
        "config": str(root / "config.json"),
        "card_sha256": _card_sha(card),
        "stage": "built",
    })
    print(json.dumps({"built": True, "invocation": str(invocation),
                      "card_sha256": _card_sha(card)}, indent=2))
    return 0


def _wait_status(path: Path, predicate, timeout=CONTROLLER_COMPLETION_SECONDS):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            time.sleep(0.1); continue
        if isinstance(value, dict) and predicate(value):
            return value
        time.sleep(0.1)
    raise RuntimeError(f"timed out waiting for status in {path}")


def cmd_launch(root: Path) -> int:
    root = root.resolve()
    state = json.loads(_state_path(root).read_text(encoding="utf-8"))
    invocation = Path(state["invocation"])
    raw = json.loads(invocation.read_text(encoding="utf-8"))
    status_path = Path(raw["output_paths"]["status"])
    receipt = launch_lane_controller(
        invocation, receipt=invocation.parent / "operator_launch.json",
        cwd=HARNESS_ROOT, expected_state_path=status_path,
    )
    pid = receipt.get("pid"); created = receipt.get("created_utc")
    terminal = {"PROVIDER_EXITED", "CONTROLLER_FAILED", "LAUNCH_FAILED",
                "PROVIDER_HANDOFF", "PROVIDER_OPERATION_UNSUPPORTED", "COORDINATION_FAILED"}
    deadline = time.monotonic() + CONTROLLER_COMPLETION_SECONDS
    status = None
    while time.monotonic() < deadline:
        q = targeted_process_query(pid)
        if q.complete and not q.errors:
            proc = q.process
            if proc is None or iso_utc(proc.created_utc) != created:
                status = _wait_status(status_path, lambda v: v.get("state") in terminal)
                break
        time.sleep(0.1)
    if status is None:
        raise RuntimeError(f"controller pid {pid} did not exit")
    state.update({
        "stage": "launched",
        "terminal_state": status.get("state"),
        "provider_terminal_outcome": status.get("provider_terminal_outcome"),
        "exit_code": status.get("exit_code"),
        "session_id": status.get("provider_session_id"),
        "prompt_bundle_sha256": status.get("prompt_bundle_sha256"),
        "prompt_content_sha256": status.get("prompt_content_sha256"),
        "status_path": str(status_path),
    })
    _write_json(_state_path(root), state)
    print(json.dumps({k: state[k] for k in (
        "terminal_state", "provider_terminal_outcome", "exit_code", "session_id",
        "prompt_bundle_sha256", "prompt_content_sha256")}, indent=2))
    return 0


def _load_card_and_result(root: Path):
    state = json.loads(_state_path(root).read_text(encoding="utf-8"))
    status = json.loads(Path(state["status_path"]).read_text(encoding="utf-8"))
    raw_card = status.get("task_card") or {}
    card = task_card_from_identity(
        card_id=raw_card.get("id"),
        lane_id=status.get("declared_lane_id"),
        worker_invocation_id=status.get("worker_invocation_id"),
        cohort_id=status.get("cohort_id"),
        revision=raw_card.get("revision"),
        content_sha256=raw_card.get("sha256"),
        completion_review_owner=status.get("completion_review_owner", "ROOT-IM"),
    )
    workspace = Path(state["workspace"])
    result_path = workspace / "RESULT.json"
    return state, status, card, workspace, result_path


def cmd_status(root: Path) -> int:
    state, status, card, workspace, result_path = _load_card_and_result(root.resolve())
    report: dict[str, Any] = {"result_present": result_path.is_file()}
    if result_path.is_file():
        raw = result_path.read_bytes()
        try:
            value = json.loads(raw.decode("utf-8"))
            result = validate_task_result(value, card=card, raw_bytes=raw)
            report["result_valid"] = True
            report["result_content_sha256"] = result.content_sha256
            report["result_commit"] = result.commit
            # prompt-sha match against controller status (the cached-wrapper gate)
            report["prompt_bundle_sha_match"] = (
                value.get("prompt_bundle_sha256") == status.get("prompt_bundle_sha256"))
            report["prompt_content_sha_match"] = (
                value.get("prompt_content_sha256") == status.get("prompt_content_sha256"))
            adv = read_task_advancement(workspace, card=card, result=result)
            report["advancement_state"] = adv.advancement.state
            report["terminal"] = adv.advancement.terminal
        except Exception as exc:  # noqa: BLE001 - report validator message for coaching
            report["result_valid"] = False
            report["error"] = str(exc)
    print(json.dumps(report, indent=2))
    return 0


def _content_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def cmd_accept(root: Path) -> int:
    """ROOT-IM authors the completion review + acceptance -> ACCEPTED (terminal)."""
    state, status, card, workspace, result_path = _load_card_and_result(root.resolve())
    raw = result_path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    result = validate_task_result(value, card=card, raw_bytes=raw)

    # No `content_sha256` field: read_task_advancement passes raw_bytes, so the
    # cross-link digest each record exposes is sha256(exact file bytes). Write
    # the review, hash its bytes, then reference that hash from the acceptance.
    review = {
        "schema": "orchestrator-completion-review/v1",
        "card_id": card.card_id,
        "lane_id": card.lane_id,
        "worker_invocation_id": card.worker_invocation_id,
        "cohort_id": card.cohort_id,
        "revision": card.revision,
        "result_sha256": result.content_sha256,
        "owner": "ROOT-IM",
        "verdict": "PASS",
        "evidence": ["HELLO.txt committed and RESULT.json validated"],
        "summary": "Reviewed committed artifact and canonical result.",
    }
    review_path = workspace / COMPLETION_REVIEW_FILENAME
    _write_json(review_path, review)
    review_sha = hashlib.sha256(review_path.read_bytes()).hexdigest()

    acceptance = {
        "schema": "orchestrator-acceptance/v1",
        "card_id": card.card_id,
        "lane_id": card.lane_id,
        "worker_invocation_id": card.worker_invocation_id,
        "cohort_id": card.cohort_id,
        "revision": card.revision,
        "card_sha256": card.content_sha256,
        "result_sha256": result.content_sha256,
        "completion_review_sha256": review_sha,
        "accepted_commit": result.commit,
        "accepted_by": "ROOT-IM",
        "verdict": "ACCEPTED",
        "summary": "Accepted committed result.",
    }
    _write_json(workspace / ORCHESTRATOR_ACCEPTANCE_FILENAME, acceptance)

    adv = read_task_advancement(workspace, card=card, result=result)
    print(json.dumps({"advancement_state": adv.advancement.state,
                      "terminal": adv.advancement.terminal,
                      "review": COMPLETION_REVIEW_FILENAME,
                      "acceptance": ORCHESTRATOR_ACCEPTANCE_FILENAME}, indent=2))
    return 0


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 3 or args[1] != "--root":
        print("usage: probe_coach.py <build|launch|status|accept> --root <dir>",
              file=sys.stderr)
        return 2
    cmd, root = args[0], Path(args[2])
    return {"build": cmd_build, "launch": cmd_launch,
            "status": cmd_status, "accept": cmd_accept}[cmd](root)


if __name__ == "__main__":
    raise SystemExit(main())
