# BEHAVIOR-04 - Terminal work remains durable, recoverable, and truthfully accounted

## Dictated outcome and source

The product fixes at most one terminal outcome from exact linked execution and
review evidence, then reconciles enabled memory effects and usage independently
without duplicating work or rewriting task truth. Outcome quality, side-effect
completion, and resource accounting remain distinct and observable. Feature
Sections 11 and 17 and Implementation Sections 2.6 and 11 dictate this outcome.

## Actors, triggers, and preconditions

ROOT or an authorized result bridge submits terminal evidence for an observed
product-harness invocation. The exact task, objective, decision, accepted plan,
dispatch/run identity, review and acceptance evidence, resolved configuration, and
enabled side effects must be durable or resolvable. Providers and background
services may later supply usage or side-effect acknowledgements.

APC-child completion alone is never eligible parent execution evidence. Missing or
unreadable terminal evidence leaves the parent unobserved.

## Behavioral flow and decision rules

1. Validate that task, objective, decision, accepted plan, actual dispatch/run,
   result, review, and acceptance all identify the same execution. Preserve PASS,
   FAIL, BLOCKED, and genuine terminal unknown distinctly from absent evidence and
   from forced or exceptional acceptance.
2. Fix one immutable local outcome. An identical replay is idempotent; a different
   terminal fact for the same decision is an explicit integrity conflict. A
   legitimate correction needs linked correction or supersession evidence and
   does not silently overwrite history.
3. Persist deterministic intents for enabled current-phase side effects with the
   local outcome at one recoverable boundary where practicable. Side effects such
   as reviewed-receipt/recent-evidence publication, EverOS ingestion, and optional
   remote telemetry run afterward and acknowledge separately. Learned-policy
   update is never one of them.
4. On restart, rediscover pending, uncertain, or incompletely acknowledged effects
   from durable state. Replay an effectful operation only when its external
   contract provides safe idempotency or exact reconciliation. Otherwise retain
   the uncertainty and require operator recovery rather than duplicate a possibly
   committed effect.
5. Coordinate conflicting local retries so concurrent processes cannot overwrite
   an accepted outcome or perform the same authoritative mutation twice. A
   completed or successfully superseded operation does not remain a live blocker.
6. Record every actual model, CLI, embedding, retrieval/rerank, ROOT, worker,
   review, correction, resume, and APC-child invocation once when it belongs to the
   product objective. Retain source/invocation identity, task/decision attribution,
   provider/model/stage, native components/total/cost when present, and
   completeness.
7. Aggregate by actual invocation rather than by references to that invocation.
   Do not double-count cumulative receipts or components already included in a
   native total. Attribute APC cost once to parent adaptation, and keep outer
   implementation-test overhead separate from inner product execution.

## State, data, and observable effects

Outcome state carries the exact identity joins, terminal status, acceptance and
forced/exception facts, evidence identity, and observation time. Usage and
side-effect state can continue changing after the outcome without modifying that
outcome.

Each side-effect operation carries stable intent and payload identity, observed
phase, error or uncertainty, acknowledgements, and supersession where applicable.
Each expected invocation has either native usage, an explicit incomplete/missing
observation, or a known not-started disposition. Unknown values stay unknown, not
zero.

Online planning/search/APC/ROOT/review/worker costs, maintenance
ingestion/extraction/publication costs, and embedding units remain distinguishable.
Late evidence is retained under its original objective/configuration and does not
retroactively change task quality.

## Edge, failure, and recovery behavior

- Review or acceptance from another task, run, decision, or plan cannot create the
  outcome. Missing evidence stays unobserved; an authoritative terminal unknown is
  recorded only when actually supplied.
- Crash before outcome fixation permits reevaluation from exact evidence. Crash
  after fixation resumes only missing side effects and usage ingestion.
- A lost external acknowledgement is reconciled by exact operation and external
  state. If safe reconciliation is impossible, keep the operation uncertain and
  do not invent exactly-once guarantees.
- Side-effect failure does not reverse a valid harness acceptance or erase recent
  reviewed evidence. It remains pending, failed, uncertain, or explicitly
  superseded with an actionable next step.
- Missing or late usage makes only the affected accounting incomplete. It does not
  turn the invocation into zero cost or invalidate a correctly linked outcome.
- Feature transition to off stops new non-safety submissions and pauses or
  reconciles in-flight work before claiming fully effective off. A late
  acknowledgement retains its original configuration attribution.

## Constraints and preserved behavior

Existing accepted outcome, review-receipt, EverOS ingestion, and procedure
operation semantics remain compatible. Original evidence or protected references
remain available as required for provenance. Reconciliation never launches learner
work, treats a child's draft task as parent success, or uses broad process cleanup.

## Acceptance scenarios

- Exact linked PASS, FAIL, and BLOCKED executions create one immutable outcome;
  wrong-task/run/decision/plan evidence and absent evidence do not.
- Identical outcome replay returns the same fact; conflicting replay produces an
  integrity conflict and preserves the original.
- A crash immediately before and after outcome fixation respectively produces no
  fabricated outcome and one fixed outcome with only missing side effects resumed.
- Lost acknowledgement during EverOS or remote reconciliation is exact-read or
  idempotently reconciled; an unsafe ambiguous operation remains uncertain rather
  than replaying under a new identity.
- Two concurrent retries cannot duplicate or overwrite the same accepted effect.
- A side-effect outage leaves valid harness acceptance intact and keeps recent
  reviewed evidence available for recovery.
- Native usage for corrections, resumes, ROOT, worker, reviewer, embeddings, and
  APC is counted once per invocation; cumulative receipts and referenced child
  usage do not double-count.
- A started call with no native usage remains incomplete, not zero. Later usage
  fills the resource record without changing the terminal outcome.
- In a nested development run, outer implementation overhead and inner product
  execution remain separately attributable.

## Implementation freedom and unresolved decisions

Transaction technology, outbox representation, operation labels, usage storage,
and aggregation APIs are implementation choices. They must preserve exact joins,
idempotency/conflict behavior, and truthful incompleteness. No product decision
remains unresolved.
