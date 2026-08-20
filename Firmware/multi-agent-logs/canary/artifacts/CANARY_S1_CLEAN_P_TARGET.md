# Canary sprint target ? `20260731-s1-clean-p`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent supervision: `75 seconds`; optional watcher poll: `180 seconds`

## Purpose and counting benchmark

Clean-P is the first fresh successor after the independently accepted Clean-O optional-watcher repair. It resumes the four persistent Luna-high/default lanes from their truthful Clean-O checkpoints, corrects only the four evidenced run-local blockers, and advances one bounded fresh live endpoint per lane without repeating accepted evidence. It counts as sprint 1 only if every lane reaches its truthful bounded endpoint/checkpoint, the primary harness and repaired optional watcher remain truthful, the manager follows `.agent-workspace/CANARY_MANAGER_FORMAL_REVIEW_GATE.md`, subagents remain bounded and cooperative, and exact cleanup leaves no relevant process. A truthful catalog/run-local failure is evidence; a validated harness, watcher, orchestration, looping, lease, or subagent-control issue makes the sprint noncounting.

## Host-only correction gate

Launch all four persistent sessions concurrently with only doer/workspace/launcher leases. In this first turn they may edit only their own experiment workspace and run focused host/fake tests. They must not start a provider/MCP lifetime, enumerate or touch hardware, create a manager request/relay, or consume a board lease. Each must write `CLEAN_P_PREPARED.md` and stop at `BUILT_WAITING_FOR_LEASE`.

- **Atlas/A22:** accept authoritative plain-text all-NULL `board_setup-plan` guidance while preserving JSON capture/classification, exact relay validation, and fail-closed handling for unrelated malformed/truncated responses.
- **Boreal/D31:** make the same bounded response-handling correction in the APP-1 helper and preserve the accepted breakpoint workflow.
- **Cygnus/A24:** replace the run-local manager-gated live stub with a real paired no-flash/no-RF P controller assembled from the already validated durable relay/launcher path; host tests must prove both dry paths and exact cleanup without provider start.
- **Delta/A26:** handle `setup_assignment_required` with `routes=[]` without indexing; follow the current setup-assignment route safely while retaining exact identity and cleanup checks.

## Bounded live endpoints

After the manager independently reviews each host gate, provider starts are serialized only for enumeration. Each endpoint has one fresh P lifetime/paired attempt and no same-epoch retry.

1. **Atlas/A22/STM-A:** complete B14 or reach one truthful populated, manager-reviewed B14 read-only request after NULL-first setup. B34 may follow only after B14 is accepted.
2. **Boreal/D31/STM-B:** without repeating RST01, set the plan-bound `app_dispatch_command` breakpoint, trigger `status\r\n`, capture halt/PC/R0-R3, perform exactly one step, and stop before resume/removal/APP-3/under-reset.
3. **Cygnus/A24/NRF-A+NRF-B:** one paired no-flash/no-RF lifetime records reset/BUSY timing and coherent `GetStatus`/`GetDeviceErrors` checkpoints for both retained CoreSX1262 paths.
4. **Delta/A26/STM-A:** only after Atlas's exact release, complete the retained `+8/+1/+1/+0` counter/version measurement without repeating R16.

A blocked or failed lane stops only itself; unrelated eligible lanes continue. No production-server repair begins without independent proof of a production-code defect.

## Manager review and stop benchmark

The manager owns a wall-clock whole-suite review deadline independent of pending event delivery. A due review preempts ordinary event draining; write the review, acknowledge the exact `MANAGER_REVIEW_DUE` ID when pending, prove `review_baseline_utc` advanced, heartbeat, and immediately rescan eligibility. Do not insert artificial 20?30 second sleeps after acknowledgements. Record deadlines, review files, event IDs, acknowledgement times, and baseline before/after.

Stop after every lane reaches its first truthful P endpoint/checkpoint. Cooperatively stop exact lane descendants, optional watcher, and primary owner/watcher; prove absence. Write a manager report and send the complete sprint to the same persistent Terra-medium auditor. Advance the counter only on an independent issue-free counting verdict.
