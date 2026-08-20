# BYO Firmware MCP: End-to-End Evaluation Program

The evaluator may use official internet sources when a package-local reference is insufficient,
but every retained input and every suite-produced file stays inside this `Firmware/` package.
Start with [README.md](README.md) for the package map. The execution procedure is
[`.codex/skills/run-firmware-test-suite/SKILL.md`](.codex/skills/run-firmware-test-suite/SKILL.md);
the live server/client workflow is [BYO-Firmware-MCP/README.md](BYO-Firmware-MCP/README.md) and
[BYO-Firmware-MCP/SERVER_GUIDE.md](BYO-Firmware-MCP/SERVER_GUIDE.md). For a verified server defect,
use the manager-controlled repair route in the execution skill rather than directly editing from a
fresh firmware run. Current progress and the permitted resume boundary live in
`.agent-workspace/SUITE_COORDINATION.md` and `multi-agent-logs/`.
**Repository evaluated:** `BYO-Firmware-MCP/`
**Original program baseline:** `9b34a849d8cc4cb1f8a1146000ded8e93d168a28`
(`fixing bugs on prototype that Jeff ran into`). Every run must bind itself to the exact server
snapshot it actually evaluates: HEAD plus the reviewed tracked diff and production-tree
fingerprint when the worktree intentionally contains uncommitted repairs. A clean checkout is
preferred for reproducibility but is not a release prerequisite, and a reviewed dirty snapshot is
not a reason to stop. Never mix server snapshots within one phase or silently advance to a later
revision.
**Available hardware:** two NUCLEO-L476RG boards and two nRF52840 DK boards, with the
STM32 boards linked by I2C on PB13/PB14 and one Waveshare CoreSX1262 module attached to each nRF
DK.

## 1. Purpose and definition of “complete”

This is a practical whole-product evaluation, not merely a collection of “can it blink?”
demos. It tests:

1. Whether a configured coding agent can start from an empty application repository, an exact
   MCU ordering code, and authoritative documentation.
2. Whether the MCP server discovers, sets up, distinguishes, and safely operates one or more
   real boards.
3. Whether an agent can build, deploy, verify, diagnose, repair, and retest realistic firmware.
4. Whether the server catches a fallible agent's mistakes without fabricating success or
   blocking correctly targeted work.
5. Whether plans, permissions, safety maps, artifact binding, process isolation, cleanup,
   timeouts, and per-board state behave correctly under failure.
6. Whether every registered MCP tool gets either:
   - a successful real-hardware exercise, or
   - an intentional, truthful refusal when the required authority is unavailable.

No finite HIL suite can cover every Python branch or every firmware situation. “Complete” for
this program therefore means all three layers below pass:

| Layer | Required coverage |
|---|---|
| Host automated tests | Unit, protocol-integration, fault-injection, and property tests for paths unsafe or impractical to induce on hardware |
| MCP contract tests | Every tool registered by the assigned server snapshot, dynamic visibility, strict schemas, plans, permissions, budgets, and restart semantics |
| Hardware experiments | Both MCU families, both probe families, one-board and two-board operation, UART, I2C, BLE, SPI/LoRa, flash, reset, debug, disconnect, cancellation, and recovery |

The original baseline contained **155 pytest-style tests**; record the actual collected count for
the assigned snapshot rather than using that historical number as a gate. The tests are strongest
around process isolation, J-Link behavior, connection promotion/cleanup, breakpoint truthfulness,
UART evidence, validation honesty, trusted-input admission, and several previously overstrict
limits. They are not a substitute for the application-level HIL campaigns below. Also note that
the current `pyproject.toml` development group declares Ruff and Pyright but not pytest; make the test runner
reproducible before treating a clean clone as testable.

## 2. What the repository says the server owns

The plan is derived from the current code and its documentation, especially:

- `BYO-Firmware-MCP/README.md` and `BYO-Firmware-MCP/SERVER_GUIDE.md`
- `BYO-Firmware-MCP/docs/architecture.md`
- `BYO-Firmware-MCP/docs/client-contract.md`
- `BYO-Firmware-MCP/docs/plan-tool-contract.md`
- `BYO-Firmware-MCP/src/pyocd_debug_mcp/server.py`
- `BYO-Firmware-MCP/src/pyocd_debug_mcp/guardrails/plan_defs.py`
- `BYO-Firmware-MCP/src/pyocd_debug_mcp/{setup_flow,safety,kernel,tools,adapters,services}/`

The relevant product boundaries are:

- project-local fresh-board setup, profile persistence, datasheet evidence, CMSIS-Pack
  verification, and safety-map generation;
- normal profile-based connection plus planned exceptional connection paths;
- process-isolated pyOCD sessions and board-scoped operation serialization;
- UART capture, write, and state-preserving multi-step exchanges;
- native-build execution and explicit artifact normalization;
- symbol, memory, CPU-register, peripheral-register, execution, breakpoint, and reset control;
- application/bootloader flash containment;
- run-scoped plans, permissions, validation gates, and budgets;
- destructive recovery with a fresh two-phase approval;
- cleanup after success, failure, timeout, cancellation, USB loss, and server shutdown.

The server intentionally ships without board profiles, packs, reference firmware, or `.firm`
runtime state. That makes a truly clean setup campaign essential.

## 3. Evaluation rules

### 3.1 Separate server correctness from agent skill

Score two things independently:

**Server score**

- Did the correct physical board receive the operation?
- Did the server reject stale, mismatched, malformed, unsafe, or unauthorized requests before
  target mutation?
- Did it report only observed facts?
- Did one board's failure leave the other board usable?
- Did it clean up sessions, serial handles, workers, plans, gates, and permissions correctly?

**Agent score**

- Did the agent follow the handshake and setup routing instead of guessing internal IDs?
- Did it obtain authoritative facts rather than invent a target, pack, pin, address, or port?
- Did it use UART/logging first and escalate to breakpoint/memory/register inspection when
  justified?
- Did it state a concrete hypothesis and interpret evidence correctly?
- Did it find the seeded root cause rather than blindly editing until the symptom disappeared?
- Did it avoid retry thrashing and clean up temporary instrumentation?

A working final application does not excuse a server safety failure. A correct server refusal
does not prove the agent debugged well.

#### 3.1.1 Zero-operator, no-external-blocker contract

A per-run specification translates this catalog into executable checks; it must not make the
catalog stricter merely because additional evidence would be nice to have. Treat a fact as a hard
prerequisite only when at least one of these is true:

- the selected catalog case explicitly requires it;
- the live server requests it to continue the public workflow;
- it is necessary to distinguish pass from fail for the claimed behavior; or
- it is necessary for electrical, RF, destructive-action, or target-identity safety.

The main suite is autonomous after launch. No main-catalog action may require another user message
or a human to touch, inspect, identify, move, rewire, relabel, reposition, power-cycle, or observe
hardware. Never require a photograph, visible marking, printed PCB revision, PCA number, removable
label, cable move, button press, jumper/solder change, DMM, logic analyzer, BLE sniffer, camera,
oscilloscope, external power instrument, or operator-timed event. Treat the connected four-board
fixture, its declared CoreSX1262 wiring, stable electronic identities, and recorded delegated
authorization as supplied inputs.

Use electronic/software-controlled equivalents: server disconnect/reconnect/reset, process-scoped
provider interruption, firmware-controlled advertising/RF disable, host-side enumeration evidence,
UART/peer counters, debug state, artifact hashes, and existing correlated evidence. Accept one
truthful, adequately correlated source; never demand the same fact through multiple modalities.
Electrical, RF, destructive-action, and target-identity safety remain mandatory, but satisfy them
from the declared fixture and live server plans rather than inventing operator work.

If a sealed run specification accidentally added such an extra gate, correct it with a signed
specification amendment and preserve already valid evidence. Removing an invented prerequisite is
a spec correction, not test weakening and not a reason to restart the doer or repeat unrelated
work.

`NEEDS_USER` and `INFRA_BLOCKED` are invalid terminal outcomes for main-catalog runs. The manager
repairs ordinary tooling, launcher, USB, network/cache, SDK, and server infrastructure; applies the
recorded delegated authorization after reviewing an exact live plan; accepts an autonomous
equivalent oracle; or corrects the spec and resumes the same persistent doer. Record temporary
resource/provider absence only as `WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` in the suite
coordination ledger, never in `RESULT.json`, and continue every unrelated lane. If a branch is
intrinsically impossible without a new human action or unavailable special equipment, move only
that branch to non-gating Appendix A and record `SKIPPED_AUTONOMY_REQUIRED`.

### 3.2 Fresh-run controls

For a **fresh setup/app** run:

1. Use a new application directory or fresh Git worktree.
2. Give the roster-assigned persistent doer a fresh, isolated task context. Do not create a new
   provider conversation merely for freshness; provider-session persistence and application-state
   freshness are separate concerns.
3. Start a new MCP server process.
4. Set a unique `BYO_MCP_ARTIFACT_ROOT`, or use that project's empty `.firm`.
5. Do not copy profiles, packs, safety maps, build outputs, or prior agent notes.
6. Record the host USB/probe/serial inventory. Exercise enumeration/reconnection with existing
   correlated port-history evidence or an autonomous host/server-controlled detach/re-enumeration;
   never request a cable move or operator-timed USB cycle.
7. Give the agent only:
   - the application requirement,
   - the exact package-level MCU ordering code established truthfully for the assigned fixture,
   - the two suite-baseline authoritative device datasheet PDFs copied by the fresh-run scaffold,
     with the specification identifying which one is applicable to each target,
   - when the case uses external wiring or modules, the manager-supplied fixed fixture wiring sheet
     containing the material facts the datasheet cannot establish, and
   - for A24/A25 only, the three explicitly allowed CoreSX1262 reference inputs named below.

The ordering code is established from the existing correlated suite record, official board
BOM/documentation, or trustworthy electronic identity evidence. Do not request another operator
statement, photograph, direct visual inspection, or PCB revision.

For a **returning-board** run, preserve `.firm` but still restart the client and server. This
distinguishes durable evidence from run-scoped authorization. Canonical shared inputs live under
`Firmware resources/datasheets/` and `Firmware resources/fixture-and-toolchain/`; the scaffolder
copies the applicable files into a new run using the legacy run-local filenames below so sealed
manifests remain compatible.

### 3.3 Information boundary

“Start with just the datasheet” must not turn into “force the agent to guess missing fixture
facts.” The fresh-run scaffold copies both suite-baseline device PDFs so one deterministic
scaffolder works for either board family; the per-run specification identifies the applicable
target document. The initial application repo should contain no code, SDK config, board profile,
pack, linker script, or generated state. It may contain:

- `REQUIREMENTS.md`
- `stm32L476rgt.pdf`
- `Nano_BLE_MCU-nRF52840_PS_v1.1.pdf`
- `.agent-workspace/FIXTURE.md`, supplied by the manager when the experiment uses corresponding
  fixed fixture facts:
  - which boards are connected;
  - STM32 I2C wiring: PB13=SCL, PB14=SDA, common ground, pull-up value and rail;
  - the **actual** CoreSX1262 module-to-nRF pin mapping;
  - the module's supported RF band and attached antenna;
  - any already-recorded solder-bridge or jumper state material to the selected interface.
- for A24/A25 only, hashed copies of `60852689.DS_SX1261_2 V2-2.pdf`,
  `waveshare-lora-module.pdf`, and `nrf-sx-pin-mappings.md`.

  Their canonical sources are
  `Firmware resources/datasheets/60852689.DS_SX1261_2 V2-2.pdf`,
  `Firmware resources/datasheets/waveshare-lora-module.pdf`, and
  `Firmware resources/fixture-and-toolchain/nrf-sx-pin-mappings.md`; keep those names inside the
  sealed run.

The doer treats this file as the fixed fixture contract. It never asks the user to inspect, meter,
rewire, move, solder, or change a jumper. A test needing a different physical configuration must
use an electronically controlled equivalent or be moved to non-gating Appendix A.

The agent may research additional official references and install an ordinary compatible SDK or
toolchain. It must say when a datasheet is insufficient. For example, an MCU datasheet cannot
prove an add-on module's wiring, the legal RF band, or a development board's solder-bridge state.
The fresh repository must not include a prewritten scheduler, ThreadX application, Zephyr
application, Devicetree overlay, or generated STM32Cube project. The agent must create or acquire
the required software through its normal documented path, pin every external dependency/version,
and record the exact source revision in the run evidence.

