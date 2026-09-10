# Overall harness fix map

> **Status: supporting implementation summary.** When this overview differs
> from the master planning document or a current detailed v2 target contract,
> the master and detailed contract win.

## Scope

This is the recommended repair map for the external neutral harness at:

```text
<root-workspace>/<harness-root>
```

It is a design/implementation plan, not a claim that these repairs already
exist in that checkout. It does not change the frozen firmware campaign.

The one explicit compatibility setting is part of this repair. `managed` enables
the manager queue, native ROOT/worker hooks, and worker coordination files.
`plain` disables that one optional package while
keeping a complete ordinary lane: worktree, selected provider launcher,
controller, result validation, lane record/monitoring, direct completion review,
and resume. Either profile can use the always-available resource locks when a
lane names a declared hardware resource. Plain is not an unsupported error path
and creates no queue or hook payload. The profile is fixed for an epoch.

## 1. Add one real setup command

Add one public command:

```text
operator_launch harness setup
operator_launch harness setup --overwrite
```

It reads the fixed `<harness-root>/harness-config.json` itself. That file is
also the only input for the one optional compatibility setting: setup validates
the stored `managed_coordination` value and materializes the matching facilities. ROOT does not pass a
pile of paths, feature flags, or a profile override every time it starts a
command.

Setup creates the active shared super-cache, installs the Codex, Claude Code,
and Qwen Code ROOT files and ROOT skills into `root_workspace`, creates the
shared runtime folders, writes the active resource manifest, and starts the one
mandatory persistent monitor. It also checks that the
required shipped hook payloads exist for a managed profile. It does **not** select, start, or rebind
the already-running ROOT CLI; open an epoch, create a lane, start a provider, or
touch hardware.

The point is that the hooks, shared helper scripts, notification skills, Stop
checks, cache, monitor, and resource state are put in place by one mechanical
operation rather than remembered as a checklist.

Normal setup fails before changing anything when a planned harness/adapter target
file already exists. `--overwrite` deliberately replaces only that complete,
preflighted set of known target files, reports every replacement, and rolls the set
back if a late write fails. It does not overwrite arbitrary ROOT-workspace files or
the active runtime cache.

## 2. Add a real, model-agnostic lane bootstrap

The neutral harness needs a product-owned public bootstrap command. Bootstrap
is ordinary harness source code, not something ROOT writes into a runtime
folder and not a persistent process.

ROOT supplies a lane request with the lane ID, task inputs, provider binding ID,
model value, and any declared resource IDs. For example, a reviewer lane can
use the Codex binding with one GPT model while a coder lane uses a different
supported CLI binding and model. Bootstrap does not choose either one. It only
validates ROOT's supplied binding/model, writes them into that lane's invocation,
and later launch uses exactly the recorded pair.

For a non-shipped provider CLI, an author writes one small adapter tree. Codex,
Claude Code, and Qwen Code ship completed versions of those trees. The adapter
provides only provider-specific project files and a small launcher binding; the
generic bootstrap, controller, worktree, queues, cache, cleanup, and monitor
remain shared harness code.

Bootstrap mechanically creates the worktree, materializes required base shared
files, writes the task prompt/result template/lane record, and writes the one
controller invocation. Managed bootstrap additionally materializes the selected
adapter's hook/queue payload; plain bootstrap omits that coordination payload.
Either profile obtains a lease when, and only when, its request names a declared
exclusive resource.
The public launcher code also creates the current epoch record when needed,
registers the lane when launch succeeds, and retires the lane/epoch records after
cleanup. ROOT invokes the public lane command, but never opens, edits, or retires
epoch/lane records itself. Bootstrap stops after preparation. A separate public
launch command starts the controller and provider.

## 3. Replace the overly strict resume gate with `resume-lane`

The current resume logic rejects many ordinary continuation cases because it
tries to treat task/prompt hashes and amendment records as a broad admission
gate. The replacement is one public ROOT command, such as:

