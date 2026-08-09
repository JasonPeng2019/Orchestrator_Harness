# Logging Additions Spec 2

## Goal

Record exactly how a worker request reaches and wakes the orchestrator, so the next test can tell
whether the manager was notified late, noticed late, or began handling late.

## Scope decision

Keep this change deliberately small. Do not redesign the harness, watcher, manager-state model, or
logging system. Reuse the existing event records wherever they already provide the required fact.

## Required wake chain

Every tested blocking request must produce this ordered chain:

1. **Request created** — existing worker-origin `AGENT_SIGNAL_CREATED` timestamp.
2. **Harness detected it** — existing harness-origin `HARNESS_SIGNAL_OBSERVED` timestamp.
3. **Wake attempted** — the component attempting the wake records the transport and timestamp.
4. **Wake delivered** — that component records delivery only after the transport confirms success.
5. **Manager noticed** — the manager's first action after resuming records receipt of that wake.
6. **Manager began handling** — existing `MANAGER_EVENT_CLAIMED` timestamp.

All six records must carry the same `epoch_id` and `event_id`. Steps 3–5 must additionally carry
one shared `wake_id`. A retry gets a new `wake_id`; it must not overwrite the earlier attempt.

## Minimal new records

Add only the records that are missing today:

### `MANAGER_WAKE_ATTEMPTED`

Written immediately before a component invokes a wake transport.

Required metadata:

- `wake_id`
- `wake_component`
- `wake_transport`
- `manager_session_id`
- `manager_invocation_id`, when one is already known

### `MANAGER_WAKE_DELIVERED`

Written immediately after the transport reports successful delivery. A failed or unknown result
must not be logged as delivered.

Required metadata:

- the same `wake_id`, component, transport, and manager identity as the attempt
- `delivery_succeeded: true`

### `MANAGER_WAKE_FAILED`

Written instead of `MANAGER_WAKE_DELIVERED` when the transport reports failure. This distinguishes
a real transport failure from a missing log record.

Required metadata:

- the same `wake_id`, component, transport, and manager identity as the attempt
- `delivery_succeeded: false`
- a short machine-readable `failure_kind`

Every attempted wake must end in exactly one delivered or failed record. An unknown or interrupted
outcome remains incomplete and therefore insufficient evidence; it must not be guessed into either
result.

### `MANAGER_WAKE_RECEIVED`

Written by the manager as its first logged action after the wake resumes it, before scanning,
claiming, deciding, or responding.

Required metadata:

- the received `wake_id`
- `wake_transport`
- `manager_session_id`
- `manager_invocation_id`

The manager must report the wake ID supplied by the transport. It must not guess the source from
nearby timestamps.

When the manager was inside an existing logged blocking wait, reuse the existing
`MANAGER_WAIT_STARTED`/`MANAGER_WAIT_FINISHED` records. The finish record must carry the matching
`wake_id`, triggering `event_id`, and `wake_transport`. This proves that the specific wait returned
because of the specific wake instead of merely ending nearby in time.

## Timestamp rules

- `source_timestamp_utc` means when that exact action occurred.
- The canonical watcher's observation timestamp remains a separate ingestion timestamp.
- Do not backdate or batch-write wake attempt/delivery records later.
- For one successful wake, ordering must be:

  `request <= detected <= attempted <= delivered <= received <= claimed`

- Equal timestamps are allowed.
- Missing stages, mismatched IDs, or impossible ordering produce `INSUFFICIENT_EVIDENCE`. The
  analyzer must not guess watcher delay, harness delay, busy-manager delay, or idle-manager delay.

### Request-level versus run-level sufficiency

`INSUFFICIENT_EVIDENCE` applies to the affected request chain. It does not automatically invalidate
an entire experiment sprint. A sprint may remain evidence-sufficient when it still contains the
minimum number of other genuine, classifiable requests required by the active experiment spec.

An orchestrator mistake, worker mistake, or later cleanup correction does not erase a complete
six-stage chain. Conversely, successful work elsewhere must not be used to fill or infer a missing
stage. The sprint checkpoint must list excluded requests and the exact reason each was excluded.

## Reviewer isolation for the retest

No watcher, observer, or reviewer subagent may run during a tested sprint. The independent result
reviewer is launched only after the sprint ends, logs drain, and process cleanup is proven. It must
not send a manager notification, acknowledge work, publish a response, or otherwise participate in
the tested wake path. This is an experiment procedure, not a new production subsystem.

## Minimum verification

Add focused tests for:

1. one complete, correctly ordered wake chain;
2. a missing wake stage becoming `INSUFFICIENT_EVIDENCE`;
3. an out-of-order timestamp becoming `INSUFFICIENT_EVIDENCE`;
4. a mismatched or reused `wake_id` being rejected;
5. every attempt having exactly one delivered or failed outcome;
6. a blocking wait finish being linked to its actual wake and event;
7. existing watcher-disabled behavior remaining unchanged.

Then run one host-only readiness test without a watcher-subagent notification. Do not begin the
three-sprint retest until the readiness timeline reconstructs all six stages.

## Explicitly out of scope

Do not add these unless the focused readiness test proves they are necessary:

- a new manager-state or queue-state system;
- broad session-recovery or crash-restart machinery;
- a general retry framework;
- a logging schema rewrite;
- additional polling modes;
- unrelated harness or watcher refactoring.

Existing request, harness-observation, claim, session-boundary, snapshot, and watcher-disabled
logging should be reused rather than replaced.
