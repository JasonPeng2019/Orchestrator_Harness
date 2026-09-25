# Lane 2 — product harness and setup

Lane 2 is the sole writer for `src/memory_harness/harness_bridge.py` and `harness_child.py`, plus product harness handoff, bootstrap, resume, launch, review, setup, provider payload, and operator entrypoint under `harness/orchestrator_harness`. Domain validation and SQLite transactions belong to lane 1. Preserve existing harness lifecycle and legacy task cards; do not introduce another scheduler, launcher, or reviewer.

Checkpoint commit: finish the harness portions of STEP-06-2 through STEP-08-2 and STEP-12-2 against lane 1's published context, dispatch, and outcome interfaces. Prove the harness-side handoff, observed native invocation, review-link handling, and installed payload in focused tests with faithful domain fixtures where needed. The real joined domain-to-harness path is pending until ROOT combines pinned lane commits; a checkpoint pass is not a product acceptance claim.

After pinning, continue STEP-11-2, STEP-13-2, and STEP-15-2 without waiting for checkpoint integration. Record any required domain-interface change for lane 1 rather than editing its files. See [LANE_GUIDE.md](../../LANE_GUIDE.md).
