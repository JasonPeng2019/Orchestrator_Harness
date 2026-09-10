# Harness v2 Tier 4 full implementation review

## What this document covers

This is a technical walkthrough of the complete `HARNESS-V2-TIER4` overhaul in
`harness-single`. It explains what existed at the plan's actual starting point,
what the original six-step Tier 4 plan replaced or added, what its final
addendum repaired, and how the shipped code actually performs those jobs.

It is deliberately about implementation, not project-management history. The
comparison is between these two commits in `harness-single`:

| Meaning | Commit |
| --- | --- |
| Candidate inspected when the original Tier 4 plan was admitted | `138b6adc61d0c2830fee94ea5166a0d083b89262` |
| Original Tier 4 product coordinate, before Addendum 2 | `7d74fb64d5644d20f1d2697328fc2fb4929af09e` |
| Current integrated candidate, including Addendum 2 | `f4328b177177a3aa71bf5f064b88ad6033b3d903` |

The current candidate was pushed to `working/firmware/v2-candidate`. Across the
full comparison, Tier 4 changed 402 tracked files: 15,988 lines added and
58,232 lines removed. The high deletion count is intentional: it includes
candidate-era campaign machinery and checked-in `.agent-workspace` execution
artifacts which do not belong in a clean v2 product. Addendum 2 is the final
23-file slice of that larger transformation.

The source paths below are relative to `harness-single/` unless stated
otherwise.

## The harness in one practical picture

Harness v2 is an execution boundary for a human or ROOT process that already
knows what work should be done. It prepares a Git worktree for one coding lane,
starts the chosen provider through a provider adapter, records durable state,
and makes cleanup and review observable. It does not decide the plan, select
the model, accept code, merge branches, or operate a scheduler.

The only public command is:

```powershell
python -m orchestrator_harness.operator_launch <command> ...
```

Every command returns the same small result shape:

```json
{
  "ok": true,
  "code": "STABLE_MACHINE_CODE",
  "summary": "short human-readable result",
  "evidence_paths": [],
  "next_action": "what to do next"
}
```

`--json` prints that object for callers. Without it, successes go to stdout and
failures go to stderr with a stable failure code. The dispatcher and parser are
in `orchestrator_harness/operator_launch.py`.

## What existed before the Tier 4 overhaul

The starting candidate was not empty. It contained a real, much older
candidate-era harness: controller/process code, provider-specific adapters,
watcher and release machinery, firmware/campaign compatibility surfaces, test
fixtures, and documentation. Some underlying ideas were useful and were kept in
spirit: isolated work, durable evidence, exact process identity, adapters, and
diagnostic observation.

It was not the v2 product defined by Parts I-XIX of the master specification.
The admitted plan explicitly treated the historical Appendix A as diagnosis,
not as a v2 contract. Its target-truth audit found a mixed candidate surface:

- many overlapping public routes (`public_launch.py`, `cli.py`, profile and
  provider modules, candidate watcher routes) rather than one v2 launcher;
- candidate/campaign state and numerous `.agent-workspace` run outputs checked
  into the product tree;
- provider, task, profile, lock, queue, and lifecycle abstractions whose
  ownership and records did not match the v2 schemas;
- firmware and watcher compatibility behavior mixed with the generic harness;
  and
- no complete, independent v2 acceptance map.

Tier 4 therefore was a replacement at the product boundary, not a compatibility
layer placed on top of the old implementation. It removed obsolete candidate
modules such as `public_launch.py`, `cli.py`, `profiles.py`, `provider.py`,
`providers.py`, `task.py`, `resource_locks.py`, `lane_lifecycle.py`, and legacy
checked-in runtime artifacts when no normative v2 consumer remained. It retained
only still-useful lower-level code where it could serve the new contracts.

## What the original Tier 4 plan built

The original plan delivers `DEL-001`: the coherent v2 product for REQ-001
through REQ-015. It was implemented in the current source tree, not in the
planning Markdown. The plan's six steps then independently admitted it, built
test assets, integrated them, performed static assurance, and reserved live
verification for real target CLIs.

