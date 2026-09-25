# Memory-backed harness remaining-work execution plan

## Outcome and boundaries

This plan implements only the unfinished behavior in the governing
[remaining-work specification](specification/SPEC.md). Its accepted product
baseline is the protected starting point, and its completed plans are historical
records:

- [STEP-01 - foundation](../finished/memory-backed-harness/steps/STEP-01-adopt-existing-foundation.md)
- [STEP-02 - reviewed experience](../finished/memory-backed-harness/steps/STEP-02-persist-reviewed-experience.md)
- [STEP-03 - trusted procedures](../finished/memory-backed-harness/steps/STEP-03-publish-trusted-procedures.md)

Those outcomes are not rerun, reformatted, or re-accepted. A remaining step may
repair a concrete compatibility defect at a consumed seam, but only that seam and
its downstream evidence are reopened.

The finish line is a fixed-strategy product path that prepares from exact state,
optionally reuses eligible reviewed memory, produces a ROOT-reviewable plan,
dispatches only the accepted plan through the existing product harness, and keeps
terminal state, usage, recovery, isolation, and operator claims truthful. The
final candidate must establish the local, live Atlas, and nested native boundaries
required by the specification.

No step implements a learned selector, benchmark, second launcher or scheduler,
new review system, general memory engine, or production deployment. The current
outer harness source is the user-supplied `references/harness-single` at `5134f6c`;
further changes require another user instruction or a reproduced run-blocking
defect. Product implementation is active under the user's resume instruction;
[HANDOFF.md](../../HANDOFF.md) owns the exact native runtime state.

## Current system and target design

The accepted package already owns its canonical records in
`src/memory_harness/contracts.py`, transactional SQLite state in `store.py`, fixed
feature configuration in `config.py`, template seeds in `templates.py`, APC
request/result contracts in `apc.py`, privacy rules in `privacy.py`, and the
initial runtime in `runtime.py`. It already has real reviewed-experience and
trusted-procedure services. The optional product-harness handoff is deliberately
narrow: `harness/orchestrator_harness/memory_handoff.py` is consumed by bootstrap,
resume, and launch. Harness review and acceptance remain owned by the existing
`review.py` path. `setup.py` already stages and composes provider/ROOT payloads and
must be extended in place, not replaced.

The remaining design is one continuous flow:

1. A preparation coordinator validates exact task, objective, plan state, route,
   configuration, and an absolute deadline. It obtains bounded candidates through
   adapters for the accepted EverOS, procedure/Atlas, and local-template services.
2. The coordinator normalizes and gates candidates before ranking, preserves an
   accepted current plan, and selects direct fill, one product-harness APC drafting
   child, or fresh ROOT planning.
3. A context finalizer refreshes plan-affecting guidance, packs mandatory and
   optional material without truncating trusted meaning, binds the accepted plan
   to the actual task/base, and hands exactly one dispatch to the existing harness.
4. A completion bridge consumes that harness's linked review/acceptance result,
   fixes one terminal outcome, and reconciles side effects and native usage from
   durable state. Optional memory bookkeeping cannot reverse valid harness
   acceptance.
5. The existing setup composer plus small operational services expose readiness,
   truthful network state, recovery, snapshots, and usage without becoming another
   controller. The final verification wave invokes these paths through the actual
   candidate product harness.

This keeps domain policy in `memory_harness`, process lifecycle in the existing
harness, and external-service behavior behind the accepted adapters. No component
calls a model provider directly to bypass the harness.

## Shared decisions and contracts

- `contracts.py` remains the single schema and canonicalization owner. Add versioned
  preparation/search, plan-disposition, finalized-context, operation, usage, and
  snapshot records there rather than inventing adapter-local shapes.
- `store.py` remains the single local state authority. Its additive migration must
  read the accepted STEP-01 through STEP-03 database and preserve exact identities,
  immutable outcomes, idempotent replays, and visibly uncertain external effects.
- Planning route/admission evidence and the fixed Standard, Problem-focused, or
  Deeper strategy are separate fields. A late Level 0 correction supersedes the
  old preparation without resetting the objective's spent time or creating a new
  logical decision.
- An injected monotonic clock and one absolute decision deadline govern optional
  work. Central configuration owns stage limits, execution reserve, context limits,
  and template thresholds; adapters receive remaining allowance and cannot create
  local budget resets. The Implementation specification's Section 16 values are
  starting defaults, not scattered literals.
- A narrow harness adapter wraps the existing launch/reconcile/result lifecycle for
  workers and APC children. It records intent before launch, reconciles ambiguous
  acknowledgement by exact identity, and never substitutes a raw provider call.
