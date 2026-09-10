# The scan, watch, and queue are currently three disconnected paths

> **Status: current detailed v2 target contract.** The early scan/router
> descriptions are candidate diagnosis; the monitor, fixed queue, and role-aware
> protocol sections define the v2 target under the master planning decision index.

## Scope

This document describes the external neutral harness at:

```text
<root-workspace>/<harness-root>
```

It does not describe or change the frozen firmware campaign runner. No campaign,
provider, MCP server, or hardware action occurred while writing this document.

## Short version

The harness currently has two different ways to notice something that ROOT should
care about, but they do not feed each other:

```text
scan / watch --until-actionable
    sees lane files and operating-system processes
    prints a diagnostic change
    does not write the manager queue

ManagerEventRouter queue
    can contain manager work
    is written only when code explicitly calls admit_notification(...)
    is not read by scan or watch --until-actionable
```

As a result, a worker can die and the scanner can correctly notice it, yet no queue
entry exists. Conversely, a queue entry can exist, yet `watch --until-actionable`
does not see it or wake ROOT for it.

In ordinary English, both are manager notifications. In the implementation, they
are separate systems.

## What `scan` actually does now

The harness configuration names a project root, one or more lane-folder patterns,
and the metadata folder name. The default example is:

```json
{
  "suite_root": "<project root>",
  "run_globs": ["worktrees/*"],
  "workspace_relpath": ".agent-workspace"
}
```

On every scan, the code expands `worktrees/*`. For each matching folder that has a
`.agent-workspace` folder, it reads the lane records it recognizes. These include
controller status JSON, agent/controller JSONL, `RESULT.json`, permission requests,
manager request/relay/signal files, declared helper or MCP-process records, and an
optional checkpoint.

It separately asks the operating system for a fresh process list. It compares that live process
list with the PID and creation-time information in the lane records. It then creates
diagnostic conditions such as:

- a controller status says a process is alive, but that exact process is gone;
- a provider exited without a valid result;
- a result is malformed or invalid;
- a declared request or relay requires attention;
- a runtime record cannot be read safely.

`scan` prints one current diagnostic snapshot. It does not open or modify a manager
queue.

## What `watch --until-actionable` actually does now

`watch --until-actionable` repeatedly runs the same scan logic. It compares the
current diagnostic-condition list with the prior list saved in the configured
diagnostic output folder. It sleeps for `poll_interval_seconds` between passes.

When a new or changed diagnostic condition is classified actionable, it prints that
condition, writes the new diagnostic cursor, and exits. ROOT must handle the result
and start a new watch command to wait for a later change.

This is a bounded foreground command. While ROOT is running it, ROOT is waiting and
cannot do normal agent work. That is acceptable when ROOT is deliberately idle. It
is not an automatic notification channel while ROOT is working.

Most importantly, this loop does **not** read `QUEUE.jsonl`. It only reads lane
metadata and the OS process snapshot. Its diagnostic cursor/output files are not the
manager queue.

### It silently ignores most normal lane outcomes

After every scan pass, `watch --until-actionable` compares the new condition list
with its previously saved list. It then applies a hardcoded filter. It exits only
for a changed condition whose data says `manager_actionable: true`, or whose type is
one of:

```text
MANAGER_SIGNAL
RESOURCE_CONFLICT
RESOURCE_AMBIGUOUS
REQUEST_EXPIRING
REQUEST_STALE
RELAY_READY
LANE_STAGE_REPEAT
```

Ordinary controller/process findings are not in that list. For example, the current
code can observe each of these yet continue waiting:

```text
CONTROLLER_EXITED       provider/controller ended
STALE_STATUS            status says running but transcript says terminal
CODING_RESULT_INVALID   result is missing or malformed
RESULT_AVAILABLE        a result appeared
WAITING_RESOURCE        a lane is waiting for a held resource
```

It is worse than merely failing to print them immediately. On an unaccepted change,
the command saves the new diagnostic cursor and uses it as the next comparison
baseline. Thus the watcher has recorded the event internally, shown it to no ROOT
user, and normally will not rediscover the same unchanged fact on the next pass. It
will simply continue until a narrow hardcoded condition appears or its timeout
expires. The default timeout is 60 seconds.

The separate `watch --until-event` command returns for any changed diagnostic
condition. That does not repair `--until-actionable`; it merely confirms that the
current actionable filter deliberately excludes normal lane lifecycle facts.

## What the queue actually does now

The manager queue is a folder containing durable queue/state/wake/delivery files.
The usual way to add an item is the `DeliveryCoordinator.admit_notification(...)`
function. That function creates an event with this shape in substance:

```text
event ID
type: MANAGER_SIGNAL
signal/notification ID
binding identity
manager_actionable: true
severity
optional extra facts and a reference to fuller payload/evidence
```

The product has no normal scan, watcher, launcher, or lane-controller call site for
`admit_notification(...)`. Its call sites are tests. Therefore this is a tested
library function, not a currently wired lane-to-manager notification pipeline.

When an event is already pending, an installed provider `PostToolUse` hook can write
a **delivery receipt**. That means only: “this provider was told that queued work
exists at this safe boundary.” It does not create a manager event, copy scanner
findings into the queue, reveal the actual event to the provider, or acknowledge it.

The current queue records also have no sender or recipient role. If two bindings
point at one queue, each sees every pending item. A worker can even see an event it
created itself. This is unsuitable as a real ROOT-to-worker or worker-to-ROOT
message route.

## Why the current split is a real design problem

The scanner is the code that already knows whether a lane died, which lane it was,
which process identity was expected, and which status/result file proves the
finding. The queue is the code intended to make manager work durable and visible to
provider hooks. Leaving them disconnected loses the useful context and gives ROOT
two separate things to remember:

1. inspect diagnostics for lane health; and
2. inspect a queue that may contain unrelated manually admitted items.

It also makes the name `watch --until-actionable` misleading. It waits for a
diagnostic change, not for all manager-actionable work.

## Required ROOT and worker skills

The adapter's ROOT payload must include this provider-local skill:

```text
adapter/root/<provider-skill-root>/manager-notification-watch/SKILL.md
```

It must tell ROOT to run the public `watch --until-actionable` command only
after ROOT has finished its current task and is deliberately waiting for worker
activity. The skill must also state the practical limitation: the command holds
the current ROOT CLI session until it returns, so ROOT must not run it while
actively working. When it returns, ROOT handles the reported item before
starting another wait. The skill does not claim that this is a background
notification process. Until the recommended monitor/queue repair exists, it
also must not claim that the current command reads the manager queue. After that
repair, the same foreground/idleness rule remains, but the command returns for
an epoch-queue event instead of only a diagnostic change.

The always-enabled shared super-cache must ship a worker `manager-notify` skill
for the standard providers at all three paths:

```text
.codex/skills/manager-notify/SKILL.md
.claude/skills/manager-notify/SKILL.md
.qwen/skills/manager-notify/SKILL.md
```

Bootstrap copies the complete cache into every worker worktree. Each provider
uses the skill in its own directory. The skill tells the worker to call its
already-written `.agent-workspace/manager-notify.py` helper when it needs ROOT
intervention, instead of hand-editing a queue file. For a custom supported CLI,
the same skill must be included in that CLI's `adapter/super-cache` payload at
the CLI's documented skill path. Setup then copies it into the shared cache in
the same way as the standard provider files.

## Recommended replacement: one setup-owned monitor, registered lanes, and one real manager queue

The queue/outbox/hook portions of this replacement apply only to the explicitly
configured **managed** lane profile. The **plain** profile keeps the same required
monitor, controlled `lane.json` records, active-lanes index, process health checks,
terminal result validation, direct completion review, and resume path, but does
not create, inspect, or wait on a manager or worker queue. The monitor does not
invent an event to replace a facility the configuration deliberately disabled.

The right basic model is one persistent monitor process for the configured harness.
`operator_launch harness setup` starts it after loading the harness's fixed
`<harness-root>/harness-config.json`. It is not one scanner beside every
subagent and it is not started ad hoc by each epoch or lane.

One scanner per worker would duplicate work, can produce duplicate events, and can
die with the worker it is supposed to report. A single monitor stays outside all
worker worktrees. It is a harness-setup process, not a worker process. Its exact
PID-plus-creation identity is written under the configured runtime root. It remains
alive as epochs and lanes come and go, then stops only through the public harness
shutdown/reconfiguration route after all active epochs have been retired.

### 1. The fixed harness configuration and setup own the monitor

The persistent configuration proposed in
`harness-epoch-runtime-record-location.md` is the sole path authority. It lives at
the fixed location:

```text
<harness-root>/harness-config.json
```

It supplies the absolute ROOT project workspace and the genuinely optional feature
choices. The harness derives the shared runtime root as
`<root_workspace>/.harness-runtime/`. The active super-cache and persistent
monitor are mandatory facilities, so neither appears as a feature choice. For
example:

```json
{
  "root_workspace": "/project-workspace",
  "managed_coordination": "enabled"
}
```

