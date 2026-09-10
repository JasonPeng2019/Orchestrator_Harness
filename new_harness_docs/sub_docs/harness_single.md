# Harness-single master planning notes

## Authority and document status

This is the v2 decision index. A later reader starts here: a settled decision in
this document overrides an older recommendation or current-candidate description
elsewhere. The detailed target contracts below elaborate the master decision; they
do not re-open it.

| Document | Status and use |
| --- | --- |
| `setup-details.md`, `harness-epoch-runtime-record-location.md`, `harness-scan-watch-queue-disconnection.md`, `harness-completion-review-acceptance-mechanism.md`, `harness-resume-mechanism-repair.md`, `harness-provider-adapter-materialization.md`, and `harness-public-shutdown-process-ownership.md` | Current detailed v2 target contracts, subject to this master index. |
| `fix_overview.md` and `fixing_reccomendations.md` | Supporting implementation summaries. They are useful only where they agree with the master and the detailed target contracts. |
| `harness-detailed-architecture-review.md` and `harness-executor-stop-hook-manager-queue-coupling.md` | Historical diagnosis of the candidate and source-checkout split. Their old router/coordinator/binding details are not v2 runtime machinery. |
| `subagent_hooks.md` | Historical compatibility evidence: it proves native PostToolUse on Codex, Claude Code, and Qwen Code. Its candidate binding and coordinator protocol is not the v2 runtime protocol. |

## Current readiness

The v2 candidate has native headless PostToolUse evidence for Codex, Claude
Code, and Qwen Code. Each provider executed a real tool call and produced a
durable `DELIVERED` receipt for a bound manager queue. The master specification
may therefore treat explicitly bound PostToolUse notification as a validated
platform capability, not an open feasibility question.

The following product decisions are already settled:

- An epoch spans the whole unchanged managed run, not one plan section or lane.
  New lanes reuse it. A new epoch is opened only after shutdown/reconfiguration
  or an epoch-sensitive immutable change; it atomically replaces the one fixed
  runtime-level manager queue with a fresh queue ID, then publishes the new
  `CURRENT_EPOCH.json` marker before any worker launches. It never replaces or
  binds a ROOT session.
- The v2 MVP uses cooperative local trust. ROOT acceptance is an operational
  workflow decision, not a security guarantee against a malicious local writer.
- The revamp starts with a fresh v2 project-local runtime tree. It does not
  migrate or open old candidate queues, bindings, coordinators, or in-flight
  lane state.
- ROOT's project workspace contains the complete runtime tree at the derived,
  locally Git-excluded path `<root-workspace>/.harness-runtime/`. Runtime state
  is not a sibling path or a separate configured root.
- The current v2 deployment keeps `<harness-root>` itself inside
  `<root-workspace>`. Product code, adapter source, and any setup-updated adapter
  binding therefore remain project-local; making the harness workspace-agnostic is
  a later product change, not an MVP concern.
- Setup materializes `.codex/`, `.claude/`, and `.qwen/` ROOT payloads together
  in that workspace. There is no `root_provider` or `root_model` config field:
  ROOT is the already-running CLI, while only each lane gets a provider-specific
  worktree binding. A static custom adapter follows the same generic
  current-epoch-pointer contract. ROOT provider/session binding is explicitly
  out of v2 MVP scope: it adds process discovery, stale-session recovery, and
  restart/rebind failure modes without improving the proven hook path.
- Crash recovery is intentionally lightweight: malformed harness records may be
  discarded or rebuilt under their own record lock; no false acknowledgement or
  acceptance is inferred. Queue recovery does not quarantine or warn about a
  broken queue: it replaces it with an empty current-epoch queue. A valid
  terminal lane can receive a replacement completion-review request after health
  reconciliation.
- ROOT hooks use the one fixed path `<runtime-root>/manager/QUEUE.json`; there
  is no ROOT `.agent-workspace` binding file or per-epoch manager-binding file.
  `CURRENT_EPOCH.json` and the queue header must agree on the active epoch and
  current queue ID. Queue health may replace the fixed queue with an empty queue
  and a fresh ID **within the same epoch**; it atomically updates
  `CURRENT_EPOCH.json`, and a writer using the old ID returns `QUEUE_REPLACED`
  without writing. `active-lanes.json` remains a rebuildable monitor index, while
  each `lane.json` remains the authoritative lane record.
- A lane, not a generation tree, is the durable unit of work. Initial launch and
  each resume assign that same lane a fresh `run_id`; the public paths accept only
  artifacts whose `{ lane_id, run_id }` matches the current `lane.json`. Resume
  keeps the same worktree and provider session, clears obsolete current
  result/review state, and intentionally permits old rejected artifacts to be
  replaced rather than archived.
- The active shared super-cache and one persistent monitor are mandatory v2
  infrastructure, not feature flags. The resource manifest/lock facility and
  normal base worktree payload are likewise always available. A project with no
  hardware declares no resources; it does not disable lock machinery. Setup
  always creates/checks these facilities.
