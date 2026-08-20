# Canary sprint target — 20260731-s1-clean-f

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent alarm: `75 seconds`; optional watcher poll:
`180 seconds`

## Why this is an appropriate benchmark

Clean-E converted all four lanes into precise, bounded corrections but did not reach a hardware
endpoint. Clean-F must validate the two repaired monitor surfaces and the three run-local repairs
while making substantial progress on both board families. It spans four persistent lanes, both STM
fixtures in serial turnover, both nRF fixtures together, multiple exact manager requests, at least
two real optional-watcher polls, and exact shutdown. It stops before unrelated application
campaigns, making the benchmark long enough to expose orchestration defects without reopening
accepted expensive work.

## Counting benchmark

The sprint counts only if every endpoint below is reached without redundant attempts or resource
conflicts, all manager reviews use fresh scans no more than 120 seconds apart, every request is
reviewed or explicitly rejected before deadline, both monitor surfaces behave correctly, shutdown
is exact, and the persistent sprint auditor accepts it.

1. **Atlas / A22 / STM-A:** preserve B12/B15/B35/B36. In one new assigned lifetime, use the live
   returned connection ID and setup route, complete the exact setup request/relay, then complete B14
   or stop at its first manager-reviewed populated read-only request if the live route requires a
   second permission boundary. Do not begin B34 unless B14 is manager-accepted during this sprint.
2. **Boreal / D31 / STM-B:** use one new assigned lifetime with the corrected per-role creation
   identity, complete setup, execute exactly one manager-approved RST01 `reset_and_run`, persist
   post-action state, and stop before APP-1 breakpoint work.
3. **Cygnus / A24 / NRF-A+NRF-B:** generate fresh launchers through the validated UV preflight, use
   one new paired lifetime, and reach the first truthful post-flash identity/UART checkpoint on both
   boards. Do not start the RF campaign.
4. **Delta / A26 / STM-A:** keep board-free R16/preparation locked. Start immediately after Atlas
   releases STM-A and persist the prepared `+8/+1/+1/+0` counter/version measurement in one new
   lifetime.

## Parallel/resource schedule

Launch all four bounded doer turns in the same scheduling batch. Boreal and Cygnus may perform
their fresh board-free preflight while Atlas briefly owns provider enumeration. Delta begins with
its no-hardware assignment check, then waits without polling until STM-A is released. Serialize
only provider enumeration and exact conflicting board/probe/UART/server-lifecycle leases. A blocked
lane never stops unrelated work.

## Manager and monitor requirements

- Start the 75-second supervision alarm and verify its first successful scan before any lane.
- Start exactly one new primary managed watcher and one optional diagnostic watcher with new output
  roots; never reuse clean-E cursor/notifications.
- Read a fresh scan and current lane tails at 90–120 second cadence. Acknowledge only events actually
  reviewed. Historical stopped-lane signals may remain in snapshots/events but must never become
  active pending notifications.
- Stop a returned checkpointed controller promptly; do not wait for `LANE_NO_PROGRESS`.
- Bind every relay to the exact request hash, lane, process lifetime, server snapshot, tool, and
  arguments. Never reuse an old request or relay.
- No production-server edit unless the manager independently validates a production defect.

## Stop and audit boundary

When all four endpoints are reached, or one bounded functional issue prevents an endpoint without
an unauthorized retry, let unrelated lanes reach their endpoints, then stop optional watcher and
primary watcher cooperatively. Verify exact controller/helper/MCP absence and zero live leases,
capture final scan/inventory, and submit the full sprint to the same persistent Terra-medium
auditor. Preserve all useful evidence even if the sprint is non-counting.
