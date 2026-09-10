# Harness defect: the neutral notification queue has no ROOT/worker roles

Observed: 2026-08-23.

> **Status: historical diagnosis of the old role-less candidate protocol.**
> Its ManagerEventRouter, registration, coordinator, and JSONL details are
> evidence of what v2 replaces, not v2 runtime machinery. The current target is
> governed by the master planning document and the queue/adapter contracts.

## Scope

This document describes only the pointed-at neutral harness:

```text
<root-workspace>/<harness-root>
```

It does not describe the frozen firmware campaign runner, its
`lane_bootstrap.py`, its campaign manifest, or its hardware rules.

## Short answer

The neutral harness has a real filesystem queue and real provider hooks, but
it does not implement a ROOT/worker messaging protocol. It implements this
smaller, generic mechanism instead:

```text
one provider project is bound to one queue folder
    -> a notification is manually added to that folder
    -> that same provider project's later hook sees it
    -> the hook emits a generic "something is queued" notice
    -> the event remains pending until code explicitly acknowledges it
```

The queue has no `recipient`, `sender`, `ROOT`, or `worker` field. A binding
does not contain a role. Therefore the code cannot tell whether a pending event
belongs to the manager, a particular worker, or the same worker that wrote it.

The resulting design is genuinely the stupidest thing this review has
encountered: the harness has a Stop gate that operates on an unaddressed shared
queue while it has no automatic way to install the corresponding ROOT hooks.

## What the external harness actually does

### 1. Binding a provider project to a queue

The caller first installs a provider adapter into a project folder. The
external harness has separate installers for Codex, Claude, and Qwen. The
installer writes provider-specific hook files and configuration under that
project folder.

The caller then binds that project to a `ManagerEventRouter` queue. For Codex,
the binding is written under the project as:

```text
<project>/.codex/orchestrator-harness-binding.json
```

The binding contains a queue folder and labels such as `run_id`, `queue_id`,
`manager_session_id`, `manager_thread_id`, `registration_id`, and
`registration_generation`. It also contains a path for that binding's delivery
coordinator state.

Those labels prove that the project and queue agree on one registration. They
do not say who the recipient is. There is no field equivalent to:

```json
{ "role": "root" }
```

or:

```json
{ "recipient_lane": "worker-a" }
```

There is also no code that materializes all static ROOT payloads in the actual
project workspace and publishes one generic active-epoch pointer. Installing
worker projects does not install the ROOT project files or tell a ROOT hook which
manager queue is current.

### 2. Creating a notification

The PostToolUse hook does not create notifications. A caller must explicitly
call the external harness's `DeliveryCoordinator.admit_notification(...)` or
the lower-level router admission API.

That call appends one pending `MANAGER_SIGNAL` event to:

```text
<queue>/QUEUE.jsonl
```

and updates the queue state/wake files. The queue folder also contains:

```text
REGISTRATION.json
STATE.json
WAKE.json
DELIVERY.jsonl
```

There is no automatic rule such as "ROOT changed the plan, therefore create a
worker notification" or "worker finished, therefore create a ROOT
notification." A program has to make the admission call.

### 3. What the provider PostToolUse hook does

For Codex, the installed `PostToolUse` hook runs after every matching tool use.
It starts a short Python process in the bound project. That process:

1. reads that project's binding JSON;
2. opens the queue folder named in it;
3. reads **all** currently pending events in that queue;
4. creates a small notice containing only a count, highest severity, and other
   queue metadata; and
5. returns a generic wake message through the provider hook and appends a
   transport receipt to `DELIVERY.jsonl`.

The generic Codex message says that a new assignment is queued and tells the
agent not to interrupt its current directive. It intentionally contains no
event ID, payload, or assignment text.

`DELIVERED` means only that this hook emitted that generic provider notice. It
does **not** mean that the real event was shown, handled, acknowledged, or
removed. The event stays pending in `QUEUE.jsonl`.

Claude and Qwen have provider-specific hook files, but use the same basic
pattern: an installed hook reads its project binding, sees pending events in
that binding's queue, and records a delivery attempt. Qwen additionally has a
provider-native notification hook.

