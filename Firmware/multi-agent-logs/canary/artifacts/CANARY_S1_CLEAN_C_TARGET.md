# Canary sprint target — 20260731-s1-clean-c

Counter before sprint: `0/3`  
Manager: current root session, sole scheduling/relay/evidence authority  
Primary harness review interval: `120 seconds`; heartbeat timeout: `420 seconds`  
Optional watcher poll interval: `300 seconds`

## Success benchmark

This sprint counts only if the general success rule in
`.agent-workspace/CANARY_SPRINT_STATE.md` passes and the persistent Terra-medium auditor accepts
the sprint. The prior clean-B attempt is not rerun; all work begins at its accepted checkpoints.

Initial concurrent batch:

1. **Atlas/A22** — board-free reconcile the closed clean-B missing-terminal-record boundary without
   inventing evidence. Retain the corrected executable-only selector and focused tests. Then, under
   one new STM-A lease/root, write the exact lane-correlated lifetime before setup, complete the
   live B14 request/oracle, preserve B12/B15/B35/B36, and stop at either completed B14 or the first
   exact B34 manager-request checkpoint.
2. **Boreal/D31** — board-free replace only `os.kill(pid,0)` with a Windows-safe exact PID plus
   creation-time identity check and pass the focused one-outstanding-helper regression. Reconcile
   that clean-B never started MCP. Then, under one new STM-B lifetime, follow the current setup/load
   route, service one outstanding request at a time, execute one approved RST01 `reset_and_run`,
   record final state, and stop before APP-1 breakpoint work.
3. **Cygnus/A24** — board-free classify and minimally fix the paired pre-provider launcher/helper
   `OSError(22)` using only focused host checks. Under fresh NRF-A+NRF-B roots, run one paired
   no-flash ownership/provider-start classification. Preserve both accepted single-board canaries,
   use no flash/RF campaign, prove exact cleanup, and stop at the paired classification checkpoint.

**Delta/A26** starts immediately when Atlas releases STM-A. It executes only the already-prepared
`+8/+1/+1/+0` counter-delta HIL slice under a fresh exact lifetime/plan/request/relay and stops at
that evidence checkpoint. It does not wait for Boreal or Cygnus.

## Operational correction

An independent manager alarm is due every 90–120 seconds while any lane is live. Every supervision
record must be based on a new no-write harness scan taken immediately before the record; cached
scans are forbidden. Each pass inspects controller and Codex identity, current JSONL tail,
checkpoint/signals, helper/MCP lifetime, outstanding request, and lease state for every live lane,
then appends one record per lane to both manager and monitor logs. Relay work does not substitute
for the pass.

A doer may keep exactly one helper and exact request open while waiting for the manager. It must not
open a replacement lifetime or request until the first is serviced or explicitly closed. The
manager reviews assignment, snapshot, board, action, request hash, live process identity, and expiry
before writing a relay.

## Stop boundary

Keep the epoch active through at least one real optional-watcher poll after lane activity. After
every launched lane reaches its stated checkpoint, reconcile exact process and lease cleanup, stop
both watchers cooperatively, and reuse the persistent Terra-medium auditor. Preserve useful
experiment progress even if the sprint is non-counting.
