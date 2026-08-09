# Execution Goal: Backward-Compatible Physical Firmware Harness Acceptance

This file is the live, user-owned execution directive for the project. Execute it completely. Do not stop after planning, partial implementation, successful compilation, successful flashing, or a partially passing application.

## 0. Operative preparation boundary — 2026-08-06

Execution remains paused while the next-run topology is prepared. The accepted S30 joined tip is
`6649cf201ded9782c2cb3bc56983f4a560728ea8`; it has not yet been admitted to the reserved candidate,
and no S4/S5, fresh C0/C1/C2, host-only rehearsal, MCP process, watcher, target repository, hardware
claim, or new physical attempt may start before explicit user resumption. Preparation work may edit
the governing documents and the external C3 support layer and may run host-only support tests. It
must not mutate the frozen stable runner, candidate product, MCP fixture, or hardware.

The next long run has this order: admit the already-tested S30 joined tip without repeating its four
green affected IDs when their dependency fingerprint is unchanged; implement and accept S4's two
candidate features; implement and accept S5's four candidate efficiency/evidence features; run fresh
C0/C1 and only dependency-invalidated C2 work; run the exact candidate
through the host-only external-attempt rehearsal; then allocate one fresh physical attempt. The
rehearsal and physical attempt use the external support contract in `test-cleanup.md` and the
verified support code under `.codex/scripts/c3_outer_support.py` and
`.codex/scripts/c3_watcher_helper.py`. That support layer's focused tests, disposable practical
smoke, independent Luna execution, and full repository gate are green; no support-preparation work
remains before explicit resume.

## 1. Authoritative inputs

Before acting, read and follow:

1. `AGENTS.md` and every applicable nested `AGENTS.md`.
2. `HANDOFF.md`.
3. This `goal.md`.
4. `active_docs/GENERALIZATION_SPEC_2.md`.
5. `active_docs/IMPLEMENTATION_ROADMAP_2.md`.
6. `plans/general-coding-harness/EXECUTION_PLAN_2.md`.
7. `active_docs/EXECUTION_READINESS_2.md`.
8. `task-card-spec.md`.
9. `test-cleanup.md`.
10. The firmware fixture, datasheet, toolchain, experiment, and MCP-server material referenced by those documents.

The specification, roadmap, and execution plan define the detailed C1-C77 contract and execution topology. This file defines the overall mandate and takes precedence over those project planning documents if I edit it during execution. System, developer, safety, and applicable `AGENTS.md` instructions still take precedence over this file.

Do not invoke the planning-only `plan-harness-workflow` skill merely to execute the already-written plan. Use it again only if a material edit to this file requires the execution plan itself to be regenerated or structurally revised.

## 2. Live-goal update protocol

`goal.md` may change while work is in progress. Execution subagents must never edit this file.
`ROOT-IM` may edit it only when the user explicitly requests a planning/directive revision, as in a
pre-execution clarification; it must never silently rewrite the user's mandate during execution.

`ROOT-IM`, the current outside implementation coordinator defined in Section 6, must reread and
hash `goal.md`:

- at initial preflight;
- before every new large step;
- before each Loop 1 and Loop 2 dispatch;
- before C0, C1, C2, C3, C4, and the safeguard;
- at the actual boundary before every mutating MCP dispatch, with continuous change observation while
  a mutating operation is in flight;
- after every resume, compaction, or new session;
- before declaring completion.

Record each observed hash in the runtime management evidence. If the hash changes:

1. stop issuing new assignments long enough to read the new directive;
2. preserve currently valid evidence and safely checkpoint active work;
3. determine which requirements, steps, tests, hardware authorization, and evidence are affected;
4. revise the plan documents when the change materially alters scope or topology;
5. invalidate and rerun only work whose dependencies changed;
6. continue from the earliest affected gate.

Do not restart unaffected green work. Do not let an already-running worker silently reinterpret its fixed assignment; checkpoint it and issue an updated assignment through its explicit owner (`ROOT-IM` during product implementation or `F.C3.O` during the final target project) when necessary.

C1 records whole-document hashes and mutating dispatch requires a current C1, so a mismatch pauses
new admission until ROOT classifies the change and refreshes the lock when needed. The mismatch does
not by itself invalidate the evidence used to create that lock: invalidation is decided by the
smallest changed lock-input domain. ROOT writes an append-only governing-change
classification that names the changed requirements/domains, gates that consume them, preserved
evidence, and the reason. Only dependent gates rerun. A change to hardware authority or an input
used by an in-flight mutation immediately suspends new calls and expires affected authorization; a
candidate-behavior change returns through its owning product gate; a test-procedure or outer-
topology change reruns only its dependent test/rehearsal/attempt work. If ROOT cannot classify a
change confidently, it uses the documented conservative fallback. This domain-scoped rule applies
to `goal.md` as well as the other governing documents; no file name by itself forces a full gate
cycle. A replacement C1 may bind current hashes while reusing every unchanged dependent gate.
Whole-document hashes and any byte-only editorial chain remain audit evidence, never the sole
dependency decision.

P4 manifest creation freezes every `external_references` path/hash through C4, safeguard, and
completion. Any later change to an external reference--including an append to
`EDITORIAL_SUPERSESSION.jsonl` or a byte-only change to one of the other four documents--invalidates
that C3 acceptance result; C4 and safeguard must reject it. Preserve the attempt, apply the normal
goal/editorial classification, and run a fresh C3 attempt (P0 plus only dependency-invalidated work)
before C4. A semantic or `goal.md` change still follows the fresh-lock route. C4 never accepts a
stale chain prefix as if it were the current terminal.

## 3. Objective

Implement `GENERALIZATION_SPEC_2` and `IMPLEMENTATION_ROADMAP_2` through `EXECUTION_PLAN_2` completely end to end.

The finished result must be a backward-compatible dual-path orchestrator harness that:

- preserves the already-successful general coding harness and its versioned coding invocation;
- continues to support existing schema-less policy-bound firmware invocations without migration;
- manages worker, MCP, relay, board, claim, event, checkpoint, result, and cleanup lifecycles honestly;
- uses the BYO Firmware MCP server as the physical firmware interaction boundary;
- passes a fresh four-board physical firmware acceptance project;
- leaves a clean, inactive, evidence-backed candidate ready for general use.

Before final C0/C1/C2, the candidate also gains the two bounded S4 features defined by
`task-card-spec.md` and `EXECUTION_PLAN_2`:

- focused invocations may bind a compact, context-rich `TASK_CARD.json`; the harness validates its
  identities, entrypoint hashes, deterministic soft-budget score, and prompt instruction, then emits
  `LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE` after a structurally valid result. A dependent lane
  remains blocked until the orchestrator writes a hash-bound `ORCHESTRATOR_ACCEPTANCE.json` verdict
  of `ACCEPTED`, `ACCEPT-WITHIN-TOLERANCE`, `CONTINUE`, or `INCOMPLETE`;
- one malformed or missing terminal result/report receives at most one same-thread report-only
  continuation with the exact validator error. That continuation may use only evidence already
  produced, may not edit product/test code or rerun tests, and must report `INCOMPLETE` when the
  evidence is absent. A second invalid submission stops; it never loops.

Immediately after S4 and before final C0/C1/C2, the candidate also gains S5's four bounded features:

- one worker thread belongs to one logical task card; same-task `CONTINUE`, the report-only retry,
  and the strict fast lane may resume it before acceptance, while an accepted thread rejects
  unrelated reuse and later work starts from a new bounded card;
- after semantic acceptance and durable evidence/revision preservation, terminal lanes leave active
  discovery, clean unused worktrees close safely, required results/transcripts become archive-only,
  and disposable caches are removed without reopening product work;
- a static read-only lane can inspect an exact immutable source commit and write to a separate result
  root without receiving a full linked worktree; mutation or source-local execution still receives
  isolated writable source state;
- concurrent controllers appending to one shared event log wait on one cross-process lock and write
  one complete flushed record at a time.

The acceptance project tests the **candidate harness and watcher**, not whether `ROOT-IM`,
`F.C3.O`, or a target worker is infallible. Assignment, prompting, sequencing, triage, command,
target-code, invalid-call, and result-envelope mistakes by those actors are expected recoverable test
work. Correct them through the owning lane or same-thread resume and retain unaffected green evidence.
Such a mistake does not by itself establish a harness/watcher defect, authorize `ABORT_REQUIRED`,
reopen a completed implementation step, invalidate C1, or justify a broad rerun. It becomes a
harness/watcher finding only when exact evidence shows that the candidate or watcher violated its
contract while accepting, rejecting, reporting, isolating, resuming, or cleaning up the mistaken
work. If an orchestrator mistake makes an immutable C3 attempt impossible to close honestly, use a
fresh attempt namespace for evidence integrity; that is not a candidate reset or implementation
failure, and it does not trigger relock unless a C1-locked input actually changes.

