# STEP-11 - Native usage remains attributable once

## Outcome

Every known started model, CLI, embedding, retrieval, APC, worker, ROOT, reviewer, correction, and resume call has truthful source-native usage or an explicit incomplete state, with no double counting. This closes [BEHAVIOR-05](../specification/behaviors/BEHAVIOR-05-native-usage-is-attributed-once.md).

## Scope and touchpoints

Add narrow usage contract/store methods in `src/memory_harness/contracts.py` and `store.py`; read source-native receipts from existing harness/provider and adapter surfaces, including STEP-04 child and STEP-07 execution identities. Avoid a separate telemetry or learner ledger.

## Implementation

Key each actual invocation by its native identity and owning objective/decision or maintenance operation, stage, and requested/resolved/native binding. Preserve provider input/output/cache/reasoning/total/cost semantics without summing included components or cumulative intermediate receipts twice. Track a started call with missing usage as incomplete, not zero; accept a late authentic receipt idempotently without rewriting the fixed outcome. Charge APC child once to parent adaptation, and distinguish outer implementation, product-test ROOT, and inner candidate work in native tests. Aggregate only compatible units/rates; include failed reuse plus fallback work in totals.

## Dependencies and integration

Consumes STEP-04 child, STEP-07 worker, and STEP-08 review/outcome identities. Produces a read surface for STEP-15 operator status and STEP-18 native accounting proof.

## Requirement-fit validation

Demonstrate repeated/cumulative receipt handling, two same-count distinct calls, late and absent usage, APC parent-child attribution, correction/resume distinction, and no quality-outcome mutation.

### Fast test suite

Add `tests/local/usage/test_native_usage.py` using realistic native receipt shapes and direct store/replay tests. Run affected existing child/dispatch tests only where receipt parsing changes. Provider-native attribution is finally observed in STEP-18.

## Failure scope and recovery

Unexposed provider counters limit only usage completeness or aggregate claims. Keep valid quality evidence and known invocation identities; never synthesize zero usage.

### Fast lane for revisiting old work

Repair the source parser or invocation join, rerun its focused usage tests, and revisit STEP-15/18 only when their usage inputs changed.
