# Global orphaned-lease discovery

## Current defect

The current monitor checks for an orphaned lease only while deriving status for a
non-retired active lane. A lease file can therefore survive after its lane has been
retired, abandoned, or otherwise removed from `active-lanes.json` without producing an
`orphaned_lease` notification.

That is the wrong discovery boundary. The resource remains blocked because the **lease
file** exists, regardless of whether its former lane still appears in the active-lane
index.

## Required change

Keep the existing persistent monitor and its normal active-lane status pass. Add one
small lease-discovery pass to that same monitor cycle:

```text
scan current lease files once
→ read each lease's resource, lane, run, and exact process identity
→ determine whether its recorded holder is still a valid live owner
→ surface each invalid owner as an orphaned lease
```

An owner is orphaned when the recorded exact PID-plus-creation-time holder is gone, or
when the lease does not belong to the lane's current run, or when the recorded lane is
retired/abandoned/missing. The pass must use retained lane records where available; it
must not rely solely on `active-lanes.json`.

This is discovery only. It must not automatically remove or reuse a lease. ROOT still
investigates and uses the existing public command:

```powershell
operator_launch lease force-release --resource-id <resource-id>
```

## Event and duplicate behavior

In managed mode, report an orphan with a normal manager event that identifies the
resource as well as the recorded lane/run. The event must be deduplicated per lease,
not merely per lane: one lane can hold more than one resource.

Use the existing manager queue/history as the durable duplicate basis where practical.
Do not add a second monitor, queue, scheduler, or general recovery service. If the
manager queue is deliberately replaced with a fresh queue identity, the still-present
orphan may be reported again in that new queue; that is appropriate because ROOT's
previous notification history is no longer available there.

In plain mode, the same lease discovery must be visible to `scan` and wake
`watch --until-actionable`, with the resource identity included in the returned
diagnostic. Plain mode does not create a manager queue.

## Constraints

- Scan the lease directory once per existing monitor pass; do not create a new process.
- Preserve the existing normal controller lease lifecycle and public force-release
  safety checks.
- A live exact holder is never reported as orphaned or released automatically.
- A force release or normal controller release makes the condition disappear on the
  next pass.
- Keep all records in the existing workspace-local runtime tree.

## Verification

Add focused tests for:

1. An active lane whose controller died with a remaining lease.
2. A retired lane with a leftover lease but no active-lane entry.
3. An abandoned or missing lane with a leftover lease.
4. An older-run lease while the lane has a newer current run.
5. A live exact holder, which must not be reported.
6. Two orphaned resources from one lane, which must remain separately identifiable.
7. No duplicate event on repeated monitor passes for the same unchanged lease.
8. A release makes the condition disappear.
9. Plain `scan`/`watch` visibility without creating or reading a manager queue.

The M09 campaign must exercise at least the retired-lane orphan case through the real
public force-release command and retain the monitor/queue/process evidence.
