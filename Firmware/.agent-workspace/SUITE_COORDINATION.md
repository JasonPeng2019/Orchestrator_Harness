# Current suite coordination

Suite-010 terminal update: `2026-08-21`  
State: `COMPLETED_WITH_FINDINGS`

- Sole terminal handoff: `.agent-workspace/epochs/20260821-plan2-suite-010-manager-012/TERMINAL_SPRINT_HANDOFF.md`.
- Required admission correction passed under `AUTONOMY_AUDIT_CORRECTED_002` with `--require-target`; original suite-009 evidence remains preserved.
- Complete selected pool: A20/A21/A24/A25 `FAIL`, Q40 `PASS`, D30/D32/D34/Q41 `BLOCKED`.
- No suite-010 worker, reviewer, watcher, MCP lifetime, plan, permission, lease, claim, or hardware action was created. Target remains clean at `5ab4b1f2f9170c3e57c35883bcb1ad22a2d04815` / `17e67a7affd2d16e1b1104e1df3dec22bfa198eb`.
- Sprint 011 was not started; control returns to ROOT.


Recovery-010 terminal update: `2026-08-20T22:36:00Z`  
State: `SUITE008_COMPLETED_WITH_FINDINGS`

- Sole terminal handoff: `.agent-workspace/epochs/20260820-plan2-suite-008-resume-010/TERMINAL_SPRINT_HANDOFF.md`.
- A21 responder identity/order gate passed, but bounded REQ-003 traffic failed; A25's corrected one-call route returned no `nrf_b` profile. D30/D34 board-free checkpoints remain valid; their live dependency edges are blocked.
- All recovery doer/provider/watcher identities are absent, fresh canonical claims are empty, and the accepted target remains clean at `dd673cb304501bfc2228b8c44f41df45a0c8608f` / `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`.
- Two possible target-v2 behaviors are recorded only as suspected harness findings for ROOT classification. This manager did not start another indexed sprint.

Current ROOT update: `2026-08-20`
State: `PLAN2_EDGE_011_FIRMWARE_RESUME_READY`

- Plan 2 v3.9.25 preserves M07/M08 credit and resumes directly at `EDGE-011` and the unfinished
  logical Firmware sprint. No continuation product repair, verification asset, or affected M08
  rerun is pending. The harness-clean streak is `0/3`.
- Suite008's runtime epoch is stopped, but its logical sprint and verified semantic checkpoints are
  the continuation input. Direct PID inspection on 2026-08-20 found the recorded
  manager `191900`, Sol `199628`, watcher `187868`, A21 controller/provider `198392`/`201268`, and
  A25 controller/provider `202348`/`199208` absent. This proves process absence only; it does not
  fabricate claim release, checkpoint acceptance, or completion.
- No manager epoch, provider session, server plan/permission, lease, claim authority, MCP action, or
  hardware action is live. Recorded user delegation does not revive Suite-008 authority. ROOT's
  dispatch of `PLAN2_SUITE_RECOVERY_MANAGER_PROMPT_009.md` creates fresh runtime authority.
- ROOT-IM reconciled the retained `055a5bd...` boundary through empty final review 062, proof 063,
  and integration/readback 064. The clean detached target and `firmware/v2-candidate` at
  `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
  `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`, are the exact accepted Firmware sprint input.
- The test orchestrator owns every logical lane and sprint until completion. It recovers affected
  lanes across provider replacement, preserves verified checkpoints, continues unrelated eligible
  work, and never returns or terminalizes a logical lane/sprint merely because an execution issue
  occurred. It records possible harness errors as suspected findings with evidence, affected
  lane/unit, observed and expected behavior, containment, continuation, and cleanup facts. ROOT
  neither intervenes nor diagnoses mid-sprint; it classifies the complete pool after completion and
  authorizes only justified between-sprint repairs.

## Historical Suite-008 last live snapshot

Suite-008 snapshot time: `2026-08-16T13:24:40Z`
Historical state: `STOPPED_AFTER_LIVE_FRESH_PARALLEL_A21_A25`

- Manager `PLAN2.SUITE.MANAGER.009`: controller PID `191900` created
  `2026-08-16T13:00:12.781780Z`; Sol PID `199628` created
  `2026-08-16T13:00:14.286948Z`; session `01a00aa8-9a8c-7592-8b69-e5e054a0009b`.
- Accepted target remains clean/detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
  `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Server snapshot is HEAD
  `61e7efc747f66d39263020265aa608950b0d281b`, tree
  `610b5b7c8f7660a8bd1ba8ee530f84bfce6cb66a`, fresh 94-file manifest
  `af680774882033fec53410af14fdf13044c9ea2119b3e68bb6ea09c9c77a2b63`.
