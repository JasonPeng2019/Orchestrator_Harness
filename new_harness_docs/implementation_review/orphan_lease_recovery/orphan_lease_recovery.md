# Orphaned lease recovery

This document describes the implementation that is currently shipped. It is about the recovery of an exclusive-resource lease whose original lane or controller is no longer a valid owner.

## What a lease is

A lane can declare an exclusive resource: something that two lanes must not use at the same time. Before the lane's controller begins provider work, it takes a lease for every resource the lane declared.

Each lease is a small JSON record in the harness runtime:

```text
<runtime>/resources/leases/<SHA-256 of resource ID>.lease
```

The record stores:

- `resource_id`: the protected resource.
- `lane_id`: the lane that took it.
- `run_id`: the particular run of that lane.
- `pid` and `creation_time`: the exact controller-process incarnation that took it.
- `acquired_at`: when it was taken.

The filename is hashed so a resource ID cannot become an unsafe filesystem path.

## Taking and normally releasing leases

The controller takes all of a lane's requested leases under a shared lease lock. It first verifies that none already exist. It then writes all of them. If writing any lease fails, it removes the leases it had written in that attempt and fails the launch. A lane therefore gets all of its exclusive resources or none of them.

During an ordinary finish, the controller first proves that its provider and helper-process boundary is gone. Only then does it remove leases whose `lane_id` and `run_id` both match its own current run. Matching the run ID is important: an old controller cannot remove a lease belonging to a later run of the same lane.

## What makes a lease orphaned

The monitor checks active lanes against the lease records. It reports `orphaned_lease` for a lane when it finds a lease for that lane and either of these is true:

1. The lease's `run_id` differs from the lane's current `run_id`. The lease belongs to an older run.
2. The recorded process no longer matches the recorded PID and creation time. The original controller is gone, or the PID has been reused.

The creation time is included because a PID by itself is not safe evidence. Operating systems can later assign the same PID to an unrelated process. The harness treats PID plus creation time as the identity of the actual holder.

The monitor reports the condition as an actionable manager event. It does not silently delete the lease. That is intentional: freeing an exclusive resource without proof could let two still-live workers use it at once.

## ROOT's recovery path

When ROOT receives the notification, the intended sequence is:

1. Read the event and the affected lane/lease evidence.
2. Acknowledge the event after reading it.
3. Determine the real cause: a dead controller, a force-stopped/retired lane, or an old lease left behind by a previous run.
4. If the lease is safe to clear, run the public command:

   ```powershell
   operator_launch lease force-release --resource-id <resource-id>
   ```

5. Fix or resume the lane separately if that is needed.
6. Close the manager event with a factual summary of what ROOT did.

Clearing a lease only makes the resource available again. It does not repair the lane, resume a provider, approve work, retire the lane, or delete the worktree.

## What the public force-release command checks

`lease force-release` is the public, one-resource-at-a-time recovery command. It does not accept a lane ID, and it will not operate on an undeclared resource.

Under the same lease lock used by acquisition, it rereads the current record and checks all of the following before removing anything:

1. The lease file exists and conforms to the lease schema.
2. The record's `resource_id` matches the requested resource.
3. The lane ID, run ID, PID, and creation time are present and valid.
4. The exact recorded process is not still alive.

If the exact PID-and-creation-time process is alive, the command refuses with `FORCE_RELEASE_HOLDER_LIVE`. This remains true even if a lane record says that the lane is retired: a live exact holder always wins over stale lane metadata.

If the exact process is not live, the command permits removal only when it can prove at least one of these conditions:

- The PID no longer exists.
- The PID exists but has a different creation time, proving it is a new, unrelated process and the original holder is dead.
- The corresponding active lane is `retired` or `abandoned`.
- The corresponding active lane has a different current run ID, proving this is an old-run lease.

If the process cannot be observed well enough and none of the lane/run proofs applies, the command refuses with `FORCE_RELEASE_HOLDER_UNPROVEN`. This is fail-closed behavior: ROOT must obtain better evidence or first safely retire/abandon the lane instead of deleting the record by hand.

After removal, the command checks that the file is really absent. A deletion failure is reported as `FORCE_RELEASE_DELETE_FAILED` rather than reported as success.

## Related forced paths

`lane force-stop` has an internal bulk-release path for all leases belonging to the lane. That path is used only after force-stop has handled the lane's process boundary; it is not the general manual recovery mechanism.

The public recovery interface remains the narrow `lease force-release --resource-id ...` command so that ROOT explicitly names the resource being released and receives a stable result code and next action.

## Important implementation limits

- The monitor's job is detection and escalation, not automatic repair. A notification is a request for ROOT to investigate.
- A corrupt lease record is skipped by the monitor's ordinary lease scan because it cannot be parsed as a valid lease. The public command detects and refuses an invalid record when ROOT targets its declared resource; it does not overwrite it.
- Do not hand-edit lease files. It bypasses the lock, the exact-process check, and the read-back verification.

## Relevant implementation files

- `harness-single/orchestrator_harness/leases.py`: lease records, atomic acquire/release, and safe single-lease force release.
- `harness-single/orchestrator_harness/monitor.py`: orphan detection and manager-event escalation.
- `harness-single/orchestrator_harness/operator_launch.py`: the public `lease force-release` command.
- `harness-single/orchestrator_harness/launch.py`: the force-stop path that releases a stopped lane's leases.
