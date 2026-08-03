# Sequential Roadmap for Generalizing the Harness

`IMPLEMENTATION_ROADMAP.md` is the authoritative execution plan. It turns this phase inventory into a one-writer, maximum-four-agent workflow.

## Purpose

This roadmap implements the seven changes in `GENERALIZATION_SPEC.md` without redesigning the working harness:

1. A general coding controller contract.
2. Durable Git lane identity.
3. Minimal merge-ready result validation.
4. Automatic generic exclusive named locks.
5. Generic configuration and operating documentation.
6. A complete worktree and merge acceptance test.
7. AI evaluation disabled by default.

The roadmap is intentionally sequential. It does not assign work to agents or define a parallel development plan. Finish and verify each phase before starting the next.

## Development Principles

- Preserve reusable process, I/O, event, checkpoint, acknowledgement, and recovery safety.
- Keep the supported firmware contract and add a separate versioned coding contract.
- Keep the current lane, event, checkpoint, result filename, watcher, and acknowledgement architecture.
- Put new behavior in small modules rather than expanding `lane_controller.py` and `reconcile.py` indefinitely.
- Use Git worktrees for lane isolation and opaque named locks for non-Git resources.
- Treat `RESULT.json` as merge evidence, not completion merely because the file exists.
- Reuse existing atomic I/O, process identity, resource conflict, and event delivery code.
- Do not add a scheduler, task database, dependency graph, adapter framework, or general file ownership.
- Use the frozen harness for development and focused tests.
- Stop the frozen harness before the candidate performs a full orchestration acceptance test.
- Keep existing synthetic firmware regressions in the required test gate; reserve physical hardware acceptance for releases or hardware-specific changes.

The expected incremental cost of preserving firmware support is approximately 1–3 agent-hours during conversion. The current complete orchestrator suite runs 208 tests in about 28 seconds on the current Windows development machine and uses no physical hardware.

## Proposed Module Boundaries

| Module | Responsibility |
|---|---|
| `orchestrator_harness/lane_controller.py` | Common controller flow and integration of the new modules. |
| `orchestrator_harness/coding_invocation.py` | Parse and validate the versioned coding invocation without changing the existing firmware validator. |
| `orchestrator_harness/git_identity.py` | Inspect and validate repository, worktree, branch, base commit, and branch tip. |
| `orchestrator_harness/result_validation.py` | Validate coding `RESULT.json` and merge readiness. |
| `orchestrator_harness/resource_locks.py` | Atomic named-lock claims, waiting, matching-owner release, and stale evidence. |
| `orchestrator_harness/discovery.py` | Discover existing records; expose raw result and claim records without deciding policy. |
| `orchestrator_harness/reconcile.py` | Combine controller, process, Git, result, and lock evidence into lane state. |
| `orchestrator_harness/events.py` | Produce truthful result, Git conflict, resource wait, and stale-claim conditions. |
| `orchestrator_harness/notifications.py` | Decide which exceptional new conditions require manager attention. |
| `harness_watcher_implementation/config.py` | Default optional AI evaluation to disabled. |

The exact filenames can change if existing module boundaries make another placement clearly simpler. The responsibilities should remain separated.

## Phase 0: Establish the Frozen Baseline

### Goal

Create a reproducible starting point before changing product code.

### Tasks

1. Review the current outer repository contents.
2. Create an initial Git commit if the repository still has no `HEAD`.
3. Record the exact baseline commit hash.
4. Create the frozen harness repository or worktree from that commit.
5. Create the candidate repository or worktree from the same commit.
6. Mark the frozen harness as immutable during development.
7. Give frozen and candidate runs separate runtime, event, acknowledgement, watcher, lock, and output roots.
8. Record the standard verification command and current expected test counts.
9. Run the complete verifier against the baseline.

### Tests

- Frozen and candidate repositories begin at the same commit.
- Frozen repository is clean.
- Candidate repository is clean before development begins.
- Standard verification passes.
- Frozen and candidate runtime paths do not overlap.

### Exit Gate

Do not begin implementation without a verified baseline and rollback copy.

## Phase 1: Characterize Reusable Safety Behavior

### Goal

Protect the reliable behavior shared by the firmware and coding paths before adding the new contract.

### Code Work