### 3.4 Authorized-use prompt clarity

Every prompt used to start or resume a test agent, reviewer, or server-repair agent must begin
with an accurate scope statement equivalent to:

> Authorized local firmware validation. Targets are limited to the named local workspace and the
> user-owned development boards explicitly assigned by this test. Follow every declared hardware
> plan and permission gate. No remote or third-party target is in scope.

Adapt that statement truthfully for host-only tests and tests with no assigned board. Describe
work in precise firmware, protocol-conformance, input-validation, debugging, and hardware-safety
terms. Do not add cyber-oriented language such as `attack`, `exploit`, `malware`, `credential
theft`, or `bypass` unless it is technically required by the exact experiment or observed
evidence.

This is a clarity rule, not a safety-evasion rule. Never disguise, split, euphemize, or omit a
material operation to influence a classifier, and never weaken an experiment, authorization
boundary, plan, permission gate, or evidence requirement. If a platform cyber-safety notice,
reroute, or refusal occurs, preserve its exact text and request context, checkpoint the exact
session, and continue other lanes. It is not a main-run terminal status.

Use the [provider-adapter contract](PROVIDER_ADAPTER.md) for all provider/model/effort/tier/route
settings, adapter status, and required pre-launch records. Do not start a live sprint or server
repair through a package script while that contract says the adapter is pending. Historical records
retain their truthful original settings and are not launch configuration.

### 3.5 Delegated hardware authorization

Preserve every live server plan, disclosure, scope check, and permission field. When the user has
explicitly delegated all in-scope suite approvals to the authoritative manager, record that grant
with its exact text and timestamp. The manager then reviews each populated live plan and may relay
the delegated permission without another conversational pause when the operation, board, artifact,
losses, and final state are contained by the recorded grant. Never extend the grant to an
unassigned board, third-party target, undeclared loss, or action the live server refuses.

Attempt an Appendix A experiment only when it is fully autonomous with existing controls,
authorization, credentials, and equipment. Otherwise record `SKIPPED_AUTONOMY_REQUIRED` without
asking the user. Do not fabricate an action or weaken the server's permission flow.

### 3.6 Manager-controlled parallel execution

Use one authoritative high-level manager and the five named roster-owned doer lanes defined below.
They are not fixed STM/nRF/host resource lanes. Eagerly launch or resume every doer whose next
phase is dependency-ready and whose workspace and resource leases are isolated; keep all eligible
lanes occupied in parallel rather than completing one doer's portfolio before starting another.
The board tokens are `STM-A`, `STM-B`, `NRF-A`, and `NRF-B`; host-only spec, build, and review work
does not consume a board token.

#### Sprint completion and finding pooling

A manager epoch or provider session is not a logical sprint. An interruption never ends the
logical sprint: preserve its sealed specification, verified checkpoints, completed evidence, and
accumulated findings; replace the dead invocation; issue fresh authority for each next live
action; and continue every feasible unrelated lane. Release or reassign a stale claim only after
complete exact old-owner/process absence proof. If proof is incomplete, wait on that exact
resource without stopping other work.

Administrative/provider errors, malformed calls, doer mistakes, specification/fixture/server
faults, and harness defects do not produce a sprint failure. Correct the affected suite-owned fact
or record its unit finding, then continue until every feasible unit has a truthful terminal
disposition. If a harness defect is observed, record it but do not start harness repair during the
sprint. First publish one `COMPLETED_WITH_FINDINGS` handoff containing the complete pool; ROOT
reviews/repairs it afterward, and the sprint earns no clean credit. A clean accepted sprint
publishes `COMPLETED_CLEAN`. Use `INCOMPLETE` only for explicit user cancellation, withdrawn
authority, or live harm that cannot be isolated safely.

Before the test orchestrator starts, the external run owner creates or selects the exact WIP
product worktree at package-local `target-harness/` and records its Git revision and dirty state.
Launch the test orchestrator from `Firmware/`. It may inspect both the suite and that product
worktree, but it must not reach above `Firmware/` or substitute the stable development harness.
Fresh firmware doers receive only their isolated run roots and may not inspect `target-harness/`.

The current high-level session remains the sole manager and owns scheduling, authorization,
leases, recovery, and evidence decisions. It launches provider turns through the WIP target's
ordinary firmware-compatible lane-controller route. The target's `orchestrator_harness` supplies
read-only reconciliation and bounded `watch --until-actionable` waits; its separate
`harness_watcher_implementation` process supplies deterministic diagnostics. Neither component
assigns resources, operates hardware, approves plans, repairs code, or replaces the manager.
Store campaign coordination below `.agent-workspace/`, harness observations below
`runtime/orchestrator-harness/<epoch>/`, and watcher-owned state below
`target-harness/runtime/harness-watcher/<epoch>/`.

Create fresh configs and runtime directories for every active manager epoch. Record the exact live
manager PID plus creation identity, every role/session and process identity, review and
no-progress intervals, target revision, and exact run roots the epoch may activate. Configure the
target harness for `fresh-experiments/*`, a one-second poll, a finite wait timeout, and the
epoch-specific observation directory. Configure exactly one deterministic watcher with explicit
manager/harness/lane log sources, a 120-180 second poll interval, a measured 10-15 minute
no-progress threshold, and `evaluator_enabled: false`. Bind it to the long-lived manager process,
not the short-lived shell that starts it. Never reuse a prior epoch's authority, requests, relays,
leases, PIDs, configs, cursors, or notifications.

Each active manager epoch is:

```text
reconcile -> start/confirm the deterministic watcher -> launch every eligible lane
-> bounded wait for an actionable role/process event or timeout
-> inspect the named lane and whole-suite state -> serial exact review/action
-> rescan every lane and lease -> fill newly eligible work -> checkpoint -> repeat
```

Wait on provider/process completion, the target's bounded
`orchestrator_harness watch --until-actionable --timeout <seconds>` call, or the active provider's
blocking wait instead of spending model turns in a tight poll. A timeout is a normal deterministic
supervision boundary: rescan lanes and leases, record the observation, then wait again. The WIP
target intentionally has no stable-only `watch --managed` or heartbeat CLI; never call those
commands. Inspect every live doer normally every two to three minutes during active HIL so a crash,
lost notification, repetition loop, or unexplained idle lease is caught. Before relaying a
permission-bearing request, verify the exact assignment, server snapshot, board, artifacts, live
producer/MCP lifetime, losses, and final state. Keep the real doer turn alive through bounded
helper gates and return it only at a genuine checkpoint, provider/lease wait, or completed slice.
Every HIL boundary records isolated MCP/state/artifact/log roots, exact process ancestry, and
first-artifact proof; cleanup targets only exact created descendants.

Every current role record carries the exact doer/task/session facts from which its lane is derived.
Every request, helper, and MCP record format that supports explicit scoping carries the
manager-assigned `declared_lane_id`. That explicit lane is authoritative even if a persistent
session ID was reused by an older task. Historical exits and checkpoints are baseline facts, not
current work; only a new lifecycle transition creates a new event.

The manager maintains these durable human-readable ledgers:

- `.agent-workspace/SUITE_COORDINATION.md`: manager identity, optional informational eligibility
  group (never an advancement gate), server HEAD plus dirty-diff/tree fingerprint, catalog test,
  canonical doer name, provider agent/session and reviewer identities, run directories, build/HIL
  dependencies, internal shards, phase-specific leases, process/runtime identities, and phase
  states;
- `.agent-workspace/SERVER_REPAIR_QUEUE.md`: only independently validated production-server
  defects, with reporting test, snapshot, evidence, reproducer, affected tests, disposition,
  repair slice, and targeted retest state.
- `.agent-workspace/epochs/<epoch>/MANAGER_LOG.jsonl`: append-only launches, notifications, exact
  reviews/actions, checkpoints, recoveries, and cleanup.
- `.agent-workspace/epochs/<epoch>/MONITOR_LOG.jsonl`: periodic whole-suite observations and
  diagnoses of inefficient, redundant, looping, stalled, or unexpectedly idle behavior.

#### Imported progress and resume boundary

On resume, read `multi-agent-logs/HANDOFF.md`, `multi-agent-logs/PROGRESS_REMAINING.md`,
`multi-agent-logs/current-state/CURRENT_SUITE_STATE.json`, and
`multi-agent-logs/current-state/CURRENT_RELEVANT_PROCESS_INVENTORY.json`. These records preserve
historical progress and evidence; their absolute paths, process identities, leases, configs,
watcher state, and authorization do not become live merely because they were copied here.

The current imported baseline records H00-H05, S10-S13, A20, A23, D33, and D36 as main-reviewed
green. It records A22/Atlas, D31/Boreal, A24/Cygnus, and A26/Delta as checkpointed but nonterminal.
Remaining main-suite work is A21, A25, D30, D32, D34, Q40, and Q41; D35, R37, and R38 remain
appendix-only. The named checkpoint directories are not currently present under
`fresh-experiments/`, so do not claim exact session or worktree resume until an exact run is
materialized and validated or an explicit fresh affected-run handoff is recorded.

M5 is closed after Q10 at its ten-attempt limit and `0/3` comparable qualifying sprints. Q10 passed
the harness and watcher gates but had insufficient manager evidence because the manager recorded
wake events in the wrong order and published responses without lane IDs. This is not evidence of a
current harness, watcher, or MCP-server defect. Never launch Q11. A new bounded M5 goal, attempt
budget, and explicit user authorization are required before live M5 validation resumes.

Before HIL starts or resumes, the manager writes the isolated run's
`.agent-workspace/RESOURCE_ASSIGNMENT.md` with its catalog/shard ID, `HIL_RUNNING`, common server
snapshot, canonical doer name, exact leases, assignment time, and manager identity. The test owner
reads but never edits this file. When a phase can reach a permission-bearing live plan, also record
the applicable delegated-authorization artifact path and SHA-256; absence means the agent may not
infer a grant.

A doer name identifies one persistent doing-subagent role and, when available, the same provider
session across tasks and completed logical sprints. At each manager or ROOT decision boundary the
session is idle and may resume only from a new manager-issued card; it never self-continues. If the
session is unavailable or the role/model selection changed, the manager records the old terminal
state and uses a correlated replacement with the same named role, durable checkpoints, accepted
evidence, and first unresolved action. Replacement never blocks sprint admission, discards green
work, or terminates the sprint. If the manager opens `N` concurrent execution lanes, it uses exactly
`N` named doers. Each task is assigned to exactly one doer, and a doer runs at most one task at a
time.

Already completed/bootstrap tasks receive no retroactive doer name. Roster-owned catalog work uses
this persistent lane pool and stable task assignment:

| Doer | Assigned catalog tasks |
|---|---|
| Atlas | S10, S13, A20, A22, D30, D32, Q41 |
| Boreal | S11, A21, D31, D36 |
| Cygnus | S12, A24, D33, D34 |
| Delta | A25, A26 |
| Nova | A23 only |

The [provider-adapter contract](PROVIDER_ADAPTER.md) is the sole authority for doer/reviewer/
server-repair models, reasoning, service tiers, route selection, and current pending-adapter
status. This table owns only named doer-to-catalog assignment.

On every scheduling pass, fill all five lanes concurrently where eligible. A blocked lane never
holds an unrelated lane: immediately assign each other idle doer its earliest dependency-ready
phase. A doer may receive its next assigned task only after its current task is terminal or at a
manager-recorded handoff, and the next phase must not depend on the blocked result. Reviewers and
server-repair coder/doer roles are not named firmware test-lane doers. On reassignment, provide the new isolated run path and forbid
access to the previous task directory; prior firmware files, leases, permission, and unevidenced
conclusions do not carry forward. Q40 remains manager-owned aggregation; assign each genuinely
missing Bxx branch to exactly one currently idle Atlas, Boreal, Cygnus, or Delta session. Do not
create a new branch-specific doer or reuse Nova.

Determine readiness per phase from only its explicit prerequisite edges, current selective
server-repair state, and required resource leases, including its isolated workspace and
doer/provider/launcher execution slots. A wave row, row number, incomplete row, unfinished
parallel-lane task, or prose row summary is never itself a dependency. Launch an eligible phase
from any row immediately, even while work in the same or an earlier row remains unfinished. Rescan
all lanes after every launch, completion, checkpoint, failure, provider-state change, repair-state
change, and lease transition. If usable hardware is idle, immediately audit all pending phases
against that hardware instead of waiting for a nominal wave to finish.

