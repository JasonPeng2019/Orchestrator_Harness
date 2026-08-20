# M5 managed-consumer smoke report

**Result: PASS (final isolated topology).** Production code was not edited.

## Final run

- Epoch: `m5-managed-consumer-luna-final`
- Harness config: `multi-agent-logs/verification/m5-managed-consumer-luna/harness-config-final.json`
- Harness output: `multi-agent-logs/verification/m5-managed-consumer-luna/fixture-suite-final/multi-agent-logs/harness-output`
- Primary identity: `primary-owner-identity-final.json`
- Diagnostic watcher config/runtime: `harness_watcher/m5-managed-consumer-luna/watcher-config-final.json` / `watcher/`
- Primary wrapper/managed owner/managed watcher: `192228` / `193220` / `182240`
- Exact primary creation identities matched live Windows-CIM identities for all three PIDs.
- Watcher owner/watcher: `193452` / `186952`; service recorded `evaluator_enabled:false`.
- Watcher isolation: `PRIMARY_HARNESS_LOST=0`, `EVALUATOR_OUTCOME=0`, `EVALUATOR_SKIPPED=7`, no evaluator child, and no evaluator sentinel.

## Quiet consumer

Command:

```powershell
python -m orchestrator_harness --config <harness-config-final.json> watch --until-actionable --timeout 0.4 --manager-session-id luna-session-final --manager-invocation-id quiet-final-001
```

Result: exit `3`; JSON event `WATCH_TIMEOUT`; no `wake_id`.

Before/after quiet consumer hashes:

- `pending-notification.json`: unchanged, SHA-256 `117af4bcd268e6ae0bb3f756c1bf4b03071680127b331ae199baaabab2433b5c`
- `managed-watch-runtime.json`: unchanged, SHA-256 `046c09953146c571799f1a15d1ae82b763dc59123300443fe2c245b9cd9ce803`
- `snapshot.json`: changed only through expected managed-owner scan progress (`da34f3bd08992d1b31c3ba079f8f88f879c0d37984701afb42b9aa2254e90ec4` to `f0c3116f092cb309989bd4e53f0604fcdd916a7ea25b7210565e14c1eaca9c49`); attention lines increased `60` to `62` from managed-owner scans, not the consumer.

## Real signal delivery

The live fixture lane was controller PID `177112`/Codex PID `189244`, state `RUNNING_CODEX`. A separate process created:

- Signal ID: `luna-managed-consumer-final-001`
- Harness event ID: `ee0790bfab3b828db08960e13f004a1f909c261dab496c448020b88772a1db13`
- Session/invocation: `luna-session-final` / `wake-final-001`
- Wake ID: `a1e7862a-7f68-415f-9e0c-79a8f75ab214`
- Transport: `blocking_harness_wait_stdout`

The separate blocking consumer returned the exact signal. Attention evidence contains exactly one `MANAGER_WAKE_ATTEMPTED` and one `MANAGER_WAKE_DELIVERED`, both with that wake ID and `delivery_succeeded:true`. All `HARNESS_SCAN_COMMITTED` records use managed watcher PID `182240`; none use the blocking consumer PID `196204`. Notification/scan changes were therefore managed-owner progress plus the required wake attention append.

## Cleanup

The exact durable event was acknowledged using harness event ID `ee0790…`. Watcher and harness were cooperatively stopped; owner files recorded `stop-file` and `managed-harness-exited`, service/runtime recorded `stop-requested`, and the live lane exited with code `0`.

Independent post-cleanup checks: Windows-CIM complete; scoped process count `0`; captured final PIDs `192228,193220,182240,193452,186952,182780,177112,189244,196204,193260` all absent. Temporary stop tokens were removed. Retained runtime/identity/log files are evidence, not live leases.

## Focused tests

```powershell
python -m unittest -q orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_managed_consumer_delivers_later_pending_without_state_mutation orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_managed_runtime_invalid_states_fail_closed orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_managed_consumer_runtime_disappearance_before_delivery_fails_closed orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_managed_consumer_quiet_timeout_has_no_wake orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_live_lane_manager_signal_remains_actionable orchestrator_harness.tests.test_manager_notifications_adversarial.ManagerNotificationAdversarialTests.test_malformed_signal_is_recorded_but_does_not_wake_without_active_state
```

Result: `Ran 6 tests in 0.280s — OK`.

```powershell
python -m unittest -q orchestrator_harness.tests.test_primary_owner_script.PrimaryOwnerScriptContractTests.test_runtime_readiness_requires_live_exact_owner_and_watcher_identities orchestrator_harness.tests.test_primary_owner_script.PrimaryOwnerScriptContractTests.test_validated_managed_identities_are_durably_written_before_supervision harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_primary_identity_terminal_is_logged_once_without_evaluator_work harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_primary_identity_healthy_mismatch_and_incomplete_are_distinct
```

Result: `Ran 4 tests in 0.050s — OK`.

## Limitations / abandoned fixture attempts

Earlier attempts were not counted: one isolated-suite launch lacked `PYTHONPATH`; one watcher launch used an absolute runtime path incompatible with the operator launcher’s service lookup; a 10-second fixture heartbeat expired before a quiet wait; two preliminary signals lacked a live lane/actionability conditions; and a one-second review interval produced an unrelated review-due notification. These were fixture/launcher setup failures. The final run used a fresh suite/output root, a live lane, a 420-second heartbeat, and a 300-second review interval.
