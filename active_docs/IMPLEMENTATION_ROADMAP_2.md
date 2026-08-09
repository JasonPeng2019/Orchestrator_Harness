# IMPLEMENTATION_ROADMAP_2: Backward-Compatible Physical Firmware Acceptance

Status: next-run preparation green; S30 joined tip `6649cf2` awaits admission, S4/S5 and final gates remain  
Governing specification: `active_docs/GENERALIZATION_SPEC_2.md`  
Execution controller: `plans/general-coding-harness/EXECUTION_PLAN_2.md`

## 1. Delivery strategy

Extend the promoted harness in three coherent large steps, prove the accumulated candidate with non-hardware gates, then hand a fresh locked candidate to `F.C3.O`, a separate acceptance-orchestrator subagent, for the physical test project. The current outside root remains `ROOT-IM`, the implementation coordinator, throughout. `ROOT-IM` must not become the final target-project orchestrator.

After the completed S1-S3/S30 product work, one bounded supplemental S4 feature stage adds the two
candidate capabilities in `task-card-spec.md`: compact hash-bound task cards with explicit
orchestrator semantic acceptance, and one same-thread report-only retry for a structurally invalid
terminal artifact. The immediately following bounded S5 stage adds terminal thread/lane lifecycle,
no-worktree static review, and locked shared-event appends. S4 and S5 are completed before fresh
C0/C1/C2 so those final gates run only once on the actual release candidate.

The implementation uses the smallest useful architecture:

1. characterize and harden the existing legacy firmware path;
2. add a reproducible MCP-backed acceptance kit and test medium;
3. finish the backward-compatible release surface and final gates;
4. run one separately orchestrated physical project;
5. complete one logical accumulated safeguard run under the admission/resume rule and promote only on complete evidence.

Atomic edits and individual modules are tasks inside a large step, not separate execution cycles. Each large step receives exactly two back-to-back review/test/fix loops. Production coding is always singular and serial. Independent review, test-writing, and test-execution work may fan out to two lanes; no pool exceeds three.

Each loop operates on repair batches, not individual findings. Reviewers finish their full assigned
affected-surface sweep and return one complete exact-tip finding set. `ROOT-IM` triages the complete
set, the serial coder repairs all accepted production findings together, and no product review,
C0, C1, or aggregate registry reconciliation runs on an intermediate batch revision. Review effort
is release-blocking only for a supported or credibly reachable deployment defect with a concrete
negative effect on correctness, safety, security, reliability, recovery, required evidence, or
required user behavior; realistic latent authorization/fail-closed defects remain in scope, while
cosmetic, unreachable, behavior-neutral, or speculative improvements do not.

## 2. Fixed subagent assignments and root ownership

`ROOT-IM` is the current outside root session and implementation coordinator. It is not launched by
this roadmap and is not governed by the model/effort/tier assignments below. All other rows are
headless `codex exec` subagents with no model substitution.

| Role | Model | Reasoning | Service tier | Pool rule |
|---|---|---|---|---|
| `ROOT-IM` implementation coordinator | Current outside root session | not assigned | not assigned | exactly 1 host; not a launched subagent |
| `F.C3.O` acceptance orchestrator | GPT-5.6 Sol | high | Fast / `priority` | exactly 1, fresh subagent |
| Product or target coder | GPT-5.6 Terra | medium | Fast / `priority` | exactly 1 active, serial |
| Reviewer or test writer | GPT-5.6 Terra | medium | Fast / `priority` | 1 by default, 2 only for independent slices |
| Doer or test executor | GPT-5.6 Luna | high | Fast / `priority` | 1 by default, 2 only for independent slices |
| `F.C3.W` supplemental watcher reviewer | GPT-5.6 Terra | medium | Fast / `priority` | 0 or 1, isolated/read-only/non-gating |

Preflight proves the exact three model/tier launch combinations: Sol-high-priority,
Terra-medium-priority, and Luna-high-priority. A missing model is a blocking
preflight failure, not grounds for substituting another model.

## 3. Working locations and ownership

`ROOT-IM` created these isolated locations during completed preflight and now preserves their exact
recorded identities:

- product candidate: a new worktree and branch from harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`;
- firmware MCP candidate: a clean worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`;
- runtime: `plans/general-coding-harness/runtime/firmware-v2/`;
- evidence: `plans/general-coding-harness/evidence/firmware-v2/`;
- final inactive runtime: `plans/general-coding-harness/runtime/promoted-firmware-v2/`, absent until
  promotion;
- disposable final target: a fresh Git repository under the current immutable
  `acceptance/attempt-NNNN/target/` namespace, not the harness or server repository;
- each physical lane: a separate MCP process, `.firm` state root, artifact root, log root, and board assignment.

The reserved coordinates are:

- harness: `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/` on new
  branch `firmware/v2-candidate`;
- MCP: `plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate/` on new branch
  `firmware/v2-mcp-candidate`.

Both were created only after their path and branch absence was checked. On resume, exact identity
and cleanliness replace the original absence check; neither is recreated or silently substituted.
The reserved promotion ref `progress/v1.2` remains absent until promotion. Any new collision is
preserved and escalated rather than cleaned or reused.

The existing dirty `Firmware/BYO-Firmware-MCP` checkout, `Firmware/Firmware resources/`, prior V1/V2 acceptance runtimes, promoted commit `4699d27`, and frozen rollback commit `287ea537` are read-only inputs.
The 13 retained linked harness worktrees from the completed project, the reserved candidate, and the
reserved MCP worktree are protected state. Other V2 lane worktrees remain protected until S5 is
accepted; after that, only lanes satisfying C75's exact evidence/revision/cleanliness/zero-process
checks may retire. The physical implementation runner is
`stable-general-harness-runner@4699d27`; `.git/modules/harness-in-progress` is only their retained
shared Git store. Never rename or remove that common directory while these worktrees exist.

All implementation-lane controller dispatch uses `.codex/scripts/stable_runner.py` and its immutable
runner lock. The launcher must reject a wrong/dirty/attached checkout, hostile lane/candidate import
paths, conflicting preloaded modules, and proof/projection outputs inside the stable checkout. A
stable-compatible projection does not transfer candidate-only finding-gate enforcement to the old
runner; ROOT validates the original artifacts until final candidate testing proves the new gate.

## 4. Preflight gates

Preflight is a gate, not a full QA cycle. It has completed for this execution. The numbered list is
retained as provenance and must not be rerun wholesale on resume; repeat only mutable checks mapped
to the next gate or a changed dependency.

1. Re-read `HANDOFF.md`, this roadmap, the specification, `EXECUTION_READINESS_2.md`, the execution plan, and all applicable `AGENTS.md` files.
2. Record the current session as `ROOT-IM`; do not apply a child-agent model gate to it and do not
   create a nested replacement implementation manager.
