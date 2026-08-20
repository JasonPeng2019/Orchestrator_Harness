# Clean-M Harness Repair — Verification

Date: 2026-07-31

## Required failing baseline

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs -v
```

Before implementation, result: **failed** at import with `ImportError: cannot import name
'admit_deferred_handoffs' from orchestrator_harness.notifications`. This was the expected red
baseline for the new durable-admission contract.

## Focused durable-handoff and launcher tests

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_operator_launch -v
```

Result: **6 passed**. Coverage includes admission-time rank persistence after lane exit, exact
correlated-signal supersession, fresh-output exited-history suppression, exact acknowledgement
preserving same-output deferred state, managed-watch deferred delivery after the higher event is
acknowledged, receipt exclusivity/validation, and detached launch receipt identity.

## Affected harness suites

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_operator_launch orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **65 passed**.

## Full local harness suite

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Result: **165 passed, 1 skipped**.

## Windows detached-survival / exact-cleanup smoke

```powershell
python -m unittest orchestrator_harness.tests.test_operator_launch.OperatorLaunchTests.test_child_survives_launch_cli_and_receipt_has_identity -v
```

Result: **1 passed**. The smoke launched a harmless Python sleep child through the standalone CLI,
verified it remained live after the launcher exited, matched its receipt PID and provider creation
time before cleanup, then removed only that exact child and verified no matching PID remained.

No hardware, firmware-MCP/server action, external agent, experiment evidence/status, or retained
Clean-M endpoint was run. The standalone launcher is not imported by watcher code paths.

## Independent-audit block resolution

### Required red baseline

```powershell
python -m unittest orchestrator_harness.tests.test_operator_launch.OperatorLaunchTests.test_failed_identity_proof_reaps_exact_spawned_child -v
```

Before the correction, result: **failed** because the captured post-spawn child still had
`returncode: None`; Windows temporary-directory cleanup also reported the child still held its
working directory. The exact audit-test child PID was then terminated and verified absent before
continuing.

### Focused block-resolution regressions

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_operator_launch -v
```

Result: **9 passed**. The new launcher regression forces `_creation_identity()` to fail after the
real `Popen` returns, then proves that exact captured child has been terminated and reaped and the
failed receipt records `cleanup_confirmed: true`. The new lifecycle regression uses three distinct
same-output `watch_managed()` invocations: admit/stop with high pending, restart after lane exit
before acknowledgement while retaining the deferred handoff, exact-ack the high event, then restart
and deliver the stored handoff without a new transition.

### Affected suites after resolution

```powershell
python -m unittest orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_operator_launch orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **67 passed**.

### Full local harness suite after resolution

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Result: **167 passed, 1 skipped**.

### Final detached-survival smoke and residue check

```powershell
python -m unittest orchestrator_harness.tests.test_operator_launch.OperatorLaunchTests.test_child_survives_launch_cli_and_receipt_has_identity -v
```

Result: **1 passed**. The exact-child residue query returned: `No launch-smoke child residue.`

No hardware, server, external lane, or retained Clean-M endpoint was run during block resolution.
