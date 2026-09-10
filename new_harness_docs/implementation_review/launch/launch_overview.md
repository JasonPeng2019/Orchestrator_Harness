# How lane launch works

This document explains how the harness starts a lane in direct English.

## The three layers

Three different things participate in a launch:

1. **ROOT's public harness command** - `operator_launch`. This is the only
   public command program that ROOT uses to operate the harness.
2. **The lane controller** - a small, long-running Python process started by
   the harness for one lane. It owns the lane's provider process, leases,
   records, and cleanup.
3. **The provider CLI** - the actual AI command-line program, such as
   `codex`, `claude`, or `qwen`.

The public command does not launch the AI CLI itself. It starts the controller;
the controller starts and supervises the provider CLI.

```text
ROOT
  -> operator_launch lane launch
    -> lane controller
      -> Codex, Claude Code, or Qwen Code
```

## Before launch

ROOT first runs `harness setup`. Setup validates the harness configuration,
installs the supported ROOT integrations, stages the worker payloads, registers
the fixed provider launch bindings, and starts the monitor. It does not start
an AI worker.

ROOT then prepares a lane:

```powershell
python -m orchestrator_harness.operator_launch lane bootstrap `
  --lane-id <lane-id> --provider <provider-id> --model <model> `
  --task-card <task-card.json>
```

Bootstrap creates an isolated Git worktree for the lane. In managed mode it
copies in the common worker material and the selected provider's worker
payload. That payload includes the provider's configuration, hooks, and worker
skills. Bootstrap also writes the worker prompt, an empty result template, the
lane record, and an invocation record. It still does not start the AI or take
an exclusive resource lease.

## Starting a supported CLI

ROOT starts the prepared lane with:

```powershell
python -m orchestrator_harness.operator_launch lane launch --lane-id <lane-id>
```

The harness checks that:

- setup left the runtime open;
- the named lane exists and is prepared;
- the launch record belongs to the lane's current run; and
- a registered provider binding exists for the selected provider.

It then starts the lane controller in the background and records the exact
controller process identity. The public command waits up to 30 seconds for the
controller to prove that the provider process is running, or to report a safe
early failure. A successful launch means the provider process has started; it
does not mean the worker has completed its task.

The controller then:

1. loads the selected provider's fixed launcher binding;
2. acquires the lane's declared exclusive leases, if any;
3. starts the provider from the lane's worktree;
4. supplies the worker prompt through standard input;
5. writes provider standard output to a transcript file and standard error to
   a separate file;
6. reads the provider's streamed JSON output for its session ID and completion
   facts;
7. records the provider process boundary so it can later clean up that exact
   process and its children; and
8. after the provider exits, proves cleanup, releases leases, and validates the
   worker's `RESULT.json`.

If the result is valid, the lane becomes `review_pending`. The controller then
waits for ROOT to complete the separate review/acceptance step. It does not
merge work or decide whether the result is acceptable.

## The three shipped providers

The harness currently ships fixed adapters for these provider IDs:

| Provider ID | CLI it starts | How it runs |
| --- | --- | --- |
| `codex` | `codex exec` | Uses JSON output, runs in the lane worktree, and receives the prompt on standard input. |
| `claude-code` | `claude --print --output-format stream-json --verbose` | Runs from the lane worktree and receives the prompt on standard input. |
| `qwen-code` | `qwen --approval-mode=yolo --output-format stream-json` | Runs from the lane worktree and receives the prompt on standard input. |

An adapter is more than a command name. It contains:

- the exact headless command-line arguments for that CLI;
- the rules for recognizing its session ID and completion information in
  streamed output; and
- its ROOT and worker configuration, hooks, and skills.

This is why the harness does not try to run an arbitrary unknown CLI with a
generic command.

## What happens when a supported CLI cannot start

"Supported" means the harness knows how to operate that CLI. It does not mean
the executable is installed, the user is authenticated, the selected model is
available, or the provider has remaining capacity.

If a supported CLI is missing or cannot start, the controller records the
failure, proves that no untracked provider process remains, releases any leases
that it safely acquired, and the public launch command returns
`LAUNCH_PROVIDER_START_FAILED`. It does not silently switch to another provider
or model.

## What happens for an unsupported CLI

The harness has no generic fallback launcher for an unsupported provider ID.

In managed mode, bootstrap fails because there is no worker payload for that
provider. In plain mode, bootstrap can prepare the bare lane material, but
`lane launch` fails before it starts an AI process because the provider has no
registered launcher binding. The failure code is `LAUNCH_BINDING_FAILED`.

This is intentional. Starting an unknown executable without a known command
format, output parser, hook contract, session format, and cleanup model would
make the harness unable to supervise it safely.

To add a new supported CLI, the harness itself must receive a new shipped
adapter with a provider ID, command builder, streamed-output parser, ROOT
payload, worker payload, and setup validation. It is a product change, not a
per-lane fallback setting.