### 1. One product boundary and one runtime tree

Tier 4 made the product a provider-agnostic local orchestration harness. It
does not contain hardware, firmware, campaign, MCP, or scheduler behavior.
`harness-config.json` supplies the absolute `root_workspace`; the code derives
the only mutable runtime root as:

```text
<root_workspace>/.harness-runtime/
```

`config.py` owns that validation and path derivation. `.gitignore` excludes the
runtime and per-worktree `.agent-workspace/` material, so a lane cannot pollute
the source checkout or accidentally become a product commit. The harness creates
its worktrees below controlled runtime locations and never pushes a lane branch.

### 2. Closed configuration, resource manifest, and setup

Tier 4 replaced loose candidate configuration with two closed versioned files:

- `harness-config/v1`: required absolute root workspace and optional
  `managed_coordination` value (`enabled` by default or `disabled`).
- `resource-manifest/v1`: the sole literal list of exclusive resource IDs.

`config.py` rejects unknown shape or invalid values. Later public commands load
the saved configuration; they do not add a second runtime path, profile switch,
or provider selection flag.

`setup.run_setup()` in `setup.py` is the single integration routine. It checks
configuration and manifest before it mutates state, stages and byte-verifies the
active super-cache, installs all shipped ROOT payloads/bindings, writes the
active manifest and empty lease directory, creates only profile-appropriate
runtime records, and starts one monitor. It is idempotent; `--overwrite` is its
only setup option. It starts no lane, provider, epoch, or worktree.

An active epoch freezes the facts that would change its meaning: workspace,
managed/plain profile, active manifest, manager queue identity/schema, and
runtime record version. Setup refuses an incompatible live change rather than
pretending the old lanes run under new configuration.

### 3. Explicit managed and plain profiles

The new default is managed coordination. A managed runtime has a manager queue,
per-lane worker inbox/outbox, installed hooks, and the two worker skills. Plain
mode is an explicit opt-out, not an error or reduced managed implementation. A
plain lane contains the checkout and normal controller/result records, but none
of the manager queue, worker coordination queues, coordination hooks, or worker
coordination payload.

That split is applied during setup and bootstrap rather than being inferred by a
worker at runtime. `setup.py`, `bootstrap.py`, `epochs.py`, and
`manager_queue.py` own the corresponding paths and records.

### 4. A shipped provider catalog and staged super-cache

Tier 4 added a simple catalog under `adapters/` for `codex`, `claude-code`, and
`qwen-code`. Each provider has:

- a ROOT payload (configuration, hooks, binding, and eight thin ROOT command
  skills);
- a managed worker payload (hooks, binding, and exactly `manager-notify` and
  `lane-assignment` skills);
- `harness/launcher_binding.py`, which exports the provider ID, adapter version,
  argument builder, and output-line parser; and
- adapter documentation and shipped-machinery notes.

The provider-neutral part lives in `super-cache/workspace/`: the worker
`.agent-workspace` skeleton plus the result checker, lane-queue helper, and
manager-notify helper. The `custom/` directory is intentionally file-only for a
local adapter extension; general lifecycle code does not need editing to stage
one.

During bootstrap, the code copies three sources into one lane: the common
managed base, the selected provider payload, and generated lane/run files.
`bootstrap.py` validates the provider's registered binding and creates a
runtime-specific binding file. A lane receives only its selected provider's
payload, never all three.

### 5. Versioned records, atomic writes, and one active epoch

Tier 4 introduced the v2 record/path layer in `core.py`, `records.py`,
`epochs.py`, and `lanes.py`. The product has versioned records for runtime
state, current epoch, epoch state, active-lane index, lane state, manager queue,
worker inbox, monitor, controller status/events, worker result, review,
acceptance, lease, overlay receipt, and invocation.

The record writer uses this pattern:

```text
short advisory lock
  -> write a validated JSON sibling in the same directory
  -> replace the old file atomically on the same volume
  -> always release the lock
```

