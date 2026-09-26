# STEP-06 - Standard preparation selects both inputs

## Outcome

Lane 1 proves one bounded Standard `PreparationService.prepare` call queries
the accepted EverOS and Atlas SearchStore shapes together and selects both
distinct trusted procedure candidates into one preparation trace without
deduplicating one away.

## Scope and touchpoints

Own a new focused module `tests/local/mvp/test_coherent_memory_path.py` and, only
for a reproduced normal-path defect, `src/memory_harness/preparation.py` or
`search.py`. Import the real `make_everos_generated_skill_search_store` and
`make_atlas_search_store` factories with deterministic public-boundary doubles;
do not edit either adapter in this lane.

## Implementation

Build one valid task card, one accepted ordinary plan, captured Standard config
with generated-skill use and Atlas shared retrieval enabled, a temporary
MemoryStore, and explicit receiver/facts/route. Feed two independently eligible
procedures with different logical/revision IDs and their unique markers through
the real adapter factories. Run bounded preparation once. Require both stores to
be queried, both candidates to be selected, and the trace to retain each exact
source kind, ID, digest, receiver/scope provenance, freshness, and
`plan_affecting` meaning. Do not weaken diversity/deduplication globally merely
to force two results; the distinct trusted identities must naturally survive.

## Dependencies and integration

Consumes the stable candidate contracts in `PLAN.md`; it may implement in
parallel with STEP-01–05. STEP-12's joined candidate later substitutes the
actual Lane 3/4 implementations and decides compatibility. Produces the exact
selected-item fixture consumed by STEP-07.

## Requirement-fit validation

One candidate, a raw untrusted hit, or two candidates collapsed to one fails the
normal coherent path. The trace must show two selected plan-affecting sources
without exposing raw approval material.

**Time-crunch repair gate:** repair only a reproduced failure of this normal
two-source Standard preparation or a critical trust/privacy/identity invariant.
Document edge ranking, extra-candidate, unsupported-route, theoretical timing,
and other non-normal findings without correction, blocking, or re-review.

### Fast test suite

Add and run `CoherentPreparationTests` from
`tests/local/mvp/test_coherent_memory_path.py`. Its decisive test invokes the
real service/factories and asserts both exact selected trace entries. If product
preparation/search code changes, also run
`tests.local.preparation.test_bounded_preparation` and the two existing STEP-04
adapter modules. Candidate-shape changes invalidate this class and STEP-07.

## Failure scope and recovery

A mismatch with one adapter shape holds only that input and STEP-07/12; the
other provider lane remains valid. Assign any adapter correction to Lane 3 or 4
rather than crossing write ownership.

### Fast lane for revisiting old work

Retain the valid adapter fixture and trace assertions, repair only the failing
normalization/selection seam, rerun this class and then STEP-07; do not replay
provider-internal tests whose inputs did not change.
