# Canary audit — 20260731-long-canary-sprint-1-success-a

Auditor: persistent `/root/canary_sprint_auditor` (`gpt-5.6-terra`, medium reasoning)  
Decision: **NON-COUNTING**. Counter remains `0/3`.

## Valid issues

1. **Manager/orchestrator process defect:** per-lane supervision jumped from
   `15:01:46.262150Z` to `15:07:50.896293Z` while lanes were live. Relay/reconciliation work
   does not replace a durable per-lane inspection. Operational correction: use an independent
   two-minute supervision timer and log every live lane each pass. No harness code change.
2. **Atlas/A22 run-local defect:** the sole fresh B14 lifetime stopped before setup/request/oracle
   because the recorder inspected global pyOCD inventory. Fix helper-owned PID-tree selection and
   add a regression with an unrelated global pyOCD process.
3. **Boreal/D31 run-local process defect:** a second sequential helper/request was opened before
   the first request received a manager relay. No overlap or lease conflict occurred, but the work
   was redundant. Fix the helper to keep exactly one outstanding request/lifetime until relay or
   explicit manager closure; add a no-relay regression.

All three invalidate the sprint. The latter two are experiment-run helper defects, not production
server or harness/watcher defects.

## Non-issues

- Optional watcher: healthy real polls at 14:52, 14:57, 15:02, 15:08, and 15:11; no
  self-observation recurrence.
- Primary harness: final scan has all four lanes checkpointed/exited/releasable and zero conflicts
  or observation/process errors.
- Delta's awkward proposed-root absence flag is not a false HIL claim because the same evidence
  explicitly records no MCP/hardware/runtime.

## Preserved progress

A22 initialization/cleanup boundary and prior locked cases; D31 setup research/routing checkpoint;
A24 NRF-B no-flash PASS; A26 R16 and counter preparation. Do not rerun accepted evidence.

