# Minimal-Risk Generalization Specification

Status: archived V1 contract; non-operative. Use `GENERALIZATION_SPEC_2.md` plus the live goal,
execution plan, `task-card-spec.md`, and `test-cleanup.md`.  
Scope: make the existing multi-agent harness usable for ordinary Python coding without redesigning it

## 1. Starting Point

The portable harness is already a working multi-agent coding system.

It already provides:

- A manager that plans and coordinates work.
- Parallel Codex lanes.
- A controller that launches and resumes Codex workers.
- Exact controller and Codex process tracking.
- Durable events and acknowledgements.
- Checkpoints and results.
- Manager notifications.
- Restart recovery and stale-worker detection.
- Exact resource-conflict detection that can be simplified into generic named locks.

Generalization must preserve the reliable manager, lane, process, event, checkpoint, result, and recovery behavior. The goal is not to replace lanes, add an automatic scheduler, or create a new orchestration protocol. The goal is to add a general coding path to the existing lane workflow.

### 1.1 Supported Firmware Decision

Keep the existing firmware path as a supported product feature:

- Keep passive permission, relay, MCP, board, and hardware observation. These paths already do nothing when their records are absent.
- Keep policy-bound firmware invocation under its existing contract.
- Keep existing firmware result handling for firmware controller records.
- Keep existing synthetic firmware tests in the required regression gate.

Add a small versioned contract boundary, not a broad profile or adapter framework. `orchestrator-coding-invocation/v1` uses the new coding rules; existing firmware invocations retain their policy-bound rules. Shared process, output, event, checkpoint, acknowledgement, and recovery machinery serves both paths.

The measured baseline is 208 orchestrator tests in about 28 seconds on the current Windows development machine. These are synthetic tests and use no physical board, firmware server, or MCP device. Preserving the firmware routes is expected to add roughly 1–3 agent-hours during conversion. Physical firmware acceptance is release-only or required after hardware-specific changes, not after ordinary coding-path changes.

## 2. General Coding Workflow

The manager plans the work before launching workers.

Each lane has:

- One planned coding task or task group.
- One Git branch.
- One separate Git worktree.
- One Codex worker at a time.
- The existing lane status, event, checkpoint, and result records.

The manager decides when lanes start, split, wait, and merge. The harness observes and manages the existing coordination protocol. It does not need to calculate a task graph or assign tasks automatically.

## 3. Branch And Worktree Model

### 3.1 One Worktree Per Concurrent Lane

A Git branch alone does not isolate a working directory. Every concurrently active lane must have its own worktree.

```text
project/                 main or integration worktree
project-worktrees/
  parser/                branch lane/parser
  database/              branch lane/database
  tests/                 branch lane/tests
```

Workers must not switch branches in a worktree another worker is using.

### 3.2 Splitting A Lane

Before lane A splits:

1. Lane A reaches a stable commit.
2. Child branches are created from that exact commit.
3. Each child branch receives a separate worktree.
4. One Codex worker is launched in each child worktree.

Conceptually:

```text
lane-a
  |\
  | lane-b
  | lane-c
```

The shared base commit records exactly where the work diverged. The harness does not need a separate dependency database for this.

### 3.3 Merging Lanes

A merge is performed by another manager-assigned lane.

The merge worker:

- Uses a dedicated integration branch and worktree.
- Merges the completed input branches.
- Resolves code conflicts.
- Reconciles incompatible design choices.
- Runs the required integration checks.
- Publishes the normal checkpoint or result.

The manager launches the merge lane only after its input lanes finish. This ordering can remain in the manager's plan; it does not need to be enforced by a new scheduler.

### 3.4 Durable Lane And Git Identity

The existing lane invocation already records the lane ID, task, and `run_root`. In general coding mode, `run_root` is the lane worktree and the invocation also records:

```json
{
  "worker_invocation_id": "worker-parser-001",
  "declared_lane_id": "parser",
  "task": "Implement the parser",
  "run_root": "C:/project-worktrees/parser",
  "git": {
    "branch": "lane/parser",
    "base_commit": "abc123...",
    "merge_inputs": []
  }
}
```

A merge lane lists the branches it is expected to combine in `merge_inputs`.

