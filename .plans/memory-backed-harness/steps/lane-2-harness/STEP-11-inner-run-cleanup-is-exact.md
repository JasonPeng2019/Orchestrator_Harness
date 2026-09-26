# STEP-11 - Inner-run cleanup is exact

## Outcome

Lane 2 proves the product harness retires the exact enhanced inner lane/run after
STEP-10, leaves no live controller/worker ownership or unresolved lease for that
identity, and does not terminate unrelated processes or worktrees.

## Scope and touchpoints

Own existing controller/review close and process-identity cleanup code/tests under
`harness/orchestrator_harness`. Do not add process-name-wide termination, delete
worktrees, or alter the frozen outer harness.

## Implementation

Drive the existing close/retirement path with one exact lane, run, PID creation
identity, and retained terminal evidence. Assert the matching process tree and
lease retire, the lane reaches terminal/closed state, and an unrelated synthetic
lane/process identity is untouched. Preserve dirty worktrees and result evidence.
The later live campaign uses this same cleanup path; this step implements/tests
it without claiming a real native process was run.

## Dependencies and integration

Consumes STEP-10's terminal identity. Produces the cleanup seam consumed by
STEP-12 integration and STEP-14 native execution. Atlas cleanup is separate in
STEP-15.

## Requirement-fit validation

Exact owned retirement and unrelated-owner preservation are both decisive.
Missing cleanup evidence remains unresolved rather than being inferred from a
quiet process listing.

**Time-crunch repair gate:** repair only a reproduced normal inner cleanup defect
or critical ownership/broad-termination/duplicate-run invariant. Document edge
diagnostics and unsupported process environments without correction, blocking,
or re-review.

### Fast test suite

Run the directly affected cases in
`orchestrator_harness.tests.test_review_manager_close` and existing process/
controller cleanup tests; add one exact-identity/unrelated-owner preservation
case if absent. Rerun only tests whose cleanup inputs change.

## Failure scope and recovery

On uncertain cleanup, quarantine the exact lane/run and reconcile its PID creation
identity and lease. Hold only reuse of that lane/resource and STEP-14; do not stop
other lanes or clean by broad name.

### Fast lane for revisiting old work

Retain STEP-09/10 evidence, repair the exact retirement seam, rerun the focused
cleanup tests, then only STEP-14 if its live cleanup consumed the changed code.
