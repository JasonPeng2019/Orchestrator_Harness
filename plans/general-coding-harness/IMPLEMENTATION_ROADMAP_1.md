# General Coding Harness Implementation Roadmap

Status: archived V1 roadmap; non-operative. Use
`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`.
All topology, lane, gate, review cadence, prompt/task-card invalidation, rerun, and completion rules
below are historical. They must not supplement or override the current plan.
Inputs: `GENERALIZATION_SPEC.md`, `codex_answer_1.md`, `codex_answer_2.md`, and `codex_answer_3.md`

## 1. Objective

Add a general coding workflow to the existing harness without redesigning its working coordination machinery.

The finished product supports two real paths:

- The existing firmware workflow, including policy-bound invocation, MCP and relay observation, and hardware-resource reconciliation.
- A versioned general coding workflow using Git worktrees, branch identity, merge-ready results, and generic exclusive named locks.

The implementation keeps planning and shared production-code changes serialized. Disjoint test files, disjoint documentation files, read-only reviews, and test executions are parallelized in isolated worktrees after the manager fixes their contracts and ownership.

## 2. Non-Negotiable Execution Rules

### 2.1 Concurrency Limit

- Never run more than four active agent tasks at once.
- The manager is one active agent, so it may use at most three subagents concurrently.
- If more than three independent subagent tasks are ready, queue the remainder for the next validation wave.
- Passive watcher and controller operating-system processes are infrastructure, not additional planning or coding agents.

### 2.2 Serialized Work

The following work is always performed one item at a time:

- Product planning and design decisions.
- Production-code changes.
- Changes to shared test fixtures or shared documentation files.
- Repairs after failed validation.
- Integration into the candidate branch.

Only one agent may edit production source at a time. Test and documentation authors may edit tracked files concurrently only when the manager has assigned exact, non-overlapping paths and frozen the behavior they document or test.

### 2.3 Parallel Work

After the writer commits a stable candidate, the manager may launch up to three independent validation agents. They may:

- Run different test suites in isolated worktrees.
- Perform read-only code and security reviews.
- Inspect schemas, Git behavior, process behavior, and documentation.
- Run stress tests against separate temporary repositories and runtime roots.

After serialized planning, the manager may also parallelize authoring when paths are disjoint:

- One production-code writer plus up to two test or documentation authors.
- Up to three test authors working in separate test files.
- Up to three documentation authors working in separate documents.

No parallel author may change a shared fixture, shared helper, production module, or another author's file. If that becomes necessary, the manager queues it for serialized integration.

Validation agents do not modify tracked files. They return findings to the manager, who chooses either one shared-file repair writer or another bounded disjoint authoring wave.

### 2.4 Authority

- The frozen harness is the only harness allowed to manage development agents.
- The candidate is ordinary code during implementation and focused testing.
- The frozen harness must stop completely before the candidate performs full acceptance.
- The frozen and candidate harnesses never share writable runtime, event, acknowledgement, output, or lock directories.

## 3. Git Layout

The outer repository currently has no initial commit. Establish Git history before using worktrees.

Use these durable lines:

| Line | Purpose |
|---|---|
| `baseline/firmware-supported` | Immutable commit containing the currently passing firmware harness. |
| `candidate/general-coding` | Integration branch for verified generalization phases. |
| `impl/<phase>/product` | The one active production-code branch. |
| `impl/<phase>/tests-<slice>` | Optional disjoint test-authoring branches. |
| `impl/<phase>/docs-<slice>` | Optional disjoint documentation branches. |
| `verify/<phase>/<name>` | Temporary read-only validation worktree pinned to the implementation commit. |

The manager creates all worktrees serially before starting a parallel wave. After the wave, the manager integrates author commits one at a time into the phase branch, verifies the combined result, and then merges or fast-forwards it into `candidate/general-coding`.

Do not begin the next coding phase while the current phase is uncommitted, under repair, or awaiting its final gate.

## 4. Standard Phase Cycle

Every coding phase follows the same sequence.

### Step A: Serialized Plan

The manager writes one bounded phase brief containing:

- Exact behavior to add.
- Files expected to change.
- Invariants that must not change.
- Focused tests to add.
- Required firmware regressions.
- Exit criteria.
- Exact file ownership for every proposed parallel author.

No other planning task runs concurrently.

### Step B: Bounded Authoring Wave

The manager may launch at most three authors after the phase plan is fixed:

