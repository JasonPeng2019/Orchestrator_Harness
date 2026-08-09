---
name: run-firmware-test-suite
description: Execute the MCP-Trial-3 fresh firmware experiment program end to end with every dependency-ready persistent doer lane running concurrently under the validated read-only orchestrator_harness, isolated resource-leased test phases, gpt-5.6-luna test agents at high reasoning on the regular/default non-Fast service tier, one designated Claude Sonnet 5 A23 doer, gpt-5.6-terra server-repair coder/doers and reviewers at high reasoning on the priority/Fast service tier, main-model evidence review, and serialized change-loop repair of verified BYO-Firmware-MCP defects. Use when asked to run, resume, parallelize, deduplicate, automate, or drive the fresh STM32L476/nRF52840 hardware tests until green, including firmware creation, HIL validation, failure triage, and server-fix/retest cycles.
---

# Run Firmware Test Suite

Run this from the `MCP-Trial-3` root. Treat
`BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` as the catalog and
`BYO-Firmware-MCP` as the server under test.

## Load before acting

1. Read `HANDOFF.md` and `PLAN.md` when present.
2. Read the selected test section in the catalog.
3. Read `.codex/design_charter.md`.
4. Read [execution-contract.md](references/execution-contract.md).
5. Read [result-contract.md](references/result-contract.md) before reviewing a result.
6. Read [model-continuity-contract.md](references/model-continuity-contract.md).
7. Read `.agent-workspace/SUITE_COORDINATION.md` and
   `.agent-workspace/SERVER_REPAIR_QUEUE.md` when either exists.
8. Read and hash-check `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.md` against its `.sha256`
   sidecar when present.
9. Read `.agent-workspace/AUTONOMY_REQUIREMENT_MATRIX.md` and verify that the selected test has an
   autonomous oracle and no unresolved operator/external-equipment dependency.
10. Run
   `python .codex/skills/run-firmware-test-suite/scripts/audit_autonomy.py`
   before every doer/reviewer launch or resume and after any catalog/skill/spec-amendment change.
   Do not launch on failure.
11. Read `orchestrator_harness/README.md`, the active harness config, and any durable harness
    handoff/state before launching or resuming parallel roles. Reconcile recorded PIDs against
    process identity and creation time; never trust a stale raw `running` declaration.
12. Load firmware MCP help/setup skills before live MCP use. Loading guidance never authorizes a
    hardware action.

## Zero-operator execution contract

Translate the selected catalog case into an executable spec without making it stricter. A
prerequisite or evidence item is a hard gate only when the catalog explicitly requires it, the live
server requests it to continue, it is necessary to distinguish pass from fail, or it is necessary
for electrical/RF/destructive/target-identity safety.

The main suite is autonomous after launch. Never make a main-catalog phase wait for another user
message or for a human to touch, inspect, identify, move, rewire, relabel, reposition, power-cycle,
or observe hardware. In particular, never require a photograph, visible marking, printed PCB
revision, PCA number, removable label, cable move, button press, jumper/solder change, DMM, logic
analyzer, BLE sniffer, camera, oscilloscope, external power instrument, or operator-timed event.
The connected four-board fixture, its declared CoreSX1262 wiring, the recorded delegated
authorization, and stable electronic identities are supplied inputs, not facts a doer must
physically re-prove.

Use electronic/software-controlled equivalents: server disconnect/reconnect/reset, process-scoped
provider interruption, firmware-controlled advertising/RF disable, host-side enumeration evidence,
UART/peer counters, debug state, artifact hashes, and existing correlated evidence. One truthful
source is enough; never require duplicate evidence modalities. Preserve electrical, RF,
destructive-action, and target-identity safety, but satisfy those boundaries from the declared
fixture and live server plans rather than inventing operator work.

`NEEDS_USER` and `INFRA_BLOCKED` are not permitted terminal outcomes for main-catalog runs. The
manager autonomously repairs routine tooling, launcher, USB, network/cache, SDK, and server
infrastructure; applies recorded delegated authorization after reviewing each exact live plan; or
issues a signed spec correction that replaces an unnecessary physical/external prerequisite with
an equivalent autonomous oracle. A temporarily unavailable resource is recorded only as
`WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` in `SUITE_COORDINATION.md`; it never creates
`RESULT.json`, never asks the user to intervene, and never stops unrelated lanes. If a branch is
intrinsically impossible without new human action or special equipment, move only that branch to
non-gating Appendix A and record `SKIPPED_AUTONOMY_REQUIRED`; never leave it as a main-suite gate.
Preserve already valid evidence and resume the same doer without repeating unrelated work.

## Authorized-use prompt clarity

Begin every new or resumed test-agent, reviewer, and server-repair prompt with an accurate,
plain-language scope statement:

> Authorized local firmware validation. Targets are limited to the named local workspace and the
> user-owned development boards explicitly assigned by the test. Follow every declared hardware
> plan and permission gate. No remote or third-party target is in scope.

Adapt the statement truthfully when a test is host-only or has no board assigned. Use precise
firmware and validation language. Do not introduce terms such as `attack`, `exploit`, `malware`,
`credential theft`, or `bypass` unless the exact catalog requirement, observed evidence, or
production defect makes that term technically necessary. Never hide, fragment, euphemize, or omit
material technical details to evade a safety system; this rule adds legitimate-use context and
removes gratuitous cyber framing without weakening the test.

If a platform cyber-safety notice, reroute, or refusal occurs, preserve the exact notice and
request context, checkpoint the exact session, and continue unrelated lanes. Resume the recorded
session when possible; this is not a main-run terminal status. Do not silently change models or
test scope to work around it.

