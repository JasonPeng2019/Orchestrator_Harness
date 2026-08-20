# Clean-O optional watcher repair verification

## Scope

Changed only the optional watcher implementation and its smoke tests:

- `harness_watcher_implementation/poller.py`
- `harness_watcher_implementation/evaluator.py`
- `harness_watcher_implementation/tests/test_watcher_smoke.py`
- `.agent-workspace/CANARY_CLEAN_O_WATCHER_REPAIR_VERIFICATION.md`

No primary `orchestrator_harness`, firmware, BYO-Firmware-MCP, catalog, active epoch, or historical
Clean-O alert/evidence/runtime file was edited. No real evaluator, live endpoint, board, or hardware
operation was run.

## Test-first reproduction

Before the implementation, the new focused command was run:

```powershell
python -m unittest harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_same_delta_stale_then_exact_recovery_is_hidden_from_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_stale_in_one_poll_then_exact_exit_in_next_poll_never_calls_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_sustained_stale_reloads_cursor_then_releases_once_with_valid_evidence harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_unrelated_identity_or_clear_does_not_suppress_stale_release harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_legacy_v2_cursor_without_quarantine_state_remains_readable -v
```

Result before repair: **2 failures, 3 errors**. The old watcher evaluated a first stale transition,
left recovery work visible, and had no durable quarantine state. This locked the cross-poll defect.

## Focused verification

```powershell
python -m unittest harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_same_delta_stale_then_exact_recovery_is_hidden_from_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_stale_in_one_poll_then_exact_exit_in_next_poll_never_calls_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_sustained_stale_reloads_cursor_then_releases_once_with_valid_evidence harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_unrelated_identity_or_clear_does_not_suppress_stale_release harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_legacy_v2_cursor_without_quarantine_state_remains_readable -v
```

Result: **5 passed**.

Coverage: same-delta exact recovery is hidden; the actual Clean-O-shaped cross-poll
`STALE_STATUS` -> exact `CONTROLLER_EXITED` causes no evaluator call; durable cursor reload
releases sustained stale once after a full poll interval with a valid evidence tuple and one alert;
unrelated identity/non-stale clear cannot suppress it; a legacy v2 cursor without the additive state
remains readable.

## Affected optional-watcher smoke suite

```powershell
python -m unittest harness_watcher_implementation.tests.test_watcher_smoke -v
```

Result: **31 passed**.

This suite retains the cursor-offset, watcher recursive-input filtering, strict evidence validation,
no-progress, alert deduplication, and evaluator-prompt checks. The packet constraint and Terra
instructions now state that only a stale identity surviving the complete quarantine interval is
eligible for `manager_failure`; no blanket stale ignore rule was added.

## Self-review and residue

Reviewed the final code path for exact identity matching, `CONTROLLER_ACTIVE`/
`CONTROLLER_EXITED`/matching `CONDITION_CLEARED` recovery, one-time maturity, retained original
source path/SHA-256/offset, and additive v2 cursor compatibility. Raw source logs and cursor offsets
are only advanced by the existing source reader; quarantined records are not rewritten.

```powershell
$repo=[regex]::Escape((Get-Location).Path); Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match $repo -and ($_.CommandLine -match 'harness_watcher_implementation|test_watcher_smoke') }
```

Result: **no matching watcher/test processes**.