Execution must optimize for prompt delivery of a production-reliable product. Review and repair
effort is release-blocking only for a reproducible defect on a supported or credibly reachable
deployment path that can negatively affect correctness, safety, security, reliability, recovery,
required evidence integrity, or a required user-visible behavior. A latent authorization, identity,
cleanup, or fail-closed defect remains production-relevant when a realistic deployed input can
trigger it. Cosmetic issues, style preferences, unreachable or purely theoretical edge cases,
behavior-neutral cleanup, and speculative hardening without a concrete negative deployment
consequence are non-findings and must not consume a repair, relock, or retest cycle.

## 4. Starting state and preservation rules

- Pin implementation control to the clean detached `stable-general-harness-runner` checkout at
  `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`; evolving product work remains in a separate isolated
  candidate worktree.
- Preserve independently recoverable detached `pre-conversion-rollback` at
  `287ea53793e3963062882012ff80c3b0e8c41587` as rollback. The locked `frozen-harness-to-use`
  directory is a temporary non-operational legacy alias.
- Treat the completed runner transition as fixed execution infrastructure. The former physical
  `harness-in-progress/` checkout is absent. The historical Git common-directory name
  `.git/modules/harness-in-progress` and matching local submodule key remain only because the active
  linked worktrees share them; never rename, delete, reinitialize, or use them as a launch path.
- Launch every S1-S5/C0-C2/C4 implementation controller through
  `.codex/scripts/stable_runner.py`, which must prove the exact clean detached
  `stable-general-harness-runner@4699d27` lock before importing or dispatching. A lane/candidate
  working directory, `PYTHONPATH`, preloaded module, or output path must not make candidate code
  importable as the controller. Proof/projection outputs remain outside the stable checkout.
- Commit `4699d27` predates the candidate executable finding gate. A stable-compatible projected
  invocation may omit candidate-only gate/isolation fields, but `ROOT-IM` must independently verify
  the unprojected current-tip finding, result, and triage artifacts before accepting that lane. The
  candidate itself must enforce the full gate during final candidate acceptance.
- Do not rewrite or recommit the promoted baseline in place.
- Do not reuse previous V1 or V2 practical-acceptance runtime state.
- Reserve `plans/general-coding-harness/runtime/promoted-firmware-v2/` for the final fresh inactive
  runtime; it must be absent before execution and is not created until every promotion gate passes.
- Preserve unrelated outer-repository changes.
- Preserve every registered worktree from the completed general-harness project. Do not reuse its
  branches or paths as V2 lanes and do not remove it as preflight cleanup.
- Preserve the present dirty `Firmware/BYO-Firmware-MCP` checkout exactly as found.
- Create a clean isolated MCP-server worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`.
- Treat `Firmware/Firmware resources/` as a read-only evidence mirror. Do not modify its datasheets, packs, fixture records, retained evidence, or manifest-bound files.
- You may refactor or change the harness, the clean MCP-server worktree, and authoritative writable firmware/test-medium source under `Firmware/` when required by an in-scope, reproduced need.
- Do not perform speculative MCP-server refactors.

The collision-proof coordinates in `EXECUTION_READINESS_2.md` were created during completed
preflight. On resume, verify their exact recorded branches, commits, common directory, and clean
state; do not recreate, relocate, reset, clean, or silently substitute them. The reserved worktrees
live below the `firmware-v2/runtime` boundary so outer development hooks do not confuse candidate
changes with outer-checkout changes. Resume only from `PARALLEL_CHECKPOINT.md`; never restart
preflight or an already-green large step merely because the stable runner was renamed.

The firmware resource manifest's historical source paths are provenance, not current file
dependencies. Revalidate all mirrored destination byte counts and SHA-256 values. Do not require or
claim a live comparison to historical source paths that are absent. Treat absolute tool paths as
live inputs only after rechecking them, and replace the obsolete historical NCS
`PYTHONPYCACHEPREFIX` with a fresh per-lane cache below the V2 runtime.

## 5. Subagent assignments (not the root session)

These assignments govern only child agents launched headlessly through `codex exec`. They do not
select, relaunch, or constrain the current outside root session. The collaboration picker is not an
availability oracle. Use the exact requested assignments with no substitution:

- every launched orchestrator subagent, including `F.C3.O`: GPT-5.6 Sol, high reasoning, Fast via `service_tier="priority"`;
- all source-code coders: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`;
- all reviewers and test writers: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`;
- all doers and test executors: GPT-5.6 Luna, high reasoning, Fast via `service_tier="priority"`;
- optional supplemental acceptance reviewer `F.C3.W`, only when ROOT decides its independent review
  is worth the cost: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`. It is not
  the required observer and never gates closure.

The current outside root is `ROOT-IM`, the host implementation coordinator. `ROOT-IM` is not a
subagent launched by this plan and has no model, reasoning-effort, or service-tier gate in this
contract. Never apply the launched-orchestrator assignment to `ROOT-IM`.

Every headless launch must explicitly use `--dangerously-bypass-approvals-and-sandbox`,
`--dangerously-bypass-hook-trust`, `--ignore-user-config`, `--json`, the exact model,
`model_reasoning_effort`, explicit `service_tier="priority"`, and an isolated
`-C` root. Capture exact model/effort/tier/thread/PID-plus-creation/exit/final-message evidence. Do
not use `--ephemeral` for resumable lanes. Prove all required launch combinations during preflight.
If one fails, diagnose and fix the launch path; do not substitute another model.

Because user configuration is ignored, no lane may rely on a globally registered MCP server. Every
controller authorized to own a physical MCP process receives an explicit isolated BYO Firmware MCP
declaration bound to the clean pin and lane-local `.firm`, artifact, and log roots. In C3 only the
candidate harness physical-lane controller receives the physical server command/environment, owns
its process and stdio endpoint, and can forward a call. O and target workers receive no physical MCP
registration, endpoint, launch command, credentials, or inheritable handle; they submit structured
operation requests to the candidate harness broker and receive its recorded results.

