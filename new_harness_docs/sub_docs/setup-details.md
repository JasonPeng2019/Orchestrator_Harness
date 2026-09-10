# Setup details: shipped files, active files, and fresh runtime state

## Scope and status

This is the proposed setup model for the current project-local v2 harness:

```text
<root-workspace>/<harness-root>
```

`<harness-root>` is a child directory of `<root-workspace>` in this v2 deployment.
It is a recommendation, not a claim about the current checkout. The current
checkout uses `<harness-root>/super-cache` directly as its active cache and does
not yet provide this public setup flow.

The revamp is fresh-runtime-only. First v2 setup creates a new v2 runtime root;
it does not open, migrate, or preserve the prior candidate's queue, binding,
coordinator, or in-flight lane state. Prior runtime folders are archival
evidence, not an input to the new harness.

## The two shipped setup guides

The product should ship exactly two guides for this workflow:

```text
<harness-root>/README.md
<harness-root>/adapters/README.md
```

`<harness-root>/README.md` is for ROOT operating the harness. Its first
section is the quick setup sequence below: choose an already-shipped provider
or finish an adapter, fill the fixed configuration and resource list, run
setup, inspect its returned result, then request a lane bootstrap/launch. The public
launcher creates epochs and lane records; ROOT does not edit them. The README
must state that setup does not launch a lane, provider, MCP server, or hardware
action.

`<harness-root>/adapters/README.md` is for someone adding a provider that the
product does not already ship. It tells them the exact small files to put below
the adapter's `root/`, `super-cache/`, and `harness/` folders, how their hooks
call the shared helpers, how `launcher_binding.py` launches that CLI, and how
to prove the copy/launch behavior. It is not a second ROOT runbook. Codex,
Claude Code, and Qwen Code already have shipped adapter trees, so ordinary
ROOT setup materializes all three static ROOT payloads; the already-running
ROOT CLI discovers only its own folder.

The current `setup-details.md` and
`harness-provider-adapter-materialization.md` are the recommendation source
for those two future shipped READMEs.

## Quick ROOT setup

This is the complete ROOT-facing setup sequence. It happens before opening an
epoch, creating a lane, starting a provider, or claiming a resource.

1. ROOT starts its normal supported CLI in the project workspace. Codex, Claude
   Code, and Qwen Code ship with the product, and setup installs the static
   project files for all three. If ROOT uses another normal stdio provider, its
   author first adds that provider's small static adapter tree exactly as
   described in `harness-provider-adapter-materialization.md`. That tree
   supplies the provider's ROOT files, worker files, and `launcher_binding.py`;
   it does not require a separate setup program or a per-epoch ROOT binding.
2. Fill in the fixed `<harness-root>/harness-config.json`: the required
   `root_workspace`, and optionally `managed_coordination`. `managed_coordination`
   **defaults to `enabled`** when omitted — managed is the default profile (see
   resolution R16 in `harness_single.md`); it is set to `disabled` only for the
   rare custom CLI that cannot support native harness hooks. The active super-cache,
   persistent monitor, resource-lock facility, and normal worktree payload are
   mandatory and are not config choices. ROOT's workspace is the project workspace. The
   runtime root is always derived as
   `<root-workspace>/.harness-runtime/`; it is not a second configured path.
   This is the only feature-settings step: the stored setting selects managed or
   plain before setup runs. ROOT does not pass paths, feature flags, or a
   profile again on normal commands.
3. Write the one ROOT-owned source resource list at
   `<harness-root>/resource-manifest.json`. It is the only place ROOT declares
   which exclusive resource names lanes may request. For example:

   ```json
   {
     "schema": "harness-resource-manifest/v1",
     "resources": [
       { "id": "fixture-a", "exclusive": true },
       { "id": "device-b", "exclusive": true }
     ]
   }
   ```

   A project with no hardware writes the same closed manifest with an empty
   `resources` array. It does not turn off or remove the generic resource-lock
   facility.

   The neutral harness treats these as exact names. Any special meaning of a
   name, such as a particular board, belongs to a surrounding campaign policy.
