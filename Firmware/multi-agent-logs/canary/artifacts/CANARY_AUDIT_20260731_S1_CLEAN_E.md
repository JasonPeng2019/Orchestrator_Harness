# Canary audit — 20260731-s1-clean-e

## Verdict

**ACCEPTED_NONCOUNTING.**  The sprint stopped cleanly and preserves useful bounded evidence, but it
does not meet the target's issue-free, all-endpoints, fresh-cadence, promptly-serviced-request
benchmark.  The consecutive counter remains **0/3**.

## Findings

| Classification | Finding and disposition | Evidence |
|---|---|---|
| manager-procedure issue | At least one supervision interval exceeded the target 120 seconds (the handoff records this independently); this alone prevents counting.  The later 75-second records do not cure an earlier miss. | `HANDOFF.md` “Clean-E canary disposition”; manager/monitor clean-E records under `.agent-workspace/ORCHESTRATOR_HARNESS/` |
| manager-procedure issue | D31's exact setup-action request was not relayed before the deliberate clean-agent stop.  It is correctly retained as expired evidence, not an action to replay. | `fresh-experiments/D31_20260726-062325/STATUS.md`; `.agent-workspace/mcp-runtime/d31-rst01-s1-clean-e/evidence/20260731T165523Z/handoff-stop.json` |
| manager-procedure issue | Delta remained RUNNING after its board-free checkpoint until manager termination; primary later emitted `LANE_NO_PROGRESS`.  The lane should have been stopped promptly once its lease-gated checkpoint was durable. | `orchestrator_harness/canary-20260731-s1-clean-e-state/events.jsonl` (`manager:lane:20260731-s1-clean-e:Delta:A26:no-progress`) |
| run-local/doer issue | A22 reached live STM-A enumeration and authoritative `board_setup-plan`, but its retained adapter used obsolete validate/connect routing.  No B14/B34 action occurred.  This is not a server defect. | `fresh-experiments/A22_20260726-062324/STATUS.md`; `.agent-workspace/mcp-runtime/a22-b14-s1-clean-e/evidence/` |
| run-local/doer issue | A24's only paired attempt used nonexistent `C:\Users\Jason\.local\bin\uv.exe`; both launchers stopped before public MCP/provider startup.  No retry, request, flash, RF, or mutation occurred. | `fresh-experiments/A24_20260726-052146/STATUS.md`; `.agent-workspace/canary/20260731-s1-clean-e/Cygnus/A24/PAIRED-FLASH/evidence/{paired_result.json,helper_failure.json,paired_cleanup.json}` |
| run-local/doer issue | D31's lifetime record gave the provider PID the launcher-start timestamp; observed provider creation differed by 11.863 seconds.  The watcher correctly reported the mismatch.  Repair only the run-local lifetime recorder to record each role's actual creation time. | primary `events.jsonl` `81f7630b…`; watcher `alerts.json` `hwa-6aec7b4567c7caef1a85d8b1`; D31 checkpoint above |
| validated primary-harness defect | Startup ingestion published stopped-epoch manager HELP signals into the active clean-E state ahead of current work.  Historical signals must remain historical/non-actionable and must not enter active notification ordering. | `orchestrator_harness/canary-20260731-s1-clean-e-state/events.jsonl` at initial `2026-07-31T16:44:32.748702Z`; `HANDOFF.md` clean-E disposition |
| validated optional-watcher defect | `hwa-77364…` classified transient startup `STALE_STATUS` observations as a manager failure even though primary confirmed live controllers shortly afterward and the condition cleared.  It is a false positive for an unresolved state-transition race, not a hardware safety incident. | watcher `alerts.json` / `events.jsonl` (`16:47:55` poll; `16:51:06` clean outcome); primary events `aee202…` then `10944b…` |
| nonissue/advisory | Primary transient `MCP_STATE_UNKNOWN` entries for controller declarations before durable lifetime discovery later cleared; they accurately expose a scan race and do not show a live conflict.  Final state is clean. | primary `events.jsonl`; `CURRENT_CANARY_READONLY_SCAN.json`; `CURRENT_RELEVANT_PROCESS_INVENTORY.json` |

## Per-lane outcome and safety

* **A22:** one recorded lifetime; no B14/B34 or board action; delayed descendant audits absent.
* **D31:** focused `board_id` fix passed; one setup-plan relay and one unexecuted setup-action request;
  no setup/RST01/APP-1/retry.  The stale helper marker was moved to evidence.
* **A24:** one failed local launch only; both roots have exact cleanup and two empty delayed-absence
  checks; no provider claim or board mutation.
* **A26:** board-free preparation passed and no MCP/action was fabricated; manager termination was
  required after its checkpoint.

Final reconciliation is acceptable: the active epoch is stopped, final scan/inventory report no
live helpers, requests, leases, conflicts, observation errors, or process errors, and watcher and
primary stopped cooperatively.  See `.agent-workspace/CANARY_ACTIVE_EPOCH.json`,
`.agent-workspace/CURRENT_CANARY_READONLY_SCAN.json`, and
`.agent-workspace/CURRENT_RELEVANT_PROCESS_INVENTORY.json`.

## Narrow repairs before a counting attempt

1. **Primary:** filter/mark historical signals before active-state notification ordering; do not
   change scheduler authority or broad event retention.
2. **Watcher:** suppress escalation of a transient `STALE_STATUS` when the same lane becomes
   identity-confirmed within the bounded subsequent scan; retain alerts for persistent mismatch.
3. **Run-local:** correct D31 per-role creation timestamp; change only A22's route adapter and A24's
   UV executable selection, each with focused host checks.
4. **Manager:** start/verify cadence before launch, relay or explicitly reject each request before
   deadline, and stop a checkpointed non-live lane without waiting for no-progress detection.

No production-server repair is justified.
