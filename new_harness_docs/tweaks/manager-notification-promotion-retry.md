# Manager notification promotion retry

## Status

Small reliability tweak. Not a change to the notification workflow or ROOT's
responsibilities.

## Problem

A managed lane writes a notification file to:

```text
<lane-worktree>/.agent-workspace/manager-notifications/notice-<id>.json
```

The monitor promotes that notice into the durable manager queue and then
archives the source file in `processed-notifications/`.

Today, if manager-queue promotion raises `ManagerQueueError`, the monitor
still moves the source file to `processed-notifications/`. ROOT can therefore
miss a worker escalation when the queue is unavailable, invalid, or belongs to
a replaced epoch.

## Required behavior

1. Read one outbox notice.
2. Promote its manager event into the durable runtime queue.
3. Move the source notice to `processed-notifications/` only after promotion
   succeeds.
4. If promotion fails, leave the source notice in `manager-notifications/` so
   a later monitor pass can retry it.
5. Do not silently discard the error. Record or surface a monitor-health
   diagnostic that tells ROOT promotion needs attention.

The queue remains the durable source of ROOT obligations. ROOT may read its
`QUEUE.json` directly with ordinary read-only agent capabilities; public
commands remain the only way to acknowledge or close events.

## Scope

The likely code change is the managed outbox loop in
`harness-single/orchestrator_harness/monitor.py` (`_consume_outbox`). It must
not change worker notification syntax, the queue event lifecycle, or ROOT's
acknowledge/close commands.

## Acceptance checks

- Successful promotion creates exactly one pending queue event and archives
  the source notice.
- A forced `ManagerQueueError` leaves the source notice in the outbox and does
  not create a processed copy.
- A later successful monitor pass promotes that retained notice and archives
  it.
- Existing managed notification and queue-lifecycle tests continue to pass.
