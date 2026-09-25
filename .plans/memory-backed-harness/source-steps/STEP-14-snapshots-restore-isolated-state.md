# STEP-14 - Snapshots restore isolated recoverable state

## Outcome

An authorized operator exports consistent synthetic product state and restores its claimed capabilities into a fresh isolated identity, with trust and pending work intact or explicitly incomplete. This closes [BEHAVIOR-08](../specification/behaviors/BEHAVIOR-08-snapshots-restore-isolated-recoverable-state.md).

## Scope and touchpoints

Build the smallest snapshot service around `src/memory_harness/store.py`'s SQLite state and existing EverOS/Atlas identity/dependency adapters; add contracts in `contracts.py` only for externally consumed snapshot meaning. No benchmark snapshot system or generic backup platform.

## Implementation

Quiesce writers or use a consistent logical capture. Include exact decisions, dispatch/outcomes, reviewed receipts, approvals/current/revoked/tombstone and representation/configuration dependencies, usage, and pending/uncertain operations required by advertised capabilities. Mark unresolved protected source or remote dependency as incomplete; never claim remote simultaneity or completion without evidence. Verify integrity and namespace/root collision before target mutation. Restore to fresh compatible scope (optional remap only if explicitly tested), preserving pending effects for STEP-09/10 reconciliation rather than replaying blindly. Historical superseded failures remain history, not live blockers.

## Dependencies and integration

Consumes STEP-09/10 operation semantics and STEP-11 usage records. Produces isolated restore state and exact dependency/next-action status for STEP-15 and STEP-18 recovery proof.

## Requirement-fit validation

Prove trusted eligible behavior after fresh restore, intact revocation and pending status, corruption/missing-dependency/collision rejection before target mutation, and isolation of unrelated roots/remote partitions.

### Fast test suite

Add `tests/local/recovery/test_snapshot_restore.py` with a small synthetic SQLite/service fixture and faulted exports; compare eligibility and pending-operation behavior before/after restore. Live-service consistency is not inferred from local doubles.

## Failure scope and recovery

An interrupted export is not a complete snapshot; source state remains authoritative. A target conflict stops before mutation; never overwrite production or merge independent outcomes implicitly.

### Fast lane for revisiting old work

Repair the missing dependency/capture/restore branch, retain unaffected source and accepted effects, rerun the focused snapshot test and STEP-15/18 only where restored state is consumed.