Do not change production behavior in this phase. Add or strengthen tests around the reusable controller, process, path, event, and recovery behavior.

### Unit Tests

- Prompt hashes remain validated.
- Prompt and output path confinement remain enforced.
- Event log writes remain confined to the configured runtime root.
- Start records controller and Codex PID plus creation identity.
- Resume requires and reuses the persisted Codex thread ID.
- A zero exit without `thread.started` remains a launch failure.
- Output paths escaping the allowed root remain rejected.
- Atomic status, checkpoint, result, resource conflict, event, and acknowledgement behavior remains reliable.
- Existing policy-bound firmware invocation, MCP, relay, board-resource, and reconciliation tests remain green.

### Smoke Test

Run one existing synthetic controller invocation from start through terminal status. Confirm process identity, output capture, event publication, and resume evidence are understood before conversion.

### Exit Gate

The characterization tests pass before introducing coding mode.

## Phase 2: Define Versioned Coding Contracts

### Goal

Freeze the small wire formats before writing behavior around them.

### Coding Invocation Contract

Coding invocation fields include:

```json
{
  "schema": "orchestrator-coding-invocation/v1",
  "worker_invocation_id": "worker-parser-001",
  "declared_lane_id": "parser",
  "task": "Implement the parser",
  "run_root": "C:/project-worktrees/parser",
  "git": {
    "branch": "lane/parser",
    "base_commit": "abc123...",
    "merge_inputs": []
  },
  "exclusive_resources": ["staging-database"]
}
```

Keep existing output paths, model settings, Codex command, resume thread, prompt path, and prompt hash fields where they already work.

### Coding Result Contract

```json
{
  "schema": "orchestrator-lane-result/v1",
  "lane_id": "parser",
  "worker_invocation_id": "worker-parser-001",
  "outcome": "completed",
  "branch": "lane/parser",
  "commit_sha": "def456...",
  "summary": "Implemented the parser and focused tests.",
  "checks": [
    {
      "name": "python -m unittest tests.test_parser",
      "status": "passed"
    }
  ]
}
```

### Lock Claim Contract

```json
{
  "schema": "orchestrator-resource-claim/v1",
  "resource": "staging-database",
  "lane_id": "parser",
  "worker_invocation_id": "worker-parser-001",
  "controller_pid": 1234,
  "controller_created_utc": "...",
  "created_utc": "..."
}
```

### Tasks

1. Define accepted fields and types.
2. Define bounded string and list sizes.
3. Define recognized outcomes and check statuses.
4. Define whether resource names are case-sensitive. Prefer exact case-sensitive matching after rejecting empty or surrounding-whitespace names.
5. Define which validation failures are invocation errors, invalid results, ordinary waits, or actionable manager events.

### Unit Tests

- Minimal valid coding invocation parses.
- Missing or empty invocation identity is rejected.
- Duplicate resource names are normalized to one exact claim or rejected consistently.
- Empty resource names and unsupported shapes are rejected.
- Valid result parses.
- Missing schema, identity, branch, commit, summary, or checks is rejected.
- Unknown result outcome and malformed check entries are rejected.
- Coding invocations do not require or interpret firmware-only fields.
- Existing firmware invocations still parse under their current contract.

### Exit Gate

Contracts and tests are stable before controller integration.

## Phase 3: Add The General Coding Controller Path

### Goal

Launch ordinary coding workers without firmware concepts while preserving the existing policy-bound firmware invocation path.

### Tasks

1. Dispatch `orchestrator-coding-invocation/v1` records to `coding_invocation.py`; leave existing firmware invocation parsing intact.
2. Continue validating prompt bytes against `prompt_sha256`.
3. Do not require firmware policy files or prompt headings for coding invocations; continue validating them for firmware invocations.
4. Keep prompt and output paths confined to the declared worktree and runtime roots.
5. Omit server snapshot, board, lease, MCP, and relay fields from the coding contract while retaining them in the firmware contract.
6. Use generic `exclusive_resources` for non-Git resources.
7. Make model, reasoning effort, service tier, sandbox, approval mode, and relevant Codex settings explicit inputs.
8. Reject unsupported or unsafe configuration values rather than silently falling back.
9. Preserve JSONL, stderr, final message, thread ID, process identity, exit code, start, and resume records.
10. Include worker invocation ID in status and lane events.
11. Record the invocation schema in controller status so reconciliation can route result handling without guessing.