3. Confirm the promoted harness and frozen rollback identities and cleanliness.
4. Confirm the outer repository's unrelated changes and record the preservation boundary.
5. Confirm the two reserved paths and branches are absent. Record the dirty firmware-server checkout
   without altering it; create both isolated worktrees at their exact pins.
6. Verify all destination entries in `Firmware/Firmware resources/SOURCE_MANIFEST.csv` by byte count
   and SHA-256. Record that historical source paths are unavailable provenance rather than claiming a
   live source comparison.
7. Resolve and record exact toolchain, device-pack, datasheet, fixture, server, and harness hashes.
   Derive a new per-lane `PYTHONPYCACHEPREFIX`; never use the absent historical cache path.
8. Prove the exact headless launch shape, including approval/sandbox bypass, hook-trust bypass,
   ignored user configuration, JSONL evidence, exact model/effort/tier, isolated root, and durable
   thread identity for resumable lanes.
9. Prove an explicit per-lane-controller clean-server MCP declaration works without global user configuration.
   Reject unreviewed `.env` files, clear ambient probe/target overrides for inventory, and bind each
   board-owning lane only to its exact assigned stable UID and reviewed target/profile.
10. Run read-only electronic discovery through that MCP boundary; prove stable identities for STM-A, STM-B, NRF-A, and NRF-B and rediscover current serial routes.
11. Resolve the retained `P.05` notation from authoritative evidence before admitting a DIO2-dependent action. Do not infer it.
12. Resolve authoritative RF admission evidence for module variant, antennas, supply/current,
    configured 915 MHz operation, power, bandwidth, bounded duty cycle, and applicable constraints.
13. During preflight record the canonical non-authorizing draft and validate only the intended authorization schemas/authority boundary; do not implement product logic here. S2 exclusively implements and tests the ordered proposal, independent signed O decision, derived authorization, expiry-through-result, exact cleanup flow, and `MCP_METHOD_POLICY.json`; C1 later validates and locks their completed hashes. The S2 contract below uses create-new/no-overwrite artifacts, new IDs for retry/fresh attempts, and only explicit user direction may extend delegated time with fresh C1.
    - Treat the canonical JSON object in `goal.md` Section 11 as the entire issuance. S2 builds default-deny `MCP_METHOD_POLICY.json` with exact method/version, allowed parameter schema/ranges/safe flags/duration maximum, and prohibited method/parameter/side-effect predicates; C1 later locks it. A destructive-capable method denies unless technically constrained/proven safe for the exact call; labels cannot override prohibition. Every mutating plan requires positive bounded `max_operation_duration_seconds`. Proposal, O decision, authorization, dispatch, and result bind exact method/version, server revision/schema, policy/evaluation hashes, arguments, plan/duration, stable probe UID, target/profile, current route/null, and immutable identity/claim paths/hashes; harness pre/post validates and mismatch denies success.
    - Two-stage key release: create nonce/keypair/launch intent; spawn O with nonce and no key; write exact post-spawn identity; exchange identity-hash acknowledgment over the inherited pipe; write create-once `ORCHESTRATOR_KEY_RELEASE.json`; only then send key/discard ROOT copy. Signed ready/work/decisions bind release hash/time and earlier records; never rewrite, and failure requires a fresh attempt.
    - At every mutating dispatch, hash all five docs and require the live set to be covered by the operative C1 plus valid append-only change dispositions. After validation create immutable `dispatch-admissions/{CALL_ID}.json` binding authorization hash, fresh five hashes, revalidated fields, monotonic clock/start/deadline; dispatch/result reference it and never mutate authorization. Enforce the declared deadline with cancellation/exact cleanup and `INDETERMINATE_TIMEOUT`/no-success on overrun. An unclassified mismatch expires calls/emits `GOVERNING_INPUT_CHANGED`; ROOT classifies the changed domain and refreshes only the lock/consuming gates needed. Keep the registered ROOT watcher in flight; change uses `INDETERMINATE_EXPIRED`.
      Register that non-agent helper's exact identity/current hashes/heartbeat in `topology/GOVERNING_INPUT_WATCHER.json`; it writes only its evidence and must exit/reap into topology shutdown.
14. Confirm destructive recovery actions remain excluded.
15. Launch one no-op headless smoke for each exact Fast launch combination: Sol-high-priority,
    Terra-medium-priority, and Luna-high-priority; record model, effort, tier, thread,
    PID-plus-creation, exit, and final-message identity.
16. Create the fresh event log, manager-signals root, implementation passed registry, out-of-scope ledger, and `PARALLEL_CHECKPOINT.md` without starting product work. C1 later freezes that registry; C3 uses only attempt-local registries.
17. Run `scan --no-write`; require no unowned active candidate process, ambiguous claim, stale actionable relay, or reused acceptance state.
18. Record the existing full-gate evidence for unchanged `4699d27`. Do not rerun it during preflight.
19. Record the candidate-root gate protocol and focused commands. S3 must materialize and test the
    exact safeguard launcher; the ordinary outer verifier's fixed `stable-general-harness-runner` target
    cannot be credited for candidate-only code.

## 5. Standard large-step cycle

Every large step uses this fixed sequence:

1. `ROOT-IM` gives one Terra-medium-Fast coder the complete bundled step.
2. After integration, independent Terra-medium-Fast reviewers inspect their full disjoint assigned
   surfaces, continue after discovering a defect, and return one complete evidence-linked finding
   set for the exact reviewed tip.
3. `ROOT-IM` rejects any finding that is not reproducibly `CODEBASE_BREAKING`,
   `FUNCTIONALITY_BREAKING`, or demonstrably `WORTH_FIXING` on a supported or credibly reachable
   deployment path with a concrete negative product consequence. For accepted findings it weighs
   problem/no-fix impact against the smallest repair's complexity, regression risk, verification
   cost, and lower-risk alternatives. The same coder repairs every accepted production finding from
   that complete result as one serial minimal batch; no review or reconciliation occurs on an
   intermediate repair commit.
4. Independent Terra-medium-Fast test writers add only missing specification and regression
   coverage, including coverage implicated by the accepted batch. Test changes merge in
   deterministic order after ownership checks to form one frozen joined tip.
5. Run the shortest dependency-invalidated smoke IDs on that tip. A failure returns immediately to
   its owning coder or test writer before remaining execution or any revived product review.
6. After smoke passes, independent Luna-high-Fast doers execute the remaining focused stable shards. Any
   reviewer whose surface changed after its complete review may perform the required targeted
   exact-tip confirmation in parallel; the step waits for both results before advancing.
7. `ROOT-IM` applies the same complete finding/admissibility decision to the joined results, batches
   every accepted production/test repair, and reruns only dependency-invalidated surfaces and IDs.
