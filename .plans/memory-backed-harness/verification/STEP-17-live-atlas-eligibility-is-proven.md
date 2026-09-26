# STEP-17 - Live Atlas eligibility is proven

## Outcome

The pinned candidate observes real scoped Atlas Vector Search and exact eligibility/current/revoked behavior on disposable synthetic records, leaving an owned eligible fixture for STEP-18. This is the live-service part of [BEHAVIOR-09](../specification/behaviors/BEHAVIOR-09-pinned-candidate-proves-the-product-path.md).

This required live normal-path proof and its scope/eligibility/privacy invariants are not relaxed. Peripheral or unsupported Atlas edge findings are classified under the [normal-operation acceptance policy](../NORMAL_OPERATION_ACCEPTANCE.md) and recorded in [KNOWN_ISSUES.md](../KNOWN_ISSUES.md) without expanding the live campaign.

## Scope and touchpoints

Use `tests/live/atlas/test_live_trusted_procedures.py`, the accepted Atlas adapter and procedure services, a dedicated `MEMORY_HARNESS_ATLAS_LIVE_DATABASE`, and the actual required index. Check ignored `.secrets/creds/` before declaring credentials absent; never copy values into plan, card, log, or output.

## Implementation

Preflight the STEP-16 pin, scoped namespace/index permissions, network profile, Atlas URI, live opt-in, and cleanup owner. Load credentials only into the authorized process. Seed synthetic approved/current and revoked/stale procedure cases, exercise actual Vector Search and exact post-read eligibility, then change/revoke and confirm old hits cannot pass. Keep one eligible synthetic fixture in the owned partition for STEP-18; its owner cleans the partition once after the native campaign, or when that campaign is blocked/abandoned. If cleanup is uncertain, expose the exact partition instead of broad deletion. Preserve the same pin for STEP-18.

## Dependencies and integration

Consumes STEP-16's candidate and STEP-13 network truth. Produces a live eligible Atlas fixture/evidence for STEP-18. Missing service/index/permission readiness holds only this live claim and any native enhanced case that depends on it.

## Requirement-fit validation

Observe the actual remote Vector Search, scope isolation, current eligibility, and stale/revoked rejection for the disposable supported fixture. Record the exact fixture owner and cleanup point; a local adapter double cannot satisfy this outcome. Do not add exhaustive remote malformed-input, timing-window, or provider-edge exploration after this required behavior passes; document any such confirmed residual instead.

### Fast test suite

Reuse STEP-16's local Atlas selector results on the same pin; rerun them only if their consumed inputs changed or those results are unreliable. The real proof is the repository's opt-in `tests.live.atlas.test_live_trusted_procedures` selection with the isolated live database and verified index.

## Failure scope and recovery

A service outage or missing index blocks only the live operation and dependent enhanced native claim. A repair-required eligibility, scope, privacy, or cleanup defect returns to its owner; a contained non-normal residual is documented without another live repair loop. If STEP-18 cannot proceed immediately, the named owner may leave the exact synthetic partition identified and blocked from conflicting reuse only as a temporary recovery state. Final acceptance requires verified cleanup of that exact owned partition unless the user explicitly authorizes retention. Never use production data or substitute an unscoped database.

### Fast lane for revisiting old work

Repair the specific adapter/index/eligibility seam and rerun the affected live fixture. Reuse local candidate results unless that selector's inputs changed or its prior result is unreliable; repin only when candidate bytes change.
