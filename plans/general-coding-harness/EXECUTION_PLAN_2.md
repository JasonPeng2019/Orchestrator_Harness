# EXECUTION_PLAN_2: Backward-Compatible Physical Firmware Acceptance

## 0. Metadata

- **Goal:** implement `GENERALIZATION_SPEC_2`, retain the accepted coding and legacy firmware paths, and certify the candidate with a separately orchestrated MCP-backed four-board firmware project.
- **Plan inputs:** `HANDOFF.md`; `active_docs/GENERALIZATION_SPEC_2.md`; `active_docs/IMPLEMENTATION_ROADMAP_2.md`; `active_docs/EXECUTION_READINESS_2.md`; `Firmware/Firmware resources/test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`; `Firmware/Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md`; `Firmware/Firmware resources/SOURCE_MANIFEST.csv`; the pinned BYO Firmware MCP source; current harness docs, source, and tests.
- **Authoritative implementation runner:** clean detached `stable-general-harness-runner` at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`.
- **Protected rollback:** independently recoverable detached `pre-conversion-rollback` at `287ea53793e3963062882012ff80c3b0e8c41587`; `frozen-harness-to-use` is a temporary locked alias.
- **Protected historical worktrees:** the 13 retained linked harness worktrees from the completed
  plan are recorded inputs, never V2 lanes or cleanup targets.
- **Firmware MCP baseline:** clean worktree to be materialized from `f003f84a7df51cd8595a3203c62e225b21da2a22`; the present dirty checkout is never reset or used as the release candidate.
- **Fresh runtime root:** `plans/general-coding-harness/runtime/firmware-v2/`.
- **Fresh evidence root:** `plans/general-coding-harness/evidence/firmware-v2/`.
- **C3 attempt roots:** matching monotonically increasing immutable runtime/evidence
  `acceptance/attempt-NNNN/` pairs beginning at `attempt-0001`; allocate one greater than the
  largest number on either side and never reuse or gap-fill an attempt number.
- **Fresh promoted runtime:** `plans/general-coding-harness/runtime/promoted-firmware-v2/`, absent
  until every promotion gate passes.
- **Harness mode:** candidate-harness-manager-owned orchestration; `evaluator_enabled: false`;
  ROOT-launched deterministic observer plus optional non-gating AI reviewer.
- **Current Portable Harness binding:** manager begins with `scan --no-write`, consumes native events through `watch --until-actionable`, clears only exact top-level events through `ack --event-id`, stores coordination state below `.agent-workspace`, records joins in `PARALLEL_CHECKPOINT.md`, requires terminal `RESULT.json`, and uses `manager-signals` only as the manager-owned repair channel. The one explicit non-manager exception is the isolated watcher's create-once attempt-evidence path `watcher/ABORT_REQUIRED.json`, monitored directly by `ROOT-IM`; it is never written or relayed through `manager-signals`.
- **Planning boundary:** this document specifies execution. It does not itself launch agents, edit product code, start the harness, run tests, or operate hardware.
- **Runner transition:** complete and frozen. The former physical `harness-in-progress/` path is
  absent. `.git/modules/harness-in-progress` and its local submodule key remain historical shared
  Git metadata for the registered linked worktrees and are never an operational launch root or a
  mid-execution rename target.
- **Pinned launcher:** every implementation controller enters through
  `.codex/scripts/stable_runner.py` and the exact
  `plans/general-coding-harness/runtime/firmware-v2/runner-migration/STABLE_RUNNER_LOCK.json`. The
  launcher proves path/commit/clean/detached state,
  rejects candidate/lane import contamination and protected outputs, and retains only trusted
  interpreter roots. No lane invokes the controller package directly from its working directory.
- **Stable/candidate gate caveat:** `4699d27` predates the executable finding gate. Projection may
  remove candidate-only fields; `ROOT-IM` independently validates the original current-tip finding,
  result, and triage artifacts. Candidate C2/C3/safeguard testing proves automatic candidate gate
  enforcement.
  - **Current execution point:** execution is user-paused for next-run preparation. Preflight and
    S1-S3 are green. S30's production repair, independent reviews, focused regression, and four-ID
    execution are complete on joined tip `6649cf201ded9782c2cb3bc56983f4a560728ea8`; ROOT has not yet
    archived/admitted it to reserved candidate `c6999d173c344b317a918df91619308fd9f93f63`.
    Topology/support preparation may update governing documents and the external support code only.
    On explicit resume, classify the governing diff by lock-input domain, preserve unchanged S30
    credit, admit that exact tip, complete mandatory S4 and then mandatory S5, then run the shortest
    affected S4/S5 smoke, fresh C0/C1, dependency-invalidated C2, and the host-only C3 rehearsal. The pinned server remains immutable
    and unlaunched; C3/hardware stay locked until all prerequisites pass.
- Gaps / surfaced issues: none

The required `none` value above refers to unresolved planning/specification ambiguity. The accepted
C0 product finding and its bounded S2 repair/review status are execution state recorded immediately
above and in `PARALLEL_CHECKPOINT.md`; they are not an unplanned scope or topology gap.

The earlier general-coding execution plan is complete and is not restarted. This bounded
firmware-compatibility release has begun and resumes only from its current checkpoint.

## 1. Agent-per-role mapping

All child agents are launched headlessly with `codex exec` in Fast mode. Fast means the ordinary model slug plus explicit `service_tier="priority"`; it is not a `-fast` model name. Every child launch uses the required full-access/no-approval controls, `--ignore-user-config`, an isolated working root, and captured thread/process/exit evidence. No launched role may omit the priority tier or substitute a different model.

The current outside root is `ROOT-IM`, the host implementation coordinator. It is not a launched
subagent and is outside the model/effort/tier assignment contract. Every child explicitly uses `--dangerously-bypass-approvals-and-sandbox`,
`--dangerously-bypass-hook-trust`, `--ignore-user-config`, `--json`, exact model/effort/tier flags,
and `-C` bound to its assigned root. Resumable lanes are not ephemeral. Processes authorized to own
an MCP server receive an explicit isolated declaration because ignored user configuration cannot
supply one; in C3 that is only the candidate physical-lane controller, never O/target workers.

| Role | Agent/model | Pool size | Reasoning | Tier | Responsibilities |
|---|---|---:|---|---|---|
| Orchestrator / planner-executor | Current `ROOT-IM` host session | 1 | not assigned | not assigned | Outside implementation coordinator; partitions work, owns integration, triage, repair routing, checkpoints, and final promotion; not a launched subagent. |
| Coder-main | GPT-5.6 Terra | 1 | medium | Fast / priority | Serial product coder for harness, MCP, acceptance-medium, or target source; never more than one active coding owner. |
| Reviewer-main | GPT-5.6 Terra | 2 | medium | Fast / priority | Independent static reviewers and test writers; two lanes only where file and question ownership are disjoint. |
| Doer-main | GPT-5.6 Luna | 2 | high | Fast / priority | Independent test executors/doers; two lanes only for isolated test shards or resources. |
| Final-reviewer | GPT-5.6 Terra | 1 | medium | Fast / priority | Fresh read-only final review; no step history or implementation ownership. |
| Acceptance-orchestrator | GPT-5.6 Sol | 1 | high | Fast / priority | Fresh `F.C3.O` subagent; runs the candidate harness and alone orchestrates the final target project. |
| Supplemental acceptance reviewer | GPT-5.6 Terra | 0 or 1 | medium | Fast / priority | Optional fresh `F.C3.W` read-only reviewer; never the required observer and never gates closure. |

`Orchestrator / planner-executor` is the validator-required row name for `ROOT-IM`; it does not make
`ROOT-IM` a launched Sol child. Role interpretation is strict: source edits are coder work; test
design/writing and review are reviewer-main work; test execution and hardware operation are
doer-main work, except the explicit isolated S4.D1 supplemental-feature implementation-doer
exception in Section 5. `ROOT-IM` coordinates creation of the product with those subagents. `ROOT-IM` is
never `F.C3.O` and never assigns final target-project work. `F.C3.O` is a separately launched
subagent and the sole target-project decision-maker.

`C3-HARNESS` denotes the candidate harness control plane and its exact controller processes operated
by `F.C3.O`; it is the system under test, not a Codex-agent role and not an agent slot. `F.C3.O` submits every target assignment
to `C3-HARNESS`. Only `C3-HARNESS` launches the assigned target worker through `codex exec`, owns its
lifecycle, and records its exact launch/result/event/claim evidence. `F.C3.O` must not directly
launch a target worker. Gates and evidence use `ROOT-IM`, `F.C3.O`, the deterministic helper,
optional `F.C3.W`, or `C3-HARNESS`
instead of an ambiguous unqualified "orchestrator" or "manager."

The validator-required final-phase lane ID `F.C3.M` is an alias for `ROOT-IM`. It never denotes a
new process, nested manager, launched subagent, or additional agent slot. Every occurrence of
`F.C3.M` in Section 7 therefore has exactly the same identity and authority as `ROOT-IM`.

The headless launch preflight must prove Sol-high-priority, Terra-medium-priority, and Luna-high-priority. A launch failure blocks preflight; it does not authorize the earlier Sol-for-Luna substitution.

## 2. Coverage checklist

| ID | Atomic completion requirement |
|---|---|
| C1 | Start from exact clean harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`. |
| C2 | Preserve frozen rollback `287ea53793e3963062882012ff80c3b0e8c41587`, prior runtimes, and unrelated outer changes. |
| C3 | Use a new isolated harness candidate branch/worktree without rewriting `4699d27`. |
| C4 | Create a clean isolated MCP worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`; do not alter the dirty source checkout. |
| C5 | Validate all 47 resource-mirror byte counts and SHA-256 hashes. |
| C6 | Do not mutate hardware before live authorization and plan evidence. |
| C7 | Retain exact harness, server, toolchain, pack, datasheet, fixture, and target hashes. |
| C8 | Isolate runtime, MCP state, artifact, and log roots per run and lane. |
| C9 | Preserve schema-less firmware invocation as the legacy dispatch route. |
| C10 | Preserve canonical policy bytes, digest, headings, embedded text, and final reminder checks. |
| C11 | Preserve legacy label-derived outputs and firmware event-log naming. |
| C12 | Preserve accepted legacy model, lease, board, MCP, snapshot, prompt, output, and resume fields. |
| C13 | Keep coding invocation V1 and its repository/result safety unchanged. |
| C14 | Reject ambiguous cross-route input and result shapes. |
| C15 | Run retained legacy fixtures, examples, and configurations without edits. |
| C16 | Require no migration, evidence rewrite, or new public firmware schema. |
| C17 | Limit shared normalization to behavior-preserving duplicate lifecycle logic. |
| C18 | Prove coding and firmware lanes coexist through dual-route automated tests. |
| C19 | Correlate worker/controller/helper/descendant identity by PID, creation evidence, and owner. |
| C20 | Correlate current MCP launcher/server/provider lifetimes exactly to the lane. |
| C21 | Bind hardware relay to exact request, arguments, lane, snapshot, decision, and expiry. |
| C22 | Keep invalid/expired/changed/unbound relays visible but non-authorizing. |
| C23 | Preserve firmware checkpoint/resume thread and path identity without invented liveness. |
| C24 | Emit native lifecycle events and clear only exact top-level acknowledgements. |
| C25 | Distinguish current operational leases from historical board declarations. |
| C26 | Give generic and hardware claims exact ownership and fail-closed stale handling. |
| C27 | Permit independent boards to progress without shared-state contamination. |
| C28 | Serialize same-board and same-resource work without double ownership. |
| C29 | Release claims/resources only after exact child/MCP exit and reap. |
| C30 | Treat unknown, partial, corrupt, or ambiguous lifecycle evidence as actionable and fail closed. |
| C31 | Broker every physical operation through the candidate controller to BYO Firmware MCP; O/target workers never hold the physical endpoint or launch capability. Retain one exact controller-owned server process/claim per finite board session while separately authorizing and chaining every post-bootstrap MCP tool call. |
| C32 | Pin the MCP revision as an immutable compatibility fixture. No project role may edit or repin it; proven defects/incompatibilities use evidence-gated `AUTHORIZED_SERVER_LIMITATION` substitution. |
| C33 | Give each physical lane controller a distinct MCP process/endpoint, `.firm`, artifact, and log root, with no endpoint inheritance by O/target workers; bind session request/open/close-or-abort evidence to its exact Server Run/process/claim. |
| C34 | Bind and rediscover all four stable board/probe identities. |
| C35 | Treat COM ports as live routes rather than board identities. |
| C36 | Match authoritative STM32 I2C2, UART, ground, and pull-up fixture bindings. |
| C37 | Resolve `P.05` authoritatively before dependent CoreSX1262 actions; never guess. |
| C38 | Match datasheet, device-pack, and compiler hashes/locks. |
| C39 | Lock canonical scope/policy; every mutation binds governing hashes, exact call/identity fields, bounded duration, signed decision, authorization, immutable pre-dispatch admission, dispatch, and result; enforce monotonic deadline/expiry fail-closed. |
| C40 | Exclude bootloader replacement, unlock, mass erase, and protection changes. |
| C41 | Constrain LoRa frequency intent, power, packet length, and duty cycle. |
| C42 | Use electronic/software physical oracles only. |
| C43 | Create each fresh disposable Four-Board Dual-Family Firmware Lab repository in the next immutable attempt namespace from exactly the five C1-locked seed files (or, on restart, that seed plus the exact accepted target source-tree commit). |
| C44 | Implement deterministic STM-A controller and STM-B responder images. |
| C45 | Prove STM32 I2C, UART, reset/reconnect, debug, recovery, and sustained traffic. |
| C46 | Prove deterministic two-board nRF52 BLE GATT exchange. |
| C47 | Prove deterministic CoreSX1262 ping/pong and radio telemetry. |
| C48 | Under one active `F.C3.P1` assignment, pass STM32 I2C and nRF52 LoRa concurrently in two non-agent physical lane process groups created, started, stopped, reaped, and owned only by `C3-HARNESS` on all four boards. |
| C49 | Retain build provenance and MCP-mediated setup/flash/reset/debug/memory/UART evidence. |
| C50 | Use behavioral oracles, not flash success, as the application gate. |
| C51 | Inject one predeclared intentional, source-controlled, non-destructive target-code defect with a recorded expected behavioral failure; diagnose, repair, and selectively retest it through the normal target path. |
| C52 | Checkpoint and resume one physical lane with the same thread/path identity. |
| C53 | Prove independent concurrency and same-resource contention with distinct lane/controller/process/claim/event/MCP roots while preserving the one-target-agent cap. |
| C54 | Close boards/candidate state; stop/reap the deterministic helper and write `WATCHER_OBSERVATION_CLOSE.json` from primary or approved fallback evidence before O closes the two attempt-root inventories; list locked external artifacts only as directly verified references, then separately close/hash ROOT's remaining O/topology inventory. |
| C55 | Use fresh Sol-high-Fast subagent `F.C3.O`, never `ROOT-IM`, for practical-acceptance decisions; require `C3-HARNESS` to launch and own every target worker. |
| C56 | Keep `ROOT-IM` as implementation supervisor, never target-task orchestrator. |
| C57 | Use a ROOT-launched isolated deterministic helper with ready, heartbeat/cursor, pooled-finding, terminal-service, exact launch/exit, and observation-close evidence; optional Terra-medium-Fast AI review is supplemental. |
| C58 | Handle the three exact helper immediate-stop conditions and O liveness/result-commit loss safely: contain registered identities, preserve evidence, and classify product versus support cause. Missing support evidence rolls only incomplete attempt work unless product behavior cannot be determined or exact product-defect evidence exists. |
| C59 | Use `ABORT_REQUIRED` for harness/watcher defects; keep target application/compiler/test/target-repository-configuration/invalid-call defects inside the target project only when no C1-locked input changes; treat a proven immutable pinned-server defect/incompatibility as `AUTHORIZED_SERVER_LIMITATION`, require exact attribution and the strongest available partial/unit substitute, disclose the physically uncertified portion, and never repair or repin the server. |

**C3 observer clarification (supersedes conflicting terminal-report wording):** Required observation
is the deterministic helper's ready, heartbeat/cursor, pooled-finding/abort-disposition, and terminal-
service evidence. ROOT launches it directly through `.codex/scripts/c3_outer_support.py`. The Terra
watcher agent is optional supplemental review; its absence/exit never invalidates an attempt. After
candidate-managed shutdown, ROOT writes required create-once
`topology/WATCHER_OBSERVATION_CLOSE.json`, binding each required fact to its primary source or the
predeclared independent fallback sources plus exact helper identity/exit. That record unlocks O's
manifest closure.

**Pooled finding rule (supersedes conflicting immediate-abort wording):** Every review, selected
test set, and observer/watch lane completes its assigned affected surface or selection, records the
complete finding set, and hands it to one triage gate. Triage deduplicates and authorizes one bounded
repair batch; ordinary findings do not stop peer checks, restart a review, or trigger repair/rerun
during the gate. Observers record non-critical violations for post-gate pooling. Immediate stop is
only for exact evidence that continuing risks an unauthorized/wrong-resource operation, loss of
containment or cleanup of a live process, or irreversible corruption of evidence required to judge
later work. ROOT owns the stop and preserves evidence.

**Outer C3 failure isolation rule:** An error in outer C3 setup, launch, monitoring, report handling,
evidence validation, or emergency cleanup is an outer-attempt procedure failure, not a candidate
failure. Correct harmless procedure/paperwork errors in place. If it prevents honest immutable-attempt
closure, close only that attempt and use a fresh namespace, preserving every candidate/test result
whose immutable evidence and dependency fingerprint remain valid. Do not reopen candidate
implementation, C0/C1/C2, or a green candidate test solely because an outer procedure failed.
Candidate repair/relock is allowed only on exact evidence of a changed C1-locked candidate input,
incorrect candidate behavior, or an untrustworthy candidate result; ROOT records the classification
before rerunning work.

If a support bug or mistake leaves enough independent evidence to decide how a valid candidate
behaved, that product test may still pass. If it does not, mark only the affected test/attempt
`INCOMPLETE` or `INDETERMINATE` and repeat only that incomplete work. Support failure never becomes a
product failure by attribution shortcut.
| C60 | Use exact requested headless models, effort, tiers, and launch owner with no substitution: `ROOT-IM` launches `F.C3.O` and optional `F.C3.W`, ROOT directly launches the non-agent helper, while `C3-HARNESS` launches target workers and `F.C3.O` never does so directly. |
| C61 | Keep production coding singleton/serial and all genuine role fan-out within 1-3. |
| C62 | Give each large step exactly two QA loops; do not cycle per module. |
| C63 | Preserve green tests through a C1-frozen implementation registry and manifest-covered per-attempt C3 registry; rerun only dependency-invalidated IDs. |
| C64 | Complete one terminal green logical `SAFEGUARD_RUN_ID` after practical success/audit; pre-admission is outside the run, environment-only interruption resumes it selectively, and a locked-input change requires a new lock/run ID. |
| C65 | Gate on applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intent. |
| C66 | Keep exhaustive apps, Q40 corpus, Q41 soaks, and destructive/try-last cases non-gating. |
| C67 | Bind evidence to exact revisions, identities, tests, artifacts, authorization, and hardware observations. |
| C68 | Obtain a fresh final reviewer decision after a complete frozen-tip sweep, with no unresolved production-relevant in-scope gap and no intentional first-finding stop. |
| C69 | Audit requirements, topology, watcher boundary, evidence, and protected state. |
| C70 | Promote only the locked green candidate into a fresh inactive runtime while preserving rollback. |
| C71 | Teach legacy firmware, coding V1, dual path, events, ack, resume, and cleanup accurately. |
| C72 | Add no unnecessary framework, scheduler, abstraction, board expansion, UI, database, endurance gate, cosmetic repair, behavior-neutral cleanup, or speculative fix without a concrete negative deployment consequence. |
| C73 | Prove through a protected baseline-to-candidate unit matrix that the original successful general harness still works, with all invalidated original and new cross-route unit tests green and no weakened coverage. |
| C74 | Bind one worker thread to one logical task card; permit only same-task continuation routes before acceptance and reject unrelated reuse after semantic acceptance. |
| C75 | Preserve accepted lane evidence/revision, remove the terminal lane from active discovery, safely close clean unused worktrees, retain archive-only results/transcripts, and discard disposable caches. |
| C76 | Support static read-only lanes against an exact immutable source commit with a separate writable result root and no linked worktree; retain isolated worktrees for mutation or source-local execution. |
| C77 | Serialize concurrent shared event-log appends with one cross-process lock so each writer waits, writes and flushes one complete record, and releases without corruption or loss. |

## 3. Decomposition and disposition

Atomic changes and individual modules are not execution steps. Preflight gates (no full cycle) establish provenance, authority, model availability, and clean roots. The implementation then uses the smallest three large steps that each produce a coherent feature or deliverable. Included modules remain bundled because their contracts fail or pass together; the table explains why one full QA cycle, implemented as exactly two back-to-back loops, is warranted for each bundle.

| Input area | Disposition | Assigned large step | Included modules | Coherent feature or deliverable | Why one full QA cycle |
|---|---|---|---|---|---|
| Promoted general-coding path and safety | Reused as-is | S1 and regression gates | coding V1 parser, repository identity, result safety, generic claims, events, protected original unit-test manifest | Protected compatibility baseline | Its baseline-to-candidate unit matrix is a mandatory non-regression oracle; it is not independently rebuilt. |
| Legacy schema-less firmware loader | Reused with minor adjustment | S1 | policy binding, invocation fields, result routing, resume | Supported backward-compatible firmware contract | Parser, prompt, result, and lifecycle behavior form one public boundary. |
| Firmware lifecycle reconciliation | Re-decomposed | S1 | exact processes, MCP lifetimes, requests/relays, leases, claims, cleanup | Honest firmware-lane lifecycle | These states share identity and release invariants and must be reviewed/tested together. |
| Fixture, toolchain, and MCP materials | Reused with minor adjustment | S2 | pinned server, manifest, board profiles, plans/permissions, isolated roots | Reproducible MCP acceptance substrate | Provenance and physical safety must agree before any target project can run. |
| Exhaustive experiment catalog | Re-decomposed | S2 | H/S/A/D core subset, bounded four-board project, extended qualification ledger | Sufficient harness certification medium | A bounded representative matrix exercises the harness without recertifying the entire server. |
| Acceptance schemas and simulations | Newly implemented | S2 | charters, stable IDs, dependency fingerprints, synthetic MCP, evidence/result contracts | Runnable test kit | Test data, failure classification, and evidence shapes must be validated as one kit. |
| Operator and release surface | Re-decomposed | S3 | quick-start, examples, dual-path config, commands, evidence templates, disposable integration | Backward-compatible release candidate | Operators need one consistent end-to-end flow and proof that both paths coexist. |
| Physical target applications | Deferred to final acceptance by design | F.C3 | STM controller/responder, nRF BLE/LoRa modes, concurrency scenario | Fresh target project created through candidate | Prebuilding the target would weaken the harness test; `F.C3.O` must decide the work and `C3-HARNESS` must launch the workers that create it. |
| Full A20-A26, B01-B39/Q40, Q41, destructive appendices | Deferred to extended qualification | None | exhaustive applications, bug corpus, endurance, recovery | Out-of-scope ledger | They add cost and risk without being necessary for the harness sufficiency claim. |

No runtime re-decomposition is allowed. A discovered in-scope gap returns to its assigned large step; new unrelated work goes to the out-of-scope ledger.

## 4. Coverage map

| ID | Owning gate | Planned proof and evidence |
|---|---|---|
| C1 | Preflight | Candidate-base record and clean Git identity. |
| C2 | Preflight, C4 | Protected-state inventory before and after execution. |
| C3 | Preflight | New candidate worktree/branch record. |
| C4 | Preflight, S2 | Clean MCP worktree record plus dirty-checkout preservation hash/status. |
| C5 | Preflight | Resource-manifest verification report for 47 files. |
| C6 | Preflight | No-mutation log and authorization boundary. |
| C7 | Preflight, C1 | Version/hash manifest locked at Checkpoint A. |
| C8 | Preflight, S2, C3 | Root-isolation tests and physical lane manifests. |
| C9 | S1 | Legacy schema-less parser characterization test. |
| C10 | S1 | Policy composition positive/negative tests. |
| C11 | S1 | Legacy output and event-path tests. |
| C12 | S1 | Accepted field-shape fixture matrix. |
| C13 | S1, S3 | Unchanged coding V1 regression IDs and disposable integration. |
| C14 | S1 | Cross-shaped input/result rejection tests. |
| C15 | S1, S3 | Retained fixture/example replay. |
| C16 | S1, S3 | Compatibility audit and zero-migration docs. |
| C17 | S1 | Diff review plus behavior-equivalence tests for any shared helper. |
| C18 | S1, S3, C2 | Dual-route unit and disposable integration gates. |
| C19 | S1 | Exact process-tree lifecycle tests. |
| C20 | S1 | MCP launcher/server/provider correlation tests. |
| C21 | S1 | Exact relay binding tests. |
| C22 | S1 | Invalid/expired/changed relay negative tests. |
| C23 | S1, C2, C3 | Synthetic and physical same-thread/path resume evidence. |
| C24 | S1, S3, C3 | Event emission and exact acknowledgement evidence. |
| C25 | S1 | Historical declaration versus operational lease tests. |
| C26 | S1 | Claim owner and stale handling tests. |
| C27 | S1, S2, C3 | Isolated concurrency simulation and four-board evidence. |
| C28 | S1, C2, C3 | Contention simulation and physical serialization evidence. |
| C29 | S1, C2, C3 | Exit/reap cleanup tests and shutdown audit. |
| C30 | S1 | Unknown/partial/corrupt lifecycle negative matrix. |
| C31 | S2, C3 | Broker-only physical-call tests, no-endpoint-inheritance audit, four-artifact rejection matrix, retained multi-call same-Server-Run proof, sequence/transition rejection, and MCP ledger. |
| C32 | Preflight, S2, C3, C4 | Immutable server pin plus any C3 `AUTHORIZED_SERVER_LIMITATION` attribution/substitute evidence; no server-repair or repin history is permitted. |
| C33 | S2, C3 | Per-controller MCP/state/artifact/log manifests; session request/open/signed-close/closed-or-aborted lifecycle; exact exit/reap/claim release; and O/worker process-environment/handle absence proof. |
| C34 | Preflight, C3 | Live discovery and four profile bindings. |
| C35 | Preflight, C3 | Probe-to-live-route mapping evidence. |
| C36 | S2, C3 | Fixture contract test and STM behavior. |
| C37 | Preflight, S2 | Authoritative mapping resolution record or dependent-test exclusion. |
| C38 | Preflight, S2 | Manifest/lock validation evidence. |
| C39 | S2, C3 | Scope/policy/governing hashes; exact call/identity/duration binding through immutable dispatch admission and result; monotonic deadline/cancel/cleanup proof; O key/signature; mismatch/expiry tests; no invalid success. |
| C40 | S2, C3 | Denied-operation policy and absence audit. |
| C41 | S2, C3 | Radio plan and bounded transmission evidence. |
| C42 | S2, C3 | Oracle inventory and no-operator-touch audit. |
| C43 | C3 | Attempt-number allocation, fresh target Git identity, C1-locked five-file seed inventory/hash proof, and restart reconstruction provenance if applicable. |
| C44 | C3 P1 | Target tests, source review, and firmware artifact hashes. |
| C45 | C3 P1 | STM UART/I2C/debug/reset/recovery evidence. |
| C46 | C3 P2 | BLE GATT protocol evidence. |
| C47 | C3 P2 | LoRa protocol and telemetry evidence. |
| C48 | C3 P3 | One `F.C3.P1` assignment plus concurrent `P3.STM`/`P3.NRF` non-agent lane records proving only `C3-HARNESS` created/started/stopped/reaped the groups, and a four-board run report. |
| C49 | S2, C3 | Build and MCP operation artifact chain. |
| C50 | S2, C3 | Behavioral pass assertions in target results. |
| C51 | C3 P3 | Pre-injection target-only defect declaration, expected behavioral failure, before/after source commits, normal failure evidence, repair, and selective rerun ledger. |
| C52 | C3 P3 | Same-thread/path checkpoint-resume record. |
| C53 | C3 P3 | Independence/contention evidence with exact controller/process/claim/event/MCP ownership and no second active target agent. |
| C54 | C3 P4 | Candidate shutdown, helper observation-close from primary/approved fallback evidence, closed in-domain attempt inventory/result with separately verified external references, independent C4 enumeration, and separately closed ROOT topology. |
| C55 | C3 | `F.C3.O` launch identity, its assignment submissions, and `C3-HARNESS` records proving the harness--not `F.C3.O`--launched each target worker. |
| C56 | C3, C4 | Topology transcript proving `ROOT-IM` did not assign target work. |
| C57 | C3 | ROOT-launched deterministic helper, exact launch identity, ready/heartbeat/cursor/finding/terminal evidence, fact-by-fact fallback validation, and `WATCHER_OBSERVATION_CLOSE.json`; optional W is supplemental. |
| C58 | C3 | Three exact immediate-stop drills plus O/helper loss and cleanup drills proving safe containment, support-vs-product classification, preserved credit, and fresh P0 only for incomplete physical work. |
| C59 | S2, C3 | Failure-classification tests and ledgers: target-local repair, watcher/harness abort, or immutable pinned-server limitation with strongest-available substitute and explicit non-certification. |
| C60 | Preflight, all lanes | Headless launch records with exact models/efforts/tiers and exact launch owner, including negative proof that `F.C3.O` never directly launched a target worker. |
| C61 | All steps, C3, C4 | Lane manifests and topology audit. |
| C62 | S1-S3 | Two-loop checkpoint evidence per large step. |
| C63 | All test gates | C1-frozen implementation registry, per-attempt manifest-covered registry, immutable prior-evidence credits, and selective-rerun ledger. |
| C64 | S3, Safeguard | Tested candidate-root safeguard launcher, pre-admission result, unique logical run ID, component checkpoint/resume ledger, and terminal full-gate result on the exact C1 lock. |
| C65 | S2, C3 | Core catalog adaptation matrix and practical evidence. |
| C66 | S2, Safeguard | Extended qualification/out-of-scope ledger. |
| C67 | All gates | Evidence index with revision and identity bindings. |
| C68 | C0 | Fresh final-review report. |
| C69 | C4 | Nested criteria/topology/evidence/protected-state audits. |
| C70 | Safeguard | Promotion and fresh inactive runtime records. |
| C71 | S3, C2 | Docs tests and new-operator disposable run. |
| C72 | S1-S3, C0, C4 | Scope ledger and complexity review. |
| C73 | S1, S3, C0, C2, C4, Safeguard | Baseline-to-candidate original unit-test manifest, shared-code dependency map, cross-route isolation tests, green affected results, and no-weakening audit. |
| C74 | S4, S5, C0, C2 | Task-card/acceptance binding plus resume-admission units and a fake-worker smoke proving accepted threads reject unrelated work while valid same-task continuations remain. |
| C75 | S5, C0, C2, C4 | Terminal-lane archive manifest, active-scan absence, retained evidence/revision hashes, safe Git worktree close proof, disposable-cache cleanup, and recovery behavior. |
| C76 | S5, C0, C2 | No-worktree static-review invocation evidence with exact source identity, separate result root, no source/peer contamination, and a source-local execution control that still allocates isolation. |
| C77 | S5, C0, C2, Safeguard | Real multi-process event-append regression proving lock wait, complete flushed JSONL records, and no malformed, interleaved, missing, or duplicate event. |

## 5. Serial step flow

Execution advances through large steps only; modules and small changes do not receive their own cycle. Preflight must pass before S1. S1 must reach Checkpoint A before S2, and S2 must reach Checkpoint A before S3. S3 unlocks mandatory supplemental S4; accepted S4 unlocks mandatory supplemental S5; accepted S5 then unlocks C0-C2. C0 reviews, C1 locks the exact inputs, and C2 proves that lock without changing it. C3 practical acceptance starts only from the latest accepted S5 tip, green C1 lock, and green C2 evidence. C4 and the safeguard follow practical success.

### End-to-end workflow layout

This is the authoritative control-flow overview. The per-step tables below remain authoritative for
the exact lane counts, bases, worktrees/run roots, joins, test IDs, and evidence. `-->` is a serial
unlock, `||` is only a preplanned independent fan-out, and `RETURN` reruns only the dependency-
invalidated work. A finding is never a transition by itself: the named orchestrator must first accept
it under the breakage-or-worth and problem-versus-fix-cost rule.

```text
IMPLEMENTATION / HARNESS-CREATION CONTROL PLANE

