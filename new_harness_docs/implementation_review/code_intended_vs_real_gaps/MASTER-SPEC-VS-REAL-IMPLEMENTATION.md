# Master-spec versus real implementation

## Scope and standard

This is a code audit against the current v2 requirements in
`new_harness_docs/master_docs/harness-master-spec.md`. It is not a list of
possible improvements. An item appears here only when either:

1. the master specification directly requires behavior the shipped code does not
   perform; or
2. the existing product flow plainly loses, strands, or misreports work.

The review read the current implementation in `harness-single/orchestrator_harness/`.
It did not treat a future tweak, a preferred architecture, or additional defensive
checking as a product defect.

## What was confirmed as real code behavior

The earlier explanations of the normal design were source-based, not based only on
the review documents:

- A managed worker writes an escalation file into its own worktree outbox; the
  monitor promotes it into the durable ROOT queue; ROOT reads, acknowledges,
  handles, and closes the resulting top-level event.
- The controller owns provider process execution and normal lease release. It
  records controller status, an append-only controller event log, provider
  transcript facts, stderr, and the last provider message.
- The monitor derives actionable statuses, including `orphaned_lease`; it does
  not automatically reclaim a lease. The public one-resource force-release
  command checks the exact PID-plus-creation-time holder before deleting a lease.
- `lane completion-review` writes the review/acceptance records; acceptance is
  separate from the review finding. Resume uses the saved native provider session
  through the selected adapter. Force-stop and shutdown use exact process identity,
  not broad executable-name killing.

Those statements describe the executable code. The findings below are the places
where the executable code does not reach the specified product behavior.

## Actual gaps

### GAP-01 — An outbox escalation can be lost when queue promotion fails

**Required behavior.** Part X.4 defines the worker outbox as a one-way escalation
path: the monitor consumes a file once, moves it to `processed-notifications/`, and
promotes the escalation to ROOT as an event. The obvious meaning is that a consumed
file reached ROOT's durable queue.

**Actual code.** `monitor._consume_outbox()` catches `ManagerQueueError` from
`promote_event()` and then unconditionally moves the original outbox file into
`processed-notifications/` anyway.

**Failure sequence.** A worker writes an escalation -> the manager queue is briefly
unreadable or cannot be atomically replaced -> promotion raises -> the source file is
marked processed -> no ROOT event exists. The escalation is no longer pending in the
worker outbox and there is no retry record.

**Why this is a real product defect.** The stated worker-to-ROOT escalation path loses
the worker's request before ROOT can receive it.

**Relevant code.** `orchestrator_harness/monitor.py`, `_consume_outbox()`.

### GAP-02 — Lost completion-review events and broken review pairs are not recovered

**Required behavior.** Part XII.5 requires health recovery to avoid permanently
stranding valid finished work. In managed mode it may create one replacement
`COMPLETION_REVIEW_REQUIRED` event when the matching valid result remains and no open
matching review event or complete acceptance pair exists. It also requires health
recovery to remove a malformed or incomplete review/acceptance pair, leaving the lane
pending rather than accepting it.

**Actual code.** `review._write_pair()` writes `COMPLETION_REVIEW.json` and then
`ORCHESTRATOR_ACCEPTANCE.json` as two separate atomic file replacements. If execution
stops between them, a one-file pair remains. The monitor only attempts to read a pair
when *both* files exist; it neither removes an incomplete pair nor restores the lane
to a clean pending state. `reconcile_active_lanes()` rebuilds the active-lane index,
but does not implement the required review-event or broken-pair recovery.

There is a second form of the same stranding problem. If a valid lane was already
marked `review_pending`, its `last_reported_actionable_status` is already
`review_pending`, and its manager review event is lost during queue replacement or
corruption, the monitor suppresses a new event as a duplicate. It does not check that
an open matching review event still exists.

**Why this is a real product defect.** A structurally valid finished lane can be left
without a route back to ROOT review, contrary to the explicit crash-recovery contract.

**Relevant code.** `orchestrator_harness/review.py`, `_write_pair()`;
`orchestrator_harness/monitor.py`, `_read_acceptance_chain()`,
`reconcile_active_lanes()`, and `_monitor_pass()`.

### GAP-03 — A normal ROOT PostToolUse hook does not create the specified durable delivery receipt

**Required behavior.** Parts X.1, X.2, X.5, and the queue-record definition say that
the managed PostToolUse hook appends a `DELIVERED` receipt to the manager event's
`delivery_history` when the hook boundary runs. This receipt is delivery evidence only;
it never acknowledges or closes the event.

