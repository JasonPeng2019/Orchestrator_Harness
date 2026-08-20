# M5 delivery-deadline repair -- Luna host-only smoke

Date: 2026-08-02. This was an uncounted host-only smoke; no production or watcher files were modified.

## Commands

1. Required-context read: `AGENTS.md`, `REPOSITORY_LAYOUT.md`, `active-working-spec/m5-harness-deadline-repair.md`, and `multi-agent-logs/attention-validation/runs/20260802-m5-s3-101953Z/SPRINT_CHECKPOINT.md`.
2. Ephemeral stdin smoke: `@' ... '@ | python -`. The body used the existing `SuiteFixture`, created one live lane and one terminal-JSONL routine lane, started native `orchestrator_harness.cli.watch_managed`, injected a blocked `HELP` signal with `delivery_deadline_utc`, paused after native pending admission, then called native `watch_until_actionable` with attention logging enabled. It read the returned event and `attention-events.jsonl`, then called `observe`/`select_actionable` and stopped the disposable managed state.
3. Controls:

   `python -m unittest -v orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_delivery_metadata_is_validated_and_propagated orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_blocked_help_delivery_deadline_precedes_stale_status orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_non_blocking_help_with_delivery_deadline_does_not_outrank_stale_status orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_attention_enabled_wake_attempts_are_correlated_and_fail_honestly orchestrator_harness.tests.test_manager_notifications.ManagerNotificationTests.test_delivery_deadline_is_response_by_time_in_pending_snapshot`

## Result

`PASS` -- native managed selection and native blocking delivery returned `MANAGER_SIGNAL` / `blocked-help` before the competing routine `STALE_STATUS` lane.

- Returned `delivery_deadline_utc`: `2026-07-30T12:01:00Z`
- Returned `agent_blocked`: `true`
- Returned `attention_epoch_id`: `m5-luna-smoke`
- Wake transport: `blocking_harness_wait_stdout`
- Wake component: `orchestrator_harness.watch_until_actionable`
- Competing stale lane: `m5-luna-smoke:Routine:S00`
- Pending snapshot response-by: `2026-07-30T12:01:00Z`
- Attention stages for `blocked-help`: `HARNESS_SIGNAL_OBSERVED`, `HARNESS_EVENT_DEFERRED`, `HARNESS_EVENT_ACTIONABLE`, `HARNESS_EVENT_PENDING`, `MANAGER_WAKE_ATTEMPTED`, `MANAGER_WAKE_DELIVERED`
- Every captured attention stage retained `delivery_deadline_utc = 2026-07-30T12:01:00Z`.

Controls: `5/5 OK`. The nonblocking HELP control correctly did not outrank `STALE_STATUS`; metadata propagation, pending rendering, and wake correlation also passed.

## Fidelity and audit

No hardware, provider, MCP, deploy, flash, commit, or push action occurred. The smoke used only the disposable `SuiteFixture` and native harness entry points; no runner, wrapper, relay, scheduler, retry controller, or watcher assistance was added. Disposable evidence was read before fixture cleanup.

SHA-256 hashes were unchanged before/after:

```text
orchestrator_harness/cli.py          1D8CA496B229E73AD20B7AAEE6819116D2DC4D400985540949BBDF11742FC9D0
orchestrator_harness/notifications.py D575E8FA924F5F493E0C38794DB67CD77BFE196BDB947D5C64398E1D53D84D35
orchestrator_harness/reconcile.py   3081EEAFFD1328A8B78A2C326000FBCB1822FD82E91B6675F9B3E10D6EB93
orchestrator_harness/discovery.py   A5F088F9A4C169D32CB2E085B7D490B4EEE1637822C8A1A6F0735856D44CD6A0
```

Two earlier ephemeral attempts failed only on smoke-driver evidence timing: the first inspected a later overwritten snapshot, and the second never released its pause gate. Both were discarded setup observations; neither indicated a harness failure. The corrected smoke above passed.
