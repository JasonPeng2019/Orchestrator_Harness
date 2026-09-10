# Harness fixing recommendations

> **Status: supporting implementation notes.** These notes do not override
> the master planning document or the current detailed v2 target contracts.
> Candidate-era receipts, bindings, and cleanup practices are not implicit v2
> requirements.

## Make setup perform the one shared-cache ingest

The harness should ship the source cache, while setup creates the one working
copy that lanes actually use:

```text
<harness-root>/super-cache/  # shipped source; never edited by a run
  -> setup's verified initial copy
<runtime-root>/super-cache/  # active working copy; used by every lane
```

On first setup, the script should stage, byte-verify, and atomically create the
runtime copy from the shipped source. It then validates that the resulting
`<runtime-root>/super-cache` contains the required configuration and hook files.
The harness-root copy is product source, not mutable run state.

Later setup calls verify and retain the active working copy; they must not silently
replace it. Additional shared material is added only to the active runtime cache.
An explicit cache-refresh operation can replace that active cache after a deliberate
request and only when no lane is using it.

“Refresh” is not part of normal lane launch. It means deliberately rebuilding the
active runtime cache from the shipped source after the product-owned cache payload
has changed. A lane already prepared from the old cache does not change, so a
refresh while lanes are live would create mixed hook/skill versions. For a simple
extra shared file, ROOT adds it to `<runtime-root>/super-cache/custom/` before
launching lanes; no refresh is needed. A full refresh happens only after all lanes
have retired, and setup must reject it while one is active.

Every later lane bootstrap should use only the active runtime-cache path as its
`overlay_cache` input and copy its current contents into the new lane
worktree. A lane must not run cache ingest, select a different cache source, or
manually edit cache/hook files while the run is in progress.

The existing ingest command is useful specifically here: it stages the supplied
source folder, compares the staged files byte-for-byte, and atomically replaces
the shared `super-cache` folder only after that comparison succeeds. It is not
a per-lane operation.

## Require the configured shared-cache path in bootstrap

Current campaign bootstrap accepts any existing `overlay_cache` directory that
has the expected files. It does not itself require:

```text
<runtime-root>/super-cache
```

The separate campaign admission adapter currently checks that path instead.
That leaves the public bootstrap route able to prepare a lane from a different
qualifying cache directory when called without the adapter.

The bootstrap route should derive the one configured shared-cache path and
reject an executor manifest whose `overlay_cache` names anything else. The
admission adapter can keep its early preflight check, but bootstrap should
enforce the same final path rule at the point where it copies cache files into
the worker worktree.

## Use a launcher-owned shared cache with disposable worktrees

The intended model is one central active cache, populated from the shipped
harness source during setup:

```text
<harness-root>/super-cache  ->  <runtime-root>/super-cache
```

The launcher—not each caller or manifest—uses that exact folder every time it
creates a worker worktree. Before starting the provider, it copies the current
contents of that central folder into the root of the new worktree and writes a
receipt proving that copy completed for that exact worktree. A lane does not
select its own cache source, and it does not need to run a separate cache
prepare command.

The cache copy is one-way. Files written or changed inside a worker worktree
never modify `<runtime-root>/super-cache`.

At lane retirement, do not hand-remove cache files or create an archive, history
directory, or overlay-restoration workflow. Retain the existing lane record; the
operator may remove a retired worktree whenever they choose. The harness must not
require that old directory for later setup, monitor startup, epoch opening, or a
new lane. A stopped unaccepted lane is different: its own worktree is required to
preserve its provider session on resume, so manual removal returns
`RESUME_WORKTREE_MISSING` and a fresh lane is the honest next action.

The receipt proves that the launcher copied the configured central cache into this
worktree before the provider was started and identifies the files it generated. It
supports narrow overlay restoration during retirement; it does not claim that the
worker's later files are cache changes.

## Add a real launcher-owned bootstrap to the neutral harness

Confirmed against:

```text
<absolute-path>/harness-v2-firmware-runner
```

The pointed neutral harness has these separate pieces:

- `workspace super-cache ingest` currently refreshes `<harness-root>/super-cache`;
- `workspace prepare` copies a caller-named cache folder into a
  caller-named worktree;
- `adapter install` writes provider-specific hook/configuration files into a
  caller-named project;
- provider binding functions connect a caller-named project to a
  caller-named queue; and
- `operator_launch` starts a controller from an already-written invocation.

It has no `lane_bootstrap.py`, no public `bootstrap` command, and no single
operation that creates/prepares a worker worktree before provider launch. The
README's `my_cli_bootstrap.py` example is only a custom-provider registration
wrapper; it does not create a worktree, apply the super-cache, install hooks,
bind notifications, or write a complete lane invocation.

