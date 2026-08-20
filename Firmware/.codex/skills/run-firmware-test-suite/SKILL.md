---
name: run-firmware-test-suite
description: Execute or resume the self-contained BYO Firmware MCP evaluation package under Firmware/, using the package-local WIP harness target for lane coordination and deterministic watcher diagnostics, isolated STM32L476 and nRF52840 runs, HIL evidence review, failure triage, and serialized repairs to the bundled BYO-Firmware-MCP server. Use when asked to run, parallelize, audit, resume, or complete the firmware experiment catalog.
---

# Run Firmware Test Suite

## Package and target boundary

Run from the `Firmware/` suite root. Codex discovers this skill from
`.codex/skills/run-firmware-test-suite/`. Resolve every live input below the suite root:

- experiment catalog: `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`
- production server under test: `BYO-Firmware-MCP/`
- shared inputs and repair charter: `Firmware resources/`
- suite skills: `.codex/skills/`
- suite helpers: `scripts/orchestration/`
- campaign state: `.agent-workspace/`
- imported progress/evidence: `multi-agent-logs/`
- isolated firmware runs: `fresh-experiments/`
- exact WIP product worktree under test: `target-harness/`
- harness observation output: `runtime/orchestrator-harness/<epoch>/`
- target-owned watcher output: `target-harness/runtime/harness-watcher/<epoch>/`

`target-harness/` is a package-local runtime worktree supplied before the test orchestrator starts.
It must contain the exact WIP/product harness revision being tested. Never substitute the stable
development harness, crawl to a parent checkout, or read a path above `Firmware/`. Provider
executables, MCP transports, SDKs, toolchains, and official internet research are runtime
capabilities rather than filesystem dependencies.

The external run owner must create/select `target-harness/`, record its Git revision and dirty
state in the epoch ledger, and launch the test orchestrator from `Firmware/`. The orchestrator may
then inspect both the package and the product under test. Fresh firmware doers still receive only
their isolated run root; they may not inspect `target-harness/`, the catalog, or server source.

## Load and validate before acting

1. Read `README.md`, the selected catalog section, and catalog section 11.1.
2. Read [execution-contract.md](references/execution-contract.md),
   [model-continuity-contract.md](references/model-continuity-contract.md), and
   [doer-roster.md](references/doer-roster.md).
3. Read [result-contract.md](references/result-contract.md) before reviewing a result.
4. Read `target-harness/QUICK_RULES.md`, `target-harness/QUICK_START.md`, and
   `target-harness/docs/HARNESS_WATCHER_GUIDE.md` before configuring a live epoch.
5. Before any production-server repair, read `BYO-Firmware-MCP/README.md`,
   `BYO-Firmware-MCP/SERVER_GUIDE.md`, the applicable linked client/plan contract, and
   `Firmware resources/test-program/design_charter.md` in full. Then use `$plan-changes` and
   `$change-loop` from this package. A possible failure is not permission to edit: only a
   manager-verified production-code defect enters that route.
6. When resuming, read `multi-agent-logs/HANDOFF.md`,
   `multi-agent-logs/PROGRESS_REMAINING.md`,
   `multi-agent-logs/current-state/CURRENT_SUITE_STATE.json`, and
   `multi-agent-logs/current-state/CURRENT_RELEVANT_PROCESS_INVENTORY.json` before the current
   `.agent-workspace/SUITE_COORDINATION.md`. Imported absolute paths, PIDs, leases, configs, and
   watcher state are historical only; preserve accepted results/checkpoints but establish fresh
   live authority in this package.
7. Read `.agent-workspace/SERVER_REPAIR_QUEUE.md`, verify
   `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.md` against its `.sha256` sidecar, and read
   `.agent-workspace/AUTONOMY_REQUIREMENT_MATRIX.md`.
8. Run `python .codex/skills/run-firmware-test-suite/scripts/audit_autonomy.py` after changing the
   package. Before any doer or reviewer launch/resume, run it with `--require-target` so the local
   WIP harness and deterministic watcher entrypoints are also proven present.
