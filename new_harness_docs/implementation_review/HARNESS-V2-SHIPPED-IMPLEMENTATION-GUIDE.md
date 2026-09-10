# Harness v2: shipped implementation guide

## Read this first

This document describes the harness that is actually shipped in
`harness-single` at commit `f4328b177177a3aa71bf5f064b88ad6033b3d903`.
It is not a workflow plan and it is not a description of a future design.

Harness v2 is a local program for ROOT to use when coordinating coding workers.
ROOT decides what work exists and which worker should do it. The harness does the
mechanical work around that decision:

- creates one isolated Git worktree for each lane;
- starts and observes one provider process for that lane;
- keeps durable records of what happened;
- prevents two lanes from holding the same declared exclusive resource;
- delivers notifications without allowing workers to edit ROOT's queue;
- lets ROOT review, accept, resume, stop, retire, or shut down lanes through
  public commands; and
- keeps run-time files out of the product checkout.

It does **not** create a task plan, select a model, choose an agent role, merge
branches, decide whether work is accepted, push Git branches, operate hardware,
or act as a general scheduler. Those remain ROOT or operator decisions.

The one public program is:

```powershell
python -m orchestrator_harness.operator_launch <command> [options]
```

Every public command returns the same five facts:

| Field | Meaning |
| --- | --- |
| `ok` | `true` for success and `false` for failure. |
| `code` | A short stable machine code such as `LAUNCH_LEASE_BUSY`. |
| `summary` | A short plain-English explanation. |
| `evidence_paths` | Exact files that the caller can inspect. |
| `next_action` | The normal safe next step. |

With `--json`, the object is printed as JSON. Without it, a success prints its
summary to stdout and exits `0`; a failure prints its stable code and summary to
stderr and exits non-zero.

## The four places files live

The most important thing to understand is that the harness deliberately keeps
four kinds of files apart. They have different owners and different rules.

| Place | What it contains | Who may write it | Is it product source? |
| --- | --- | --- | --- |
| Harness root | The shipped harness code, adapters, docs, and source cache | Developers; setup only installs/checks shipped material | Yes |
| ROOT workspace | The project ROOT is managing and the three installed ROOT provider payloads | ROOT/setup | Project files are source; installed payloads are operational support |
| Runtime root | Epoch, monitor, queue, lease, active-cache, and lane record state | Harness programs | No; Git-ignored |
| Lane worktree | One worker's checkout, result, transcript, worker inbox/outbox, and controller files | That lane's controller and worker, within defined files | It is an isolated Git worktree, not ROOT's checkout |

The terms used below are:

```text
<harness-root>    the harness-single repository
<root-workspace>  the project workspace named in harness-config.json
<rt>              <root-workspace>/.harness-runtime
```

In this project, `harness-single/` is the harness root and it is nested inside
the configured ROOT workspace. The design is still project-local: all normal
product, runtime, cache, disposable, and worktree paths remain under the project
workspace rather than using arbitrary machine-wide folders.

## What ships in the harness root

The following is the useful shipped layout. It is a guide to responsibilities,
not a claim that every file in the repository is listed.

```text
<harness-root>/
  harness-config.json             ROOT's closed v2 configuration
  resource-manifest.json          ROOT's closed list of exclusive resources
  README.md                       short operating guide
  QUICK_START.md                  shortest normal operator sequence
  QUICK_RULES.md                  safety and authority rules

  adapters/                       the provider catalog
    README.md                      how a local file-only adapter is structured
    codex/
    claude-code/
    qwen-code/
      README.md                    provider-specific notes
      harness/launcher_binding.py  provider command-builder/output-parser source
      root/                        ROOT-facing provider payload
      super-cache/                 managed worker-facing provider payload
      shipped-machinery/           notes about supplied machinery

  super-cache/
    workspace/.agent-workspace/   provider-neutral worker files
      result-stop-check.py
      lane-queue.py
      manager-notify.py
      hook-dispatch.py
    custom/                        empty-by-default file-only extension area

  orchestrator_harness/           Python implementation
    operator_launch.py             the only public command parser/dispatcher
    config.py                      config and resource-manifest validation
    setup.py                       one-time runtime/provider installation
    epochs.py                      one active epoch and runtime path ownership
    bootstrap.py                   prepare a lane worktree
    launch.py                      start, force-stop, and retire lanes
    controller.py                  long-lived per-lane controller
    monitor.py                     one persistent runtime monitor
    manager_queue.py               ROOT queue and worker inbox operations
    leases.py                      named exclusive-resource leases
    review.py                      completion review and acceptance pair
    resume.py                      restart a stopped, unaccepted lane
    shutdown.py                    close the whole runtime safely
    scan_watch.py                  scan, watch, and health reconciliation
    records.py / core.py           locks, atomic JSON, IDs, hashes, timestamps
    processes.py                   exact process identity and termination helpers
    root_hook_dispatch.py          common ROOT hook behavior
    root_hook_wrapper.py           hook invocation wrapper
    provider_adapters/             registered bindings for the three providers
    tests/                         ordinary product tests and v2 acceptance tests

  examples/
    v2_disposable_fixture.py       harmless local rehearsal fixture
    v2_live_matrix.py              live-provider matrix contract, not fake proof
```