Use the pinned server's stdio command `uv run --project
plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate --locked
pyocd-debug-mcp`, resolving the project argument to its absolute path and setting
`BYO_MCP_ARTIFACT_ROOT` to the lane's isolated state/artifact root. Keep stdout exclusive to MCP
framing and capture stderr separately. Never launch the dirty source checkout as the acceptance
server.

Do not inherit an ambient probe or target route. Reject unreviewed `.env` files; explicitly clear
`PYOCD_PROBE_UID` and `PYOCD_TARGET` for inventory; then bind a board-owning lane only to its exact
assigned probe UID and reviewed target/profile. Record the effective non-secret routing environment.

## 6. Required orchestration distinction

Use these identifiers in gates, evidence, and handoffs; do not use an unqualified "orchestrator" or
"manager" where the owner could be ambiguous:

1. `ROOT-IM` is the current outside root session. It coordinates the multi-agent creation of the harness retrofit, including product coding, review, test writing, test execution, integration, repairs, checkpoints, final safeguard, and promotion. It is outside the subagent assignment table in Section 5.
2. `F.C3.O` is a fresh Sol-high-Fast acceptance-orchestrator subagent launched directly by `ROOT-IM`. It operates the candidate harness under test and is the sole decision-maker for the final target project. `ROOT-IM` may start, supervise, terminate, and receive the result of this topology, but it must not assign or orchestrate target-project tasks.
3. `C3-HARNESS` denotes the candidate harness control plane and its exact controller processes, operated by `F.C3.O`. It is the system under test, not a Codex-agent role and not an agent slot. `F.C3.O` submits every target assignment to `C3-HARNESS`; `C3-HARNESS`, not `F.C3.O`, launches the assigned target worker through `codex exec`, owns its lifecycle, and records its exact launch/result/event/claim evidence. Direct target-worker launch by `F.C3.O` is prohibited because it would bypass the harness being certified.
4. `F.C3.A1`, `F.C3.C1`, `F.C3.P1`, and `F.C3.R1` are candidate-harness-launched target workers. They receive one serial assignment at a time through `C3-HARNESS`, return results through it, and do not report to `ROOT-IM` for target-project decisions.
5. ROOT directly launches the deterministic non-agent watcher helper, which is the required observer
   and writes ready/heartbeat/finding/terminal-service evidence. `F.C3.W`, if launched, is optional
   supplemental read-only review and never gates work or manifest closure.

`F.C3.O` must coordinate its own multi-agent target-project creation flow by submitting serial target
test-writer, coder, doer, and reviewer assignments through `C3-HARNESS` while the deterministic
helper provides required observation. Optional `F.C3.W` liveness is irrelevant to this authority.

Keep production coding singular and serial. Role fan-out must remain between one and three and be used only for genuinely independent review, test-writing, or test-execution slices. Follow the preplanned pools in `EXECUTION_PLAN_2`; do not repartition dynamically merely because work is difficult or slow.

## 7. Implementation method

- Execute the three coherent large steps S1-S3 in order.
- Give each large step exactly two back-to-back QA loops.
- Treat atomic edits and individual modules as work inside a large step, not as separate loop cycles.
- Use isolated worktrees or run roots and disjoint ownership for parallel lanes.
- Bind every worker thread to one logical task card. Resume it only for unresolved same-card work,
  the one report-only repair, or the strict fast lane before semantic acceptance. Once accepted, do
  not reuse that thread for unrelated work; launch a new bounded card/thread.
- Allocate a full linked worktree only for source mutation or source-local execution state. Static
  read-only work uses the exact immutable candidate source plus a separate result root. After
  acceptance, preserve evidence and retained revision first, then remove the lane from active scans,
  safely close any clean unused worktree, archive required transcripts/results, and remove only
  disposable caches.
- Serialize every append to a shared event log with one cross-process lock. Another controller waits
  until the writer flushes and releases the lock; concurrent writes may never interleave or disappear.
- `ROOT-IM` owns every implementation merge, join, finding decision, failure classification, and final verification outside the final target project.
- Reviewers recommend; `ROOT-IM` decides implementation findings, while `F.C3.O` decides target-project findings during practical acceptance.
- Every reviewer, test writer, and test executor uses the candidate's structured finding-admissibility
  gate. A submitted gap is eligible for triage only when it is exactly one of
  `CODEBASE_BREAKING`, `FUNCTIONALITY_BREAKING`, or `WORTH_FIXING`. Every eligible submission must
  bind reproducible evidence and an affected requirement/behavior, propose the smallest sufficient
  fix, and explicitly compare the problem's impact and no-fix cost against implementation
  complexity, regression risk, verification cost, and lower-risk alternatives. The submitter must
  conclude, with evidence, that the problem outweighs the total risk and cost of the proposed fix.
- The executable gate validates that closed structure and rejects unsupported, incomplete, PASS-with-
  gap, style-only, speculative-hardening, cleanup, preference, or "technically nicer" findings.
  `ROOT-IM` or `F.C3.O` then independently decides whether the evidence is true and the tradeoff is
  favorable; a reviewer-supplied boolean or score is never sufficient proof. A rejected or
  inadmissible suggestion may be recorded as a non-finding but must not trigger source changes,
  reopen a green step, invalidate C1, or rerun a green test.
- An accepted repair is the smallest change whose expected benefit still outweighs its added
  complexity, regression surface, and verification burden. If no such repair exists, reject or
  defer the finding instead of making the product more fragile.
- A reviewer must finish the complete assigned affected-surface review even after finding a valid
  defect, unless an external blocker makes further inspection impossible. It returns one complete
  current-tip finding set; it must not intentionally stop at the first finding. `ROOT-IM` triages
  that whole set, and the serial coder repairs all accepted findings as one bounded batch before
  another independent review. No C0 or ordinary product review runs on an intermediate revision
  inside that batch.
- On a frozen joined revision, run the shortest already-required dependency-invalidated smoke IDs
  first. If they pass, the remaining focused test execution and read-only review may run in
  parallel; neither result unlocks the next gate until both join on the same revision. A production
  change invalidates both dependent conclusions and returns through the same batched flow.
- A correction that changes no production source, operative policy, public contract, locked
  configuration, test oracle, or behavioral expectation is administrative and resumes in the same
  lane without a new product review or green-test rerun. A strictly test-only correction may use the
  fast lane only when its diff is limited to synthetic fixture/setup or test metadata, the exact
  failed IDs are known, no production/policy/contract/locked-configuration file changes, and no test
  oracle, assertion strength, expected outcome, stable ID, or coverage obligation changes. The same
  test-author thread records that deterministic eligibility checklist, corrects the fixture, and
  reruns exactly the failed IDs once before any unrelated smoke or work starts. It receives no C0,
  ordinary review, registry/dependency reconciliation, or aggregate join. A failed rerun or any
  unproved condition leaves the fast lane for the material route. If C1 already exists, changed
  candidate/test bytes still require a new C1 and dependency-invalidated C2. Any change to expected
  product behavior, coverage obligations, an operative test/evidence contract, production, or policy
  remains material and uses the full review/relock route. The fast lane is pre-C3 only; after a C3
  attempt starts, the existing attempt/lock/C4 invalidation rules remain authoritative.
- Before an expensive selected test set whose result depends on custom per-check subprocess/process
  evidence, its executor performs one local recordability preflight. The preflight launches no real
  product/MCP/hardware work and proves that the executor can create and validate one complete
  inner-check record: stable ID, exact inputs, worker/process creation identity, timing, command,
  output paths, and exit outcome. A preflight failure is a same-lane procedure correction and does
  not invalidate product credit or launch the expensive selection. A post-run report/path/schema
  correction with already-complete raw identity evidence is administrative; if raw evidence cannot
  be reconstructed, rerun only the affected stable ID on the same lock. Bind a successful preflight
  to the runner/procedure/configuration/environment fingerprint and reuse it until that fingerprint
  changes; do not repeat it merely because another test set starts.
- When a selected test run reports only fixture, mock, or executor-environment defects, ROOT records
  the complete classified set, repairs that set as one test-only batch, and reruns the selection once.
  Do not rerun the same broad selection after each individual fixture correction. A candidate/product
  finding exits this batching rule and follows the material route.
- Before allocating any C3 attempt root, watcher, target repository, MCP process, or hardware claim,
  run one host-only C3 rehearsal on the exact green C1/C2 candidate using disposable local fakes.
  It proves candidate-side launch admission, retained-session authorization, exact process/identity
  binding, duplicate-assignment refusal, watcher correlation, recovery/idempotence, cleanup, and
  terminal closure. It may reuse unchanged green rehearsal IDs by dependency fingerprint. A failure
  is classified before any C3 attempt exists; candidate defects follow the material repair/relock
  route, while fixture/executor defects use the same-lane rules above. Only a green rehearsal unlocks
  the first physical C3 attempt.
- Preserve every raw lane result, but reconcile the dependency map, passed registry, and aggregate
  join evidence once for the accepted batch tip rather than for each intermediate repair commit.
- Create C1 only after the batch tip has its clean terminal C0 decision and joined green affected
  tests. C1 is the exact stable release-candidate lock, not an intermediate repair checkpoint.
- Preserve stable test IDs and phase-separated passed registries. The implementation registry is
  `runtime/firmware-v2/passed-tests.json`; C1 locks it and C3 never writes it. Each C3 attempt owns
  `acceptance/attempt-NNNN/passed-tests.json`, included in that attempt's P4 manifest. A fresh attempt
  creates a fresh registry and may re-credit unchanged prior results only by immutable path/hash and
  dependency-fingerprint references, never by copying or mutating prior registry state.
- There is no arbitrary iteration cap. Continue diagnosis, repair, and selective verification while meaningful in-scope progress remains possible.
- Reject unrelated frameworks, schedulers, hardware abstractions, board expansion, UIs, databases, and exhaustive/endurance work that is unnecessary for C1-C77.

## 8. Protected original general-harness behavior

Treat the original successful general harness as a protected unit-regression baseline.

1. Record its baseline unit-test manifest and accepted results before implementation.
2. Map shared production modules to the original unit-test IDs that protect them.
3. Whenever firmware compatibility work changes shared parsing, controller, process, reconciliation, event, claim, Git/result, configuration, documentation, or cleanup behavior, run every affected original general-harness unit test.
4. Add cross-route unit tests proving firmware compatibility cannot change coding invocation, coding result, repository safety, claims, events, acknowledgements, resume, or cleanup behavior.
5. Do not obtain green results by deleting original tests, skipping them, marking them expected-failure, weakening their assertions, or leaving shared-code changes unmapped.
6. If test structure must move, preserve the original behavior and failure assertions at equal or greater strength and record the mapping.
7. C0 and C4 auditors must explicitly compare baseline and candidate test manifests, dependency mappings, executed affected IDs, deletions, skips/xfails, and assertion strength.
8. C73 is blocking. Promotion is forbidden unless this protected regression matrix is complete and green.

## 9. Test-retention rule

Do not rerun a green test unless code, configuration, server behavior, firmware, hardware identity, or an upstream artifact in its dependency fingerprint changed.

- Rerun failed and newly implicated stable test IDs after repair.
- Preserve unrelated green evidence.
- A shared harness change invalidates all mapped original general-harness unit tests.
- A target firmware, target-repository MCP configuration, or target MCP call-input change invalidates only its affected target tests and downstream practical sprint.
- A harness or watcher repair invalidates its affected synthetic/integration gates and the earliest dependent practical sprint.
- Run the complete accumulated candidate safeguard exactly once after practical acceptance and C4 are green on the locked revision.
- If that locked revision changes after the safeguard, the new revision requires its own one final safeguard; do not claim the earlier result.

"Exactly once" means one logical `SAFEGUARD_RUN_ID` per exact C1 lock. Before creating that ID, run
a pre-safeguard environment admission that performs no safeguard source check or test. Admission may
be repaired and repeated. Once the logical safeguard starts, an environment-only interruption may
resume the same run ID and rerun only incomplete or dependency-invalidated components; it is not a
second logical safeguard, and completed green components remain credited when their dependencies are
unchanged. Any source, test, server, locked configuration, or other C1-input change ends that run as
failed and requires the normal new-lock route plus a new run ID. Promotion requires one terminal
green logical safeguard record with no incomplete component.

The ordinary outer `.codex/scripts/verify.py` targets `stable-general-harness-runner`; it is not evidence for
code that exists only in the candidate worktree. Run the safeguard against the exact candidate root
with its BasedPyright baseline mapped without expansion. Only after that gate is green may promotion
create the distinct `progress/v1.2` branch at the candidate commit and stage it in
the immutable stable runner for the required outer verification. Preserve `progress/v1.1`; do not push or
publish without an explicit live directive.

After durable promotion evidence, close temporary linked worktrees only with exact Git worktree
operations after proving they are clean, retained by branch/pin, and unused by any process. Never
recursively delete their directories.

## 10. Firmware and hardware interface

Use the BYO Firmware MCP server for every physical interaction, including discovery, setup, connect, flash, reset, debug, memory/register access, UART, and returning-state operations. Direct pyOCD control, direct serial control, and ad hoc probe scripts are not acceptance evidence.

Each physical lane must own a separate MCP process, project-local `.firm` state, artifact root, log root, board assignment, and exact process identity. Same-board or same-resource work serializes; independent boards may run concurrently only after identity and root isolation are proven.

For C3, “lane owns” means its candidate-harness controller owns those physical capabilities. The
target agent and O cannot address the BYO server directly. The controller accepts only a structured
operation request, constructs and verifies the proposal/decision/authorization/admission chain, then
alone writes to physical MCP stdio. Missing any one of the four artifacts rejects forwarding. C4
audits process environments/handles and call ledgers for absence of a bypass path.

Stable probe/board identity is authoritative. COM ports are rediscovered live routes, not identities. Resolve the retained CoreSX1262 `P.05` notation from authoritative evidence before any dependent action; never guess it.

## 11. Hardware authorization and safety

I authorize ordinary setup, application flashing, reset, debug, memory/register inspection, UART, BLE, and bounded legal-band low-power 915 MHz LoRa work on the four named fixtures—STM-A, STM-B, NRF-A, and NRF-B—subject to the MCP server's exact live plans, permissions, and recorded delegated-authorization evidence.

The following JSON object is the complete user-issued hardware scope. Its canonical hash is the
SHA-256 of UTF-8 JSON serialized with keys sorted, no insignificant whitespace, and no ASCII
escaping. C1 copies the parsed object verbatim; no agent may infer another action or widen a bound.
S2 must produce C1-locked `MCP_METHOD_POLICY.json`, a default-deny method-and-parameter allowlist.
For each exact server method/version it records one action class, permitted parameter schema/ranges,
required safe flags, and explicit prohibited-method/parameter/side-effect predicates. A method that
can mass-erase, unlock, change protection, replace bootloader, or perform another prohibited action
is denied unless the server/live plan can technically constrain and prove that capability absent for
the exact call; it cannot be made safe merely by labeling it `application_flash` or `connect_setup`.
Unmapped methods/parameters, ambiguous side effects, and any prohibited predicate deny.
Every runtime policy evaluation is canonical and hashable; it binds the exact MCP method/version,
pinned server revision, MCP schema hash, locked policy path/hash, normalized parameters, matched rule,
action class, allow/deny result, reasons, and the policy's maximum permitted duration. Every mutating
MCP plan must contain a positive integer `max_operation_duration_seconds`; it denies if missing,
invalid, or above that policy maximum.

`USER_HARDWARE_AUTHORIZATION_V1`:

```json
{
  "allowed_action_classes": [
    "probe_discovery_read",
    "connect_setup",
    "application_flash",
    "reset",
    "debug_halt_resume",
    "memory_register_read",
    "uart_session_io",
    "ble_gatt_test",
    "lora_ping_pong_test"
  ],
  "expires_at_utc": null,
  "fixtures": ["STM-A", "STM-B", "NRF-A", "NRF-B"],
  "limits": {
    "application_flash": {
      "application_regions_only": true,
      "allow_bootloader_replace": false,
      "allow_mass_erase": false,
      "allow_protection_change": false,
      "allow_target_unlock": false
    },
    "ble": {"max_tx_power_dbm": 0},
    "lora": {
      "bandwidth_hz": 125000,
      "center_frequency_hz": 915000000,
      "coding_rate_denominator": 5,
      "max_campaign_minutes": 30,
      "max_payload_bytes": 64,
      "max_tx_airtime_ms_per_60s": 6000,
      "max_tx_power_dbm": 10,
      "spreading_factor_max": 10,
      "spreading_factor_min": 7
    },
    "uart": {"max_write_bytes_per_call": 256}
  },
  "prohibited_action_classes": [
    "bootloader_replace",
    "mass_erase",
    "protection_change",
    "target_unlock",
    "destructive_recovery"
  ],
  "schema_version": "user-hardware-authorization-v1"
}
```

These are maxima, not entitlements: authoritative live fixture/RF evidence and MCP policy may narrow
or deny them. In particular, LoRa must use exactly 915 MHz, no more than 10 dBm, no more than 64
payload bytes, no more than 6000 ms transmit airtime per rolling 60 seconds, and no more than a
30-minute campaign, with 125000 Hz bandwidth, coding rate 4/5, and spreading factor 7 through 10;
use lower power/airtime where practical. BLE transmit power is at most 0 dBm.

I do not authorize bootloader replacement, target unlock, mass erase, protection changes, or other destructive recovery. If one becomes genuinely necessary, preserve evidence and request separate authority rather than assuming it.

The user is the sole issuer of hardware authority through this Section 11 (or a later explicit user
directive). During preflight `ROOT-IM` records, but does not issue or expand,
`plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json`;
that draft cannot authorize mutation. At C1,
`ROOT-IM` mechanically creates `DELEGATED_HARDWARE_AUTHORIZATION.json` by copying the user-issued
scope and any explicit user expiry exactly, then adding only derived bindings: the exact operative
goal hash, C1 lock ID, four stable board identities, destructive exclusions, RF limits, and MCP
server pin. This is
validation and attestation, not issuance; `ROOT-IM` may neither add an allowed action nor otherwise
alter or expand the user's scope. The final artifact's canonical path is
`plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json`;
the sibling `C1_LOCK.json` records that path and SHA-256.

One candidate-owned controller process represents one retained MCP **Server Run** for exactly one
attempt/lane/board claim. Before launch, `C3-HARNESS` allocates an opaque UUID `SESSION_ID` and
atomically creates `hil/{lane-id}/sessions/{SESSION_ID}/SESSION_REQUEST.json`. That closed record
binds the exact attempt, lane, board/resource, probe/target/profile/route, C1/delegated artifact,
pinned server revision/schema, locked method policy, governing documents, target/seed/topology
identities, allowed user action classes, and a finite session deadline. It does not authorize a
hardware call. The session's permissible state transitions come only from the locked method policy;
the requester cannot supply or widen a free-form call sequence.

The controller acquires the board claim once, launches and initializes one server process, performs
only the fixed protocol bootstrap plus the side-effect-free `initialization_handshake` with empty
arguments, and atomically records `SESSION_OPEN.json` with the exact controller/server process
identities, returned Server Run ID, bootstrap transcript/hash, starting policy phase, and session-
request path/hash. It then retains the same transport, process identity, isolated roots, claim, and
Server Run across later calls. O and target workers have no write access to session control records,
server stdin, or its launch/termination capability.

Every later MCP `tools/call`--including setup, validation, plan disclosure, plan acceptance, action,
observation, and returning-state calls--is separately authorized. Its closed request binds
`SESSION_ID`, `SESSION_OPEN` path/hash, a consecutive `sequence_number`, the prior result path/hash
(canonical `null` only for the first call), and the method-policy transition from the current phase.
The controller accepts only the next sequence number, exact immutable predecessor, same session/
claim/C1/pin/policy/identity bindings, and a transition permitted by the locked policy. Dynamic
server output grants no authority: any plan object, permission, exposed action, or fallback learned
from a prior response must be copied into a new exact proposal and independently signed decision for
the next call. After each result, the controller records the resulting phase and advances only by
the immutable result chain; rejection or failure cannot be skipped or rewritten.

Normal closure requires a create-once signed
`session-close-decisions/{SESSION_ID}.json` from `F.C3.O`, binding the session-open record, exact
last result/phase, close rationale/time, and expected returning state. `C3-HARNESS` alone verifies
that decision, requires every policy-mandated returning-state call to have completed through its own
call handshake, closes stdin/server state, obtains natural exit or performs bounded exact-child
termination, drains stdout/stderr, reaps the exact process, releases the claim, and creates
`SESSION_CLOSED.json`. Expiry, revocation, watcher abort, governing-input change, invalid sequence,
call failure, or O loss instead lets the controller perform transport/process cleanup without a
signed normal-close record and create `SESSION_ABORTED.json`; it may not invent a returning-state
hardware call, record success, or call the session closed-clean. No session survives an attempt,
restarts under the same ID, or accepts a call after close/abort.

The closed executable contract for this boundary is
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
(SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`). S2 and
every later gate must implement and validate that exact contract; prose elsewhere may summarize but
may not widen it. Its default-deny gating inventory is exactly `setup_overview`, `load_setup_tool`,
`board_setup-plan`, `board_setup`, `continue_setup`, `board_fix_setup`, `board_validate`,
`get_setup_status`, `get_board_info`, `get_state`, `flash_application-plan`, `flash_application`,
`reset_and_run`, `read_memory_symbol`, `read_serial-plan`, `read_serial`, `write_serial-plan`,
`write_serial`, `serial_exchange-plan`, `serial_exchange`, and `disconnect`. All other pinned-server
methods are denied for this project, including bootloader, unlock, protection, mass-erase,
destructive-recovery, write-memory/register, breakpoint/execution-write, extended-qualification,
batch, and direct-bypass surfaces.

