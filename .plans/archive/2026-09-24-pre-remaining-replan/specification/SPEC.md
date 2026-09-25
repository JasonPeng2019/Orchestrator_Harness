# Memory-backed harness remaining-work specification

## Product intent and authority

Finish the fixed-strategy memory-backed coding harness from its accepted
STEP-01 through STEP-03 baseline. The remaining product must turn exact ROOT
state plus optional reviewed memory into a bounded planning decision, dispatch
only a ROOT-accepted plan through the existing harness, retain truthful terminal
and resource evidence, support safe operation and recovery, and prove the real
integrated path. Completed foundation, reviewed-experience, and trusted-procedure
work is an input to this specification, not behavior to redesign or repeat.

Authority is, in descending order:

1. Direct user instructions and repository instructions.
2. `new_harness_memory_docs/PRODUCT_FEATURE_SPEC_v65.md` for observable product
   behavior, trust boundaries, fallbacks, and current-phase scope.
3. Binding sections of
   `new_harness_memory_docs/PRODUCT_IMPLEMENTATION_SPEC_v67.md` for shared
   technical contracts and required development verification.
4. The accepted product source and tests at product commit
   `e2bd6bdf1987c9168b3abb879d532ffbd9b6f266` for the protected current
   baseline.
5. `new_harness_memory_docs/PRODUCT_SPEC_DETAILED_v72.md` as non-normative
   source and rationale guidance.

The user's later role-mapping changes supersede older named development-model
assignments where they conflict. They do not change deployed product behavior:
development roles come from `.plans/SUBAGENT_ROLE_MODEL_MAPPING.json`, while a
product APC child always uses the run's explicit `apc_adaptation_binding`.

Statements below are dictated requirements unless labeled otherwise. A
necessary derived behavior is identified where it follows from a dictated
boundary. Working assumptions are confined to the final section. Storage,
module, command, and schema design remain implementation freedom except where a
governing contract fixes their meaning.

## Current behavior and required change

The accepted baseline already provides:

- exact task, plan, decision, envelope, dispatch-operation, outcome, review,
  experience, procedure, and APC request/result contracts;
- compatible SQLite persistence for decisions, dispatches, outcomes, reviewed
  trajectories, EverOS receipts/cases/generated-skill approvals, and trusted
  procedure lifecycle state;
- fixed-strategy configuration and a hard deferred boundary for learned
  selection;
- privacy and worker credential filtering;
- five local template seeds plus deterministic direct-fill and fresh-plan
  primitives;
- a narrow optional memory handoff in bootstrap, resume, and launch;
- real, scoped EverOS reviewed-experience ingestion and retrieval; and
- immutable approved procedures, ordered designation, scoped Atlas publication
  and discovery, exact-read eligibility, withdrawal, revocation, exposure, and
  durable reconciliation.

The historical plans for those accepted outcomes live under
`.plans/finished/memory-backed-harness/steps/`. They have no remaining execution
work. The baseline's 70-test local result with one optional-EverOS skip is
retained evidence; a live Atlas claim was not established because credentials
were unavailable.

The required change is only the unfinished product path described by the six
behaviors below: bounded preparation, template/APC plan production, safe final
context and dispatch, post-execution durability and accounting, isolated
operator controls, and integrated product proof. Existing STEP-01 through
STEP-03 behavior remains compatible. A concrete defect discovered while a
remaining behavior consumes that baseline may be repaired at its owning seam,
but completed scope is not reopened merely to restyle, re-review, or regenerate
evidence.

## Actors, boundaries, and non-goals

The actors are:

- **ROOT**, which owns the objective, exact current state, plan acceptance,
  recovery decisions, live-operation authority, and final acceptance;
- the **operator**, which configures services, isolation, credentials, network
  mode, recovery, snapshots, and administrative procedure operations;
- the **product harness**, which remains the sole owner of worker and APC-child
  launch, correction, review, resume, and cleanup;
- an **execution worker**, which receives only the finalized task and accepted
  plan context needed for its assignment and no product control-plane authority;
- an **APC drafting child**, which can produce a bounded proposed plan but has no
  parent-plan, implementation, publication, ROOT, or recursive-launch authority;
- **EverOS**, which supplies scoped reviewed case/skill memory;
- **Atlas**, which supplies scoped shared-procedure discovery while exact product
  state remains authoritative for delivery; and
- during development verification only, the outer **implementation harness** and
  delegated **product-test ROOT**, which exercise an isolated candidate product
  harness and are not deployment architecture.

In scope are the ordinary all-off path, fixed Standard, Problem-focused, and
Deeper preparation, local and Atlas-backed optional memory, template direct fill,
real harness-launched light adaptation, fresh planning, final context, dispatch,
outcomes, reconciliation, native usage, snapshots, network modes, an operator
surface, and synthetic/local/live/native verification.

Out of scope are a learned selector or any learner state/training/inference/update
machinery; every benchmark, benchmark subset, leaderboard run, or scored
comparison; automatic template mining; another launcher, scheduler, review
system, general memory engine, secret manager, dashboard, or APC service;
expansion or requalification of `references/harness-single` without a reproduced
run-blocking defect; production deployment; and claims of hardened same-user
sandbox isolation.

## Shared terminology and product rules

- **Exact current state** is ROOT/harness state loaded by exact identity. It is
  never reconstructed by semantic search.
- A **planning route** or topology admission result is distinct from the selected
  **fixed search strategy**. A late Level 0 result corrects the route; it does not
  relabel stale topology preparation as ordinary memory output.
- A **decision** is one logical preparation for one bounded objective and captured
  configuration. Process restart, internal queries, and result correction do not
  silently create new decisions or replenish budgets.