When `operator_launch harness setup` runs, it resolves that known configuration
file itself, validates the project workspace and its derived contained runtime
root, creates the monitor-state folder if needed, and starts exactly one mandatory
monitor. It writes a durable monitor record such as:

```text
<runtime-root>/monitor/MONITOR.json
```

That record contains the config identity, monitor PID, process creation time, start
time, current health, `last_heartbeat_at` (refreshed each pass; the ROOT liveness
hook reads it for freshness), and its `stop_requested`/`STOPPED` state. A later setup must prove that this exact monitor is still
alive before reusing it; it must not trust a recycled PID or silently start a second
monitor. This setup route launches no provider and no worker worktree. It only starts
the configured shared monitor infrastructure.

### Minimal monitor lifecycle and crash recovery

The monitor is intentionally lightweight. Setup takes one short exclusive
`monitor-record` lock before reading or replacing `MONITOR.json`:

- If the record's exact PID-plus-creation identity is live, setup returns
  `SETUP_MONITOR_ALREADY_RUNNING` and starts nothing.
- If that exact identity is absent, setup removes the stale record, starts one
  fresh monitor, and writes the new identity.
- Ordinary setup never kills a live monitor. Two routes may deliberately stop a
  still-live monitor, each only after matching both PID and creation time: public
  shutdown's narrow exceptional-recovery route (which sets `stop_requested` under
  the monitor-record lock), and the ROOT monitor-liveness hook's hung-monitor path
  (master resolution R15), which stops a monitor that is alive but has stopped
  emitting heartbeats before starting a fresh one under the `monitor-record` lock.

There is no replay, supervisor, or elaborate post-crash recovery service. A fresh
monitor begins with a health check and scans the currently registered active lanes.
The monitor-record lock also prevents two starters — a setup command and the ROOT
monitor-liveness hook (R15), or two of either — from both deciding that no monitor
is live and double-starting.

### Monitor heartbeat and ROOT liveness watchdog

Because the monitor is the sole producer of ROOT events, a silently dead or hung
monitor would otherwise stop all delivery. Detection and recovery is managed-only
(master resolution R15 is authoritative). First, on each pass the monitor stamps
`last_heartbeat_at` in `MONITOR.json`; it writes no heartbeat event to the manager
queue. Second, a managed ROOT PostToolUse liveness
hook makes two checks at each ROOT tool boundary, both from the single small
`MONITOR.json` (never the growing queue): that the recorded monitor process (PID
plus creation time) is alive, and that `last_heartbeat_at` is within the last `X`
minutes. If either fails — dead or absent, or alive-but-stale (hung) — the hook
directs ROOT to start a fresh monitor through the same `monitor-start` route above,
stopping the hung process first. It leaves a monitor alone only when the record is
marked stopped (`stop_requested`/`STOPPED`) **and** the process is dead — a
completed deliberate stop; a dead record with no stop mark is a crash and a hung
record is restarted, while a stop mark with a still-live process is surfaced to
ROOT rather than double-started. A plain epoch has no queue and no ROOT hooks; there a stale monitor surfaces only through ROOT's own
`scan`/`watch` polling and recovery is manual.

The monitor reads the one active-epoch marker below the same configured runtime
root. Thus it learns about the epoch from:

```text
<runtime-root>/CURRENT_EPOCH.json
<runtime-root>/epochs/<epoch-id>/epoch-state.json
```

For a managed epoch it validates the marker against the header of the fixed
`<runtime-root>/manager/QUEUE.json`, then reads the active epoch's exact
`active-lanes.json` index. For a plain epoch it validates the marker's explicit
`lane_mode: "plain"` form and reads the same index without opening a queue. A
managed epoch-open command replaces the fixed queue with a fresh queue ID; a
plain epoch creates no queue. An epoch-retirement command marks the epoch closed
and clears the marker. The monitor ignores a missing or closed epoch.

### 2. Bootstrap prepares every lane; launch registers it as active

The neutral harness needs a real one-manifest public bootstrap route, modeled on the
frozen campaign runner's prepare-only `lane_bootstrap.py`. The external neutral
checkout does not currently have that layer. Bootstrap validates the lane inputs,
creates the worktree and `.agent-workspace/`, applies enabled preparation, and writes
one small, atomic lane record. It starts no provider. Its record location is not
supplied as an ad hoc caller argument; it is derived from `harness-config.json`, the
generated epoch ID, and the lane ID:

```text
<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/lane.json
```

It should contain the exact facts the monitor needs:

- lane ID and stable invocation/task ID;
- a readable task-card reference or task summary;
- provider and role;
- exact worktree path and `.agent-workspace` path;
- exact in-worktree controller-status, result, event-log, transcript, stderr,
  last-message, and evidence paths;
- for a managed lane only, exact `manager_notification_dir`,
  `manager_notify_command`, and worker-queue paths plus the shared run/queue
  identity; and
- after launch, the provider PID **and process creation time**.

Bootstrap first writes `lane.json` with state `PREPARED` and a fresh `run_id`.
The separate public launch route then starts the temporary controller, records that
controller's PID-plus-creation identity, and only then atomically adds exactly this
entry to:

```text
<runtime-root>/epochs/<epoch-id>/active-lanes.json
```

```json
{
  "lane_id": "lane-001",
  "run_id": "run-<opaque-id>",
  "lane_record_path": "<runtime-root>/epochs/<epoch-id>/lanes/lane-001/lane.json"
}
```

The controller updates the lane record with the provider PID-plus-creation identity
when it starts the provider. It writes its changing status and chronological event
history to the declared `.agent-workspace/` paths in the worktree. PID alone is not
enough because the operating system can later assign that same number to an unrelated process.

After owned-process cleanup is proved, retirement marks the lane record retired and
removes that exact lane/run entry from `active-lanes.json`. If a controller dies
unexpectedly, the entry remains active until the monitor and ROOT have classified it;
it must not disappear simply because its controller process exited. The harness does
not require a retired worktree to remain on disk or run a cleanup route before later
work: operators may remove old worktrees themselves. No later setup, monitor start,
epoch open, or new-lane bootstrap scans or validates those retired paths.

The monitor rereads the active epoch's `active-lanes.json` on every pass. It opens
only the `lane.json` paths listed in that file, then reads only the exact in-worktree
records those lane files declare. A newly launched lane is therefore visible on the
next pass without restarting the monitor. This is more precise than discovering
arbitrary folders through a broad `worktrees/*` glob and does not accidentally inspect
an unrelated worktree. The index is derived: if it is missing or malformed, health
reconciliation rebuilds it from this epoch's controlled lane-record directory; a
  `lane.json` record remains authoritative. The monitor treats a missing worktree
  as actionable only for an entry that is currently active; it never probes a
  retired lane just because its record still names an old worktree.

### 3. The monitor checks only registered lanes

The monitor performs the useful parts of today's scan: reads the registered active
lane's declared in-worktree records, takes a fresh process snapshot, and checks the
exact expected process identity. It does not search all `lanes/` records or all
worktrees. It should create a condition only from facts it can point to.

It does **not** use a deduplication key, condition generation, or a search through
`QUEUE.json` to decide whether to write another event. Each active external
`lane.json` stores one plain value named `last_reported_actionable_status`. The
monitor changes only that field, under the same short lane-record lock used by the
controller; it reads the latest record, updates that one field, and atomically
replaces the file. The controller remains authoritative for every other field.
The lock covers only this one reread-and-replace operation and is released in a
`finally` path as soon as that writer finishes; a crashed controller or monitor
loses its operating-system lock when its process handle closes.

On each pass, the monitor derives the lane's current actionable status from its
declared controller records and compares it with that saved value:

- same status: write nothing;
- changed from no actionable status to an actionable status: in managed mode,
  write one new timestamped ROOT event and save that status; in plain mode, save
  only the status in the lane record;
- changed from one actionable status to a different actionable status: in managed
  mode, write one new timestamped ROOT event and replace the saved status; in
  plain mode, replace only the saved status; and
- changed back to no actionable status: clear the saved value and write no event.

If the same problem later truly recurs, it first clears and then becomes
actionable again, so it is a status change and receives a new event. This is the
only suppression rule. A timestamp records when an event was written; it is not
a comparison key.

This is deliberately a lightweight, non-mission-critical recovery policy. In
managed mode a crash between a queue write and the later lane-status update may
result in a repeated event on a later monitor pass; a malformed in-flight record
may be discarded by health recovery. Plain mode has no such queue publication.
Neither mode promises exactly-once event publication or replays every lost
in-flight notification.

### Managed worker-requested ROOT help uses one declared outbox

Each active **managed** `lane.json` must declare these three deterministic
worktree paths. A plain lane has none:

```text
<worktree>/.agent-workspace/manager-notifications/
<worktree>/.agent-workspace/processed-notifications/
<worktree>/.agent-workspace/manager-notify.py
```

Bootstrap creates both empty folders and the helper before the provider starts. A
worker that needs a ROOT decision, permission, missing input, or recovery action
runs its declared helper, for example:

```text
python .agent-workspace/manager-notify.py \
  --severity blocking \
  --summary "Choose the board revision before I continue" \
  --evidence logs/probe-output.txt
```

The helper validates its arguments and creates one immutable JSON file in the
declared folder. It writes a temporary file first, then renames it to a fresh
notification ID. The file contains that ID, the lane ID, current `run_id`,
severity, summary, creation time, and optional evidence paths. It cannot edit
`lane.json`, locks, or the shared queue.

On each monitor pass, after resolving the active lane from `active-lanes.json`,
the monitor reads only unprocessed files in that lane's declared notification
folder. It validates that the lane ID and `run_id` match the active record and
that evidence paths remain inside that worktree. For a valid file, it creates one
`target: ROOT` event and then moves the outbox file into that lane's
declared `processed-notifications/` folder. Later passes read only the original
inbox, not the processed folder. This is ordinary one-time file consumption, not
a dedup key or a search for a matching queue event. A malformed or mismatched file
becomes a separate ROOT diagnostic with its exact path, then is moved to the
processed folder with its original bytes preserved; it is never silently treated
as a valid escalation.

The monitor scans this worktree folder. ROOT's idle `watch --until-actionable`
does **not** scan it again: it returns for the resulting ROOT-targeted queue event.
That gives ROOT one notification source and prevents the same worker request from
producing two competing alerts.

### Managed ROOT-to-worker instructions use a different lane-local queue

Worker-to-ROOT help and ROOT-to-worker work are opposite directions. They must not
share the epoch manager queue or a worker's escalation outbox.

Managed bootstrap creates this additional file and records its exact path in
`lane.json`; plain bootstrap does not:

```text
<worktree>/.agent-workspace/QUEUE.json
```

ROOT adds an assignment only through the public command installed in ROOT's
`send-lane-notification` skill:

```text
operator_launch send-lane-notification --lane-id <lane-id> --prompt "<assignment>"
```

The command resolves `<lane-id>` through `active-lanes.json`, opens its declared
`lane.json`, and checks that the provider state is `RUNNING` and the recorded
PID-plus-creation identity is still alive. A lane that is missing, retired, exited,
or has a mismatched process identity returns `LANE_NOT_RUNNING`; the command creates
no message and tells ROOT to resume that lane instead. It never guesses a worktree
or leaves an assignment in a dead lane's folder.

For a live lane, the command atomically adds one `PENDING` assignment to exactly
that `.agent-workspace/QUEUE.json`. The item contains its ID, lane ID, current
`run_id`, ROOT's prompt, time, state, and transition history. This file is not
read by the persistent monitor or ROOT's `watch --until-actionable`; those use the
epoch manager queue only.

The selected provider adapter installs a PostToolUse hook and a Stop hook for this
one local file. PostToolUse gives the worker a direct safe-boundary reminder that an
incoming ROOT assignment is waiting; it does not change the assignment state. Stop
rejects normal provider exit while an assignment is `PENDING` or `ACKNOWLEDGED`.
The worker uses a bootstrap-created local helper to mark it `ACKNOWLEDGED`, then
`COMPLETE`, or `BLOCKED` with a reason. `BLOCKED` also uses the existing worker
outbox so ROOT gets a real manager event; it is terminal for the worker queue and
permits the worker to stop. Thus a worker is never blocked by ROOT's unrelated
manager work, but it cannot silently finish while its own unaddressed ROOT work
remains.

### The managed escalation instruction is mechanically added to prompts

The managed lane controller's provider-launch code appends a generated escalation
block after every managed worker task prompt it constructs. The worker cannot lose
the instruction because a task card omitted it. The block includes the exact helper
command for the current worktree and says:

- use it when work needs a ROOT decision, authority, missing input, or help;
- include the decision/action ROOT needs and relevant local evidence;
- do not rely on a final chat answer as a notification; and
- after a blocking escalation, stop at a safe boundary rather than inventing the
  missing decision.

The managed orchestrator's generated initial prompt receives the matching ROOT block. It
states that a worker escalation becomes a ROOT-targeted manager-queue event, and
that ROOT must inspect, resolve, and acknowledge its top-level event ID only after
ROOT completes its current task. These are controller-generated prompt fragments,
not optional wording copied into task cards or `AGENTS.md`.

The managed active super-cache payload contains `.codex`, `.claude`, and `.qwen`
`manager-notify` skills that repeat the same worker instruction after the cache overlay is
copied. Those cache-owned skills reinforce the mandatory generated prompt block;
they do not replace it. A plain lane receives no escalation block, helper, or
manager-notify skill. Provider adapters remain free to add separate hooks,
bindings, or provider-specific instructions, but they do not modify the
cache-owned skill files.