The decision's finite state machine is mandatory, not illustrative. Fixed candidate bootstrap ends
at `BOOTSTRAPPED`; setup/validation may advance only through the listed route, load, null-plan,
populated-plan, paired-action, continuation/fix, and ready transitions; operation plans/actions may
advance only through their listed disclosed/ready states; returning state is `disconnect` followed
by signed normal close. Runtime board IDs, routes, plan contents, permissions, continuation IDs,
response fields, and action parameters are predecessor-bound values, not preauthorized schema
values. Each is copied into a new proposal and independently signed before use. For an allowed
method with no MCP-native `*-plan`, the candidate proposal plus canonical policy evaluation is the
create-once candidate control plan; evidence must label it that way and must not claim a server plan.

Every call carries the canonical delegated-scope hash, exactly one policy action class, and a closed
`scope_effect` object. Normal calls use all-null effect fields. BLE/LoRa calls additionally bind the
exact target-operation manifest, electronic-admission paths/hashes, and limits that equal or narrow
the user maxima. Both action classes must be separately allowed and non-prohibited. `scope_effect`
is harness authorization metadata outside MCP arguments and is never forwarded to the server.

The final C1 delegated artifact has exactly five top-level keys: `schema_version`,
`issuance_source`, `canonical_user_scope_sha256`, `user_issued_scope`, and `derived_bindings`.
`user_issued_scope` is the verbatim parsed object above. `derived_bindings` has exactly
`c1_lock_id`, `operative_goal_sha256`, `stable_fixtures`, `destructive_exclusions`, `rf_limits`,
`mcp_server_pin`, `mcp_method_policy`, and `governing_documents`. Stable fixture and path/hash
subschemas are closed as specified in the decision. No agent may add an authority flag, invented
timestamp/expiry, action, fixture, C1 lock hash, or other field. ROOT writes and hashes this artifact
before writing `C1_LOCK.json`, so the construction remains non-circular.

