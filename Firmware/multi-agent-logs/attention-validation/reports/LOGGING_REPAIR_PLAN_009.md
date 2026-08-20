# Logging Repair 009 — continuous causal coverage and formal-review deadlines

## Goal

Make the watcher answer one plain question without guessing: when the manager attended a subagent
or a scheduled formal review late, was it explicitly waiting/absent, explicitly busy with other
work, or not fully observed?

## Evidence that requires this repair

Sprint `20260801-attention-r9` is rejected at 0/3. Its canonical timeline contains a real sequence
of manager wait plus Cygnus/Atlas/Boreal handling and four late formal reviews, but the analyzer
cannot join successive explicit activities and does not classify late review starts. See
`20260801-attention-r9/ATTENTION_SUFFICIENCY_REPORT.md`.

## Required behavior

### 1. Normalize explicit manager activity intervals

Implement one internal interval representation with:

- manager session and invocation identity;
- start/end timestamps and source record IDs;
- activity identity and related event ID when applicable;
- cause class: `idle_or_absent` or `busy`.

Derive only from paired, canonical records:

- `MANAGER_WAIT_STARTED` → matching `MANAGER_WAIT_FINISHED`: idle;
- validated supervisor absence pair: idle/absent;
- `MANAGER_TOOL_STARTED` → matching `MANAGER_TOOL_FINISHED`: busy;
- `MANAGER_EVENT_CLAIMED` → matching `MANAGER_RESPONSE_PUBLISHED` (or, when explicitly declared
  terminal for the activity, matching decision/checkpoint): busy handling that exact event;
- `MANAGER_REVIEW_STARTED` → its matching response/checkpoint: busy review work.

Do not require normal claim records to invent `activity_id` or `related_event_id`; the exact event
ID plus manager session/invocation is the correlation key for event handling. Reject ambiguous,
cross-invocation, reversed, overlapping-incompatible, or unpaired records.

### 2. Prove a causal interval chain, not one convenient interval

Replace the single-interval requirement with an interval-union/chain check over the exact causal
window. The chain may contain multiple successive explicit activities from the same manager
invocation. It must cover the whole window; any uncovered time remains
`INSUFFICIENT_EVIDENCE`. Do not infer activity from transcript silence, process existence, harness
observation, or nearby point events.

For a fully covered chain:

- classify `IDLE_OR_ABSENT_MANAGER_DELAY` only when every covering interval is idle/absence;
- classify `BUSY_MANAGER_DELAY` when at least one covering interval is busy;
- retain notification-precedence rules: no successful canonical watcher notification is
  insufficient, and notification after a response deadline is harness delivery delay;
- retain exact wait-wake-to-claim handling and no-silence inference.

If real recorder transitions inherently leave a timestamp gap, do **not** hide it with a generous
fuzz constant. Add the smallest explicit additive record/field needed to close a state transition,
document it, and make old producers fail insufficient rather than being misclassified.

### 3. Classify formal-review cadence deadlines

Add a first-class branch for `MANAGER_REVIEW_STARTED` carrying `formal_review_due_utc`:

- on-time review start has no blocking impact;
- late review start uses the explicit causal chain from the due time through the review start;
- all-idle/absence coverage → `IDLE_OR_ABSENT_MANAGER_DELAY`;
- any busy coverage → `BUSY_MANAGER_DELAY`;
- incomplete coverage → `INSUFFICIENT_EVIDENCE`.

Formal review is self-scheduled, so do not require `WATCHER_NOTIFICATION_SENT` for the review event.
Preserve the existing acknowledgement-only behavior for a baseline update that is late after the
exact review/decision/response completed on time. Make precedence deterministic so a late review
start is not mislabeled acknowledgement-only.

### 4. Keep watcher optional

All watcher functionality remains conditional. With attention logging disabled or the watcher not
included, recorder paths no-op exactly as documented; normal harness and experiment execution must
not fail or require watcher files.

### 5. Tests and practical validation

Add focused tests that reproduce and distinguish:

1. R9-style response deadline: timely notification, wait interval followed by two other-event
   handling intervals, then a late claim → busy manager delay when fully covered.
2. The same shape with an uncovered gap → insufficient.
3. Entire-window explicit wait/absence → idle/absent manager delay.
4. Missing notification and late notification retain insufficient/harness precedence.
5. R9-style formal review due during another event's handling, late review start → busy manager
   delay.
6. Formal review due during a complete wait and late start → idle/absent manager delay.
7. Late formal review with a gap → insufficient.
8. On-time review and late baseline update → acknowledgement-only.
9. Cross-invocation or mismatched event pairs never form a chain.
10. Logging-disabled recorder remains a no-op.

Update `tests/run_attention_practical.py` with at least one fully covered multi-interval busy case.
Update `ATTENTION_LOGGING.md` with exact producer ordering and the formal-review rule.

## Verification gate

The coder must run and report:

- `python -m unittest discover -s harness_watcher_implementation/tests -t . -q`
- `python harness_watcher_implementation/tests/run_attention_practical.py`
- `python -m compileall -q harness_common orchestrator_harness harness_watcher_implementation`
- focused Ruff `F` checks on changed Python files;
- focused Pyright on changed Python files.

Then the main agent independently audits the diff and runs a fresh host-only metadata-file readiness
case proving a drained cursor and correct multi-interval/formal-review classifications. No new E2E
sprint starts until that readiness gate is green.

## Non-goals

- No codex-exec wake bridge.
- No production BYO-Firmware-MCP changes.
- No inference from silence or process liveness.
- No change to firmware experiment pass/fail evidence.
