# Frozen-to-Candidate Harness Development Flow

## Purpose

Use the current frozen harness to coordinate development of the work-in-progress harness without running two authoritative harnesses at the same time.

The design follows one rule:

> Only one harness may manage real agents in an orchestration epoch.

## Repository Roles

### Frozen Harness

The frozen harness is the known baseline.

It coordinates:

- The primary implementation agent.
- Review agents.
- Unit-test agents.
- Lock stress-test agents.
- Git and result-validation test agents.
- Reusable safety regression-test agents.

Do not modify the frozen harness during candidate development. Keep its exact Git commit recorded and its worktree clean.

### Work-In-Progress Harness

The work-in-progress harness contains the seven generalization changes.

During normal development it is software being edited and tested. It is not an active manager of the agents developing it.

It becomes authoritative only during an isolated full acceptance test or after final promotion.

## What "Testing the Candidate" Means

While the frozen harness is active, testing the candidate means exercising candidate code as an ordinary test subject. It does not mean starting the candidate as a second live orchestration harness.

Allowed examples:

- Import candidate modules from unit tests.
- Validate candidate results using temporary JSON files.
- Validate branches and worktrees in temporary Git repositories.
- Exercise named locks in temporary lock directories.
- Run reconciliation against synthetic records.
- Run the candidate lane controller with a fake subprocess instead of a real Codex worker.
- Start short-lived candidate CLI processes that read and write only isolated test fixtures.

In these tests, the frozen harness controls one outer test agent. Candidate code may execute inside that agent's test process, but it has no authority over real agents, the development epoch, or frozen harness state.

While the frozen harness is active, the candidate must not:

- Start or resume real Codex workers.
- Start a live manager epoch.
- Own a development manager heartbeat.
- Run as the managed watcher for the development epoch.
- Observe or acknowledge the frozen harness's live events.
- Read or write the frozen harness's runtime directories.
- Control the agents implementing or testing it.

This is component and isolated integration testing, not nested orchestration.

## Phase 1: Development Under the Frozen Harness

The frozen harness is the only authority.

```text
frozen harness
  -> implementation agent
  -> review agent
  -> unit-test agent
  -> lock-test agent
  -> Git/result-test agent
  -> safety-regression agent
```

Agents work on the work-in-progress repository. Prefer one production-code writer at a time because the main changes converge on `lane_controller.py`, discovery, and reconciliation.

Parallel agents should focus on independent work such as:

- Focused unit-test authoring in manager-assigned disjoint files.
- Documentation authoring in manager-assigned disjoint files.
- Failure-case design.
- Read-only review.
- Lock stress tests with isolated temporary lock roots.
- Git worktree validation with isolated temporary repositories.
- Process, event, checkpoint, and recovery safety checks.
- Documentation review.

The candidate code may be imported or launched as a short-lived subprocess by tests using disposable fixtures. It must not start real Codex workers, create a live orchestration epoch, or manage development agents during this phase.

## Phase 2: Focused Candidate Testing

Focused tests remain under the frozen harness and may run in parallel when isolated.

Every parallel test must have its own:

- Temporary repository.
- Worktree directory.
- Runtime root.
- Lock root.
- Event and output directories.
- Manager epoch ID.
- Ports or other external resources.

Suitable parallel tests include:

- General coding invocation validation.
- Wrong-branch and missing-commit rejection.
- Result-schema and stale-invocation rejection.
- Uncontended and contended named locks.
- Matching-owner lock release.
- Unknown process identity preventing lock release.
- Reusable process, event, checkpoint, and recovery behavior.
- Existing synthetic firmware invocation, MCP, relay, hardware-resource, and reconciliation behavior.

These tests exercise candidate components against disposable state. They do not start the candidate's real manager loop, managed watcher, or real Codex lanes, and therefore do not create a second orchestration hierarchy.

### Firmware Regression Policy

Firmware remains a supported product path. Its existing synthetic tests are part of the required repository regression gate, not an optional historical suite.

On the current Windows development machine, the complete orchestrator suite runs 208 tests in about 28 seconds. It uses synthetic records and subprocesses, not a physical board, firmware server, or MCP device. The expected one-time compatibility cost is approximately 1–3 agent-hours to preserve the firmware invocation and result routes while adding the versioned coding routes.

Do not run physical hardware validation during every development cycle. Reserve real firmware/hardware acceptance for releases and changes to hardware-specific behavior.

## Phase 3: Prepare Full Acceptance