A claimed pinned-server defect is not a free-form skip. `F.C3.O` may create only the signed request
`server-limitation-decisions/{LIMITATION_ID}.json`; `C3-HARNESS` alone validates it through the
narrow decision-defined entry point and creates
`hil/{lane-id}/server-limitations/{LIMITATION_ID}.json`. Admission requires a dispatched physical
call chain, raw pinned-server failure, exact terminal session/process evidence, pinned-source and
counterfactual attribution, and rejection of harness admission failures, unsafe/invalid calls,
fixture/operator/environment errors, hardware absence, or unknown cause. The substitute must be the
first safe available option in this order: partial MCP, focused pinned-component integration, then
candidate-boundary unit; it runs as a normal uniquely identified C3-HARNESS assignment. The original
physical test remains `NOT_CERTIFIED`, and this route can never replace, skip, xfail, weaken, or
satisfy a protected original general-harness test.

Every authorized call follows one ordered, immutable handshake. `C3-HARNESS` first allocates a fresh
opaque UUID `CALL_ID` and atomically creates
`hil/{lane-id}/call-proposals/{CALL_ID}.json`, binding exact C1/delegated path/hash, attempt, lane,
logical board, stable probe UID, reviewed target/profile, current rediscovered route (canonical `null`
when unused), session ID/open path/hash, consecutive sequence/predecessor/transition, create-once
board-identity and claim-acquisition evidence paths/hashes, MCP method/version,
pinned server revision, MCP schema hash, locked `MCP_METHOD_POLICY.json` path/hash, exact arguments,
canonical policy-evaluation object/hash, live plan path/hash, required
`max_operation_duration_seconds`, and permission result. After reading that proposal, `F.C3.O`--not
`C3-HARNESS`--atomically creates attempt-evidence
`authorization-decisions/{CALL_ID}.json`, binding proposal path/hash, the same exact fields, O's
exact process/thread identity, approve/deny decision, rationale, UTC time, and expiry. The decision
directory is O-owned; `C3-HARNESS` has read-only consumption authority and must never create or edit
a decision record. This boundary is cryptographically enforced: before launch, `ROOT-IM` creates a
fresh `O_LAUNCH_NONCE` and ephemeral Ed25519 keypair and atomically writes
`topology/ORCHESTRATOR_LAUNCH_INTENT.json` with attempt, nonce, public key, requested model/effort/
tier, and UTC time. ROOT launches O with the nonce but no private key over a bidirectional inherited
anonymous pipe. After process creation ROOT atomically creates
`topology/ORCHESTRATOR_IDENTITY.json` binding the intent path/hash, nonce/public key, and exact O
PID-plus-creation/thread/model identity, sends that identity path/hash over the pipe, and requires O
to acknowledge the exact hash/nonce over the same pipe. ROOT then atomically writes
`topology/ORCHESTRATOR_KEY_RELEASE.json` containing the acknowledgment and release UTC time, releases
the private key over the pipe, and immediately discards its copy. O may publish signed ready/work/
decision only after reading the key-release record; every signed record binds its path/hash and has
an issued time no earlier than release. The harness rejects earlier/unbound decisions. None of the
three records is rewritten; failure preserves the attempt and requires a fresh one. The private key never enters a
file, environment variable, prompt, log, target process, or harness process. O signs canonical JSON
bytes of each decision; `C3-HARNESS` verifies the signature and identity record before dispatch, and
C4 verifies provenance/signatures. Missing/invalid signature or failed key isolation blocks C3.
Only for a valid signed `approve` record does `C3-HARNESS` atomically create immutable
`hil/{lane-id}/authorizations/{CALL_ID}.json`, binding the delegated artifact and the exact proposal
and O-decision paths/hashes plus the same exact call/board/probe/target/route/identity/claim/method/
server/schema/policy/evaluation/argument/plan/duration fields. Every creation uses same-directory temporary plus create-new/no-overwrite
rename; a call ID/path is never overwritten or reused. Dispatch and result ledgers reference all
three authorization-handshake paths and SHA-256 values.
Immediately before submitting the MCP call,
`C3-HARNESS` must validate every bound field and refuse dispatch or a success record if any field is
missing, expired, mismatched, or out of scope. Post-dispatch authorization cannot cure an
unauthorized call. `F.C3.O` may approve only inside the recorded user scope; only the user may expand
authority. The actual dispatch method/version, server revision/schema, policy path/hash, normalized
arguments, freshly recomputed policy-evaluation hash, plan/duration, stable probe UID, target/profile,
route, and live create-once identity/claim paths/hashes must exactly equal the proposal, O decision,
and derived authorization; any difference denies before submission. After the call, result validation
rediscovers/records the same identity and route and revalidates the claim; mismatch forbids success
and uses bounded cleanup. Dispatch/result ledgers retain all values and hashes, and C4 verifies them.

