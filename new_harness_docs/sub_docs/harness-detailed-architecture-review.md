# Firmware-v2 harness: detailed architecture review

> **Status: historical diagnosis and source evidence.** This records the
> candidate's old checkout, router, coordinator, and binding behavior. It does
> not define the v2 runtime protocol; use the master planning document and the
> current detailed v2 target contracts for that.

## Scope and important source split

There are currently two different local harness checkouts. They are not
interchangeable.

- The campaign's frozen runner is
  `MCP-Trial-3/firmware-v2-harness-runner` at commit
  `e2145c5c4420fa47bc71d642eb9fb995d03b5f98`. It has
  `orchestrator_harness/lane_bootstrap.py`.
- The external runner is
  `<absolute-path>/harness-v2-firmware-runner`
  at commit `10383827b92c50e43b35f64cade1295c5af27793` when inspected. It
  has uncommitted changes, includes the Claude/Qwen adapter work, and does
  not have `lane_bootstrap.py`.

Consequently, a claim that the external checkout can bootstrap campaign
worktrees is false as it exists today. Conversely, a claim that the frozen
campaign bootstrap supports the external checkout's Qwen implementation is
also false. Documentation and launch routes must name the checkout they mean.

No hardware, MCP, provider, or campaign action was run for this review.

## 1. Bootstrap: how a lane is actually created

This capability exists in the frozen campaign runner at
`orchestrator_harness/lane_bootstrap.py:465-637`.

Bootstrap is a real program, rather than a list of things ROOT is expected to
remember. It reads one bootstrap manifest and:

1. Validates the lane ID, workflow role, canonical role mapping, base commit,
   branch, task card, resource manifest, runtime paths, resource list, and
   launch settings.
2. Runs `git worktree add -b <branch> <experiment-root>/worktrees/<name>
   <base-commit>`.
3. Creates `.agent-workspace` inside that new worktree.
4. Applies the cache overlay and writes its receipt.
5. Installs/binds event-delivery hook material when event delivery is
   requested.
6. Writes the worker prompt, a truthful-result template, the controller
   invocation JSON, and paths for status/stdout/stderr records.
7. Stops. It does not launch Codex, flash hardware, use an MCP server, or do
   campaign work.

That separation is good. Preparing a controlled worker environment is not the
same operation as launching a worker. The corresponding cleanup route refuses
to remove a worktree with tracked or untracked changes
(`lane_bootstrap.py:640-666`), so it cannot casually discard worker work.

The problem is not bootstrap itself. The problem is that this useful layer is
absent from the separate external checkout, while the two are discussed as
though they are one product.

## 2. Lane controller: what happens after launch

The controller is a one-shot supervisor process. It is not a persistent
harness program.

Its invocation reader validates that:

- `run_root` is an existing worktree;
- the prompt and all output paths are contained under the intended worktree;
- the prompt bytes match the declared SHA-256;
- output paths do not collide with reserved result/acceptance records.

See `lane_controller.py:231-281` and `lane_controller.py:387-430`.

Before it starts a provider, the controller validates Git state, checks that
there is no duplicate active declaration, verifies an optional overlay receipt,
checks requested provider operations, and writes status beginning in
`LAUNCH_FAILED`. This avoids reporting an interrupted launch as healthy. The
main control path starts at `lane_controller.py:1811`.

After the provider is started, the controller streams provider stdout/stderr to
files, parses the provider's lifecycle records, waits for the exact child
process boundary to be cleaned up, validates the worker result, and writes a
terminal controller status.

Most importantly, provider success is not campaign success. A provider can
complete while its result is invalid, blocked, or awaiting ROOT acceptance.
The controller deliberately keeps terminal acceptance pending rather than
turning a zero exit code into a firmware-test pass
(`lane_controller.py:3117-3231`). This is good separation of responsibility.

## 3. Process ownership and named firmware leases

Each exact resource name, for example `STM-A`, becomes an atomic claim file
under the lane's declared resource-lock root. A claim contains the lane ID,
worker invocation ID, controller PID, creation timestamp/identity, and a
boundary marker. See `resource_locks.py:317-471`.

The practical flow is:

1. The controller creates all requested claims. If it obtains one resource but
   cannot obtain the next, it releases the partial set before waiting.
2. Before the provider starts, it arms the claims. From that point onward, a
   controller disappearance means a provider child might still exist.
3. On contention, the next lane checks the old owner PID *and its creation
   identity*. It cannot reclaim a claim merely because a PID number no longer
   looks familiar.
4. It removes a stale claim only after rechecking the exact claim bytes under
   the resource's kernel lock.
5. At the end, it releases claims only after the owned process boundary is
   proven clean. If proof is incomplete, it retains the claim and records the
   unresolved boundary instead.