- Diagnostic watcher PID `187868`, creation `windows-filetime:134313596971508876`, is READY,
  owner-bound to Sol PID `199628`, poll 150 seconds, no-progress threshold 720 seconds,
  `evaluator_enabled:false`.
- Fresh persistent Qwen reviewers: A21 `6a2e18e6-761d-45ec-adb9-759c1cd18bf4`, A25
  `2c70a86a-79a8-44d3-84d8-694830d73459`, D30
  `b05125a2-a3fa-44af-975a-6f3901f65e55`, D34
  `72ffb129-79e3-4312-811a-e03fb8eb09fd`. Their launches were direct, all nine claims each were
  verified, and current reviewer controllers are release-safe with zero held claims.
- Boreal/A21 `PLAN2.A21.BOREAL.022`: controller PID `198392` created
  `2026-08-16T13:24:28.918484Z`; provider PID `201268` created
  `2026-08-16T13:24:32.936639Z`; session `33e57760-be42-4b41-9511-2105ac93bb83`; all 18
  STM/provider/workspace/MCP claims verified. It adopts only clean commit `4a888b6...` and admitted
  unchanged-input build/UART proof, then freshly verifies live identity/roles before REQ-003.
- Delta/A25 `PLAN2.A25.DELTA.015`: controller PID `202348` created
  `2026-08-16T13:24:28.936585Z`; provider PID `199208` created
  `2026-08-16T13:24:33.161525Z`; session `c3e672fa-943c-436b-ac71-737ed5b10eca`; all 22
  Nordic/provider/workspace/MCP claims verified. It independently commits the exact one-file UUID
  correction and builds both roles fresh before live validation.
- Both launch-verification latches are published, no pause marker exists, and A21/A25 HIL overlaps
  under disjoint full claims. D30/D34 retain only matching board-free checkpoints. D30 awaits the
  exact A20 artifact; D32 follows D30. D34 HIL awaits only A21 plus the A23/A24 nRF edge. Q40 uses
  only real inputs; Q41 follows the declared Atlas edge; Nova has no work.
- At this snapshot, the target-clean streak remained `0/3`. ROOT's separate harness-evidence review
  was not read. This section supplies history, not live authority.

Suite-007 terminal update: `2026-08-16T12:49:18Z`
State: `TERMINAL_INCOMPLETE_ROOT_OWNED_SCOPE_BARRIER_FORCED_CONTAINMENT`

- Terminal handoff:
  `.agent-workspace/epochs/20260816-plan2-suite-007/TERMINAL_SPRINT_HANDOFF.md`.
- A21 and A25 exceeded their frozen repair/build boundaries after external pause/diagnosis sidecars
  appeared without a native actionable request. Experimental images are now present on both STM
  boards and NRF-B; exact identities are sealed in the handoff and receive no acceptance credit.
- Both exact doer controllers finalized with empty Windows Job boundaries and zero Suite007 claims
  after exact provider/Qwen descendant containment. No `RESULT.json` exists and reviewers were not
  resumed for terminal evidence review.
- D30/D34 and downstream D32/D34/Q41 remain dependency-blocked; Q40 and Nova receive no invented
  work or credit. The sprint is not accepted and target-clean streak remains `0/3`.
- Suite006's 22 historical claims remain untouched. The accepted target remains clean/detached at
  `dd673cb304501bfc2228b8c44f41df45a0c8608f` and was never edited or pushed.

Suite-007 update: `2026-08-16T12:06:00Z`
State: `LIVE_PARALLEL_HIL_AND_REVIEWER_CONTINUITY`

- Manager lane `PLAN2.SUITE.MANAGER.008`: controller PID `169036`, created
  `2026-08-16T11:54:37.105031Z`; Sol PID `191392`, created
  `2026-08-16T11:54:39.340712Z`; session `01a00a6c-9116-7501-b210-a1302f84d23c`.
- Accepted target remains clean and detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`,
  tree `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Server snapshot is HEAD
  `61e7efc747f66d39263020265aa608950b0d281b`, tree
  `610b5b7c8f7660a8bd1ba8ee530f84bfce6cb66a`, complete tracked+untracked
  manifest `7163d17286a0910ab6d4ada156077844458f466ef5f8c15496e2d99eb0c3efd8`.
- Suite006 is terminal and historical. Its 22 A25 claim files remain untouched. Suite007's fresh
  canonical lock root began empty and now owns exactly 76 verified claims across the admitted batch.
- Diagnostic watcher PID `199940`, creation `windows-filetime:134313554269718298`, is READY,
  owner-bound to Sol PID `191392`, polling at 150 seconds with a 720-second evidence threshold and
  `evaluator_enabled:false`.
- Boreal/A21 lane `PLAN2.A21.BOREAL.021`: fresh replacement session
  `dbc9b49c-2823-4fc3-8b1b-d41a2d3faf52`, controller PID `183676`, provider PID `159224`, all 18
  declared STM/provider/workspace/MCP claims verified. Active prompt contains the exact PLLM/PLLR
  field correction, single-rebuild and pre-flash proof boundary.
