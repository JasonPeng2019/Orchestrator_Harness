# The Minimum Needed to Generalize the Harness

The harness already works as a multi-agent coding system. The safest plan is to keep its manager, lanes, controller, events, checkpoints, results, and recovery behavior.

The goal is to add ordinary coding support to the same reliable lane system while retaining the existing firmware path as a supported product feature.

This does not require a large compatibility framework. Keep the existing firmware invocation and observation behavior intact, then route new versioned coding invocations through the general coding validation described below.

## Use Git As the Lane Structure

Plan the work before launching agents.

Each lane should have:

- One planned task.
- One Git branch.
- One separate Git worktree.
- One Codex worker.
- The existing harness status, checkpoint, result, and event files.

A branch alone is not enough for concurrent work because switching branches changes the shared working directory. Each active lane needs its own worktree.

When one lane splits into two:

1. Commit the parent lane's stable work.
2. Create both child branches from that commit.
3. Give each branch a separate worktree.
4. Launch one worker in each worktree.

When lanes need to rejoin, launch a merge worker in another branch and worktree. That worker merges the input branches, resolves conflicts, runs tests, and publishes the normal result.

## Verify Each Lane's Git Identity

The harness should record and verify:

```json
{
  "worker_invocation_id": "worker-parser-001",
  "lane_id": "parser",
  "worktree": "C:/project-worktrees/parser",
  "branch": "lane/parser",
  "base_commit": "abc123...",
  "merge_inputs": []
}
```

Before launching Codex, confirm that the worktree exists, has the expected branch checked out, and contains the base commit. Also report if two active lanes use the same worktree or branch.

This is not a scheduler. It prevents a lane from silently running in the wrong Git location and gives a restarted manager a durable record of the lane plan.

## Validate Results Before Merging

Keep `RESULT.json`, but require a small merge-ready result:

```json
{
  "schema": "orchestrator-lane-result/v1",
  "lane_id": "parser",
  "worker_invocation_id": "worker-parser-001",
  "outcome": "completed",
  "branch": "lane/parser",
  "commit_sha": "def456...",
  "summary": "Implemented the parser.",
  "checks": [
    {"name": "pytest tests/test_parser.py", "status": "passed"}
  ]
}
```

Before calling the lane merge-ready, confirm that the result belongs to the current lane attempt, the branch matches, the commit exists at the branch tip, and no project changes were forgotten in the worktree.

The harness records the worker's reported checks. The merge worker still runs final integration checks.

## Ownership Can Stay Simple

For ordinary code, each lane owns its branch and worktree. The harness does not need a new file-ownership system.

If two lanes edit the same code, Git reports the conflict when the merge worker combines them.

For external resources, the manager only declares opaque names in the lane plan:

```json
{
  "exclusive_resources": ["staging-database"]
}
```

The lane controller handles the rest automatically. If two lanes request `staging-database`, one runs while the other waits without launching Codex. When the first lane finishes, its controller releases the lock and the waiting lane continues.

The harness does not need separate cases for databases, services, ports, accounts, or deployment environments.

A lock claim records its exact owner:

```json
{
  "resource": "staging-database",
  "lane_id": "lane-a",
  "worker_invocation_id": "worker-...",
  "controller_pid": 1234,
  "controller_created_utc": "..."
}
```

Normal acquisition, waiting, and release require no manager involvement. The manager is notified only when a claim is stale, malformed, or waiting unusually long.

Do not add expiry, capacity, shared-lock modes, or resource-specific adapters. Never automatically release a claim while the owner's process identity is unknown.

Use the same generic lock for every external resource. If a future task uses hardware, it can declare an opaque name such as `board:test-device-1`; the harness does not need hardware-specific rules.

## Only Seven Changes Are Needed

### 1. Add the General Coding Contract

The lane controller currently requires a fixed firmware policy, exact prompt headings, firmware server information, and fixed Codex settings.

