# Canary sprint target — 20260731-s1-clean-b

Counter before sprint: `0/3`  
Manager: current root session, sole scheduling/relay/evidence authority  
Primary harness review interval: `120 seconds`; heartbeat timeout: `420 seconds`  
Optional watcher poll interval: `300 seconds`

## Success benchmark

This sprint counts only if the general success rule in
`.agent-workspace/CANARY_SPRINT_STATE.md` passes and the persistent Terra-medium auditor accepts
the sprint.

Initial concurrent batch:

1. **Atlas/A22** — board-free: fix only the B14 lifetime recorder so it selects the helper-owned
   PID tree; add the unrelated-global-pyOCD regression and pass focused tests. Then, under a fresh
   STM-A lease/root, use exactly one lifetime and one outstanding request at a time, complete the
   live B14 request/oracle slice, preserve B12/B15/B35/B36, and stop before B34 unless B14 closes
   early enough for a single bounded B34 request checkpoint.
2. **Boreal/D31** — board-free first: add the no-relay/no-second-helper regression and fix the
   run-local helper accordingly. Under one fresh STM-B lifetime, follow the returned setup/load
   route, disclose and service one RST01 plan/request, execute one approved `reset_and_run`,
   record the truthful final state, and stop before APP-1 breakpoint work.
3. **Cygnus/A24** — under fresh NRF-A+NRF-B roots, run only the paired no-flash
   ownership/provider-start classification. Preserve the accepted single-board canaries, use no
   flash/RF campaign, prove exact cleanup, and stop at the paired classification checkpoint.

Delta/A26 has no nonduplicative resource-compatible first slice while Atlas owns STM-A and Cygnus
owns the nRF pair. It is not launched merely to stay busy. As soon as Atlas releases STM-A, resume
Delta for the already-prepared `+8/+1/+1/+0` counter-delta HIL slice if the sprint is still open.

## Operational correction

A separate manager supervision alarm is due every 120 seconds while any lane is live. At each due
point the manager reads current controller identity, JSONL tail/checkpoint/signals, helper/MCP
lifetime, and lease state for every live lane and appends one record per lane to both manager and
monitor JSONL logs. Relay work never substitutes for this pass.

A doer may keep one helper waiting for an exact manager relay inside its current turn, but must not
open a replacement helper/lifetime while a request is outstanding. All exact relays remain
manager-authored after current-process, assignment, snapshot, board, action, and expiry review.

## Stop boundary

After every launched lane reaches the stated checkpoint, obtain at least one optional-watcher poll
after lane activity, reconcile exact process/lease cleanup, stop both watchers cooperatively, and
reuse the persistent Terra-medium auditor. Any useful progress remains preserved even if the
sprint is non-counting.

