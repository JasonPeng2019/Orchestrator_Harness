# STEP-05 - Atlas handoff is owned and cleanable

## Outcome

Lane 4 adds explicit campaign control to the live test: normal/default and all
failure paths drop the exact UUID-owned collection; an explicit handoff request
retains exactly the one eligible STEP-04 fixture only after every live assertion
passes and writes the nonsecret manifest defined in `PLAN.md`.

## Scope and touchpoints

Own only the live test and
`tests/local/atlas/test_live_fixture_control.py`. Use an explicit manifest-path
environment input as the handoff opt-in; its absence means cleanup. This is
test/campaign control, not a new product command, ledger, or deployment setting.

## Implementation

Keep collection ownership local to the test's fresh UUID. In `finally`, drop the
collection unless a boolean set only after the last STEP-04 assertion confirms a
valid manifest was atomically written to the explicit path. The manifest contains
only the exact nonsecret fields in `PLAN.md`; reject a pre-existing path or write
failure by falling back to cleanup. Close client/store/temp resources in both
modes. Do not implement cleanup by database prefix, process name, or broad query.

## Dependencies and integration

Consumes STEP-04. Produces the reviewed Lane 4 commit and the manifest contract
used by STEP-13–15. Master, not Lane 4's implementation worker, supplies
credentials, requests retention, and performs final cleanup.

## Requirement-fit validation

Offline tests must simulate success, assertion failure, manifest failure, and
default execution. Only successful explicit handoff retains; every other path
drops exactly once. The manifest must omit URI/key/control credentials and name
the cleanup owner/target completely.

**Time-crunch repair gate:** repair only a reproduced normal handoff/default
cleanup defect or a critical secret/ownership/broad-deletion invariant. Document
cosmetic manifest issues and non-normal provider edges without correction,
blocking, or re-review.

### Fast test suite

Run `AtlasLiveHandoffControlTests` in
`tests/local/atlas/test_live_fixture_control.py`. Its decisive assertions are
retain-only-after-success, exact single drop otherwise, and nonsecret complete
manifest. Rerun STEP-03/04 classes only when their consumed fields changed.

## Failure scope and recovery

If manifest status is uncertain, assume the exact collection may remain, expose
its known UUID target, and let Master reconcile that target before reuse. Never
start a second live handoff against the same target.

### Fast lane for revisiting old work

Retain passing representation/eligibility setup, repair only campaign control,
rerun the handoff class, and rerun STEP-13 only if a live collection was already
created under the changed logic.
