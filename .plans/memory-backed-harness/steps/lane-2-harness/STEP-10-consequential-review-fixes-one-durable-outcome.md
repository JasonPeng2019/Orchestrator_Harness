# STEP-10 - Consequential review fixes one durable outcome

## Outcome

Lane 2 proves the enhanced worker result from STEP-09 reaches the existing
separate consequential reviewer, and the exact accepted/rejected native terminal
evidence records one immutable durable outcome with minimal requested/resolved/
native invocation attribution.

## Scope and touchpoints

Own the existing product `review.py`, `terminal_evidence.py`, native receipt
tests, and focused terminal-outcome tests. Shared outcome/store contracts remain
Lane 1-owned; request reassignment if a provider defect is reproduced there.
Do not implement complete usage accounting or a new review record.

## Implementation

Use the real terminal evidence bundle: exact task card, accepted plan, final
context, dispatch observation, worker result containing both markers, and
separate review result. Validate it before calling the accepted outcome recording
path. Assert one durable outcome links the same decision/plan/run/evidence digest
and that quality cannot be fabricated by forced acceptance. Capture only the
minimal invocation fields already supported; explicit incompleteness is allowed
where the current contract permits it.

## Dependencies and integration

Consumes STEP-09. Produces the reviewed terminal contract consumed by STEP-11's
inner cleanup, STEP-12 integration, and STEP-14 native proof.

## Requirement-fit validation

The reviewer must be a distinct consequential observation, the outcome must be
durable and exact-linked, and duplicate/conflicting terminal writes must not
change fixed quality.

**Time-crunch repair gate:** repair only a reproduced normal review/outcome defect,
ordinary compatibility problem, or critical fabricated-success/durability/
identity invariant. Document full-accounting gaps, extra role tiers, and edge
review diagnostics without correction, blocking, or re-review.

### Fast test suite

Run the focused enhanced native-review test in
`orchestrator_harness.tests.test_step08_native_review_evidence` and the directly
affected cases in `tests.local.contracts.test_terminal_outcome`. Add one marker-
bound terminal test if no current test proves the exact final context/result is
the reviewed evidence. Rerun only when terminal/review inputs change.

## Failure scope and recovery

An invalid review holds outcome acceptance, not the already-observed worker run.
Retain the exact evidence and correct/review it through the supported path; do
not relaunch the worker unless its result itself is invalid.

### Fast lane for revisiting old work

Resume from terminal evidence validation or durable outcome write, retain the
STEP-09 run/result, rerun the focused review/outcome cases, then STEP-11/14.