### Unit Tests

- Ordinary coding prompt is accepted.
- Prompt hash mismatch is rejected.
- Prompt and output path escape is rejected.
- Firmware-only fields are not required by the coding contract.
- Configured Codex settings appear in the executed argument list.
- Resume uses the current lane's persisted thread ID.
- Resume with a mismatched invocation or thread fails closed.
- Fake Codex completion produces the expected coding status.
- Fake Codex failure, cancellation, missing thread, and malformed JSONL remain visible.
- Reusable safety characterization tests continue passing.
- Existing firmware controller tests continue passing unchanged.

### Smoke Test

Use a temporary Git repository and a fake Codex executable. Launch one coding invocation, observe `thread.started` and `turn.completed`, and confirm the controller publishes general status and events. Then run the existing synthetic policy-bound firmware controller smoke.

### Exit Gate

One coding lane and one synthetic firmware lane can each complete through their own contracts while all reusable safety tests pass.

## Phase 4: Implement Durable Git Lane Identity

### Goal

Prove each coding lane is operating in the intended Git worktree and branch.

### Tasks

1. Implement Git commands without an implicit shell.
2. Resolve the actual repository and worktree root.
3. Confirm `run_root` is that worktree or the explicitly permitted working directory within it.
4. Read the checked-out branch without relying on user-facing formatted output.
5. Confirm the declared branch matches.
6. Confirm the declared base commit exists.
7. Capture repository common directory, worktree path, branch, start commit, and base commit.
8. Persist verified Git identity in controller status.
9. On resume, verify the lane still refers to the same worktree and branch.
10. Detect duplicate active worktree and duplicate active branch declarations during reconciliation.
11. Reuse resource-conflict machinery where possible by representing worktree and branch identities as internal exclusive resources.

### Unit Tests

- Valid worktree and branch pass.
- Ordinary clone root passes as a worktree.
- Wrong branch fails before Codex launch.
- Non-Git directory fails.
- Missing base commit fails.
- Branch name containing spaces or invalid syntax fails appropriately.
- Detached HEAD behavior is explicitly rejected unless later required.
- Windows path case and separator differences do not create false duplicate worktrees.
- Two active lanes on the same worktree are reported.
- Two active lanes on the same branch are reported.
- Different branches and worktrees are allowed.
- Resume after branch switching fails closed.

### Smoke Test

Create a temporary repository, create two branches and two worktrees, validate both, then deliberately point one invocation at the wrong branch and confirm Codex is never launched.

### Exit Gate

No coding worker starts until its declared Git identity is proven.

## Phase 5: Implement Merge-Ready Result Validation

### Goal

Prevent stale, malformed, uncommitted, or wrong-branch work from being treated as ready to merge.

### Tasks

1. Parse `orchestrator-lane-result/v1` in `result_validation.py`.
2. Match lane ID and worker invocation ID to the current controller attempt.
3. Match the declared result branch to the verified lane branch.
4. Confirm `commit_sha` exists.
5. Confirm `commit_sha` is the current branch tip.
6. Confirm no project changes remain uncommitted outside ignored runtime state.
7. Validate outcome, summary, and reported check records.
8. Keep checks as recorded evidence; do not execute arbitrary commands from `RESULT.json`.
9. Change coding lanes to merge-ready only after validation passes.
10. Apply the versioned result validator to coding lanes. Retain current firmware result interpretation only for controller records explicitly identified as firmware invocations.
11. Emit a durable invalid-result condition with a bounded reason when validation fails.

### Unit Tests

- Current invocation, branch tip, clean worktree, and valid checks pass.
- Result from an older worker invocation is rejected.
- Wrong lane is rejected.
- Wrong branch is rejected.
- Missing commit is rejected.
- Existing commit that is not the branch tip is rejected.
- Dirty tracked file is rejected.
- Untracked project file is rejected.
- Ignored `.agent-workspace` runtime files do not make the project dirty.
- Empty summary is rejected.
- Malformed checks and unsupported statuses are rejected.
- Failed or checkpoint outcomes do not become merge-ready.
- Repeated scans produce one stable invalid-result event rather than event spam.
- Replacing an invalid result with a valid current result clears the invalid condition and produces merge-ready state.
- Firmware result shapes remain accepted for firmware lanes but never make a coding lane merge-ready.

