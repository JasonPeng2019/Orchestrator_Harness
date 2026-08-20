# Clean-M harness repair plan

Owner of plan/spec/scope: current main orchestrator  
Implementation agent after independent plan acceptance: persistent
`/root/canary_harness_coder` (Terra high)  
Independent plan/result auditor: persistent `/root/canary_sprint_auditor` (Terra medium)

## Slice 1 — focused failing notification tests

1. Add a focused managed-watch regression that creates, in one scan, a higher-priority current
   condition plus an actionable uncorrelated `MANAGER_SIGNAL`/checkpoint handoff.
2. Assert the higher condition is pending and the lower handoff is durably retained.
3. Transition the lane to exited, acknowledge the exact higher event, and assert the retained
   handoff becomes pending on the next scan without a new signal transition.
4. Stop/restart managed watch against the same output state after lane exit, both before and after
   the higher-priority acknowledgement, and assert the deferred handoff and its admission order
   survive and are delivered.
5. Add focused tests for fresh-output historical suppression, request-correlated supersession,
   backward-compatible loading, and exact-ack removal.
6. Run only those tests and record the expected red baseline before production edits.

## Slice 2 — durable handoff backlog

1. Extend notification-state serialization with an optional ordered `deferred` handoff list;
   missing fields load as empty.
2. Add a narrow notification helper that ranks all currently actionable conditions and identifies
   only file-backed durable handoff types (`MANAGER_SIGNAL`, `CHECKPOINT_UPDATED`,
   `RESULT_AVAILABLE`) eligible for deferral. At admission, persist the full immutable event plus
   its computed priority, normalized deadline/order key, identity, and admission timestamp.
3. In managed watch, collect newly actionable durable handoffs even while another event is pending.
   Deduplicate by event ID and never defer acknowledged events.
4. Before choosing a new pending event, prune only exact superseded request-correlated signals,
   merge current candidates with deferred handoffs, and select deterministically. Current
   candidates use current priority; deferred candidates use their **stored admission-time**
   priority/deadline/order and are never sent back through `_priority()` or current lane-liveness
   gating after admission. Persist the remainder.
5. Update exact acknowledgement so it clears the pending event without clearing unrelated deferred
   handoffs. Preserve current heartbeat/re-arm behavior.
6. Make the focused tests green, then run the affected notification/managed-watch suites.

## Slice 3 — manager-side detached launcher

1. Add `orchestrator_harness/operator_launch.py` as a standalone explicit CLI. Do not import it
   from `cli.py`, reconciliation, notification, watcher, or lane-controller paths.
2. Accept explicit `--receipt`, `--label`, `--role`, `--cwd`, optional
   `--expected-state-path`, and argv after `--`.
3. Validate paths/argv and exclusive-create the receipt reservation. Spawn without a shell using
   Windows breakaway/no-window flags or a POSIX new session. Capture exact PID+creation identity
   with a short bounded retry and atomically finalize the receipt. On pre-proof failure, return
   nonzero and record the failed launch without attached fallback.
4. Add unit tests for validation/receipt exclusivity/flags and a Windows integration smoke where a
   harmless child outlives the launch-CLI process. The fixture removes only that exact child after
   verifying identity.
5. Add concise README/operator usage and amend the harness spec only to distinguish the external
   manager primitive from the read-only watcher. Do not broaden watcher authority.

## Slice 4 — verification and independent audit

1. Run the new focused notification and launcher tests.
2. Run the existing affected manager-notification, active-manager-watch, lane-controller, stable-I/O,
   and lifecycle tests; do not rerun unrelated expensive real-agent/hardware tests.
3. Run the full local harness unit suite once after focused green.
4. Run one board-free practical launch smoke using the new operator utility and a harmless local
   process; prove survival, receipt identity, cooperative/exact cleanup, and no residue.
5. Have the same persistent auditor review the diff, tests, and practical evidence. Fix only
   validated functional gaps; do not chase speculative hardening.

## Successor canary gate

No successor canary starts until:

- the independent repair audit passes;
- the primary and optional watcher owners and every lane controller are launched through the new
  operator utility;
- the manager demonstrates one synthetic exact `MANAGER_REVIEW_DUE` acknowledgement advancing the
  baseline; and
- final synthetic process inventory is empty.

The Clean-M counter remains `0/3`; no retained endpoint is rerun during repair.

## Audit-block resolution slice

Independent implementation audit validated a post-spawn launcher leak and a missing lifecycle
acceptance test. Resolve only those two concrete gaps:

1. Add a focused failing test that wraps the real `Popen`, forces `_creation_identity()` to return
   `None`, captures the exact spawned harmless child, and asserts the launcher returns failure only
   after that child has been terminated and reaped. Also assert the failed receipt reports cleanup
   truthfully.
2. Add a narrow private cleanup helper in `operator_launch.py`. If any failure occurs after spawn
   and before successful receipt finalization, act only through the captured `Popen` handle:
   terminate, wait for a short bounded interval, then kill and wait if needed. Record cleanup
   outcome in the failed receipt. If absence cannot be confirmed, include that in the raised error;
   never claim fail-closed success while the exact child remains live. Do not use name-based or
   broad process termination.
3. Add an actual same-output managed-watch lifecycle regression: first invocation admits the lower
   handoff behind a higher pending event and stops; a distinct second invocation on the same output
   state sees the lane exited and preserves the deferred handoff before exact acknowledgement;
   after exact acknowledgement, a further managed invocation selects/delivers the stored handoff
   using admission-time rank without a new transition. Prove fresh-output suppression remains.
4. Run the two new focused regressions, the 65-test affected command, and the full local harness
   suite once only after focused green. Run the harmless survival/cleanup smoke once. Record exact
   results and process residue in the existing verification document.
5. Return the corrected diff to the same persistent independent auditor. Do not run hardware,
   server, external lane, or retained Clean-M endpoints.
