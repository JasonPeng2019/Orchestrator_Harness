import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\stable-general-harness-runner",
)

from orchestrator_harness.operator_launch import launch_process


root = Path(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness")
stable_root = root / "stable-general-harness-runner"
runtime_root = root / ".codex" / "runtime" / "stable-harness" / "claude-qwen-parity-001"
invocation = runtime_root / "parity-implementer-cp01.invocation.json"
receipt = runtime_root / "parity-implementer-cp01.launch.json"
status = (
    root
    / ".firmware-v2-harness-runner-worktrees"
    / "claude-qwen-parity-implementation"
    / ".agent-workspace"
    / "parity-implementer-cp01.status.json"
)

print(
    json.dumps(
        launch_process(
            receipt=receipt,
            label="LANE-IMPLEMENTER-001",
            role="PARITY_IMPLEMENTER",
            cwd=stable_root,
            argv=[sys.executable, "-m", "orchestrator_harness.lane_controller", str(invocation)],
            expected_state_path=status,
        ),
        sort_keys=True,
    )
)