Parallel execution must obey all of the following:

1. Never run duplicate managers/controllers for the same suite, two doers for one task, two live
   provider sessions under one doer name, or concurrent repairs against one server worktree.
   Keep the roster-assigned persistent doer for every phase and internal shard of its current task.
   Q40 branches not already evidenced by an application campaign use an idle ordinary roster doer
   without rebuilding the base application.
2. Give every test its own run, MCP process, artifact root, and server state root unless the test
   explicitly evaluates a shared process. Every server-consuming phase records the same immutable
   server snapshot.
3. Before each phase, lease its doer/provider/launcher execution slot, isolated workspace, every
   board token, probe, serial endpoint, peer/radio, autonomous electronic control actually used,
   USB-enumeration or power scope actually disrupted, global server lifecycle, and mutable
   cache/artifact/state root. External lab instruments and manual controls are outside the
   main-suite contract and consume no lease.
   Overlapping exclusive leases are forbidden. Only the manager assigns leases; agents never
   self-acquire hardware.
4. Track `SPEC_READY`, `BUILDING`, `BUILT_WAITING_FOR_LEASE`, `HIL_RUNNING`, `CHECKPOINTED`, and
   `PASS_CLAIMED` independently of terminal run status. Build phases need build prerequisites and
   host leases; HIL phases additionally need HIL prerequisites, a server snapshot, and hardware
   leases. Only an explicit consumed result/evidence edge, the selective server-repair state, or an
   actually conflicting exclusive lease blocks a phase. Table position, wave membership, numeric
   test order, and another lane's unfinished state do not. A failure blocks that test, dependency
   descendants, and conflicting leases; it does not cancel unrelated eligible work. All required
   tests remain release gates.
5. Treat S12, D34, cross-family barriers, and any test whose isolation cannot be proven as
   exclusive. A multi-board test owns its internal concurrency.
6. Permit future spec authoring, read-only spec review, and isolated board-free builds during HIL.
   A completed build preserves an immutable artifact/configuration handoff and waits at
   `BUILT_WAITING_FOR_LEASE`; it may not enter HIL until the manager assigns its leases.
7. A catalog item may define independent board/family execution shards, but they remain internal
   phases operated by the task's assigned lane doer. Give each shard immutable scope,
   an isolated application/build tree, and unique leases. The doer may orchestrate concurrent
   processes but may not delegate a shard to another doing subagent. The manager aggregates the
   evidence into one catalog verdict. Sharding must not duplicate a branch, weaken an oracle, or
   omit work.

Each sealed spec defines safe checkpoint boundaries and a maximum pause latency. Between numbered
requirements and bounded soak/repetition epochs, the agent checks for
`.agent-workspace/PAUSE_REQUESTED.md`. It never pauses an atomic hardware mutation mid-operation.
After the current bounded action completes or times out, it flushes evidence, records live and
cleanup state, writes `.agent-workspace/PARALLEL_CHECKPOINT.md`, and returns without a terminal
result. The manager consumes runtime notifications or uses an ordinary blocking role/process wait;
it never burns model turns in a tight polling loop. During active HIL it still
performs a bounded supervision pass normally every two to three minutes so a missing notification,
crashed role, inefficient repetition, or unexplained idle lease is diagnosed promptly.

If the manager suspects a controller-caused false conflict, cross-lane attachment, or stale
notification, diagnose it without interrupting unaffected roles. Once confirmed, stop new
launches, checkpoint only affected live roles, stop the exact affected processes, preserve all
completed evidence, and resume only incomplete work after the controller issue is corrected. Do
not restart the whole suite or already-passed lanes.

Before ending a manager epoch, durably hand off ownership or checkpoint every live role, stop the
deterministic watcher and other exact owned processes cooperatively, confirm their PID-plus-creation
identities are absent, and record pending state. Never use a broad process-name or command-line
match for cleanup. The next manager reconciles the package-local ledger before resuming.

A test-agent `SERVER_FAILURE` is a claim, not automatic repair authority. The manager first
reproduces and classifies it. For a verified production-server defect, open this selective repair
barrier:

1. add it to `SERVER_REPAIR_QUEUE.md`;
2. stop starting new server-consuming or HIL phases and request a safe checkpoint from every active
   server/HIL consumer;
3. wait until those consumers are checkpointed and mark them frozen; isolated board-free
   spec/build/review phases may continue only if they do not invoke or depend on the live server;
4. process queued defects serially as small main-authored repairs, keeping unrelated
    server/HIL consumers frozen and closing each item only after its reporting agent passes a
    targeted retest;
5. record one final common server snapshot and restart every checkpointed MCP process;
6. resume the exact persistent agents, bind builds completed during repair to the new snapshot
    before HIL, and retain unrelated verified evidence.

#### Incremental evidence and bounded adversarial review

Every PASS is durable evidence bound to the exact sealed spec/amendment, source and artifact
fingerprints, server snapshot, fixture identity, and relevant lease/state. A later failed test,
repair, or adversarial criticism invalidates only the requirement/evidence edges it contradicts or
whose inputs changed.

- Rerun the failed check, directly affected requirements, and the smallest regression surface
  reached by the change. Do not rerun all tests, restart every lane, repeat an expensive application
  campaign/soak, or rebuild from scratch merely because one check or review failed.
- Keep unrelated eligible lanes running and retain their accepted evidence. Restart only MCP
  processes that consumed changed server code. Resume only HIL/firmware phases whose snapshot or
  required evidence was invalidated.
- Each sealed-spec reviewer gets one spec pass and one PASS-evidence pass. Rejected evidence permits
  one targeted follow-up covering only the missing/invalidated proof; it does not reopen unchanged
  accepted requirements.
- Reviewers label findings `ACTIONABLE` or `ADVISORY`. Actionable findings demonstrate an evidenced
  main-catalog requirement violation, credible safety/data-loss/identity risk, reproducible
  failure, or likely hang/orchestration collapse. Style preferences, speculative hardening,
  vanishingly unlikely cases without evidence, unrelated features, and disproportionate complexity
  are advisory.
- The high-level manager records advisory findings but does not block delivery or expand scope for
  them. When actionable findings are resolved and objective gates are green, stop the adversarial
  loop and deliver the working product; do not seek perfection through repeated reviews.

Every production-server repair uses `Firmware resources/test-program/design_charter.md`, this
catalog, and `.codex/skills/run-firmware-test-suite/references/execution-contract.md` as live
constraints, not a one-time preface. The manager rereads the applicable clauses before specifying
the repair, before writing and validating the plan, before implementation, and before accepting
the neutral tests and targeted HIL retest. Every repair-role prompt requires the same
package-local contract.

Start a HIL phase when its own declared host, setup, electronic identity, server-snapshot, and
resource prerequisites are green. Do not impose a blanket H00–H05 barrier: unrelated host/fault
matrix cases continue in parallel, while any failed host requirement that the selected HIL path
actually consumes is repaired autonomously before that phase. Never stop scheduling other eligible
lanes merely because one test, provider, board, or fixture is waiting.

### 3.7 Required evidence bundle

Use the isolated `fresh-experiments/<test-id>_<timestamp>/` run created by the suite scaffolder and
save the items below when they are applicable to the selected case or a claimed pass/fail fact.
Absence of an irrelevant evidence type is not a test failure:

- server Git commit, dirty status, reviewed diff fingerprint, and production-tree fingerprint;
- OS, `uv`, Python, pyOCD, SDK, compiler, and agent/model versions;
- the exact initial prompt and every follow-up;
- full MCP request/response transcript, including `tools/list_changed`;
- USB/debug-probe and serial-port inventory at the boundaries where identity, enumeration, or
  cleanup is under test;
- hashes of input PDFs, packs, ELF/HEX/BIN/map files, and collected manifest;
- native build stdout/stderr and exact argv/cwd/environment declarations for cases that build;
- application Git diff and seeded-bug ID (the bug key remains hidden from the agent);
- `.firm` snapshots at boundaries where durable state or freshness is under test, without treating
  them as proof of live authority;
- UART captures and peer-to-peer packet counters;
- independent autonomous oracle evidence: host serial logger, known-good peer, debug/register
  state, artifact/build inspection, electronic identity, or target behavior;
- final board run state and a pass/fail record for server and agent separately.

### 3.8 Agent allocation and comparison

Create each application once. Assign every roster-owned catalog task, including A23/APP-4, to the
named persistent doer in section 3.6. The [provider-adapter contract](PROVIDER_ADAPTER.md) owns
model/effort/route/session allocation, the reviewer and server-repair roles, and all pre-launch
records. This document's local rule is that the reviewer stays read-only and that the server repair
is admitted only after a manager-verified production-server defect.

Q40 fills only seeded-branch coverage that the earlier application campaigns did not execute. It
must not rebuild an application, rerun an already evidenced branch, or run every branch once per
provider. Report coverage and quality by application, bug class, hardware, and budget; it is not a
cross-provider model comparison.

## 4. Fixed fixture contract and safety

### 4.1 Board identities

The manager maps these names to the already-recorded stable electronic identities:

- `STM-A`, `STM-B`
- `NRF-A`, `NRF-B`

No removable label, marking, photograph, revision check, or user observation is required. Let
`setup_overview` and the server route friendly names, and use the manager assignment plus stable
probe/USB/VCOM identities to detect swaps.

### 4.2 STM32 I2C fixture

The supplied fixed fixture uses the STM32L476 datasheet's PB13=I2C2_SCL and PB14=I2C2_SDA under
AF4:

- PB13 to PB13 (SCL)
- PB14 to PB14 (SDA)
- GND to GND
- the already-installed suitable 3.3 V pull-ups declared by the fixture record

The doer does not meter, photograph, rewire, or change this fixture. Diagnose through firmware
counters, GPIO/register configuration, UART, peer behavior, and server/debug evidence. The Nucleo
manual states that USART2 on PA2/PA3 is connected to the ST-LINK virtual COM port by default; the
manager-supplied fixture record is authoritative for any already-existing bridge state.

### 4.3 nRF/CoreSX1262 fixture

The manager-supplied fixed fixture record provides the actual CoreSX1262 SPI
SCK/MOSI/MISO/CS, RESET, DIO, RF-switch, and power connections for each module, plus:

- module variant and frequency band;
- antenna appropriate for that band;
- supply voltage and current capability;
- logic voltage compatibility;
- local regulatory frequency, bandwidth, duty-cycle, and power rules.

The fixture record attests the already-connected suitable antennas. Use the lowest practical
transmit power and a legal test frequency. The doer never asks for antenna inspection,
repositioning, rewiring, or another RF-authorization statement.

### 4.4 Independent oracles

External lab instruments are outside the main-suite contract and are never requested. Use
host-side timestamped serial logging, target UART, peer-observed packet counters, artifact hashes,
build/map inspection, electronic identity, register/debug state, and directly observed target
behavior as independent oracles. MCP success text alone is not sufficient for a behavioral claim.

## 5. Fresh application campaigns

Each application is built in a separate empty repository. Keep acceptance strings unique and
machine-checkable. Create every clean application/run beneath `fresh-experiments/` with
`.codex/skills/run-firmware-test-suite/scripts/fresh_test.py`. The workspace is only a parent
container; each
experiment child must still begin with only the inputs allowed by section 3.3.

### 5.1 Required scheduler/OS distribution

The applications deliberately use three different concurrency models. Do not replace one model
with a more familiar RTOS merely to make the build easier.

| Application | Required execution model | Queue requirement |
|---|---|---|
| APP-1 | STM32, custom bare-metal cooperative scheduler written in the fresh repo | statically allocated bounded event and UART queues |
| APP-2 | STM32, custom bare-metal tick-driven fixed-priority scheduler written in the fresh repo | per-task bounded queues plus ISR-to-task event queue |
| APP-3 | STM32, Eclipse ThreadX | ThreadX message queues between ISR-facing producers, CLI, workers, and supervisor |
| APP-4 | nRF, Zephyr through a pinned nRF Connect SDK/Zephyr workspace | `k_msgq` for BLE events/data and `k_work` only for justified deferred work |
| APP-5 | nRF, Zephyr through the same pinned toolchain family | `k_msgq` between GPIO/SPI/radio events and radio worker |
| APP-6 | nRF, Zephyr | separate bounded BLE, LoRa, command, and response queues |

For every model:

- all queues have explicit item type, depth, full policy, producer/consumer ownership, and
  counters for enqueue, dequeue, high-water mark, full, drop, timeout, and corruption;
