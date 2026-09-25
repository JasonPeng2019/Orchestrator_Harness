"""Write the lane RESULT.json for MI-NORMAL-001-BUILD-EXEC with a canonical hash."""
from __future__ import annotations

import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ASSEMBLY = Path(r"C:/Users/Jason/Documents/Jason/Orchestrator-Harness-3")
WT = ASSEMBLY / "development/product/worktree_example/.harness-runtime/worktrees/77574f69003e45a49701a47083c346c2/normal-001-build-exec"
CORE = WT / "harness/orchestrator_harness/core.py"

spec = importlib.util.spec_from_file_location("harness_core", CORE)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
evidence = [
    "C:/Users/Jason/Documents/Jason/Orchestrator-Harness-3/development/evidence/STEP-001/NORMAL-001-BUILD-EXEC/result.json",
    str(WT / ".agent-workspace/task-card.json"),
    str(WT / ".agent-workspace/invocation.json"),
    str(WT / ".agent-workspace/controller.status.json"),
    str(WT / ".agent-workspace/harness-hook-binding.json"),
    str(WT / ".agent-workspace/overlay-receipt.json"),
    str(WT / ".agent-workspace/QUEUE.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/epochs/77574f69003e45a49701a47083c346c2/lanes/normal-001-build-exec/lane.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/epochs/77574f69003e45a49701a47083c346c2/epoch-state.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/epochs/77574f69003e45a49701a47083c346c2/active-lanes.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/monitor/MONITOR.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/RUNTIME_STATE.json"),
    str(ASSEMBLY / "development/product/worktree_example/.harness-runtime/CURRENT_EPOCH.json"),
    str(ASSEMBLY / "development/test-runs/normal-001-build-exec-probe/stdlib_control_probe.py"),
]
record = {
    "schema": "result/v1",
    "lane_id": "normal-001-build-exec",
    "run_id": "b5c03ad02022407bb1a2b3a1090518fd",
    "outcome": "PASS",
    "summary": (
        "MI-NORMAL-001-BUILD (M02-A1..A7) returned the unchanged reviewable tip "
        "a54ad14a8f59409ee1e88c2473e3617c123f20b8 with focused evidence: the already-accepted "
        "resolver/option-persistence/canonical-repair seams were inspected and the exact writer "
        "binding chain (codex / deepseek-v4.1-flash:cloud / reasoning_effort=max / service_tier=normal "
        "/ launcher=ollama) re-resolved and matched at the lane and invocation records; all 7 resolver "
        "contract tests passed; a stdlib-only control probe verified the six CONTROL-READY fixture "
        "behaviors (early terminal exit, independent refill, preserved checkpoint, lost-handle "
        "reconciliation, lingering owned descendant cleanup with exit readback) so no M02 pure helper "
        "is earned; M03 fixture assets remain pending. Durable report at "
        "development/evidence/STEP-001/NORMAL-001-BUILD-EXEC/result.json. Factual evidence only; not ROOT acceptance."
    ),
    "evidence": evidence,
    "completed_at": completed_at,
}
record["content_hash"] = core.content_hash(record)
out = WT / "RESULT.json"
out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"result_path": str(out), "content_hash": record["content_hash"], "completed_at": completed_at}))