It uses canonical JSON and SHA-256 content hashes for integrity links, not
signatures or identity claims. After an interrupted write, the next writer
parses and health-checks the real record; it does not accept an arbitrary
temporary sibling as a successful update.

An epoch is launcher-owned. It opens when the first lane is bootstrapped, has a
fresh ID and (in managed mode) fresh queue ID, contains every lane for that run,
and is closed only when the active-lane/event rules allow it or shutdown applies.
Lane IDs are supplied by ROOT and must be unique across the epoch, even after
retirement.

### 6. Bootstrap, launch, controller, and exact process ownership

`bootstrap.run_bootstrap()` validates lane ID, provider/model, task card,
exclusive resources, active configuration, and paths before it makes a
worktree. It then creates the controlled Git branch/worktree, prepares the
overlay and records, writes the truthful result template and invocation, and
returns a `prepared` lane. It never starts the provider itself.

`launch.run_launch()` consumes that prepared invocation. The long-lived
`controller.py` owns one provider process and its helpers for one running lane;
the short CLI does not retain those process handles. The controller records its
status, append-only events, transcript/stderr facts, result validation, cleanup
proof, and terminal lane state. It only writes facts for its own worktree.

`processes.py` identifies every owned process by PID plus creation time. It uses
platform-specific process primitives behind that common contract, so stop and
cleanup target exactly the process launched for that lane. A PID that has been
reused is not treated as the old process. The Windows work also corrected Job
Object startup/containment and batch-shim invocation through `COMSPEC` while
preserving the same higher-level identity rule on every platform.

### 7. Monitor, queues, hooks, and ROOT/worker separation

`monitor.py` is the one persistent process. Each pass reads the controlled epoch
and lane records, derives actionable status from durable facts, updates its
heartbeat and watched-lane count, and, for managed mode only, promotes a status
change into one deduplicated manager event. It does not discover arbitrary
worktrees or turn normal resource contention into a monitor event.

Tier 4 created three distinct coordination channels:

- The manager queue at its fixed runtime path is ROOT's managed inbox. The
  monitor is its event producer, ROOT changes event state, and a PostToolUse
  hook may append only a `DELIVERED` receipt.
- Each managed worker has its own inbox. Only
  `send-lane-notification` appends a `PENDING` assignment; the worker helper
  advances it.
- Each managed worker has an outbox for escalation. The monitor consumes each
  notification once and promotes it into the manager queue.

The provider-native hook files call shared dispatch/wrapper code:
`root_hook_dispatch.py`, `root_hook_wrapper.py`, and the staged worker helpers.
The hook boundary is deliberately narrow: it reports/delivers facts through the
authorized queue route and uses exact monitor/lane identities. Workers cannot
write ROOT's queue, and ROOT does not hand-edit worker queues.

`scan_watch.py` supplies read-only `scan`, foreground `watch`, and public health
reconciliation. Monitor recovery detects dead, hung, and deliberately stopped
states from its record and uses the monitor lock; it never starts a second
monitor over a live exact identity or resurrects a deliberately stopped one.

### 8. Leases, review, resume, retirement, and shutdown

`leases.py` implements named opaque resource leases. Launch acquires every
requested declared lease under the lease lock or acquires none and returns
`LAUNCH_LEASE_BUSY` before starting a provider. Normal cleanup proves the
controller boundary is gone before releasing its leases.

The worker's `RESULT.json` is not an acceptance decision. `review.py` validates
its schema, lane/run identity, content hash, task card, and source commit. ROOT
then writes a linked `COMPLETION_REVIEW.json` and
`ORCHESTRATOR_ACCEPTANCE.json` outside the worktree. A non-PASS finding cannot
be accepted normally; force acceptance needs an explicit recorded reason.

`resume.py` gives a stopped, unaccepted lane a fresh run ID and replaces only
the current-run artifacts in the required order. The product records the
resume/review boundary so stale results and old hook artifacts cannot affect a
new run. `launch.py` also owns targeted force-stop and graceful retirement;
`shutdown.py` closes the runtime. None of those paths kills a broad process
name. Cleanup and archive proof come before normal lease release or worktree
retirement.

