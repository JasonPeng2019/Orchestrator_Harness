# M5 sprint checkpoint ? 20260802-m5-s1a-061555Z

> Historical disposition notice: the current-policy re-audit in `THREE_GATE_REAUDIT.md` supersedes
> this checkpoint's old perfect-run `RESET` disposition and records S1a as `QUALIFYING (1/3)`.
> Original findings below remain unchanged historical evidence.

## Root disposition

**RESET ? accepted count remains 0/3.**

This sprint is not counted. No native code repair is justified by the invalidating findings; the next attempt uses corrected direct operating order and a complete final harness drain.

## Evidence summary

- Four genuine HELP requests from Atlas/A22, Boreal/D31, Cygnus/A24, and Delta/A26.
- All four have complete six-stage wake chains and unique wake IDs.
- Quiet control: valid 15-second `WATCH_TIMEOUT`, no wake.
- Busy control: Delta request created inside the 30-second manager hash audit; it was observed after busy work ended, so no busy-delay attribution.
- Watcher: diagnostic-only, evaluator disabled, 379 explicit skips, zero route rejects, zero attention errors, cursor drained, clean stop.
- Harness/watcher/workers: all 12 recorded process identities absent after shutdown; no unexpected epoch process; no leases, board tokens, or MCP servers.
- Python fingerprint and all 11 sealed inputs match. `validate_sprint_finalize`: pass, 214 records.

## Root audit of reviewer findings

1. **Accepted ? Atlas evidence invalid.** The first claim/response recorder calls used a non-allowlisted source ID and failed. The response was then acknowledged before valid claim/response records were emitted. This caused `response_to_ack_seconds=-15.422541`. It is an operator-order defect, not a native recorder defect.
2. **Accepted as observed behavior, not yet a repair finding ? harness queue delay.** Boreal and Cygnus were intentionally deferred behind earlier pending events and became actionable 179.210 s and 101.552 s after observation. Delivery itself reached the manager in about 2.3-2.5 s. Retest with prompt claim/ack order; do not change code on one contaminated sprint.
3. **Accepted ? watcher health and isolation pass.** No forbidden assistance influenced request discovery. Post-sprint transcript inspection occurred only after invocation finish and native shutdown for cleanup.
4. **Accepted ? quiet control.**
5. **Accepted with limitation ? busy request was created during busy work, but its observation occurred afterward; it does not demonstrate manager-busy handling delay.**
6. **Partially rejected ? cleanup process identities pass, but log drain does not.** Contrary to the reviewer?s lenient treatment, explicit M5 Stage 7 requires draining every harness notification. `pending-notification.json` still retains unacknowledged `MANAGER_REVIEW_DUE` event `df8bf...10cd` plus deferred checkpoint controls. That is an evidence/drain defect and independently requires RESET.
7. **Rejected as unnecessary for M5 ? a separate `MANAGER_DECISION_RECORDED` event is not part of the required six-stage chain.** The durable response contains the decision and timestamp. Continue to record claim and response explicitly.

## Smallest correction for the next attempt

- Use `source_id=main-orchestrator` on the first recorder call.
- Strict order: wait receipt -> valid claim record -> write/publish response -> exact acknowledgement. Never acknowledge after a failed record operation.
- Before invocation finish/shutdown, keep using direct blocking harness waits to drain and acknowledge every control event; run the final watcher poll only after the harness pending/deferred set is empty.
- No runner, wrapper, relay, helper program, or native code change.

## Workload outcome

Workers finalized host-only proposal checkpoints. This is workload-only and does not affect M5 disposition.
