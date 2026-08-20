# Historical relay-assisted manager-attention verdict

> **Invalid for the production-wake architecture decision.** R12-R14 included an internal
> watcher-subagent notification path, so they did not test whether the production blocking harness
> wait alone wakes the persistent orchestrator. Preserve this report as evidence that the relay
> worked and as historical timing data. M4 proves host-only readiness; M5 is the new
> production-realistic three-sprint decision gate.

## Original goal

Determine whether the orchestrator needed a separate active manager program using `codex exec`, or
whether a persistent orchestrator was sufficiently attentive.

## Original verdict (superseded)

The run originally concluded: **keep the persistent manager**. That conclusion is superseded for
the production-wake question because the relay influenced request discovery.

## Historical evidence

| Sprint | Blocking gates | Formal review | Historical disposition |
|---|---|---|---|
| R12 | 2 `NO_BLOCKING_IMPACT`; 2 `HARNESS_DELIVERY_DELAY` | `BUSY_MANAGER_DELAY`, 95.579740 s late | relay-assisted accepted 1/3 |
| R13 | 2 `NO_BLOCKING_IMPACT`; 2 `HARNESS_DELIVERY_DELAY` | `BUSY_MANAGER_DELAY`, 116.566727 s late | relay-assisted accepted 2/3 |
| R14 | 2 `NO_BLOCKING_IMPACT`; 2 `HARNESS_DELIVERY_DELAY` | `BUSY_MANAGER_DELAY`, 54.595199 s late | relay-assisted accepted 3/3 |

Across those runs, 12/12 blocking gates had durable receipt/work-resume evidence, no 300-second
deadline was missed, and no material event was classified idle/absent. These facts remain valid
for the relay-assisted arrangement.

## What the historical run proves

The watcher-subagent relay could notify a live persistent orchestrator, and the resulting manager
work could be measured. It does **not** identify what would have resumed the manager without that
relay and therefore cannot choose the production architecture.

## Current recommendation

Run M5 under `active-working-spec/m5-three-sprint-wake-test.md` with no internal relay or AI
evaluator during a counted sprint. Choose the architecture only from three consecutive accepted
M5 checkpoints.

## Preserved evidence

- `multi-agent-logs/attention-validation/runs/20260801-attention-r12/`
- `multi-agent-logs/attention-validation/runs/20260801-attention-r13/`
- `multi-agent-logs/attention-validation/runs/20260801-attention-r14/`
- `harness_watcher/runs/20260801-attention-r12/watcher/attention-report.json`
- `harness_watcher/runs/20260801-attention-r13/watcher/attention-report.json`
- `harness_watcher/runs/20260801-attention-r14/watcher/attention-report.json`

