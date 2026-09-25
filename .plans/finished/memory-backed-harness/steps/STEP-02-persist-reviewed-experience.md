# STEP-02 - Reviewed execution experience persists and remains trustworthy

> Completed and accepted. This is a historical plan record, not active work.

## Outcome

Accepted executions, failures, disproved hypotheses, and their evidence survive
restart and retirement as reviewed trajectories. The product can send those
trajectories through a real EverOS adapter to create searchable cases and skill
candidates while preserving exact provenance. Generated guidance remains evidence
until explicitly approved; curated guidance is selected explicitly.

## Scope and touchpoints

Extend `src/memory_harness/experience.py`, the shared records in `contracts.py`,
and transactional storage in `store.py`. Add the smallest adapter around the
vendored EverOS public surfaces rooted at `harness/vendor/everos/src/everos/`,
notably `service/memorize.py`, `service/search.py`, and the agent case/skill
models and recall paths. Add focused tests under `tests/local/experience/` and
dependency/package configuration in `pyproject.toml` when the real adapter needs
it. Modify vendored EverOS only when a product adapter test demonstrates that its
public contract cannot provide a required behavior.

## Implementation

- Convert one terminal, correctly linked product outcome plus its review evidence
  into an immutable reviewed trajectory. Retain task/objective/decision/run and
  accepted-plan identity, references to authoritative evidence, success/failure,
  failed hypotheses, and protected-source references without copying secrets.
- Persist the trajectory before optional extraction. Keep recent reviewed evidence
  directly searchable until its case representation is durably confirmed; an
  uncertain EverOS flush never permits duplicate ingestion or loss of the source.
- Map the product's application/project/namespace/owner boundary to EverOS roots
  and filters. Reject unverified or cross-owner history instead of guessing scope.
- Resolve returned cases and skill candidates to exact source case IDs and reviewed
  receipts. Instruction-like text from a case is historical evidence, not executable
  guidance.
- Implement approval for generated skills only when every declared source case and
  receipt resolves uniquely and was reviewed. Approval binds the exact content,
  intended recipients, issuer, and origin; it never rewrites generated origin or
  auto-installs/executes helper scripts. Curated selection names the governing
  items instead of treating every visible skill as approved.
- Apply `privacy.py` before reusable extraction/model input and to derived content.
  Preserve raw authoritative evidence with its protected owner when it cannot be
  safely copied.

## Dependencies and integration

The integrated Stage-A identities, outcome schema, privacy policy, and SQLite
store from Step 01 are required. Step 03 consumes reviewed receipts and approved
skill/procedure candidates; therefore Step 02 integrates before any publication
work. The implementation worker owns the adapter and tests together so no separate
test-author handoff is needed.

## Requirement-fit validation

- For T04, create reviewed success and failure trajectories, restart the process,
  retire the synthetic run, and assert that exact evidence references, failed
  hypotheses, and review state remain queryable. Simulate interrupted extraction
  and prove recent evidence remains available until a confirmed representation
  exists.
- For T05, approve a generated candidate with complete reviewed provenance, then
  reject missing, ambiguous, cross-owner, or unreviewed source IDs. Assert approval
  preserves generated origin and that an unlisted curated item is not selected.
- Exercise the real EverOS add/search path with a temporary isolated memory root;
  verify owner/project filtering and restart persistence. Adapter doubles may
  cover faults, but a fixture-only `ExperienceRecord` list is no longer sufficient.
- Use known-secret fixtures across trajectory creation, extraction requests, cases,
  skills, and logs for the applicable T18 claims.

## Failure scope and recovery

An EverOS dependency or API mismatch blocks only the real adapter outcome. Prefer
a narrow product-side adapter correction; touch vendored source only with a focused
regression test. An uncertain extraction/flush leaves the reviewed trajectory
authoritative and pending; reconcile its stable ingestion identity before retry.
Privacy failure blocks only the unsafe reusable payload, not retention of protected
source evidence or unrelated task completion.