8. Administrative result-envelope, metadata, evidence-field, command, or path corrections that do
   not change operative product/test meaning resume in the same lane and do not reset product
   review or green tests. A strict test-only fast lane applies only to synthetic fixture/setup or
   test-metadata diffs with known failed IDs and a deterministic checklist proving unchanged
   production, policy, contract, locked configuration, oracle, assertion strength, expected outcome,
   stable ID, and coverage obligation. Use the same test-author continuation and rerun exactly those
   IDs once before unrelated work; do not create C0, ordinary review, or reconciliation. A change to
    expected behavior, coverage obligations, or an operative test/evidence contract is material.
   These continuations are available only while the logical task remains unaccepted. After semantic
   acceptance, the thread is terminal; unrelated later work starts from a new bounded task card.
9. Before an expensive selected executor set with custom inner-process evidence, run one local
   recordability preflight that performs no real product/MCP/hardware work and validates a complete
   sample record: stable ID, inputs, worker/process identity, timing, command, outputs, and outcome.
   Bind its green result to the runner/procedure/configuration/environment fingerprint and reuse it
   until that fingerprint changes. A preflight/report procedure defect stays in the same lane; reconstruct complete raw evidence or
   rerun only the affected ID on the same lock. If a selection reports only fixture/mock/environment
   defects, batch every classified correction and rerun that selection once.
10. The second loop immediately rechecks only dependency-invalidated surfaces and IDs under the same
   batch/smoke/parallel-join rules. Unchanged green evidence remains credited.
11. After the batch tip is accepted, reconcile its dependency map, green stable IDs, and aggregate
   evidence into the implementation registry once; raw lane evidence remains preserved throughout.
12. Checkpoint A records that exact accepted revision, residual scope, clean process state, and the
    unlocked next step.

There is no arbitrary iteration cap. Repeated same-signature failure, oscillation, only-extraneous scope churn, or unrecoverable error is escalated with evidence; difficult work alone is not a reason to stop.

The gate is fail-closed on missing/stale/cross-lane finding artifacts and PASS-with-gap results. Its
closed schema requires exact evidence, affected requirement/behavior, observed/expected behavior,
reproduction, impact/no-fix consequence, smallest sufficient fix, implementation complexity,
regression risk, verification cost, alternatives, and the submitter's reasoned conclusion that the
problem outweighs the fix. Code validates structure and identity; the owning orchestrator validates
truth and tradeoff. Style-only, speculative, cleanup, or merely nicer suggestions are retained only
as rejected non-findings and cause no edit, reset, relock, or retest.

For this gate, credible impact requires a supported or realistically reachable deployed trigger and
a concrete consequence for correctness, safety, security, reliability, recovery, required evidence
integrity, or required user-visible behavior. Latent authorization and fail-closed defects remain
eligible when such a trigger exists. Cosmetic, unreachable, behavior-neutral, and purely theoretical
issues do not enter a repair batch.

## 6. Large step S1: Legacy firmware lifecycle and compatibility

### Product work

1. Capture accepted schema-less firmware invocation and result fixtures from the current implementation and retained evidence.
2. Characterize policy-bound prompt verification, filenames, event log location, model settings, server snapshot, leases, board tokens, MCP declarations, and resume behavior.
3. Characterize coding-versus-firmware dispatch and reject ambiguous or cross-shaped results.
4. Audit exact worker/helper/MCP process identity and lifecycle reconciliation for active, waiting, checkpointed, exited, unknown, and cleanup states.
5. Audit exact request/relay hashes, arguments, server snapshot, expiry, and manager ownership.
6. Audit board and generic claim ownership, same-resource serialization, independent-resource concurrency, stale handling, and release-after-reap behavior.
7. Factor a shared primitive only when identical semantics are proven by tests; otherwise keep the firmware and coding adapters separate.
8. Add compatibility, lifecycle, event, request/relay, resume, claim, and dual-route tests.
9. Record a protected baseline manifest of the original successful general-harness unit tests, map shared production modules to those IDs, and run every dependency-invalidated original unit test after shared changes.
10. Add focused cross-route unit tests proving firmware compatibility work cannot change coding invocation, result, claim, event, repository, or cleanup behavior.
11. Reject test deletions, skips, expected failures, or weakened assertions used to hide a general-harness regression; require equal-or-stronger replacement coverage for any structural test move.
12. Update the firmware contract documentation without changing legacy caller requirements.

### Exit

S1 passes when existing fixtures remain accepted, malformed or ambiguous shapes fail closed, resource and MCP state is honest, every dependency-invalidated original general-harness unit test and every new cross-route unit test is green, no original coverage was weakened, all stable tests are registered, and no physical board was mutated.

## 7. Large step S2: MCP-backed acceptance kit and test medium

### Product and test-medium work

