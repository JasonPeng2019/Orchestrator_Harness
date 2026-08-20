import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "stable-general-harness-runner"))

from orchestrator_harness.git_safety import (  # noqa: E402
    declaration_from_invocation,
    validate_coding_result,
)


invocation_path = ROOT / (
    "plans/general-coding-harness/runtime/firmware-v2/generalization/"
    "generalization-20260810T182017Z-0365e2613294/stages/RELEASE/lanes/"
    "RELEASE.FORMAT.P/INVOCATION_003.json"
)
result_path = ROOT / (
    "plans/general-coding-harness/runtime/firmware-v2/worktrees/"
    ".harness-candidate-worktrees/plan2-release-format-001/"
    ".agent-workspace/RESULT.json"
)
invocation = json.loads(invocation_path.read_text(encoding="utf-8"))
result = json.loads(result_path.read_text(encoding="utf-8"))
declaration = declaration_from_invocation(invocation, Path(invocation["run_root"]))
identity = validate_coding_result(
    result,
    lane_id=invocation["lane_id"],
    worker_invocation_id=invocation["worker_invocation_id"],
    declaration=declaration,
)
print(identity.head_commit)