```text
operator_launch resume-lane --lane-id <id> --resume-task-card <new-card> \
  --rationale "<why this lane should continue>" --prompt "<new instruction>"
```

The command reads the old lane record itself. It checks only the facts that
must actually stop resume: the lane is not already ROOT-accepted, its recorded
worktree still exists, it has a
saved provider session ID, its provider/model binding remains recorded, and
the provider CLI accepts that saved session when asked to resume.

The new resume card is the current task card for the resumed work. The resume
prompt contains ROOT's rationale, the new resume card, and the new instructions.
The command preserves the same worktree and provider session, assigns the existing
lane a fresh `run_id`, and clears obsolete current result/review state. It does not
archive prior rejected artifacts or create a generation tree. ROOT does not rebuild
a PID, worktree, invocation, or provider resume command manually. If the provider
no longer knows the session, the command returns that provider error; it does not
fabricate a new session. If the operator has removed the stopped lane's worktree,
it returns `RESUME_WORKTREE_MISSING` rather than manufacturing a replacement.

## 4. Make bootstrap always copy the required central super-cache

The shared super-cache is required—not an optional caller-selected folder. The
product ships a read-only source tree:

```text
<harness-root>/super-cache/
```

On first setup, the harness byte-verifies and copies it to the active runtime
copy:

```text
<runtime-root>/super-cache/
```

Every bootstrap uses that one active folder. It never accepts a random per-lane
cache path.

Bootstrap copies the common base files and, only for a managed lane, the selected
provider payload into the new worktree by preserving their relative paths, like
checking out a small file tree at the worktree root. It **copies**, never moves,
source cache files.
Before changing the worktree, it preflights every destination. An existing
destination file is an error: do not merge or overwrite it. The error tells
ROOT the exact stale destination and the matching adapter/cache source path.
ROOT may delete the exact stale generated file, using that source as the
reference, then rerun bootstrap. No special cleanup command or extra permission
step is needed. Bootstrap itself still never deletes a collision automatically.

## 5. Give every live file one deterministic home

Stop accepting a hodgepodge of unrelated path arguments and searching arbitrary
folders for state. The fixed configuration names only the stable roots:

```text
<harness-root>/harness-config.json
  -> root_workspace
  -> managed_coordination compatibility choice only
```

Setup alone reads those choices and materializes their matching optional
runtime/adapter facilities. Bootstrap, launch, resume, and adapters consume the
result; they do not select, detect, or override a profile.

Everything else is derived from those values:

```text
<root-workspace>/            ROOT's project workspace
  <harness-root>/            project-local product source, fixed config, shipped templates
  .codex/.claude/.qwen/      static ROOT files and skills
  .harness-runtime/          all mutable harness state
    RUNTIME_STATE.json         one lifecycle gate
    super-cache/             active shared cache
    resources/               active resource manifest and live leases
    monitor/                 setup-started monitor record
    manager/QUEUE.json       managed profile only; fresh ID per managed epoch
    epochs/<epoch-id>/       diagnostics and lane registry
    worktrees/<epoch-id>/<id>/ lane worktrees (managed or plain)
```

The fixed harness source cache and adapter templates start under the project-local
`harness-root`.
Setup makes their active runtime copy. Other live state belongs under the
derived `<root-workspace>/.harness-runtime/` tree; it must not be scattered
elsewhere in the project workspace, a worker worktree, or arbitrary temporary
folders. Each command derives and records the exact path it uses instead of
searching for a likely one.

## 6. Managed profile: replace the current ambiguous queue behavior with two directional queues

In the managed profile there are two separate notification directions, not one
shared file used by both sides. Plain lanes create neither queue and use the
direct completion-review/resume path instead.

```text
worker -> ROOT:  <runtime-root>/manager/QUEUE.json
ROOT   -> worker: <worktree>/.agent-workspace/QUEUE.json
```

