# Portable Harness Development Handoff

## Purpose

This repository is being developed into a Codex-native multi-agent orchestration protocol for ordinary software work in Python or any other language. It is not intended to become a generic file watcher, and the development-only `.codex/` tooling must not be confused with the product being built.

The product code being changed is the `harness-in-progress/` submodule on `progress/v1.1`. The known-good harness used to coordinate that development is the `frozen-harness-to-use/` submodule on `frozen-v1`. Both began from the same portable firmware/HIL orchestration baseline, so its reliable coordination machinery is worth keeping, but many schemas, paths, states, policies, docs, and tests still encode the original firmware experiment.

## Current Status

The product is already a working multi-agent coding harness: a manager plans work, Codex workers execute in parallel lanes, the lane controller launches and resumes them, and the harness provides durable observation, events, checkpoints, and recovery. Its observation/reconciliation component is intentionally read-only; that does not make the complete system only an observer. The remaining problem is specialization: `orchestrator_harness/README.md`, `SPEC.md`, discovery, reconciliation, event classification, sample configuration, and tests retain extensive MCP-Trial-3, M5, hardware, lease, relay, and firmware assumptions.

Do not develop directly in `frozen-harness-to-use`. Run coordination from the frozen submodule, make product changes in `harness-in-progress`, and update the outer submodule pointer only after a candidate commit is intentionally selected.

The agreed direction preserves the existing firmware path as a supported product feature while adding a separate versioned coding contract. Preserve the working manager, lanes, process identity, controller lifecycle, events, checkpoints, results, acknowledgement, recovery, policy-bound firmware invocation, and firmware observation behavior. Keep the synthetic firmware tests in the required regression gate. `GENERALIZATION_SPEC.md` defines the product contract. `IMPLEMENTATION_ROADMAP.md` is the authoritative execution plan. The manager alone performs planning and assigns exact file ownership. Production and shared-file changes are serialized; disjoint test and documentation files plus isolated test execution may use at most three subagents alongside the manager. The `codex_answer_*.md` files provide supporting rationale and simpler explanations.

## Product Architecture Today

`harness-in-progress/orchestrator_harness/` currently provides the observation, coordination-state, and lane-control parts of the working multi-agent system. It:

- Discovers run directories and each run's `.agent-workspace` records.
- Reconciles worker/controller/Codex/helper/MCP process evidence.
- Produces stable, durable, at-least-once events and requires exact acknowledgement by `event_id`.
- Supports bounded blocking waits and a foreground managed-watch loop.
- Tracks a manager epoch, session/invocation identities, heartbeat, pending notification, preemption, and recovery state.
- Uses atomic/stable I/O and exact PID plus process-creation identity rather than unsafe process-name matching.
- Observes permission requests, manager relays, checkpoints, results, provider waits, resource-release possibilities, and hardware ownership conflicts.
- Leaves task planning, lane assignment, integration decisions, approvals, and hardware actions to the manager, while its lane controller performs manager-requested Codex launches and resumes.

`harness-in-progress/harness_watcher_implementation/` is a second, passive diagnostic watcher:

- Tails configured JSONL sources and records deterministic diagnostics.
- Can optionally invoke an AI evaluator, but that evaluator is not required for orchestration.
- Must remain observational: it should not manage workers, repair code, make decisions, or wake a closed Codex conversation.

The root development environment under `.codex/` is separate from both packages. It helps Codex write and verify this repository.

## What To Preserve

The following mechanisms are generally useful and should be preserved while names and schemas are simplified:

- A main manager owns integration, cross-worker decisions, and the final result.
- Workers receive bounded tasks and can execute autonomously in parallel.
- Stable manager, worker, session, invocation, and epoch identities prevent old records from being mistaken for current work.
- Controller and Codex child processes are tracked by PID plus creation time, including parentage and explicit unknown/stale states.
- Codex lifecycle evidence remains first class: thread start, turn completion/failure/cancellation, resume identity, JSONL output, stderr, exit code, and final message.
- Durable events use stable IDs, exact acknowledgement, deduplication, at-least-once delivery, pending state, and deterministic priority/preemption.
- Blocking wait is preferable to polling through extra relay agents. A persistent manager repeatedly waits, handles one event, acknowledges it, reconciles, and waits again.
- Atomic writes, stable reads, size limits, path confinement, and deterministic state recovery remain core safety properties.
- Checkpoints allow interrupted workers or manager sessions to resume without reconstructing all state from chat history.
- Reconciliation distinguishes confirmed running, confirmed exited, and insufficient evidence. Unknown must never be treated as safely dead.
- Deterministic tests, synthetic process fixtures, WSL isolation tests, and passive attention evidence remain valuable after firmware details are removed.
- The diagnostic watcher stays optional and passive rather than becoming another autonomous manager.

## What Is Firmware-Specific

These are the main quirks that must not define the generalized protocol:

- Default run discovery under `fresh-experiments/*`.
- A fixed `.agent-workspace` layout with `permission-requests/`, `manager-relays/`, `PARALLEL_CHECKPOINT.md`, and `RESULT.json`.
- Special handling of boards, probes, serial ports, radios, firmware servers, hardware roots, HIL lanes, and MCP process lifetimes.
- Permission relay validation tied to hardware leases, request hashes, producer lifetimes, and firmware-era schemas.
- Resource-release logic that assumes controller, Codex, helper, and MCP lifetimes all affect physical-device safety.
- M5 timing targets, attention-chain evidence, sprint verdicts, fixed review cadence, and firmware-specific recovery rules.
- Event names and priorities such as MCP active/exit/unknown, relay ready, provider wait, and hardware resource conflict.
- Firmware-specific evaluator exclusions and prompt language.
- CLI descriptions, package docstrings, examples, canaries, tests, and docs named for MCP-Trial-3 or parallel firmware lanes.
- Launcher validation coupled to exact firmware-era prompt headings, policy hashes, expected outputs, model flags, and sandbox settings.