4. Run the one public setup command:

   ```text
   operator_launch harness setup
   ```

   It installs ROOT material, creates the active shared cache, writes the
   active resource manifest and shared lease directory under `runtime_root`,
   and starts the configured monitor. It does not start a lane or provider.
5. Check the returned setup result and confirm that this file exists before
   requesting any lane bootstrap/launch:

   ```text
   <runtime-root>/resources/RESOURCE_MANIFEST.json
   ```

   That generated file—not the source file and not a worker worktree—is the
   manifest every later lane bootstrap uses. The controller later writes only
   temporary lease files below `<runtime-root>/resources/leases/` while a
   lane is actually running.

To change the resource list later, first use the public shutdown/retirement
route so no epoch or live lease remains, edit the fixed source manifest, and
run setup again. Setup must reject a changed source manifest while an epoch is
active or a live lease remains. ROOT never edits the generated runtime manifest
or an individual lease file by hand.

## What ROOT does after setup

The harness-root `README.md` should end its quick section with this short
operating order:

1. For each lane, ask the public bootstrap route to use a chosen shipped
   `--provider`, `--model`, task input, and zero or more resource IDs from the
   generated manifest only in a managed lease-enabled run. The launcher code
   creates the current epoch and lane registry automatically when needed; a
   managed epoch also gets queue/binding records. ROOT never opens or edits those
   records itself. Bootstrap prepares a worktree and invocation; it does not
   start the provider.
2. Use the public launch route with that invocation. The controller, not ROOT,
   starts/cleans its provider process and creates a temporary resource lease only
   for a managed lease-enabled lane.
3. When ROOT is idle, use the installed watch skill. In managed mode, when its
   PostToolUse notice says a manager event is pending, finish the current task,
   read the queue, and use the acknowledgement skill for the event IDs actually
   read. In plain mode, watch returns changed lane status directly and no queue is
   opened. A plain lane cannot wake ROOT: when using a CLI without usable harness
   hooks/notifications, ROOT must remember to run `scan --no-write` when it
   returns to management work and `watch --until-actionable` while it is idle.
4. Use the installed completion-review, resume, and shutdown skills instead of
   editing a result-review file or process record. `send-lane-notification` is
   managed-only. A plain completion review uses `--lane-id` and a rejection gives
   direct resume-required output; neither profile asks ROOT to hand-edit a lease
   or queue file. The public shutdown route retires lanes before it stops the
   setup-started monitor.

This tells ROOT what to do at each boundary without asking it to recreate
bootstrap, queue, hook, lock, or process-management mechanics manually.

## The two roots and the derived runtime tree

```text
<root-workspace>                       ROOT's project workspace
  <harness-root>/                     project-local product code and shipped source material
  .codex/                              static Codex ROOT config, hooks, and skills
  .claude/                             static Claude Code ROOT config, hooks, and skills
  .qwen/                               static Qwen Code ROOT config, hooks, and skills
  .<custom-agent>/                     optional static custom ROOT adapter payload
  .harness-runtime/                   all mutable harness runtime state
    RUNTIME_STATE.json                 lifecycle gate: OPEN, SHUTTING_DOWN, or CLOSED
    CURRENT_EPOCH.json                 active epoch ID; manager queue ID only when managed
    manager/
      QUEUE.json                       managed profile only; replaced for each managed epoch
    super-cache/
    resources/
    monitor/
    epochs/
    worktrees/
```

