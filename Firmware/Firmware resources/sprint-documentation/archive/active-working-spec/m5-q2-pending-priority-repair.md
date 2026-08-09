# M5 Q2 Native Pending-Priority Repair

## Goal

Fix the verified native harness defect from `20260802-m5-q2-123208Z`: a routine pending
`CHECKPOINT_UPDATED` notification prevented later deadline-bound blocked `HELP` signals from
becoming actionable until after their delivery deadlines.

This is a repair to the harness itself. It must not add a runner, wrapper, relay, retry loop,
background helper, or any other support layer around the harness.

## Verified failure

The managed harness admitted new worker signals while one notification was pending, but it always
kept returning the existing pending item until exact acknowledgement. Its priority selector ran only
when the pending slot was empty. In Q2, a priority-5 checkpoint occupied that slot while priority-1.5
blocked HELP signals accumulated in the deferred queue.

This made native queue order contradict the harness's existing priority/deadline policy.

## Accepted design

Add one narrow selection operation in the native notification layer:

1. After normal admission and mutable-handoff coalescing, compare the current pending event with the
   already-ranked deferred events.
2. Preempt only when a deferred event has a **strictly higher priority** (a lower numeric priority)
   than the pending event.
3. Move the preempted pending event back into the durable deferred queue with stable ranking and its
   original admission time, so it is not lost and is delivered after urgent work is acknowledged.
4. Make the higher-priority event the pending event and emit normal actionable/pending attention
   records for that transition.
5. Equal- or lower-priority work must not preempt. Existing exact-ack/redelivery behavior remains
   unchanged when no strict priority inversion exists.

The rule is generic across existing notification priorities; it must not hard-code lane names,
request IDs, paths, timestamps, or the Q2 epoch. Deadline ordering continues to break ties only
within the same priority, exactly as it does now.

## Required implementation

- Put the queue-selection logic in `orchestrator_harness/notifications.py`, the existing owner of
  notification admission and ranking.
- Call it from the managed native loop in `orchestrator_harness/cli.py` after admission/coalescing
  and before persisting/printing the pending state.
- Preserve notification identity, payload, admission facts, acknowledgement state, and at-least-once
  delivery.
- Keep the deterministic watcher read-only and unchanged unless a test proves a separate defect.
- Do not change the M5 evidence standard or excuse any Q2 delay.

## Required tests

1. A pending `CHECKPOINT_UPDATED` plus a newly admitted urgent blocked HELP selects HELP immediately.
2. The displaced checkpoint remains deferred and becomes selectable after HELP is acknowledged.
3. Equal- or lower-priority deferred work does not replace the pending event.
4. Repeated managed polling does not duplicate or lose either event.
5. The managed-loop regression test proves the HELP becomes actionable without waiting for the
   checkpoint acknowledgement.
6. Existing harness and watcher suites remain green.

## Repair workflow and acceptance

1. Root owns this plan and the final decision.
2. The persistent Terra coder implements the smallest change and tests.
3. An independent Terra reviewer reports concrete correctness risks; it never blocks.
4. Root accepts or rejects each finding and sends only accepted fixes back to the coder.
5. Luna runs focused practical smoke testing after review findings are resolved.
6. Root runs the relevant full suites, compile checks, readiness checks, and refreezes the tested
   Python surface.
7. Because native harness behavior changes, the comparable M5 count remains/reset to `0/3` and the
   next live attempt is attempt 3 of the goal's maximum 10 attempts.

## Definition of done

- Urgent work can no longer remain behind a lower-priority pending notification.
- The displaced notification is durable and eventually delivered.
- No wrapper or compensating runtime layer was added.
- Independent review has no accepted unresolved finding.
- Focused practical smoke and required test suites pass.
- Q2 is durably checkpointed as `HARNESS_BUG`, `WATCHER_PASS`, and
  `MANAGER_EVIDENCE_INSUFFICIENT`.
- `PLAN.md`, `HANDOFF.md`, current coordination/state, baselines, and readiness evidence describe the
  repaired surface and the actual `0/3`, attempt `2/10` boundary.
