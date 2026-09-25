# STEP-15 - Operator controls expose product truth

## Outcome

An authorized operator can inspect actionable readiness and invoke the remaining setup, prepare/finalize, network-state, pending/recovery, snapshot, and usage behavior through one thin product surface. This completes the operator part of [BEHAVIOR-06](../specification/behaviors/BEHAVIOR-06-setup-and-readiness-preserve-ownership.md) and exposes [BEHAVIOR-07](../specification/behaviors/BEHAVIOR-07-network-mode-claims-match-enforcement.md)/[08](../specification/behaviors/BEHAVIOR-08-snapshots-restore-isolated-recoverable-state.md), without a second controller.

## Scope and touchpoints

Use the existing harness operator entrypoint where it already owns setup/launch, and a narrow `memory_harness` service facade over `runtime.py`, `store.py`, configuration, snapshot, and usage. Choose concrete command names only when an automation consumer needs them; do not add a dashboard or parallel scheduler.

## Implementation

Expose exact build/root, installed composition, compatible schema, service/binding availability, requested/effective feature and network state, pending/uncertain operations, and one next action without secret values. Route setup and native launch to their existing owners; route domain recovery only through exact operation IDs and STEP-09/10 retry rules. Expose snapshot/usage as read or explicitly authorized operations, not implicit task-path effects. A missing service blocks only dependent actions. Document the minimal supported invocation at its real entrypoint.

## Dependencies and integration

Consumes STEP-11 through STEP-14 state surfaces and existing setup/runtime. Produces the operator-facing controls used to preflight STEP-16/17/18 and recover an isolated failed run.

## Requirement-fit validation

Show ready and blocked examples, no credential leak, exact pending/uncertain next action, no duplicate launch/review authority, and supported recovery/snapshot/usage invocation.

### Fast test suite

Add a focused `tests/local/operator/test_readiness.py` selector and affected harness `test_operator_launch.py` cases. Assert the facade reports actual installed payload and operation state; mocked source-template readiness alone cannot decide the claim.

## Failure scope and recovery

An unavailable dependency changes only its readiness/action result. Never mutate live state during a read-only readiness call or hide pending operations to report ready.

### Fast lane for revisiting old work

Repair the specific domain-to-operator projection, rerun its direct tests, and revisit only the proof step whose preflight consumed the changed result.