Keep those requirements for existing firmware invocations. Add a versioned coding contract that:

- Accepts a normal coding prompt.
- Keeps prompt hash and path safety checks.
- Does not require hardware, lease, board, MCP, or server fields.
- Uses generic `exclusive_resources` instead.
- Allows configured Codex model, reasoning, sandbox, and approval settings.
- Preserves all existing process, thread, output, exit, and resume tracking.

Use a small contract dispatcher rather than a broad profile or adapter system. Existing policy-bound invocations continue through the current firmware validator. New coding invocations use the general validator. Both share the existing process, path, output, failure, and resume machinery.

### 2. Add Durable Git Lane Identity

Attach the worktree, branch, base commit, worker invocation, and merge inputs to the existing lane invocation. Verify the Git facts before launching Codex.

### 3. Validate Merge-Ready Results

Keep `RESULT.json`, but require it to identify the current lane, worker invocation, branch, commit, summary, and reported checks. Do not treat a stale or malformed file as completion.

### 4. Add the Generic Named Lock

Add optional `exclusive_resources` to a lane invocation.

Before launching Codex, the controller atomically claims every requested name in a consistent order. It waits when a name is occupied and releases only claims matching its exact lane, invocation, PID, and process creation identity.

Reuse the harness's existing resource-conflict events. Add manager attention only for stale, malformed, unknown, or excessively delayed claims.

### 5. Add a Generic Example

Document how to:

- Create branch/worktree lanes.
- Point existing `run_globs` at them.
- Launch normal coding workers.
- Wait for current harness events.
- Publish the existing checkpoint and result files.
- Launch a merge worker.

Keep `.agent-workspace`, `PARALLEL_CHECKPOINT.md`, and `RESULT.json`. Renaming them is unnecessary.

### 6. Add One End-to-End Test

Create a temporary Python Git repository, run two separate worktree lanes, then run a merge lane.

The test should prove that:

- Both lanes are tracked independently.
- Coding invocations do not supply firmware, hardware, MCP, or relay records.
- Existing checkpoints, results, events, and acknowledgements work.
- The merged Python tests pass.

This test is the real proof that the harness is generalized.

### 7. Turn AI Evaluation Off by Default

Use deterministic monitoring unless AI evaluation is explicitly enabled. This does not disable the Codex workers.

## Do Not Change Yet

Do not add or rewrite:

- The lane architecture.
- An automatic scheduler.
- A task database.
- Formal lane-dependency records.
- General file ownership.
- Worker states.
- Event names or acknowledgement.
- The checkpoint format or any broader result redesign beyond the minimal merge-ready fields.
- Discovery and reconciliation architecture.
- A project-adapter framework.
- A broad firmware adapter or compatibility framework beyond the small versioned contract boundary.
- Harness-enforced Ruff, Pyright, or test commands.

The manager already controls ordering, and Git branches record where work splits and merges. The merge worker can run project checks through its normal instructions.

## Firmware Test Cost

Firmware remains supported, so its automated compatibility tests remain required.

The current orchestrator suite contains 208 tests and completed in about 28 seconds on the current Windows development machine. These tests use synthetic files and process fixtures; they do not contact a real board, firmware server, or MCP device.

Expected preservation cost during generalization:

- Approximately 1–3 agent-hours to keep the firmware invocation and result routes separate from the new coding routes.
- About 28 seconds for the whole orchestrator test suite per verification run; firmware tests are only part of that time.
- Little ongoing work unless shared controller, reconciliation, result, or event behavior changes.

Real-hardware acceptance is not required on every change. Run it only for releases or changes to hardware-specific behavior.

## Practical Stopping Point

Make the seven contained changes additively, keep the synthetic firmware tests passing, add the coding tests, and use the harness on the next real coding project.

Only add more abstraction when that real project reveals a specific limitation. Do not redesign working parts in anticipation of problems that may never occur.
