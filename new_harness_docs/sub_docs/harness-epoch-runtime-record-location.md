# Harness defect: no single defined home for ROOT epoch records

Observed: 2026-08-23 during review of the executor Stop-hook/manager-queue
coupling correction.

> **Status: current detailed v2 target contract.** Sections explicitly labeled
> current harness inventory describe the candidate baseline only; the proposed
> v2 rules in this document are subject to the master planning decision index.

## The problem

The harness and surrounding workflow instructions require several live records to exist
outside executor worktrees: the fresh epoch configuration, feature
record, manager binding, queue state, resource-lease state, and lane runtime
records. They say that these are "outside-tree" or below `runtime_root`, but do
not define one canonical run-level directory or the paths of ROOT-owned
records.

Without that convention, a future implementation could scatter records across
the repository root, `fresh-experiments/`, an arbitrary provider workspace, or
ad-hoc temporary folders. In particular, a ROOT Stop hook would have no stable,
safe path from which to reopen the bound manager queue.

## Existing harness boundary

The harness already has the right primitive: every lane invocation has a
required `runtime_root` that must be an existing directory separate from the
lane's `run_root`. It constrains the resource-lock root and lane event-log path
to sit below that runtime root. See
`orchestrator_harness/lane_controller.py:617-634` in the active harness.

The current workflow documentation also requires each executor's `queue_root`
to be below its `runtime_root`. It does not, however, prescribe the one
run-level runtime-root layout or the ROOT manager-binding location.

## Current harness path inventory

The earlier proposed epoch directory is not every external file or path the
harness uses. For a normal executor lane, the active harness has these
external locations. This table describes the current harness behavior;
the proposed fix below removes ROOT's public `--config <path>` choice.

| Location | Chosen by | What goes there |
| --- | --- | --- |
| Manager `--config` file | ROOT | `suite_root`, lane-discovery globs, and diagnostic `output_dir`. |
| Diagnostic `output_dir` | `--config` | Harness scan/watch outputs. It is separate from `runtime_root` unless the caller deliberately points both below the same epoch folder. |
| `runtime_root` | Lane invocation | Required per-lane runtime parent. |
| `event_log_path` | Lane invocation | Lane-controller event log; must be below `runtime_root`. |
| `resource_lock_root` | Lane invocation or default | Lease files. If omitted, current coding lanes default to `<runtime_root>/coding-resource-locks`. |
| `queue_root` | Event-delivery binding | The manager-queue directory. The harness hardcodes `REGISTRATION.json`, `QUEUE.jsonl`, `STATE.json`, `WAKE.json`, and `DELIVERY.jsonl` inside it. |
| `coordinator_root` | Binding or default | Delivery-coordinator state, including `DELIVERY_COORDINATOR.json`. Codex defaults it to `<queue_root>/codex-coordinator`. |
| Super-cache directory | Bootstrap/overlay input | **Current harness behavior:** the existing `<harness-root>/super-cache`; it is outside the executor worktree. The proposed setup below moves this mutable directory below `runtime_root`. |

Separate public commands also take more external paths: source-view/cache/result
roots, lane archive roots, and handoff-preflight task/result/evidence paths.
Those are command-specific, not required for every executor lane.

The harness does **not** currently force all of the preceding paths below one
parent. It accepts several independent paths and validates only local
containment rules:

- `event_log_path` and the lease root must be below `runtime_root`.
- Queue and coordinator roots come from the event-delivery binding.
- Diagnostic `output_dir` comes from the manager config.
- `exclusive_resources` contains names such as `STM-A`; those names become
  lease files below `resource_lock_root`, but do not themselves specify a
  filesystem location.

## Required convention (not implemented here)

Create one fixed, ROOT-owned runtime root for the configured project workspace.
Its canonical form is:

```text
<root-workspace>/.harness-runtime/
```

Each epoch is a fresh child of that persistent project-local runtime tree:

```text
<root-workspace>/.harness-runtime/epochs/<epoch-id>/
```

Use the following small, fixed layout:

```text
<runtime-root>/
  RUNTIME_STATE.json           # one lifecycle gate
  CURRENT_EPOCH.json           # active epoch ID; queue ID only for a managed epoch
  manager/
    QUEUE.json                 # managed profile only; replaced per managed epoch

<epoch-runtime-root>/
  diagnostics/
  active-lanes.json            # exact currently monitored lane records
  lanes/
    <lane-id>/lane.json        # outside-worktree lane metadata
```

In the **managed** profile, the manager queue has one stable runtime-level path.
Every enabled static ROOT hook opens `<runtime-root>/manager/QUEUE.json`; it
never searches worktrees or uses a provider/session binding. A fresh managed
epoch gets a freshly generated `queue_id`: the harness stages and validates an
empty replacement queue, then atomically replaces the fixed file.
`CURRENT_EPOCH.json` names both the active epoch and the queue ID, so the
dispatcher rejects a mismatch rather than acting on stale events.

The **plain** profile has no manager queue and no enabled harness hook. Its
`CURRENT_EPOCH.json` records the active epoch and `lane_mode: "plain"`, but has
no `queue_id`; an already-materialized static ROOT wrapper returns without
opening a queue, emitting a notice, or applying a Stop gate. This is important:
the plain profile does not pretend a missing queue is a broken managed queue.

This does **not** mean creating a record for every feature. The persistent
configuration, queue, lease state, and lane records retain their existing responsibilities;
the only new ROOT-hook routing record is the generic current-epoch marker. The
point is to give all live epoch state one predictable home without adding a
second ROOT binding file.

## Ownership rules

- Source-controlled plans and durable project documentation remain in the
  repository.
- Worktree-local provider configuration and lane result files remain in the
  runner-created executor worktree.
- Live queue, lock, manager, and lane-metadata state live under the fresh
  epoch runtime root. Controller execution status and controller event history
  live in that lane's worktree under `.agent-workspace/`.
- `fresh-experiments/` is never a ROOT state destination or a place for ROOT
  to create/read/manage these records.

## Acceptance criteria

1. Setup derives exactly one persistent project-local runtime root at
   `<root-workspace>/.harness-runtime/`. Starting an epoch creates exactly one
   fresh child directory below its `epochs/` folder.
2. Every invocation's runtime, resource-lock path when a declared resource is
   requested, and worktree are descendants of that project-local runtime root. In the managed
   profile the one manager queue is fixed at
   `<runtime-root>/manager/QUEUE.json`; lane metadata remains below the current
   epoch; runtime-wide resource leases are shared below
   `<runtime-root>/resources/leases/` only when the lease facility is enabled.
3. The managed-profile ROOT hook dispatcher opens only the fixed manager queue
   and accepts it only when its `epoch_id` and `queue_id` match
   `CURRENT_EPOCH.json`. It rejects a missing, malformed, or mismatched record.
   A plain-profile wrapper performs no queue read or write and applies no
   harness Stop gate.
4. The monitor's outside-worktree state is limited to epoch and lane metadata.
   It follows the exact declared in-worktree controller paths; it does not use
   a broad worktree glob or create a second copy of the controller's logs.

## Plain-English file and location reference