## Subagent approvals and sandbox

- Every Codex and Claude doer/reviewer launch or resume must compose its task prompt through
  `scripts/orchestration/prompt_policy.py`. The helper verifies
  `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.sha256`, prepends and appends the authoritative
  policy, and records its SHA-256 in controller status. Refuse the launch if composition or hash
  verification fails. Never invoke an older direct prompt/launcher that lacks this binding;
  historical launcher artifacts remain evidence only.
- Every **new or resumed** Codex suite role must be launched with
  `--dangerously-bypass-approvals-and-sandbox --ignore-user-config -c approval_policy="never" -c approvals_reviewer="user"`.
  This is an explicit launcher contract, not an inherited parent setting: fail the launch before
  starting a session if any component is absent. The first flag supplies no sandbox/no approval;
  the explicit policy and reviewer settings make the no-approval/no-auto-review intent
  unambiguous under all ordinary config layers. Do not set `approvals_reviewer="auto_review"`,
  `-a on-request`, or `-s workspace-write`. Record `sandbox="danger-full-access"`,
  `approval_policy="never"`, and the actual launcher value `approvals_reviewer="user"` in the controller status.
- Apply the provider-equivalent unrestricted/no-command-approval configuration to every Claude
  role. Preserve the exact provider setting in its controller status. Do not rely on the parent
  conversation or IDE configuration being inherited by an external launcher.
- The explicit `subagent exec` configuration and deterministic autonomy audit enforce this
  contract. Historical direct launcher wrappers were deleted during repository cleanup; do not
  recreate or reuse them.
- Unrestricted Codex command execution is **not** hardware authorization. Flash, erase, unlock,
  protection, recovery, RF, and power-fault actions still require the live firmware-server plan
  and the recorded delegated hardware authorization in this skill.

## Non-negotiable role split

- Treat Codex **Fast mode** as `service_tier="priority"`, independently of model and reasoning
  effort. Pass it on every new **and resumed** Terra role. Do not invent a `-fast` model slug.
- Run every Codex catalog/test-lane agent turn with `gpt-5.6-luna`,
  `reasoning_effort="high"`, and the explicit non-Fast tier `service_tier="default"`. This
  includes Luna turns that author fresh firmware application code; Luna roles must never use
  Fast/priority.
- A23 is the sole provider exception: run its one persistent doer on **Claude Sonnet 5** through a
  persistent unrestricted/no-command-approval launcher. Record the exact provider model identifier,
  launcher, session identity, and settings. Do not claim Codex `service_tier` or reasoning
  settings for Claude. After one bounded retry window, a genuine Claude-provider outage may not
  block the suite: record it and transparently continue A23 with the persistent `gpt-5.6-luna` fallback
  at high reasoning and the regular/default tier. This loses the provider-comparison datapoint but not the
  firmware/server test; never substitute silently.
- Run every `gpt-5.6-terra` server-repair coder/doer, reviewer, spec-tester, and
  regression-tester turn with `reasoning_effort="high"` and
  `service_tier="priority"` (Fast mode). No Terra role in this suite runs on the default tier.
- The **main model** specifies, schedules, reviews evidence, and invokes `$change-loop` for a
  verified production-code server defect. It does not implement fresh firmware or perform the test
  in place of the test agent.
- Assign each roster-owned catalog test except A23 to its named persistent lane doer from
  [the doer roster](references/doer-roster.md). Create that doer through `subagent exec` (not the
  regular internal subagent tool) only for its first assigned task; resume the same session for
  later assigned tasks, with:
  - `fork_turns="none"`
  - `model="gpt-5.6-luna"`
  - `reasoning_effort="high"`
  - `service_tier="default"`
- Start A23 once with the designated persistent Claude Sonnet 5 launcher and no inherited parent
  conversation. Q40 is a manager-owned corpus aggregation; it does not create another base
  application or ordinary catalog test agent. It may open only missing, nonduplicated seeded
  branches by assigning each branch to one currently idle Atlas, Boreal, Cygnus, or Delta session.
  Do not create branch-specific doers or reuse Nova.
- Keep every named doer session persistent through its assigned tasks, routine firmware iteration,
  and server repair/retest. Resume it instead of opening disposable same-model sessions.
  Replacement is allowed only for a
  necessary model change or an irrecoverable session, with the old/new identity, reason, verified
  evidence boundary, and remaining work recorded under the
  [model continuity contract](references/model-continuity-contract.md). Never replace it merely
  because a test is red or slow.
- Resume an existing `gpt-5.4` doer as `gpt-5.6-luna` at high/default without restarting or
  retesting completed work. Do not otherwise restart an in-progress test merely to adopt the new
  model or the A23 Claude exception.
- After sealing and before assigning/resuming the doer for that task, invoke one **persistent adversarial reviewer**
  through `subagent exec` with `fork_turns="none"`, `model="gpt-5.6-terra"`, and
  `reasoning_effort="high"`, and `service_tier="priority"`. It first reviews the sealed spec;
  resume that exact reviewer with the same settings after a `PASS` claim for the evidence review.
  It is separate from the persistent test agent and is read-only: it never operates hardware or
  edits either firmware or server code, and must not open `BYO-Firmware-MCP`.
- The test agent owns all fresh application code, builds, instrumentation, HIL actions, firmware
  diagnosis, and test evidence. It must not read or edit `BYO-Firmware-MCP`, invoke or read
  `$change-loop`/`$plan-changes`, or propose a server repair workflow.