### 4. What the provider Stop hook does

The installed Stop hook starts another short process. It reads the same project
binding and the same queue. If the queue has any `OPEN` notification item, the
hook rejects stopping. In the Codex path, it asks Codex to continue.

The current external code has no branch like this:

```text
if bound_project_is_ROOT:
    enforce pending-notification Stop gate
else:
    allow worker to stop
```

It applies the same pending-event Stop decision to every project that receives
the installed adapter and binding.

The hook does not acknowledge the event. A separate caller must invoke the
coordinator/router acknowledgement method with the event ID. Only that explicit
acknowledgement removes the event from the pending queue.

## The four actual problems

### 1. ROOT does not automatically receive PostToolUse notification handling

The external harness has the capability to install the Codex, Claude, or Qwen
adapter in a ROOT project. It does not automatically materialize all static
ROOT payloads in the actual project workspace, publish generic active-epoch
routing, or confirm that ROOT's CLI discovers those hook settings.

Therefore a worker-only setup can have several worker hooks checking queues
while ROOT has no hook at all. There is no automatic ROOT queue check at a tool
boundary.

### 2. The worker Stop gate is not role-safe

The Stop hook is physically running in the session it may block. That part is
not mysterious. The defect is that it blocks a worker based on any pending
event in whichever queue the worker was bound to.

Under the required ownership rule, workers may publish their result/event and
then finish. Only ROOT must be prevented from ending while ROOT's unresolved
management work remains. The current generic external installer cannot express
that rule, because it has no manager/worker routing role in either the queue
context or the Stop
decision.

### 3. There is no automatic ROOT-only Stop gate

The external harness supplies a generic Stop-hook implementation, not a
ROOT-only one. It will run for ROOT only if setup first installs the static
ROOT payload in the project workspace and its native wrapper can read the
active-epoch pointer.

So the capability exists, but the needed setup/ownership rule does not. The
current code does not guarantee the desired result:

```text
ROOT has unresolved notifications -> ROOT cannot stop
worker has unresolved ROOT notifications -> worker may still stop
```

### 4. The queue is not a TX/RX protocol and has no addresses

`QUEUE.jsonl` is one list of pending events. It is not split into an outgoing
side and an incoming side. A provider binding merely says, "read this whole
queue." `notice_for_wake()` treats every pending event in that folder as a
reason to create a notice.

If ROOT and two workers share one queue folder, all three bindings see the same
pending list. If worker-side code is given that same router/binding and calls
`admit_notification(...)`, the worker has added an event to the same list its
own next PostToolUse hook will read. The normal PostToolUse hook does not do
that admission itself, but the queue design permits the self-notification
mistake.

This is not a one-way ROOT-to-worker inbox and it is not a one-way
worker-to-ROOT results channel. It is an unaddressed shared ledger.

## Concrete consequence

With one shared queue, the following is possible:

```text
ROOT or worker-side code adds event X to QUEUE.jsonl
    -> Worker A uses a tool
    -> Worker A's PostToolUse hook sees event X and emits its generic wake
    -> Worker B uses a tool
    -> Worker B's PostToolUse hook also sees event X and emits its generic wake
    -> either worker tries to stop
    -> its Stop hook sees event X and may keep that worker alive
    -> ROOT may have no hook and no automatic notice at all
```

No queue record in that sequence proves event X was for Worker A, Worker B, or
ROOT. The only thing that selected the recipients was the erroneous choice to
bind all of them to the same folder.

## Minimum correction required

This requires a real harness change, not a campaign prompt reminder.

1. Add explicit queue roles: `manager` or `worker`.
2. During setup, install every shipped standard ROOT adapter payload in the
   project workspace. Each static native ROOT hook wrapper opens the fixed
   runtime manager queue and validates its epoch/queue IDs against
   `CURRENT_EPOCH.json`; it does not bind a particular ROOT CLI, model, or
   session.
3. Install/enforce the pending-notification Stop gate for that generic ROOT
   **manager queue** only. A worker must never be stopped by unresolved ROOT
   manager work.