9. Load the firmware MCP help/setup guidance before live MCP use. Guidance is not hardware
   authorization.

## Safety and authorization

Do not operate hardware merely because fixture files exist. Before the first HIL phase, require a
current user instruction authorizing hardware testing and record its exact scope in
`.agent-workspace/USER_DELEGATED_AUTHORIZATION.md`. For each live plan, the manager verifies the
board, electronic identity, artifact, operation, losses, permission mode, and final state before
relaying only authorization already granted. Never bypass a server plan, permission check, or
safety refusal.

After an authorized launch, the main catalog is zero-operator. Do not require another message,
visual inspection, cable move, button press, rewiring, external lab instrument, or operator-timed
observation. Use the fixed fixture, stable electronic identity, UART/peer/debug evidence, and
autonomous server/software controls. Move an intrinsically manual or unavailable-equipment branch
to non-gating Appendix A as `SKIPPED_AUTONOMY_REQUIRED`.

`NEEDS_USER` and `INFRA_BLOCKED` are not terminal main-suite results. Record temporary provider or
resource waits in the suite ledger, checkpoint safely, and continue unrelated eligible work.

## Roles and scheduling

Use one authoritative logical manager role and the rostered logical doers. A doer role is not a
resource lane, and neither a logical manager nor logical doer is identical to one provider session.
Give each task to exactly one doer role and each role at most one active task. Prefer the recorded
session when valid; replace any manager/doer/reviewer invocation through the continuity/recovery
contract when it exits, becomes invalid, or cannot resume. Session continuity is never required for
logical-sprint continuity.

Launch or resume **all** eligible named doer lanes concurrently in the same scheduling batch.
Catalog section 11.1 is the authoritative cross-test edge list. Row order, numeric order, an
unfinished peer task, or a blocked lane is not a dependency. Continue unrelated lanes while
another waits. Recompute readiness after every launch, completion, checkpoint, failure, provider
change, repair-state change, and lease transition.

| Doer | Assigned catalog tasks |
|---|---|
| Atlas | S10, S13, A20, A22, D30, D32, Q41 |
| Boreal | S11, A21, D31, D36 |
| Cygnus | S12, A24, D33, D34 |
| Delta | A25, A26 |
| Nova | A23 only |

The [Firmware provider-adapter contract](../../../PROVIDER_ADAPTER.md) is the sole authority for
the doer, reviewer, and server-repair model/effort/tier/route allocation and its current pending
status. The reviewer remains read-only; a server repair is separate from named test doers and is
admitted only after a manager-verified production-server defect.

The acceptance orchestrator/test orchestrator is one authoritative logical manager role. A concrete
manager session/epoch is replaceable and receives a new identity and live authority; it schedules
the suite and owns firmware/MCP-server decisions, and is neither a doer nor a reviewer.

## Sprint completion and interruption

An interruption is not a sprint result. Keep the same logical sprint ID, sealed specification,
verified checkpoints, completed evidence, and accumulated findings. If a manager, provider, or
lane invocation cannot continue, verify its exact process tree and any live action are absent or
contained, publish a continuity handoff, and issue fresh runtime authority for the first affected
action. Release or reassign a stale claim only after complete old-owner/process absence proof;
otherwise hold only that exact resource. Continue every unrelated dependency-ready lane.

Administrative/provider failures, malformed calls, doer mistakes, specification/fixture/server
faults, and harness defects do not terminalize the sprint. Correct the affected suite-owned fact or
record a terminal unit finding and continue every feasible unit. If a harness defect is observed,
record it but do not launch harness repair during the sprint. First publish one
`COMPLETED_WITH_FINDINGS` handoff containing the full pool; ROOT reviews and repairs that pool
after completion. A clean accepted sprint publishes `COMPLETED_CLEAN`. Use `INCOMPLETE` only for
explicit user cancellation, withdrawn authority, or live harm that cannot be isolated safely.

## WIP harness and deterministic watcher

