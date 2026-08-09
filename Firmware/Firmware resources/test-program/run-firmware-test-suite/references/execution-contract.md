# Fresh Firmware Test Execution Contract

## Contents

1. Suite state machine
2. Harness-assisted parallel coordination
3. Test specification rules
4. Isolation and allowed inputs
5. Test-agent model and continuity contract
6. Main-model review
7. Server-failure escalation
8. Recovery and resumption

## 1. Suite state machine

Use these durable states:

```text
CREATED -> SPEC_READY -> SPEC_REVIEWED -> AGENT_RUNNING
AGENT_RUNNING -> PASS_CLAIMED -> (ADVERSARIAL_EVIDENCE_REVIEW) -> MAIN_REVIEW -> GREEN
AGENT_RUNNING -> SERVER_FAILURE -> MAIN_VERIFIED_SERVER_FAILURE
MAIN_VERIFIED_SERVER_FAILURE -> REPAIR_BARRIER -> CHANGE_LOOP -> SERVER_FIXED -> AGENT_RUNNING
```

Never transition `PASS_CLAIMED` directly to `GREEN`. After sealing, one persistent read-only
reviewer first writes `SPEC_ADVERSARIAL_REVIEW.md`; the main model records the one resulting spec
approval before the test agent starts. Every structurally valid PASS then resumes that exact
reviewer for the evidence review in `ADVERSARIAL_REVIEW.md`; `RUN_STATE.json` remains
`PASS_CLAIMED` until main review records a verdict. Never create a replacement test agent to escape
a red state. Persist the test-agent and reviewer identities, canonical task names, and models in
the run state as soon as they are spawned. A test-agent replacement is allowed only under
`model-continuity-contract.md`, with a durable recorded handoff.

`AGENT_RUNNING` may be temporarily coordinated as `PAUSE_REQUESTED`, `CHECKPOINTED`, or `FROZEN`
in the suite ledger. Those are not `RUN_STATE.json` terminal statuses and do not create or alter
`RESULT.json`. The exact persistent agent resumes from the recorded checkpoint.

Temporary resource/provider absence is similarly recorded only as `WAITING_FOR_RESOURCE` or
`WAITING_FOR_PROVIDER` in the suite ledger. Main-catalog runs never terminate as `NEEDS_USER` or
`INFRA_BLOCKED`, never request physical/operator intervention, and never stop unrelated lanes.

Every main-catalog-required behavior remains a hard release gate; Appendix A, optional
recommendations, and catalog-unsupported spec prerequisites do not. On a non-intentional failure,
block that test, its dependency descendants, and conflicting resource leases. Every unrelated
dependency-ready phase continues. A verified production server defect opens a barrier for
server-consuming and HIL
phases, but isolated board-free work that does not invoke the server may continue. The main model uses
change-loop only for a verified production-code defect; it must not use it for firmware, fixture,
SDK, host, specification, evidence, documentation-only, or metadata-only work. Rerun the exact
failed behavior before its gate becomes green. An intentional refusal/negative case passes only
when its specified refusal behavior is observed.

## 2. Harness-assisted parallel coordination

The suite uses one authoritative main-model manager and a five-session roster-owned doer pool: Atlas,
Boreal, Cygnus, Delta, and Nova. These are execution lanes, not fixed STM/nRF/host resource lanes.
Concurrency is bounded by one active task per doer, satisfied dependencies, isolated workspaces,
launcher/host capacity, and exact phase resource leases. The physical board tokens are `STM-A`,
`STM-B`, `NRF-A`, and `NRF-B`; board-free work may overlap them.

Treat concurrency as an affirmative scheduling requirement. On every scheduling pass, evaluate all
five lanes and launch or resume every eligible non-conflicting lane in the same batch. Never wait
for a blocked lane before advancing unrelated work. A dependency wave is an eligibility map, not a
serial queue; its row number, row membership, and row completion are never prerequisites. Compute
readiness per phase from explicit prerequisite edges, selective server-repair state, and required
resource leases, including the isolated workspace and doer/provider/launcher execution slot.
Catalog section 11.1 is the authoritative cross-test edge list. A sealed run may refine a listed
edge down to the exact consumed artifact/evidence phase, but it may not add an unlisted whole-test,
whole-row, or unrelated-lane dependency.

