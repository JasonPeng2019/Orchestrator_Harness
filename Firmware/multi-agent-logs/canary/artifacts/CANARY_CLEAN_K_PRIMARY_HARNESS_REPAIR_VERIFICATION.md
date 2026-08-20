# Clean-K Primary Harness Repair — Verification

Date: 2026-07-31

## Focused modules

```powershell
python -m unittest orchestrator_harness.tests.test_reconcile orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **128 passed**.

## Full primary discovery

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Result: **155 passed, 1 skipped**.

## Clean-K retained-data no-write check

```powershell
python -m orchestrator_harness --config orchestrator_harness/canary-20260731-s1-clean-k.json scan --no-write
```

Result: exit 0. A separate in-memory condition projection of the same Clean-K configuration reported 189 retained conditions and selected `null`. It retained 20 exact expired relay records (`BOUND_EXPIRED`); every one had `manager_actionable: false`.

No hardware action, external-agent launch, or state write was performed by this verification.

## Focused audit correction (current unknown request actionability)

```powershell
python -m unittest orchestrator_harness.tests.test_reconcile orchestrator_harness.tests.test_manager_notifications -v
```

Result: **94 passed**.

The added controls exercise missing and partial creation evidence through reconciliation and notification selection: unresolved `UNKNOWN` requests are selected before their deadline and retained but not selected after it. Explicit reconciled `manager_actionable` true/false event controls cover the same notification boundary.

## Full discovery after audit correction

```powershell
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Result: **158 passed, 1 skipped**.

No hardware action, external-agent launch, Clean-K retained-data scan, or other expensive retained check was rerun for this narrow code-only correction.

## Main-agent acceptance check

```powershell
python -m unittest orchestrator_harness.tests.test_reconcile.ReconcileTests.test_missing_creation_unknown_request_is_actionable_only_before_deadline orchestrator_harness.tests.test_reconcile.ReconcileTests.test_partial_creation_unknown_request_is_actionable_only_before_deadline orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_unknown_request_event_uses_reconciled_actionability_boundary -v
```

Result: **3 passed**. This manager-owned check independently exercised both reconcile boundaries and
the notification authority bit without rerunning hardware, agents, or unrelated expensive tests.