This is deliberately conservative and is one of the strongest parts of the
harness. It can leave a board unavailable after an uncertain failure, but that
is much better than giving two workers the same board.

The design weakness is path configuration: the lock root still comes from a
bootstrap/invocation path instead of being derived from one central harness
configuration.

## 4. Provider adapters

The generic controller asks an adapter to build the actual CLI command, encode
the prompt, parse its stream records, and map the provider's final state to
`COMPLETED`, `FAILED`, or `CANCELLED`.

- Codex uses a headless `codex exec` launch, JSON output, and a worktree
  working directory. It supports resume/session parsing.
- Claude uses `claude --print --output-format stream-json`, then parses its
  initialization and result records.
- Qwen adapter code exists in the external checkout, but it is not thereby a
  campaign executor in the frozen bootstrap.

The provider starts inside its generated worktree. The launcher does not use
`--ignore-user-config`, so normal user configuration remains available while
project configuration is taken from that worktree.

The frozen bootstrap currently requires executor role mapping to select Codex;
see `lane_bootstrap.py:413-452`. Thus Qwen/Claude work in the other checkout is
not integrated merely by existing elsewhere. That is a real integration gap,
not a provider preference.

## 5. Super-cache: what it does and does not do

The super-cache is a controlled overlay. It is not a shared live filesystem and
not a magical way to make hooks execute.

For executor lanes, the campaign bootstrap requires an `overlay_cache` that
contains:

- `.codex/config.toml` with `features.hooks = true`;
- `.codex/hooks.json`;
- a native command hook under each of `SessionStart`, `PreToolUse`, and `Stop`.

See `lane_bootstrap.py:201-248`.

The overlay implementation preflights every change. New directories merge;
normal existing-file collisions are rejected; only explicitly declared text
append targets may be appended. If preparation fails after changing files, it
rolls its own changes back. Its receipt records the target worktree identity,
role, files created/appended, and pre/post bytes, which makes exact retirement
possible. See `workspace_overlay.py:530-602`.

That is sound overlay engineering.

However, a hook configuration being copied into a worktree does not by itself
prove that the provider invokes it. The Codex CLI 0.149.0 failure described in
the earlier external-harness README is historical evidence, not the current
v2-candidate status. Native headless PostToolUse delivery has now been proven
through the current `harness-single` candidate for Codex, Claude Code, and
Qwen Code; each provider executed a real tool call and wrote a durable
`DELIVERED` receipt. See `subagent_hooks.md` for the exact provider proofs.

That proof establishes native adapter hook discovery and PostToolUse delivery.
It does not make an overlay receipt proof that a hook ran, prove every hook
type or provider mode, or prove the proposed role-aware Stop gates. Those
remain separate implementation and acceptance-test requirements.

There is also a source divergence: the external README describes the cache as
not supplying hooks, whereas the campaign bootstrap explicitly requires
hook-enabled cache contents. This must be reconciled rather than papered over
in documentation.

## 6. Manager queue and event delivery

`ManagerEventRouter` is a durable filesystem event ledger. Given a queue root,
it owns fixed queue records including:

- `REGISTRATION.json`: the exact registered run/queue identity;
- `QUEUE.jsonl`: event and acknowledgement history;
- `STATE.json`: current derived active state;
- `WAKE.json`: a monotonically increasing queue revision;
- `DELIVERY.jsonl`: evidence of attempted notification delivery.

Every event is bound to the exact run, queue, manager session/thread,
registration, manager invocation, and generation. This prevents one stale lane
from writing into a different manager's queue.

`DeliveryCoordinator` stores separate coordinator state in
`DELIVERY_COORDINATOR.json`. It builds a deliberately sparse delivery notice:
binding identity, queue revision, pending count, severity/class, timestamp,
and adapter profile. A delivery receipt means only that an attempt was
delivered; it never removes the underlying queue work. See
`host_adapters.py:580-790` and `host_adapters.py:1085-1199`.

Only ROOT, through the bound router, may acknowledge the top-level event ID.
It must not acknowledge `data.signal_id`. This is correct: a failed or
misdirected notification transport cannot silently lose a manager event.

The fatal practical limitation is notification. There is no independently
running harness daemon that watches the queue and injects an event into ROOT's
context. A durable queue is useful evidence, but it is not by itself a wake-up
mechanism.

## 7. What `scan` and `watch --until-actionable` actually do

`scan` reads the configured worktree folders, their status/result records, and
an OS process snapshot. It reports diagnostics such as a lane claiming to be
running while its claimed process is gone.

`watch --until-actionable` repeats that scan on a timer, compares the new
diagnostic conditions against the prior conditions, prints an actionable
difference, and exits. It is a foreground poller. The exact loop is in
`cli.py:209-253`.

