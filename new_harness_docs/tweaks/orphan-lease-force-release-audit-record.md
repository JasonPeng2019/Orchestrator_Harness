# Durable audit record for public orphan-lease force release

## Current behavior

`operator_launch lease force-release --resource-id <id>` performs the real recovery
correctly: it validates the requested declared resource, rereads the lease under the
lease lock, refuses a live exact holder, permits a dead/superseded/retired holder, removes
the one lease, and verifies that the file is gone.

The command returns a structured result to its caller, but it does not leave a durable
harness-owned record of the public recovery attempt. After a successful release, the
missing lease proves the resource is free; it does not say when the command was run,
which prior holder was released, or what result the command returned.

## Required change

Add one runtime-owned, append-only audit record for every public
`lease force-release` attempt. This is an audit trail, not a new lease authority,
automatic reclaim policy, approval gate, or replacement for ROOT's manager event.

Use one fixed runtime path owned by the lease subsystem, for example:

```text
<runtime>/resources/force-release-audit.jsonl
```

Each entry must contain only the facts needed to reconstruct the operation:

- timestamp;
- requested `resource_id`;
- operation outcome (`SUCCEEDED` or `FAILED`);
- the stable public result code;
- a short factual summary;
- when a lease record was safely readable, its prior `lane_id`, `run_id`, PID, and
  creation time; and
- on success, evidence that the lease's post-operation read-back was absent.

Do not store provider prompts, credentials, full environment variables, or unrelated
queue/event contents. The harness does not currently know the human/operator identity,
so it must not fabricate one.

## Ordering and honest failure behavior

The audit must not make the actual release ambiguous:

1. Record a durable `STARTED` entry before the destructive lease deletion attempt.
2. Run the existing exact-identity validation and release operation unchanged.
3. Append a durable terminal `SUCCEEDED` or `FAILED` entry after the actual outcome is
   known.

If the terminal audit write fails after the lease release succeeded, the command must
not claim the release failed or pretend no mutation occurred. It must return a distinct,
honest result that says: the lease was released and read-back confirmed, but the terminal
audit entry could not be written. The preceding `STARTED` entry remains durable evidence
that an operation was attempted. If the initial audit entry cannot be written, fail before
deleting the lease, because this public operation now requires a durable audit trail.

## Constraints

- Keep the existing single-resource public command and all exact holder/lane/run checks.
- Do not automatically release orphaned leases.
- Do not require ROOT acknowledgement, approval, or a new manager event before a
  correctly targeted public release.
- Keep the record project-workspace/runtime confined and platform-neutral.
- Reuse the existing record/locking helpers; do not create a second queue, service, or
  background process.

## Verification

Add focused tests showing:

1. A successful force release writes `STARTED` then `SUCCEEDED`, records the original
   holder facts, and confirms the lease is absent.
2. A live-holder refusal writes `STARTED` then `FAILED` and leaves the lease untouched.
3. An invalid or missing lease writes an honest failed attempt without inventing holder
   facts.
4. Initial audit-write failure prevents release.
5. Terminal audit-write failure after a successful release reports the true two-part
   outcome and leaves the `STARTED` evidence intact.
6. The existing orphaned-lease recovery path remains otherwise unchanged in the live
   integration campaign.
