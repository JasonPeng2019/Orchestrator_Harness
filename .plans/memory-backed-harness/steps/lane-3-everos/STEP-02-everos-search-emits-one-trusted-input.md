# STEP-02 - EverOS search emits one trusted input

## Outcome

Lane 3 queries one isolated EverOS public surface and proves
`make_everos_generated_skill_search_store` emits exactly the STEP-01 stored
skill's current trusted procedure as a downstream-compatible candidate. A
wrong-scope hit and a hit without the exact durable approved/current join emit
nothing.

## Scope and touchpoints

Own `src/memory_harness/everos_adapters.py`,
`src/memory_harness/local_procedure_adapters.py`, and focused EverOS tests.
Use `experience.load_vendored_everos_public_surface`/`EverOSAdapter` with an
isolated root following the repository's documented vendored install path under
`harness/vendor/everos`; do not edit vendored code or machine-global settings.

## Implementation

Invoke STEP-01's helper against a fresh caller-owned store/root, expose that
skill through the accepted public EverOS service in an isolated process, query
it by task text, and pass the raw hit through
`EverOSAdapter.search_skill_candidates`. Construct the product SearchStore with
the real durable store, trusted procedure service, scope, receiver, facts,
route, and current configuration. Query the SearchStore and require one result
whose source kind is `everos_generated_skill`, whose logical/revision IDs and
digest match STEP-01, and whose sanitized payload carries
`EVEROS_MVP_MARKER`. Repeat with a foreign scope and with an unapproved or stale
durable join and require an empty result. Do not replace the public call with a
hand-built candidate.

## Dependencies and integration

Consumes STEP-01's reusable helper but owns and cleans its own temporary root.
Its emitted candidate shape is frozen by the shared contracts
in `PLAN.md` and is consumed by STEP-06 and the joined STEP-12 gate. If the
vendored package cannot be loaded in the intended isolated environment, report
that exact prerequisite; local adapter-double evidence remains useful but does
not satisfy the public-surface claim.

## Requirement-fit validation

Evidence must distinguish a raw EverOS search hit from a trusted product input:
only the exact stable skill/content/source-case/scope candidate rejoined to the
current eligible procedure may be returned.

**Time-crunch repair gate:** repair only a reproduced defect in this normal
stored-skill retrieval/join or a critical trust/scope/privacy invariant. Record
all edge, unsupported, theoretical, exhaustive, or non-normal findings without
repair, blocking, or re-review.

### Fast test suite

Run `EverOSStoredSkillSearchTests` from
`tests/local/mvp/test_everos_mvp_path.py`. When adapter code changes, also run
`tests.local.preparation.test_step04_everos_generated_skill_store` and
`tests.local.preparation.test_step04_everos_generated_skill_call_gate`. The
decisive assertions are one exact eligible result and zero foreign/untrusted
results.

## Failure scope and recovery

A vendored-install failure holds only the actual-public-surface claim and the
enhanced native campaign that consumes it. Preserve STEP-01 and other lanes.

### Fast lane for revisiting old work

Resume from the first failing boundary—vendored load, public query, exact join,
or candidate normalization—rerun the focused class and only the changed adapter
module's existing tests, then resume STEP-12.
