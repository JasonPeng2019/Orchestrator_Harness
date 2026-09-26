# STEP-16 - Pinned candidate passes local checks

## Outcome

One integrated candidate passes a curated local gate for normal product operation and affected critical invariants, plus the isolated install/import check where packaging inputs changed. This is the local-evidence part of [BEHAVIOR-09](../specification/behaviors/BEHAVIOR-09-pinned-candidate-proves-the-product-path.md), not a substitute for live or native evidence. Confirmed non-normal residuals are classified under the [normal-operation acceptance policy](../NORMAL_OPERATION_ACCEPTANCE.md) and recorded in [KNOWN_ISSUES.md](../KNOWN_ISSUES.md).

## Scope and touchpoints

Pin the integrated product source/configuration produced by STEP-04 through STEP-15. Use the repository's existing `tests/local` unittest layout, directly affected `harness/orchestrator_harness/tests`, and its documented package build/install path. Do not run vendored test trees or benchmarks.

## Implementation

Before the wave, confirm the candidate revision, installed entrypoint, explicit APC binding, role map, fixture inputs, and relevant local dependencies. Run a curated integrated gate covering one ideal fixed-strategy path, ordinary legacy/all-off preservation, credible recovery at changed seams, and the critical invariants touched by STEP-05–15. Run affected harness tests for changed harness seams. If packaging, exports, or runtime dependencies changed, build/install into an isolated environment and import the product there. Run the full relevant local product suite once only as best-effort diagnostics when time permits; classify every failure instead of requiring all non-normal cases to pass. A fix changes the pinned candidate: rerun only checks whose source/config/environment inputs changed, then carry the new pin to STEP-17/18.

## Dependencies and integration

Consumes the integrated implementation outcomes. Produces local and install evidence tied to one candidate for live Atlas and nested native operations; no release claim is made from a passing outer-only suite.

## Requirement-fit validation

The curated gate must decide the supported deterministic contracts, normal launch/setup behavior, affected compatibility, credible recovery, and critical invariants. Isolated install must prove packaging only when its inputs changed. A failure that breaks one of those claims requires repair; a contained non-normal failure is documented and does not hold the candidate. Report actual skips and failures; unavailable evidence is not a pass, and a report typo cannot overturn passing behavior.

### Fast test suite

Build the curated command from the directly affected STEP selectors and representative joined normal-path, legacy/all-off, recovery, and critical-invariant modules. The broad diagnostic command is `python -m unittest discover -s tests/local -t . -p "test_*.py"` from the candidate root; its documented-only edge failures do not replace the curated gate. Run changed harness test selectors with their existing unittest runner. On a narrow correction, use that STEP's fast selection first, then rerun only the affected integrated checks. Do not rerun the whole suite just to refresh a summary.

## Failure scope and recovery

A repair-required shared-contract failure returns to its owning implementation step. A packaging failure blocks the installed-candidate claim when packaging inputs changed; local source-test evidence whose inputs are unchanged remains valid. Documented-only findings enter the known-issues register without a correction or re-review loop.

### Fast lane for revisiting old work

Retain unaffected passing selections, repair the failing owner seam, and repin only when consumed candidate bytes change. Rerun the direct fast suite plus invalidated combined checks, not every historical step.