### 4. A real finding is admitted to the queue

For a new actionable condition, the monitor calls the existing router admission
route. The event should contain the actual useful context, not merely “something
happened”:

```text
target: ROOT
lane: D30-executor-2
task: build and flash the NRF-A contract probe
provider: Codex
expected process: PID 18420, created 2026-08-23T14:03:12Z
finding: provider exited; no valid RESULT.json was produced
evidence: <exact controller status and result paths>
```

Each event receives its normal unique event ID so ROOT can acknowledge the exact
item it read, plus a creation time for the audit trail. Neither value is used as a
deduplication key. The saved `last_reported_actionable_status` is what stops a
monitor loop from repeatedly reporting one unchanged condition.

The monitor's admission policy must include the lane outcomes the present watcher
silently filters out: provider/controller exit, a contradictory status/transcript,
missing or invalid result, cleanup proof failure, an `orphaned_lease` (an
exclusive-resource lease whose owning lane's
run is dead or retired — see resolution R14 in `harness_single.md`; the monitor
detects it but never auto-reclaims it), and — per resolution R4 in
`harness_single.md` — a structurally valid result awaiting review
(`review_pending`). The monitor is the sole producer of ROOT events, so
`review_pending` is promoted as an ordinary actionable status change like every
other item in this set; the controller only records the status. It should not
reuse the present hardcoded `--until-actionable` list.

### 5. Make the queue the one manager-notification source

The queue format needs an explicit recipient/role field. At minimum it must support
`ROOT` and an exact worker/lane target. ROOT-only diagnostics produced by the monitor
must not be visible as work for an executor. A worker assignment must not be visible
as every worker's assignment.

With that routing added, every condition that requires ROOT action goes through the
same queue: lane failures, invalid results, permission requests, external blockers,
and worker-created escalation files. ROOT-to-worker assignments instead go through
the selected worker's distinct local queue above. The existing
PostToolUse behavior becomes useful:
when ROOT is working, ROOT's own installed static provider hook checks the fixed manager
queue after every tool boundary. While one or more ROOT-targeted events remain
unacknowledged, it returns the same short reminder: finish the current ROOT task,
then use the `acknowledge-manager-notification` skill. The hook does not open,
acknowledge, or resolve an event itself. A prior delivery receipt never suppresses
this reminder; only explicit acknowledgement does.

This requires real static ROOT adapter installation plus generic active-epoch
routing: setup installs all shipped ROOT payloads in the project workspace, and
their native hooks open the fixed manager queue and validate it against
`CURRENT_EPOCH.json`. The external harness does not yet create this v2
materialization automatically.

### ROOT must explicitly own and close every event

Delivery is not acknowledgement. A PostToolUse hook records that ROOT was reminded;
`watch --until-actionable` returning records only that an event is waiting. Neither
action changes the event's manager state.

The proposed queue has one authoritative file:

```text
<runtime-root>/manager/QUEUE.json
```

It contains a header with the active `epoch_id` and freshly generated `queue_id`,
plus every event and its current state/transition history. ROOT changes state only
through the public manager-event route, always using the top-level `event_id`:

```text
PENDING       event was admitted; ROOT has not opened it
ACKNOWLEDGED  ROOT opened it after completing its current ROOT task
COMPLETE      ROOT addressed it
BLOCKED       ROOT cannot address it; reason, owner, and next action are recorded
```

`PENDING` is the event's one authoritative “unacknowledged” value. The
PostToolUse hook tests for ROOT-targeted events in that state. Do not add a
second `unacknowledged` boolean beside it: two acknowledgement representations
would be two pieces of state that can disagree. `ACKNOWLEDGED` means ROOT used
the public command after reading that event.

The public acknowledgement route is deliberately small:

```text
operator_launch manager acknowledge --event-id <top-level-event-id>
```

ROOT first reads the queue. For each event ROOT actually read, the shipped
`acknowledge-manager-notification` skill directs it to call this command with
that one top-level ID. The command opens the fixed manager queue, takes the short
queue-file lock, verifies the queue header matches `CURRENT_EPOCH.json`, verifies
the event belongs to ROOT, and atomically changes
that event from `PENDING` to `ACKNOWLEDGED`. It never accepts a queue path from
ROOT, never acknowledges a nested signal ID, and never marks an event complete.
An already-acknowledged ID returns `ALREADY_ACKNOWLEDGED` without a second write.
Unknown or non-ROOT-targeted IDs fail without changing the queue.