- A doer name identifies one persistent doing-subagent session, not a task. If the manager opens
  `N` concurrent execution lanes, it uses exactly `N` named doers. Each task is assigned to one
  doer, and each doer runs at most one task at a time. Record the doer name separately from its
  provider agent/session ID. Do not retroactively name completed/bootstrap task agents.
  Reviewers and server-repair coder/doer roles are not named firmware test-lane doers.
- The main model is the only suite manager. It may run at most one active task in each of
  the five named doer lanes, and only when dependencies and all required leases—including the
  isolated workspace plus doer/provider/launcher execution slots—allow it. Never run two
  managers/controllers for the same suite, two active
  doers for the same task, two live sessions under one doer name, or two repair loops against the
  same runtime.
- On every scheduling pass, launch or resume **all** eligible named doer lanes concurrently. Do
  not finish one doer's portfolio before starting another, and do not leave an eligible lane idle
  merely because a different test, provider, board, or fixture is waiting. A waiting task stops
  only its dependency descendants and conflicting leases. An idle doer may advance to its earliest
  unrelated dependency-ready roster task only after its current task is terminal or at a
  manager-recorded safe handoff.
- Compute eligibility per task phase from only its explicit prerequisites, current server-repair
  state, and required resource leases, including its isolated workspace and
  doer/provider/launcher execution slots. A dependency-wave row, row number, row completion, or unfinished task
  in another lane is never itself a prerequisite. Start an eligible phase from any row immediately;
  do not wait for the current or an earlier row to finish. After every launch, completion,
  checkpoint, failure, lease change, or provider wait, rescan every lane and fill all newly eligible
  work. Use catalog section 11.1 as the authoritative cross-test edge list. A sealed spec may split
  one listed edge into finer consumed-artifact phases, but it must not invent an unlisted
  whole-test, whole-row, or unrelated-lane dependency. Unexpectedly idle, usable hardware requires
  an immediate scheduling audit.
- Schedule resources, not fixed STM/nRF/host lanes. The board tokens are `STM-A`, `STM-B`, `NRF-A`,
  and `NRF-B`. Also lease each doer/provider/launcher execution slot, isolated workspace, probe,
  serial endpoint, peer/radio, autonomous electronic control, USB-enumeration or power-disruption
  scope actually affected, mutable artifact/cache root, and server process/state/lifecycle scope.
  Board-free spec, build, and evidence-review phases may overlap hardware work when their host
  resources are isolated.

## Non-negotiable test gate

- Every main-catalog-required behavior remains a hard release gate. Appendix A, an optional
  recommendation, or an accidentally invented spec prerequisite is not a release gate. A real
  failure blocks that test, its dependency
  descendants, and conflicting resource leases, but does not cancel an unrelated already-eligible
  phase.
- A claimed server failure does not immediately freeze the suite. The main model first validates
  it. If it is not a production server defect, reject the claim and resume the same test agent.
- A verified production server defect starts a selective repair barrier: stop launching new
  server-consuming or HIL phases, request bounded safe checkpoints from active server/HIL
  consumers, and repair queued defects serially through `$change-loop`. Pure spec, isolated
  firmware build, and read-only evidence-review phases may continue only if they neither invoke nor
  depend on the live server or leased hardware.
- After repair, bind every subsequent server-consuming phase to the same recorded repaired
  snapshot, restart the affected MCP processes, and target-retest each affected
  reproducer/requirement. Do not mark the failed test or any dependent release gate green until the
  exact failure passes. Intentional negative/refusal cases pass only when the observed refusal
  matches their specification.

### Incremental retest and bounded-review policy

- Treat every verified PASS as durable evidence bound to its exact spec, source/artifact/server
  snapshot, fixture identity, and relevant leases. A later failure or criticism invalidates only
  the evidence it actually contradicts or whose covered inputs changed.
- After any test, adversarial, or repair failure, rerun the failed check, the directly affected
  requirements, and the smallest regression surface reached by the change. Never restart the whole
  suite, every lane, an expensive application campaign, a soak, or already evidenced branches from
  scratch merely because one check failed.
- Continue unrelated eligible lanes and preserve their evidence. Restart an MCP process only when
  it consumed changed server code; resume a firmware/HIL phase only when its snapshot or required
  evidence was invalidated.
- Give each adversarial reviewer one bounded pass per artifact stage plus one targeted follow-up for
  rejected evidence. Reviewers must distinguish **ACTIONABLE** functional findings from
  **ADVISORY** hardening. Actionable means an evidenced main-catalog requirement violation,
  credible safety/data-loss/identity risk, reproducible failure, or likely hang/orchestration
  collapse. Style, speculative robustness, vanishingly unlikely cases without evidence, unrelated
  features, and disproportionate complexity are advisory.
- The main manager records advisory findings but does not block delivery or expand scope for them.
  Once actionable findings are resolved and objective gates are green, stop reviewing and deliver;
  do not seek another verdict or pursue a perfect product.

## Harness-assisted parallel coordination

The validated `orchestrator_harness` is required whenever two or more suite roles may overlap,
and for every HIL/server-consuming scheduling epoch even when only one lane is initially ready.
It is a read-only reconciler and notification path, not a coordinator or authority. The current
high-level session remains the sole suite manager. A separate supervisory agent is not part of
normal suite execution; the root-supervisor/Sol-manager arrangement used for harness acceptance
was a validation fixture only.

Create one suite-epoch config from `orchestrator_harness/config.example.json`. Its `run_globs`
must list every run root the epoch may activate, its output directory must be a unique directory
under `multi-agent-logs/orchestrator-harness/<epoch>/` and outside all observed run roots, and its manager review,
no-progress, and heartbeat intervals must be explicit. Use the validated defaults of 300, 600,
and 420 seconds unless a bounded acceptance run intentionally uses shorter values; heartbeat
timeout must remain greater than the review interval. Never reuse
a prior epoch's config, output state, requests, relays, PIDs, or notification records as a live
suite configuration.