### 9. One public CLI, usable docs, packaging, and portability

Tier 4 collapsed the public surface onto
`python -m orchestrator_harness.operator_launch`. Its groups are:

```text
harness setup|shutdown
lane bootstrap|launch|completion-review|force-stop|retire
resume-lane
manager acknowledge|close
send-lane-notification
scan | watch | health reconcile|monitor-recover
```

Every route produces the same five-field result object, stable machine code,
human summary, evidence paths, next action, JSON option, stdout/stderr split,
and exit status. The operator README and quick start show the real route rather
than re-implementing lifecycle behavior in shell instructions. Addendum 2 later
added the `lease force-release` group and made a nonblank close summary required;
those final-surface changes are described separately below.

The package metadata was updated so provider bindings, super-cache material,
and required assets are included in a built distribution. Paths use `Path`
operations and generated runtime locations rather than hard-coded host paths.
The portable fixtures deliberately use a temporary root with spaces and fake
process identities to verify cross-platform assumptions without calling that
fake work live provider evidence.

### 10. Independent tests and the original six-step plan

Tier 4 added the v2 acceptance suite under
`orchestrator_harness/tests/v2_acceptance/`. It has CHECK-U1 through CHECK-U5
for product layout/configuration/epoch behavior, profiles/catalog/monitor/queue
behavior, lifecycle/lease/review/resume behavior, records and CLI behavior, and
portable disposable behavior. The test assets keep their fixture oracles
separate from product code.

The master plan's steps were:

1. Admit the exact master-spec contract and clean target/frozen revisions.
2. Build and accept the v2 product (`DEL-001`).
3. Build and accept independent verification assets (`DEL-002`).
4. Integrate both accepted tips.
5. Run accumulated static assurance, including the full suite, compile/import,
   hygiene, documentation, and independent review.
6. Run the authorized native provider matrix (`DEL-003`).

Steps 1-5 produced the integrated static candidate. Step 6 has a real-world
prerequisite and is described honestly in the live-evidence section below.

### Master-spec-to-code crosswalk

This is the complete functional coverage of the original master plan. It is a
map to the implementation, not a claim that a source read alone proves a
provider ran live.

| Master-spec part | What Tier 4 implemented | Primary code/data home |
| --- | --- | --- |
| I-II | Provider-agnostic harness boundary, product/runtime/worktree layout, and actor ownership | `README.md`, `config.py`, `epochs.py`, `bootstrap.py` |
| III | Managed default and plain opt-out with different materialized files | `config.py`, `setup.py`, `bootstrap.py` |
| IV | Shared super-cache and three staged adapter sets with ROOT/worker payload separation | `super-cache/`, `adapters/`, `provider_adapters/` |
| V | Closed v2 configuration and resource manifest | `config.py`, `harness-config.json`, `resource-manifest.json` |
| VI | Idempotent setup, cache/binding trust checks, fresh v2 state, and monitor start | `setup.py` |
| VII | Single active epoch and immutable epoch facts | `epochs.py`, `lanes.py`, `bootstrap.py` |
| VIII | Bootstrap, controller invocation, lane state, and provider ownership | `bootstrap.py`, `launch.py`, `controller.py` |
| IX | Persistent monitor, status derivation, event deduplication, liveness and recovery | `monitor.py`, `scan_watch.py`, `setup.py` |
| X | Manager queue, per-worker inbox/outbox, and native hook dispatch | `manager_queue.py`, `events.py`, `root_hook_*.py`, staged helpers |
| XI | Declared opaque leases, all-or-nothing launch acquisition, cleanup-before-release | `leases.py`, `launch.py`, `controller.py` |
| XII | Worker result validation plus separate ROOT review and acceptance records | `review.py`, `records.py` |
| XIII-XIV | Resume, targeted force stop, accepted retirement, shutdown, and Git hygiene | `resume.py`, `launch.py`, `shutdown.py`, `processes.py` |
| XV-XVI | Actionable remediation, versioned schemas, canonical hash links, locks, atomic records | `operator_launch.py`, `records.py`, `core.py`, `epochs.py` |
| XVII | One public command grammar and stable result/error convention | `operator_launch.py`, user READMEs |
| XVIII | Cross-platform paths, process identity, packaging, and disposable fixtures | `processes.py`, `records.py`, package metadata, `examples/v2_disposable_fixture.py` |
| XIX | Native live matrix contract and explicit evidence boundary | `examples/v2_live_matrix.py`, `tests/v2_acceptance/contract.py` |