### Smoke Test

Create a coding worktree, commit a valid change, and publish a matching result. Confirm merge-ready state. Then test a stale invocation and a commit behind the branch tip and confirm both remain non-terminal.

### Exit Gate

The harness never reports a coding lane as merge-ready solely because `RESULT.json` exists.

## Phase 6: Implement Generic Exclusive Named Locks

### Goal

Serialize non-Git external resources without resource-specific logic or routine manager intervention.

### Storage Design

- Store claims beneath one candidate epoch lock root shared by its lane controllers.
- Derive safe claim filenames from a cryptographic hash of the exact resource name.
- Store the original resource name and exact owner identity inside the claim.
- Use atomic exclusive creation so only one controller can acquire a free resource.

### Acquisition Algorithm

1. Validate and sort exact resource names.
2. Attempt acquisition in canonical order.
3. If every claim succeeds, launch Codex.
4. If one claim is busy, release claims acquired during that attempt.
5. Publish `WAITING_RESOURCE` with the blocking name and current owner evidence.
6. Wait using a bounded polling interval and retry.
7. Do not launch Codex while any required claim is unavailable.

### Release Algorithm

1. On normal controller completion, inspect each owned claim.
2. Delete only claims whose lane ID, invocation ID, PID, and creation identity exactly match the controller.
3. Never delete an unknown, malformed, or differently owned claim.
4. Make repeated release attempts idempotent.

### Stale Claim Rules

- A claim is stale only when exact process identity proves the recorded controller absent or mismatched.
- Incomplete process-provider evidence remains unknown, not stale.
- Unknown claims are never automatically released.
- Stale, malformed, and excessively delayed claims produce manager-review events.
- Do not add expiry, capacity, shared locks, resource adapters, or automatic lock stealing.

### Unit Tests

- One controller acquires and releases one name.
- Two controllers contending for one name never both enter the protected section.
- Different names can be held concurrently.
- Multiple names are handled in canonical order.
- Partial acquisition is released before retry.
- Waiting status identifies the blocking resource.
- Normal release wakes a waiter.
- Controller failure executes matching-owner cleanup when possible.
- Simulated hard crash leaves a claim for reconciliation.
- Confirmed absent owner is classified stale.
- Unknown owner remains locked.
- Wrong invocation, PID, creation time, or lane cannot release a claim.
- Malformed claim fails closed.
- Resource names with filesystem characters remain safe because filenames are hashed.
- Repeated acquisition and release do not leak claims.

### Stress Test

Run multiple subprocesses through at least 100 acquisition cycles on the same name. Record entry and exit times and prove protected intervals never overlap. Repeat with several names and multi-lock requests. Run this test on Windows.

### Smoke Test

Start two fake coding controllers that request the same name. Confirm the first launches Codex, the second waits without launching Codex, and the second starts after the first releases the claim.

### Exit Gate

Normal contention is automatic, exact, and manager-free. Unknown ownership remains safely blocked.

## Phase 7: Integrate Discovery, Reconciliation, Events, and Notifications

### Goal

Expose new facts through the existing durable observation and event system without rewriting it.

### Tasks

1. Include worker invocation ID, verified Git identity, requested resources, active claims, and waiting resource in lane snapshots.
2. Validate coding results during reconciliation before assigning merge-ready state.
3. Add internal worktree and branch conflicts to existing conflict observation where practical.
4. Preserve exact stable event IDs across unchanged scans.
5. Add focused conditions for invalid coding result, resource wait timeout, stale claim, and malformed claim.
6. Keep ordinary lock waiting non-actionable until its configured warning threshold.
7. Keep stale, malformed, unknown, or excessive waits actionable.
8. Preserve current pending-event priority, displacement, restoration, and exact acknowledgement.
9. Avoid turning ordinary application test failures into harness defects.

### Unit Tests

- New lane fields appear in snapshots.
- Unchanged observations retain the same event ID.
- Invalid result becomes actionable once and remains durable until handled or corrected.
- Normal short resource wait does not wake the manager.
- Excessive wait does wake the manager.
- Stale and malformed claims wake the manager.
- Unknown ownership cannot be acknowledged into an unsafe release.
- Higher-priority safety events still displace and later restore lower-priority events.
- Exact acknowledgement remains required.
- Existing generic pending delivery and priority behavior remains unchanged.

