# STEP-01 - EverOS stored-skill lineage is authentic

## Outcome

Lane 3 produces one isolated synthetic stored skill whose lineage is created
through the accepted product services: reviewed source case IDs and scope lead
to a durable generated-skill candidate, source approval, generated procedure,
procedure approval, and current designation for the exact receiver. Its
sanitized content carries `EVEROS_MVP_MARKER` as the unique downstream
material-use marker. It also produces one reusable verification helper that can
stage the same lineage into a caller-supplied temporary MemoryStore and EverOS
root for STEP-02 and STEP-14.

## Scope and touchpoints

Use `experience.ReviewedExperienceService`, `MemoryStore` generated-skill APIs,
and `procedures.TrustedProcedureService.procedure_from_generated_skill` without
changing their public contracts. Lane 3 owns changes only in
`src/memory_harness/experience.py` and focused tests under
`tests/local/mvp/` or existing `tests/local/experience/`. Put the shared
verification-only builder in `tests/local/mvp/everos_fixture.py`; it accepts
caller-owned paths/store/scope and returns existing product IDs/objects rather
than writing a manifest or inventing another persistence format. `store.py`,
`procedures.py`, and vendored EverOS are protected provider surfaces; a defect
there returns to Master for ownership rather than being patched cross-lane.

## Implementation

Build a temporary memory root and exact `ExperienceScope`. Create one synthetic
reviewed case, then use the accepted generation/approval calls to persist a
stored skill with stable ID, sanitized content containing the marker, and exact
source-case provenance. Convert that candidate through the accepted procedure
service, approve it for one receiver, designate it current in one partition,
and read every record back by product API. Implement the helper by composing
these same accepted calls so a later caller can stage a fresh root
deterministically. Do not insert SQL rows or fabricate a SearchStore candidate
directly. Keep existing stored skills and reviewed cases unchanged.

## Dependencies and integration

Consumes the accepted persistence and trust contracts at `4263abf`. Produces a
reusable fixture-builder helper for STEP-02 and STEP-14; it retains no temporary
root after its caller cleans up. No runtime/global EverOS installation is needed
until STEP-02 queries the public surface.

## Requirement-fit validation

Assert the read-back stable skill ID, sanitized content digest, exact scope,
source-case IDs, source approval, generated procedure origin, procedure
approval recipients, partition, and current revision all agree. A missing or
mismatched link must fail instead of becoming trusted guidance.

**Time-crunch repair gate:** repair only a reproduced defect in this normal
stored-skill lineage or a critical trust/privacy/durability invariant. Document
edge, malformed, unsupported, theoretical, or non-normal findings in
`KNOWN_ISSUES.md`; they do not block, launch correction, or require re-review.

### Fast test suite

Add `EverOSStoredSkillLineageTests` in
`tests/local/mvp/test_everos_mvp_path.py` and run that class with `unittest`.
Its decisive assertions are the complete API-read-back chain above and a second
caller-supplied root receiving an equivalent independently staged lineage from
the helper. Also run the
existing `tests.local.experience.test_generated_trust` only if production
experience code changes. A change to lineage construction or trust records
invalidates this evidence.

## Failure scope and recovery

An unavailable vendored runtime does not affect this local durable lineage;
do not block STEP-01 on it. A provider-surface defect holds STEP-01/02 and is
reassigned by Master; other lanes continue.

### Fast lane for revisiting old work

Retain the helper and any passing read-back links, repair the
first broken product API boundary, rerun the focused class and only STEP-02 if it
already consumed the changed lineage.