### The source tree is not a runtime directory

`adapters/`, `super-cache/`, and `orchestrator_harness/` are shipped material.
Normal lane execution does not write results, queue files, lease files, or
provider transcripts into them. Setup copies the source cache into `<rt>` first,
then bootstrap copies the needed pieces into one worktree.

This separation matters because a worker can edit its assigned worktree but
cannot use that fact to rewrite ROOT's review decision, the shared manager
queue, or the shipped provider binding.

## Configuration files: exactly what ROOT supplies

`harness-config.json` is a closed two-key object. A normal managed configuration
looks like this:

```json
{
  "root_workspace": "C:\\path\\to\\the\\project-workspace",
  "managed_coordination": "enabled"
}
```

Only these keys are allowed:

| Key | Required | Meaning |
| --- | --- | --- |
| `root_workspace` | Yes | An absolute, non-symlink path to the project ROOT will use. |
| `managed_coordination` | No | `enabled` (the default) or `disabled`. |

`config.py` derives the runtime path from this value. A later command cannot
provide a different runtime path, profile flag, or alternate configuration file
to change the meaning of an active run.

`resource-manifest.json` is also closed. It is the only source of resource IDs
that a lane may request:

```json
{
  "schema": "resource-manifest/v1",
  "resources": [
    { "id": "shared-device", "exclusive": true }
  ]
}
```

The list may be empty. Each ID must be nonblank and unique, and every entry must
say `exclusive: true`. A launch may request only an ID from the active runtime
copy of this manifest.

Changing the workspace, managed/plain mode, or resource list while an epoch or
lease is live is not silently accepted. The harness returns an error and asks
ROOT to shut down first. That prevents an old lane from continuing under a new
meaning of "the workspace" or "this resource."

## What `harness setup` installs and creates

Run setup once from the harness root:

```powershell
python -m orchestrator_harness.operator_launch harness setup
```

Setup has a validation phase and a write phase. It validates configuration,
resource manifest, the complete shipped adapter catalog, planned ROOT payload
destinations, and the active-cache plan before it writes anything. A collision
in normal mode therefore fails before a partial payload installation.

On success it creates or refreshes this runtime tree:

```text
<rt>/
  RUNTIME_STATE.json                 state: OPEN
  monitor/MONITOR.json               one monitor's PID, creation time, state, heartbeat
  manager/QUEUE.json                 managed only; idle queue before an epoch opens
  resources/
    RESOURCE_MANIFEST.json           atomic active copy of ROOT's manifest
    leases/                          empty until a controller holds a resource
  super-cache/
    workspace/                       active copy of the common source cache
    adapter-payloads/
      codex/
      claude-code/
      qwen-code/                     active copies of worker provider payloads
    custom/                          preserved optional local additions
  epochs/                            empty until first bootstrap
  worktrees/                         empty until first bootstrap
```

It also installs all three ROOT payloads beneath `<root-workspace>`:

```text
<root-workspace>/.codex/
<root-workspace>/.claude/
<root-workspace>/.qwen/
```

Each ROOT payload contains its provider configuration/binding, hooks, and eight
small ROOT skills. The skills tell ROOT to use the public launcher; they are not
alternate implementations of queue writes, polling, process control, or setup.