ROOT-IM (this host session; integration and implementation decisions)
  |
  +--> Preflight
  |
   +--> S1 --> Checkpoint A --> S2 --> Checkpoint A --> S3 --> Checkpoint A
   |      |                      |                      |
   |      `-- each large step uses the fixed two-loop shape below --'
   |
   +--> S4 --> accepted S4 tip --> S5 --> accepted joined tip --> shortest affected smoke
         | S4/S5 red: RETURN owning lane before C0
         ` green: (C0 complete fresh read-only sweep || remaining focused execution) --> join
                    | accepted complete finding/test batch: RETURN to owning S-step
                    |   --> repair/adapt whole batch --> new joined tip/smoke --> fresh C0 join
                    ` green
                        --> C1 exact-input lock
                        --> C2 unchanged-lock synthetic/disposable verification
                               | execution-only failure: correct/rerun affected IDs on same C1
                               | locked-input repair: RETURN to owning S-step --> fresh C0/C1/C2
                                ` green: unlock C3

FIXED S1/S2/S3 LARGE-STEP SHAPE (creation process; ROOT-IM coordinates it)

P: one serial product/coder lane
  --> (R1 || R2 where that step preplans both; otherwise R1)
  --> ROOT-IM review join and merit triage
  --> (A1 || A2 where preplanned; otherwise A1) for accepted test work
  --> ROOT-IM ordered integration join
  --> (D1 || D2 where preplanned; otherwise D1) for independent execution
  --> ROOT-IM result join and merit triage
         | accepted product/test defect: RETURN to the owning lane; rerun affected IDs
          ` green: advance Loop 1 --> Loop 2 --> Checkpoint A

S4/S5 SUPPLEMENTAL FEATURE SHAPE (two bounded serial stages after S3/S30; ROOT-IM coordinates them)

ROOT S4 feature specification/implementation plan
  --> D1 one isolated implementation doer
  --> R1 independent focused review
  --> D2 focused unit/disposable smoke execution
  --> ROOT-IM complete-result triage --> accepted S4 tip
  --> ROOT S5 feature specification/implementation plan
  --> P1 one serial product coder
  --> (R1 focused review || D1 focused unit/disposable practical execution)
  --> ROOT-IM complete-result triage --> accepted S5 tip --> fresh C0/C1/C2

FINAL TEST CONTROL PLANE (separate orchestration; candidate is the system under test)

ROOT-IM/F.C3.M
  +--> launch and supervise F.C3.O (fresh Sol-high-Fast orchestrator subagent)
  +--> directly launch deterministic observer helper (required, non-agent)
  +--> optionally launch F.C3.W (fresh Terra-medium-Fast supplemental review)
  `-- never assign or orchestrate target-project work