- The one compatibility setting defines two honest, epoch-immutable lane
  profiles. A **managed**
  profile enables the one optional **managed coordination** package: the manager
  event loop/delivery and worker provider configuration/hooks. A **plain**
  profile disables that one package: it still creates a normal worktree, prompt,
  controller, provider session, `RESULT.json`, lane record, active-lane index,
  monitoring, direct completion review, and resume path, but creates no manager
  or worker queue and enables no harness hook. Either profile may claim a
  declared exclusive resource through the same always-available lock facility.
  It is a
  complete ordinary provider lane, not a managed lane with missing prerequisites
  or a degraded error path. The selected profile is explicit configuration, not
  runtime detection; changing it opens a new epoch.
- A plain lane cannot wake or notify ROOT. This is the intentionally simple
  operating contract for a provider CLI that cannot use the harness hook/queue
  route: ROOT actively runs `scan --no-write` when resuming management work and
  `watch --until-actionable` while it is idle, then handles the returned lane
  status through the direct review/resume commands. No hook reminder, manager
  event, delivery receipt, or automatic wake-up is expected or fabricated.
- `<harness-root>/harness-config.json` is the sole authority for optional
  harness settings. Its only v2 compatibility flag is
  `managed_coordination`, which selects managed or plain. `harness setup` reads
  and validates that one file, then materializes the matching coordination
  facilities. Bootstrap, launch, resume, and adapter commands do not take
  feature flags, profiles, or per-lane overrides, and they do not infer a
  profile from a CLI at runtime.
- Worktrees belong only to the lane that is currently using them. A live lane
  and a resumable stopped lane require their own recorded worktree, but the
  harness never requires a retired lane's worktree to remain on disk. Operators
  may remove old worktrees themselves; later setup, epoch opening, bootstrap,
  monitor startup, and new-lane execution use controlled current records and
  never scan or validate retired worktrees. If an operator removes the one
  worktree of a stopped unaccepted lane, that lane cannot preserve its session
  on resume and returns `RESUME_WORKTREE_MISSING`; a fresh lane is then the
  honest path.
- Every replaceable harness file or directory stages as a unique temporary
  sibling of its final project-local destination, never in a system temporary or
  shared staging directory. For append-only files, the harness copies the last
  complete file to that sibling, appends there, validates, and atomically
  replaces; a successful replacement consumes the sibling and failure cleanup
  deterministically removes any unconsumed temporary.
- Setup returns its structured result to ROOT but writes no separate
  setup-evidence record. Shutdown uses one project-local runtime lifecycle state
  and the existing `monitor/MONITOR.json`; it does not create separate
  shutdown-marker or monitor-stop-request/acknowledgement files.

## Items the master specification must include

These are remaining specification/verification tasks, not unresolved MVP product
direction.

1. **Epoch-breaking-change table.** The immutable facts that require a new epoch
   are: the `root_workspace` (and therefore the derived runtime root); the
   `managed_coordination` profile (managed↔plain); the declared exclusive-resource
   set (the resource manifest); the manager-queue schema/`queue_id` (each epoch
   stages a fresh queue); and the runtime-record schema version. Explicitly
   **non-breaking** (they stay within the active epoch): adding or retiring lanes;
   ordinary task/plan content; ROOT's provider, model, and session identity; and
   each lane's own provider/model choice. Any breaking change is accepted only
   through the shutdown/retirement path (R2); the rest is refinement/verification.