Whenever roles overlap, or any HIL/server-consuming epoch is active, start exactly one
`orchestrator_harness` managed watcher from a fresh suite-epoch config whose `run_globs` cover
every run the epoch may activate. The watcher is read-only; the current high-level session is the
sole manager. Record the watcher/owner PID identities and creation times, config hash, output
paths, manager/monitor logs, and heartbeat lease below
`multi-agent-logs/orchestrator-harness/<epoch>/`.

The manager consumes one durable actionable notification at a time, inspects its named lane and
the compact whole-suite state, performs any exact relay/recovery/lease decision itself, and then
acknowledges the exact event ID. The same watcher self-arms after acknowledgement. During active
HIL, inspect every live doer normally every two to three minutes and renew the watcher heartbeat
before expiry during longer reviews. Never acknowledge a notification without reviewing it.
Never use the watcher to launch, stop, approve, relay, classify, or repair.

Derive controller lanes from exact doer/task/session facts. Scope request/helper/MCP record formats
that support it with the exact manager-assigned `declared_lane_id`; it overrides any reused
persistent session ID. Historical lifecycle
conditions are baselined on watcher startup, not replayed as current work, while persistent safety,
request, conflict, provider, and manager-signal conditions remain actionable.

The main model maintains:

- `.agent-workspace/SUITE_COORDINATION.md`, containing manager identity, optional informational
  eligibility group (never an advancement gate), server snapshot, catalog test, canonical doer
  name, provider agent/session and reviewer identities,
  build/HIL dependencies, internal shards, phase-specific leases, process/runtime identities, and
  phase states; and
- `.agent-workspace/SERVER_REPAIR_QUEUE.md`, containing only manager-validated production-server
  defects and their evidence, disposition, repair slice, and targeted retest state.

Before HIL starts or resumes, the manager writes the run-local
`.agent-workspace/RESOURCE_ASSIGNMENT.md` with catalog ID, internal shard/phase, canonical doer
name, `HIL_RUNNING`, assigned server snapshot, exact leases, assignment time, and manager identity.
The test owner treats it as
read-only. This run-local copy lets an isolated agent verify authority without reading suite-root
state. When a phase may reach a permission-bearing live plan, the assignment also binds the
applicable delegated-authorization artifact path and SHA-256. Without that exact binding, the
agent must not infer a grant.

Use the following prompt-driven protocol:

1. Record one authoritative manager. A doer name identifies one persistent session. Assign each
   catalog test to one doer from `doer-roster.md` and record the doer separately from its provider
   identity. A doer runs only one task at a time but may receive a later roster task after a
   terminal or manager-checkpointed handoff. On every resume, inspect live processes and the ledger.
   Never permit two doers on one task, two live sessions under one doer name, or duplicate
   controllers for a persistent role or `CL_RUNTIME_DIR`.
   Immediately after reconciliation, fill every eligible lane; do not leave a lane idle merely
   because another lane is waiting on a provider, board, fixture, review, or dependency.
2. Record one immutable server snapshot for every server-consuming phase: Git HEAD, dirty status,
   and a stable diff/tree fingerprint. Each HIL owner starts a separate MCP process and state root
   from that snapshot unless the sealed test explicitly evaluates shared-process behavior.
   For a Codex CLI role inheriting the configured `byo-firmware` server, set per-process
   `mcp_servers.byo-firmware.cwd` and
   `mcp_servers.byo-firmware.env.BYO_MCP_ARTIFACT_ROOT` overrides on its launcher. Confirm the
   effective config and first public artifact/event path; if either escapes the assigned root,
   checkpoint at the next safe boundary and correct the launcher before retesting.
3. Before each phase, lease all execution, physical, and host-global resources it may use or
   mutate: doer/provider/launcher execution slot, isolated workspace, friendly board, probe UID,
   serial endpoint, peer/radio, autonomous electronic control actually used,
   USB-enumeration or power scope actually affected, server lifecycle, and mutable
   artifact/cache/state roots. External lab instruments and manual controls are not prerequisites
   and are never requested. Exclusive leases may not overlap. Only the
   manager writes assignments; an agent never self-acquires hardware.