Before the candidate manages any test agents:

1. Stop assigning new development work.
2. Finish or checkpoint every active development lane.
3. Record the frozen harness state and current candidate commit.
4. Run the normal focused and repository test suites.
5. Stop the frozen managed watcher and manager loop cleanly.
6. Confirm the exact frozen harness processes have stopped.
7. Create a fresh candidate epoch with new runtime and output directories.
8. Create a disposable target Git repository for acceptance testing.

The frozen harness remains available on disk for rollback but has no active authority during acceptance.

## Phase 4: Candidate Full Acceptance

The work-in-progress harness becomes the only active orchestration harness. A separate acceptance-test supervisor owns the test lifecycle but does not plan or perform the coding task.

Use this authority structure:

```text
acceptance-test supervisor
  |
  |-- candidate harness under test
  |     |-- one coding lane at a time
  |     |-- disjoint test lane A
  |     |-- disjoint test lane B
  |     `-- one merge lane at a time
  |
  |-- deterministic watcher and logs
  `-- read-only watcher subagent
```

The candidate harness performs the software work. The supervisor and watcher evaluate the candidate harness. The candidate must not judge its own orchestration correctness.

Run one complete scenario at a time:

```text
work-in-progress harness
  -> coding lane A on branch/worktree A
  -> merge A
  -> coding lane B on branch/worktree B
  -> merge B
  -> parallel disjoint test lanes on isolated worktrees
  -> merge lane on an integration branch/worktree
```

The scenario must prove:

1. Both coding lanes use the new coding contract without supplying firmware, board, MCP, or relay records.
2. Each lane uses its declared branch, worktree, base commit, and worker invocation ID.
3. Independent test lanes run concurrently when their files and resources do not conflict.
4. Two test lanes declaring the same generic resource are serialized automatically.
5. Normal lock contention does not require manager action.
6. Checkpoints and events remain durable.
7. Stale or wrong-branch results are rejected.
8. Valid results identify real branch-tip commits.
9. The merge lane merges both completed branches.
10. Final Python integration checks pass.
11. Events require exact acknowledgement.
12. The candidate shuts down cleanly.

Do not run the frozen harness during this scenario. Do not run several full candidate orchestration topologies in parallel.

### Acceptance Workload

Give the candidate harness one complete, disposable Python application to build from beginning to end. The application should be complex enough to require real planning, serialized production implementation, branch merging, and parallel disjoint test authoring and execution, but deterministic and local enough that failures can be reproduced.

A suitable workload is a local task-tracking application with:

- Data models and validation.
- SQLite persistence.
- A service layer.
- A command-line interface.
- JSON import and export.
- Filtering and status transitions.
- Unit and integration tests.
- User documentation.

The candidate manager decides how to divide the work but launches only one production-code lane at a time. A reasonable sequence is design/API, model, storage, CLI, import/export, and integration, merging each stable production branch before the next begins. Once interfaces and exact file ownership are fixed, disjoint test and documentation authors may run concurrently.

The target project must use no network services, secrets, physical hardware, or production resources.

### Watcher Roles

The deterministic watcher records the candidate manager, harness, controller, worker, lock, result, event, and acknowledgement actions.

A watcher subagent is enabled only for full acceptance. It:

- Reads the watcher output and candidate evidence.
- Does not edit either codebase.
- Does not acknowledge events.
- Does not direct workers.
- Does not repair code.
- Does not stop or kill processes.
- Publishes a bounded critical-finding record with exact evidence when necessary.

The watcher subagent is read-only. It cannot also terminate the test. Only the external acceptance-test supervisor has stop authority.

### Critical Abort Criteria

Abort only for a harness-level failure whose continuation would invalidate the test or risk corrupting code or state. Examples include:

- A worker edits outside its declared worktree.
- Two workers use the same branch or worktree.
- Two workers simultaneously hold the same exclusive named lock.
- A stale, wrong-lane, or wrong-branch result is accepted as merge-ready.
- The harness loses or misidentifies a worker process.
- Event, pending-notification, acknowledgement, or lock state is corrupted.
- The candidate declares success while required work failed.
- The candidate deadlocks and cannot recover within its declared bounds.
- The candidate reads or writes frozen harness runtime state.
- The candidate cannot stop its exact process descendants safely.

Do not abort for ordinary workload failures such as buggy application code, a failing unit test, a normal merge conflict, an implementation retry, or temporarily incomplete work. Those are conditions the candidate harness is expected to handle. They become harness failures only when the harness handles them incorrectly.

