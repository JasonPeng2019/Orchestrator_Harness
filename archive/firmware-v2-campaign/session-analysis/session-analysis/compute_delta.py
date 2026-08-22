import sys, json
sys.path.insert(0, r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\.codex\scripts")
from pathlib import Path
import dev_state

root = Path(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness")
delta = dev_state.verification_delta(root)
if delta is None:
    print("NO BASELINE")
else:
    print("changed count:", len(delta.changed_paths))
    for p in delta.changed_paths:
        print(p.as_posix())