4. Track `SPEC_READY`, `BUILDING`, `BUILT_WAITING_FOR_LEASE`, `HIL_RUNNING`, `CHECKPOINTED`, and
   `PASS_CLAIMED` in the suite ledger, separately from terminal `RUN_STATE.json`. A build starts
   when build prerequisites and host leases are ready. HIL starts only after its HIL prerequisites,
   assigned server snapshot, and hardware leases are ready.
5. Future specs, read-only spec reviews, and isolated board-free builds may run while hardware
   tests run. A completed build records an immutable artifact/configuration handoff and stops at
   `BUILT_WAITING_FOR_LEASE`; it grants no hardware authority.
6. A catalog item may define independent board/family shards, but they are internal phases owned
   by that task's assigned lane doer. Each shard needs immutable scope, an isolated
   application/build tree, and unique leases. The doer may orchestrate concurrent processes but
   may not delegate a shard to a second doing subagent. The manager records one catalog verdict
   after verifying the aggregate coverage map. Sharding may not duplicate or omit coverage.
7. A verified production-server defect stops new server-consuming/HIL launches. The manager writes
   `PAUSE_REQUESTED.md` only into active server/HIL runs. Each affected agent checks for it between numbered
   requirements and bounded soak/repetition epochs. After any current atomic hardware operation
   reaches its declared finite completion/timeout, the agent flushes evidence, records board and
   cleanup state, writes `PARALLEL_CHECKPOINT.md`, and returns without a terminal result.
   Board-free spec/build/review phases may continue only if they do not invoke or depend on the
   live server and cannot transition into HIL.
8. Wait through agent/process completion events, managed-watcher notifications, or an ordinary
   blocking shell wait. Do not use repeated model turns to poll. Still perform the bounded
   supervision pass above so a missing notification, crash, repetition loop, or idle lease is
   caught promptly.
9. When every active server/HIL consumer is checkpointed, mark those consumers frozen. Process the
   validated repair queue serially with one main-authored plan/change-loop at a time. Concurrent
   production edits or repair loops are forbidden.
10. After the queue is drained, restart checkpointed MCP processes from the same new server
    snapshot. Remove each pause request, update the ledger, and resume the exact persistent agents.
    Bind builds completed during repair to this snapshot before HIL. Affected tests rerun the
    minimal reproducer and reached requirements; unrelated verified evidence is retained.
11. If a watcher defect is confirmed, stop new launches, checkpoint only affected live roles,
    stop exact watcher/controller/affected descendants, preserve all completed evidence, make the
    focused local harness repair, run its focused and ordinary host tests, and resume only
    incomplete work. Never restart the whole suite or passed lanes for a harness repair.
12. Before ending an epoch, renew and durably hand off watcher ownership or issue cooperative
    `watch stop`, confirm exact watcher/controller absence, and record pending state. Heartbeat
    expiry is the fail-closed cleanup path if the manager disappears.

`PARALLEL_CHECKPOINT.md` must state the optional informational eligibility group, server snapshot,
last completed requirement, evidence paths, in-flight operation (`none` at a safe checkpoint), board/session/serial state, cleanup
performed, remaining work, and the exact first action on resume. A long soak or repetition loop
must define bounded epochs and persist cumulative counters so pause latency is bounded rather than
the full soak duration.

## 3. Test specification rules

The main model writes one immutable `.agent-workspace/SPEC.md` before spawning. Each spec must
contain:

- catalog test ID/title and source server commit;
- canonical named doer from `doer-roster.md`;
- objective and explicitly excluded behavior;
- required boards and roles;
- exact truthfully established MCU/package identifiers;
- manager-declared fixed fixture wiring and autonomous oracle material to the selected case;
- execution model (custom scheduler, ThreadX, or Zephyr when applicable);
- setup/build/flash/debug/lifecycle actions to exercise;
- seeded fault, if any, hidden oracle key location, and disclosure rule;
- numbered requirements, each with an observable pass and failure condition;
- build prerequisites and HIL prerequisites as separate dependency sets;
- internal catalog-defined shard map, when applicable;
- phase-specific resource requests and the immutable build-to-HIL artifact handoff;
- required raw evidence and final board state;
- mutation/risk class, applicable recorded delegated authorization, and whether the live plan
  exceeds it;
- finite time/retry bounds derived from the protocol or test objective;
- dependency prerequisites and requested exclusive/shared resources;
- disruptive USB, server-lifecycle, power, or cross-board scope; and
- safe checkpoint boundaries, bounded long-run epochs, and maximum pause latency.

