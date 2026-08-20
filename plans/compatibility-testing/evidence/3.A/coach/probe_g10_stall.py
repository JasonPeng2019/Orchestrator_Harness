"""G10 stall-detection — ACCEPTED SYNTHETIC/FAKE (user, 2026-08-20).

The live stall PRODUCERS were removed in the S4 lane refactor: config keys
`manager_review_interval_seconds` / `lane_no_progress_seconds` are now
legacy/"no S4 runtime effect" (config.py ~168-184), so the current harness
never emits MANAGER_REVIEW_DUE / LANE_NO_PROGRESS / LANE_STAGE_REPEAT from a
live lane.  Only the CLASSIFIER wiring survives (disposition table +
priority ranking + actionable selection).  A live emergent stall is therefore
not reachable at all on this harness, which is why the user accepts a fake.

This probe fabricates the three stall conditions (using the harness's OWN
`stable_condition` builder, not a hand-rolled dict) and drives them through the
surviving classifier: CURRENT_EVENT_DISPOSITIONS lookup, `_priority`, and
`select_actionable`.  It proves the classifier still recognises and ranks the
stall events; it does NOT claim a live stall was observed.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from orchestrator_harness.events import stable_condition
from orchestrator_harness.notifications import (
    CURRENT_EVENT_DISPOSITIONS,
    EVENT_DISPOSITION_OBSERVED,
    _priority,
    select_actionable,
)

STALL_KINDS = ("MANAGER_REVIEW_DUE", "LANE_NO_PROGRESS", "LANE_STAGE_REPEAT")


def main() -> int:
    observed_at = datetime(2026, 8, 20, 9, 30, tzinfo=timezone.utc)
    lane_id = "claude-hello"
    # A fabricated stalled lane snapshot: same stage across observations, no head
    # movement, an old manager review timestamp.  Purely synthetic input.
    snapshot = {
        "lanes": [
            {
                "lane_id": lane_id,
                "operational_state": "RUNNING_PROVIDER",
                "process_state": "RUNNING_PROVIDER",
                "thread_id": "3cd1b7ee-ec24-4ad8-be37-4161b5577691",
                "phase": "implementation",
                "board_tokens": ["stage:implementation"],
            }
        ]
    }
    conditions: dict[str, dict] = {}
    report = {"synthetic": True, "note": "FAKE stall per user acceptance; no live producer exists post-S4",
              "kinds": {}}
    for kind in STALL_KINDS:
        identity = f"lane:{lane_id}:{kind.lower()}"
        cond = stable_condition(
            identity, kind, "info",
            {"lane_id": lane_id, "reason": "synthetic stall fixture",
             "stage": "implementation"},
        )
        conditions[identity] = cond
        disposition = CURRENT_EVENT_DISPOSITIONS.get(kind)
        priority = _priority(cond, snapshot, observed_at)
        report["kinds"][kind] = {
            "event_id": cond["event_id"],
            "disposition": disposition,
            "disposition_is_observed": disposition == EVENT_DISPOSITION_OBSERVED,
            "priority": priority,
            "priority_recognised": priority is not None,
        }
    selected = select_actionable(
        conditions, snapshot, observed_at=observed_at,
        acknowledged_event_ids=set(), newly_observed_event_ids=None,
    )
    report["selected_actionable"] = (
        None if selected is None
        else {"type": selected["type"], "admitted_priority": selected["admitted_priority"],
              "notification": selected["notification"]}
    )
    report["all_recognised"] = all(
        v["disposition"] is not None and v["priority_recognised"]
        for v in report["kinds"].values()
    )
    print(json.dumps(report, indent=2))
    return 0 if report["all_recognised"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