Setup does **not** create `CURRENT_EPOCH.json`, an epoch folder, a lane
worktree, a provider session, a lane lease, or a worker process. Those belong to
later operations.

If setup finds a valid active cache and valid installed payloads, it keeps them.
`harness setup --overwrite` is the narrow opt-in way to replace planned harness
payload targets. It does not mean "erase the runtime."

## Managed and plain mode: the real difference

The profile is chosen once by `managed_coordination` and stays fixed for the
epoch.

### Managed mode

Managed mode is the default. It gives ROOT a manager queue and gives each lane a
separate worker inbox/outbox. It also stages provider hook material and the two
worker coordination skills.

Use it when ROOT wants the harness to deliver lane events and send a running
worker additional assignments.

### Plain mode

Plain mode is a complete no-coordination variant. It still has a worktree,
controller records, result validation, review, leases, and cleanup. It does not
have:

- a manager queue;
- worker inbox or escalation outbox;
- installed worker coordination hooks;
- worker `manager-notify` or `lane-assignment` skills; or
- provider coordination payload in the lane worktree.

ROOT observes a plain lane with `scan` or foreground `watch`. There is no hidden
fallback that turns plain mode into managed mode.

## Provider catalog: what is shipped for Codex, Claude Code, and Qwen Code

The harness ships three named adapters: `codex`, `claude-code`, and `qwen-code`.
They have the same four-part layout:

```text
adapters/<provider-id>/
  harness/launcher_binding.py
  root/<provider-dot-directory>/
  super-cache/<provider-dot-directory>/
  shipped-machinery/
  README.md
```

The provider dot directory is `.codex`, `.claude`, or `.qwen`.

### Launcher binding

The binding is imported from the registered matching path under
`orchestrator_harness/provider_adapters/<provider-id>/`. It supplies four
things: `PROVIDER_ID`, `ADAPTER_VERSION`, `build_argv(...)`, and
`parse_line(...)`.

The shared controller asks the binding to build the provider command and parse
its output. It does not contain a large `if provider == ...` tree for lifecycle
behavior. Bootstrap verifies that the selected binding declares the provider ID
it was asked to use.

### ROOT payload

Setup installs all ROOT payloads because ROOT may use any of the installed
provider CLIs. Every ROOT payload supplies the same eight thin skills:

1. wait for a manager notification;
2. acknowledge a manager event;
3. close an ordinary manager event;
4. review a completed lane;
5. send an assignment to a lane;
6. resume a lane;
7. force-stop a lane; and
8. shut down the harness.

They tell ROOT which public command to run and when. For example, the close
skill tells ROOT to read the fixed manager queue, acknowledge a top-level event,
handle it, then use `manager close`; it never tells ROOT to edit `QUEUE.json`.

### Worker payload

Bootstrap stages only the selected provider's worker payload in a managed lane.
It contains the provider's hook setup/binding and exactly two coordination
skills:

- `manager-notify`: call the supplied helper to create an escalation file.
- `lane-assignment`: call the supplied helper to acknowledge, complete, or block
  a ROOT assignment.

The worker does not receive all providers' payloads. A Claude lane does not get
Codex or Qwen worker configuration, and a plain lane gets none of this managed
coordination material.

## The first lane: what bootstrap creates

ROOT prepares a lane with:

```powershell
python -m orchestrator_harness.operator_launch lane bootstrap `
  --lane-id feature-a `
  --provider codex `
  --model <model-name> `
  --exclusive-resource shared-device `
  --task-card <path-to-project-task-card.json>
```

`--exclusive-resource` may be omitted or repeated. It is a name from the
resource manifest, not a path or a hardware command.

Before bootstrap creates a worktree, it checks the lane ID, task card, provider,
model, active configuration, requested resource IDs, and destination paths. A
reused lane ID, an undeclared resource, a missing adapter, or an existing target
worktree fails before a provider starts.

If no epoch is active, bootstrap opens one. An epoch is a group of lanes that
share the same profile, configuration identity, and active resource manifest.
Its files look like this:

```text
<rt>/
  CURRENT_EPOCH.json
  epochs/<epoch-id>/
    epoch-state.json
    active-lanes.json
    lanes/<lane-id>/
      lane.json
      COMPLETION_REVIEW.json          appears only after ROOT reviews
      ORCHESTRATOR_ACCEPTANCE.json    appears only after ROOT decides
  worktrees/<epoch-id>/<lane-id>/
    ...the project's Git checkout on a new lane branch...