- Delta/A25 lane `PLAN2.A25.DELTA.014`: fresh replacement session
  `4354ec22-6c3d-4c28-b059-1550b7a642d7`, controller PID `195960`, provider PID `196412`, all 22
  declared Nordic/provider/workspace/MCP claims verified. The lane adopts commit `c1904c6e...` and
  reproduced Role A/B artifacts with an explicit no-rebuild boundary.
- Persistent Qwen reviewer sessions: A21 `abd9a94b-1104-432b-89e0-4a8ec4c12ab5`, A25
  `7e1b7a43-e00a-471e-b9c6-2ca94dd2b80f`, D30
  `827cdf67-f10b-4998-b7a7-b3de68bda2d9`, D34
  `62947b74-4d7f-452b-a1ae-8f81638c9586`. Each has nine isolated claims and is read-only.
- D30 and D34 preserve adopted board-free checkpoints. D30 still awaits the exact accepted A20
  APP-1/debug-trampoline artifact; D32 follows D30. D34 HIL waits only on A21 and its declared
  A23/A24 Nordic edge. Q41 follows its Atlas edge. Q40 advances only from real inputs; Nova has no work.
- Current target-clean streak remains `0/3`. ROOT's separate harness-evidence review is not a suite input.

Suite-006 update: `2026-08-16T11:44:31Z`
State: `TERMINAL_INCOMPLETE_ROOT_OWNED_CONTINUATION_AND_RETAINED_BOUNDARY_BARRIER`

- Terminal handoff:
  `.agent-workspace/epochs/20260816-plan2-suite-006/TERMINAL_SPRINT_HANDOFF.md`.
- A21 is stopped and boundary-empty but cannot truthfully satisfy ROOT's required active-prompt
  amendment because its persisted task-card digest names assembled Markdown, not an existing JSON
  task-card artifact accepted by the amendment validator.
- A25's corrected task-local relaunch is stopped with no provider and zero claims acquired. The
  earlier interrupted controller left 22 fail-closed `INVENTORY_UNKNOWN` claim records whose
  retained-boundary evidence is incomplete. They remain exact input to the resumed lane and may be
  released/reassigned only after complete exact absence proof; they were not
  deleted or rewritten.
- Every recorded delegated controller/provider exact identity is absent; no matching MCP/helper
  remains. The evaluator-disabled watcher stopped cooperatively and its exact identity is absent.
- The accepted target remains clean/detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`,
  tree `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. The sprint earns no target-clean credit; streak
  remains `0/3`.

Historical live-state detail follows and is superseded by this terminal update.

- Epoch `20260816-plan2-suite-006`; manager lane `PLAN2.SUITE.MANAGER.007`, controller PID
  `190816` created `2026-08-16T10:11:01.495413Z`, Sol PID `161620` created
  `2026-08-16T10:11:03.252819Z`, session `01a00a0d-b851-7c21-9c6f-05a20647807e`.
