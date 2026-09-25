# STEP-05 - Terminal work and isolated operations remain durable and truthful

## Outcome

Implement [BEHAVIOR-04](../specification/behaviors/BEHAVIOR-04-terminal-work-remains-durable-and-accounted.md)
and [BEHAVIOR-05](../specification/behaviors/BEHAVIOR-05-operators-control-isolated-recoverable-runs.md).
The integrated product fixes one exactly linked terminal outcome, safely reconciles
enabled side effects and native usage, and lets an operator inspect, snapshot,
restore, and recover an isolated run without overstating completion, network
enforcement, or service availability.

## Scope and touchpoints

Extend `src/memory_harness/contracts.py`, `store.py`, `runtime.py`, `config.py`, and
`privacy.py`, adding cohesive reconciliation, usage, snapshot, and operations
modules as needed. Reuse the accepted experience/procedure services for side
effects. Add only a narrow completion bridge around the product harness's existing
`review.py` and memory handoff; harness acceptance remains its authority.

Extend `harness/orchestrator_harness/setup.py` and the actual provider-launch
configuration only for composition and network behavior that the existing staged
composer does not already satisfy. Reuse `operator_launch` as the process launcher.
Do not add a scheduler, duplicate review path, mandatory broad CLI, or replacement
setup system. Update existing READMEs where an operator needs the resulting setup,
readiness, recovery, or snapshot behavior.

## Implementation

Deliver this broad outcome through serial source-coherent assignments: linked
outcome/effect reconciliation first, then invocation usage, snapshot and namespace
recovery, and network/setup/operator wiring. Keep one writer over shared records
and runtime contracts, retain each useful completed slice, and combine corrections
only when they share one invariant and proof.

1. Validate that task, objective, decision, accepted plan, dispatch, run, and the
   harness review/acceptance pair identify the same execution before fixing an
   outcome. Preserve absent evidence, genuine terminal unknown, and known terminal
   failure as different states. Identical replay returns the original immutable
   outcome; a conflicting replay reports an integrity conflict without mutation.
   APC draft completion can never satisfy the parent execution outcome.
2. In one local transaction, persist the fixed outcome and deterministic intents
   for each enabled follow-on effect. Execute EverOS/Atlas or other external effects
   outside the transaction, then acknowledge them separately. On restart, scan the
   same durable pending/uncertain identities and use exact readback or source-backed
   idempotency before retry. A side-effect failure stays actionable but does not
   overturn valid harness acceptance or change the fixed outcome.
3. Store one usage record per actual invocation, including decision/task/source,
   stage, requested/resolved/native binding where available, native input/output/
   cache/reasoning totals where exposed, and a completeness reason. Parse provider-
   native receipts at their existing adapter boundary. Missing usage is incomplete,
   not zero; late data fills accounting without changing outcome. Deduplicate
   cumulative receipts, keep correction/resume calls distinct, link APC cost once,
   and separate outer development overhead from inner product execution.
4. Implement consistent snapshot export with SQLite's supported consistency
   mechanism and a quiesced or resolvable EverOS state. Include exact local records,
   procedure approval/current/revocation dependencies, representation/configuration
   identity, usage, provenance references, and pending operations needed for the
   claimed restored behavior. Verify integrity and namespace/owner identity before
   restore. Restore only to a fresh isolated namespace, or a specifically tested
   remap; reject corruption, missing critical dependencies, collisions, and silent
   merge before target mutation.
5. Resolve requested and effective `soft_guardrail_network`, `atlas_memory_only`,
   and `restricted_local` profiles before work. Enforce restricted-local at the
   Atlas/service adapter so task retrieval and retry make no Atlas call. Suppress
   provider-native web tools where supported and record remaining shell egress.
   Claim Atlas-only only when unrelated-destination blocking is independently
   enforced and verified on the actual launched payload; otherwise report the
   strongest truthful effective profile and reason.
6. Extend the existing setup composer to preflight command/provider ownership
   collisions before mutation, deterministically preserve harness and ROOT-suite
   behavior, validate the staged and actual launched payload, and make repeat setup
   idempotent. Detect later upstream overwrite and recompose. Use staged atomic
   replacement and retain a recoverable marker so interrupted composition blocks
   enhanced dispatch until validation or repair; ordinary unaffected behavior and
   unrelated roots remain untouched.
