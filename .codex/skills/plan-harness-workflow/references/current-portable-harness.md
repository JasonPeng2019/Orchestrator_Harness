# Current Portable Harness Binding

Use this reference when filling the execution template. Re-read the live harness documentation before every plan because the product is being generalized.

## Authority

- One persistent orchestrator is the only planner, launcher, decision-maker, integrator, resource owner, and acknowledgement authority.
- Workers perform assigned work. They do not manage other workers.
- The native harness observes run records and delivers durable events. It does not schedule or launch workers.
- The deterministic watcher records diagnostics only. Keep `evaluator_enabled: false`.
- Do not add a wrapper, alternate scheduler, relay, polling loop, repair controller, or AI watcher subagent.

## Concurrency

There are at most four active agents: one orchestrator and three workers.

- Production coding is singular and serial.
- Planning and triage are singular.
- Static review may fan out over up to three disjoint slices.
- Test and documentation authoring may fan out over up to three manager-assigned disjoint files or conceptual slices.
- Test execution may fan out over up to three isolated slices.
- More than three slices run in ordered waves.
- Every fan-out rejoins before one orchestrator triage.

## Preflight

Every emitted plan must include:

1. Establish a Git baseline before worktrees. If `git rev-parse --verify HEAD` fails, create the initial reviewed commit first.
2. Use a frozen harness copy to coordinate candidate development.
3. Give every author or runner a separate branch/worktree when it writes or needs isolated state.
4. Give every harness epoch fresh config, output, watcher runtime, cursor, manager session ID, and manager invocation ID.
5. Keep runtime under ignored runtime directories, never source packages.
6. Run the coordinating harness from `frozen-harness-to-use` so its Python packages import correctly.
7. Treat `harness-in-progress` as candidate code only; do not use it to coordinate its own full-system acceptance run.

Useful development helper when available:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py create <task> --owner <agent>
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py list
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py close <task>
```

Create and close worktrees serially. Never close a dirty worktree.

## Native Runtime Sequence

The downstream runner, not this planner skill, performs this sequence:

```powershell
python -m orchestrator_harness --config local-config/harness.json scan --no-write
python -m harness_watcher_implementation --config local-config/watcher.json poll
python -m harness_watcher_implementation --config local-config/watcher.json start --owner-pid <durable-owner-pid>
python -m orchestrator_harness --config local-config/harness.json watch --until-actionable --timeout 60 --manager-session-id <session-id> --manager-invocation-id <invocation-id>
python -m orchestrator_harness --config local-config/harness.json ack --event-id <native-event-id>
python -m harness_watcher_implementation --config local-config/watcher.json stop
python -m orchestrator_harness --config local-config/harness.json watch stop
```

The plan must preserve these rules:

- Exit `0` from the wait means handle one returned event.
- Exit `3` means quiet timeout; return to the native wait when appropriate.
- Exit `1` means preserve and diagnose the failure; do not create a workaround layer.
- Preserve `wake_id`.
- `data.signal_id` is the worker/source identity.
- The top-level `event_id` is the acknowledgement identity.
- Publish and verify a response before acknowledgement.
- Use exact PID plus creation identity for cleanup. Never stop by broad process name.

## Lane Binding

Each planned role execution receives:

- A unique lane ID and run root covered by `run_globs`.
- A separate `.agent-workspace`.
- A concrete task/spec file and assigned conceptual slice.
- A branch/worktree when it writes tracked files.
- Explicit resource ownership assigned by the manager.
- A completion or checkpoint contract.

Use current handoffs:

- `PARALLEL_CHECKPOINT.md` for interrupted or waiting work.
- `RESULT.json` for completed lane output.
- `.agent-workspace/manager-signals/*.json` for valid `HELP`, `FEEDBACK`, `INSTRUCTION`, `PASS`, or `CHECKPOINT` signals during live work.
- Controller status and JSONL files for process/thread evidence.

The current harness treats the existence of `RESULT.json` as result evidence. The orchestrator must validate the plan-defined fields, assigned slice, branch, commit, test evidence, and producer identity before using or merging it.

## Current Limitations the Plan Must Respect

- The native harness does not launch agents.
- The current lane controller is policy-bound and firmware-oriented. Use it only with its valid existing invocation, or name another external worker-launch mechanism. Do not pretend the generalized coding contract already exists.
- The harness does not create branches or worktrees.
- It does not enforce file ownership.
- It does not provide the planned generic named-lock service.
- It does not validate merge readiness.
- It cannot wake a closed or terminated conversation.
- Code and configuration must remain frozen during a live run.

## Repair Boundary

Do not repair code inside a live failed topology.

1. Stop new launches.
2. Reach a safe worker boundary.
3. Stop watcher and harness cooperatively.
4. Prove exact descendants are gone.
5. Preserve runtime evidence.
6. Start a fresh repair epoch.
7. Repair and test.
8. Start a new acceptance epoch.
