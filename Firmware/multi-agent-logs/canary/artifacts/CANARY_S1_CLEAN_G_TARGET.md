# Canary sprint target — 20260731-s1-clean-g

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent alarm: `75 seconds`; optional watcher poll:
`180 seconds`

## Why this is an appropriate benchmark

Clean-F validated overlapping lanes, three exact relays, bounded supervision, and exact shutdown,
but exposed primary request discovery and two run-local entry gaps. The repairs are now host-green,
including a fresh repair-epoch integration regression that prevented expired historical signals
from occupying the live notification slot. Clean-G must exercise those repaired surfaces in live
use while reaching the same four bounded catalog endpoints. It spans both STM fixtures, both nRF
fixtures, current request/relay discovery, at least two optional-watcher polls, STM-A lease
turnover, and exact shutdown without reopening accepted expensive work.

## Counting benchmark

This sprint counts only if every endpoint below is reached without redundant attempts or resource
conflicts; all manager reviews use fresh scans no more than 120 seconds apart; every current request
is reviewed or explicitly rejected before deadline; historical expired signals never become
pending; both monitor surfaces behave correctly; shutdown is exact; and the same persistent
Terra-medium sprint auditor accepts the whole epoch.

1. **Atlas / A22 / STM-A:** preserve B12/B15/B35/B36. Rebind the host-green adapter to fresh
   clean-G roots. In one assigned lifetime, use the live returned connection/setup route and exact
   request-bound relays; complete B14 or stop at its first manager-reviewed populated read-only
   request if the live route requires another bounded permission boundary. Do not begin B34 unless
   B14 is accepted in this sprint.
2. **Boreal / D31 / STM-B:** rebind the host-green returned-route helper to clean-G. In one assigned
   lifetime, complete setup through any explicit `board_fix_setup`/load-validation route, execute
   exactly one manager-approved RST01 `reset_and_run`, persist post-action state, and stop before
   APP-1 breakpoint work.
3. **Cygnus / A24 / NRF-A+NRF-B:** use a fresh manager assignment containing the existing root
   server project, generate brand-new launchers through the host-green preflight, use one paired
   lifetime, and reach the first truthful post-flash identity/UART checkpoint on both boards. Do
   not start the RF campaign.
4. **Delta / A26 / STM-A:** preserve R16 and clean-F preparation. Rebind it to fresh clean-G roots,
   remain board-free while STM-A is owned, then immediately run the prepared `+8/+1/+1/+0`
   counter/version measurement in one new lifetime after Atlas releases STM-A.

## Parallel/resource schedule

Launch all four board-free rebind/preflight turns in the same scheduling batch. Start live provider
enumeration in short manager-controlled windows: A22 first, then D31 after A22's first public MCP
artifact, then A24 after D31's first public artifact. The resulting HIL lifetimes may overlap because
their board/probe/UART/state roots are disjoint. Delta stays board-free and takes STM-A immediately
after Atlas releases it. A waiting or failed lane never stops unrelated eligible work.

## Manager and monitor requirements

- Start the 75-second supervision alarm and prove its first scan before any lane.
- Start exactly one new primary managed watcher and one optional diagnostic watcher using clean-G
  output roots. Never reuse clean-F or repair-epoch cursor/notification state.
- Read a fresh whole-suite scan and every live lane tail every 90–120 seconds and immediately on a
  durable notification. Acknowledge only the exact reviewed event.
- Historical stopped-lane signals and expired/closed requests remain observable but must never
  occupy the pending notification slot or acquire a resource.
- Bind every relay to the exact current request hash, lane, live process identity, server snapshot,
  tool, arguments, and expiry. Never reuse a prior epoch request or relay.
- Stop a returned checkpointed controller promptly; do not wait for `LANE_NO_PROGRESS`.
- No production-server edit unless the manager independently validates a server defect.

## Stop and audit boundary

When all four endpoints are reached, or one bounded functional issue prevents an endpoint without
an unauthorized retry, let unrelated lanes reach their endpoints. Stop the optional watcher and
primary watcher cooperatively; verify exact controller/helper/MCP absence and zero leases/conflicts;
capture final scan/inventory; stabilize current records; and submit the entire sprint to the same
persistent Terra-medium auditor. Preserve all useful evidence even if the sprint is non-counting.