- ISRs only acknowledge hardware, capture minimal data, and enqueue/defer through a documented
  ISR-safe path; they never block, allocate, print, or perform long protocol work;
- every task/thread has one responsibility, a documented priority, static stack where supported,
  measured stack margin, and a bounded blocking policy;
- shared peripherals have exactly one ownership discipline; mutex lock ordering and any priority
  inheritance are documented;
- the watchdog is fed by a supervisor that checks task progress, not blindly by a timer ISR;
- no dynamic allocation is permitted after initialization in the acceptance build;
- queue-full, starvation, priority inversion, deadlock, stack exhaustion, and lost-wakeup paths are
  deliberate benchmark targets rather than undefined “stress.”

The custom bare-metal schedulers are intentionally small test applications, not production RTOSes.
They must be understandable from their source and must not import FreeRTOS, CMSIS-RTOS, ThreadX, or
Zephyr kernel code.

### APP-1: STM32 bare-metal cooperative scheduler, heartbeat, and diagnostic CLI

**Purpose:** first build, artifact, application flash, reset, UART, symbol, and basic-debug path.

Required behavior:

- a custom run-to-completion cooperative event scheduler with a static task table;
- scheduler tasks for heartbeat, UART RX parsing, command execution, telemetry, and health;
- UART RX and periodic timer ISRs that enqueue fixed-size events without doing application work;
- bounded queues with an explicit full policy and visible queue/scheduler counters;
- LED heartbeat with configurable `blink_period_ms`;
- UART at 115200 baud with a stable prompt;
- commands: `help`, `status`, `blink on`, `blink off`, `blink period <ms>`, `counters`,
  `queue status`, `scheduler status`, `reset-cause`, and `version`;
- global debug symbols for boot count, scheduler tick/dispatch count, queue state, task heartbeats,
  error flags, and blink period;
- truthful boot banner containing build ID and reset cause;
- ELF and linker map with debug information.

Acceptance:

- a single `serial_exchange` proves ordered state survives on one port open;
- `read_memory_symbol` agrees with `status`;
- `reset_and_run` increments the boot counter and produces one boot banner;
- `halt` stops the heartbeat and `resume` restores it;
- a controlled UART burst reaches the documented queue-full policy without memory corruption,
  lost scheduler liveness, or an unexplained drop;
- no task can monopolize the cooperative scheduler beyond its documented run-to-completion bound.

### APP-2: Dual-STM32 bare-metal fixed-priority scheduler, I2C RPC, and telemetry

**Purpose:** two-board routing, simultaneous sessions, I2C diagnosis, concurrency, and peer
evidence.

Roles:

- each image contains a custom tick-driven, fixed-priority, run-to-completion scheduler with
  statically configured tasks and no external RTOS;
- tasks cover I2C protocol state, UART CLI, telemetry, timeout/recovery, and health supervision;
- the I2C/UART/timer ISRs enqueue minimal events for task-level processing;
- controller sends `{sequence, opcode, length, payload, CRC}`;
- responder validates the frame and returns status plus monotonic counters;
- both expose UART CLIs and counters for TX, RX, NACK, timeout, CRC failure, bus recovery, and
  last sequence, plus per-task dispatch, deadline miss, starvation, queue depth/high-water, full,
  drop, and timeout counters;
- begin at 100 kHz; add a 400 kHz build only after 100 kHz is proven;
- include bounded I2C timeouts and a documented bus-recovery path.

Acceptance:

- 10,000 request/reply operations with zero silent corruption;
- controller and responder counters reconcile;
- a reset of either board recovers without power-cycling the other;
- a failure on one MCP session does not invalidate the peer session;
- the lowest-priority telemetry/health tasks continue to make documented progress during maximum
  I2C and UART load;
- queue wraparound, simultaneous ISR/task access, and repeated full/empty transitions remain
  correct.

### APP-3: STM32 ThreadX startup, low-power, watchdog, and fault lab

**Purpose:** reset variants, early-startup debugging, connect-under-reset, fault forensics, and
reset-loop diagnosis in a real RTOS application.

Required behavior:

- Eclipse ThreadX acquired from an official, pinned revision and built for the Cortex-M4 target;
- statically allocated ThreadX threads, stacks, queues, mutexes, event flags, and timers;
- separate boot/supervisor, heartbeat, UART RX, CLI command, telemetry, and fault-injection
  threads with documented priorities and preemption behavior;
- UART/timer/peripheral ISRs use only allowed non-blocking ThreadX/driver paths and defer work to
  threads through queues or event flags;
- a supervisor checks each thread heartbeat, queue progress, and stack margin before feeding the
  watchdog;
- a documented mutex policy with priority inheritance where a shared peripheral requires it;
- early boot stages marked in RAM and UART when available;
- watchdog with retained boot/reset counters;
- selectable WFI/low-power mode;
- debug build containing safe commands that trigger divide-by-zero, invalid pointer access,
  stack exhaustion, queue saturation, priority inversion, deadlock, and a watchdog loop;
- a fault record containing stacked PC/LR and fault-status registers, when software can capture
  them without hiding the original failure.

Acceptance:

- the agent distinguishes a halted core, running core, fault handler, and reset loop;
- it uses `reset_and_halt` or `connect_under_reset` when normal attach cannot observe early boot;
- it identifies the deliberately seeded cause from target evidence, not only from source review;
- queue item sizing/storage, thread stacks, priority ordering, wait options, and ISR/thread API
  context are visible in the evidence and correct;
- high-priority load does not starve health supervision, and the priority-inversion test is
  bounded rather than intermittent.

### APP-4: Dual-nRF Zephyr BLE sensor/service pair

**Purpose:** fresh nRF setup, dual J-Link sessions, Zephyr/NCS-style build, BLE state diagnosis,
UART, and multi-image artifact selection.

Roles:

- use a pinned nRF Connect SDK/Zephyr revision, board target, Kconfig, and Devicetree inputs;
- BLE callbacks publish compact events into `k_msgq`; protocol/state processing occurs in
  dedicated threads, not in callbacks or ISRs;
- use Zephyr workqueues only where the work-item lifecycle and bounded execution are justified;
- peripheral advertises a custom service with readable state and notifications;
- central scans, filters, connects, discovers, subscribes, and logs sequence-numbered values;
- both expose a UART diagnostic shell with role, address, connection state, RSSI, discovery
  state, subscription state, packet counters, queue depth/high-water/full/drop, and thread stack
  margins;
- one variant enables MCUboot or another legitimate multi-image output so multiple ELF/map
  candidates exist.

Acceptance:

- 1,000 ordered notifications with counters reconciled at both ends;
- disconnect/reconnect works after either board resets;
- the agent explicitly selects the application artifact rather than guessing among child images;
- simultaneous J-Link sessions remain independent;
- BLE callback bursts and reconnect storms do not block the system workqueue, overflow silently,
  or lose ordering without a counter.

### APP-5: Dual-nRF Zephyr CoreSX1262 ping/pong link

**Purpose:** SPI register debugging, external-radio interrupt handling, RF configuration, packet
evidence, and peer isolation.

Required behavior:

- use the manager-supplied hashed `waveshare-lora-module.pdf`,
  `nrf-sx-pin-mappings.md`, and `60852689.DS_SX1261_2 V2-2.pdf` inputs; the attached radios are
  915 MHz Waveshare CoreSX1262 modules and the mapping file defines their fixed nRF52840 DK
  connections;
- use Zephyr threads, `k_msgq`, GPIO callbacks, SPI APIs, and delayed work/timers from the pinned
  workspace;
- DIO GPIO callbacks enqueue compact IRQ events and never perform SPI transactions directly;
- one radio worker owns the SX1262 state machine and SPI device; CLI/telemetry threads communicate
  with it through bounded command/result queues;
- first prove both SX1262 SPI paths without transmitting by observing the documented reset/BUSY
  protocol and coherent `GetStatus` plus `GetDeviceErrors` responses; SX1262 has no SX1276-style
  version register, so do not invent one;
- configure an agreed legal frequency, bandwidth, spreading factor, coding rate, sync word, CRC,
  preamble, and output path;
- send sequence-numbered packets with application CRC;
- record RSSI, SNR, IRQ flags, timeout, CRC failure, and last sequence;
- expose a UART shell for register dump, radio state, counters, queue state, send, receive, and
  reset.

Acceptance:

- 1,000 bidirectional packets with no unexplained sequence loss;
- autonomous status/error opcode round-trips, GPIO/IRQ counters, UART diagnostics, and peer packet
  evidence agree with firmware's claimed SPI/DIO behavior;
- a module reset and an MCU reset both recover;
- mismatched RF parameters are diagnosed specifically rather than called “bad hardware”;
- an IRQ burst, command burst, and receive timeout cannot cause concurrent SPI ownership,
  unbounded workqueue execution, or an unreported queue drop.

### APP-6: nRF Zephyr BLE-to-LoRa bridge

**Purpose:** realistic RTOS/concurrency debugging and an integrated system using BLE, SPI, GPIO
interrupts, queues, timers, UART, and two boards.

Behavior:

- use the same manager-supplied hashed CoreSX1262 module, datasheet, and fixed nRF52840 DK mapping
  inputs allowed for A24;
- use statically defined Zephyr threads/stacks with documented priorities and bounded waits;
- `NRF-A` receives BLE commands and sends corresponding LoRa requests;
- `NRF-B` returns LoRa replies; `NRF-A` publishes the result by BLE notification;
- use separate bounded `k_msgq` instances for BLE ingress, LoRa commands, LoRa responses, and BLE
  egress rather than a shared global message object;
- use a single-owner LoRa worker and non-blocking BLE callback-to-thread handoff;
- bounded queues, message IDs, retry limits, full/drop policies, and end-to-end latency counters;
- health CLI reports thread/task state, queue depth/high-water marks, stack margins, radio states,
  and error counters.

Acceptance:

- bounded functional/load exercise shows no deadlock, silent loss, runaway retry, or unbounded
  queue growth;
- firmware-controlled BLE disconnect, induced LoRa timeout/config mismatch, server-issued peer
  reset, and MCP reconnect each recover;
- end-to-end IDs prove that a BLE success is not incorrectly inferred from only a LoRa transmit.

## 6. Experiment series

Use the resource/phase waves in section 11 only as a visual grouping of likely concurrency.
Preserve dependencies where a later phase consumes earlier firmware/setup evidence, but never use
row order or row completion as a gate. Phases with satisfied case-specific dependencies, isolated
workspaces, and disjoint leases run concurrently across every eligible doer lane, including phases
listed in later rows. A failed case blocks only its dependency descendants and conflicting leases.
Appendix A is autonomous, non-gating, and tried only after it cannot delay main-suite work.

### Phase H — Host and MCP contract, no target mutation

#### H00 — Reproducible server-snapshot materialization

1. Materialize the exact recorded server snapshot in a new path, including its reviewed tracked
   diff when the assigned snapshot is intentionally dirty.
2. Run `uv sync --locked`.
3. Run the documented package build/import checks, Ruff, Pyright, and the complete automated test
   suite using a declared/reproducible pytest environment.
4. Start the stdio server from an unrelated working directory.
5. Verify stdout contains only MCP framing; provider chatter must go to stderr.
6. Repeat on a path containing spaces and Unicode.
7. Run the host-only suite in CI on supported Windows and POSIX hosts so Windows job/process
   cleanup and POSIX process-group branches both receive real coverage.

**Pass:** install is lockfile-reproducible; all checks run from documented commands; no
environment-specific path is required; stdio framing is clean. A missing test dependency is a
testability failure until documented and fixed.

#### H01 — Handshake, discovery, strict schemas, and dynamic visibility

1. Record the initial `tools/list`; derive the expected registered and initially advertised tool
   counts from the assigned server snapshot rather than treating historical counts as permanent.
2. Call `initialization_handshake` first.
3. Call every `*-plan` with the universal all-NULL envelope.
4. Submit malformed plans: flattened action parameters, omitted fields, extra fields, wrong JSON
   types, invalid budget, boilerplate hypothesis, and permission on a non-permission plan.
5. Confirm malformed submissions do not replace an already valid plan or consume its budget.
6. Accept one harmless plan and verify the action becomes visible plus a
   `tools/list_changed` notification is sent.
7. Call the hidden action with a stale/static binding before and after unlock.
8. Exhaust or replace the plan and verify the action relocks.
9. Exercise the exact server-returned one-child `action_batch` fallback once with a simulated
   static client.

