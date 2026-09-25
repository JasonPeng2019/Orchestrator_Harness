# STEP-06 - Final context binds one accepted plan

## Outcome

ROOT receives a bounded, privacy-safe final context tied to the exact accepted task/plan/base; it is ready for dispatch but does not claim an invocation. This is the context half of [BEHAVIOR-03](../specification/behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md).

## Scope and touchpoints

Complete the existing `src/memory_harness/context.py` finalizer and validation, its `preparation.py`/`runtime.py` callers, `privacy.py`, and the final-context envelope in `harness/orchestrator_harness/memory_handoff.py`. `tests/local/preparation/test_final_context_dispatch.py` already covers part of this seam.

## Implementation

Require ROOT acceptance of an exact plan revision before finalization. Recheck plan-affecting eligibility and source freshness under the remaining bound; a late revocation or incompatible change blocks or triggers explicit ROOT replan, never silently substitutes memory. Pack mandatory task/plan/base/route and trusted security meaning before optional content, dropping optional items as whole units if needed; mandatory overflow is an explicit failure. Sanitize and authorize every recipient before rendering; all-off carries no optional memory context. Bind a stable finalized-context identity to the accepted plan and task, with no launch success claim.

## Dependencies and integration

Consumes STEP-05 prepared state and an exact ROOT-accepted plan. Produces the immutable handoff consumed by STEP-07's actual harness launch; context validation remains in the domain package, lifecycle remains in the harness.

## Requirement-fit validation

Show accepted-vs-proposed plan separation, mandatory overflow, optional trimming, recipient privacy, stale/revoked guidance handling, and all-off omission. A valid finalized envelope is necessary but not evidence of launch.

### Fast test suite

Run `python -m unittest tests.local.preparation.test_final_context_dispatch -q` and affected `harness/orchestrator_harness/tests/test_memory_handoff.py` cases. Add focused acceptance/freshness/privacy assertions where existing tests do not decide the claim. Inputs are plan state, selected guidance, privacy policy, and context limit.

## Failure scope and recovery

An unsafe or overlarge mandatory context blocks only enhanced dispatch for that plan; retain the accepted plan and exact reason. A changed plan revision requires a new finalized envelope.

### Fast lane for revisiting old work

Re-enter the finalizer or envelope validator, retain valid preparation and acceptance, rerun direct context tests and STEP-07's handoff consumer if the envelope changed.