- **Current plan state** distinguishes absent, candidate/review, execution-
  accepted, and inconsistent nonempty plan references. An accepted plan for the
  same objective has precedence over memory.
- **Optional memory** includes historical cases, approved guidance, and plan
  templates. It can be omitted when unavailable or ineligible, but cannot replace
  mandatory task/plan state, grant authority, or erase valid work.
- **Finalized** means the exact execution envelope is ready to dispatch;
  **dispatched** means the existing harness launch is observed or reconciled.
  These are not the same state.
- An **outcome** is at most one immutable local terminal fact per decision, based
  on exact linked execution and review/acceptance evidence. Missing evidence is
  not a terminal unknown.
- **Usage evidence** has a separate lifecycle from outcome quality. Missing usage
  is incomplete, not zero, and late usage does not alter the immutable outcome.
- All feature values, dependencies, availability reasons, network mode, time
  budget, and positive execution reserve resolve before optional preparation.
  All enhancements off bypass the optional pipeline entirely while preserving
  the inherited harness lifecycle.
- Product-managed workers and APC children never receive memory approval,
  publication, revocation, policy-mutation, or other control-plane credentials.
  Known secret and confidential content is omitted, safely represented, or kept
  behind a protected reference at every reusable or remote boundary.
- Completed authoritative effects are never blindly replayed. Effectful ambiguous
  operations require source-backed idempotency or exact reconciliation; otherwise
  they remain visibly uncertain for operator recovery.
- Feature or service failure blocks only the behavior that depends on it when
  mandatory state and security remain valid. It never turns an optional hit into
  authority or reverses an already valid harness acceptance.

## Behavior map and relationships

| Behavior | Dictated outcome | Depends on or interacts with |
| --- | --- | --- |
| [BEHAVIOR-01](behaviors/BEHAVIOR-01-bounded-preparation-selects-eligible-memory.md) | One bounded preparation preserves exact state and returns only eligible optional memory or an honest no-memory result. | Accepted STEP-01–03 contracts, EverOS, procedure eligibility, feature resolution |
| [BEHAVIOR-02](behaviors/BEHAVIOR-02-reuse-produces-a-root-reviewable-plan.md) | Template reuse deterministically produces a bounded proposal or falls back to fresh ROOT planning. | BEHAVIOR-01 shortlist and budget; existing product-harness child lifecycle |
| [BEHAVIOR-03](behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md) | Only an exact ROOT-accepted plan becomes safe worker context and one reconciled product-harness dispatch. | BEHAVIOR-01 optional guidance; BEHAVIOR-02 plan disposition |
| [BEHAVIOR-04](behaviors/BEHAVIOR-04-terminal-work-remains-durable-and-accounted.md) | Linked terminal work remains immutable while side effects and native usage reconcile truthfully. | BEHAVIOR-03 dispatch identity; accepted experience/procedure services |
| [BEHAVIOR-05](behaviors/BEHAVIOR-05-operators-control-isolated-recoverable-runs.md) | Operators can configure, inspect, snapshot, restore, and recover isolated runs without overstating enforcement or completion. | BEHAVIOR-01–04 state and services |
| [BEHAVIOR-06](behaviors/BEHAVIOR-06-integrated-candidate-proves-the-real-product-path.md) | A pinned candidate demonstrates the local, live Atlas, and nested native product path with owned cleanup. | BEHAVIOR-01–05 complete; development-only harness topology |

## Product-wide constraints and acceptance

Privacy, authorization, exact identity, deterministic integrity, persisted-schema
compatibility, and source/recipient scope apply end to end. Optional memory never
weakens a task constraint, accepted plan, procedure gate, or harness lifecycle.
Existing Stage-A databases and ordinary legacy task cards remain readable; an
incompatible schema change needs an explicit supported read or migration path.

The product-wide journey is accepted when one pinned candidate can:

1. compose and validate the existing harness and ROOT-suite capabilities without
   ownership loss, then run an ordinary all-off task without optional memory calls
   or context;
2. prepare an enhanced synthetic task from exact state, reviewed EverOS history,
   an eligible scoped Atlas procedure, and the local template library;
3. exercise direct-fill and fresh fallback locally and a real near-match drafting
   child through an explicit `apc_adaptation_binding`;
4. obtain ROOT acceptance, finalize the exact context, dispatch through the
   candidate product harness, and bind terminal review to one outcome;
5. reconcile enabled experience/procedure effects and native usage across restart
   without duplication;
6. export and restore the needed state into an isolated identity boundary; and
7. close every owned child and runtime resource while leaving outer or unrelated
   state untouched.

Local doubles decide deterministic failure and recovery branches, but they do not
prove actual Atlas Vector Search or native product-harness/model execution. Those
claims require the boundaries in BEHAVIOR-06. An unavailable credential or native
binding leaves only the dependent live claim unresolved; it cannot be reported as
passing and does not erase unaffected local evidence.

No acceptance activity may run a benchmark or instantiate learned-selector code.
Release communication must state `benchmark execution: deferred/not run` and
`learned selector: deferred/not implemented`.

## Assumptions and unresolved product decisions

Working assumption: the accepted STEP-01–03 interfaces can be extended compatibly
for remaining behavior. Confirm this at each first consumer with focused contract
and migration tests; a disproved assumption repairs only the affected seam and its
downstream evidence.

Working uncertainty: live Atlas credentials and every requested native provider
binding may not be present when verification begins. Readiness must establish
availability before the affected operation; absence changes evidence availability,
not product behavior or the validity of completed local work.

There are no unresolved product decisions. Concrete module boundaries, persisted
field names, CLI syntax, search algorithm, snapshot mechanism, and supported
adapter composition remain implementation choices constrained by the behaviors
above.
