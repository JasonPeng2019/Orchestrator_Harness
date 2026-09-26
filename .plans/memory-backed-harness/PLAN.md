# Coherent two-hour memory-backed harness MVP execution plan

## Execution status

Complete on pinned candidate `2544045a4ddf38622948dd3da8a9e6051c92a802`.
The real Atlas handoff passed, one actual priority-tier native Standard worker
materially used both the trusted EverOS stored skill and eligible Atlas
procedure, the consequential review returned PASS/ACCEPTED, the terminal
outcome was durably recorded, and exact local plus Atlas cleanup was verified.
The focused all-off zero-optional-call behavior remains passing. Deferred work
listed below remains outside this MVP decision.

## Outcome and boundaries

Deliver one supported Standard-strategy lifecycle in which a valid task is
prepared with both a trusted EverOS generated stored skill and a real eligible
Atlas procedure, the selected guidance reaches a ROOT-accepted privacy-safe
final context, the actual product harness runs a worker and consequential
reviewer, one terminal outcome is durable, and all exact owned resources are
cleaned. The accepted plan or worker result must contain machine-checkable use
of one distinct nonsecret marker carried only by each trusted source.

Also preserve one focused all-off lifecycle: the normal harness still completes
while optional EverOS, Atlas, and APC calls remain zero. Atlas is therefore a
core execution input, EverOS stored skills remain a core execution input, and
the harness spine remains functional end to end.

The implementation base is the clean joined product commit
`4263abf970d34c2b96957857eb38787b25775c09` on
`integration/checkpoint-20260925`. The superseded full plan and specification
are preserved at `../archive/2026-09-26-pre-two-hour-mvp/`; they retain
historical rationale but do not add work to this cut. Existing accepted
capability is preserved, not deleted.

This MVP does not finish operator commands, generalized readiness/recovery,
snapshot qualification, the full EverOS service-gating matrix, extra
strategies/routes/profiles, exhaustive recovery/usage, multiple worker tiers,
packaging, broad discovery, benchmarks, the learned selector, or post-MVP
repairs. Confirmed non-gating findings are recorded in `KNOWN_ISSUES.md` under
`NORMAL_OPERATION_ACCEPTANCE.md` and do not start repair loops.

Master-ROOT may edit planning files, integrate reviewed product commits, load
ignored credentials into the one authorized synthetic live process, run the
isolated native campaign, and clean exact owned resources. Lane writers may
edit only their declared product/test surfaces. No push, production data,
broad deletion, credential disclosure, or frozen outer-harness expansion is
authorized.

## Current system and target design

At `4263abf`, `PreparationService.prepare` in
`src/memory_harness/preparation.py` already resolves captured configuration,
runs bounded `SearchStore` inputs, selects trusted candidates, and can finalize
an accepted plan. `context.finalize_context` and `validate_final_context` bind
the selected payload to the task, plan, decision, base, checkpoint, execution
role, invocation target, and recipient. `MemoryRuntime.dispatch_finalized` and
the product `harness/orchestrator_harness` bridge validate that exact envelope
before native launch and can persist terminal evidence through
`MemoryRuntime.record_terminal_outcome`.

The EverOS path is already present in
`everos_adapters.make_everos_generated_skill_search_store`: a public EverOS
skill hit must rejoin the exact durable generated-skill candidate and its
current trusted procedure. The Atlas path is already present in
`atlas_adapters.make_atlas_search_store` and
`procedures.TrustedProcedureService.resolve_atlas`: discovery is followed by
exact approval/current/recipient/predicate validation. The blocking verification
gap is that `tests/live/atlas/test_live_trusted_procedures.py` currently builds a
3-dimensional `live-deterministic-embedding/v1` fixture, while the product path
uses `local-token-overlap/v1`, 512 dimensions, cosine distance, and sanitizer
`v1`; the live test also revokes and drops its only fixture, leaving nothing for
the native campaign.

The target keeps those existing product seams. Lane 3 proves the authentic
EverOS stored-skill lineage and search result. Lane 4 makes the disposable Atlas
test product-compatible and capable of an explicit, exactly owned handoff. Lane
1 proves both real candidate shapes survive one Standard preparation and safe
finalization. Lane 2 proves the product harness's all-off, enhanced launch,
review, outcome, and cleanup seams. Master integrates the four reviewed lane
tips, runs the real Atlas handoff, then runs one enhanced native task against
the same pin and cleans both resource scopes.

## Shared decisions and contracts

- **Fixed route:** Standard strategy, `ordinary` route, and one existing
  reliable template/accepted-plan path. No APC child is required for the
  enhanced campaign; all-off must make zero APC calls.
