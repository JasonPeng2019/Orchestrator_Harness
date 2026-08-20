import sys
sys.path.insert(0, r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\.codex\scripts")
from pathlib import Path
import dev_state

root = Path(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness")
delta = dev_state.verification_delta(root)
out = []
for p in delta.changed_paths:
    out.append(p.as_posix())
with open(r"C:\Users\Jason\Documents\Jason\Orchestrator_Harness\scratch\session-analysis\changed-paths.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))
print("wrote", len(out))