- Accepted target is clean/detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
  `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Server snapshot is HEAD
  `61e7efc747f66d39263020265aa608950b0d281b`, commit tree
  `610b5b7c8f7660a8bd1ba8ee530f84bfce6cb66a`, tracked-diff fingerprint
  `1ce5a45f8da18050885c86c7d8fb175d4ba235ef`; no repair barrier is active.
- Watcher PID `196588`, creation identity `windows-filetime:134313494095300785`, startup token
  `6d2f61dd-01b1-443b-b423-58dbfc4bfd2c`, is `READY`, owner-bound to Sol PID `161620`, polling
  every 150 seconds with a 720-second evidence threshold and `evaluator_enabled:false`.
- Suite-005 processes, watcher, plans, permissions, leases, claims, MCP/server lifetimes, and live
  evidence are historical only. Fresh suite-006 run roots adopt only hash-validated sealed specs,
  source/build artifacts, reviewer continuity inputs, and matching board-free proof.
- Boreal/A21 lane `PLAN2.A21.BOREAL.020` is `HIL_RUNNING`. Controller PID `161676` created
  `2026-08-16T10:25:24.964351Z` acquired all 18 declared claims before provider PID `203184`
  created `2026-08-16T10:25:36.083967Z`. Claims include both exact STM boards/probes/COM ports,
  fixed PB13/PB14 I2C peer/link, STM USB scope, isolated MCP/server lifetime/state/artifact root,
  provider slot, workspace, cache, and artifacts. Firmware commit and all six artifacts match the
  accepted suite-005 handoff.
- Delta/A25 lane `PLAN2.A25.DELTA.012` is `BUILDING` board-free. Inspection rejected a false
  `BUILT_WAITING_FOR_LEASE` adoption because NRF-B lacks BLE-central stimulus, four separate APP-6
  queues are absent, and NRF-B performs command work in its UART ISR. It owns the smallest fresh
  DeepSeek-high completion task and no board/radio/USB claim. Nordic HIL will use a different fresh
  controller/provider identity declaring all Nordic resources before provider start.
- Persistent suite-006 Qwen reviewers are `PLAN2.A21.REVIEWER.010`,
  `PLAN2.A25.REVIEWER.011`, `PLAN2.D30.REVIEWER.012`, and `PLAN2.D34.REVIEWER.013`. Each is
  read-only, isolated, and forbidden from hardware/server-source access; it is later resumed only
  for its owning module's evidence review.
- Atlas/D30 and Cygnus/D34 adopted their matching suite-005 board-free checkpoints. D30 HIL remains
  blocked only on the absent exact accepted A20 APP-1/debug-trampoline artifact; D32 follows the
  completed D30 handoff. D34 HIL remains blocked only on accepted A21 plus a materialized declared
  A23/A24 Nordic baseline and the fresh four-board lease. Q41 follows its declared Atlas edges.
- Manager-owned Q40 indexing is preserved without invented coverage credit or duplicate branches.
  All ordinary doers are assigned or dependency-blocked; Nova receives no work. Target-clean streak
  remains `0/3` pending terminal handoff and ROOT classification.

Suite-005 update: `2026-08-16T10:01:30Z`
State: `TERMINAL_ROOT_OWNED_LAUNCH_AUTHORITY_BARRIER_CLEANED`

- Terminal handoff: `.agent-workspace/epochs/20260816-plan2-suite-005/TERMINAL_SPRINT_HANDOFF.md`.
- The first dependency-ready doer/reviewer batch launched concurrently. A21 completed its exact
  closed PLLSRC repair and both rebuilds; D30 and D34 completed board-free checkpoints. A25 exited
  without its required checkpoint/result and receives no acceptance credit. Q40 receives no
  credit; Nova received no work.
- Native instruction `root-a21-missing-hardware-claims-001`, event
  `b48b37fe29b269aa3685bec7343228a77d71269e9a02a077ae4f59807edbf223`, stopped A21 before HIL:
  its canonical persistent identity lacks all hardware/MCP/server claims and cannot add them on
  resume. No populated plan, ordinary permission, flash, or accepted result exists.
- Watcher stopped cooperatively. All 17 recorded delegated suite-005 identities are absent,
  canonical claims are empty, and no delegated provider or MCP boundary remains. The accepted target remains clean/detached
  at the stated commit/tree. Target-clean streak remains `0/3`, unclassified here.

- Epoch `20260816-plan2-suite-005`; manager lane `PLAN2.SUITE.MANAGER.006`; controller PID `66692`
  created `2026-08-16T09:28:07.5376900Z`; Sol provider PID `42932` created
  `2026-08-16T09:28:09.2109410Z`, session `01a009e6-6f3f-7d72-9bf9-98f0bc5f427c`.
- Accepted target is clean/detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree
  `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Suite-004's retained STM-A claim is historical,
  untouched, and never consulted as suite-005 authority. Suite-005 uses only
  `runtime/orchestrator-harness/20260816-plan2-suite-005/canonical-resource-locks`.
- Fresh run roots are `A21_20260816-plan2-suite-005`, `A25_20260816-plan2-suite-005`,
  `D30_20260816-plan2-suite-005`, and `D34_20260816-plan2-suite-005`, plus matching fresh reviewer
  roots. `ADOPTED_INPUTS.json` records every retained specification/source/build/board-free
  evidence file and explicitly excludes controller status, transcript, plan, permission, lease,
  server state, resource assignment, result, process authority, and live evidence.
- First dependency-ready doer batch after watcher READY and fresh reviewer bindings: Boreal/A21
  exact closed PLLSRC source repair and rebuild; Delta/A25 two-Nordic-only rebuild/fixture route;
  Atlas/D30 board-free preparation pending exact A20 input; Cygnus/D34 board-free continuation;
  manager-owned Q40 incremental indexing. D32 follows D30, D34 HIL waits only on A21 plus its
  declared Nordic edge, and Q41 follows its Atlas edge. Nova has no assigned work.
- No suite-005 board plan, permission, lease, validation stamp, MCP lifetime, hardware action, or
  resource claim exists at this prelaunch boundary. Fresh delegated authorization is recorded in
  `.agent-workspace/USER_DELEGATED_AUTHORIZATION.md`.

Suite-004 update: `2026-08-16T09:21:18Z`
State: `TERMINAL_ROOT_OWNED_INCOMPLETE_BOUNDARY_CLEANED`