After ROOT has actually handled an acknowledged ordinary notification, the new
`close-manager-notification` skill directs it to run:

```text
operator_launch manager close --event-id <top-level-event-id> \
  --outcome COMPLETE|BLOCKED --summary "<what ROOT did or needs>"
```

The command accepts only an `ACKNOWLEDGED` ROOT event in the fixed manager queue,
takes the same queue lock and epoch/queue-ID checks, then atomically changes it to
`COMPLETE` or `BLOCKED` and appends the summary to that event's history. A closed
event returns `MANAGER_CLOSE_ALREADY_CLOSED`; a `PENDING`, unknown, or non-ROOT
event is rejected without a write.
It does not launch or resume a lane. The completion-review command closes its own
completion event automatically; all other ordinary ROOT notifications use this
public close route.

Every queue writerâ€”the monitor admitting an event, a ROOT acknowledgement or
resolution, and a PostToolUse delivery receiptâ€”takes the same short queue-file
lock, confirms its expected `epoch_id`/`queue_id` match both the queue header and
`CURRENT_EPOCH.json`, then reads `QUEUE.json`, changes the relevant event in
memory, writes a temporary replacement, and atomically replaces `QUEUE.json`. The
delivery receipt adds a delivery-history entry but never changes the event's manager
state. There is no `STATE.json`, `QUEUE.jsonl`, coordinator, or second authoritative
state store to coordinate.

The atomic replacement makes a normal crash leave either the old complete queue or
the new complete queue, not a half-written authoritative `QUEUE.json`. On monitor
startup and before normal parsing, a small health check validates every required
record. It deletes stale malformed temporary files. If the authoritative queue itself
is malformed despite atomic publication (for example, manual corruption), recovery
removes the broken record and, under the queue lock, stages a new empty queue with a
fresh `queue_id` for the still-active epoch before atomically updating
`CURRENT_EPOCH.json`. Writers carrying the old queue ID return `QUEUE_REPLACED` and
write nothing. Losing pending events is an accepted failure mode for this
non-mission-critical harness; recovery never claims they were handled or acknowledged.

One narrow exception prevents a lost queue from stranding a valid finished lane:
completion-review recovery may reissue a new `COMPLETION_REVIEW_REQUIRED` event
from that lane's valid terminal record when no complete review/acceptance chain or
open matching review event remains. It records that replacement as recovery
evidence and does not claim that the lost original event was handled. The full
rule is in `harness-completion-review-acceptance-mechanism.md`.

`BLOCKED` is an explicit finished manager decision, not an ignored item: it must
name the external dependency or person that must unblock it and it prevents a
campaign PASS.

ROOT works one manager task at a time. While a current ROOT task is in progress,
the PostToolUse hook keeps returning its short reminder while events remain
unacknowledged, but explicitly tells ROOT not to open the queue yet. After that
current task is complete, ROOT reads the queue and uses the acknowledgement skill
for the next selected event. ROOT then finishes it as `COMPLETE` or `BLOCKED`
before taking another manager task. The ROOT-only Stop gate refuses a normal stop
while any ROOT event is `PENDING` or `ACKNOWLEDGED`; executor workers are never
subject to this gate.

### 6. Make the existing watch command profile-aware when ROOT is idle

Keep the existing public command name. In managed mode it replaces the current
disconnected diagnostic-only behavior with a queue wait:

```text
watch --until-actionable
```

It reads ROOT-targeted items from the same durable queue and returns only when a new
actionable event exists. The background monitor continues to scan lanes and adds
such events while ROOT waits. ROOT handles and acknowledges the top-level event ID,
then starts the next idle watch when it is ready to wait again.

This command remains a foreground wait, which is fine because ROOT uses it only when
idle. It no longer pretends to watch a different diagnostic system while the queue
holds the real manager work.

In plain mode the same command waits only for a changed actionable status in the
controlled active-lane records and returns that lane/status directly. It does not
open a manager queue or require acknowledgement. ROOT can inspect the lane or use
the direct completion-review/resume command as appropriate. This keeps ordinary
idle monitoring useful without quietly reintroducing a queue into plain mode.

This is an active ROOT responsibility, not a notification mechanism: for a
non-managed provider whose CLI cannot use the hook/queue route, nothing wakes
ROOT after the lane changes. ROOT must deliberately run `scan --no-write` when it
returns to management work and `watch --until-actionable` when it is deliberately
idle. The returned plain lane status is the prompt to inspect, review, resume, or
otherwise act; it is not a manager event and needs no acknowledgement.