**Pass:** discovery is guidance only; direct calls cannot bypass handler locks; unknown fields are
rejected; dynamic and static-client paths enforce identical plan, gate, permission, and budget
checks.

#### H02 — No-board, absent-board, ambiguous-board, and duplicate assignment

Test these inventories separately:

- no probes connected;
- one board connected;
- two identical STM32 probes;
- two identical nRF J-Link probes;
- all four boards;
- one extra unrelated serial adapter;
- a familiar board name that matches no profile;
- two requested friendly names aimed at the same physical connection;
- the literal normalized `no board` sentinel alone and incorrectly mixed with another name.

**Pass:** `setup_overview` offers friendly, bounded choices; does not ask the user for internal
IDs; never assigns one physical connection to two logical boards; and gives a specific recovery
step for absence or ambiguity.

#### H03 — Native build and artifact collector matrix

For small synthetic projects and the six real apps, test:

- exact argv, cwd, repeatable environment values, inherited network, and intentional `--offline`;
- missing executable, compile failure, link failure, timeout, and cancellation;
- valid ELF+map, ELF+HEX+map, HEX without coherent ELF, raw BIN, zero-byte file, malformed ELF,
  malformed HEX, and map from a different build;
- output directory already non-empty;
- paths with spaces, Unicode, and symlinks;
- a Zephyr/NCS multi-image tree with several legitimate ELF and map files;
- explicit `--artifact ROLE=PATH` selection from ambiguous output;
- `collect_build_artifacts` canonical names, byte-for-byte hashes, `expected_roles`, and manifest.

**Pass:** the server/helper never invents a build provider or artifact; multiple candidates are
reported for explicit selection rather than treated as a generic build failure; malformed or
incoherent outputs do not become flash authority; offline mode is described honestly as
best-effort client guards, not a network sandbox.

#### H04 — Datasheet, pack, and durable-evidence correctness

Use disposable artifact roots:

1. Correct exact part + correct official PDF + official pack.
2. Correct part + wrong-family PDF.
3. Near-match part suffix/package.
4. Pack with no exact device leaf.
5. Pack containing several similar device leaves.
6. Corrupt/empty pack and corrupt/empty PDF.
7. Change pack/PDF bytes after a candidate or plan is prepared.
8. Replay a valid returning-board setup with no network.
9. Exercise `pyocd-pack-repair` against a disposable partial index.
10. Tamper with profile, pack manifest, cache, and safety-map files one at a time.

**Pass:** exact bytes and exact leaf are replayed; client strings and manifests remain indices,
not authority; mismatches name the repair; cache hints never open a gate; corrupt authority is not
silently regenerated if doing so could lose one-way allocation information.

#### H05 — Managed-operation and process fault injection

Use the fake provider worker and a test MCP client to induce:

- provider stdout noise, malformed JSON, wrong request ID, crash, hang before ready, hang mid-call;
- blocked parent write, cancellation, deadline expiry, and EOF;
- cleanup exception, marker unlink failure, unconfirmed termination, and stale marker on restart;
- serial open/read/write/close exceptions;
- report-write failure during connection promotion and disconnect.

**Pass:** failure is bounded, honestly attributed, and isolated to the affected board; confirmed
cleanup removes ownership; unconfirmed cleanup remains fail-closed and actionable; no MCP stdout
corruption occurs.

### Phase S — Fresh and returning board setup

#### S10 — Fresh STM32 setup from datasheet

Run twice, once per Nucleo, from separate fresh APP-1 repositories:

1. Give only a friendly board name, the already-established exact MCU ordering code, local official
   PDF, and UART requirement. Use the suite's correlated electronic/official identity record; do
   not request a marking, photograph, PCB revision, or another operator statement.
2. Follow `initialization_handshake` → `setup_overview` → `load_setup_tool` →
   `board_setup-plan` → `board_setup`.
3. If research or a friendly board choice is requested, the manager supplies it from the existing
   assignment/electronic identity record and uses `continue_setup` exactly as directed.
4. Intentionally choose the wrong identical board once, then use the supported repair flow.
5. Run `board_safety_refresh`, `board_validate`, `get_setup_status`, `connect`,
   `get_board_info`, and `disconnect`.

**Pass:** the server derives/replays support, captures the exact PDF, resolves the stable probe and
VCOM identity, creates project-local evidence, performs a non-destructive live identity check, and
reports code readiness separately from UART readiness.

#### S11 — Fresh nRF setup from datasheet

Repeat S10 for each nRF DK. Use the exact `nRF52840-QIAA` ordering information truthfully
established for each assigned DK; do not infer the package suffix from the marketing name alone.
The existing correlated official board/BOM and electronic evidence is sufficient. `PCA10056`,
printed PCB revision, a board photograph, direct visual chip inspection, and another operator
statement are never S11 prerequisites.

**Pass:** both identical J-Link probes and their virtual COM ports remain distinguishable;
setup/validation on one nRF never grants readiness to the other; no hidden checkout board profile
is required.

#### S12 — Four-board simultaneous routing

With all boards connected:

1. Request all four by familiar names in one `setup_overview`.
2. Make the correct choices and validate all four; do not repeat the wrong-board or
   duplicate-assignment cases already covered by S10/S11 and H02.
3. Replay the already-captured USB(3)→USB(4) port-change evidence and repeat setup overview, or use
   an autonomous host/server-controlled detach/re-enumeration if fresh evidence is necessary. No
   cable move, live absent epoch, or operator-timed event is required.

**Pass:** a port-number change does not silently retarget a profile; stable identities remap
correctly; each logical board has exactly one live physical connection.

#### S13 — Returning state versus run-scoped authority

1. Preserve valid `.firm` state and restart only the MCP server.
2. Observe `get_setup_status` before connecting/validating.
3. Attempt a stale guarded action copied from the prior run.
4. Reconnect and revalidate.
5. Call the MCP server's logical `disconnect` for one board and test both that board and a
   still-connected peer; do not physically detach anything.
6. Restart after a valid plan and full-session permission.

**Pass:** profiles/evidence persist, but connections, assignments, plans, permissions, unlocked
tools, and validation gates do not. Disconnect clears only the named board.

### Phase A — Real application workflows

#### A20 — APP-1 build, collect, flash, reset, and UART

Atlas runs `A20/STM-A` and `A20/STM-B` as internal execution shards with isolated application
trees and one aggregate A20 verdict. No second A20 doing subagent is launched.

1. Agent creates APP-1 and its cooperative scheduler/queues from the empty repo using official
   sources; no external RTOS or scheduler code is allowed.
2. Build with the project's native tool and preserve ELF+map.
3. Optionally normalize outputs with `collect_build_artifacts`.
4. Initialize and submit `flash_application-plan`; the manager reviews the exact populated plan,
   relays the already-recorded delegated permission, and then performs `flash_application` without
   another chat pause.
5. Verify artifact digest, returned programming result, and final observed target state.
6. Run `reset_and_run`, bounded `read_serial`, `write_serial`, and a three-step
   `serial_exchange`.
7. Reboot five times and reconcile boot counters and banners.
8. Send controlled UART bursts through empty, partially full, full, wraparound, and recovered queue
   states while reading scheduler/queue symbols and health counters.

**Pass:** programming success is not called behavioral success; “running” is reported only when
observed; CLI evidence proves behavior; artifact hashes remain stable from accepted plan through
execution; the custom scheduler remains live and its declared queue-full policy matches evidence.

#### A21 — APP-2 dual-STM32 I2C

1. Build controller and responder, including their custom fixed-priority schedulers, as explicit
   role artifacts.
2. Flash each artifact to its intended board.
3. Use both UARTs to establish role, build ID, and initial counters.
4. Run functional traffic, 10,000-frame stress, controller reset, responder reset, and
   server-controlled peer disconnect/reconnect.
5. Debug one seeded fault at a time from the I2C bug catalog in section 7.
6. Run simultaneous long UART captures or inspections against both boards.
7. Saturate I2C and UART producers while proving deadline, starvation, queue-full, and wraparound
   counters on both scheduler instances.

**Pass:** no role/artifact swap, counters reconcile, MCP operations do not serialize unrelated
boards unnecessarily, and a provider/USB failure on one board does not poison the other.

#### A22 — APP-3 startup, low-power, watchdog, and fault debugging

Atlas partitions the seeded faults into internal `A22/STM-A` and `A22/STM-B` execution shards when
both boards are available and may drive their disjoint processes concurrently. Each shard uses an
isolated application tree; no second A22 doing subagent is launched, and the aggregate A22 verdict
requires every assigned fault. For each seeded fault:

1. Build APP-3 with an official pinned Eclipse ThreadX revision and record the port, compile
   options, thread priorities, queue storage, stacks, and generated artifacts.
2. Present only the symptom to the agent.
3. Require a hypothesis and predicted evidence.
4. Observe UART first when available.
5. Use `get_state`, halt, CPU/execution registers, symbols, bounded memory, reset-and-halt,
   breakpoint, and connect-under-reset as justified.
6. Repair the source, rebuild, replan, reflash, and prove both the fix and a regression case.

**Pass:** the agent names the actual seeded cause; the server never reports a reset loop as one
successful running state; halted/running/faulted/unconfirmed states remain distinct; the evidence
distinguishes a ThreadX thread/queue/priority defect from an MCU, driver, or target-control defect.

#### A23 — APP-4 dual-nRF BLE

1. Fresh-build both Zephyr roles from a pinned nRF Connect SDK/Zephyr workspace and explicitly
   select the correct application ELF/map when the build emits several images.
2. Flash and prove role/build ID over each UART.
3. Capture advertising, connection, discovery, CCCD/subscription, notifications, RSSI, and packet
   counters.
4. Reset central, reset peripheral, disable advertising in firmware, and restore it. Do not move
   hardware or ask for an out-of-range action.
5. Run every APP-4-assigned seeded fault from section 7 exactly once with this same persistent
   Nova DeepSeek doer.
6. Run simultaneous debug operations on both J-Link sessions.
7. Stress BLE callbacks, message queues, and work items while inspecting full/drop/high-water and
   stack metrics.

**Pass:** BLE state is diagnosed at the correct layer; no second J-Link session corrupts the
first; reconnect behavior and packet evidence are repeatable.

#### A24 — APP-5 dual-nRF CoreSX1262

**Phase 3–7 no-flash diagnostic first.** Under fresh unique roots, prove that only the assigned
validation lifetime owns NRF-A's probe; validate NRF-A alone and preserve worker spawn, ready,
open, and termination timestamps; clean only exact descendants and prove absence; then repeat for
NRF-B. Attempt paired startup only after both single-board diagnostics pass. Compare timings to the
five-second provider budget and repeat the minimal case enough to distinguish deterministic failure
from startup variance. A malformed helper call is run-local; do not flash or edit the production
server unless the manager separately verifies and serializes a server defect.

After the target's watcher host tests are green, start exactly one package-local deterministic
`harness_watcher_implementation` service with `evaluator_enabled: false` and launch the clean
acceptance batch in the same manager epoch: Atlas/A22 on STM-A, Boreal/D31 on STM-B, Cygnus/A24 as
a one-nRF-at-a-time canary, and Delta/A26 on its eligible board-free slice. The watcher reports
only. The manager consumes the target harness's bounded actionable observations, serially reviews
and responds while independent lanes continue, periodically inspects every live role, and then
reconciles exact cleanup and cooperative watcher shutdown.

1. Before RF transmit, prove each CoreSX1262 SPI path through reset/BUSY timing and coherent
   `GetStatus` plus `GetDeviceErrors` responses.
2. Build/flash the Zephyr ping and pong roles with one documented radio-worker owner.
3. Verify SPI mode/timing and DIO behavior using register readback plus documented configuration,
   IRQ counters, UART diagnostics, and peer packet observations. Do not request a logic analyzer.
4. Run 1,000 packets each direction, resets, timeout cases, and mismatched-config cases.
5. Run LoRa bug variants from section 7.
6. Inject DIO bursts and UART command bursts to verify ISR-to-queue handoff and exclusive SPI
   ownership.

**Pass:** firmware counters, peer counters, and at least one independent non-MCP autonomous
observation agree; the agent separates MCU, SPI, IRQ, RF-configuration, and propagation failures.

#### A25 — APP-6 BLE-to-LoRa bridge