It does not:

- persist as a manager process;
- asynchronously wake ROOT;
- allow ROOT to do other work while waiting;
- re-arm itself after printing;
- read or acknowledge the ManagerEventRouter queue.

So the queue and the watcher are separate systems. Describing this foreground
diagnostic poller as a native manager event loop makes it sound far more
capable than it is.

## 8. Executor Stop-hook / ROOT queue coupling

The installed Stop-hook logic asks whether its bound manager queue has pending
events. It does not distinguish a ROOT process from an executor process.
`notification_stop_request()` in `host_adapters.py:1332-1389` applies the
same queue gate to whichever process runs that hook.

That creates the backwards behavior:

1. An executor publishes its result/event for ROOT.
2. ROOT has not yet acknowledged it.
3. The executor's Stop hook sees that ROOT-owned event.
4. The executor can be prevented from stopping.

That is wrong ownership. An executor should publish its result, stop, and
release hardware only after its own process cleanup is proven. ROOT alone
should be prevented from ending while ROOT-owned manager events remain. The
current source does not enforce that distinction.

## 9. Resume and structured handoff

Resume is strict by design. It compares the previous controller status,
invocation ID/schema, provider session/thread, Git state, and task/prompt
identity. If the exact continuation cannot be proven, it creates a structured
handoff and avoids launching a provider under a fabricated resumed session.
See `lane_controller.py:1811-2107`.

This is not needless complication. It prevents an agent from continuing the
wrong task, on the wrong branch, with the wrong hardware/test history.

## 10. Current design verdict

The solid parts are:

- exact process cleanup and fail-closed lease release;
- atomic resource claims with PID-reuse protection;
- bounded worktree creation and dirty-worktree cleanup refusal;
- path containment and prompt hashing;
- overlay receipts and rollback;
- strict resume identity;
- durable queue records that do not lose work merely because notification
  delivery failed.

The parts requiring real correction are:

- two divergent checkouts being discussed as one harness;
- scattered runtime/configuration path selection;
- `watch --until-actionable` being a blocking diagnostic poller rather than an
  automatic manager notification mechanism;
- generic ROOT epoch routing still needs implementation in the new harness:
  reuse one epoch while immutable configuration is unchanged; on a new epoch,
  atomically replace the fixed manager queue with a fresh queue ID, then publish
  `CURRENT_EPOCH.json` without replacing or binding a ROOT session;
- executor Stop hooks being coupled to ROOT's queue;
- Qwen/Claude adapter work not being integrated into the frozen campaign
  bootstrap;
- contradictory cache/hook behavior described by the external runner versus
  the campaign runner.

The persistent harness configuration and setup approach proposed in
`harness-epoch-runtime-record-location.md` would directly address the
scattered-path problem. It would not, by itself, repair the wake mechanism or
the Stop-hook ownership bug; those require explicit implementation and live
role-aware Stop-hook evidence. Native PostToolUse delivery is no longer an
open feasibility issue for Codex, Claude Code, or Qwen Code; its current proof
and limits are recorded in `subagent_hooks.md`.
provider evidence.

---

# Appendix: direct-English implementation description

This appendix replaces the previous appendix. It uses plain English and names
the actual command, input field, file, and process involved. It intentionally
does not describe what the harness is *meant* to achieve.

## 1. What "the controller" actually is

"Controller" is not a permanent harness program. It is just the name for one
temporary Python process created for one worker run.

The public launch code starts this command:

```text
<python> -m orchestrator_harness.lane_controller <invocation.json>
```

The launch code creates that process, records its PID and
start time in a launch-receipt JSON file, starts it, and then the launch code
returns. It does not remain open in the background to manage that process.

The newly started Python process reads `invocation.json`. It then starts a
second process: the selected agent CLI. For a Codex worker, that second process
is `codex exec ...`. It runs that command with the worker worktree as its
current folder. The temporary Python process captures the CLI's normal output
and error output into files. When the CLI has ended, it checks cleanup, writes
its final status JSON, and exits.

The real process chain is therefore:

```text
ROOT starts a launch command
  -> that command starts one temporary Python process
       -> that Python process starts codex exec
            -> codex exec ends
       -> the Python process ends
```

The only long-lived things are files left behind: the launch receipt, status
file, CLI output files, lock files, and queue files. There is no always-running
harness process behind them.

## 2. How the worktree is actually made

The campaign copy has a separate short-lived bootstrap command. It is not part
of the temporary controller process above.

It is called with:

```text
python -m orchestrator_harness.lane_bootstrap <manifest.json> --result <result.json>
```

The manifest contains direct path values such as:

```json
{
  "experiment_root": "/chosen/experiment/folder",
  "source_repository_root": "/existing/Git/repository",
  "runtime_root": "/chosen/runtime/folder",
  "worktree_name": "worker-01",
  "branch": "worker-01-branch",
  "base_commit": "a 40-character Git commit ID"
}
```

Those paths come from that one manifest. They do not come from a permanent
harness configuration file.

The bootstrap command then does this:

1. Creates `<experiment_root>/worktrees` and `<experiment_root>/dispatch`.
2. Writes the task-card and resource-manifest copies under `dispatch`.
3. Runs Git to create:

   ```text
   <experiment_root>/worktrees/<worktree_name>
   ```

   on the requested new branch and base commit.
4. Creates `<worktree>/.agent-workspace`.
5. Writes the worker prompt, a result template, and `invocation.json` into
   `.agent-workspace`.
6. Writes the chosen `runtime_root` into `invocation.json`.
7. Exits.

The controller cannot create a worktree itself. It refuses to run unless the
`run_root` written in `invocation.json` is already an existing directory.

The external harness checkout with the Claude/Qwen work does not contain this
bootstrap command. That is a literal code difference, not just documentation
drift.

## 3. How the cache is actually copied

There are two separate ways the code uses a cache folder.

### Generic cache refresh

This command takes two direct command-line paths:

```text
python -m orchestrator_harness workspace super-cache ingest \
  --source <folder-to-copy-from> \
  --harness-worktree <harness-folder>
```

It copies every ordinary file and folder under `--source` into a temporary
folder next to:

```text
<harness-folder>/super-cache
```

It reads the source files again and compares their bytes with the temporary
copy. If they match, it renames the temporary folder to `super-cache`. If a
previous `super-cache` folder exists, it renames that old folder aside first.
If this fails before the final rename, the old cache remains in place.

This command does not create a worker worktree and does not put files into any
worker worktree.

### Campaign worker preparation

The campaign bootstrap manifest contains a direct string field:

```json
{
  "overlay_cache": "/some/folder"
}
```

Bootstrap uses that field as the source folder. It does not ask a permanent
harness service for a cache. It does not prove that the path is the harness's
own `super-cache` directory; it only checks that the named folder exists and
has the expected `.codex` files. The separate campaign admission adapter is
what currently checks the expected cache location.

For every file below `overlay_cache`, bootstrap first checks whether the same
relative path already exists in the new worktree.

- If the file does not exist in the worktree, it reads the cache file's bytes
  and writes those bytes into the worktree.
- If a folder already exists, it uses the folder and continues below it.
- If a normal file already exists, bootstrap stops with an error.
- The only exception is a file explicitly listed in
  `<overlay_cache>/.super-cache.json` under `append_text`. For that case it
  reads the old worktree file, then appends the cache file's bytes to it.

It plans all of those changes before changing the worktree. If writing fails
halfway through, it removes files it created and restores old bytes for files it
appended to. It then writes:

```text
<worktree>/.agent-workspace/overlay-receipt.json
```

That receipt says which paths it created or appended, and stores the old/new
bytes for changed files. It does not contain a cache version or cache hash.
Editing the cache later does not modify a prepared worktree.

## 4. How hook setup differs between the campaign and the neutral harness

The earlier description in this document was the **campaign runner's** hook
setup. It is not how the pointed external harness now intends its neutral cache
to work.

### Campaign runner: cache-owned hooks plus adapter-owned hooks

In the frozen campaign runner, an executor manifest names `overlay_cache`.
Bootstrap requires that folder to contain:

```text
<overlay_cache>/.codex/config.toml
<overlay_cache>/.codex/hooks.json
```

It copies those files into every new worker worktree. It checks only that the
files say hooks are enabled and contain command-hook entries for `SessionStart`,
`PreToolUse`, and `Stop`.

If that same manifest contains `event_delivery`, bootstrap then runs the Codex
adapter installer. The installer writes its own hook scripts under
`<worktree>/.codex/hooks/`, adds its own entries to the already copied
`<worktree>/.codex/hooks.json`, and writes the adapter/binding JSON files.

In other words, the campaign runner has two inputs editing the worker's hook
setup:

```text
campaign super-cache
  -> copies .codex config and hook settings into the worker

Codex adapter installer
  -> adds harness hook scripts and more hook settings to that worker
```

Those inputs must remain compatible. The campaign cache check only proves the
cache files look right; it does not prove Codex loaded or ran them. The earlier
headless `codex exec` failure is historical. The current `harness-single`
candidate has separately proven native Codex PostToolUse delivery, but that
does not prove this older campaign overlay alone activates its hooks. See
`subagent_hooks.md` for the current proof boundary.

