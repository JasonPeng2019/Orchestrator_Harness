# Phase 3 Wake Logging - Code Implementation Plan

## Objective

Implement the six-stage wake chain in `active-working-spec/phase-3-wake-logging.md` and
`logging_additions_spec_2.md` with the smallest changes to the existing harness attention-log
pipeline.

This plan is authored and owned by the root orchestrator. The Terra coder implements it; the Terra
reviewer only provides feedback. The reviewer never blocks, and the root decides whether each
finding warrants a change.

## Current code path

The existing production-relevant path is:

1. A worker writes a manager signal containing its durable `signal_id`.
2. `orchestrator_harness.cli.watch_until_actionable()` observes and selects it.
3. `SafeOutput.append_attention()` writes harness-owned attention records to
   `<harness-output>/attention-events.jsonl`.
4. The blocking harness command writes the selected event to stdout and returns.
5. The root manager records its own attention events through
   `python -m harness_watcher_implementation ... record-attention`.
6. `harness_watcher_implementation.attention.ingest_attention()` canonicalizes the harness and
   producer logs.
7. `analyze_event()` classifies the resulting timeline.

Existing records already cover request creation, harness observation, waits, claims, decisions,
responses, and worker resume. The missing production facts are the harness's exact wake attempt
and transport outcome, the wake ID returned to the manager, the manager's exact receipt, and
strict analyzer correlation across those facts.

## Accepted implementation decisions

### Production wake transport

For this phase, the tested wake component and transport are:

- `wake_component`: `orchestrator_harness.watch_until_actionable`
- `wake_transport`: `blocking_harness_wait_stdout`

“Delivered” means the harness successfully wrote and flushed the selected wake-bearing event to
the blocking command's stdout. It does **not** mean the manager noticed it; that separate fact is
`MANAGER_WAKE_RECEIVED`.

### Wake identity

Generate one UUIDv4 `wake_id` for each actual stdout delivery attempt. A redelivery of an existing
pending notification is a new attempt and therefore receives a new `wake_id`. Never derive it from
timestamps or reuse an event ID.

### Manager identity

When attention logging is enabled, `watch --until-actionable` must receive:

- `--manager-session-id`
- `--manager-invocation-id`

These values are copied into the attempt and outcome records. Existing non-attention uses remain
compatible: when attention logging is disabled, these arguments are not required and no wake
records are emitted.

### Manager receipt

The harness cannot truthfully write `MANAGER_WAKE_RECEIVED` because it cannot know when the root
manager resumed. Immediately after the blocking command returns, the root records
`MANAGER_WAKE_RECEIVED` through the existing orchestrator `record-attention` producer path, using
the `wake_id` and `wake_transport` returned in stdout. That must be the root's first logged action
before scan, claim, decision, or response.

The root then records `MANAGER_WAIT_FINISHED` with the same event, wake ID, transport,
session/invocation, and the activity ID from its preceding `MANAGER_WAIT_STARTED` record. No new
manager-state subsystem or second recorder is needed.

### Explicit transport failure

If stdout write/flush fails after a durable attempt record, write `MANAGER_WAKE_FAILED` with:

- the same correlation and manager fields;
- `delivery_succeeded: false`; and
- a bounded machine-readable `failure_kind` based on the exception type.

Then propagate the original error. Never emit `MANAGER_WAKE_DELIVERED` for that attempt.

If stdout succeeds but durable delivery logging itself fails, do not fabricate a failed transport:
the timeline remains incomplete and analyzes as `INSUFFICIENT_EVIDENCE`.

### Analyzer result for a failed transport

Do not add a broad new top-level classification. Add a bounded `wake_evidence` result describing
`COMPLETE`, `FAILED`, `INSUFFICIENT_EVIDENCE`, or `NOT_APPLICABLE`.

For a blocking request with an explicit failed transport:

- `wake_evidence.status` is `FAILED` with its `failure_kind`; and
- the existing overall classification is `HARNESS_DELIVERY_DELAY`.

A missing or contradictory stage instead produces `INSUFFICIENT_EVIDENCE`.

### Historical watcher relay

Keep `WATCHER_NOTIFICATION_SENT` valid so historical evidence remains readable, but stop using it
as proof of production-manager availability for a blocking wake analysis. A blocking request must
have the new production wake chain. Formal scheduled reviews and explicitly nonblocking events do
not require a wake chain.

## Implementation slices

### Slice 1 - Extend the attention record contract

Files:

- `harness_watcher_implementation/attention.py`
- `harness_watcher_implementation/tests/test_attention.py`
- `harness_watcher_implementation/tests/test_attention_ingestion.py` when provenance coverage is
  best placed there

Changes:

