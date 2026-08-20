# Canary audit — 20260731-s1-clean-f

## Verdict

**ACCEPTED_NONCOUNTING.**  The final boundary is clean and the manager cadence/shutdown evidence
meets the stated operational limit, but the counting endpoints were not all reached and there is a
validated primary discovery defect plus bounded run-local defects.  The canary counter therefore
remains **0/3**.  No production-server repair is justified.

## Evidence-led findings

| Classification | Finding | Evidence and disposition |
|---|---|---|
| **validated primary-harness defect** | Primary discovery retained current clean-F HELP signals but did not discover the matching live `.agent-workspace/manager-requests` and `manager-relays`; supervision scans consequently reported `requests: []` and raised resource ambiguity during a real D31 request. | `orchestrator_harness/canary-20260731-s1-clean-f-state/events.jsonl` (clean-F D31 HELP/`RESOURCE_AMBIGUOUS`); `.agent-workspace/ORCHESTRATOR_HARNESS/{MANAGER_LOG,MONITOR_LOG}.jsonl`; D31 request/relay roots.  Repair discovery of the two manager directories only; preserve historical-signal filtering and do not change scheduler authority. |
| **nonissue/advisory** | Watcher alert `hwa-e02017a3ddd6157a0f2a60b9` observed D31 `turn.completed` before controller-finalization state was written.  The next watcher poll was clean and controller exit was subsequently reconciled; no duplicate manager, action, or lease resulted.  This is a normal terminalization race, not a real manager failure and not a watcher-code defect. | `harness_watcher/runs/20260731-s1-clean-f/watcher/{alerts.json,events.jsonl}`: alert at `17:38:19Z`, no-defect poll at `17:41:26Z`; primary events.  Clear/acknowledge as advisory; no code change. |
| **run-local/doer issue** | D31 accepted `continue_setup` with `board_id`, then received explicit `board_fix_setup` / load-validate redirect but called `board_validate` without first loading it and stopped at `setup_tool_not_loaded`.  It did not invent an action or retry. | `fresh-experiments/D31_20260726-062325/STATUS.md`; D31 clean-F checkpoint/evidence, including the returned redirect and `board_validate` response recorded in clean-F manager supervision.  Focused helper route test must require `load_setup_tool(board_fix_setup)` then validation before a new lifetime. |
| **run-local/doer issue** | A24 clean-F launchers used a nonexistent run-local `BYO-Firmware-MCP` path; this is a launcher-root derivation failure, not provider or server behavior.  It prevented public MCP startup/post-flash work; no retry, flash, RF, or mutation occurred. | `fresh-experiments/A24_20260726-052146/.agent-workspace/canary/20260731-s1-clean-f/Cygnus/A24/` launcher/failure evidence and current status/checkpoint.  Correct the assignment-derived server root and focused launcher preflight before one new paired lifetime. |
| **nonissue/advisory** | A22 and A26 performed only their bounded prep/checkpoint work; no redundant hardware lifetime or resource conflict was found.  Their target endpoints cannot establish a counting pass after the primary/run-local findings. | respective `STATUS.md`, `PARALLEL_CHECKPOINT.md`, and clean-F signals. |
| **nonissue/advisory** | Cadence satisfied the 120-second target after the alarm's pre-launch scan; records are approximately 75–91 seconds apart.  Optional watcher supplied four real post-launch polls and stopped cooperatively. | clean-F `MANAGER_LOG.jsonl`/`MONITOR_LOG.jsonl`; watcher events at `17:34:58`, `17:38:06`, `17:41:19`, `17:44:26` UTC. |

## Safety and shutdown

No evidence shows duplicate controllers, duplicate helper/lifetime ownership, conflicting board
leases, a reused request/relay, or unsafe hardware work.  The final scan and relevant-process
inventory report no live controllers, workers, helpers, MCP descendants, requests, leases,
conflicts, observation errors, or process errors.  The optional watcher and managed primary both
stopped cooperatively.  See `.agent-workspace/CURRENT_CANARY_READONLY_SCAN.json`,
`.agent-workspace/CURRENT_RELEVANT_PROCESS_INVENTORY.json`,
`.agent-workspace/CANARY_ACTIVE_EPOCH.json`, and primary clean-F state/events.

## Narrow follow-up

1. Add focused primary coverage for live request/relay discovery under each run's
`.agent-workspace/manager-requests` and `manager-relays`; retest the discovery path only.
2. Correct D31's redirect-following helper and A24's assignment-derived server-root launcher;
host-test each, then give each a fresh lifetime/request only as required.
3. Treat `hwa-e020…` as a finalization transient; do not change watcher code unless it persists
across a later identity-reconciliation delta.

No server code, production repair loop, broad monitor refactor, or replay of accepted evidence is
warranted.