## What Addendum 2 added after the original Tier 4 delivery

The addendum closes three concrete product gaps and adds an independent
acceptance layer around the full requirement inventory.

### Change A: ignore generated harness runtime files

File changed: `.gitignore`

The candidate now ignores `.harness-runtime/` in addition to the pre-existing
worker runtime material. This is intentionally a small change. Runtime records
are evidence and operational state, not source code; allowing them into a Git
diff makes a lane's output look like a product change and can accidentally
pollute a commit.

This does not move or rename runtime state. It only tells Git not to treat a
runtime directory produced by a normal harness run as a source file to stage.
`tests/v2_acceptance/test_baseline_product_oracles.py` checks both this rule and
the existing `.agent-workspace/` ignore rule.

### Change B: a safe public orphaned-lease recovery command

Files changed:

- `orchestrator_harness/operator_launch.py`
- `orchestrator_harness/leases.py`
- `tests/test_lease_force_release.py`

#### New command

The only public recovery route is now:

```powershell
python -m orchestrator_harness.operator_launch lease force-release --resource-id <id>
```

It is intentionally a top-level `lease` command group. It is not an
undocumented direct-file edit and it is not a `lane force-release` alias.

#### What the CLI does

`_lease_force_release()` in `operator_launch.py` performs the command-level
work:

1. It finds the harness root and loads the saved configuration and resource
   manifest.
2. It refuses an undeclared resource. This prevents a typo from being turned
   into a deletion request against a made-up lease path.
3. It uses the configured runtime root, not the current shell directory.
4. It provides `force_release_lease()` with a callback that can look up the
   current active lane for the lease holder.
5. It converts the result into the standard five-field public result object.
   On failure, the `next_action` explains whether the operator should stop a
   real holder, retire/abandon a lane, repair an invalid record, or simply stop
   because no lease exists.

The parser also exposes the command in `--help` and dispatches it through the
same one-launcher entry point as every other public command.

#### What actually permits deletion

`force_release_lease()` in `leases.py` is the operation that may remove one
`*.lease` file. Its order is important:

1. It calculates the one lease path from the requested resource ID.
2. It takes the shared leases lock.
3. While holding that lock, it re-reads and schema-validates the current lease
   record. It confirms that the record's `resource_id` still equals the command
   argument and that `lane_id`, `run_id`, PID, and process creation time are all
   present and valid.
4. It resolves the current lane **while the lease lock is still held**. That
   prevents a stale lane proof from being used after a different lease state is
   observed.
5. It checks the exact PID-plus-creation-time holder identity.

There are only two ways an orphaned record becomes releasable:

- The recorded process is gone, or the PID now belongs to a process with a
  different creation time. The latter means the old holder is gone and the PID
  has been recycled.
- The exact old process cannot be proven gone, but the durable current lane
  record proves that this lane is retired, abandoned, or is running a different
  `run_id`. That proves the lease belongs to an obsolete run rather than the
  current one.

If the exact recorded process is still live, the function returns
`FORCE_RELEASE_HOLDER_LIVE`. If the process cannot be proved dead and the lane
record does not prove that the old run is obsolete, it returns
`FORCE_RELEASE_HOLDER_UNPROVEN`. In both cases the lease file remains in place.

Only after that proof does the code unlink the one file. It immediately checks
that the path is no longer a file; an unlink error or failed readback becomes
`FORCE_RELEASE_DELETE_FAILED`, never a false success.