After that validation and immediately before submission, `C3-HARNESS` samples its monotonic clock
and atomically creates immutable `hil/{lane-id}/dispatch-admissions/{CALL_ID}.json`. It binds the
authorization path/hash, freshly observed five governing-document hashes, every revalidated call/
identity/policy/plan field, monotonic clock identity, `dispatch_start_monotonic`, and
`dispatch_deadline_monotonic = start + max_operation_duration_seconds`. Creation-to-submission time
counts against the duration. Dispatch and result reference this fourth path/hash; authorization is
never rewritten.

At the actual boundary immediately before every mutating MCP dispatch, `C3-HARNESS` independently
rehashes `goal.md` plus the four governing planning/readiness documents and requires each current
hash to pass its rule: `goal.md` must exactly equal its C1 hash, while only the other four may equal
their C1 hash or valid editorial-chain terminal. It binds that live
five-hash set into the create-once dispatch admission and dispatch/result ledgers. Any mismatch expires every pending call,
refuses dispatch, emits `GOVERNING_INPUT_CHANGED`, and invokes the live-goal protocol. A ROOT-owned
read-only file watcher remains active during mutating operations; a detected mid-call mismatch is
revocation and follows the `INDETERMINATE_EXPIRED` cancellation/cleanup/no-success path.
This watcher is a registered non-agent deterministic helper with exact PID-plus-creation identity,
current hashes, and heartbeat in `topology/GOVERNING_INPUT_WATCHER.json`; it consumes no agent slot,
has no write authority outside its own topology evidence, and must exit/reap into the topology
shutdown inventory.

Expiry cannot be invented or extended by an agent. The delegated record copies an explicit
user-supplied `expires_at_utc` exactly, or stores `null` when the user supplied none; in either case it
expires immediately on user revocation/scope change, C1 invalidation/replacement, or final
completion. Every call record for an attempt expires when that attempt exits or aborts; otherwise it
uses UTC and expires at the earlier of the delegated timestamp
(when non-null) and five minutes after creation; it is one-shot and also expires on any bound-field
change. Before dispatch, remaining validity must cover the live plan's declared maximum operation
duration plus a fixed 60-second result/cleanup margin. Authorization must remain valid through
result commitment. If it expires or is revoked mid-call, request safe MCP cancellation where
supported, preserve the raw outcome as `INDETERMINATE_EXPIRED`, perform bounded cleanup, and
prohibit success; claims release only after exact child/MCP exit and reap. A retry requires a new
call ID. Only a later explicit user directive may set or extend the
delegated timestamp, which is a semantic authority change requiring a fresh C1.

The harness monitors the admission's monotonic deadline. At the declared maximum it requests safe
cancellation; if the operation does not finish, it performs the exact bounded MCP/controller
termination and cleanup contract. Result evidence records start, deadline, actual monotonic end,
elapsed duration, cancellation/termination outcome, and authorization validity. End after deadline is
`INDETERMINATE_TIMEOUT`, never success, and claims remain held until exact exit/reap/cleanup.

The C1 identity has a non-circular construction order. `ROOT-IM` first allocates a fresh opaque UUID
`C1_LOCK_ID` that is not derived from any content hash. It then creates the authorization artifact
at the canonical C1 directory bound to that ID, hashes the artifact, and finally writes sibling
`C1_LOCK.json` containing the ID, canonical authorization path/hash, and every other locked-input
hash. The lock-record SHA-256 is computed last, written to sibling `C1_LOCK.sha256`, and is never an
input to the authorization artifact. Every replacement C1 uses a new UUID/directory and the same
order; consumers may use only the path and hashes named by the operative C1 record.

Require no manual rewiring, visual inspection, button press, meter use, cable movement, or other operator intervention. Use electronic and software oracles. Use the lowest practical radio power, short packets, and bounded duty cycle. A successful flash is not behavioral success.

Do not infer that the attached module variant or current operating constraints admit 915 MHz merely
from the requested test frequency. Before RF transmit, require authoritative fixture/setup evidence
for both modules, antennas, supply/current limits, configured frequency, transmit power, bandwidth,
duty cycle, and applicable operating constraints. If that cannot be proven electronically, block
the RF-dependent gate without substituting a different frequency or requesting manual inspection.

## 12. Final physical acceptance project

The fresh final target is the **Four-Board Dual-Family Firmware Lab**, created in a disposable Git repository through the candidate harness by the separate acceptance orchestrator's multi-agent team.

S2 must create the prospective `TARGET_SEED_MANIFEST.json`. It enumerates and hashes exactly four
read-only bootstrap files: `TARGET_CHARTER.md`, `PINNED_INPUTS.json`, `TEST_CONTRACT.json`, and
`EVIDENCE_SCHEMA.json`. C1 later locks those five prepared files and separately records the
manifest's own hash. The initial C3 repository
contains exactly those five seed files and no completed application source. They are locked inputs
and target workers may not edit them. Target-created application source, tests, build files, and
target-repository-local configuration added after initialization are target-local and are versioned
in the target dependency fingerprint; a required seed-file change invalidates C1.

The required practical sprints are:

1. **P0 host and routing:** MCP protocol/schema, plans, permissions, isolated roots, toolchains, all four stable board identities, current serial routes, setup, and returning-state behavior.
2. **P1 STM32 pair:** tests first, then deterministic STM-A controller and STM-B I2C2 responder images with machine-readable UART evidence, sequence/checksum/error behavior, sustained ordered traffic, reset/reconnect, bounded recovery, and debugger observability; P1 requests every physical MCP action through the candidate harness broker.
3. **P2 nRF52 pair:** tests first, then one bounded codebase proving two-board BLE GATT command/acknowledgement and two-board 915 MHz CoreSX1262 ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence.
4. **P3 concurrent proof:** keep exactly one target doer agent (`F.C3.P1`) active and give it one candidate-harness assignment that requests two concurrent non-agent physical lane process groups: `P3.STM` owns STM-A/STM-B and `P3.NRF` owns NRF-A/NRF-B. During normal operation only `C3-HARNESS` may create, start, stop, and reap those groups; it owns both lane records, exact controller/process identities, claims, events, and cleanup, and each lane has separate MCP processes, `.firm`, artifact, and log roots. The narrow ROOT emergency host-termination rule below applies only when the controller cannot perform shutdown. `F.C3.P1` may request and operate both only through its assigned harness interfaces; it may not spawn either group or another Codex agent. Prove concurrent progress, isolation, same-resource contention/queueing, exact relays, a same-thread/path resume, one predeclared intentional target-code defect/fix, and selective retesting. Before injection, `F.C3.O` must record the exact source-controlled, non-destructive defect and expected behavioral failure. It may affect only target application source--never the harness, MCP server, fixture, authorization, or hardware configuration--and must fail through the normal target test path before candidate-launched target workers diagnose, repair, and selectively retest it.
5. **P4 shutdown and evidence:** return boards to the declared end state; close UART/debug/MCP; prove exact candidate-managed child exit/reap, zero claims, and exact event acknowledgements; stop/reap the deterministic helper and have ROOT create `topology/WATCHER_OBSERVATION_CLOSE.json`; then have `F.C3.O` atomically create attempt-evidence `EVIDENCE_MANIFEST.json` followed by `ACCEPTANCE_RESULT.json`. At a quiescent checkpoint O recursively inventories every regular file in both attempt runtime/evidence roots, with no symlink/reparse point or unresolved temporary file. The manifest lists/hashes every file, including failed/denied/conflicting evidence, except exactly itself, the not-yet-created result, and reserved `topology/`. This closed set includes the attempt-local passed registry; target seed/source and all assignments/results; event/claim/relay lifecycle; proposals, O decisions, call authorizations/admissions, MCP plans/permissions/dispatch/results; build/firmware/physical protocols; controlled defect/repair/retests; deterministic-observer evidence; and P4 candidate-managed cleanup. C1/delegated/editorial artifacts outside the attempt roots are not inventory files; the manifest lists their canonical paths/hashes only as `external_references`. After manifest creation no in-domain file may appear or change. O must create the hash-bound, non-cryptographic result within 90 seconds; it binds schema, attempt, C1, target, manifest path/hash, observation-close record, P4 state, O decision, and UTC time. C4 independently enumerates both roots, rejects every unknown/unlisted in-domain file or hash mismatch, verifies every external reference, and verifies the result. Assignment workers keep terminal `RESULT.json`. Reserved `topology/` contains O launch/key-release identity and liveness, ROOT-owned helper launch/exit/observation-close provenance, any optional AI-review provenance, and ROOT shutdown evidence. After O exits, ROOT closes/hashes that subtree in `topology/TOPOLOGY_SHUTDOWN.json`; C4 verifies its inventory separately. Pre-exit evidence does not claim O/helper exit.