The suite owns scheduling, hardware authority, leases, evidence decisions, and repair decisions.
The WIP harness under `target-harness/` supplies provider/lane lifecycle, read-only reconciliation,
and bounded event waits. Its separate `harness_watcher_implementation` process supplies
deterministic diagnostics. Neither component schedules work, assigns hardware, approves a plan,
or replaces the manager.

For every overlapping or HIL/server-consuming epoch:

1. Create fresh epoch paths for live runtime authority. Put the harness config and manager ledgers below
   `.agent-workspace/epochs/<epoch>/`, harness output below
   `runtime/orchestrator-harness/<epoch>/`, and watcher runtime below
   `target-harness/runtime/harness-watcher/<epoch>/`. Never reuse live authority from another
   epoch; carry durable logical-sprint state only through the continuation handoff above.
2. Configure the target harness with the `Firmware/` suite root, `fresh-experiments/*` run glob,
   `.agent-workspace` workspace path, a one-second poll interval, a finite bounded-wait timeout,
   and the epoch-specific harness output directory.
3. Configure the deterministic watcher with explicit manager/harness/lane log sources, a
   120-180 second poll interval, an evidence-based 10-15 minute no-progress threshold, and
   `evaluator_enabled: false`. The watcher must not launch an AI evaluator.
4. Require the external launcher to publish the exact live manager PID plus creation identity in
   the epoch ledger. Start the watcher from the target worktree with that PID. Do not bind it to a
   short-lived shell process.
5. Reconcile once, start or confirm exactly one watcher, then launch every eligible lane through
   the target harness's ordinary firmware-compatible lane-controller route.
6. The manager waits with the target's bounded
   `orchestrator_harness watch --until-actionable --timeout <seconds>` command or the active
   provider's blocking session wait. A timeout is a normal supervision boundary: rescan lanes and
   leases, write the observation, then wait again. It is not a test failure and must never become
   an unbounded silent wait.
7. During active HIL, inspect every live doer normally every two to three minutes. Review the
   named lane before acting on an event. Record exact recovery, lease, and cleanup decisions.
8. On epoch completion, stop the watcher cooperatively, verify its exact PID-plus-creation identity
   is absent, and retire only the processes and runtime paths owned by that epoch.

The WIP target intentionally has no stable-only `watch --managed` or heartbeat CLI. Do not call
those commands. Use its bounded diagnostic watch plus its separate deterministic watcher process.

After a terminal sprint handoff, ROOT may run its own separate evidence reviewer for possible
general-harness defects. That reviewer reports only to ROOT; its report is not a suite input. The
test orchestrator must not read, schedule, store, or act on it, and it must stay focused on the
firmware sprint and verified BYO-Firmware-MCP repairs.

## Durable coordination

The manager maintains:

- `.agent-workspace/SUITE_COORDINATION.md`: manager and target revision, doer/session bindings,
  dependencies, phases, leases, waits, and checkpoints.
- `.agent-workspace/SERVER_REPAIR_QUEUE.md`: independently validated production-server defects and
  their repair/retest state.
- `.agent-workspace/epochs/<epoch>/MANAGER_LOG.jsonl`: launches, notifications, reviews, resource
  decisions, checkpoints, recoveries, and cleanup.
- `.agent-workspace/epochs/<epoch>/MONITOR_LOG.jsonl`: bounded whole-suite observations and
  diagnosed stalls, loops, or idle resources.

`multi-agent-logs/` is retained input evidence from earlier runs. It currently establishes a clean
safe boundary, accepted green catalog work, four persistent-lane checkpoints, and the closed Q10
M5 result. Q10 passed `HARNESS_PASS` and `WATCHER_PASS`, but manager evidence was insufficient
(`MANAGER_EVIDENCE_INSUFFICIENT`) because the manager recorded wake events in the wrong order and
published responses without lane IDs. That result proves no current harness, watcher, or server
defect. Q1-Q10 exhausted the goal's attempt budget; never launch Q11. Live M5 continuation requires
a new bounded goal, new attempt budget, and explicit user authorization.