The spec translates the catalog; it may not add evaluator-only prerequisites or any new
operator/physical action. Never require a PCA number, printed PCB revision, photograph, direct
visual chip inspection, removable label, cable move, button press, repositioning, rewiring,
jumper/solder change, DMM, logic analyzer, BLE sniffer, camera, oscilloscope, external power
instrument, or operator-timed event. Use the declared fixed fixture, stable electronic identity,
software-controlled fault injection, UART/peer/debug evidence, and live server plans. One truthful,
adequately correlated source is enough; do not demand duplicate modalities. Build and HIL
dependency lists contain only behavior actually consumed by that phase, never a blanket completion
barrier.

Do not reveal a seeded bug's answer to the test agent. State only the symptom and acceptance
behavior. Keep the answer key outside the run directory.

The test agent may amend application design details, but not weaken the spec. Only the main model
may append a spec correction, with reason and timestamp, before the affected action is rerun.
Removing a catalog-unsupported prerequisite is a correction rather than weakening; preserve valid
evidence and do not restart unrelated work.

## 4. Isolation and allowed inputs

At seal time the run root may contain only:

```text
stm32L476rgt.pdf
Nano_BLE_MCU-nRF52840_PS_v1.1.pdf
.agent-workspace/
```

The canonical baseline source files live in the task-owned asset directories under
`fresh-experiments/S10_20260726-034312/.agent-workspace/assets/datasheets/` and
`fresh-experiments/S11_20260726-034313/.agent-workspace/assets/datasheets/`; the scaffold preserves the
legacy filenames above inside each run for sealed-manifest compatibility.

For A24/A25 only, the manager may also place hashed copies of
`60852689.DS_SX1261_2 V2-2.pdf`, `waveshare-lora-module.pdf`, and
`nrf-sx-pin-mappings.md` in the run root. Fixed fixture facts belong in the manager-supplied
`.agent-workspace/FIXTURE.md`. No other parent/root document is allowed.

