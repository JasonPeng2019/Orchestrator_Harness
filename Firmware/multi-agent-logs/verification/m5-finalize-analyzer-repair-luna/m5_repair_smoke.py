from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from harness_watcher_implementation.attention import analyze_event, canonicalize, make_source_record
from orchestrator_harness.attention_sprint import (
    AttentionSprintError,
    event_selection_snapshot,
    formal_baseline_snapshot,
    invocation_snapshot,
    validate_sprint_finalize,
)


OUT = Path(__file__).resolve().parent / "m5-repair-smoke-results.json"
EPOCH = "m5-finalize-analyzer-repair-luna"


def snapshot(*, selected: str | None = None, reason: str = "FORMAL_REVIEW_BASELINE") -> dict[str, object]:
    event = {"event_id": "gate", "type": "HELP", "priority": 1, "age_seconds": 0.0, "agent_blocked": True}
    if reason == "SELECT_ACTIONABLE":
        return event_selection_snapshot([event], event_id=selected or "gate")
    if reason == "FORMAL_REVIEW_BASELINE":
        return formal_baseline_snapshot([event])
    return invocation_snapshot([event])


def sprint_row(kind: str, event_id: str, *, source_role: str | None = None, complete: bool = True, reason: str = "FORMAL_REVIEW_BASELINE") -> dict[str, object]:
    row: dict[str, object] = {
        "epoch_id": "sprint-contract",
        "event_id": event_id,
        "kind": kind,
    }
    if source_role is not None:
        row["source_role"] = source_role
    if kind in {"MANAGER_INVOCATION_STARTED", "MANAGER_INVOCATION_FINISHED"}:
        row["pending_work_snapshot"] = snapshot(reason="BOUNDARY_INVENTORY")
    elif kind in {"FORMAL_REVIEW_BASELINE_ADVANCED", "FORMAL_REVIEW_BASELINE"}:
        row["pending_work_snapshot"] = snapshot(reason=reason) if complete else {"complete": False, "events": [], "selected_event_id": None, "selection_reason": "UNKNOWN"}
    elif kind == "MANAGER_EVENT_CLAIMED":
        row["pending_work_snapshot"] = snapshot(selected="gate", reason="SELECT_ACTIONABLE")
    return row


def run_sprint_contract() -> dict[str, object]:
    incomplete_harness = sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "telemetry-activation-incomplete", source_role="harness", complete=False)
    incomplete_harness_after_review = sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "telemetry-review-incomplete", source_role="harness", complete=False)
    activation = sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "explicit-activation", source_role="orchestrator")
    post_review = sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "explicit-post-review", source_role="orchestrator")
    common = [
        sprint_row("MANAGER_INVOCATION_STARTED", "start"),
        incomplete_harness,
        activation,
        sprint_row("MANAGER_EVENT_CLAIMED", "gate"),
        sprint_row("AGENT_SIGNAL_CREATED", "gate"),
        sprint_row("MANAGER_REVIEW_STARTED", "review"),
        incomplete_harness_after_review,
        post_review,
        sprint_row("MANAGER_INVOCATION_FINISHED", "finish"),
        sprint_row("AGENT_GATE_EXPIRED", "gate") | {"terminal_gate_expired": True},
    ]
    validate_sprint_finalize(common, epoch_id="sprint-contract")

    activation_rejected = False
    try:
        validate_sprint_finalize(
            [
                sprint_row("MANAGER_INVOCATION_STARTED", "start"),
                sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "bad-activation", source_role="harness", complete=False),
                sprint_row("MANAGER_EVENT_CLAIMED", "gate"),
                sprint_row("AGENT_SIGNAL_CREATED", "gate"),
                sprint_row("MANAGER_INVOCATION_FINISHED", "finish"),
                sprint_row("AGENT_GATE_EXPIRED", "gate") | {"terminal_gate_expired": True},
            ],
            epoch_id="sprint-contract",
        )
    except AttentionSprintError as exc:
        activation_rejected = "activation formal-review baseline" in str(exc)
    assert activation_rejected, "incomplete or non-orchestrator activation telemetry unexpectedly satisfied the gate"

    post_review_rejected = False
    try:
        validate_sprint_finalize(
            [
                sprint_row("MANAGER_INVOCATION_STARTED", "start"),
                sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "explicit-activation", source_role="orchestrator"),
                sprint_row("MANAGER_EVENT_CLAIMED", "gate"),
                sprint_row("AGENT_SIGNAL_CREATED", "gate"),
                sprint_row("MANAGER_REVIEW_STARTED", "review"),
                sprint_row("FORMAL_REVIEW_BASELINE_ADVANCED", "bad-post-review", source_role="harness", complete=False),
                sprint_row("MANAGER_INVOCATION_FINISHED", "finish"),
                sprint_row("AGENT_GATE_EXPIRED", "gate") | {"terminal_gate_expired": True},
            ],
            epoch_id="sprint-contract",
        )
    except AttentionSprintError as exc:
        post_review_rejected = "formal review lacks a later baseline" in str(exc)
    assert post_review_rejected, "incomplete or non-orchestrator post-review telemetry unexpectedly satisfied the gate"

    return {
        "accepted_combined_timeline": True,
        "accepted_baselines": ["explicit-activation", "explicit-post-review"],
        "ignored_incomplete_harness_telemetry": ["telemetry-activation-incomplete", "telemetry-review-incomplete"],
        "activation_negative_rejected": activation_rejected,
        "post_review_negative_rejected": post_review_rejected,
    }


