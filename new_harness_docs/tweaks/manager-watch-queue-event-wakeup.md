# Manager watch must wake for queue-only events

## Status

Small manager-loop liveness fix.

## Problem

The shipped ROOT skill `manager-notification-watch` tells ROOT to run:

```text
operator_launch watch --until-actionable
```

when ROOT is deliberately idle and waiting for manager activity. The current
watch implementation only checks derived lane statuses. It does not return
when a worker creates a manager-queue event that has no simultaneous actionable
lane status.

This means a queue-only worker escalation can remain unnoticed while ROOT is
deliberately waiting. ROOT will see it after another tool-use hook or a manual
queue read, but the idle watch did not perform its stated job.

## Required behavior

`watch --until-actionable` must return promptly when either condition becomes
true:

1. a lane has an actionable derived status; or
2. the managed manager queue contains a new or unresolved event.

The returned structured result must identify whether it woke for a lane status
or a manager event and include the relevant top-level manager `event_id` when
the queue caused the wake-up. ROOT then reads the durable queue read-only and
uses the ordinary acknowledge/handle/close flow.

Plain mode has no manager queue. In plain mode, watch continues to wake only
for lane-status conditions.

## Scope and constraints

- This is a foreground blocking wait used only when ROOT is deliberately idle.
  It is not a background daemon and cannot wake a terminated/inactive ROOT
  conversation.
- Do not create a second queue, relay, acknowledgement mechanism, or event
  producer. `runtime/manager/QUEUE.json` remains authoritative.
- Do not alter manager-event states merely by observing them.
- Preserve existing timeout behavior and the explicit `--until-event <id>`
  behavior.
- Deduplicate repeated wake-ups from the same unresolved event until ROOT has
  handled it, while still returning promptly for a newly created event.

## Acceptance checks

1. In managed mode, a worker outbox notice promoted to the manager queue wakes
   an already-running `watch --until-actionable` even when no lane-status
   condition is actionable.
2. The returned record identifies the top-level queue event ID and requires no
   manual polling to discover it.
3. A lane-status condition still wakes watch as before.
4. Terminal queue events do not keep waking watch.
5. Plain mode never attempts to read or create a manager queue.
6. Timeout, `--until-event`, and normal acknowledgement/close behavior remain
   unchanged.
7. A real-provider live integration test proves the idle ROOT watch wakes for
   a real worker `manager-notify` escalation.