### Pointed external harness: neutral cache, adapter-owned hooks

The pointed external harness intentionally removed the shipped cache's
`.codex/hooks.json`, `.agent/stop-verify.ps1`, `.super-cache.json`, and
`AGENTS.md`. Its normal shared cache is therefore empty until a caller chooses
content and ingests it.

Its cache route only copies caller-selected files into a worktree. It does not
require the cache to provide `.codex` files, does not inspect cache hook
settings, and does not claim the cache installed or ran provider hooks.

After optional cache preparation, the provider adapter is a separate setup
step. The adapter owns the hook scripts, hook declarations, adapter manifest,
and manager-event binding files for its provider. For example, the documented
order is:

```text
optional cache ingest
  -> optional cache copy into the new worktree and receipt
  -> install/check the selected provider adapter in that worktree
  -> launch the provider
```

That gives one product owner for shipped hook setup: the provider adapter, not
the cache.

A caller can still deliberately place `.codex` or provider files in a custom
cache source. In that case those are caller-owned files and can still conflict
with the adapter. The external harness does not claim that arbitrary caller
cache content is automatically compatible with adapter files.

The pointed harness also has a separate native-hook repair for Codex, Claude,
and Qwen. It establishes provider hook discovery/trust at launch and records
delivery separately from cache preparation. Its reported live proof is evidence
for native adapter hook delivery, not evidence that an overlay receipt made a
hook run. That repair is described as locally verified but uncommitted in the
external checkout.

## 5. What event delivery actually writes

**Neutral-harness part.** Both harnesses have the same basic file-backed
manager queue and provider-adapter idea. A provider adapter is given a queue
folder and manager identity, writes a provider-specific binding in the
worktree, and later its **PostToolUse** hook reopens that binding to record a
delivery attempt.
The external neutral harness has adapters for Codex, Claude, and Qwen. It does
not have a firmware campaign manifest or a permanent queue service.

**Campaign-only part.** The frozen campaign adds an `event_delivery` object to
its bootstrap manifest. Its `lane_bootstrap.py` checks that object, creates the
queue/binding automatically, and currently installs the Codex adapter. The
external neutral harness does not contain that campaign bootstrap file or this
firmware-specific manifest shape. The campaign also requires every executor to
use the shared epoch manager identity; that is campaign policy, not a general
property of a neutral coding lane.

For the campaign object, the caller supplies a folder path plus these IDs: run,
queue, manager session, manager thread, registration, manager invocation, and
generation. Bootstrap checks that the supplied queue folder is below the
supplied runtime folder. The shared queue uses these files:

```text
REGISTRATION.json
QUEUE.jsonl
STATE.json
WAKE.json
DELIVERY.jsonl
```

It also creates:

```text
<runtime_root>/codex-coordinators/<lane-id>/DELIVERY_COORDINATOR.json
<worktree>/.codex/orchestrator-harness-binding.json
```

The binding JSON tells a later hook where those queue/coordinator folders are
and repeats the supplied IDs.

The campaign's literal sequence is:

1. `lane_bootstrap.py` reads the `event_delivery` JSON object from the bootstrap
   manifest. If it is absent, that function does nothing; the campaign's
   separate admission rules are what require it for an executor lane.
2. After creating the new Git worktree, bootstrap calls the Codex adapter's
   installer for that worktree. That installer writes the adapter-owned Codex
   hook files and its adapter record under `<worktree>/.codex/`.
3. Bootstrap creates one temporary `ManagerEventRouter` Python object from the
   supplied queue path and IDs. Its constructor creates or checks the queue
   files above. It does not start a child process.
4. Bootstrap gives that router object and
   `<runtime_root>/codex-coordinators/<lane-id>` to the Codex binding helper.
   That helper writes `DELIVERY_COORDINATOR.json` and the binding JSON. Bootstrap
   records the resulting paths and IDs in its result JSON, then exits.

The external neutral harness has no step that reads `event_delivery` from a
firmware manifest. Its provider adapters can still be installed and bound to a
queue, but the caller supplies that setup through the adapter/lane route rather
than receiving the campaign's automatic bootstrap sequence.

The exact Codex binding path shown above is a campaign-Codex example. The
neutral Claude and Qwen adapters use their own provider files, but follow the
same pattern: files on disk, opened when a hook runs, rather than a continuously
running connection to ROOT.

This limitation is neutral-harness behavior, not firmware-specific behavior.
When bootstrap or an adapter call ends, nothing stays open watching the files.
A later **PostToolUse** hook execution reopens its binding JSON and the queue
files. If there is an outstanding delivery notice, it appends a delivery receipt
to `DELIVERY.jsonl`; otherwise it records no delivery receipt. It then prints a
hook result and ends. There is no socket, pipe, background queue reader, or
program that can independently insert a message into ROOT's active context.