| Thing | What it is | Where it lives | How its location is chosen |
| --- | --- | --- | --- |
| Monitor configuration | The monitor reads the fixed harness config plus `CURRENT_EPOCH.json` and controlled lane records. | No separate v2 manager-config file. | `operator_launch` resolves `<harness-root>/harness-config.json`; callers never pass an arbitrary config path. |
| Diagnostic output folder | Harness scan/watch snapshots, observations, and diagnostics. | `<runtime-root>/epochs/<epoch-id>/diagnostics/`. | Derived from the active epoch; callers never pass `output_dir`. |
| Runtime root | The project-local parent for all mutable harness state. | Proposed: `<root-workspace>/.harness-runtime/`; each epoch is its `epochs/<epoch-id>/` child. | Derived from the configured `root_workspace`; never supplied per lane. |
| `RUNTIME_STATE.json` | The one runtime lifecycle gate. Its state is `OPEN`, `SHUTTING_DOWN`, or `CLOSED`. | `<runtime-root>/RUNTIME_STATE.json`. | Setup creates or reopens it; shutdown atomically updates it under its short lock. |
| Lane event log | The controller's chronological execution-event log. | Proposed: `<worktree>/.agent-workspace/controller.events.jsonl`. | The public launcher derives the exact in-worktree path and supplies it as `event_log_path`. |
| `active-lanes.json` | The small, rebuildable index of lanes the monitor must currently inspect. It contains an exact lane-record path and current `run_id` for each active lane. `lane.json` is authoritative if they disagree. | `<epoch>/active-lanes.json`. | The public launch, resume, and retirement routes update this derived file atomically; health reconciliation may rebuild it from the controlled lane-record directory. |
| `lane.json` | Outside-worktree metadata for one lane: identity, one current `run_id`, exact worktree paths, provider/session and process identities, current artifact paths, and lifecycle state. It is not a copy of the controller log or a generation-history tree. | `<epoch>/lanes/<lane-id>/lane.json`. | The public bootstrap/launch and resume routes derive and update it; ROOT never edits it. |
| Manager-notification folder | The managed worker's one-way escalation outbox. Each file means the worker needs ROOT intervention. It is not the shared manager queue. | `<worktree>/.agent-workspace/manager-notifications/`. | Managed bootstrap derives the path, creates it, and records it in `lane.json`. A plain lane has none. |
| `manager-notify.py` | The managed worker's provider-neutral command that creates one notification file in the outbox. | `<worktree>/.agent-workspace/manager-notify.py`. | Managed bootstrap creates it beside the declared outbox. A plain lane has none. |
| Lane `QUEUE.json` | A managed live worker's incoming assignments from ROOT. It is not the epoch manager queue and it is never read by another worker. | `<worktree>/.agent-workspace/QUEUE.json`. | Managed bootstrap creates the empty file and records its exact path in `lane.json`; `send-lane-notification` is the only ROOT writer. A plain lane has none. |
| `lane-queue.py` | The managed local helper that lets a worker acknowledge, complete, or block a ROOT assignment without hand-editing JSON. | `<worktree>/.agent-workspace/lane-queue.py`. | Managed bootstrap creates it beside the lane queue. A plain lane has none. |
| Lease folder | Files used to claim exclusive hardware such as `STM-A`. | `<runtime_root>/resources/leases/`. | Derived from `root_workspace` and always created by setup. It remains empty when no lane requests hardware. |
| Lease files | One generated file per claimed resource. | Inside the lease folder. | Harness generates the filename from the `exclusive_resources` name. `["STM-A"]` is an invocation input for either managed or plain lane; the controller creates a file only while that lane holds the resource. |
| Manager `QUEUE.json` | The managed profile's authoritative manager-event queue. Its header contains `epoch_id` and freshly generated `queue_id`; its events contain current state and transition history. | `<runtime_root>/manager/QUEUE.json`. | Managed setup creates an idle valid queue. Each managed epoch stages an empty new queue with a new ID and atomically replaces this fixed path under the queue lock. A plain profile does not create or read it. |
| Super-cache | The shared reusable overlay input for worker worktrees. Its base payload is always copied; managed-only notification skills and provider-hook payloads are copied only for a managed lane. | Proposed: `<runtime_root>/super-cache/`. | Its path is derived, not configured separately. Setup initializes the baseline payload there. |
| Worker hook/binding files | Codex/Claude/Qwen provider setup for a managed executor. | Inside the executor worktree, for example `.codex/orchestrator-harness-binding.json`. | Hardcoded relative paths installed by the adapter only for the managed profile. Plain lanes use the launcher binding without copying provider hook/config payloads. |
| `feature-record.md` | Optional human/workflow evidence of selected features. | Outside the harness contract. | The harness neither creates nor reads it. |
| `CURRENT_EPOCH.json` | Generic active-epoch marker. For managed epochs, enabled ROOT wrappers read its `epoch_id` and fixed manager `queue_id`. For plain epochs, it says `lane_mode: "plain"` and has no queue ID; there is no active harness hook route. It has no path, ROOT provider, model, or session field. | `<runtime_root>/CURRENT_EPOCH.json`. | Epoch open atomically writes it after replacing the managed queue or after creating the plain epoch record; retirement clears it after normal closure. |

Some paths are arguments, some are fields inside the config or binding, and
some filenames are hardcoded once a parent folder is known. The current harness
does not enforce this layout. The v2 design instead derives every mutable path
from the one project-local runtime root and then derives epoch-specific paths
from its current `epochs/<epoch-id>/` child.

### One local temporary-file rule

Every v2 harness write that can replace an existing record or tree uses a unique
temporary sibling in the **destination's own parent directory**. It validates
that sibling, then performs a same-volume atomic rename or replacement while
holding that record's short lock. This includes queues, epoch and lane records,
the active-lanes index, monitor and lifecycle records, cache and manifest copies,
and setup `--overwrite` replacements.

That lock exists only for one read-modify-replace operation. The writer acquires
it, rereads the current complete record, changes only its owned fields, validates
and replaces the record, then releases the operating-system lock in a
`finally`/cleanup path. It is not a durable `locked` field and ROOT never
manages it. If a writer crashes, closing its process handle releases the lock;
the next writer performs the normal parse/health check before continuing.

For a truly append-only file, this does **not** mean rebuilding the live file
from scratch: the harness copies the last complete live file to its unique
temporary sibling, appends the one new record to that sibling, validates it, and
atomically replaces the live file. It never appends in place to the live shared
file. A record whose existing item changes state is instead edited in the
temporary copy before that same replacement.

For example, a queue update stages
`<runtime-root>/manager/QUEUE.json.tmp.<operation-id>`, not a file in
a system temporary directory or a shared staging folder. A directory copy such as the active
super-cache likewise stages as a sibling of `super-cache/`. A rollback copy,
when one is needed, is also a unique sibling. The holder of the same destination
lock may remove only its harness-named stale temporary or rollback siblings
after rechecking the destination; the harness never scans or cleans an arbitrary
system temporary directory. This keeps every transient harness file inside the
project workspace and preserves the atomic-replacement guarantee.

The deterministic cleanup rule is strict: on a successful atomic replacement,
the temporary sibling is consumed by the rename and therefore no longer exists
as a temporary file. The writer removes any temporary or rollback sibling that
was not consumed before releasing its lock, including through its `finally`
path on failure. After a crash, the next holder of that destination lock removes
only the known harness-named leftovers for that destination before proceeding.
No successful harness operation may leave a temporary file behind.

