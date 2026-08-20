# Canary sprint target — 20260731-s1-clean-d

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; supervision alarm: `90 seconds`; heartbeat timeout: `420 seconds`  
Optional diagnostic watcher poll interval: `300 seconds`

## Success benchmark

This sprint counts as the first consecutive issue-free sprint only if every launched lane reaches
its bounded benchmark, the manager performs fresh whole-suite supervision at no more than 120-second
intervals from **before lane launch**, all eligible nonconflicting work is scheduled promptly, the
primary harness and optional watcher behave correctly, shutdown is exact, and the persistent
Terra-medium auditor accepts the result.

Initial concurrent batch:

1. **Atlas/A22 on STM-A** — preserve B12/B15/B35/B36 and every selector/routing diagnostic. Start
   one fresh isolated lifetime. Use the live server's current connection ID
   `probe:066FFF514988525067233337` in `connection_assignments`, complete the open B14 reset/boot
   oracle, and stop at completed B14 or the first exact B34 manager-request checkpoint. Do not
   repeat closed cases.
2. **Boreal/D31 on STM-B** — preserve the Windows-safe helper fix and the prior truthful
   disconnected result. Start one fresh isolated lifetime, process the returned setup-research and
   `continue_setup` route until STM-B is validated/connected, then perform exactly one newly planned
   RST01 `reset_and_run` and record the post-action state. Stop before APP-1 breakpoint work.
3. **Cygnus/A24 on NRF-A+NRF-B** — preserve both single-board and the paired no-flash canaries.
   Start two fresh isolated paired lifetimes with distinct UV roots, obtain current setup/flash
   plans for the already built PING/PONG artifacts, publish/service one exact request at a time,
   and reach the first truthful post-flash identity/UART checkpoint on both boards. No diagnostic
   replay, RF campaign, or unnecessary retry.

**Delta/A26** launches immediately after Atlas releases STM-A. The manager supplies a new isolated
assignment. Delta uses the run-local launcher and MCP stdio client under
`fresh-experiments/A26_20260726-062325/.agent-workspace/` (or a minimal focused derivative inside
that run) to create one lane-correlated local MCP lifetime; it does not depend on an IDE-injected MCP
tool surface. It then executes only the prepared `+8/+1/+1/+0` counter-delta measurement with one
fresh plan/request/relay and stops at the persisted evidence checkpoint.

## Manager supervision and relay contract

- Start the 90-second alarm loop before launching any lane. Every alarm takes a new no-write scan,
  logs every current-epoch lane to both manager and monitor JSONL, and renews the heartbeat.
- Inspect every notification and current lane tail. Never acknowledge from a cached scan.
- A doer keeps at most one helper and request alive. The manager validates assignment, snapshot,
  board, action, artifact, losses, final state, request hash, and producer lifetime before writing
  an exact relay.
- A waiting or failed lane blocks only its actual descendants and conflicting leases. It never
  stops unrelated work.
- No server edit is permitted unless the manager independently validates a production defect and
  enters the design-charter/change-loop process.

## Stop boundary

Keep the epoch live through at least one real optional-watcher poll after lane activity. When all
launched lanes reach their benchmarks, reconcile exact process/lease cleanup, stop the optional
watcher and primary harness cooperatively, capture a final fresh scan/inventory, and submit the
sprint to the same persistent Terra-medium auditor. Preserve all experiment progress even if the
sprint does not count.
