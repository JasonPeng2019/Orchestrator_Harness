from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from orchestrator_harness.attention_sprint import (
    event_selection_snapshot,
    formal_baseline_snapshot,
    invocation_snapshot,
    validate_sprint_finalize,
)
from orchestrator_harness.config import load_config

AUDIT = Path(__file__).resolve().parent
EPOCH = "20260801-attention-r11-repair011-readiness"
SESSION = "readiness-session"
INVOCATION = "readiness-invocation"
WATCHER_CONFIG = AUDIT / "watcher-config.json"


def utc(offset: float = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset)).isoformat().replace("+00:00", "Z")


def poll() -> None:
    subprocess.run(["python", "-m", "harness_watcher_implementation", "--config", str(WATCHER_CONFIG), "poll"], cwd=ROOT, check=True, capture_output=True, text=True)


def record(role: str, source: str, event: str, kind: str, metadata: dict) -> None:
    path = AUDIT / f"{kind}-{event}.metadata.json"
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    subprocess.run([
        "python", "-m", "harness_watcher_implementation", "--config", str(WATCHER_CONFIG),
        "record-attention", "--role", role, "--source-id", source,
        "--epoch-id", EPOCH, "--event-id", event, "--kind", kind,
        "--metadata-file", str(path),
    ], cwd=ROOT, check=True, capture_output=True, text=True)
    poll()


def manager(**extra: object) -> dict:
    return {"manager_session_id": SESSION, "manager_invocation_id": INVOCATION, **extra}


def main() -> None:
    runtime = ROOT / "harness_watcher" / "runs" / EPOCH
    if runtime.exists():
        shutil.rmtree(runtime)
    ordinary = AUDIT / "ordinary.jsonl"
    ordinary.write_text("", encoding="utf-8")
    primary = AUDIT / "primary-boundary-config.json"
    primary.write_text(json.dumps({
        "suite_root": "../../..", "run_globs": ["fresh-experiments/A22_20260726-062324"],
        "output_dir": "repair011-readiness-state", "manager_review_interval_seconds": 60,
        "manager_heartbeat_timeout_seconds": 600, "attention_sprint_lifetime_seconds": 300,
        "attention_logging_enabled": True, "attention_epoch_id": EPOCH,
    }, indent=2), encoding="utf-8")
    boundary = load_config(primary)
    WATCHER_CONFIG.write_text(json.dumps({
        "poll_interval_seconds": 1,
        "observed_sources": [{"path": str(ordinary.relative_to(ROOT)).replace("\\", "/"), "role": "orchestrator", "source_id": "ordinary"}],
        "runtime_root": str(runtime.relative_to(ROOT)).replace("\\", "/"),
        "no_progress_seconds": 900, "max_tail_bytes": 65536,
        "evaluator_command": ["python", "-c", "raise SystemExit(0)"],
        "attention_logging_enabled": True, "attention_lock_timeout_seconds": 5,
        "attention_producers": [
            {"role": "orchestrator", "source_id": "root"},
            {"role": "subagent", "source_id": "lane"},
            {"role": "subagent", "source_id": "watcher-observer"},
        ],
    }, indent=2), encoding="utf-8")

    deadline = utc(60)
    pending = [
        {"event_id": "healthy", "type": "HELP", "priority": 1, "age_seconds": 0, "agent_blocked": True, "response_deadline_utc": deadline},
        {"event_id": "expired", "type": "HELP", "priority": 2, "age_seconds": 0, "agent_blocked": True, "response_deadline_utc": deadline},
    ]
    record("orchestrator", "root", "invocation", "MANAGER_INVOCATION_STARTED", manager(pending_work_snapshot=invocation_snapshot(pending)))
    record("orchestrator", "root", "baseline-activation", "FORMAL_REVIEW_BASELINE_ADVANCED", {"pending_work_snapshot": formal_baseline_snapshot(pending)})
    for event in ("healthy", "expired"):
        record("subagent", "lane", event, "AGENT_SIGNAL_CREATED", {"lane_id": "readiness:lane:test", "agent_blocked": True, "response_deadline_utc": deadline})
        record("subagent", "watcher-observer", event, "WATCHER_NOTIFICATION_SENT", {"wake_transport": "collaboration.send_message", "delivery_succeeded": True, "response_deadline_utc": deadline})
        record("orchestrator", "root", event, "MANAGER_EVENT_CLAIMED", manager(manager_state="READING_EVENT", pending_work_snapshot=event_selection_snapshot(pending, event_id=event)))
    record("orchestrator", "root", "healthy", "MANAGER_RESPONSE_PUBLISHED", manager(manager_state="READING_EVENT"))
    record("subagent", "lane", "healthy", "AGENT_RESPONSE_RECEIVED", {"lane_id": "readiness:lane:test"})
    record("subagent", "lane", "healthy", "AGENT_WORK_RESUMED", {"lane_id": "readiness:lane:test"})
    record("subagent", "lane", "expired", "AGENT_GATE_EXPIRED", {"lane_id": "readiness:lane:test", "terminal_gate_expired": True})
    record("orchestrator", "root", "review", "MANAGER_REVIEW_STARTED", manager(manager_state="READING_EVENT", formal_review_due_utc=utc(10)))
    record("orchestrator", "root", "baseline-post-review", "FORMAL_REVIEW_BASELINE_ADVANCED", {"pending_work_snapshot": formal_baseline_snapshot([])})
    record("orchestrator", "root", "invocation", "MANAGER_INVOCATION_FINISHED", manager(pending_work_snapshot=invocation_snapshot([])))
    poll()

    timeline = [json.loads(line) for line in (runtime / "watcher" / "attention-timeline.jsonl").read_text(encoding="utf-8").splitlines() if line]
    validate_sprint_finalize(timeline, epoch_id=EPOCH)
    report = json.loads((runtime / "watcher" / "attention-report.json").read_text(encoding="utf-8"))
    findings = {item["event_id"]: item["classification"] for item in report["events"]}
    verdict = {
        "schema": "attention-repair011-readiness/v1", "epoch_id": EPOCH,
        "boundary_lifetime_seconds": boundary.attention_sprint_lifetime_seconds,
        "heartbeat_timeout_seconds": boundary.manager_heartbeat_timeout_seconds,
        "cursor_drained": report["cursor_drained"], "observation_error_count": len(report["observation_errors"]),
        "healthy_classification": findings["healthy"], "terminal_expired_present": any(row.get("kind") == "AGENT_GATE_EXPIRED" for row in timeline),
        "finalize_passed": True,
    }
    verdict["passed"] = verdict["cursor_drained"] is True and verdict["observation_error_count"] == 0 and verdict["healthy_classification"] == "NO_BLOCKING_IMPACT" and verdict["terminal_expired_present"] is True
    (AUDIT / "READINESS_VERDICT.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    print(json.dumps(verdict, indent=2))
    if not verdict["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