- Terminal handoff: `.agent-workspace/epochs/20260816-plan2-suite-004/TERMINAL_SPRINT_HANDOFF.md`.
- ROOT externally stopped A21 controller PID `168480`, created `2026-08-16T09:04:35.676423Z`, before complete retained-boundary cleanup. The accepted target correctly preserves its exact `board:STM-A` claim as `MAY_EXIST_INCOMPLETE`; it remains focused-continuation proof input and cannot be reacquired until complete exact old-owner/process absence is established.
- A fresh A21 controller proved the barrier without launching a provider or holding a claim and was stopped by exact identity. All suite worker/provider/MCP boundaries are absent. Watcher PID `190780` was stopped cooperatively.
- A21 remains nonterminal with a closed PLLSRC scaffolding repair checkpoint. A25 remains nonterminal because host Intel Bluetooth was not in the assigned fixture; resume requires explicit resource authority or a valid fixture-only stimulus. D30/D32/D34/Q41 retain only their declared dependency barriers. Q40 has no coverage credit; Nova received no work.
- Exact Nordic and provisional STM actions are recorded in the terminal handoff and manager JSONL. No destructive or topology-changing action occurred.
- Accepted target remains clean/detached at `dd673cb304501bfc2228b8c44f41df45a0c8608f`, tree `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`. Target and BYO server source were not edited.
- No terminal module `RESULT.json` exists. The manager makes no target-clean streak classification and did not launch or read ROOT's Terra evidence reviewer.

Replacement update: `2026-08-16T06:02:11Z`
State: `BLOCKED_FOR_ROOT_TARGET_REPAIR_CLEANED`

- Manager `PLAN2.SUITE.MANAGER.004` successfully proved the corrected normal watcher start and
  cooperatively stopped it with exact watcher identity absent.
- D30, D34, and A25 completed board-free preparation with release-safe controller cleanup. A25
  exceeded the sealed build and pause bounds before completing. A21 failed three distinct
  validated launches before status, claims, or provider start. Further affected launches are
  frozen; all child boundaries, claims, and the watcher are cleaned.
- ROOT handoff: `.agent-workspace/epochs/20260816-plan2-suite-003/TARGET_DEFECT_HANDOFF.md`.
- No hardware plans, permissions, leases, tool calls, hardware actions, results, target edits,
  server edits, or remote pushes occurred. Target-clean streak remains `0/3` pending ROOT review.

Updated: 2026-08-15 for Plan 2 parallel hardware continuation
State: `WAITING_FOR_ROOT_SUPERVISOR_CONTRACT_RECONCILIATION`

## Historical epoch 20260816-plan2-suite-003

- Manager lane: `PLAN2.SUITE.MANAGER.003`; invocation `plan2-suite-manager-003`.
- Controller: PID `203072`, created `2026-08-16T05:06:23.691833Z`.
- Provider: Codex `gpt-5.6-sol`, PID `200376`, created
  `2026-08-16T05:06:26.343827Z`, session
  `01a008f6-ddf0-7062-ba04-47863bf4f6af`.
- No prior doer/reviewer session, plan, permission, lease, MCP lifetime, or process authority is
  reused. A21 adopts only the immutable `SPEC_REVIEWED` specification/evidence checkpoint.
- Target commit is detached `055a5bd137039eaa1917e4a859a3d5bf30eb6444`. ROOT asserted a clean
  accepted launch, but current read-only reconciliation found untracked
  `orchestrator_harness/portable_orchestrator_harness.egg-info/`, created
  `2026-08-16T05:05:06.9479329Z` before this provider started. The manager will not delete, edit,
  repair, or conceal it; it is retained as a preparation/target hygiene signal.
- Server snapshot: HEAD `61e7efc747f66d39263020265aa608950b0d281b`, source tree
  `2a1769b931de075c699627d315da81448461af5b`, tracked-diff fingerprint
  `1ce5a45f8da18050885c86c7d8fb175d4ba235ef`; reviewed dirty surface currently includes
  `README.md`, `pyrightconfig.json`, and `tests/`. No repair barrier is active.
- Read-only host inventory: STM-A `066FFF514988525067233337`/COM12, STM-B
  `0668FF514988525067213913`/COM17, NRF-A `683710208`/COM16, NRF-B
  `683854191`/COM15; all present/OK. Connectivity grants no lease.
- Initial eligible board-free batch: Boreal/A21 implementation-build, Delta/A25
  specification-build, Atlas/D30 specification/address-map preparation, Cygnus/D34
  specification/host preparation, plus manager-owned Q40 indexing.
- Deferred: A21/A25 HIL await their fresh artifacts, reviewed plans, ordinary permissions, exact
  leases, and reverified identities; D30 consuming cases await exact verified A20 artifacts; D32
  awaits Atlas's D30 handoff and each shard's own artifact edges; D34 HIL awaits A21 plus its nRF
  baseline edge and exclusive four-board lease; Q41 awaits an Atlas handoff and each shard edge.
