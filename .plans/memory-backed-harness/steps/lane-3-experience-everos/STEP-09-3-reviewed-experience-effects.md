# STEP-09-3 — Recover reviewed experience and generation

This step is a derivative of [original STEP-09](../../source-steps/STEP-09-local-effects-reconcile.md).

Owner: lane 3. This is the complete reviewed-experience and generation assignment.

Use the existing reviewed-trajectory and ingestion store methods published by lane 1 at the `runtime.py` outcome boundary; extend `src/memory_harness/experience.py` rather than creating a second receipt or ingestion store.

Use the fixed outcome and lane 1's durable effect identity to retain reviewed trajectory, recent exact evidence, experience ingestion, and eligible generation independently of EverOS availability. Keep original source and operation identity on retries; do not generate a new quality outcome. Apply experience-write and generated-skill-creation off before new or queued submission while keeping exact local reviewed evidence. Preserve accepted provenance and approval gates; do not build learner updates.

Checkpoint evidence may cover adapter behavior with faulted inputs in lane-3-owned `tests.local.experience.test_outcome_to_ingestion_retry`; run lane 1's local-effect state selector read-only. After final merge, ROOT-owned joined evidence uses a real fixed local outcome and exercises crash/restart before and after intent, replay/concurrency, EverOS outage, and both off switches. Mark that joined check pending before merge.

Implement in `src/memory_harness/experience.py` and its focused tests, consuming lane 1's exact outcome and operation identities without editing shared store/contracts/runtime files. At the recoverable outcome boundary, keep deterministic intent for reviewed receipt, recent exact evidence, eligible experience ingestion, and generation under captured configuration. Local reviewed evidence survives an EverOS outage. On restart discover only missing or uncertain effects; confirmed ingestion/generation is not reissued with a fresh ID. Preserve accepted review provenance and generated-skill approval; do not add learner updates. Feature-off is checked before queued as well as new work, while already-submitted uncertain work remains visible. Run affected `tests.local.experience.test_reviewed_trajectory`, `test_step02_review_corrections`, and a focused outcome-to-ingestion retry test. An uncertain effect blocks only its conflicting duplicate, never the fixed quality outcome or unrelated effects.

For a revisit, repair only the affected ingestion/generation transition or identity join, keep valid reviewed evidence, and rerun focused retry and feature-off checks. Do not repeat accepted STEP-02's full suite unless its contract changed. Revisit STEP-10 only if shared operation semantics changed.
