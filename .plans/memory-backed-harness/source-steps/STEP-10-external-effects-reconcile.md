# STEP-10 - Enabled external effects reconcile safely

## Outcome

Enabled EverOS/Atlas publication, administrative safety operations, and optional telemetry retain exact pending/uncertain/acknowledged state and recover without blind duplicate writes. This is the external-effects portion of [BEHAVIOR-04](../specification/behaviors/BEHAVIOR-04-terminal-outcome-and-effects-reconcile.md).

## Scope and touchpoints

Extend operation state in `src/memory_harness/store.py`/`contracts.py` and the existing `everos_adapters.py`, `atlas_adapters.py`, `procedures.py`, and runtime service calls where they submit external effects. Reuse accepted trust, approval, designation, publication, withdrawal, and revocation authority; do not redesign it.

## Implementation

Write a stable intent/payload identity before each enabled external submission. On lost acknowledgement, query the exact remote effect or use an adapter's demonstrated idempotency key before retry; if neither is safe, retain visible uncertainty. Serialize conflicting pending retries without blocking unrelated operations. Off transitions prevent new non-safety writes and pending publication retries, while authorized revoke/withdraw remains governed by its separate policy/network control. Drain, reconcile, or isolate in-flight work before reporting fully off; late acknowledgement belongs to the original configuration. Remote outage never changes a fixed local outcome.

## Dependencies and integration

Consumes STEP-08's outcome and STEP-09's operation lifecycle. Produces pending-state/recovery truth for STEP-14 snapshot and STEP-15 operator controls. Live Atlas eligibility itself is proven in STEP-17.

## Requirement-fit validation

Test lost acknowledgement, concurrent retry, off transition, revoke/withdraw exception, scoped remote identity, and outage independence. A local double proves state logic but not an actual Atlas service result.

### Fast test suite

Add a focused `tests/local/effects/test_external_reconciliation.py` selector using deterministic adapter faults, and run directly affected existing procedure/publication tests. Assert no second submission after ambiguity without exact reconciliation or demonstrated idempotency.

## Failure scope and recovery

Contain only the exact uncertain remote operation and conflicting retries; do not erase pending state to make a switch appear off. Use an authorized operator recovery path when automatic reconciliation cannot decide it.

### Fast lane for revisiting old work

Re-enter the affected adapter/operation transition, keep fixed outcomes and unrelated acknowledgements, rerun fault/feature-off tests, then STEP-14/15 only if their consumed state changed.