This is a correctness guard against stale identity and PID reuse, not a general
"are you sure" barrier. Once the caller names a declared resource and the
recorded holder is genuinely proven obsolete, the command performs the requested
release without an extra confirmation prompt.

#### Tests for the lease path

`tests/test_lease_force_release.py` directly tests the meaningful cases:

- A live exact holder is never released, even if a stale lane record says it is
  retired.
- A missing process can be released.
- A recycled PID can be released.
- An unobservable but still-current run cannot be released.
- Retired, abandoned, or superseded runs can be released.
- Missing, invalid, and resource-mismatched records return stable failure codes.
- The lane lookup happens after the lease has been re-read under the lock.

### Change C: atomic manager-queue updates and required close summaries

Files changed:

- `orchestrator_harness/manager_queue.py`
- `orchestrator_harness/operator_launch.py`
- `orchestrator_harness/review.py`
- `tests/test_manager_queue_atomicity.py`
- `tests/test_manager_queue_close.py`
- `tests/test_review_manager_close.py`
- `tests/test_operator_launch.py`

#### The queue transaction

Before the addendum, queue operations had record locking, but the full sequence
of read, epoch/header validation, mutation, and replacement was not guaranteed
to share one lock scope. Two writers could both read an old queue and then one
could replace the other writer's change.

The addendum gives all manager-queue writers one helper:

```text
_update_manager_queue(runtime, mutate)
  -> lock manager queue path
  -> read and schema-check queue
  -> compare queue epoch_id and queue_id with current epoch marker
  -> apply one mutation
  -> atomically replace the queue only if changed
  -> unlock
```

`promote_event`, `acknowledge_event`, `close_event`, and
`append_delivery_history` all call this helper. The shared helper keeps queue
ownership in one location instead of putting subtly different lock logic in
four writers.

`tests/test_manager_queue_atomicity.py` instruments the lock, queue read,
epoch-header read, and atomic replacement. It proves all four happen while the
same queue lock is held.

#### Required terminal summary

The command is now:

```powershell
python -m orchestrator_harness.operator_launch manager close `
  --event-id <id> --outcome COMPLETE|BLOCKED --summary <text>
