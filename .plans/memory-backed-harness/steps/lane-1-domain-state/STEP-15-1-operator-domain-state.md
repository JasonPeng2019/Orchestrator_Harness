# STEP-15-1 — Expose exact domain readiness and recovery

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-15](../../source-steps/STEP-15-operator-controls-expose-truth.md).

Owner: lane 1. This is the complete operator-facing domain-state assignment.

Keep one narrow `memory_harness` facade over the existing `runtime.py`, `store.py`, resolved configuration, snapshot, and usage surfaces; lane 2 owns the harness operator entrypoint.

Provide a narrow read/recovery facade over configuration, compatible schema, preparation, pending and uncertain operations, snapshots, and usage. Report exact build/root, requested/effective feature and network state, unavailable dependency, and one actionable next step without credentials. Read-only readiness must not mutate state. Recovery uses exact operation IDs and STEP-09/10 retry rules. Keep domain decisions here; lane 2 exposes them through the existing harness operator entrypoint.

Evidence: focused ready/blocked, no-secret, pending/uncertain, and non-mutating-read tests. A missing service blocks only its dependent action.

Project actual preparation/finalization, compatible schema, exact build/root, requested/effective features and network profile, service and binding availability, pending/uncertain operations, snapshot dependencies, and usage completeness. Supply a single actionable next step per blocked action without hiding unrelated ready actions or leaking credentials. Recovery is an explicitly authorized exact-operation action under the STEP-09/10 reconciliation rules; snapshot mutation likewise requires explicit authority, while readiness and usage reads stay non-mutating. Do not add scheduler, launcher, reviewer, or another controller. Add lane-1-owned `tests.local.operator.test_readiness` and directly affected service tests for ready/blocked paths, exact pending ID, no-secret output, absent service, and no mutation on read. Lane 2 presents this facade through the existing harness entrypoint.

For a revisit, repair only the affected domain-to-operator projection and rerun its direct readiness/recovery checks. Revisit only the integrated proof step whose preflight consumed the changed result.