def stamp(seconds: float) -> str:
    return (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds)).isoformat()


def attention_record(index: int, event_id: str, kind: str, seconds: float, **metadata: object) -> dict[str, object]:
    if kind == "AGENT_SIGNAL_CREATED":
        role, source_id = "subagent", "lane"
    elif kind in {"MANAGER_WAKE_ATTEMPTED", "MANAGER_WAKE_DELIVERED", "MANAGER_WAKE_FAILED", "HARNESS_SIGNAL_OBSERVED"}:
        role, source_id = "harness", "harness"
    elif kind == "WATCHER_NOTIFICATION_SENT":
        role, source_id = "subagent", "lane"
    else:
        role, source_id = "orchestrator", "root"
    source = make_source_record(
        recorder=source_id,
        epoch_id=EPOCH,
        event_id=event_id,
        kind=kind,
        source_timestamp_utc=stamp(seconds),
        metadata=metadata,
    )
    return canonicalize(
        source,
        observed_timestamp_utc=stamp(seconds),
        source_path=f"m5-smoke/{index}/{kind}.jsonl",
        source_role=role,
        source_id=source_id,
        source_generation="1",
        byte_start=index,
        byte_end=index + 1,
    )


def run_analyzer_contract() -> dict[str, object]:
    event_id = "blocking-event"
    wake_id = "b3bbd28a-6cdd-4dd5-9d49-bd6d0c14fc4e"
    wake = {
        "wake_id": wake_id,
        "wake_component": "orchestrator_harness.watch_until_actionable",
        "wake_transport": "blocking_harness_wait_stdout",
        "manager_session_id": "active-session",
        "manager_invocation_id": "active-invocation",
    }
    records = [
        attention_record(0, event_id, "AGENT_SIGNAL_CREATED", 0, lane_id="lane", agent_blocked=True, response_deadline_utc=stamp(7)),
        attention_record(1, event_id, "HARNESS_SIGNAL_OBSERVED", 1),
        attention_record(2, event_id, "MANAGER_INVOCATION_STARTED", 1.5, **{**{ "pending_work_snapshot": {"complete": False, "events": [], "selected_event_id": None, "selection_reason": "UNKNOWN"}}, **{k: wake[k] for k in ("manager_session_id", "manager_invocation_id")}}),
        attention_record(3, event_id, "MANAGER_WAKE_ATTEMPTED", 2, **wake),
        attention_record(4, event_id, "MANAGER_WAKE_DELIVERED", 3, **wake, delivery_succeeded=True),
        attention_record(5, event_id, "MANAGER_WAKE_RECEIVED", 4, **{k: wake[k] for k in ("wake_id", "wake_transport", "manager_session_id", "manager_invocation_id")}),
        attention_record(6, event_id, "MANAGER_WAIT_FINISHED", 4.5, activity_id="wait", **{k: wake[k] for k in ("wake_id", "wake_transport", "manager_session_id", "manager_invocation_id")}),
        attention_record(7, event_id, "MANAGER_EVENT_CLAIMED", 5, manager_session_id=wake["manager_session_id"], manager_invocation_id=wake["manager_invocation_id"], manager_state="READING_EVENT"),
        attention_record(8, event_id, "MANAGER_RESPONSE_PUBLISHED", 6, manager_session_id=wake["manager_session_id"], manager_invocation_id=wake["manager_invocation_id"], manager_state="READING_EVENT"),
    ]
    report = analyze_event(records, epoch_id=EPOCH, event_id=event_id)
    assert not any(row["kind"] == "WATCHER_NOTIFICATION_SENT" for row in records)
    assert report["classification"] == "NO_BLOCKING_IMPACT", report
    assert report["metrics"]["deadline_lateness_seconds"] == 0.0, report

    unrelated = list(records)
    unrelated[-1] = attention_record(8, event_id, "MANAGER_RESPONSE_PUBLISHED", 9, manager_session_id="different-session", manager_invocation_id="different-invocation", manager_state="READING_EVENT")
    unrelated.append(attention_record(9, "unrelated-event", "MANAGER_RESPONSE_PUBLISHED", 10, manager_session_id=wake["manager_session_id"], manager_invocation_id=wake["manager_invocation_id"], manager_state="READING_EVENT"))
    negative = analyze_event(unrelated, epoch_id=EPOCH, event_id=event_id)
    assert negative["classification"] == "INSUFFICIENT_EVIDENCE", negative
    assert negative["metrics"]["deadline_lateness_seconds"] is None, negative
    return {
        "notification_count": 0,
        "production_wake_status": report["wake_evidence"]["status"],
        "healthy_classification": report["classification"],
        "healthy_deadline_lateness_seconds": report["metrics"]["deadline_lateness_seconds"],
        "unrelated_identity_classification": negative["classification"],
        "unrelated_identity_deadline_lateness_seconds": negative["metrics"]["deadline_lateness_seconds"],
        "unrelated_response_record_id": unrelated[-1]["record_id"],
    }


def main() -> None:
    result = {
        "schema": "m5-repair-smoke-results/v1",
        "sprint_contract": run_sprint_contract(),
        "analyzer_contract": run_analyzer_contract(),
        "result": "PASS",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

