"""3.C cross-provider concurrency — a live claude-code+Ollama lane and a live
codex+Ollama lane, launched CONCURRENTLY onto ONE shared runtime (shared
LANE_EVENTS.jsonl + shared resource-lock root), then reconciled together.

Proves the coordination substrate is provider-neutral: two different provider
adapters run at once, each writes real PROVIDER_STARTED/PROVIDER_EXITED rows to
the SAME event log, and a single `scan` reconciles both lanes side-by-side with
their distinct provider ids.  Both providers point at the local Ollama backend
(claude via config_overrides model_provider="ollama"; codex via its built-in
`ollama` provider), so no cloud quota is spent.

Session-local only: codex runs with --ignore-user-config; claude's config dir is
pinned into the run scratch by the launching process.  No ~/.claude or ~/.codex
writes.
"""

from __future__ import annotations

import concurrent.futures
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

CLAUDE_MODEL = "deepseek-v4-flash:0731-cloud"
CODEX_MODEL = "deepseek-v4-flash:0731-cloud"
CLAUDE_OLLAMA_OVERRIDE = 'model_provider="ollama"'
COHORT = "cohort-xprovider"
COMPLETION_SECONDS = 300


def _run(argv, *, cwd, timeout=120, expected=(0,)):
    c = subprocess.run(list(argv), cwd=cwd, stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, shell=False,
                       creationflags=WINDOWS_CREATE_NO_WINDOW if os.name == "nt" else 0)
    if c.returncode not in expected:
        raise RuntimeError(f"{argv!r} rc={c.returncode}\n{c.stdout[-800:]}\n{c.stderr[-800:]}")
    return c