Start exactly one managed watcher for the config:

```powershell
python -m orchestrator_harness --config <suite-harness-config> watch --managed
```

Attach its stdout/stderr to durable manager-owned logs or a yielded foreground process cell.
Record watcher PID, owner PID, both creation times, config hash, output paths, and lifecycle state
in `multi-agent-logs/orchestrator-harness/<epoch>/ROLE_REGISTRY.json`. The manager also keeps:

- `.agent-workspace/SUITE_COORDINATION.md`: manager identity, optional informational eligibility
  group (never an advancement gate), server snapshot, catalog test, stable doer name, provider
  agent/session and reviewer identities, run directory, phase, dependencies, leased resources,
  and state.
- `.agent-workspace/SERVER_REPAIR_QUEUE.md`: validated defect ID, reporting run, server snapshot,
  reproducer, evidence, affected phases/tests, disposition, and repair/retest state.
- `multi-agent-logs/orchestrator-harness/<epoch>/MANAGER_LOG.jsonl`: every launch, notification, review,
  relay decision, acknowledgement, heartbeat, checkpoint, recovery, and exact cleanup result.
- `multi-agent-logs/orchestrator-harness/<epoch>/MONITOR_LOG.jsonl`: periodic whole-suite observations and
  any diagnosed inefficient, redundant, looping, or stalled behavior.

Before an agent begins or resumes HIL, the manager also writes that run's
`.agent-workspace/RESOURCE_ASSIGNMENT.md` with the catalog/shard ID, phase, server snapshot,
canonical doer name, leased resources, assignment time, and manager identity. The agent may read
but never edit it. When the phase can reach a permission-bearing live plan, include the applicable
delegated-authorization artifact path and SHA-256; without that binding the agent may not infer a
grant.

Use these rules:

**Required managed scheduling epoch.** Execute exactly:
`reconcile -> start/recover one managed watcher -> launch every eligible lane -> consume one
durable actionable notification -> inspect the named lane and compact whole-suite state -> serial
exact review/action -> ack the exact event ID -> rescan every lane and lease -> fill newly eligible
work -> heartbeat/checkpoint -> repeat`. The same watcher self-arms after exact acknowledgement;
do not relaunch it after every event.

Read the watcher output and inspect every live doer at least once per manager-review interval and
normally every two to three minutes during active HIL. Use
`python -m orchestrator_harness --config <suite-harness-config> heartbeat` before the recorded
heartbeat lease expires during a long review. A pending notification is durable and must be
redelivered after a watcher restart until this succeeds:

```powershell
python -m orchestrator_harness --config <suite-harness-config> ack --event-id <exact-event-id>
```

Never acknowledge before reviewing the exact event and relevant doer output. `RELAY_READY`
requires a request-SHA-256- and live-lifetime-bound manager decision. The watcher only reports
facts. The manager alone writes relays, changes leases, recovers a lane, classifies a failure, or
starts a serialized server repair. Doers remain alive through bounded helper gates; only a genuine
checkpoint, provider/lease wait, or completed slice ends their turn. Use explicit controller
states `RUNNING_CODEX`, `CODEX_EXITED`, `CONTROLLER_INTERRUPTED`, `LAUNCH_FAILED`, and
`CONTROLLER_FAILED`; never call a lane generically "running". A watcher `STALE_STATUS` overrides a
contradictory raw declaration.

Every current controller status must carry the exact doer/task/session facts from which its lane
is derived. Every request, helper, and MCP record format that supports explicit scoping must carry
the manager-assigned `declared_lane_id`. That explicit lane is authoritative even when a persistent
session ID was reused by an older task; session identity is only a fallback when no explicit lane
exists. On watcher bootstrap, historical helper/MCP exits and old
checkpoint/result availability are baseline facts, not a queue of current manager work. Only a
new lifecycle transition is actionable, while persistent live request, conflict, provider,
process-safety, and manager-signal conditions remain actionable. Historical checkpoint body text
must never create a current provider wait.

0. **Fill every eligible lane.** Evaluate Atlas, Boreal, Cygnus, Delta, and Nova on each manager
   pass and launch/resume all dependency-ready, non-conflicting phases in the same scheduling
   batch. Continue unrelated lanes while another waits. Treat dependency-wave rows only as visual
   scheduling hints: never wait for a row, every task in a row, or every earlier row to finish.
   Start work from any row as soon as that phase's explicit prerequisites and leases are satisfied.
   Repeat this evaluation after every task-state, provider-state, repair-state, or lease transition.
1. **One manager.** On every start/resume, read the coordination ledger. Record this manager as
   authoritative before launches. If another live controller owns the same suite/test/runtime,
   do not launch duplicates; reconcile or stop the duplicate first.
2. **One immutable server snapshot.** Record the server HEAD plus dirty-diff/tree fingerprint
   assigned to every server-consuming phase. Do not silently let concurrent server consumers run
   different revisions.
