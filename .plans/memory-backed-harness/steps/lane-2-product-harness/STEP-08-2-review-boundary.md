# STEP-08-2 — Supply exact native review evidence

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-08](../../source-steps/STEP-08-terminal-outcome-is-fixed-once.md).

Owner: lane 2. This is the complete native-review evidence assignment.

At the existing review/completion seam supply lane 1 with the exact observed invocation, result, review, acceptance, and exceptional-acceptance evidence. Do not infer terminal state from an absent receipt and do not let an APC child result stand for its parent. Repeated delivery of the same native evidence must be safe; contradictory or wrong-run evidence must remain visible for the domain transaction to reject.

Evidence: affected harness review and lifecycle tests for PASS, FAIL, BLOCKED, no observation, replay, wrong run, and forced acceptance. Lane 1 alone fixes the immutable local outcome.

Supply exact task, objective, decision, accepted plan, dispatch/run, result, review, and acceptance identities at the existing `harness/orchestrator_harness/review.py` completion seam. Preserve PASS, FAIL, BLOCKED, genuine terminal unknown, and forced/exceptional acceptance distinctions. An absent receipt is not terminal unknown; a child APC review is not parent acceptance. Deliver the same evidence safely after crash/restart, without modifying a prior fixed outcome or inferring success from process exit. If native evidence conflicts or is wrong-run, expose it for lane 1's transaction to reject while preserving original evidence. Run directly affected harness review/lifecycle selectors and the domain outcome selector for replay, pre/post-fixation crash, conflict, and quality-versus-effect separation. The integrated native campaign later proves the real completion boundary.

For a revisit, repair only the exact native-evidence join and retain valid dispatch receipts. Rerun focused review/outcome tests; revisit STEP-09/10 only if the outcome identity consumed by those effects changed.
