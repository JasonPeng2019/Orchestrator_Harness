from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

workspace = Path(sys.argv[1]).resolve()
signal_id = sys.argv[2]
epoch = sys.argv[3]
lane_id = f"{epoch}:Atlas:A00"
target = workspace / "manager-signals" / f"{signal_id}.json"
target.parent.mkdir(parents=True, exist_ok=True)
value = {
    "schema": "manager-signal/v1",
    "signal_id": signal_id,
    "kind": "HELP",
    "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "deadline_utc": "2099-01-01T00:00:00Z",
    "lane_id": lane_id,
    "agent_blocked": True,
    "task": "A00",
    "phase": "managed-consumer-smoke",
    "summary": "isolated managed consumer wake",
    "evidence_paths": [],
    "attention_epoch_id": epoch,
}
target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(target), "signal_id": signal_id}, sort_keys=True))
