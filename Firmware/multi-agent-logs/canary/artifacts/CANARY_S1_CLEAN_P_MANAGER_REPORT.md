# Clean-P canary manager report

- Epoch: `20260731-s1-clean-p`
- Canary target: advance four independent E2E lanes through one bounded live MCP lifetime while exercising the primary `orchestrator_harness` and optional `harness_watcher` under active manager review.
- Manager classification: **NONCOUNTING**
- Consecutive issue-free sprint counter after this epoch: **0/3** (subject to the required independent sprint audit).
- Production server repair: **none**. No observed failure was isolated to production code in `BYO-Firmware-MCP`.

## Lane outcomes

| Doer | Task | Bounded outcome | Classification |
|---|---|---|---|
| Atlas | A22 | The single live lifetime reached MCP `initialize`, then the run-local controller rejected valid plain-text `initialization_handshake` guidance as `non_json_or_truncated_response`. It never reached setup or a hardware action. Host self-test artifacts also contaminated the live evidence namespace. | Run-local parser/evidence-isolation defect; noncounting. |
| Boreal | D31 | The single live lifetime reached the setup route. A copied Clean-M helper emitted stale epoch IDs and omitted current required populated-plan fields, so the manager rejected the exact request before any hardware action. | Run-local controller/request-construction defect; noncounting. |
| Cygnus | A24 | One paired NRF-A/NRF-B lifetime stopped on a pre-public `initialize` timeout. No setup, reset/BUSY, flash, or RF action occurred. The first checkpoint signal was stale Clean-M metadata; a corrected Clean-P signal was later written. | Run-local transport/metadata defect; noncounting. |
| Delta | A26 | The doer made three avoidable preflight attempts before launching one provider. It reached the setup route, then a copied controller raised `NameError: setup is not defined` instead of using `setup_result`. No populated plan, relay, or board/counter action occurred. | Run-local preflight/controller defect; noncounting. |

## Harness and watcher observations

- The primary harness tracked controller starts/exits, MCP lifetimes, manager signals, resource ambiguity, and manager-review deadlines.
- Transient `STALE_STATUS` observations during controller finalization later resolved to `CONTROLLER_EXITED`; the reviewed Delta example is recorded in `.agent-workspace/CANARY_S1P_DELTA_STALE_EVENT_REVIEW.json`.
- Five formal manager reviews were completed and acknowledged. Review 005 was authored before its 120-second deadline.
- The optional watcher evaluated ten polls. Every evaluator outcome was `defect=false`, `alert_id=null`; it emitted no durable false alert from the primary harness's transient stale observations.
- The optional watcher stopped cooperatively with `exit_reason=stop-requested`.
- The primary managed watcher stopped cooperatively with `exit_reason=stop-requested`. Its sleeping owner process was exact-identity terminated only after the child watcher had exited.
- All four endpoint controller/Codex processes and all recorded harness/watcher PIDs were absent at the cleanup boundary.

## Evidence index

- Primary watcher runtime: `orchestrator_harness/canary-20260731-s1-clean-p-state/managed-watch-runtime.json`
- Optional watcher service/events/cursor: `harness_watcher/runs/20260731-s1-clean-p/watcher/`
- Manager reviews/acks: `.agent-workspace/CANARY_S1P_MANAGER_REVIEW_001.md` through `_005.md` and matching `_ACK.json` files
- Optional watcher audit: `.agent-workspace/CANARY_S1_CLEAN_P_OPTIONAL_WATCHER_AUDIT.json`
- Atlas checkpoint: `fresh-experiments/A22_20260726-062324/.agent-workspace/CLEAN_P_LIVE_CHECKPOINT.md`
- Boreal checkpoint: `fresh-experiments/D31_20260726-062325/.agent-workspace/CLEAN_P_LIVE_CHECKPOINT.md`
- Cygnus checkpoint: `fresh-experiments/A24_20260726-052146/.agent-workspace/CLEAN_P_LIVE_CHECKPOINT.md`
- Delta checkpoint: `fresh-experiments/A26_20260726-062325/.agent-workspace/CLEAN_P_LIVE_CHECKPOINT.md`

## Manager disposition

Clean-P does not count toward the required three consecutive issue-free sprints because every lane exposed a material run-local execution fault. The available evidence does **not** presently justify a harness or watcher code change: the primary harness surfaced the actual runtime state, and the optional watcher correctly quarantined transient stale samples rather than raising a durable false alarm. The next candidate sprint must correct the four run-local controller/adaptor defects and use a fresh epoch/runtime without replaying unrelated completed work.