4. Give each worker its own separate incoming assignment queue. To notify Worker A,
   ROOT explicitly adds an assignment to Worker A's queue; it does not add it to
   ROOT's manager queue or a shared queue. A Worker A Stop hook may block Worker A
   only on unresolved assignments in that one local queue.
5. Keep acknowledgement explicit and target the event in the recipient's queue.
   A transport `DELIVERED` receipt must continue to be only delivery evidence,
   never an acknowledgement.

The existing provider-native hook facilities are sufficient for steps 2 and 3:
the missing work is role-aware installation/binding and addressed queue layout.
No persistent watcher, scheduler, relay, or invented background service is
required for this correction.

## Validation required after a repair

1. Bind ROOT and Worker A to different queue folders. Add one event to ROOT's
   queue; confirm only ROOT's next provider hook sees a notice.
2. Add one event to Worker A's queue; confirm only Worker A's next provider
   hook sees a notice.
3. Confirm a Worker A Stop hook allows Worker A to exit even when ROOT's queue
   has pending events, but blocks Worker A when **Worker A's own** incoming queue
   has a `PENDING` or `ACKNOWLEDGED` assignment.
4. Confirm ROOT's Stop hook blocks ROOT while ROOT's queue has an `OPEN` event,
   then permits stop after the explicit acknowledgement.
5. Confirm a `DELIVERED` record leaves the event pending until acknowledgement.
6. Repeat the binding/hook proof for Codex, Claude, and Qwen; their provider
   hook syntax differs, but the queue ownership result must be identical.

## Required distinction: ROOT manager queue versus worker incoming queue

The earlier correction remains correct, but it must be read precisely. It is wrong
to stop an executor because the shared manager queue has work for ROOT. It is valid
to stop an executor that is trying to finish while ROOT has given **that executor**
an unfinished assignment.

The corrected design therefore has two different queue files:

```text
<runtime-root>/manager/QUEUE.json
    ROOT's manager queue: monitor findings and worker-to-ROOT requests.
    Only ROOT's static provider hook wrappers and ROOT's Stop gate use it.

<worker-worktree>/.agent-workspace/QUEUE.json
    One worker's incoming ROOT assignments.
    Only that worker's PostToolUse and Stop hooks use it.
```

They are not two views of one file. An event in one must never make the other hook
fire or block the other process.

### How ROOT sends a worker assignment

Harness setup installs a ROOT-provider skill that directs ROOT to the public route:

```text
operator_launch send-lane-notification --lane-id <lane-id> --prompt "<assignment>"
```

That command first reads the active-lane index and the selected lane record. It
requires the lane to be `RUNNING` and verifies that the recorded provider
PID-plus-creation identity is still the same live process. If either check fails,
it returns `LANE_NOT_RUNNING`, writes no queue item, and tells ROOT to resume the
lane through the public resume route. It must not create a stranded assignment for
a previous run or restart a lane on its own.

For a live lane, the command takes a short lock on that lane's declared
`.agent-workspace/QUEUE.json`, reads it, adds an item with a fresh assignment ID,
the lane ID and current `run_id`, ROOT's prompt, `PENDING` state, and a history
entry, then atomically replaces the file. It never edits the epoch manager queue.

### What the worker hooks do

Bootstrap creates the empty lane queue and its local `lane-queue.py` resolution
helper before provider launch. The adapter installs these provider-native behaviors
for the worker's own queue only:

1. **PostToolUse:** after a matching tool call, read that lane queue. If one or more
   assignments are `PENDING` or `ACKNOWLEDGED`, return a direct notice identifying
   the assignment ID and telling the worker to finish its current safe operation,
   then inspect and resolve the assignment. It records delivery history but does
   not acknowledge or complete the assignment itself.
2. **Stop:** before the provider finishes, read that same queue. Reject normal stop
   while any assignment is `PENDING` or `ACKNOWLEDGED`. It does not read ROOT's
   queue, another lane's queue, or general manager events.

The worker uses `lane-queue.py` to move an assignment through:

```text
PENDING -> ACKNOWLEDGED -> COMPLETE
                         -> BLOCKED (reason required)
```