The worker-to-ROOT path is a small worker outbox plus the monitor. A worker
uses the shipped `manager-notify` skill/script when it needs ROOT intervention;
the monitor turns that into an event in ROOT's manager queue. ROOT uses the
public `send-lane-notification` command to put a new assignment only in that
one live worker's incoming queue.

Both queue files have a simple in-place state machine:

```text
PENDING -> ACKNOWLEDGED -> COMPLETE
                       -> BLOCKED
```

`PENDING` is the one meaning of “unacknowledged”; do not add a second boolean
that can disagree with it. PostToolUse does a small presence check. While its
own queue has pending work, it returns a short notice telling the model to
finish its current safe task, then read and handle the notification using the
shipped public skill/helper. It does not read, acknowledge, or resolve events
by itself.

The selected provider adapter writes the real native hooks. The worker Stop
hook reads only that worker's incoming queue and rejects Stop until every local
assignment is complete or blocked. ROOT's Stop hook reads only ROOT's manager
queue and rejects Stop until every ROOT event is complete or blocked. A worker
must never be blocked by work that belongs to ROOT. After ROOT handles an
acknowledged ordinary event, the `close-manager-notification` skill runs
`operator_launch manager close --event-id <id> --outcome COMPLETE|BLOCKED
--summary "<what ROOT did or needs>"`. Completion review closes its own event.

## 7. Rework scan/watch around the one ROOT queue

The existing scan and `watch --until-actionable` concepts are useful, but they
must stop treating arbitrary transcript growth or unrelated filesystem findings
as ROOT notifications.

Setup starts one persistent monitor. It reads only registered active lane
records and their declared status/event files. When a worker emits a declared
manager-notify outbox item, or a registered lane reaches a real actionable
state change, the monitor writes one ROOT event into ROOT's `QUEUE.json`.

There is no deduplication key, condition-generation key, or queue search for a
matching old event. For a status-driven notice, the lane's external runtime
record keeps one plain `last_reported_actionable_status` value. Under the
lane-record lock, the monitor reads the latest record, changes only that field,
and atomically replaces the file; the controller owns every other lane field.
The lock is held only for that one update and is released automatically in the
writer's cleanup path or when a crashed process closes its operating-system
handle.
The monitor compares the current actionable status with that saved value. If they
are the same, it writes nothing. If the status changes, it writes one new
timestamped event and replaces the saved value. A worker-created outbox file is one explicit
request; after the monitor admits it, the monitor moves that file to the lane's
processed-notifications folder, so later passes do not read it again.

This is intentionally non-mission-critical recovery. Queue writes use a temporary
file plus atomic replacement, so an ordinary crash leaves the old complete queue or
the new complete queue. Startup health checks remove malformed temporary records.
If the authoritative queue is malformed despite that protocol, the monitor removes
it and initializes a fresh empty queue with a new queue ID in the same active epoch;
it atomically updates `CURRENT_EPOCH.json`, and writers using the old ID return
`QUEUE_REPLACED` without writing. In-flight notifications may be lost or repeated
after a crash, but are never claimed handled or acknowledged.

The foreground ROOT `watch --until-actionable` command then waits only for a
change to that ROOT queue. It is used when ROOT is deliberately idle. It does
not scan arbitrary worktrees, does not treat each provider transcript word as
an event, and does not replace the monitor. The ROOT PostToolUse notice is the
other reminder while ROOT is working.

## 8. Ship the standard hook and skill material; make adapters copy-only

The active super-cache always contains the shared worker helper programs and
the shipped Codex, Claude Code, and Qwen Code worker hook/skill payloads.
Setup puts every shipped standard ROOT hook/skill payload in `root_workspace`:
`.codex`, `.claude`, and `.qwen`. Each native ROOT hook wrapper calls the same
generic current-epoch dispatcher; this is not a selected-provider binding.

An adapter is deliberately simple. It is just a tree of files copied to three
fixed destinations:

```text
adapter/root/       -> <root-workspace>/
adapter/super-cache/-> <runtime-root>/super-cache/
adapter/harness/launcher_binding.py
                     -> fixed registered harness binding path
```

The adapter files bridge provider-specific gaps: native hook configuration and
small wrappers, the CLI's skill paths, and the provider's start/resume/stdout
format. They call existing generic harness helpers. They do not introduce a
daemon, relay, replacement controller, or custom queue implementation.

Setup preflights all destination paths. Normal setup fails without changing anything
when an adapter-owned file already exists; `setup --overwrite` deliberately replaces
only the planned adapter/harness targets and reports them. The adapter README
explains exactly what an author must put in those three folders for a new standard
CLI. The harness-root README is the separate guide for ROOT operating the harness.

## 9. Make resources a setup-owned runtime facility

ROOT writes the allowed resource list **before** setup at the fixed source path:

```text
<harness-root>/resource-manifest.json
```

Setup validates it and writes the active file used by lanes:

```text
<runtime-root>/resources/RESOURCE_MANIFEST.json
<runtime-root>/resources/leases/
```

This is a small but important correction: ROOT should not hand-edit the active
runtime manifest after setup. ROOT authors the source list; setup makes the
active copy. A lane may name only IDs listed in that active file. The controller
creates the temporary lock file at launch and releases it only after it has
proved its own provider/helper processes are gone.

The lease folder is directly below `runtime-root`, not an epoch, so two active
epochs cannot both claim the same non-shareable resource. ROOT has authority
over the declared resource list; the controller has authority over live locks.

The harness-root README must give the exact short setup order: finish a custom
adapter only if needed, fill `harness-config.json`, write the source resource
list, run setup, check the generated active files, then begin a public lane
bootstrap/launch request. The launcher creates and retires epochs itself. The
README also lists the available features and the public commands/skills ROOT
uses later.

## 10. Add public shutdown plus its ROOT skill

Add:

```text
operator_launch harness shutdown
```

The command blocks new work, asks each active lane to perform its normal
controller-owned cleanup, verifies that controller/provider/helper processes
are gone, then asks the setup-started monitor to stop and verifies that exact
monitor process is gone. It does not kill every process with a name such as
`python`, `codex`, or `claude`.

The ROOT-only `harness-shutdown` skill tells ROOT to use that exact command when
intentionally ending the harness. It forbids closing a terminal, broad process
kills, or editing process/lease records directly.

## Important additions missing from the ten-item shorthand

### Worker result checking is separate from ROOT acceptance

Managed worker Stop hooks should reject a missing or malformed `RESULT.json`, so
a worker repairs its own result before exit. Plain lanes have no worker hook; the
common controller performs the same result validation when the provider exits.
That check only proves the result has the right lane/task/result shape. It does
not grant credit.

After a valid managed lane result, the controller records `review_pending` in its
worktree records and the persistent monitor promotes that status change into one
completion-review event for ROOT (see resolution R4 in `harness_single.md`). A
valid plain result becomes direct review-pending lane state.
The ROOT-only `review-lane-completion` skill directs ROOT to
`operator_launch lane completion-review`, which writes a factual
`PASS`/`FAIL`/`BLOCKED` completion review plus ROOT's separate
`ACCEPTED`/`REJECTED` approval through the public route. By default it makes one
cheap current task/result identity check against the managed reviewed event snapshot
or the plain lane's recorded current bundle; a mismatch is actionable. ROOT may use
a recorded `--force-accept` reason only for a structurally valid current chain it
has inspected. An accepted lane cannot be resumed. A rejected lane is marked
`REJECTED`; managed mode writes `LANE_RESUME_REQUIRED` back into ROOT's manager
queue while plain mode returns direct resume-required output. ROOT then uses
`resume-lane` with a new current task card. The review command never restarts the
provider itself. This keeps a valid `FAIL` or `BLOCKED` worker report reviewable
without falsely treating it as success.