1. Add these kinds to `KINDS`:
   - `MANAGER_WAKE_ATTEMPTED`
   - `MANAGER_WAKE_DELIVERED`
   - `MANAGER_WAKE_FAILED`
   - `MANAGER_WAKE_RECEIVED`
2. Permit harness provenance only for attempt/delivered/failed, and orchestrator provenance only
   for received. Preserve existing producer-role restrictions for all other records.
3. Validate required fields:
   - Attempt: `wake_id`, `wake_component`, `wake_transport`, manager session/invocation.
   - Delivered: same identity fields and `delivery_succeeded: true`.
   - Failed: same identity fields, `delivery_succeeded: false`, and nonempty
     `failure_kind`.
   - Received: `wake_id`, `wake_transport`, manager session/invocation.
4. Validate every `wake_id` as UUIDv4.
5. When `MANAGER_WAIT_FINISHED` carries a wake, require its `wake_id` and `wake_transport`; its
   top-level `event_id` is the triggering event correlation.
6. Require orchestrator provenance for wake-bearing `MANAGER_WAIT_FINISHED` records.

Slice test gate:

- valid records for all four kinds;
- missing/invalid fields rejected;
- wrong producer provenance rejected;
- failed and delivered outcome shapes cannot be confused; and
- watcher-disabled recorder behavior remains unchanged.

### Slice 2 - Emit wake attempts and outcomes from the blocking harness wait

Files:

- `orchestrator_harness/cli.py`
- `orchestrator_harness/tests/test_manager_notifications.py`
- `orchestrator_harness/tests/test_manager_notifications_adversarial.py`
- `orchestrator_harness/tests/test_active_manager_watch_smoke.py` only where its direct calls need
  explicit manager identity

Changes:

1. Add a small private helper in `cli.py` responsible only for one stdout wake attempt:
   - generate UUIDv4 `wake_id`;
   - append `MANAGER_WAKE_ATTEMPTED` before touching stdout;
   - write and flush a copy of the selected event containing `wake_id`, `wake_transport`, and
     `wake_component`;
   - append exactly one `MANAGER_WAKE_DELIVERED` after successful flush; or
   - append exactly one `MANAGER_WAKE_FAILED` when write/flush raises, then re-raise.
2. Use that helper for both:
   - a newly selected actionable event; and
   - redelivery of an already pending event.
3. Do not create wake records for `WATCH_TIMEOUT`.
4. Extend `watch_until_actionable()` with optional manager session/invocation parameters.
5. Extend the `watch --until-actionable` parser with the two manager identity arguments.
6. When `config.attention_logging_enabled` is true, reject a production blocking wait missing
   either identity before entering the loop. When logging is disabled, retain the existing call
   contract and output.
7. Do not put `wake_id` into the durable pending notification itself. Each redelivery is a distinct
   transport attempt and receives a fresh ID; the returned stdout copy carries the attempt ID.

Slice test gate:

- attempt precedes one successful delivered record;
- stdout includes the same wake ID/component/transport;
- pending redelivery gets a different wake ID;
- simulated stdout failure produces attempted + failed and no delivered;
- timeout produces no wake stages or wake ID;
- missing manager identity fails before waiting only when attention logging is enabled; and
- existing disabled/non-attention behavior remains compatible.

### Slice 3 - Build and enforce the six-stage analyzer chain

Files:

- `harness_watcher_implementation/attention.py`
- `harness_watcher_implementation/tests/test_attention.py`

Changes:

1. Add one pure helper that groups attempt/outcome/receipt/wait-finish records by `wake_id` and
   returns the bounded `wake_evidence` object.
2. Validate all attempts, not only the final successful one:
   - every attempt has exactly one outcome;
   - outcome component/transport/manager identity matches the attempt;
   - no wake ID is reused for a second attempt;
   - failed attempts have no receipt;
   - the selected successful attempt has exactly one receipt and one matching wake-bearing wait
     finish;
   - receipt and claim use the same manager session/invocation;
   - no manager action for that invocation falls between delivery and receipt; and
   - source-action timestamps satisfy
     `created <= observed <= attempted <= delivered <= received <= claimed`.
3. Use `source_timestamp_utc` for action ordering. Keep canonical
   `observed_timestamp_utc` separate for ingestion metrics and integrity checks.
4. Treat missing stages, duplicates, mismatches, or impossible ordering as
   `wake_evidence.status: INSUFFICIENT_EVIDENCE` and force the overall classification to
   `INSUFFICIENT_EVIDENCE`.
5. Treat a complete failed attempt as `wake_evidence.status: FAILED` and
   `HARNESS_DELIVERY_DELAY`.
6. For a complete successful chain:
   - use delivered time for transport/delivery metrics;
   - use received time as proven manager availability;
   - calculate attempted-to-delivered, delivered-to-received, and received-to-claim durations;
   - stop using `WATCHER_NOTIFICATION_SENT` as availability evidence.