| Role | Allowed ownership |
|---|---|
| Product writer | Production modules and any unavoidable shared helper. No other writer touches them. |
| Test author A | One explicitly assigned new or isolated test file. |
| Test or documentation author B | Another explicitly disjoint test or documentation file. |

Each author:

1. Creates or enters the phase worktree.
2. Writes only the files assigned by the manager.
3. Runs focused tests.
4. Reviews its diff for unrelated changes.
5. Commits one stable implementation candidate.
6. Publishes the commit and focused-test result.

If the phase has no safely disjoint authoring work, use only the product writer. If more than three authoring tasks are available, queue the remainder for another wave.

### Step C: Serialized Author Integration

The manager:

1. Stops the authoring wave.
2. Verifies that ownership did not overlap.
3. Integrates author commits one at a time into the phase branch.
4. Assigns one serialized writer to resolve any integration issue.
5. Runs the combined focused tests.

### Step D: Parallel Validation Wave

The manager freezes the implementation commit and launches at most three validation agents:

| Agent | Default responsibility |
|---|---|
| Validator A | New feature behavior and failure cases. |
| Validator B | Existing firmware and shared-safety regressions. |
| Validator C | Read-only design, security, concurrency, and maintainability review. |

Each validator uses a separate worktree and temporary runtime roots. Additional checks wait for the next wave.

### Step E: Repair

The manager combines the findings into one ordered repair plan. Production and shared-file repairs use one writer. Clearly disjoint test or documentation repairs may use another bounded authoring wave. Then the relevant validation wave repeats.

### Step F: Integration Gate

When all findings are resolved:

1. Run the focused phase gate once in a clean worktree.
2. Integrate the phase into `candidate/general-coding`.
3. Record the commit, commands, results, and known limitations.
4. Remove temporary implementation and validation worktrees.

### Recommended Authoring Allocation

The manager may use these allocations after completing each phase plan:

| Phase | Author 1 | Author 2 | Author 3 |
|---|---|---|---|
| AI default | Watcher configuration source | Watcher default tests | Example configuration and one assigned document |
| Coding invocation | Controller and coding parser | New coding-contract tests | New firmware/coding routing tests |
| Git identity | Git module and controller integration | Git identity unit tests | Duplicate-lane and resume tests |
| Result validation | Result module and reconciliation hook | Coding-result tests | Firmware-result routing tests |
| Named locks | Lock module and controller integration | Lock unit tests | Lock stress and crash tests |
| Reconciliation | Discovery/reconciliation/events source | Coding snapshot and event tests | Notification and firmware-routing tests |
| Documentation | Product-facing README ownership | Coding quick start and examples | Firmware documentation audit and labels |
| Integration test | Shared integration fixture owner | Success-path test file | Failure, cleanup, and repetition test file |

If an allocation requires two authors to touch the same helper or test file, it is not disjoint. The manager assigns that shared file to one author and queues the other work.

## 5. Phase 0: Establish the Baseline

### Purpose

Create a reproducible frozen harness and candidate before changing product code.

### Serialized Work

1. Review which current untracked files belong in the repository.
2. Create the initial commit.
3. Create `baseline/firmware-supported` at that commit.
4. Create the frozen harness worktree from the baseline.
5. Create `candidate/general-coding` and its candidate worktree.
6. Assign completely separate runtime directories to frozen and candidate copies.
7. Record Python, Git, Codex, Ruff, BasedPyright, and Windows versions.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run the orchestrator tests, including all synthetic firmware tests. |
| B | Run watcher tests and `.codex` integration tests. |
| C | Run Ruff, formatting, BasedPyright, compilation, and inspect repository/runtime separation. |

After the wave, run the complete verifier once serially.

### Baseline Evidence

- Baseline commit hash.
- Clean frozen worktree.
- Clean candidate worktree.
- Complete verifier output.
- Current measured reference: 208 orchestrator tests in about 28 seconds on this Windows machine.

### Exit Gate

Do not modify product code until the frozen baseline passes and the two harness copies have isolated writable state.

## 6. Phase 1: Disable AI Evaluation by Default

### Purpose

Make deterministic monitoring the default without disabling Codex workers or explicit evaluator use.

### Implementation Scope

Change:

- `harness_watcher_implementation/config.py` dataclass default from `true` to `false`.
- Configuration loader fallback from `true` to `false`.
- `harness_watcher_implementation/config.example.json` to `false`.
- Focused watcher tests for omitted, explicit false, explicit true, and invalid values.
- Generic documentation that describes the default.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run watcher configuration and polling tests. Prove omission never launches the evaluator. |
| B | Run orchestrator and firmware regressions to prove worker launching is unaffected. |
| C | Inspect documentation and every `evaluator_enabled` default or example for contradictions. |