3. **Explicit phase leases.** Before each phase, the manager records its doer/provider/launcher
    execution slot, isolated workspace, board tokens, probes, serial endpoints, radio/peer,
    autonomous electronic controls actually used, USB/power scope actually affected,
    mutable cache/artifact roots, server process/state root, and disruptive host action. An absent
    external instrument is never requested, leased, or treated as a prerequisite. No overlapping
    exclusive lease is allowed. Each
   HIL run gets its own MCP process and state/artifact root unless the test explicitly evaluates a
   shared process. An agent never self-assigns a board or advances into HIL without a manager-written
   assignment. When `codex exec` inherits a configured `byo-firmware` MCP, pass per-process
   `mcp_servers.byo-firmware.cwd` and
   `mcp_servers.byo-firmware.env.BYO_MCP_ARTIFACT_ROOT` overrides from that assignment; a prompt
   alone does not change the configured server's cwd. Verify the first public artifact/event path
   is under the assigned root before continuing HIL.
4. **Dependency and phase scheduling.** Track `SPEC_READY`, `BUILDING`,
   `BUILT_WAITING_FOR_LEASE`, `HIL_RUNNING`, `CHECKPOINTED`, and `PASS_CLAIMED` separately from the
   terminal run status. A build may start when its build prerequisites and host leases are ready;
   HIL may start only when its HIL prerequisites, server snapshot, and hardware leases are ready.
   Count only a declared consumed result/evidence edge, the selective server-repair state, or an
   actually conflicting exclusive lease as a blocker. Do not infer a dependency from table
   position, wave membership, numeric test order, another lane's unfinished state, or a prose
   wave-exit summary. Later-row work may run before earlier-row work. When a phase releases or
   cannot use a resource, immediately offer that resource to every other eligible lane rather than
   leaving it idle.
   Use an exclusive barrier for all-board routing, global USB/power disruption, shared server
   lifecycle, or any phase whose isolation cannot be proven.
5. **Bounded checkpoints.** Every spec names safe boundaries and a maximum pause latency. Between
   numbered requirements and between bounded soak epochs, the test agent checks for
   `.agent-workspace/PAUSE_REQUESTED.md`. It never interrupts flash/erase or another atomic hardware
   mutation mid-operation; it waits for the declared finite bound, flushes evidence, records live
   state and cleanup, writes `.agent-workspace/PARALLEL_CHECKPOINT.md`, and returns without writing
   a terminal `RESULT.json`. This coordination pause is not a terminal test status.
6. **Event-driven waiting.** After requesting pauses, yield to agent/process completion,
   managed-watcher notifications, or an ordinary shell/process wait. Do not spend model turns
   repeatedly polling. A yielded watcher process cell or durable notification log is the preferred
   wake-up path. The manager still performs a bounded two-to-three-minute supervision pass while
   HIL is active so a broken role, missing notification, or inefficient loop is caught promptly.
7. **Resume, do not replace.** After the manager removes the pause request and records the new
   server snapshot and phase assignment, resume the exact persistent agent from
   `PARALLEL_CHECKPOINT.md`. Retest only work reached by the server change; preserve unrelated
   verified evidence.
8. **MCP ownership and cleanup.** For every HIL boundary, record exact controller, Codex, helper,
   MCP-parent, and provider-worker PID identities and creation times; use a unique project/state/
   artifact/log root and prove the first public artifact/event is within it. Clean only exact
   descendants created by that boundary; never use a broad command-line substring.
9. **A24 no-flash diagnostic and acceptance batch.** Before A24 RF work, use fresh roots to prove
   NRF-A probe ownership, validate NRF-A alone while recording spawn/ready/open/termination timing,
   clean exact descendants and prove absence, then repeat NRF-B. Attempt paired startup only after
   both singles pass; compare each latency to five seconds and repeat the minimum case enough to
   classify deterministic failure versus variance. Do not flash or edit the server for this
   diagnosis. Then launch the clean A22/STM-A, D31/STM-B, A24 one-nRF-at-a-time canary, and eligible
   board-free A26 batch in the same manager epoch.
10. **One assigned doer across internal shards.** A catalog item may define independent board/family shards
   solely to unlock real resource parallelism, but they remain phases of one task under its one
   named doer. Give each shard immutable scope, an isolated application/build tree, and unique
   leases. The doer may orchestrate concurrent processes for disjoint shards but may not delegate
   one to another doing subagent. The manager records one aggregate catalog verdict. Sharding does
   not duplicate a branch, relax an oracle, or turn a catalog item into optional work.
11. **Harness recovery is selective.** If an observed inefficiency, false conflict, stale
    notification, or cross-lane attachment may be a harness defect, diagnose it without
    interrupting roles. Once confirmed, stop new launches, request bounded checkpoints only from
    live affected roles, stop the exact watcher/controller and exact affected descendants, and
    preserve every completed result. Fix the harness locally, run only focused harness tests plus
    its ordinary host suite, restart one watcher against the same run set, and resume only
    incomplete work. Never restart the whole suite or already-passed lanes for a watcher repair.
12. **Harness shutdown is bounded.** Before ending an active manager epoch, either renew the
    heartbeat and durably hand off ownership, or request cooperative shutdown with
    `python -m orchestrator_harness --config <suite-harness-config> watch stop`. Confirm the exact
    watcher/controller identities are absent and record `pending` state. Do not kill by broad
    command-line match. If the manager disappears, heartbeat expiry is the expected fail-closed
    cleanup path; on resumption, reconcile first and restart once so any pending event is
    redelivered.

The manager may prepare/seal future specs and run their read-only spec reviews while hardware
phases execute. It may also start isolated board-free build phases as soon as their build
dependencies are ready; those agents must stop at `BUILT_WAITING_FOR_LEASE` until their HIL
dependencies and manager-assigned hardware leases are valid.

## Quick start

List catalog tests:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py list
```

Create one isolated run:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py create A20
```