- Privacy and recipient checks run before queries, embeddings, remote payloads,
  APC context, worker context, usage diagnostics, and logs. Workers and APC children
  never receive memory control-plane credentials.
- Credential readiness checks the ignored `.secrets/creds/` directory before
  declaring Atlas, MongoDB, or DeepInfra access unavailable. Load only the needed
  values into the authorized process: map the stored Atlas URI to
  `MEMORY_HARNESS_ATLAS_URI`, supply an isolated
  `MEMORY_HARNESS_ATLAS_LIVE_DATABASE`, and set the live-test opt-in only for the
  owned operation; map the stored DeepInfra key to the required `EVEROS_*__API_KEY`
  variables. Never place values in task cards, prompts, logs, or committed files.
  Files on disk do not replace service/index/network readiness checks.
- Requested network mode, effective mode, enforcement source, unsuppressed
  capability, and outage state are distinct. Claims are based on the actual service
  adapter and launched payload, not the requested label.
- The public operational boundary is the smallest Python service facade needed by
  setup/readiness, recovery, snapshot, network-state, and usage consumers. Reuse
  existing harness entrypoints for process launch. Add a CLI only if a concrete
  automation consumer requires one during implementation.
- `.plans/SUBAGENT_ROLE_MODEL_MAPPING.json` is the only development-role mapping.
  Immediately before a native launch, ROOT resolves the named role with
  `development/test-tools/resolve-role.py` and applies only the mapping's
  user-authorized fallback rules. Product APC execution remains independently
  bound by the run's explicit `apc_adaptation_binding`.
- The outer implementation harness is `development/dogfood/harness`, projected
  from the current reference baseline. Its new bootstrap/resume task cards include
  nonempty `acceptance_criteria`, `deliverables`, and
  `reason_for_acceptance_and_deliverables`; those fields state the assignment's
  outcome without adding an evidence or review layer. This outer-card requirement
  does not remove the product's legacy memory-handoff compatibility.
  Product worktrees belong under
  `development/product/worktree_example/.harness-runtime/worktrees/`. Every new task
  card names the absolute product root, this plan, and its assigned step because
  the product worktree does not contain the top-level `.plans` tree.

## Step map and execution order

ROOT is the single delivery and integration owner. STEP-04 remains one acceptance
outcome, but its work is assigned in small, serial, source-coherent slices on one
commit chain. Retain accepted slices and continue the active lane named in
`HANDOFF.md`, then resolve the remaining retrieval/trust, template/APC,
store/prompt wiring, and budget/migration seams in dependency order. STEP-05 may
also use serial slices rather than one context-heavy assignment. One writer owns
overlapping contracts, storage, runtime, and harness seams at a time. ROOT inspects
each changed surface and integrates each completed outcome. STEP-06 delegates one
verification wave over a pinned read-only candidate because the specification
requires the nested product-harness boundary; it adds no parallel product writer.

Source-coherent is a ceiling, not a reason to bundle independent seams. After the
active local-procedure lane, give each worker one observable boundary and its
direct focused tests: remote approved-skill discovery, APC child ownership,
final context/dispatch wiring, and budget/migration compatibility are separate
assignments. Do not repeat the whole STEP-04 test matrix per slice. If a focused
test fails, check its fixture and assertion against the existing contract before
changing product behavior. A watch timeout alone never restarts a healthy worker;
for a long-running lane, inspect its native status, changed bytes, and focused
failures, then send one targeted correction rather than extending watches blindly.

| Step | Produces | Governing behavior | Depends on | Owner or lane |
| --- | --- | --- | --- | --- |
| [STEP-04](steps/STEP-04-prepare-and-dispatch-with-memory.md) | Bounded preparation, template/APC proposal, safe context, and one reconciled dispatch | [BEHAVIOR-01](specification/behaviors/BEHAVIOR-01-bounded-preparation-selects-eligible-memory.md), [BEHAVIOR-02](specification/behaviors/BEHAVIOR-02-reuse-produces-a-root-reviewable-plan.md), [BEHAVIOR-03](specification/behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md) | Accepted STEP-01 through STEP-03 baseline | ROOT-launched `complex_writer` |
| [STEP-05](steps/STEP-05-reconcile-and-operate-durably.md) | Durable outcome/side-effect/usage reconciliation plus truthful setup, network, snapshot, and recovery controls | [BEHAVIOR-04](specification/behaviors/BEHAVIOR-04-terminal-work-remains-durable-and-accounted.md), [BEHAVIOR-05](specification/behaviors/BEHAVIOR-05-operators-control-isolated-recoverable-runs.md) | Integrated STEP-04 | ROOT-launched `complex_writer` |
| [STEP-06](steps/STEP-06-prove-the-integrated-product.md) | Local, live Atlas, and nested native proof for one pinned candidate | [BEHAVIOR-06](specification/behaviors/BEHAVIOR-06-integrated-candidate-proves-the-real-product-path.md); integrated proof of BEHAVIOR-01 through BEHAVIOR-05 | Integrated STEP-05 and required live/native readiness | ROOT-launched `test_root`; candidate-harness test roles |