- **EverOS input:** one result from the accepted
  `everos_generated_skill` SearchStore, backed by an actual public-surface skill
  hit and exact durable candidate/procedure join. Required downstream fields are
  source kind, logical/revision identity, payload/content digest, exact scope and
  recipient provenance, and an `EVEROS_MVP_MARKER` value present only in its
  sanitized guidance. STEP-01 owns one reusable verification helper that stages
  this lineage into a caller-supplied temporary product store/EverOS root; it
  returns existing product identities and paths, not a parallel evidence record.
  STEP-02 uses it locally and STEP-14 uses it for a fresh inner campaign fixture.
- **Atlas input:** one result from the accepted `atlas_trusted_procedure`
  SearchStore, backed by real Atlas Vector Search plus exact post-read
  eligibility. Its representation is `local-token-overlap/v1`, 512 dimensions,
  cosine, sanitizer `v1`. Required downstream fields mirror the EverOS identity
  contract and carry a distinct `ATLAS_MVP_MARKER` only in sanitized guidance.
- **Material use:** selected IDs/digests and both markers appear in the durable
  final context. The accepted plan or native worker result must reproduce the
  two markers or perform their two distinct marker-directed actions. Merely
  logging search success does not pass.
- **Privacy:** credentials, raw approval evidence, control-plane data, and
  unsanitized source records never enter the worker context, result, manifest,
  or logs.
- **Atlas handoff manifest:** nonsecret JSON containing database, collection,
  index, partition/scope, publication/logical/revision IDs, receiver, query,
  route/facts, representation identity, Atlas marker, and cleanup owner. It
  contains no URI/key and is emitted only after all live eligibility assertions
  pass. The existing product contracts remain the evidence source; this is not
  a new product ledger.
- **Ownership:** the live collection name contains a fresh UUID. Default,
  assertion-failure, and abort behavior drops it. Explicit handoff mode retains
  exactly one eligible fixture until Master completes or abandons STEP-14, after
  which STEP-15 drops and read-checks that exact collection.
- **Acceptance:** only a reproduced supported-path/ordinary-compatibility or
  critical-invariant defect repair-gates. One fresh exact-tip reviewer examines
  each lane's combined candidate after its last implementation step; it is not a
  separate product step.

## Step map and execution order

Exactly four implementation lanes run in parallel because the four existing
lane-ROOTs have disjoint write ownership and the candidate/search/envelope
contracts at `4263abf` are already stable. Each lane-ROOT sequences only its own
steps through its existing frozen harness and returns one reviewed terminal
commit. No implementation lane waits for another lane to finish. Master is not
a fifth lane: it owns the serial join and live/shared-resource operations only
after the four reviewed tips exist.

### Lane 1 - coherent preparation and context

| Step | Produces | Depends on |
| --- | --- | --- |
| [STEP-06](steps/lane-1-context/STEP-06-standard-preparation-selects-both-inputs.md) | One bounded Standard preparation selecting both stable candidate shapes | Accepted shared contracts at `4263abf` |
| [STEP-07](steps/lane-1-context/STEP-07-final-context-binds-both-inputs-safely.md) | Durable worker-bound context with both IDs/digests/markers and no secrets | Lane 1 STEP-06 |

### Lane 2 - product harness lifecycle

| Step | Produces | Depends on |
| --- | --- | --- |
| [STEP-08](steps/lane-2-harness/STEP-08-all-off-harness-lifecycle-stays-inherited.md) | Focused product-harness all-off completion with zero optional calls | Accepted product-handoff contract at `4263abf` |
| [STEP-09](steps/lane-2-harness/STEP-09-enhanced-handoff-preserves-worker-input.md) | Focused enhanced handoff/prompt/result seam preserving both memory inputs | Frozen final-context/envelope contract at `4263abf` |
| [STEP-10](steps/lane-2-harness/STEP-10-consequential-review-fixes-one-durable-outcome.md) | Consequential review, durable outcome, and minimal attribution | Lane 2 STEP-09 |
| [STEP-11](steps/lane-2-harness/STEP-11-inner-run-cleanup-is-exact.md) | Exact inner-run retirement without collateral cleanup | Lane 2 STEP-10 |

### Lane 3 - EverOS stored skills

| Step | Produces | Depends on |
| --- | --- | --- |
| [STEP-01](steps/lane-3-everos/STEP-01-everos-stored-skill-lineage-is-authentic.md) | Authentic stored-skill/candidate/procedure lineage and reusable fixture builder | Accepted EverOS/store contracts at `4263abf` |
| [STEP-02](steps/lane-3-everos/STEP-02-everos-search-emits-one-trusted-input.md) | Trusted scoped EverOS SearchStore result and negatives | Lane 3 STEP-01 |

### Lane 4 - Atlas procedure handoff

