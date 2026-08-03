# Simple Roadmap for Generalizing the Harness

## Goal

Keep the harness and its supported firmware workflow, then add a separate path for normal Python coding projects.

Make the changes one at a time. Finish and test each step before moving on.

## Step 1: Freeze the Current Version

1. Commit the current repository.
2. Make a frozen copy that will coordinate development.
3. Make a candidate copy where changes will be written.
4. Keep their logs and runtime files completely separate.
5. Run the full current test suite and record the passing baseline.

## Step 2: Protect the Reliable Parts

Add tests for the reusable controller behavior before adding the coding contract.

Test that:

- Prompt hashes and safe paths are checked.
- Process and Codex thread identities are still tracked.
- Resume still works.
- Unsafe paths are rejected.
- Atomic records, events, acknowledgements, checkpoints, and recovery still work.

Keep the existing synthetic firmware tests required. They protect a supported product path and already run without physical hardware.

## Step 3: Define the New Coding Records

Define three small formats:

- A coding-lane invocation.
- A merge-ready `RESULT.json`.
- A generic resource-lock claim.

A coding lane records its lane ID, worker attempt, task, worktree, branch, base commit, merge inputs, and required named resources.

A result records its lane, worker attempt, branch, commit, summary, and checks.

A lock records a plain resource name and its exact owning controller.

Write format-validation tests before connecting these records to the controller.

## Step 4: Add the General Coding Path

Keep the existing firmware contract and add a versioned coding contract.

The converted controller should:

- Accept a normal coding prompt.
- Keep prompt hash and path checks.
- Do not require firmware prompt headings or policy files for coding invocations.
- Do not include hardware, lease, MCP, relay, or server fields in coding invocations.
- Use generic named resources instead.
- Use configured Codex settings.
- Keep all existing process, output, thread, failure, and resume tracking.

Use a small contract dispatcher, not a large profile framework. Existing firmware invocations keep their current validation; coding invocations use the new contract.

Smoke test one coding lane and one existing policy-bound firmware lane with fake Codex.

## Step 5: Verify the Git Worktree

Before launching Codex, confirm:

- The lane directory is a real Git worktree.
- It has the expected branch checked out.
- The base commit exists.
- Another active lane is not using the same branch or worktree.

Test correct worktrees, wrong branches, missing commits, duplicate branches, duplicate worktrees, and resume after an unexpected branch switch.

Smoke test: create two temporary worktrees, validate both, then prove a wrong-branch lane never launches Codex.

## Step 6: Validate Results

Keep the filename `RESULT.json`, but stop treating any JSON file as successful completion.

Before a lane is ready to merge, confirm:

- The result belongs to the current lane and worker attempt.
- The branch is correct.
- The commit exists at the branch tip.
- No project changes were forgotten in the worktree.
- The result summary and reported checks are valid.

Test stale results, wrong lanes, wrong branches, missing commits, old commits, dirty worktrees, malformed checks, and corrected replacement results.

Smoke test: accept one valid committed result and reject stale and wrong-branch results.

## Step 7: Add Generic Named Locks

A lane may request a plain name such as:

```json
{
  "exclusive_resources": ["staging-database"]
}
```

Before launching Codex, the controller claims every required name.

If a name is busy:

- Do not launch Codex.
- Wait automatically.
- Start after the current owner releases it.

Only the exact owner may release a claim. Never release a claim when owner identity is unknown.

Test normal acquisition, contention, different names, multiple names, normal release, crashes, stale owners, unknown owners, malformed claims, and incorrect release attempts.

Stress test the same lock through at least 100 acquisition cycles and prove protected work never overlaps.

## Step 8: Connect Everything to Existing Events

Add the new facts to current lane snapshots and events:

- Worker attempt and coding invocation identity.
- Git identity.
- Requested and held locks.
- Resource waiting.
- Invalid result reasons.
- Merge-ready state.

Keep the existing durable event IDs and exact acknowledgement process.

Short normal lock waits should not wake the manager. Stale, malformed, unknown, or excessively delayed claims should.

Smoke test one lane through waiting, running, invalid result, corrected result, merge-ready state, and exact acknowledgement.

## Step 9: Turn AI Evaluation Off by Default

When the setting is omitted, use deterministic monitoring without starting an AI evaluator.

