# Remaining fixed-strategy memory-harness specification

## Product intent and authority

Finish only the behavior still unaccepted after the completed STEP-01 through
STEP-04 foundation and the first accepted STEP-05 Level 0 slice. The product must turn that preparation into a reviewable plan and
safe dispatch, retain truthful terminal and operational state, and prove the
integrated product path. Accepted behavior is a protected input, not a new work
assignment.

Authority is, in order: direct user and repository instructions;
`new_harness_memory_docs/PRODUCT_FEATURE_SPEC_v65.md` for product behavior;
the **binding** sections of `PRODUCT_IMPLEMENTATION_SPEC_v67.md` for shared
contracts and development verification; and the accepted candidate through
`cc5b4f2d03626b393581c231303f5d79a4627cf2` for the existing baseline.
`PRODUCT_SPEC_DETAILED_v72.md` is background, not another requirement source.
The user's later role-mapping choices in
`.plans/SUBAGENT_ROLE_MODEL_MAPPING.json` override older named development-test
bindings; they do not set deployed product defaults or the product APC binding.

Requirements below are dictated unless explicitly called an assumption or
implementation freedom. Repository module layout, internal algorithms, schema
field names, and test organization remain planning choices where the governing
sources do not fix their meaning.

## Current behavior and required change

The accepted candidate has exact task/plan/decision and operation contracts,
compatible SQLite state, fixed strategies and all-off controls, privacy guards,
five local template families, reviewed EverOS experience, trusted local/Atlas
procedure lifecycle, and bounded search over eligible local, EverOS, and Atlas
sources. Accepted STEP-04 slices include deadline handling, procedure selection,
local/Atlas adapters, template shortlisting, reviewed-case retrieval, and the
trusted EverOS-skill join. The completed plans are under
`.plans/finished/memory-backed-harness/steps/`; their behavior may be repaired
only when a remaining consumer exposes a concrete defect.

Real product-harness APC drafting is accepted at `a64ebfa9135960ad817752d447588feb5d782d80`; do not redo it absent a concrete remaining-consumer defect. Final context and actual
dispatch wiring, remaining whole-stage budget/compatibility closure, terminal effects and
usage, operator controls, snapshots, and integrated proof remain. The behaviors
below describe only those remaining outcomes. An already-correct part of one
behavior needs preservation or focused proof, not reimplementation.

## Actors, boundaries, and non-goals

ROOT owns exact current state, plan review/acceptance, recovery, live authority,
and final acceptance. The existing product harness owns worker/APC launch,
correction, review, resume, and cleanup. An APC child drafts but cannot accept the
parent plan or implement it. Execution workers receive only the accepted task and
safe context, never product control-plane authority. An authorized operator
configures, inspects, snapshots, and recovers isolated runs. EverOS supplies
scoped reviewed memory; Atlas supplies scoped shared-procedure discovery and
exact eligibility state. A delegated product-test ROOT exists only in development
verification, not normal deployment.

In scope: fixed Standard, Problem-focused, and Deeper behavior where still
consumed; preservation and final proof of accepted real bounded APC adaptation or fresh fallback; exact final context and
dispatch; linked outcomes and side-effect/usage reconciliation; truthful setup,
network modes, and snapshot recovery; and local, live Atlas, and nested native
proof. Out of scope: learned-selector machinery, benchmark execution or scored
comparisons, a new scheduler/launcher/reviewer, automatic template mining, a
secret manager, a dashboard, a second memory engine, a generic APC service,
production deployment, and requalification or expansion of
`references/harness-single` without a reproduced run-blocking defect.

## Shared terminology and product rules

- Exact task, plan, execution, and outcome state is loaded by identity, never
  reconstructed from semantic retrieval. A nonempty invalid plan reference is
  inconsistent mandatory state, not an absent plan.
- One bounded objective has one logical preparation decision and captured
  configuration. Restart, retry, route correction, or model-result correction
  does not silently create a fresh budget or decision.
- An APC result is a proposed plan. Only ROOT's acceptance of an exact revision
  makes a plan executable. Finalized context is ready for dispatch; it is not an
  observed harness invocation.
- Optional historical cases, approved procedures, and templates remain distinct.
  They cannot grant authority, rewrite task facts, or erase an accepted plan.
- The local terminal outcome is immutable and distinct from separately evolving
  side-effect and native-usage state. Missing evidence is not terminal unknown;
  missing usage is not zero.