- Nova has no eligible work (A23-only and forbidden for Q40). No other named doer is idle, so no
  missing Q40 branch is assigned in this pass.
- Watcher launch barrier: ROOT's `BOUNDED-TEST-v1` supervisor rejected the required combination
  before Python was spawned: an expected upper bound of 20 seconds with an 8-second cleanup
  allowance is rejected because that supervisor caps cleanup at 5 seconds for a 20-second bound.
  No bounded result or watcher runtime was created. The normal target `start` path therefore has
  not run and cannot be classified. The manager did not weaken the parameters, use `serve`, edit
  the target, or launch any lane. Exact next action is for ROOT to reconcile its supervisor with
  the controlling 20+8 requirement (or explicitly amend that requirement), after which watcher
  start uses a new unique result stem and READY is required before lane launch.

## Current authority and resume inputs

Current package authority is:

- `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`
- `.codex/skills/run-firmware-test-suite/SKILL.md` and its references
- this ledger and each future run's `.agent-workspace/`

`multi-agent-logs/HANDOFF.md`, `multi-agent-logs/PROGRESS_REMAINING.md`, and
`multi-agent-logs/current-state/CURRENT_SUITE_STATE.json` are imported historical evidence only.

The imported records establish that no prior manager epoch, doer process, reviewer process,
controller, MCP process, board lease, server-repair barrier, watcher, or hardware action is active.
Their old absolute paths, PIDs, leases, configs, and process records are historical only. Do not
revive them or treat them as current authority. The current user authorization is recorded in
`USER_DELEGATED_AUTHORIZATION.md`; it authorizes a new Plan 2 sequence, not an imported run.

## Preserved progress

Main-reviewed green:

- H00-H05
- S10-S13
- A20, A23
- D33, D36

Checkpointed, nonterminal persistent lanes:

- Atlas: A22, then D30/D32/Q41
- Boreal: D31, then A21
- Cygnus: A24, then D34
- Delta: A26, then A25

The imported current-state record names the original run roots, but those `fresh-experiments/`
directories are not currently materialized in this package. Their checkpoints therefore cannot be
resumed yet. Preserve the recorded progress classification, but do not claim live session or
filesystem continuity. Before resuming one of these lanes, either materialize and validate its
exact run directory or create a fresh affected run with an explicit handoff that retains only the
evidence actually available here.

Remaining main-suite work after an authorized resume:

- A21, A25, D30, D32, D34, Q40, Q41

Appendix-only non-gating work: D35, R37, R38.

The historical M5 attention-validation goal is closed at Q10 with `0/3` comparable qualifying sprints. Q10
passed the harness and watcher gates but lacked sufficient manager evidence because wake records
were ordered incorrectly and responses omitted lane IDs. This is not evidence of a current
harness, watcher, or MCP-server defect. Never launch Q11. It is unrelated to the new Plan 2
hardware sequence.

## Current Plan 2 indexed clean sequence

Plan 2 v3.9.25 starts at `0/3`. Each predeclared catalog scenario receives a stable
`logical_sprint_id` and `sprint_sequence_index`; one replaceable manager epoch may host several and
launch every dependency-ready resource-compatible lane. Apply completed results by index, not
arrival order. A completed accepted sprint that ROOT classifies harness-clean adds one. A sprint
with suspected harness findings still completes and seals the full pool. ROOT reviews only after
that terminal handoff: a confirmed harness defect resets to `0/3` and receives any accepted repair
before the next indexed sprint; a rejected suspicion or suite-owned issue does not automatically
reset. Server/firmware/
specification/fixture/doer defects are corrected or terminally recorded in the same sprint, while
every feasible unrelated lane continues. Runtime interruption replaces the invocation and authority;
it does not create a new sprint or terminal failure. The only normal terminal statuses are
`COMPLETED_CLEAN` and `COMPLETED_WITH_FINDINGS`. The Qwen bridge no-tool smoke remains accepted.

The retained accepted watcher coordinate is
`055a5bd137039eaa1917e4a859a3d5bf30eb6444` (tree
`3f6f4c7d17881b7c4cfdd21ab31f00c710067ff6`), while the current clean target points at
`dd673cb304501bfc2228b8c44f41df45a0c8608f`. Final review 062, proof 063, and integration/readback
064 reconcile that accepted descendant and bind it as the focused repair base. The normal Windows watcher start path has direct
nested-Job `READY`, status, cooperative-stop, independent-review, and 52-test post-join proof.
The target-clean streak remains `0/3`; this repair was discovered before a retry sprint performed
any hardware action and therefore earns no sprint credit.

## Preserved A21 retry checkpoint

- Retry epoch `20260816-plan2-a21-002`, run
  `fresh-experiments/A21_20260816-plan2-a21-002`, is sealed `SPEC_REVIEWED`.