```

`CURRENT_EPOCH.json` is a small pointer to the active epoch. `epoch-state.json`
holds the immutable configuration identity and epoch state. `active-lanes.json`
is a rebuildable index; `lane.json` is the authoritative lane record.

Bootstrap then runs `git worktree add -b ...` against the project workspace. It
creates the lane worktree under the runtime root, creates `.agent-workspace/`,
copies the common cache overlay, copies the selected provider payload when
managed, and records a copy receipt.

The result is a prepared lane, not a running lane. Bootstrap writes the input
the controller will later consume, but it does not start a provider or take a
lease.

## What is inside a lane worktree

For a managed lane, the important files are:

```text
<rt>/worktrees/<epoch-id>/<lane-id>/
  RESULT.json                         worker's terminal result
  .agent-workspace/
    invocation.json                   prepared controller input; launch consumes it
    controller.status.json            controller status snapshot
    controller.events.jsonl           append-only controller audit trail
    provider-transcript.jsonl         parsed/provider transcript facts
    provider-stderr.txt               provider stderr capture
    last-message.txt                  final provider message capture
    overlay-receipt.json              what bootstrap copied
    harness-hook-binding.json         generated run-specific hook paths/identity
    hook-dispatch.py                  shared managed hook entry point
    result-stop-check.py              Stop hook result validator
    QUEUE.json                        this worker's ROOT-to-worker inbox
    lane-queue.py                     worker helper to move assignment state
    manager-notify.py                 worker helper to create escalation output
    manager-notifications/            unconsumed worker escalation files
    processed-notifications/          escalation files consumed by monitor
  .codex/ or .claude/ or .qwen/       selected worker provider payload only
```

For a plain lane, the controller files, transcript, `invocation.json`, and
`RESULT.json` still exist. The managed-only queue, helpers, notification
directories, hook machinery, worker skills, and provider coordination payload
do not.

The folder outside the worktree is just as important:

```text
<rt>/epochs/<epoch-id>/lanes/<lane-id>/
  lane.json
  COMPLETION_REVIEW.json
  ORCHESTRATOR_ACCEPTANCE.json
