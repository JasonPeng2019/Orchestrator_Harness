# Harness — ROOT setup and operating guide

This is the guide for **ROOT** (the running agent CLI) to take the harness from a
codebase sitting in a repo to integrated and working in that repo. Everything
here is grounded in `setup-details.md`, `harness_single.md`, and
`harness-provider-adapter-materialization.md`. A separate `adapters/README.md`
covers adding a provider the product does not already ship — it is not part of
normal setup.

> Path examples use forward slashes for readability; the implementation uses the
> host's native separator (the harness is cross-platform).

## What the harness is

A provider-agnostic orchestration harness under cooperative local trust. A
running ROOT CLI supervises subagent worker CLIs, each in its own Git worktree
(a **lane**). Codex, Claude Code, and Qwen Code ship with the product; any other
stdio CLI is added through a small static adapter. All mutable state lives under
the locally Git-excluded runtime tree `<root-workspace>/.harness-runtime/`, so
worktree files never enter ROOT's status or commits.

There are two profiles, fixed per run: **managed** (the default — manager queue,
worker inbox, hooks, and a monitor that pushes events to ROOT) and **plain** (a
rare opt-out for a CLI that cannot support native hooks — no queue or hooks; ROOT
polls instead). Resource leases apply in both.

## Before you start

- The harness codebase sits at `<harness-root>` and contains
  `harness-config.json`, `resource-manifest.json`, `super-cache/`, `adapters/`,
  and this README.
- A supported provider CLI is installed and runnable: Codex, Claude Code, or
  Qwen Code. For any other stdio CLI, its author first adds that provider's
  static adapter tree exactly as described in `adapters/README.md` before setup.
- **Setup does not launch a lane, provider, MCP server, or any hardware action.**
  It only integrates the harness into the workspace.

## Setup sequence (one-time)

This is the complete ROOT-facing sequence. It happens before opening an epoch,
creating a lane, starting a provider, or claiming a resource.

**1. Start your supported CLI (ROOT) in the project workspace.** Setup installs
the static project files for all three shipped providers; the running CLI later
discovers only its own folder. (Custom provider → finish its adapter tree first.)

**2. Fill in `<harness-root>/harness-config.json`.** Exactly one required key and
one optional key:

```json
{
  "root_workspace": "<absolute-path-to-project-workspace>",
  "managed_coordination": "enabled"
}
```

`managed_coordination` **defaults to `enabled` (managed) when omitted**; set it to
`disabled` only for a custom CLI that cannot support native hooks. The runtime
root is always derived as `<root-workspace>/.harness-runtime/` — it is not a
second configured path. This is the only place a profile is chosen; ROOT never
passes paths, flags, or a profile again on later commands.

**3. Write `<harness-root>/resource-manifest.json`** — the one closed list of
exclusive resource names lanes may request:

```json
{
  "schema": "harness-resource-manifest/v1",
  "resources": [
    { "id": "fixture-a", "exclusive": true },
    { "id": "device-b", "exclusive": true }
  ]
}
```

A project with no hardware writes the same file with an empty `resources: []`. It
does not remove or disable the generic resource-lock facility. Names are treated
literally; any meaning of a name belongs to a surrounding campaign policy.

**4. Run the one public setup command:**

```text
operator_launch harness setup
```

It installs ROOT material, creates the active shared cache, writes the active
resource manifest and shared lease directory under the runtime root, and starts
the configured monitor. It does not start a lane or provider. Setup is
idempotent — safe to re-run — and never silently replaces an approved cache. Use
`operator_launch harness setup --overwrite` only to deliberately replace the
planned harness/adapter targets (it reports them).

**5. Verify before requesting any lane.** Check the returned setup result and
confirm this generated file exists:

```text
<runtime-root>/resources/RESOURCE_MANIFEST.json
```

That generated file — not the source manifest, not a worker worktree — is the
manifest every later lane bootstrap uses.

*To change the resource list later:* first run the shutdown/retirement route so no
epoch or live lease remains, edit the source manifest, then run setup again.
Setup rejects a changed source manifest while an epoch is active or a lease is
live. ROOT never edits the generated runtime manifest or a lease file by hand.

## What `operator_launch harness setup` does (for context)

You do not run these individually — the one command performs them, in order:

