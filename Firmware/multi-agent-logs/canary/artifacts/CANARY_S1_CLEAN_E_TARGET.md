# Canary sprint target - 20260731-s1-clean-e

Counter before sprint: `0/3`
Manager: current root session, sole scheduler/relay/evidence authority
Primary review interval: `120 seconds`; supervision alarm: `75 seconds`; heartbeat timeout: `420 seconds`
Optional diagnostic watcher poll interval: `180 seconds`

## Why this is an appropriate benchmark

Clean-D proved all four lane-controller and local-MCP paths but stopped before target actions. Clean-E
must convert those exact bounded findings into substantial experiment progress without replaying
locked work. The benchmark spans all four persistent lanes, both board families, serial resource
turnover on STM-A, multiple permission relays, at least two optional-watcher polls during live work,
and exact shutdown. It is long enough to expose orchestration, monitor, and watcher defects but
stops before unrelated application campaigns.

## Success benchmark

This sprint counts only if all four lane endpoints below are reached, the manager uses fresh scans
at no more than 120-second intervals from before launch, every exact request is reviewed before its
deadline, eligible work is scheduled promptly, the primary harness and optional watcher behave
correctly, shutdown is exact, and the persistent Terra-medium auditor accepts the sprint.

### Concurrent preparation and resource order

Launch all four persistent Luna-high/default doers together. Atlas owns the first short global
`provider-enumeration` lease. Boreal, Cygnus, and Delta must perform only their focused run-local
preparation while that lease is held, then checkpoint and return if they need it; they do not spin
or poll. Resume each immediately when its actual resource becomes eligible. Provider enumeration is
serialized only through `setup_overview`/connection-list capture; later nonconflicting work overlaps.

1. **Atlas/A22 / STM-A** - preserve B12/B15/B35/B36 and all clean-D evidence. In one fresh lifetime,
   capture a live setup overview under the enumeration lease and use only a current returned debug
   connection ID. Complete B14. If B14 closes, stop at the first exact B34 request or bounded oracle.
2. **Boreal/D31 / STM-B** - focused prep adds required `board_id` to the run-local `continue_setup`
   path and runs only focused helper tests. After the enumeration lease is granted, use one fresh
   lifetime, connect STM-B, execute exactly one fresh RST01 `reset_and_run`, and persist post-action
   state. Stop before APP-1 breakpoint work.
3. **Cygnus/A24 / NRF-A+NRF-B** - focused prep corrects the runner to use exact official Nordic
   CMSIS-Pack evidence with required `board_id`, declares `declared_lane_id` plus request-hash
   sidecars, and never invents `board_fix_setup`. After the enumeration lease is granted, use one
   fresh paired lifetime and reach the first truthful post-flash identity/UART checkpoint on both
   boards. Do not begin the RF campaign.
4. **Delta/A26 / STM-A** - focused prep proves assignment-derived roots and the repaired command
   state permit `setup_overview`. After Atlas releases STM-A and the enumeration lease is granted,
   use one fresh lifetime and persist the prepared `+8/+1/+1/+0` counter/version measurement.

## Manager supervision and relay contract

- Start the 75-second fresh-scan alarm before any lane launch. Each pass scans current state, logs
  every current-epoch lane to both manager and monitor JSONL, and renews the heartbeat.
- Inspect every fresh notification and lane tail. Never acknowledge from a cached scan.
- Review HELP/request events immediately and well before their deadline. Bind a relay to the exact
  live request hash, declared lane, board, action, artifact, and producer lifetime.
- Never relay an action not supported by the live server route. Reject invalid requests promptly
  with manager feedback so the doer can checkpoint without waiting for timeout.
- A doer has at most one helper and one request per board. A waiting lane blocks only its descendants
  and conflicting leases; later-row board-free work remains eligible.
- No server edit unless the manager independently validates a production defect and enters the
  design-charter/change-loop process.

## Stop boundary

Keep the epoch live through at least two real optional-watcher polls after lanes launch. When every
lane reaches its endpoint, or a single bounded issue makes that endpoint impossible without an
unauthorized retry, reconcile exact cleanup, stop optional watcher then primary harness
cooperatively, capture a final fresh scan/inventory, and submit to the same persistent
Terra-medium auditor. Preserve all progress even if non-counting.
