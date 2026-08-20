from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1]).resolve()
epoch = sys.argv[2]
workspace = root / "runs" / "A00_test" / ".agent-workspace"
stop = root / "lane-stop.token"
workspace.mkdir(parents=True, exist_ok=True)
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
status = workspace / "atlas_controller.status.json"
status.write_text(json.dumps({
    "state": "running",
    "controller_pid": os.getpid(),
    "codex_pid": child.pid,
    "doer": "Atlas",
    "task": "A00",
    "phase": "waiting manager signal",
    "thread_id": "luna-live-lane",
    "declared_lane_id": f"{epoch}:Atlas:A00",
    "started_utc": now,
    "controller_started_utc": now,
    "codex_started_utc": now,
    "board_tokens": [],
    "mcp_servers": [],
}, indent=2) + "\n", encoding="utf-8")
try:
    while not stop.exists():
        time.sleep(0.2)
finally:
    child.terminate()
    child.wait(timeout=10)
    status.write_text(json.dumps({
        "state": "exited",
        "controller_pid": os.getpid(),
        "codex_pid": child.pid,
        "doer": "Atlas",
        "task": "A00",
        "phase": "complete",
        "thread_id": "luna-live-lane",
        "declared_lane_id": f"{epoch}:Atlas:A00",
        "started_utc": now,
        "controller_started_utc": now,
        "codex_started_utc": now,
        "ended_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "exit_code": 0,
        "board_tokens": [],
        "mcp_servers": [],
    }, indent=2) + "\n", encoding="utf-8")