When something adds an event, it appends an event record to `QUEUE.jsonl`, then
updates `STATE.json` and `WAKE.json`. When ROOT acknowledges an event, it
appends an acknowledgement record and updates the latter two files again. A
delivery receipt goes in `DELIVERY.jsonl`; it does not acknowledge or delete
the event.

The frozen campaign's acknowledgement path is Python code that must be given
the exact queue binding; it uses the top-level event ID, not a worker signal ID
inside the event data. This is a campaign integration detail, not evidence that
the neutral external harness has a persistent manager process.

Nothing in this sequence delivers a queue event into a different agent's chat
context. The queue files are durable evidence only. A hook can append a
delivery receipt, but it cannot acknowledge ROOT's event or make ROOT's model
receive text by itself.

## 6. What `scan` and `watch --until-actionable` actually read

**Neutral-harness part.** `scan` and `watch --until-actionable` are generic,
diagnostic commands in both harnesses. They use a separate JSON configuration
file passed directly to the command:

```text
python -m orchestrator_harness --config <some-config.json> scan
python -m orchestrator_harness --config <some-config.json> watch --until-actionable --timeout 60
```

The config chooses folders to search for worker worktrees, the relative path of
`.agent-workspace`, where diagnostic output is written, and how long to wait
between scans. It does not contain the single universal paths for the cache,
runtime, leases, queue, or coordinator. If `--config` is omitted, the command
uses the packaged example config. There is no current built-in global
`harness-config.json`. That is true of the neutral harness too.

`scan` searches the configured worktree folders. It reads lane status/workspace
files and asks the operating system which processes exist. It prints one JSON report.
It does not read `QUEUE.jsonl` and does not touch the event queue.

`watch --until-actionable` repeats that same scan in a loop inside the command
that ROOT started. It compares the latest scan with the previous scan. If a
listed condition changed, it prints one JSON report and exits. If the timeout
is reached, it prints a timeout report and exits.

More literally, every loop iteration calls the suite-discovery code, asks the
OS for a fresh process snapshot, turns those results into diagnostic
conditions, and compares that condition list with the previous list. It then
sleeps for the configured `poll_interval_seconds`. Its output directory stores
the last cursor/diagnostic records; it is not the manager queue and no part of
this loop opens `QUEUE.jsonl`.

So while ROOT is waiting for that command, ROOT is occupied by the command. If
the command returns, ROOT has to start it again to watch further changes. It
does not remain running after printing. It does not inspect the separate event
queue folders. It does not wake ROOT automatically. Those are generic watcher
limitations; they are not caused by the firmware campaign.

**Campaign-only part.** This campaign's instructions require ROOT to run
`scan --no-write` and then `watch --until-actionable` during an epoch. That
makes the command part of this campaign's procedure, but does not change how
the neutral watcher works underneath.

## 7. What the provider launch actually does

**Neutral-harness part.** A generic lane invocation names a provider command,
model/settings, and a worktree. A short-lived controller starts the selected
provider with that worktree as its working directory. The pointed-at neutral
harness has provider adapters for Codex, Claude, and Qwen; each adapter builds
the command line for its own CLI. It is the adapter, not the cache, that owns
provider launch settings and hook setup.

**Campaign-only part.** The frozen campaign's bootstrap writes the
`invocation.json` and its executor mapping currently selects Codex. The literal
Codex command below therefore describes the frozen campaign runner, not the
neutral harness's Claude or Qwen launches.

For Codex, the code always builds a command containing:

```text
codex exec
--dangerously-bypass-approvals-and-sandbox
--skip-git-repo-check
--json
--output-last-message <worktree>/.agent-workspace/last-message.txt
--cd <worktree>
```

It also adds the configured model, reasoning level, service tier, and
`approval_policy` configuration value. It may add
`--dangerously-bypass-hook-trust` when an overlay receipt is present.

The important implementation problem is simple: the invocation's `sandbox`
field is written into status/evidence, but the Codex command-building code does
not turn that field into a real Codex sandbox setting. It always sends
`--dangerously-bypass-approvals-and-sandbox` instead. This is provider-adapter
behavior, not a firmware rule; the external neutral harness's Codex adapter
also currently has that dangerous-bypass command shape.

The same command also includes an `approval_policy` configuration value. Neither
harness proves which instruction Codex gives priority to when that value and
the dangerous bypass switch are both present. Therefore those recorded
sandbox/approval values are not normal enforcement evidence.

The code does not add `--ignore-user-config` and does not replace the provider
home directory. The child process starts in the worker worktree, so it can see
both normal user configuration and project configuration in that worktree.
That worktree-root configuration rule is shared behavior; the campaign makes
it mandatory for its executor lanes.