F.C3.O decides target work
  --> submits one assignment at a time to C3-HARNESS
  --> C3-HARNESS alone launches/owns one of A1, C1, P1, or R1
  --> target result/events return through C3-HARNESS to F.C3.O
  --> next sprint or targeted target-local correction

deterministic helper observes independently
  --> ordinary findings: pool through gate --> one ROOT triage/bounded batch
  --> exact safety/containment/evidence-corruption condition: ROOT contains topology
      --> classify product vs support cause without discarding unaffected credit

F.C3.O classification routes
  | target/operator/test/application mistake with no locked-input change:
  |   correct inside the target project and rerun only affected C3 work
  | pinned MCP server defect/incompatibility: AUTHORIZED_SERVER_LIMITATION
  |   --> F.C3.O exact attribution --> strongest safe partial/unit substitute via C3-HARNESS
  |   --> retain physical non-certification --> continue affected sprint
  ` O/helper loss or immutable-evidence closure failure: use approved fallback evidence or preserve
      attempt --> fresh C3 only for incomplete work,
      unless a locked input changed, in which case use the owning-step relock route

C3 green --> C4 independent audit fan-out --> ROOT-IM join and merit triage
  | accepted evidence-only gap: correct C4 annotation --> repeat C4
  | accepted target-local gap: fresh C3 from earliest invalidated sprint --> C4
  | accepted locked-input gap: RETURN owning S-step --> C0 --> C1 --> C2 --> C3 --> C4
  ` green --> one accumulated Safeguard --> reconciliation/promotion --> completion
