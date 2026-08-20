# Canary sprint target — `20260731-s1-clean-q`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `180 seconds`; independent supervision: `60 seconds`; optional watcher poll: `180 seconds`

## Purpose and counting benchmark

Clean-Q is the fresh successor to independently audited noncounting Clean-P. It preserves all accepted experiment evidence, corrects only the four evidenced run-local failures, and advances one bounded fresh endpoint per persistent lane. It counts as sprint 1 only if all four lanes reach their declared truthful endpoint/checkpoint with no harness, watcher, manager, orchestration, looping, lease, or subagent-control issue; exact cleanup must leave no relevant process. A truthful product/test failure may be evidence, but a preventable run-local controller failure makes the sprint noncounting.

## Host-only correction gate

Resume all four persistent Luna-high/default sessions concurrently with only doer/workspace/launcher leases. They may edit only their own experiment workspace and run focused host/fake tests. They must not start a provider/MCP lifetime, enumerate or touch hardware, create a manager request/relay, or consume a board lease. Each writes `CLEAN_Q_PREPARED.md` and returns at `BUILT_WAITING_FOR_LEASE`.

- **Atlas/A22:** accept authoritative plain-text `initialization_handshake` guidance while preserving JSON capture and fail-closed handling for actually malformed/truncated responses. Isolate all host/fake-test artifacts from the fresh live-Q runtime/evidence namespace. Test the exact Q controller entrypoint and response parser.
- **Boreal/D31:** implement a true Q helper/controller with Q-only epoch, request IDs, phases, launcher labels, runtime roots, and artifact paths. Construct the current populated `board_setup-plan` request with every live-required expected-return field and setup fact. Test the exact Q entrypoint and request schema; do not copy stale M metadata.
- **Cygnus/A24:** correct all Q signal IDs, paths, phases, and labels before use. Exercise the exact paired Q initialize transport against a bounded fake provider and prove it can obtain both first public artifacts without timing out; retain exact descendant cleanup.
- **Delta/A26:** fix the preflight predicate so numeric zero is not treated as boolean failure; use `setup_result` consistently after the NULL setup call. Test the exact Q entrypoint through the setup route and prove one-pass preflight.

The manager independently checks each prepared gate before granting any live lease. No doer may improvise a second correction/live attempt inside the same phase.

## Bounded live endpoints

After host-gate acceptance, provider starts are serialized only for enumeration. Each endpoint gets one fresh Q lifetime/paired attempt and no same-epoch retry.

1. **Atlas/A22/STM-A:** complete B14 or reach one truthful populated, manager-reviewed B14 read-only request after NULL-first setup. B34 may follow only after B14 is accepted.
2. **Boreal/D31/STM-B:** without repeating RST01, set the plan-bound `app_dispatch_command` breakpoint, trigger `status\r\n`, capture halt/PC/R0-R3, perform exactly one step, and stop before resume/removal/APP-3/under-reset.
3. **Cygnus/A24/NRF-A+NRF-B:** one paired no-flash/no-RF lifetime records reset/BUSY timing and coherent `GetStatus`/`GetDeviceErrors` checkpoints for both retained CoreSX1262 paths.
4. **Delta/A26/STM-A:** only after Atlas's exact release, complete the retained `+8/+1/+1/+0` counter/version measurement without repeating R16.

A blocked or failed lane stops only itself; unrelated eligible lanes continue. No production-server repair begins without independent proof of a production-code defect.

## Manager review and stop benchmark

`.agent-workspace/CANARY_MANAGER_FORMAL_REVIEW_GATE.md` is mandatory. While any controller is active, the manager maintains an independent wall-clock deadline and completes a whole-suite review at least every 150 seconds (stricter than the configured 180-second harness reminder). A due review preempts ordinary event draining. Each review records its authored time, previous acknowledged baseline, active lane identities, exact work/progress, requests/relays, leases, anomalies, and next deadline. The manager then acknowledges the exact pending review event, proves the harness baseline advanced, heartbeats, and immediately rescans eligibility. No ordinary task may consume the manager long enough to miss this gate.

Stop after every lane reaches its first truthful Q endpoint/checkpoint. Cooperatively stop exact lane descendants, optional watcher, and primary owner/watcher; prove absence. Write a manager report and send the complete sprint to the same persistent Terra-medium auditor. Advance the counter only on an independent issue-free counting verdict.