Never append a new epoch into an old log directory or reuse a process/lease merely because it
appears there. Reconcile recorded evidence and identities, safely release/reassign only proven stale claims, and
issue fresh live authority before deciding what durable work can continue. If an imported checkpoint names a run
directory that is not present under `fresh-experiments/`, exact session resume is unavailable:
materialize and validate that run, or create a fresh affected run with an explicit continuity
handoff. Never invent a missing workspace or discard unrelated accepted credit merely because one
checkpoint cannot be resumed.

Lease each doer/provider slot, isolated workspace, server process/state/artifact root, and every
board, probe, serial endpoint, radio/peer, USB/power scope, or mutable cache used. Board tokens are
`STM-A`, `STM-B`, `NRF-A`, and `NRF-B`; exclusive leases may not overlap. Only the manager writes a
run-local `.agent-workspace/RESOURCE_ASSIGNMENT.md`.

Track `SPEC_READY`, `BUILDING`, `BUILT_WAITING_FOR_LEASE`, `HIL_RUNNING`, `CHECKPOINTED`, and
`PASS_CLAIMED` separately from terminal status. Future spec work, read-only review, and isolated
board-free builds may overlap HIL. A build without a HIL lease writes
`BUILT_WAITING_FOR_LEASE.md` and returns without a terminal result.

## Quick start and per-test loop

From `Firmware/`:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py list
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py create A20
```

The scaffolder copies the package-local STM32L476 and nRF52840 PDFs. For A24/A25, add only the
applicable SX126x/module/pin-mapping inputs named by the execution contract. Put fixed fixture facts
in the run-local `.agent-workspace/FIXTURE.md`; never expose the catalog, another run, target
harness source, server source, example firmware, or hidden bug key to a fresh doer.

For each selected test:

1. Create the isolated run and author numbered observable requirements, evidence, finite
   time/retry bounds, safe checkpoints, prerequisites, and exact resources.
2. Seal the spec. Put later corrections in `SPEC_AMENDMENTS.md`; never rewrite the sealed spec.
3. Bind the one persistent sprint MCP reviewer and resolve only actionable spec findings.
4. Launch the roster doer through the target harness's provider/lane lifecycle with the isolated
   run as its worktree. Record its logical doer, provider session, controller, and process IDs.
5. Let the doer build, request manager-assigned HIL leases, operate through the live MCP
   plan/permission surface, collect evidence, repair firmware failures, and finish with `PASS` or
   `SERVER_FAILURE`.
6. Run `python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py verify <run-dir>`.
7. Resume the same reviewer for evidence review. It writes only
   `.agent-workspace/ADVERSARIAL_REVIEW.md` and may not inspect product/server source.
8. The manager accepts or rejects each actionable finding. Request only invalidated proof, then
   record the final review with `fresh_test.py review`.

## Checkpoint and server repair

When the manager independently proves a production-server defect:

1. Stop new server/HIL launches and collect bounded checkpoints from active consumers. Continue
   unrelated isolated board-free work.
2. Record the defect in `.agent-workspace/SERVER_REPAIR_QUEUE.md` and create
   `fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id>/request.md`.
3. The manager rereads `Firmware resources/test-program/design_charter.md`, inspects
   `BYO-Firmware-MCP/`, and uses `$plan-changes` to prepare and directly author one narrow plan.
4. Obtain one independent read-only plan review, then use `$change-loop` for one serialized repair
   with independent focused and affected regression tests.
5. Restart an isolated MCP process from the repaired server state and resume only the reporting
   doer for the minimal reproducer and affected requirements. Close the queue item only after the
   targeted HIL retest passes.
6. Drain repairs one at a time, update checkpointed assignments, and resume only incomplete or
   invalidated work.

Never open a server repair for firmware, fixture, SDK, host, spec, evidence, documentation-only,
or metadata-only failures.

## Completion

Finish only when every required selected main-catalog test has a manager-reviewed `GREEN` result
and its required aggregation is complete, or the user explicitly narrows the sprint. Appendix A
is non-gating. Publish a final matrix containing run path, doer/session, target-harness revision,
server and firmware revisions, result, evidence, repair history, exclusions, lease cleanup, and
remaining limitations. Do not commit, push, deploy, or operate hardware outside an authorized
live test plan.