`<root-workspace>` is the project ROOT works in, and `<harness-root>` is its
project-local harness child. Its hidden `.harness-runtime/` child is the only
runtime root; every mutable **runtime** file belongs below it. Setup derives that
path and rejects a configuration that tries to place runtime state beside or
outside the project workspace. Static ROOT payloads belong at the workspace root
and shipped/registered adapter code belongs under `<harness-root>`; those writes
also remain within the project workspace. When the ROOT
workspace is a Git worktree, setup records `.harness-runtime/` in that
workspace's local Git exclusion so monitor state and nested lane worktrees do
not appear as project changes. The runtime tree is never a lane worktree and is
never copied into a lane as project source.

The provider folders above are static project material, not runtime state and
not a selection of an active ROOT session. Setup writes all three shipped
standard folders together. The CLI that is already running as ROOT loads only
the folder native to that CLI. A custom CLI works the same way after its adapter
author supplies a static `.<custom-agent>/` payload before setup. Managed ROOT
hooks open the fixed `<runtime-root>/manager/QUEUE.json` path. Plain wrappers
return through their explicit no-op branch without opening a queue. The only
managed dynamic cross-check is `CURRENT_EPOCH.json`, which carries the active
epoch and queue IDs but no provider, model, or session identity.

## ROOT is already running; lane provider/model choices are lane inputs

There is no `root_provider`, `root_model`, ROOT session ID, or selected-ROOT
binding in `harness-config.json`. ROOT is the CLI that the operator has already
launched in `<root-workspace>`; setup does not choose it, start it, replace it,
or create a second ROOT session.

Setup materializes every shipped standard ROOT adapter payload in that one
workspace: `.codex/`, `.claude/`, and `.qwen/`. Each payload exposes the same
ROOT skills and a native hook wrapper. A static custom adapter may likewise add
its own `.<custom-agent>/` project payload before setup. Consequently, the
currently running CLI discovers its own static files without the harness having
to identify which provider it is.

When a managed epoch is active, all of those ROOT hook wrappers call the same
generic dispatcher. It opens the fixed `<runtime-root>/manager/QUEUE.json` and
checks that its epoch/queue IDs match `<runtime-root>/CURRENT_EPOCH.json`. This
is dynamic event-routing context, not a provider-specific ROOT binding: it
contains no ROOT provider/model/session identity. With no active epoch or an
explicit plain epoch, the dispatcher returns normally without queue work.

This is a deliberate v2 MVP boundary. The harness atomically replaces one fixed
manager queue with a fresh logical queue for each epoch; it does not bind that
queue to a ROOT provider process or session. Provider/session binding would require
discovering the real ROOT process, persisting provider-specific state, handling
stale identities and partial rebinds, and often starting a replacement ROOT
session when a CLI does not reload its configuration. None of that changes how
the three proven native hooks find the queue, so it would add failure modes with
no current benefit under cooperative local trust.

The static project payload must be present before a ROOT CLI session starts,
unless that CLI is independently proven to reload project hook configuration.
If it does not reload, the operator manually restarts ROOT once after setup; a
future user-facing usage guide will state that operational step. The harness
never starts, restarts, or rebinds ROOT, and an epoch change never requires a
ROOT restart. One active ROOT control session per project runtime is the
supported operating model, because two sessions in the same workspace would
intentionally read the same current-epoch pointer.

For every lane, ROOT supplies a separate provider and model when it requests
that lane's public bootstrap/launch operation:

```text
operator_launch lane bootstrap \
  --lane-id lane-001 \
  --provider qwen-code \
  --model <chosen-Qwen-model> \
  ...
```

Bootstrap is a short program, not an agent. It only validates ROOT's supplied
provider/model, copies the matching shipped worker template, and writes those
same values to the invocation used by the later lane controller launch.

The standard Codex, Claude Code, and Qwen Code templates all remain available
at once. ROOT can therefore use one provider while concurrently launching lanes
with any supported provider and different models. Each lane has its own
worktree and invocation, so one selection cannot change another lane.

## The one persistent template-to-runtime copy

The super-cache is the only harness-root template that becomes a persistent,
editable runtime working copy:

```text
<harness-root>/super-cache/   shipped source; setup and lanes never edit it
                 |
                 | first `operator_launch harness setup`
                 v
<runtime-root>/super-cache/   active working copy; every lane reads this one
```

The shipped source contains the normal product-owned worker material: shared
`.agent-workspace` helpers, Codex/Claude Code/Qwen Code hook payloads, and
worker skills. The active copy starts as a byte-verified copy of that source.

After setup, any approved extra shared files go only below:

```text
<runtime-root>/super-cache/custom/
```

No lane reads the harness-root cache directly. No worker edit flows back into
either cache. A worker receives a fresh overlay copy from the active runtime
cache when bootstrap creates its worktree.

## Everything setup creates or copies

| Source | Destination | Why |
| --- | --- | --- |
| `<harness-root>/super-cache/` | `<runtime-root>/super-cache/` | One persistent active cache copy for every later lane. |
| `<harness-root>/resource-manifest.json` | `<runtime-root>/resources/RESOURCE_MANIFEST.json` | ROOT declares the allowed exclusive resource IDs once; setup writes the active copy every lane must use. |
| All shipped standard ROOT adapter payloads, plus installed custom ROOT adapter payloads | `<root-workspace>/.codex/...`, `.claude/...`, `.qwen/...`, and any `.<custom-agent>/...` | Each possible ROOT CLI discovers its own static skills/hooks in the already-running project workspace. These are not runtime state. |
| All shipped worker templates | `<runtime-root>/super-cache/adapter-payloads/<provider-id>/...` | The active cache retains every supported lane-provider payload. Bootstrap later copies only the lane request's selected provider payload into that lane's worktree. |
| All shipped `harness/launcher_binding.py` files | Fixed registered paths below `<harness-root>/orchestrator_harness/provider_adapters/<provider-id>/` | The controller imports the exact binding selected by each lane invocation. These are harness code, not runtime state. |
| Nothing | `<runtime-root>/RUNTIME_STATE.json` | Setup creates the one lifecycle record in `OPEN` state. Shutdown temporarily changes it to `SHUTTING_DOWN`, then `CLOSED`. A later setup changes `CLOSED` back to `OPEN`. |
| Nothing | `<runtime-root>/monitor/MONITOR.json` | Setup creates this live monitor identity after it starts the monitor. It also carries requested/stopped state. |
| Nothing | `<runtime-root>/resources/leases/` | Setup creates the one shared parent for controller-owned lease files. |
| Nothing | `<runtime-root>/manager/QUEUE.json` | Setup creates an idle valid queue at this fixed path; epoch open atomically replaces it with a fresh queue ID and empty event list. |
| Nothing | `<runtime-root>/CURRENT_EPOCH.json` | Epoch open atomically publishes the active epoch and fresh queue IDs after queue replacement; epoch retirement clears it. |
| Nothing | `<runtime-root>/epochs/...` | Opening an epoch creates its diagnostics and lane registry. The manager queue is runtime-level, not epoch-local. |
| Nothing | `<runtime-root>/worktrees/<epoch-id>/<lane-id>/` | Bootstrap creates one new Git worktree for one new lane. |

Setup must preflight adapter destinations before it copies anything. In normal mode,
a target-file collision is an error; it must not merge or overwrite a hook, skill,
settings file, or launcher binding. `operator_launch harness setup --overwrite`
deliberately replaces only the complete preflighted set of harness/adapter target
files, reports every replacement, and restores them on a late copy failure. It does
not authorize arbitrary ROOT-workspace overwrites or active-cache replacement.

Every shipped standard ROOT payload includes these same eight ROOT-only skills:

```text
manager-notification-watch
acknowledge-manager-notification
close-manager-notification
review-lane-completion
send-lane-notification
resume-lane
force-stop-lane
harness-shutdown
```