Fill every `[REQUIRED]` field in the generated `.agent-workspace/SPEC.md`, then seal it:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py seal <run-dir>
```

The scaffold reads canonical shared inputs from the task-owned asset directories listed below and
copies only these
baseline target documents into the run root using their legacy run-local names:

- `stm32L476rgt.pdf`
- `Nano_BLE_MCU-nRF52840_PS_v1.1.pdf`

Everything else initially lives under `.agent-workspace/`. Never copy the master plan, server
source, prior runs, firmware examples, SDK projects, packs, profiles, or build outputs. For A24
and A25, the manager may additionally supply hashed copies of
`60852689.DS_SX1261_2 V2-2.pdf`, `waveshare-lora-module.pdf`, and
`nrf-sx-pin-mappings.md`; the actual attached radios are Waveshare CoreSX1262 modules, not
SX1276.

Use the canonical sources at
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/sx1261-sx1262-v2.2.pdf`,
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/waveshare-lora-module.pdf`, and
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/board-mappings/nrf-sx1262-pin-mappings.md`,
retaining those legacy run-local names. The canonical STM32 and nRF baseline datasheets are owned
by `fresh-experiments/S10_20260726-034312/.agent-workspace/assets/datasheets/` and
`fresh-experiments/S11_20260726-034313/.agent-workspace/assets/datasheets/`, respectively.

## Per-test loop

1. **Create and specify.** Scaffold a new directory, write objective requirements, exact hardware
   facts material to the case,
   observable pass/fail oracles, allowed destructive scope, and evidence requirements in
   `SPEC.md`. Use official current sources to record:
   - NUCLEO-L476RG MCU: `STM32L476RGT6`
   - nRF52840 DK application MCU/package: `nRF52840-QIAA`
   Use the recorded correlated electronic/official source for the MCU/package input. Do not ask for
   a physical board revision/marking, `PCA10056`, printed PCB revision, board photo, direct visual
   inspection, or another operator statement. If a real electronic contradiction could change
   target selection or safety, fail closed on that action and use the manager-supplied fixture
   record or an autonomous server/electronic check to resolve it.
   Also record the canonical doer name, build and HIL prerequisites separately, internal
   catalog-defined shards, phase-specific resource leases, disruptive/global scopes, safe
   checkpoint boundaries, and maximum pause latency.
2. **Seal.** Run `fresh_test.py seal`. Do not change the spec after the agent starts; create a
   signed amendment in `.agent-workspace/SPEC_AMENDMENTS.md` only to correct a genuine spec error.
3. **Review the sealed spec once.** Start one persistent read-only reviewer through `subagent exec`
   with `fork_turns="none"`, `model="gpt-5.6-terra"`, `reasoning_effort="high"`, and
   `service_tier="priority"`. Give it the absolute run path and
   `.agent-workspace/REVIEWER_PROMPT.md`; it writes
   `.agent-workspace/SPEC_ADVERSARIAL_REVIEW.md` without operating hardware or inspecting the
   server. Persist its identity:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-reviewer <run-dir> `
     --reviewer-id <agent-id> --task-name <canonical-task-name> --model gpt-5.6-terra
   ```

   The reviewer labels findings `ACTIONABLE` or `ADVISORY` under the policy above. The main model
   records the one review after addressing any genuine spec error with a signed
   `SPEC_AMENDMENTS.md` entry and declines advisory scope growth. Do not launch a spec-review loop:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py approve-spec <run-dir> `
     --note "Sealed requirements and any recorded amendment are executable and falsifiable."
   ```
4. **Invoke the assigned doer.** For an ordinary lane doer's first task, create it through
   `subagent exec` with `fork_turns="none"`, `model="gpt-5.6-luna"`,
   `reasoning_effort="high"`, and `service_tier="default"`; for every later assigned task, resume
   that same persistent session with the same settings. Do not use the regular internal subagent
   tool. For A23, use Nova's
   recorded persistent Claude Sonnet 5 launcher. Put the absolute run path and generated
   `TEST_AGENT_PROMPT.md` in the task message. Require all tool workdirs to be the run directory
   and the first command to print/verify the current path. Explicitly forbid `$change-loop` and
   `$plan-changes`; they are unavailable to the fresh-experiment test agent. Immediately persist
   the returned identity:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-agent <run-dir> `
     --agent-id <agent-id> --task-name <canonical-task-name> `
     --model <gpt-5.6-luna-or-claude-sonnet-5>
   ```
5. **Let the agent converge, wait for a lease, or checkpoint.** Do not pull routine firmware failures back to the main model. The
   agent keeps editing, building, flashing through live plan/permission gates, observing, and
   retesting until it emits a terminal result. If its build completes before HIL is eligible, it
   records the immutable build handoff and returns at `BUILT_WAITING_FOR_LEASE`. During a repair
   barrier, a server/HIL consumer may instead return at the requested safe checkpoint without
   changing `RUN_STATE.json` to a terminal status.
6. **Validate the claim.** Run:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py verify <run-dir>
   ```

7. **Adversarial evidence review.** For every `PASS` claim that passed structural validation,
   resume the recorded sealed-spec reviewer through `subagent exec`; do not create a new reviewer.
   Give it the absolute run directory containing `SPEC.md`, `SPEC_AMENDMENTS.md` if present,
   `RESULT.json`, `TEST_REPORT.md`, and all evidence paths. It must independently reassess the
   evidence without deferring to its earlier spec approval. It must not open or
   read anything under `BYO-Firmware-MCP`, including server source, tests, documentation, runtime
   state, or Git history. It must not operate hardware, invoke destructive tools, alter the run, or
   edit the server. Require it to write
   `.agent-workspace/ADVERSARIAL_REVIEW.md` and report numbered criticisms. Each criticism must
   name the supporting evidence, the expected observable server behavior, why the observed behavior
   indicates a server defect rather than an agent/fixture issue, and a minimal observable
   regression and label itself `ACTIONABLE` or `ADVISORY`. It must explicitly report
   `NO_ACTIONABLE_SERVER_ISSUES` when it finds none. An
   inability to complete the workflow from the available MCP guidance/evidence is itself a
   communication or product-surface criticism, not permission to inspect the server.