- All-off bypasses optional memory and APC work while preserving the inherited
  harness lifecycle. Feature Spec Section 15 is the sole disabled-state and
  dependency table: remaining APC, dispatch/context, and outcome/effect
  consumers enforce its resolved state at service entry, including pending
  work and off transitions, rather than merely filtering returned content.
  An off transition is not reported fully disabled until affected in-flight
  work is drained, reconciled, or isolated.
- Known secrets and unrelated confidential content do not enter reusable or
  remote-bound payloads. Product-managed workers and APC children do not receive
  approval, publication, revocation, or policy-mutation credentials.
- Ambiguous effectful operations require exact reconciliation or source-backed
  idempotency before retry. Otherwise uncertainty remains visible and blocks only
  conflicting work.

## Behavior map and relationships

| Behavior | Outcome/status | Main prerequisite |
| --- | --- | --- |
| [BEHAVIOR-01](behaviors/BEHAVIOR-01-preparation-continuity-stays-bounded-and-compatible.md) | Continued preparation respects the original budget and old durable state. | Accepted search/plan contracts |
| [BEHAVIOR-02](behaviors/BEHAVIOR-02-apc-child-produces-a-reviewable-plan.md) | Accepted real harness-owned APC draft or honest fresh fallback reaches ROOT; preserve and consume it. | Accepted template shortlist; BEHAVIOR-01 budget |
| [BEHAVIOR-03](behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md) | An exact accepted plan becomes safe context and one reconciled dispatch. | BEHAVIOR-02 or fresh/current plan |
| [BEHAVIOR-04](behaviors/BEHAVIOR-04-terminal-outcome-and-effects-reconcile.md) | Linked terminal truth remains fixed while enabled effects recover. | BEHAVIOR-03 execution identity |
| [BEHAVIOR-05](behaviors/BEHAVIOR-05-native-usage-is-attributed-once.md) | Native work and incomplete usage remain truthfully attributable. | Decisions, child, execution, and review identities |
| [BEHAVIOR-06](behaviors/BEHAVIOR-06-setup-and-readiness-preserve-ownership.md) | Operators compose and inspect the actual isolated product. | Existing harness and ROOT-suite setup |
| [BEHAVIOR-07](behaviors/BEHAVIOR-07-network-mode-claims-match-enforcement.md) | Requested network modes match actual task-path enforcement. | Resolved configuration and launched payload |
| [BEHAVIOR-08](behaviors/BEHAVIOR-08-snapshots-restore-isolated-recoverable-state.md) | A consistent snapshot restores required trust and pending state in isolation. | Durable records and recovery semantics |
| [BEHAVIOR-09](behaviors/BEHAVIOR-09-pinned-candidate-proves-the-product-path.md) | One pinned candidate proves local, live Atlas, and nested native behavior. | BEHAVIOR-01 through BEHAVIOR-08 |

## Product-wide constraints and acceptance

Scope, authorization, exact identity, privacy, deterministic integrity, and
persisted-schema compatibility apply across the behaviors. Existing Stage-A
databases and ordinary legacy task cards remain readable through an explicit
supported read or migration path. Optional failures cannot overturn valid
harness acceptance or weaken mandatory state and security.

For each newly wired service path, a disabled feature prevents corresponding
work before launch or submission; already-submitted effects retain their
original configuration attribution. The all-off ordinary task path makes no
optional EverOS/Atlas or APC call while the inherited harness still completes.

[BEHAVIOR-09](behaviors/BEHAVIOR-09-pinned-candidate-proves-the-product-path.md)
owns the end-to-end development proof. Local doubles can decide deterministic
failure branches but cannot prove actual Atlas Vector Search or native
product-harness/model execution. Missing credentials or provider bindings leave
only their dependent claims unresolved, never passing. Release communication must
state `benchmark execution: deferred/not run` and
`learned selector: deferred/not implemented`.

## Assumptions and unresolved product decisions

Working assumption: the accepted candidate's interfaces can be extended
compatibly. Confirm at the first remaining consumer with focused contract or
migration checks; a disproved assumption repairs only its affected seam.

Working uncertainty: required live Atlas or native provider access may be
unavailable at verification time. Check readiness before the affected operation;
absence changes evidence availability, not product meaning. No product decision
is currently unresolved.
