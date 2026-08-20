# Task: Phase 1, Area 1.J — Host adapter records, non-delivery (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated adapter/router/pending
inputs**. You do NOT launch any `claude`/provider subprocess, you do NOT modify any harness
source module, and you do NOT "fix to green" — a test that reveals a real gap is a valid,
recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_host_adapters -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_s4_contract.py` — **your primary model** for building a live
    `DeliveryCoordinator`: it has a `_router(root, session=...)` helper returning a
    `ManagerEventRouter`, `create_codex_adapter(router, transport=SyntheticCodexTransport())`,
    an `_event(id)` builder, `router.admit(event)`, and calls `coordinator.acknowledge_event(id)`.
    Note line ~615: `acknowledge_event(receipt)` with a `DeliveryReceipt` is **rejected** — copy
    that idiom for the N4 guardrail. Also `select_host_adapter("codex"|"future-host", router)`.
  - `orchestrator_harness/tests/test_s4_repair.py` — more coordinator lifecycle idioms.
  - `orchestrator_harness/tests/support.py`.

## Code under test — `orchestrator_harness/host_adapters.py` (grep bodies before asserting)

- `ManagerEventAck` (:404): frozen dataclass, `event_id` + `action="ACKNOWLEDGED"`;
  `__post_init__` raises `HostAdapterError("manager event action must be ACKNOWLEDGED")` for any
  other action; `as_record()` → `{"schema": MANAGER_EVENT_ACK_SCHEMA, "event_id", "action"}`.
- `DeliveryCoordinator.acknowledge_event(event_id, *, action="ACKNOWLEDGED")` (:1161) — the ONLY
  legitimate manager path that mints a `ManagerEventAck`. Guardrails: passing a `DeliveryReceipt`
  as `event_id` → `HostAdapterError("a delivery receipt is not a manager event acknowledgement")`;
  acking an `EXTERNALLY_BLOCKED` item → `HostAdapterError("EXTERNALLY_BLOCKED notification items
  cannot be acknowledged by the worker")`.
- `NotificationStopDecision` (:424): `permitted`(bool) / `reason` / `open_count` /
  `externally_blocked_count` / `declarations`(tuple). `__post_init__` enforces: `permitted` bool,
  non-empty `reason`, non-negative counts, and each declaration is a dict whose keys are EXACTLY
  `{"notification_id","required_actor","required_action"}` else
  `HostAdapterError("stop decision declarations have an invalid closed shape")`. `as_record()`
  omits `declarations` when empty.
- `DeliveryCoordinator.notification_stop_request()` (:1332) — produces the decision via the stop
  matrix: any OPEN item → `permitted=False` (`NOTIFICATION_STOP_OPEN_ITEMS_REMAIN`); empty active
  queue → `permitted=True` (`NOTIFICATION_STOP_QUEUE_EMPTY`); all `EXTERNALLY_BLOCKED` → permitted
  only after `record_notification_final_response(...)` named every active blocked ID with its
  exact `required_actor`/`required_action` (`NOTIFICATION_STOP_EXTERNAL_DECLARED`), else
  `permitted=False` (`NOTIFICATION_STOP_EXTERNAL_RESPONSE_REQUIRED`). Related methods:
  `mark_externally_blocked(...)` (grep it near :1300-1330) and `record_notification_final_response`
  (:1392). Import the `NOTIFICATION_STOP_*` reason constants; don't hard-code the strings.
- `_severity_for(record)` (:537): if `record["facts"]["severity"]` is a non-empty str → rank
  `{critical:0,error:1,warning:2,info:3}` (unknown → 4), returns `(rank, value.lower())`; else
  falls back to numeric `record["priority"]`: `<=1 → (1,"error")`, `<=3 → (2,"warning")`,
  else `(3,"info")`; non-numeric priority defaults to `3.0`.
- `_highest_pending(pending)` (:557): empty list → `DeliveryBindingError("cannot summarize an
  empty manager queue")`; else sorts by `(priority, severity_rank, admission_seq, event_type)` and
  returns `(event_type, severity_str)` of the first (highest-priority) item.

## What to build

Create ONE new test module: `orchestrator_harness/tests/test_compat_host_adapters.py`

One test per item:

1. **N4** `ManagerEventAck` is minted only by the manager acknowledge path. Build a live
   `DeliveryCoordinator` (the `test_s4_contract` idiom), `router.admit` an event, call
   `coordinator.acknowledge_event(event_id)` → assert a valid `ManagerEventAck`
   (`as_record()["schema"] == MANAGER_EVENT_ACK_SCHEMA`, `action == "ACKNOWLEDGED"`). Then assert
   the guardrails: `acknowledge_event(<a DeliveryReceipt>)` raises; acking an EXTERNALLY_BLOCKED
   item raises; and constructing `ManagerEventAck(event_id, action="DENIED")` directly raises
   `HostAdapterError` (a fabricated non-ACK typed object is impossible — the type itself refuses).
2. **N5** `NotificationStopDecision` shape + stop matrix. Assert the three decision shapes via
   `notification_stop_request()`: (a) an OPEN item → `permitted=False`, correct reason/counts;
   (b) empty queue → `permitted=True`; (c) all-EXTERNALLY_BLOCKED before vs. after
   `record_notification_final_response(...)` → `permitted` flips False→True with the closed
   `declarations` tuple present only on the accepted path. Also assert the dataclass rejects an
   invalid declaration shape directly (a declaration dict with a wrong/extra key).
3. **N7** `_severity_for` / `_highest_pending`. Feed a **mixed-severity** pending set (facts-based
   severities: critical/error/warning/info + unknown; plus a priority-only fallback item) and
   assert `_severity_for` returns the documented `(rank, label)` for each, and `_highest_pending`
   selects the correct `(event_type, severity)` under the full sort key (exercise a priority tie
   broken by severity, and a further tie broken by `admission_seq`). Assert the empty-queue
   `DeliveryBindingError`.

If any behavior differs from N4/N5/N7 as described (a fabricated ack is accepted; the stop matrix
permits a stop with an OPEN item; severity/highest-pending mis-ranks — a fail-open / safety-
relevant difference is HIGHER severity, flag it clearly), **do not invent behavior** — document
ACTUAL behavior in a green test and record a FINDING (feature ID, input, expected vs. observed,
`host_adapters.py:<line>`). Never edit source.

## Pass criterion

- New module green under the run command above.
- Re-run the model suites to confirm shared coordinator fixtures/state are undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s4_contract orchestrator_harness.tests.test_s4_repair -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.J/`:
- `test-run.log` — full `-v` output of your new module.
- `host-regression.log` — `-v` output of re-running the two model suites.

## Final report (return as your last message)

A markdown table: one row per feature ID (N4, N5, N7), each `PASS` / `FINDING` (one-line
what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and the pass/fail
tally. Do not modify any file outside your new test module and the evidence dir.
