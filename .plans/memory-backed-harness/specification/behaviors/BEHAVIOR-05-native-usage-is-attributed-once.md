# BEHAVIOR-05 - Native usage is attributed once and incompleteness stays visible

## Dictated outcome and source

For each actual model, CLI, embedding, retrieval, APC, ROOT, worker, reviewer,
correction, and resume invocation, the product retains source-native usage when
available and an honest coverage state when it is not. Aggregation never counts
one invocation twice or changes a fixed quality outcome. Feature Section 17 and
binding Implementation Section 2.6 govern this outcome.

## Actors, triggers, and preconditions

Product service and harness adapters observe invocation start and provider
receipts. ROOT and operators inspect per-objective resource use. A provider may
return cumulative, partial, late, or no usage; an APC child may be referenced by
both its own receipt and its parent decision.

## Behavioral flow and decision rules

1. Attribute each started invocation to its exact source, task/objective/decision
   or maintenance operation, stage, requested/resolved/native binding where
   available, and an invocation identity. Keep correction and resume calls
   distinct even in one session.
2. Parse native input/output/cache/reasoning/total/cost units only where exposed.
   Do not add a component again when already included in the provider total, sum
   cumulative intermediate receipts twice, or equate embedding units with
   completion-model tokens.
3. Record expected coverage for a known started call lacking native usage as
   incomplete, not zero. A late authentic receipt fills the resource record
   idempotently under its original objective/configuration and measurement
   window without modifying terminal quality.
4. Link an APC support child's cost once to parent online adaptation. Separate
   online planning/review/execution, maintenance ingestion/publication, and
   embedding work. In a nested development test, distinguish outer
   implementation orchestration, product-test ROOT, and inner candidate work.
5. Report combined cost only under a declared compatible unit or rate mapping;
   do not claim savings or efficiency from missing usage or exclude failed reuse
   attempts and fallback work.

## State, data, and observable effects

Usage records retain native source and invocation identity, attribution,
components/total/cost when observed, and coverage/completeness reason. Resource
history may be updated by late evidence; the linked task outcome is immutable.
Stage latency and objective wall time remain distinguishable.

## Edge, failure, and recovery behavior

Re-parsing the same receipt is idempotent. Two different calls with identical
token counts remain two calls. A started call with no native receipt remains
incomplete. An unavailable provider counter or incompatible unit limits only
the aggregate claim that depends on it; quality evidence remains separately
usable. Late evidence cannot be charged to an unrelated current objective.

## Constraints and preserved behavior

No learner observation/update store is introduced. Usage collection respects
privacy and task/recipient scope. Development-test role mapping is evidence for
that run, not a product default.

## Acceptance scenarios

- Corrections, resumes, ROOT, worker, reviewer, embeddings, and APC calls each
  appear once by actual invocation; cumulative receipts and child references do
  not double-count.
- A known started call with no usage is incomplete rather than zero; a later
  receipt fills its record without changing the terminal outcome.
- Outer implementation overhead and inner product execution remain separately
  attributable in a nested test.
- An attempted reuse followed by fresh planning includes both costs and cannot
  be reported as a clean cache hit or unqualified savings claim.

## Implementation freedom and unresolved decisions

Storage, parsing adapters, aggregation surface, and compatible cost policy are
implementation choices. No product decision remains unresolved.