`acknowledge-manager-notification` tells ROOT to read the fixed manager queue, then call
`operator_launch manager acknowledge --event-id <top-level-event-id>` for each
event ID it actually read. The skill never tells ROOT to edit `QUEUE.json`.

`close-manager-notification` tells ROOT to finish an acknowledged ordinary
ROOT event through `operator_launch manager close --event-id <event-id> --outcome
COMPLETE|BLOCKED --summary "<what ROOT did or needs>"`. It never edits the queue
or restarts a lane; completion review closes its own event.

`review-lane-completion` is profile-aware. In managed mode it tells ROOT how to
handle an acknowledged `COMPLETION_REVIEW_REQUIRED` queue event. It compares the
event's copied task criteria, result, and evidence, then runs:

```text
operator_launch lane completion-review \
  --event-id <event-id> \
  --review-outcome PASS|FAIL|BLOCKED \
  --approval ACCEPTED|REJECTED \
  --review-summary "<ROOT's reasoning>"
```

In plain mode the same skill identifies the controlled terminal
`review_pending` lane and runs the same command with `--lane-id <lane-id>` in
place of `--event-id`. It never edits acceptance/review files or a lane record
directly. `--review-outcome` (the factual finding `PASS`/`FAIL`/`BLOCKED`) and
`--approval` (ROOT's separate decision `ACCEPTED`/`REJECTED`) are two independent
fields given together on every call, not alternatives; `ACCEPTED` requires a `PASS`
finding. A stale-source
error normally means ROOT resumes the lane; ROOT may use `--force-accept
--force-reason "<reason>"` only after inspecting a harmless current-record
difference. `REJECTED` creates a separate `LANE_RESUME_REQUIRED` event only in
managed mode; plain mode returns direct resume-required output. The review skill
does not restart a provider itself.

`harness-shutdown` tells ROOT to run exactly:

```text
operator_launch harness shutdown
```

when intentionally ending the configured harness run. It explicitly forbids
closing a terminal, broad process-name kills, or direct edits to process or
lease records. The public command retires active lanes through their normal
controller cleanup routes before it stops the setup-started monitor.

## Files that must not be copied from a runtime template

These items are created fresh because their contents are specific to one live
run. Reusing a template would carry stale IDs, process identities, or queue
state into another run.

```text
<runtime-root>/RUNTIME_STATE.json
<runtime-root>/CURRENT_EPOCH.json
<runtime-root>/manager/QUEUE.json
<runtime-root>/monitor/MONITOR.json
<runtime-root>/epochs/<epoch-id>/epoch-state.json
<runtime-root>/epochs/<epoch-id>/active-lanes.json
<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/lane.json
<runtime-root>/resources/RESOURCE_MANIFEST.json
<runtime-root>/resources/leases/...
<runtime-root>/worktrees/<epoch-id>/<lane-id>/...
```

The same rule applies to a managed worker's `.agent-workspace` binding and
incoming lane queue, and to every lane's controller status/event records,
`RESULT.json`, and provider session ID. Bootstrap or the controller writes only
the profile-appropriate files with that lane's real IDs and paths.

## Files that stay in the harness root

These files are product inputs, not execution state, so setup does not copy
them to `runtime_root`:

```text
<harness-root>/harness-config.json
<harness-root>/resource-manifest.json       # ROOT-authored fixed setup input
<harness-root>/orchestrator_harness/...
<harness-root>/super-cache/                 # shipped source only
<harness-root>/adapters/README.md
<harness-root>/adapters/shipped-machinery/
<harness-root>/orchestrator_harness/provider_adapters/<provider-id>/launcher_binding.py
```

`harness-config.json` stays here because every public command must find its
fixed configuration without ROOT supplying a path. The launcher binding stays
here because the generic controller imports it as code. Neither file is a
runtime record.

## What `operator_launch harness setup` does

1. Finds `<harness-root>/harness-config.json` by locating its own harness root
   and reads the one optional compatibility setting from that file. The public setup
   command accepts no separate feature or profile argument.
2. Validates the configured absolute `root_workspace`, derives the contained
   `<root-workspace>/.harness-runtime/` root, verifies that it is not a
   symbolic link (the runtime tree relies on same-volume atomic rename), and
   validates the fixed ROOT-authored `<harness-root>/resource-manifest.json`.
   The runtime root **may** sit inside another root's lane worktree — that is
   allowed and not rejected; the operator accepts that the owning lifecycle's
   `git worktree prune` or a manual worktree deletion could remove the nested
   runtime tree.
3. Validates the stored flags as one legal profile before creating optional
   state, then creates these empty runtime parents when missing. It does **not** pre-create
   `<runtime-root>/super-cache`; that path is the atomic destination in the
   next step. `manager/` is created only for the explicit managed profile;
   a plain profile has no manager queue:

   ```text
   <runtime-root>/worktrees/
    <runtime-root>/monitor/
    <runtime-root>/epochs/
    <runtime-root>/resources/
    <runtime-root>/manager/             # managed profile only
   ```

4. Creates `RUNTIME_STATE.json` in `OPEN` state when absent; when it is
   `CLOSED`, atomically changes it back to `OPEN` as the first idempotent
   setup step. Managed setup then creates and validates the one fixed idle manager
   queue at `<runtime-root>/manager/QUEUE.json` when it does not already exist.
   Its idle header has no active epoch; managed epoch open later stages and
   atomically replaces it with a fresh queue ID and empty event list. Plain setup
   creates no queue and the already-installed static ROOT wrapper is explicitly
   inactive for that profile.
5. If the active runtime cache did not exist, stages and byte-verifies the copy
   from `<harness-root>/super-cache`, then atomically puts it at
   `<runtime-root>/super-cache`.
6. If that cache already exists, checks it and leaves it alone. Setup never
   silently replaces a working cache containing extra approved material.
7. Stages, byte-verifies, and atomically writes the source resource list to
   `<runtime-root>/resources/RESOURCE_MANIFEST.json`, then creates the shared
   `<runtime-root>/resources/leases/` parent. If the active resource manifest
   already matches, setup leaves it in place. If it differs, setup refuses the
   change while an epoch is active or a live lease exists.
8. Materializes all shipped standard ROOT payloads in `root_workspace`
   (`.codex`, `.claude`, and `.qwen`) and any installed static custom ROOT
   payload. It also installs/checks the complete shipped lane-provider catalog
   and its fixed launcher bindings; the active cache retains all of the standard
   worker payloads. Standard worker material already present in the source cache
   is not copied a second time. In normal mode any target-file collision rejects
   the whole copy; `--overwrite` replaces only the planned harness/adapter
   targets and reports them.
9. Starts the one mandatory persistent monitor. Under a short monitor-record lock,
   an exact live `MONITOR.json` identity returns
   `SETUP_MONITOR_ALREADY_RUNNING`; an absent or stale monitor record is
   removed and followed by one fresh monitor record.

Setup does not open an epoch, make a worktree, or launch a provider. Managed setup
creates only the idle fixed manager-queue shell; managed epoch open creates its
fresh logical queue by atomically replacing that file. Plain setup creates neither
queue nor worker hook payload, but still creates the required cache and monitor.
Bootstrap, launch, resume, and adapter commands consume this setup-selected
profile; they do not accept a feature switch or make an independent mode choice.

Checking that a hook payload was copied is not proof that a provider will execute
it. Before a provider is admitted to a hook-dependent lane, disposable headless
proof must show that its project configuration is discovered, PostToolUse fires,
its Stop response can reject completion, and the provider honors that response. A
provider that cannot pass this proof is unsupported for hook-dependent lanes until
a controller-level fallback is designed and proven.

## Clear failure results

The harness-root `README.md` must state that every public command returns a
structured result with these fields:

```text
ok
code
summary
evidence_paths
next_action
```

`code` is a short stable reason, not a generic Python exception. The first
public implementation should use at least these codes:

| Command | Failure codes |
| --- | --- |
| Setup | `SETUP_CONFIG_INVALID`, `SETUP_CACHE_INVALID`, `SETUP_RESOURCE_MANIFEST_INVALID`, `SETUP_ADAPTER_COLLISION`, `SETUP_OVERWRITE_FAILED`, `SETUP_MONITOR_ALREADY_RUNNING` |
| Bootstrap | `BOOTSTRAP_REQUEST_INVALID`, `BOOTSTRAP_WORKTREE_EXISTS`, `BOOTSTRAP_CACHE_COLLISION`, `BOOTSTRAP_ADAPTER_MISSING`, `BOOTSTRAP_RESOURCE_UNDECLARED` |
| Launch | `LAUNCH_INVOCATION_INVALID`, `LAUNCH_BINDING_FAILED`, `LAUNCH_LEASE_BUSY`, `LAUNCH_CONTROLLER_START_FAILED`, `LAUNCH_PROVIDER_START_FAILED` |
| Resume | `ALREADY_ACCEPTED`, `LANE_RUNNING`, `RESUME_WORKTREE_MISSING`, `NO_SAVED_SESSION_ID`, `INVALID_RESUME_TASK_CARD`, `RESUME_LANE_WRITE_FAILED`, or the provider's native resume error |
| Manager close | `MANAGER_CLOSE_NOT_ACKNOWLEDGED`, `MANAGER_CLOSE_ALREADY_CLOSED`, `MANAGER_CLOSE_NOT_ROOT_EVENT`, `MANAGER_CLOSE_INVALID_OUTCOME` |
| Completion review | `COMPLETION_REVIEW_EVENT_INVALID`, `COMPLETION_REVIEW_NOT_ACKNOWLEDGED`, `COMPLETION_REVIEW_STALE_SOURCE`, `COMPLETION_REVIEW_FORCE_REASON_INVALID`, `COMPLETION_REVIEW_OUTPUT_CONFLICT`, `COMPLETION_REVIEW_WRITE_FAILED` |
| Shutdown | `SHUTDOWN_LANE_CLEANUP_UNPROVEN`, `SHUTDOWN_MONITOR_UNPROVEN`, `SHUTDOWN_RUNTIME_AMBIGUOUS` |

For example, `BOOTSTRAP_CACHE_COLLISION` names the exact destination and its
matching cache/adapter source. ROOT may remove that exact stale generated file,
then rerun bootstrap; bootstrap never removes it on its own. `LAUNCH_LEASE_BUSY`
means an ordinary resource contention, so its next action is to wait or launch
work that does not need that resource. Cleanup-proof failures preserve evidence
and leave a lease in place; they never claim successful shutdown.

## Later execution path

```text
setup
  -> active runtime cache and resource manifest exist
  -> ROOT supplies one lane's provider/model to bootstrap
  -> launcher creates fresh epoch records when required
  -> bootstrap creates fresh lane worktree and copies that provider's payload
  -> launch starts the lane controller and provider
```

The source cache is not consulted after setup. The active runtime cache is the
single source used by bootstrap for the configured harness installation.

## Observable checks

1. Before setup, the harness-root source cache exists and no runtime cache is
   required.
2. First setup creates a byte-verified active runtime cache without changing
   the source cache.
3. A second setup preserves approved additions in the active cache.
4. A lane bootstrap reads the active runtime cache, never the source cache.
5. Setup writes one active resource manifest and shared lease root below
   `runtime_root`; a lane cannot request an ID absent from that manifest.
6. A new epoch has empty fresh queue/manager records; none are copied from a
   prior epoch, while its lanes still use the same runtime-wide lease root.
7. A new worktree has a fresh lane binding and result path; it does not reuse
   another lane's process, queue, or session records.