`COMPLETE` and a documented `BLOCKED` state permit the worker to stop. A worker
that uses `BLOCKED` must also call its existing `manager-notify.py` helper so the
monitor creates a ROOT event explaining why resumption or a decision is needed.
The worker never hand-edits either JSON queue.

This is a real harness repair. It is not present in the pointed neutral checkout or
the frozen campaign runner today, and it must be proven separately for Codex, Claude,
and Qwen. Required proof: a live lane receives an assignment; its next safe-boundary
hook notices it; Stop is rejected while it is unresolved; `COMPLETE` allows exit;
and a dead lane returns `LANE_NOT_RUNNING` without a new queue record.

## External-harness source locations

- Queue admission and pending-notice construction:
  `orchestrator_harness/host_adapters.py:835-918` and `1205-1249`.
- Delivery receipt recording without acknowledgement:
  `orchestrator_harness/host_adapters.py:954-1060`.
- Codex binding and installed hook route:
  `orchestrator_harness/codex_adapter.py:1745-1808` and `1914-2041`.
- Claude and Qwen installed hook routes:
  `orchestrator_harness/claude_installer.py:876-955` and
  `orchestrator_harness/qwen_installer.py:570-620`.

## Additional required correction: adapters install every real provider hook

This is a recommendation for the neutral harness. It is not implemented in the
pointed checkout today.

The word **hook** must mean a real hook declaration that the selected provider
CLI will execute. A file merely copied into a worktree is not a hook. The
selected Codex, Claude Code, or Qwen Code adapter must write that provider's
actual hook configuration and any small provider-specific wrapper it needs.

The shared harness supplies the Python programs that do the provider-neutral
work. The adapter supplies the one provider-specific step that makes the CLI
call those programs.

For example, the normal executor Stop check should work as follows:

1. The shared cache places this ordinary Python program in every worker
   worktree:

   ```text
   <worktree>/.agent-workspace/result-stop-check.py
   ```

2. The selected provider adapter writes that provider's native Stop-hook
   declaration. Its declared command calls that exact script.

3. `result-stop-check.py` reads the existing lane invocation/task identity and
   `<worktree>/RESULT.json`. It checks that the result exists, is JSON, has the
   required shape, and names the exact lane/card/invocation that launched the
   worker.

4. A valid result makes the provider hook allow the provider to stop. A missing
   or invalid result makes the adapter's hook response reject Stop and prints
   the exact validation error to the still-running worker. The worker fixes
   `RESULT.json` and tries to finish again.

The script does **not** accept the task. It checks only the worker-owned result
file. ROOT still reviews and accepts or rejects a valid result later.

The same ownership rule applies to every hook discussed in this document:

| Hook behavior | Shared Python/helper code | Actual provider hook declaration |
| --- | --- | --- |
| Worker receives a local assignment after a tool call | Reads that worker's local `QUEUE.json` | Selected worker adapter writes PostToolUse |
| Worker cannot exit with unfinished local assignments | Reads that worker's local `QUEUE.json` | Selected worker adapter writes Stop |
| Worker cannot exit with a missing or invalid `RESULT.json` | Runs `result-stop-check.py` | Selected worker adapter writes Stop |
| ROOT sees a manager-queue notice after a tool call | Generic dispatcher opens the fixed manager `QUEUE.json` and validates `CURRENT_EPOCH.json` | Every installed ROOT adapter writes native PostToolUse configuration |
| ROOT cannot exit with unresolved manager work | Generic dispatcher opens the fixed manager `QUEUE.json` and validates `CURRENT_EPOCH.json` | Every installed ROOT adapter writes native Stop configuration |

No generic cache copy may invent, merge, or activate a provider hook by itself.
The adapter is the sole owner of provider hook configuration. This avoids one
piece of cache content and a different adapter both trying to modify the same
provider hook file.

## Required super-cache layout and automatic materialization

The super-cache should be required, not optional. It contains product-owned
worker material that the harness depends on: shared helpers, the result Stop
checker, ROOT/worker skills, and the shipped provider adapter payloads. A lane
must not be able to launch with the cache absent or disabled.

