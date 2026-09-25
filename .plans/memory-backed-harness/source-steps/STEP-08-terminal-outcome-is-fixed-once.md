# STEP-08 - Terminal outcome is fixed once

## Outcome

Exact linked native review and acceptance evidence fixes one immutable local terminal outcome; missing evidence remains missing and conflicting replay is visible. This is the terminal-state portion of [BEHAVIOR-04](../specification/behaviors/BEHAVIOR-04-terminal-outcome-and-effects-reconcile.md).

## Scope and touchpoints

Extend `src/memory_harness/runtime.py` `record_outcome`, `store.py` outcome transaction, and `contracts.py` validation through the existing `harness/orchestrator_harness/review.py` completion seam. Preserve accepted STEP-01 outcome records and reviewed-evidence provenance.

## Implementation

Resolve task, objective, decision, accepted plan, observed dispatch/run, result, review, and acceptance by exact identity. Distinguish PASS, FAIL, BLOCKED, genuine terminal unknown, forced/exceptional acceptance, and no terminal observation. Refuse wrong-identity or APC-child evidence for the parent. Make fixation transactional: identical replay returns the same outcome; contradictory replay reports integrity conflict; legitimate correction uses linked supersession, never overwrite. Keep follow-on effect and usage state outside the fixed quality outcome so their outages cannot reverse harness acceptance.

## Dependencies and integration

Consumes STEP-07's observed invocation identity and existing native review/acceptance. Produces immutable local outcome identity for STEP-09/10 effects, STEP-11 usage linkage, and operator recovery.

## Requirement-fit validation

Exercise exact PASS/FAIL/BLOCKED joins, absent or wrong-run evidence, replay/conflict, crash before/after local fixation, and separation of quality from optional effects.

### Fast test suite

Extend `tests/local/contracts/test_runtime_dispatch.py` or add a focused `tests/local/outcomes/test_terminal_outcome.py` selector for those joins and replay; run that selector plus the directly affected harness review tests. The native campaign in STEP-18 later proves the real completion boundary.

## Failure scope and recovery

An identity conflict blocks only the affected outcome and its effects. Preserve the existing fixed row and native evidence; do not retry by assigning a new outcome ID.

### Fast lane for revisiting old work

Re-enter the exact join or transaction failure, retain valid dispatch evidence, rerun focused outcome tests and STEP-09/10 only when their consumed outcome identity changed.