Before launching Codex, the controller validates:

- `run_root` is a real Git worktree.
- The worktree has the declared branch checked out.
- The declared base commit exists.
- The lane and worker invocation IDs are non-empty.

The harness detects and reports two active lanes declaring the same worktree or branch. It does not schedule lanes or interpret the Git graph.

This record makes the manager's plan recoverable and prevents a worker from silently running on the wrong branch.

### 3.5 Minimal Merge-Ready Result

Keep the `RESULT.json` filename, but do not treat the presence of any JSON object as successful completion.

A completed coding lane publishes:

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
      "name": "pytest tests/test_parser.py",
      "status": "passed"
    }
  ]
}
```

Before reporting the lane as merge-ready, validate:

- The schema is supported.
- Lane and worker invocation IDs match the current lane attempt.
- The outcome is a recognized terminal value.
- The declared branch matches the lane invocation.
- The commit exists and is the current tip of that branch.
- The worktree has no uncommitted project changes outside ignored runtime state.
- The summary and checks have valid shapes.

The harness records reported checks but does not rerun arbitrary project commands. The merge worker remains responsible for final integration checks.

An absent, stale, malformed, mismatched, or uncommitted result produces an invalid-result event and does not make the lane merge-ready.

## 4. Ownership Model

For ordinary source code, the branch and worktree are the ownership boundary.

The harness does not need general file-ownership records. Two lanes may edit the same logical file on separate branches without a filesystem race. Git exposes incompatible edits when the merge lane combines them.

### 4.1 Manager Declares Resources, Controller Enforces Them

Git cannot isolate every external resource, but the harness does not need separate logic for databases, services, ports, deployment environments, accounts, and other possible dependencies.

The manager records opaque resource names in each lane plan. The lane controller automatically acquires those names before launching Codex, waits when a name is already held, and releases them when the lane finishes.

```text
lane-a: database migration  -> staging-database
lane-b: API implementation -> no external resource
lane-c: deployment test    -> staging-database
```

The manager may launch all three lane controllers. Lanes A and B start immediately. Lane C waits automatically until A releases `staging-database`, so normal contention does not require manager attention.

### 4.2 Generic Exclusive Named Lock

Use one opaque exclusive named lock:

```json
{
  "exclusive_resources": ["staging-database"]
}
```

The harness knows only that two active lanes cannot hold the same exact resource name. It does not know whether the name represents a database, service, account, port, or environment.

Required behavior:

- One lock type: exclusive.
- Exact string matching.
- Requested in the lane invocation before Codex launch.
- Atomic acquisition so two controllers cannot both succeed.
- Canonical name ordering when a lane requests multiple locks.
- A waiting controller publishes `WAITING_RESOURCE` and retries without launching Codex.
- Normal release when the controller finishes.
- A claim records the resource name, lane ID, worker invocation ID, controller PID, and controller creation identity.
- A controller releases only claims whose exact owner identity matches its invocation.
- A crashed owner's claim is considered stale only when exact process reconciliation proves that owner absent.
- A claim is never automatically released while process state is unknown.
- Manager notification only for stale, malformed, or excessively delayed claims.
- No resource-specific adapters, capacity, shared-lock mode, approval rules, or dependency types.

The existing resource-conflict snapshot and `RESOURCE_CONFLICT` event machinery should be reused rather than replaced. Add focused waiting/stale-lock events only where the current events cannot describe the lock condition truthfully.

### 4.3 No Specialized Resource Types

Generic exclusive names are the only resource mechanism required by new coding lanes.

If a future coding task happens to use a physical or external resource, the manager declares an opaque name such as `board:test-device-1` or `service:staging`. The lock system does not interpret the prefix.

Existing board, probe, serial, MCP, relay, and lease observation remains supported for firmware records and stays passive when those records are absent. Do not connect new coding features to those specialized rules or build a broad adapter framework around them.

## 5. Existing Conventions To Keep

The first general version keeps these existing conventions:

- Lanes and manager-driven lane assignment.
- `.agent-workspace` as the lane runtime directory.
- `PARALLEL_CHECKPOINT.md` as the checkpoint filename.
- `RESULT.json` as the result filename, with the minimal merge-ready validation in section 3.5.
- Current worker and operational states.
- Current event types, priorities, pending delivery, and acknowledgement.
- Current manager signals.
- Current process identity and recovery rules.
- Current polling and managed-watch behavior.
- Existing discovery and reconciliation infrastructure, including dormant legacy observations that do not affect coding lanes.

These can be renamed or redesigned later only if real use demonstrates a problem. Renaming them is not required to run ordinary Python work.

## 6. Required Changes

Only seven initial changes are required.

### 6.1 Convert The Lane Controller To General Coding

The current controller requires several firmware-run details even when the lane only edits code:

- A fixed autonomous policy file.
- Exact firmware-era prompt headings.
- A fixed event-log location and filename.
- A required server snapshot.
- Firmware-oriented hardware and MCP metadata.
- Fixed Codex approval and sandbox arguments.

Add `orchestrator-coding-invocation/v1` beside the existing firmware invocation contract. Dispatch by contract rather than introducing a broad profile framework.

The general coding controller must:

- Accept an ordinary manager-written task prompt.
- Continue validating the prompt hash.
- Keep output paths confined to the lane worktree and runtime roots.
- Make server snapshot, hardware, lease, board, and MCP fields optional and irrelevant to a normal coding invocation.
- Use `exclusive_resources` for every non-Git resource.
- Allow the lane event log under the configured harness runtime root.
- Use configured Codex model, reasoning, sandbox, approval, and service-tier settings.
- Preserve controller PID, Codex PID, process creation identity, thread ID, JSONL, stderr, last message, exit code, start, and resume behavior.

Conversion requirement:

- Do not require firmware-era prompt headings or policy-file coupling on the coding path; retain the existing validation for firmware invocations.
- Make fixed firmware sandbox, approval, and model assumptions configurable for coding invocations while retaining current values as defaults where useful.
- Add coding contract tests alongside the required synthetic firmware tests.
- Preserve process identity, path confinement, start, resume, output, and failure safety.

### 6.2 Add Durable Lane And Git Identity

Extend general coding invocations with `worker_invocation_id` and the small `git` object from section 3.4. Validate the worktree, branch, and base commit before launching Codex. Publish the verified values in controller status so reconciliation and recovery use the same identity.

Reuse the existing lane and process records. Do not add a task database or Git scheduler.

Tests must cover the correct worktree, wrong branch, missing base commit, duplicate active worktree, duplicate active branch, and resume of the same lane with a new worker invocation ID.

### 6.3 Validate Merge-Ready Results

Validate `RESULT.json` using section 3.5 before changing a lane to terminal/merge-ready state.

Tests must reject stale invocation IDs, wrong lanes, wrong branches, missing commits, non-tip commits, dirty project worktrees, malformed checks, and unsupported outcomes. Coding results are the only supported terminal-result contract in the candidate.

### 6.4 Add The Generic Exclusive Named Lock

Add optional `exclusive_resources` to the lane invocation and persisted controller status.

Implement atomic claim, waiting, matching-owner release, and stale-claim reconciliation as defined in section 4. Do not add resource categories or resource-specific behavior.

Tests must cover:

- An uncontended lane acquiring and releasing a lock.
- Two lanes requesting the same name, with only one Codex worker running at a time.
- Different names running concurrently.
- Multiple names acquired in canonical order.
- Normal release waking a waiting lane.
- A controller crash leaving a stale claim.
- Unknown process evidence preventing automatic release.
- A controller being unable to release another invocation's claim.

### 6.5 Add A Generic Configuration And Operating Example

Add one documented example using the configuration features that already exist:

- A project or worktree-parent `suite_root`.
- `run_globs` that discover lane worktrees.
- `.agent-workspace` as `workspace_relpath`.
- A fresh output directory for the manager epoch.
- No hardware, MCP, or permission requests.
- AI evaluation disabled.

The example must show:

1. Creating two worktree lanes.
2. Launching one Codex worker in each lane.
3. Waiting for existing harness events.
4. Publishing the minimal merge-ready result.
5. Launching a merge lane.
6. Running final Python project checks.

No new project-adapter framework is required.

### 6.6 Add One General End-To-End Test

Add one test proving that the system implements the coding contract when no firmware records are supplied.

The test must:

1. Create a temporary Git repository with an initial commit.
2. Create two branches and separate worktrees.
3. Launch or simulate one coding lane in each worktree.
4. Confirm both lanes are discovered and tracked independently.
5. Confirm there are no required board, MCP, relay, or hardware records.
6. Publish checkpoints or results using the existing filenames.
7. Create a merge lane that combines both branches.
8. Run a small Python test suite.
9. Confirm normal event delivery and exact acknowledgement.
10. Confirm wrong-branch and stale results are rejected before merging.

This test is the proof of generalization. It is more valuable than a broad internal refactor.

### 6.7 Disable AI Evaluation By Default

Change the watcher so omitted configuration means:

```json
"evaluator_enabled": false
```

Update:

- The watcher configuration dataclass default.
- The configuration loader fallback.
- The example configuration.
- Focused tests and documentation.

Deterministic monitoring remains enabled. This change does not disable Codex workers.

## 7. Changes Explicitly Deferred

Do not implement these unless a real project demonstrates the need:

- A new scheduler.
- A task database.
- A parsed dependency graph.
- General file-ownership records.
- Broad replacement or renaming of worker states beyond the required `WAITING_RESOURCE` condition.
- New event names or schemas.
- A general project-adapter framework.
- Configurable checkpoint and result filenames.
- A new checkpoint format.
- A broader result redesign beyond the minimal merge-ready contract.
- Harness-enforced Ruff, Pyright, pytest, or build commands.
- Large discovery or reconciliation rewrites.
- A broad firmware adapter or profile framework beyond the small versioned contract dispatcher.
- Broad package and CLI renaming.

The manager and merge worker can run project checks through their normal Codex instructions. Harness-level validation can be added later if practical use shows it is necessary.

## 8. Risk Controls

Every generalization change must follow these rules:

1. Preserve reusable safety and reliability behavior and the currently supported firmware contract.
2. Change shared logic only where the coding contract requires it.
3. Add a focused test before or with each behavior change.
4. Keep the existing synthetic firmware suite passing as a required compatibility gate.
5. Avoid schema migrations unless required.
6. Do not rename stable files or states merely for appearance.
7. Make one independently verifiable change at a time.
8. Stop expanding scope once the generic worktree test passes.

## 9. Implementation Order

### Phase 1: Prove The Reusable Boundary

- Add characterization tests for process identity, atomic I/O, path confinement, events, acknowledgement, checkpoint/resume, and recovery behavior that will remain.
- Add the failing skeleton of the generic two-worktree test.

### Phase 2: Open The Minimum Generic Path

- Add the general coding invocation path to the lane controller.
- Route the new versioned coding contract separately while leaving firmware-only fields in the firmware contract.
- Add durable lane/worktree/branch identity and pre-launch Git validation.
- Add the minimal merge-ready result validator.
- Add generic exclusive named-lock acquisition, waiting, release, and stale-claim handling.
- Set AI evaluation to off by default.

### Phase 3: Prove And Document Usage

- Complete the two-lane plus merge-lane end-to-end test.
- Add the generic configuration and operating example.
- Run the converted orchestrator and watcher suites.

After Phase 3, use the harness on the next real Python task before making further architectural changes.

## 10. Completion Criteria

The minimal generalization is complete when:

- The manager can plan ordinary Python work into lanes.
- Each concurrent lane runs on its own branch and worktree.
- The supported coding invocation contains no required firmware, board, MCP, or relay records.
- Every coding lane is tied to a verified worktree, branch, base commit, and worker invocation.
- A lane becomes merge-ready only when its result matches the current invocation and a real branch-tip commit.
- Two lanes requesting the same generic resource are serialized automatically without launching two Codex workers.
- Normal lock waiting and release require no manager action, while stale or unknown ownership fails safely.
- The existing harness observes lane processes, checkpoints, results, and events.
- A merge worker can combine completed lane branches and run project checks.
- AI evaluation is off unless explicitly enabled.
- Coding lanes do not depend on firmware-specific behavior, fields, tests, or operating documentation.
- The supported firmware path still passes its required synthetic tests.
- The generic end-to-end worktree test passes reliably.

No broader rewrite is required to call the harness generalized for ordinary Python coding.
