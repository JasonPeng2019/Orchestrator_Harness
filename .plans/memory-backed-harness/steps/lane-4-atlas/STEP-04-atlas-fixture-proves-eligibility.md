# STEP-04 - Atlas fixture proves exact eligibility

## Outcome

Lane 4 makes the opt-in live test define two compatible synthetic procedures:
one remains approved/current/eligible for the intended receiver, while the
other is revoked after initial delivery. The same test requires zero delivery
to a wrong receiver and zero delivery of the revoked fixture, while preserving
the eligible fixture for optional handoff.

## Scope and touchpoints

Continue in `tests/live/atlas/test_live_trusted_procedures.py` and the narrow
offline control test. Use the real `TrustedProcedureService`,
`AtlasProcedureAdapter`, Vector Search, and exact-read logic; do not add a local
substitute for the live proof.

## Implementation

Publish both fixtures into STEP-03's UUID-owned collection/index using distinct
logical/revision/publication IDs and distinct search text. Query the intended
receiver and assert the eligible publication is discovered and exact-read as
current, approved, correctly represented, and not revoked. Query a receiver
outside the approval/partition and assert zero delivery. Revoke only the second
fixture and assert it can no longer pass `resolve_atlas`; re-query the retained
fixture and require it still passes. Give the retained procedure an
`ATLAS_MVP_MARKER` instruction unique to its sanitized body.

## Dependencies and integration

Consumes STEP-03. Produces the eligibility facts and retained publication
identity consumed by STEP-05 and later proven against real Atlas in STEP-13.
Offline tests can verify orchestration/identity setup but cannot satisfy the
real Vector Search claim.

## Requirement-fit validation

The live assertions decide four normal claims: eligible discovery, exact
read/current validation, wrong-recipient exclusion, and post-revocation
exclusion without invalidating the other eligible procedure.

**Time-crunch repair gate:** repair only a reproduced failure of those normal
eligibility claims or a critical recipient/trust/privacy invariant. Note remote
provider edge cases and non-normal timing/malformed behavior in
`KNOWN_ISSUES.md` without repair, blocking, or re-review.

### Fast test suite

Extend `AtlasLiveEligibilityControlTests` in
`tests/local/atlas/test_live_fixture_control.py` to exercise the two-fixture
control flow with deterministic fakes of the remote boundary and exact product
records. Run that class plus existing
`tests.local.preparation.test_step04_atlas_search_adapters` if product adapter
code changes. STEP-13 is the decisive real-service proof.

## Failure scope and recovery

A live failure before handoff leaves no accepted manifest and must run the exact
collection cleanup in STEP-05's default/failure path. It holds STEP-13/14, not
Lane 1–3 local evidence.

### Fast lane for revisiting old work

Preserve STEP-03, repair the specific fixture/eligibility assertion, rerun the
offline control class, then only the failed STEP-13 live campaign.
