"""Phase 0 step 0.5 probe: re-confirm the six originally-passing live behaviors.

The prior round proved these behaviors with the REAL ``claude`` CLI against the
local Ollama Anthropic-compatible endpoint.  This probe re-runs that set after
the 0.1-0.4 fixes, with the Ollama redirect flowing through the invocation's
``provider.config_overrides`` env channel (0.3) - that channel is the mechanism
under test, so the probe never sets process-level ANTHROPIC_* variables itself.

Behaviors under test (all must pass):
  1. 2-lane concurrency with genuine claude subprocesses (own worktree / file /
     branch each; no cross-lane contamination) via ``launch_lane_controller``.
  2. Provider event/evidence logging: PROVIDER_STARTED/PROVIDER_EXITED in the
     shared LANE_EVENTS.jsonl with real session_id/thread_id, provider_id
     ``claude-code``, provider_terminal_outcome COMPLETED.
  3. Transcript parsing: system/init -> STARTED, result/success -> COMPLETED
     classified from the real transcript.
  4. MISSING result detection with no RESULT.json written.
  5. --resume <session_id>: the resumed process recalls prior turn content
     (the "HELLO FROM LANE A" proof).
  6. watch --until-actionable -> WATCH_TIMEOUT for a genuinely completed lane.

Phase-0 gate: a claude lane launches with no flag error (the --verbose fix) and
is not a false-COMPLETED; the happy path is asserted here (file exists +
COMPLETED).  The denied path was proven in step 0.2.

Evidence is written to the kept fixture root under ``scratch/0.5/fixture-root``
and a per-behavior summary is printed at the end.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

# Direct execution puts ``scratch/0.5/`` first on sys.path; keep the root-level
# command equivalent to importing the harness from its package.
HARNESS_ROOT = Path(__file__).resolve().parent.parent.parent
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.models import iso_utc
from orchestrator_harness.processes import (
    WINDOWS_CREATE_NO_WINDOW,
    targeted_process_query,
)
from orchestrator_harness.profile import RuntimeProfile
from orchestrator_harness.prompt_bundle import prompt_bundle_record_from_paths
from orchestrator_harness.public_launch import launch_lane_controller
from orchestrator_harness.provider import (
    ClaudeCodeProviderAdapter,
    claude_config_override_env,
)

# The real model served by the local Ollama the config_overrides channel
# redirects to.
CLAUDE_MODEL = "deepseek-v4-flash:0731-cloud"
# The 0.3 config-overrides alias that expands (in claude_config_override_env) to
# ANTHROPIC_BASE_URL=http://localhost:11434, ANTHROPIC_AUTH_TOKEN=ollama,
# ANTHROPIC_API_KEY="".  This is the ONLY redirect the probe relies on.
CLAUDE_OLLAMA_OVERRIDE = 'model_provider="ollama"'
ANTHROPIC_KEYS = ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY")

# Bounds: each real claude lane makes a real Ollama round-trip; keep the probe
# finite (~5-10 min total).
LANE_COMPLETION_SECONDS = 200.0
WATCH_TIMEOUT_SECONDS = 3.0
CONTROLLER_EXIT_WAIT_SECONDS = 240.0

TOOLS = ["Read", "Bash", "Write", "Edit", "Glob", "Grep"]

BEHAVIORS: dict[str, dict[str, Any]] = {}


def _record(behavior: str, result: str, evidence: str, detail: str = "") -> None:
    BEHAVIORS[behavior] = {
        "result": result,
        "evidence": evidence,
        "detail": detail,
    }
    print(f"[behavior] {behavior}: {result}  ({evidence})")
    if detail:
        print(f"    detail: {detail}")


class ProbeError(RuntimeError):
    pass


def _run(
    argv: Sequence[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    expected: tuple[int, ...] = (0,),
    timeout: float = 60,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    kwargs: dict[str, Any] = dict(
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        shell=False,
        creationflags=WINDOWS_CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    if input_text is not None:
        # ``input=`` implies stdin=PIPE; passing stdin explicitly alongside
        # input is rejected by subprocess.run.
        kwargs["input"] = input_text
    else:
        kwargs["stdin"] = subprocess.DEVNULL
    completed = subprocess.run(list(argv), **kwargs)
    if completed.returncode not in expected:
        raise ProbeError(
            f"command failed ({completed.returncode}): {list(argv)!r}\n"
            f"stdout: {completed.stdout[-2000:]}\nstderr: {completed.stderr[-2000:]}"
        )
    return completed


def _git(cwd: Path, *args: str) -> str:
    return _run(("git", *args), cwd=cwd).stdout.strip()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _claude_command() -> list[str]:
    claude = shutil.which("claude")
    if not claude:
        raise ProbeError("no claude CLI on PATH; install Claude Code")
    return [claude]


def _provider_env_launcher(extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """Env-scoped launcher for DIRECT claude calls only.

    Sets the ANTHROPIC_* redirect variables on this child process only; never
    mutates the probe's own os.environ.  Mirrors the expansion produced by the
    invocation's config_overrides channel.
    """
    env = dict(os.environ)
    env["ANTHROPIC_BASE_URL"] = "http://localhost:11434"
    env["ANTHROPIC_AUTH_TOKEN"] = "ollama"
    env["ANTHROPIC_API_KEY"] = ""
    if extra:
        env.update(extra)
    return env


def _strip_anthropic_from_probe_env() -> list[str]:
    """Remove inherited ANTHROPIC_* from the probe's own environment.

    The parent harness that launched this probe routes its own claude session
    through the local Ollama and set these variables.  If they were left in the
    probe's environment the lane controller's child would inherit them, and the
    redirect would not prove the config_overrides channel.  Removing them makes
    config_overrides the ONLY possible redirect source for every lane child.
    """
    removed = sorted(key for key in ANTHROPIC_KEYS if key in os.environ)
    for key in removed:
        del os.environ[key]
    return removed


def _lane_events(runtime: Path) -> list[dict[str, Any]]:
    path = runtime / "LANE_EVENTS.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _invocation(
    *,
    lane: str,
    worktree: Path,
    common_dir: Path,
    base_commit: str,
    runtime: Path,
    prompt_text: str,
    command: Sequence[str],
    status_name: str,
    jsonl_name: str,
    stderr_name: str,
    last_message_name: str,
) -> Path:
    workspace = worktree / ".agent-workspace"
    workspace.mkdir(exist_ok=True)
    prompt = workspace / "worker-prompt.md"
    prompt.write_text(prompt_text, encoding="utf-8")
    branch = _git(worktree, "branch", "--show-current")
    worker_id = f"{lane}-001"
    card = {
        "schema": "orchestrator-task-card/v1",
        "card_id": f"card-{lane}",
        "lane_id": lane,
        "stage_cohort_id": f"cohort-{lane}",
        "worker_invocation_id": worker_id,
        "objective": f"Create {lane}-artifact.txt and commit it",
        "revision": "r1",
    }
    workflow_id = "probe-0.5"
    profile_id = f"profile-{lane}"
    profile = RuntimeProfile(
        profile_id,
        "implementer",
        "claude-code",
        CLAUDE_MODEL,
        tuple(TOOLS),
        ("repo",),
        (),
        ("CLAUDE_CONFIG_DIR", "HOME"),
    )
    bundle = prompt_bundle_record_from_paths(
        workflow_id=workflow_id,
        task_card_id=card["card_id"],
        profile_id=profile_id,
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
        "workflow": {"id": workflow_id, "version": "1"},
        "task_card": {
            "id": card["card_id"],
            "revision": card["revision"],
            "sha256": hashlib.sha256(
                json.dumps(card, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
        },
        "role": "implementer",
        "provider": {
            "id": "claude-code",
            "model": CLAUDE_MODEL,
            "command": list(command),
            "allowed_tools": TOOLS,
            # The 0.3 child-env channel.  No service_tier or approval_policy
            # may appear here (both raise for claude-code).
            "config_overrides": [CLAUDE_OLLAMA_OVERRIDE],
        },
        "profile": profile.to_record(),
        "prompt_bundle": bundle,
        "output_paths": {
            "status": str(workspace / status_name),
            "jsonl": str(workspace / jsonl_name),
            "stderr": str(workspace / stderr_name),
            "last_message": str(workspace / last_message_name),
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


def _start_controller(invocation: Path) -> dict[str, Any]:
    raw = json.loads(invocation.read_text(encoding="utf-8"))
    status_path = Path(raw["output_paths"]["status"])
    receipt_path = invocation.parent / "probe_operator_launch.json"
    return launch_lane_controller(
        invocation,
        receipt=receipt_path,
        cwd=HARNESS_ROOT,
        expected_state_path=status_path,
    )


def _wait_for_status(
    path: Path,
    predicate: Any,
    *,
    timeout: float = LANE_COMPLETION_SECONDS,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            time.sleep(0.05)
            continue
        if isinstance(value, dict) and predicate(value):
            return value
        time.sleep(0.05)
    raise ProbeError(f"timed out waiting for status condition in {path}")


def _finish_controller(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Wait for the canonical lane controller to reach a terminal state."""
    pid = receipt.get("pid")
    created_utc = receipt.get("created_utc")
    if not isinstance(pid, int) or not isinstance(created_utc, str):
        raise ProbeError(
            f"operator launch receipt has no exact process identity: {receipt}"
        )
    terminal_states = {
        "PROVIDER_EXITED",
        "CONTROLLER_FAILED",
        "LAUNCH_FAILED",
        "PROVIDER_HANDOFF",
        "PROVIDER_OPERATION_UNSUPPORTED",
        "COORDINATION_FAILED",
    }
    deadline = time.monotonic() + CONTROLLER_EXIT_WAIT_SECONDS
    while time.monotonic() < deadline:
        query = targeted_process_query(pid)
        if query.complete and not query.errors:
            process = query.process
            if process is None or iso_utc(process.created_utc) != created_utc:
                status_path = Path(str(receipt["expected_state_path"]))
                return _wait_for_status(
                    status_path,
                    lambda value: value.get("state") in terminal_states,
                )
        time.sleep(0.05)
    raise ProbeError(
        f"controller PID {pid} with creation identity {created_utc} did not exit"
    )


