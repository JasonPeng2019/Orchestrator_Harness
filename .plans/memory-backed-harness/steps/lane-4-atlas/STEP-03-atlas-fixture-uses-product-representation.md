# STEP-03 - Atlas fixture uses the product representation

## Outcome

Lane 4 converts the disposable live Atlas fixture and its single UUID-owned
index from the incompatible 3-dimensional test representation to the product
representation: `local-token-overlap/v1`, 512 dimensions, cosine metric, and
sanitizer `v1`.

## Scope and touchpoints

Own `tests/live/atlas/test_live_trusted_procedures.py` and one narrow offline
test under `tests/local/atlas/`. Product `atlas.py`, `atlas_adapters.py`, and
`procedures.py` change only if the offline test reproduces a normal-path product
defect. Never touch credential files.

## Implementation

Replace the three-count embedding helper with a deterministic 512-dimensional
token-overlap embedding compatible with the product identity. Both document and
query vectors must use one helper and have exactly 512 finite numeric entries.
Create the collection's sole vector index with `dimensions=512` and retain the
existing filter fields. Build every synthetic fixture in that collection with
the same model/dimension/metric/sanitizer identity; never mix the old 3-D
records with the new index.

## Dependencies and integration

Consumes the accepted representation identity in `src/memory_harness/atlas.py`.
Produces the common representation builder used by STEP-04 and the manifest in
STEP-05. It does not call Atlas locally.

## Requirement-fit validation

The offline check must prove deterministic document/query vectors, exact length
512, the pinned identity fields, and index creation arguments. A 3-D fixture or
identity mismatch must fail before any remote mutation.

**Time-crunch repair gate:** repair only a reproduced defect in the normal
product-compatible representation or a critical integrity/privacy invariant.
Document non-normal provider edges, malformed vectors, theoretical cases, and
unrelated findings without correction, blocking, or re-review.

### Fast test suite

Add `AtlasLiveRepresentationTests` in
`tests/local/atlas/test_live_fixture_control.py` and run that class. It imports
the live-test helper without enabling the live test and asserts the identity,
vector length/content stability, and index arguments. Rerun it when embedding or
representation fields change.

## Failure scope and recovery

An optional Atlas dependency missing from the local interpreter holds only
helper import/execution; use the repository's intended test environment rather
than weakening the product identity. No remote cleanup is needed before STEP-13.

### Fast lane for revisiting old work

Keep any passing deterministic-vector assertions, repair only the mismatched
representation/index field, rerun the focused class, then STEP-04/05 if they
consumed that field.