```

The worker can write `RESULT.json` in its worktree. It cannot write the two
ROOT decision records because they are outside its working tree and are written
only by `lane completion-review`.

## Launching a prepared lane: what runs and who owns it

ROOT starts a prepared lane with:

```powershell
python -m orchestrator_harness.operator_launch lane launch --lane-id feature-a
```

The short launch command reads the saved lane record and its
`.agent-workspace/invocation.json`. The invocation is not rewritten at launch.
The command starts the long-lived controller; the controller starts the provider
and owns the resulting process boundary.

The controller's job is concrete:

1. Acquire every requested lease or no lease at all.
2. Start the selected provider through its registered binding.
3. Record PID-plus-creation-time identity for the provider and helpers.
4. Capture provider transcript, stderr, and last message in the lane worktree.
5. Maintain `controller.status.json` and append factual execution entries to
   `controller.events.jsonl`.
6. Read and validate `RESULT.json` when the provider reaches a terminal state.
7. Mark the lane `review_pending` only when the result is valid; otherwise mark
   it `result_invalid`.
8. Prove its provider/helper process boundary is gone before normal lease
   release.

The controller is the only long-lived lane process. ROOT's launcher command
returns; ROOT does not keep a provider process handle and does not directly own
the lane's lease.

### Exact process identity

`processes.py` treats a process as this pair:

```text
PID + process creation time
```

A later process with the same PID is not the old provider. Every safe stop,
cleanup proof, orphan check, and monitor liveness check uses both values. The
harness never finds a process by a broad executable name such as `codex` and
kills every matching instance.

### Normal lease acquisition

If the lane requested resources, the controller uses `leases.acquire_leases()`.
It takes the leases lock, first checks whether every requested lease file is
absent, then writes all of its lease records. If any one resource is already
held, it writes none and launch returns `LAUNCH_LEASE_BUSY`. It does not leave a
provider waiting invisibly for a resource.

The lease file stores the resource ID, lane ID, run ID, controller PID, process
creation time, and acquisition time. The normal release path only removes a
lease belonging to that lane's current run after cleanup proof.

## The monitor: what it reads and what it writes

Setup starts one persistent monitor for a runtime. It is not one monitor per
lane and it is not another task scheduler.

On every pass, `monitor.py` reads:

```text
CURRENT_EPOCH.json
epochs/<epoch-id>/epoch-state.json
epochs/<epoch-id>/active-lanes.json
epochs/<epoch-id>/lanes/<lane-id>/lane.json
<lane worktree>/.agent-workspace/controller.status.json
lease records when needed for orphan detection
```

It does not scan the disk looking for arbitrary worktrees. It only examines
lanes recorded in the active epoch.

From those records it derives actionable facts such as:

- a valid terminal result that needs ROOT review;
- a missing, malformed, or contradictory terminal result;
- a controller that exited;
- a provider that exited without a result;
- a status/transcript contradiction;
- terminal work with cleanup still unproven; or
- an orphaned lease.

Normal resource contention is deliberately absent from this list. A resource
conflict was already reported synchronously as `LAUNCH_LEASE_BUSY`, before a
second provider was started.

The monitor updates `monitor/MONITOR.json` with its exact identity, state,
heartbeat time, and watched-lane count. It also rebuilds the active-lane index
from controlled lane records when health reconciliation is needed. `lane.json`
remains authoritative if the index and lane record disagree.

## Managed coordination: three separate queues, not one shared file

Managed mode has three different channels. They must not be confused.

| Channel | Location | Writer(s) | Reader(s) | Purpose |
| --- | --- | --- | --- | --- |
| Manager queue | `<rt>/manager/QUEUE.json` | Monitor creates events; ROOT changes event state; hook appends delivery receipt only | ROOT | Tell ROOT something needs attention |
| Worker inbox | `<worktree>/.agent-workspace/QUEUE.json` | ROOT appends assignment; worker helper changes assignment state | That one worker | Send ROOT-to-worker work |
| Worker outbox | `<worktree>/.agent-workspace/manager-notifications/` | Worker helper | Monitor | Ask ROOT for a decision or help |

### Manager queue

The manager queue is `manager-queue/v1`. It has an epoch ID and a fresh queue
ID, plus events. An event contains an event ID, type, lane ID, run ID, optional
actionable status, summary, state, history, and delivery history.

The event states are:

```text
PENDING -> ACKNOWLEDGED -> COMPLETE or BLOCKED
```

There are only three legitimate writers:

1. The monitor appends a new event.
2. ROOT acknowledges or closes an existing event through the public command.
3. The managed PostToolUse hook appends a `DELIVERED` receipt.

The controller and workers never write it. The receipt also never changes an
event from `PENDING` to `ACKNOWLEDGED`; a hook delivery is not ROOT handling an
event.

Every queue change goes through `_update_manager_queue()` in
`manager_queue.py`. It takes the queue lock, reads and schema-checks the whole
file, confirms its epoch/queue header still matches `CURRENT_EPOCH.json`,
changes only the permitted record fields, atomically replaces the JSON file if
it changed, then releases the lock. A writer using an old queue identity gets
`QUEUE_REPLACED` instead of writing to the wrong queue.

### ROOT's manager loop

When ROOT is deliberately idle, it can wait:

```powershell
python -m orchestrator_harness.operator_launch watch --until-actionable --timeout 5m
```

After a managed notification, ROOT reads the manager queue without editing it,
acknowledges each top-level event it actually handled, acts on the underlying
condition, and closes the ordinary event:

```powershell
python -m orchestrator_harness.operator_launch manager acknowledge --event-id <id>
python -m orchestrator_harness.operator_launch manager close `
  --event-id <id> --outcome COMPLETE --summary "reviewed the lane result"
```

Closing an event records ROOT's handling decision. It does not magically fix
the lane or release a lease. The ground truth changes only when the relevant
controller, worker, or cleanup operation changes it.

