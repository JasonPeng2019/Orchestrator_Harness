# STEP-07-2 — Observe and reconcile the native launch

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-07](../../source-steps/STEP-07-harness-dispatch-reconciles-invocation.md).

Owner: lane 2. This is the complete native-launch assignment.

At the actual bootstrap/resume/launch boundary validate lane 1's exact accepted envelope and final context, call lane 1's `record_dispatch_intent` operation and confirm its intent is durable, then use the existing product harness to launch. Link the observed native invocation to the task, plan, context, lane, and run. A lost acknowledgement triggers exact native lookup; unresolved ownership prevents a second blind launch. Exclude product control-plane credentials from worker prompt, environment, and tools. Keep harness review and cleanup ownership unchanged.

Evidence: directly affected memory_handoff, launch-boundary, and lifecycle tests including ambiguity, wrong-plan refusal, credential exclusion, and legacy behavior. Lane 1 owns the domain intent transaction.

Use the existing `harness/orchestrator_harness/memory_handoff.py`, `bootstrap.py`, `resume.py`, and `launch.py` path. Validate the exact accepted plan and finalized context again at the actual last launch boundary; a prepared envelope alone is not an observed invocation. Join actual native run/task/plan/context identity to the prelaunch intent. A lost acknowledgement requires exact native lookup before any retry; unresolved ownership blocks conflicting launch or reuse. Feature-off and all-off must reach the real launch path without optional memory/APC work, while ordinary legacy task cards still complete. Scrub product control-plane credentials and mutation authority from the actual worker prompt, environment, tools, configuration, and diagnostics without inventing a secret manager. A required task credential uses a validated task-only channel or blocks only its dependent action. Keep existing harness launch, review, cancellation, and cleanup authority; add no scheduler. Run `test_memory_handoff.py`, `test_step04_launch_boundary.py`, `test_step04_lifecycle_integration.py`, and the affected domain dispatch selector. A missing mandatory handoff blocks only enhanced launch, not unrelated lanes.

For a revisit, inspect the exact intent/native receipt pair and repair only that join. Launch, envelope, or credential-input changes invalidate the direct dispatch and harness-launch checks; rerun those focused checks, not the full harness suite per edit. Revisit STEP-08 only if the execution identity changed.