The process sequence is also short-lived and literal: ROOT uses the public
launch route to start `python -m orchestrator_harness.lane_controller
<invocation.json>`. ROOT's launcher returns after recording that controller's
process identity. The controller reads the invocation, verifies the requested
overlay receipt when one is supplied, builds one provider command, then calls
`subprocess.Popen(..., cwd=<worktree>)` with stdin/stdout/stderr pipes. It
waits, writes status/transcript/result evidence, attempts cleanup, releases or
retains resource claims, and exits. There is no controller left running after
that lane reaches a terminal state.

The external neutral controller does the same type of work for the provider
named by its invocation. When its optional overlay receipt is present, its
current Codex path also derives session-level hook settings and trusted-project
settings before building `codex exec`; those external native-hook changes are
not part of the frozen campaign controller.

## 8. How board locks are actually used

**Neutral-harness part.** The controller has a generic file-lock feature. A
normal coding lane can request any exact non-shareable resource name, such as a
service or test-fixture name. The controller writes lock files under a
`resource_lock_root`; if none is supplied, it defaults to
`<runtime_root>/coding-resource-locks`. The lock acquisition, wait/recheck,
and cleanup proof described below are generic controller behavior.

**Campaign-only part.** The campaign bootstrap manifest has a list such as:

```json
{
  "exclusive_resources": ["STM-A"]
}
```

Campaign bootstrap writes that list into `invocation.json`. It also writes the
lock folder as:

```text
<runtime_root>/coding-resource-locks
```

After the temporary controller Python process starts, but before it starts
Codex, it creates one lock file for each listed name in that folder. Each file
contains the controller process ID and start-time identity, the lane ID, and the
worker invocation ID.

The file name is not literally `STM-A.json`: the generic lock code hashes the
resource text with SHA-256 and adds `.json`. The JSON inside still says that the
resource is `STM-A`. For each requested resource, the controller creates that
file with an operating-system exclusive-create operation. It sorts the resource
names first, so two lanes requesting the same pair try them in the same order.
That is generic lock implementation, not board logic.

If another lane already has `STM-A`, the controller removes any partial locks
it acquired for its own attempt, then waits and checks the existing lock again.
It only removes an old lock after it can prove the recorded process is gone and
the lock file has not changed underneath it.

After the CLI exits, the controller checks that the CLI process and any child
processes it owns are gone. Only then does it delete its lock files. If it
cannot prove that, it leaves the lock file in place. The lock is therefore held
by the temporary controller process's recorded identity, not by ROOT and not
by the provider CLI itself.

The special meanings of `STM-A`, `NRF-A`, and `NRF-B`, the ban on STM-B, and
the requirement to match a hardware resource manifest are campaign-only rules.
The neutral lock engine does not know that a string names a board.

## 9. What the Stop hook does wrong in literal terms

**Neutral-harness part.** The installed provider Stop hooks reread their
worktree binding and then read the queue files named by that binding. In the
pointed-at neutral harness this shared manager-queue Stop check exists in the
Codex, Claude, and Qwen adapter paths. It is an adapter/harness design problem,
not a cache feature and not a firmware-campaign rule.

**Campaign-only part.** The frozen campaign automatically binds an executor
worktree to the epoch's shared manager queue through its `event_delivery`
manifest. It currently does so for Codex. That campaign wiring makes the
generic Stop-hook problem appear in a hardware lane, but it did not create the
problem.

For the campaign's Codex path, an unacknowledged queue event makes the Stop
hook tell Codex to continue instead of stopping. The code does not check whether
the worktree belongs to ROOT or to a worker. Claude and Qwen have their own
provider-specific Stop responses, but make the same shared-queue decision.

The literal Stop-hook work is: a provider starts the installed hook command;
that command reads the binding JSON in the current worktree; it constructs a
temporary router from `queue_root` and the stored manager IDs; it reads the
queue's pending-event state; then it asks the delivery coordinator whether
stopping is permitted. If the answer is no, the Codex hook calls its
continuation transport. The hook reports a JSON result and exits. It never
checks a field meaning "this binding belongs to ROOT," because no such field or
role check exists in that decision path.

That means this exact sequence can happen:

1. A worker has the same manager queue binding installed in its worktree.
2. The worker creates a result/event for ROOT.
3. ROOT has not acknowledged the event yet.
4. The worker's Stop hook reads the shared queue and sees the unacknowledged
   event.
5. The worker's Stop hook asks Codex not to stop.

The worker is then blocked by work that belongs to ROOT. That is an actual
shared-file behavior, not merely an unfortunate description of the design. It
would occur in a neutral non-firmware lane too when a worker is bound to the
same unresolved manager queue.

