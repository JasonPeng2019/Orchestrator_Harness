# STEP-09 - Enabled local effects reconcile after the outcome

## Outcome

A fixed outcome yields recoverable enabled local reviewed-evidence, experience-ingestion, and generation work without repeating the quality decision. This is the local-effects portion of [BEHAVIOR-04](../specification/behaviors/BEHAVIOR-04-terminal-outcome-and-effects-reconcile.md).

## Scope and touchpoints

Use existing `MemoryStore` review receipt, reviewed trajectory, and `experience_ingestions` methods in `src/memory_harness/store.py`, `experience.py`, `contracts.py`, and `runtime.py`. Preserve accepted provenance and generated-skill gates; do not build learner updates.

## Implementation

At the recoverable local outcome boundary, retain deterministic intent for each effect allowed by the captured configuration. Persist reviewed receipts and recent exact evidence independently of optional EverOS availability. Make ingestion/generation retries use their original source and operation identities; enforce experience-write/generated-skill-creation off before new or pending submission. On crash, discover only missing or uncertain effects. Two processes cannot commit conflicting local effect progress, and a confirmed effect is not re-issued under a fresh identity. Keep effect error/uncertainty actionable while the terminal outcome remains fixed.

## Dependencies and integration

Consumes STEP-08's fixed outcome and existing reviewed-experience contracts. Produces durable local effect/operation semantics reused by STEP-10 remote effects and STEP-14 snapshots.

## Requirement-fit validation

Show crash/restart before and after intent, independent recent evidence during EverOS outage, idempotent/concurrent retry, and actual suppression when experience write or generation is off.

### Fast test suite

Run directly affected `tests/local/experience/test_reviewed_trajectory.py` and `test_step02_review_corrections.py` plus a new focused outcome-to-ingestion retry selector. Do not repeat accepted STEP-02's full suite unless its contract changed.

## Failure scope and recovery

An uncertain ingestion blocks only duplicate/conflicting submission for that effect. Preserve the fixed outcome, reviewed receipt, and other completed effects.

### Fast lane for revisiting old work

Repair the local effect transition or identity join, rerun its focused retry/feature-off tests and STEP-10 only if the shared operation semantics changed.