### Smoke Test

Run a coding lane through starting, waiting for a resource, running, publishing an invalid result, correcting it, becoming merge-ready, and exact event acknowledgement.

### Exit Gate

The existing manager loop can consume all new conditions without a new event transport or acknowledgement protocol.

## Phase 8: Disable AI Evaluation By Default

### Goal

Keep normal monitoring deterministic unless AI evaluation is explicitly requested.

### Tasks

1. Change the watcher dataclass default to `false`.
2. Change the loader fallback to `false`.
3. Change the example configuration to `false`.
4. Update documentation that implies evaluation starts by omission.
5. Keep explicit `true` behavior working.

### Unit Tests

- Omitted setting produces `false`.
- Explicit `false` produces `false`.
- Explicit `true` produces `true`.
- Non-boolean values are rejected.
- Disabled polling never invokes the evaluator command.
- Explicit enablement invokes the configured evaluator in the existing supported path.

### Smoke Test

Start the watcher from a minimal config without `evaluator_enabled`. Confirm deterministic polling works and no evaluator process starts.

### Exit Gate

AI evaluation is opt-in without affecting worker agents or deterministic monitoring.

## Phase 9: Add Generic Configuration and Operating Documentation

### Goal

Make the harness usable for coding without removing the documentation needed by the supported firmware path.

### Artifacts

- One generic harness configuration example.
- One coding invocation example.
- One coding `RESULT.json` example.
- One named-lock example.
- One branch split and worktree creation walkthrough.
- One merge-lane walkthrough.
- One rollback and promotion checklist.

### Documentation Requirements

- Explain that one branch is not enough; every concurrent lane needs a separate worktree.
- Explain that the manager plans lane splits and merges.
- Explain that Git provides code isolation and named locks cover only non-Git resources.
- Explain that the frozen harness controls development and the candidate controls only full acceptance.
- Explain that `.agent-workspace`, `PARALLEL_CHECKPOINT.md`, and `RESULT.json` filenames remain.
- Explain how to keep runtime state out of Git.
- Explain exact commands for validation and clean shutdown.
- Keep firmware operating instructions, clearly label them as the firmware workflow, and make the generic coding quick start the primary entry point.

### Documentation Smoke Test

Follow the generic quick start from a clean temporary repository without using undocumented files or manual repairs.

### Exit Gate

A new user can launch one fake coding lane and inspect its result using only the generic documentation.

## Phase 10: Build the Automated Test Pyramid

### Unit Test Layer

Run fast, isolated tests for:

- Coding invocation contracts.
- Reusable process, event, checkpoint, and recovery safety.
- Git worktree and branch validation.
- Result parsing and merge readiness.
- Lock acquisition, waiting, release, and stale evidence.
- Snapshot reconciliation.
- Event stability and acknowledgement.
- Evaluator configuration.
- Existing firmware invocation, MCP lifetime, relay binding, board-resource, and reconciliation behavior.

### Component Smoke Layer

Maintain small executable smokes for:

1. One coding controller with fake Codex.
2. Two worktrees with correct and incorrect branch declarations.
3. One valid and several invalid results.
4. Two controllers contending for one generic lock.
5. One stale lock and one unknown-owner lock.
6. One full event delivery and acknowledgement cycle.
7. One controller resume and process-identity safety run.
8. Watcher startup with evaluation omitted.
9. One existing policy-bound firmware controller run with fake Codex.

### Integration Layer

Add an isolated temporary-repository test that:

1. Creates an initial Git commit.
2. Creates two branches and worktrees.
3. Starts two coding controllers with fake Codex workers.
4. Confirms independent Git identity.
5. Exercises one shared generic lock.
6. Publishes one stale result and confirms rejection.
7. Publishes current committed results and confirms merge readiness.
8. Creates an integration branch and merges both results.
9. Runs a small Python test suite.
10. Confirms durable events and exact acknowledgement.

### Regression Layer

Run:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Use `--full` when changing watcher retention or lifecycle behavior.