7. Expose setup/readiness, network-state inspection, pending reconciliation,
   snapshot export/import, and usage ingestion through a small public operations
   facade over these same domain services. Return build/root, composition, schema,
   service/binding, mode/enforcement, pending/uncertain state, and the next action
   without secrets. Use existing harness entrypoints for dispatch and completed
   procedure operations. Add a command wrapper only if Step 06 has an actual
   automation consumer that cannot call the facade directly.

## Dependencies and integration

This step consumes STEP-04's exact decision, accepted-plan context, child and worker
operations, and dispatch identity. One serial `complex_writer` owns shared product
state plus the narrow harness completion/setup seams. ROOT integrates the result
and freezes a candidate for STEP-06; the candidate's domain operations, not a new
test-only controller, are what the nested verification must invoke.

## Requirement-fit validation

- For BEHAVIOR-04, feed exact and mismatched review/acceptance pairs into the
  completion bridge and assert PASS/FAIL/BLOCKED fixation, absent versus terminal-
  unknown evidence, idempotent replay, conflict preservation, and no parent outcome
  from APC completion. Inject crashes immediately before/after outcome fixation and
  every side-effect boundary; restart and concurrent retries must complete each
  accepted effect at most once while retaining uncertain unsafe operations.
- Exercise usage with missing, late, cumulative, corrected, resumed, APC, ROOT,
  worker, and reviewer receipts. Assert no invented zeroes, no double count, exact
  outer/inner attribution, and no outcome mutation when accounting changes.
- For BEHAVIOR-05 snapshots, export a synthetic state with current/revoked
  procedures and a pending operation, restore into a fresh namespace, and prove
  equivalent eligibility plus safe pending recovery. Corruption, missing dependency,
  and identity collision must fail before partial target mutation.
- At the actual service and launch boundaries, exercise all three network profiles,
  including an unenforced Atlas-only request and a restricted-local recovery pass;
  assert the reported effective mode and that restricted-local issues no Atlas task
  call.
- Exercise setup with an ownership collision, repeated composition, simulated
  upstream overwrite, and interruption between staging and commit. Assert
  pre-mutation failure, idempotence, recomposition, enhanced-dispatch blocking, and
  validation of the payload actually handed to a worker.
- Test the public operations facade against temporary roots and service fakes and
  run affected harness tests. After ROOT integrates the step, run the full local
  command from `PLAN.md` once. Build/install/import a wheel only if package exports,
  dependencies, or packaging inputs changed. A failed assertion is compared with
  the contract and observed behavior before changing the product; setup and
  network claims require checks at the actual adapter or launched-payload boundary.

### Fast test suite

Add focused repository-native modules during implementation:
`tests/local/operations/test_step05_outcomes_effects.py` for exact joins, immutable
outcomes, crash/retry, and external acknowledgement;
`test_step05_usage.py` for per-invocation and incomplete usage;
`test_step05_snapshot.py` for consistent export, isolated restore, and pending
dependencies; and `test_step05_network_readiness.py` for real adapter gates and
the operator facade (the latter three under `tests/local/operations/`). Add
`harness/orchestrator_harness/tests/test_step05_setup_composition.py` for actual
staged/launched payload ownership and recovery. From the product worktree, run
one changed product module with
`python -m unittest discover -s tests/local/operations -t . -p <its-filename>`;
run the setup module with
`python -m unittest discover -s harness/orchestrator_harness/tests -t harness -p "test_step05_setup_composition.py"`.
These selectors must exist by STEP-05 completion and exercise the named production
seams; a fake-only network check cannot establish the launched profile. A change
to shared `contracts.py` or `store.py` also selects the existing direct contract
or migration tests that consume it. The complete local suite runs at the
integration point in `PLAN.md`, not after each narrow correction.

## Fast lane and failure recovery

A completion-bridge bookkeeping failure leaves harness acceptance valid and the
memory operation pending. A missing usage receipt affects accounting completeness
only. A failed external effect, snapshot, composition, or network enforcement claim
holds only the operation that depends on it and exposes an actionable state; it
does not replay an unsafe effect or mutate an unrelated namespace. Repair the owning
transition with the current owner/session/workspace, retaining valid STEP-04 and
STEP-05 outputs. Rerun the corresponding fast-suite module and only direct
consumers of the changed record, service gate, or launched payload, then resume at
the interrupted STEP-05 slice or candidate integration. If an effect's completion
is ambiguous, exact-read its owned identity before retry; if impact cannot be
bounded, use the normal integrated candidate check. A new worker or worktree is
reserved for exhausted context, unsafe overlap, or an already pinned candidate.