### Worker inbox and outbox

ROOT sends a worker an assignment with:

```powershell
python -m orchestrator_harness.operator_launch send-lane-notification `
  --lane-id feature-a --prompt "Run the focused tests and report the result."
```

The command checks that the lane exists, is managed, is running, and still has
the exact recorded live process identity. It then appends one `PENDING`
assignment to that lane's inbox under the inbox lock. It does not say the worker
read it.

The worker uses `lane-queue.py` to move its own assignment through
`PENDING -> ACKNOWLEDGED -> COMPLETE` or `BLOCKED`. If blocked, it uses
`manager-notify.py` to create an outbox escalation that names the decision or
action it needs and includes local evidence. The monitor consumes that file once
and turns it into a manager event.

## Review and acceptance: the worker result is not ROOT's decision

The worker writes this file in its own worktree:

```text
RESULT.json  (schema result/v1)
```

It contains lane/run identity, an outcome (`PASS`, `FAIL`, or `BLOCKED`), a
summary, evidence paths, completion time, and a canonical content hash.

The controller checks whether the result matches its current lane/run/task and
is structurally valid. A valid result leads to `review_pending`; an invalid or
missing one leads to `result_invalid`. In managed mode, the monitor turns that
into the corresponding manager event.

ROOT records the actual review with:

```powershell
python -m orchestrator_harness.operator_launch lane completion-review `
  --event-id <managed-event-id> `
  --review-outcome PASS `
  --approval ACCEPTED `
  --review-summary "The result and evidence meet the task card."
```

Plain mode uses `--lane-id` instead of `--event-id`. The two selectors are
mutually exclusive.

`review.py` reads the task card and result, checks their schemas and hashes,
checks lane/run identity, reads the worktree's current commit, and writes this
linked pair outside the worktree:

```text
COMPLETION_REVIEW.json
ORCHESTRATOR_ACCEPTANCE.json
```

The acceptance record includes the review's content hash. Matching copied text
is not enough; a review/acceptance pair must link to the actual review content.

`review-outcome` is ROOT's factual finding. `approval` is ROOT's separate
decision. `ACCEPTED` normally requires `PASS`. A non-PASS acceptance is possible
only with the explicit `--force-accept --force-reason ...` route, and the reason
is persisted in the acceptance record. A rejection leaves the lane available for
resume; an accepted lane is not normally resumable.

For a managed review, the same command closes its own review event with a
generated nonblank summary such as `completion review recorded: PASS / ACCEPTED`.

## Resume, force-stop, retirement, and shutdown

### Resume

Use resume only for a stopped, unaccepted lane:

```powershell
python -m orchestrator_harness.operator_launch resume-lane `
  --lane-id feature-a --resume-task-card <new-task-card.json> `
  --rationale "Address the rejected review findings."
```

`resume.py` uses the existing lane worktree and native provider-session context.
It creates a fresh run ID, clears the previous run's current result/review/
acceptance and worker-inbox artifacts, writes the new task-card state, validates
the fresh invocation, and only then returns the lane to running state. It does
not invent a new worktree or pretend that an old PID is still valid. If the
worktree or saved provider session is missing, the honest answer is to bootstrap
a new lane.

### Force-stop

Use force-stop only for one stuck lane:

```powershell
python -m orchestrator_harness.operator_launch lane force-stop --lane-id feature-a
```

`launch.py` resolves the lane record, targets only recorded provider/helper/
controller identities, proves the process boundary is gone, force-releases that
lane's leases, and marks the lane retired. If a process cannot be terminated,
the command returns `FORCE_STOP_PROCESS_SURVIVED` and keeps the evidence. It
does not fall back to killing every process with a provider name.

### Normal retirement

After a lane has a valid `ACCEPTED` record, ROOT retires it with:

```powershell
python -m orchestrator_harness.operator_launch lane retire `
  --acceptance-ref <path-to-ORCHESTRATOR_ACCEPTANCE.json>
```

Retirement validates the acceptance chain, waits for/proves cleanup, releases
the lane's lease only after that proof, records the retired state, and retains
the lane branch. A retired worktree can later be removed by the operator; the
harness does not require retired worktrees for new setup or new lanes.

