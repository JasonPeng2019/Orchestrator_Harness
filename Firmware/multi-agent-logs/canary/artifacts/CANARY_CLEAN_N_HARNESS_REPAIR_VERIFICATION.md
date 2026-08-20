# Clean-N Harness Repair Verification

## Focused regression command

```powershell
python -m unittest orchestrator_harness.tests.test_clean_n orchestrator_harness.tests.test_clean_m_handoffs -v
```

Result: **9 passed**. Covers discovery -> process -> post-sample clock ordering, newest mutable
checkpoint coalescing/pending supersession metadata, immutable manager-signal separation, and the
same-output managed handoff lifecycle.

## Affected suites

```powershell
python -m unittest orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_clean_n -v
```

Result: **67 passed**.

## Full local harness suite

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Result: **170 passed, 1 skipped**.

## Board-free same-output lifecycle evidence

`CleanMHandoffTests.test_managed_restart_preserves_before_ack_and_delivers_after_ack` is run in
the focused and affected commands. It uses distinct managed-watch invocations over one output
state, preserves deferred work through stop/restart, then exact-acknowledges and delivers the
stored event. It creates only temporary fixture processes/state and leaves no process residue.

No hardware, firmware, server, provider/MCP public operation, external lane, or Clean-N endpoint
was run.

## Acceptance-gap closure

```powershell
python -m unittest orchestrator_harness.tests.test_clean_n -v
```

Result: **5 passed**. The deterministic slow-sample test uses a status/process identity beginning
between nominal scan start and the completed inventory, then proves `observe()` and an actual
bounded `watch_managed()` iteration classify it `RUNNING_CODEX`, not `STALE_STATUS`. Existing
reconcile stale/absent controls remain in the affected suite.

```powershell
python -m unittest orchestrator_harness.tests.test_clean_n orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **69 passed**. Added admission-path checkpoint versions coalesce through pending-plus-
deferred replacement, with old ID distinct from the current replacement; same-output restart
coverage remains exercised by the managed-handoff lifecycle test.

The production code was unchanged after the prior full-suite run; per bounded instruction the
full suite was not rerun solely for these focused test additions. No hardware, server, or external
lane was run.

## Audit-block resolution: promoted mutable admission order

Focused:
```powershell
python -m unittest orchestrator_harness.tests.test_clean_n -v
```
Result: **6 passed**.

Affected:
```powershell
python -m unittest orchestrator_harness.tests.test_clean_n orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```
Result: **70 passed**.

Final full suite:
```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```
Result: **173 passed, 1 skipped**.

The new promotion regression proves a deferred old checkpoint retains its original `admitted_utc`
when selected later, so a newer admission replaces it and carries transitive supersession metadata.
No hardware, server, or external lane was run.

## Final same-output canonical-ack lifecycle

Focused:
```powershell
python -m unittest orchestrator_harness.tests.test_clean_n -v
```
Result: **7 passed**.

Affected:
```powershell
python -m unittest orchestrator_harness.tests.test_clean_n orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```
Result: **71 passed**.

`CleanNTests.test_managed_checkpoint_promotion_restart_and_exact_ack` drives distinct bounded
managed-watch invocations against one durable output state: an old deferred checkpoint promotes,
a newer checkpoint replaces it, canonical acknowledgement rejects the superseded old ID, accepts
the current ID, and a later same-output restart produces no obsolete pending wake. Production code
was unchanged for this test-only acceptance closure, so the full-suite result above remains the
latest (**173 passed, 1 skipped**) and was not rerun. No hardware, server, or external lane was run.
