# Clean-M harness repair independent audit

**Verdict: PASS**

No hardware, server, external lane, or retained Clean-M endpoint was run.

## Prior BLOCK resolution

The launcher failure-path defect is fixed. `operator_launch.launch_process()` now invokes
`_cleanup_exact_child()` whenever a child was spawned but launch/identity proof fails. That helper
terminates, waits, escalates to kill only on timeout, and reports whether the captured `Popen`
handle was reaped. The failed receipt records `child_pid`, `cleanup_confirmed`, and any cleanup
error; an unconfirmed cleanup raises a failure that says so.

`test_failed_identity_proof_reaps_exact_spawned_child` forces `_creation_identity()` to fail after
the real child is spawned, then proves the exact captured child has a return code, is absent from
the process inventory, and has a failed receipt with `cleanup_confirmed: true`. This directly
covers the former leak; it is not merely pre-spawn argument validation.

The previously missing lifecycle coverage is also present. The three-invocation
`test_managed_restart_preserves_before_ack_and_delivers_after_ack`:

1. admits the lower-priority handoff while the higher event is pending and stops;
2. restarts from the same output state after the lane exits, before acknowledgement, and verifies
   the same pending event and deferred entry remain; then acknowledges the exact higher event;
3. restarts again against the exited lane and receives the stored `MANAGER_SIGNAL` without a new
   transition.

## Deferred handoff and authority review

- Admission stores the immutable event with admission-time priority, deadline order, identity, and
  timestamp. `select_actionable_with_deferred()` selects deferred entries using only those stored
  facts, never calling `_priority()` or current lane-liveness on them. This fixes the original
  post-exit Delta loss.
- Pruning is limited to acknowledged events and a current condition of the same exact identity
  proving `correlated_request_answered: true`; the exact correlated-supersession test passes.
- Managed watch admits durable handoffs before its pending-event continue, and exact acknowledgement
  preserves the deferred list in `SafeOutput.acknowledge_notification()`.
- Fresh-output historical exited signals remain unadmitted. `MANAGER_SIGNAL` remains distinct from
  transition-only `CHECKPOINT_UPDATED`.
- Search of non-test harness paths found `operator_launch` / `launch_process` only in
  `operator_launch.py`; watcher/CLI/reconcile/notification/lane-controller paths do not import or
  invoke it. The launcher consequently preserves the watcher's read-only boundary.

## Independent command result

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_operator_launch orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **67 passed** in 8.527 seconds.

This includes the launcher survival/receipt identity smoke and exact post-spawn failure cleanup,
the stored-rank post-exit handoff test, same-output three-invocation restart test, fresh-output
suppression, exact correlated supersession, acknowledgement preservation, and affected legacy
notification/managed-watch suites.

## Residue

The audit's prior deliberate child PID `194256` is absent. The focused launcher tests each verify
their own exact child is absent after cleanup. A final targeted process query found no matching
audit/launch-smoke child (apart from the query shell's own command text). No residue was found.

The legacy verification section still records its earlier pre-resolution count, but its appended
block-resolution section reports the superseding 9-focused / 67-affected results. This is a
historical verification narrative detail, not a functional defect.