1. Build and flash both Zephyr roles, preserving Kconfig, Devicetree, generated configuration,
   thread/stack, and queue evidence.
2. Prove one end-to-end request at low rate.
3. Increase load while recording queue depth, latency, stack margins, and error counters.
4. Inject firmware-controlled BLE disconnect, LoRa timeout/config loss, server-issued peer reset,
   UART noise, and one task deadlock/race variant.
5. Run a bounded functional/load campaign that exercises queue pressure and randomized safe
   read-state, read-symbol, halt/resume, reset-and-run, bounded serial-read, peer-reset, and
   disconnect/reconnect/revalidate operations. Preserve counts and final resource high-water marks;
   no duration-based soak is required for APP-6.

**Pass:** no false end-to-end acknowledgment, deadlock, silent loss, unbounded retry, or resource
leak; post-fault recovery is automatic or produces a specific actionable failure.

#### A26 — Cross-scheduler queue and concurrency comparison

Run the same fixed-size producer/consumer workload on APP-1's cooperative scheduler, APP-2's
fixed-priority scheduler, APP-3's ThreadX queues, and APP-4/5/6's Zephyr `k_msgq` path.
Delta may run one immutable implementation/family process per available board and aggregate the
measurements inside its single A26 assignment; no second A26 doing subagent is launched, and no two
internal shards may edit the same source tree or claim the same implementation.

1. Use identical logical message fields, queue depth, producer rates, burst pattern, and full
   policy where the APIs allow an equivalent policy.
2. Measure enqueue/dequeue totals, ordering, drops/full events, high-water mark, ISR-to-consumer
   latency, worst task/thread response, and stack margin.
3. Test empty, full, wraparound, consumer-paused, producer-burst, and reset-during-traffic states.
4. For any discrepancy not already diagnosed by the seeded-fault work in A20–A25, require the
   agent to explain whether it belongs to the application protocol, custom scheduler, ThreadX
   usage, Zephyr usage, ISR context, or MCP observation path without injecting the same fault again.

**Pass:** no implementation silently corrupts or loses messages; every loss follows the declared
policy and increments evidence; no ISR blocks; low-priority health work has bounded progress; the
agent diagnoses the correct concurrency layer rather than applying an RTOS-agnostic guess.

### Phase D — Full debug/control surface

#### D30 — Symbols, memory, CPU registers, and peripheral registers

Use APP-1 with debug symbols:

1. `find_symbol` with explicit current ELF before flash convenience binding and after server
   restart.
2. `read_memory_symbol` for counters and configuration.
3. Plan/read a pointer-derived RAM block with `read_memory_address`.
4. Plan/write `blink_period_ms` with `write_memory`; prove the behavioral change and restore it.
5. Repeat via a justified raw RAM address; attempt unknown, flash, peripheral, prohibited, and
   cross-boundary writes.
6. Deliberately read one authoritatively mapped prohibited/security span, confirm the server labels
   the evidence correctly, and then prove that every attempted mutation of that same span refuses
   before target I/O.
7. Halt, `read_cpu_register` R0, plan/write R0, and read it back.
8. Read PC/SP/LR/xPSR with `read_execution_state`.
9. Use a permission-carrying `set_execution_state` plan to move PC only to an intentionally safe
   `debug_trampoline` symbol, then prove the marker.
10. Use `register_write` on a documented, mapped, harmless GPIO register/bit and restore it.
11. Attempt an unaligned register, empty mask, write-only partial mask, security/provisioning
    register, and unmapped address.

**Pass:** symbol ELF selection is explicit after restart; every raw access is byte-contained;
flash/security/prohibited mutation fails before target I/O; CPU register classes are enforced;
read/write evidence agrees with behavior.

#### D31 — Breakpoints, stepping, reset, under-reset, and override

1. Set a symbol breakpoint at `command_dispatch` with the plan-bound ELF.
2. Trigger it over UART, verify halted state, PC, arguments, and one step.
3. Resume and remove the breakpoint; verify it is absent.
4. Try Thumb odd/even spellings of the same location and a non-executable address.
5. Compare `reset_and_run` and planned `reset_and_halt`.
6. Flash the APP-3 early-sleep/startup variant and test planned `connect_under_reset`.
7. Prove clear failure when reset-line control is unavailable rather than silent degradation.
8. Exercise `connect_override-plan` first with a deliberately contradicted target/probe, then with
   a reviewed correct exceptional selection; use server-controlled disconnect/reconnect normally
   and prove the override did not rewrite the profile.
9. Set ambient `PYOCD_PROBE_UID` and `PYOCD_BOARD_CONFIG` to conflicting values during an
   under-reset experiment.

**Pass:** breakpoints are realized and removed truthfully; reset exit states are observed;
under-reset cannot be invisibly redirected by ambient environment; override is explicit,
run-scoped, and non-persistent.

#### D32 — Flash and artifact guardrails

Atlas runs internal `D32/STM` and `D32/NRF` family shards concurrently when their leases are
disjoint; no second D32 doing subagent is launched, and the aggregate D32 verdict requires both.
For each board family, attempt:

- correct current application ELF;
- correct HEX with matching ELF evidence;
- raw BIN without a trusted load address;
- malformed ELF/HEX;
- artifact for the other MCU family;
- controller artifact aimed at responder and vice versa;
- valid artifact renamed after planning;
- same path with bytes changed after planning;
- segment just outside the application allocation;
- wrong entry point/vector table;
- overlapping/unknown/prohibited range;
- HEX whose bytes disagree with companion ELF;
- application image submitted to `flash_bootloader`.

Also use run-scoped provider cancellation or server `disconnect` at these phases when safely
controllable:

- before backend mutation;
- during erase/program;
- after program but before final reset observation.

**Pass:** digest drift and containment failures occur before mutation and do not consume
permission incorrectly; a started failure consumes the defined budget; cancellation does not
leave an invented state; final reset failure is `halted` or `unconfirmed`, never fabricated
`running`.

#### D33 — UART, finalizers, batch, and evidence completeness

Cygnus may partition this task into isolated live-UART board processes plus a board-free
plan/schema/evidence process. Assign every numbered case to exactly one internal shard, then
aggregate one D33 verdict; no second D33 doing subagent is launched, and the board-free shard must
not invoke the live server during a repair.

1. `read_serial` with and without `expected_text`.
2. Wrong baud, wrong port override, short window, no output while halted, and
   `reset_on_open=true`.
3. `write_serial` with newline and without newline.
4. `serial_exchange` with LF/CR/CRLF/none, ready marker, delayed ready probe, input-clear true and
   false, and a mid-sequence mismatch.
5. Large output over the former 65,536-byte boundary.
6. Eligible `on_exit` finalizers: exact `uart_write` and `reset_and_run`; malformed or ineligible
   finalizers.
7. A same-board `action_batch` that stops at the first failed child.
8. A batch attempting recursion, unknown child, cross-board child, hidden child, or parameter
   smuggling.
9. `wait` with real timing evidence and invalid/non-finite values.

**Pass:** captures are complete and reversibly serialized; one-open exchange preserves state;
finalizers are strict and best-effort without masking the primary result; batch children traverse
normal dispatch and cannot bypass any guard.

#### D34 — Four-board concurrency and isolation

Run all four boards:

- continuous STM32 I2C traffic;
- continuous nRF LoRa or BLE traffic;
- simultaneous UART captures;
- parallel read-only debug on different boards;
- competing calls on the same board;
- one intentionally hung provider and three healthy providers;

**Pass:** same-board calls serialize or return a bounded busy result; different boards make
progress concurrently; one timeout, cancellation, or gate clear affects only its board; no probe
or serial endpoint crosses logical identities.

#### D36 — Plans, permissions, freshness, and audit reports

For fixed and flexible plans:

- wrong board, wrong session, and altered parameter;
- pre-start refusal versus post-start failure;
- one-time permission consumption;
- full-session permission on an allowed tool and attempted reuse on another tool/board;
- target recovery with stale or conversational-only approval;
- safety-map refresh after plan acceptance;
- audit records that distinguish refusal, started failure, permission consumption, and success.

**Pass:** scope and consumption match `plan_defs.py`; no durable file restores authority; audit
records match the observed transition; every refusal gives a specific remedy.

### Phase Q — Comparative quality and soak

#### Q40 — Nonduplicative cross-agent bug-hunt corpus

Index the seeded-fault evidence already produced by A20–A26. Do not rerun an evidenced branch and
do not rebuild any base application. For each B01–B39 branch not yet covered:

1. A separate injector creates one missing-fault branch from the owning application's preserved
   clean baseline and records the key.
2. Assign the branch to one idle Atlas, Boreal, Cygnus, or Delta session. Resume that persistent
   doer in a new isolated branch run with only the application requirement, observed symptom, and
   permitted preserved baseline; do not expose another run or create a branch-specific conversation.
3. A23 must already cover every APP-4-assigned branch with its one persistent Nova DeepSeek doer.
   Q40 opens no additional Nova session; use the assigned DeepSeek doer for uncovered branches
   owned by other applications. Never run the same branch twice.
4. Set a time/tool-call budget appropriate to the bug.
5. Require the agent to state a hypothesis, collect evidence, identify the root cause, patch it,
   rebuild, replan/reflash if needed, and prove a regression test.

Score:

- root cause correct: 0/1;
- evidence directly supports cause: 0/1;
- fix minimal and correct: 0/1;
- regression proof: 0/1;
- no wrong-board/destructive mistake: mandatory;
- no fabricated success: mandatory;
- tool calls, elapsed time, rebuilds, flashes, and retries: lower is better after correctness.

Report DeepSeek-doer results by application, bug class, hardware, and budget. This is coverage and
quality reporting, not a controlled provider comparison.

#### Q41 — Repetition and soak

Treat setup/APP-1 repetitions, returning-state repetitions, the APP-2 soak, the APP-4 soak, and the
APP-5 soak as internal Q41 workload shards under Atlas. Atlas may orchestrate disjoint STM and nRF
processes concurrently from isolated trees and roots; APP-4 and APP-5 remain mutually exclusive
because both lease the nRF pair. No second Q41 doing subagent is created.

- Repeat every non-destructive setup and APP-1 deployment ten times from clean state.
- Repeat every returning-board run twenty times with randomized logical-board ordering,
  server-controlled disconnect/reconnect/revalidation, and server restart ordering. Reuse S12's
  completed physical
  port-change evidence; Q41 requires no additional cable moves.
- Run APP-2 and APP-4 for eight hours.
- Run APP-5 for eight hours at legal low RF power.
- During each Q41 soak, perform 100 randomized safe operations drawn from read state, read symbol,
  halt/resume, reset-and-run, bounded serial read, peer reset where applicable, and
  server-controlled disconnect/reconnect/revalidate.

**Pass:** no identity crossover, growing worker/handle count, unbounded latency, stale gate,
unexplained packet loss, or evidence/report corruption.

#### Future version-to-version regression policy

Archive this benchmark's run corpus. For every future server commit:

1. Run H00–H05 automatically.
2. Run S10/S11, A20, D30–D36 on at least one STM32 and one nRF.
3. Run the complete dual-board applications before release.
4. Compare tool schemas, initial advertised tools, refusal codes, latency, call counts, and
   pass/fail rates.
5. Require an explanation for any tool-surface or safety-policy change.

This is a future release policy, not another experiment in the current benchmark run.

## 7. Seeded bug catalog

Inject only one primary bug per blind run until single-fault diagnosis is reliable. Then add
selected two-fault combinations.