Harness setup installs both `manager-notification-watch` and
`acknowledge-manager-notification` skills in `.codex`, `.claude`, and `.qwen` at
the configured ROOT workspace. The first tells ROOT to run one `scan --no-write`
before idling, then this command while idle; it follows the profile-aware behavior
above. The second applies only to managed queue events. Together they are the
managed ROOT-side counterpart to the executor cache's `manager-notify` skill.

## Deliberate boundaries

- The monitor is ordinary provider-agnostic Python, started by harness setup. It
  does not require a Codex, Claude, or Qwen hook to detect a dead lane.
- Provider-native PostToolUse hooks are only the non-blocking reminder while an
  active ROOT is doing tool work. They do not replace the monitor, create events,
  or acknowledge events; they keep reminding ROOT while an event is
  unacknowledged and tell ROOT to finish its current task before using the shipped
  acknowledgement skill.
- Workers do not need their own status scanners and do not write the shared queue.
  They use the one bootstrap-created `manager-notify.py` helper when they need ROOT
  help; the monitor turns the resulting outbox file into the targeted queue event.
  Ordinary lane health still comes from the one monitor.
- ROOT-to-worker work does not go through that manager queue. The public
  `send-lane-notification`
  command writes only the selected live lane's local `QUEUE.json`; its PostToolUse
  and Stop hooks read only that file. The monitor does not duplicate or relay it.
- This does not claim magical wake-up while ROOT is actively reasoning. No supported
  CLI hook injects a queue event into an ongoing model turn. The reminder occurs at
  the next tool boundary; the idle watch handles the idle case.

## Observable acceptance criteria

The design is complete only if these outcomes can be shown with a disposable
host-only lane:

1. Launching a new lane writes its registry record; the existing monitor discovers
   it without restart.
2. In an uninterrupted run, a simulated provider exit produces one ROOT-targeted
   queue event with the lane, task, PID-plus-creation identity, finding, and
   evidence paths.
3. Repeated uninterrupted monitor passes do not duplicate that event while it
   remains open. A crash between the queue and lane-status writes may produce a
   repeated event after recovery; this is accepted and visibly logged.
4. ROOT's idle `watch --until-actionable` returns for that queue event; the old
   diagnostic-only behavior is not used to receive it.
5. A worker bound to another queue/recipient does not see ROOT's lane-failure event.
6. A ROOT PostToolUse hook returns a reminder after every tool boundary while a
   ROOT event remains unacknowledged. A prior delivery receipt does not suppress it.
7. A disposable worker runs its generated `manager-notify.py` command. The monitor
creates exactly one ROOT-targeted event containing its lane, `run_id`, summary,
   and source file; ROOT's idle watch returns for that event.
8. Repeating monitor passes does not duplicate the worker escalation, and a malformed
   outbox file is reported as a diagnostic rather than accepted as a request.
9. Retiring an epoch removes its active lane records and clears the current-epoch
   marker, but does not stop the configured monitor that may serve later epochs.
10. The public harness shutdown/reconfiguration route stops the monitor and verifies
   its exact PID-plus-creation identity before considering the shared harness
   infrastructure closed.
11. A PostToolUse delivery receipt and a `watch --until-actionable` return both leave
    the event `PENDING`; neither is counted as ROOT acknowledgement.
12. After ROOT completes its current task, the public
    `operator_launch manager acknowledge --event-id <top-level-event-id>` command
    updates only the inspected event in `QUEUE.json` to `ACKNOWLEDGED` and adds its
    history entry. An explicit `COMPLETE` or documented `BLOCKED` update closes it
    in that same file.
13. ROOT cannot stop normally while a ROOT-targeted event remains `PENDING` or
    `ACKNOWLEDGED`; the corresponding executor worker can stop after publishing its
    result and is not blocked by ROOT's queue.
14. ROOT can add one assignment through `send-lane-notification` only while the selected exact
    provider process is live. The assignment appears only in that lane's declared
    local `QUEUE.json`; it is absent from ROOT's manager queue and every other lane.
15. That lane's PostToolUse hook reports the local assignment without changing its
    state. Its Stop hook rejects exit while the assignment is `PENDING` or
    `ACKNOWLEDGED`, then permits exit after `COMPLETE` or a documented `BLOCKED`.
16. A queue attempt after provider exit returns `LANE_NOT_RUNNING`, writes nothing,
    and names the public resume route; it never starts a provider itself.
17. A stale or malformed temporary record is removed by the startup health check.
    A malformed authoritative queue is removed and reinitialized empty with a fresh
    queue ID in the same active epoch; the harness never claims its lost pending
    events were handled.