That is a design gap. The caller is currently expected to remember and perform
several independent setup commands in the right order. The harness has no one
place that can prove every worker was prepared the same way.

The neutral harness should provide one public bootstrap command or API. ROOT
must supply a small lane requestâ€”the source repository/base revision, lane
name, provider binding ID, provider model, task/prompt inputs, and declared
resourcesâ€”and the program carries out this exact finite sequence. Bootstrap
does not choose a provider or model.

1. Create one fresh, disposable Git worktree under the harness-managed worker
   root, derived as `<runtime-root>/worktrees/<epoch-id>/<lane-id>/`. Refuse
   an existing or ambiguous target; do not reuse an arbitrary caller worktree.
2. Derive the canonical cache location from the configured runtime root:
   `<runtime-root>/super-cache`. Do not accept a per-lane cache-source path.
3. Copy the central **base** cache into the new worktree root and write the
   completed overlay receipt there. Fail before provider launch if the
   copy/receipt fails.
4. Validate the lane's provider binding ID against the shipped adapter catalog,
   then install that exact provider payloadâ€”Codex, Claude Code, or Qwen Codeâ€”
   into the same worktree and record that lane's model value in the invocation. The
   adapter, rather than the cache, owns provider hook and configuration files.
   This payload installation is managed-only. Plain bootstrap records the same
   selected provider/model and uses the common launcher binding, but deliberately
   omits provider hook/configuration payloads.
5. In managed mode apply the selected **worker** binding. That worker receives
   its own queue and provider-specific worktree configuration. In plain mode
   there is no worker queue/binding/hook payload; the common launcher binding
   still starts the selected provider. ROOT is not bootstrap-bound: its static
   wrapper opens the fixed runtime manager queue only in managed mode and is a
   no-op in plain mode. Bootstrap must not bind every worker to one shared queue
   or install the ROOT-only Stop gate in a worker.
6. Write one validated invocation JSON that names the exact created worktree,
   provider, prompt/task inputs, and overlay receipt. Include queue/binding
   identity only for the managed profile; include a resource-lock identity only
   when either profile requests a declared exclusive resource.
7. Return a bootstrap result containing the worktree path, receipt path,
   adapter check result, invocation path, and managed queue/binding identity only
   when applicable. Only this result may be passed to the public controller
   launcher.

In short:

```text
lane request
  -> create fresh worktree
  -> automatically copy canonical base cache
  -> materialize the selected provider model (and managed payload when enabled)
  -> apply that worker's queue binding only when managed
  -> write verified invocation
  -> public launch
```

Bootstrap is not a persistent service and it is not a second scheduler. It is
a short, one-shot setup command that exits after it has created the prepared
worktree and written the required current lane records. The existing controller
remains responsible for the provider process, resource claims, status, cleanup
proof, and retirement; it does not create an archive or generation history.

With this command, callers no longer manually string together cache prepare,
adapter install, binding, and invocation-file creation. The launcher itself
becomes the one enforceable entry point for a correctly prepared subagent lane.

## Make exclusive resources a ROOT-authored setup input

The resource names that a lane may claim must not be free-form lane input and
must not live inside a worktree or one epoch directory. ROOT writes one fixed
source list before setup:

```text
<harness-root>/resource-manifest.json
```

`operator_launch harness setup` validates that list and writes the active copy
and the one shared lock parent:

```text
<runtime-root>/resources/RESOURCE_MANIFEST.json
<runtime-root>/resources/leases/
```

The source file contains exact neutral resource IDs, for example
`fixture-a` or `device-b`. The generic harness does not infer what an ID means;
a surrounding campaign may have stricter rules for its own resource names.

Every later lane bootstrap accepts `--exclusive-resource <id>` only when the
ID exists in the active runtime manifest. It derives the manifest and lease
paths itself, writes the selected IDs into the invocation, and accepts no
per-lane manifest or lease-root path. The temporary lane controller creates a
lock file only after launch, waits on contention, and deletes its own lock only
after it has proved its provider/helper processes are gone.

The lock directory belongs directly under `runtime-root`, not under an epoch.
V2 permits only one active epoch, but this runtime-wide location still gives
every live lane one simple shared exclusion point. ROOT never manually makes or
removes lease files; ROOT's authority is limited to the pre-run resource list.

A later setup call may verify the same manifest. If ROOT changes the source
list, setup must reject the update while an epoch is active or a live lease
remains. After public shutdown/retirement, ROOT may change the source list and
rerun setup to atomically replace the active copy. This is the smallest setup
contract that keeps the resource inventory stable while lanes are running.