P4 is ordered into two subphases. First, candidate-managed shutdown finishes; the deterministic helper
writes its terminal-service record, then ROOT stops/reaps it and writes the immutable
`WATCHER_OBSERVATION_CLOSE.json`. Only then is required observation quiescent and O may create the
manifest. Optional AI-review output may be retained but is not a closure dependency. In the manifest,
C1/delegated/editorial state is an
`external_references` array of canonical paths/hashes outside the attempt roots, not part of the
closed file inventory; C4 verifies each external reference directly against the operative C1. The
closed inventory itself remains exactly the two attempt roots minus the stated exclusions.

Use the applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intentions from the supplied experiment medium. The exhaustive A20-A26 matrix, B01-B39/Q40 corpus, Q41 endurance soaks, and destructive/try-last appendices remain extended non-gating qualification.

To avoid a second self-hash cycle, `topology/TOPOLOGY_SHUTDOWN.json` inventories and hashes every
other regular file in `topology/` but explicitly excludes itself. Symlink/reparse/temp entries are
forbidden. C4 independently enumerates that domain and separately hashes/verifies the shutdown file.

### C3 watcher requirement clarification (supersedes conflicting P4 watcher wording)

The required C3 observer is the deterministic watcher helper and its ready, heartbeat, abort, and
terminal-service evidence. `F.C3.W` is supplemental independent review: its report, final message,
and exit/reap are preserved when available but are not prerequisites for manifest closure or physical
acceptance. An early W-agent exit alone is not `WATCHER_LOST` and does not invalidate an otherwise
complete attempt.

`WATCHER_LOST` applies only to loss, staleness, or corruption of the deterministic helper/evidence.
After candidate-managed shutdown, ROOT writes create-once
`topology/WATCHER_OBSERVATION_CLOSE.json`, binding the helper ready/heartbeat/service-terminal/abort
records and exact helper identity/exit. This required record, rather than a W terminal report,
unlocks O's manifest closure. If W has exited, ROOT may also write `topology/WATCHER_EXIT.json` with
available report/final-message provenance; that record is supplemental and never blocks acceptance.

### Pooled finding rule (supersedes conflicting immediate-abort wording)

Every review, selected test set, and watcher/observer completes its assigned affected surface or
selection, records its complete finding set, and hands it to one triage gate. Triage deduplicates
the set and authorizes one bounded repair batch; no ordinary finding may stop peer checks, restart a
review, or trigger an in-gate repair/rerun. Watchers record non-critical violations for that pooled
triage rather than aborting the run.

The only immediate-stop exception is exact evidence that continuing risks an unauthorized or
wrong-resource operation, loss of containment or cleanup of a live process, or irreversible
corruption of evidence needed to judge later work. ROOT owns that stop, preserves all evidence, and
the normal post-gate repair/relock route applies. A failed assertion, non-dangerous behavior mismatch,
incomplete non-critical evidence, target/test defect, or safely contained harness defect is recorded
and pooled instead.

### Outer C3 failure isolation rule

An error in outer C3 setup, launch, monitoring, report handling, evidence validation, or emergency
cleanup is an outer-attempt procedure failure, not a candidate failure. Correct a harmless procedure
or paperwork error in place and continue. If it prevents honest closure of the immutable attempt,
close that attempt and use a fresh namespace. Preserve every candidate/test result whose immutable
evidence and dependency fingerprint remain valid. Do not reopen candidate implementation, C0/C1/C2,
or a green candidate test merely because an outer procedure failed.

Escalate to candidate repair/relock only when exact evidence shows that the outer failure changed a
C1-locked candidate input, caused the candidate to behave incorrectly, or made the candidate result
itself untrustworthy. ROOT owns this classification and must record its reason before rerunning work.

## 13. Required observer, pooled findings, and support-failure isolation

This section is operative and supersedes every later or earlier sentence in this file that makes an
AI watcher report/exit acceptance-critical, treats every observer finding as an immediate abort, or
turns an outer support failure into a candidate reset.

ROOT directly starts the deterministic watcher helper from the reusable external support layer,
binds its exact process identity, and waits for its ready record before target work. The helper runs
through candidate-managed shutdown, writes heartbeat/cursor and terminal-service evidence, and is
stopped/reaped by ROOT. ROOT then writes create-once
`topology/WATCHER_OBSERVATION_CLOSE.json`. The record resolves helper identity, readiness,
heartbeat, abort disposition, terminal service, and exit through either the normal primary source or
the exact predeclared independent backups in the evidence-fallback matrix. Optional AI-watcher
artifacts are supplemental only.

Reviews, selected test sets, and observations finish their assigned surface and pool all
non-critical findings into one deduplicated triage and one bounded repair batch. Only exact evidence
of an unauthorized/wrong-resource operation, loss of live-process containment/cleanup, or
irreversible corruption of evidence required to judge later work may stop live execution
immediately. That safety stop preserves evidence and does not by itself invalidate product credit.

A setup, fixture, runner, watcher-helper, report, schema, evidence-writer, monitoring, launch,
supervision, or cleanup bug is `OUTER_ATTEMPT_PROCEDURE_FAILURE`, not a product failure. Correct it in
place when the product outcome remains determinable. If the support failure leaves insufficient
evidence to determine whether a valid product passed, mark only that affected work
`INCOMPLETE`/`INDETERMINATE` and use a fresh support/physical attempt as needed. Preserve all other
immutable candidate/test credit. Reopen candidate work or a product gate only when exact evidence
shows a changed product dependency, incorrect candidate behavior, or a candidate result that cannot
be trusted.

Cleanup never signals an unverified PID. An already-exited or identity-uncertain registered child is
recorded without signalling it, and cleanup continues for every other registered child. The failed
attempt is not misreported as a clean pass.

### Orchestrator liveness and closure

`ROOT-IM` monitors O's exact process plus `topology/ORCHESTRATOR_HEARTBEATS.jsonl` from O readiness
through result commitment and normal exit. Manifest creation starts the bounded result-commit
deadline. Unexpected O exit, lost/stale liveness, deadline without a valid result, or normal exit
without a valid result is `ORCHESTRATOR_LOST`: stop new work, clean only the registered topology,
preserve the partial attempt, and classify it under the support-failure boundary above. A partial
manifest/result is never completed or reused in place.

After a valid result and O's exact normal exit/reap, ROOT writes create-once
`topology/ORCHESTRATOR_EXIT.json`. On abnormal loss, `ORCHESTRATOR_LOST.json` retains available
identity/exit/final-message evidence and never claims normal exit. `TOPOLOGY_SHUTDOWN.json`
inventories the applicable record.

Termination authority is ordered. ROOT first requests ordinary controller-managed shutdown. Only
when the exact registered controller is unavailable or unresponsive may ROOT perform host-process
termination/reap of the pre-registered controller/MCP/process-group identities. ROOT atomically
writes `topology/EMERGENCY_TERMINATION.json` with the shutdown request/path/hash, failure proof,
exact identities, per-process terminate/reap outcomes, and UTC/monotonic times. This is not authority
to call MCP, manipulate hardware, infer board success, or kill an unregistered process. Board state
becomes indeterminate, the attempt cannot pass, and the next attempt must run P0 returning-state
recovery through a healthy controller before mutation.

