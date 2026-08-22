import json
import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\stable-general-harness-runner")
from orchestrator_harness.operator_launch import launch_process
root = Path(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness")
runtime = root / ".codex" / "runtime" / "stable-harness" / "claude-qwen-parity-001"
print(json.dumps(launch_process(receipt=runtime / "parity-implementer-cp01-lint-final.launch.json", label="LANE-IMPLEMENTER-CP01-LINT-FINAL-001", role="PARITY_IMPLEMENTER", cwd=root / "stable-general-harness-runner", argv=[sys.executable, "-m", "orchestrator_harness.lane_controller", str(runtime / "parity-implementer-cp01-lint-final.invocation.json")], expected_state_path=root / ".firmware-v2-harness-runner-worktrees" / "claude-qwen-parity-implementation" / ".agent-workspace" / "parity-implementer-cp01.status.json"), sort_keys=True))
