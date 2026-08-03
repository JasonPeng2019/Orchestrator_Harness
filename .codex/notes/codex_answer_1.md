# Generalizing the Portable Multi-Agent Orchestrator

## Goal

Turn this repository into a reusable system for coordinating Codex agents on any software project, not only the original firmware project.

The multi-agent design is useful. The main work is removing firmware-specific assumptions from the core system.

## Keep

These parts are broadly useful:

- One main agent manages the work and makes decisions.
- Worker agents run separate tasks in parallel.
- Workers can ask the main agent for help or report progress and completion.
- Requests and results are stored so they are not lost.
- Events are acknowledged only after they are handled.
- Worker processes are tracked by PID and start time.
- Checkpoints let interrupted workers resume later.
- Logs and state are written safely and predictably.
- The watcher reports coordination problems but does not manage workers itself.

## Generalize

### Paths and File Names

The repository expects paths and files from the firmware project, including:

- `fresh-experiments/*`
- `.agent-workspace`
- `permission-requests/`
- `manager-relays/`
- `PARALLEL_CHECKPOINT.md`
- `RESULT.json`
- MCP process files

These locations and names should be configurable or defined by a project adapter.

### Hardware Resources

The current system understands boards, probes, serial ports, radios, hardware leases, and MCP servers.

The core should instead support simple named resources that can be shared or exclusive. Firmware projects can add the hardware details through an optional adapter.

### Worker Requests

Workers currently use a permission-request and relay system designed for hardware access.

Workers should remain mostly autonomous. The orchestrator only needs requests for coordination that a worker cannot safely decide alone:

- Ownership of a shared file.
- Ownership of another shared resource.
- A design decision that affects other workers or the overall project.

Questions, approvals, secrets, dependencies, and external-service problems do not need their own orchestration request types. Workers should handle those through their normal instructions and tool policies. Hardware ownership can remain part of the optional firmware adapter because it requires strict leases to prevent races.

### Worker States

Keep the full Codex process lifecycle. The simpler worker states should summarize it for scheduling, not replace it:

- `STARTING`: The controller started, but the Codex child is not yet confirmed.
- `RUNNING`: The Codex PID and start time are verified.
- `WAITING_FOR_INPUT`: The worker requested a shared file, resource, or design decision.
- `WAITING_FOR_DEPENDENCY`: The worker recorded an external wait.
- `CHECKPOINTED`: The worker published a checkpoint.
- `COMPLETED`: Codex completed and the expected result is valid.
- `FAILED`: Codex failed to launch, reported failure, or exited unsuccessfully.
- `CANCELLED`: Codex reported cancellation.
- `STALE`: The recorded Codex process is absent or does not match its start identity.
- `UNKNOWN`: Process evidence is incomplete.

Continue tracking Codex-specific details underneath these states:

- Controller and Codex PIDs and start times.
- Codex thread IDs and resume behavior.
- `thread.started`, `turn.completed`, `turn.failed`, and `turn.cancelled` events.
- JSONL output, stderr, exit code, and final message.
- Model, reasoning, sandbox, approval, and service-tier settings.

Only hardware relays, MCP helpers, provider waits, and hardware-release rules should move out of the core and into the firmware adapter.

### Project Rules

Each project should define:

- How tasks are found.
- Which commands workers may run.
- How work is tested and reviewed.
- What counts as completion.
- Which files or resources cannot be edited at the same time.
- Which actions require approval.

Python projects could define commands for tests, formatting, linting, and type checking. Other languages could provide their own commands.

### Timing and Recovery

The current time limits and recovery steps came from the M5 firmware experiment. They should be configurable.

The existing recovery sequence can remain available, but it should not be required for every project or failure.

### Prompt and Model Settings

The worker launcher requires exact firmware-era prompt headings, policy hashes, Codex flags, and model settings.

Keep prompt verification, but allow each project to configure:

- The model and reasoning level.
- Sandbox and approval settings.
- The project instructions.
- Expected outputs.
- Start and resume behavior.
- Time limits.

### Watcher Rules

The watcher contains rules about firmware failures, hardware waits, MCP ownership, and permission relays.

The general watcher should focus on coordination problems, such as:

- A worker was lost.
- Work was assigned twice.
- A worker is stuck or looping.
- A request did not reach the main agent.
- The main agent did not respond.
- Two workers claim the same exclusive resource.

A failing test is normally a task result, not a failure of the orchestrator.

### Names and Documentation

The package name, examples, tests, and documentation still refer to MCP-Trial-3, firmware lanes, and M5 runs. Rename the core around general software work and keep the firmware setup as an example adapter.

### Safer Default

Set `evaluator_enabled` to `false` by default. The watcher will still collect logs and report process and coordination state, but it will not launch an extra Codex model to judge the orchestrator unless explicitly enabled. This does not disable the Codex worker agents.

## Suggested Structure

### Core

The core manages agents, tasks, requests, events, checkpoints, processes, logs, and shared resources.

### Project Adapter

A project adapter defines task discovery, commands, tests, completion rules, and project-specific resources.

### Execution Settings

Execution settings define the Codex model, concurrency, time limits, sandbox rules, and watcher behavior.

### Firmware Adapter

The existing board, probe, MCP, relay, and M5 behavior can remain as an optional firmware adapter.

## Summary

Keep the multi-agent orchestration system. Move fixed firmware paths, hardware resources, permission relays, M5 rules, and prompt requirements out of the core and into configurable project adapters.