```

There are two checks, deliberately at two boundaries:

1. `_nonblank_summary()` in the CLI strips whitespace and makes argparse reject
   a missing or blank `--summary` before dispatch.
2. `close_event()` validates again before it reads or mutates the queue. This
   keeps direct Python callers from bypassing the public-parser check.

For a valid close, `close_event()` trims the supplied text, changes the event
state to `COMPLETE` or `BLOCKED`, writes the normalized summary on the event,
and writes the same summary into the terminal history item. Therefore the
answer to "why was this event closed?" survives both in the current event view
and in its audit trail.

`tests/test_manager_queue_close.py` proves that `None`, an empty string, and
whitespace-only input fail before queue access, that no write occurs on that
failure, and that both terminal outcomes preserve a trimmed summary.

#### Completion review now obeys the same contract

`review.run_completion_review()` already wrote a linked review/acceptance pair.
For a managed review it now also calls `close_event()` with a generated,
nonblank summary such as:

```text
completion review recorded: PASS / ACCEPTED
```

The review pair remains the detailed durable evidence. The short queue summary
is a reliable state-transition explanation, not a replacement for that pair.
`tests/test_review_manager_close.py` checks that this internal call always
supplies a nonblank summary containing both the review outcome and approval.

### Change D: independent acceptance assets for the full addendum

Files added or changed below `orchestrator_harness/tests/v2_acceptance/`:

- `audited_gap_inventory.py`
- `gap_map.py`
- `candidate_boundary_oracles.py`
- `contract.py`
- `test_gap_map.py`
- `test_baseline_product_oracles.py`
- `test_atomic_concurrency.py`
- `test_live_matrix_contract.py`
- updates to `test_check_u3.py` and `test_claim_map.py`

These files are mostly **test and acceptance machinery**, not runtime behavior.
They make it possible to show exactly what was checked without putting a second
implementation of the harness into the tests.

#### The 82-gap inventory and map

`audited_gap_inventory.py` is a source-local snapshot of the 82 marked rows in
the master implementation checklist. It stores the checklist path, its SHA-256,
the selection rule, and the base candidate being audited.

`gap_map.py` maps each individual gap ID to one observable check. Each map row
names:

- the check and test class,
- the scenario and trigger,
- the expected observable result,
- required cleanup, and
- the invariant the test is protecting.

`test_gap_map.py` checks that the inventory has exactly 82 unique entries and
that every entry has exactly one complete map row. This prevents a checklist row
from quietly vanishing from test coverage.

#### Product-facing tests versus synthetic fixtures

The test suite deliberately separates three kinds of evidence:

1. **Product-facing tests** import and exercise the candidate itself. For
   example, `test_baseline_product_oracles.py` parses the actual public CLI and
   inspects the actual `.gitignore`.
2. **Synthetic/fixture tests** exercise an explicit disposable model or fake
   process where that is the appropriate way to test record, race, and cleanup
   contracts. `test_atomic_concurrency.py` is clear that its barrier and lock
   are a fixture oracle, not candidate code or live provider proof.
3. **Live-only tests** reserve claims that require a real native provider and
   host. `test_live_matrix_contract.py` proves that the live matrix remains
   marked `RESERVED_FOR_M09` until those real runs occur.

This separation is important. A fake process proves a fake-process property; it
does not prove that Codex, Claude Code, or Qwen Code actually ran correctly on a
native target.

#### Boundary oracles

`candidate_boundary_oracles.py` defines small observation-only assertions for
two subtle lifecycle boundaries:

- Resume must persist `resuming` before replacing current-run artifacts, and
  validate the fresh invocation before persisting `running`.
- A rejected review must create exactly one `LANE_RESUME_REQUIRED` event, owned
  by completion review, rather than duplicating it during resume.

The updated `test_check_u3.py` supplies both correct and deliberately mutated
candidate-observation sequences to prove that the oracles detect reversed or
duplicated behavior. The helper observes a public boundary; it does not tell the
product how to implement resume internally.

### Change E: documentation was made consistent with the implementation

Files changed:

- `README.md`
- `orchestrator_harness/README.md`
- `QUICK_START.md`

The user-facing documents now show the only recovery command as `lease
force-release --resource-id <id>`, rather than suggesting a non-existent lane
route. They also show `manager close` with its required `--summary <text>`.

This is not cosmetic. The public CLI rejects a missing summary, so an example
without it teaches a command that will fail. The documentation update was
reviewed again after the implementation change specifically to eliminate that
mismatch.

## How the complete Tier 4 implementation was assembled

The work was not one hand edit. The original Tier 4 replacement first removed
the obsolete candidate surface and built the v2 core; the final addendum then
closed gaps found by the independent implementation checklist.

| Commit family | Full-plan contribution |
| --- | --- |
| `3592641`, `125c906`, `9108896` | Independent v2 acceptance assets, runtime-ignore boundary, and atomic-write recovery test. |
| `a3c3fca`, `acf0785` | Closed v2 config and schema-bearing resource manifest. |
| `29c08c1`, `e3a7ddd` | Super-cache, provider adapter catalog, setup, and bootstrap materialization. |
| `f80aa67`, `487badf`, `6b3ef24` | Shipped package assets and collapse of candidate surfaces onto v2 consumers. |
| `b7387d1`, `6139dfe`, `068bc75` | Cross-platform exact process ownership and Windows Job/batch launch repairs. |
| `204aa0e` through `51a60e8` | Worker/ROOT hook dispatch, provider wrappers, monitor recovery, and installed ROOT payload binding. |
| `0cd3c9d`, `7d74fb6` | Deterministic launch cleanup/lease reuse and lane-queue acknowledgement correction. |
| `388fc04` through `f4328b1` | Addendum 2 coverage assets, safe orphan release, queue atomicity, and documentation correction. |

The final addendum itself is a merge of reviewed, narrow changes rather than one
large hand edit:

| Commit | Implementation contribution |
| --- | --- |
| `388fc04` | Initial independent acceptance inventory and mapping assets. |
| `06e378b` | Stronger acceptance boundary oracles. |
| `5cb76ea` | Initial safe lease recovery and manager-close summary implementation. |
| `b758917` | Repair: one atomic manager-queue transaction and lane proof resolved under the locked lease re-read. |
| `a691c09` / `c216cdf` | Documentation fixes for the public lease route and required summary. |
| `f4328b1` | Final integration of the accepted product and acceptance-test changes. |

The important point is that the later commits did not add alternative behavior.
They repaired two race/staleness windows in the first implementation:

- Queue validation and replacement are now one lock-protected transaction.
- Lease deletion now resolves the lane state only after re-reading the lease
  under its lock.

That keeps the final design small: one new lease command, one queue-update
helper, one summary contract, and tests that exercise their real boundaries.

## Final current behavior: an operator walkthrough

The following shows where the complete Tier 4 implementation takes effect in
normal use.

1. ROOT writes the closed harness configuration and resource manifest, then
   runs `harness setup`.
2. ROOT bootstraps and launches a lane. If it names a declared exclusive
   resource, the normal launch path creates its lease.
3. With managed coordination, the monitor emits a manager event. ROOT runs
   `manager acknowledge` and later must run `manager close` with a real summary.
   The close becomes an atomic, durable queue transition.
4. ROOT records `lane completion-review`. If it is a managed review, the review
   writer also closes its own manager event with the generated summary.
5. Normally, cleanup releases the lane's leases. If a lease is genuinely
   orphaned, ROOT runs `lease force-release --resource-id <id>`. The command
   verifies exact holder/lane evidence before deleting that one lease record.
6. Runtime files created during the run remain out of the source diff because
   `.harness-runtime/` and `.agent-workspace/` are ignored.

## What is deliberately not claimed as complete

The code and static/synthetic acceptance work are integrated. The project does
not claim that this alone is live proof for every provider and operating system.

The live matrix still requires real, authorized native runs for each provider's
ROOT and worker behavior, monitor recovery, queue isolation, and serial lease
reuse. Windows was available for readiness rehearsal. Native macOS and a native
Linux-storage runner were not available under the documented boundary, so
REQ-017 remains `INCOMPLETE` rather than being inferred from unit tests, WSL
mounts, fixtures, or transcripts.

That limitation is intentional and visible in
`tests/v2_acceptance/contract.py`, `test_live_matrix_contract.py`, and the
workspace-level `HANDOFF.md`. It is an evidence prerequisite, not a known
product-code defect.

## Source guide

| Need to understand | Start here |
| --- | --- |
| Public command grammar, dispatch, and structured results | `orchestrator_harness/operator_launch.py` |
| One safe orphaned-lease deletion | `orchestrator_harness/leases.py` |
| Queue writers, lock transaction, and close summary | `orchestrator_harness/manager_queue.py` |
| Review/acceptance records and managed review close | `orchestrator_harness/review.py` |
| Setup, staging, and installed provider material | `orchestrator_harness/setup.py` |
| Worktree and worker preparation | `orchestrator_harness/bootstrap.py` |
| Launch, cleanup, stop, and retirement | `orchestrator_harness/launch.py`, `shutdown.py`, `processes.py` |
| Durable lock and JSON replacement primitive | `orchestrator_harness/records.py` |
| User-level command reference | `README.md`, `orchestrator_harness/README.md`, `QUICK_START.md` |
| Full Tier 4 coverage contract | `master_planning/harness-v2-tier4/`, `orchestrator_harness/tests/v2_acceptance/` |

## Review method used for this document

This review was based on the Git diff from `138b6ad` to `f4328b1`, the original
Tier 4 plan and master specification, the current source files named above, the
current tests, and the accepted workspace handoff. It does not treat planning
documents or test names as proof that uninspected code exists. Where live
provider evidence is absent, this document says so.
