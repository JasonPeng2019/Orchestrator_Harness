# STEP-04 - Bounded memory preparation produces one safe harness dispatch

## Outcome

Implement [BEHAVIOR-01](../specification/behaviors/BEHAVIOR-01-bounded-preparation-selects-eligible-memory.md),
[BEHAVIOR-02](../specification/behaviors/BEHAVIOR-02-reuse-produces-a-root-reviewable-plan.md),
and [BEHAVIOR-03](../specification/behaviors/BEHAVIOR-03-accepted-plan-dispatches-with-safe-context.md).
For one exact objective, the product produces eligible optional memory or an honest
empty result, obtains a direct-fill, harness-adapted, or fresh ROOT plan, finalizes
only the accepted plan, and creates at most one reconciled product-harness dispatch.

## Scope and touchpoints

The worker extends the accepted owners in
`development/product/worktree_example/src/memory_harness/`: `contracts.py`,
`store.py`, `config.py`, `runtime.py`, `templates.py`, `apc.py`, and `privacy.py`.
Add cohesive preparation/search, context-finalization, and harness-adapter modules
where separation helps; `search.py`, `context.py`, and `harness_bridge.py` are
descriptive names, not mandatory file boundaries. The current candidate chain
already contains these modules and partial contract/launch work; continue from
accepted slices rather than recreating them from the baseline.

Change `harness/orchestrator_harness/memory_handoff.py` and its bootstrap, resume,
launch, or operator-launch consumers only where the existing optional seam cannot
carry finalized context or exact launch reconciliation. Keep the harness controller,
review lifecycle, task-card compatibility, and all-off path intact. Consume the
accepted EverOS and procedure APIs; do not redesign completed STEP-02 or STEP-03
services or modify `references/harness-single`.

## Implementation

Treat the numbered items as completion obligations, not one worker assignment.
Keep one writer and split remaining changes by source context and proof: finish
the pending retrieval deadline review, then trust/deduplication and real store
adapters, template/APC proposal and child ownership, actual prompt/store wiring,
and budget/migration compatibility. Move a slice when a demonstrated dependency
requires it; combine findings only when the same invariant, owner, and focused
check cover them. Each accepted slice remains on the same commit chain.

1. Extend canonical records and persistence for the preparation input, normalized
   candidate and disposition, bounded search trace, plan disposition, APC child
   operation, and finalized context. Represent current-plan states explicitly:
   absent, candidate/review, execution-accepted, and inconsistent nonempty
   reference. Add a compatible read/migration path for the accepted database.
2. Build preparation around one logical decision and an injected monotonic absolute
   deadline. Resolve feature dependencies, network mode, route/admission evidence,
   strategy, stage allowances, and positive execution reserve before optional calls.
   An accepted same-objective plan bypasses template selection; an invalid nonempty
   plan returns mandatory-state failure. A late Level 0 permanently supersedes the
   old packet and permits at most one bounded ordinary-route re-prepare or explicit
   no-memory continuation without replenishing spent time.
3. Add bounded adapters over the existing EverOS, local template/procedure, and
   Atlas procedure services. Give each enabled store a real chance within its
   sub-budget and reserve independent capacity for candidate kinds. Normalize and
   gate before ranking: validate schema, provenance, scope/recipient, approval,
   designation/revocation, predicates/conflicts, route/capability, integrity,
   representation, and required live or frozen freshness. Deduplicate one logical
   revision across stores without a ranking bonus and apply deterministic
   specificity/tie rules.
4. Upgrade the five existing template families to use comparable sanitized
   representations and centrally configured thresholds. Direct fill may populate
   only typed trusted fields and must preserve structure and invariants. Keep lower-
   ranked eligible candidates available. Incomparable/low scores and invalid
   substitutions go to fresh ROOT planning.
5. For one eligible near match, create the bounded APC request and invoke the
   existing product harness through the narrow harness adapter using the run's
   explicit `apc_adaptation_binding`. Count queue, launch, correction, collection,
   validation, and cleanup against the enclosing deadline. Persist launch intent
   before the call and reconcile exact child identity before any retry. Validate
   parent/objective/template identity, permitted edits, artifact limits, result,
   and native usage. Missing or invalid binding, timeout, invalid result, ambiguity,
   or ROOT rejection returns to fresh planning without raw-provider fallback,
   recursion, implementation authority, or a fabricated parent outcome.
6. Keep ROOT plan acceptance distinct from APC proposal completion. Immediately
   before finalization, recheck plan-affecting procedure freshness. Render mandatory
   task/plan material first; include only coherent authorized optional items that
   fit. Never truncate approved meaning. Bind the full context integrity to the
   actual task, objective, repository base, accepted plan, rendered items, and role
   separation, scrub control credentials, and validate the actual task card/base at
   the existing dispatch seam.