7. Update idle-wait attribution to require the matching production `wake_id` and transport rather
   than `collaboration.send_message`.
8. Leave formal-review and nonblocking analysis behavior unchanged.

Slice test gate:

- complete ordered chain accepted;
- each individual missing stage is insufficient;
- duplicate or absent attempt outcomes are insufficient;
- reused/mismatched wake IDs are insufficient;
- out-of-order source timestamps are insufficient even if ingestion order looks valid;
- one failed attempt followed by a distinct successful retry is accepted when both attempts have
  exactly one outcome;
- a failed attempt without a retry identifies harness delivery failure;
- manager action before receipt is insufficient;
- receipt-to-claim delay is distinguishable from delivery-to-receipt delay; and
- legacy watcher relay alone cannot prove a production blocking wake.

### Slice 4 - Document the manager-side receipt procedure

Files:

- `harness_watcher_implementation/ATTENTION_LOGGING.md`
- `orchestrator_harness/README.md`
- `.codex/skills/run-firmware-test-suite/SKILL.md` only where the active blocking-wait procedure is
  defined

Changes:

1. Replace the watcher-subagent notification procedure as the normal path with the exact blocking
   harness wait invocation, including manager session/invocation arguments.
2. Document that the first manager logging action after return is `MANAGER_WAKE_RECEIVED` using
   the returned wake fields.
3. Document the matching `MANAGER_WAIT_FINISHED` and existing `MANAGER_EVENT_CLAIMED` records.
4. Keep the watcher-subagent relay documented as historical/fallback behavior, not production wake
   proof.
5. State that no wake records are fabricated for quiet timeouts.

Documentation must use parameterized example paths under `multi-agent-logs/` and
`harness_watcher/<epoch>/`; do not reintroduce `.agent-workspace` logging paths.

### Slice 5 - Focused practical smoke

Files:

- Prefer extending `harness_watcher_implementation/tests/run_attention_practical.py`.
- Add a new smoke file only if the existing practical runner cannot express the production wait
  without becoming confusing.

The smoke must be host-only and exercise:

1. a synthetic external manager signal;
2. harness observation;
3. a real `watch --until-actionable` blocking process with manager identity arguments;
4. returned wake fields;
5. manager receipt, wait finish, and claim records through the real recorder path;
6. canonical ingestion; and
7. a complete analyzer result with all wake metrics.

Also run a quiet timeout and prove it contains no wake ID or wake stages. No internal collaboration
message, watcher subagent, firmware action, provider action, or hardware action is allowed.

## Coder/reviewer execution loop

1. Launch one persistent GPT-5.6-terra medium coder with this plan.
2. Have it implement one vertical slice and run that slice's focused tests.
3. Launch an independent GPT-5.6-terra medium reviewer after the implementation.
4. The reviewer returns numbered code/test findings and does not edit.
5. The root audits every finding:
   - accept verified code-breaking, evidence-breaking, or clearly worthwhile simple fixes;
   - reject unsupported, stylistic, speculative, out-of-scope, or disproportionate changes.
6. The root writes each accepted fix precisely and resumes the same coder.
7. Repeat until the root decides all objective requirements pass and no root-accepted finding
   remains.
8. Then use the Luna smoke-test subagent. Smoke failures return to the root, which decides whether
   to send a focused fix to the coder.

The reviewer never blocks and never decides when to advance. The root's evidence-backed decision
is final.

## Verification commands

The coder may use narrower commands during slices. Before Phase 3 completion, run at minimum:

```powershell
python -m unittest harness_watcher_implementation.tests.test_attention -v
python -m unittest harness_watcher_implementation.tests.test_attention_ingestion -v
python -m unittest harness_watcher_implementation.tests.test_attention_recorder_cli -v
python -m unittest orchestrator_harness.tests.test_manager_notifications -v
python -m unittest orchestrator_harness.tests.test_manager_notifications_adversarial -v
python -m unittest orchestrator_harness.tests.test_active_manager_watch_smoke -v
python -m unittest discover -s orchestrator_harness/tests -t . -q
python -m unittest discover -s harness_watcher_implementation/tests -t . -q
python -m compileall -q orchestrator_harness harness_watcher_implementation harness_common scripts/orchestration
```

Run Ruff and Pyright over changed Python files. Report existing unrelated failures honestly; do not
perform a mass style/type cleanup.

## Stop and report conditions

Return to the root before broadening the plan if implementation proves any of these assumptions
false:

- stdout flush is not the actual blocking-wait transport boundary;
- the manager cannot receive the returned wake ID before another logged action;
- existing attention ingestion cannot preserve distinct source and observation timestamps;
- an unavoidable change would require a new queue/manager-state/retry system; or
- the change would break watcher-disabled no-op behavior.

Do not guess around these contradictions. The root revises the plan if necessary.