| Step | Produces | Depends on |
| --- | --- | --- |
| [STEP-03](steps/lane-4-atlas/STEP-03-atlas-fixture-uses-product-representation.md) | Product-compatible 512-dimensional live fixture | Accepted Atlas representation contract at `4263abf` |
| [STEP-04](steps/lane-4-atlas/STEP-04-atlas-fixture-proves-eligibility.md) | Eligible, wrong-recipient, and revoked live cases | Lane 4 STEP-03 |
| [STEP-05](steps/lane-4-atlas/STEP-05-atlas-handoff-is-owned-and-cleanable.md) | Explicit manifest/retention/default-cleanup seam | Lane 4 STEP-04 |

### Master integration and live proof - not an implementation lane

| Step | Produces | Depends on |
| --- | --- | --- |
| [STEP-12](steps/integration/STEP-12-reviewed-lanes-form-one-local-candidate.md) | One integrated pin passing the focused local MVP gate | Lane 1 STEP-07, Lane 2 STEP-08–11, Lane 3 STEP-02, Lane 4 STEP-05, and four lane reviews |
| [STEP-13](steps/integration/STEP-13-real-atlas-produces-the-owned-handoff.md) | Real Atlas evidence plus one retained eligible manifest | Master STEP-12 |
| [STEP-14](steps/integration/STEP-14-native-enhanced-lifecycle-materially-uses-memory.md) | Actual candidate-harness worker/reviewer/outcome using both sources | Master STEP-12 and STEP-13 |
| [STEP-15](steps/integration/STEP-15-owned-resources-are-clean-and-mvp-is-decided.md) | Verified exact cleanup and final requirement-fit decision | STEP-13/14 attempts that created ownership |

All four lane heads launch together. STEP-12 reconciles any actual shared-contract
repair and reruns only affected consumers; this possible integration repair is
not a pre-emptive lane wait. STEP-13 and STEP-14 are serial because the native
campaign consumes the retained real Atlas fixture. STEP-15 always runs after any
live/native ownership was created, even when a dependent behavior remains open.

## Integration and whole-product validation

Master inspects each reviewed lane delta for ownership overlap, then integrates
Lane 3, Lane 4, Lane 1, and Lane 2 commits onto the clean integration worktree.
That order puts provider/fixture shapes before their joined consumers; a
conflict-free cherry-pick is not evidence, so STEP-12 runs the step-local focused
selectors on the actual joined bytes plus the existing exact final-context,
memory-handoff, terminal-outcome, privacy, and all-off checks named in its file.
No broad discovery, packaging, snapshot, operator, extra-strategy, or benchmark
gate is part of this MVP.

The local candidate cannot prove Atlas service behavior or native product-harness
execution. STEP-13 alone proves real Vector Search and retained-fixture ownership.
STEP-14 alone proves the actual candidate launches a worker and reviewer and
persists the outcome. STEP-15 alone decides cleanup by readback. A failure holds
only the claim and consumers that use its changed input; unrelated passing lane
evidence is retained.

For the authorized time-crunch recovery, STEP-14 may make one controlled local
restaging attempt without repeating STEP-13 only after readback proves the failed
bootstrap published no lane/run/PID/lease, its attempt-created child worktree and
branch are absent, and the exact outer staging worktree is unregistered. Preserve
the failed staging directory and intent as evidence, allocate a distinct retry
directory and fresh EverOS owner, and keep the same validated Atlas manifest and
collection. This is not authorization to replay a worker launch: any launch
intent, registered lane, or ambiguous process stops the retry and goes directly
to exact reconciliation/cleanup.

## Risks, assumptions, and unresolved decisions

- The live Atlas account/index permission or network may be unavailable. Preflight
  before mutation; if unavailable, STEP-13 and STEP-14's Atlas-dependent claim
  remain open while STEP-12 stays valid.
- The current product may already satisfy Lane 1–3 and most Lane 2 behavior. In
  that case those steps add only decisive focused coverage; product source is
  changed only for a reproduced gate defect.
- Lane 4's index creation is the only planned remote schema mutation and is
  confined to one UUID-owned collection/index. Never broaden cleanup if the
  manifest is missing; report the exact known owner and reconcile it.
- If a lane changes a shared candidate or envelope shape despite the frozen
  contract, stop only its direct consumers, assign the shared change to the
  current owner, and rerun the invalidated focused selections after integration.
- STEP-01/02's temporary local roots are never reused as native evidence.
  STEP-14 stages a fresh isolated EverOS root through their reusable helper;
  STEP-15 closes and removes that exact root after product processes release it.
- No unresolved user decision prevents execution. Benchmark execution remains
  deferred/not run; the learned selector remains deferred/not implemented.