### Exit Gate

Omitting the setting produces `false`, explicit `true` still works, and the complete verifier passes.

## 7. Phase 2: Add the Versioned Coding Invocation

### Purpose

Add ordinary coding prompts without weakening the existing firmware contract.

### Contract Boundary

- Existing schema-less policy-bound invocations continue through the current firmware validator.
- New records declare `"schema": "orchestrator-coding-invocation/v1"`.
- Unknown explicit schemas fail closed.
- Controller status records the selected invocation schema.

### Implementation Scope

1. Add `orchestrator_harness/coding_invocation.py`.
2. Parse coding lane ID, worker invocation ID, task, worktree, Git declaration, requested resources, prompt, output paths, Codex settings, and resume identity.
3. Keep prompt hash and path-confinement checks.
4. Do not require firmware policy text, server snapshots, boards, MCP servers, relays, or leases for coding invocations.
5. Preserve the existing policy-bound firmware parser and its exact checks.
6. Route both contracts into the shared launch, JSONL, stderr, thread, process-identity, exit, and resume machinery.
7. Record `invocation_schema` and `worker_invocation_id` in coding status and events.
8. Reject a resume whose invocation identity or persisted Codex thread does not match.

### Required Tests

- Minimal coding invocation.
- Ordinary prompt and prompt-hash mismatch.
- Unsafe prompt or output paths.
- Configured model, reasoning, service tier, sandbox, and approval settings.
- Start, failure, cancellation, missing thread, and resume.
- Unknown schema rejection.
- Existing policy-bound firmware controller tests unchanged.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run new coding-controller tests and adversarial input cases. |
| B | Run the existing firmware controller and discovery tests. |
| C | Review dispatch, path confinement, command construction, and resume identity without editing. |

### Exit Gate

One fake coding lane and one fake policy-bound firmware lane both complete through their own contracts, with no duplicated process-launch implementation.

## 8. Phase 3: Verify Git Lane Identity

### Purpose

Prevent a coding worker from starting in the wrong repository, worktree, or branch.

### Implementation Scope

1. Add `orchestrator_harness/git_identity.py`.
2. Execute Git without an implicit shell.
3. Verify the repository common directory and actual worktree root.
4. Verify the declared branch.
5. Verify the declared base commit exists.
6. Record repository, worktree, branch, base commit, and starting commit in controller status.
7. Revalidate the same worktree and branch on resume.
8. Detect duplicate active worktree and branch declarations during reconciliation.
9. Apply Git validation only to versioned coding invocations; do not impose it on the existing firmware contract.

### Required Tests

- Correct ordinary clone and linked worktree.
- Wrong branch.
- Non-Git directory.
- Missing base commit.
- Detached HEAD.
- Duplicate active worktree.
- Duplicate active branch.
- Windows path case and separator normalization.
- Branch switch before resume.
- Firmware controller behavior unchanged.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run valid and invalid worktree tests in an isolated temporary repository. |
| B | Run duplicate-lane and resume tests in a different temporary repository. |
| C | Review Git command safety, Windows path handling, and failure-before-launch behavior. |

### Exit Gate

A coding worker cannot launch until its Git identity is proven. Firmware invocations still follow their existing requirements.

## 9. Phase 4: Validate Merge-Ready Coding Results

### Purpose

Stop stale or uncommitted coding work from being treated as ready to merge while keeping firmware results supported.

### Implementation Scope

1. Add `orchestrator_harness/result_validation.py`.
2. Validate `orchestrator-lane-result/v1` for coding lanes.
3. Match lane ID, worker invocation ID, branch, and current branch-tip commit.
4. Reject dirty project worktrees while excluding ignored runtime state.
5. Validate outcome, summary, and reported check records without executing commands from the result file.
6. Preserve existing firmware result interpretation only for controller records identified as firmware invocations.
7. Emit a durable bounded invalid-result condition for coding lanes.
8. Clear that condition when a valid current result replaces the bad result.

### Required Tests

- Valid current coding result.
- Stale worker invocation.
- Wrong lane or branch.
- Missing or non-tip commit.
- Dirty tracked and untracked project files.
- Malformed outcomes and checks.
- Stable invalid-result event and correction.
- Firmware result accepted for a firmware lane.
- Firmware result never accepted for a coding lane.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run coding result and Git-state tests. |
| B | Run firmware result, checkpoint, discovery, and reconciliation regressions. |
| C | Review schema routing, dirty-tree policy, event stability, and command-injection resistance. |

