# Required harness feature: public shutdown with exact process ownership

> **Status: current detailed v2 target contract.** Its statements about the
> present neutral harness describe the missing baseline capability; the required
> public shutdown behavior is governed by the master planning decision index.

## Scope

This recommendation applies to the current project-local v2 harness:

```text
<root-workspace>/<harness-root>
```

`<harness-root>` is a child of the project workspace in this v2 deployment.

It is not a change to the frozen firmware campaign runner. No provider, MCP server,
or hardware action occurred while writing this document.

## Current state

The neutral harness has per-lane controller cleanup and a `lane retire` command.
It does **not** have a public harness-wide shutdown command. It also does not yet
have the persistent monitor proposed in the accompanying scan/watch/queue
recommendation.

Closing Codex, Claude, Qwen, or a terminal window is not reliable
cleanup for a background Python process. A persistent monitor can survive a CLI
session closing. Therefore it needs an intentional, public stop route with evidence.

## Do not use one global mutable process list

Do not make shutdown blindly kill every PID in one shared `processes.json` file.
That file would be easy to leave stale, and the operating system can later reuse a PID for an
unrelated process. A broad process-name kill is worse: it could kill an unrelated
Python, Codex, Claude, Qwen, compiler, or user process.

Instead, keep one exact process record with the owner that created it, all below the
configured shared runtime root:

```text
<runtime-root>/
  RUNTIME_STATE.json
  monitor/MONITOR.json
  epochs/<epoch-id>/lanes/<lane-id>/lane.json
```

`MONITOR.json` belongs to harness setup and identifies the one persistent monitor.
Each `lane.json` belongs to the public launcher/controller path and identifies that
lane's controller, provider, helpers, task, and runtime artifacts.

Every live-process record needs at least:

- owner (`monitor` or exact lane/invocation ID);
- PID;
- process creation time;
- command/program identity sufficient for a diagnostic check;
- start time and current lifecycle state; and
- the public cleanup route responsible for it.

PID plus creation time is the required kill identity. A matching PID without a
matching creation time is an unknown process, not permission to terminate it.

## Correct ownership boundary

The shutdown command should coordinate cleanup; it should not duplicate the lane
controller's job.

```text
harness setup owns the persistent monitor
lane controller owns its provider and helper processes
harness shutdown coordinates both owners
```

A lane controller already knows its direct provider handle, child-process boundary,
leases, and the evidence needed before a lane can release its claims. It is the
right place to stop that lane's provider/helper processes. A global shutdown script
should invoke the lane's normal public cleanup route, rather than independently
killing provider PIDs listed in a registry.

The only ordinary direct process shutdown owned by the harness-wide command is the
setup-started persistent monitor, after all active lanes are closed.

## Required public command behavior

Add a public command such as:

```text
operator_launch harness shutdown
```

It resolves the fixed `<harness-root>/harness-config.json`; ROOT does not pass a
collection of arbitrary process IDs or path roots.

The command must perform this sequence:

1. Under the runtime-state lock, atomically change
   `<runtime-root>/RUNTIME_STATE.json` from `OPEN` to `SHUTTING_DOWN`. New epoch
   and lane launch commands reject while that state is present.
2. Read every active epoch and lane record below the configured runtime root.
3. Request ordinary public cleanup for each exact active lane. The lane controller
   stops its own provider/helpers, records cleanup evidence, and releases its own
   leases only after exact process cleanup is proved.
4. Re-read the lane records and refuse success if a lane is still live, cleanup is
   unproven, or its runtime record is malformed/ambiguous.
5. Under the monitor-record lock, set `stop_requested: true` in the existing
   `<runtime-root>/monitor/MONITOR.json`. The monitor changes that same record to
   `STOPPED`, records its stop time, and exits. No request or acknowledgement file
   is created.
6. Wait for the exact monitor PID-plus-creation identity to disappear. Only then
   atomically change `RUNTIME_STATE.json` to `CLOSED`.

The monitor must be stopped **after** lane cleanup. Otherwise a lane failure during
shutdown may go unrecorded, and no monitor remains to report an incomplete cleanup.
Shutdown does not need a separate recovery daemon: a later setup sees an absent
recorded monitor identity, removes that stale record, and starts one fresh monitor.
A still-live monitor is not silently replaced during ordinary setup.

## Required ROOT shutdown skill

Setup must place this short ROOT-only skill in each shipped provider's normal
ROOT skill folder:

```text
.codex/skills/harness-shutdown/SKILL.md
.claude/skills/harness-shutdown/SKILL.md
.qwen/skills/harness-shutdown/SKILL.md
```

For a custom supported CLI, its adapter supplies the same file under:

```text
adapter/root/<provider-skill-root>/harness-shutdown/SKILL.md
```

The skill says only this: use `operator_launch harness shutdown` when
intentionally ending the harness run; do not close a terminal, kill by process
name, or edit process records; the command closes lanes first and the monitor
second; and a failed shutdown is evidence to preserve, not permission for a
broad-kill retry. It is not copied into worker worktrees.

## Exceptional recovery

If a lane controller is already dead or cannot perform its cleanup, shutdown may use
a narrow fallback against the exact registered process identity. It must first prove
both PID and creation time match the record. It must record that this was forced
recovery and preserve the failed lane's evidence.

The same narrow rule applies if public shutdown must recover a monitor that did not
honor the `stop_requested` state in `MONITOR.json`. It may target only the exact monitor
PID-plus-creation identity from `MONITOR.json`, records forced recovery, and refuses
success if absence cannot then be proved. Ordinary `harness setup` never performs
that kill or replaces a live monitor.

An unknown identity, a mismatched creation time, or a process that cannot be proved
gone is a shutdown failure. It is never a successful shutdown and never permission
for a broad process kill.

## Observable acceptance criteria

With disposable host-only lanes, prove all of the following:

1. Setup starts one monitor and writes a complete `MONITOR.json` record.
2. Shutdown rejects a new lane launch once `RUNTIME_STATE.json` is `SHUTTING_DOWN`.
3. Shutdown invokes normal cleanup for each active lane before asking the monitor
   to stop.
4. A lane's provider/helper processes are cleaned by that lane controller, and its
   lease is not released before cleanup proof exists.
5. Shutdown records and rejects an unproven lane cleanup rather than claiming pass.
6. The monitor observes `stop_requested` in its own record, exits, and its exact PID-plus-creation
   identity is verified absent.
7. A deliberately stale PID record never causes shutdown to terminate an unrelated
   process.
8. A later setup recognizes an absent recorded monitor identity as stale, removes
   it, and starts one fresh monitor without attempting to replay the former
   monitor's in-flight scan work.