- The Qwen 397B reviewer returned `SPEC_APPROVED` with no actionable finding.
- No doer, plan, permission, lease, MCP action, board operation, or hardware action began.
- The A21-only Sol manager was intentionally stopped because it contradicted the suite-wide
  parallel scheduling contract and because native watcher start exposed the now-repaired target
  defect. Its exact artifacts are retained under
  `.agent-workspace/epochs/20260816-plan2-a21-002/manager-archive-002/`.
- A replacement manager may adopt the sealed specification as a checkpoint, but it must create new
  provider sessions and all new live authority. It must not claim conversation or lease continuity.

## Next suite-wide scheduling pass (prepared at EDGE-011)

ROOT dispatches the prepared replacement logical manager against accepted target `dd673cb...`.
The manager first reconciles suite-008's verified semantic checkpoints, resumes every unfinished
lane from its first unresolved action under fresh runtime/action authority, and launches every eligible
nonconflicting lane in one scheduling pass:

- Boreal: continue A21 from the first unresolved responder byte-identity/order gate; revalidate only
  affected electronic state before any newly authorized live action.
- Delta: retry the malformed A25 `setup_overview` call with the corrected invocation shape and
  continue its remaining Nordic validation under fresh authority.
- Atlas: reuse the valid D30 board-free checkpoint, advance to D32 only through its declared
  handoff/dependency edge, and retain Q41 for its later dependency point.
- Cygnus: reuse the valid D34 board-free checkpoint; its HIL waits only on A21 and the declared
  Nordic baseline, not on unrelated board-free work.
- The manager advances Q40 indexing whenever its declared inputs are ready and assigns any missing
  branch only to an idle named doer.

Board-free tasks overlap freely. Hardware tasks overlap only when exact leases do not conflict. A
wait or server-repair barrier blocks only its owning lane; unrelated lanes continue.

## Historical first A21 epoch

- Epoch: `20260815-plan2-a21-001`; selected scenario: `A21` only.
- Target: clean detached `Firmware/target-harness/` at
  `1302d90b2e1439c6f7f66031821a8f452a159f78`.
- Manager lane: `PLAN2.A21.MANAGER.001`; controller PID `167616` created
  `2026-08-15T23:32:06.438596Z`; Sol provider PID `175512` created
  `2026-08-15T23:32:07.789888Z`; session
  `01a007c4-c4ca-7b00-b1d0-def351b5f5cc`.
- Watcher: initial PID `190932` and replacement PID `197624` were stopped cooperatively while
  correcting the observed-source set. Current PID `184960`, creation identity
  `windows-filetime:134313112390898255`, startup token
  `b5fa4f37-0887-44cd-b084-170e1d87ad53`, is READY
  with `evaluator_enabled: false`, 150-second polling, 720-second evidence-based no-progress
  threshold, and exact manager PID/creation binding.
- Isolated run: `fresh-experiments/A21_20260815-plan2-a21-001`, sealed `SPEC_READY`.
- Reviewer lane `PLAN2.A21.REVIEWER.001`: canonical Qwen invocation prepared for
  `qwen3.5:397b-cloud`; session `3370c320-ca7b-4340-990e-309a90d640c5` returned
  `SPEC_APPROVED` with no actionable findings and was exactly cleaned.
- Boreal lane `PLAN2.A21.BOREAL.001`: session
  `eb4a855d-b6e2-4a2a-b4c0-8db858db6927` completed the board-free checkpoint. Manager structural
  review quarantined intermediate commit `261961f` because it still carries a non-L476 RCC map.
- Fresh A21-only HIL lease `SOL-PLAN2-A21-001-HIL-LEASE-001` is issued through
  `RESOURCE_ASSIGNMENT.md` for STM-A/STM-B, their exact probe/VCOM identities, the fixed I2C peer,
  scoped electronic reconnect, and an isolated MCP process/artifact root. It authorizes no action
  until the board-free correction, live identity, populated plan, and normal permission all agree.
- No live MCP action or hardware action has occurred yet.

## A21 terminal classification

- A21 ended `INCOMPLETE_NOT_PASSED`; there is no `RESULT.json`, PASS,
  SERVER_FAILURE, harness-defect classification, or target-clean claim.
- STM-A matched and completed bounded setup/validation, but its only flash
  action was refused before write because the initial stack pointer exceeded
  verified SRAM1. STM-B's exact probe/VCOM identity was absent from live
  inventory, and no substitute was used.
- Boreal committed the authoritative STM32L476 register correction at
  `1461d4d`; a later 96 KiB SRAM1 linker correction remains uncommitted in the
  isolated firmware worktree.
- Setup evidence used package `.firm/` instead of remaining wholly inside the
  assigned A21 MCP root. This is retained as a truthful routing/configuration
  mismatch, not classified as a server or harness defect.