The regression gate includes Ruff, formatting, BasedPyright, compilation, orchestrator tests, watcher tests, Codex development integration tests, and the existing synthetic firmware coverage. At the measured baseline, the complete orchestrator suite runs 208 tests in about 28 seconds on the current Windows development machine.

The routine regression gate must not require a physical board, firmware server, or MCP device. Run real firmware/hardware acceptance only before releases or after hardware-specific changes.

### Stress Layer

- Repeat lock contention enough times to catch overlap and cleanup races.
- Repeat worktree creation and removal cycles.
- Repeat stale-result replacement and event deduplication.
- Run relevant subprocess tests under Windows load.
- Confirm every spawned process and temporary worktree is cleaned up exactly.

### Exit Gate

All automated layers pass before full candidate acceptance.

## Phase 11: Prepare the Full Practical Acceptance Test

### Goal

Test the candidate as a real multi-agent harness by having it build a complete disposable Python application.

### Authority Rules

1. Finish or checkpoint development controlled by the frozen harness.
2. Record the candidate commit under test.
3. Stop the frozen harness and confirm its exact processes are gone.
4. Start an external acceptance-test supervisor.
5. Start the candidate as the only active orchestration harness.
6. Start the deterministic watcher.
7. Enable the read-only watcher subagent only for this acceptance run.
8. Use fresh runtime, output, event, acknowledgement, lock, and epoch paths.

### Watcher Subagent Rules

- Read candidate and watcher evidence only.
- Never edit the harness or target project.
- Never direct or message coding workers.
- Never acknowledge harness events.
- Never stop processes.
- Publish a critical finding with exact evidence when a harness invariant is broken.

Only the external supervisor may stop the acceptance run.

## Phase 12: Final Practical Coding Project

### Project

Build a local Python task-tracking application called `taskboard`.

The project is deliberately large enough to require planning, several serialized production-code lanes, integration, parallel disjoint test and documentation authoring, parallel test execution, and recovery while remaining deterministic and local.

### Runtime Constraints

- Python 3.11 or newer.
- Standard library runtime dependencies only.
- No network access.
- No secrets.
- No hardware.
- No production services.
- SQLite database stored in a configurable local path.
- Tests may use the existing repository test runner.

### Functional Requirements

#### Domain Model

- Projects contain tasks.
- Tasks have stable IDs, titles, descriptions, creation times, and statuses.
- Statuses include `todo`, `in_progress`, `blocked`, and `done`.
- Status transitions are validated.
- Tasks may depend on other tasks.
- A task cannot become `done` while an unfinished dependency remains.
- Dependency cycles are rejected.

#### Storage

- SQLite schema creation is automatic.
- Projects, tasks, and dependencies persist across process runs.
- Writes use transactions.
- Invalid references fail without partial updates.
- Tests use isolated temporary databases.

#### Service Layer

- Create, update, list, and retrieve projects and tasks.
- Change task status under domain rules.
- Add and remove dependencies.
- Filter tasks by project and status.
- Produce a summary containing task counts by status.

#### Command-Line Interface

- Create and list projects.
- Create, show, list, and update tasks.
- Add and remove task dependencies.
- Filter task listings.
- Show project summaries.
- Select the database path explicitly.
- Return nonzero exit codes and clear messages for invalid input.

#### Import And Export

- Export a project, its tasks, and dependencies to deterministic JSON.
- Import valid exported JSON into an empty database.
- Reject malformed data, duplicate identities, invalid statuses, missing dependencies, and cycles.
- Leave the database unchanged after a failed import.

#### Quality

- Public functions have useful type annotations.
- Domain, storage, service, CLI, and import/export behavior have tests.
- One end-to-end test uses the CLI across multiple process invocations.
- A README explains setup and example commands.

### Why This Project Tests the Harness

- Separate modules create clear boundaries for serialized production coding and parallel test or documentation files with disjoint ownership.
- Shared domain interfaces test whether branches remain compatible.
- SQLite and import transactions provide meaningful correctness checks.
- The branch structure tests verified worktrees and base commits.
- Merge readiness requires valid branch-tip results.
- An integration branch must combine independently completed work.
- A declared test resource can exercise automatic named-lock waiting.
- A deliberate checkpoint and resume can exercise Codex thread recovery.
- A pre-seeded stale result can prove stale invocation rejection.
- Final tests distinguish ordinary application bugs from harness defects.