8. **Judge the criticisms.** Independently compare the spec, diffs, exact build commands,
   artifacts, MCP evidence, applicable identity/behavioral oracles, final state, and each
   adversarial criticism. An
   agent's prose is not proof.
   - Reject criticisms not supported by the evidence or attributable to firmware, fixture, SDK,
     test-spec, or agent mistakes. Record the rationale in the main review note.
   - Record but do not fix or gate on advisory perfection/hardening findings. Do not add product
     complexity whose cost is disproportionate to the evidenced risk.
   - For every validated **production-code** server defect, record the criticism, evidence paths,
     accepted scope, and rejected criticisms/rationale in the server change request, then use the
     server repair loop.
   - Do not mark the run green while an actionable criticism is unresolved. Conversely, do not keep
     the review loop open after actionable findings are resolved and the objective gates pass.
9. **Record the verdict.** Only when no actionable criticism remains, record a successful
   independent review:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py review <run-dir> `
     --verdict GREEN --note "All numbered requirements independently evidenced."
   ```

   Use `--verdict REJECTED` when proof is inadequate, then request only the missing/invalidated
   proof from the recorded agent session (or its formally recorded necessary replacement). Resume
   the reviewer once for that targeted evidence; it must not reopen already accepted requirements
   unless the new change directly invalidated them. For a sharded task, record the
   catalog ID green in `SUITE_COORDINATION.md` only after its one named doer has completed every
   required shard and the manager has checked the aggregate coverage map.
10. **Request missing proof.** If a claimed pass is incomplete or a claimed server defect is not
    isolated, resume the recorded agent through its recorded provider launcher with the precise
    missing checks.
    Use the model-change/session-recovery handoff only when its necessity criteria are met; do not
    create a disposable same-model session for an ordinary follow-up.
11. **Handle run status:**
   - `PASS`: mark green only after main-model review passes.
   - `SERVER_FAILURE`: verify it is reproducible and belongs to production server code rather than
     firmware, wiring, SDK, host, documentation, metadata, test specification, or misunderstanding.
     Queue and start a repair barrier only for the production-code case.
    - Reject `NEEDS_USER` or `INFRA_BLOCKED` from a main-catalog doer. Do not relay a user request.
      Apply delegated authorization, repair the environment, substitute an autonomous equivalent,
      or append a signed correction. If a resource is temporarily absent, checkpoint the exact
      session and record `WAITING_FOR_RESOURCE`/`WAITING_FOR_PROVIDER` only in the suite ledger
      while all unrelated lanes continue. If the action intrinsically needs human manipulation or
      unavailable special equipment, reclassify only that action into Appendix A and record
      `SKIPPED_AUTONOMY_REQUIRED`.
12. **Advance eligible phases.** Assign a dependency-ready catalog task to its roster doer and
    resume that persistent session when it is idle and the phase leases do not conflict. A doer
    may take its next assigned task only after its current task is terminal or at a manager-recorded
    handoff. Internal shards stay inside that doer's session; never launch another doing subagent
    for them. During a repair barrier, do not start server-consuming or HIL work; isolated
    board-free spec/build/review work may proceed under the selective-freeze rules.

## Server repair loop

Only the main model may initiate this loop, and only for a reviewed `SERVER_FAILURE` proven to
require a production-code change in `BYO-Firmware-MCP`. Do not use it for fresh-experiment work,
firmware/fixture/SDK failures, missing evidence, documentation-only or metadata-only issues, or
test-spec corrections.

Before entering the loop, the main model must:

1. add the independently validated defect to `SERVER_REPAIR_QUEUE.md`;
2. stop launching new server-consuming/HIL phases and write `PAUSE_REQUESTED.md` only in active
   runs that consume the server or hardware;
3. wait for those nonterminal consumers to return bounded `PARALLEL_CHECKPOINT.md`; a reporting
   agent that already returned a terminal result is already quiescent;
4. record those consumers `FROZEN` and verify no test/repair controller operates hardware or the
   server worktree; separately record any continuing board-free build/spec/review phase and prove
   that it does not invoke the server; and
5. order queued defects into small independent repair slices.

Treat `.codex/design_charter.md` as a live repair constraint. The main model rereads it before
specifying the repair, before authoring and validating the plan, before each distinct
implementation slice or feature, and before accepting the neutral tests and targeted HIL retest.
Every repair-role prompt requires that role to reread the charter at the same relevant boundaries
and to stop and report any conflict. A single read at suite startup is not sufficient for a server
edit.

Process queued repairs one at a time. Never run concurrent change-loops or production-code edits.
If a queued report is rejected during manager analysis, record the reason and resume its test
agent rather than manufacturing a repair.

The current main model must inspect `BYO-Firmware-MCP` and author the server-repair plan there
directly; it must not launch a planner agent. The doer, spec tester, and regression tester must all
use `gpt-5.6-terra` at high reasoning on `service_tier="priority"` and be launched with
`BYO-Firmware-MCP` as their workspace. Preserve the priority tier on every resume. The
fresh-experiment run remains
evidence-only input to the main model; it is never a change-loop role workspace.

