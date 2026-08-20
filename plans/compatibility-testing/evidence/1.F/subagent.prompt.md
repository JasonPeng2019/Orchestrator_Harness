# Task: Phase 1, Area 1.F — Notification & event taxonomy (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated event/record/snapshot
inputs**. You do NOT launch any `claude`/provider subprocess, you do NOT modify any harness
source module, and you do NOT "fix to green" — a test that reveals a real gap is a valid,
recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_notification_taxonomy -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_manager_notifications_adversarial.py` (fabricates event
    records, drives selection/priority/coalescing; uses `SuiteFixture`, `conditions_from_snapshot`)
  - `orchestrator_harness/tests/support.py` (SuiteFixture, NOW, write_json)
- Code under test: `orchestrator_harness/notifications.py` and `orchestrator_harness/events.py`.
  **Confirmed real symbols (grep to verify signatures/bodies before use — do NOT guess args):**
  - `select_actionable` (notifications.py:1824), `select_actionable_with_deferred` (:1959),
    `preempt_pending_with_higher_priority` (:2028), `coalesce_mutable_handoffs` (:2091).
  - Actionable predicates: `_event_manager_actionable`, `_manager_request_is_actionable`.
  - Lane-notify ineligibility: `_manager_signal_ineligibility_reason` returns
    `"ALREADY_ANSWERED"` / `"INVALID_LANE_ID"` / `"LANE_NOT_LIVE"` (notifications.py:~1592-1631).
  - Dispositions: `EVENT_DISPOSITION_WAKING="WAKING_MANAGER_EVENT"`,
    `EVENT_DISPOSITION_OBSERVED="OBSERVED_STATE"`, `EVENT_DISPOSITION_SUPERSEDED="SUPERSESSION"`;
    map `EVENT_DISPOSITIONS` (notifications.py:140).
  - Record kinds are the string set `{"EVENT","ACK","SUPERSESSION"}` (validated at :663).
  - `_MUTABLE_HANDOFF_TYPES = {"CHECKPOINT_UPDATED","RESULT_AVAILABLE"}` (:37).
  - Actionable events carry field `"notification": "MANAGER_ACTION_REQUIRED"` (:1864, :2007, :2086, :2150).
  - `HARNESS_SCAN_COMMITTED` is a real event kind in the taxonomy list (:115).
  - The **priority defaults table** is a dict literal inside a method (notifications.py:~1047-1063):
    `HARNESS_WATCHER_ALERT:0, RELAY_READY/REQUEST_AMBIGUOUS/RELAY_UNBOUND/REQUEST_EXPIRY_WARNING:1,
    COORDINATION_FAILED/RESOURCE_CONFLICT/OBSERVATION_UNCERTAIN:2, MANAGER_SIGNAL:3,
    CONTROLLER_EXITED/HELPER_EXITED/MCP_EXITED/PROVIDER_WAIT:4, CHECKPOINT_UPDATED/RESULT_AVAILABLE:5`.
    Lower number = higher preemption priority. It is NOT a module-level constant — assert the
    ordering **through observable behavior** (`preempt_pending_with_higher_priority` /
    `select_actionable` selection), not by importing a private dict, unless you find a public accessor.
  - events.py kinds: `COORDINATION_FAILED`, `CODING_RESULT_INVALID`, `RESULT_AVAILABLE`,
    `MANAGER_SIGNAL` (all real).

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_notification_taxonomy.py`

Fabricate event/record/signal inputs (no live lane) and assert the taxonomy/selection logic.
One test method per item:

1. **G1** actionable class membership: `RELAY_READY`, `REQUEST_AMBIGUOUS`, `RELAY_UNBOUND`,
   `REQUEST_EXPIRY_WARNING` are actionable; a non-actionable kind (e.g. `WORKER_OUTPUT`/`LOG`)
   is NOT selected by `select_actionable`.
2. **G2** duplicate controller / coding-branch / coding-worktree conflict → correct conflict
   event kinds emitted (`DUPLICATE_*` / `RESOURCE_CONFLICT` — verify the real kind names first).
3. **G3** invalid result → `CODING_RESULT_INVALID` / `COORDINATION_FAILED` failure events emitted.
4. **G5** process-health events (`STALE_STATUS`, `PROCESS_STATE_UNKNOWN`,
   `PROCESS_INVENTORY_INCOMPLETE`, `OBSERVATION_ERROR`) — drive from the matching fixture; assert
   each emitted. (Verify exact kind spellings in source; record any absent one as a FINDING/BLOCKED.)
5. **G6** `MANAGER_SIGNAL` actionable: fabricate a manager-signal record → surfaced as actionable.
6. **G18** `HARNESS_SCAN_COMMITTED` marker present **exactly once** per scan commit.
7. **G23** `HARNESS_WATCHER_ALERT` top-priority: alert + a lower-priority pending event →
   alert selected first.
8. **G24** numeric preemption ordering (0 alert … 5 RESULT_AVAILABLE): assert
   `preempt_pending_with_higher_priority` respects the table (higher-priority/lower-number wins).
9. **G25** disposition tri-state WAKING/OBSERVED/SUPERSEDED: drive a supersession → transitions.
10. **G26** record kinds EVENT/ACK/SUPERSESSION: construct one of each → classified correctly;
    an out-of-set kind rejected (validation at :663).
11. **G27** lane-notify outcome codes: notify an already-answered / bad-id / dead lane →
    `ALREADY_ANSWERED` / `INVALID_LANE_ID` / `LANE_NOT_LIVE` respectively.
12. **G28** `"notification":"MANAGER_ACTION_REQUIRED"` field convention on actionable events.
13. **G29** deferred + priority preemption (`select_actionable_with_deferred`): higher-priority
    arrival preempts a deferred pending one.
14. **G30** coalescing mutable handoffs (`coalesce_mutable_handoffs`): two mutable handoffs for
    the same target → coalesced to one.
15. **G32** `RESULT_AVAILABLE` terminal event at lowest priority (5): terminal valid result →
    `RESULT_AVAILABLE` emitted, priority 5.

If any taxonomy/selection differs from G1–G32 (wrong membership, missing kind, wrong priority,
wrong outcome code), **do not invent behavior** — write the test to document ACTUAL behavior and
record a FINDING (feature ID, fabricated input, expected vs. observed, `notifications.py:<line>`
or `events.py:<line>`). If a named event kind does not exist at all, record BLOCKED with the reason.

## Pass criterion

- New module green under the run command above.
- Re-run the model suite to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_manager_notifications_adversarial -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.F/`:
- `test-run.log` — full `-v` output of your new module.
- `notif-regression.log` — `-v` output of re-running `test_manager_notifications_adversarial`.

## Final report (return as your last message)

A markdown table: one row per feature ID (G1,G2,G3,G5,G6,G18,G23–G30,G32), each `PASS` /
`FINDING` (one-line what-differed) / `BLOCKED` (why). Then the exact commands run, the test
count, and the pass/fail tally. Do not modify any file outside your new test module and the
evidence dir.