### Exit Gate

Coding lanes become merge-ready only from a valid current branch-tip result. Firmware lanes retain their existing result behavior.

## 10. Phase 5: Add Generic Exclusive Named Locks

### Purpose

Serialize non-Git resources without teaching the harness about every resource type.

### Implementation Scope

1. Add `orchestrator_harness/resource_locks.py`.
2. Accept optional `exclusive_resources` on coding invocations.
3. Hash exact resource names into safe claim filenames while storing the original names in claims.
4. Acquire multiple resources in canonical order through atomic exclusive creation.
5. Release partial acquisitions before retrying after contention.
6. Publish `WAITING_RESOURCE` without launching Codex.
7. Release only claims matching lane, invocation, PID, and process creation identity.
8. Treat a claim as stale only when exact process evidence proves the owner absent.
9. Never steal or expire a claim whose owner state is unknown.
10. Leave firmware hardware-resource and relay behavior unchanged.

### Required Tests

- Acquire and release one resource.
- Two contenders never overlap.
- Different resources run concurrently.
- Multiple resources use canonical ordering.
- Partial acquisition cleanup.
- Waiting controller does not launch Codex.
- Normal release wakes a waiter.
- Crash leaves a reconcilable claim.
- Confirmed stale owner versus unknown owner.
- Wrong owner cannot release a claim.
- Malformed claim fails closed.
- Unsafe resource characters remain filesystem-safe.

### Parallel Validation Wave 1

| Validator | Task |
|---|---|
| A | Run acquisition, release, and matching-owner tests. |
| B | Run stale, unknown, malformed, and crash tests. |
| C | Review atomicity, cleanup paths, lock ordering, and Windows filesystem behavior. |

### Parallel Validation Wave 2

Queue this separately if the first wave already uses all three validator slots:

| Validator | Task |
|---|---|
| A | Run at least 100 same-resource contention cycles. |
| B | Run multi-resource and independent-resource stress cases. |
| C | Run firmware resource and relay regressions. |

### Exit Gate

No stress run shows overlapping ownership, normal contention requires no manager action, and unknown ownership remains locked.

## 11. Phase 6: Integrate Reconciliation, Events, and Notifications

### Purpose

Expose Git, result, and lock facts through the existing durable manager protocol without rewriting it.

### Implementation Scope

1. Extend discovery only for new claim and coding-result evidence.
2. Add invocation schema, worker invocation ID, Git identity, requested resources, claims, and waiting resource to coding lane snapshots.
3. Preserve firmware permission, relay, MCP, board, and hardware observation.
4. Add internal duplicate worktree and branch conflicts.
5. Add invalid-result, stale-claim, malformed-claim, and excessive-resource-wait conditions.
6. Keep ordinary short lock waits non-actionable.
7. Preserve stable event IDs, priority, pending delivery, preemption, restoration, and exact acknowledgement.
8. Keep application test failures separate from harness failures.

### Required Tests

- Coding snapshot fields.
- Stable repeated observations.
- Duplicate Git identity conflicts.
- Short and excessive resource waits.
- Invalid-result correction.
- Stale, unknown, and malformed claims.
- Event preemption and exact acknowledgement.
- Existing firmware MCP, relay, resource-conflict, active-management, and notification tests.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Run coding discovery, reconciliation, and event tests. |
| B | Run the complete existing firmware reconciliation and notification suite. |
| C | Review event stability, priority, acknowledgement, and false-positive risks. |

### Exit Gate

The manager can consume every new condition through the existing event and acknowledgement protocol, and all firmware regressions pass.

## 12. Phase 7: Add Generic Configuration and Documentation

### Purpose

Make coding work the obvious entry point without removing the supported firmware documentation.

### Implementation Scope

1. Add a generic coding configuration example.
2. Add a versioned coding invocation example.
3. Add a coding `RESULT.json` example.
4. Add a named-lock example.
5. Document branch creation, worktree creation, lane splitting, and merge lanes.
6. Document frozen, candidate, acceptance, rollback, and promotion roles.
7. Make the generic coding quick start the primary README entry.
8. Retain and clearly label the existing firmware workflow documentation.
9. Replace visible MCP-Trial-specific CLI descriptions where they incorrectly describe the whole product.
10. Remove the firmware-specific forbidden output root if it can reject an otherwise valid general project path.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Follow the generic quick start in a clean temporary repository. |
| B | Follow the firmware documentation far enough to validate configuration and a fake policy-bound launch. |
| C | Review every example, command, path, and default for contradictions or stale names. |