def _transcript_events(path: Path) -> list[tuple[str, str, str]]:
    """Parse a captured stream-json transcript via the real adapter.

    Returns (kind, outcome, detail) triples for every classified event.
    """
    adapter = ClaudeCodeProviderAdapter()
    events: list[tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            event = adapter.parse_transcript_line(line.encode("utf-8"))
        except Exception:  # defensive: never let one line break the probe
            continue
        if event is not None:
            events.append((event.kind, event.outcome or "", event.detail or ""))
    return events


def _assistant_texts(path: Path) -> list[str]:
    """Extract assistant text content from a stream-json transcript."""
    texts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if value.get("type") != "assistant":
            continue
        message = value.get("message")
        if not isinstance(message, Mapping):
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, Mapping) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str) and text.strip():
                    texts.append(text.strip())
    return texts


def _normalize(value: str) -> str:
    return " ".join(value.lower().replace('"', "").replace("'", "").split())


def run_probe(root: Path) -> dict[str, Any]:
    root = root.resolve()
    project = root / "project"
    worktrees = root / "worktrees"
    runtime = root / "runtime"
    project.mkdir(parents=True)
    worktrees.mkdir()
    runtime.mkdir()

    # ---- environment setup: prove the redirect must come from config_overrides
    removed = _strip_anthropic_from_probe_env()
    claude_config_dir = root / "claude-config-dir"
    claude_config_dir.mkdir(exist_ok=True)
    os.environ["CLAUDE_CONFIG_DIR"] = str(claude_config_dir)
    print(f"[env] removed inherited ANTHROPIC_* from probe env: {removed}")
    print(f"[env] CLAUDE_CONFIG_DIR for all lane children: {claude_config_dir}")
    assert not any(
        key in os.environ for key in ANTHROPIC_KEYS
    ), "probe env still carries ANTHROPIC_*"
    expansion = dict(claude_config_override_env(CLAUDE_OLLAMA_OVERRIDE))
    print(f"[env] claude_config_override_env expansion: {expansion}")

    # ---- git fixture project with two lane worktrees
    _git(project, "init", "-b", "main")
    _git(project, "config", "user.email", "probe@example.invalid")
    _git(project, "config", "user.name", "Phase 0.5 Probe")
    (project / "README.md").write_text("# Probe project\n", encoding="utf-8")
    (project / ".gitignore").write_text(".agent-workspace/\n", encoding="utf-8")
    _git(project, "add", "README.md", ".gitignore")
    _git(project, "commit", "-m", "Initial probe project")
    base_commit = _git(project, "rev-parse", "HEAD")
    common_dir = (project / ".git").resolve()
    alpha = worktrees / "lane-alpha"
    beta = worktrees / "lane-beta"
    _git(project, "worktree", "add", "-b", "lane/alpha", str(alpha), base_commit)
    _git(project, "worktree", "add", "-b", "lane/beta", str(beta), base_commit)

    command = _claude_command()

    # ---- behavior 1+2: launch two genuine claude lanes concurrently
    alpha_prompt = (
        "Perform exactly this task in the current directory:\n"
        "\n"
        "1. Create a file named alpha-artifact.txt whose content is exactly this "
        "single line:\n"
        "\n"
        "   HELLO FROM LANE A\n"
        "\n"
        "2. Stage and commit it:\n"
        "\n"
        "   git add alpha-artifact.txt\n"
        "   git commit -m \"add alpha artifact\"\n"
        "\n"
        "Then reply with one short line containing the commit hash. Do not modify "
        "any other file and do not ask questions.\n"
    )
    beta_prompt = (
        "Perform exactly this task in the current directory:\n"
        "\n"
        "1. Create a file named beta-artifact.txt whose content is exactly this "
        "single line:\n"
        "\n"
        "   HELLO FROM LANE B\n"
        "\n"
        "2. Stage and commit it:\n"
        "\n"
        "   git add beta-artifact.txt\n"
        "   git commit -m \"add beta artifact\"\n"
        "\n"
        "Then reply with one short line containing the commit hash. Do not modify "
        "any other file and do not ask questions.\n"
    )

    alpha_inv = _invocation(
        lane="lane-alpha",
        worktree=alpha,
        common_dir=common_dir,
        base_commit=base_commit,
        runtime=runtime,
        prompt_text=alpha_prompt,
        command=command,
        status_name="worker_alpha.status.json",
        jsonl_name="worker_alpha.jsonl",
        stderr_name="worker_alpha.stderr.log",
        last_message_name="worker_alpha_last_message.txt",
    )
    beta_inv = _invocation(
        lane="lane-beta",
        worktree=beta,
        common_dir=common_dir,
        base_commit=base_commit,
        runtime=runtime,
        prompt_text=beta_prompt,
        command=command,
        status_name="worker_beta.status.json",
        jsonl_name="worker_beta.jsonl",
        stderr_name="worker_beta.stderr.log",
        last_message_name="worker_beta_last_message.txt",
    )

    print("[concurrency] launching alpha + beta controllers simultaneously ...")
    launch_start = time.monotonic()
    alpha_receipt = _start_controller(alpha_inv)
    beta_receipt = _start_controller(beta_inv)
    alpha_status_path = alpha / ".agent-workspace" / "worker_alpha.status.json"
    beta_status_path = beta / ".agent-workspace" / "worker_beta.status.json"

    alpha_status: dict[str, Any] = {}
    beta_status: dict[str, Any] = {}
    alpha_error: str | None = None
    beta_error: str | None = None
    try:
        alpha_status = _finish_controller(alpha_receipt)
    except ProbeError as exc:
        alpha_error = str(exc)
    try:
        beta_status = _finish_controller(beta_receipt)
    except ProbeError as exc:
        beta_error = str(exc)
    launch_elapsed = time.monotonic() - launch_start
    print(f"[concurrency] both controllers terminal after {launch_elapsed:.1f}s")

    # behavior 1: concurrency + isolation
    b1_messages: list[str] = []
    b1_pass = True
    if alpha_error or beta_error:
        b1_pass = False
        b1_messages.append(f"controller errors alpha={alpha_error!r} beta={beta_error!r}")
    if b1_pass:
        for name, worktree, status, other_file in (
            ("alpha", alpha, alpha_status, "beta-artifact.txt"),
            ("beta", beta, beta_status, "alpha-artifact.txt"),
        ):
            artifact = worktree / f"{name}-artifact.txt"
            if not artifact.is_file():
                b1_pass = False
                b1_messages.append(f"{name}: {artifact.name} not created")
            if (worktree / other_file).exists():
                b1_pass = False
                b1_messages.append(f"{name}: cross-lane file {other_file} present")
        branch_alpha = _git(alpha, "branch", "--show-current")
        branch_beta = _git(beta, "branch", "--show-current")
        if branch_alpha != "lane/alpha":
            b1_pass = False
            b1_messages.append(f"alpha on wrong branch {branch_alpha!r}")
        if branch_beta != "lane/beta":
            b1_pass = False
            b1_messages.append(f"beta on wrong branch {branch_beta!r}")
        alpha_head = _git(alpha, "rev-parse", "HEAD")
        beta_head = _git(beta, "rev-parse", "HEAD")
        if alpha_head == base_commit:
            b1_pass = False
            b1_messages.append("alpha made no commit")
        if beta_head == base_commit:
            b1_pass = False
            b1_messages.append("beta made no commit")
        alpha_files = _git(alpha, "diff", "--name-only", f"{base_commit}..{alpha_head}").split()
        beta_files = _git(beta, "diff", "--name-only", f"{base_commit}..{beta_head}").split()
        if alpha_files != ["alpha-artifact.txt"]:
            b1_pass = False
            b1_messages.append(f"alpha commit touched {alpha_files!r}")
        if beta_files != ["beta-artifact.txt"]:
            b1_pass = False
            b1_messages.append(f"beta commit touched {beta_files!r}")
    _record(
        "1-lane-concurrency",
        "PASS" if b1_pass else "FAIL",
        "fixture-root/worktrees + git diff",
        "; ".join(b1_messages) or "each lane touched only its own file and branch",
    )

    # behavior 2: provider event/evidence logging
    events = _lane_events(runtime)
    started = [row for row in events if row.get("event") == "PROVIDER_STARTED"]
    exited = [row for row in events if row.get("event") == "PROVIDER_EXITED"]
    b2_messages: list[str] = []
    b2_pass = len(started) >= 2 and len(exited) >= 2
    for lane_prefix, status in (("lane-alpha", alpha_status), ("lane-beta", beta_status)):
        lane_started = [row for row in started if row.get("declared_lane_id") == lane_prefix]
        lane_exited = [row for row in exited if row.get("declared_lane_id") == lane_prefix]
        if not lane_started or not lane_exited:
            b2_pass = False
            b2_messages.append(f"{lane_prefix}: missing STARTED/EXITED")
            continue
        row = lane_started[0]
        if row.get("provider_id") != "claude-code":
            b2_pass = False
            b2_messages.append(f"{lane_prefix}: provider_id {row.get('provider_id')!r}")
        ex = lane_exited[0]
        if ex.get("provider_terminal_outcome") != "COMPLETED":
            b2_pass = False
            b2_messages.append(
                f"{lane_prefix}: outcome {ex.get('provider_terminal_outcome')!r}"
            )
        if not isinstance(ex.get("session_id"), str) or not ex["session_id"].strip():
            b2_pass = False
            b2_messages.append(f"{lane_prefix}: empty session_id in EXITED")
        if not isinstance(ex.get("thread_id"), str) or not ex["thread_id"].strip():
            b2_pass = False
            b2_messages.append(f"{lane_prefix}: empty thread_id in EXITED")
    _record(
        "2-provider-event-logging",
        "PASS" if b2_pass else "FAIL",
        "fixture-root/runtime/LANE_EVENTS.jsonl",
        "; ".join(b2_messages) or "STARTED/EXITED for both lanes with session/thread ids",
    )

    # behavior 3: transcript parsing (STARTED/COMPLETED)
    b3_pass = True
    b3_messages: list[str] = []
    for name, worktree, status in (
        ("alpha", alpha, alpha_status),
        ("beta", beta, beta_status),
    ):
        transcript = worktree / ".agent-workspace" / f"worker_{name}.jsonl"
        kinds = _transcript_events(transcript)
        kinds_list = [kind for kind, _, _ in kinds]
        if "STARTED" not in kinds_list:
            b3_pass = False
            b3_messages.append(f"{name}: no STARTED in transcript")
        if "COMPLETED" not in kinds_list:
            b3_pass = False
            b3_messages.append(f"{name}: no COMPLETED in transcript")
        if status.get("provider_terminal_outcome") != "COMPLETED":
            b3_pass = False
            b3_messages.append(f"{name}: status outcome {status.get('provider_terminal_outcome')!r}")
    _record(
        "3-transcript-parse",
        "PASS" if b3_pass else "FAIL",
        "fixture-root/worktrees/*/worker_*.jsonl",
        "; ".join(b3_messages) or "init->STARTED and success->COMPLETED from real transcript",
    )

    # behavior 4: MISSING result detection (no RESULT.json written)
    b4_pass = True
    b4_messages: list[str] = []
    for name, worktree, status in (
        ("alpha", alpha, alpha_status),
        ("beta", beta, beta_status),
    ):
        validation = status.get("result_validation")
        if not isinstance(validation, Mapping) or validation.get("state") != "MISSING":
            b4_pass = False
            b4_messages.append(f"{name}: result_validation={validation!r}")
        if (worktree / ".agent-workspace" / "RESULT.json").exists():
            b4_pass = False
            b4_messages.append(f"{name}: RESULT.json unexpectedly present")
    _record(
        "4-missing-result",
        "PASS" if b4_pass else "FAIL",
        "fixture-root/worktrees/*/worker_*.status.json",
        "; ".join(b4_messages) or "result_validation.state == MISSING for both lanes",
    )

    # ---- phase-0 gate (happy path)
    gate_messages: list[str] = []
    gate_pass = True
    adapter = ClaudeCodeProviderAdapter()
    from orchestrator_harness.provider import ProviderLaunchSpec

    sample_spec = ProviderLaunchSpec(
        action="start",
        command=tuple(command),
        model=CLAUDE_MODEL,
        reasoning_effort="normal",
        service_tier="default",
        session_id=None,
        run_root=alpha,
        last_message_path=alpha / ".agent-workspace" / "gate-last",
        config_overrides=(CLAUDE_OLLAMA_OVERRIDE,),
    )
    sample_argv = adapter.build_argv(sample_spec)
    if "--verbose" not in sample_argv:
        gate_pass = False
        gate_messages.append("build_argv missing --verbose")
    if "--permission-mode" not in sample_argv:
        gate_pass = False
        gate_messages.append("build_argv missing --permission-mode")
    if "bypassPermissions" not in sample_argv:
        gate_pass = False
        gate_messages.append("build_argv missing bypassPermissions default")
    if not (alpha / "alpha-artifact.txt").is_file():
        gate_pass = False
        gate_messages.append("alpha-artifact.txt missing (happy path artifact)")
    if alpha_status.get("provider_terminal_outcome") != "COMPLETED":
        gate_pass = False
        gate_messages.append(
            f"alpha outcome {alpha_status.get('provider_terminal_outcome')!r} != COMPLETED"
        )
    _record(
        "gate-happy-path",
        "PASS" if gate_pass else "FAIL",
        "gate-proof.txt + alpha-artifact.txt exists",
        "; ".join(gate_messages) or "no flag error; real lane COMPLETED with artifact committed",
    )

    # ---- behavior 5: --resume <session_id> recall proof
    session_id = alpha_status.get("provider_session_id")
    resume_result: dict[str, Any] = {"attempted": False}
    if isinstance(session_id, str) and session_id.strip():
        resume_transcript = root / "resume-transcript.jsonl"
        resume_question = (
            "In this conversation you were given an earlier instruction that told "
            "you to create a file and write one specific line of content into it. "
            "Reply with ONLY that exact content line and nothing else.\n"
        )
        resume_argv = [
            *command,
            "--print",
            "--output-format",
            "stream-json",
            "--verbose",
            "--resume",
            session_id,
            "--model",
            CLAUDE_MODEL,
            "--permission-mode",
            "bypassPermissions",
        ]
        print(f"[resume] launching direct --resume {session_id}")
        try:
            completed = _run(
                resume_argv,
                cwd=alpha,
                env=_provider_env_launcher(),
                timeout=LANE_COMPLETION_SECONDS,
                input_text=resume_question,
            )
            lines = [ln for ln in completed.stdout.splitlines() if ln.strip()]
            resume_transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
            texts = _assistant_texts(resume_transcript)
            reply = " | ".join(texts[-3:])
            resume_result = {
                "attempted": True,
                "returncode": completed.returncode,
                "session_id": session_id,
                "reply_excerpt": reply[:500],
            }
            found = any("hello from lane a" in _normalize(text) for text in texts)
            b5_pass = completed.returncode == 0 and found
            b5_messages = [f"returncode={completed.returncode}"]
            if not found:
                b5_messages.append(
                    f"reply does not recall content; texts={[t[:80] for t in texts]}"
                )
            (root / "resume-proof.txt").write_text(
                json.dumps(resume_result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        except ProbeError as exc:
            b5_pass = False
            b5_messages = [f"probe error: {exc}"]
            resume_result["error"] = str(exc)
        _record(
            "5-resume",
            "PASS" if b5_pass else "FAIL",
            "resume-proof.txt + resume-transcript.jsonl",
            "; ".join(b5_messages) or "resumed real session recalls HELLO FROM LANE A",
        )
    else:
        _record(
            "5-resume",
            "FAIL",
            "resume-proof.txt",
            f"no provider_session_id captured: {session_id!r}",
        )

    # ---- behavior 6: watch --until-actionable -> WATCH_TIMEOUT
    watch_config = {
        "suite_root": ".",
        "run_globs": ["worktrees/*"],
        "workspace_relpath": ".agent-workspace",
        "output_dir": "runtime/watch-epoch",
        "poll_interval_seconds": 0.2,
        "watch_timeout_seconds": WATCH_TIMEOUT_SECONDS,
        "request_warning_seconds": 120,
        "request_critical_seconds": 30,
        "process_start_tolerance_seconds": 2,
        "max_json_bytes": 4000000,
        "max_jsonl_tail_bytes": 512000,
        "stable_read_retries": 4,
        "stable_read_delay_seconds": 0.03,
    }
    watch_config_path = root / "watch-config.json"
    _write_json(watch_config_path, watch_config)
    try:
        watch_completed = _run(
            [
                sys.executable,
                "-m",
                "orchestrator_harness",
                "--config",
                str(watch_config_path),
                "watch",
                "--until-actionable",
                "--timeout",
                str(WATCH_TIMEOUT_SECONDS),
            ],
            cwd=root,
            # The watch runs from the fixture root (relative suite paths in the
            # config); the harness package must be importable there.
            env={**dict(os.environ), "PYTHONPATH": str(HARNESS_ROOT)},
            expected=(0, 1, 2, 3),
            timeout=60,
        )
        watch_output = watch_completed.stdout + watch_completed.stderr
        (root / "watch-result.txt").write_text(
            f"exit_code={watch_completed.returncode}\n---\n{watch_output}",
            encoding="utf-8",
        )
        b6_pass = (
            watch_completed.returncode == 3 and "WATCH_TIMEOUT" in watch_output
        )
        _record(
            "6-watch-timeout",
            "PASS" if b6_pass else "FAIL",
            "watch-result.txt",
            f"exit_code={watch_completed.returncode}; "
            f"WATCH_TIMEOUT in output: {'WATCH_TIMEOUT' in watch_output}",
        )
    except ProbeError as exc:
        (root / "watch-result.txt").write_text(f"error: {exc}\n", encoding="utf-8")
        _record("6-watch-timeout", "FAIL", "watch-result.txt", f"probe error: {exc}")

    # ---- gate proof file (file-exists + outcome assertions output)
    gate_lines = [
        "PHASE 0 GATE PROOF",
        "==================",
        f"probe env ANTHROPIC_* inherited and removed: {removed}",
        f"config_overrides expansion: {json.dumps(expansion)}",
        f"adapter argv includes --verbose: {'--verbose' in sample_argv}",
        f"adapter argv includes --permission-mode bypassPermissions: {'bypassPermissions' in sample_argv}",
        f"alpha-artifact.txt exists: {(alpha / 'alpha-artifact.txt').is_file()}",
        f"alpha-artifact.txt content: {alpha / 'alpha-artifact.txt'!s}",
        f"alpha provider_terminal_outcome: {alpha_status.get('provider_terminal_outcome')!r}",
        f"alpha state: {alpha_status.get('state')!r}",
        f"alpha exit_code: {alpha_status.get('exit_code')!r}",
        f"alpha provider_session_id: {alpha_status.get('provider_session_id')!r}",
        f"alpha branch: {alpha_status.get('branch')!r}",
        f"beta provider_terminal_outcome: {beta_status.get('provider_terminal_outcome')!r}",
        f"beta state: {beta_status.get('state')!r}",
        f"beta provider_session_id: {beta_status.get('provider_session_id')!r}",
        f"beta branch: {beta_status.get('branch')!r}",
        "",
        "GATE VERDICT: " + ("PASS" if gate_pass else "FAIL"),
    ]
    try:
        artifact_text = (alpha / "alpha-artifact.txt").read_text(encoding="utf-8")
        gate_lines.append(f"alpha-artifact.txt raw content: {artifact_text!r}")
    except OSError:
        gate_lines.append("alpha-artifact.txt raw content: <missing>")
    (root / "gate-proof.txt").write_text("\n".join(gate_lines) + "\n", encoding="utf-8")

    return {
        "schema": "orchestrator-0.5-probe/v1",
        "model": CLAUDE_MODEL,
        "config_overrides": [CLAUDE_OLLAMA_OVERRIDE],
        "inherited_anthropic_removed": removed,
        "lanes": {
            "alpha": {
                "state": alpha_status.get("state"),
                "outcome": alpha_status.get("provider_terminal_outcome"),
                "exit_code": alpha_status.get("exit_code"),
                "session_id": alpha_status.get("provider_session_id"),
                "branch": alpha_status.get("branch"),
                "result_validation": alpha_status.get("result_validation"),
                "error": alpha_error,
            },
            "beta": {
                "state": beta_status.get("state"),
                "outcome": beta_status.get("provider_terminal_outcome"),
                "exit_code": beta_status.get("exit_code"),
                "session_id": beta_status.get("provider_session_id"),
                "branch": beta_status.get("branch"),
                "result_validation": beta_status.get("result_validation"),
                "error": beta_error,
            },
        },
        "resume": resume_result,
        "concurrency_elapsed_s": round(launch_elapsed, 1),
        "events": {"started": len(started), "exited": len(exited)},
        "behaviors": BEHAVIORS,
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    keep_root: Path | None = None
    if args:
        if len(args) != 2 or args[0] != "--keep":
            print(
                "usage: probe.py [--keep DIRECTORY]",
                file=sys.stderr,
            )
            return 2
        keep_root = Path(args[1]).resolve()
        if keep_root.exists():
            print("--keep DIRECTORY must not already exist", file=sys.stderr)
            return 2
        keep_root.mkdir(parents=True)
    try:
        if keep_root is not None:
            result = run_probe(keep_root)
            result["cleanup"] = "retained by --keep"
        else:
            import tempfile

            with tempfile.TemporaryDirectory(prefix="probe-0.5-") as temporary:
                temporary_path = Path(temporary)
                result = run_probe(temporary_path)
            result["cleanup"] = "temporary repository removed"
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ProbeError, OSError, ValueError, json.JSONDecodeError) as exc:
        if keep_root is not None:
            print(f"probe failed; retained at {keep_root}: {exc}", file=sys.stderr)
        else:
            print(f"probe failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
