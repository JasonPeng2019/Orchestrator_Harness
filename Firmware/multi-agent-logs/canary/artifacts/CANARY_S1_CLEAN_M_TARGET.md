# Canary sprint target - `20260731-s1-clean-m`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent supervision: `75 seconds`; optional watcher
poll: `180 seconds`

## Purpose and counting benchmark

Clean-M is the first live successor after the independently accepted Clean-K primary-harness
lifecycle/actionability repair. It advances only unmet or immediately following catalog work.
It counts as one issue-free sprint only if all four bounded endpoints below complete, every
manager-review interval is explicitly acknowledged with a whole-suite review, all current exact
requests are reviewed and relayed before deadline, the primary harness and optional watcher have
no validated defect, and shutdown proves exact process/resource absence. Preserve every accepted
Clean-K endpoint and all earlier locked evidence; do not rerun D31 RST01, the A24 paired flash, or
the A24 post-flash identity/UART checkpoints.

## Concurrent board-free correction/preparation phase

Resume all four persistent Luna sessions concurrently with only their doer/workspace/launcher
leases. No provider, MCP, board, serial, probe, radio, or server-lifecycle lease exists in this
phase.

- **Atlas/A22:** correct only the retained Clean-K Windows `GetProcessTimes` handle/creation-time
  recorder, prove exact PID+creation capture with focused host tests, and prepare one fresh L B14
  continuation using the already-proved NULL-first setup order.
- **Boreal/D31:** preserve the accepted RST01 checkpoint and prepare the next APP-1
  `command_dispatch` breakpoint/hit/one-step slice using the locked A20 ELF and UART baseline.
- **Cygnus/A24:** preserve both accepted flash and post-flash checkpoints; prepare a no-flash,
  pre-RF paired slice that proves reset/BUSY timing plus coherent `GetStatus` and
  `GetDeviceErrors` evidence on both CoreSX1262 paths. RF transmission remains disabled.
- **Delta/A26:** correct only the retained Clean-K exact provider-process matcher so it recognizes
  the actual launcher/uv/`pyocd-debug-mcp.exe` ancestry without weakening PID+creation proof, and
  prepare the preserved `+8/+1/+1/+0` measurement in one fresh L lifetime.

Each lane writes a fresh `CLEAN_L_PREPARED.md`, focused host proof, and nonterminal checkpoint. A
host correction must not rewrite retained evidence or create `RESULT.json`.

## Counting endpoints

1. **Atlas/A22/STM-A:** one fresh L lifetime completes B14, or reaches its first truthful populated
   manager-reviewed B14 read-only request after the already-proved NULL-first setup. Preserve
   B12/B15/B35/B36; do not start B34 unless B14 is accepted and the target remains within this
   bounded turn.
2. **Boreal/D31/STM-B:** one fresh L lifetime sets the plan-bound APP-1 `command_dispatch`
   breakpoint, triggers it over UART, records the halted state and PC/argument evidence, performs
   exactly one step, then stops before resume/removal or any APP-3/under-reset work. Do not repeat
   RST01.
3. **Cygnus/A24/NRF-A+NRF-B:** one fresh paired no-flash lifetime records both pre-RF SPI
   reset/BUSY plus coherent `GetStatus`/`GetDeviceErrors` checkpoints using the retained flashed
   artifacts. Do not flash and do not transmit RF.
4. **Delta/A26/STM-A:** immediately after Atlas releases STM-A, one fresh L lifetime completes the
   prepared `+8/+1/+1/+0` counter/version measurement without redoing R16 or accepted preparation.

## Scheduling and manager procedure

Launch all four board-free turns together. When they checkpoint, release live work by real leases:
Atlas on STM-A, Boreal on STM-B, and Cygnus on the nRF pair may overlap; Delta starts immediately
after Atlas's exact STM-A cleanup. Serialize only the short provider-enumeration windows and exact
conflicting board/probe/serial/server-lifecycle roots. A waiting or failed lane never stops
unrelated eligible work.

The primary harness and optional watcher are read-only. The manager checks every live lane and the
pending notification at least every two to three minutes. At every `MANAGER_REVIEW_DUE`, the
manager performs and logs a whole-suite lane/request/lease review, acknowledges that exact event,
then rescans eligibility. Higher-priority request handling does not substitute for this formal
review. Every request/relay is immutable, exact-hash-bound, current-lifetime-bound, and reviewed by
the manager before execution. Valid manager-signal kinds are only `HELP`, `FEEDBACK`,
`INSTRUCTION`, `PASS`, and `CHECKPOINT`.

Each live lane gets one fresh bounded lifetime/paired attempt. A run-local failure checkpoints
without a same-epoch retry while unrelated work continues. Count only if all four endpoints are
reached with no duplicate controller/lifetime, missed request, stale actionable history, lease
conflict, supervision gap, manager-procedure defect, harness/watcher defect, or unclean shutdown.
Otherwise preserve useful progress, audit non-counting, and repair only independently validated
harness/watcher defects.