2. **Versioned record schemas.** Define exact schema/version, required fields,
   state transitions, writer, reader, lock/atomic-write rule, health check, and
    recovery behavior for every persistent record: `RUNTIME_STATE.json`,
    `CURRENT_EPOCH.json`, `epoch-state.json`, `lane.json`, `active-lanes.json`, the
    fixed manager `QUEUE.json` **and** the per-lane worker-inbox
    `.agent-workspace/QUEUE.json` (these are two distinct records), monitor records,
    the controller's worktree records (`controller.status.json` — the monitor's
    actionable-status source — and the `controller.events.jsonl` event log), the
    worker's `RESULT.json` (the record that "structurally valid result" checks
    validate), completion-review records, and acceptance records; the lease-file
    and overlay-receipt formats should be pinned here too. Each record's version
    string follows the established `<record-name>/v1` convention (as in
    `manager-queue/v1`, `current-epoch/v1`); unify the mixed `harness-` prefixing
    of the existing strings while doing so. The ledger must also require every
    temporary write to be a same-directory sibling of its final project-local
    destination. **Complete in `harness-record-schemas.md`** — every record covered,
    and both returned decisions resolved (identity/hash = `sha256` over canonical
    JSON, integrity-only, no signing; `cleanup_unproven` = monitor-derived from the
    controller's `cleanup_proven` fact).
3. **One public CLI contract.** Collect every public command, required inputs,
   success output, stable failure code, next action, and ownership boundary in
   one place. This includes setup, bootstrap, launch, manager acknowledgement,
   send-lane-notification, completion review, resume, force-stop lane, retirement,
   shutdown, and health reconciliation. **Drafted in `harness-cli-contract.md`**
   (every command's inputs, success output, failure codes, next action, and
   ownership; the `setup-details` failure table reused verbatim, other codes marked
   as defaults); two points returned there — the `lane`-grouping of `resume-lane`/
   `send-lane-notification`, and the defaulted failure codes / `health reconcile` form.
4. **Native verification matrix.** Preserve the completed three-provider
   PostToolUse proof and add focused real-CLI tests for role-aware Stop behavior:
   reject unresolved ROOT/worker work, permit valid `PASS`/`FAIL`/`BLOCKED`
   completion, and verify that one role's queue never blocks another role.

## Boundary

The Stop-hook item is an acceptance-test requirement, not a reason to reopen the
validated PostToolUse design. The remaining work should refine and implement the
settled v2 contract without adding a security subsystem or a second scheduler.

## Resolutions added this revision

These points were opened as design-decision gaps or cross-document
inconsistencies during review and are now settled. Per the authority rule at the
top of this document, each decision below overrides any conflicting text in the
detailed target contracts; the detailed docs elaborate these decisions, they do
not re-open them.

### R1. Lane identity and resume scope

- Resume only ever targets a lane in the one active epoch. `resume-lane`
  resolves a bare `--lane-id` through `CURRENT_EPOCH.json` and that epoch's
  `lanes/` directory only; it never searches a retired epoch. There is no
  cross-epoch resume.
- A lane ID is unique for the lifetime of its epoch, **including retired lanes**
  (whose `lane.json` is retained). Bootstrap rejects a `--lane-id` already
  present in the current epoch's `lanes/` directory — a distinct
  `BOOTSTRAP_LANE_ID_IN_USE` result — whether or not the old worktree still
  exists on disk. A fresh unit of work always uses a new lane ID; a stopped,
  unaccepted lane is continued with `resume-lane`, not by reusing its ID.

### R2. Epoch reconfiguration does not migrate lanes

- Any change to an epoch-immutable fact — the `managed_coordination` profile,
  the resource manifest, the runtime root, or the enabled immutable feature set
  — is accepted only through the shutdown/retirement path. Setup rejects such a
  change while an epoch is active or a live lease remains; the guard already
  stated for the resource manifest applies equally to the profile flag.
- Opening a new epoch retires the previous epoch and all of its lanes. Paused,
  unaccepted lanes are **not** migrated, and there is no cross-epoch resume (R1).
  To carry work forward, the operator copies files from an old worktree into a
  fresh lane's worktree in the new epoch and starts a **new lane** from that
  state. This is not a resume and is not treated as one: it is an ordinary new
  lane that happens to begin from copied files, so — like every new lane — it
  starts a fresh provider session. No provider session or run history is expected
  to carry over, and none is; the lane simply continues the work from the file
  state it was given.

### R3. `LANE_RESUME_REQUIRED` is an ordinary ROOT event closed by the resume skill

- `LANE_RESUME_REQUIRED` is an ordinary ROOT manager event. It is acknowledged
  with `manager acknowledge` and closed with `manager close --outcome COMPLETE`
  exactly like any other ordinary ROOT event.
- The `resume-lane` **command** stays queue-free. The `resume-lane` **skill**
  carries the closure: it directs ROOT to acknowledge the event, run
  `resume-lane` with a new card, then close the event as `COMPLETE` with a
  summary naming the new `run_id`. If ROOT decides not to resume, it still
  closes the event (`COMPLETE`, summary "not resuming") so the ROOT Stop gate is
  not held open.
- The event is closed once ROOT has *acted on the request* (issued the resume,
  or decided against it), **not** when the lane is eventually accepted; holding
  it open until final acceptance would block ROOT's Stop gate for the entire
  redo, and the resumed run raises its own fresh completion-review event anyway.
  This also removes the prior contradiction in which the resume skill was said to
  "handle" the event while the command spec never touched the queue.

### R4. The monitor is the sole producer of ROOT inbox events

- The controller never writes the manager queue. On its terminal transition the
  controller records the result-validation outcome and sets an actionable lane
  status — `review_pending` for a structurally valid result, `result_invalid`
  for a missing/malformed/wrong-task/contradictory one — in its own worktree
  records (controller status + event log), in both profiles.
- The persistent monitor is the only writer of ROOT-targeted events. Each pass
  it derives every registered lane's current actionable status from the
  controller records and, on a **status change**, promotes exactly one event to
  ROOT's inbox in managed mode (or leaves the status for `watch` in plain mode),
  using the existing `last_reported_actionable_status` value as its only dedup.
  This deletes the prior "the controller is a permitted producer for this one
  event" carve-out and removes the dual-producer duplication risk.
- Boundary, stated once: the lane event log lives in the worktree and is a
  permanent, controller-owned audit record — it is **not** drained into the
  inbox, and the monitor does not move log entries. Two monitor input channels
  feed the one inbox: (a) actionable status changes derived from controller
  records, deduped by `last_reported_actionable_status`; and (b) worker-outbox
  files, consumed once by moving them to `processed-notifications/`. The
  controller owns worktree records; the monitor owns *producing* inbox events;
  ROOT owns *advancing and consuming* its events. "Sole producer" means the monitor
  is the only component that **creates** events — it does **not** mean the monitor is
  the only component that writes `QUEUE.json`. Three components write the queue file,
  each under the same short queue lock: the monitor (admits new events), ROOT
  (advances an event `PENDING`→`ACKNOWLEDGED`→`COMPLETE`/`BLOCKED` via the manager
  commands), and the managed PostToolUse hook (appends a delivery-history entry — a
  `DELIVERED` receipt that never changes the event's manager state; schema ledger
  §6). The **controller and worker never write the manager queue** at all — they use
  worktree records and the worker outbox. (The monitor's heartbeat is a
  `MONITOR.json` field, not a queue write.)

### R5. Symmetric worker inbox; plain has none

- The worker incoming inbox (`.agent-workspace/QUEUE.json`, `lane-queue.py`, the
  worker PostToolUse/Stop hooks, and the `lane-assignment` skill) is the
  symmetric counterpart of ROOT's manager inbox and is part of the managed
  package. It ships installed and active for Codex, Claude Code, and Qwen Code on
  every managed lane.
- Both inboxes are managed-only. A plain lane has no worker inbox, and
  `send-lane-notification` is a managed-only route: in a plain configuration its
  skill states it is unavailable and the command returns a clear failure. A
  *running* plain lane cannot be sent new instructions — the accepted plain-mode
  limitation. To give a plain lane new work, review/reject it and use
  `resume-lane`.

### R6. Manager-queue growth (accepted)

- Unbounded manager-queue growth is accepted for the MVP. The queue may be
  managed manually if it grows large; manual removal falls back to the existing
  empty-queue recovery (a fresh `queue_id`, pending events lost, never claimed
  handled). No compaction subsystem is added.

### R7. Git hygiene for worktrees

- The runtime tree, and therefore every lane worktree, is locally Git-excluded by
  default; that is what keeps worktree files out of ROOT's status/commits, and
  because lane branches are never pushed the remote stays clean. The exclusion
  does **not** clean up Git's own bookkeeping. Because operators may delete a
  retired worktree folder by hand, `harness shutdown` and epoch retirement run
  `git worktree prune` against the lane's source repository to clear the dangling
  `.git/worktrees/<id>` administrative entries. Local lane branches are retained
  (they hold the lane's committed work and are never pushed); the operator may
  delete them at will.

### R8. Resume clears the worker mailbox

- Under the lane-record lock, `resume-lane` empties the lane's worker incoming
  `.agent-workspace/QUEUE.json` to a valid empty queue carrying the fresh
  `run_id`, in addition to clearing the current `RESULT.json`,
  `COMPLETION_REVIEW.json`, and `ORCHESTRATOR_ACCEPTANCE.json`. Assignments carry
  the current `run_id`, and the worker Stop/PostToolUse hooks consider only
  assignments matching the current `run_id`, so no stale assignment from a prior
  run can block or be delivered to the resumed run.

### R9. Smaller items

- **Config closed key set.** `harness-config.json` is a closed schema with one
  required key, `root_workspace`, and one optional key, `managed_coordination`,
  which defaults to `enabled` when omitted (see R16); any other key returns
  `SETUP_CONFIG_INVALID`. (The runtime root is not a config key; it is always
  derived as `<root-workspace>/.harness-runtime/`. The `schema` version key
  belongs to the separate `resource-manifest.json`, not to `harness-config.json`.)
- **Actionable-status set.** The statuses the monitor promotes, and that plain
  `watch --until-actionable` returns, are enumerated as: `controller_exited`,
  `provider_exited_no_result`, `result_invalid`, `review_pending`,
  `cleanup_unproven`, `status_transcript_contradiction`, and `orphaned_lease`
  (a live lease held by a lane whose run is dead or retired — see R14). This is
  the closed input to the versioned-record-schema task (item 2 above). Each status
  reaches ROOT as a manager event: `review_pending` as `COMPLETION_REVIEW_REQUIRED`
  and `result_invalid` as `LANE_RESULT_INVALID` (their existing dedicated-flow
  events), and the remaining statuses as one generic `LANE_STATUS_CHANGED` event
  carrying the `actionable_status` field — the monitor already dedups on
  `last_reported_actionable_status`, so a distinct event type per status buys
  nothing. Resource contention is deliberately **not** in this set: a contended
  launch fails synchronously with `LAUNCH_LEASE_BUSY` (R14), so no running lane
  ever waits and
  the monitor has nothing to promote.
- **Closed-epoch safety on the ROOT hot path.** Epoch retirement clears
  `CURRENT_EPOCH.json` **before** it marks the epoch closed, so no window exists
  in which the marker points at a closed epoch; a crash in that window leaves no
  marker and the ROOT dispatcher simply no-ops. The dispatcher keeps validating
  only marker↔queue agreement and gains no epoch-state read on the tool-boundary
  path.
- **Lock ordering.** When an operation needs more than one lock it acquires them
  in the fixed order runtime-state → manager-queue → lane-record →
  resource-lease → monitor-record. In normal operation the monitor is the only
  multi-lock holder (manager-queue then lane-record); controllers take only the
  lane-record lock and ROOT takes only the manager-queue lock, so the order is
  never inverted. `monitor-record` is a **single** lock covering every operation
  on `MONITOR.json` — starting or replacing the monitor and writing fields such as
  `stop_requested` all take it — so a start can never race a stop. (This unifies
  what earlier text called a separate "monitor-start" lock; there is one
  `MONITOR.json` lock, named `monitor-record`. The "monitor-start *route*" remains
  the name of the start procedure, not a second lock.)
- **`health reconciliation`.** It is primarily an automatic function of monitor
  startup and each monitor pass — rebuild `active-lanes.json` from the epoch's
  controlled `lanes/` directory, discard malformed temporaries, and reissue a
  replacement review event or restore `review_pending` when a terminal result
  remains valid. It is also exposed as a public command ROOT may run manually;
  its full input/output contract remains part of the one-public-CLI-contract task
  (item 3 above).

### R10. Super-cache layout (was a cross-document inconsistency; refined for the managed-default model of R16)

- The active super-cache uses this canonical layout, resolving the top-level
  `.codex/`/`.claude/`/`.qwen/` versus `adapter-payloads/<provider-id>/` conflict
  in favour of the namespaced form:

  ```text
  <runtime-root>/super-cache/
    workspace/                       # the MANAGED provider-neutral base: the .agent-workspace
                                     #   skeleton plus the provider-neutral helpers
                                     #   result-stop-check.py, lane-queue.py, manager-notify.py.
                                     #   Copied for a managed lane (the default, R16).
    adapter-payloads/<provider-id>/  # per-provider managed payload: that provider's hook/config
                                     #   files and its two worker skills (manager-notify,
                                     #   lane-assignment). Copied for the selected provider only.
    custom/                          # optional caller additions
  ```

- Setup copies each shipped provider adapter's `super-cache/` tree to
  `adapter-payloads/<provider-id>/`. A **managed** lane (the default) copies
  `workspace/` plus `adapter-payloads/<selected-provider>/`, and bootstrap then
  *creates* the per-lane pieces that are not cache templates: the incoming
  `.agent-workspace/QUEUE.json`, the `manager-notifications/` outbox folder, the
  lane records, the task prompt, and the result template. A **plain** lane (the
  rare exception, R16) copies none of this: its base is empty, and its worktree
  is bootstrap-generated only — the task prompt, result template, controller/lane
  records, and an empty `.agent-workspace/` skeleton. So "the base is empty"
  describes the plain case; the managed base is `workspace/`.
- These three sources are a convenience for whoever implements bootstrap; to the
  operator they are one action. A lane's worktree is assembled by a single
  bootstrap materialization — some files copied from `workspace/`, some from the
  selected `adapter-payloads/<provider-id>/`, some generated fresh — not by three
  separate user-visible steps.
- Two clarifications worth stating, because they differ from the historical
  `workspace/` (executor-stop) layout and from a first reading of R12:
  - **Worker skills stay per-provider** in `adapter-payloads/<provider-id>/`
    (consistent with R11 and with setup-details, which copies only the selected
    provider's payload), *not* bundled into `workspace/`. This avoids copying
    every provider's skill folders into every managed worktree. (Confirmed: this
    is the intended cache organization, not the historical all-in-`workspace/`
    form.)
  - **The provider-neutral helpers in `workspace/` are shipped for every managed
    lane regardless of provider**, since they are provider-neutral; the
    "shipped-for-standard / fresh-made-for-custom" distinction of R12 therefore
    applies only to the per-provider `adapter-payloads/<provider-id>/` payload
    (shipped for Codex/Claude/Qwen, authored by the adapter for a custom CLI),
    not to these helpers.

### R11. Worker skill inventory and count (was a cross-document inconsistency)

- There are exactly two worker-side skills, both managed-only: `manager-notify`
  (worker asks ROOT for help) and `lane-assignment` (worker acknowledges,
  completes, or blocks a task ROOT placed in its inbox). With the eight ROOT
  skills — the original seven plus `force-stop-lane` (added for lane remediation;
  see "Operator responses to actionable statuses") — that is **ten** standard skill
  files per provider set. The earlier "eight skills" *total* (from before
  `lane-assignment` existed) and the "the cache owns only `manager-notify`"
  statement are both stale and superseded here. `lane-assignment` ships in each
  provider's `adapter-payloads/<provider-id>/` payload alongside `manager-notify`.
  (Monitor liveness is handled by a ROOT PostToolUse hook, not a skill — see R15 —
  so it does not add to the skill count.)

### R12. Worker helper provenance (was a cross-document inconsistency)

- The provider-neutral worker helper scripts ship in the super-cache for Codex,
  Claude Code, and Qwen Code and are copied into managed worktrees. For a custom
  provider whose adapter does not ship them, the harness writes the same generic
  helpers fresh at managed bootstrap. The helpers are provider-neutral and read
  their per-lane paths from the lane binding / `lane.json`, so the shipped copy
  and the freshly written copy are identical in content; adapters never author
  these helpers.

### R13. Parallelism is across lanes, not epochs (was a cross-document inconsistency)

- This is a parallel multi-agent system: many lanes run concurrently under one
  epoch, and the runtime-wide `resources/leases/` facility exists to give those
  concurrent **lanes** one shared exclusion point. The stale rationale referring
  to "two active epochs" is corrected to "concurrent lanes." The one-active-epoch
  invariant is unchanged. Concurrent *epochs* are explicitly not in scope; that
  would overturn an invariant repeated throughout the contracts and is a separate,
  larger change if ever intended.

### R14. Orphaned exclusive-resource leases escalate to ROOT

- **A lease is written at launch and held only while the lane's controller lives.**
  Bootstrap only *declares* a lane's exclusive resources (`--exclusive-resource
  <id>`) and takes no lease; the separate launch route obtains the
  controller-owned lease, and the controller releases it as soon as it has proved
  its own provider/helper processes are gone. A resource is therefore held only
  during that lane's active run — not reserved at bootstrap and not for the whole
  epoch — so a freed lease is immediately reusable in series by a later lane that
  needs the same resource. ROOT owns the declared resource list; the controller
  owns the live lease.
- A short read-modify-replace OS lock auto-releases when its process handle
  closes, but an exclusive-resource **lease** is a file under
  `<runtime-root>/resources/leases/` that persists if its holder dies. A crashed
  or retired lane can therefore leave a lease behind, and in the concurrent-lane
  model (R13) that would block any other lane requesting the same resource.
- A stale lease is **not** auto-reclaimed. Reclaiming it silently would hand a
  resource to a new lane without the cleanup proof the retirement/shutdown path
  requires before a lease is released, so a crashed holder's lease may have left
  hardware in an unknown state. Instead the monitor detects it — on a pass, a
  lease whose owning lane's current-run process identity (PID + creation time) is
  dead, or whose lane record is retired/abandoned, is an actionable condition —
  and promotes the `orphaned_lease` status to ROOT (managed) or surfaces it via
  `watch` (plain). There is no automatic reclaim, but the manual clear is a plain
  **force-release**: the harness enforces no cleanup-attestation policy on the
  operator. Its role is only to surface the condition — an exclusive lease whose
  holding lane is dead or retired, so the resource may have been left in an unknown
  state — and let ROOT decide. Given that report, the intelligent ROOT either
  clears/releases the lease and reuses the resource or escalates to the operator on
  its own; the harness does not mandate one path, it states what is wrong and lets
  ROOT choose the fix. The exact public release/clear command surface is part of
  the one-public-CLI-contract task (item 3 above).
- **Resource acquisition is fail-fast and all-or-nothing; ROOT orchestrates any
  wait.** The intended model does not assign exclusive resources concurrently —
  ROOT sequences lane launches so a resource is free before it launches a lane
  that needs it. If a launch does hit contention, it acquires every declared
  exclusive resource or none: if any is unavailable, it acquires none (releasing
  anything it momentarily claimed) and the launch **fails synchronously** with
  `LAUNCH_LEASE_BUSY` — no lane starts, and nothing is held partially. ROOT then
  does the waiting: it holds off and re-launches once the lane currently holding
  the resource finishes. So contention is still a wait, but a ROOT-orchestrated
  one, not an auto-waiting lane. Because no lane ever holds one lease while waiting
  for another — there is no waiting lane at all — there is no hold-and-wait and so
  no lease deadlock, and no fixed global acquisition order is required. There is no
  busy-retry; ROOT decides when to re-launch.

### R15. Monitor heartbeat and the ROOT monitor-liveness PostToolUse hook

- The monitor is the sole producer of ROOT events (R4), so a silently dead
  monitor would stop all ROOT event delivery. Detection and recovery is
  managed-only — it depends on a ROOT hook, which a plain epoch does not have;
  there, ROOT's own `scan`/`watch` polling surfaces a stale monitor and recovery
  is manual.
- **Heartbeat (liveness signal).** On each pass the monitor stamps
  `last_heartbeat_at` (with the watched-lane count) in `MONITOR.json`. That single
  small field is the whole heartbeat — the freshness signal the hook reads (below).
  The monitor writes **no** heartbeat event to the manager queue; its only
  manager-queue writes are the actionable status-change events of R4.
- **Liveness detection and recovery (the real mechanism) is a ROOT PostToolUse
  hook, not a skill.** The monitor's identity — its PID and creation time — is
  already recorded at the deterministic, concrete path
  `<runtime-root>/monitor/MONITOR.json` (which is under ROOT's workspace via
  `<root-workspace>/.harness-runtime/`). On each ROOT tool boundary, ROOT's
  managed PostToolUse hook makes **two** checks, both from the single small
  `MONITOR.json` it already opens (never the growing queue): (1) is that specific
  process — matched by PID **and** creation time, so a reused PID is not mistaken
  for the monitor — still alive; and (2) is the monitor's `last_heartbeat_at`
  within the last `X` minutes. If **either** check fails — the process is dead or
  absent, **or** the process is alive but its last heartbeat is older than `X`
  (a hung monitor) — the hook returns that fact into ROOT's context and directs
  ROOT to start a fresh monitor through the same monitor-start route setup uses:
  take the `monitor-record` lock, replace the stale `MONITOR.json` identity (and,
  for a hung monitor, first stop the stale process), and launch one monitor wired
  to the correct runtime root, epoch marker, `active-lanes.json`, and manager
  queue. The hook only detects and directs; ROOT performs the start.
- **"Deliberately stopped" means marked stopped *and* actually dead.** The hook
  leaves a monitor alone only when `MONITOR.json` is marked `stop_requested`/
  `STOPPED` **and** the process is confirmed dead — a cleanly completed deliberate
  stop (e.g., after shutdown). A stop mark is not by itself a reason to do nothing;
  it is combined with the liveness result the hook already has:
  - dead **and** marked stopped → clean shutdown; the hook does nothing.
  - dead with **no** stop mark → a crash; the hook restarts it.
  - alive but stale (hung) with no stop mark → hung; the hook restarts it.
  - marked stopped but still **alive** → the stop did not take effect; this is not
    a clean stop, so the hook does not silently ignore it, but it also must not
    start a second monitor while one is live — it surfaces the anomaly to ROOT and
    lets ROOT resolve it.
  Because ROOT invokes shutdown as a single blocking call and cannot act until it
  returns, no restart can interleave *during* shutdown; this guard covers the one
  tool boundary immediately after shutdown returns, where the record is marked
  stopped and the process has exited. The check reuses the `MONITOR.json` read and
  the liveness result the hook already has, so it adds nothing to the tool-boundary
  path.
- **Cross-platform.** Both checks are platform-neutral, consistent with the
  harness's cross-platform portability principle (see the design principle at the
  end of this document): a process existence-plus-start-time check and a
  timestamp comparison are implementable identically on Windows, macOS, and Linux
  (for example through a cross-platform process API). No part of this mechanism
  may hardcode a platform assumption.
- **Reliability note.** With the staleness check added, the hook now catches both
  a dead monitor and a hung one (alive but no longer making passes). This whole
  path is a belt-and-suspenders for a rare case — ROOT is almost always active
  unless it too crashes, in which case recovery is manual: the ROOT agent inspects
  what is and is not alive, kills stragglers, and restarts from a fresh setup.
- The heartbeat interval `X` needs a defined default (and is reused as the
  staleness threshold); it is part of the versioned-record-schema task (item 2
  above). `X` must be set **comfortably larger than the monitor's pass interval**,
  so a healthy monitor that is simply between passes is never read as hung.
  Recommended starting default: a ~30-second monitor pass and `X` ≈ 3 minutes
  (several passes of margin, which absorbs normal pass jitter on a busy host);
  finalize the exact values in the schema and verification tasks.

### R16. Managed is the default profile; plain is the exception

- Managed coordination is the normal, default behavior. `managed_coordination`
  is omitted in the common case and defaults to `enabled`; the resulting managed
  lane gets the full package (manager queue, worker inbox and outbox, ROOT and
  worker hooks, provider worktree configuration, and the `workspace/` +
  `adapter-payloads/<provider-id>/` materialization of R10). This intentionally
  reverses the earlier "no implicit default" stance: the overwhelmingly common
  case should not have to state the profile.
- Plain (`managed_coordination: "disabled"`) is a deliberate, explicit opt-out
  reserved for the rare, eccentric CLI that cannot support native hooks or the
  provider config the managed package needs. A plain lane runs through the same
  launcher/controller but with no coordination package: no queue, inbox, outbox,
  hooks, worker skills, or copied worker payload — its worktree is
  bootstrap-generated only (R10), and resource safety (leases) still applies
  (R14). Plain is the exception, not a co-equal mode; the contracts describe it
  so a hookless provider is still launchable, not because it is expected.

## Operator responses to actionable statuses (remediation)

The monitor surfaces each actionable status to ROOT as a manager-queue event
(managed) or via `scan`/`watch` (plain); this section says what ROOT is expected
to *do* about each. Two framing rules first:

- **Closing an event is not resolving the condition.** `manager close` records that
  ROOT handled the *notification*; it does not change the lane's ground truth. A
  status clears only when the underlying fact changes (e.g. a stuck process finally
  exits, so `cleanup_proven` becomes true). If ROOT closes an event while the
  condition persists, the monitor's `last_reported_actionable_status` dedup keeps it
  from re-alerting, but the condition stays truthfully recorded in the lane records
  and its consequences (a held lease blocking new launches, an un-retirable lane, a
  later shutdown failure) resurface on their own. ROOT is trusted to act, not
  policed — the harness reports ground truth and never claims a close "fixed" it.
- **`resume-lane` re-does the task; it does not clean up a finished one.** Resume is
  for "the work must run again" (fresh `run_id`, fresh session). It is the wrong
  tool for a lane whose work is done but whose teardown is stuck.

Expected response per status:

| Status | What it means | ROOT's response |
| --- | --- | --- |
| `review_pending` | Terminal, structurally valid result awaiting review | Run `lane completion-review` (`--review-outcome` + `--approval`). `PASS`+`ACCEPTED` finishes the lane; otherwise `resume-lane` to redo. |
| `result_invalid` | `RESULT.json` missing or malformed | Review it (typically `FAIL`/`REJECTED`), then `resume-lane` to redo, or `lane force-stop` / retirement to abandon. |
| `provider_exited_no_result` | Provider exited without producing a result | Inspect transcript/stderr; `resume-lane` to retry, or `lane force-stop` / retirement to abandon. |
| `controller_exited` | The lane controller process died | Investigate; `resume-lane` to restart the run, or `lane force-stop` to clean up (which also clears the now-orphaned lease). |
| `status_transcript_contradiction` | Recorded status disagrees with the provider transcript's terminal state | Establish the lane's true state; `resume-lane` if work must redo, else `lane force-stop`. |
| `cleanup_unproven` | Task done, but the lane's processes will not exit (controller alive, `cleanup_proven` still false) | Clear the straggler so the live controller finishes teardown and drops the lease; if it will not clear or the controller is wedged, `lane force-stop`. |
| `orphaned_lease` | An exclusive lease held by a lane whose run is dead or retired | Force-release the lease (R14) before reusing the resource. |

### `force-stop lane` — the targeted single-lane hard stop

`operator_launch lane force-stop --lane-id <lane-id>` forcibly terminates one named
lane's processes — its provider, helper processes, and its controller, matched by
the PID+creation identities recorded in `lane.json` — then **force-releases any
exclusive lease that lane held** and marks the lane `retired`. It is the targeted,
single-lane counterpart to `harness shutdown` (which does this for the whole
runtime), and the escalation for a lane stuck in `cleanup_unproven` or whose
controller is itself wedged. Because it force-releases the lease without the
graceful cleanup-proof handshake, ROOT owns the safety decision — the same
operator-owns-the-risk stance as the R14 orphaned-lease force-release. It works in
both profiles, selected by `--lane-id`. It is exposed as a public route and as the
ROOT skill `force-stop-lane` (the eighth ROOT skill, R11); its exact inputs,
outputs, and failure codes are consolidated in the one-public-CLI-contract task.

The harness is cross-platform and targets Windows, macOS, and Linux equally. No
component, contract, helper, hook, or launcher may hardcode a platform
assumption. Concretely:

- **Paths.** Path examples in these documents use forward-slash notation for
  readability; they are illustrative. An implementation joins and stores paths
  with the host's native separator and must not assume a particular one. No
  drive-letter or platform-specific absolute-path form is normative.
- **Process identity and liveness.** A process is identified by its process ID
  plus its start/creation time and checked for liveness through a cross-platform
  process API — never a platform-specific call.
- **Launcher and scripts.** "The launcher" and "a helper script" mean the
  platform-native entry point; no specific extension (`.cmd`, `.ps1`, `.sh`) is
  normative, and shell examples use platform-neutral syntax.
- **No platform-specific vocabulary is normative.** Terms such as reparse point,
  junction, drive letter, or a specific OS's environment-variable names must not
  appear as requirements; use neutral descriptions (symbolic link or path
  redirection; a system temporary directory; the operating system).
- **Filesystem semantics.** The harness relies only on portable guarantees —
  same-volume atomic rename/replace and advisory process-scoped file locks — not
  on any one OS's filesystem behavior.

Where a historical/diagnosis document describes the prior external harness, it
may still name that system's platform specifics as a matter of record; those are
descriptions of the old system, not requirements of this design.
