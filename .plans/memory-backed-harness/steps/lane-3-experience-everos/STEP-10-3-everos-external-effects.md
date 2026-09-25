# STEP-10-3 — Reconcile EverOS submissions

This step is a derivative of [original STEP-10](../../source-steps/STEP-10-external-effects-reconcile.md).

Owner: lane 3. This is the complete EverOS external-effect assignment.

At the EverOS service boundary use lane 1's stable intent, payload identity, and pending/uncertain/acknowledged transitions. Recover lost acknowledgement by exact remote readback or demonstrated idempotency before retry; otherwise retain uncertainty and block conflicting submission only. Honor experience-write and other applicable off gates at service entry, including pending non-safety work. Late acknowledgement keeps original configuration attribution. Supply real dependency/availability facts to STEP-14-1 and STEP-15-1; do not assert remote snapshot simultaneity.

Checkpoint evidence covers adapter exact lookup, idempotency behavior, and deterministic faults without claiming outcome integration. After final merge, joined evidence covers exact linked effect, outage, lost acknowledgement, concurrent retry, off transition, and immutable local outcome; report that joined check pending on the isolated branch.

For any model, CLI, embedding, or retrieval call actually started by the EverOS adapter, expose its native invocation identity and source-native usage receipt to lane 1's usage contract. If the source exposes no counters, report the started call as incomplete, never zero; accept late receipts without duplicating a call or changing the fixed outcome. Add lane-3-owned adapter tests for available, absent, and late counters. Do not create a second usage ledger.

Implement at `src/memory_harness/everos_adapters.py` and relevant experience service calls, consuming the lane 1 operation record. Persist stable source, scope, payload, original configuration, and operation identity before any enabled submission. Distinguish pending, uncertain, and acknowledged. A lost acknowledgement permits retry only after exact remote readback or demonstrated source-backed idempotency; if neither proves safety, leave uncertainty and block only the conflicting duplicate. Serialize concurrent retries, permit unrelated effects, and attribute a late acknowledgement to the original configuration. Experience-write/all-off prevents new and pending non-safety submissions; in-flight work must drain, reconcile, or be isolated before reporting fully off. Remote outage cannot reverse local acceptance. Add lane-3-owned `tests.local.experience.test_everos_external_reconciliation` deterministic adapter-fault cases; run but do not edit lane 1's state selector. Local doubles prove state logic, not remote simultaneity or a live-service claim; report unresolved dependencies to snapshot/operator consumers.

For a revisit, repair only the affected EverOS adapter or exact operation transition, keep fixed outcomes and unrelated acknowledgements, and rerun fault and feature-off checks. Revisit STEP-14/15 only if their consumed operation state changed.
