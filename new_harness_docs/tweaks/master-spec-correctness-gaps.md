# Master-spec correctness gaps

These are implementation changes required because the shipped code either fails an
explicit v2 master-spec behavior or loses/strands work in the stated product flow.
They are not optional hardening ideas.

The source audit is at
`new_harness_docs/implementation_review/code_intended_vs_real_gaps/MASTER-SPEC-VS-REAL-IMPLEMENTATION.md`.

## 1. Do not consume a worker escalation until it is durably promoted

**Current defect:** `monitor._consume_outbox()` moves an outbox notification to
`processed-notifications/` even if `promote_event()` failed. ROOT can lose the
worker's escalation completely.

**Required change:** promote the event first. Move the outbox file only after the
queue write succeeded. On a failed promotion, keep the original outbox file pending
for a later monitor pass and preserve the failure evidence.

**Done when:** a simulated manager-queue write failure leaves the source outbox file
in place; a later successful pass creates exactly one manager event and only then
moves the file to `processed-notifications/`.

## 2. Implement the required review-event and broken-pair recovery

**Current defect:** a valid `review_pending` lane can be stranded if its manager
review event is lost/reset, because the monitor suppresses a replacement event as a
duplicate. A crash between the review and acceptance file writes can also leave an
incomplete pair which no health path removes.

**Required change:** implement Part XII.5 of the master spec:

- remove a malformed or incomplete review/acceptance pair without inferring
  acceptance;
- preserve/restore the terminal pending state; and
- in managed mode create exactly one replacement completion-review event when the
  current valid result has no complete pair and no open matching event.

**Done when:** fault-injection tests cover a lost manager review event and an
interruption between the two pair writes. In both cases the valid lane becomes
reviewable again without a duplicate open review event or an inferred acceptance.

## 3. Make normal ROOT PostToolUse delivery create a durable event receipt

**Current defect:** the wrapper writes `delivery_history` only if its environment
contains `HARNESS_EVENT_ID`. The harness does not set that variable in its normal
production route, so a normal pending manager event can be noticed without gaining
the specified durable `DELIVERED` receipt.

**Required change:** bind the real unresolved manager event(s) to the ROOT hook's
delivery handling, using a harness-owned mechanism that works for the normal shipped
provider route. Append a receipt only as delivery evidence; never acknowledge or close
the event automatically.

**Done when:** a real normal hook invocation with a pending event adds one durable
`DELIVERED` entry to that event's `delivery_history`, while the event remains pending.

## 4. Return the required information in the ROOT delivery notice

**Current defect:** the notice has a provider ID, event types, count, and timestamp,
but not the master-spec's highest class/severity or binding identity. Escalation
severity is currently flattened into free text, so it cannot be selected reliably.

**Required change:** preserve the needed class/severity as structured event data and
make the content-free ROOT notice include pending count, highest class/severity,
binding identity, and timestamp.

**Done when:** multiple pending events with different severities produce a notice
containing the expected highest severity and the fixed binding/queue identity, without
including an event payload or changing any manager-event state.

## 5. Record the watched-lane count in each monitor heartbeat

**Current defect:** the master spec requires `MONITOR.json` heartbeat evidence to
include the watched-lane count. The implementation only refreshes `health` and
`last_heartbeat_at`.

**Required change:** record the number of lanes the monitor inspected in the same
heartbeat update, with a defined value when no active epoch exists.

**Done when:** a monitor pass over a known number of active lanes updates both the
heartbeat timestamp and the correct watched-lane count atomically in `MONITOR.json`.

## 6. Restore the specified monitor-recovery authority boundary

**Current defect:** the master spec assigns the ROOT PostToolUse hook detection and
direction only; ROOT is meant to run the monitor-start route. The current hook directly
calls `run_monitor_recover()`, which can kill and replace a monitor before ROOT receives
the notice.

**Required change:** make the hook report the unhealthy monitor and the public recovery
action to ROOT without performing replacement itself, or explicitly revise the master
spec if automatic hook-side recovery is the desired product design.

**Done when:** the actual code and master spec agree on who performs recovery, and a
test demonstrates the selected behavior for dead, hung, and deliberately stopped
monitors.

## Diagnostic evidence note

The current logs are useful for diagnosing an individual lane, but they cannot prove
all native provider integrations work or automatically identify every unimplemented
feature. In particular, monitor passes can skip a lane on an exception without recording
that error, while later heartbeats can still appear healthy. The fuller evidence audit is
at `new_harness_docs/implementation_review/logging_actual_correctness/LOGGING-AND-DIAGNOSTICS.md`.
