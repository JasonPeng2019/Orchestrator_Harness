# STEP-14-1 — Capture and restore isolated durable state

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-14](../../source-steps/STEP-14-snapshots-restore-isolated-state.md).

Owner: lane 1. This is the complete snapshot and isolated-restore assignment.

Build around `src/memory_harness/store.py` SQLite state and existing EverOS/Atlas identity/dependency adapters. Add `contracts.py` fields only where snapshot meaning is externally consumed; do not build a benchmark snapshot system or generic backup platform.

Build the smallest consistent SQLite snapshot/export and fresh-scope restore around accepted store state. Include exact decisions, dispatch/outcomes, reviewed receipts, trust/approval/current/revoked records, representation/configuration dependencies, usage, and pending or uncertain operations needed by advertised capabilities. Mark unresolved remote or protected-source dependencies incomplete. Verify integrity, namespace/root collision, and compatibility before target mutation. Restore pending effects for reconciliation, never blind replay, and preserve unrelated roots/partitions.

Only an authorized operator may invoke export or restore at the snapshot service boundary, including calls that bypass the operator CLI; neither operation is an implicit task-path effect. Use synthetic product state for acceptance proof. Reject unauthorized export before disclosing protected state and unauthorized restore before target mutation, with focused negative tests.

Lanes 3 and 4 supply source-specific dependency/readiness facts through their existing adapters, not a second snapshot engine. Evidence: synthetic before/after eligibility and pending-state tests, corrupt/missing-dependency rejection, and isolated restore.

Quiesce writers or take a provably consistent logical capture. Include approvals, current/revoked/tombstone state, and the provenance needed to distinguish historical superseded failures from live blockers. Never claim remote simultaneity or protected-source completeness without evidence. An interrupted export is not a complete snapshot and leaves the source authoritative. Restore only into a fresh compatible scope; optional identity remap is allowed only when explicitly tested. Reject corrupt input, missing required dependencies, and namespace/root collision before target mutation. Never overwrite production or implicitly merge independent outcomes. Restore pending/uncertain effects for exact reconciliation, not blind replay. Add `tests.local.recovery.test_snapshot_restore` with synthetic SQLite/service fixtures, faulted export, before/after trust eligibility, revocation, pending status, and unrelated-root isolation. Local doubles cannot prove live-service consistency.

For a revisit, repair only the missing dependency, capture, or restore branch and retain unaffected source state and accepted effects. Rerun the focused snapshot tests; revisit STEP-15/18 only where restored state is consumed.