```

The upper two blocks are the multi-agent process used to create and verify the harness. The final-test
block is deliberately different: `F.C3.O`, not `ROOT-IM`, orchestrates the target project, while the
candidate `C3-HARNESS`, not either orchestrator directly, launches and owns every target worker.

### Preflight gates (no full cycle)

Preflight followed `EXECUTION_READINESS_2.md` and the roadmap in order. It recorded the current root
as `ROOT-IM` without applying a child model gate; rechecks protected revisions, hashes, toolchain files, and reserved
path/branch/promotion-ref absence; creates the candidate and clean MCP worktrees only at their reserved runtime
coordinates; replaces the absent historical NCS cache path with lane-local cache state; proves all
exact headless model/tier launches; supplies the clean server through explicit per-lane-controller MCP
configuration; performs read-only identity discovery; records authority/exclusions; and establishes
fresh manager state. Historical manifest source paths are recorded as unavailable provenance, never
as a failed runtime dependency or a falsely verified live source copy.

The explicit server declaration uses `uv run --project
plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate --locked
pyocd-debug-mcp` after resolving that project argument to its absolute path, plus lane-local
`BYO_MCP_ARTIFACT_ROOT`, a lane-assigned working directory, MCP-only stdout, and separately captured
stderr. It cannot name the dirty input checkout.
The launcher rejects unreviewed `.env` files and ambient `PYOCD_PROBE_UID`/`PYOCD_TARGET` values;
inventory clears both, and a board-owning lane receives only its exact assigned UID and reviewed
target/profile.

RF remains unadmitted until authoritative fixture/setup evidence confirms both module variants,
antennas, supply/current constraints, configured 915 MHz operation, transmit power, bandwidth,
bounded duty cycle, and applicable operating constraints. A requested frequency or user permission
alone is not technical/regulatory admission evidence.

Preflight also recorded the candidate-root gate protocol and focused commands. S3 materialized and
tested the exact safeguard launcher. The outer `.codex/scripts/verify.py` is bound to
`stable-general-harness-runner` and cannot prove a different worktree. These gates passed before S1.
On resume, rerun only mutable checks whose dependency changed; do not repeat the full preflight or
credit the outer gate for candidate code. No state-changing hardware operation is part of preflight.

**Next-run external-support readiness gate (no product cycle):** before S4 or any C3 allocation,
ROOT validates the prepared outer support source `.codex/scripts/c3_outer_support.py`, reusable
observer `.codex/scripts/c3_watcher_helper.py`, their unit tests, and
`.codex/scripts/run_c3_outer_support_smoke.py`. Required evidence is: focused tests green; the
eight-scenario host-only smoke green; one independent Luna-high practical execution green and
semantically accepted by ROOT; full repository verification green; exact source/test hashes; and
zero residual helper/test processes. This gate changes no candidate, stable runner, MCP fixture, or
hardware input and therefore cannot invalidate product credit. A support-test failure returns only to
this support layer, in one bounded correction batch, and the affected support checks rerun once.

Preparation result (2026-08-06): **PASS**. Focused suite: 16/16; host-only smoke: 8/8;
independent Luna-high verdict: PASS with empty findings after one sandbox-only no-test dispatch was
corrected; full repository `verify.py --full`: `VERIFY: PASS`; related residual processes: zero.
Exact hashes are retained in the preparation acceptance record named in `HANDOFF.md`.

### Global lane topology

For each original S1-S3 step, the product lane and bundled modules complete before independent
review. Those already-completed step topologies remain historical. A reopened repair groups all
accepted findings from the complete review result into one serial batch and does not review,
checkpoint, or reconcile an intermediate commit. The fixed original flow is:

`product lane and bundled modules -> review lane(s) -> triage -> author lane(s) -> integration -> test lane(s) -> triage -> failure route or Checkpoint A`

`ROOT-IM` owns implementation integration at every join. Production changes never fan out. Review/test-writing/test-execution pools may contain one or two lanes as preplanned below; the runtime never re-partitions them.

Every reviewer, test-writer, and test-executor lane created by this plan enables the candidate's
optional backward-compatible finding gate. A terminal result is valid only with a lane/invocation/
role/commit-bound `orchestrator-review-findings/v1` artifact: PASS has zero findings; FAIL has one or
more; BLOCKED may have zero only for a non-gap external condition. Every submitted finding is
exactly `CODEBASE_BREAKING`, `FUNCTIONALITY_BREAKING`, or `WORTH_FIXING` and contains reproducible
evidence, affected requirement/behavior, observed/expected behavior, impact/no-fix consequence, the
smallest sufficient fix, complexity/regression/verification costs, alternatives, and a reasoned
problem-outweighs-fix conclusion. The code validates structure and identity. `ROOT-IM` or `F.C3.O`
independently decides truth and tradeoff; unsupported, style-only, speculative, cleanup, or merely
nicer suggestions are rejected and cause no edit, reset, relock, or retest.

Every reviewer completes its full assigned affected-surface and critical-control-path sweep after a
valid finding unless an external blocker prevents continued inspection. It returns one complete
exact-tip finding set and may not intentionally stop at the first defect. A blocking finding must
show a supported or credibly reachable deployed trigger and a concrete negative consequence for
correctness, safety, security, reliability, recovery, required evidence integrity, or required
user-visible behavior. Realistically triggerable latent authorization, identity, cleanup, and
fail-closed defects qualify. Cosmetic, unreachable, behavior-neutral, purely theoretical, and
speculative-hardening suggestions do not.

### Included modules and serial tasks

| Step | Bundled serial product work | Unblocks |
|---|---|---|
| Preflight | provenance, clean roots, hashes, authority, model launch, read-only discovery | S1 |
| S1 | firmware compatibility, lifecycle, relays, claims, cleanup, dual-route tests | S2 |
| S2 | MCP substrate, fixture manifest, acceptance charter, evidence schemas, simulations | S3 |
| S3 | dual-path docs/config, operator commands, integration, release templates | S4 |
| S4 | supplemental task-card semantic-acceptance and one report-only-retry features | S5 |
| S5 | terminal task/lane lifecycle, no-worktree static review, locked shared-event append | C0-C2 |
| C0-C2 | fresh review, C1 final lock, C2 proof of unchanged locked inputs | C3 |
| C3 | separately orchestrated physical target project | C4 |
| C4 | nested static audits and any targeted repair | Safeguard |
| Safeguard | single accumulated suite, reconciliation, promotion | Completion |

### Failure route

Only gaps admitted by the structured finding gate and independently accepted on problem-versus-fix
merit return to Coder-main or a test-author lane. The accepted repair is the smallest sufficient
change; if its complexity, regression risk, or verification burden outweighs the demonstrated
production consequence, the finding is rejected or deferred. `ROOT-IM` triages the complete
finding/test result and routes every accepted item as one bounded repair batch. No product review,
C0, aggregate dependency-map/registry reconciliation, or C1 lock is created for an intermediate
batch revision. Execution/environment mistakes return to the failing
doer lane. Mistakes by `ROOT-IM`, `F.C3.O`, or a target worker--bad assignments, prompts, ordering,
commands/config paths, target edits, invalid calls, triage, or result envelopes--are expected
recoverable workload and return to their owner for targeted correction or same-thread resume. They
do not by themselves emit `ABORT_REQUIRED`, reopen green implementation steps, invalidate C1, or
erase unrelated green credits. A target-side MCP call or target-repository-configuration defect
remains C3 target work only when it changes no C1-locked input. The C1 lock covers operative
goal/planning hashes, the candidate, server pin/configuration, acceptance-kit and lane/MCP launch
templates, fixture bindings, the five-file target seed, test/evidence contracts, authorization, and
other implementation inputs; it excludes target source/configuration created and versioned inside
the disposable target repository. A required locked-input change leaves the target-local route.
A reproduced defect/incompatibility in the immutable pinned MCP server uses
`AUTHORIZED_SERVER_LIMITATION`; O retains exact attribution and assigns the strongest safe partial
MCP or pinned-component/candidate-boundary unit substitute through `C3-HARNESS`. It does not end the
attempt merely to repair or repin the server, and it never converts the unexecuted physical portion
into a pass. Harness/watcher defects during C3 trigger `ABORT_REQUIRED` and return to the owning
implementation step. An orchestrator mistake
that prevents honest closure of immutable attempt evidence rolls only to a fresh attempt namespace
unless a locked input changed; this is not a candidate reset. Every route reruns targeted affected
stable IDs only, except P0 always reruns for every fresh C3 runtime.

Administrative result-envelope, metadata, evidence-field, command, and path corrections that do
not change operative product or test meaning resume in the same lane and do not invalidate product
review or green tests. A strict test-only fast lane applies only to synthetic fixture/setup or test
metadata with known failed IDs after a deterministic checklist proves no production/policy/contract/
locked-configuration change and no oracle, assertion-strength, expected-outcome, stable-ID, or
coverage-obligation change. The same test-author continuation corrects it and reruns exactly those
failed IDs once before any unrelated smoke or work; it creates no C0, ordinary review, registry/
dependency reconciliation, or aggregate join. Failure or any unproved condition leaves the fast lane
for the material route. Raw lane evidence is always preserved, while dependency mapping, registry
reconciliation, and aggregate join evidence are finalized once for the accepted production batch tip.

### Supplemental feature stage S4: task-card acceptance and report-only recovery

**Placement and non-bypass rule.** This is a mandatory material candidate-feature stage after the
current S30 joined-tip archive/admission and before the next fresh C0/C1/C2 cycle. It exists before
C3 because the current run has not begun a new acceptable C3 attempt. `ROOT-IM` must not classify the
pending S30 C0/C1/C2 route as final, allocate a C3 rehearsal, create an `attempt-NNNN`, launch O/helper,
start MCP, or claim hardware until S4 and S5 are accepted and a new C0/C1/C2 pair has passed on the exact S5
tip. If a future run reaches or closes C3 before this stage is admitted, S4 and then S5 run
immediately after that C3 attempt and before any successor C3/C4/safeguard work; neither changes an
immutable closed attempt.

**ROOT specification and plan.** Before dispatching a child, `ROOT-IM` writes one bounded
`S4_ROOT_FEATURE_PLAN.md` that binds the exact candidate base, changed modules, test scope, and
acceptance evidence. For feature 1 it must treat top-level `task-card-spec.md` as the authoritative
product contract: task-card context/entrypoints/budget, durable
`LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE`, and hash-bound
`ORCHESTRATOR_ACCEPTANCE.json` with `ACCEPTED`, `ACCEPT-WITHIN-TOLERANCE`, `CONTINUE`, or
`INCOMPLETE`. The plan must state that a worker's self-reported `RESULT.json` is only structurally
valid until the orchestrator's semantic verdict. For feature 2 it specifies the one same-thread,
report-only retry after a malformed or missing terminal report/result: inject the exact validator
failure; permit only existing evidence; prohibit code/test changes and test reruns; validate once;
then classify incomplete/reject or narrowly rerun the genuinely affected check. No separate broad
specification is required for feature 2.

**Implementation and review lanes.** S4 is intentionally small and serial:

1. `ROOT-IM` writes and locks the S4 feature plan, including the explicit boundary that the frozen
   stable runner remains unchanged; only the dogfooded candidate may change.
2. `S4.D1` is one isolated Luna-high-Fast implementation doer. This is the narrow exception to the
   ordinary doer source-edit rule: it may edit only the candidate's generic coding-invocation/lane
   controller/result-validation modules and their directly affected tests. It implements both
   features in one coherent candidate change and writes a complete result.
3. `S4.R1` is one independent Terra-medium-Fast reviewer. It reads the S4 plan, `task-card-spec.md`,
   candidate diff, and focused evidence; it runs the focused read-only task-card/result contract unit
   IDs, then verifies that the implementation does not turn a worker result into final acceptance,
   that tolerance cannot override strict criteria, and that retry is exactly once/same-thread/report-
   only. It returns one complete finding set and no source edit.
4. `S4.D2` is one disjoint Luna-high-Fast test doer. It runs focused unit tests and one disposable
   smoke using a fake Codex worker. The smoke proves: a structurally valid result emits the exact
   acceptance-pending event/instruction and does not release dependent work before a bound verdict;
   `CONTINUE` resumes the same recorded thread with exact gaps; and one malformed terminal report
   receives one report-only resume, then either validates or stops without a loop/test rerun.
5. `ROOT-IM` triages the complete reviewer/test results as one bounded batch. Only accepted
   production findings return to `S4.D1`; report-only/test-environment corrections remain in their
   owning lane under the existing pooled fast-lane rule. On acceptance, ROOT records the final S4 tip,
   dependency map, passed IDs, feature-plan hash, review result, and smoke/unit evidence.

**S4 acceptance criteria.** Both features must have focused unit coverage and the one disposable
smoke above; all affected original general-harness tests stay green; task-card JSON/card/event/result
identity and hashes are exact; no automatic semantic acceptance, dependent dispatch, test rerun, or
unbounded retry occurs; and no MCP, watcher, hardware, or pinned-server process is launched. An
accepted S4 tip is a material candidate change and unlocks S5 only. It must not trigger C0, C1, C2,
rehearsal, or C3 until S5 is also accepted.

### Supplemental feature stage S5: efficient lane lifecycle and event integrity

**Placement and non-bypass rule.** S5 starts only from the accepted S4 tip and completes before the
next fresh C0/C1/C2 cycle. It is not retroactive work inside S1-S4 and does not invalidate unchanged
S30/S4 evidence. `ROOT-IM` must not launch C0, create C1, run C2/rehearsal, allocate C3, launch MCP,
or claim hardware until S5 is accepted. The frozen stable runner remains unchanged; only the
dogfooded candidate may change.

**ROOT specification and plan.** Before dispatch, `ROOT-IM` writes
`S5_ROOT_FEATURE_PLAN.md` binding the exact accepted S4 base, C74-C77, candidate modules, focused
test IDs, protected historical paths, and acceptance evidence. The plan chooses the smallest
implementation that provides:

1. logical task/thread admission: same-task `CONTINUE`, the one report-only recovery, and the strict
   fast lane remain resumable before acceptance; `ACCEPTED` or `ACCEPT-WITHIN-TOLERANCE` rejects
   unrelated reuse and requires a new bounded task card/thread;
2. terminal-lane retirement: after evidence and revision preservation, accepted lanes leave active
   discovery, clean unused linked worktrees close through verified Git operations, required
   transcripts/results remain archive-only, and disposable caches are removed;
3. `immutable-read-only-view` source allocation: static read-only work binds an exact source commit
   and separate writable result root without a linked worktree, while mutation or source-local test
   execution retains isolated writable source state; and
4. one cross-process lock per shared event-log path: a writer waits, appends and flushes one complete
   record, then releases; do not add per-controller logs or a merge subsystem.

**Implementation, review, and test lanes.** S5 uses one serial writer and one final join:

1. `S5.P1` is one Terra-medium-Fast product coder. It owns only the candidate task-card/resume
   admission, lane discovery/retirement, Git/source allocation, event append, and directly affected
   tests/docs. It implements all four features as one coherent change.
2. After the P1 tip is frozen, `S5.R1` is one independent Terra-medium-Fast reviewer and `S5.D1` is
   one disjoint Luna-high-Fast test doer. They may overlap because both are read-only and use separate
   result roots. R1 audits correctness, compatibility, Git/path/process safety, evidence retention,
   and over-engineering. D1 runs the focused units and disposable practical described below.
3. `ROOT-IM` joins their exact-tip results once. Accepted product findings return together to S5.P1
   as one bounded batch; administrative/test-only failures remain in their owning lane. No
   intermediate S5 revision receives C0, C1, or aggregate reconciliation.

**S5 required proof.** Focused units plus one disposable practical must prove all of the following:

- valid same-task continuation routes still resume, but an accepted task rejects unrelated reuse and
  a new task/card/thread succeeds;
- evidence/revision hashes are durable before terminal retirement; active discovery no longer scans
  the retired lane; clean unused worktrees close safely; dirty, live, unretained, ambiguous, or
  unpreserved lanes remain untouched and recoverable;
- a static read-only reviewer inspects the exact source commit and writes only to its result root
  without creating a linked worktree or contaminating a peer, while a source-local test control still
  receives isolated writable source state; and
- at least two real processes contend on one event log, the later writer waits on the same lock, and
  every expected JSONL record is complete, parseable, unique, and present.

After S5 acceptance, ROOT runs one audited retirement pass over eligible terminal V2 lanes only.
The 13 protected historical worktrees, immutable acceptance evidence, dirty/ambiguous lanes, live
paths, and unretained revisions are out of scope. The accepted S5 tip then receives the shortest
affected smoke and the one fresh C0/C1/C2 route.

### Unlocks

A step unlocks the next only when both loops are green, joins are complete, `PARALLEL_CHECKPOINT.md` is reconciled, the passed registry is updated, exact managed processes are exited, and `ROOT-IM` has acknowledged all top-level actionable implementation events. During C3, `F.C3.O` processes target-project events through `C3-HARNESS`; `ROOT-IM` does not take over that event stream.

## 6. Per-step execution spec

These are fixed conceptual roles and lane counts. The Current Portable Harness binding is mandatory in every step: start with `scan --no-write`; operate from isolated worktrees/run roots; observe through `watch --until-actionable`; clear through exact `ack --event-id`; require current-tip `RESULT.json`; record the passed registry; and leave no unowned process or claim. Each pool is the smallest useful pool for the planned independent slices.

### Step S1: Legacy firmware lifecycle and compatibility

- Step class: large step
- Coherent feature or deliverable: one backward-compatible firmware invocation/lifecycle boundary beside unchanged coding V1.
- Included modules: firmware invocation parsing, policy binding, result routing, process/MCP reconciliation, relay binding, resource claims, events, resume, cleanup, protected original general-harness unit tests, and dual-route tests.
- Included serial tasks: characterize accepted fixtures; implement minimal corrections; integrate review findings; merge test branches; repair production or test defects; checkpoint the locked result.
- Why grouped by coherence: every module consumes the same lane identity and determines whether legacy firmware work is authorized, live, complete, or releasable.
- Why full QA is justified: a compatibility error can silently misroute work or release real hardware, so parser, identity, relay, and cleanup behavior require combined review and regression coverage.
- Granularity boundary: no individual parser, event, relay, or claim edit receives a separate cycle; unrelated MCP feature work is excluded.
- Smallest useful pool: one coder; two reviewers split public compatibility from lifecycle safety; two test writers and two doers split contract tests from reconciliation/integration tests.

| Role pool | Size | Independent ownership |
|---|---:|---|
| Review | 2 | R1 public invocation/result/docs compatibility; R2 process/MCP/relay/claim/cleanup safety. |
| Test/document authoring | 2 | A1 schema/policy/dual-route and original coding-isolation tests; A2 lifecycle/relay/resource/event tests plus shared-code dependency mapping. |
| Test execution | 2 | D1 protected original-unit/contract shard; D2 reconciliation/process/disposable integration shard. |

**Explicit lane topology**

`S1.P -> S1.SR -> (S1.R1 || S1.R2) -> S1.JR -> S1.P -> S1.CA`

`S1.CA -> S1.SA -> (S1.A1 || S1.A2) -> S1.JA -> S1.ST -> (S1.D1 || S1.D2) -> S1.JT -> S1.P`

| Lane ID | Agent role | Starts after / base | Branch / worktree or run root | Join / merge target and order | Failure route |
|---|---|---|---|---|---|
| `S1.P` | Coder-main | Preflight / exact `4699d27` candidate | dedicated S1 product worktree | owns candidate; receives JR then JA changes in `ROOT-IM` order | accepted product gap returns here serially |
| `S1.R1` | Reviewer-main | S1.P integration revision | read-only review root | report joins at S1.JR before R2-independent triage | finding to `ROOT-IM`; no edits |
| `S1.R2` | Reviewer-main | same S1.P revision | separate read-only review root | report joins at S1.JR | finding to `ROOT-IM`; no edits |
| `S1.A1` | Reviewer-main test writer | accepted S1.JR revision | isolated schema/compatibility test worktree | first test merge at S1.JA | test defect returns to A1 |
| `S1.A2` | Reviewer-main test writer | same accepted S1.JR revision | isolated lifecycle test worktree | second test merge at S1.JA after conflict audit | test defect returns to A2 |
| `S1.D1` | Doer-main | merged S1.JA revision | isolated unit test run root | results join at S1.JT | environment/test failure to D1; product failure to S1.P |
| `S1.D2` | Doer-main | same merged revision | isolated integration test run root | results join at S1.JT | environment/test failure to D2; product failure to S1.P |

**Loop 1**

1. S1.P implements the complete bundle and returns a current-tip result.
2. S1.SR fans out R1/R2; S1.JR performs merge-then-triage of reports, not code.
3. S1.P fixes accepted findings; S1.CA records the accepted production revision.
4. S1.SA fans out A1/A2. `ROOT-IM` merges A1 then A2 at S1.JA and resolves ownership conflicts before testing.
5. S1.ST fans out D1/D2. S1.JT classifies failures and routes only affected IDs.
6. Repeat targeted fix/test work until the Loop 1 pass criteria are met.

**Loop 2**

1. Begin immediately from Loop 1's accepted revision; lane roles remain fixed conceptual assignments.
2. There is no ordinary static review. R1 or R2 revives only if post-review production code changed in its owned risk area.
3. A1/A2 add or correct tests only for surfaced gaps. D1/D2 rerun failed or dependency-invalidated stable IDs; green unrelated IDs remain credited.
4. Pass criteria: C9-C30 and C73 are green; every dependency-invalidated original general-harness unit test and every new cross-route isolation test passes; no original test was unjustifiably deleted, skipped, marked expected-failure, weakened, or left unmapped; no hardware mutation occurred; all exact test processes exited; no actionable event or claim remains.
5. Checkpoint A records S1 revision, test-id scheme, passed registry entries, reviewer decisions, and the S2 unlock.

### Step S2: MCP-backed acceptance kit and test medium

- Step class: large step
- Coherent feature or deliverable: one reproducible, safety-bound kit that a fresh acceptance orchestrator can use to create and observe the four-board project.
- Included modules: server pin/worktree, resource hashes, fixture profiles, MCP launch isolation, plan/permission policy, user-derived delegated/call authorization schemas, target charter, exact five-file seed manifest, protocol specs, evidence/result schemas, opt-in structured finding-admissibility gate, catalog adaptation, synthetic MCP, and dry-run enforcement.
- Included serial tasks: create manifests and schemas; implement kit tooling; keep the pinned server
  immutable; implement exact server-limitation attribution and strongest-available substitution;
  integrate test branches; validate materialization and failure classification.
- Why grouped by coherence: provenance, MCP configuration, fixture ownership, target instructions, and evidence must describe the same exact run or physical results are untrustworthy.
- Why full QA is justified: the kit crosses process, safety, hardware-routing, and retained-evidence boundaries even before state-changing hardware work begins.
- Granularity boundary: no datasheet, board profile, schema, or catalog case gets an individual cycle; exhaustive server qualification remains outside this release.
- Smallest useful pool: one coder; two reviewers split safety/provenance from target/evidence sufficiency; two test writers and two doers split host/MCP contracts from target/simulation contracts.

| Role pool | Size | Independent ownership |
|---|---:|---|
| Review | 2 | R1 server/fixture/safety/provenance; R2 target charter/evidence/sufficiency/over-engineering. |
| Test/document authoring | 2 | A1 host/MCP/isolation negative tests; A2 target-materialization/evidence/selective-rerun tests. |
| Test execution | 2 | D1 host/schema/MCP simulation shard; D2 disposable target/dry-run/failure-classification shard. |

**Explicit lane topology**

`S2.P -> S2.SR -> (S2.R1 || S2.R2) -> S2.JR -> S2.P -> S2.CA`

`S2.CA -> S2.SA -> (S2.A1 || S2.A2) -> S2.JA -> S2.ST -> (S2.D1 || S2.D2) -> S2.JT -> S2.P`

| Lane ID | Agent role | Starts after / base | Branch / worktree or run root | Join / merge target and order | Failure route |
|---|---|---|---|---|---|
| `S2.P` | Coder-main | S1 Checkpoint A | dedicated S2 product worktree; clean pinned MCP worktree is read-only evidence | owns candidate acceptance-kit work only | accepted kit product gap returns here; server source never does |
| `S2.R1` | Reviewer-main | S2.P integration revision | read-only safety/provenance root | report joins at S2.JR | finding to `ROOT-IM`; no mutation |
| `S2.R2` | Reviewer-main | same revision | separate read-only target/evidence root | report joins at S2.JR | finding to `ROOT-IM`; no mutation |
| `S2.A1` | Reviewer-main test writer | accepted S2.JR revision | isolated host/MCP test worktree | first merge at S2.JA | test defect returns to A1 |
| `S2.A2` | Reviewer-main test writer | same accepted revision | isolated target/evidence test worktree | second merge at S2.JA | test defect returns to A2 |
| `S2.D1` | Doer-main | merged S2.JA revision | isolated synthetic MCP run root | results join at S2.JT | execution error to D1; product error to S2.P |
| `S2.D2` | Doer-main | same merged revision | isolated disposable target run root | results join at S2.JT | execution error to D2; product error to S2.P |

**Loop 1**

1. S2.P implements the kit without operating hardware beyond already-authorized read-only discovery.
   Its current bounded repair adds delegated-scope/method-policy enforcement and a production-
   executable retained Server Run: one session request/open, one exact MCP process and claim across
   consecutive predecessor-bound separately authorized calls, policy-defined transitions, signed O
   normal close, and fail-closed abort/drain/reap. Its normative input is
   `evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json` at SHA-256
   `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`: exact closed method
   inventory, finite transition graph, guarded plan/action protocol, direct candidate-control-plan
   rule, delegated-scope/action/`scope_effect` binding, five-key final C1 authorization schema, and
   narrow limitation API. It does not edit or launch the pinned server. It replaces all target-seed
   `PINNED_SERVER_REPAIR` routes with `AUTHORIZED_SERVER_LIMITATION` and never treats a limitation
   substitute as physical PASS.
2. S2.SR fans out R1/R2 with the finding gate enabled; S2.JR validates their artifacts, rejects non-breaking or net-negative-complexity suggestions, and triages only admissible provenance/safety and target/evidence findings together.
3. Never edit or repin server source. If a server defect/incompatibility is reproduced, preserve its
   exact evidence and prove the limitation classifier/substitution machinery using the strongest
   available partial MCP or focused pinned-component/candidate-boundary unit proof.
4. S2.SA fans out A1/A2; merge in A1 then A2 order at S2.JA.
5. S2.ST fans out D1/D2 in isolated roots; S2.JT routes only affected failures.

**Loop 2**

1. Start from Loop 1's accepted kit and pin with the same fixed conceptual lanes.
2. There is no ordinary static review; revive R1/R2 only for post-review production changes within their owned risk.
3. Rerun only invalidated host, simulation, target-materialization, or dry-run IDs from the passed registry.
4. Pass criteria: C4-C8 and C31-C42 plus C49, C59, C65-C66 are evidenced; no direct physical bypass is possible; no unapproved mutation occurred; roots and processes are clean.
5. Checkpoint A locks server/fixture/toolchain hashes, acceptance charters, the five-file target seed and hashes, stable IDs, evidence schemas, and the S3 unlock.

### Step S3: Release integration and backward-compatible operator surface

- Step class: large step
- Coherent feature or deliverable: one operator-ready dual-path release surface and disposable integration proof.
- Included modules: quick-start, legacy/coding/dual examples, headless role configuration, runtime commands, event acknowledgement, resume, cleanup, integration tests, candidate-root safeguard launcher, and release-evidence templates.
- Included serial tasks: integrate docs/config/tooling and the candidate-root gate; run one focused review; add final docs/integration coverage; execute disposable operator flow; checkpoint the release candidate.
- Why grouped by coherence: documentation, examples, CLI/config behavior, and integration tests jointly define what operators can actually run.
- Why full QA is justified: stale instructions or examples would break backward compatibility even if internal unit tests were green.
- Granularity boundary: no individual document, example, or command gets a separate cycle; no new UI or framework is admitted.
- Smallest useful pool: one coder, one reviewer, one test writer, and one doer because the operator journey is a single sequential surface.

| Role pool | Size | Independent ownership |
|---|---:|---|
| Review | 1 | R1 whole operator surface, backward compatibility, and scope. |
| Test/document authoring | 1 | A1 docs assertions and disposable dual-path integration. |
| Test execution | 1 | D1 new-operator run plus affected docs/integration IDs. |

**Explicit lane topology**

`S3.P -> S3.R1 -> S3.JR -> S3.P -> S3.CA -> S3.A1 -> S3.JA -> S3.D1 -> S3.JT -> S3.P`

| Lane ID | Agent role | Starts after / base | Branch / worktree or run root | Join / merge target and order | Failure route |
|---|---|---|---|---|---|
| `S3.P` | Coder-main | S2 Checkpoint A | dedicated S3 product worktree | owns final product integration | accepted product/docs gap returns here |
| `S3.R1` | Reviewer-main | S3.P integration revision | read-only whole-surface review root | singleton direct handoff at S3.JR | finding to `ROOT-IM`; no edits |
| `S3.A1` | Reviewer-main test writer | accepted S3.JR revision | isolated docs/integration worktree | singleton direct handoff at S3.JA | test/docs defect returns to A1 |
| `S3.D1` | Doer-main | merged S3.JA revision | fresh disposable operator run root | singleton direct handoff at S3.JT | execution error to D1; product error to S3.P |

**Loop 1**

1. S3.P integrates the operator and release surface.
2. R1 reviews the complete journey; S3.JR triages its report and S3.P repairs accepted gaps.
3. S3.CA locks production for A1's docs/integration additions; S3.JA integrates them.
4. D1 performs the fresh disposable dual-path operator run and reports stable IDs to S3.JT.

**Loop 2**

1. Begin immediately from the Loop 1 accepted revision with the same fixed conceptual roles.
2. There is no ordinary static review; R1 revives only for a post-review product change.
3. A1 and D1 address and rerun only changed or failed IDs; all unrelated green registry entries remain credited.
4. Pass criteria: C13, C15-C18, C24, C43, C60-C63, C67, and C71-C73 are ready for final audit; the protected original-unit matrix remains green for every dependency invalidated by S3; the operator path is accurate; process/claim/event state is clean.
5. Checkpoint A locks the candidate and final/acceptance spec inputs, updates `PARALLEL_CHECKPOINT.md`, and unlocks C0.

## 7. Final phase

The final and acceptance lane topology is preplanned. C0 reviews, C1 locks, and C2 proves the unchanged locked inputs. C3 uses separate subagent `F.C3.O` to operate the candidate system under test. C4 is the ordinary post-lock static-review phase; only a C4 repair that invalidates C1 may explicitly re-enter C0. `ROOT-IM` supervises implementation; `F.C3.O` decides target work; `C3-HARNESS` exclusively launches and lifecycle-manages target workers.

### C0 - fresh final-reviewer

First finish all known production/test adaptation and freeze one joined candidate tip. Run the
shortest already-required dependency-invalidated smoke IDs; a failure returns to its owner before
C0. After smoke is green, launch exactly one fresh Final-reviewer, Terra-medium-Fast, read-only and
without prior step context, while the remaining focused Luna-high-Fast execution runs independently on
the same exact tip. The reviewer audits `GENERALIZATION_SPEC_2`, C1-C77, the complete candidate
diff, critical control paths, legacy compatibility, safety, MCP boundary, tests, docs, and
over-engineering. It explicitly compares the original successful general-harness unit-test manifest
with the candidate: shared-code dependency coverage, executed affected IDs, skips/expected failures,
deletions, and assertion strength.

The reviewer must finish that complete sweep after discovering a defect and return one complete
exact-tip finding set, not a first-finding result. It returns either `NO CANDIDATE GAP / READY` or
all evidence-linked admissible findings it can substantiate. Reviewer recommends; `ROOT-IM` decides
after both review and focused execution join. Accepted production findings route together as one
bounded serial batch to the owning step and invalidate only dependent tests; test authors adapt all
affected coverage before the next frozen tip. No C0 runs on intermediate repair revisions. After the
new smoke passes, a new fresh C0 and remaining focused execution may again overlap.

A strict test-only fast lane correction is limited to synthetic fixture/setup or test metadata, has
known failed IDs, and records a deterministic checklist proving no production, policy, contract,
locked configuration, test oracle, assertion strength, expected outcome, stable ID, or coverage
obligation changed. The same test-author continuation reruns exactly those IDs once before unrelated
work; it creates no C0, ordinary review, or reconciliation. Administrative corrections that change
no product or test meaning resume without a new product review or test rerun. A change to expected
product behavior, coverage obligations, an operative test/evidence contract, production, or policy
is material and uses the full route. Reconcile the final dependency map, registry, and aggregate
evidence once after the exact accepted production batch tip. The fast lane is available only before
C3 starts; post-C3 attempt/lock/C4 invalidation is unchanged.

### C1 - final lock and readiness audit

Only after C0 is clean and its same-tip focused execution join is green, `ROOT-IM` locks:

- candidate revision and clean status;
- exact operative hashes for `goal.md`, `GENERALIZATION_SPEC_2.md`, `IMPLEMENTATION_ROADMAP_2.md`,
  `EXECUTION_PLAN_2.md`, and `EXECUTION_READINESS_2.md`;
- immutable server pin/configuration and any server-limitation attribution/substitute history;
- fixture/toolchain/resource hashes and live board identities;
- preflight non-authorizing
  `plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json`,
  C1-attested exact user scope in canonical
  `plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json`,
  its operative goal hash/scope, path/hash, explicit/null user expiry and event expiry, per-call
  UUID/path/expiry schema, canonical user-scope object hash, and C1-locked default-deny
  `MCP_METHOD_POLICY.json` containing exact method/version, one action class, allowed parameter
  schema/ranges/required safe flags, and explicit prohibited-method/parameter/side-effect predicates,
  plus numeric UART/BLE/LoRa bounds and excluded destructive actions;
- final/acceptance spec, acceptance-kit and lane/MCP launch templates,
  `TARGET_SEED_MANIFEST.json` plus its four exact read-only files/hashes, stable IDs,
  dependency graph, and test/evidence contracts;
- implementation `runtime/firmware-v2/passed-tests.json`, `PARALLEL_CHECKPOINT.md`, out-of-scope
  ledger, and zero-process/zero-claim state. That registry becomes read-only to C3.

The seed manifest enumerates exactly `TARGET_CHARTER.md`, `PINNED_INPUTS.json`,
`TEST_CONTRACT.json`, and `EVIDENCE_SCHEMA.json`; C1 separately records the manifest hash. Those
five files are read-only locked inputs. This is final Checkpoint A. Its lock excludes target application source and target-repository-local
configuration later created and versioned through `C3-HARNESS`; those are governed by the target
dependency fingerprint. No full accumulated suite runs here.

For authorization, `ROOT-IM` mechanically creates the final C1 record by copying the user-issued
scope and any explicit user expiry exactly into the exact five-key schema `schema_version`,
`issuance_source`, `canonical_user_scope_sha256`, `user_issued_scope`, and `derived_bindings`.
`derived_bindings` contains exactly `c1_lock_id`, `operative_goal_sha256`, `stable_fixtures`,
`destructive_exclusions`, `rf_limits`, `mcp_server_pin`, `mcp_method_policy`, and
`governing_documents`, with the closed fixture/reference subshapes in
`S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`. No extra authority flag, invented time/expiry,
fixture, action, or C1 lock hash is admitted. That action is
validation and attestation, not issuance; it cannot alter or expand scope.

The delegated `expires_at_utc` is copied exactly when explicitly user-supplied and otherwise is
`null`; authority expires on user revocation/scope change, C1 invalidation/replacement, or
completion. Every call authorization is one-shot and expires at the earlier of the delegated time
(if any) and five UTC minutes after creation, on a bound-field change, or when its attempt
exits/aborts. A fresh attempt under the same operative C1 uses new call IDs. Retry uses a new call ID.
Only an explicit user directive may set/extend delegated time, forcing fresh C1.

The serialization order is mandatory and non-circular: ROOT first allocates a fresh opaque UUID
`C1_LOCK_ID` that is not derived from content and canonical `final/c1/{C1_LOCK_ID}/`; creates and
hashes that directory's authorization artifact; then writes sibling `C1_LOCK.json` containing the
ID, canonical authorization path/hash, and all other locked-input hashes. Its hash is computed last
into sibling `C1_LOCK.sha256` and is never an authorization input. Every replacement C1 allocates a
new UUID/directory; consumers may use only operative C1 paths/hashes.

### C2 - final test loop

Run the final disposable non-hardware project and all dependency-invalidated synthetic gates: the protected original general-harness unit tests, new cross-route coding-isolation units, dual-route compatibility, MCP lifetime, relay binding, event/ack, resource contention, same-thread/path resume, target materialization, failure classification, exact shutdown, and docs/operator flow. Use targeted stable test IDs and preserve only demonstrably unchanged green results. C2 must be green before hardware is admitted.

C2 is verification of the current C1 lock, not permission to drift from it. If a C2 failure is an
environment/test-execution issue and no locked input changes, rerun only the failed IDs against the
same lock. If repair changes the candidate, server pin, test/evidence contract, configuration,
authorization, fixture binding, acceptance-kit/lane/MCP template, or another C1-locked
implementation input, the lock is invalid: create a new C1 Checkpoint A and rerun every dependency-
invalidated C2 ID. Production, policy, expected-behavior, coverage-obligation, or other operative
changes return to the owning implementation step and full fresh C0. A qualifying strict test-only
fast lane correction instead requires its checklist and exact failed-ID rerun before the new C1; it
never inherits the old lock. C3 may consume only the latest green S4/C1/C2 pair.

Before an expensive selected executor set with custom per-check subprocess evidence, its doer first
runs one same-lane recordability preflight. It performs no real product, MCP, or hardware work and
must validate one complete sample record: stable ID, exact inputs, worker/process creation identity,
timing, command, output paths, and exit outcome. A preflight or reconstructable report/path/schema
defect is corrected in place without invalidating product credit; irrecoverable raw identity evidence
reruns only the affected stable ID on the same lock. Its green evidence is bound to the exact runner,
procedure, configuration, and environment fingerprint and reused until that fingerprint changes.
When a selected set reports only fixture, mock,
or executor-environment defects, ROOT batches the complete classified test-only set and reruns that
selection once, never once per individual fixture correction.

A post-C1 governing-document hash change follows the live-goal protocol and always receives an
append-only change-classification record. ROOT maps changed requirement IDs to the plan's lock-input
domains and gate dependency matrix, preserves every non-consuming gate, and reruns only consumers.
A hardware-authority or in-flight-mutation dependency change suspends affected calls immediately; a
candidate behavior/contract change uses the owning product route; a test-procedure/evidence or outer-
topology change reruns only its dependent test/rehearsal/attempt work. Byte-only editorial changes
may use the reviewed chain. When dependency impact cannot be classified confidently, use the
documented conservative fallback. No document name or whole-file hash alone forces a full relock.

P4 manifest creation freezes every `external_references` path/hash through C4, safeguard, and
completion. Any later governing-document change or editorial-chain append invalidates that C3
acceptance result; C4/safeguard reject it and never accept an earlier chain prefix as current.
Preserve the attempt, apply the normal goal/editorial classification, and run a fresh C3 attempt
(P0 plus only dependency-invalidated work) before C4. A semantic or `goal.md` change still requires
the owning-step/fresh-C0/C1/C2 route.

### C3 - practical test

**Pre-attempt host-only rehearsal.** Before allocating an `attempt-NNNN` pair, launching `F.C3.O` or
the required helper, creating a target repository, starting MCP, or claiming hardware, run an exact-C1/C2
candidate rehearsal against disposable local fakes. It must prove launch admission, retained-session
authorization, exact process/identity binding, duplicate-assignment refusal, watcher correlation,
recovery/idempotence, cleanup, and terminal closure. Reuse only dependency-unchanged green rehearsal
IDs. Candidate failures return through the material repair/relock route; fixture/executor failures
stay in their lane. A green rehearsal unlocks the physical attempt but is never physical evidence.

The practical test is the fresh Four-Board Dual-Family Firmware Lab. The initial attempt's target repository begins with exactly the five C1-locked seed files and no completed application implementation. Target workers cannot edit the seed; subsequent source/tests/build files/target-local configuration are versioned target work. A restarted attempt may add only the exact accepted target source-tree commit as reconstruction input.

**Final and acceptance lane topology**

`F.C3.M (= ROOT-IM) -> direct codex exec F.C3.O || direct non-agent deterministic helper [|| optional F.C3.W review]`

`ROOT-IM -> nonce/key/ORCHESTRATOR_LAUNCH_INTENT -> spawn F.C3.O with nonce/no key -> exact ORCHESTRATOR_IDENTITY -> O identity-hash acknowledgment -> ORCHESTRATOR_KEY_RELEASE -> private-key transfer/discard -> release-bound O ready/work`

`F.C3.O -> assignment -> C3-HARNESS -> codex exec -> one F.C3 target worker -> RESULT/events -> C3-HARNESS -> F.C3.O`

`helper observation -> ordinary finding pool OR exact safety stop -> ROOT containment -> product/support classification -> one bounded route`

`F.C3.O -> AUTHORIZED_SERVER_LIMITATION -> exact attribution -> strongest safe substitute assigned through C3-HARNESS -> explicit physical non-certification -> continue`

`F.C3.O crash/stall/incomplete P4 commit -> ORCHESTRATOR_LOST -> F.C3.M (= ROOT-IM) -> exact topology termination/preservation -> classified fresh C3`

| Lane ID | Agent/model | Authority | Root and lifetime | Handoff/failure route |
|---|---|---|---|---|
| `F.C3.M` | Exact alias for `ROOT-IM`, the current outside implementation coordinator; not another agent | Launches O, the deterministic helper, and optional W; withholds O key; monitors liveness/P4; owns observation closure, support-failure classification, safe cleanup, implementation repair/promotion; never assigns target tasks or repairs the pinned server | outside candidate and target roots; entire C3 | acts on O completion/loss or exact helper stop; preserves product credit across support failures |
| `F.C3.O` | Fresh Sol-high-Fast acceptance orchestrator | Sole target-project decision-maker; receives the ephemeral private key only after the identity/key-release gate, signs release-bound independent hardware decisions, submits assignments to `C3-HARNESS`, and owns sprint order/triage/evidence; never directly launches target workers | isolated acceptance-orchestrator root; P0-P4 | target-local defects stay here; harness defect goes to W/ROOT; pinned-server source defect is reported to ROOT; unexpected loss fails attempt |
| `C3-HARNESS` | Candidate harness control plane and exact controller processes; not a Codex-agent role or slot | Sole target-worker launcher/lifecycle owner and sole holder of each physical MCP launch/stdio capability; brokers structured requests only after all four call artifacts validate | candidate runtime operated by O; entire C3 attempt | rejects invalid results/calls/direct endpoints; surfaces actionable state to O/W; never edits source |
| deterministic helper | Non-agent process launched directly by ROOT | Required observer; writes only ready/heartbeat/cursor/finding/terminal-service evidence; no approval/task/launch authority | external support root through candidate shutdown; ROOT owns exact launch/stop/reap/close | ordinary findings pool; only three exact conditions request safety stop; missing facts use approved fallbacks or make only the attempt incomplete |
| `F.C3.W` | Optional fresh Terra-medium-Fast reviewer | Supplemental independent read-only review only; no required evidence, approval, task, launch, stop, or closure authority | separate optional review root | report/exit retained when available; absence or loss never gates the attempt |
| `F.C3.A1` | Terra-medium-Fast target test writer | Writes tests and evidence assertions only | candidate-launched disposable target worktree; one assignment at a time | result returns through `C3-HARNESS`; test defect is reassigned by O through the harness |
| `F.C3.C1` | Terra-medium-Fast target coder | Writes target application/firmware only; may diagnose but never edit the harness or pinned MCP server | candidate-launched disposable target worktree; never concurrent with another target worker | result returns through `C3-HARNESS`; target product defect is reassigned by O through the harness |
| `F.C3.P1` | Luna-high-Fast doer/test executor | Builds and requests harness-brokered MCP/hardware operations, runs stable tests, captures returned evidence; no source edits and no direct physical endpoint | candidate-launched isolated per-sprint run; controller owns MCP roots | result returns through `C3-HARNESS`; execution issue is reassigned by O through the harness |
| `F.C3.R1` | Terra-medium-Fast target reviewer | Read-only source/result/evidence review | candidate-launched isolated review root after each sprint | result returns through `C3-HARNESS`; O classifies findings |

`F.C3.O` occupies one Codex-agent slot beside `ROOT-IM`; exactly one of A1/C1/P1/R1 is active at a
time. Optional `F.C3.W` may use the remaining slot. The deterministic helper and `C3-HARNESS`
controller processes are non-agent processes. The target-creation process remains decided by O and
worker lifecycle remains managed by the candidate harness.

**C3 external ownership:** ROOT alone allocates the attempt pair, launches/stops/reaps the helper,
writes helper launch/abort-observation/observation-close records, classifies outer procedure failures,
and performs emergency cleanup. The helper alone writes its ready/heartbeat/finding/terminal-service
records. O alone decides target work and seals manifest/result. `C3-HARNESS` alone owns target-worker,
claim, MCP, event, and ordinary candidate cleanup. Optional W owns only its supplemental report.

**Observation evidence-fallback matrix:** each backup use is written into
`WATCHER_OBSERVATION_CLOSE.json` with exact hashes, attempt/process identity, sequence/time
correlation, evaluator `ROOT-IM`, and two independent source classes. Candidate-owned evidence alone
cannot corroborate a candidate-behavior claim.

| Required fact | Primary source | Allowed independent backup classes | Missing disposition |
|---|---|---|---|
| exact helper identity/launch | ROOT `WATCHER_HELPER_LAUNCH.json` plus retained process handle | ROOT launch log and native OS creation-identity snapshot | attempt incomplete before target work |
| readiness before target work | helper `WATCHER_READY.json` | ROOT wait/admission record plus first correlated helper heartbeat | attempt incomplete; target work must not start |
| continuous heartbeat/cursor | helper `WATCHER_HEARTBEATS.jsonl` | ROOT supervision snapshots plus independently timestamped candidate/external event progress | incomplete observation interval only |
| finding/immediate-stop disposition or observed absence | helper finding/abort record plus ROOT abort-observation record | ROOT supervision snapshot plus correlated external MCP/OS/target evidence for the same interval | incomplete affected conclusion; safety containment may still occur |
| terminal service after candidate shutdown | helper `WATCHER_SERVICE_TERMINAL.json` | ROOT stop/reap record plus final correlated heartbeat/candidate-shutdown evidence | attempt cannot seal until proved or rolled |
| exact helper exit/reap | ROOT retained-handle wait in observation-close | native OS before/after identity snapshots plus helper terminal/output record | attempt cannot seal until proved or rolled |

Physical concurrency does not add a target agent. For P3, the one active `F.C3.P1` receives one
candidate-harness assignment and requests two concurrent non-agent physical lane process groups:
`P3.STM` owns STM-A/STM-B and `P3.NRF` owns NRF-A/NRF-B. During normal operation only `C3-HARNESS`
creates, starts, stops, and reaps those groups and owns both exact lane records, controller/process identities, claims,
events, and cleanup; each group owns distinct MCP processes, `.firm`, artifact, and log roots. P1 may
request and operate both only through the assigned harness interfaces and may not spawn a group or
launch another Codex agent.

The candidate physical-lane controller is the exclusive capability broker. It alone receives the
pinned BYO server command/environment, launches/owns the MCP process, and holds its stdio handles.
O and target workers receive no physical MCP registration, endpoint, credential, launch command, or
inheritable handle; they submit structured operation requests and receive controller-recorded results.
The controller refuses to forward without valid proposal, signed O decision, authorization, and
dispatch admission. Negative tests and C4 audit process environments/handles plus ledgers for bypass.

For every mutating operation, `C3-HARNESS` allocates a fresh opaque UUID `CALL_ID` and atomically
create-new/no-overwrite writes `hil/{lane-id}/call-proposals/{CALL_ID}.json`, binding operative C1 and
delegated path/hash, exact attempt/lane/logical board, stable probe UID, reviewed target/profile,
current route or canonical null, create-once board-identity/claim-acquisition evidence paths/hashes,
MCP method/version, pinned server revision/schema hash, locked `MCP_METHOD_POLICY.json` path/hash,
exact arguments, canonical policy-evaluation object/hash, live plan path/hash, required positive
`max_operation_duration_seconds`, and permission. After reading
it, O independently atomically creates attempt-evidence `authorization-decisions/{CALL_ID}.json`
binding proposal path/hash, matching fields, O's exact process/thread identity,
approve/deny/rationale/time/expiry. Before launch ROOT creates `O_LAUNCH_NONCE`/ephemeral Ed25519
keypair and atomically writes `topology/ORCHESTRATOR_LAUNCH_INTENT.json` with attempt, nonce, public
key, requested model/effort/tier, and time. It spawns O with the nonce but no private key over a
bidirectional inherited anonymous pipe. After process creation, before O ready/work/decision, ROOT
atomically creates `topology/ORCHESTRATOR_IDENTITY.json` binding intent path/hash, nonce/public key,
and exact PID-plus-creation/thread/model, sends its path/hash over the pipe, and requires O's exact
nonce/hash acknowledgment. ROOT then atomically writes create-once
`topology/ORCHESTRATOR_KEY_RELEASE.json` as the not-before authorization for key transfer, containing
that acknowledgment and release UTC time; only then does ROOT send the private key and discard its
copy. O may sign ready/work/decision only after reading that release record; each signed record binds
its path/hash and has an issued time no earlier than release. The three topology records are never
rewritten; any failure preserves the attempt and requires a fresh one. The key never enters file/env/
prompt/log/target/harness state. O signs canonical decision JSON. The decision root is O-owned and
harness-read-only; harness verifies signature, launch, identity, and key-release binding before
dispatch and C4 verifies provenance. Only valid signed approval permits the harness to atomically create `hil/{lane-id}/authorizations/{CALL_ID}.json`
binding both earlier paths/hashes and copying the same exact call/method/server/schema/policy/
evaluation/argument/plan/duration plus board/probe/target/route/identity/claim fields. Before MCP
submission the harness validates all fields and any editorial chain; invalid state prevents
dispatch/success. It then samples its monotonic clock and atomically creates immutable
`hil/{lane-id}/dispatch-admissions/{CALL_ID}.json`, binding authorization path/hash, fresh five
governing hashes, every revalidated field, clock identity, start, and deadline = start + declared
duration. Dispatch/result reference all four paths/hashes plus exact method/version, server/schema, policy/evaluation hashes, normalized arguments,
plan/duration, and probe/target/route/identity/claim. The harness recomputes policy evaluation and
requires equality across actual dispatch, proposal, O decision, and authorization before submission;
result validation rediscovers identity/route and revalidates claim, and mismatch forbids success.
Each one-shot ID expires within five UTC minutes (or earlier delegated/event/attempt
expiry), is never overwritten/reused, and retry gets a new ID. Dispatch requires remaining validity
to cover the live plan maximum plus a fixed 60-second result/cleanup margin, and authorization must
remain valid through result commitment. Mid-call expiry/revocation requests safe MCP cancellation
where supported, records raw outcome as `INDETERMINATE_EXPIRED`, performs bounded cleanup, forbids
success, and holds claims until exact child/MCP exit/reap.
Admission-to-submission time counts. The harness enforces the monotonic deadline; at the declared
maximum it requests safe cancellation and, if still running, performs exact bounded MCP/controller
termination/cleanup. Result records start/deadline/end/elapsed and cancellation/termination. An
overrun is `INDETERMINATE_TIMEOUT`, never success, and claims remain held through exit/reap/cleanup.

The user-issued scope is exactly the canonical JSON object in `goal.md` Section 11. C1 records its
sorted-key compact UTF-8 JSON SHA-256 and copies its fixtures, nine action classes, prohibitions,
application-flash/UART/BLE/LoRa numeric bounds, and explicit/null expiry verbatim. S2/C1 create and
lock default-deny `MCP_METHOD_POLICY.json`. For each exact server method/version it records one action
class, permitted parameter schema/ranges, required safe flags, and explicit prohibited-method/
parameter/side-effect predicates. An unmapped method denies. A destructive-capable method also
denies unless the exact call is technically constrained and evidenced safe; an action-class label
cannot override a prohibited semantic, and live technical evidence may only narrow maxima. The
policy sets a maximum duration per method; every mutating plan requires a positive integer
`max_operation_duration_seconds` at or below it, otherwise deny.

At the actual boundary before each mutating MCP dispatch, the harness independently rehashes
`goal.md` and all four governing planning/readiness docs, requires the live set to be covered by the
operative C1 plus valid append-only change dispositions, and binds it into the immutable dispatch
admission and dispatch/result ledgers. An unclassified mismatch expires all pending calls, refuses
dispatch, emits `GOVERNING_INPUT_CHANGED`, and invokes live-goal handling. ROOT classifies the
changed domain, refreshes C1 when needed, and preserves every non-consuming gate.
ROOT's read-only governing-file watcher remains active in flight; detected change is revocation and
uses `INDETERMINATE_EXPIRED` cancellation/cleanup/no-success handling.
It is a registered non-agent deterministic helper with exact PID-plus-creation/current hashes/
heartbeat in `topology/GOVERNING_INPUT_WATCHER.json`, writes only its own evidence, consumes no agent
slot, and must exit/reap into the topology shutdown inventory.
The same-resource contention subcase is a second operation against an already-owned exact resource
inside this assignment and must queue or fail closed without acquiring duplicate ownership.

**Practical sprint order and pass criteria**

1. **P0 host/routing:** verify H00/H01/H02/H05 intent, strict MCP schemas/plans, clean per-lane roots, all four stable probes/current VCOM routes, S10-S13 setup and returning-state evidence, and no mutation outside authorization.
2. **P1 STM32:** A1 authors tests; C1 implements controller/responder; P1 builds and requests harness-brokered MCP setup/flash/reset/debug/read/UART operations; R1 audits. Require deterministic checksummed sequenced I2C2 exchange, error recovery, reconnect, debug observability, and sustained ordered traffic.
3. **P2 nRF52:** repeat the test-first multi-agent sequence for BLE peripheral/central GATT exchange and 915 MHz CoreSX1262 low-power ping/pong. Resolve `P.05` before any dependency or mark only that dependent action unadmitted; the required core cannot pass if unresolved mapping blocks it.
4. **P3 concurrency:** under the single P1 assignment, run accepted STM and LoRa modes simultaneously as `P3.STM` and `P3.NRF` with distinct MCP/root/claim/event ownership. Exercise independent progress, a same-resource queue/fail-closed contender, exact relay/authorization, a same-thread/path resume, and one predeclared intentional target-code defect. Before injection O records the exact source-controlled, non-destructive change and expected behavioral failure. It may modify only target application source, never harness/server/fixture/authorization/hardware configuration; the ordinary target test path must observe the failure before O submits diagnosis/repair assignments through `C3-HARNESS` and reruns only invalidated IDs.
5. **P4 shutdown/evidence:** first close boards and all candidate-managed state. ROOT then stops/reaps
   the deterministic helper and writes `WATCHER_OBSERVATION_CLOSE.json` from exact primary or
   approved fallback sources. O's thin attempt-local sealer calls
   `c3_outer_support.validate_observation_close()` and may not import a closed-attempt sealer that
   requires AI-watcher output. Only after required observation is closed does O recursively enumerate
   every regular file under both attempt roots, including adverse/failed/denied/conflicting evidence;
   symlink/reparse/unresolved-temp entries are forbidden. O atomically creates
   `EVIDENCE_MANIFEST.json` listing/hashing every file except itself, not-yet-created
   `ACCEPTANCE_RESULT.json`, and reserved `topology/`. Canonical locked artifacts outside the attempt
   roots appear only as verified external references. O writes the bound result within 90 seconds.
   C4 independently enumerates and verifies. After O exits, ROOT writes `ORCHESTRATOR_EXIT.json` and
   closes reserved topology evidence. Optional AI-reviewer artifacts are supplemental.
The shutdown file inventories/hashes every other regular topology file but excludes itself;
symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and
separately hashes/verifies shutdown.

**Operative observer/support boundary**

ROOT directly launches the deterministic helper through `.codex/scripts/c3_outer_support.py` and
uses that support layer for classification, observation closure, outer-failure disposition, and safe
cleanup. Reviews, tests, and observations complete their assigned surface and pool ordinary findings.
Only exact evidence of an unauthorized/wrong-resource operation, loss of containment/cleanup of a
live process, or irreversible corruption of evidence needed to judge later work stops immediately.
After containment, ROOT still decides whether the cause is a product defect or a support failure.

Support failures are corrected in place when the product result remains determinable. Otherwise only
the affected attempt/work becomes incomplete and rolls fresh, retaining all independent immutable
product credit. Cleanup records an already-gone or identity-unverified child without signalling it
and continues for all other registered children. Candidate repair/relock requires exact product-
material evidence, never merely a helper/controller/report failure.

The deterministic helper must not convert an orchestrator/operator mistake or an expected
rejection/failure caused by that mistake into an automatic product failure. It observes whether the
candidate rejects, contains, reports, resumes, and cleans up the work according to contract and
records a complete finding for pooled triage. Orchestrator-side correction uses the owning lane and
selective retest; an immutable-attempt rollover does not reset implementation or C1 unless exact
dependency evidence requires it.

Termination is ordered: ROOT first requests normal controller-managed shutdown. Only when the exact
registered controller is unavailable/unresponsive may ROOT host-terminate/reap the pre-registered
controller/MCP/process-group identities and atomically write
`topology/EMERGENCY_TERMINATION.json` with request/failure proof, exact identities, per-process
outcomes, and UTC/monotonic times. This is no MCP/hardware/broad-kill authority. Board state is
indeterminate, the attempt fails, and fresh-attempt P0 returning-state recovery precedes mutation.

The helper writes create-once attempt evidence `watcher/ABORT_REQUIRED.json` only for one of the
three explicit live-safety conditions and binds the exact evidence that supports it. `ROOT-IM`
monitors that path from helper readiness through terminal service; it is never relayed through O,
`C3-HARNESS`, or `manager-signals/`.

Before target work, the helper publishes readiness and then heartbeats at the configured bounded
cadence with exact process identity, monotonic sequence, timestamp, and observation cursor. ROOT
monitors both process and evidence. Helper exit, stale evidence, or observation-access loss is a
support failure: contain live registered work when necessary, then prove the missing facts through
the fallback matrix or mark only the affected attempt incomplete. Optional AI-review launch/report/
exit provenance may be retained separately but is never required for C57/P4.

ROOT also monitors O's exact process and `topology/ORCHESTRATOR_HEARTBEATS.jsonl` every 30 seconds
with a 90-second stale threshold through result commitment and normal exit. Manifest creation starts
an absolute 90-second result deadline. Unexpected O exit, stale/lost liveness, missed result
deadline, or normal exit without valid result is `ORCHESTRATOR_LOST`: ROOT stops new work,
terminates/reaps only registered identities, preserves the partial immutable attempt, writes
`topology/ORCHESTRATOR_LOST.json`, and applies the same repair/relock-versus-environment
classification before a fresh attempt. Partial manifest/result files are never completed or reused.

After valid result and exact normal O exit/reap, ROOT atomically creates
`topology/ORCHESTRATOR_EXIT.json` binding O identity/key-release/result paths/hashes, reaped identity,
exit code/time, and captured final-message content/hash. On abnormal loss, `ORCHESTRATOR_LOST.json`
retains all available exit/final-message fields and never claims a normal exit. The topology shutdown
inventories the applicable record; missing normal provenance blocks completion.

Target application/compiler/test/target-repository-configuration/invalid-call defects remain with `F.C3.O` only when no C1-locked input changes; O routes
their repair only through `C3-HARNESS`. A required locked kit/template/configuration change leaves
the target-local route. A reproduced immutable pinned MCP server defect/incompatibility is different:
O records `AUTHORIZED_SERVER_LIMITATION` with the exact call/raw/process/source/counterfactual
evidence, then assigns the strongest safe substitute through `C3-HARNESS` in this order: supported
partial MCP test, focused test of the implicated pinned-server component, synthetic candidate
boundary unit. No role edits or repins the server, uses a direct hardware bypass, or calls the
unexecuted physical behavior passed. C4 rejects misattribution and convenience substitutions.

Every C3 attempt allocates the next monotonically increasing matching runtime/evidence
`acceptance/attempt-NNNN/` pair: one greater than the largest number on either side, or
`attempt-0001` only when neither side has an attempt. Both chosen paths must be absent; a one-sided
path or collision stops allocation for preservation/triage. Each pair has separate `target/`,
`hil/`, `events/`, `claims/`, `manager-signals/`, and `.agent-workspace/` roots. Prior pairs remain
retained read-only and are never cleared, overwritten, gap-filled, or reused. Every pair creates a
fresh attempt-local `passed-tests.json`. The C1-locked implementation
registry is never written. The new attempt registry may re-credit prior green results only by
immutable evidence path/hash and unchanged dependency fingerprint; it never copies or mutates prior
registry state and is included in P4's manifest. The initial attempt starts from the five locked seed
files only. A restart uses the next pair and a fresh target Git repository; a restarted
repository may reconstruct the exact last accepted target source-tree commit plus that seed but
copies no prior build outputs, mutable runtime state, claims, events, or process records. P0 always
reruns. Other earlier green target IDs stay credited only if their dependency fingerprints are
unchanged; identity-dependent IDs rerun from the earliest invalidated sprint, and every artifact
produced by the new attempt originates in its numbered roots.

Green target tests are not redone unless their declared source, harness/server behavior, configuration, hardware identity, runtime/repository/process identity, or upstream artifact dependency changed.

### C4 - nested static-audit loop

After practical success, fresh Terra-medium-Fast auditors independently inspect requirement coverage, role/topology separation, watcher classification, physical/electronic evidence, revision bindings, protected state, scope, and preservation of original general-harness unit behavior. One audit explicitly compares baseline and candidate unit-test manifests, shared-code dependency mappings, results, deletions, skips/expected failures, and assertion strength; it must detect any firmware-compatibility change that can regress the original general harness without a green unit oracle. Their reports join before triage.

The validator compatibility phrase is "only post-checkpoint-A static-review revival." Its exact
meaning here is that C4 is the only ordinary static-review revival while the current C1 Checkpoint A
remains valid. If a repair invalidates C1, the required fresh C0 starts a new lock cycle and may not
reuse or claim continuity with the invalidated checkpoint. Classify each accepted gap before repair:

- evidence-only correction: correct only a C4-owned report/annotation under
  `plans/general-coding-harness/evidence/firmware-v2/final/C4/annotations/`, outside every attempt
  root, then repeat C4; it cannot satisfy, alter, explain away, replace, or add acceptance evidence,
  and any defect in closed C3 evidence requires a fresh C3 attempt;
- target-source or target-repository-local-configuration repair with no locked-input change: start a
  fresh C3 attempt, rerun P0 and the earliest dependency-invalidated sprint, then repeat C4;
- any candidate/server/kit/template/fixture-binding/test-contract/authorization or other C1-locked
  input repair: return to its owning implementation step, run fresh C0, create a new C1 lock, rerun
  invalidated C2, start fresh C3 at P0 and the earliest invalidated target sprint, then repeat C4.

That last route is the sole allowed post-lock C0 re-entry. Within each mandatory route, only
dependency-invalidated automated or practical IDs rerun. Repeat C4 without an iteration cap until
every C1-C77 row is `PASS`, with no unresolved production-relevant in-scope gap. Conditional or deferred entries are
permitted only in the separate non-gating extended-qualification ledger, never in C1-C77.

C4 never creates a second or "final" lock. Before safeguard it verifies that candidate revision and
every locked input exactly equal the current C1 record. `goal.md` must exactly equal its C1 hash.
Each of the other four governing docs may use its own valid unbroken
`EDITORIAL_SUPERSESSION.jsonl` chain rooted at its locked hash, whose terminal hash becomes that
document's equality target; any other difference uses the locked-input repair route above.

## 8. Safeguard

After C4 is clean, retain the final C1 lock and run a pre-safeguard environment admission that
executes no safeguard source check or test. Repair and repeat admission until green. Then create one
logical `SAFEGUARD_RUN_ID` for that exact lock and execute the complete accumulated suite.

The validator compatibility phrase "complete accumulated suite exactly once" means one terminal
logical safeguard run per exact C1 lock under this admission/resume protocol; it does not require
rerunning already-green components after an environment-only interruption.

The safeguard includes the repository's required Ruff, format, BasedPyright-without-baseline-expansion, compilation, the complete original general-harness unit corpus, orchestrator, watcher, Codex integration, attention-retention, synthetic firmware, newly accumulated cross-route/compatibility/MCP/integration tests, and any server gate invalidated by an actual server change. It also verifies that no baseline unit was silently deleted, skipped, expected-failed, or weakened. An environment-only interruption resumes the same logical run ID and reruns only incomplete or dependency-invalidated components; completed green components remain credited when unchanged. A source/test/server/locked-input change ends that run as failed, follows the normal re-lock route, and requires a new run ID. Promotion requires one terminal green logical record with no incomplete component.

Every source check and test in this safeguard names the exact reserved candidate root. BasedPyright
uses the existing finding baseline mapped to candidate-relative paths without admitting new
findings. An invocation of the outer verifier while the stable runner still points at
`4699d27` is baseline evidence only and cannot satisfy this safeguard.

On green safeguard:

1. reconcile exact process, MCP, UART/debug session, claim, relay, event, and worktree state;
2. write the completion summary with candidate/server/target revisions, models, test counts, physical outcomes, and final token/agent evidence where available;
3. finalize the out-of-scope ledger for exhaustive applications, Q40, Q41, destructive recovery, added boards, and unrelated improvements;
4. write candidate, server, acceptance, watcher, topology, criteria, protected-state, full-verification, promotion, and completion records;
5. create `progress/v1.2` at the exact green candidate commit, stage the explicitly named stable runner on that
   distinct branch for the required outer verifier, and create a fresh inactive promoted runtime;
   preserve `progress/v1.1`, `pre-conversion-rollback`, the frozen legacy alias, and the prior promoted baseline. External push
   or publication requires an explicit live user directive.
6. after durable promotion evidence, close the two clean temporary linked worktrees with exact Git
   worktree operations only after retained-revision and zero-process checks; never recursively
   delete a worktree path.

Promotion is prohibited if any required physical behavior, identity, authorization, cleanup, topology, evidence, original general-harness unit regression, or C1-C77 audit is incomplete.

## 9. Rules the runner applies

1. Optimize for a working product efficiently, not activity volume. Confidence should be roughly 99.9% at promotion because independent implementation, review, tests, practical behavior, and evidence converge.
2. The workflow's compatibility phrase is "reviewer recommends; orchestrator decides." In this plan that phrase resolves explicitly to: `ROOT-IM` decides implementation findings, and `F.C3.O` decides final target-project findings. Every submitted review/test gap first passes the structured breakage-or-worth and problem-versus-fix-cost gate; a reviewer assertion alone never authorizes work. It never assigns the Sol-high-Fast child profile to `ROOT-IM`. Reviewers and watchers do not edit product code or silently expand scope.
3. Production coding is singular and serial. A second source-editing agent never overlaps Coder-main.
4. Use the preplanned 1-2 lane pools. The runtime never re-partitions a pool or invents another lane because work is slow.
5. Fan-out requires real independent file/question/resource ownership. Multi-lane results use merge-then-triage; a singleton uses singleton direct handoff without fake split/join work.
6. Every lane has a stable ID, explicit base, isolated branch/worktree or run root, deterministic join, and failure route.
7. Test-id scheme: `S1-COMP-*`, `S1-LIFE-*`, `S2-MCP-*`, `S2-KIT-*`, `S3-DUAL-*`, `F-P0-*` through `F-P4-*`, plus retained upstream IDs. IDs never change merely because a run is repeated.
8. The applicable phase registry stores ID, dependency fingerprint, exact revisions/config/hardware identity, result, and evidence. C1 freezes the implementation registry; C3 writes only its manifest-covered attempt registry and references prior evidence immutably. Targeted stable test IDs rerun only after failure or dependency invalidation.
9. Pass criteria require all assigned IDs green, joined evidence complete, current-tip result and required finding artifact valid, no unresolved accepted in-scope finding, and exact clean process/resource/event state.
10. There is no iteration cap. Continue repair and selective verification while meaningful in-scope progress is possible.
11. Escalate a repeated same-signature failure after `stall_threshold` consecutive cycles with the same cause and no new evidence.
12. Escalate oscillation when two or more fixes alternate the same observable failure state without net progress.
13. Reject only-extraneous scope churn: unrelated refactors, frameworks, extra boards, exhaustive catalog work, UI, databases, endurance expansion, style-only review suggestions, and fixes whose complexity/regression/verification cost outweighs demonstrated benefit go to the ledger.
14. An unrecoverable error means exact evidence proves progress cannot continue within existing authority or available fixture state; difficulty, elapsed time, or a target defect is not unrecoverable.
15. `scope_policy` admits only requirements and defects necessary for backward-compatible firmware operation, MCP-backed acceptance, or preserved coding behavior. Everything else is deferred.
16. `gap_scope` is `change`: review and repair the planned change plus directly implicated pre-existing behavior, not every unrelated failing concern in the repository.
17. Hardware authority is explicit and narrow. Direct pyOCD/serial bypass, guessed wiring, operator touch, illegal RF behavior, and destructive recovery are prohibited.
18. `F.C3.O` decides target work and submits assignments; `C3-HARNESS` alone launches/owns target workers; `F.C3.M` (which is exactly `ROOT-IM`, not another agent) supervises implementation and exact termination/repair only. Confusing any of these roles invalidates C3.
19. ROOT directly owns the required deterministic helper. The helper has no kill/task/approval
    authority. Optional `F.C3.W` is read-only supplemental review and never gates acceptance.
20. Candidate deterministic watch remains diagnostic (`evaluator_enabled: false`). External helper
    evidence is independently closed by ROOT using the fact-by-fact fallback matrix.
21. Hardware/application/MCP target failures and ordinary coordinator/orchestrator/worker/support
    mistakes remain in their owning project/lane with selective correction. A support bug cannot
    block a product pass when sufficient independent evidence determines the valid product outcome;
    if evidence is insufficient, only affected work is incomplete. Candidate work reopens only on
    exact evidence of a product defect or changed product dependency.
22. `final_full_verification` is true, but the full accumulated suite runs only at the safeguard after physical success and C4.
23. The original successful general-harness unit suite is protected: map shared code to baseline IDs, run every invalidated unit, add cross-route isolation units, and forbid green-by-deletion, skip, expected failure, or weakened assertion. C0 and C4 must audit this evidence explicitly.
24. Reviewers complete the assigned affected-surface sweep and report one complete exact-tip finding
    set. They do not intentionally stop after the first defect. `ROOT-IM` repairs accepted findings
    as one bounded batch and never reviews or reconciles an intermediate batch commit.
25. A blocking finding proves a supported or credibly reachable deployed trigger plus a concrete
    negative product consequence. Cosmetic, unreachable, behavior-neutral, theoretical, and
    speculative-hardening suggestions are non-findings; realistically triggerable latent safety,
    authorization, identity, cleanup, and fail-closed defects remain blocking.
26. Before C0, the shortest affected smoke IDs run first; after they pass, complete read-only C0 and
    remaining focused execution may overlap on the same frozen tip. C1 waits for their join.
27. **Verification classification:** `production/material` changes use the full bounded repair batch;
    a **strict test-only fast lane** is only for fixture/setup-or-metadata-only corrections with known
    failed IDs. Its **deterministic diff/eligibility checklist** proves unchanged production, policy,
    contract, locked configuration, test oracle, assertion strength, expected outcome, stable ID, and
    coverage obligation. The same continuation reruns **exactly those failed IDs** once; there is
    **no fresh C0** and **no unrelated smoke** or work before it. Administrative corrections resume
    their lane without product review or test rerun. Any failed/unproved checklist or
    expected-behavior, coverage-obligation, operative-contract, production, or policy change is
    material.
28. Dependency maps, registry state, and aggregate join evidence reconcile once per accepted batch
    tip, while every raw lane result remains preserved.
29. Before an expensive executor selection relying on custom per-check process evidence, run one
    local **recordability preflight** first. It validates one complete inner-process record without
    product, MCP, or hardware work. Batch all classified fixture/mock/executor-environment
    corrections from a selected run before one rerun of that selection. Before any physical C3
    allocation, run an exact-C1/C2 candidate **host-only rehearsal** against disposable local fakes;
    it is mandatory admission evidence but never substitutes for the physical attempt.
30. **External-operation readiness:** the host-only rehearsal and the green outer-support smoke are
    required before attempt/O/helper/target/MCP/hardware allocation; neither grants physical credit.
31. **Scoped lock-input domains:** this project uses candidate behavior/public contract, test
    semantics/coverage, test-execution procedure/evidence, external-attempt topology, hardware/MCP
    authority, and immutable fixture/toolchain inputs. Whole-document hashes are audit records only.
32. **Gate dependency matrix:** S4 consumes task-card/semantic-acceptance contracts; S5 consumes the
    accepted S4 contract plus lane lifecycle/source allocation/event integrity; C0 consumes the full
    candidate behavior and coding-lane control contract;
    C1 consumes all operative product/authority domains; C2 consumes candidate/test-semantics and
    its selected procedure/evidence; rehearsal consumes candidate/C1/C2 plus external topology but
    no physical identity; C3 consumes all domains including live fixture/hardware identity; C4 and
    safeguard consume exact evidence from the gates they audit. ROOT records the concrete mapping in
    every change classification and invalidates only consuming gates.
33. **Governing-change classification:** for every governing edit ROOT records old/new hashes,
    changed requirement IDs, changed domains, invalidated gates, preserved evidence, and reason.
34. **Conservative fallback:** when ROOT cannot confidently map a change to domains/consumers, it
    suspends dependent external work and reruns the smallest documented enclosing gate set that can
    restore confidence; it does not silently guess or automatically restart unrelated green work.
35. **Logical thread lifetime:** one thread serves one task card. Resume it only for unresolved
    same-card work, the one report-only recovery, or the strict fast lane before acceptance. An
    accepted thread is terminal; unrelated later work starts a new bounded card/thread.
36. **Source-allocation mode:** allocate a linked worktree only for mutation or source-local
    execution state. Static read-only work uses an exact immutable source view plus a separate result
    root. Every lane records its selected mode and reason.
37. **Terminal-lane retirement:** after semantic acceptance and durable evidence/revision
    preservation, remove the lane from active discovery, safely close any clean unused linked
    worktree, retain required archive-only artifacts, and remove disposable caches. Never touch a
    dirty, live, unretained, ambiguous, unpreserved, or protected historical lane.
38. **Shared-event serialization:** every process appending to one event log waits on the same
    cross-process lock, writes and flushes one complete record, then releases it. Concurrent-process
    regression evidence is required.

## 10. File handoffs

`ROOT-IM` owns final integration and the authoritative copies of these handoffs:

| Handoff | Required location | Producer | Consumer |
|---|---|---|---|
| Governing specification | `active_docs/GENERALIZATION_SPEC_2.md` | planning turn | all lanes |
| Roadmap criteria | `active_docs/IMPLEMENTATION_ROADMAP_2.md` | planning turn | all lanes and audits |
| Execution plan | `plans/general-coding-harness/EXECUTION_PLAN_2.md` | planning turn | `ROOT-IM` |
| Task-card product contract | top-level `task-card-spec.md` | planning turn; S4/S5 ROOT plans bind its hash | S4/S5 implementation/review/test lanes and later generic coding orchestration |
| External C3 support contract | top-level `test-cleanup.md` | preparation turn | ROOT, rehearsal, C3, C4 |
| External C3 support source | `.codex/scripts/c3_outer_support.py`, `.codex/scripts/c3_watcher_helper.py`, and `.codex/scripts/run_c3_outer_support_smoke.py` | preparation turn; exact hashes recorded before resume | ROOT-generated future attempt controller; never imported from closed attempt roots |
| S4 feature plan | `plans/general-coding-harness/evidence/firmware-v2/S4/S4_ROOT_FEATURE_PLAN.md` | `ROOT-IM` before S4 child dispatch | S4.D1/R1/D2, C0/C2 auditors |
| S5 feature plan | `plans/general-coding-harness/evidence/firmware-v2/S5/S5_ROOT_FEATURE_PLAN.md` | `ROOT-IM` after S4 acceptance and before S5 child dispatch | S5.P1/R1/D1, C0/C2/C4 auditors |
| S5 terminal-lane archive manifest | `plans/general-coding-harness/evidence/firmware-v2/S5/TERMINAL_LANE_ARCHIVE_MANIFEST.json` | `ROOT-IM` after S5 acceptance | C0/C2/C4 and safeguard |
| Implementation workspace | `plans/general-coding-harness/runtime/firmware-v2/.agent-workspace/` | `ROOT-IM` during S1-S5/C0-C2/C4 | implementation lanes and audits; never reused as C3 attempt state |
| C3 attempt workspace | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/.agent-workspace/` | `C3-HARNESS` controllers during that attempt | `F.C3.O`, deterministic helper, optional `F.C3.W`; immutable after attempt exit |
| Parallel state | `plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md` for implementation; `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/PARALLEL_CHECKPOINT.md` for C3 | `ROOT-IM` at implementation joins; `F.C3.O` through candidate commands during C3 | next lane/gate; attempt file retained read-only after exit |
| Passed registries | implementation `plans/general-coding-harness/runtime/firmware-v2/passed-tests.json`; C3 `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/passed-tests.json` | ROOT writes implementation until C1 freeze; `C3-HARNESS` writes only current attempt registry | selective planner; C4 verifies C1 immutability and manifest coverage/reference integrity |
| Native event log | `plans/general-coding-harness/runtime/firmware-v2/events/LANE_EVENTS.jsonl` for implementation; `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/events/LANE_EVENTS.jsonl` for C3 | candidate controllers | `ROOT-IM` during implementation; `F.C3.O` and helper observation during the named attempt |
| Manager signals | implementation `plans/general-coding-harness/runtime/firmware-v2/manager-signals/`; C3 `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/manager-signals/` | exact manager-owned relay/repair producer | explicit owning control plane only: `ROOT-IM` outside C3, `F.C3.O` through `C3-HARNESS` inside the named attempt; watcher abort is explicitly excluded |
| Product step evidence | `plans/general-coding-harness/evidence/firmware-v2/S1/` through `S3/` | step lanes/`ROOT-IM` | C0/C4 auditors |
| Final automated evidence | `plans/general-coding-harness/evidence/firmware-v2/final/` | C0-C2/safeguard | promotion audit |
| Practical acceptance evidence | `plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/` | F.C3.O/ROOT helper; optional F.C3.W supplemental | C4 and completion; every prior attempt retained read-only |
| Acceptance manifest/result | attempt evidence create-once `EVIDENCE_MANIFEST.json`, then `ACCEPTANCE_RESULT.json` within 90 seconds | `F.C3.O` only after candidate shutdown and valid helper observation close | closed inventory of all regular files across both roots except self/result/reserved topology, plus separately verified external references; C4 independently enumerates and rejects unknown/unlisted/mismatched files |
| O identity/liveness | reserved prelaunch `topology/ORCHESTRATOR_LAUNCH_INTENT.json`, post-spawn `ORCHESTRATOR_IDENTITY.json`, `ORCHESTRATOR_KEY_RELEASE.json`, heartbeats, normal `ORCHESTRATOR_EXIT.json`, or loss | ROOT writes create-once intent/identity/key-release/exit-or-loss; O acknowledges identity before key transfer and writes heartbeats | release-bound signatures, 30/90 liveness, P4 deadline, exact final-message/exit/reap, and C4 provenance |
| Governing-input watcher | reserved `topology/GOVERNING_INPUT_WATCHER.json` | ROOT-owned registered non-agent helper writes exact identity/current hashes/heartbeat only | mid-call revocation; exact exit/reap covered by topology shutdown |
| C3 topology shutdown | attempt evidence `topology/TOPOLOGY_SHUTDOWN.json` | `ROOT-IM` after helper observation close and O/remaining registered topology exit/reap | inventories/hashes every other topology file, excludes itself, forbids symlink/temp, and is separately hashed/verified by C4 |
| Observer evidence | attempt evidence `watcher/WATCHER_READY.json`, `watcher/WATCHER_HEARTBEATS.jsonl`, pooled findings/abort-disposition, `WATCHER_SERVICE_TERMINAL.json`; ROOT-owned `topology/WATCHER_HELPER_LAUNCH.json` and `WATCHER_OBSERVATION_CLOSE.json`; optional AI review artifacts | deterministic helper writes observation records; ROOT writes launch/close and validates fallback sources | gates target start and manifest closure; provides complete observation without making a support failure an automatic product failure |
| Target project | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/target/` | F.C3.A1/C1 through `C3-HARNESS` | F.C3.P1/R1 |
| Per-lane MCP state/artifacts | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/` | `C3-HARNESS` lane controller/MCP server only | F.C3.P1 receives returned results only in its `RESULT.json`; O/W/C4 consume broker evidence read-only |
| Retained MCP session | `hil/{lane-id}/sessions/{SESSION_ID}/SESSION_REQUEST.json`, `SESSION_OPEN.json`, and terminal `SESSION_CLOSED.json` or `SESSION_ABORTED.json`; O normal-close intent at `session-close-decisions/{SESSION_ID}.json` | `C3-HARNESS` creates lifecycle evidence and alone owns process/stdio/claim; F.C3.O creates only the signed normal-close decision | one finite attempt/lane/board Server Run; every post-bootstrap call separately authorized, consecutive, predecessor-bound, policy-transition-valid; terminal exact drain/exit/reap/release |
| Hardware authorization | canonical preflight/C1 scope plus default-deny `MCP_METHOD_POLICY.json`; proposal, signed O decision, authorization, and pre-dispatch admission under one call ID | harness proposes; O signs; harness derives immutable authorization, then separately admits fresh live state without rewriting it | exact four paths/hashes through result; monotonic plan deadline plus validity margin; timeout/expiry/revocation is no-success with exact cleanup |
| Lane result | direct lane `.agent-workspace/RESULT.json` | each mutable lane | owning controller plus `ROOT-IM` during implementation or `F.C3.O` through `C3-HARNESS` during C3 |
| Completion and promotion | `plans/general-coding-harness/evidence/firmware-v2/final/completion.md` and adjacent records | `ROOT-IM` | future sessions |