1. Write the exact observed/expected behavior, minimal reproducer, evidence paths, affected
   server commit, and exclusions to
   `fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id>/request.md`. Never put
   experiment repair-control state in `BYO-Firmware-MCP`.
2. Use a unique runtime to prepare the request so an existing change-loop is not overwritten:

   ```bash
   cd BYO-Firmware-MCP
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     bash ../.codex/skills/plan-changes/scripts/plan.sh --prepare \
       ../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id>/request.md
   ```

   The current main model then reads the plan-authoring contract, inspects the server repository,
   writes the runtime's `plan.md` directly, and validates it:

   ```bash
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     bash ../.codex/skills/plan-changes/scripts/plan.sh --validate
   ```

   Never delegate this plan to a subagent, `codex exec` planner, doer, or tester.
3. Perform exactly one independent, read-only adversarial review of the main-authored plan using
   `gpt-5.6-terra`, `reasoning_effort="high"`, and `service_tier="priority"`. Record the reviewed
   plan SHA-256, reviewer identity, and numbered actionable risks/test targets plus nonblocking
   advisory notes in the runtime's `plan-review.md`. If execution proves a genuine plan mistake,
   record a minimal evidence-backed amendment and review only that amendment once; do not regenerate
   the whole plan or re-review unchanged items. The neutral tester gate and later evidence review
   are the correctness backstops.
4. Invoke `$change-loop` immediately:

   ```bash
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     DOER_MODEL=gpt-5.6-terra \
     SPEC_TESTER_MODEL=gpt-5.6-terra \
     REGRESSION_TESTER_MODEL=gpt-5.6-terra \
     CL_REASONING_EFFORT=high \
     CL_CODEX_FLAGS='--dangerously-bypass-approvals-and-sandbox --ignore-user-config --config approval_policy="never" --config approvals_reviewer="user" --config service_tier="priority"' \
     bash ../.codex/skills/change-loop/scripts/run_loop.sh
   ```

   Do not weaken or replace this full-access/no-approval configuration. Retain
   `--config service_tier="priority"` so every start and resume remains in Fast mode.

5. If either neutral spec or regression test fails, stop. The main model analyzes the failure and
   deploys/resumes the change-loop doer to fix the server; rerun the failed test and only
   regressions whose covered source/contracts changed. Retain the other gate's validated passing
   evidence through the change-loop pass cache. Accept server repair only when both gates have a
   current pass or validated unaffected-pass reuse. Do not commit.
6. Restart/reload an isolated MCP process for the reporting test so it does not exercise stale
   code. Keep every other server/HIL consumer frozen; board-free non-server phases may continue.
7. Resume only the **recorded reporting test-agent session** through its recorded provider
   launcher, identify only the new server commit/diff, and request a targeted retest: the minimal
   reproducer, every requirement and control directly touched by the accepted server change, and
   the relevant evidence capture. If a necessary model/session handoff was recorded, resume the
   replacement from the same durable evidence boundary. Do **not** rerun the whole expensive
   application test merely because the agent/model changed or unless the server change's scope
   reaches those requirements.
8. Record the queue item closed only after its targeted retest passes, then repeat serially until
   the queue is drained. Reload every checkpointed server-consuming run's MCP process from the same
   final snapshot, update the coordination ledger, remove pause requests, and resume affected
   recorded agents for targeted retests before unrelated checkpointed server/HIL work continues.
   Bind builds that completed during repair to that snapshot before they enter HIL. Use a
   replacement only under the continuity contract.

Do not let the test agent propose or make server edits. Do not use `$change-loop` for firmware,
fixture, SDK, infrastructure, documentation-only, metadata-only, evidence, or test-spec errors.

## Permission and safety boundary

- Record an explicit user delegation that authorizes the manager to continue all in-scope suite
  approvals. For each populated live plan, the manager reviews the exact board, artifact,
  operation, losses, and final state and may relay the recorded delegated permission without
  another chat pause when they are within that grant. Never invent a permission value or extend
  the grant beyond the assigned user-owned fixture.
- Follow every live MCP plan and permission gate. Preserve every destructive disclosure in
  evidence. Any action not already covered by the recorded delegation is ineligible for the main
  suite; move/keep it in non-gating Appendix A and skip it without asking the user.
- D35, R37, and R38 are autonomous try-last Appendix A experiments, not main release gates. Run
  them only when every fixture, backup, control, permission, and recovery step is already
  available without further operator intervention; otherwise record
  `SKIPPED_AUTONOMY_REQUIRED`. If attempted after main work cannot be delayed, keep D35/R38 with
  Delta and R37 with Cygnus as defined by the doer roster.
- Keep RF frequency, antenna, power, and duty cycle legal for the actual module/region.
- Never claim all-green while a required test is unreviewed or incomplete. A manual/external-only
  branch cannot remain required: replace it with an autonomous equivalent or move it to Appendix A.

## Completion

Finish the main suite only when every main-catalog test has a main-reviewed `PASS` and the
manager-owned Q40 nonduplicative corpus gate is complete, or the user explicitly narrows the
suite. Appendix A and future version-to-version regression policy are not release gates. Write a
final suite matrix with run directory, agent identity, server commit, firmware commit, result,
evidence path, repair loop (if any), Appendix A `PASS`/skip/gap outcomes, and unresolved
exclusions. Include the final reconciled lane table, harness config/hash, manager and monitor logs,
notification/ack record, exact PID-identity cleanup, and watcher terminal state. Stop the managed
watcher cooperatively or let a deliberately handed-off heartbeat lease remain active; never leave
an unowned background watcher. Never commit, push, deploy, or flash outside a live test plan.