This is a harness/configuration-contract defect, not a BYO Firmware MCP,
firmware, board, or test-plan defect.

## Detailed proposed fix: one persistent harness config, derived epoch paths

The fix should not require ROOT to assemble a different set of root-path flags
for every lane or every manager epoch. The harness should have one persistent
configuration file for the whole managed task, for example:

```text
<harness-root>/harness-config.json
```

This is a fixed harness location, not a ROOT-supplied command argument. The
public harness command resolves its own root and always loads exactly this
file. ROOT edits the known configuration contents once, then invokes public
commands without a config pathname.

This is configuration, not live state. It is the one path authority for stable
harness settings and the only place optional behavior is selected:

```json
{
  "schema": "firmware-v2-harness-config/v1",
  "root_workspace": "/project-workspace",
  "managed_coordination": "enabled"
}
```

The closed config schema has one required key, `root_workspace`, and one optional
key, `managed_coordination`, which takes `enabled` or `disabled` and **defaults to
`enabled`** when omitted — managed is the default profile (see resolution R16 in
`harness_single.md`). Any missing required key, or any key outside this closed
set, makes setup return `SETUP_CONFIG_INVALID` (see resolution R9). The runtime
root is derived, not configured, and the `schema` version key lives in
`resource-manifest.json`, not here.

The ROOT workspace is configured once. The runtime root is then always derived
as `<root_workspace>/.harness-runtime/`, so it belongs to the project workspace
rather than to an unrelated sibling folder. ROOT supplies neither a config
pathname nor separate runtime, queue, coordinator, lease, diagnostic, cache,
worktree, and lane-log paths to public commands. The public harness derives:

```text
<runtime_root>/super-cache/
<runtime_root>/worktrees/
<runtime_root>/monitor/
<runtime_root>/resources/
<runtime_root>/epochs/
```

ROOT also owns one fixed pre-run input beside the fixed configuration:

```text
<harness-root>/resource-manifest.json
```

That file is the whole allowed list of exact exclusive resource IDs for this
configured harness installation. `harness setup` validates it and writes the
active runtime copy at:

```text
<runtime_root>/resources/RESOURCE_MANIFEST.json
```

For a project with no hardware, the manifest's `resources` list is simply empty.
That is the normal no-hardware declaration; it does not select a feature profile
or remove the generic controller lock facility.

No lane may invent a resource name. Bootstrap accepts a requested exclusive
resource only when its ID appears in this generated runtime manifest. The
controller later creates and removes only its own temporary lock files under
`<runtime_root>/resources/leases/`. ROOT is the authority for the resource
list; the controller is the authority for the live lock files. Neither workers
nor lanes edit either one directly.

The resource manifest is a ROOT-authored list of permitted hardware names, not
a second feature-settings file. Resource locking is always available: an empty
manifest simply means this project uses no hardware, and a lane that names a
declared resource receives the normal lock regardless of its profile. The one
optional setting in `harness-config.json` is `managed_coordination`, which
controls only the manager-event, hook, and worker-config package. No public lane
command accepts an `--enable-*`, `--disable-*`, profile override, or per-lane
feature flag. Setup validates the stored value before it creates the matching
coordination state. When an epoch opens, its record carries that immutable
configuration identity so later commands consume it rather than make a new
choice.

For every prepared lane, the worktree path is also derived rather than supplied
as another root-path argument:

```text
<runtime_root>/worktrees/<epoch-id>/<lane-id>/
```

This is the explicit ownership split:

- `<harness-root>` is a child of `<root_workspace>` in the current v2 deployment.
  It contains product material: harness code, the fixed `harness-config.json`, the
  ROOT-authored fixed `resource-manifest.json`, the shipped read-only
  `<harness-root>/super-cache/` source tree, shipped adapter templates, and
  registered `launcher_binding.py` modules used as harness code.
- `<root_workspace>` is ROOT's actual project workspace. Setup writes
  ROOT-facing provider skills there and derives its hidden
  `.harness-runtime/` child as the home for every mutable/generated harness
  item: the shared **active working copy** of the cache, generated worktrees,
  monitor record, active resource manifest, global controller lease files,
  epochs, queues, diagnostics, and lane metadata. That child
  is locally Git-excluded when the workspace is a Git worktree.

The two same-named cache folders have intentionally different jobs:

```text
<harness-root>/super-cache/  # shipped source; setup and lanes never edit it
                 |
                 | setup makes the first verified copy
                 v
<runtime_root>/super-cache/  # active working copy; every lane reads this one
```

No ordinary run command writes cache, worktree, queue, lease, monitor, or log
state below `<harness-root>`. Setup may install/check registered adapter bindings
there, but that remains inside the project workspace. The current external harness still uses
`<harness-root>/super-cache` directly as its active cache; changing that
implementation is required for this proposed contract to become real.

### What the setup command does

Provide one public setup route with an explicit replacement option:

```text
operator_launch harness setup
operator_launch harness setup --overwrite
```

`operator_launch` resolves `<harness-root>/harness-config.json` itself. A
config-path override may exist in private unit-test helpers, but not in the
normal ROOT-facing command surface.

ROOT is already launched in the configured project workspace, so the config does
not contain a ROOT provider/model choice or session identity. Setup materializes
all shipped standard ROOT-facing payloads (`.codex`, `.claude`, and `.qwen`) in
that workspace, plus any static custom adapter already installed in the catalog.
Setup does not choose or start ROOT, and it does not restrict later lanes to any
one provider or model.

It reads the persistent configuration and:

1. validates that the configured `root_workspace` is absolute and safe, then
   derives `<root_workspace>/.harness-runtime/`; the derived directory must be
   contained by the project workspace, must not be a symbolic link or other path redirection, and must
   not be an executor worktree;
2. creates `runtime_root` and its derived `worktrees/`, `monitor/`, `epochs/`,
   and `resources/` directories if they do not already exist. In the managed
   profile only, it also creates `manager/` and writes/validates an idle manager
   `QUEUE.json` whose header has no active epoch. Plain setup creates neither.
   It does not pre-create `super-cache/`, because that path is the atomic
   destination in the next step;
3. when the required active super-cache does not yet exist, byte-verifies and
   transactionally copies the shipped
   `<harness-root>/super-cache` source tree to
   `<runtime_root>/super-cache`;
4. when that active cache already exists, verifies it and leaves it unchanged.
   Setup must not silently overwrite a working cache that may contain approved
   added content; a later explicit cache-refresh route can make a new verified
   copy only after the caller deliberately requests it;
5. validates the fixed source `resource-manifest.json`, then stages,
   byte-verifies, and atomically writes its active copy to
   `<runtime_root>/resources/RESOURCE_MANIFEST.json`. It creates the one
   shared lease parent `<runtime_root>/resources/leases/`. A later setup call
   leaves an identical active manifest in place; it rejects a changed one while
   an epoch is active or any live lease remains. ROOT never hand-edits the
   active manifest or a lease file;
6. reads the one stored compatibility flag, validates `managed_coordination` as
   either `enabled` or `disabled`, and later records that immutable profile
   identity when an epoch opens; no public command supplies a separate feature
   or profile choice;