Their canonical sources are
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/sx1261-sx1262-v2.2.pdf`,
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/waveshare-lora-module.pdf`, and
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/board-mappings/nrf-sx1262-pin-mappings.md`;
retain the legacy run-local names above.

The workspace may contain the generated spec, prompt, manifests, state, result schema, and an empty
evidence directory. After the agent starts it creates the application repository and all build
state in the run root.

The test agent may use:

- the two supplied local PDFs;
- for A24/A25 only, the three manager-supplied hashed CoreSX1262 inputs listed above;
- the run-local manager-supplied `.agent-workspace/FIXTURE.md` when the selected case needs fixed
  wiring, antenna, or bridge-state facts;
- official internet sources it finds itself;
- ordinary SDK/toolchain/package acquisition;
- the live BYO firmware MCP tools;
- physical boards named by the spec;
- files it creates in its own run.

It may not read:

- the master experiment Markdown;
- another experiment directory;
- server source/tests/docs or `.firm` from another project;
- parent/root documents other than the two copied baseline PDFs and the explicit A24/A25 inputs;
- pre-existing firmware examples or generated board profiles.

It may not invoke, read, or use `$change-loop` or `$plan-changes`. Those workflows are reserved
for the main model's verified production-server repairs.

It must not use direct pyOCD/OpenOCD/nrfjprog/J-Link/ST-LINK operations as a substitute for the MCP.
An ordinary vendor build tool is allowed. Independent autonomous oracles are limited to the
declared fixture and software/electronic evidence available without external lab equipment:
host-side serial logging, peer-observed counters, firmware protocol traces, debug/register state,
artifact inspection, and electronic identity. A spec must not request a logic analyzer, BLE/RF
sniffer, oscilloscope, DMM, camera, or another operator/external-instrument action.

## 5. Test-agent model and continuity contract

Invoke ordinary tests through `subagent exec`, not the regular internal subagent tool, with:

```text
fork_turns: none
model: gpt-5.6-luna
reasoning_effort: high
service_tier: default
task_name: firmware_lane_<doer-name-lower>
```

`default` is the regular tier required for Luna doers. `priority` is Codex Fast mode and is
reserved for Terra reviewers and repair roles; neither is a model suffix.

A23 is the sole provider exception. Invoke Nova, its one persistent doer, with Claude Sonnet 5 through a
persistent unrestricted/no-command-approval Claude launcher with no inherited parent conversation. Record the
launcher's exact model identifier and settings. Do not apply Codex `service_tier` or reasoning
labels to Claude. After one bounded retry window, transparently bind A23 to a persistent `gpt-5.6-luna`
high-reasoning regular/default fallback if the Claude provider is unavailable; record the necessary
model change and loss of the provider-comparison datapoint. Never substitute silently. Q40 is
manager-owned corpus aggregation rather than another base-application test-agent assignment;
assign each missing branch to one idle Atlas/Boreal/Cygnus/Delta session rather than creating a
branch-specific doer.

The test-agent task message must:

1. give the absolute run directory;
2. point to `.agent-workspace/TEST_AGENT_PROMPT.md` and `SPEC.md`;
3. require the first command to verify the run directory;
4. forbid server-source access and edits;
5. require autonomous firmware/test iteration;
6. require one result-contract terminal state, except for a manager-requested parallel checkpoint;
7. require raw evidence before returning; and
8. require pause-file checks at the sealed spec's safe boundaries.

The agent owns firmware code and tests. It should remain in one turn as long as useful. If it
returns early with progress prose, resume the recorded session through its recorded provider launcher and tell it to
continue from its durable state. Do not accept “looks good,” a build-only result, or a flash-only
result. A requested pause is valid only with a complete `PARALLEL_CHECKPOINT.md`; it is not a PASS
or other terminal result. Do not create sequential disposable same-model sessions.

Keep the original session unless a model change is necessary or the session is irrecoverable.
Follow `model-continuity-contract.md` for the allowed reasons, required old/new identity record,
verified evidence boundary, and no-unnecessary-redo rule. A run already active on another model is
grandfathered and must not restart merely to adopt the new default.

Before starting that test agent, launch one persistent read-only reviewer with
`fork_turns: none`, `model: gpt-5.6-terra`, `reasoning_effort: high`, and
`service_tier: priority`. Its first task points
to `REVIEWER_PROMPT.md`, requires it to write `SPEC_ADVERSARIAL_REVIEW.md`, and forbids hardware
operations, server access, firmware/server edits, and change-loop use. Bind it with
`fresh_test.py bind-reviewer`, then let the main model append a signed `SPEC_AMENDMENTS.md` only
for a genuine spec error and call `fresh_test.py approve-spec`. Resume this recorded reviewer—not a
new reviewer—with the same model, reasoning, and service tier after a PASS claim for the evidence
review.

## 6. Main-model review

Before the main-model review, resume the one recorded read-only adversarial reviewer through
`subagent exec` for every PASS claim. Do not use the regular internal subagent tool.
It receives only the run directory and reads the sealed spec, result, report, and raw evidence. It
must not open or read `BYO-Firmware-MCP` (including its source, tests, documentation, runtime
state, or Git history), operate hardware, or edit firmware/server files. It writes
`.agent-workspace/ADVERSARIAL_REVIEW.md`. Its report either states
`NO_ACTIONABLE_SERVER_ISSUES` or supplies numbered criticisms with evidence paths, expected
observable behavior, server-versus-fixture/firmware reasoning, and a minimal observable
regression. Label each criticism `ACTIONABLE` or `ADVISORY`. Actionable findings demonstrate an
accepted requirement violation, credible safety/data-loss/identity risk, reproducible failure, or
likely hang/orchestration collapse. Speculative hardening, style, vanishingly unlikely cases
without evidence, unrelated features, and disproportionate complexity are advisory. Missing or
inadequate MCP guidance that blocks the required workflow is actionable; it is never permission to
inspect the server.

For `PASS`, verify only evidence applicable to the selected requirements:

- the initial manifest proves a fresh start;
- every numbered requirement has raw evidence;
- exact build commands exit zero and artifacts match the flashed plan;
- behavioral evidence comes after flash/reset and from the intended board;
- peer counters or independent oracles reconcile where required; no particular lab instrument is
  implied;
- debug conclusions identify the seeded cause rather than only changing symptoms;
- queue/RTOS tests include full/wraparound/ISR/priority/stack evidence when specified;
- temporary instrumentation is either removed or explicitly retained by the spec;
- final source diff is coherent and final board state is stated;
- no direct hardware utility bypassed the MCP.
- every adversarial criticism was independently accepted or rejected with recorded rationale.

Retain every previously accepted requirement/evidence edge whose spec, artifact, server snapshot,
fixture identity, and relevant behavior are unchanged. A rejected review triggers only the missing
or invalidated proof and one targeted reviewer follow-up; it never restarts the whole test or
reopens unrelated accepted requirements. When actionable findings are resolved and objective gates
pass, stop reviewing. Advisory findings are recorded but do not block delivery.

Resume the recorded test-agent session through its recorded provider launcher for gaps. If the continuity contract
requires a replacement, the replacement becomes the recorded owner and resumes the durable
evidence boundary without redoing already verified requirements merely because its model changed.
The main model may rerun host-only verification commands, inspect files, and compare evidence, but
it must not replace the agent as firmware implementer/tester outside that recorded exception.

For `SERVER_FAILURE`, require at least:

- exact MCP call sequence and complete response/error;
- expected behavior tied to the spec/server contract;
- target/server commit and run state;
- proof the correct artifact, board, and applicable wiring/SDK/preconditions were used;
- a minimal repeatable reproducer;
- a second observation or a strong explanation why repetition is unsafe;
- proof the failure remains when firmware/test mistakes are corrected.

## 7. Server-failure escalation

The main model independently reads the server contract and relevant code. Only if the defect is a
real production-code server defect, create a narrow change request and run `$change-loop` with a
test-specific `CL_RUNTIME_DIR`. Do not use change-loop for documentation-only/metadata-only,
firmware, fixture, SDK, host, test-spec, or evidence work.

Before editing the server, add the validated defect to `SERVER_REPAIR_QUEUE.md`, stop new
server-consuming/HIL launches, request and receive bounded checkpoints from all active server/HIL
consumers, and record those consumers `FROZEN`. Isolated board-free non-server phases may continue.
Do not hold a model turn open to poll; wait on role/process completion. Only the main model may
drain the queue, and it does so serially with one production repair/change-loop at a time.

The current main/orchestrating model directly authors the one plan; never delegate plan authorship
to a subagent, Codex exec planner, doer, or tester. Conduct one read-only adversarial plan review.
Record the reviewed plan SHA-256,
reviewer identity, and its numbered risks/test targets in `plan-review.md`, then begin the
change-loop immediately. If execution proves a genuine plan mistake, the main model records a
minimal evidence-backed amendment and obtains one targeted review of that amendment only; it does
not regenerate the whole plan or re-review unchanged items. The neutral gate and the subsequent
targeted retest remain the correctness backstops.

The repair must:

- be general rather than board-specific;
- preserve live plan/permission gates;
- include spec and regression tests owned by change-loop tester roles;
- rerun only failed or invalidated checks and affected regressions; retain unchanged passing gate
  evidence rather than restarting expensive tests or experiments from scratch;
- avoid editing the fresh firmware run;
- avoid changing the test to make the failure disappear;
- pass the neutral change-loop gate before HIL retest.

After each repair passes its neutral gate, keep unrelated server/HIL consumers frozen, restart an isolated MCP
process for the reporting run, and resume only its recorded agent for the minimal reproducer and
requirements reached by that change. Close the queue item only after that targeted retest passes,
then process the next item serially. After the queue is drained, record one final server snapshot,
restart every checkpointed MCP process from it, remove pause requests, and resume the recorded sessions
through their recorded provider launchers (or their formally recorded necessary replacements). Unaffected agents
resume their exact checkpoint. Do not repeat unrelated expensive acceptance or soak work unless
change scope requires it.

## 8. Recovery and resumption

Durable truth lives in:

- root `.agent-workspace/SUITE_COORDINATION.md`
- root `.agent-workspace/SERVER_REPAIR_QUEUE.md`
- `.agent-workspace/RUN_STATE.json`
- `.agent-workspace/SPEC.md`
- `.agent-workspace/RESULT.json`
- `.agent-workspace/TEST_REPORT.md`
- `.agent-workspace/PARALLEL_CHECKPOINT.md` when paused
- `.agent-workspace/evidence/`

Before compaction or session exit, record every active test/shard, phase, leases, server snapshot, run path,
agent ID/task/model, pause/checkpoint state, queued repair, server change-loop runtime, last
verified evidence, and exact next follow-up. Never discard a session mapping merely because its
last turn failed.