## 10. What exists today versus what does not

The following separates reusable harness code from the frozen campaign wrapper.

| Area | Neutral harness | Frozen campaign integration |
| --- | --- | --- |
| Cache | Optional caller-selected overlay and optional receipt. The product ships no cache payload. | Requires executor `overlay_cache` at the campaign's harness `super-cache` location and writes a receipt during bootstrap. |
| Provider adapters | Codex, Claude, and Qwen adapters own their own launch/hook files. | Executor bootstrap currently selects Codex and invokes its adapter automatically. |
| Event delivery | File-backed queue and per-provider bindings; no persistent manager service. | `event_delivery` manifest carries the epoch manager identity and makes delivery mandatory for executors. |
| Resource claims | Generic string-named locks with process-cleanup proof. | Limits hardware tokens to the campaign resource manifest, including STM-A/NRF-A/NRF-B rules. |
| Scan/watch | Optional diagnostic scan/diff tools. | ROOT is instructed to use a specific scan/watch sequence during an epoch. |

The quickest implementation-level way to tell the two apart is by the input
file that starts the work:

- In the neutral harness, the caller runs a direct overlay command with
  `--source`, `--harness-worktree`, `--super-cache`, `--worktree`, and
  `--receipt` paths. The controller later receives an ordinary lane invocation
  that may contain `overlay_receipt`. No receipt means the optional cache was
  not requested.
- In the frozen campaign, ROOT gives `lane_bootstrap.py` one campaign manifest.
  That JSON contains the source repository, experiment/runtime roots,
  worktree/branch names, task/resource references, `overlay_cache`,
  `event_delivery`, and `exclusive_resources`. Bootstrap creates the worktree,
  copies the overlay, installs/binds Codex when event delivery is present, and
  writes the invocation JSON that the controller later reads.

The important file readers are also different:

- `workspace_overlay.py` reads the cache source and writes the overlay receipt.
  It is generic. In the external harness the controller accepts a missing
  receipt; in the frozen campaign controller a coding/subagent invocation
  rejects a missing receipt.
- `lane_bootstrap.py` exists only in the frozen campaign copy. It reads the
  campaign manifest and turns campaign-specific fields into generic controller
  input fields.
- `lane_controller.py`, `provider.py`, `resource_locks.py`, and the queue code
  are the generic execution pieces. They are invoked for a lane, do their work,
  write files, and exit; they are not a resident harness service.

These are real, working local operations in the code:

- copy files from an input cache folder into a worktree and write a receipt;
- start a temporary controller process and a provider child process;
- write CLI output/status/result files;
- create lock files and keep them after uncertain cleanup;
- create/update queue JSON and JSONL files;
- install provider hook files and write queue-binding JSON files.

The frozen campaign additionally creates a Git worktree from its bootstrap
manifest and automatically prepares/binds its Codex executor worktree. Those
two automation steps are campaign-specific; the neutral harness instead gives
the caller public overlay and provider-adapter operations.

These are absent or limited in both harnesses:

- a permanent harness/manager program;
- automatic delivery of a changed queue file into ROOT's active agent context;
- a watcher that stays running after it prints a result;
- a watcher that reads the manager queue;
- one built-in configuration file that gives every command the same cache,
  runtime, lease, queue, and coordinator paths;
- a worker-safe Stop hook separate from a ROOT queue check;

The frozen campaign specifically does **not** use the pointed-at external
Claude/Qwen adapter work or its later native-hook repair. The external harness
reports live provider-native hook delivery separately from cache preparation;
that work has not been integrated into the campaign's frozen bootstrap.

The campaign's Codex adapter specifically still does not use the invocation's
`sandbox` field to enforce a real Codex sandbox.

## Source locations

- Worktree/bootstrap file writes: `lane_bootstrap.py:465-637`.
- Cache refresh/copy behavior: `workspace_overlay.py:158-220` and `349-602`.
- Controller and provider process creation: `public_launch.py:48-80`,
  `operator_launch.py:320-419`, and `lane_controller.py:2888-2918`.
- Codex command construction: `provider.py:406-442`.
- Queue file setup and acknowledgement: `notifications.py:364-460` and
  `1280-1371`.
- Queue binding file setup and installed Stop-hook path:
  `codex_adapter.py:1612-1672` and `1818-1885`.
- Foreground scan/watch loop and config flag: `cli.py:190-258`.
- Neutral external comparison: `<absolute-path>/harness-v2-firmware-runner/orchestrator_harness/provider.py:475-780`,
  `cli.py:400-470`, and the Codex/Claude/Qwen installer files. That checkout
  has no `lane_bootstrap.py`.