7. in normal mode, installs each complete shipped ROOT payload (including the
   ROOT skills and native hook wrappers) in the configured `root_workspace` only
   when every planned destination is absent. The wrappers are active only in the
   managed profile; a plain profile has their explicit no-op behavior rather than
   a queue to bind;
   a collision rejects the complete materialization. With `--overwrite`, setup
   replaces exactly the preflighted harness-owned hook, skill, adapter, and binding
   destinations, reports each replacement, and rolls back that materialization if a
   late write fails;
8. starts the one mandatory provider-agnostic monitor process and writes its
   PID-plus-creation identity and
   health record under `<runtime_root>/monitor/MONITOR.json`. It takes the short
   monitor-record lock, returns `SETUP_MONITOR_ALREADY_RUNNING` for an exact live record,
   and replaces only an absent/stale record with a fresh monitor;
9. rejects a missing source tree, malformed active cache or resource manifest,
   second live monitor,
   or conflicting feature/path
   configuration.

The active super-cache, persistent monitor, resource-lock facility, and normal
worktree payload are always on and are not config choices. The one compatibility
setting selects one explicit lane profile; the harness does not guess from a
missing file, absent resource, or observed CLI behavior.

`managed` and `plain` are not two launchers. They share the same public
bootstrap/launch/controller/result/resume and resource-lock machinery. The one
compatibility flag merely decides whether that common lane receives the optional
manager-queue and native-hook code. A profile is fixed for the active epoch, and
a setup/reconfiguration that changes it opens a new epoch.

The configuration validates this small explicit dependency table instead:

| Flag or fixed facility | Valid setting | Dependency / effect |
| --- | --- | --- |
| Active super-cache | Always on | Not a flag. Every lane bootstrap uses the runtime cache. |
| Persistent monitor | Always on | Not a flag. It owns the active-lane scan and health checks. |
| Resource manifest and lock facility | Always on | Not a flag. Setup always validates/copies the manifest and creates the lease parent. An empty manifest declares no hardware; any lane that names a declared resource uses the same controller lock path. |
| Normal worktree payload (`.agent-workspace` and task/result/controller files) | Always on | Not a flag. It is generic harness structure, not provider hook configuration. |
| `managed_coordination` | `enabled` (**managed**) or `disabled` (**plain**) | The only v2 compatibility setting. Managed lanes get the fixed manager queue, worker queues/outbox, enabled ROOT/worker harness hooks, and provider worktree configuration. Plain lanes get none of that package but remain fully launchable through the same provider launcher/controller. `disabled` exists solely for a provider that cannot prove the required native hooks; ROOT then uses `scan --no-write` and `watch --until-actionable`. |

For clarity, the complete plain profile is exactly:

```json
{
  "managed_coordination": "disabled"
}
```

In plain mode setup still materializes the shared cache, monitor, normal ROOT
project files, and provider launcher bindings. This complete set is a
deterministic consequence of the stored setting, not a later lane decision. It
does **not** create a manager queue, start a manager-event loop, copy worker
hook/config payloads, or create a worker outbox or incoming queue. Its lanes
still use the ordinary resource lock when they request a declared resource. If static ROOT hook
configuration was already loaded from an earlier managed setup, its generic
wrapper takes the explicit plain branch and exits immediately; it does not turn
the absence of a queue into a failure.

Setup does not launch a worker and does not need an executor worktree to exist. It
prepares and validates the shared harness infrastructure, including the mandatory
monitor.

### Managed-profile super-cache manager-notification skills

This recommendation intentionally changes the old empty, caller-selected neutral
cache. The harness ships this baseline payload in its read-only source tree:

```text
<harness-root>/super-cache/
```

On first setup, that source tree becomes the active runtime copy. A **managed**
bootstrap copies this payload into its worktree before the worker starts:

```text
<runtime_root>/super-cache/adapter-payloads/
  codex/.codex/skills/manager-notify/SKILL.md
  codex/.codex/skills/lane-assignment/SKILL.md
  claude/.claude/skills/manager-notify/SKILL.md
  claude/.claude/skills/lane-assignment/SKILL.md
  qwen/.qwen/skills/manager-notify/SKILL.md
  qwen/.qwen/skills/lane-assignment/SKILL.md
```

There are two managed worker skills per provider: `manager-notify` and
`lane-assignment` (see resolution R11 in `harness_single.md`). The `manager-notify`
files give the same direct instruction in their provider's normal skill
format: when the worker needs manager intervention, run the lane's declared
`.agent-workspace/manager-notify.py` command; state the decision or action ROOT
needs; attach relevant local evidence; and do not write the shared queue or rely on
a final chat message.

The skill must tell the worker to use the exact helper path recorded in its
`lane.json`, rather than hardcoding an epoch, queue, or worktree path in the cached
file. The helper and notification folder are still created per lane by bootstrap;
the cache contains guidance, not live lane state or an executable notification tool.

The managed lane controller's mechanically appended prompt block remains required.
The cache skill is a second, provider-native reminder after the managed overlay is
copied. It does not replace prompt injection, and a copied skill file is not
evidence that a provider loaded or followed it. A plain bootstrap copies only the
base cache content needed for its normal provider run; it does not copy this
manager-notification skill or any other queue/hook payload.

The cache owns exactly these two managed worker skills per provider —
`manager-notify` and `lane-assignment` — and no others. A Codex, Claude, or Qwen
adapter may add its own hooks, bindings, launch overrides, or other provider-specific
files after preparation, but it must not overwrite, merge into, or become the owner
of the cached worker skills. If a provider needs extra wording, its adapter
adds a separate provider-owned prompt fragment or file.

Any extra shared content belongs only in the active
`<runtime_root>/super-cache/custom/` tree. It never edits the shipped source
tree. A lane reads the complete active cache, including approved custom content;
it never reads the harness-root source tree directly.

### ROOT workspace manager skills

Setup also writes this separate, harness-owned baseline into the configured ROOT
workspace. These are **not** copied into executor worktrees:

```text
<root_workspace>/
  .codex/skills/manager-notification-watch/SKILL.md
  .claude/skills/manager-notification-watch/SKILL.md
  .qwen/skills/manager-notification-watch/SKILL.md
  .codex/skills/acknowledge-manager-notification/SKILL.md
  .claude/skills/acknowledge-manager-notification/SKILL.md
  .qwen/skills/acknowledge-manager-notification/SKILL.md
  .codex/skills/close-manager-notification/SKILL.md
  .claude/skills/close-manager-notification/SKILL.md
  .qwen/skills/close-manager-notification/SKILL.md
  .codex/skills/review-lane-completion/SKILL.md
  .claude/skills/review-lane-completion/SKILL.md
  .qwen/skills/review-lane-completion/SKILL.md
  .codex/skills/send-lane-notification/SKILL.md
  .claude/skills/send-lane-notification/SKILL.md
  .qwen/skills/send-lane-notification/SKILL.md
  .codex/skills/resume-lane/SKILL.md
  .claude/skills/resume-lane/SKILL.md
  .qwen/skills/resume-lane/SKILL.md
  .codex/skills/harness-shutdown/SKILL.md
  .claude/skills/harness-shutdown/SKILL.md
  .qwen/skills/harness-shutdown/SKILL.md
```

The watch and acknowledgement skills give ROOT this direct idle-time procedure:

1. When resuming management work or before intentionally becoming idle, run one
   `scan --no-write` to collect the current lane facts.