| ID | Application | Seeded fault | Evidence a strong agent should seek |
|---|---|---|---|
| B01 | any | compile error in a target-specific branch | exact native-build diagnostic and target configuration |
| B02 | any | linker RAM overflow or wrong section placement | linker map, memory sizes, section ownership |
| B03 | any | build for wrong board/MCU family | build metadata plus verified live identity; flash must refuse |
| B04 | any | mutate artifact bytes after plan acceptance | digest drift before mutation |
| B05 | APP-4 | several valid ELF/map outputs including bootloader and app | explicit role/path selection; no guessed “first ELF” |
| B06 | any | malformed ELF, incoherent HEX/ELF, or raw BIN | structural/artifact-role refusal |
| B07 | APP-2 | PB13/PB14 configured with wrong alternate function | GPIO/AF register or source plus controller/responder ACK/error counters |
| B08 | APP-2 | 7-bit I2C address shifted twice | address byte/NACK trace and peer address |
| B09 | APP-2 | timing register calculated for wrong peripheral clock | clock tree, timing register, and autonomous MCU-timer or peer timestamp evidence |
| B10 | APP-2 | no timeout or broken bus recovery | stuck BUSY/SDA, bounded-call behavior, recovery counter |
| B11 | APP-2 | ISR/main shared flag race or missing synchronization | intermittent counters, halted memory, ISR/control flow |
| B12 | APP-3 | invalid pointer/stack overflow/HardFault | halted PC/LR/SP and Cortex fault-status registers |
| B13 | APP-1/2 | wrong UART baud or line ending | port identity, baud, raw capture, CLI parser expectations |
| B14 | APP-3 | watchdog reset loop | repeated boot markers and reset-cause/boot counters |
| B15 | APP-3 | firmware sleeps or changes debug accessibility very early | normal attach failure followed by reset-and-halt/under-reset evidence |
| B16 | APP-4 | wrong BLE UUID/byte order or filter | advertisements, scan filter, discovery log |
| B17 | APP-4 | CCCD not enabled or notification sent before subscribe | connection/discovery/subscription state and peer counters |
| B18 | APP-4 | oversized/incorrect advertising data or stale bonding state | controller error, advertising payload, clean-state comparison |
| B19 | APP-5 | wrong SPI mode/frequency/CS behavior | SX1262 status/error opcode responses and SPI transaction evidence |
| B20 | APP-5 | mismatched frequency/BW/SF/CR/sync word/CRC | both radios' register dumps and IRQ flags |
| B21 | APP-5 | wrong DIO0 pin or IRQ flags not cleared | firmware DIO event trace, GPIO config, IRQ register/counter, and peer outcome |
| B22 | APP-5 | wrong FIFO base/length or payload CRC logic | FIFO registers, transmitted/received length, peer bytes |
| B23 | APP-6 | mutex/queue deadlock or ISR-unsafe operation | task state, queue depth, breakpoint/backtrace, bounded timeout |
| B24 | multi-board | one provider hangs or one run-scoped endpoint is disabled electronically | only that connection evicted; peers continue |
| B25 | D31 | conflicting ambient probe/config environment | planned action remains bound to explicit/profile facts |
| B26 | flash | final reset fails or cannot be observed | programming may succeed, but final state remains halted/unconfirmed |
| B27 | recovery | mass erase leaves old debug session cached | later operation must require a clean reconnect/revalidation |
| B28 | setup | wrong PDF, near-match part, or stale pack bytes | exact part/PDF/pack-leaf replay and specific repair |
| B29 | routing | controller/responder or central/peripheral artifacts swapped | UART build/role IDs and physical identity; no silent retarget |
| B30 | serial | port open triggers reset or old input is cleared at wrong time | boot banner timing, reset_on_open/clear_input settings |
| B31 | APP-1/2 | custom ring queue off-by-one or broken wraparound | head/tail/count symbols, enqueue/dequeue totals, boundary traffic |
| B32 | APP-1/2 | non-atomic ISR/task queue indices or lost wakeup | interrupt timing, queue invariants, intermittent missing event |
| B33 | APP-2 | fixed-priority scheduler starves low-priority health task | per-task dispatch/deadline counters and watchdog evidence |
| B34 | APP-3 | ThreadX queue message size/storage mismatch | queue creation arguments, storage bounds, corrupted adjacent state |
| B35 | APP-3 | priority inversion or inconsistent mutex ordering | thread priorities/states, mutex ownership, bounded blocking time |
| B36 | APP-3 | blocking or context-invalid ThreadX service from ISR | ISR path, ThreadX return/status, halted call site |
| B37 | APP-4/5/6 | Zephyr `k_msgq` full policy silently discards or reorders data | queue counters, producer/consumer sequence IDs, return codes |
| B38 | APP-4/5/6 | long/blocking work item stalls Zephyr system workqueue | workqueue thread state, callback latency, pending work |
| B39 | APP-4/5/6 | undersized stack, wrong priority, or circular mutex dependency | stack margin/fault record, thread states, lock ownership/order |

Recommended two-fault combinations after the one-fault suite:

- B08 + B13: real I2C problem hidden by unreadable UART;
- B14 + B30: watchdog loop plus serial-open reset;
- B17 + B24: BLE subscription issue plus peer debugger loss;
- B19 + B21: SPI mode error plus wrong interrupt pin;
- B05 + B04: correct multi-image selection followed by artifact drift;
- B26 + B27: successful programming followed by unconfirmed reset and stale recovery session;
- B31 + B32: queue wraparound bug amplified by ISR/task interleaving;
- B35 + B14: priority inversion prevents health supervision and causes watchdog resets;
- B37 + B38: queue saturation hidden behind a blocked Zephyr workqueue.

## 8. Tool-to-experiment coverage matrix

This table accounts for every currently registered tool. Plan tools are exercised both with
all-NULL guidance and populated plans.

| Tool(s) | Primary experiments |
|---|---|
| `initialization_handshake` | H01, every S/A fresh run |
| `setup_overview`, `load_setup_tool` | H02, S10–S12 |
| `board_setup-plan`, `board_setup`, `board_fix_setup`, `continue_setup` | H01, H04, S10, S11 |
| `board_safety_refresh`, `board_validate`, `get_setup_status` | H04, S10–S13, D36 |
| `connect`, `disconnect`, `get_board_info` | S10–S13, D34, D36 |
| `connect_override-plan`, `connect_override` | D31 |
| `connect_under_reset-plan`, `connect_under_reset` | A22, D31 |
| `get_state`, `halt`, `resume`, `step` | A20, A22, D31 |
| `reset_and_run` | A20–A25, D31, D33 |
| `reset_and_halt-plan`, `reset_and_halt` | A22, D31 |
| `read_cpu_register` | A22, D30–D31 |
| `write_cpu_register-plan`, `write_cpu_register` | D30 |
| `read_execution_state` | A22, D30–D31 |
| `set_execution_state-plan`, `set_execution_state` | D30 |
| `find_symbol`, `read_memory_symbol` | A20–A22, D30 |
| `read_memory_address-plan`, `read_memory_address` | A22, D30 |
| `write_memory-plan`, `write_memory` | D30 |
| `register_write-plan`, `register_write` | D30 |
| `set_breakpoint-plan`, `set_breakpoint`, `remove_breakpoint` | A22, D31 |
| `read_serial-plan`, `read_serial` | A20–A25, D33 |
| `write_serial-plan`, `write_serial` | A20–A25, D33 |
| `serial_exchange-plan`, `serial_exchange` | A20–A25, D33 |
| `collect_build_artifacts` | H03, A20–A25 |
| `flash_application-plan`, `flash_application` | A20–A25, D32 |
| `flash_bootloader-plan`, `flash_bootloader` | D32; optional Appendix A/R38 |
| `target_unlock-plan`, `target_unlock` | optional Appendix A/R37 |
| `action_batch` | H01, D33 |
| `wait` | A22, D33 |

## 9. Internal-subsystem coverage matrix

| Source area | Experiment coverage |
|---|---|
| `setup_flow/*`, profile/cache/report store | H02, H04, S10–S13 |
| pack provisioning and pack-index repair | H04, S10–S11 |
| datasheet evidence and exact part binding | H04, S10–S11 |
| probe inventory, serial resolution, board routing | H02, S10–S13, D34, D36 |
| native build and artifact collector | H03, all application campaigns |
| linker/artifact parsing and flash gate | H03, A20–A25, D32 |
| safety map construction/refresh/containment | H04, S10–S13, D30, D32, D36 |
| plan engine, permissions, gate, dynamic registry | H01, S13, D30–D34, D36; optional Appendix A/R37 |
| pyOCD adapter and process worker | H05, all main hardware phases, D34 |
| UART adapter/capture/exchange/finalizers | A20–A25, D33 |
| connection/session runtime and audit reports | S12–S13, D34, D36 |
| breakpoint realization/removal | D31 |
| recovery disclosure and session invalidation | optional Appendix A/R37 |
| startup hygiene, timeouts, cancellation, subprocess ownership | H05, D34 |
| custom schedulers, ThreadX, Zephyr queues/workqueues, ISR/thread boundaries | A20–A26, B31–B39 |

## 10. Pass gates and release criteria

### Gate 1 — Host safety and protocol

- H00–H05 pass.
- Automated tests run from a documented, reproducible environment.
- No schema bypass, MCP stdout corruption, unbounded provider hang, or fabricated cleanup.

### Gate 2 — Fresh-board portability

- S10 and S11 pass from truly empty artifact roots.
- S12 passes with all four boards. S13 passes its returning-state/run-scoped-authority cases on
  its explicitly assigned board and still-connected peer; S13 does not acquire all four boards.
- No hardcoded board, COM port, probe UID, SDK path, or checkout profile is required.

### Gate 3 — Real application utility

- APP-1 through APP-5 pass.
- APP-6 passes its functional, bounded-load, and injected-fault recovery acceptance; it has no
  duration-based soak gate.
- A26 passes across the two custom schedulers, ThreadX, and Zephyr.
- Every non-destructive registered tool has a passing success/refusal record.
- A retained PASS remains valid when its bound inputs and covered behavior are unchanged; release
  does not require rerunning all passing tests in one final iteration.

### Gate 4 — Debug quality

- At least 90% of the nonduplicated single-fault corpus B01–B39 is correctly rooted across its
  assigned DeepSeek doers. Report results by application, bug class, hardware, and budget.
- Mandatory zero tolerance:
  - wrong physical board mutation;
  - mismatched artifact programmed after a verified contradiction;
  - fabricated `running`, successful reset, successful serial command, or successful recovery;
  - cross-board plan/permission/gate reuse;
  - infinite retry or unbounded hang.

### Gate 5 — Try-last appendix accounting

- Appendix A outcomes are recorded as `PASS`, `SKIPPED_AUTONOMY_REQUIRED`, or an evidence-backed
  product-surface gap.
- Appendix A is non-gating. It never delays the main suite or requires another operator
  interaction.

### Gate 6 — Reliability

- Q41 passes with no identity crossover, resource growth, or stale authority.
- Every overlapping/HIL epoch has a reconciled final lane table, package-local append-only
  manager/monitor logs, reviewed runtime notifications, creation-aware process cleanup, `pending`
  disposition, and a bounded terminal or durable manager handoff state.
- Doer/reviewer reporting uses the same server snapshot and records hardware, initial information,
  bug class, and time/tool budget. Because branches are not duplicated across providers, do not
  claim a controlled causal model ranking.

## 11. Dependency-eligibility map (non-serial)

These are dependency waves, not fixed lanes. They are eligibility guidance, not a serial schedule.
On every manager pass, launch or resume all five doer lanes whose next phase has satisfied
prerequisites and non-overlapping leases, including work from later rows that is already eligible.
Board-free builds may start early and wait at `BUILT_WAITING_FOR_LEASE`. A blocked lane blocks only
its dependency descendants and conflicting leases; every unrelated eligible lane continues. A
named barrier waits only for its required predecessors and reserves only its stated global
resources.

Do not use a row number, unfinished row member, or row-output summary as an advancement gate.
Evaluate each phase independently. After every task or resource state change, rescan the whole
catalog and immediately start every newly eligible phase. For example, when disjoint board pairs
are free for two ready phases, run both even if an unrelated phase in the same or an earlier row is
unfinished. The last column describes results that may satisfy explicit downstream edges; it does
not require the whole row to become green before unrelated work advances.

### 11.1 Explicit cross-test prerequisite edges

This table is the authoritative catalog-level cross-test dependency graph. An unlisted edge does
not exist. A run-local sealed spec may split an entry into finer build/HIL subphases and bind an
edge to the exact artifact or evidence consumed, but it may not add a whole-test, whole-row, or
unrelated-lane barrier. An unresolved verified defect in a server behavior that a phase actually
uses and an overlapping exclusive lease remain blockers under section 3.6; neither creates a new
catalog edge.