- After a cooperative pause was not observed at successive safe setup/planning
  boundaries, the manager stopped the exact verified provider-owned process
  tree. Controller cleanup is reaped, boundary empty, and claim release-safe.
- The one terminal suite handoff is
  `.agent-workspace/epochs/20260815-plan2-a21-001/TERMINAL_SUITE_HANDOFF.md`.
  ROOT alone selects any later work.

## Future scheduling and target contract

Launch every dependency-ready, resource-compatible named lane concurrently. A waiting lane never
stops unrelated work. Catalog section 11.1 is the cross-test dependency authority.

This section is usable only after `EDGE-011`. Before any live resume, the external owner must prepare the exact WIP product worktree at
`target-harness/` and launch the test orchestrator from `Firmware/`. Run the package audit with
`--require-target`, reconcile the imported checkpoints against the current files and target, and
create fresh epoch configs and runtime roots. Use the target's bounded
`orchestrator_harness watch --until-actionable` path plus its owner-bound deterministic
`harness_watcher_implementation` process with `evaluator_enabled: false`; do not use the old
stable-only managed-watcher/heartbeat interface.

## Future role allocation

No prior provider session is live or resumable. The [provider-adapter contract](../PROVIDER_ADAPTER.md) owns
the provider/model/effort/tier allocation, current route status, and required pre-launch record.
Its local distinction between named doers, the one sprint reviewer, the server implementer, and
repair-test/scaffolding roles applies here without duplication.

ROOT may separately launch its mapped harness-evidence reviewer only after the sprint's terminal
handoff. Its report goes to ROOT, not this ledger: the test orchestrator must not read, schedule,
store, or act on it.

## Future invocation record

After `EDGE-011` and before launching work, append the new invocation and record:

- manager PID plus creation identity and epoch ID;
- exact `target-harness/` Git revision and dirty state;
- exact `BYO-Firmware-MCP/` server state;
- each catalog task, doer, provider session, reviewer, run directory, and phase;
- which imported result/checkpoint edges were revalidated and retained;
- build and HIL prerequisites;
- workspace, process, board, probe, serial, radio/peer, USB/power, cache, state, and artifact leases;
- current waits and safe checkpoints;
- current user hardware authorization, if any; and
- exact next eligible actions.

Keep new manager logs below `.agent-workspace/epochs/<epoch>/`, harness observations below
`runtime/orchestrator-harness/<epoch>/`, watcher state below
`target-harness/runtime/harness-watcher/<epoch>/`, and run-specific state inside its run.

## 2026-08-21 plan2-firmware-suite-012 manager-014 terminal record

- Authority: manager PID 31484, creation `windows-filetime:134318005537080841`; all prior runtime authority treated dead; suite-012 standing four-board non-destructive delegation used.
- Target: clean `5ab4b1f2f9170c3e57c35883bcb1ad22a2d04815` / tree `17e67a7affd2d16e1b1104e1df3dec22bfa198eb`.
- Units: S10 GREEN, S11 GREEN with suspected target finding, S13 GREEN, D36 GREEN, Q40 accepted SERVER_FAILURE source/baseline finding.
- Terminal disposition: `COMPLETED_WITH_FINDINGS`; handoff at `.agent-workspace/epochs/20260821-plan2-suite-012-manager-014/TERMINAL_SPRINT_HANDOFF.md`.
- Cleanup: watcher cooperatively stopped; all suite controller/provider/MCP/helper identities absent; boards logically disconnected; claims/leases/permissions/plans terminal.

## 2026-08-21 plan2-firmware-suite-013 manager-015 terminal record

- Admission selected exactly S10, S11, S13, and D36. S12 was excluded for unchanged non-elevated
  host policy; Q40 was excluded for the still-absent qualifying-source/baseline prerequisite.
- S10 and S11 each ended schema-valid, independently reviewed `SERVER_FAILURE` after two genuinely
  fresh exact-current server lifetimes returned an empty debug-connection inventory while serial
  choices exposed the expected boards. No setup or hardware action became possible.
- S11 preserved both Nordic electronic identities. The mandatory intentional other-probe case was
  truthfully `NOT_REACHED`, received no credit, and remains part of the finding impact.
- S13 and D36 completed fresh board-free work and ended schema-valid, independently reviewed
  dependency-contained `SERVER_FAILURE`; no historical setup was substituted and no live case was
  credited.
- Terminal disposition: `COMPLETED_WITH_FINDINGS`. Sole handoff:
  `.agent-workspace/epochs/20260821-plan2-suite-013-manager-015/TERMINAL_SPRINT_HANDOFF.md`.
- Watcher stopped cooperatively; worker/provider/MCP/helper boundaries are absent, hardware remained
  logically disconnected, and claims/plans/permissions/leases are terminal. Suite 014 was not
  started.