2. When ROOT has no active work of its own, run `watch --until-actionable`.
   In the corrected design this existing public command waits on ROOT-targeted
   manager-queue events; it does not use a worktree glob or inspect provider
   transcripts as its notification source.
3. When the watch returns, inspect the queue event. For each top-level event ID
   ROOT actually read, use the acknowledgement skill's public command below;
   then resolve the event and start another idle watch only when ROOT is idle
   again.

While ROOT is carrying out a current ROOT task, a PostToolUse reminder is only a
reminder. It returns after every tool boundary while the fixed manager queue has
one or more unacknowledged events. It explicitly says not to open or acknowledge
the queue until the current ROOT task is complete, then to use the
`acknowledge-manager-notification` skill. ROOT works one manager task at a time.
Delivery by a hook or return from a watch never counts as ROOT acknowledgement.

`scan` is a one-time snapshot, not a wait. `watch --until-actionable` is a
foreground command and is used only while ROOT is deliberately idle. In the
managed profile the skill does not ask ROOT to poll or invent another notification
route; it waits on the one manager queue.

For a **plain** lane, this is deliberately more direct: because its provider CLI
does not participate in the harness hook/manager-notification route, ROOT must
actively use `scan --no-write` when it returns to management work and
`watch --until-actionable` while idle. The plain watch returns changed lane status
from controlled records; it is not a queue event, requires no acknowledgement, and
does not wake ROOT by itself. ROOT then chooses the appropriate public direct
review or resume command.

The remaining five skills name their exact public routes:
`close-manager-notification` marks an acknowledged ordinary ROOT event
`COMPLETE` or `BLOCKED`; `review-lane-completion` handles an acknowledged
completion event and runs `lane completion-review`; `send-lane-notification` sends
work only to a live lane's incoming queue; `resume-lane` resumes a
rejected/unaccepted stopped lane with a new resume card, the same worktree/provider
session, and a fresh current `run_id`; and `harness-shutdown` runs controlled
cleanup. A rejected completion review writes `LANE_RESUME_REQUIRED` into ROOT's
manager queue; the review skill does not restart the provider and the resume skill
handles that new event.

The setup route owns only these named ROOT skill files. A later normal setup leaves
the shared runtime cache and manifest alone but rejects an existing planned ROOT
materialization target; `setup --overwrite` deliberately refreshes those exact
harness-owned files and reports every replacement. Provider adapters may add
separate ROOT-provider hooks, bindings, or extra instructions, but they do not alter
the ROOT watch skills or the worker `manager-notify` cache skills.

The three `acknowledge-manager-notification` skills give ROOT this exact public
route for the manager queue:

```text
operator_launch manager acknowledge --event-id <top-level-event-id>
```

The command opens the fixed runtime manager queue itself; ROOT supplies only the
exact top-level event ID. It validates the queue header against `CURRENT_EPOCH.json`,
takes that queue's short lock, reads the event, and atomically changes its
acknowledgement in `QUEUE.json`. It returns
`ACKNOWLEDGED` after a first acknowledgement, `ALREADY_ACKNOWLEDGED` without a
second write when ROOT repeats the same ID, and an error for an unknown,
wrong-queue, or non-ROOT-targeted ID. It does not mark the event `COMPLETE` or
`BLOCKED`.

The skill tells ROOT to inspect the queue read-only first, then run this command
only for the top-level IDs ROOT actually read. ROOT must not use a `DELIVERED`
receipt, a nested signal ID, or direct JSON editing as an acknowledgement.

After handling an acknowledged ordinary ROOT event, `close-manager-notification`
runs `operator_launch manager close --event-id <top-level-event-id> --outcome
COMPLETE|BLOCKED --summary "<what ROOT did or needs>"`. It accepts only that
acknowledged ROOT event in the fixed queue, changes it atomically to the selected
terminal state, and records the summary. It never starts or resumes a lane.

The three `send-lane-notification` skills give ROOT one equally direct instruction
for assigning work to a **live** lane:

```text
operator_launch send-lane-notification --lane-id <lane-id> --prompt "<assignment>"
```

This is the only ROOT-facing writer for a worker's incoming queue. ROOT does not
open a worker worktree and does not edit its `QUEUE.json` directly. The command
resolves the lane through the active-lane record, checks the exact provider
PID-plus-creation identity and controller state, and writes only when that exact
lane is still running. If it is not running, it writes nothing and returns
`LANE_NOT_RUNNING`, telling ROOT to use the public resume route instead. It never
silently queues a message for a dead process or automatically resumes one.

### How a new epoch works

When ROOT submits a public lane bootstrap/launch request, the launcher code
resolves the current epoch itself. An epoch is the whole stable managed run, not
one section of a plan and not one lane. If an active epoch has the same immutable
harness configuration, every later bootstrap, launch, and resume reuses that
epoch. A complex project buildout may therefore remain in one epoch from its
first lane until it is intentionally stopped.

The launcher creates a new epoch only when there is no active epoch, public
shutdown/reconfiguration closed the old one, or an epoch-sensitive immutable fact
changes. Ordinary new lanes, new plan sections, and their provider/model choices
do not by themselves create another epoch. The selected `managed` or `plain`
profile is an immutable epoch fact. A managed epoch receives a new logical
manager queue ID at the fixed runtime queue path; a plain epoch receives none.
When a new epoch is required, the launcher creates one new epoch identifier and
derives every epoch-specific path below the configured runtime root:

```text
<runtime_root>/resources/                 # created at setup; shared by epochs
  RESOURCE_MANIFEST.json                   # ROOT's allowed resource IDs
  leases/                                  # controller-owned live lock files

<runtime_root>/manager/
  QUEUE.json                               # managed profile only; fresh ID per managed epoch

<runtime_root>/epochs/<epoch-id>/
  epoch-state.json
  diagnostics/
  active-lanes.json
  lanes/
    <lane-id>/lane.json
```

The paths are not new ROOT arguments. They are a deterministic consequence of
`runtime_root`, the launcher-generated `epoch-id`, and the lane identifier. For
a lane named `lane-001`, the public launcher always uses exactly:

```text
<runtime_root>/epochs/<epoch-id>/lanes/lane-001/lane.json
<runtime_root>/worktrees/<epoch-id>/lane-001/
<worktree-for-lane-001>/.agent-workspace/controller.status.json
<worktree-for-lane-001>/.agent-workspace/controller.events.jsonl
<worktree-for-lane-001>/.agent-workspace/provider-transcript.jsonl
<worktree-for-lane-001>/.agent-workspace/provider-stderr.txt
<worktree-for-lane-001>/.agent-workspace/last-message.txt
<worktree-for-lane-001>/RESULT.json
```

A managed lane additionally has the outbox, `manager-notify.py`, worker
`QUEUE.json`, and `lane-queue.py` below `.agent-workspace/`. A plain lane does
not. Its controller status, event log, transcript, result, provider session,
and `lane.json` are ordinary execution records, not manager coordination files.

### Plain epoch opening

A plain epoch uses the same epoch/lane directory and lifecycle machinery, but
does not manufacture an unused queue. Opening it is simply:

1. Retire the old epoch and confirm no old controller is still live.
2. Create the new epoch in `OPENING` state with immutable `lane_mode: "plain"`.
3. Atomically write `CURRENT_EPOCH.json` with that epoch ID and mode, with no
   `queue_id`.