### Safe Abort Procedure

When the watcher subagent publishes a critical finding:

1. The supervisor stops new lane launches.
2. The supervisor requests cooperative candidate shutdown.
3. It waits for bounded cleanup.
4. It stops only exact remaining candidate descendants if required.
5. It preserves logs, events, checkpoints, branches, lock claims, and process evidence.
6. It confirms every candidate process has stopped.
7. It marks the acceptance epoch failed.

Never terminate processes by broad name or command matching.

### Repair After A Critical Abort

Do not spawn a repair agent until the candidate acceptance topology is completely stopped.

Then:

1. Restart the frozen harness in a new repair/development epoch.
2. Spawn one Sol repair agent against the candidate harness source.
3. Allow that agent to use its own repair subagents if useful.
4. Keep all repair branches, worktrees, runtime roots, and identities separate from the failed acceptance epoch.
5. Run focused and regression tests under the frozen harness.
6. Stop the frozen harness again before starting a fresh candidate acceptance attempt.

The repair chain is never part of the failed candidate test and must not be mistaken for one of its coding lanes.

## Phase 5A: Rollback After Failure

If full acceptance fails:

1. Stop the candidate harness and confirm its exact processes have stopped.
2. Preserve the isolated candidate logs and failure evidence.
3. Do not reuse the failed candidate epoch as a new run.
4. Restart the frozen harness with its recorded state or a fresh development epoch.
5. Resume candidate development or start the isolated Sol repair flow from the last checkpoint.
6. Fix and repeat focused tests before another full acceptance attempt.

The candidate must never continue managing development agents after a failed acceptance run.

## Phase 5B: Promotion After Success

If full acceptance passes:

1. Record the verified candidate commit and test evidence.
2. Mark that commit as the promoted harness version.
3. Start a fresh real manager epoch using the promoted harness.
4. Use fresh runtime, output, event, and acknowledgement state.
5. Keep the frozen harness unchanged as a rollback option.
6. Do not restart the frozen harness unless the promoted version is stopped first.

Promotion is a change of authority, not a continuation of the acceptance epoch.

## State Separation

The frozen and candidate harnesses must never share writable runtime state.

Keep separate:

- Harness output roots.
- Event logs.
- Pending notifications.
- Acknowledgement logs.
- Watcher service state.
- Manager heartbeats.
- Lock claims.
- Epoch identifiers.
- Temporary test repositories.

Historical read-only logs may be compared, but one harness must never acknowledge or mutate the other harness's events.

## Test Parallelism Rules

| Activity | Harness authority | Parallel? |
|---|---|---|
| Candidate implementation | Frozen | Prefer one production writer |
| Test authoring | Frozen | Yes, only in manager-assigned disjoint files |
| Documentation authoring | Frozen | Yes, only in manager-assigned disjoint files |
| Test execution | Frozen | Yes, with isolated writable resources |
| Git/result tests | Frozen | Yes, with isolated repositories |
| Lock tests | Frozen | Yes, with isolated lock roots |
| Reusable safety regressions | Frozen | Yes when test fixtures are isolated |
| Synthetic firmware regressions | Frozen | Yes when test fixtures are isolated |
| Physical firmware acceptance | Outside routine development | Release-only or after hardware-specific changes |
| Full candidate orchestration acceptance | Candidate only | No, one topology at a time |
| Real work after promotion | Promoted candidate | According to normal lane plan |

## Terminology

Use these names consistently:

- **Frozen harness:** unchanged bootstrap version coordinating development.
- **Candidate harness:** work-in-progress version being developed or tested.
- **Promoted harness:** candidate version after successful acceptance.
- **Target repository:** disposable project used during full acceptance.
- **Acceptance-test supervisor:** external lifecycle owner that starts and stops the test but does not perform the coding task.
- **Watcher subagent:** test-only, read-only evaluator that reports critical findings but cannot intervene.

Avoid calling both repositories the "working harness." The names describe their authority and reduce mistakes during handoff.

## Summary

Use the frozen harness for development and parallel focused testing. Stop it before the candidate performs a full orchestration test. Let the candidate build one complete disposable Python application while an external supervisor and read-only watcher evaluate it. Then either stop the candidate and restore the frozen harness for repair, or promote the candidate and leave the frozen harness inactive as rollback.

Never nest two authoritative harnesses and never let both manage real agents at the same time.
