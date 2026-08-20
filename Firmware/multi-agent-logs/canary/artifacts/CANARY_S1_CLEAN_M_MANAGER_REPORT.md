# Canary Clean-M manager report

Epoch: `20260731-s1-clean-m`  
Disposition: **NONCOUNTING — independent audit required**  
Counter before/after manager review: `0/3` -> `0/3`

## Benchmark result

Clean-M did not satisfy any of its four counting endpoints. It nevertheless preserved accepted
earlier evidence, completed all four host-preparation slices, exercised concurrent persistent
Luna lanes, exercised the primary harness through live transitions and exact acknowledgements,
and produced useful bounded failure evidence without repeating accepted hardware actions.

- **Atlas / A22:** the one live lifetime completed the required all-NULL setup-plan
  initialization, then a run-local adapter attempted to decode an empty/non-JSON response.
  B14 and its populated manager request were not reached. No board action occurred and exact
  cleanup passed.
- **Boreal / D31:** the accepted RST01 checkpoint was preserved. The one released APP-1
  lifetime reached provider startup, but the run-local controller missed the actual
  `pyocd-debug-mcp.exe` identity in its bounded pre-public capture and failed closed before any
  public MCP operation. No setup, breakpoint, UART action, step, RST01 repeat, or APP-3 action
  occurred. Exact helper/launcher/uv/provider/Python absence was independently checked.
- **Cygnus / A24:** the accepted paired flash and post-flash identity/UART evidence was
  preserved. The one paired no-flash attempt spawned both exact roots, then failed before a
  public MCP artifact with `OSError(22, "Invalid argument")`. No flash, RF transmission, setup,
  or board operation occurred. Both delayed absence checks passed.
- **Delta / A26:** the pre-release turn consumed no lifetime. After the manager released STM-A,
  one exact live command received the public initialize response (`pyocd-debug 1.28.1`) and then
  failed closed while normalizing a CIM row with an invalid `ProcessId`. No setup, manager
  request, board/UART operation, counter measurement, or retry occurred. Cleanup proof reports
  zero provider processes and zero Clean-M lifetime files.

No `RESULT.json` was created for an incomplete endpoint. No BYO-Firmware-MCP production defect
was established and no server repair was opened.

## Harness and watcher observations

1. **Manager launch topology failure.** The first primary watcher owner and first Cygnus live
   controller were started under transient tool-shell jobs and were reaped without normal exit
   records. Neither had reached MCP/provider/hardware action. The manager recovered the primary
   watcher and the unstarted Cygnus continuation with Windows
   `CREATE_BREAKAWAY_FROM_JOB | CREATE_NO_WINDOW`. This manager operational failure alone makes
   Clean-M noncounting.
2. **Optional watcher discontinuity.** The optional watcher PID `174288` produced five evaluated
   polls, all `defect=false`, through `2026-07-31T21:52:00Z`, then disappeared with the same
   launch-topology disruption and no service-stop record. It was not restarted inside the
   invalidated epoch.
3. **Possible primary priority-starvation defect.** Delta's current checkpoint event
   `e7d3c7d4d5845701f4051f9ea9079364e8f5a1322767ec2f7f73155cdb7fadd1` was recorded while a
   higher-priority actionable event was pending. After the higher-priority event was reviewed and
   acknowledged, the still-unreviewed manager signal never became pending. The manager found and
   reviewed it directly in `events.jsonl`. Independent audit must decide whether the primary
   selection/re-arm logic incorrectly drops lower-priority immutable events observed in the same
   scan.
4. **Transient exit-race signal.** The primary harness briefly classified Delta as stale because
   the controller had written `CODEX_EXITED` about five seconds before its exact process tree
   finished exiting. The condition cleared automatically. Independent audit should decide whether
   this is acceptable conservative behavior or needs lifecycle grace/ordering.
5. The recovered primary managed watcher shut down cooperatively with
   `exit_reason=stop-requested`; exact owner/watcher identities are absent. The optional watcher,
   every lane controller/Codex process, and every Clean-M helper/MCP/provider identity are absent
   in the final process inventory.

## Principal evidence

- Target: `.agent-workspace/CANARY_S1_CLEAN_M_TARGET.md`
- Manager log: `.agent-workspace/ORCHESTRATOR_HARNESS/MANAGER_LOG.jsonl`
- Final scan: `.agent-workspace/CANARY_S1M_FINAL_SCAN.json`
- Final process inventory: `.agent-workspace/CANARY_S1M_FINAL_PROCESS_INVENTORY_BEFORE_STOP.json`
- Primary events/runtime:
  `orchestrator_harness/canary-20260731-s1-clean-m-state/events.jsonl` and
  `managed-watch-runtime.json`
- Optional watcher: `harness_watcher/runs/20260731-s1-clean-m/watcher/events.jsonl`
- A22 cleanup:
  `fresh-experiments/A22_20260726-062324/.agent-workspace/mcp-runtime/a22-b14-s1-clean-m/evidence/clean-m-cleanup-audit.json`
- A24 result:
  `fresh-experiments/A24_20260726-052146/.agent-workspace/canary/20260731-s1-clean-m/Cygnus/A24/PAIRED-PRE-RF/evidence/paired_result.json`
- D31 checkpoint:
  `fresh-experiments/D31_20260726-062325/.agent-workspace/CLEAN_M_LIVE_CHECKPOINT.md`
- A26 bounded stop and cleanup:
  `fresh-experiments/A26_20260726-062325/.agent-workspace/evidence/clean-m/s1m-bounded-functional-stop.json`
  and `s1m-cleanup-proof.json`

## Required independent decisions

The persistent canary auditor must independently decide:

1. whether the lower-priority Delta checkpoint was genuinely lost from the actionable queue;
2. whether a primary-harness repair is required for that behavior;
3. whether the five-second controller-exit race is a defect or acceptable conservative noise;
4. whether the breakaway launch contract must become a durable manager-side launcher/helper;
5. whether any optional-watcher defect exists beyond the manager's transient-job launch error;
6. whether all cleanup and non-retry claims are supported.

Clean-M cannot increment the success counter under any audit outcome.