4. Mark the epoch `ACTIVE`; bootstrap may now create plain lanes.

No `manager/QUEUE.json`, worker queue/outbox, manager event, queue lock, hook
delivery receipt, or lease claim is created by that sequence. The persistent
monitor still tracks the plain lane's controller and record health through
`active-lanes.json`; it simply has no queue event to emit or await.

### Generic ROOT routing when an epoch opens

In the **managed** profile, ROOT hooks never need to locate an epoch-specific queue. Every static Codex,
Claude, Qwen, or custom ROOT wrapper calls the generic dispatcher, which always
opens this fixed file:

```text
<runtime_root>/manager/QUEUE.json
```

The queue is logically fresh for every epoch even though its path is permanent.
The queue header and current-epoch marker are deliberately small and
provider-neutral:

```json
// <runtime_root>/manager/QUEUE.json
{
  "schema": "firmware-v2-manager-queue/v1",
  "epoch_id": "epoch-20260828-001",
  "queue_id": "<fresh generated queue ID>",
  "events": []
}
```

```json
// <runtime_root>/CURRENT_EPOCH.json
{
  "schema": "firmware-v2-current-epoch/v1",
  "epoch_id": "epoch-20260828-001",
  "queue_id": "<the same fresh queue ID>"
}
```

Neither record contains a provider, model, CLI executable, session, or queue
path. The dispatcher accepts the queue only when both records parse and their
epoch/queue IDs agree. The queue path is fixed, so no `manager/binding.json` or
ROOT `.agent-workspace` binding file exists in v2.

Opening a new **managed** epoch performs this small sequence before the launcher
marks it active or launches its first worker:

1. Retire the old epoch and all of its lanes; confirm no old lane/controller can
   still write a manager event.
2. Create the new epoch in `OPENING` state and stage a valid empty manager queue
   with a fresh `queue_id` and the new `epoch_id`.
3. Under the one manager-queue lock, atomically replace the fixed
   `<runtime_root>/manager/QUEUE.json` with that staged queue.
4. Atomically write `CURRENT_EPOCH.json` with the same new epoch/queue IDs.
5. Mark the epoch `ACTIVE`; only then permit its lane launches and manager-event
   writes.

Every manager-event writer records its epoch/queue IDs and must match both live
records before it writes. A late old lane therefore receives `EPOCH_RETIRED`
instead of contaminating the new queue. If queue health finds a malformed
authoritative queue for a still-valid active epoch, it removes that record and
installs a fresh empty fixed queue with a fresh `queue_id` for the same epoch,
then updates `CURRENT_EPOCH.json`. A writer carrying the former ID returns
`QUEUE_REPLACED` and writes nothing. If the active-epoch record itself cannot
be trusted, the next normal epoch open creates the fresh queue instead. This
non-mission-critical recovery does not replay lost events, emit a quarantine
record, or recreate a ROOT session.

The first path is the external metadata record. The remaining paths are lane
execution records. The controller writes the status, event log, transcript,
stderr, and last-message files in the worktree. `RESULT.json` remains the
worker's result file; the controller reads and validates it rather than writing
the worker's claim for it.

For a managed lane, `lane.json` also contains the exact
`manager_notification_dir` and `manager_notify_command` paths above. Bootstrap
creates both before the worker starts. The helper accepts a short summary,
severity, and optional worktree-local evidence paths. It writes one new JSON
file to the declared notification folder by writing a temporary file and
renaming it into place. It never writes the shared queue, lease files, or
`lane.json`. A plain `lane.json` has no such fields.

For a managed lane, `lane.json` must also contain the exact `incoming_queue_path` and
`incoming_queue_command`. Those refer only to this lane's
`.agent-workspace/QUEUE.json` and `.agent-workspace/lane-queue.py`. They are
not aliases for `<runtime_root>/manager/QUEUE.json`, which remains ROOT's separate
manager queue.

The incoming queue holds ROOT-created assignments with an event ID, lane ID,
current `run_id`, prompt, creation time, current state, and transition history.
The public `send-lane-notification` command takes that file's short lock, reads the
whole file, adds one `PENDING` assignment, writes a temporary replacement, and atomically
replaces `QUEUE.json`. It does not modify the runtime manager queue or claim that
the worker has seen the assignment.

The worker uses its declared `lane-queue.py` helper rather than editing the JSON.
It may change a received assignment from `PENDING` to `ACKNOWLEDGED`, then to
`COMPLETE`; if it cannot carry it out, it records `BLOCKED` with a reason and
uses `manager-notify.py` to escalate that fact to ROOT. `COMPLETE` and documented
`BLOCKED` are terminal worker-side states. This avoids leaving a worker held open
forever when the only possible next step belongs to ROOT.

`epoch-state.json` holds dynamic facts created for this one epoch: the epoch ID,
immutable configuration identity including `lane_mode`, opening/active/closed
lifecycle state, lane directory, and ownership status. It is generated by the
harness, not hand-edited by ROOT. It contains no ROOT provider/session,
manager-binding, or queue-path fields. In managed mode the ROOT Stop gate opens
the fixed runtime manager queue and cross-checks its IDs against
`CURRENT_EPOCH.json`; plain mode has no harness Stop gate.

The persistent monitor reads `CURRENT_EPOCH.json`, then the one declared active
epoch's `epoch-state.json` and `active-lanes.json`. It therefore needs no queue
path discovery, provider binding, or restart when lanes change. For a plain
epoch it records health against the lane record only; it does not create a
synthetic manager event to compensate for the intentionally disabled facility.

ROOT does not have an `epoch open`, `epoch retire`, or lane-record editing step.
The public launcher owns those records. For a managed epoch it atomically replaces
the fixed manager queue with a fresh queue ID; for a plain epoch it writes no
queue. It publishes the generic current-epoch marker before it prepares the first
lane, updates the active-lane index as controllers start/retire, and retains that
same epoch for later lanes while its immutable configuration remains unchanged. It
closes the epoch only after no active lane and, in managed mode, no unresolved ROOT
manager event remain, or during the public shutdown/reconfiguration route. A later
lane receives a fresh generated epoch only when that closure or an epoch-sensitive
change requires one; it never reuses prior event IDs, queue IDs, or process
ownership.

The resource manifest is intentionally not inside the epoch directory. V2 has one
active epoch at a time, but the runtime-wide `resources/leases/` folder still
makes every live exclusive claim explicit and keeps the manifest stable for the
whole configured runtime. It is not an epoch-local file that ROOT can rewrite
midway through a run.

### Existing campaign bootstrap and the missing neutral-harness layer

The frozen campaign runner already proves that bootstrap can be a real program,
not a checklist ROOT must remember. Its
`orchestrator_harness/lane_bootstrap.py:465-637` function
`bootstrap_coding_lane(manifest_path)` reads one manifest and then:

1. validates the lane ID, workflow role, canonical role selection, base commit,
   branch, task card, resource manifest, runtime paths, resource list, and launch
   settings;
2. runs `git worktree add -b <branch> <experiment-root>/worktrees/<name>
   <base-commit>`;
3. creates the worktree's `.agent-workspace/` directory;
4. applies the selected cache overlay and writes its receipt;
5. installs/binds event-delivery material when requested; and
6. writes the worker prompt, truthful-result template, controller invocation JSON,
   and controller status/transcript/stderr/last-message paths.