1. Finds and reads `harness-config.json` (accepts no feature or profile argument).
2. Validates `root_workspace`, derives `<root-workspace>/.harness-runtime/`,
   verifies it is not a symbolic link, and validates
   `resource-manifest.json`.
3. Creates the empty runtime parents when missing — `worktrees/`, `monitor/`,
   `epochs/`, `resources/`, and `manager/` (managed profile only).
4. Creates `RUNTIME_STATE.json` in `OPEN` (or flips it back to `OPEN` if
   `CLOSED`); managed setup also creates the idle manager `QUEUE.json`.
5. Stages, byte-verifies, and atomically installs the active `super-cache/` from
   the harness root; if a valid cache already exists it is left alone.
6. Writes the active `RESOURCE_MANIFEST.json` and creates the shared `leases/`
   parent; refuses a changed manifest while an epoch or live lease exists.
7. Materializes the shipped ROOT payloads (`.codex`, `.claude`, `.qwen`) plus any
   custom payload, and installs the provider catalog and launcher bindings.
8. Starts the one mandatory persistent monitor under the monitor-record lock (a
   live one returns `SETUP_MONITOR_ALREADY_RUNNING`; a stale record is replaced).

Note: a copied hook payload is not proof a provider will run it. Before a provider
is used on a hook-dependent (managed) lane, disposable headless proof must show
its config is discovered, PostToolUse fires, and it honors a Stop rejection.

## Directory layout: before and after setup

Two roots — the spec treats them as distinct and does not require them to be the
same physical directory: `<harness-root>/` is the harness product/code, and
`<root-workspace>/` is the project workspace `root_workspace` points at.

**`<harness-root>/` — before setup, and left unchanged by it** (setup treats it as
the *source*; the only write it ever makes here is registering a custom provider's
`launcher_binding.py` if you add one):

```text
<harness-root>/
  harness-config.json          # you fill in: root_workspace (+ optional managed_coordination)
  resource-manifest.json       # you author: the closed list of exclusive resource IDs (or [])
  README.md                    # this guide
  adapters/                    # shipped provider catalog
    README.md                       # guide for adding a non-shipped provider
    codex/  claude-code/  qwen-code/     # each has: root/  super-cache/  harness/launcher_binding.py  ...
  super-cache/                 # SOURCE cache
    workspace/                      # provider-neutral base: .agent-workspace/ skeleton +
                                    #   result-stop-check.py, lane-queue.py, manager-notify.py
    custom/                         # optional shared additions
  orchestrator_harness/        # harness implementation + the operator_launch CLI
    provider_adapters/<provider-id>/launcher_binding.py    # registered bindings (shipped)
```

**`<root-workspace>/` — before setup** (just your project):

```text
<root-workspace>/
  .git/
  ...your project files...
  # no .harness-runtime/, and no harness-installed .codex/.claude/.qwen payloads
```

**`<root-workspace>/` — after setup** (setup adds the three ROOT payloads and the
runtime tree):

```text
<root-workspace>/
  .git/
  ...your project files...

  .codex/                      # ROOT payload — all three installed; your CLI uses only its own
    config.toml   hooks.json   orchestrator-harness-binding.json
    hooks/  orchestrator_harness_post_tool_use.py  orchestrator_harness_stop.py  ...
    policies/bounded-exclusions.gitignore
    skills/  manager-notification-watch/  acknowledge-manager-notification/
             close-manager-notification/  review-lane-completion/
             send-lane-notification/  resume-lane/  force-stop-lane/
             harness-shutdown/       (SKILL.md in each)
  .claude/   # settings.json, hooks/…, orchestrator-harness-binding.json, same 8 skills
  .qwen/     # analogous

  .harness-runtime/            # = <runtime-root>, Git-excluded
    RUNTIME_STATE.json              # OPEN
    monitor/MONITOR.json            # written once the monitor process starts
    manager/QUEUE.json              # idle queue (managed profile only)
    resources/
      RESOURCE_MANIFEST.json        # active copy of your manifest
      leases/                       # empty — a lease appears only while a lane holds a resource
    super-cache/                    # active copy of the cache
      workspace/                        # base copied into every worktree
      adapter-payloads/codex|claude|qwen/   # per-provider hooks/config + 2 worker skills
      custom/
    epochs/                         # EMPTY until an epoch opens
    worktrees/                      # EMPTY until a lane is bootstrapped
```