## Integration and whole-product validation

Each implementation worker owns its behavior and focused tests in one native
worktree. ROOT reviews the changed bytes and observed checks, then uses the existing
harness retirement/integration lifecycle. Its ordinary task, result, review, and
acceptance records are runtime inputs to the product and are not duplicated into a
plan report. A behavior defect holds its step and consumers; an administrative
defect is corrected locally and does not erase valid code or evidence.

After STEP-05 is integrated, run the authoritative product-local suite once on the
candidate:

```powershell
python -m unittest discover -s tests/local -t . -p "test_*.py"
```

Run affected harness tests when a harness seam changes. Build and import an
isolated wheel once when final packaging, exports, or runtime dependencies changed.
STEP-06 may reuse those results only when its pinned source and consumed inputs are
identical; otherwise it reruns the affected check. Its live Atlas lifecycle and
nested native wave remain separate claims because local doubles cannot prove
either boundary.

The approximate critical path is the remaining serial STEP-04 seams, STEP-05's
shared state and operations, candidate pinning, a live eligible Atlas procedure,
the enhanced native task, and exact cleanup. After candidate pinning, isolated
local checks, Atlas/service readiness, and role/binding preflight can proceed as
their inputs and host resources allow; the native enhanced task consumes the live
procedure and the pinned candidate, so those edges are serial. Schedule ready
independent checks as capacity frees rather than waiting for a whole test wave.
An ordinary failure ends only its coordinate; collect other feasible results
before a compatible repair. Native/provider and service capacity have not been
measured for this candidate, so do not promise a duration or parallel speedup.
Reassess only future work if a slice repeats without meaningful progress, a live
step overruns its budget, or host/provider contention appears.

The integrated enhanced journey must join preparation, eligible EverOS and Atlas
memory, template/APC or fallback planning, ROOT acceptance, final context, real
product-harness dispatch, linked terminal review, outcome and usage reconciliation,
restart/snapshot behavior, and owned cleanup. The all-off journey proves that the
same product preserves ordinary harness behavior without optional initialization
or calls. Final communication states `benchmark execution: deferred/not run` and
`learned selector: deferred/not implemented`.

When a check fails, compare the assertion, observed behavior, and governing
contract before assigning product repair. Only conclusions that consumed the
failed or changed input are invalidated. Pool findings only when one owner can
repair one coherent invariant and prove it with the same focused checks; otherwise
use separate corrections. A product defect returns to STEP-04 or STEP-05, creates
a new candidate only when pinned bytes actually change, and reruns its selected
fast-suite entries plus affected integrated consumers. Credentials still
unavailable after checking `.secrets/creds/` and
securely loading the authorized process—or an unavailable requested native
binding—leave only the dependent live claim unresolved; they do not convert a
fixture into proof or discard passing local work.

## Risks, assumptions, and unresolved decisions

- The accepted schema may need additive evolution at several shared records. Each
  first consumer proves old-database read/migration behavior; a failure repairs that
  contract and its consumers without reopening accepted experience or procedure
  semantics.
- Child launch and remote writes can succeed before acknowledgement is observed.
  Persisted intent plus exact lookup/idempotency is required before retry; an
  unreconcilable effect remains actionable and uncertain.
- Workspace composition crosses provider-owned payloads. Ownership collisions fail
  before mutation, staged replacement remains atomic, and interrupted or overwritten
  composition blocks only enhanced dispatch until the actual payload is repaired.
- Atlas and DeepInfra credentials are stored under ignored `.secrets/creds/`, but
  may not yet be mapped into the current process. Step readiness checks that source
  first, then verifies the loaded variables, scoped database/index permissions,
  connectivity, and requested provider bindings. A remaining failure limits only
  the affected live operation and never permits silent substitution or relabeling
  local evidence.

There are no unresolved implementation decisions that prevent Step 04 from
starting after the run is explicitly resumed.