Do not build a broad firmware adapter or profile framework. Dispatch the new `orchestrator-coding-invocation/v1` contract separately and leave the existing firmware validator, discovery, reconciliation, events, tests, and documentation supported.

## Agreed Minimal Generalization

Use Git branches and worktrees as the lane structure:

- One planned task or task group per lane.
- One branch and separate worktree per concurrent lane.
- Child lanes branch from a stable parent commit.
- A manager-launched merge lane combines completed branches and runs integration checks.
- Every coding lane records and validates its worktree, branch, base commit, worker invocation ID, and merge inputs.
- `RESULT.json` must match the current lane/invocation and a real branch-tip commit before the lane is merge-ready.
- Git and worktrees provide code isolation; no general file-ownership protocol is planned.
- The manager declares opaque external resource names; lane controllers automatically acquire, wait for, and release one generic exclusive named lock type.
- Normal lock contention does not wake the manager. Only stale, malformed, unknown, or excessively delayed claims require attention.
- Generic exclusive named locks replace specialized hardware lease behavior.

Only seven initial product changes are planned:

1. Add the versioned general coding contract beside the existing policy-bound firmware contract.
2. Add durable lane/worktree/branch/base-commit identity and validate it before Codex launch.
3. Validate the minimal merge-ready `RESULT.json` against the current lane invocation and branch tip.
4. Add one generic exclusive named lock using atomic claims and exact process identity.
5. Add a generic worktree-lane configuration and operating example.
6. Add one end-to-end test with two coding worktrees and a merge lane.
7. Set `evaluator_enabled` to `false` by default, including loader fallback, example, tests, and docs.

Keep `.agent-workspace`, `PARALLEL_CHECKPOINT.md`, `RESULT.json`, current worker lifecycle, durable events, acknowledgements, discovery structure, reconciliation structure, manager signals, and the supported hardware/MCP/relay firmware behavior. Keep new coding features separate from the specialized firmware resource model. Do not add a scheduler, task database, dependency schema, file ownership, broad adapter framework, or harness-enforced project checks unless the next real project proves one is necessary.

## Development-Only Codex Tooling

The following root tooling exists only to help develop this codebase. It must not be imported into or shipped as the harness runtime protocol.

- `.codex/config.toml` enables project hooks and registers local skills.
- `.codex/hooks.json` installs SessionStart, PreToolUse, PreCompact, and Stop hooks.
- `.codex/scripts/hook_runner.py` restores this handoff, blocks selected destructive shell commands, reminds before compaction, and invokes verification before stopping when files changed.
- `.codex/scripts/verify.py` runs Ruff, formatting checks, BasedPyright, compilation, both product unit suites, and Codex integration tests.
- `.codex/scripts/dev_state.py` records the verified repository snapshot used by the Stop hook.
- `.codex/scripts/worktree_task.py` provides optional isolated Git worktrees for parallel development.
- `.codex/skills/verify` describes repository verification.
- `.codex/skills/checkpoint` creates or refreshes this handoff.
- `.codex/skills/worktree` covers isolated worktree tasks.
- `.codex/skills/test-first` and `.codex/skills/api-design` are explicit opt-in skills, not automatic noise.
- `.codex/skills/plan-harness-workflow` is an explicit opt-in planner that writes detailed execution plans bound to the current Portable Harness protocol; invoke it with `$plan-harness-workflow`.
- There is no verifier agent and no external reference workflow checkout. Those were intentionally removed.

Hooks and project skills are loaded when a new Codex session starts in this repository. Because the hook configuration changed while creating this file, Codex may request one-time trust confirmation at the next session start. The SessionStart hook now injects `HANDOFF.md` on both fresh startup and resume.

The worktree helper operates against committed history. The outer repository tracks both harness repositories as submodules; product branches and worktrees belong in `harness-in-progress`, not in the frozen submodule.

## Verification And Next Step

Verified on 2026-08-02 after the frozen/candidate submodule split and development-path rewiring:

- Ruff lint passed.
- Ruff format check passed.
- BasedPyright passed with zero new errors; the existing 122 findings remain in the renamed baseline.
- Python compilation passed.
- Orchestrator suite passed: 208 tests, one skipped.
- Watcher suite passed: 99 tests.
- Codex integration suite passed: 13 tests.
- Overall result: `VERIFY: PASS`.

The localhost CONNECT-proxy relay test previously assumed the HTTP response header and tunneled payload would arrive in separate `recv` calls. TCP may coalesce them, causing the test to discard `hello` and time out. The test now preserves bytes following the header terminator; it passed 30 consecutive focused runs and the complete gate.

Standard verification command:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Use `--full` when changing watcher retention or lifecycle behavior.

The repository split is complete. Use `frozen-harness-to-use` to coordinate work and implement the authoritative roadmap sequentially in `harness-in-progress`; update the outer gitlink only after selecting a committed candidate revision. Do not parallelize implementation until a separate multi-agent execution plan is requested.

Do not claim the generalization is implemented yet. At this checkpoint, only the development environment and design direction are established.
