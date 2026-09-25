# STEP-04 - APC child produces a ROOT-reviewable proposal

Accepted at product commit `a64ebfa9135960ad817752d447588feb5d782d80`. This is historical execution scope, not an open assignment; the resume instructions below describe the now-completed lane.

## Outcome

A near-match template uses a real bounded child launched by the candidate product harness and returns a validated proposal for ROOT; unavailable or invalid adaptation reaches honest fresh planning. This closes [BEHAVIOR-02](../../../memory-backed-harness/specification/behaviors/BEHAVIOR-02-apc-child-produces-a-reviewable-plan.md), not parent execution.

## Scope and touchpoints

The former unaccepted APC lane is recorded by the [active plan](../../../memory-backed-harness/PLAN.md), preserving valid work through rejected commits `cd6c223` and `ab83a70`. The implementation touched `src/memory_harness/harness_bridge.py`, `harness_child.py`, `preparation.py`, `contracts.py`, and `harness/orchestrator_harness/launch.py`; direct tests exist in `tests/local/preparation/test_step04_native_apc_child.py` and affected harness tests. The accepted template shortlist and `references/harness-single` are protected inputs.

## Implementation

Use native scan and the exact rejected review before resuming the same lane; do not bootstrap another writer over it. Complete the product-harness adapter so ROOT supplies the exact parent decision, immutable template revision, trusted bindings, allowed edits, explicit lower-capability `apc_adaptation_binding`, effective absolute deadline, and result contract. Persist/reconcile launch ownership before retry; include queue, CLI, correction, collection, validation, and cleanup in the same bound, with no late unbounded native effect. A missing or altered child card cannot downgrade its scrubbed credential boundary. Validate native result and forbidden edits before offering a proposal. A candidate/reviewed plan stays in review unless ROOT explicitly replans. Direct fill launches no child; missing binding, unsafe ambiguity, timeout, invalid output, or rejection uses fresh planning without claiming adaptation success.

## Dependencies and integration

Consumes accepted template selection and the existing harness child lifecycle. Produces a proposal/fallback disposition and exact child identities for STEP-05 budget, STEP-06 plan acceptance, and STEP-11 usage. ROOT alone accepts the parent plan. One writer owns the current APC lane until its exact state is settled.

## Requirement-fit validation

Show a real candidate-harness child path, bounded proposal validation, no direct provider substitute, two supported explicit binding configurations, and safe fallback/cleanup. The native nested demonstration remains STEP-18; a local harness double does not satisfy that later claim.

### Fast test suite

Run `python -m unittest tests.local.preparation.test_step04_native_apc_child -q` plus the directly affected `harness/orchestrator_harness/tests/test_step04_launch_boundary.py` and `test_step04_lifecycle_integration.py` selectors from the candidate worktree. Assert a valid proposal waits for ROOT, invalid/ambiguous/late paths fall back or remain unresolved without duplicate launch, and actual launch config honors the supplied binding. Rerun only tests affected by changed harness code.

## Failure scope and recovery

If child ownership or cleanup is still ambiguous, block conflicting resource reuse, expose the exact identity, and continue only safe fresh planning. An exited provider without result is a lane-state question, not evidence that the partial commit passed or that all preparation must restart.

### Fast lane for revisiting old work

Keep accepted STEP-04 search/template slices and any valid APC correction. Re-enter at the failing child launch/result/validation branch; rerun the direct APC selection and changed harness selectors, then STEP-05/06 consumers only if their inputs changed.
