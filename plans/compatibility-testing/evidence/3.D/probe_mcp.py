"""3.D MCP under Claude+Ollama — one bounded live attempt.

Wires a local stdio MCP server (mcp_marker_server.py, no SDK) into a real
claude-code lane via the harness invocation's provider.mcp_config channel, then
launches the lane against the local Ollama backend and observes whether:
  (a) the harness threads --mcp-config into the claude argv (wiring), and
  (b) the model reaches through the MCP transport and calls the tool
      (a written marker file is authentic proof of a completed MCP round-trip).

Bounded: single lane, single turn.  Quota-safe (local Ollama).  Session-local:
CLAUDE_CONFIG_DIR pinned into <root>/claude-config (fresh dir => no other MCP
servers), Ollama redirect via config_overrides model_provider="ollama".  No
~/.claude / global writes.
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
LANE = "mcp"
COHORT = "cohort-mcp"
COMPLETION_SECONDS = 420
MARKER_TEXT = "MCP-3D-OK"
SERVER = Path(__file__).resolve().parent / "mcp_marker_server.py"


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
    (project / "README.md").write_text("# mcp\n", encoding="utf-8")
    (project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
    _git(project, "add", "README.md", ".gitignore")
    _git(project, "commit", "-m", "init")
    base = _git(project, "rev-parse", "HEAD")
    return project, (project / ".git").resolve(), base


def _invocation(root, wt, common_dir, base, runtime, marker_path):
    workspace = wt / ".agent-workspace"
    workspace.mkdir(exist_ok=True)
    prompt = workspace / "worker-prompt.md"
    prompt.write_text(
        "You have an MCP tool available named record_marker (server 'marker'). "
        f"Call the tool mcp__marker__record_marker with text exactly '{MARKER_TEXT}'. "
        "Do not create any files yourself; use ONLY the MCP tool. "
        "After the tool returns, reply with one word: done.",
        encoding="utf-8")
    branch = _git(wt, "branch", "--show-current")
    worker_id = f"{LANE}-001"
    card = {"schema": "orchestrator-task-card/v1", "card_id": f"card-{LANE}",
            "lane_id": LANE, "stage_cohort_id": COHORT,
            "worker_invocation_id": worker_id, "objective": "call MCP marker tool",
            "revision": "r1"}
    card_sha = hashlib.sha256(json.dumps(card, sort_keys=True,
                              separators=(",", ":")).encode()).hexdigest()
    mcp_tool = "mcp__marker__record_marker"
    tools = ["Read", "Bash", mcp_tool]
    mcp_config = {"mcpServers": {"marker": {
        "command": sys.executable,
        "args": [str(SERVER)],
        "env": {"MCP_MARKER_PATH": str(marker_path)},
    }}}
    profile = {"schema": "orchestrator-runtime-profile/v1", "id": f"profile-{LANE}",
               "role": "implementer", "provider": "claude-code", "model": CLAUDE_MODEL,
               "tools": tools, "capabilities": ["repo"], "resources": [],
               "provider_needs": ["CLAUDE_CONFIG_DIR", "HOME"]}
    bundle = prompt_bundle_record_from_paths(
        workflow_id="mcp", task_card_id=card["card_id"],
        profile_id=f"profile-{LANE}", paths=(("instructions", prompt),), run_root=wt)
    inv = {
        "schema": "orchestrator-worker-invocation/v1", "action": "start",
        "run_root": str(wt), "runtime_root": str(runtime), "lane_id": LANE,
        "worker_invocation_id": worker_id, "cohort_id": COHORT,
        "workflow": {"id": "mcp", "version": "1"},
        "task_card": {"id": card["card_id"], "revision": "r1", "sha256": card_sha},
        "role": "implementer",
        "provider": {"id": "claude-code", "model": CLAUDE_MODEL,
                     "command": [shutil.which("claude")],
                     "allowed_tools": tools,
                     "config_overrides": ['model_provider="ollama"'],
                     "mcp_config": mcp_config},
        "profile": profile, "prompt_bundle": bundle,
        "output_paths": {"status": str(workspace / "worker_controller.status.json"),
                         "jsonl": str(workspace / "worker_claude.jsonl"),
                         "stderr": str(workspace / "worker_claude.stderr.log"),
                         "last_message": str(workspace / "worker_last_message.txt")},
        "event_log_path": str(runtime / "LANE_EVENTS.jsonl"),
        "resources": [],
        "repository": {"common_dir": str(common_dir), "worktree_root": str(wt),
                       "branch": branch, "base_commit": base},
    }
    path = workspace / "invocation.json"
    _write_json(path, inv)
    return path, workspace / "worker_controller.status.json"


def _launch_and_wait(invocation: Path, status_path: Path):
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
        time.sleep(0.2)
    for _ in range(600):
        try:
            v = json.loads(status_path.read_text(encoding="utf-8"))
            if v.get("state") in terminal:
                return v
        except (OSError, json.JSONDecodeError):
            pass
        time.sleep(0.2)
    raise RuntimeError(f"no terminal status for {status_path}")


def cmd_run(root: Path) -> int:
    root = root.resolve()
    # Session-local env: fresh config dir (no other MCP servers) + 180k window.
    cfg = root / "claude-config"; cfg.mkdir(parents=True, exist_ok=True)
    os.environ["CLAUDE_CONFIG_DIR"] = str(cfg)
    os.environ["CLAUDE_CODE_AUTO_COMPACT_WINDOW"] = "180000"
    os.environ["CLAUDE_CODE_MAX_CONTEXT_TOKENS"] = "200000"

    project, common_dir, base = _init_project(root)
    runtime = root / "runtime"; runtime.mkdir()
    wt = root / "worktrees" / f"lane-{LANE}"
    _git(project, "worktree", "add", "-b", f"lane/{LANE}", str(wt), base)
    marker_path = root / "mcp_marker.txt"
    inv, status_path = _invocation(root, wt, common_dir, base, runtime, marker_path)
    _write_json(root / "config.json", {"suite_root": ".", "run_globs": ["worktrees/*"]})

    status = _launch_and_wait(inv, status_path)

    # Wiring proof: did the claude argv actually carry --mcp-config?
    from orchestrator_harness.lane_controller import load_invocation, _provider_launch_spec
    from orchestrator_harness.provider import provider_adapter
    argv_has_mcp = None
    argv_snapshot = None
    try:
        wi = load_invocation(inv)
        spec = _provider_launch_spec(wi, None)
        argv = provider_adapter("claude-code").build_argv(spec)
        argv_has_mcp = "--mcp-config" in argv
        argv_snapshot = argv
    except Exception as exc:  # wiring introspection best-effort
        argv_has_mcp = f"introspection-error: {exc}"

    marker_written = marker_path.exists()
    marker_value = marker_path.read_text(encoding="utf-8").strip() if marker_written else None

    events = []
    log = runtime / "LANE_EVENTS.jsonl"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                d = json.loads(line)
                events.append({"event": d.get("event") or d.get("type"),
                               "lane_id": d.get("lane_id"),
                               "session": d.get("provider_session_id")})

    report = {
        "bounded_attempt": True,
        "lane_state": status.get("state"),
        "provider_terminal_outcome": status.get("provider_terminal_outcome"),
        "provider_session_id": status.get("provider_session_id"),
        "argv_has_mcp_config": argv_has_mcp,
        "argv_snapshot": argv_snapshot,
        "marker_written": marker_written,
        "marker_value": marker_value,
        "marker_matches": marker_value == MARKER_TEXT,
        "events": events,
    }
    _write_json(root / "mcp-report.json", report)
    print(json.dumps(report, indent=2))
    return 0


def main() -> int:
    a = sys.argv[1:]
    if len(a) < 3 or a[0] != "run" or a[1] != "--root":
        print("usage: probe_mcp.py run --root <dir>", file=sys.stderr); return 2
    return cmd_run(Path(a[2]))


if __name__ == "__main__":
    raise SystemExit(main())
