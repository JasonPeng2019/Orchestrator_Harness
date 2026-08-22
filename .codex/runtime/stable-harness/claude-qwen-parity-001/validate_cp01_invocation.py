from pathlib import Path
import sys

sys.path.insert(
    0,
    r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\stable-general-harness-runner",
)

from orchestrator_harness.lane_controller import load_invocation


invocation = load_invocation(
    Path(
        r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\.codex\runtime\stable-harness\claude-qwen-parity-001\parity-implementer-cp01.invocation.json"
    )
)
assert invocation.model == "gpt-5.6-luna"
assert invocation.reasoning_effort == "xhigh"
assert invocation.config_overrides == [
    "model_context_window=272000",
    "model_auto_compact_token_limit=120000",
    'model_auto_compact_token_limit_scope="total"',
]
print("INVOCATION_VALID")
