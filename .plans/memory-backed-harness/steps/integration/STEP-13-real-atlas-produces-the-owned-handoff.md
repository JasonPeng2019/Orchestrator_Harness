# STEP-13 - Real Atlas produces the owned handoff

## Outcome

Master runs the pinned STEP-12 candidate's opt-in live Atlas test against one
isolated synthetic database/UUID collection, observes real 512-dimensional
Vector Search and exact eligibility behavior, and receives one complete
nonsecret manifest for the still-eligible retained fixture.

## Scope and touchpoints

Use ignored `.secrets/creds/` only to populate the authorized process's
`MEMORY_HARNESS_ATLAS_URI`; set a dedicated
`MEMORY_HARNESS_ATLAS_LIVE_DATABASE`, `MEMORY_HARNESS_RUN_LIVE_ATLAS=1`, and the
explicit manifest-path handoff input from STEP-05. Never print or persist
credential values. Master is the only live-operation and cleanup owner.

## Implementation

Preflight the pinned revision, optional dependencies, URI/database presence,
network reachability, collection/index permissions, empty fresh manifest path,
and exact cleanup target construction before mutation. Run only
`tests.live.atlas.test_live_trusted_procedures`. Require the live observations
from STEP-04 and the STEP-05 success manifest. Validate the manifest's
representation identity, receiver/scope, publication/logical/revision IDs,
query/route/facts, marker, and cleanup owner; reject secrets or missing fields.
Do not reuse a stale manifest or existing collection.

## Dependencies and integration

Consumes STEP-12 and STEP-05's campaign control. Produces the real live evidence
and retained fixture consumed by STEP-14. STEP-15 owns cleanup whether this step
succeeds or aborts after remote creation.

## Requirement-fit validation

Only actual remote Vector Search plus exact readback establishes the live claim.
Require eligible delivery, wrong-recipient zero delivery, revoked zero delivery,
and retained eligible re-delivery on the exact candidate pin.

**Time-crunch repair gate:** repair only a reproduced normal Atlas eligibility/
handoff defect or critical recipient, trust, privacy, representation, or cleanup
invariant. Document peripheral provider edges and non-normal behavior without
correction, blocking, or re-review. Missing service/access readiness leaves this
claim open; it is not a product failure or pass.

### Fast test suite

Before live mutation, rerun only STEP-03–05 offline classes if their bytes or
environment inputs changed. The decisive command is the repository's opt-in
`tests.live.atlas.test_live_trusted_procedures` selection with the isolated live
variables. Do not broaden to other live tests.

## Failure scope and recovery

Any failure after collection creation transfers exact cleanup responsibility to
STEP-15. Expose the exact database/collection/index known from the run; never
drop a database or prefix-matched resources. STEP-12 remains valid.

### Fast lane for revisiting old work

Repair only the failed representation, eligibility, manifest, or environment
precondition; rerun its offline class when code changed and then this one live
test. Reuse STEP-12 if candidate bytes are unchanged.
