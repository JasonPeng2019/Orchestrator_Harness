# STEP-16 - Pinned candidate passes local checks

## Outcome

One integrated candidate passes the relevant local product suite, affected harness checks, and isolated install/import check where packaging inputs changed. This is the local-evidence part of [BEHAVIOR-09](../specification/behaviors/BEHAVIOR-09-pinned-candidate-proves-the-product-path.md), not a substitute for live or native evidence.

## Scope and touchpoints

Pin the integrated product source/configuration produced by STEP-04 through STEP-15. Use the repository's existing `tests/local` unittest layout, directly affected `harness/orchestrator_harness/tests`, and its documented package build/install path. Do not run vendored test trees or benchmarks.

## Implementation

Before the wave, confirm the candidate revision, installed entrypoint, explicit APC binding, role map, fixture inputs, and relevant local dependencies. Run the full relevant local product suite once after integration; run affected harness tests for changed harness seams. If packaging, exports, or runtime dependencies changed, build/install into an isolated environment and import the product there. Separate actual failures from optional skipped live tests. A fix changes the pinned candidate: rerun only checks whose source/config/environment inputs changed, then carry the new pin to STEP-17/18.

## Dependencies and integration

Consumes the integrated implementation outcomes. Produces local and install evidence tied to one candidate for live Atlas and nested native operations; no release claim is made from a passing outer-only suite.

## Requirement-fit validation

The full relevant local suite must decide deterministic contracts and fault branches, affected harness tests must decide launch/setup changes, and isolated install must prove packaging only when its inputs changed. Report actual skips and failures; a report typo cannot overturn passing behavior.

### Fast test suite

The direct command is `python -m unittest discover -s tests/local -t . -p "test_*.py"` from the candidate root; run changed harness test selectors with their existing unittest runner. On a narrow correction, use that STEP's fast selection first, then rerun only the affected integrated checks. Do not rerun the whole suite just to refresh a summary.

## Failure scope and recovery

A genuine shared-contract failure returns to its owning implementation step. A packaging failure blocks the installed-candidate claim; local source-test evidence whose inputs are unchanged remains valid.

### Fast lane for revisiting old work

Retain unaffected passing selections, repair the failing owner seam, and repin only when consumed candidate bytes change. Rerun the direct fast suite plus invalidated combined checks, not every historical step.