### Exact process ownership remains important

The lane controller owns its provider and helper processes, the monitor owns
only itself, and shutdown coordinates those owners. Process records need a PID
plus process-creation time, not just a PID, so a later reused PID is
not mistaken for a harness process. Resource locks are released only after the
owning controller proves cleanup.

### Every repair needs disposable host-only proof

Before implementing hook-dependent lanes or using hardware, prove the setup path,
cache copy/collision error, adapter materialization, real headless hook discovery
and Stop enforcement for Codex, Claude, and Qwen, directional queues, notification
acknowledgement, Stop behavior, resume, lease contention, and shutdown with
disposable host-only lanes. A provider that cannot prove its hooks ran is unsupported
for hook-dependent lanes until a controller-level fallback is designed. A file merely
existing is not proof that a CLI hook actually ran.

### Public operations need clear failure statuses

Every public command returns a small structured result with `ok`, `code`, a
plain-English `summary`, exact `evidence_paths`, and a safe `next_action`. It
must not return only a generic exception or make ROOT search logs to learn what
happened.

The initial codes should be clear and narrow:

| Operation | Example failure codes |
| --- | --- |
| Setup | `SETUP_CONFIG_INVALID`, `SETUP_CACHE_INVALID`, `SETUP_RESOURCE_MANIFEST_INVALID`, `SETUP_ADAPTER_COLLISION`, `SETUP_OVERWRITE_FAILED`, `SETUP_MONITOR_ALREADY_RUNNING` |
| Bootstrap | `BOOTSTRAP_REQUEST_INVALID`, `BOOTSTRAP_WORKTREE_EXISTS`, `BOOTSTRAP_CACHE_COLLISION`, `BOOTSTRAP_ADAPTER_MISSING`, `BOOTSTRAP_RESOURCE_UNDECLARED` |
| Launch | `LAUNCH_INVOCATION_INVALID`, `LAUNCH_BINDING_FAILED`, `LAUNCH_LEASE_BUSY`, `LAUNCH_CONTROLLER_START_FAILED`, `LAUNCH_PROVIDER_START_FAILED` |
| Resume | `ALREADY_ACCEPTED`, `LANE_RUNNING`, `RESUME_WORKTREE_MISSING`, `NO_SAVED_SESSION_ID`, `INVALID_RESUME_TASK_CARD`, `RESUME_LANE_WRITE_FAILED`, or the provider's native resume error |
| Manager close | `MANAGER_CLOSE_NOT_ACKNOWLEDGED`, `MANAGER_CLOSE_ALREADY_CLOSED`, `MANAGER_CLOSE_NOT_ROOT_EVENT`, `MANAGER_CLOSE_INVALID_OUTCOME` |
| Completion review | `COMPLETION_REVIEW_EVENT_INVALID`, `COMPLETION_REVIEW_NOT_ACKNOWLEDGED`, `COMPLETION_REVIEW_STALE_SOURCE`, `COMPLETION_REVIEW_FORCE_REASON_INVALID`, `COMPLETION_REVIEW_OUTPUT_CONFLICT`, `COMPLETION_REVIEW_WRITE_FAILED` |
| Shutdown | `SHUTDOWN_LANE_CLEANUP_UNPROVEN`, `SHUTDOWN_MONITOR_UNPROVEN`, `SHUTDOWN_RUNTIME_AMBIGUOUS` |

`LAUNCH_LEASE_BUSY` is ordinary contention, not a harness crash: its next action
is to wait or launch work that does not need that resource. The cleanup-related
codes are fail-closed: the harness preserves evidence and leaves the lease in
place rather than reporting shutdown success.

## Final answer: what was missing?

Your ten items cover the main repair map. The three additions above are the
important missing pieces: result shape versus ROOT acceptance, exact process
ownership/cleanup proof, and host-only proof for every provider path. They are
not new subsystems; they are the checks that make the ten repairs reliable.