`ROOT-IM` must then:

1. terminate only the registered acceptance process tree;
2. preserve the failed runtime and evidence;
3. repair the harness or watcher through the owning implementation large step and its existing two-loop topology, preserving unchanged green IDs;
4. if any C1-locked input changes, run fresh C0, create a new C1 lock, and run dependency-invalidated C2 IDs;
5. apply the C3 restart protocol below only after the latest required C1/C2 pair is green.

Firmware application, compiler, target-test, target-repository configuration, and invalid-MCP-call defects are not harness aborts. Here "target-repository configuration" means configuration created inside the disposable C3 target repository whose dependency fingerprint is owned by that target project; it excludes the C1-locked harness configuration, acceptance-kit/lane templates, MCP launch templates, server pin/configuration, fixture bindings, authorization, and test/evidence contracts. Target-local defects remain work owned by `F.C3.O` and are repaired through target assignments submitted to `C3-HARNESS`. If a target finding requires any locked configuration/input to change, it leaves the target-local route and follows the C1 invalidation route.

A reproduced defect or incompatibility in the pinned BYO Firmware MCP server implementation is
neither target-source work nor a watcher `ABORT_REQUIRED`, and repairing that server is outside this
goal. The clean pinned worktree stays immutable; `ROOT-IM`, `F.C3.O`, implementation coders, and
target workers may not edit, recommit, or repin it.

`F.C3.O` may mark one affected test `AUTHORIZED_SERVER_LIMITATION` only with exact evidence that the
candidate reached and correctly contained the server boundary: call/method/version, raw MCP result
or failure, process and returning-state evidence, implicated pinned-source evidence, and why the
failure belongs to the server rather than the harness, target, fixture, inputs, or operator. O then
assigns the strongest safe substitute through `C3-HARNESS`: first a supported partial end-to-end MCP
test, otherwise a focused unit/integration test using the implicated pinned-server component,
otherwise a synthetic unit test of the candidate boundary. The original physical test is retained
as limited, not called green; the substitute has its own stable ID. No route may use direct
pyOCD/serial, weaken safety, silently skip evidence, or claim unexecuted physical behavior was
certified. C4 independently validates attribution and that no stronger safe substitute was
available. This exception never applies to the protected original general-harness unit tests.

Every C3 attempt uses a monotonically increasing immutable namespace
`plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/` and matching evidence
namespace `plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/`, beginning at
`attempt-0001`. Choose one greater than the largest number present in either runtime or evidence;
use `0001` only when neither side contains an attempt. Both paths for the chosen number must be
absent; a one-sided path or collision stops allocation for preservation/triage. Each attempt contains
its own `target/`, `hil/`, `events/`, `claims/`, `manager-signals/`, and `.agent-workspace/` roots.
Create the pair together; never clear, overwrite, fill a numbering gap, or reuse a prior attempt,
and leave completed/failed attempts retained read-only.

Every C3 restart caused by `ABORT_REQUIRED`, orchestration/evidence rollover, or another prescribed
attempt-ending condition uses a
new attempt namespace and fresh disposable target Git repository. The initial attempt begins from
the five locked seed files only. A restarted repository may reconstruct the exact last accepted
target source-tree commit plus the same locked seed, but it must not copy old build outputs, runtime
state, claims, events, or process records. P0 always reruns for the fresh attempt. Earlier green
target evidence remains credited only where its declared dependency fingerprint is unchanged;
tests dependent on the changed goal/harness/server/runtime/repository/process identity rerun from
the earliest invalidated sprint, and every new-attempt artifact originates in its numbered roots.

## 14. Audits and final verification

- C0 uses a fresh read-only Terra-medium-Fast reviewer with no implementation ownership. It reviews
  only a frozen joined candidate that has passed its shortest affected smoke IDs, completes the
  entire assigned candidate/critical-control-path sweep, and returns one complete finding set rather
  than stopping at the first defect. Remaining focused execution may overlap C0, but C1 waits for
  their exact-revision join.
- C0 explicitly audits backward compatibility and the original general-harness unit baseline before physical work.
- C2 runs the dependency-invalidated original unit tests, cross-route tests, disposable dual-path project, synthetic MCP/lifecycle, relay, event/ack, contention, resume, cleanup, and operator gates.
- C1 locks the operative goal/planning-document hashes, exact candidate revision, server pin/configuration, acceptance-kit and lane/MCP launch templates, fixture bindings, the five-file target seed, test/evidence contracts, authorization, and other implementation inputs consumed by C2/C3. It does not lock target application source or target-repository-local configuration subsequently created through `C3-HARNESS`; those are versioned in the target dependency fingerprint. If C2 repair changes a C1-locked input, the lock is invalid and a new C1 plus dependency-invalidated C2 are mandatory. Production, policy, behavioral-contract, coverage-obligation, or other operative changes return to the owning implementation step and full fresh C0. A qualifying pre-C3 strict test-only fast lane correction never inherits the old lock; changed candidate/test bytes still require a new C1 and dependency-invalidated C2, but it needs only its eligibility record and exact failed-ID rerun before that lock. Environment-only reruns and target-local changes that change no C1-locked input do not require re-locking. C3 may start only from the latest green C1 lock and its green C2 evidence.
- C4 uses fresh Terra-medium-Fast auditors after practical success.
- C4 audits C1-C77 coverage, orchestration-role separation, watcher boundary, physical evidence, exact revisions, protected state, scope, and baseline-to-candidate unit-test preservation.
- C4 and the safeguard require a current governing-input disposition: exact operative C1 equality or
  a valid append-only classification/editorial terminal for each change. A mismatch pauses admission
  and refreshes C1 as needed, but reruns only gates consuming a changed domain. Candidate/product,
  authority, or acceptance-evidence changes follow their owning routes; unrelated green gates remain
  credited. C4/safeguard never invent a second final lock.
- A C4 "evidence-only correction" means only a C4-owned report/annotation fix written outside every immutable C3 attempt root, under `plans/general-coding-harness/evidence/firmware-v2/final/C4/annotations/`. It cannot satisfy, alter, explain away, replace, or add any acceptance requirement/artifact. Any missing, incorrect, inconsistent, or incomplete closed C3 evidence requires a fresh C3 attempt from P0 and the earliest invalidated sprint, then C4. Target-source/local-config findings do the same. A repair changing a C1-locked input returns through its owning step, fresh C0/C1/C2, fresh C3, and C4. This C0 route is the sole ordinary post-lock exception.
- After C4 is green, complete the one logical `SAFEGUARD_RUN_ID` for the exact C1 lock under Section 9's admission/resume rule.
- Also run the outer repository verification required by `AGENTS.md` before final completion, including `--full` when the changed behavior triggers that requirement.

## 15. Completion criteria

Do not return as complete until all of the following are true:

1. C1-C77 each have exact evidence and no unresolved in-scope gap.
2. The original successful general harness remains protected by a complete green unit-regression matrix with no hidden weakening.
3. Existing schema-less firmware callers require no migration and the coding V1 path remains correct.
4. The separately orchestrated physical project passes STM32 I2C, nRF52 BLE, nRF52 LoRa, and concurrent four-board behavior.
5. Every accepted production-relevant harness, watcher, firmware, MCP, compiler, application, and
   test defect encountered in scope has been diagnosed, minimally repaired, and selectively
   retested; cosmetic, unreachable, behavior-neutral, and speculative non-findings remain deferred.
6. No required hardware action depended on guessed wiring or unauthorized destructive recovery.
7. All exact managed worker, helper, MCP, debug, UART, and watcher processes are exited and reaped.
8. All resource claims are released, all required top-level events are exactly acknowledged, and no actionable request/relay residue remains.
9. C0 and C4 audits are clean.
10. One terminal logical accumulated-safeguard record is green on the exact C1 lock with no incomplete component.
11. The required outer development verification is green.
12. Completion, candidate, server, acceptance, watcher, topology, criteria, protected-state, full-verification, promotion, and out-of-scope evidence are written.
13. The promoted runtime is fresh, inactive, and ready for general use while the prior rollback remains preserved.

If work remains safely possible, continue. Do not stop merely because the task is long, difficult, or required multiple repair cycles.