It then returns `status: prepared`. It does **not** start Codex or another provider,
operate hardware, flash a board, start an MCP server, or perform campaign work. A
separate public launch route consumes the written invocation later. That separation
is deliberate: preparing a controlled worker environment and launching a worker are
different operations.

Its paired `cleanup_coding_lane()` at lines 640-666 first runs Git status including
untracked files and refuses removal if anything changed. It therefore cannot casually
discard a worker's edits.

The separate external neutral-harness checkout has no `lane_bootstrap.py` or
equivalent one-manifest prepare-only public route. Its lower-level worktree/overlay
and provider-controller pieces are useful, but ROOT must currently assemble their
inputs. The two checkouts must not be described as though this capability already
exists in both.

**Recommendation:** move this capability into the neutral harness as one
provider-neutral public bootstrap route. It accepts a generic manifest, validates and
prepares the lane, creates the worktree and `.agent-workspace/`, applies the enabled
cache, installs the selected adapter material only for a managed lane, writes the
invocation and result template, and atomically creates the `lane.json` record in
state `PREPARED`. Managed bootstrap additionally creates the notification
outbox/helper and incoming lane queue/helper; plain bootstrap explicitly omits
them. It stops there. A distinct launch command starts the temporary controller
and only then makes the lane active. Worktree removal is an operator action, not
a harness cleanup prerequisite: a retired worktree may be removed manually and
must not affect a later setup or launch.

The existing campaign bootstrap is the reference for this split, not a claim that it
already contains the proposed generic `lane.json`, `active-lanes.json`, one-file queue,
or worker-notification outbox features.

### How lane bootstrap changes

ROOT continues to provide the task-specific information for a lane, such as
the lane ID, task card, and exact `exclusive_resources`.
It does not provide runtime path plumbing. For example:

```text
operator_launch lane bootstrap \
  --lane-id lane-001 \
  --provider <shipped-provider-id> \
  --model <provider-model-name> \
  --task-card <task-card> \
  --exclusive-resource <resource-token>
```

ROOT supplies `--provider` and `--model` in that request. Bootstrap is not an
agent and does not select either value: it validates them, selects the matching
fixed shipped payload, and writes the same values into the lane invocation.
The later public launch consumes that invocation without replacing those values.
Different lane invocations may name different provider IDs and model values at
the same time.

ROOT does not supply an epoch ID. The public launcher determines or creates the
current epoch before bootstrap writes the worktree/invocation paths. ROOT also
does not update `lane.json` or `active-lanes.json`; the bootstrap, launch,
controller, monitor's one owned status field, resume, and retirement code own
those writes at their respective stages.

For each `--exclusive-resource`, bootstrap opens only the already-generated
`<runtime_root>/resources/RESOURCE_MANIFEST.json` and checks for an exact ID
match. It rejects a missing, duplicate, or undeclared ID before creating a
worktree. ROOT cannot bypass the resource list by supplying a different
manifest path with one lane request. The invocation records the selected IDs
and the one derived shared lease root; it does not copy the resource definition
into the worktree.

A plain profile disables coordination, not resource safety. A plain bootstrap
may name `--exclusive-resource` exactly as a managed bootstrap may, provided the
resource appears in the active manifest. The shared controller acquires and
releases that project-local lease; ROOT simply learns the lane's later state by
its required scan/watch path rather than a hook notification.

The public bootstrap route derives and supplies internally:

```text
runtime_root        = <root-workspace>/.harness-runtime/
event_log_path      = <worktree>/.agent-workspace/controller.events.jsonl
resource_manifest   = <runtime-root>/resources/RESOURCE_MANIFEST.json
resource_lock_root  = <runtime-root>/resources/leases/ (always available)
manager_queue_path  = <runtime-root>/manager/QUEUE.json (managed coordination only)
manager_queue_id    = <CURRENT_EPOCH.json>.queue_id     (managed coordination only)
overlay_cache        = <runtime-root>/super-cache       (required shared cache)
```

The `manager_queue_*` fields, worker queue/outbox paths, and provider hook/config
payload are absent from a plain invocation and plain `lane.json`, rather than
being empty path strings. Its provider command still comes from the same selected
`launcher_binding.py`, and its controller still writes the ordinary status,
event-log, transcript, and result records.

The public route must not accept arbitrary path arguments from ROOT. It derives
the exact in-worktree event-log path itself. Because every lane worktree is now
also below the project-local `runtime_root`, that event-log path satisfies the
controller's normal runtime containment rule without a special exception.

It then creates the executor worktree, applies the super-cache, installs the
provider's managed worktree-local configuration/binding only when the profile
enables it, writes the invocation and other prepared-lane records, and stops. It
does not obtain a live lease, start a controller, or launch a provider. ROOT
never hand-creates those files in a worker worktree. The separate public launch
route obtains the controller-owned lease only for a managed lease-enabled lane
and starts the provider only after it consumes the prepared invocation.

Before provider launch, this same public route writes the derived lane metadata
record:

```text
<runtime_root>/epochs/<epoch-id>/lanes/<lane-id>/lane.json
```

The record identifies the lane, task, role, provider, worktree, exact in-worktree
controller paths, and the controller/provider PID-plus-creation identities once
known. A managed record additionally identifies manager-notification and worker
queue paths and expected manager epoch/queue IDs. Any record whose lane requests
a declared resource identifies its external lease path, independent of profile.
A plain record omits only the coordination fields. The write sequence
must be deterministic:

1. Bootstrap derives the record and all paths. Managed bootstrap creates the
   in-worktree `manager-notifications/` folder and `manager-notify.py` helper,
   plus the empty incoming `QUEUE.json` and `lane-queue.py` helper. Plain
   bootstrap creates none of those coordination files. Both atomically write
   `lane.json` with a fresh `run_id`, explicit `lane_mode`, and state `PREPARED`.
2. The public launch route starts the temporary controller, records that exact
   controller PID-plus-creation identity, and only then atomically adds the
   lane's `{ lane_id, run_id, lane_record_path }` entry to
   `<epoch>/active-lanes.json`.
3. The controller records provider identity in `lane.json` when it starts the
   provider. Its changing execution state and chronological event history go to
   the declared files in `.agent-workspace/`, not to a second external log.
4. After owned-process cleanup is proved, retirement records the final lane
   state and removes that exact lane/run entry from `active-lanes.json`, while
   retaining `lane.json`. It does not need the retired worktree to remain on
   disk: an operator may remove that old worktree later without changing the
   record or breaking another lane.

`resume-lane` does not create another worktree. Under the lane-record lock it assigns
the same lane a fresh `run_id`, writes the new current task/rationale/instructions,
and clears obsolete current result/review/acceptance artifacts through the public
harness route. It does not archive prior rejected artifacts, create a history folder,
or maintain task-generation lineage.

There must be at most one writer holding the lane-record lock at a time. The
launch route owns initialization before handoff, the controller owns every normal
lane field while it runs, and retirement owns finalization after controller
cleanup. The monitor is the one narrow concurrent participant: while holding the
same lock, it may change only `last_reported_actionable_status` after rereading
the latest record. An unexpected controller exit leaves the lane listed as active
until the monitor and public launcher have classified it; it must not silently
disappear. In managed mode ROOT may resolve the resulting manager event; in plain
mode it uses the record's direct status. ROOT never edits the lane record.