`CURRENT_EPOCH.json`, `epochs/<epoch-id>/…`, and `worktrees/…` are **not** created
by setup — epoch-open and bootstrap create them later, during the operating loop.

## What a lane worktree looks like

Bootstrapping a lane creates one Git worktree (a checkout of your project on its
own branch) plus a record folder **outside** the worktree. The split is
deliberate: the worker may write inside its worktree, but the review and
acceptance records it must not be able to forge live outside it.

**Inside the worktree** `<runtime-root>/worktrees/<epoch-id>/<lane-id>/` (a managed
lane shown; items marked *managed* are absent from a plain lane):

```text
<lane worktree>/
  ...a full checkout of your project, on its own branch...
  RESULT.json                    # the worker's result file (worker-written)
  ...worker evidence files...
  .agent-workspace/
    controller.events.jsonl      # controller's execution-event log
    controller.status.json       # controller status snapshot
    provider-transcript.jsonl  provider-stderr.txt  last-message.txt   # controller captures
    result-stop-check.py         # managed: helper the Stop hook runs
    hook-dispatch.py  harness-hook-binding.json  overlay-receipt.json  # managed: hook machinery + copy receipt
    QUEUE.json                   # managed: worker inbox from ROOT (send-lane-notification writes it)
    lane-queue.py                # managed: helper to acknowledge / complete / block an assignment
    manager-notify.py            # managed: helper to raise an escalation
    manager-notifications/       # managed: escalation outbox
    processed-notifications/     # managed: escalations the monitor has consumed
  .codex/                        # managed: provider payload copied from the active cache
    hooks.json  orchestrator-harness-binding.json  hooks/…
    skills/manager-notify/SKILL.md  skills/lane-assignment/SKILL.md     # the 2 worker skills
```

**Outside the worktree**, in the lane's record folder
`<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/` (controller/ROOT-owned, so the
worker cannot forge them):

```text
<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/
  lane.json                      # authoritative lane metadata: identity, current run_id, paths, state
  COMPLETION_REVIEW.json         # written only by the completion-review route
  ORCHESTRATOR_ACCEPTANCE.json   # written only by the completion-review route (ROOT's decision)
```

A **plain** lane's worktree has the checkout, `RESULT.json`, and the
controller-written `.agent-workspace/` files (`controller.events.jsonl`,
`controller.status.json`, transcript/stderr/last-message), but none of the
*managed* items above — no worker inbox or helpers, no escalation outbox, no hook
machinery, no provider hook/config payload, and no worker skills. Its `lane.json`
still lives in the same record folder outside the worktree.

## After setup: the operating loop

Once integrated, this is how ROOT actually runs work. (The public launcher creates
the epoch and lane records automatically — ROOT never opens or edits them.)

1. **Bootstrap a lane** — a short program that validates inputs, copies the
   matching worker template, and writes the invocation; it does **not** start the
   provider:

   ```text
   operator_launch lane bootstrap \
     --lane-id lane-001 \
     --provider claude-code \
     --model <chosen-model> \
     [--exclusive-resource fixture-a ...] \
     <task input>
   ```

2. **Launch the lane.** The controller — not ROOT — starts the provider process
   and, for a managed lease-enabled lane, takes the resource lease:

   ```text
   operator_launch lane launch ...
   ```

   Resource contention is fail-fast: if a declared resource is busy the launch
   returns `LAUNCH_LEASE_BUSY` and no lane starts. ROOT orchestrates the wait —
   hold off and re-launch once the current holder finishes.

3. **While idle / returning to management.** In managed mode, use the installed
   watch skill: when the PostToolUse notice says an event is pending, finish the
   current task, read the queue, and acknowledge the IDs you read
   (`operator_launch manager acknowledge --event-id <id>`), closing them when done
   (`operator_launch manager close --event-id <id> --outcome COMPLETE`). In plain
   mode there is no queue and a lane cannot wake ROOT, so run `scan --no-write`
   when you return to management and `watch --until-actionable` while idle.

