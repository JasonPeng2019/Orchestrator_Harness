# STEP-08 - All-off harness lifecycle stays inherited

## Outcome

Lane 2 proves a valid all-features-off task follows the ordinary inherited
product-harness lifecycle through bootstrap, worker completion, consequential
review, and close without creating memory state/envelopes or calling EverOS,
Atlas, or APC. This is focused preservation, not a separate full native
campaign.

## Scope and touchpoints

Own focused tests in `harness/orchestrator_harness/tests/`, principally
`test_memory_handoff.py` and the smallest existing bootstrap/review/close tests.
Change product harness code only for a reproduced all-off regression. Do not add
a new runner or optional-service abstraction.

## Implementation

Extend the existing all-off task fixture to the smallest existing in-process
harness lifecycle that observes bootstrap, worker terminal result, review, and
close. Patch/spies belong only at the optional provider/APC boundaries and must
assert zero calls; do not mock away the normal harness state transitions being
claimed. Assert no memory SQLite/envelope is created and the ordinary result and
review are still retained.

## Dependencies and integration

Consumes the accepted legacy/all-off handoff at `4263abf` and may run in
parallel with all provider/context work. Produces the focused preservation
evidence consumed by STEP-12. It is independent of Atlas readiness.

## Requirement-fit validation

Both halves matter: the harness lifecycle completes normally, and every optional
memory/APC boundary remains zero-call. Merely returning `None` from preparation
without observing lifecycle completion is insufficient.

**Time-crunch repair gate:** repair only a reproduced all-off normal-lifecycle
regression, ordinary compatibility defect, or critical unintended optional
call/state mutation. Document edge teardown diagnostics and unsupported modes
without correction, blocking, or re-review.

### Fast test suite

Add one focused all-off lifecycle test to the existing harness test module that
owns the chosen bootstrap/review path, and run that exact test plus
`MemoryHandoffSeamTests.test_all_off_bypasses_memory_and_learned_mode_fails_before_state`.
Run adjacent module tests only if shared harness logic changes.

## Failure scope and recovery

An all-off failure blocks STEP-08 and final MVP acceptance but not enhanced
provider implementation. Repair the ordinary harness seam; do not disable
enhanced code globally to obtain a pass.

### Fast lane for revisiting old work

Retain all enhanced work and any passing ordinary phases, repair the first
failing all-off lifecycle transition, and rerun only this focused test and its
directly changed harness module.
