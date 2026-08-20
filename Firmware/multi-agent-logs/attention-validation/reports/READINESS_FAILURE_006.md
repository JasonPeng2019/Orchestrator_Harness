# READINESS FAILURE 006 — historical ordinary events polluted the R5 attention report

R5 is noncounting; counter remains **0/3**. The exact Atlas blocking signal was correctly delivered through the collaboration mailbox, claimed immediately after wait return, answered before its response deadline, and recorded through agent receipt/resume. However, the optional watcher's attention report also created 255 `INSUFFICIENT_EVIDENCE` rows from unrelated historical ordinary harness/lane events, stamped as R5. This prevents a clean sprint-level causal report and is a genuine instrumentation gap.

The valid R5 challenge itself classified `HARNESS_DELIVERY_DELAY`: source record creation was already later than the +10s delivery deadline and watcher observation followed later, while response still met +120s. This does not evidence manager idleness.

No provider, MCP, hardware, flash, RF, request, relay, or RESULT action occurred. Repair follows `LOGGING_REPAIR_PLAN_006.md` with the required Terra-medium coder, then restarts under a fresh epoch.

The optional watcher also exited before cooperative stop because unsupported/missing-evidence Terra evaluator output raised a service-fatal validation error. This independently breaks continuous watcher coverage and is included in repair 006.