**Actual code.** `root_hook_wrapper.run()` appends a delivery receipt only when the
hook environment contains `HARNESS_EVENT_ID`. There is no production code in the
harness that selects an unresolved queue event and sets that environment variable for
the provider hook. The only in-repository use that supplies it is a unit test.

Normal hook execution can therefore produce a ROOT notice and a root-hook liveness
line while leaving every queue event's `delivery_history` empty.

**Why this is a real product defect.** The specified durable proof that the hook
delivered a manager notification is absent in the normal shipped route.

**Relevant code.** `orchestrator_harness/root_hook_wrapper.py`, `run()`;
`orchestrator_harness/manager_queue.py`, `append_delivery_history()`.

### GAP-04 — The ROOT delivery notice omits required notice information

**Required behavior.** Part X.2 says the content-free ROOT delivery notice contains
pending count, highest class/severity, binding identity, and timestamp.

**Actual code.** `root_hook_dispatch._notice()` includes a provider ID, unresolved
count, a sorted set of event *types*, and a timestamp. It does not calculate or return
the highest severity, and it does not include the bound queue/epoch identity. Outbox
severity is flattened into a free-text event summary during promotion, so there is no
structured manager-event severity from which the hook could calculate a highest value.

**Why this is a real product defect.** ROOT receives a weaker notice than the specified
one: it cannot use the notice itself to identify the queue binding or prioritize by the
specified severity/class.

**Relevant code.** `orchestrator_harness/root_hook_dispatch.py`, `_notice()` and
`dispatch()`; `orchestrator_harness/monitor.py`, `_consume_outbox()`.

### GAP-05 — The monitor heartbeat lacks the required watched-lane count

**Required behavior.** Part IX.3 defines the monitor heartbeat as a refreshed
`last_heartbeat_at` value **with the watched-lane count** in `MONITOR.json`.

**Actual code.** `monitor._heartbeat()` writes only `health` and
`last_heartbeat_at`. The monitor record construction in `setup._start_monitor_locked()`
also has no watched-lane-count field.

**Why this is a real product defect.** A fresh heartbeat proves only that the monitor
loop reached its heartbeat write. It does not provide the specified evidence of how
many lanes the monitor was watching.

**Relevant code.** `orchestrator_harness/monitor.py`, `_heartbeat()`;
`orchestrator_harness/setup.py`, `_start_monitor_locked()`.

### GAP-06 — Monitor recovery is performed by the hook, rather than directed to ROOT as specified

**Required behavior.** Part IX.3 says the ROOT PostToolUse hook detects an unhealthy
monitor and directs ROOT to start a replacement through the monitor-start route; ROOT
performs that start.

**Actual code.** On every ROOT PostToolUse boundary,
`root_hook_dispatch.dispatch()` directly calls `run_monitor_recover()`. That function
can start or replace a monitor immediately, including force-stopping a hung monitor.
The notice reports the result after the hook has already acted.

**Why this is a master-spec mismatch.** It changes the stated authority and timing of
monitor recovery from "detect and direct ROOT" to automatic recovery inside the hook.
It is listed for fidelity to the specification, not as an argument that automatic
recovery is inherently worse.

**Relevant code.** `orchestrator_harness/root_hook_dispatch.py`, `dispatch()`;
`orchestrator_harness/setup.py`, `run_monitor_recover()`.

## Deliberately not counted as gaps in this document

These items have been discussed, but they are not failures of the shipped master-spec
behavior and are therefore excluded from the findings above:

- The proposed bounded invalid-result correction loop using native provider resume.
  The shipped master specification currently routes `result_invalid` to review and
  explicit `resume-lane`; the automatic correction loop is a requested future tweak.
- A generic `watch --until-actionable` wake-up for a new queue-only event. The current
  command watches lane-derived actionable status, with a separate explicit
  `--until-event` route. The broader wake-up behavior is a documented requested tweak,
  not counted here as a pre-existing master-spec failure.
- The strict exact-identity checks in public orphan-lease force release. They are
  additional safeguards, but do not stop the specified recovery path when the holder is
  provably dead or the lane/run is provably superseded.
- The absence of a real native multi-provider M09 campaign. That is an evidence/test
  completion gap, not proof that a particular implementation path is broken. It must
  remain clearly reported as unverified rather than called a pass.

## Audit limitation

This is a source inspection, not a completed native-provider campaign. It establishes
what the Python implementation will do along the traced paths. It does not prove that
Codex, Claude Code, or Qwen Code will invoke their installed native hooks correctly on
this host; that needs the still-uncompleted live test campaign.