Every handoff records exact revision, lane identity, timestamp, dependency fingerprint, and evidence hashes. Test writers never overwrite product evidence; reviewers never mutate source; doers never edit tests or source; joins preserve both raw lane outputs and the manager's decision.

## 11. Config block

```yaml
plan_id: firmware-generalization-v2
# external-operation readiness: green host-only rehearsal and outer-support smoke before real resources
# scoped lock-input domains: candidate behavior; test semantics; execution evidence; external topology; authority; immutable fixtures
# gate dependency matrix: Section 9 rule 32 is authoritative and every change record instantiates it
# governing-change classification: append-only hashes, requirement IDs, domains, invalidated gates, preserved evidence, and reason
# conservative fallback: smallest enclosing documented gates when dependency impact cannot be classified confidently
runtime_root: plans/general-coding-harness/runtime/firmware-v2
evidence_root: plans/general-coding-harness/evidence/firmware-v2
implementation_passed_registry: plans/general-coding-harness/runtime/firmware-v2/passed-tests.json
c1_evidence_root: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}
delegated_authorization_draft: plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json
delegated_authorization: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json
user_hardware_scope_source: goal.md Section 11 USER_HARDWARE_AUTHORIZATION_V1 canonical JSON object
mcp_method_policy: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/MCP_METHOD_POLICY.json
editorial_supersession: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/EDITORIAL_SUPERSESSION.jsonl
promoted_runtime_root: plans/general-coding-harness/runtime/promoted-firmware-v2
candidate_worktree: plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate
candidate_branch: firmware/v2-candidate
candidate_base: 4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f
frozen_rollback: 287ea53793e3963062882012ff80c3b0e8c41587
mcp_server_worktree: plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate
mcp_server_branch: firmware/v2-mcp-candidate
mcp_server_base: f003f84a7df51cd8595a3203c62e225b21da2a22
acceptance_attempt_runtime: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN
acceptance_attempt_evidence: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN
c3_passed_registry: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/passed-tests.json
call_authorization: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/authorizations/{CALL_ID}.json
call_proposal: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/call-proposals/{CALL_ID}.json
orchestrator_call_decision: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/authorization-decisions/{CALL_ID}.json
dispatch_admission: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/dispatch-admissions/{CALL_ID}.json
acceptance_result: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/ACCEPTANCE_RESULT.json
acceptance_evidence_manifest: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/EVIDENCE_MANIFEST.json
orchestrator_identity: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_IDENTITY.json
orchestrator_launch_intent: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_LAUNCH_INTENT.json
orchestrator_key_release: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_KEY_RELEASE.json
orchestrator_heartbeats: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_HEARTBEATS.jsonl
orchestrator_exit: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_EXIT.json
observer_support_source: .codex/scripts/c3_outer_support.py
observer_helper_source: .codex/scripts/c3_watcher_helper.py
observer_support_smoke: .codex/scripts/run_c3_outer_support_smoke.py
watcher_helper_launch: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/WATCHER_HELPER_LAUNCH.json
watcher_observation_close: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/WATCHER_OBSERVATION_CLOSE.json
emergency_termination: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/EMERGENCY_TERMINATION.json
governing_input_watcher: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/GOVERNING_INPUT_WATCHER.json
acceptance_topology_shutdown: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/TOPOLOGY_SHUTDOWN.json
acceptance_manifest_exclusions: [EVIDENCE_MANIFEST.json, ACCEPTANCE_RESULT.json, topology/]
acceptance_attempt_policy: one greater than largest runtime/evidence number, or 0001 if none; both chosen paths absent; preserve one-sided/collision state; never clear, overwrite, gap-fill, or reuse
target_seed_manifest: TARGET_SEED_MANIFEST.json
target_seed_files: [TARGET_CHARTER.md, PINNED_INPUTS.json, TEST_CONTRACT.json, EVIDENCE_SCHEMA.json]
evaluator_enabled: false
stall_threshold: 3
scope_policy: backward-compatible firmware harness, MCP acceptance kit, four-board certification, and directly implicated coding regressions only
gap_scope: change
final_full_verification: true
final_full_verification_semantics: one logical SAFEGUARD_RUN_ID per exact product lock; governing changes use domain classification and preserve non-consuming gates; admission is outside run; environment interruption resumes incomplete/invalidated components
governing_invalidation_policy: record whole-document hashes, classify changed requirement IDs into project lock-input domains, invalidate only consuming gates; use conservative fallback only when unclassifiable
task_card_feature: S4 implements orchestrator-task-card/v1, deterministic entrypoint score, compact prompt, semantic-acceptance-pending event, and hash-bound orchestrator verdict before dependent dispatch
report_only_retry_feature: S4 permits exactly one same-thread report-only continuation after missing/malformed terminal artifact; no code/test edit, execution rerun, fabricated evidence, or second retry
logical_thread_lifetime_feature: S5 binds one thread to one logical task card; same-task continuation/report-only/strict-fast-lane routes remain before acceptance; accepted thread rejects unrelated reuse
terminal_lane_retirement_feature: S5 preserves evidence and revision before excluding accepted terminal lane from active discovery, safely closing clean unused worktree, retaining archive-only artifacts, and deleting disposable caches
readonly_source_allocation_feature: S5 supports exact immutable source view plus separate writable result root without linked worktree for static read-only lanes; mutation/source-local execution retains isolated writable source
event_log_lock_feature: S5 uses one cross-process lock per shared event log; writers wait, append and flush one complete record, release; concurrent-process regression required
protected_general_harness_unit_regressions: true
max_role_fanout: 2
max_agents_beside_ROOT_IM: 3
production_coder_pool: 1
reviewer_pool: 2
doer_pool: 2
green_test_policy: retain unless dependency fingerprint changes
review_completion_policy: complete assigned affected-surface sweep; never intentional first-finding stop
repair_batch_policy: triage complete finding/test result; repair all accepted items before next product review
production_finding_policy: supported or credibly reachable deployed trigger plus concrete negative consequence; latent safety/authorization/fail-closed defects included; cosmetic/unreachable/behavior-neutral/speculative issues excluded
pre_c0_policy: freeze joined tip; run shortest affected smoke; then overlap complete read-only C0 with remaining focused execution; join before C1
non_product_correction_policy: same-lane administrative resume; strict test-only fast lane requires fixture/setup-or-metadata-only diff, deterministic unchanged-oracle/assertion/contract checklist, and one exact failed-ID rerun before unrelated work, with no C0/ordinary review/reconciliation; expected-behavior/coverage/operative-contract/production/policy change is material
executor_recordability_policy: before an expensive custom inner-process-evidence selection, same-lane no-product/MCP/hardware preflight validates stable ID, exact inputs, process creation identity, timing, command, outputs, and exit; bind green evidence to runner/procedure/configuration/environment fingerprint and reuse until it changes; reconstructable procedure defects stay same-lane, irrecoverable raw identity evidence reruns only affected ID on same lock
fixture_batch_policy: after one selected run reports only classified fixture/mock/executor-environment defects, correct the complete test-only batch then rerun the selection once
c3_rehearsal_policy: before attempt/O/helper/target/MCP/hardware allocation, exact-C1/C2 host-only disposable-fake rehearsal proves admission, retained-session auth, identity binding, duplicate refusal, observer correlation, recovery/idempotence, cleanup, terminal closure; green required for physical admission, not physical credit
observer_finding_policy: complete assigned surface; pool ordinary findings; immediate stop only for exact unauthorized/wrong-resource, live-containment/cleanup, or irreversible-evidence-corruption condition
outer_support_failure_policy: correct in place when product outcome remains determinable; otherwise mark only affected work incomplete and roll support/attempt; preserve all immutable unaffected product credit; product repair requires exact product evidence
batch_reconciliation_policy: preserve raw lane evidence; reconcile dependencies, registry, and aggregate join once per accepted batch tip
hardware_interface: BYO Firmware MCP only
rf_frequency_intent_mhz: 915
destructive_recovery: excluded
acceptance_orchestrator: gpt-5.6-sol high priority
acceptance_target_launch_owner: C3-HARNESS only; F.C3.O submits assignments and never directly launches a target worker
acceptance_server_source_policy: immutable; AUTHORIZED_SERVER_LIMITATION requires exact attribution, strongest-safe partial/unit substitute, and explicit physical non-certification
coder: gpt-5.6-terra medium priority
reviewer_and_test_writer: gpt-5.6-terra medium priority
doer_and_test_executor: gpt-5.6-luna high priority
optional_watcher_reviewer: gpt-5.6-terra medium priority; zero or one; non-gating
model_substitution: forbidden
codex_approval_and_sandbox: dangerously-bypass-approvals-and-sandbox
codex_hook_trust: dangerously-bypass-hook-trust
codex_user_config: ignored
mcp_registration: explicit per lane
mcp_environment: allowlisted; no unreviewed .env or ambient probe/target route
historical_manifest_sources: provenance only; destination hashes required
ncs_python_cache: fresh per lane below runtime root
candidate_gate_root: reserved candidate worktree, never implicit stable-general-harness-runner
promotion_branch: progress/v1.2
external_publish: requires explicit live directive
```

The runner must validate this plan before execution. Configuration cannot weaken an atomic criterion, add a model substitution, expand hardware authority, reuse a prior acceptance runtime, or turn an extended qualification item into a release gate without an explicit plan revision.
