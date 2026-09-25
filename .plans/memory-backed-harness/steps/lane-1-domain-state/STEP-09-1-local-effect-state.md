# STEP-09-1 — Own local effect intent and recovery

This step is a derivative of [original STEP-09](../../source-steps/STEP-09-local-effects-reconcile.md).

Owner: lane 1. This is the complete local-effect state assignment.

Reuse the existing `MemoryStore` review-receipt, reviewed-trajectory, and `experience_ingestions` methods in `src/memory_harness/store.py`; connect them through `contracts.py` and the `runtime.py` recoverable outcome boundary. Lane 3 owns `experience.py` adapter behavior and does not edit these shared records.

Define the durable operation identity and transitions shared by local effects and STEP-10 external effects. From a fixed STEP-08 outcome, retain independently recoverable reviewed receipt, recent exact evidence, ingestion, and generation intent according to captured configuration. Concurrent processes must not commit conflicting progress; a confirmed effect cannot be resubmitted under a new identity. An uncertain effect remains actionable while the terminal outcome stays fixed. Feature-off prevents new or pending non-safety submission without erasing local review evidence.

Lane 3 owns the experience/EverOS implementation in STEP-09-3. Evidence: lane-1-owned `tests.local.effects.test_local_effect_state` store/replay/concurrency and off-state tests, including crashes before and after intent; run the lane-3-owned focused outcome-to-ingestion retry selector read-only when it exists.

At the recoverable fixed-outcome boundary, persist deterministic intent for each effect allowed by captured configuration. Keep the reviewed receipt and recent exact evidence independent of optional EverOS availability. Ingestion and generation retries retain their original source and operation identities. After a crash discover only missing or uncertain effects, never resubmit confirmed ones under fresh IDs. Enforce experience-write and generated-skill-creation off before new and pending submission without erasing local evidence; do not build learner updates. Run directly affected `tests.local.experience.test_reviewed_trajectory` and `test_step02_review_corrections` cases read-only; lane 3 owns the outcome-to-ingestion adapter retry selector. An uncertain ingestion blocks only its conflicting duplicate, preserving the fixed outcome and other completed effects.

For a revisit, repair only the local effect transition or identity join and rerun focused retry and feature-off checks. Retain valid fixed outcomes and review evidence; do not repeat accepted STEP-02's full suite unless its contract changed. Revisit STEP-10 only if shared operation semantics changed.
