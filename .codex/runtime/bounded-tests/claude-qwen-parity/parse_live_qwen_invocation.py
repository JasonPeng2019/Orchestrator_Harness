import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from orchestrator_harness.lane_controller import load_invocation

invocation = load_invocation(
    Path(
        ".agent-workspace/live-qwen-fixture-003/worktrees/lane-qwen/.agent-workspace/invocation.json"
    )
)
print(invocation.provider.provider_id)
