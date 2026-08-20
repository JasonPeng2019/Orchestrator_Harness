# Clean-L pre-sprint startup abort

Clean-L never became a canary sprint and does not affect the `0/3` counter. No lane, helper, MCP,
provider, board, request, relay, or optional watcher was started.

The first primary managed watcher was launched under a fresh owner process, but the owner invoked
the independent supervision heartbeat before `managed-watch-runtime.json` was ready. The native
command's startup error terminated the PowerShell owner. The primary watcher then correctly
failed closed with `exit_reason: owner-identity-lost` and PID `190468` became absent. This is a
manager-owned startup-script sequencing defect, not a primary-harness or optional-watcher defect.

The owner script now waits for the managed runtime before its first supervision pass and records
supervision errors without abandoning ownership. Because Clean-L output authority was consumed,
it will not be reused; the first live successor uses a wholly fresh Clean-M config/output/runtime.