Test omitted, explicit false, explicit true, and invalid settings.

## Step 10: Write the Generic Instructions

Document how to:

- Create branches and worktrees.
- Start coding lanes.
- Split work from a stable commit.
- Merge completed branches.
- Declare named resources.
- Write a valid result.
- Stop, roll back, and promote the harness.

Keep `.agent-workspace`, `PARALLEL_CHECKPOINT.md`, and `RESULT.json`.

Follow the documentation once from a clean temporary repository.

## Step 11: Run the Automated Tests

Run four levels of tests.

### Unit Tests

Test every validator, Git check, lock operation, state transition, and configuration setting by itself.

### Smoke Tests

Run small complete examples for coding launch, Git validation, result validation, lock contention, event acknowledgement, process/resume safety, and watcher startup.

### Integration Test

Create two temporary worktrees, run two fake coding lanes, exercise one shared lock, reject a stale result, accept valid committed results, merge both branches, and run a small Python test.

### Full Regression Test

Run:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Everything must pass before the candidate controls real agents.

Keep the existing synthetic firmware tests in this required gate. The measured orchestrator baseline is 208 tests in about 28 seconds on the current Windows development machine. Preserving the firmware path is expected to add roughly 1–3 agent-hours to the conversion.

These routine tests use no real board, firmware server, or MCP device. Run physical firmware acceptance only for a release or a change to hardware-specific behavior.

## Step 12: Prepare the Full Candidate Test

1. Finish or checkpoint frozen-harness development.
2. Stop the frozen harness completely.
3. Start an outside test supervisor.
4. Start the candidate as the only active harness.
5. Start deterministic watcher logging.
6. Enable the read-only watcher subagent only for this test.
7. Use a new temporary project and new runtime directories.

The watcher subagent may report critical problems but cannot edit, direct agents, acknowledge events, stop processes, or fix code. Only the outside supervisor may stop the test.

## Step 13: Build the Practical Test Project

Have the candidate harness build a local Python task tracker called `taskboard` from beginning to end.

It should support:

- Projects and tasks.
- Task statuses and valid status changes.
- Dependencies between tasks.
- Cycle detection.
- SQLite storage.
- A command-line interface.
- JSON import and export.
- Filtering and summaries.
- Unit and integration tests.
- A README with examples.

Use only local files and the Python standard library. Do not use network services, secrets, hardware, or production systems.

This project is useful because it naturally has separate modules, shared interfaces, database behavior, branch merging, and meaningful tests.

The full run should prove:

- Only one production-code lane runs at a time.
- Disjoint test and documentation authors can run concurrently in separate worktrees.
- Independent test executions can run concurrently with isolated writable state.
- Every lane uses its declared branch and worktree.
- Child work starts from recorded commits.
- A shared named resource is serialized automatically.
- One lane checkpoints and resumes.
- A stale result is rejected.
- Valid results point to real branch-tip commits.
- A merge lane combines the work.
- Final application tests pass.
- Events are acknowledged exactly.
- All candidate processes stop cleanly.

Do not abort because application code has a normal bug, a test fails, or a merge conflict occurs. The candidate should handle those problems.

Abort only if the harness breaks an important rule, such as using the wrong worktree, overlapping one lock, accepting an invalid result, corrupting events, losing processes, falsely claiming success, or shutting down unsafely.

## Step 14: Repair or Promote

If the test fails:

1. Stop the candidate completely.
2. Save all evidence.
3. Restart the frozen harness in a new repair run.
4. Fix the candidate and add a regression test.
5. Repeat acceptance with a fresh project and epoch.

If the test passes:

1. Record the passing candidate commit.
2. Stop the acceptance run.
3. Promote the candidate.
4. Start a fresh real epoch.
5. Keep the frozen harness turned off but available for rollback.

## Final Stopping Point

Stop adding features when:

- Reusable safety behavior works for both invocation paths.
- Normal coding lanes use the versioned coding contract.
- Existing synthetic firmware tests still pass.
- Git identity, results, and locks are safe.
- AI evaluation is off by default.
- All automated tests pass.
- The candidate successfully builds and merges the complete `taskboard` project.
- The watcher finds no unresolved critical harness failure.

Use the promoted harness on a real project before considering any more abstractions.