### Required Harness Behaviors During the Project

The acceptance supervisor verifies that:

1. The candidate manager creates a sensible plan from the project request.
2. Only one production-code lane runs at a time.
3. Independent test and documentation authors may run concurrently in different worktrees when the manager assigns disjoint files.
4. Child work begins from recorded stable commits.
5. At least two test lane controllers request the same test-only generic resource and are serialized automatically.
6. Normal resource waiting does not require manager intervention.
7. One lane publishes a checkpoint and successfully resumes.
8. A stale or mismatched result is not accepted.
9. Every merge-ready lane identifies a real current branch-tip commit.
10. A merge lane integrates completed inputs.
11. Merge conflicts or failing application tests are handled as coding work, not immediate harness failure.
12. Final application tests pass.
13. Exact event acknowledgement and clean process shutdown succeed.

The candidate manager chooses the detailed decomposition. Planning and production-code lanes remain serialized; test and documentation authoring may be parallel only after it assigns exact disjoint ownership. Planning quality is part of what is being observed.

### Critical Abort Conditions

The watcher subagent reports, and the supervisor aborts, only for harness-level failures such as:

- Editing outside a declared worktree.
- Duplicate active branch or worktree use.
- Overlapping ownership of one generic lock.
- Invalid result accepted as merge-ready.
- Lost or misidentified processes.
- Corrupted event, acknowledgement, or lock state.
- False success while required work failed.
- Unrecoverable harness deadlock.
- Access to frozen harness runtime state.
- Unsafe or incomplete exact-process shutdown.

Do not abort for a normal application bug, failed test, retry, or merge conflict unless the candidate handles it incorrectly.

### Acceptance Success Criteria

- The finished `taskboard` application meets every functional requirement.
- All application tests pass.
- The candidate harness meets every required behavior above.
- No critical watcher finding remains unresolved.
- Candidate processes and runtime state shut down cleanly.
- Evidence is sufficient to reproduce the run.

## Phase 13: Failure, Repair, and Rerun

### On Critical Failure

1. Supervisor stops new launches.
2. Supervisor requests cooperative candidate shutdown.
3. Supervisor stops only exact remaining candidate descendants if required.
4. Preserve logs, events, checkpoints, branches, claims, and process evidence.
5. Confirm the candidate topology is completely stopped.
6. Mark the candidate epoch failed and never reuse it.

### Repair

1. Restart the frozen harness in a new repair epoch.
2. Spawn the repair process against candidate source only.
3. Keep repair branches, agents, and state separate from the failed acceptance project.
4. Add a regression test reproducing the critical defect.
5. Fix the defect and run focused plus full regression tests.
6. Stop the frozen harness before trying acceptance again.
7. Create a fresh target repository and candidate epoch for the rerun.

## Phase 14: Promotion

### Tasks

1. Record the passing candidate commit.
2. Record unit, smoke, integration, stress, reusable safety regression, and practical acceptance evidence.
3. Stop and confirm all acceptance processes.
4. Mark the candidate commit as promoted.
5. Start a fresh real epoch using the promoted harness.
6. Keep the frozen baseline inactive but available for rollback.
7. Do not reuse acceptance runtime or target-project state for real work.

## Final Definition of Done

The product is complete when:

- Reusable process, path, event, checkpoint, acknowledgement, and recovery behavior remains verified.
- Ordinary coding lanes use the versioned coding invocation contract.
- Existing firmware lanes remain supported through their policy-bound invocation contract.
- Git worktree, branch, base commit, and invocation identity are proven.
- Coding results are merge-ready only when tied to valid branch-tip commits.
- Generic named locks serialize external resources automatically.
- Normal lock contention does not burden the manager.
- Unknown lock ownership fails safely.
- AI evaluation is off by default.
- Generic documentation works from a clean repository.
- Unit, smoke, integration, stress, and full regression tests pass.
- All retained synthetic firmware tests pass; no physical hardware run is required for ordinary coding changes.
- The candidate builds the complete `taskboard` application through a real multi-agent acceptance run.
- The read-only watcher and external supervisor find no unresolved critical harness defect.
- Promotion and rollback procedures are proven.

Stop at this point. Do not add more abstraction until a real post-promotion project demonstrates a specific need.