4. **Review a completed lane** (the review closes its own event):

   ```text
   operator_launch lane completion-review --event-id <id> \
     --review-outcome PASS|FAIL|BLOCKED \
     --approval ACCEPTED|REJECTED
   ```

   Two distinct fields: `--review-outcome` is the factual finding (recorded in
   `COMPLETION_REVIEW.json`), and `--approval` is ROOT's separate accept/reject
   decision (recorded in `ORCHESTRATOR_ACCEPTANCE.json`); `ACCEPTED` requires a
   `PASS` finding. Both are given together — they aren't alternatives, and neither
   is the `manager close --outcome COMPLETE|BLOCKED` from step 4 (that closes a
   queue event; its `BLOCKED` is unrelated to a `BLOCKED` review finding). Plain
   mode uses `--lane-id`. A forced approval uses
   `--force-accept --force-reason "<why the change is harmless>"` and still
   requires a valid current task/result chain.

5. **Resume or repair a lane** (same worktree, same provider session):

   ```text
   operator_launch resume-lane --lane-id <id> --resume-task-card <new-card>
   ```

6. **Assign work to a running managed lane** (managed only):

   ```text
   operator_launch send-lane-notification --lane-id <id> --prompt "<assignment>"
   ```

7. **Hard-stop one stuck lane.** When a single lane is wedged — its processes won't
   exit (a `cleanup_unproven` that won't clear) or its controller is itself stuck —
   force-stop just that lane:

   ```text
   operator_launch lane force-stop --lane-id <id>
   ```

   It terminates that lane's provider/helper/controller processes, force-releases
   any exclusive lease it held, and marks it retired. Use it for one lane; use
   `harness shutdown` (below) for the whole runtime. See "responding to lane
   events" for which status calls for which response.

8. **Shut down.** Retires lanes (evidence/cleanup-proof first) and then stops the
   setup-started monitor:

   ```text
   operator_launch harness shutdown
   ```

## Responding to lane events

When the monitor surfaces an actionable status (as a queue event in managed mode, or
via `scan`/`watch` in plain mode), here is the expected response. Two rules first:
closing an event (`manager close`) records that you *handled the notification* — it
does not clear the underlying condition, which goes away only when the ground truth
changes (e.g. a stuck process finally exits); and `resume-lane` re-runs a lane's
task, so it is the wrong tool for a lane whose work is *done* but whose teardown is
stuck. (The authoritative table is in `harness_single.md`.)

- **`review_pending`** — run `lane completion-review`; `PASS`+`ACCEPTED` finishes it, else `resume-lane`.
- **`result_invalid`** — review (usually `FAIL`/`REJECTED`), then `resume-lane` to redo or `lane force-stop` to abandon.
- **`provider_exited_no_result`** — check transcript/stderr; `resume-lane` to retry or `lane force-stop` to abandon.
- **`controller_exited`** — investigate; `resume-lane` to restart, or `lane force-stop` to clean up.
- **`status_transcript_contradiction`** — establish the true state; `resume-lane` or `lane force-stop`.
- **`cleanup_unproven`** — clear the straggler so the live controller finishes and drops the lease; if it won't clear, `lane force-stop`.
- **`orphaned_lease`** — force-release the lease before reusing that resource.

## What you have once set up

- **Parallel lanes under one active epoch**, each isolated in its own worktree and
  branch; lane branches are retained and never pushed.
- **Managed profile (default):** the monitor is the sole producer of ROOT events,
  stamps a heartbeat in `MONITOR.json` every pass, and is watched by a ROOT PostToolUse hook that
  restarts it if it dies or hangs (but never resurrects one that shutdown stopped).
- **Plain profile:** no queue or hooks; ROOT polls with `scan`/`watch`; leases
  still apply and recovery is manual.
- **Exclusive-resource leases:** fail-fast and all-or-nothing, with ROOT
  orchestrating any wait; an orphaned lease (holder dead/retired) is surfaced to
  ROOT to clear — the harness reports what is wrong and lets ROOT decide.
- **All runtime state under the Git-excluded `.harness-runtime/`;** shutdown and
  retirement run `git worktree prune` to clear dangling worktree bookkeeping.

## A note on command surfaces

`operator_launch harness setup` and the setup sequence above are settled. The
exact flags, outputs, and failure codes of the lane/manager/watch routes are being
finalized in the harness's single public-CLI-contract task; the forms shown here
match what the specs currently specify.