The controlling S2 repair contract is the immutable
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
(SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`). Its closed method policy,
finite retained-session state machine, predecessor-bound guarded plan/action flow, per-call
delegated-scope/action/effect enforcement, five-key final C1 authorization support, create-once
server-limitation API, and `AUTHORIZED_SERVER_LIMITATION` seed route are implemented and preserved
at candidate `659dd03` with their green credits. The later accepted pre-C3 gap requires the bounded
candidate-owned control-plane/provenance repair preserved on product lane `e5ced272`; it must be
joined with adapted CP04 coverage and pass the optimized batch/smoke/review/execution flow before
fresh terminal C0. Keep the pinned server unmodified and
unlaunched during this repair.

1. Add a version-pinned acceptance manifest containing harness, server, fixture, datasheet, pack, and toolchain identities.
2. Add per-lane MCP launch templates with isolated process, `.firm`, artifact, log, board, and serial-route bindings.
3. Add exact evidence schemas for host preflight, setup, build, flash, behavioral assertions, checkpoint/resume, contention, cleanup, and final result.
4. Add the Four-Board Dual-Family Firmware Lab charter and bounded STM32, nRF52 BLE, nRF52 LoRa, and concurrent-campaign sprint definitions.
5. Add deterministic protocol definitions, target-role manifests, stable test IDs, dependency fingerprints, selective invalidation rules, and machine-readable `RESULT.json` requirements.
6. In S2 add the prospective `TARGET_SEED_MANIFEST.json`, enumerating hashes for exactly
   `TARGET_CHARTER.md`, `PINNED_INPUTS.json`, `TEST_CONTRACT.json`, and `EVIDENCE_SCHEMA.json`.
   C1 later locks those five prepared files. They form the read-only initial C3 repository;
   application source/tests/build files
   and target-repository-local configuration created later are target-local.
7. Adapt only the applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and D30-D36 intentions from the supplied firmware experiment catalog.
8. Mark the rest of A20-A26, B01-B39/Q40, Q41, and destructive/try-last appendices as extended, non-gating qualification.
9. Add synthetic MCP processes and disposable repositories that exercise launch, relay, result, cleanup, and failure classification without hardware.
10. Add dry-run validation that every physical operation is expressed as a harness-brokered MCP call with a live plan/permission step. Only the candidate lane controller receives the physical MCP launch/stdin capability; reject target/O endpoint inheritance plus direct probe, serial, or MCP bypasses.
11. Keep the clean MCP server worktree immutable. Add deterministic classification and evidence for
    a genuine pinned-server defect/incompatibility, plus a bounded substitution path: supported
    partial MCP proof first, then a focused test against the implicated pinned-server component, then
    a synthetic candidate boundary unit only when stronger proof is impossible. Never repair or
    repin the server in this project.
12. Add the smallest closed retained-Server-Run control plane: a create-once session request/open
    record, one exact board claim and MCP process retained across separately authorized calls,
    policy-defined phase transitions, consecutive predecessor-bound call chains, signed O normal-
    close intent, and terminal closed/aborted evidence with exact drain/reap/claim release. Protocol
    bootstrap is fixed and side-effect-free; setup/validate/plan/action/observe/return-state calls
    each keep their own proposal, O decision, authorization, admission, result, and deadline.
13. Extend the default-deny method policy with one action class, a closed parameter schema/ranges,
    safe flags, prohibited predicates, maximum duration, and session role/allowed transitions for
    every supported exact method/version. Enforce the canonical delegated user scope and deny an
    unmapped fixture, action class, parameter, transition, expired binding, or prohibited effect.

### Exit

S2 passes when a fresh agent can materialize the target project from the kit, all non-hardware MCP/
lifecycle simulations--including retained multi-call session, sequence rejection, scope/policy
denial, signed close, abort cleanup, and exact reap--are green, no direct-hardware bypass exists,
source/evidence ownership is unambiguous, the exact pre-C1 executable contract is implemented, no
target seed authorizes server repair/repin, focused policy/session/limitation regressions are green,
and the physical board state remains unchanged except for separately authorized read-only discovery.

## 8. Large step S3: Release integration and backward-compatible operator surface

### Product work

1. Integrate the acceptance kit with the harness quick-start and configuration surface while keeping coding invocation V1 and schema-less firmware invocation intact.
2. Provide one legacy firmware example, one coding example, and one dual-path manager example.
3. Document headless agent launches, exact model roles, Fast as `service_tier="priority"`, no-substitution behavior, and the `ROOT-IM`-plus-three Codex-agent concurrency cap; `C3-HARNESS` controller processes are system-under-test processes, not agent slots.
4. Document the separate `ROOT-IM` implementation-coordination and `F.C3.O` acceptance-orchestration responsibilities.
5. Add operator commands for fresh runtime creation, `scan --no-write`, `watch --until-actionable`, exact `ack --event-id`, checkpoint/resume, passed-registry inspection, and exact shutdown verification.
6. Add disposable end-to-end integration coverage proving coding and firmware lanes coexist without event, claim, result, or cleanup cross-contamination.
7. Add release-evidence templates for final review, acceptance watcher, topology audit, criteria audit, protected state, promotion, and completion.
8. Materialize and test the candidate-root safeguard launcher. It must bind Ruff, formatting,
   BasedPyright baseline mapping, compilation, and test commands to the reserved candidate rather
   than silently checking a candidate or legacy alias.
9. Remove only obsolete material made incorrect by this retrofit; do not broaden the framework.

### Exit

S3 passes when a new operator can run both paths from the docs, old firmware fixtures require no migration, all disposable integration gates are green, and the candidate is ready to lock at final Checkpoint A.

### Mandatory supplemental S4 before C0

1. ROOT writes an exact feature plan bound to `task-card-spec.md` and the joined S30 candidate tip.
2. One Luna-high-Fast implementation doer adds task-card validation/prompt rendering, the durable
   semantic-acceptance-pending event and verdict gate, plus one same-thread report-only structural
   repair retry. The frozen stable runner is unchanged.
3. One independent Terra-medium-Fast reviewer checks the complete focused diff and runs the contract
   unit tests. One disjoint Luna-high-Fast doer runs those units plus the disposable fake-Codex smoke.
4. ROOT triages the complete result once. Accepted defects return as one bounded batch. S4 passes
   only when no dependent lane can start before a hash-bound orchestrator verdict, strict criteria
   cannot be tolerated, and the report-only path cannot edit code, rerun tests, fabricate evidence,
   or retry more than once.

### Mandatory supplemental S5 after S4 and before C0

1. Only after S4 is accepted, ROOT writes one exact S5 feature plan bound to the accepted S4 tip,
   `task-card-spec.md`, and C74-C77. The frozen stable runner remains unchanged.
2. One Terra-medium-Fast product coder implements the smallest coherent candidate change:
   accepted task threads become terminal; accepted lanes can be removed from active discovery and
   safely archived; static read-only lanes can use an exact immutable source view plus separate
   result root without a linked worktree; and every shared event-log append waits on one
   cross-process lock.
3. One independent Terra-medium-Fast reviewer audits the complete focused diff for correctness,
   compatibility, evidence retention, Git/path safety, and unnecessary complexity. One disjoint
   Luna-high-Fast doer runs focused units and disposable practical tests.
4. The practical tests prove: same-task `CONTINUE`/report-only/strict-fast-lane resumes remain
   available while an accepted thread rejects unrelated reuse; a terminal lane leaves active scans
   only after hashes and revision identity are retained; a static reviewer creates no linked
   worktree and cannot contaminate the source/result of a peer; source-local tests still receive a
   worktree; and concurrent processes produce complete, non-interleaved event records while the
   second writer waits for the first lock holder.
5. ROOT pools reviewer/test findings once and returns accepted product gaps as one bounded repair
   batch. After acceptance, ROOT performs one audited retirement pass over eligible terminal V2
   lanes only. Protected historical worktrees, dirty/ambiguous lanes, live paths, and unpreserved
   evidence are excluded. The exact accepted S5 tip then enters the shortest affected smoke and
   fresh C0/C1/C2 route.

## 9. Final automated phase C0-C2

1. **Pre-C0 join:** finish all known production and test adaptation, form one frozen joined tip, and
   run its shortest already-required dependency-invalidated smoke IDs. Do not launch C0 for an
   intermediate or known-red revision.
2. **C0 fresh review plus focused execution:** after smoke passes, launch a new Terra-medium-Fast
   final reviewer with no prior step context while Luna-high-Fast doers run the remaining focused IDs on
   that exact tip. The reviewer completes the whole requirement, compatibility, safety, critical
   control-path, diff, original-unit-regression, and over-engineering sweep even after finding a
   defect, and returns one complete finding set. It compares baseline/candidate test manifests and
   checks deletion, skip, expected failure, weakening, and unmapped shared changes. Join both sides.
3. Triage the complete finding/test result. If production changes, route every accepted finding as
   one bounded serial repair batch, adapt affected tests, rerun the smoke, and then obtain a fresh
   C0 on the new joined tip. A qualifying strict test-only fast lane correction records its
   deterministic eligibility checklist and reruns exactly the failed IDs once in the same
   test-author continuation before unrelated work; it does not create C0, ordinary review, or
   reconciliation. Administrative corrections resume without a new product review or test rerun.
   Expected-behavior, coverage-obligation, or
   operative test/evidence-contract changes are material and require the full route. This focused
   continuation is pre-C3 only; post-C3 invalidation rules are unchanged.
4. Reconcile the dependency map, passed registry, and aggregate evidence once for the accepted
   batch tip. **C1 lock and audit** starts only after the clean terminal C0 and exact-tip focused-test
   join: allocate fresh UUID/directory; copy canonical user scope verbatim; lock its hash plus
   default-deny method/parameter policy; write authorization then C1 lock/hash in non-circular order.
    Target-local source/config is excluded. A post-C1 governing change is classified by changed
    lock-input domain and invalidates only consuming gates. Hardware-authority/in-flight-mutation
    changes suspend calls immediately; product-behavior changes use the owning material route;
    test-procedure or outer-topology changes rerun only dependent test/rehearsal/attempt work. Use the
    documented conservative fallback only when the change cannot be classified. Confirm zero
    managed process/claim.
5. **C2 final test loop:** run the final disposable non-hardware project, synthetic MCP lifecycle,
   dual-path compatibility, event/acknowledgement, checkpoint/resume, cleanup gates, and every
   original general-harness unit test invalidated by the accumulated diff. Reuse only demonstrably
   unchanged green IDs from the registry.
6. If C2 repair changes any C1-locked candidate, server pin/configuration, kit/lane/MCP template,
   fixture binding, test/evidence contract, authorization, or other implementation input, create a
   new C1 Checkpoint A and rerun dependency-invalidated C2 IDs. Production, policy, expected-
   behavior, coverage-obligation, or other operative changes return to their owning implementation
   step and full fresh C0. A qualifying strict test-only fast lane correction may proceed to the new
   C1 only after its checklist and exact failed-ID rerun; it never inherits the old C1. An environment-
   only rerun with no locked-input change does not require a new lock. C3 starts only from the latest
   green C1/C2 pair.
7. Do not run the full accumulated safeguard here.

### C3 host-only rehearsal gate

Before allocating a C3 attempt namespace, launching O or the required deterministic helper, creating a target repository, starting the
MCP server, or claiming hardware, run the exact-C1/C2 candidate through one disposable host-only C3
rehearsal. It covers launch admission, retained-session authorization, process/identity binding,
duplicate-assignment refusal, watcher correlation, recovery/idempotence, cleanup, and terminal
closure. Reuse only dependency-unchanged green rehearsal IDs. A candidate failure returns through the
material repair/relock route; fixture/executor defects remain in their lane. A green rehearsal is a
mandatory C3 admission prerequisite, not a physical-pass substitute.

## 10. Final practical phase C3: separately orchestrated hardware project

### Topology

The rules in this subsection are operative and supersede older W-terminal-report language elsewhere
in the roadmap. ROOT uses `.codex/scripts/c3_outer_support.py` for the external lifecycle and
`.codex/scripts/c3_watcher_helper.py` for deterministic observation,
finding classification, evidence closure, support-failure disposition, and safe cleanup. Closed
historical attempt scripts are never imported as mutable production support.

1. `ROOT-IM` creates O nonce/key/intent; spawns fresh Sol-high-Fast O with nonce/no key; records exact
   post-spawn identity; receives identity-hash acknowledgment; records key release; only then sends
   private capability and accepts release-bound signed ready/work/decision. ROOT directly launches
   the deterministic non-agent helper and records its create-once launch/identity before helper
   readiness. `F.C3.W` is optional supplemental review and is never acceptance-critical.
2. Before either launch, allocate the next monotonically increasing immutable runtime/evidence pair
   `acceptance/attempt-NNNN/`: one greater than the largest number on either side, or `attempt-0001`
   only when neither side has an attempt. Both chosen paths must be absent; a one-sided path or
   collision stops for preservation/triage. Give it separate `target/`, `hil/`, `events/`, `claims/`,
    `manager-signals/`, and `.agent-workspace/` roots. Preserve all prior attempts read-only; never
    clear, overwrite, fill a numbering gap, or reuse them.
   Create fresh attempt-local `passed-tests.json` inside the attempt runtime. Never write the
   C1-locked implementation registry; re-credit unchanged prior results only by immutable evidence
   path/hash and dependency fingerprint references.
3. `F.C3.O` owns target-project decisions and operates `C3-HARNESS`, the candidate harness control plane and its exact controller processes. `C3-HARNESS` is the system under test, not a Codex-agent role or slot.
4. The helper writes only attempt-local observation evidence. ROOT validates ready/heartbeat/cursor,
   pools ordinary findings, requests immediate stop only for the three exact safety conditions, and
   after candidate shutdown writes `WATCHER_OBSERVATION_CLOSE.json` from primary or approved backup
   sources. A helper/support failure rolls only incomplete support work unless product behavior is
   no longer determinable. ROOT separately monitors O at 30/90 through result/exit and writes exact
   `ORCHESTRATOR_EXIT.json` or loss evidence.
5. Exactly one target agent is active at a time. Optional `F.C3.W` may occupy the otherwise free
   review slot but is not needed; `C3-HARNESS` controller processes do not consume agent slots.
6. `F.C3.O` serially submits these assignments to `C3-HARNESS`, which launches each target worker through `codex exec`, records its exact lifecycle/evidence, and returns its result. Direct target-worker launch by `F.C3.O` is prohibited:
   - a Terra-medium-Fast target test writer;
   - a Terra-medium-Fast target coder;
   - a Luna-high-Fast test doer/hardware executor;
   - a Terra-medium-Fast target evidence reviewer.
7. `ROOT-IM` monitors only high-level progress, exact helper stop records, pooled observer findings,
   and terminal acceptance status; it
   does not assign target work, decide target application repairs, or repair the pinned MCP server.

### Sprints

1. **P0 — host and routing:** prove MCP handshake/schema, strict plans, isolated roots, toolchain availability, all four stable board identities, current serial routes, fresh setup, and returning-state behavior.
2. **P1 — STM32 pair:** tests first, then implement and run the controller/responder images; prove deterministic I2C2 protocol, UART evidence, reset/reconnect, debug observability, bounded error recovery, and ordered sustained traffic.
3. **P2 — nRF52 pair:** tests first, then implement the bounded dual-mode codebase; prove deterministic BLE GATT exchange and legal-band low-power CoreSX1262 ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence.
4. **P3 — concurrent harness proof:** keep one `F.C3.P1` doer agent active under one candidate assignment while it requests two concurrent non-agent physical lane process groups: `P3.STM` owns STM-A/STM-B and `P3.NRF` owns NRF-A/NRF-B. During normal operation only `C3-HARNESS` creates, starts, stops, and reaps those groups and owns both lane/controller/process/claim/event/cleanup records; each lane has distinct MCP, `.firm`, artifact, and log roots. `F.C3.P1` may request and operate them only through assigned harness interfaces and cannot spawn them. Prove independence, same-resource contention, exact relays, a same-thread/path resume, one predeclared intentional target-code defect/fix, selective retest, and no cross-resource mutation. Before injection `F.C3.O` records the exact source-controlled, non-destructive defect and expected behavioral failure. It may affect only target application source and must fail through the normal test path before repair.
5. **P4 — shutdown and evidence:** close boards/candidate state; ROOT stops/reaps the deterministic
   helper and writes `WATCHER_OBSERVATION_CLOSE.json`; then inventory both attempt roots. The
   manifest lists every in-domain file except self/result/topology and uses `external_references` for
   canonical C1/delegated/governing paths/hashes outside those roots. No later in-domain write. O
   creates result in 90 seconds; C4 independently enumerates both roots and verifies external
   references. After O exit ROOT writes `ORCHESTRATOR_EXIT.json` and separately closes topology.
   The shutdown file inventories/hashes every other regular `topology/` file but excludes itself; symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and separately hashes/verifies shutdown.
   Manifest creation freezes all external-reference paths/hashes through completion. Any later doc
   change or editorial-chain append invalidates that C3 result; preserve it, apply the normal
   classification, and use a fresh attempt before C4. Never accept a stale editorial-chain prefix.

### Failure routing

- Mistakes by `ROOT-IM`, `F.C3.O`, or a target worker--including bad assignment, prompt, order,
  command/config path, target edit, invalid MCP call, triage, or result-envelope content--return to
  their owning lane for targeted correction or same-thread resume. They are expected adverse
  workload, not evidence of a candidate/watcher defect. They do not emit `ABORT_REQUIRED`, reopen a
  green implementation step, invalidate C1, or erase unrelated green credits. A fresh C3 namespace
  required solely because immutable evidence can no longer close is an attempt rollover, not a
  candidate reset; relock occurs only when a C1-locked input changes.
- Target application, compiler, target-test, target-repository-configuration, or invalid-MCP-call failure stays inside the acceptance project only when it changes no C1-locked input. `F.C3.O` submits diagnosis/repair assignments through `C3-HARNESS` and reruns only affected IDs. A required locked kit/template/configuration change leaves this route.
- A reproduced pinned MCP server defect/incompatibility is reported by `F.C3.O` as
  `AUTHORIZED_SERVER_LIMITATION`; neither O, ROOT, nor a target/implementation coder edits or repins
  the server. O retains exact attribution evidence and assigns the strongest safe substitute in the
  order partial MCP, focused pinned-component unit/integration, synthetic candidate boundary unit.
  The unexecuted physical behavior is reported as not physically certified. C4 must reject a weak or
  convenient substitution when stronger safe evidence was available.
- A reproducible candidate defect observed by the helper is pooled unless continuing would cross one
  of the three exact immediate-stop boundaries. ROOT performs the product/support classification
  from exact evidence after containment or at the gate join; only an admitted product defect reopens
  candidate work.
- If helper liveness or observation evidence fails, ROOT first uses the predeclared evidence-fallback
  matrix. Complete correlated backup evidence may close the attempt; otherwise only the affected
  attempt becomes incomplete and rolls fresh. Optional AI-watcher loss is irrelevant.
- If O liveness/result commitment fails, `ROOT-IM` records `topology/ORCHESTRATOR_LOST.json`, stops/reaps the registered topology, preserves the partial attempt, and never completes or reuses partial manifest/result files. Classify the cause independently: an orchestrator-side failure rolls only to a fresh attempt with unchanged locked inputs and retained eligible green credits; only exact evidence of a harness/watcher or locked-input defect enters its corresponding implementation/relock route.
- Every C3 restart uses the next immutable `attempt-NNNN` pair and fresh disposable target Git repository. The new repository may reconstruct the exact accepted target source-tree commit plus the locked seed but copies no build/runtime state. P0 always reruns; later green target tests remain credited only when their dependencies did not change, and new-run artifacts come only from the new attempt.
- No broad process kill is permitted. Termination uses the registered root/child identities.
- ROOT requests controller-managed shutdown first. Only if the registered controller is unavailable/
  unresponsive may ROOT terminate/reap its pre-registered controller/MCP/process-group host identities,
  recording `topology/EMERGENCY_TERMINATION.json`. This grants no MCP/hardware authority; the attempt
  fails with indeterminate board state and fresh-attempt P0 recovery is required before mutation.

### C3 watcher closure clarification

The deterministic watcher helper is the required C3 observer. Its ready, heartbeat, abort, and
terminal-service evidence remain fail-closed. `F.C3.W` is supplemental independent review; its
report/final-message/exit provenance is retained when available but its early exit alone is not
`WATCHER_LOST` and never blocks manifest closure. After candidate-managed shutdown, ROOT writes
required `topology/WATCHER_OBSERVATION_CLOSE.json` binding the helper evidence and exact helper
identity/exit. Only that required closure unlocks O's manifest; `WATCHER_EXIT.json` is supplemental.

### Pooled finding rule

Every review, selected test set, and observer/watch lane completes its assigned affected surface or
selection, records the complete finding set, and sends it to one triage gate. Triage deduplicates and
authorizes one bounded repair batch; ordinary findings do not stop peer checks, restart review, or
trigger repair/rerun during the gate. Observers record non-critical violations for post-gate pooling.

Immediate stop is reserved for exact evidence of an unauthorized/wrong-resource operation, loss of
containment or cleanup of a live process, or irreversible corruption of evidence required to judge
later work. ROOT owns the stop and preserves evidence. Safely contained defects and non-critical
evidence gaps are recorded and pooled.

### Outer C3 failure isolation

Treat errors in outer C3 setup, launch, monitoring, report handling, evidence validation, and
emergency cleanup as outer-attempt procedure failures, not candidate failures. Correct harmless
procedure/paperwork errors in place. If an error prevents honest immutable-attempt closure, close only
that attempt and use a fresh namespace, preserving every candidate/test result with immutable valid
evidence and an unchanged dependency fingerprint. Do not reopen candidate implementation, C0/C1/C2,
or green candidate tests solely due to an outer procedure failure.

Escalate to candidate repair/relock only if exact evidence shows a changed C1-locked candidate input,
incorrect candidate behavior, or an untrustworthy candidate result. ROOT records the classification
before rerunning work.

## 11. Final audit, safeguard, and promotion

1. **C4 nested static audit:** after practical success, launch fresh Terra-medium-Fast auditors for requirement coverage, topology/role separation, evidence consistency, watcher boundary, protected state, scope, and preservation of the original successful general-harness unit behavior. The audit compares baseline-to-candidate test IDs, dependency mappings, results, skips/xfails, assertion strength, and shared-code coverage. C4 is the ordinary post-lock static-review phase; the explicit locked-input repair route below may re-enter C0.
2. Classify gaps before repair. "Evidence-only" is only a C4 report/annotation correction under `evidence/firmware-v2/final/C4/annotations/`, outside attempts, and can never satisfy/alter/replace acceptance evidence. Any closed-C3 evidence or target-source/config defect requires fresh C3 from P0/earliest invalidated, then C4. Locked-input repair uses owning step/fresh C0/C1/C2/C3/C4. Rerun dependency-invalidated IDs only.
3. Verify that live governing hashes are covered by the operative C1 and append-only change dispositions. An unclassified mismatch pauses admission; ROOT classifies its domains, refreshes C1 if needed, and reruns only consuming gates. Never create an unrelated second/final lock here.
4. Run a pre-safeguard environment-admission gate that executes no safeguard source check or test;
   repair/repeat admission until green. Then create exactly one logical `SAFEGUARD_RUN_ID` for the
   C1 lock. An environment-only interruption resumes that ID and only incomplete/invalidated
   components; a locked-input change ends it and requires a new lock/run ID.
5. Require Ruff, formatting, BasedPyright with no baseline expansion, compilation, orchestrator tests, watcher tests, Codex integration tests, attention retention, synthetic firmware tests, and all newly accumulated tests to pass.
6. Reconcile zero process, claim, request, relay, and event residue.
7. Write completion, candidate, server, acceptance, watcher, topology, criteria, protected-state, full-verification, promotion, and out-of-scope records.
8. Promote a fresh inactive runtime and preserve the prior frozen rollback.

The safeguard operates on the reserved candidate root, including a non-expanded mapping of the
existing BasedPyright baseline. Only a green candidate safeguard permits creation of
`progress/v1.2` at that exact commit and staging of the explicitly named stable runner on the distinct branch for
the required outer verifier. Preserve `progress/v1.1`; do not publish externally without a live
directive.

Once promotion evidence is durable, close the temporary candidate and MCP linked worktrees only
through exact Git worktree operations after clean-state, retained-revision, and zero-process checks.
Never recursively delete a worktree path.

## 12. Atomic completion criteria

These IDs are the authoritative checklist consumed by the execution plan.

| ID | Requirement |
|---|---|
| C1 | Product work starts from exact clean harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`. |
| C2 | Frozen rollback `287ea53793e3963062882012ff80c3b0e8c41587`, prior runtimes, and unrelated outer changes are preserved. |
| C3 | A new isolated harness candidate branch/worktree is used; `4699d27` is not rewritten. |
| C4 | A clean isolated MCP server worktree is created from `f003f84a7df51cd8595a3203c62e225b21da2a22`; the dirty source checkout is untouched. |
| C5 | All 47 resource-mirror files pass byte-count and SHA-256 validation. |
| C6 | Preflight does not mutate hardware before live authorization and plans are recorded. |
| C7 | Exact harness, server, toolchain, pack, datasheet, fixture, and target hashes are retained. |
| C8 | Every run and lane has isolated runtime, MCP state, artifact, and log roots. |
| C9 | Schema-less firmware invocation remains the legacy dispatch route. |
| C10 | Canonical policy bytes, digest sidecar, headings, embedded text, and final reminder remain enforced. |
| C11 | Legacy label-derived output filenames and firmware event-log naming remain accepted. |
| C12 | Legacy model settings, leases, board tokens, MCP declarations, server snapshot, prompt, outputs, and resume fields retain their accepted shapes. |
| C13 | `orchestrator-coding-invocation/v1` behavior and repository/result safety remain unchanged. |
| C14 | Coding and firmware input/result shapes cannot ambiguously satisfy the other route. |
| C15 | Retained legacy fixtures, examples, and accepted configurations still run without edits. |
| C16 | No migration, evidence rewrite, or new public firmware schema is required. |
| C17 | Any internal normalization is behavior-preserving and limited to proven duplicate lifecycle logic. |
| C18 | Dual-route automated tests prove coding and firmware lanes coexist. |
| C19 | Worker, controller, helper, and descendant identity uses PID plus creation evidence and ownership correlation. |
| C20 | MCP launcher, server, and provider lifetimes are exact, current, and lane-correlated. |
| C21 | Hardware relays bind exact request hash, arguments, lane, server snapshot, decision, and expiry. |
| C22 | Expired, stale, malformed, changed, or unbound relays remain visible and cannot authorize execution. |
| C23 | Firmware checkpoint/resume preserves same thread and path identity without inventing liveness. |
| C24 | Native lifecycle events are emitted and only exact top-level `ack --event-id` acknowledgements clear them. |
| C25 | Board tokens and operational leases are distinguished from historical declarations. |
| C26 | Generic and hardware claims have exact owner identity and fail-closed stale handling. |
| C27 | Independent board lanes can progress concurrently without shared-state contamination. |
| C28 | Same-board and same-resource work serializes without double ownership. |
| C29 | Claims and hardware resources release only after exact child/MCP exit and reap are proven. |
| C30 | Unknown, partial, corrupt, or ambiguous lifecycle evidence fails closed and remains actionable. |
| C31 | Acceptance workers request every physical operation through the candidate harness broker; only its lane controller holds/uses the BYO Firmware MCP stdio/launch capability after validating all four call artifacts. |
| C32 | The server revision is pinned and changes only for a reproduced in-scope defect. |
| C33 | Each physical lane controller owns a distinct MCP process/endpoint, `.firm` state, artifact root, and log root; O/target workers receive no direct physical endpoint or inheritable capability. |
| C34 | Four board profiles bind stable board/probe identity and are rediscovered at run start. |
| C35 | COM ports are live routes, never primary board identity. |
| C36 | STM-A/STM-B I2C2, UART, ground, and pull-up fixture bindings match authoritative material. |
| C37 | The CoreSX1262 `P.05` notation is resolved authoritatively before any dependent action and is never guessed. |
| C38 | Datasheet, device-pack, and compiler inputs match their recorded hashes/locks. |
| C39 | Canonical scope/policy/duration/identity/governing fields bind proposal, signed decision, authorization, immutable pre-dispatch admission, dispatch, and result; monotonic deadline overrun, mismatch, or expiry is fail-closed/no-success. |
| C40 | Bootloader replacement, unlock, mass erase, and protection changes remain excluded. |
| C41 | LoRa uses 915 MHz fixture intent, lowest practical power, short packets, and bounded duty cycle. |
| C42 | Physical assertions use electronic/software oracles only; no operator touch is required. |
| C43 | The final target is a fresh disposable Four-Board Dual-Family Firmware Lab repository. |
| C44 | STM-A controller and STM-B responder images implement a deterministic machine-readable protocol. |
| C45 | The STM32 pair proves ordered I2C exchange, checksum/sequence/error evidence, UART, reset/reconnect, debug, and sustained traffic. |
| C46 | The nRF52 codebase proves a deterministic two-board BLE GATT command/acknowledgement mode. |
| C47 | The nRF52 codebase proves deterministic CoreSX1262 ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence. |
| C48 | Accepted STM32 I2C and nRF52 LoRa subsystems pass concurrently on all four boards in two non-agent groups whose complete lifecycle is owned only by `C3-HARNESS`. |
| C49 | Build/artifact provenance and MCP-mediated setup, flash, reset, debug, memory/register, and UART evidence are retained. |
| C50 | Behavioral oracles, not flash success, determine application pass. |
| C51 | One predeclared intentional, source-controlled, non-destructive target-code defect produces its recorded expected behavioral failure, is diagnosed, repaired, and selectively retested without changing or being called a harness/server/fixture defect. |
| C52 | One real physical lane checkpoints and resumes with the same thread/path identity. |
| C53 | Practical acceptance proves independent concurrency and same-resource contention behavior. |
| C54 | Boards/candidate state close; O's closed-inventory manifest/result covers all in-domain files; ROOT's separate closed topology inventory proves O/helper reap and preserves any optional W evidence; C4 independently enumerates both domains. |
| C55 | Fresh Sol-high-Fast subagent `F.C3.O`, never `ROOT-IM`, owns final practical-project decisions, while `C3-HARNESS` exclusively launches and owns target workers. |
| C56 | `ROOT-IM` remains implementation coordinator/supervisor and never assigns final target-project work. |
| C57 | ROOT directly launches the non-agent deterministic helper; exact ready/heartbeat/terminal/abort-disposition/exit facts close through `WATCHER_OBSERVATION_CLOSE.json` using primary or approved independent backup evidence. Optional `F.C3.W` review is supplemental and non-gating. |
| C58 | Helper/O loss first contains registered topology. A support failure is corrected in place or rolls only the incomplete attempt; only controller unavailability permits ROOT's recorded pre-registered-host-process emergency termination and fresh-P0 returning-state recovery. Product credit is invalidated only by exact product-material evidence or an indeterminate required result. |
| C59 | Deterministic observation pools ordinary candidate, target, and support findings; only the three exact live-safety conditions request immediate containment. Target application/compiler/test/target-repository-configuration/invalid-call defects remain acceptance-project work when no C1-locked input changes; a proven immutable pinned-server defect/incompatibility uses `AUTHORIZED_SERVER_LIMITATION` with exact attribution, strongest-available substitution, and explicit non-certification of the skipped physical portion, never server repair or repinning. |
| C60 | `ROOT-IM` launches `F.C3.O`, directly launches the non-agent helper, and may launch optional `F.C3.W`; `F.C3.O` submits target assignments and never launches target workers directly; `C3-HARNESS` launches each target coder, reviewer/test-writer, and doer with the exact requested model, effort, and tier through headless `codex exec`, with no substitution. This child-launch criterion does not apply to `ROOT-IM`. |
| C61 | Production coding is singleton/serial; actual role fan-out is 1-3 and used only for independent work. |
| C62 | Each implementation large step receives exactly two back-to-back QA loops; modules do not receive individual cycles. |
| C63 | The C1-frozen implementation registry and fresh manifest-covered attempt registry prevent rerunning unchanged green tests without allowing C3 to mutate locked or prior state. |
| C64 | One terminal green logical `SAFEGUARD_RUN_ID` covers the complete accumulated safeguard after practical success/final audit; pre-admission is outside the run, environment-only interruption resumes it selectively, and any locked-input change requires a new lock and run ID. |
| C65 | The core gate uses the applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intentions. |
| C66 | Exhaustive A20-A26, B01-B39/Q40, Q41 soaks, and destructive/try-last cases are explicitly non-gating extended qualification. |
| C67 | Evidence binds requirements to exact revisions, identities, tests, artifacts, authorization, and hardware observations. |
| C68 | A fresh final reviewer completes the full frozen-tip sweep and reports no unresolved admissible production-relevant compatibility, safety, correctness, or complexity gap; every submitted gap proves a credible deployed trigger and concrete negative consequence, passes the structured category/evidence/cost-benefit gate, and receives the owning orchestrator's independent decision. |
| C69 | Final nested audits prove requirement coverage, role topology, watcher boundary, evidence consistency, and protected state. |
| C70 | Promotion occurs only from the locked green candidate into a fresh inactive runtime while preserving rollback. |
| C71 | Quick-start and examples accurately teach legacy firmware, coding V1, dual-path operation, events, acknowledgements, resume, and cleanup. |
| C72 | No unnecessary framework, scheduler, hardware abstraction, board expansion, UI, database, endurance gate, or reviewer-driven fix whose complexity/regression/verification cost is disproportionate to its demonstrated benefit is added. |
| C73 | A protected baseline-to-candidate unit-test matrix proves the original successful general harness still works: every dependency-invalidated original unit test and new cross-route isolation test is green, and audits find no unjustified deletion, skip, expected failure, weakened assertion, or unmapped shared-code change. |
| C74 | One worker thread is bound to one logical task card: only same-task `CONTINUE`, the one report-only recovery, and the strict fast lane may resume it before acceptance; accepted threads reject unrelated reuse. |
| C75 | After semantic acceptance and durable evidence/revision preservation, a terminal lane leaves active discovery, any clean unused linked worktree closes safely, required results/transcripts remain archive-only, and disposable caches are removed without reopening product work. |
| C76 | Static read-only lanes can inspect an exact immutable source commit and write results separately without a full linked worktree; mutation or source-local execution still receives isolated writable source state. |
| C77 | All concurrent writers to one shared event log wait on one cross-process lock and append complete flushed records; a real multi-process regression proves no malformed, interleaved, or lost event. |

## 13. Stop conditions

The implementation is genuinely complete only when C1-C77 have evidence, no accepted
production-relevant in-scope gap remains, the original successful general-harness unit behavior
remains proven, the practical project is green under `F.C3.O` with complete deterministic-helper
observation, one terminal logical
safeguard run is green with no incomplete component, and promotion records point to a clean inactive
runtime. Cosmetic, unreachable, behavior-neutral, and speculative non-findings may remain deferred.
A narrowly reviewed `AUTHORIZED_SERVER_LIMITATION` may satisfy only its affected criterion through
the strongest available substitute and must disclose the physically uncertified portion. A
partially working application, a green flash, an unreviewed or convenience substitution, or an
unresolved identity ambiguity is not completion.