### Whole-runtime shutdown

Use shutdown when ending the run:

```powershell
python -m orchestrator_harness.operator_launch harness shutdown
```

`shutdown.py` changes `RUNTIME_STATE.json` from `OPEN` to `SHUTTING_DOWN`,
handles every active lane, proves cleanup, releases its leases, retires it,
clears `CURRENT_EPOCH.json`, stops the monitor, marks the runtime `CLOSED`, and
runs `git worktree prune` against the project workspace. If any lane's cleanup
cannot be proved, it returns `SHUTDOWN_LANE_CLEANUP_UNPROVEN`; it does not claim
the runtime is closed.

## Orphaned lease recovery

Most lease files are removed by normal controller cleanup or the targeted
force-stop route. The final Tier 4 addendum also provides one explicit operator
recovery command for a genuinely orphaned single lease:

```powershell
python -m orchestrator_harness.operator_launch lease force-release `
  --resource-id shared-device
```

The route is intentionally not a text-file deletion instruction. In order, it:

1. loads the saved configuration and resource manifest;
2. refuses a resource ID that is not declared;
3. takes the shared lease lock;
4. re-reads and validates the exact lease record under that lock;
5. checks resource ID, lane ID, run ID, PID, and process creation time;
6. looks up the current lane while still holding the lock; and
7. deletes only that lease file after the old holder is proven obsolete.

It refuses to release an exact live holder (`FORCE_RELEASE_HOLDER_LIVE`). It
also refuses an unprovable holder unless the current lane record proves the old
run was retired, abandoned, or superseded by a different run. A PID whose
creation time has changed is a recycled PID, so it can safely be treated as the
old holder being gone. After deletion the code checks that the file is really
absent; a failed delete is not reported as success.

## The important state machines

These are the core state changes an operator will see.

### Lane lifecycle

```text
prepared
  -> running
  -> review_pending | result_invalid
  -> accepted
  -> retired