The configured persistent monitor reads `active-lanes.json`, then opens only
the `lane.json` files named there and the exact paths declared inside them. It
does not scan every directory below `lanes/` or every worktree. A newly launched
lane is therefore visible on the next monitor pass without restarting the
monitor, while an unrelated worktree cannot be mistaken for a lane.

`active-lanes.json` is a monitor index, not a second lane authority. The exact
`lane.json` state wins if the two disagree. If the index is missing or malformed,
health reconciliation scans only this epoch's controlled `lanes/` directory,
rebuilds the index from lane records in an active lifecycle state, and never
treats an index-only entry as a real lane.

The managed provider-launch prompt is not allowed to rely on the worker
discovering its coordination helpers itself. The managed lane controller
mechanically appends a generated escalation and incoming-assignment block to the
worker task prompt. The block gives the exact `manager-notify.py` command,
explains when ROOT help is needed, and says to call the helper before stopping or
continuing past a manager decision. It also gives the exact `lane-queue.py`
command and says that a ROOT assignment is acknowledged, completed, or blocked
through that command rather than by editing `QUEUE.json`. The managed ROOT
initial-prompt template receives the matching queue-event block. These blocks are
generated from lane/epoch records, not copied manually into task cards or
`AGENTS.md`. A plain lane receives neither block or helper path; it receives only
its normal task/result prompt and controller result contract.

### Why this removes the current hodgepodge

The existing harness accepts several independent root-path inputs: `output_dir`
in the scan/watch config, `runtime_root`, `event_log_path`, optional
`resource_lock_root`, `queue_root`, optional `coordinator_root`, and the
super-cache path. The fix reduces ROOT's stable path input to one config file.
The harness derives all of the remaining live locations from it.

Hardcoded names still have a useful limited role. In the proposed queue design,
the runtime manager path is always exactly `manager/QUEUE.json`; it does not
split authoritative event state between `QUEUE.jsonl` and `STATE.json`. The
current router's `REGISTRATION.json`, `QUEUE.jsonl`, `STATE.json`, `WAKE.json`,
`DELIVERY.jsonl`, and coordinator layout are historical/current behavior that
must be replaced, not retained by this fix. Once
`resource_lock_root` is known, the harness derives a lock filename from the
exact resource ID selected from the generated runtime manifest. There is no
need to put every generated filename in user configuration. The neutral lock
engine does not assign special board meaning to an ID; a campaign that needs
such rules validates them before it calls the neutral lane route.

Public setup, epoch, scan, watch, bootstrap, launch, status, and cleanup commands
remain on-demand commands. `harness setup` also starts the one mandatory
provider-agnostic monitor, which stays alive to observe registered active epochs.
It is recorded under the configured runtime root and is stopped only by the public
harness shutdown/reconfiguration route, after active epochs are retired.

### Required observable validation

1. `harness setup` succeeds from one persistent config and creates/checks only
   the configured shared infrastructure; it launches no provider or lane.
2. Every setup creates the active runtime resource manifest and shared lease root.
   Managed setup additionally creates the valid idle fixed manager queue before
   any lane request; plain setup creates no queue. Neither profile creates a
   lease claim until a lane requests a declared resource. The public launcher creates the exact derived epoch
   directory and `epoch-state.json` when required; no queue/lease/diagnostic root
   or epoch ID is separately supplied by ROOT.
3. Bootstrap for a lane produces an invocation whose runtime, in-worktree
   event-log, resource-manifest, and overlay-cache paths exactly match the
   derivation rules above. A managed invocation additionally has its fixed manager
   queue ID. Either profile records the shared lease path only when it requests a
   declared resource. An undeclared resource is rejected before worktree creation.
4. A wrong, missing, non-absolute, worktree-inside, or conflicting config path
   is rejected before a worktree, provider, lease, or hardware action occurs.
5. A second epoch created from the same persistent config gets a different
   state directory. A managed epoch also gets a fresh manager queue ID at the
   same stable queue path; a plain epoch creates no queue. Both retain the same
   configuration and super-cache.
6. No normal ROOT-facing harness command accepts a config-path option or can
   select a different configuration file.
7. Setup takes the short monitor-record lock and starts exactly one verified
   monitor from the fixed configuration. A
   second setup returns `SETUP_MONITOR_ALREADY_RUNNING` for an exact live identity; an
   absent identity is removed and replaced with one fresh monitor record. A new lane
   becomes observable without restarting the monitor only after its exact
   `lane.json` entry appears in that epoch's `active-lanes.json`.
8. In managed mode, a worker can run its declared `manager-notify.py` command and create one valid
   outbox file. The monitor admits exactly one ROOT-targeted queue event for it;
   the worker never receives direct write access to the shared manager queue.
9. In managed mode setup creates both worker skills — `manager-notify` and
   `lane-assignment` — for each provider in the active super-cache. A disposable
   Codex, Claude, and Qwen lane each proves that its provider discovers the
   corresponding copied skills; the generated prompt block is present independently
   in all three launches.
10. In managed mode setup writes the three ROOT `manager-notification-watch` skills to the
     configured `root_workspace`. A disposable invocation of each provider proves
     its already-installed static payload is discovered and directs idle ROOT to the
     corrected `watch --until-actionable` route.
11. The same managed setup writes the three ROOT `acknowledge-manager-notification`
     skills. A disposable invocation of each provider proves that its PostToolUse
     notice follows `CURRENT_EPOCH.json` and names this skill while a manager event
     remains unacknowledged; after ROOT reads the event, the public acknowledgement
     command changes only that top-level event to `ACKNOWLEDGED`.
12. The same managed setup writes the three ROOT `close-manager-notification` skills.
    A disposable acknowledged ordinary event proves that `manager close` changes
    only that top-level event to `COMPLETE` or `BLOCKED`.
13. The same managed setup writes the three ROOT `send-lane-notification` skills. A queue attempt for a
    live disposable lane writes one assignment only to that lane's declared
    `.agent-workspace/QUEUE.json`; the same attempt after that provider exits
    returns `LANE_NOT_RUNNING`, writes nothing, and names the public resume route.
14. The same setup writes the three ROOT `review-lane-completion` skills. A valid
    managed terminal lane result creates one `COMPLETION_REVIEW_REQUIRED` manager
    event; a valid plain terminal result becomes direct review-pending state.
    ROOT uses the profile-matched skill/public command to write `ACCEPTED` or
    `REJECTED`. A managed rejection writes one `LANE_RESUME_REQUIRED` manager
    event; a plain rejection returns direct resume-required output. Neither starts
    a provider.
15. The same setup writes the three ROOT `resume-lane` and `harness-shutdown`
    skills. Their commands respectively resume a stopped, unaccepted lane with a
    new resume card, or perform the public controller/monitor cleanup route; the
    skills never edit a lane record or process identity directly.
16. A disposable plain lane proves all of the following together: its worktree
    has no worker queue/outbox, hook binding, provider hook/config payload, or
    lease file; the common launcher/controller writes a valid `RESULT.json`; direct
    `lane completion-review --lane-id` writes the decision pair; and a rejection
    returns direct resume-required output without emitting a manager event.
