# STEP-10-1 — Own external effect state

This step is a derivative of [original STEP-10](../../source-steps/STEP-10-external-effects-reconcile.md).

Owner: lane 1. This is the complete shared external-operation assignment.

Extend the existing operation state in `src/memory_harness/store.py` and `contracts.py` and the `runtime.py` service calls that submit effects; the EverOS and Atlas/procedure adapters remain with lanes 3 and 4.

Extend the STEP-09-1 operation semantics for EverOS, Atlas, and optional telemetry submissions. Persist a stable intent and payload identity before an enabled remote call. After lost acknowledgement, allow retry only after exact remote reconciliation or demonstrated adapter idempotency; otherwise keep uncertainty visible. Serialize conflicting retries, preserve unrelated effects, and report off transitions as pending until in-flight work is drained, reconciled, or isolated. Authorized revoke/withdraw follows its separate safety control. A remote outage never changes the fixed local outcome.

Lanes 3 and 4 own their respective adapter calls and exact readback. Evidence: operation-state fault, replay, concurrency, and feature-off tests shared with their adapter tests.

The durable operation record distinguishes pending, uncertain, and acknowledged for each exact source, scope, payload, and original configuration. Lost acknowledgement cannot be treated as failure or permission to issue another write. Late acknowledgement belongs to the original configuration. An off transition blocks new non-safety work and pending publication retries, but cannot report fully off until in-flight effects are drained, reconciled, or isolated. Authorized revoke/withdraw uses its own policy and network gate; an outage does not make it complete. Keep ROOT/operator recovery keyed to the exact operation ID, with unrelated effects free to proceed. Add lane-1-owned `tests.local.effects.test_external_reconciliation` cases using deterministic adapter faults and run directly affected procedure/publication tests without editing another lane's selector. Assert no second submission after ambiguity without exact reconciliation or demonstrated idempotency. A deterministic double establishes state logic, not live Atlas eligibility. Failure remains attached to the one operation and never changes a fixed local outcome.

For a revisit, repair only the affected operation transition, retain fixed outcomes and unrelated acknowledgements, and rerun deterministic fault and feature-off checks. Revisit STEP-14/15 only if the operation state they consume changed.