additional terminal/problem states: blocked, abandoned
```

The controller owns observed terminal result status. ROOT owns review and
acceptance. Launch/resume/retire routes make the short lifecycle transitions.

### Manager event lifecycle

```text
PENDING -> ACKNOWLEDGED -> COMPLETE | BLOCKED
```

Only ROOT moves an event through its state. The monitor produces events. A hook
can say delivery happened but cannot acknowledge or close one.

### Worker assignment lifecycle

```text
PENDING -> ACKNOWLEDGED -> COMPLETE | BLOCKED
```

ROOT appends an assignment. The assigned worker advances only its own assignment.

### Runtime lifecycle

```text
OPEN -> SHUTTING_DOWN -> CLOSED
```

Setup creates or reopens an `OPEN` runtime. Shutdown is the only normal route to
`CLOSED`.

## Why records are written atomically

Most runtime files are JSON records. `records.py` uses a short advisory lock and
a temporary sibling in the same directory. It validates the new JSON, then uses
same-volume atomic replacement. The old complete file remains visible until the
new complete file replaces it; a half-written target file is not the normal
outcome.

The code stores SHA-256 hashes of canonical JSON in records that need integrity
links, such as results and review/acceptance pairs. This detects an accidental
mismatch or stale copied record. It is not a cryptographic identity system and
does not claim that a hash proves who authored a file.

The important lock order is fixed so concurrent code does not take the same
locks in opposite order:

```text
runtime-state -> manager-queue -> lane-record -> resource-lease -> monitor-record
```

## Public command reference in plain English

| Command | What it actually does | What it deliberately does not do |
| --- | --- | --- |
| `harness setup [--overwrite]` | Validates config/catalog, stages cache, installs ROOT payloads, starts monitor | Start a lane/provider or open an epoch |
| `harness shutdown` | Retires live lanes after cleanup proof, stops monitor, closes runtime | Broad-kill processes or erase lane branches |
| `lane bootstrap ...` | Validates request and prepares one worktree/record/invocation | Start provider or take lease |
| `lane launch --lane-id` | Starts the controller; controller starts provider and leases | Rewrite the prepared invocation |
| `lane completion-review ...` | Validates worker result and writes ROOT review/acceptance pair | Merge code or run the worker's reported checks |
| `resume-lane ...` | Starts a new run in same stopped unaccepted lane | Resume accepted work or invent missing session/worktree state |
| `lane force-stop --lane-id` | Stops one exact recorded stuck lane and releases its lease | Kill provider processes by name |
| `lane retire --acceptance-ref` | Gracefully retires one accepted lane after cleanup proof | Create acceptance |
| `manager acknowledge --event-id` | ROOT marks one read event acknowledged | Fix the underlying lane condition |
| `manager close --event-id --outcome --summary` | ROOT records terminal handling of an ordinary event | Clear the condition or restart a lane |
| `lease force-release --resource-id` | Deletes one proven orphaned declared lease | Delete a live or unproven holder's lease |
| `send-lane-notification --lane-id --prompt` | Appends one assignment to a running managed worker inbox | Claim delivery or edit manager queue |
| `scan --no-write` | Returns a read-only status snapshot | Mutate runtime records |
| `watch --until-actionable ...` | Blocks ROOT's foreground session until an actionable fact appears | Run as a background scheduler |
| `health reconcile` | Rebuilds lane index and re-derives status | Change task meaning or acceptance |
| `health monitor-recover` | Handles missing/dead/hung monitor state under monitor lock | Start a second monitor over a live exact identity |

## What the test suite proves, and what it does not

The shipped tests have three honest layers.

1. Ordinary unit/product tests check real parser, record, setup, bootstrap,
   lease, queue, review, monitor, provider-binding, packaging, and process code.
2. The `tests/v2_acceptance/` suite adds independent CHECK-U1 through CHECK-U5
   fixtures and oracles. These check layout/configuration/epochs, profiles and
   queues, lifecycle/review/leases, records/CLI, and portability/disposable
   behavior. The 82-gap inventory maps the master checklist to observable checks.
3. The live matrix has four `CHECK-LIVE-*` checks and explicit Windows, macOS,
   and Linux platform claims. It requires real native provider CLI execution.

The first two layers have been run and accepted as static/synthetic evidence.
They do not become live proof merely because a fixture imitates a provider or a
process. The project has a Windows disposable readiness result, but native macOS
and native Linux-storage runner evidence remains unavailable. Therefore REQ-017
is still truthfully `INCOMPLETE`.

## What changed from the pre-Tier-4 candidate

The overhaul was a replacement, not a cosmetic wrapper. It removed candidate-era
firmware/campaign compatibility routes and checked-in historical run artifacts,
then added the v2 product boundary described above: one public launcher, closed
config/manifest, one runtime root, one active epoch, managed/plain profiles,
staged provider catalog, new record layer, controller/monitor/queue ownership,
review/acceptance chain, exact process and lease handling, portability checks,
and independent acceptance assets.

The final addendum made three concrete corrections after the main delivery:

- ignore `.harness-runtime/` so runtime state cannot appear in source commits;
- add `lease force-release` with exact identity/lane proof; and
- make manager queue read/validate/mutate/replace one transaction while requiring
  and preserving a nonblank close summary.

For the detailed Git-history comparison, see
`HARNESS-V2-IMPLEMENTATION-REVIEW.md` beside this guide.

## Where to read next

| If you need to understand... | Read... |
| --- | --- |
| Normal use | `harness-single/QUICK_START.md` and `README.md` |
| Every public command and record contract | `harness-single/orchestrator_harness/README.md` and `SPEC.md` |
| Configuration and runtime root derivation | `harness-single/orchestrator_harness/config.py` |
| Setup and installed payloads | `harness-single/orchestrator_harness/setup.py` |
| Worktree construction | `harness-single/orchestrator_harness/bootstrap.py` |
| Controller launch/cleanup | `harness-single/orchestrator_harness/launch.py` and `controller.py` |
| Monitor and status derivation | `harness-single/orchestrator_harness/monitor.py` and `scan_watch.py` |
| Queue ownership | `harness-single/orchestrator_harness/manager_queue.py` |
| Leases | `harness-single/orchestrator_harness/leases.py` |
| Review/acceptance | `harness-single/orchestrator_harness/review.py` |
| Full accepted plan and live-evidence boundary | `master_planning/harness-v2-tier4/` and `HANDOFF.md` |