The product should ship this read-only source tree under the harness root.
Setup makes a verified active working copy at
`<runtime-root>/super-cache/`; bootstrap reads only that runtime copy:

```text
<harness-root>/super-cache/  -- setup -->  <runtime-root>/super-cache/

<runtime-root>/super-cache/
  workspace/                         # copied into every prepared worktree
    .agent-workspace/
      result-stop-check.py
      lane-queue.py
      manager-notify.py
    .codex/skills/...
    .claude/skills/...
    .qwen/skills/...
  adapter-payloads/
    codex/root/                      # copied only for a Codex lane
      .codex/...
    claude-code/root/                # copied only for a Claude lane
      .claude/...
    qwen-code/root/                  # copied only for a Qwen lane
      .qwen/...
  custom/                            # optional caller-added shared content
```

`root` in each adapter payload is a path root, not a second worker directory.
The materializer copies every descendant of that folder to the same relative
path below the new worktree. It behaves like checking out a small file tree at
the worktree root:

```text
super-cache/adapter-payloads/codex/root/.codex/hooks/stop-wrapper.py
    becomes
<worktree>/.codex/hooks/stop-wrapper.py

super-cache/adapter-payloads/claude-code/root/.claude/hooks/stop-wrapper.py
    becomes
<worktree>/.claude/hooks/stop-wrapper.py
```

It must not copy `adapter-payloads/codex` itself into a worker as a literal
`adapter-payloads` directory. Its contents are mapped to their intended
provider paths.

ROOT supplies one `provider` ID and one `model` value with each public lane
bootstrap/launch request. Bootstrap is only a validator/materializer: it never
chooses either value. It validates the ID against the shipped catalog, records
both values in the lane invocation, and then has these two fixed copy steps:

1. Copy `super-cache/workspace/` into every new worktree, preserving relative
   paths.
2. Read the lane provider value recorded in the invocation and copy only that
   provider's `adapter-payloads/<provider>/root/` tree into the same worktree, preserving
   relative paths.

After those copies, the adapter writes the lane-specific binding values that
cannot live in a shared cache, such as the exact lane ID, invocation ID, queue
paths, and manager registration identity. It then writes or updates its own
provider hook declaration so it calls the shared helpers in that worktree.

The copy code must stage and preflight both trees before changing the worktree.
It must refuse an unexpected collision rather than silently overwrite a file.
The adapter may update only files it explicitly owns. The resulting overlay
receipt records the common-cache tree, selected adapter tree, and provider ID.

Codex, Claude Code, and Qwen Code payloads are shipped product content in
`<harness-root>/super-cache`. First setup makes the active runtime copy; a caller
does not supply them per lane. The only optional cache input is extra caller
content under `<runtime-root>/super-cache/custom/`. That content may add ordinary
shared files, but it must not replace adapter-owned hook declarations or wrappers.

The public setup/prepare route must therefore enforce all of the following:

- create the required runtime `super-cache` from the shipped source if it is
  absent;
- verify the product-owned common and three provider adapter payloads in that
  active copy;
- reject a lane whose required cache trees or selected provider payload are
  missing;
- always materialize the common tree and the selected adapter tree before
  provider launch; and
- always run the selected adapter installation/binding step after copying.

There is no `cache disabled` lane under this design. The optional part is only
whether the caller has placed additional files in `super-cache/custom/`.

## Validation required for this additional correction

For each of Codex, Claude Code, and Qwen Code, prepare a disposable worktree
and prove all of the following:

1. The common `result-stop-check.py` is present at the expected worktree path.
2. Only the selected provider's payload appears in the matching provider
   directory.
3. The adapter wrote a real native Stop hook pointing to that checker.
4. Attempting to finish with no `RESULT.json` is rejected by the provider.
5. Writing a malformed result is rejected by the provider.
6. Writing a valid `PASS`, `FAIL`, or `BLOCKED` result permits the provider to
   stop. This proves shape validation, not ROOT acceptance.
7. A custom shared cache file appears in the worktree without changing any
   adapter-owned hook path.
