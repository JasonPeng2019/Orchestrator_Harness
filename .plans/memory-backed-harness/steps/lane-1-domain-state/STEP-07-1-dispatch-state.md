# STEP-07-1 — Persist and reconcile dispatch identity

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-07](../../source-steps/STEP-07-harness-dispatch-reconciles-invocation.md).

Owner: lane 1. This is the complete durable-dispatch assignment.

Wire the existing `src/memory_harness/runtime.py` `dispatch`, `record_dispatch_intent`, and `reconcile_ambiguous_dispatch` operations to lane 2's harness handoff; use the shared `store.py` intent state rather than creating a second dispatch path.

At the domain boundary validate the STEP-06-1 final context against the exact accepted plan and actual target. Persist one dispatch intent before lane 2 performs an effectful native launch. Join an observed invocation by task, decision, plan, context, lane, and run identity. An ambiguous acknowledgement requires exact native reconciliation; unresolved ownership blocks conflicting relaunch. Preserve ordinary cards with no memory handoff and enforce feature-off before optional dispatch work.

Expose narrow runtime/store operations for lane 2's STEP-07-2; do not create another launcher or review authority. Evidence: direct runtime-dispatch tests for wrong/proposed context, intent replay, ambiguous acknowledgement, exact reconciliation, and legacy path preservation.

Distinguish finalized context, recorded intent, observed invocation, ambiguous, abandoned, failed launch, and reconciled native ownership. Validate exact task, objective, decision, base, route, accepted revision, context, target lane, and run at the last domain boundary. A nonempty wrong or stale plan is a hard enhanced-dispatch error. An abandoned pre-dispatch decision never receives an outcome. Preserve the existing harness's review and cleanup ownership. Unknown native ownership blocks only conflicting relaunch or lane reuse; it must not mutate accepted state or break unrelated ordinary cards. Run `tests.local.contracts.test_runtime_dispatch` plus affected `test_memory_handoff.py`, `test_step04_launch_boundary.py`, and `test_step04_lifecycle_integration.py` cases. Include feature-off/all-off and actual observed-versus-intended distinctions; no local envelope test alone proves launch.

For a revisit, inspect the exact persisted intent and native receipt, repair only their join, and retain unrelated valid dispatch state. Changed launch, envelope, or credential inputs invalidate direct dispatch and affected harness-launch checks; rerun those checks and revisit STEP-08 only if execution identity changed.
