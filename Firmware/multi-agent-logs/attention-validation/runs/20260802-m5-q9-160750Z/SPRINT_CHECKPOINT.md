# M5 Q9 Sprint Checkpoint

- Epoch: `20260802-m5-q9-160750Z`
- Attempt: `9/10`
- Result: `WATCHER_BUG`
- Gates: `HARNESS_PASS`, `WATCHER_BUG`, `MANAGER_EVIDENCE_INSUFFICIENT`
- Qualifying count: `0/3`
- Natural boundary: reached
- Cleanup: exact; all registered processes absent and resources empty
- AI evaluator during sprint: off
- Watcher mode: deterministic diagnostic-only

## What happened

Root incorrectly passed unquoted path arguments when starting the four existing
external worker controllers. The controllers exited, their Codex children
finished naturally, and the resulting HELP signals were correctly treated as
non-live by the native harness. The watcher incorrectly blamed the harness for
the absence of delivery.

## Next action

Implement the narrow passive eligibility-evidence repair in `REPAIR_PLAN.md`,
review and smoke it, rerun M4 readiness, refreeze the Python surface, and then
run Q10 with correctly quoted controller arguments. Q10 is the final permitted
live attempt. Never launch Q11.