### Exit Gate

A new user can run a fake coding lane using only generic documentation, and the documented firmware path still matches its tested contract.

## 13. Phase 8: Add the General Coding Integration Test

### Purpose

Prove the complete coding path in a disposable Git repository.

### Bounded Parallel Test Authoring

After the manager defines the shared fixture contract, up to three authors may work in disjoint test files. One author owns any shared fixture. Together they add coverage that:

1. Creates an initial Python repository commit.
2. Creates two branches and separate worktrees.
3. Starts two fake coding controllers.
4. Proves independent Git identity.
5. Exercises one shared generic lock and proves non-overlap.
6. Publishes a stale result and proves rejection.
7. Publishes valid committed results and proves merge readiness.
8. Creates an integration branch and merges both branches.
9. Runs a small Python test suite.
10. Verifies durable events and exact acknowledgement.
11. Cleans every process, worktree, claim, and temporary file.

The test may run its fake controllers concurrently. This is test execution against disposable resources, not parallel development of the harness.

### Parallel Validation Wave

| Validator | Task |
|---|---|
| A | Repeat the successful two-worktree integration path. |
| B | Run wrong-branch, stale-result, lock-contention, and cleanup failure cases. |
| C | Run the existing synthetic firmware controller and reconciliation suites. |

### Exit Gate

The general integration test passes repeatedly on Windows without flakes, and the firmware suite remains green.

## 14. Phase 9: Complete Automated Release Candidate Gate

### Parallel Validation Wave

Use one fixed candidate commit and three isolated worktrees:

| Validator | Task |
|---|---|
| A | Ruff, formatting, BasedPyright, and compilation. |
| B | All orchestrator tests, including synthetic firmware coverage. |
| C | Watcher tests and `.codex` development integration tests. |

If any task fails, use the serialized repair cycle. Do not patch from validation worktrees.

### Serialized Final Gate

Run once after the parallel wave:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Also run `--full` once before acceptance because the release changes watcher configuration and the overall supported workflow.

### Exit Gate

- Static checks pass.
- Coding unit, smoke, integration, and stress tests pass.
- All required synthetic firmware tests pass.
- No new BasedPyright baseline entries exist.
- Repeated lock and worktree tests are stable.
- The candidate commit and all evidence are recorded.

## 15. Phase 10: Full Candidate Acceptance

### Authority Transition

1. Finish or checkpoint frozen-harness development.
2. Record the candidate commit.
3. Stop the frozen manager and watcher.
4. Prove their exact processes have stopped.
5. Start the outside acceptance supervisor.
6. Start the candidate as the only active harness.
7. Use fresh runtime, event, acknowledgement, output, and lock roots.

### Agent Concurrency During Acceptance

Keep the four-agent maximum:

| Slot | Role |
|---|---|
| 1 | Candidate manager. Planning is serialized here. |
| 2 | Read-only watcher subagent. |
| 3 | One production-code worker, test author, documentation author, or test executor. |
| 4 | One disjoint test/documentation author or isolated test executor. |

Only one target-project production-code worker runs at a time. After the manager fixes interfaces and file ownership, a disjoint test or documentation author may run beside it. When no production writer is active, two disjoint test authors or isolated test executors may run beside the watcher. More work waits for later waves.

Parallel coding capability is exercised by the disposable fake-controller integration and lock stress tests. The practical project deliberately keeps real code writing serialized to reduce ambiguity while accepting the new harness.

### Practical Project

Have the candidate build the local `taskboard` Python application defined in `codex_answer_3.md`.

Use a serialized production implementation sequence:

1. Domain model and public interfaces.
2. SQLite storage.
3. Service layer.
4. CLI.
5. JSON import and export.
6. Integration tests and documentation.
7. Merge and final repair.

Each production step uses its own branch and worktree, begins from a recorded commit, publishes a valid result, and is merged before the next production step begins.

Once the manager freezes the relevant public interface, assign disjoint test and documentation files in parallel where useful. These authors never change production modules or shared fixtures. The manager integrates their commits serially.

After stable integration commits, run up to two independent test agents alongside the watcher subagent. Suitable divisions are domain/storage tests and CLI/import-export tests. They may author missing tests only when the manager has assigned disjoint files; otherwise they remain read-only executors. Queue any additional test group.

### Watcher and Abort Rules

The watcher subagent reads evidence only. It never edits, directs workers, acknowledges events, stops processes, or repairs failures.

