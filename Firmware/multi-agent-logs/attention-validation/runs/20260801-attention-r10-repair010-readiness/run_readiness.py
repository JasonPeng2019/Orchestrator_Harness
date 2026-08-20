from __future__ import annotations

import json
import subprocess
import time
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = Path(__file__).resolve().parent
CONFIG = AUDIT / "readiness-config.json"
EPOCH = "20260801-attention-r10-repair010-readiness"
SESSION = "readiness-session"
INVOCATION = "readiness-invocation"


def utc(offset: float = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset)).isoformat().replace("+00:00", "Z")


def poll() -> None:
    subprocess.run(["python", "-m", "harness_watcher_implementation", "--config", str(CONFIG), "poll"], cwd=ROOT, check=True, capture_output=True, text=True)


def record(role: str, source: str, event: str, kind: str, metadata: dict) -> str:
    path = AUDIT / f"{kind}-{event}.metadata.json"
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    result = subprocess.run([
        "python", "-m", "harness_watcher_implementation", "--config", str(CONFIG),
        "record-attention", "--role", role, "--source-id", source,
        "--epoch-id", EPOCH, "--event-id", event, "--kind", kind,
        "--metadata-file", str(path),
    ], cwd=ROOT, check=True, capture_output=True, text=True)
    poll()
    return json.loads(result.stdout)["record_id"]


def manager(**extra: object) -> dict:
    return {"manager_session_id": SESSION, "manager_invocation_id": INVOCATION, **extra}


def main() -> None:
    runtime = ROOT / "harness_watcher" / "runs" / EPOCH
    if runtime.exists():
        shutil.rmtree(runtime)
    ordinary = AUDIT / "ordinary-source.jsonl"
    ordinary.write_text("", encoding="utf-8")
    CONFIG.write_text(json.dumps({
        "poll_interval_seconds": 1,
        "observed_sources": [{"path": str(ordinary.relative_to(ROOT)).replace("\\", "/"), "role": "orchestrator", "source_id": "ordinary-readiness"}],
        "runtime_root": str(runtime.relative_to(ROOT)).replace("\\", "/"),
        "no_progress_seconds": 900,
        "max_tail_bytes": 65536,
        "evaluator_command": ["python", "-c", "raise SystemExit(0)"],
        "attention_logging_enabled": True,
        "attention_lock_timeout_seconds": 5,
        "attention_producers": [
            {"role": "orchestrator", "source_id": "root"},
            {"role": "subagent", "source_id": "lane"},
            {"role": "subagent", "source_id": "watcher-observer"},
        ],
    }, indent=2), encoding="utf-8")

    deadline = utc(30)
    record("subagent", "lane", "healthy", "AGENT_SIGNAL_CREATED", {"lane_id": "readiness:lane:test", "agent_blocked": True, "response_deadline_utc": deadline})
    record("orchestrator", "root", "invocation", "MANAGER_INVOCATION_STARTED", manager(pending_work_snapshot={"complete": True, "events": [{"event_id": "healthy", "type": "HELP", "priority": 1, "age_seconds": 0, "agent_blocked": True, "response_deadline_utc": deadline}], "selected_event_id": "healthy", "selection_reason": "SELECT_ACTIONABLE"}))
    record("subagent", "watcher-observer", "healthy", "WATCHER_NOTIFICATION_SENT", {"wake_transport": "collaboration.send_message", "delivery_succeeded": True, "response_deadline_utc": deadline})
    record("orchestrator", "root", "healthy", "MANAGER_EVENT_CLAIMED", manager(manager_state="READING_EVENT"))
    record("orchestrator", "root", "healthy", "MANAGER_RESPONSE_PUBLISHED", manager(manager_state="READING_EVENT"))

    review_due = utc(1)
    record("orchestrator", "root", "review-tool", "MANAGER_TOOL_STARTED", manager(activity_id="review-tool", manager_state="RUNNING_TOOL"))
    time.sleep(2)
    tool_finished = record("orchestrator", "root", "review-tool", "MANAGER_TOOL_FINISHED", manager(activity_id="review-tool", manager_state="RUNNING_TOOL"))
    record("orchestrator", "root", "formal-review", "MANAGER_REVIEW_STARTED", manager(manager_state="READING_EVENT", formal_review_due_utc=review_due, continuous_from_record_id=tool_finished))
    poll()

    report = json.loads((runtime / "watcher" / "attention-report.json").read_text(encoding="utf-8"))
    selected = {item["event_id"]: item for item in report["events"] if item["event_id"] in {"healthy", "formal-review"}}
    verdict = {
        "schema": "attention-repair010-readiness/v1",
        "epoch_id": EPOCH,
        "cursor_drained": report["cursor_drained"],
        "healthy_classification": selected["healthy"]["classification"],
        "formal_review_classification": selected["formal-review"]["classification"],
        "healthy_missing_evidence": selected["healthy"]["missing_evidence"],
        "formal_review_missing_evidence": selected["formal-review"]["missing_evidence"],
    }
    verdict["passed"] = verdict["cursor_drained"] is True and verdict["healthy_classification"] == "NO_BLOCKING_IMPACT" and verdict["formal_review_classification"] == "BUSY_MANAGER_DELAY"
    (AUDIT / "READINESS_VERDICT.json").write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    print(json.dumps(verdict, indent=2))
    if not verdict["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
