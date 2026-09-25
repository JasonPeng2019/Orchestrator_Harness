# STEP-03 - Approved procedures publish, resolve, and revoke safely

> Completed and accepted. This is a historical plan record, not active work.

## Outcome

The product manages versioned procedures from local approval through partitioned
Atlas publication and discovery. Receivers can establish content, origin,
authorization, current designation, representation compatibility, and revocation
before delivery. Lost acknowledgements, stale writes, withdrawal, and revocation
are recoverable without treating search-index visibility as authoritative state.

## Scope and touchpoints

Add `src/memory_harness/procedures.py`; extend `contracts.py`, `store.py`,
`atlas.py`, `privacy.py`, package exports, and `pyproject.toml` as required. Use
the vendored `langchain-mongodb` `MongoDBAtlasVectorSearch` search/index primitives
where they preserve the contract, with direct PyMongo exact reads for fields or
vectors the wrapper does not return reliably. Add deterministic tests under
`tests/local/procedures/` and `tests/local/atlas/`, plus one credential-gated,
uniquely namespaced live test under `tests/live/atlas/`.

## Implementation

- Define a normalized procedure record with origin-qualified logical identity,
  immutable behavior revision and payload, approval/issuer/recipient evidence,
  partition, structured applicability/conflict/capability/route predicates,
  representation identity, and separate current/revoked/withdrawn state.
- Extend `MemoryStore` with transactional procedure, designation, publication,
  revocation, and stable external-operation records. Migrate an existing Stage-A
  database without losing its decisions, operations, or outcomes.
- Require explicit designation after approval. Use a generation or conditional
  predecessor so delayed designation, publish, withdrawal, or rollback attempts
  cannot overwrite newer state. Authorized rollback is a new ordered operation.
- Publish only to an authorized partition after scanning body, metadata, query,
  and representation payloads. Track source-local intent, remote durable result,
  and local acknowledgement independently. On a lost response, exact-read the
  operation/revision before retry.
- Make revocation fence every tracked active copy before claiming managed global
  completion. Partition withdrawal is narrower. Neither operation silently selects
  older history; already-delivered exposure remains recorded.
- Use Atlas Vector Search only for discovery. Resolve shortlisted documents by
  exact ID/revision and revalidate approval, recipient, current designation,
  revocation, predicate semantics, payload integrity, and representation before
  use. Index lag or a stale vector hit cannot authorize delivery.

## Dependencies and integration

Step 02 supplies reviewed source receipts and generated approval provenance.
Step 04 consumes the normalized procedure records and Atlas search adapter. All
live operations use a synthetic application/project/namespace and one owner; the
worker must not touch production collections or another run's namespace.

## Requirement-fit validation

- T06-T07 tests change behavior, references, compatibility, and redaction meaning
  to require new revisions; reject incoherent truncation, cross-owner/project/app/
  namespace delivery, untrusted issuers, and unresolved remote evidence.
- T08 tests that approval alone changes no current designation; a durable remote
  acceptance precedes a shared-current claim; delayed older designation loses;
  explicit rollback creates a new operation.
- T09 tests multi-partition revocation, narrower withdrawal, stale/in-flight
  publish fencing, recorded prior exposure, and retry after ambiguous acknowledgement.
- Adapter tests prove identical predicate meaning and representation metadata
  across local serialization, Atlas documents, exact reads, and search results.
- The live Atlas test creates its own namespace/index/data, observes an actual
  Vector Search hit, exact-reads and lifecycle-validates it, then revokes it and
  verifies it cannot be delivered before cleaning only its owned resources. This
  live test proves the adapter boundary, not the final nested product flow.

## Failure scope and recovery

Missing credentials or Atlas permissions leave the live claim unresolved but do
not invalidate deterministic lifecycle tests. Preserve the namespace for diagnosis
only when cleanup would destroy needed evidence; otherwise delete owned synthetic
data. An ambiguous remote operation stays uncertain until exact reconciliation and
must not be retried under a new identity. A schema or predicate bug invalidates the
affected procedure consumers and representation tests, not Step 02 trajectories.
