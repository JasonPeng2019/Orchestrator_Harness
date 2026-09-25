# STEP-07 - Harness dispatch reconciles one invocation

## Outcome

The existing product harness launches only the exact accepted, finalized plan and records whether its invocation happened, remained ambiguous, or failed. This is the launch half of [BEHAVIOR-03](../specification/behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md).

## Scope and touchpoints

Wire `src/memory_harness/runtime.py` `dispatch`/`record_dispatch_intent`/`reconcile_ambiguous_dispatch` to `harness/orchestrator_harness/memory_handoff.py` and existing `bootstrap.py`, `resume.py`, `launch.py`, and review lifecycle. Use current harness tests `test_memory_handoff.py`, `test_step04_launch_boundary.py`, and `test_step04_lifecycle_integration.py`.

## Implementation

Validate the exact accepted plan and finalized context at the last launch boundary; preserve legacy task-card behavior when memory is absent. Record one dispatch intent before an effectful launch and join the observed native run by task/plan/context identity. A lost acknowledgement triggers exact harness lookup, not a second blind launch; unresolved ambiguity stays visible. Scrub product control-plane credentials from actual worker prompt, environment, and tools without inventing a secret manager. Feature-off/all-off must reach the launch path. Do not add a scheduler or second review decision.

## Dependencies and integration

Consumes STEP-06's final envelope. Produces exact native execution identity for STEP-08 terminal outcome and STEP-11 usage. Harness-owned lifecycle remains authoritative for launch, review, and cleanup.

## Requirement-fit validation

Prove the difference between finalized context and observed invocation, no dispatch of proposed/wrong-plan context, one launch after ambiguous acknowledgement, legacy path preservation, and actual credential exclusion.

### Fast test suite

Run `python -m unittest tests.local.contracts.test_runtime_dispatch -q` from the product root and the three directly affected harness test files with their documented runner. Add a focused ambiguous-acknowledgement test if absent. Changed launch/envelope/credential inputs invalidate this selection; no full harness suite per edit.

## Failure scope and recovery

Unknown native ownership blocks conflicting relaunch or reuse of that lane. A missing required plan/context blocks enhanced launch but does not mutate accepted state or break unrelated legacy lanes.

### Fast lane for revisiting old work

Inspect the exact intent/native receipt pair, repair only that join, rerun direct dispatch and harness-launch tests, and revisit STEP-08 only if execution identity changed.