Only the supervisor may abort, and only for harness-level failures such as:

- Editing outside the declared worktree.
- Duplicate active worktree or branch use.
- Overlapping ownership of one generic lock.
- Invalid coding result accepted as merge-ready.
- Lost or misidentified processes.
- Corrupted events, acknowledgements, or claims.
- False harness success.
- Unrecoverable harness deadlock.
- Access to frozen runtime state.
- Unsafe shutdown.

Ordinary application bugs, failed tests, merge conflicts, and retries are coding work, not immediate harness aborts.

### Acceptance Exit Gate

- The complete `taskboard` project passes its tests.
- Coding invocations require no firmware records.
- Git identity and result validation remain correct.
- Generic lock behavior is demonstrated.
- Checkpoint and resume succeed.
- Parallel test and documentation authors remain within their assigned files, and parallel test executors remain isolated.
- Events and acknowledgements remain exact and durable.
- Candidate shutdown leaves no live descendants.
- The watcher reports no unresolved critical harness defect.

## 16. Phase 11: Firmware Release Acceptance

Synthetic firmware tests remain required throughout development. Physical firmware testing is separate.

Before publishing a release that claims firmware support:

1. Reserve the required board, probe, server, and MCP resources exclusively.
2. Run one known policy-bound firmware workflow using the promoted candidate.
3. Verify request, relay, MCP lifetime, board ownership, checkpoint/result, event, acknowledgement, and shutdown evidence.
4. Run this test serially with no unrelated hardware or acceptance activity.
5. Record the hardware identifiers, candidate commit, result, and cleanup evidence.

Do not run physical firmware acceptance for every ordinary coding change. Run it for releases and after hardware-specific changes.

## 17. Failure and Repair Flow

### Focused or Regression Failure

1. Finish the current validation wave.
2. Manager consolidates findings.
3. Close validation agents and worktrees.
4. One repair agent changes production or shared files; disjoint test/documentation repairs may use a later bounded authoring wave.
5. Add or update the reproducing test.
6. Rerun focused validation, then the queued wave.

### Full Candidate Acceptance Failure

1. Supervisor stops new candidate launches.
2. Request cooperative shutdown.
3. Stop only exact remaining candidate descendants if needed.
4. Preserve logs, events, checkpoints, branches, results, and claims.
5. Confirm the candidate topology is completely stopped.
6. Restart the frozen harness in a new repair epoch.
7. Use one serialized repair writer.
8. Repeat automated gates before a fresh acceptance epoch.

Never repair the candidate while it is still managing the failed acceptance topology.

## 18. Promotion

Promote only when:

- Every phase commit is integrated into `candidate/general-coding`.
- The complete automated gate passes.
- Required synthetic firmware tests pass.
- Full coding acceptance passes.
- Physical firmware acceptance passes for a public firmware-supporting release.
- Candidate processes shut down cleanly.
- Evidence identifies the exact promoted commit.

After promotion:

1. Start a fresh real manager epoch from the promoted commit.
2. Use new runtime and output state.
3. Keep the frozen baseline inactive as rollback.
4. Do not reuse acceptance runtime or target-project state.

## 19. Expected Commit Sequence

Use one verified commit per bounded change where practical:

1. `baseline: record supported firmware harness`
2. `watcher: disable AI evaluation by default`
3. `controller: add versioned coding invocation`
4. `git: verify coding lane worktree identity`
5. `results: validate coding merge readiness`
6. `locks: add generic exclusive resource claims`
7. `events: integrate coding lane evidence`
8. `docs: add general coding workflow`
9. `tests: add general coding worktree integration`
10. `release: record acceptance fixes`

Do not combine unrelated phases merely to reduce commit count. Do not start several implementation branches at once.

## 20. Definition of Done

The roadmap is complete when:

- General coding and firmware invocations are both supported and tested.
- All harness production-source and shared-file changes were produced serially.
- Parallel test and documentation authors had exact disjoint file ownership.
- Parallel validation never exceeded three subagents plus the manager.
- Every parallel test used isolated writable resources.
- Coding lanes verify their Git worktree, branch, base commit, and invocation identity.
- Coding results identify valid current branch-tip commits.
- Generic named locks serialize non-Git resources safely.
- AI evaluation is disabled unless explicitly enabled.
- Generic documentation works from a clean repository.
- Required synthetic firmware tests remain green.
- Full practical coding acceptance succeeds.
- Release-only physical firmware evidence exists when publishing firmware support.
- No critical harness defect remains unresolved.