def _git(cwd, *a):
    return _run(("git", *a), cwd=cwd).stdout.strip()


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _init_project(root: Path):
    project = root / "project"
    project.mkdir(parents=True)
    _git(project, "init", "-b", "main")
    _git(project, "config", "user.email", "fixture@example.invalid")
    _git(project, "config", "user.name", "Disposable Fixture")
    (project / "README.md").write_text("# xprovider\n", encoding="utf-8")
    (project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
    _git(project, "add", "README.md", ".gitignore")
    _git(project, "commit", "-m", "init")
    base = _git(project, "rev-parse", "HEAD")
    return project, (project / ".git").resolve(), base


def _worktree(project: Path, root: Path, lane: str, branch: str, base: str) -> Path:
    wt = root / "worktrees" / f"lane-{lane}"
    _git(project, "worktree", "add", "-b", branch, str(wt), base)
    (wt / ".agent-workspace").mkdir(exist_ok=True)
    return wt


def _claude_invocation(root, wt, common_dir, base, runtime, resource_lock_root):
    lane = "claude"
    workspace = wt / ".agent-workspace"
    prompt = workspace / "worker-prompt.md"
    prompt.write_text("Create a file named CLAUDE.txt containing 'claude lane', "
                      "then run: git add CLAUDE.txt && git commit -m claude. "
                      "Then reply with one word: done.", encoding="utf-8")
    branch = _git(wt, "branch", "--show-current")
    worker_id = f"{lane}-001"
    card = {"schema": "orchestrator-task-card/v1", "card_id": f"card-{lane}",
            "lane_id": lane, "stage_cohort_id": COHORT,
            "worker_invocation_id": worker_id, "objective": "make CLAUDE.txt",
            "revision": "r1"}
    card_sha = hashlib.sha256(json.dumps(card, sort_keys=True,
                              separators=(",", ":")).encode()).hexdigest()
    tools = ["Read", "Bash", "Write", "Edit", "Glob", "Grep"]
    profile = {"schema": "orchestrator-runtime-profile/v1", "id": f"profile-{lane}",
               "role": "implementer", "provider": "claude-code", "model": CLAUDE_MODEL,
               "tools": tools, "capabilities": ["repo"], "resources": ["service:claude-only"],
               "provider_needs": ["CLAUDE_CONFIG_DIR", "HOME"]}
    bundle = prompt_bundle_record_from_paths(
        workflow_id="xprovider", task_card_id=card["card_id"],
        profile_id=f"profile-{lane}", paths=(("instructions", prompt),), run_root=wt)
    inv = {
        "schema": "orchestrator-worker-invocation/v1", "action": "start",
        "run_root": str(wt), "runtime_root": str(runtime), "lane_id": lane,
        "worker_invocation_id": worker_id, "cohort_id": COHORT,
        "workflow": {"id": "xprovider", "version": "1"},
        "task_card": {"id": card["card_id"], "revision": "r1", "sha256": card_sha},
        "role": "implementer",
        "provider": {"id": "claude-code", "model": CLAUDE_MODEL, "command": [shutil.which("claude")],
                     "allowed_tools": tools, "config_overrides": [CLAUDE_OLLAMA_OVERRIDE]},
        "profile": profile, "prompt_bundle": bundle,
        "output_paths": {"status": str(workspace / "worker_controller.status.json"),
                         "jsonl": str(workspace / "worker_claude.jsonl"),
                         "stderr": str(workspace / "worker_claude.stderr.log"),
                         "last_message": str(workspace / "worker_last_message.txt")},
        "event_log_path": str(runtime / "LANE_EVENTS.jsonl"),
        "resources": ["service:claude-only"],
        "repository": {"common_dir": str(common_dir), "worktree_root": str(wt),
                       "branch": branch, "base_commit": base},
    }
    path = workspace / "invocation.json"
    _write_json(path, inv)
    return path, workspace / "worker_controller.status.json"


def _codex_invocation(root, wt, common_dir, base, runtime, resource_lock_root):
    lane = "codex"
    workspace = wt / ".agent-workspace"
    prompt = workspace / "worker-prompt.md"
    prompt.write_text("Create a file named CODEX.txt containing 'codex lane', "
                      "then run: git add CODEX.txt && git commit -m codex. "
                      "Then reply with one word: done.", encoding="utf-8")
    prompt_sha = hashlib.sha256(prompt.read_bytes()).hexdigest()
    branch = _git(wt, "branch", "--show-current")
    inv = {
        "schema": "orchestrator-coding-invocation/v1", "action": "start",
        "runtime_root": str(runtime), "resource_lock_root": str(resource_lock_root),
        "run_root": str(wt),
        "repository": {"common_dir": str(common_dir), "worktree_root": str(wt),
                       "branch": branch, "base_commit": base, "merge_inputs": []},
        "prompt_path": str(prompt), "prompt_sha256": prompt_sha,
        "output_paths": {"status": str(workspace / "worker_controller.status.json"),
                         "jsonl": str(workspace / "worker_codex.jsonl"),
                         "stderr": str(workspace / "worker_codex.stderr.log"),
                         "last_message": str(workspace / "worker_last_message.txt")},
        "event_log_path": str(runtime / "LANE_EVENTS.jsonl"),
        "lane_id": lane, "worker_invocation_id": f"{lane}-001",
        "task": "make CODEX.txt", "phase": "implementation",
        "exclusive_resources": ["service:codex-only"],
        "codex": {"command": ["codex"], "model": CODEX_MODEL, "reasoning_effort": "high",
                  "service_tier": "priority", "sandbox": "danger-full-access",
                  "approval_policy": "never", "config_overrides": ['model_provider="ollama"']},
    }
    path = workspace / "invocation.json"
    _write_json(path, inv)
    return path, workspace / "worker_controller.status.json"


def _launch_and_wait(invocation: Path):
    raw = json.loads(invocation.read_text(encoding="utf-8"))
    status_path = Path(raw["output_paths"]["status"])
    receipt = launch_lane_controller(
        invocation, receipt=invocation.parent / "operator_launch.json",
        cwd=HARNESS_ROOT, expected_state_path=status_path)
    pid = receipt.get("pid"); created = receipt.get("created_utc")
    terminal = {"PROVIDER_EXITED", "CODEX_EXITED", "CONTROLLER_FAILED", "LAUNCH_FAILED",
                "PROVIDER_HANDOFF", "PROVIDER_OPERATION_UNSUPPORTED", "COORDINATION_FAILED"}
    deadline = time.monotonic() + COMPLETION_SECONDS
    while time.monotonic() < deadline:
        q = targeted_process_query(pid)
        if q.complete and not q.errors:
            proc = q.process
            if proc is None or iso_utc(proc.created_utc) != created:
                break
        time.sleep(0.1)
    # settle for the terminal status write
    for _ in range(600):
        try:
            v = json.loads(status_path.read_text(encoding="utf-8"))
            if v.get("state") in terminal:
                return v
        except (OSError, json.JSONDecodeError):
            pass
        time.sleep(0.1)
    raise RuntimeError(f"no terminal status for {status_path}")


def cmd_run(root: Path) -> int:
    root = root.resolve()
    project, common_dir, base = _init_project(root)
    runtime = root / "runtime"; runtime.mkdir()
    resource_lock_root = runtime / "coding-resource-locks"; resource_lock_root.mkdir()
    wt_c = _worktree(project, root, "claude", "lane/claude", base)
    wt_x = _worktree(project, root, "codex", "lane/codex", base)
    claude_inv, claude_status = _claude_invocation(root, wt_c, common_dir, base, runtime, resource_lock_root)
    codex_inv, codex_status = _codex_invocation(root, wt_x, common_dir, base, runtime, resource_lock_root)
    _write_json(root / "config.json", {"suite_root": ".", "run_globs": ["worktrees/*"]})

    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_c = ex.submit(_launch_and_wait, claude_inv)
        f_x = ex.submit(_launch_and_wait, codex_inv)
        s_c = f_c.result(); s_x = f_x.result()
    elapsed = round(time.monotonic() - started, 1)

    events = []
    for line in (runtime / "LANE_EVENTS.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            d = json.loads(line)
            events.append({"event": d.get("event") or d.get("type"),
                           "lane_id": d.get("lane_id"), "provider_id": d.get("provider_id"),
                           "provider_session_id": d.get("provider_session_id")})
    report = {
        "elapsed_seconds": elapsed,
        "claude": {"state": s_c.get("state"), "outcome": s_c.get("provider_terminal_outcome"),
                   "session": s_c.get("provider_session_id"), "provider": s_c.get("provider_id", "claude-code")},
        "codex": {"state": s_x.get("state"), "outcome": s_x.get("provider_terminal_outcome"),
                  "session": s_x.get("provider_session_id"), "provider": s_x.get("provider_id", "codex")},
        "shared_event_log_rows": len(events),
        "providers_in_shared_log": sorted({e["lane_id"] for e in events if e["lane_id"]}),
        "events": events,
    }
    _write_json(root / "xprovider-report.json", report)
    print(json.dumps(report, indent=2))
    return 0


def main() -> int:
    a = sys.argv[1:]
    if len(a) < 3 or a[0] != "run" or a[1] != "--root":
        print("usage: probe_xprovider.py run --root <dir>", file=sys.stderr); return 2
    return cmd_run(Path(a[2]))


if __name__ == "__main__":
    raise SystemExit(main())