7. Ensure all-off returns through the inherited harness path without initializing
   memory, creating optional context, launching APC, or scheduling background
   effects. Learned-strategy requests remain a deferred error without importing
   learner code. Update existing package/operator documentation only for the new
   callable preparation/finalization behavior.

## Dependencies and integration

The step consumes the specification's protected accepted experience and procedure
contracts. One `complex_writer` owns the product and narrow harness-seam changes in
a native outer-harness worktree so shared schemas do not split across writers. ROOT
integrates the result only after inspecting the actual diff and focused evidence.
STEP-05 consumes the resulting decision, dispatch, child-operation, final-context,
and compatibility contracts.

## Requirement-fit validation

- For BEHAVIOR-01, use a fake monotonic clock and controlled store adapters to
  exercise each fixed strategy, unknown/insufficient time, fair slow-store access,
  independent kind capacity, deduplication, live/frozen freshness, current-plan
  precedence, and late/repeated Level 0 correction. Assert deadlines and reserve at
  service entry, not merely filtered results. Also block store consumption,
  normalization, and final ranking under a real wall clock: a fake clock alone
  cannot prove that one absolute stage deadline releases the caller. Confirm that
  late work cannot change a returned packet.
- For BEHAVIOR-02, test all five seeded families with comparable and incompatible
  representations. Cover typed direct fill, lower-ranked selection, near-match APC,
  ROOT rejection, invalid edits/results, absent/invalid binding, timeout, ambiguous
  acknowledgement, exact reconciliation, cleanup, and fresh fallback. Deterministic
  provider processes can prove the harness contract here; they do not claim native
  model coverage.
- For BEHAVIOR-03, vary task, objective, base, plan identity, freshness, mandatory
  size, optional size, recipient scope, credentials, and repeated dispatch. Assert
  that mandatory overflow blocks, optional overflow omits whole items, stale
  plan-affecting guidance returns to ROOT, copied envelopes fail against the actual
  task card, and the same dispatch intent cannot launch twice.
- Add migration/contract tests that open accepted STEP-01 through STEP-03 state and
  preserve its decisions, reviewed experience, and procedure lifecycle. Run the
  existing bootstrap/resume/launch tests affected by the handoff changes and prove
  all-off and legacy task cards still use the ordinary path.
- Run the new and directly affected local tests in the worker lane. The complete
  local suite is deferred to the integrated candidate after STEP-05; unchanged
  accepted suites are not rerun solely to regenerate evidence. Before repairing a
  failed assertion, compare it with the specification and the observed behavior;
  a passing mock-only test does not establish the actual harness dispatch seam.

### Fast test suite

The existing independently selectable product tests are
`tests/local/preparation/test_step04_search_deadline.py`,
`test_step04_contract_corrections.py`, `test_bounded_preparation.py`,
`test_reuse_planning.py`, and `test_final_context_dispatch.py` (the latter four
also under `tests/local/preparation/`), plus
`tests/local/contracts/test_step04_handoff_plan_state.py` and
`tests/local/procedures/test_step04_migration_compatibility.py`. Select a file with
`python -m unittest discover -s <its-directory> -t . -p <its-filename>` from the
product worktree; newly added STEP-04 regressions join the same directory and
selector. For an actual harness-seam change, run
`python -m unittest discover -s harness/orchestrator_harness/tests -t harness -p "test_step04*.py"`
and select `test_memory_handoff.py` separately if its shared contract changed.
The deadline selector must fail on the reproduced two-second blocker with a
0.1-second allowance; launch tests must exercise the real bootstrap/resume/launch
consumers. Run only selectors whose inputs changed, then their direct consumers.

## Fast lane and failure recovery

An optional store, candidate, or APC failure falls back within the same objective
when mandatory state remains sound. An ambiguous child or dispatch holds only that
operation until exact reconciliation; it never authorizes another blind launch.
A mandatory identity, plan, privacy, or context-integrity failure returns to ROOT.
For a scoped code defect or failed check, ROOT keeps accepted slices and valid test
results, sends one coherent correction to the current owner/session/worktree when
usable, and reruns only the selected fast-suite file plus direct harness or storage
consumers whose inputs changed. Resume at that slice's review/integration point.
Use a fresh context only when the native session is exhausted or the current
workspace cannot safely continue, carrying forward its valid commit. Inspect
accepted STEP-01 through STEP-03 work only at the suspect compatibility seam; if
no material defect is found, leave it and its tests alone. If the affected scope
cannot be bounded, return to the normal STEP-04 integration check.
