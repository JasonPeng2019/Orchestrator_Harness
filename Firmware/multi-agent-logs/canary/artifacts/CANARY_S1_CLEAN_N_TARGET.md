# Canary sprint target — `20260731-s1-clean-n`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent supervision: `75 seconds`; optional watcher
poll: `180 seconds`

## Purpose and counting benchmark

Clean-N is the first successor after the independently accepted Clean-M harness repair. It uses
the new durable operator launcher for the primary owner, optional-watcher owner, and every external
lane controller. It advances four preserved nonterminal catalog tasks without repeating accepted
evidence. It counts only if all four bounded live endpoints complete, exact manager-review acks
advance the baseline, no role loops/retries or crosses a lease, the harness/watcher/orchestrator/
subagents show no validated issue, and exact cooperative cleanup leaves no relevant process.

Before any lane launches, retain the synthetic gate evidence proving (a) a launcher child survives
the short-lived launcher and is cleaned exactly, and (b) an exact synthetic
`MANAGER_REVIEW_DUE` acknowledgement advances `review_baseline_utc`.

## Concurrent board-free correction phase

Resume Atlas, Boreal, Cygnus, and Delta concurrently. Each gets only its doer/workspace/launcher
lease. Each reads its latest Clean-M checkpoint and fixes only the observed run-local pre-action
failure, writes a fresh `CLEAN_N_PREPARED.md`, runs focused host tests, and stops at a nonterminal
ready checkpoint. No provider, MCP, board, probe, serial, RF, server-lifecycle, or shared mutable
artifact lease exists in this phase.

- **Atlas/A22:** make the setup transport retain and classify the exact populated-plan response;
  an empty/non-JSON response must be diagnosed and corrected before a live launch. Preserve the
  accepted all-NULL setup ordering and B12/B15/B35/B36.
- **Boreal/D31:** make the APP-1 launcher capture the actual launcher/`uv`/
  `pyocd-debug-mcp.exe` ancestry and prove provider startup locally without touching hardware.
  Preserve accepted RST01.
- **Cygnus/A24:** eliminate the exact paired-launch `OSError(22)` before provider startup while
  retaining distinct per-board environments/roots and the no-flash/no-RF boundary. Preserve the
  accepted flash and post-flash checkpoints.
- **Delta/A26:** ignore malformed CIM rows such as nonnumeric `ProcessId` while still requiring one
  valid exact PID+creation ancestry match; prove malformed-only input fails closed. Preserve R16
  and the prepared `+8/+1/+1/+0` measurement.

Each correction gets one bounded host implementation attempt in its persistent Luna session. A
lane that cannot prove readiness checkpoints; unrelated lanes continue. No live attempt starts
from a red host proof.

## Counting live endpoints

After all applicable host proofs are green, launch every resource-compatible endpoint immediately:

1. **Atlas/A22/STM-A:** one fresh N lifetime completes B14, or reaches a truthful populated,
   manager-reviewed B14 read-only request after the accepted NULL-first setup. Do not run B34
   unless B14 is accepted and it fits the same bounded turn.
2. **Boreal/D31/STM-B:** one fresh N lifetime reaches APP-1, sets the plan-bound
   `app_dispatch_command` breakpoint, triggers `status\r\n`, records halt/PC/R0-R3, performs
   exactly one step, and stops before resume/removal, APP-3, or under-reset work. Do not repeat
   RST01.
3. **Cygnus/A24/NRF-A+NRF-B:** one fresh paired no-flash N lifetime records reset/BUSY timing and
   coherent `GetStatus`/`GetDeviceErrors` checkpoints on both retained CoreSX1262 paths. Do not
   flash or transmit RF.
4. **Delta/A26/STM-A:** immediately after Atlas's exact release, one fresh N lifetime completes
   the preserved `+8/+1/+1/+0` counter/version measurement without repeating R16.

Each lane gets exactly one fresh live lifetime/paired attempt. There is no same-epoch retry.

## Manager procedure

The primary harness and optional watcher are read-only. The manager checks the current pending
notification and individually inspects every live lane every two to three minutes. At each exact
`MANAGER_REVIEW_DUE`, the manager first writes a whole-suite review record, invokes canonical
`ack --event-id`, then immediately verifies and records that `review_baseline_utc` advanced before
rescheduling. Every request/relay is immutable, exact-hash-bound, current-lifetime-bound, and
reviewed before action. Valid signal kinds remain `HELP`, `FEEDBACK`, `INSTRUCTION`, `PASS`, and
`CHECKPOINT`.

Atlas/STM-A, Boreal/STM-B, and Cygnus/the nRF pair may overlap after serialized provider-
enumeration windows. Delta starts as soon as Atlas releases STM-A. A waiting or failed lane never
stops unrelated eligible work. No server repair barrier starts without an independently validated
production-server defect.

At the benchmark, stop lane/controller descendants exactly, stop the optional watcher
cooperatively, stop the primary owner/watch cooperatively, prove exact absence, write a manager
report, and send the complete sprint to the same persistent Terra-medium auditor. Any validated
issue keeps the counter at `0/3`; useful catalog evidence remains preserved.
