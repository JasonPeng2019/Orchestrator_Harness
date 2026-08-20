# Canary audit — 20260731-s1-clean-g

## Verdict and counter

**ACCEPTED_NONCOUNTING.** Counter: **0/3 before, 0/3 after.**

Clean-G correctly stopped before HIL after validating a primary-harness safety/data-integrity
defect.  The stop preserved useful four-lane preparation evidence and was the right working-product
decision, but the target's four live endpoints were consequently not reached and an actionable
primary defect prevents an issue-free counting sprint.

## Findings

| Classification | Signature / judgment | Evidence |
|---|---|---|
| **primary-harness defect** | **Historical closed-lifetime PID-reuse false positive.** Closed clean-D A26 and A24 lifetime records were rediscovered as `MCP_STATE_UNKNOWN` and later `MCP_EXITED` when unrelated recycled PIDs were observed/disappeared.  A26 explicitly recorded `closed_before_board_action`; A24 had real creation data but discovery reduced expected start to null.  Historical closed lifetime records must not produce active actionable state from PID reuse.  These are one shared signature, not two independent defects. | `.agent-workspace/CANARY_CLEAN_G_ISSUES.jsonl` event IDs `f2f2c803…`, `2d8bc0d5…`, `949b065d…`; `orchestrator_harness/canary-20260731-s1-clean-g-state/events.jsonl`; role registry `observed_issue`. |
| **optional-watcher: correct** | The optional watcher independently reported the historical PID-reuse condition as a warning regression.  It did not schedule, relay, kill, or misrepresent it as a current board action.  This is correct diagnostic behavior, not a watcher defect. | `harness_watcher/runs/20260731-s1-clean-g/watcher/{events.jsonl,alerts.json}`. |
| **nonissue/advisory** | Boreal's approximately two-second `CODEX_EXITED` / `STALE_STATUS` finalization window cleared to clean controller exit with exit code 0 and exact process absence.  It matches the previously accepted finalization transient and produced no duplicate work or unsafe action. | primary events and `.agent-workspace/ORCHESTRATOR_HARNESS/{MANAGER_LOG.jsonl,MONITOR_LOG.jsonl}` clean-G entries; `ROLE_REGISTRY.json` Boreal final state. |
| **manager/orchestrator: correct** | Manager acknowledged/reviewed the one false-positive signature, continued unrelated board-free lanes, and stopped before HIL rather than treating a historical PID as live.  Fresh supervision scans were at roughly 75–93 second cadence, within the 120-second requirement. | `CANARY_CLEAN_G_ISSUES.jsonl`; manager/monitor logs; clean-G auto scans. |
| **doers: correct/useful** | All four lanes completed their bounded rebind/preflight checkpoints once, with no HIL/MCP lifetime/request/relay fabricated after the stop decision.  A22 retained setup route, D31 ran six returned-route tests, A24 ran six launcher/preflight tests with separate roots, and A26 ran four static assignment-root tests. | four clean-G controller status/JSONL/checkpoint/signal/prepared artifacts; manager/monitor entries; `ROLE_REGISTRY.json`. |

## Shutdown and safety

Final state is clean: all lane controllers/Codex workers/helpers are absent, current requests and
hardware leases are empty, and resource conflicts, observation errors, and process errors are
zero.  The supervision alarm, optional watcher, and managed primary all stopped cooperatively.
See `.agent-workspace/CANARY_S1G_FINAL_SCAN.json` (SHA-256
`c4762eb21bf6d1210fcb51412d32accad292d445290c648d766352dffc8b58ed`),
`.agent-workspace/CANARY_S1G_FINAL_PROCESS_INVENTORY.json`,
`.agent-workspace/CANARY_ACTIVE_EPOCH.json`, and
`.agent-workspace/ORCHESTRATOR_HARNESS/ROLE_REGISTRY.json`.

## Narrow repair and retest

Repair only primary lifetime discovery/reconciliation: terminal closed lifetime records need a
terminal disposition that prevents PID probing/actionable `MCP_STATE_UNKNOWN` transitions; when a
PID is considered, compare the role's actual creation evidence rather than a nullable derived
`expected_started_utc`.  Add focused regressions for the A26 closed-before-board-action and A24
creation-time cases, plus current-live lifetime coverage.  Retest that discovery surface and then
run one new, fully bounded counting epoch; do not rerun clean-G host preparation or accepted
catalog evidence.

No optional-watcher repair, production-server repair, broad monitor redesign, or experiment replay
is justified.