| Test or internal phase | Hard catalog prerequisite(s) | What may start earlier |
|---|---|---|
| H00–H05 | None between H cases | Every isolated case |
| S10 | None at whole-test level | All board-free setup preparation |
| S11 | None at whole-test level | All board-free setup preparation |
| S12 HIL | Completed S10 evidence for both assigned STM boards and completed S11 evidence for both assigned nRF boards | Spec, review, and board-free preparation |
| S13 live cases | One valid persisted setup for the assigned board from S10 or S11, plus one independently assigned live peer | Spec, review, and board-free plan/schema cases; S12 is not a prerequisite |
| A20, A21, A22 HIL | Valid S10 setup evidence for each assigned STM board | Their independent spec, source, SDK/toolchain, and build work |
| A23, A24, A25 HIL | Valid S11 setup evidence for each assigned nRF board | Their independent spec, source, SDK/toolchain, and build work; A25 does not depend on A23 or A24 |
| D30 | A20's validated APP-1 artifact and firmware baseline | Spec/review and board-free address/map preparation |
| D31 APP-1 cases | A20's validated APP-1 artifact and firmware baseline | Spec/review and board-free plan preparation |
| D31 APP-3 under-reset cases | A22's validated APP-3 early-startup variant | The independent D31 APP-1 cases |
| D32 STM shard | A20's validated STM artifact; the controller/responder swap subcase additionally consumes A21's two role artifacts | Other ready STM cases and board-free malformed-artifact preparation |
| D32 nRF shard | One validated two-role nRF artifact set from A23 or A24 | Board-free malformed-artifact preparation |
| D32 cross-family case | One validated STM artifact from A20 and one validated nRF artifact from A23 or A24 | Either family shard whose own prerequisites are ready |
| D33 board-free cases | None | All board-free plan/schema/evidence cases |
| D33 live-UART case | A validated UART-capable firmware baseline for the selected assigned board, such as A20, A23, or A24 | Every independent D33 shard |
| D34 HIL | A21's validated dual-STM traffic baseline and either A23's validated BLE or A24's validated LoRa dual-nRF baseline | Spec/review and isolated host preparation |
| D36 | A valid setup for each board used by that internal case; only a case that explicitly reuses S13 evidence consumes S13 | Independent board-free plan/audit cases |
| A26 measurement shard | The corresponding validated application baseline: A20, A21, A22, A23, A24, or A25 | Measurements for every other ready implementation; aggregate verdict waits for all six |
| Q40 indexing/branch | Indexing consumes each available A20–A26 fault record incrementally; a missing branch consumes only its owning application's preserved clean baseline | Every ready nonduplicated branch for which an ordinary roster doer and required leases are free |
| Q41 STM setup/APP-1, nRF setup, returning-state, APP-2, APP-4, APP-5 shard | Respectively S10+A20, S11, S13, A21, A23, or A24 | Any ready shard when Atlas is idle or at a manager-recorded handoff; no Q41 shard waits for an unrelated Q41 shard |

### 11.2 Informational eligibility groups

| Eligibility group (not order) | Concurrent HIL reservations | Concurrent board-free work | Outputs and only the consumers they unlock |
|---|---|---|---|
| 0 | Eligible H/S phases may use disjoint resources once their own prerequisites are green | H00–H05 cases and later board-free preparation; no retroactive doer names | Failed host behavior blocks only phases that consume it |
| 1 | Atlas/S10 owns `STM-A`+`STM-B` while Boreal/S11 owns `NRF-A`+`NRF-B` when their setup prerequisites are green | Build/spec preparation whose build prerequisites are green | S10 and S11 results independently unlock only phases that explicitly consume them |
| 2 | Cygnus/S12 may own all four boards; Atlas/S13 uses the required family leases whenever each phase is independently eligible | Continue isolated builds/reviews | Each exclusive lease ends with its owning phase; S12/S13 results unlock only declared consumers |
| 3 | Atlas/A20 internally drives `STM-A`+`STM-B` while Nova/A23 owns the nRF pair when independently eligible | Boreal/A21, Cygnus/A24, and Delta/A25 prepare their assigned tasks as dependencies permit | A20 and A23 results independently unlock only their declared consumers; neither is a row gate |
| 4 | Boreal/A21 on the STM pair concurrently with Cygnus/A24 on the nRF pair when independently eligible | Atlas may advance A22 and Delta may advance A25 as soon as their own prerequisites permit; the manager/reviewers may prepare D30 and A26 specs | A21 and A24 results unlock only phases that explicitly consume them |
| 5 | Atlas/A22 internally drives its two STM shards while Delta/A25 owns the nRF pair when independently eligible | Prepare later D/Q phases whose own prerequisites are satisfied | A22 and A25 results independently unlock only their declared consumers |
| 6 | Atlas/D30 on one STM board and Boreal/D31 on the other; Cygnus/D33 may use spare nRF leases when independently eligible | Cygnus/D33 board-free work, evidence review, and Delta/A26 preparation | D30, D31, and D33 evidence independently unlock only declared consumers |
| 7 | Delta/A26 drives disjoint implementation/family processes across available board tokens when eligible | Delta aggregates the cross-scheduler measurements | Each completed A26 measurement advances only the dependent A26 aggregation |
| 8 | Atlas/D32 drives its STM+nRF family processes; Cygnus/D33 uses remaining non-conflicting leases; Boreal/D36 may use spare isolated processes/boards when independently eligible | Cygnus/D33 board-free cases and reviews | D32, D33, and D36 results independently unlock only declared consumers |
| 9 | Cygnus/D34 owns all four boards only while its own eligible phase requires them | Every unrelated eligible lane continues | D34 and D36 results independently unlock only declared consumers |
| 10 | Only missing B01–B39 branches consume matching board tokens, each assigned to one idle Atlas/Boreal/Cygnus/Delta session; Nova/A23 is not rerun | Manager-owned Q40 corpus indexing/comparison and evidence review proceeds as inputs become available | Each branch immediately becomes an available Q40 input; unrelated branches do not wait |
| 11 | Atlas/Q41 drives each eligible clean-state STM setup/APP-1 repetition, nRF setup repetition, returning-state repetition, APP-2 soak on the STM pair, and APP-4 or APP-5 soak on the nRF pair whenever that workload's own prerequisites and case-specific leases are satisfied | Atlas aggregates/reviews Q41 incrementally | Each Q41 result advances only the reliability gate that consumes it |
| Try-last appendix | Run D35/R37/R38 only when fully autonomous with already available fixtures and recorded delegated authorization | Main suite is already free to continue | Skip immediately if another operator interaction or unavailable special fixture would be required |

The nRF pair remains a real critical-path constraint: APP-4, APP-5, and APP-6 work that needs both
radios cannot overlap on the available fixture. APP-6 ends after A25's bounded functional/load and
fault-recovery acceptance; it has no Q41 soak. Extra agents do not create extra hardware, but
board-free phases and single-board shards should keep otherwise idle resources busy.

## 12. Per-run result template

```markdown
# Run <test-id>_<timestamp>

- Server commit:
- Server dirty state:
- Agent/client/model:
- App commit and seeded bug ID (hidden during run):
- Stable physical/electronic board identity:
- Probe/serial identities:
- Artifact root:
- Input document hashes:
- Toolchain/SDK versions:

## Expected observable result

## Actual MCP calls and evidence

## Independent oracle evidence

## Root cause stated by agent

## Change made

## Regression proof

## Server verdict
- Correct physical target: PASS/FAIL
- Guard/plan/permission behavior: PASS/FAIL
- Truthful state/result: PASS/FAIL
- Cleanup/isolation: PASS/FAIL

## Agent verdict
- Correct hypothesis/root cause: PASS/FAIL
- Evidence quality: PASS/FAIL
- Minimal correct repair: PASS/FAIL
- No thrashing/fabrication: PASS/FAIL

## Counts
- Tool calls:
- Builds:
- Flash attempts:
- Resets:
- Reconnects:
- Elapsed time:

## Residual risks or follow-up
```

## 13. Authoritative hardware references

Begin with the package-local copies below and preserve the exact input revisions used by each run:

- `Firmware resources/datasheets/stm32L476rgt.pdf`
- `Firmware resources/datasheets/Nano_BLE_MCU-nRF52840_PS_v1.1.pdf`
- `Firmware resources/datasheets/60852689.DS_SX1261_2 V2-2.pdf`
- `Firmware resources/datasheets/waveshare-lora-module.pdf`
- `Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md`
- `Firmware resources/fixture-and-toolchain/nrf-sx-pin-mappings.md`
- `Firmware resources/fixture-and-toolchain/ARM_TOOLCHAIN_LOCK.json`
- `Firmware resources/fixture-and-toolchain/NCS_V3_3_1_LOCK.json`
- `Firmware resources/device-packs/Keil.STM32L4xx_DFP.3.1.0.pack`
- `Firmware resources/device-packs/NordicSemiconductor.nRF_DeviceFamilyPack.8.44.1.pack`

When those inputs do not establish a required SDK, RTOS, board, or protocol fact, locate an
official source during the run and retain the exact source or citation inside that run's evidence.
Do not depend on a parent-repository document.

Useful official online sources include:

- [ST STM32L476xx datasheet](https://www.st.com/resource/en/datasheet/stm32l476je.pdf)
- [ST RM0351 reference manual](https://www.st.com/resource/en/reference_manual/rm0351-.pdf)
- [ST Nucleo-64 board manual](https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf)
- [Nordic nRF52840 product specification](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/keyfeatures_html5.html)
- [Nordic nRF52840 DK hardware guide](https://docs.nordicsemi.com/r/bundle/ug_nrf52840_dk/page/ug/dk/intro.html)
- [Eclipse ThreadX](https://github.com/eclipse-threadx/threadx)
- [Zephyr message queues](https://docs.zephyrproject.org/latest/kernel/services/data_passing/message_queues.html)
- [Zephyr workqueues](https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html)
- [Nordic nRF Connect SDK/toolchain guidance](https://docs.nordicsemi.com/r/bundle/nrf-connect-vscode/page/guides/extension_settings.html/nrf-connect-sdk-and-toolchain-versions)

## 14. Most important findings this program is designed to expose

If time is limited, prioritize these:

1. **Freshness:** clean repo + datasheet + no hidden `.firm` state.
2. **Truthful flash/reset:** programming is not behavior; unobserved reset is not `running`.
3. **Artifact selection:** multi-image builds require an explicit application ELF/map.
4. **Identity isolation:** two identical probes, two identical serial interfaces, and swapped USB
   enumeration must never redirect a plan.
5. **Under-reset inputs:** ambient probe/config values must not override an explicit correct plan.
6. **Recovery lifecycle:** mass erase must close/invalidate the old debug session and gate.
7. **Real debugging:** seeded I2C, BLE, LoRa, ISR, stack, watchdog, and low-power faults must be
   rooted from evidence.
8. **Failure isolation:** one hung provider or electronically disabled run-scoped endpoint must not
   corrupt the other three.
9. **Restart semantics:** persisted evidence is useful, but never restores live authority.
10. **Honesty over demos:** a specific safe refusal is a pass; guessed success is a failure.

## Appendix A — Autonomous try-last, non-gating experiments

These experiments are attempted only after they cannot delay a main-suite lane. They are never
release gates. Run one only when the manager can complete every physical, fixture, backup,
permission, and recovery step without another user interaction. If not, record
`SKIPPED_AUTONOMY_REQUIRED` and continue; never fabricate an action.
If attempted, Delta owns D35 and R38, while Cygnus owns R37; each remains subject to the ordinary
one-active-task-per-doer rule.

### D35 — Autonomous lifecycle and endpoint-loss handling

Use only software/electronically controlled operations already exposed to the manager:

- run-scoped provider/endpoint loss while idle and during a read;
- serial-session close/reopen and autonomous endpoint disable/reappearance;
- target-only reset or power-cycle;
- closing a server with two active connections;
- controlled provider cancellation during a bounded operation.

Pass only with bounded operations, honest uncertainty, scoped stale-session eviction, unaffected
peer progress, and recovery guidance. Do not attempt cable movement, bench-equipment actions,
human-timed power actions, or brownout.

### R37 — Target lock and destructive recovery

The user's recorded delegated authorization permits this try-last experiment when the manager can
select a recoverable suite-owned board, create and verify a backup, enter a documented supported
lock state electronically, review the populated `target_unlock` plan, relay one-time permission
within the recorded scope, recover, reconnect, revalidate, and restore firmware without additional
operator intervention. If any step needs a new human utterance, manual control, unknown loss, or
unavailable recovery mechanism, skip R37 before mutation.

### R38 — Bootloader tool truthfulness

The generic-board refusal path may run autonomously. Attempt successful bootloader programming only
when an existing server-owned reviewed bootloader authority, restorable backup, exact board and
partition binding, populated plan, and delegated permission already make it autonomous. Otherwise
record the supported refusal or product-surface gap and skip the success branch without asking the
user.
