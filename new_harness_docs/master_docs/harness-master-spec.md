# Harness — Master Specification (v2)

**This document is the single canonical specification for the harness.** It is
self-sufficient: every mechanism, decision, record schema, and command needed to
implement any part of the product is contained here. If this file and the other
harness documents ever disagree, **this file wins**. The other documents
(`harness_single.md`, `harness-record-schemas.md`, `harness-cli-contract.md`,
`setup-details.md`, `README.md`, `harness-epoch-runtime-record-location.md`,
`harness-scan-watch-queue-disconnection.md`,
`harness-completion-review-acceptance-mechanism.md`,
`harness-resume-mechanism-repair.md`,
`harness-provider-adapter-materialization.md`,
`harness-public-shutdown-process-ownership.md`, `fix_overview.md`,
`fixing_reccomendations.md`) are absorbed into this one; the historical/superseded
material among them is preserved in **Appendix A** and is explicitly *not* part of
the v2 specification.

> **Notation.** Path examples use forward slashes for readability; an implementation
> joins and stores paths with the host's native separator and must never assume a
> particular one. Abbreviations: `<harness-root>` = the installed harness product;
> `<root-workspace>` = the project workspace `root_workspace` points at; `<rt>` =
> the derived runtime root `<root-workspace>/.harness-runtime`; `<worktree>` = a
> lane's Git worktree. Record schemas are in Part XVI; the CLI is in Part XVII.

> **Settled-decision (`R#`) key.** In-text labels like `R4` or `R14` are the settled
> resolutions from the source authority `harness_single.md`; they are absorbed into
> this spec, so look them up here: **R1**→I.3/VIII/XIII, **R2**→VII, **R3**→XIII,
> **R4**→IX.2/X.1, **R5**→X.3, **R6**→X.1, **R7**→XIV.4, **R8**→XIII.2, **R9**→V/VII/IX/XVI,
> **R10**→IV, **R11**→IV.4, **R12**→IV, **R13**→I.3/XI, **R14**→XI, **R15**→IX.3,
> **R16**→III/V.

---

## Table of contents

- **Part I — Overview, vocabulary, and design principles**
- **Part II — Directory and file layout**
- **Part III — Profiles: managed and plain**
- **Part IV — Super-cache and provider adapters**
- **Part V — Configuration**
- **Part VI — Setup**
- **Part VII — Epochs**
- **Part VIII — Lanes: bootstrap, launch, and the controller**
- **Part IX — The persistent monitor**
- **Part X — Coordination: manager queue, worker inbox, worker outbox, and hooks**
- **Part XI — Resources and leases**
- **Part XII — Completion review and acceptance**
- **Part XIII — Resume**
- **Part XIV — Force-stop, retire, and shutdown**
- **Part XV — Operator responses to actionable statuses (remediation)**
- **Part XVI — Record schemas (all records)**
- **Part XVII — Public CLI contract (all commands)**
- **Part XVIII — Cross-platform portability**
- **Part XIX — Remaining work**
- **Appendix A — Historical diagnosis and candidate protocol (NOT the v2 spec)**
- **Appendix B — Source-document to master-section map**

---

# Part I — Overview, vocabulary, and design principles

## I.1 What the harness is

The harness is a **provider-agnostic orchestration harness** operating under
**cooperative local trust**. A running agent CLI (the **ROOT**) spawns and supervises
subagent worker CLIs, each isolated in its own Git worktree — a unit called a
**lane**. The harness ships first-class support for **Codex, Claude Code, and Qwen
Code**, and a file-only **adapter** format so any other stdio agent CLI can be added
without touching harness code.

Everything mutable the harness produces at runtime lives under a single, locally
Git-excluded runtime tree, `<root-workspace>/.harness-runtime/` (`<rt>`). The
project's own repository is never polluted: worktree files stay out of ROOT's
status and commits, and lane branches are never pushed.

The harness does **no hardware, environment, or campaign work**. It never flashes a
board, operates a device, starts an MCP server, or performs domain tasks. Its job is
strictly orchestration: prepare isolated lanes, start and supervise provider
processes, route events and assignments, arbitrate exclusive resources, mediate
review/acceptance, and tear down cleanly. Any hardware or environment action is the
responsibility of the work running inside a lane or of an external campaign layer.

## I.2 Actors and their lifetimes

- **ROOT** — the long-running orchestrator agent CLI the operator drives. ROOT issues
  the public commands, reviews results, and decides remediation. ROOT is trusted; the
  harness reports ground truth to ROOT and never polices it.
- **The launch route** — a short-lived program invoked per lane operation (bootstrap,
  launch, resume, force-stop, retire). It validates inputs, acts, and returns. It is
  **not** an agent and holds no long-lived state. It owns creating/retiring epochs and
  lane records.
- **The lane controller** — one long-lived supervisor process **per lane**, started by
  the launch route. The controller starts and cleans up the lane's provider process,
  writes the lane's worktree execution records, validates the worker's result, holds
  the lane's exclusive lease(s), and proves its own process cleanup. The controller —
  **not** ROOT — owns live leases and the provider process.
- **The persistent monitor** — exactly one process per runtime, the only actor that
  persists across lanes and epochs. It derives each lane's actionable status and, in
  managed mode, is the **sole producer** of ROOT-inbox events. It is started by setup
  and supervised by a ROOT liveness hook.
- **The worker** — the provider process inside a lane's worktree, doing the actual
  task. It reads its own inbox (managed) and writes its result; it never reads another
  lane's files and never writes the manager queue.

## I.3 Core vocabulary

- **Epoch** — one whole stable run of the harness. Exactly **one epoch is active at a
  time**. An epoch groups the lanes launched under one unchanged immutable
  configuration. Parallelism is across concurrent **lanes within** the active epoch —
  never across epochs.
- **Lane** — one unit of delegated work: a Git worktree (a branch checkout of the
  project) plus its controller, records, and (managed) coordination files. Identified
  by an operator-chosen **`lane_id`**, unique for the epoch's lifetime including retired
  lanes.
- **`run_id`** — an opaque, harness-generated identifier for one provider run of a lane.
  Resume assigns a fresh `run_id`; hooks and records filter by the current `run_id` so
  stale-run artifacts are ignored.
- **Profile** — a per-lane, **epoch-immutable** choice of `managed` (default; full
  coordination package) or `plain` (rare opt-out; no coordination package). See Part III.
- **Super-cache** — the runtime's provider-neutral + per-provider material that bootstrap
  overlays into each worktree. See Part IV.
- **Adapter** — the file-only package that teaches the harness one provider (its ROOT
  payload, worker payload, and launcher binding). Codex/Claude/Qwen ship as adapters;
  others are added the same way. See Part IV.
- **Manager queue** — the managed profile's single authoritative ROOT-event queue
  (`<rt>/manager/QUEUE.json`). Distinct from a lane's **worker inbox**
  (`<worktree>/.agent-workspace/QUEUE.json`).

## I.4 Design principles (normative)

These principles govern every part; later parts elaborate them.

1. **One active epoch.** The launcher opens an epoch only when none is active and reuses
   the active one for later lanes while its immutable configuration is unchanged. A new
   epoch is opened only after the current one is retired (shutdown) or an
   epoch-immutable fact changes.

2. **The monitor is the sole *producer* of ROOT events** (managed). Only the monitor
   *creates* inbox events, by deriving lane status from controller records and promoting
   one event on a status change. "Sole producer" does **not** mean sole *writer* of the
   queue file — see principle 3.

3. **Three components write the manager queue, each under the same short queue lock:**
   the monitor (admits new events), ROOT (advances an event's state via the manager
   commands), and the managed PostToolUse hook (appends a delivery-history "DELIVERED"
   receipt that never changes an event's manager state). The controller and worker
   **never** write the manager queue; they use worktree records and the worker outbox.

4. **Report ground truth; ROOT decides.** The harness surfaces conditions (a bad result,
   a stuck process, an orphaned lease); it does not enforce remediation policy. Closing a
   notification never changes ground truth — a condition clears only when the underlying
   fact changes. ROOT, being capable, acts or escalates. The harness never claims a
   ROOT action "fixed" anything it cannot observe.

5. **Cleanup-proof-first for resources.** A lane's exclusive lease is released only after
   the controller proves its own provider/helper processes are gone (or a forced path
   accepts the operator's risk). This prevents handing a resource to a new lane while a
   zombie process still uses it.

6. **Fail-fast, ROOT-orchestrated resource contention.** Exclusive resources are declared
   at bootstrap and acquired atomically at launch (all-or-nothing). A contended launch
   fails immediately (`LAUNCH_LEASE_BUSY`); no lane sits waiting. ROOT sequences launches
   and re-launches once the holder finishes, so resources are shared in series.

7. **Atomic, local, lock-guarded writes.** Every record that can be replaced is written
   as a unique temporary sibling in the destination's own parent directory, validated,
   then atomically renamed under that record's short lock. A crash leaves either the old
   or the new complete file, never a half-written one. The harness relies only on portable
   guarantees: same-volume atomic rename and advisory process-scoped file locks.

8. **Cross-platform.** The harness targets Windows, macOS, and Linux equally. No
   component hardcodes a platform assumption. See Part XVIII.

9. **Managed is the default; plain is a rare, explicit opt-out** for a CLI that cannot
   support native hooks. Plain is complete (review/acceptance and leases still work), not
   a degraded error path.

10. **Records carry integrity, not identity proof.** Cross-record links use a `sha256`
    content hash plus ids; records are not signed. Under cooperative local trust this
    detects mismatched/mis-linked records, which is all that is required.

---

# Part II — Directory and file layout

The spec treats two roots as distinct; it does not require them to be the same
physical directory. `<harness-root>` is the harness product/code; `<root-workspace>`
is the project workspace `root_workspace` points at, where ROOT runs and where the
runtime tree and ROOT payloads are installed.

## II.1 `<harness-root>` — the shipped product (setup treats it as read-only source)

```text
<harness-root>/
  harness-config.json          # ROOT authors: root_workspace (+ optional managed_coordination)
  resource-manifest.json       # ROOT authors: closed list of exclusive resource IDs (or [])
  README.md                    # ROOT operating guide
  adapters/                    # shipped provider catalog
    README.md                       # guide for adding a non-shipped provider
    codex/  claude-code/  qwen-code/     # each: root/  super-cache/  harness/launcher_binding.py  README.md  shipped-machinery/
  super-cache/                 # SOURCE cache: workspace/ (+ custom/)
    workspace/                      # provider-neutral base: .agent-workspace/ skeleton + result-stop-check.py, lane-queue.py, manager-notify.py
    custom/                         # optional shared additions
  orchestrator_harness/        # harness implementation + the operator_launch CLI
    provider_adapters/<provider-id>/launcher_binding.py    # registered launcher bindings (shipped)
```

Setup writes nothing here except registering a **custom** provider's
`launcher_binding.py` under `orchestrator_harness/provider_adapters/<custom-id>/` if
one is added; for the three shipped providers it only installs/checks.

In the current v2 deployment, `<harness-root>` itself is kept **inside**
`<root-workspace>`, so product code, adapter source, and any setup-updated adapter binding
remain project-local; making the harness workspace-agnostic is a later product change, not
an MVP concern. Worktrees belong only to the lane currently using them: a live lane and a
resumable stopped lane require their own recorded worktree, but the harness never requires a
*retired* lane's worktree to remain on disk. Operators may remove old worktrees themselves;
later setup, epoch opening, bootstrap, monitor startup, and new-lane execution use
controlled current records and **never scan or validate retired worktrees**.

## II.2 `<root-workspace>` — before setup

```text
<root-workspace>/
  .git/
  ...your project files...
  # no .harness-runtime/, and no harness-installed .codex/.claude/.qwen payloads
```

## II.3 `<root-workspace>` — after setup

Setup installs the three ROOT payloads and builds the runtime tree. The runtime tree
is locally Git-excluded by default so worktree files never enter status/commits.

```text
<root-workspace>/
  .git/
  ...your project files...

  .codex/                      # ROOT payload — all three installed; the running CLI uses only its own
    config.toml   hooks.json   orchestrator-harness-binding.json   bounded-launchers.json
    hooks/  orchestrator_harness_post_tool_use.py  orchestrator_harness_stop.py  orchestrator_harness_bounded_policy.py
    policies/bounded-exclusions.gitignore
    skills/  manager-notification-watch/ acknowledge-manager-notification/ close-manager-notification/
             review-lane-completion/ send-lane-notification/ resume-lane/ force-stop-lane/ harness-shutdown/   (SKILL.md each)
  .claude/   # settings.json, hooks/…, orchestrator-harness-binding.json, same 8 ROOT skills
  .qwen/     # analogous (also orchestrator_harness_notification.py hook)

  .harness-runtime/            # = <rt>, Git-excluded
    RUNTIME_STATE.json              # OPEN
    monitor/MONITOR.json            # written once the monitor starts
    manager/QUEUE.json              # idle managed queue (managed profile only)
    resources/
      RESOURCE_MANIFEST.json        # active copy of the source manifest
      leases/                       # empty; a lease appears only while a lane holds a resource
    super-cache/                    # active copy of the cache
      workspace/                        # base overlaid into every worktree
      adapter-payloads/codex|claude|qwen/   # per-provider hooks/config + 2 worker skills
      custom/
    epochs/                         # EMPTY until an epoch opens
    worktrees/                      # EMPTY until a lane is bootstrapped
```

`CURRENT_EPOCH.json`, `epochs/<epoch-id>/…`, and `worktrees/…` are **not** created by
setup — epoch-open and bootstrap create them later (Parts VII–VIII).

## II.4 A lane's worktree and record folder

Bootstrapping a lane creates a Git worktree **and** an outside-worktree record folder.
The split is deliberate: the worker may write inside its worktree, but the review and
acceptance records it must not forge live outside it.

**Inside the worktree** `<rt>/worktrees/<epoch-id>/<lane-id>/` (managed shown; items
marked *managed* are absent from a plain lane):

```text
<lane worktree>/
  ...a full checkout of the project, on its own branch...
  RESULT.json                    # the worker's result file (worker-written)
  ...worker evidence files...
  .agent-workspace/
    controller.status.json       # controller status snapshot (monitor's status source)
    controller.events.jsonl      # controller execution-event log (append-only audit)
    invocation.json              # the controller invocation bootstrap wrote; launch consumes it
    provider-transcript.jsonl  provider-stderr.txt  last-message.txt
    result-stop-check.py         # managed: helper the Stop hook runs
    hook-dispatch.py  harness-hook-binding.json  overlay-receipt.json   # managed: hook machinery + copy receipt
    QUEUE.json                   # managed: worker inbox from ROOT (send-lane-notification appends)
    lane-queue.py                # managed: helper to acknowledge / complete / block an assignment
    manager-notify.py            # managed: helper to raise an escalation
    manager-notifications/       # managed: escalation outbox
    processed-notifications/     # managed: escalations the monitor has consumed
  .codex/                        # managed: provider payload copied from the active cache
    hooks.json  orchestrator-harness-binding.json  hooks/…
    skills/manager-notify/SKILL.md  skills/lane-assignment/SKILL.md   # the 2 worker skills
```

**Outside the worktree**, the lane's record folder
`<rt>/epochs/<epoch-id>/lanes/<lane-id>/` (controller/ROOT-owned):

```text
<rt>/epochs/<epoch-id>/lanes/<lane-id>/
  lane.json                      # authoritative lane metadata: identity, run_id, paths, state, last_reported_actionable_status
  COMPLETION_REVIEW.json         # written only by the completion-review route
  ORCHESTRATOR_ACCEPTANCE.json   # written only by the completion-review route (ROOT's decision)
```

A **plain** lane's worktree has the checkout, `RESULT.json`, the controller-written
`.agent-workspace/` files (`controller.status.json`, `controller.events.jsonl`,
`invocation.json`, transcript/stderr/last-message), but none of the *managed* items
(no worker inbox/helpers, no escalation outbox, no hook machinery, no provider
hook/config payload, no worker skills). Its `lane.json` still lives in the record
folder outside the worktree.

---

# Part III — Profiles: managed and plain

A lane's profile is fixed by the `managed_coordination` config setting (Part V), is
**immutable for the epoch's lifetime**, and changing it opens a new epoch.

## III.1 Managed (the default)

`managed_coordination: "enabled"` (the default when omitted). A managed lane gets the
full coordination package:

- The runtime **manager queue** (`<rt>/manager/QUEUE.json`) — ROOT's inbox, produced by
  the monitor.
- A per-lane **worker inbox** (`<worktree>/.agent-workspace/QUEUE.json`) for ROOT→worker
  assignments, plus the `lane-queue.py` helper.
- A per-lane **worker outbox** (`manager-notifications/`) for worker→ROOT escalations,
  plus the `manager-notify.py` helper.
- **Hooks**: ROOT PostToolUse (delivery notice + monitor-liveness, Part IX) and Stop
  (gate); worker PostToolUse (delivery notice) and Stop (reject unresolved work/invalid
  result).
- The provider **worktree configuration/binding** (`orchestrator-harness-binding.json`,
  provider hooks) and the **two worker skills** (`manager-notify`, `lane-assignment`).
- The persistent monitor pushes events to ROOT; ROOT learns of events via a hook notice
  and consumes the queue.

## III.2 Plain (rare, explicit opt-out)

`managed_coordination: "disabled"`. Reserved for an eccentric CLI that cannot support
native hooks or the provider config the managed package needs. A plain lane runs
through the same launcher/controller but with **no** coordination package: no manager
queue, no worker inbox/outbox, no hooks, no worker skills, no copied worker payload.
Its worktree is bootstrap-generated only. **Resource leases still apply.**

Plain is **not** auto-accept and **not** a degraded error path — review/acceptance is
still done through the same public command. Because a plain lane cannot wake ROOT
(no queue, no hooks), ROOT polls: it runs `scan --no-write` when returning to
management and `watch --until-actionable` while deliberately idle (Parts IX, XVII).

## III.3 What plain deliberately lacks (stated once)

No manager event, no manager queue, no hook notice/Stop gate, no delivery receipt, no
automatic wake-up, no `LANE_RESUME_REQUIRED` event, no worker inbox/outbox, no worker
skills. A declared hardware lease, when requested, remains normal controller behavior.

---

# Part IV — Super-cache and provider adapters

## IV.1 The super-cache

Setup installs one active super-cache at `<rt>/super-cache/`, copied from the shipped
`<harness-root>/super-cache/` source plus the per-provider adapter payloads. Layout:

```text
<rt>/super-cache/
  workspace/                          # provider-neutral base for every managed lane
    .agent-workspace/                     # skeleton bootstrap copies into a worktree
    result-stop-check.py  lane-queue.py  manager-notify.py   # provider-neutral helper scripts
  adapter-payloads/<provider-id>/     # per-provider payload: hooks/config + the 2 worker skills
  custom/                             # optional caller additions
```

- `workspace/` is the **managed base**: the `.agent-workspace/` skeleton and the three
  provider-neutral helpers, copied into every managed worktree. These helpers ship for
  all managed lanes regardless of provider (the "shipped-standard vs made-fresh-for-
  custom" distinction of principle applies only to `adapter-payloads/<provider-id>/`).
- `adapter-payloads/<provider-id>/` holds that provider's hooks/config and its **two
  worker skills** (`manager-notify`, `lane-assignment`). Only the selected provider's
  payload is copied into a given managed worktree.
- A **plain** lane copies only the base content its normal provider run needs; it does
  not receive the queue/hook payload or worker skills.

## IV.2 Bootstrap materialization (one action, three sources)

To the operator, a worktree is assembled by a **single bootstrap materialization**;
the "three sources" are only an implementation convenience:

- Copied from `workspace/`: the provider-neutral helpers + the `.agent-workspace/`
  skeleton.
- Copied from `adapter-payloads/<selected-provider>/`: that provider's hooks/config and
  its two worker skills.
- **Generated** by bootstrap (not from the cache): the incoming worker `QUEUE.json`, the
  `manager-notifications/` outbox, the lane records, the worker prompt, the
  truthful-result template, and the controller `invocation.json`. `lane.json` is written
  outside the worktree.

## IV.3 The adapter catalog and adding a provider

The shipped catalog is `<harness-root>/adapters/<provider-id>/`. Each adapter tree is:

```text
<harness-root>/adapters/<provider-id>/
  README.md                 # what to put below (per-tree)
  root/                     # -> installed into <root-workspace> as the provider's ROOT payload
    <provider dotdir>/...        # e.g. .codex/{config, hooks.json, hooks/, orchestrator-harness-binding.json, skills/<8 ROOT skills>}
  super-cache/              # -> installed into <rt>/super-cache/adapter-payloads/<provider-id>/
    <provider dotdir>/...        # worker hooks/config + skills/{manager-notify, lane-assignment}
  harness/launcher_binding.py    # -> registered under <harness-root>/orchestrator_harness/provider_adapters/<provider-id>/
  shipped-machinery/        # documentation for the adapter author
```

Within this document, `adapter/` is shorthand for "the selected `adapters/<provider-id>/`
tree." The single adapter-author guide is `<harness-root>/adapters/README.md`. In v2,
**binding is performed by setup and bootstrap** — there is no standalone
`adapter install`/`check`/`bind` public command (that belongs to the historical
candidate protocol, Appendix A). Each `harness/launcher_binding.py` must define the strict
symbols `PROVIDER_ID`, `ADAPTER_VERSION`, `build_argv(...)` (assemble the provider's headless
launch argument vector), and `parse_line(...)` (read the provider's output); the controller
loads the single registered binding and checks that its `PROVIDER_ID` matches before use.

## IV.4 Skills inventory (ten per provider set: eight ROOT + two worker)

**Eight ROOT skills** (in each provider's `root/<dotdir>/skills/`), each a thin wrapper
over an existing public command:

1. `manager-notification-watch` — when deliberately idle, use `watch --until-actionable`.
2. `acknowledge-manager-notification` — after reading events, `manager acknowledge --event-id`.
3. `close-manager-notification` — `manager close --event-id --outcome COMPLETE|BLOCKED`.
4. `review-lane-completion` — run `lane completion-review` (finding + approval).
5. `send-lane-notification` — `send-lane-notification --lane-id --prompt`.
6. `resume-lane` — `resume-lane` for a stopped, unaccepted lane with a new task card.
7. `force-stop-lane` — `lane force-stop --lane-id` to hard-stop one stuck lane.
8. `harness-shutdown` — `operator_launch harness shutdown` to end the whole runtime.

**Two worker skills** (managed only; in each provider's `adapter-payloads/<id>/…/skills/`):

- `manager-notify` — raise an escalation via `.agent-workspace/manager-notify.py`.
- `lane-assignment` — acknowledge/complete/block a ROOT assignment via
  `.agent-workspace/lane-queue.py`; escalate a block with `manager-notify.py`.

Monitor liveness is a ROOT PostToolUse **hook**, not a skill (Part IX), so it does not
add to the skill count. Worker skills are per-provider by design (avoids copying every
provider's skills into every worktree).

## IV.5 Skill contract — what each `SKILL.md` must instruct

Each skill is a thin instruction wrapper over an existing public command; none implements
polling, queue mutation, bindings, or hooks itself. Required content:

- **`manager-notification-watch`** — say exactly when ROOT uses `watch --until-actionable`:
  only after ROOT has finished its current task and is deliberately waiting for worker
  activity; the command occupies the current ROOT CLI session while it waits; ROOT must not
  start it while actively working, and must handle the returned actionable report before
  starting another wait. It is an operational instruction, not a background process or a
  replacement queue.
- **`acknowledge-manager-notification`** — after finishing the current ROOT task, inspect the
  fixed manager queue **read-only**; for every top-level event ID ROOT actually read, run
  `operator_launch manager acknowledge --event-id <id>`. Never edit `QUEUE.json`.
- **`close-manager-notification`** — finish an acknowledged ordinary ROOT event via
  `operator_launch manager close --event-id <id> --outcome COMPLETE|BLOCKED --summary "…"`.
  Never edit the queue or restart a lane; completion review closes its own event.
- **`review-lane-completion`** (profile-aware) — managed: handle an acknowledged
  `COMPLETION_REVIEW_REQUIRED` event, compare its copied task criteria/result/evidence, and
  run `lane completion-review --event-id …`; plain: identify the controlled terminal
  `review_pending` lane and run the same command with `--lane-id`. `--review-outcome` and
  `--approval` are two independent both-required fields (`ACCEPTED` requires `PASS`); a
  stale-source error normally means resume; `--force-accept --force-reason` only after
  inspecting a harmless current-record difference; `REJECTED` creates a `LANE_RESUME_REQUIRED`
  event (managed) or direct resume-required output (plain). Never edits review/acceptance/lane
  files directly; never restarts a provider itself.
- **`send-lane-notification`** — use the public `send-lane-notification` command with the lane
  ID and prompt.
- **`resume-lane`** — for a stopped, unaccepted lane, use `resume-lane` with a new resume task
  card, truthful rationale, and current instructions. Do not reconstruct a session, PID,
  worktree, invocation, or amendment/hash record.
- **`force-stop-lane`** — to hard-stop one stuck lane, use `lane force-stop --lane-id`; it
  terminates that lane's provider/helper/controller, force-releases its lease, and marks it
  retired. For one lane; use `harness shutdown` for the whole runtime. Do not kill by broad
  process name or edit lease/process records.
- **`harness-shutdown`** — run `operator_launch harness shutdown` when intentionally ending
  the run. Do not close terminals, kill by broad process name, or edit process/lease records;
  preserve failed-shutdown evidence and do not retry with broad kills.
- **Worker `manager-notify`** (managed only) — when ROOT intervention is needed, run
  `.agent-workspace/manager-notify.py` with the decision/action needed; do not hand-edit
  manager queue files.
- **Worker `lane-assignment`** (managed only) — for a ROOT assignment, use
  `.agent-workspace/lane-queue.py` to acknowledge/complete/block it; escalate a block with
  `manager-notify.py`; never hand-edit either queue.

---

# Part V — Configuration

Configuration is a **closed** two-key set in `<harness-root>/harness-config.json`,
plus the ROOT-authored resource manifest. ROOT never passes paths, feature flags, or
a profile again on any later command — the stored config selects everything.

## V.1 `harness-config.json`

```json
{
  "root_workspace": "<absolute-path-to-project-workspace>",
  "managed_coordination": "enabled"
}
```

- **`root_workspace`** (required) — the absolute path to the project workspace. The
  runtime root is always **derived** as `<root-workspace>/.harness-runtime/`; it is not
  a second configured path. Changing `root_workspace` opens a new epoch.
- **`managed_coordination`** (optional) — `enabled` (default when omitted) or
  `disabled`. Selects the profile (Part III). Immutable per epoch; changing it opens a
  new epoch.

This is the only feature-settings step; the setting selects managed vs plain before
setup runs. (Schema string: `harness-config/v1`.)

There is **no** `root_provider` or `root_model` config field: ROOT is the already-running
CLI, and only each *lane* gets a provider-specific worktree binding. Binding a ROOT
provider/session is explicitly **out of v2 MVP scope** — it would add process discovery,
stale-session recovery, and restart/rebind failure modes without improving the proven hook
path. Bootstrap, launch, resume, and adapter commands likewise take no feature flags,
profiles, or per-lane overrides, and never infer a profile from a CLI at runtime.

## V.2 `resource-manifest.json`

The single ROOT-authored source list of exclusive resource names a lane may claim:

```json
{
  "schema": "resource-manifest/v1",
  "resources": [
    { "id": "fixture-a", "exclusive": true },
    { "id": "device-b", "exclusive": true }
  ]
}
```

A project with no hardware writes the same file with `"resources": []`; this does not
remove the generic resource-lock facility. Names are literal; any meaning belongs to a
surrounding campaign policy, not the harness. The manifest lives at the harness root
(not inside any worktree or epoch directory) and is not an epoch-local file ROOT can
rewrite mid-run. Setup copies it to the active `<rt>/resources/RESOURCE_MANIFEST.json`;
that generated file is what every later bootstrap uses. Changing the source manifest
is an epoch-immutable change: setup refuses it while an epoch is active or a lease is
live, so changing it requires shutdown → a new epoch.

---

# Part VI — Setup

Setup integrates the harness into the workspace. It is **idempotent** and starts no
lane or provider.

## VI.1 The ROOT-facing sequence (one-time)

1. **Start your supported CLI (ROOT) in the project workspace.** Setup installs static
   project files for all three shipped providers; the running CLI later discovers only
   its own folder. For a custom provider, finish its adapter tree first (Part IV.3).
2. **Fill `<harness-root>/harness-config.json`** (Part V.1).
3. **Write `<harness-root>/resource-manifest.json`** (Part V.2; empty `resources: []` if
   none).
4. **Run** `operator_launch harness setup`.
5. **Verify** before requesting any lane: check the returned result and confirm
   `<rt>/resources/RESOURCE_MANIFEST.json` exists.

To change an epoch-immutable input later (profile, manifest, root_workspace), run the
shutdown/retirement route first, edit, then re-run setup.

## VI.2 What `operator_launch harness setup` does (internal, in order)

You do not run these individually; the one command performs them:

1. **Reads config.** Finds `<harness-root>/harness-config.json`; reads `root_workspace`
   and the optional `managed_coordination`. Accepts no separate feature/profile argument.
2. **Validates and derives.** Validates the absolute `root_workspace`; derives
   `<root-workspace>/.harness-runtime/`; verifies that root is **not a symbolic link**
   (the runtime tree relies on same-volume atomic rename). The runtime root **may** sit
   inside another root's lane worktree — that is allowed and not rejected; the operator
   accepts that the owning lifecycle's `git worktree prune` or a manual worktree deletion
   could remove the nested runtime tree. Validates the source `resource-manifest.json`.
3. **Creates the runtime parents** when missing: `<rt>/worktrees/`, `<rt>/monitor/`,
   `<rt>/epochs/`, `<rt>/resources/`, and `<rt>/manager/` (managed only). It does **not**
   pre-create `<rt>/super-cache/` (that is the atomic destination in step 5).
4. **Sets lifecycle state.** Writes `<rt>/RUNTIME_STATE.json` = `OPEN` (or flips
   `CLOSED`→`OPEN` as the first idempotent step). Managed setup also creates and validates
   the idle manager `QUEUE.json`; plain creates no queue and leaves the installed ROOT
   wrapper inactive.
5. **Installs the active cache.** If none exists, stages and byte-verifies a copy of the
   shipped `<harness-root>/super-cache/` (assembling `adapter-payloads/<provider-id>/`
   from each `adapters/<provider>/super-cache/`), then atomically places it at
   `<rt>/super-cache/`.
6. **Preserves an existing cache.** If a valid cache already exists, it is checked and
   left alone — never silently overwriting a working cache with approved extra material.
7. **Writes the runtime manifest + leases.** Stages, byte-verifies, and atomically writes
   the source manifest to `<rt>/resources/RESOURCE_MANIFEST.json`, and creates
   `<rt>/resources/leases/`. If it matches, it leaves it; if it differs, it refuses while
   an epoch or live lease exists.
8. **Materializes ROOT payloads.** Installs the shipped `.codex`, `.claude`, `.qwen` ROOT
   payloads (plus any custom) in `root_workspace`, and installs/checks the provider catalog
   and launcher bindings (`<harness-root>/orchestrator_harness/provider_adapters/<id>/
   launcher_binding.py`). A file collision rejects the whole copy in normal mode;
   `--overwrite` replaces only the planned harness/adapter targets and reports them.
9. **Starts the monitor.** Starts the one mandatory persistent monitor under the
   `monitor-record` lock, writing its identity (PID + creation time) to
   `<rt>/monitor/MONITOR.json`. A live identity returns `SETUP_MONITOR_ALREADY_RUNNING`
   and starts nothing; an absent/stale record is removed and replaced.

## VI.3 Hook trust is proven, not assumed

Copying a hook payload is **not** proof a provider will execute it. Before a provider is
used on a hook-dependent (managed) lane, disposable **host-only headless proof** must show
that its config is discovered, PostToolUse fires, and it honors a Stop rejection. The full
required checklist: setup copies all ROOT, super-cache, and launcher-binding files to their
fixed paths; the CLI discovers its hooks and all ten skills (eight ROOT + the two worker
skills); a **real PostToolUse hook runs**; the **Stop hook rejects unresolved work and an
invalid/missing result**; new and resumed launches use the binding; and each possible
destination-file collision leaves no partial copy. No firmware, MCP server, or hardware is
needed. Each proof uses a fresh ignored runtime root, a fresh Git lane, and one real
registered manager queue with one pending event; the criterion is a durable `DELIVERED`
`post_tool_use` receipt independent of transcript wording. (The shipped providers were so
proven; see Appendix A for the evidence and the exact per-provider proof commands.)

## VI.4 Fresh start — no migration of candidate state

The revamp starts with a fresh v2 project-local runtime tree. Setup does **not** migrate or
open old candidate queues, bindings, coordinators, or in-flight lane state; prior runtime
folders are archival only. (The candidate protocol is preserved for reference in Appendix A
and is not part of v2.)

## VI.5 What is created fresh vs what stays in the harness root

**Created fresh — never copied from a template** (a template would carry stale IDs, process
identities, or queue state into another run): `RUNTIME_STATE.json`, `CURRENT_EPOCH.json`, the
manager `QUEUE.json`, `MONITOR.json`, `epoch-state.json`, `active-lanes.json`, `lane.json`,
the active `RESOURCE_MANIFEST.json`, `resources/leases/…`, and
`worktrees/<epoch-id>/<lane-id>/…`. The same holds for a managed worker's binding and
incoming lane queue, and every lane's controller status/event records, `RESULT.json`, and
provider session ID — bootstrap or the controller writes only the profile-appropriate files
with that lane's real IDs and paths.

**Stays in the harness root — never copied to the runtime tree** (product inputs, not
execution state): `harness-config.json`, the source `resource-manifest.json`,
`orchestrator_harness/…`, the shipped `super-cache/` source, `adapters/README.md`,
`adapters/shipped-machinery/`, and each
`orchestrator_harness/provider_adapters/<id>/launcher_binding.py`. `harness-config.json`
stays so every public command finds its fixed configuration without ROOT supplying a path;
the launcher binding stays because the generic controller imports it as code.

---

# Part VII — Epochs

## VII.1 One active epoch; launcher-owned

ROOT has **no** `epoch open`, `epoch retire`, or lane-record editing command. The public
launcher owns those records. It creates a new epoch **only when no epoch is active**, and
otherwise reuses the active epoch for later lanes while the epoch's immutable
configuration is unchanged. It publishes the generic current-epoch marker before it
prepares the first lane, updates the active-lane index as controllers start/retire, and
closes the epoch only after no active lane remains and, in managed mode, no unresolved
ROOT manager event remains — or during the shutdown/reconfiguration route. A later lane
gets a fresh epoch only when that closure or an epoch-sensitive change requires one; it
never reuses prior event IDs, queue IDs, or process ownership. A lane operation that
arrives for an already-retired epoch (a "late old lane") receives `EPOCH_RETIRED` and does
not proceed.

For a managed epoch, opening atomically replaces the fixed manager queue with a **fresh
`queue_id`**; a plain epoch writes no queue.

## VII.2 Epoch-immutable facts (force a new epoch)

Changing any of these is accepted **only** through the shutdown/retirement path (setup
refuses the change while an epoch is active or a live lease remains):

- `root_workspace` (and therefore the derived runtime root),
- the `managed_coordination` profile (managed ↔ plain),
- the declared exclusive-resource set (the resource manifest),
- the manager-queue schema / `queue_id` (each epoch stages a fresh queue),
- the runtime-record schema version.

## VII.3 Explicitly non-breaking (stay within the active epoch)

- adding or retiring lanes,
- ordinary task/plan content,
- ROOT's own provider, model, and session identity,
- each lane's own provider/model choice.

## VII.4 Records

`CURRENT_EPOCH.json` is the small generic marker of which epoch is active (+ the managed
`queue_id`); `epoch-state.json` is the fuller per-epoch record (config identity incl.
`lane_mode`, opening/active/closed lifecycle, lane directory, ownership). Neither carries
a ROOT provider/session, manager-binding, or queue-path field. Retirement clears
`CURRENT_EPOCH.json` before the epoch is marked closed. (Full schemas: Part XVI §2–§3.)

---

# Part VIII — Lanes: bootstrap, launch, and the controller

## VIII.1 Bootstrap (a short program, not an agent)

`operator_launch lane bootstrap --lane-id <id> --provider <p> --model <m>
[--exclusive-resource <rid> …] --task-card <file>` prepares one lane. It opens a new
epoch if none is active, then:

1. validates the lane ID (rejecting a reused ID for the epoch — `BOOTSTRAP_LANE_ID_IN_USE`),
   provider/model, resource list (each `--exclusive-resource` must be in the active
   manifest — else `BOOTSTRAP_RESOURCE_UNDECLARED`), runtime paths, and launch settings;
2. runs `git worktree add -b <branch> <rt>/worktrees/<epoch-id>/<lane-id> <base-commit>`;
3. creates the worktree's `.agent-workspace/`;
4. applies the selected cache overlay and writes its receipt (`overlay-receipt.json`);
5. installs/binds event-delivery material when managed (the provider payload + worker
   skills + hooks + inbox/outbox);
6. writes the worker prompt, the truthful-result template, the controller invocation
   (`invocation.json`), and the controller status/transcript/stderr/last-message paths;
   writes `lane.json` outside the worktree; updates `active-lanes.json`.

It returns `status: prepared`. It does **not** start a provider, take a lease, operate
hardware, or perform work. A separate launch route consumes the written invocation.

## VIII.2 Launch

`operator_launch lane launch --lane-id <id>` consumes the prepared `invocation.json`.
The **controller** (not the launch caller, not ROOT) starts the provider process and,
for a managed lease-enabled lane, atomically acquires all declared exclusive leases
(all-or-nothing, fail-fast — Part XI). A contended launch returns `LAUNCH_LEASE_BUSY`
and starts nothing.

## VIII.3 The controller's responsibilities (per lane, long-lived)

- Starts and later cleans up the lane's provider and helper processes; captures the
  provider transcript, stderr, and last message.
- Writes its worktree execution records: `controller.status.json` (its status snapshot,
  including a raw `cleanup_proven` flag and its `recorded_status`) and the append-only
  `controller.events.jsonl` audit log — in both profiles.
- Validates the worker's `RESULT.json` and, on its terminal transition, records the
  actionable lane status **in its own worktree records** (never the manager queue):
  `review_pending` for a structurally valid result, `result_invalid` for a
  missing/malformed/wrong-task/contradictory one.
- Owns the lane's live lease(s): creates them at launch, and releases them only after
  proving its own provider/helper processes are gone (sets `cleanup_proven: true`).
- Copies a valid `ACCEPTED` advancement into its status after review, so a later resume
  cannot re-run accepted work.

## VIII.4 Lane lifecycle states (in `lane.json`)

`prepared` (bootstrap) → `running` (launch) → `review_pending` | `result_invalid`
(terminal worker result recorded) → `accepted` → `retired`; plus `blocked` and
`abandoned`. The controller advances the worktree-derived states; the launch/resume/
retire routes set `running`/`retired`.

---

# Part IX — The persistent monitor

Exactly one monitor process per runtime, started by setup and the only actor persistent
across lanes and epochs. It reads `CURRENT_EPOCH.json`, then the active epoch's
`epoch-state.json` and `active-lanes.json`; it therefore needs no queue-path discovery,
provider binding, or restart when lanes change.

## IX.1 Status derivation (the monitor's core job)

On each pass the monitor inspects **only registered lanes** (those in `active-lanes.json`)
and derives each lane's current actionable status from the controller's worktree records.
It takes the controller's `recorded_status` directly (`review_pending`, `result_invalid`)
and **derives** the statuses the controller cannot self-report:

- `controller_exited` and `provider_exited_no_result` — from process liveness + the
  controller's `result_state`;
- `status_transcript_contradiction` — recorded status vs the provider transcript's
  terminal state;
- `cleanup_unproven` — the controller is alive and its result terminal, but its
  `cleanup_proven` flag is still false (a stuck cleanup; distinct from `orphaned_lease`);
- `orphaned_lease` — a lease held by a lane whose run is dead or retired (Part XI).

Resource contention is **not** in this set: a contended launch fails synchronously with
`LAUNCH_LEASE_BUSY`, so no running lane ever waits and there is nothing to promote.

## IX.2 Producing events (managed) and dedup

On a **status change**, the monitor promotes exactly one event to the manager queue
(managed) or leaves the status for `watch` (plain), deduped by the lane's single
`last_reported_actionable_status` value, which it writes into `lane.json` under the
lane-record lock. Status→event mapping: `review_pending` → `COMPLETION_REVIEW_REQUIRED`;
`result_invalid` → `LANE_RESULT_INVALID`; every other status → one generic
`LANE_STATUS_CHANGED` event carrying an `actionable_status` field. (`LANE_RESUME_REQUIRED`
is the separate resume-signal event, Part XIII.)

The monitor also consumes worker-outbox files once, moving them to
`processed-notifications/`. The lane event log (`controller.events.jsonl`) is a permanent,
controller-owned worktree audit record — it is **not** drained into the inbox and the
monitor never moves its entries.

## IX.3 Heartbeat and the ROOT liveness hook (R15)

Because the monitor is the sole producer of events, a silently dead or hung monitor would
stop all ROOT event delivery. Detection/recovery is **managed-only** (it needs a ROOT
hook; plain has none, so there ROOT's own `scan`/`watch` surfaces a stale monitor and
recovery is manual).

- **Heartbeat (liveness signal):** each pass the monitor stamps `last_heartbeat_at` (with
  the watched-lane count) in `MONITOR.json`. That single small field **is** the whole
  heartbeat; the monitor writes **no** heartbeat event to the manager queue.
- **ROOT PostToolUse liveness hook:** on each ROOT tool boundary it makes two checks, both
  from the single small `MONITOR.json` (never the growing queue): (1) is the recorded
  process — matched by PID **and** creation time — alive; (2) is `last_heartbeat_at` within
  the last `X` minutes. If **either** fails (dead/absent, or alive-but-stale/hung), the
  hook returns that into ROOT's context and directs ROOT to start a fresh monitor through
  the same monitor-start route setup uses (take the `monitor-record` lock, replace the
  stale `MONITOR.json` identity, and — for a hung monitor — stop the stale process first).
  The hook detects and directs; ROOT performs the start.
- **Never resurrect a deliberate stop:** the hook leaves a monitor alone only when
  `MONITOR.json` is marked stopped (`stop_requested`/`STOPPED`) **and** the process is
  actually dead (a clean shutdown). A dead process with no stop mark is a crash (restart);
  hung (restart); marked-stopped-but-alive is a stop that did not take (surface to ROOT,
  do not start a second monitor). Because ROOT runs shutdown as a single blocking call, no
  restart can interleave during shutdown; this guard covers the one boundary right after
  it returns.
- `X` is the staleness threshold (reused as the heartbeat interval); it must be
  comfortably larger than the monitor's pass interval. **Recommended default:** ~30s pass,
  `X` ≈ 3 minutes; finalize in the schema/verification work. This is a belt-and-suspenders
  for a rare case (ROOT is almost always alive unless it too crashes, in which case
  recovery is manual: the ROOT agent inspects what is alive, kills stragglers, restarts).

## IX.4 Health reconciliation

`health reconciliation` is primarily an automatic function of monitor startup and each
pass: rebuild `active-lanes.json` from the epoch's controlled `lanes/` directory (a
rebuildable index, not a second authority — `lane.json` wins on disagreement) and
re-derive status. It is also exposed as the manual `operator_launch health reconcile`.

## IX.5 Crash recovery is minimal

There is no replay, supervisor, or elaborate post-crash recovery service. A fresh monitor
begins with a health check and scans the currently registered active lanes. The
`monitor-record` lock (one lock for start, replace, and field writes) exists so two
starters — a setup command and the ROOT liveness hook, or two of either — never both
decide no monitor is live and double-start.

---

# Part X — Coordination: manager queue, worker inbox, worker outbox, and hooks

## X.1 The manager queue (managed) and its three writers

`<rt>/manager/QUEUE.json` (schema `manager-queue/v1`) is the managed profile's single
authoritative ROOT-event queue, at one fixed path, replaced per epoch with a fresh
`queue_id`. A plain profile does not create or read it. Header `{ schema, epoch_id,
queue_id }`; events `{ event_id, type, lane_id, run_id, actionable_status?, summary,
state, history, delivery_history }`.

**Every queue writer takes the same short queue-file lock, confirms its `epoch_id`/
`queue_id` match both the header and `CURRENT_EPOCH.json`, reads `QUEUE.json`, changes the
relevant event in memory, writes a temporary replacement, and atomically replaces the
file.** The three writers:

- the **monitor** — admits (produces) new events; the sole producer;
- **ROOT** — advances an event `PENDING`→`ACKNOWLEDGED`→`COMPLETE`/`BLOCKED` via
  `manager acknowledge`/`close`;
- the managed **PostToolUse hook** — appends a **delivery-history** entry (a lightweight
  `DELIVERED` receipt: outcome + timestamp) that records the hook ran but **never** changes
  the event's manager `state`.

The controller and worker never write the manager queue. There is **no** `STATE.json`,
`QUEUE.jsonl`, coordinator, `REGISTRATION.json`, or second authoritative store — the
single `QUEUE.json` is authoritative. Unbounded growth is accepted for the MVP; if the
file grows large or is corrupted, manual removal falls back to empty-queue recovery
(a fresh `queue_id`; pending events are lost and never treated as handled). No compaction
subsystem is added. Queue **health** may likewise replace the fixed queue with an empty
queue and a fresh `queue_id` **within the same epoch**; it atomically updates
`CURRENT_EPOCH.json`, and a writer still using the old queue ID returns `QUEUE_REPLACED`
without writing.

Event types: `COMPLETION_REVIEW_REQUIRED`, `LANE_RESULT_INVALID`, `LANE_RESUME_REQUIRED`,
`LANE_STATUS_CHANGED` (carries `actionable_status` for statuses without a dedicated event).

## X.2 ROOT's consumption loop (managed)

ROOT is told an event is pending by the PostToolUse hook's delivery notice (a content-free
notice: pending count, highest class/severity, binding identity, timestamp). After
finishing its current task, ROOT reads the queue read-only, acknowledges each top-level
event ID it read (`manager acknowledge --event-id`), handles it, and closes it
(`manager close --event-id --outcome COMPLETE|BLOCKED`). The completion-review command
closes its own event automatically; all other ordinary notifications use the close route.
Closing an event never changes the underlying lane condition (Part XV).

## X.3 The worker inbox (managed) — ROOT→worker assignments

`<worktree>/.agent-workspace/QUEUE.json` (schema `lane-inbox/v1`) holds a running managed
worker's incoming assignments from ROOT: `{ event_id, lane_id, run_id, prompt, created_at,
state, history }`, state `PENDING`→`ACKNOWLEDGED`→`COMPLETE` or `BLOCKED` (with reason). It
is **distinct from** the manager queue and never read by another worker; a plain lane has
none. `operator_launch send-lane-notification --lane-id --prompt` is the only writer that
**appends** an assignment (under the file's short lock); the **worker advances** an
assignment's state via its `lane-assignment`/`lane-queue.py` helper. `lane.json` records the
managed lane's `incoming_queue_path` and `incoming_queue_command`. Hooks filter by the
current `run_id`; resume resets this file to an empty queue for the fresh run.

## X.4 The worker outbox (managed) — worker→ROOT escalations

`<worktree>/.agent-workspace/manager-notifications/` is a one-way escalation outbox: each
file means the worker needs ROOT intervention (written via `manager-notify.py`, which takes
a `--severity`, e.g. `blocking`). It is
**not** the manager queue. The monitor consumes each file once, moving it to
`processed-notifications/`, and promotes the escalation to ROOT as an event.

**The escalation instruction is mechanically added to prompts, not left to task cards.**
The managed lane controller's provider-launch code appends a generated escalation block
after every managed worker task prompt it constructs, so the worker cannot lose the
instruction because a task card omitted it. That block carries the exact helper command for
the current worktree and says: use it when work needs a ROOT decision, authority, missing
input, or help; include the decision/action ROOT needs plus relevant local evidence; do not
rely on a final chat answer as a notification; and after a blocking escalation, stop at a
safe boundary rather than inventing the missing decision. The managed orchestrator's
generated initial prompt receives the matching ROOT block (a worker escalation becomes a
ROOT-targeted manager-queue event that ROOT must inspect, resolve, and acknowledge by its
top-level event ID only after finishing its current task). These are controller-generated
prompt fragments, not optional wording copied into task cards or `AGENTS.md`. The cache-owned
`manager-notify` worker skills **reinforce** the same instruction after the overlay copy;
they do not replace the mandatory generated block. A plain lane receives no escalation
block, helper, or `manager-notify` skill.

## X.5 Hooks

Managed lanes install native provider hooks (proven per Part VI.3):

- **ROOT PostToolUse** — the delivery notice (X.2) **and** the monitor-liveness check (IX.3).
- **ROOT Stop** — the gate that prevents ROOT from idling with unresolved obligations.
- **Worker PostToolUse** — the worker-side delivery notice.
- **Worker Stop** — rejects a `REJECT` while local work is unresolved or the `RESULT.json`
  is missing/invalid; permits a valid `PASS`/`FAIL`/`BLOCKED` terminal. Exiting with
  success is not a valid Stop bridge.

Hook file names in the v2 ROOT payload are `orchestrator_harness_post_tool_use.py`,
`orchestrator_harness_stop.py` (and `orchestrator_harness_bounded_policy.py`; Qwen also
`orchestrator_harness_notification.py`); the worktree hook machinery is `hook-dispatch.py`
(invoked with `--boundary <boundary>` — e.g. post-tool-use or stop — to select which hook
boundary fired)
+ `harness-hook-binding.json`. An installed-but-unbound provider hook is a **setup error**
that fails loudly (`installed <provider> hook has no harness binding`) rather than
silently pretending delivery occurred.

---

# Part XI — Resources and leases

## XI.1 Lease lifecycle (written at launch, held only while the controller lives)

An exclusive-resource **lease** is a file under `<rt>/resources/leases/` (schema
`resource-lease/v1`), one per currently-held resource, the folder created empty by setup.
Bootstrap only **declares** a lane's exclusive resources (`--exclusive-resource <id>`) and
takes no lease; the **launch** route obtains the controller-owned lease, and the controller
releases it as soon as it has proved its own provider/helper processes are gone. A resource
is therefore held only during that lane's active run — not reserved at bootstrap and not
for the whole epoch — so a freed lease is immediately **reusable in series** by a later
lane. ROOT owns the declared resource list; the controller owns the live lease. Fields:
`resource_id`, `lane_id`, `run_id`, holder `pid`+`creation_time`, `acquired_at`; the
filename is generated deterministically from the `resource_id`.

## XI.2 Fail-fast, all-or-nothing acquisition; ROOT orchestrates the wait

The intended model does not assign exclusive resources concurrently — ROOT sequences
launches so a resource is free before it launches a lane that needs it. If a launch does
hit contention, it acquires **every** declared resource or **none**: if any is unavailable
it acquires none (releasing anything momentarily claimed) and the launch **fails
synchronously** with `LAUNCH_LEASE_BUSY`; no lane starts and nothing is held partially. ROOT
then holds off and re-launches once the current holder finishes — a wait, but
ROOT-orchestrated, not an auto-waiting lane. Because no lane ever holds one lease while
waiting for another, there is no hold-and-wait and so no lease deadlock, and no global
acquisition order is required. There is no busy-retry.

## XI.3 Orphaned leases — surfaced, never auto-reclaimed

A crashed or retired lane can leave a lease behind. A stale lease is **not** auto-reclaimed:
reclaiming it silently would hand a resource to a new lane without the cleanup proof the
retirement path requires, and a crashed holder may have left the resource in an unknown
state. Instead the monitor detects it (holder `pid`+`creation_time` dead, or `lane_id`/
`run_id` retired) and promotes `orphaned_lease` to ROOT (managed) or surfaces it via `watch`
(plain). Clearing is a plain **force-release** — the harness enforces no cleanup-attestation
policy; it surfaces the condition and lets the intelligent ROOT clear/reuse or escalate to
the operator on its own. `lane force-stop` and the orphaned-lease clear are the two forced
releasers (Part XIV). A short read-modify-replace OS lock (used for record writes)
auto-releases when its handle closes; a resource lease is a persistent file and does not.

---

# Part XII — Completion review and acceptance

## XII.1 The chain and the two decision records

The lifecycle is: **task card → `RESULT.json` → `COMPLETION_REVIEW.json` →
`ORCHESTRATOR_ACCEPTANCE.json`.** The two decision files have fixed lane-record paths
outside the worktree so the worker cannot forge them:

```text
<rt>/epochs/<epoch-id>/lanes/<lane-id>/COMPLETION_REVIEW.json
<rt>/epochs/<epoch-id>/lanes/<lane-id>/ORCHESTRATOR_ACCEPTANCE.json
```

`RESULT.json` is the worker's result; `COMPLETION_REVIEW.json` is the factual finding;
`ORCHESTRATOR_ACCEPTANCE.json` holds the final `ACCEPTED`/`REJECTED` verdict. A reader checks
that the card/result/review/acceptance hashes and IDs refer to the same task and commit; if
both review files are absent the task is `ACCEPTANCE_PENDING`; if only one exists the chain
is an error. The controller copies a valid `ACCEPTED` advancement into its own status, which
prevents a later resume. The worker cannot make itself accepted by setting a field in
`RESULT.json`; the separate review/acceptance records are still required.

## XII.2 The one public review command (both profiles)

```text
operator_launch lane completion-review (--event-id <id> | --lane-id <id>)
  --review-outcome PASS|FAIL|BLOCKED
  --approval ACCEPTED|REJECTED
  --review-summary "<ROOT's reasoning>"
  [--evidence <path> …]
  [--force-accept --force-reason "<why the change is harmless>"]
```

`--review-outcome` and `--approval` are **two independent, both-required fields — a factual
finding AND a separate decision, not two names for one thing and not alternatives.**
`--review-outcome` is the finding (did the work pass?), vocabulary `PASS`/`FAIL`/`BLOCKED`,
recorded in `COMPLETION_REVIEW.json`. `--approval` is ROOT's accept/reject decision,
vocabulary `ACCEPTED`/`REJECTED`, recorded in `ORCHESTRATOR_ACCEPTANCE.json`. One rule links
them: **`ACCEPTED` requires a `PASS` finding**; `REJECTED` may accompany any finding. Neither
field is the `manager close --outcome COMPLETE|BLOCKED` event-close vocabulary (a different
command; its `BLOCKED` is an event-close state, not the review's `BLOCKED` finding). This
command is the **only** writer of the two decision files, writes them as a pair, and closes
its own managed review event automatically.

## XII.3 How ROOT learns review is needed; profiles

- **Managed:** the controller records `review_pending` (or `result_invalid`); the monitor
  (sole producer) promotes `COMPLETION_REVIEW_REQUIRED` (or `LANE_RESULT_INVALID`); ROOT
  acknowledges and runs the review with `--event-id`.
- **Plain:** the controller records terminal result validation in `lane.json` and its normal
  worktree records; ROOT runs the same command with `--lane-id`, reading only the controlled
  lane record and current artifacts. Plain is not auto-accept — the same factual finding and
  separate acceptance decision are made, just reached directly.

## XII.4 Forced acceptance and source-identity check

`--force-accept --force-reason "…"` allows `ACCEPTED` with a non-`PASS` finding, recording
the reason; a forced approval still requires a structurally valid current task/result chain
(a stale source is rejected — `COMPLETION_REVIEW_STALE_SOURCE`). The command performs one
final source-identity check (card/result/run currency), not a general hash sweep.

## XII.5 Crash recovery for a lost review event or broken pair

The harness does not promise exactly-once event publication; a startup health check may
discard a malformed temporary record or reset a malformed manager queue, which is allowed to
lose an in-flight notification but must **not** permanently strand a valid finished lane.

- **Managed reconciliation may create exactly one replacement `COMPLETION_REVIEW_REQUIRED`
  event** — but only when all hold: the lane has a terminal, structurally valid
  `RESULT.json`; neither a complete linked review/acceptance pair nor an open matching review
  event exists; and the lane record identifies that same `run_id`. The replacement is
  recorded in the lane record as recovery evidence; it is a **new request** to review the
  same finished work, not a replay that claims the lost event was acknowledged or handled.
- **Plain reconciliation** merely preserves or restores the direct `review_pending` lane
  state after removing a broken artifact; it creates no queue record.
- **A broken review/acceptance pair** — a malformed or incomplete `COMPLETION_REVIEW.json` /
  `ORCHESTRATOR_ACCEPTANCE.json` at the known paths — is removed by health recovery, leaving
  the lane acceptance pending. Recovery writes no replacement acceptance and **never** infers
  `ACCEPTED` from one surviving file. No replay service, distributed transaction, or attempt
  to reconstruct partial ROOT reasoning is required.

---

# Part XIII — Resume

## XIII.1 `resume-lane`

`operator_launch resume-lane --lane-id <id> --resume-task-card <file> [--rationale "…"]`
re-runs a **stopped, unaccepted** lane in its **same worktree and provider session** with a
**fresh `run_id`**. It re-does work; it is **not** a cleanup tool for a finished-but-stuck
lane.

## XIII.2 Mechanical behavior

It sets the lane `RESUMING`, replaces the task/rationale/instruction fields, and clears the
prior run's obsolete current state: `RESULT.json`, `COMPLETION_REVIEW.json`,
`ORCHESTRATOR_ACCEPTANCE.json`, and — for a managed lane — empties the worker incoming
`.agent-workspace/QUEUE.json` to a valid empty queue carrying the fresh `run_id`. Hooks
filter by the current `run_id`, so stale-run artifacts are ignored. It never reconstructs a
session, PID, worktree, invocation, or amendment/hash record; it writes a fresh invocation
for the new run.

## XIII.3 What remains deliberately strict

- `ALREADY_ACCEPTED` — a lane with a valid acceptance chain is not re-resumed (the
  controller's copied `ACCEPTED` advancement blocks it).
- `LANE_RUNNING` — a still-active lane is not resumed.
- `RESUME_WORKTREE_MISSING` / `NO_SAVED_SESSION_ID` — if there is no worktree or no native
  session to resume, resume fails; the honest path is a **new** lane (fresh bootstrap), not a
  resume.
- Managed resume issues a normal `LANE_RESUME_REQUIRED` event where appropriate; plain
  resume restores direct review-pending handling.

## XIII.4 Result and acceptance after resume

The normal final-result route validates the new `RESULT.json` against both the current task
card and the lane's current `{ lane_id, run_id }`. A stale result (from an old run) is
rejected as `RESULT_STALE_RUN` and **never reaches ROOT review**. A structurally valid
`PASS`/`FAIL`/`BLOCKED` result produces a managed completion-review event (managed) or makes
the same direct `lane completion-review --lane-id` route available (plain); neither profile
requires a historical worktree to be present. If ROOT rejects the work, the lane becomes
resumable again — ROOT can submit another resume card to the same lane and same provider
session, creating no archive, new worktree, or generation folder.

---

# Part XIV — Force-stop, retire, and shutdown

These are the three ways a lane or the runtime ends. `lane retire` is the graceful end of an
**accepted** lane; `lane force-stop` is the forceful end of a **stuck** lane; `harness
shutdown` ends the whole runtime.

## XIV.1 `lane force-stop` — targeted single-lane hard stop

`operator_launch lane force-stop --lane-id <id>` forcibly terminates one lane's processes —
its provider, helper, and controller, matched by the PID+creation identities in `lane.json`
— then **force-releases** any exclusive lease it held and marks the lane `retired`. It is the
single-lane counterpart to `harness shutdown` and the escalation for a lane stuck in
`cleanup_unproven` or whose controller is itself wedged. Because it force-releases the lease
without the graceful cleanup-proof handshake, ROOT owns the safety decision (the same
operator-owns-the-risk stance as the orphaned-lease clear). Both profiles; selected by
`--lane-id`. Exposed as the ROOT skill `force-stop-lane`. On `FORCE_STOP_PROCESS_SURVIVED`
(a process cannot be terminated even forcibly), escalate to the operator/host — an unkillable
process is outside the harness's authority.

## XIV.2 `lane retire` — graceful end of an accepted lane

`operator_launch lane retire --acceptance-ref <file>` gracefully retires one accepted lane
for archive/close: cleanup-proof-first, releasing its lease after proof, branch retained. It
takes a reference to the lane's existing `ORCHESTRATOR_ACCEPTANCE.json` (it does not create
acceptance). On `RETIRE_CLEANUP_UNPROVEN`, `lane force-stop` then treat as done. A retirement
that empties the epoch triggers epoch close (Part VII). Retirement **retains** the lane
record and does **not** hand-remove cache files or create an archive, history directory, or
overlay-restoration workflow; the operator may remove a retired worktree whenever they
choose, and the harness never requires that directory afterward. (The overlay receipt
supports only narrow overlay restoration during retirement; it does not claim the worker's
later files are cache changes.)

## XIV.3 `harness shutdown` — end the whole runtime

`operator_launch harness shutdown` ends the runtime with exact process ownership:

1. It flips `<rt>/RUNTIME_STATE.json` `OPEN`→`SHUTTING_DOWN` and rejects any new lane launch.
2. Each **lane's** provider/helper processes are cleaned by **that lane's controller** — the
   right owner. There is no global mutable process list; the shutdown never kills by broad
   process name. A lane's lease is **not** released before its cleanup proof exists.
3. Under the `monitor-record` lock it sets `stop_requested: true` in the existing
   `MONITOR.json`. The monitor observes `stop_requested` in its own record and exits; its
   exact PID+creation identity is used, so a recycled PID is never mistaken for it. **The
   monitor is stopped after lane cleanup** (otherwise a lane failure during shutdown would
   lose its manager path).
4. It atomically changes `RUNTIME_STATE.json` to `CLOSED` (clearing `CURRENT_EPOCH.json`
   first).

Shutdown uses this one project-local runtime lifecycle state and the existing
`monitor/MONITOR.json`; it creates **no** separate shutdown-marker or
monitor-stop-request/acknowledgement files. (Symmetrically, `harness setup` returns its
structured result to ROOT but writes no separate setup-evidence record.)

Because ROOT invokes shutdown as a single **blocking** call, it cannot do anything else
until the call returns; the ROOT liveness hook (Part IX.3) therefore cannot resurrect the
deliberately-stopped monitor. On failure it preserves evidence and does **not** retry with
broad kills. Failure codes: `SHUTDOWN_LANE_CLEANUP_UNPROVEN`, `SHUTDOWN_MONITOR_UNPROVEN`,
`SHUTDOWN_RUNTIME_AMBIGUOUS`.

**Exceptional recovery:** only a narrow recovery route may target a still-live monitor, and
only after matching both PID and creation time and honoring `stop_requested` — it may target
only the exact monitor, never a broad kill. Two routes may deliberately stop a still-live
monitor, each only after matching PID+creation: shutdown's exceptional-recovery route, and
the ROOT liveness hook's hung-monitor path.

## XIV.4 Git hygiene

The runtime tree, and every lane worktree, is locally Git-excluded by default, keeping
worktree files out of ROOT's status/commits; because lane branches are never pushed the
remote stays clean. The exclusion does not clean Git's own bookkeeping, so `harness shutdown`
and epoch retirement run `git worktree prune` against each lane's source repository to clear
dangling `.git/worktrees/<id>` entries. Local lane branches are retained.

---

# Part XV — Operator responses to actionable statuses (remediation)

The monitor surfaces each actionable status to ROOT as a manager-queue event (managed) or
via `scan`/`watch` (plain); this part says what ROOT is expected to **do**. Two framing
rules:

- **Closing an event is not resolving the condition.** `manager close` records that ROOT
  handled the *notification*; it does not change the lane's ground truth. A status clears
  only when the underlying fact changes (e.g. a stuck process finally exits, so
  `cleanup_proven` becomes true). If ROOT closes an event while the condition persists, the
  monitor's `last_reported_actionable_status` dedup keeps it from re-alerting, but the
  condition stays truthfully recorded in the lane records and its consequences (a held lease
  blocking new launches, an un-retirable lane, a later shutdown failure) resurface on their
  own. ROOT is trusted to act, not policed.
- **`resume-lane` re-does the task; it does not clean up a finished one.** Resume is for
  "the work must run again"; it is the wrong tool for a done-but-stuck lane.

| Status | Meaning | ROOT's response |
| --- | --- | --- |
| `review_pending` | Terminal, structurally valid result awaiting review | `lane completion-review` (finding + approval). `PASS`+`ACCEPTED` finishes it, then `lane retire`; otherwise `resume-lane`. |
| `result_invalid` | `RESULT.json` missing or malformed | Review (usually `FAIL`/`REJECTED`), then `resume-lane` to redo, or `lane force-stop`/retire to abandon. |
| `provider_exited_no_result` | Provider exited without a result | Inspect transcript/stderr; `resume-lane` to retry, or `lane force-stop`/retire to abandon. |
| `controller_exited` | Lane controller process died | Investigate; `resume-lane` to restart, or `lane force-stop` to clean up (also clears the now-orphaned lease). |
| `status_transcript_contradiction` | Recorded status disagrees with the provider transcript | Establish the true state; `resume-lane` or `lane force-stop`. |
| `cleanup_unproven` | Task done, but processes won't exit (controller alive, `cleanup_proven` false) | Clear the straggler so the live controller finishes teardown and drops the lease; if it won't clear or the controller is wedged, `lane force-stop`. |
| `orphaned_lease` | Lease held by a lane whose run is dead/retired | Force-release the lease before reusing that resource. |

---

# Part XVI — Record schemas (all records)

This part is the complete, authoritative schema ledger for every persistent record. It is
self-contained; the shared conventions apply to every record, then each record is specified
with schema/version, fields, state transitions, writer, reader, lock/atomic rule, health
check, and recovery.
## Conventions that apply to every record

- **Version string.** Every JSON record carries a top-level `schema` field of the
  form `<file-stem-in-kebab-case>/v1` — the record's own filename stem, lower-kebab,
  plus `/v1`. Examples: `harness-config.json` → `harness-config/v1`,
  `resource-manifest.json` → `resource-manifest/v1`, `RUNTIME_STATE.json` →
  `runtime-state/v1`, `CURRENT_EPOCH.json` → `current-epoch/v1`, the manager
  `QUEUE.json` → `manager-queue/v1`. There is no separate product prefix beyond
  what the filename already carries; the canonical string for each record is given
  in its section below. **[default]**
- **Atomic write (the one-local-temp-file rule).** Every write that can replace an
  existing record writes a unique temporary sibling in the destination's *own
  parent directory*, validates it, then performs a same-volume atomic rename while
  holding that record's short lock. The lock is released in a `finally`/cleanup
  path; if a writer crashes, closing its process handle releases the OS lock, and
  the next writer performs the normal parse/health check before continuing. This
  is not a durable `locked` field and ROOT never manages it.
- **Multi-lock order.** When one operation needs more than one lock it acquires
  them in the fixed order runtime-state → manager-queue → lane-record →
  resource-lease → monitor-record. In normal operation only the monitor takes two
  (manager-queue then lane-record).
- **Identities and hashes (settled — deliberately the simplest option).** `epoch_id`,
  `queue_id`, `event_id`, and `run_id` are opaque, harness-generated unique strings
  (a UUID or timestamp+random); they are never reused across epochs. `lane_id` is
  operator-supplied at bootstrap and unique for the epoch's lifetime, including
  retired lanes. Content identity/linkage uses a `sha256` hex digest over the
  record's canonical (sorted-key, UTF-8) JSON, stored in a `content_hash` field;
  cross-record links store both the referenced `*_id` and its `*_hash`. This is
  integrity only — records are **not** signed and there is no PKI; under the
  harness's cooperative-local-trust model the hash chain just detects mismatched or
  mis-linked records, which is all that is needed.
- **Timestamps.** ISO-8601 UTC strings (e.g. `2026-06-01T12:00:00Z`).
- **General health check.** On read, a reader parses the file, checks `schema`,
  checks required fields are present and well-typed, and checks that any embedded
  `epoch_id`/`run_id`/`lane_id` match the context it was opened for. Record-specific
  checks are noted per record.
- **Version-mismatch recovery. [default]** A record whose `schema` major version is
  unrecognized is *not* migrated silently: the reader refuses to act on it and
  surfaces a clear error (for a lane record this becomes an actionable condition;
  for setup it aborts). The MVP adds no migration subsystem, consistent with R6's
  "no compaction subsystem" stance.

## Already-defined inputs (not re-specified here)

`<harness-root>/harness-config.json` (`harness-config/v1`) and the source
`<harness-root>/resource-manifest.json` → active `<rt>/resources/RESOURCE_MANIFEST.json`
(`resource-manifest/v1`) are ROOT-authored setup inputs with schemas already fixed
in `setup-details.md`/`fixing_reccomendations.md`. Their only additions under this
ledger are the conventions above (version string form, atomic write for the active
manifest copy).

---

## 1. `RUNTIME_STATE.json`  →  `<rt>/RUNTIME_STATE.json`

- **Schema:** `runtime-state/v1`.
- **Fields:** `schema`; `state` ∈ {`OPEN`, `SHUTTING_DOWN`, `CLOSED`}; `updated_at`.
- **States/transitions:** `OPEN` → `SHUTTING_DOWN` → `CLOSED` (public shutdown);
  `CLOSED` → `OPEN` (setup re-open, the first idempotent setup step). No other
  transitions.
- **Writer:** setup (create, or `CLOSED`→`OPEN`); public shutdown (`OPEN`→
  `SHUTTING_DOWN`→`CLOSED`), each under the runtime-state lock.
- **Reader:** the public launcher (refuses a new lane launch unless `OPEN`); setup;
  the monitor (informational).
- **Lock/atomic:** runtime-state lock + atomic sibling rename.
- **Health check:** exactly one of the three states; absent file at a command that
  requires the runtime means setup has not run.
- **Recovery:** absent → setup creates it in `OPEN`. A crash mid-transition leaves
  the last atomically-written state; setup re-open and shutdown are both
  idempotent from any prior state.

## 2. `CURRENT_EPOCH.json`  →  `<rt>/CURRENT_EPOCH.json`

- **Schema:** `current-epoch/v1`. The small generic active-epoch marker.
- **Fields:** `schema`; `epoch_id`; `lane_mode` ∈ {`managed`, `plain`}; for a
  managed epoch, `queue_id` (the fixed manager queue's current id); `opened_at`.
  It has **no** path, ROOT provider, model, or session field. A plain marker has
  `lane_mode: "plain"` and no `queue_id`.
- **States/transitions:** absent (no active epoch) → present (epoch open) → absent
  (retirement clears it before the epoch is marked closed, per R9). One active
  marker at a time.
- **Writer:** the public launcher — written atomically *after* it stages the fresh
  managed queue (or after creating the plain epoch record), and cleared by
  retirement/shutdown before closure.
- **Reader:** the managed ROOT Stop-gate/dispatcher (reads `epoch_id` + `queue_id`
  and cross-checks the manager queue header); the monitor (reads it first, then the
  active epoch's `epoch-state.json` + `active-lanes.json`).
- **Lock/atomic:** written under the runtime-state lock (it gates epoch identity)
  + atomic sibling rename. **[default: runtime-state lock]**
- **Health check:** managed marker must carry a `queue_id` that matches the manager
  queue header; a marker pointing at a closed epoch is the crash window R9
  describes and the dispatcher simply no-ops.
- **Recovery:** absent → no active epoch; the next bootstrap/launch opens one.
  Marker/queue `queue_id` disagreement → dispatcher no-ops (does not act on a stale
  pairing).

## 3. `epoch-state.json`  →  `<rt>/epochs/<epoch-id>/epoch-state.json`

- **Schema:** `epoch-state/v1`. The fuller per-epoch record (the marker is the
  pointer; this is the state).
- **Fields:** `schema`; `epoch_id`; `config_identity` (the immutable configuration
  including `lane_mode` and the enabled immutable feature set); `lifecycle` ∈
  {`opening`, `active`, `closed`}; `lane_dir` (this epoch's `lanes/` path);
  `ownership` status; `opened_at`/`closed_at`. **No** ROOT provider/session,
  manager-binding, or queue-path fields.
- **States/transitions:** `opening` → `active` → `closed`.
- **Writer:** the public launcher (open/activate/close), under the lane-record-tier
  lock for the epoch directory. **[default lock tier]**
- **Reader:** the monitor (after the marker); the launcher (to decide reuse vs a
  new epoch).
- **Health check:** `config_identity` must equal the active config; a mismatch is
  an epoch-breaking change and forces a new epoch (task 1).
- **Recovery:** a crash during `opening` leaves a non-`active` epoch the launcher
  can retire and replace; health reconciliation may rebuild `active-lanes.json`
  (below) from `lane_dir` regardless.

## 4. `active-lanes.json`  →  `<rt>/epochs/<epoch-id>/active-lanes.json`

- **Schema:** `active-lanes/v1`. A small, rebuildable monitor index — **not** a
  second lane authority.
- **Fields:** `schema`; `epoch_id`; `lanes`: list of `{ lane_id, lane_record_path,
  run_id }`. `lane.json` is authoritative if the two ever disagree.
- **States/transitions:** grows/shrinks as controllers start and retire; no
  internal lifecycle.
- **Writer:** the public launch, resume, and retirement routes (atomic update); the
  monitor's health reconciliation may rebuild it wholesale from the epoch's
  controlled `lanes/` directory.
- **Reader:** the monitor (the set of lanes to inspect each pass).
- **Lock/atomic:** lane-record-tier lock + atomic sibling rename.
- **Health check:** every listed `lane_record_path` must exist and its `lane.json`
  `run_id` must match; on disagreement the monitor trusts `lane.json` and flags the
  index for rebuild.
- **Recovery:** treated as disposable — rebuilt from the `lanes/` directory by
  health reconciliation at monitor startup and each pass.

## 5. `lane.json`  →  `<rt>/epochs/<epoch-id>/lanes/<lane-id>/lane.json`

- **Schema:** `lane/v1`. The authoritative outside-worktree record for one lane.
- **Fields:** `schema`; `lane_id`; one current `run_id`; `worktree_path` and the
  exact in-worktree artifact paths (`result_path`, `controller_status_path`,
  `controller_events_path`, transcript/stderr/last-message paths); `provider`
  (`{ id, model }`); `session` identity; `process` identity (`{ pid, creation_time }`);
  `lifecycle` state; `acceptance_advancement` (set once a valid `ACCEPTED` chain
  exists, to prevent re-resume); `last_reported_actionable_status` (the monitor's
  single dedup marker — the last actionable status it promoted for this lane; see
  Writer). **Managed only:** `incoming_queue_path` and
  `incoming_queue_command` (this lane's `.agent-workspace/QUEUE.json` and
  `lane-queue.py`); a plain `lane.json` has neither.
- **States/transitions [default enum]:** `prepared` (bootstrap) → `running` (launch)
  → `review_pending` | `result_invalid` (terminal worker result recorded) →
  `accepted` → `retired`; plus `blocked` and `abandoned`. The controller advances
  the worktree-derived states; the launch/resume/retire routes set
  `running`/`retired`.
- **Writer:** the public bootstrap/launch/resume/force-stop/retirement routes derive
  and update it, and ROOT never edits it directly; the launcher reflects `lifecycle`
  here while the controller's detailed execution state lives in its own worktree
  records (§9–10). The **monitor** writes exactly one field —
  `last_reported_actionable_status` — after rereading, under the lane-record lock,
  as its dedup marker (managed and plain alike).
- **Reader:** the monitor (via `active-lanes.json`), the completion-review command
  (plain mode source of truth), resume, retirement.
- **Lock/atomic:** lane-record lock + atomic sibling rename.
- **Health check:** `run_id` present and unique; artifact paths resolve under this
  lane's worktree; managed record has both incoming-queue fields.
- **Recovery:** authoritative — used to rebuild `active-lanes.json`; a malformed
  `lane.json` is a per-lane actionable error, never silently regenerated.

## 6. Manager `QUEUE.json`  →  `<rt>/manager/QUEUE.json`

- **Schema:** `manager-queue/v1`. The managed profile's authoritative ROOT-event
  queue (one fixed path, replaced per epoch). A plain profile does not create or
  read it.
- **Fields:** header `{ schema, epoch_id, queue_id }`; `events`: list of
  `{ event_id, type, lane_id, run_id, actionable_status?, summary, state, history,
  delivery_history }`. `history` is the append-only list of state transitions; a
  managed PostToolUse hook may append a **delivery-history** entry (a lightweight
  "delivered" receipt: `outcome: "DELIVERED"` + timestamp) that records the hook ran
  but **never** changes the event's manager `state` (scan-watch). This is v2's whole
  delivery-receipt facility — there is no separate coordinator, `REGISTRATION.json`,
  or `DELIVERY.jsonl` second store (those belong to the historical candidate protocol
  in `subagent_hooks.md`, not v2).
  Event `type` ∈ {`COMPLETION_REVIEW_REQUIRED`, `LANE_RESULT_INVALID`,
  `LANE_RESUME_REQUIRED`, `LANE_STATUS_CHANGED`} (see R9: `LANE_STATUS_CHANGED`
  carries the `actionable_status` field for the statuses without a dedicated
  event). `history` is the append-only list of state transitions with timestamps.
- **Event states/transitions:** `PENDING` → `ACKNOWLEDGED` → `COMPLETE`, or
  `ACKNOWLEDGED` → `BLOCKED` (with reason). The monitor creates `PENDING`; ROOT
  moves to `ACKNOWLEDGED` (`manager acknowledge`) and to `COMPLETE`/`BLOCKED`
  (`manager close --outcome COMPLETE|BLOCKED`). *(This `--outcome` is the event's
  close state; it is unrelated to a lane review's `--review-outcome`, §12.)*
- **Writer:** three components write the file, each under the queue lock — the
  monitor (the **sole producer**: only it *creates* events, per R4), ROOT (advances
  event state via the manager commands), and the managed PostToolUse hook (appends a
  `delivery_history` entry only, never changing manager state). The launcher stages a
  fresh empty queue (new `queue_id`) at epoch open. The controller and worker never
  write it; the monitor's heartbeat is a `MONITOR.json` field (§8), not a queue write.
- **Reader:** ROOT (its inbox); the completion-review command (requires an
  `ACKNOWLEDGED` `COMPLETION_REVIEW_REQUIRED` event in managed mode).
- **Lock/atomic:** manager-queue lock + atomic sibling rename for every append and
  state change (read-whole → change owned fields → replace).
- **Health check:** header `epoch_id`/`queue_id` must match `CURRENT_EPOCH.json`;
  events reference live lanes/runs.
- **Recovery:** unbounded growth is accepted (R6). If corrupt/over-large, manual
  removal falls back to empty-queue recovery: stage a fresh `queue_id`, pending
  events are lost and never treated as handled (R6). No compaction subsystem.

## 7. Worker-inbox `QUEUE.json`  →  `<worktree>/.agent-workspace/QUEUE.json`

- **Schema:** `lane-inbox/v1`. A managed live worker's incoming assignments from
  ROOT. Distinct from §6; never read by another worker; absent for a plain lane.
- **Fields:** `schema`; `lane_id`; `run_id`; `assignments`: list of
  `{ event_id, lane_id, run_id, prompt, created_at, state, history }`.
- **Assignment states/transitions:** `PENDING` → `ACKNOWLEDGED` → `COMPLETE`, or
  `BLOCKED` (with reason). ROOT (`send-lane-notification`) appends a `PENDING`
  assignment; the worker advances state via its `lane-queue.py` helper and escalates
  a `BLOCKED` via `manager-notify.py`.
- **Writer:** `send-lane-notification` is the only ROOT writer (append under the
  file's short lock); the worker advances assignment state via the helper.
- **Reader:** the worker (through the helper). The monitor does not read it.
- **Lock/atomic:** the file's own short lock + atomic sibling rename.
- **Health check:** `run_id` matches the lane's current run; hooks filter by current
  `run_id` (R8) so stale-run assignments are ignored.
- **Recovery:** on resume the file is reset to an empty queue for the fresh `run_id`
  (R8), alongside clearing `RESULT.json`/`COMPLETION_REVIEW.json`/
  `ORCHESTRATOR_ACCEPTANCE.json`.

## 8. `MONITOR.json`  →  `<rt>/monitor/MONITOR.json`

- **Schema:** `monitor/v1`. The one persistent monitor's identity + liveness record.
- **Fields:** `schema`; `config_identity`; `pid`; `creation_time`; `started_at`;
  `health`; `last_heartbeat_at` (refreshed each pass — the freshness signal the
  ROOT liveness hook reads, R15); `stop_requested` (bool) / derived `STOPPED`.
- **States/transitions:** live (fresh `pid`+`creation_time`, `last_heartbeat_at`
  advancing) → `stop_requested` set (shutdown asks it to stop) → `STOPPED`
  (process exited). A fresh monitor replaces a stale identity.
- **Writer:** the monitor (its own `health`/`last_heartbeat_at` each pass); setup
  and the ROOT liveness-hook recovery path write/replace the identity under the
  monitor-record lock; public shutdown sets `stop_requested` under the same lock.
- **Reader:** setup (to no-op vs replace); the ROOT PostToolUse liveness hook
  (PID+creation liveness **and** `last_heartbeat_at` freshness, both from this one
  small file, never the queue, R15).
- **Lock/atomic:** the single `monitor-record` lock (R9 — one lock for start,
  replace, and field writes) + atomic sibling rename.
- **Health check:** the recorded `pid`+`creation_time` must be a live process; a
  reused PID with a different creation time is not the monitor.
- **Recovery:** dead-or-absent (no `stop_requested`) or hung (`last_heartbeat_at`
  older than `X`) → the liveness hook has ROOT start a fresh monitor under the
  `monitor-record` lock; `stop_requested`+dead → deliberate stop, left alone (R15).

## 9. `controller.status.json`  →  `<worktree>/.agent-workspace/controller.status.json`

- **Schema:** `controller-status/v1`. The controller's execution-status snapshot —
  the monitor's actionable-status source.
- **Fields:** `schema`; `lane_id`; `run_id`; `controller_state` (running / exited);
  `provider_state` (running / exited, with exit info); `result_state`
  (absent / invalid / valid); `cleanup_proven` (bool — whether the controller has
  confirmed its own provider/helper processes are gone); `recorded_status` — the
  actionable status the *controller itself* records, ∈ {`review_pending`,
  `result_invalid`}; `acceptance_advancement` once the controller copies a valid
  `ACCEPTED` chain into its status; `updated_at`.
- **States/transitions:** the controller records `review_pending` after a terminal,
  structurally valid `RESULT.json`, or `result_invalid` after an invalid/missing
  one; it sets `cleanup_proven` once its processes are confirmed gone; it copies
  `ACCEPTED` advancement in after review.
- **Writer:** the lane controller (under the lane-record lock for its own record).
- **Reader:** the monitor each pass, to **derive** the lane's current actionable
  status: it takes the controller's `recorded_status` directly, and derives the
  statuses the controller cannot self-report — `controller_exited` and
  `provider_exited_no_result` (from process liveness + `result_state`),
  `status_transcript_contradiction` (recorded status vs the provider transcript's
  terminal state), `cleanup_unproven` (controller alive and its result terminal, but
  `cleanup_proven` is still false — a stuck cleanup, distinct from a dead holder's
  `orphaned_lease`), and `orphaned_lease` (from lease state, §14). Resume also
  compares it.
- **Lock/atomic:** lane-record lock + atomic sibling rename.
- **Health check:** `run_id` matches `lane.json`; `recorded_status` in the permitted
  set {`review_pending`, `result_invalid`}.
- **Recovery:** if the controller process is gone and the status is non-terminal,
  the monitor derives `controller_exited`; a status that contradicts the transcript
  yields `status_transcript_contradiction`.

## 10. `controller.events.jsonl`  →  `<worktree>/.agent-workspace/controller.events.jsonl`

- **Schema:** `controller-events/v1` declared on the **first line** as a header
  object `{ schema }`; every subsequent line is one event object. Append-only
  audit log; **not** drained into the manager inbox and never a decision input for
  the monitor (R4). **[default: JSONL, header-on-first-line]**
- **Fields per line:** `{ ts, run_id, event_type, detail }`.
- **States/transitions:** none (append-only).
- **Writer:** the lane controller (append). **Reader:** humans/diagnostics; not the
  monitor's status derivation.
- **Lock/atomic:** append-only; the controller is the single writer. (Not replaced,
  so the sibling-rename rule does not apply; a truncated final line is tolerated on
  read.)
- **Health check:** the first-line `schema` header is recognized; each subsequent
  line parses as an event object, and a malformed line is skipped (advisory log).
- **Recovery:** a partial trailing line is ignored; the log is advisory, so
  corruption never blocks lane progress.

## 11. `RESULT.json`  →  `<worktree>/RESULT.json`

- **Schema:** `result/v1`. The worker's result file (written from the truthful-result
  template); the record "structurally valid result" checks validate.
- **Fields:** `schema`; `lane_id`; `run_id`; `outcome` ∈ {`PASS`, `FAIL`, `BLOCKED`};
  `summary`; `evidence` (list of workspace-relative paths/refs); `content_hash`;
  `completed_at`. The worker **may not** self-accept: an `acceptance_state` written
  here is not honored — acceptance requires §12/§13 (completion-review 72–75).
- **States/transitions:** written once per run; replaced (fresh `run_id`) on resume.
- **Writer:** the worker (its result), validated by the controller.
- **Reader:** the controller (validity → `review_pending`/`result_invalid`); the
  completion-review command (the reviewer compares card criteria, `RESULT.json`,
  and cited evidence).
- **Lock/atomic:** written in the worktree by the worker; the controller reads it.
  **[default]** atomic sibling rename by the worker helper so a half-written result
  is never observed.
- **Health check ("structurally valid"):** parses; `schema` recognized; `lane_id`/
  `run_id` match this lane's current run; `outcome` in the enum; `content_hash`
  matches. Anything else → `result_invalid` (completion-review 132).
- **Recovery:** missing or invalid → controller records `result_invalid`; resume
  clears it for the fresh run (R8).

## 12. `COMPLETION_REVIEW.json`  →  `<rt>/epochs/<epoch-id>/lanes/<lane-id>/COMPLETION_REVIEW.json`

- **Schema:** `completion-review/v1`. The factual review record (the finding).
- **Fields:** `schema`; `lane_id`; `run_id`; `review_outcome` ∈ {`PASS`, `FAIL`,
  `BLOCKED`}; `review_summary`; `evidence` (refs ROOT cited); `task_card_id` +
  `task_card_hash`; `result_id` + `result_hash`; `commit`; `reviewed_at`;
  `content_hash`. It lives **outside** the worktree so the worker cannot write it.
- **States/transitions:** written once per run by the review command; replaced only
  after re-validating the same lane/run (completion-review 86–88).
- **Writer:** the `lane completion-review` command **only** (the sole supported
  writer); never hand-written; never the worker.
- **Reader:** the controller (to copy a valid `ACCEPTED` advancement into its
  status); retirement/archive (`--acceptance-ref`).
- **Lock/atomic:** lane-record lock + atomic sibling rename; written as a pair with
  §13.
- **Health check:** the card/result/review/acceptance hashes and IDs must all refer
  to the same task and commit (completion-review 35). One of the pair present
  without the other is a chain error.
- **Recovery:** both absent → `ACCEPTANCE_PENDING`; exactly one present → chain
  error surfaced (not silently repaired).

## 13. `ORCHESTRATOR_ACCEPTANCE.json`  →  `<rt>/epochs/<epoch-id>/lanes/<lane-id>/ORCHESTRATOR_ACCEPTANCE.json`

- **Schema:** `orchestrator-acceptance/v1`. ROOT's separate accept/reject decision.
- **Fields:** `schema`; `lane_id`; `run_id`; `approval` ∈ {`ACCEPTED`, `REJECTED`};
  `accepted_by` (non-empty; ROOT); `review_ref` (link to §12 `content_hash`);
  `task_card_id`/`hash`, `result_id`/`hash`, `commit`; optional
  `force_accept_reason` (present only when `--force-accept` overrode the
  `ACCEPTED`-requires-`PASS` rule); `decided_at`; `content_hash`. Outside the
  worktree.
- **States/transitions:** written once per run by the review command, paired with
  §12. `ACCEPTED` requires a `PASS` finding unless `force_accept_reason` is set.
- **Writer:** the `lane completion-review` command **only**.
- **Reader:** the controller (advancement); retirement (`--acceptance-ref`).
- **Lock/atomic:** lane-record lock + atomic sibling rename; paired with §12.
- **Health check:** same-task/commit hash+ID linkage as §12; `approval` in the enum;
  `ACCEPTED` without `PASS` requires a non-empty `force_accept_reason`.
- **Recovery:** as §12 (pair integrity; one-without-the-other is a chain error).

## 14. Lease file  →  `<rt>/resources/leases/<generated-from-resource-id>`

- **Schema:** `resource-lease/v1`. One file per currently-held exclusive resource;
  the folder is created empty by setup and stays empty when nothing is claimed.
- **Fields:** `schema`; `resource_id`; `lane_id`; `run_id`; holder `pid` +
  `creation_time`; `acquired_at`. The filename is generated deterministically from
  the `resource_id` (not from lane input). **[default field set — grounded in R14's
  orphan-detection needs]**
- **States/transitions:** created at launch when the lane's declared resource is
  free; removed on clean finish after cleanup proof; persists if the holder crashes
  (→ orphaned).
- **Writer:** the lane controller (creates at launch, removes after proving its own
  processes are gone, R14); a `REJECTED`/retirement path releases after cleanup;
  `lane force-stop` and an operator orphaned-lease clear both **force-release** it
  without the graceful cleanup handshake (R14 / operator-responses section).
- **Reader:** the launcher (a contended launch fails fast with `LAUNCH_LEASE_BUSY`,
  R14); the monitor (detects an orphaned lease: holder `pid`+`creation_time` dead or
  `lane_id`/`run_id` retired → `orphaned_lease`).
- **Lock/atomic:** resource-lease lock + atomic create/remove; multi-resource
  acquisition is all-or-nothing (R14).
- **Health check:** holder identity is a live process and the `lane_id`/`run_id` is
  an active lane.
- **Recovery:** orphaned leases are **not** auto-reclaimed; the monitor surfaces
  `orphaned_lease` and ROOT force-releases (R14). Its clearing is the plain
  force-release of R14 (no enforced attestation).

## 15. `overlay-receipt.json`  →  `<worktree>/.agent-workspace/overlay-receipt.json`

- **Schema:** `overlay-receipt/v1`. The receipt bootstrap writes when it applies the
  selected cache overlay (epoch-runtime: bootstrap "applies the selected cache
  overlay and writes its receipt").
- **Fields:** `schema`; `lane_id`; `run_id`; `profile` (`managed`/`plain`);
  `base_cache_ref` (the `super-cache/workspace` version applied); `provider_payload`
  (the `adapter-payloads/<provider-id>` applied, managed only); `applied_at`.
  **[default field set]**
- **States/transitions:** written once at bootstrap; rewritten on resume for the
  fresh run. **[default]**
- **Writer:** bootstrap. **Reader:** diagnostics / resume verification (that the
  expected overlay was applied). Not a monitor decision input.
- **Lock/atomic:** written in the worktree at bootstrap; atomic sibling rename.
- **Health check:** `schema` recognized and `lane_id`/`run_id` match the lane's
  current run.
- **Recovery:** advisory; a missing/mismatched receipt is a bootstrap/resume
  integrity signal, not a runtime blocker.

## 16. Controller invocation  →  `<worktree>/.agent-workspace/invocation.json`

- **Schema:** `controller-invocation/v1`. The launch specification bootstrap writes
  and the launch route later *consumes* to start the lane's controller/provider
  (epoch-runtime: bootstrap "writes the … controller invocation JSON"; "a separate
  public launch route consumes the written invocation later"). **[default filename;
  the v2 docs name it "the controller invocation JSON" — only the historical doc
  spells `invocation.json`]**
- **Fields:** `schema`; `lane_id`; `run_id`; `provider` (`{ id, model }`); the
  resolved launcher entry point and argument vector; the base child environment and
  working directory; the worktree and artifact paths; `content_hash`; `created_at`.
- **States/transitions:** written once at bootstrap (`status: prepared`); replaced
  with a fresh `run_id` on resume; consumed (read) by launch — launch does not
  rewrite it.
- **Writer:** bootstrap (a short program). **Reader:** the launch route (and the
  controller it starts). ROOT never edits it.
- **Lock/atomic:** written in the worktree at bootstrap via atomic sibling rename;
  read-only thereafter.
- **Health check:** parses; `schema` recognized; `lane_id`/`run_id` match the lane's
  current run; the launcher entry point resolves. A malformed invocation is exactly
  the launch failure `LAUNCH_INVOCATION_INVALID`.
- **Recovery:** on `LAUNCH_INVOCATION_INVALID`, re-bootstrap the lane; resume writes
  a fresh invocation for the new run.
- **Sibling bootstrap inputs (same writer, same lifecycle, not separately schema'd):**
  the **worker prompt** and the **truthful-result template** bootstrap also writes
  into the worktree are per-lane inputs (not mutable runtime state); they follow the
  same atomic-write and resume-refresh rules. `RESULT.json` (§11) is filled against
  that template.

---

## Decisions (both resolved)

Everything above is settled. The two points that were returned for a call have both
been decided:

**A. `cleanup_unproven` — resolved: monitor-derived.** The controller records the raw
fact `cleanup_proven` (has it confirmed its own provider/helper processes are gone)
in `controller.status.json`; it does **not** record `cleanup_unproven` as a status.
The monitor derives `cleanup_unproven` when a lane's controller is alive and its
result is terminal but `cleanup_proven` is still false — a stuck cleanup, distinct
from `orphaned_lease` (holder already dead). This matches the monitor's admission
list in `harness-scan-watch-queue-disconnection.md` ("cleanup proof failure"). §9 is
finalized accordingly.

**B. Identity/hash scheme — resolved: the simple default.** `sha256` over canonical
JSON in `content_hash`, opaque generated IDs, operator-supplied `lane_id`, integrity
only (no signing, no PKI). See the conventions section above.

---

# Part XVII — Public CLI contract (all commands)

This part is the complete, authoritative contract for every public `operator_launch`
command: purpose, inputs, success output, stable failure codes, next action, and ownership
boundary. The shared conventions apply to every command, then each command follows.
## Conventions (apply to every command)

- **Invocation.** All commands are subcommands of the one launcher binary,
  `operator_launch …`. There is no other public entry point; ROOT never edits
  records by hand.
- **Exit + output. [default]** Success = process exit `0` with a short human status
  line on stdout (bootstrap's is the documented `status: prepared`); every command
  accepts `--json` to emit a machine-readable result object instead. **Every public
  command returns a small structured result with the fields `{ ok, code, summary,
  evidence_paths, next_action }`** — `ok` (success boolean); `code` (a short stable reason,
  not a generic exception); `summary` (plain-English); `evidence_paths` (exact paths); and
  `next_action` (a safe suggested next step). A command must not return only a generic
  exception or force ROOT to search logs. Failure =
  non-zero exit with a single stable failure code from this contract on stderr,
  plus a human message. A failure code names the exact offending path/id where one
  applies (e.g. `BOOTSTRAP_CACHE_COLLISION` names the destination).
- **No partial writes.** Any command that replaces a record does so through the
  temp-sibling + atomic-rename rule under that record's lock (see the schema
  ledger); a failed command leaves the prior state intact.
- **Ownership.** These are ROOT/operator-facing commands. Bootstrap, launch,
  resume, force-stop, retire, and shutdown are *short programs*, not agents — they
  validate, act, and return. The lane **controller** (not ROOT, not these commands)
  is what actually runs a provider and owns live leases; the **monitor** is the
  sole producer of manager-queue events. Commands never spawn a provider except
  where noted (launch, via the controller).
- **Profiles.** `--event-id` selects a managed lane through its queue event;
  `--lane-id` selects a lane by record (the plain-mode form, and the direct form
  for force-stop/retire). The two selectors are never combined.
- **Records touched** per command reference the schema ledger sections (§N there).
- **No separate provider-binding command.** In v2, binding a provider's hooks to the
  manager queue is performed by `setup` (installs/checks the payloads and bindings)
  and `bootstrap` (installs/binds event-delivery material for the lane). There is no
  standalone `adapter install` / `adapter check` / `adapter bind` public command —
  those belong to the historical *candidate* protocol in `subagent_hooks.md` (which
  the master classifies as compatibility evidence, not the v2 runtime surface), not
  to this contract.

---

## `operator_launch harness setup [--overwrite]`

- **Purpose:** one-time integration — install ROOT payloads, build the active cache,
  write the active resource manifest + lease dir, start the monitor. Idempotent.
  `--overwrite` replaces only the planned harness/adapter targets (and reports them).
- **Inputs:** none beyond `--overwrite`; reads `<harness-root>/harness-config.json`
  and `<harness-root>/resource-manifest.json`.
- **Success:** exit 0; runtime is `OPEN` and `<rt>/resources/RESOURCE_MANIFEST.json`
  exists.
- **Failure codes:** `SETUP_CONFIG_INVALID`, `SETUP_CACHE_INVALID`,
  `SETUP_RESOURCE_MANIFEST_INVALID`, `SETUP_ADAPTER_COLLISION`,
  `SETUP_OVERWRITE_FAILED`, `SETUP_MONITOR_ALREADY_RUNNING` (informational — a live
  monitor already exists, nothing started).
- **Next action:** on `SETUP_MONITOR_ALREADY_RUNNING`, proceed (already running); on
  collision codes, resolve the named target or re-run with `--overwrite`.
- **Ownership:** operator/ROOT. **Records:** RUNTIME_STATE §1, manager QUEUE §6
  (managed), RESOURCE_MANIFEST, MONITOR §8, the active cache.

## `operator_launch harness shutdown`

- **Purpose:** end the whole runtime — retire every live lane through its normal
  cleanup route, then stop the persistent monitor. Cleanup-proof-first.
- **Inputs:** none.
- **Success:** exit 0; all lanes retired, monitor `STOPPED`, `RUNTIME_STATE`
  `CLOSED` (via `SHUTTING_DOWN`).
- **Failure codes:** `SHUTDOWN_LANE_CLEANUP_UNPROVEN` (a lane's processes could not
  be proven gone), `SHUTDOWN_MONITOR_UNPROVEN`, `SHUTDOWN_RUNTIME_AMBIGUOUS`. On
  failure it preserves evidence and does **not** retry with broad kills.
- **Next action:** for `SHUTDOWN_LANE_CLEANUP_UNPROVEN`, `lane force-stop` the
  offending lane(s), then retry shutdown.
- **Ownership:** operator/ROOT. **Records:** RUNTIME_STATE §1, CURRENT_EPOCH §2
  (cleared before close), lane §5, lease §14, MONITOR §8.

## `operator_launch lane bootstrap --lane-id <id> --provider <p> --model <m> [--exclusive-resource <rid> …] --task-card <file>`

- **Purpose:** prepare one lane — create its worktree + `.agent-workspace`, apply the
  cache overlay, write the worker prompt/result template and the controller
  invocation. Opens a new epoch if none is active. Does **not** start a provider or
  take a lease.
- **Inputs:** `--lane-id` (operator-chosen, unique for the epoch's lifetime);
  `--provider`, `--model`; zero or more `--exclusive-resource <rid>` (each must be
  in the active manifest); `--task-card`.
- **Success:** exit 0; `status: prepared`; `lane.json`, worktree, and `active-lanes`
  entry exist.
- **Failure codes:** `BOOTSTRAP_REQUEST_INVALID`, `BOOTSTRAP_LANE_ID_IN_USE` (id
  already used this epoch, incl. a retired lane — R1), `BOOTSTRAP_WORKTREE_EXISTS`,
  `BOOTSTRAP_CACHE_COLLISION`, `BOOTSTRAP_ADAPTER_MISSING`,
  `BOOTSTRAP_RESOURCE_UNDECLARED` (a named resource is not in the manifest).
- **Next action:** on success, `lane launch` the lane; on `…RESOURCE_UNDECLARED`,
  fix the manifest (requires shutdown to change it) or drop the resource.
- **Ownership:** ROOT (short program). **Records:** lane §5, active-lanes §4,
  epoch-state §3, CURRENT_EPOCH §2, overlay-receipt §15.

## `operator_launch lane launch --lane-id <id>`

- **Purpose:** consume the prepared invocation and start the lane — the controller
  starts the provider process and, for a managed lease-enabled lane, atomically
  acquires all declared exclusive leases (all-or-nothing, fail-fast).
- **Inputs:** `--lane-id`.
- **Success:** exit 0; lane `running`; leases (if any) held by the controller.
- **Failure codes:** `LAUNCH_INVOCATION_INVALID`, `LAUNCH_BINDING_FAILED`,
  `LAUNCH_LEASE_BUSY` (a declared resource is held — ordinary contention, not a
  crash), `LAUNCH_CONTROLLER_START_FAILED`, `LAUNCH_PROVIDER_START_FAILED`.
- **Next action:** on `LAUNCH_LEASE_BUSY`, ROOT waits for the current holder to
  finish and re-launches (R14 — ROOT orchestrates the wait; no lane sits waiting).
- **Ownership:** ROOT invokes; the **controller** performs the start and owns the
  lease. **Records:** lane §5, lease §14, controller.status §9.

## `operator_launch lane completion-review (--event-id <id> | --lane-id <id>) --review-outcome PASS|FAIL|BLOCKED --approval ACCEPTED|REJECTED --review-summary "…" [--evidence <path> …] [--force-accept --force-reason "…"]`

- **Purpose:** record ROOT's review of a finished lane and write the paired
  `COMPLETION_REVIEW.json` + `ORCHESTRATOR_ACCEPTANCE.json`. Managed selects the lane
  via its acknowledged review event (`--event-id`); plain via `--lane-id`.
- **Inputs:** `--review-outcome` (the factual finding) **and** `--approval` (ROOT's
  separate accept/reject decision) — two independent, both-required fields, not
  alternatives; `ACCEPTED` requires a `PASS` finding unless `--force-accept
  --force-reason "…"` overrides it. `--review-summary`, optional `--evidence`.
- **Success:** exit 0; the review/acceptance pair written; managed review event set
  `COMPLETE` (the command closes its own event). `ACCEPTED` advances the lane
  toward `accepted`/retirement; `REJECTED` leaves it for resume.
- **Failure codes:** `COMPLETION_REVIEW_EVENT_INVALID`,
  `COMPLETION_REVIEW_NOT_ACKNOWLEDGED` (managed event not `ACKNOWLEDGED` first),
  `COMPLETION_REVIEW_STALE_SOURCE` (card/result/run no longer current),
  `COMPLETION_REVIEW_FORCE_REASON_INVALID` (`ACCEPTED`+non-`PASS` without a reason),
  `COMPLETION_REVIEW_OUTPUT_CONFLICT` (a review/acceptance pair already exists),
  `COMPLETION_REVIEW_WRITE_FAILED`.
- **Next action:** `REJECTED` → `resume-lane`; `ACCEPTED` → `lane retire` when done.
- **Ownership:** ROOT; this command is the **only** writer of `COMPLETION_REVIEW.json`
  and `ORCHESTRATOR_ACCEPTANCE.json`. **Records:** COMPLETION_REVIEW §12,
  ORCHESTRATOR_ACCEPTANCE §13, RESULT §11 (read), lane §5, manager QUEUE §6 (managed).

## `operator_launch resume-lane --lane-id <id> --resume-task-card <file> [--rationale "…"]`

- **Purpose:** re-run a stopped, unaccepted lane in its **same worktree and provider
  session** with a fresh `run_id`. Clears the prior run's `RESULT.json`,
  `COMPLETION_REVIEW.json`, `ORCHESTRATOR_ACCEPTANCE.json`, and the worker inbox
  `QUEUE.json` for the new run (R8). It re-does work; it is not a cleanup tool.
- **Inputs:** `--lane-id`, `--resume-task-card`, optional `--rationale`. It never
  reconstructs a session, PID, worktree, or invocation.
- **Success:** exit 0; lane `running` under a new `run_id`.
- **Failure codes:** `ALREADY_ACCEPTED` (lane already has a valid acceptance chain —
  no re-resume), `LANE_RUNNING` (still active), `RESUME_WORKTREE_MISSING`,
  `NO_SAVED_SESSION_ID` (no native session to resume), `INVALID_RESUME_TASK_CARD`,
  `RESUME_LANE_WRITE_FAILED`, or the provider's native resume error.
- **Next action:** on `RESUME_WORKTREE_MISSING`/`NO_SAVED_SESSION_ID`, the honest
  path is a **new** lane (fresh bootstrap), not a resume.
- **Ownership:** ROOT (short program). **Records:** lane §5, worker inbox §7, RESULT
  §11, COMPLETION_REVIEW §12, ORCHESTRATOR_ACCEPTANCE §13 (all reset for the new run).

## `operator_launch lane force-stop --lane-id <id>`

- **Purpose:** hard-stop one stuck lane — forcibly terminate its provider, helper,
  and controller processes (matched by the `lane.json` identities), force-release
  any exclusive lease it held, and mark it `retired`. The single-lane counterpart to
  `harness shutdown`; the escalation for `cleanup_unproven`/wedged controller.
- **Inputs:** `--lane-id` (both profiles).
- **Success:** exit 0; the lane's processes gone, its lease released, lane `retired`.
- **Failure codes [default]:** `FORCE_STOP_LANE_NOT_FOUND`,
  `FORCE_STOP_PROCESS_SURVIVED` (a process could not be terminated even forcibly),
  `FORCE_STOP_LEASE_RELEASE_FAILED`.
- **Next action:** on `FORCE_STOP_PROCESS_SURVIVED`, escalate to the operator/host
  (an unkillable process is outside the harness's authority).
- **Ownership:** ROOT; force-release carries the operator-owns-the-risk stance of the
  R14 orphaned-lease clear. **Records:** lane §5 (→ retired), lease §14 (force-release).

## `operator_launch lane retire --acceptance-ref <file>`

- **Purpose:** gracefully retire one **accepted** lane for archive/close — cleanup-
  proof-first, releasing its lease after proof. The normal end for a lane that
  passed review (as opposed to force-stop, which is the forceful end for a stuck one).
- **Inputs:** `--acceptance-ref` (a reference to the lane's existing
  `ORCHESTRATOR_ACCEPTANCE.json`; it does not create acceptance).
- **Success:** exit 0; lane `retired`, lease released after cleanup proof, branch
  retained.
- **Failure codes [default]:** `RETIRE_ACCEPTANCE_MISSING`/`RETIRE_ACCEPTANCE_INVALID`
  (no valid accepted chain), `RETIRE_LANE_ACTIVE`, `RETIRE_CLEANUP_UNPROVEN` (mirrors
  the shutdown code), `RETIRE_WRITE_FAILED`.
- **Next action:** on `RETIRE_CLEANUP_UNPROVEN`, `lane force-stop` then treat as done.
- **Ownership:** ROOT. **Records:** lane §5 (→ retired), lease §14, CURRENT_EPOCH §2
  (a retirement that empties the epoch triggers epoch close per R9).

## `operator_launch manager acknowledge --event-id <id>`

- **Purpose:** move one manager-queue event from `PENDING` to `ACKNOWLEDGED` after
  ROOT has read it. Managed only.
- **Inputs:** `--event-id` (the exact top-level event id ROOT read).
- **Success:** exit 0; event `ACKNOWLEDGED`.
- **Failure codes [default]:** `MANAGER_ACK_EVENT_NOT_FOUND`,
  `MANAGER_ACK_ALREADY_ACKNOWLEDGED`, `MANAGER_ACK_NOT_ROOT_EVENT`.
- **Next action:** handle the event, then `manager close`.
- **Ownership:** ROOT is the sole state-advancer of queue events. **Records:**
  manager QUEUE §6.

## `operator_launch manager close --event-id <id> --outcome COMPLETE|BLOCKED`

- **Purpose:** close an acknowledged manager-queue event. `--outcome` is the event's
  **close state** (unrelated to a lane review's `--review-outcome`). Managed only.
- **Inputs:** `--event-id`, `--outcome COMPLETE|BLOCKED`.
- **Success:** exit 0; event `COMPLETE` (or `BLOCKED` with a reason).
- **Failure codes:** `MANAGER_CLOSE_NOT_ACKNOWLEDGED`, `MANAGER_CLOSE_ALREADY_CLOSED`,
  `MANAGER_CLOSE_NOT_ROOT_EVENT`, `MANAGER_CLOSE_INVALID_OUTCOME`.
- **Next action:** none — but closing the event does not clear the underlying
  condition (see the operator-responses section); the condition clears only when
  ground truth changes.
- **Ownership:** ROOT. **Records:** manager QUEUE §6.

## `operator_launch send-lane-notification --lane-id <id> --prompt "…"`

- **Purpose:** append one assignment to a running managed lane's worker inbox. It does
  not modify the manager queue and does not claim the worker has seen it. Managed
  only; a plain or non-running lane cannot be messaged.
- **Inputs:** `--lane-id`, `--prompt`.
- **Success:** exit 0; one `PENDING` assignment appended to the lane inbox.
- **Failure codes [default]:** `SEND_LANE_NOT_FOUND`, `SEND_LANE_NOT_MANAGED`,
  `SEND_LANE_NOT_RUNNING`, `SEND_LANE_WRITE_FAILED`.
- **Next action:** none; the worker acts via its `lane-assignment` skill.
- **Ownership:** ROOT (via this command) is the only writer that *appends*
  assignments to the worker inbox; the worker advances an assignment's state
  (`PENDING`→`ACKNOWLEDGED`→`COMPLETE`/`BLOCKED`) via its `lane-assignment` helper.
  **Records:** worker inbox §7.

## `operator_launch scan --no-write` and `operator_launch watch --until-actionable [--timeout <dur>] [--until-event <id>]`

- **Purpose:** ROOT-side polling of lane status. `scan --no-write` returns a
  read-only snapshot (no record writes); `watch --until-actionable` occupies the
  ROOT session and blocks until an actionable condition exists. Primary in plain mode
  (no queue to push events); a plain lane cannot wake ROOT, so ROOT scans on return
  and watches while deliberately idle.
- **Inputs:** `scan`: `--no-write`. `watch`: `--until-actionable`, optional
  `--timeout`, optional `--until-event`.
- **Success:** exit 0; `scan` prints the snapshot; `watch` returns when an actionable
  condition appears (or on `--timeout`).
- **Failure codes [default]:** `SCAN_NO_ACTIVE_EPOCH`; `WATCH_TIMEOUT` (if
  `--timeout` elapses with nothing actionable).
- **Next action:** act on the reported condition per the operator-responses table.
- **Ownership:** ROOT; read-only (`scan`) / blocking read (`watch`). **Records:**
  reads active-lanes §4, lane §5, controller.status §9; writes none.

## `operator_launch health reconcile` **[default form]**

- **Purpose:** the manual entry point to the health reconciliation the monitor already
  runs at startup and each pass — rebuild `active-lanes.json` from the epoch's
  controlled `lanes/` directory and re-derive lane status. (The routine path is
  automatic; this is the on-demand invocation R9 refers to.)
- **Inputs:** none.
- **Success:** exit 0; `active-lanes.json` rebuilt/consistent.
- **Failure codes [default]:** `HEALTH_RECONCILE_NO_ACTIVE_EPOCH`.
- **Next action:** none in the normal case.
- **Ownership:** ROOT/operator; the monitor owns the automatic path. **Records:**
  active-lanes §4 (rebuilt), lane §5 (read), epoch-state §3 (read).

---

## Decisions (both resolved)

Both open choices have been decided; this contract is settled.

**A. Command grouping — resolved: keep as-is.** Most lane operations are `lane`
subcommands (`lane bootstrap`, `lane launch`, `lane completion-review`,
`lane force-stop`, `lane retire`), while `resume-lane` and `send-lane-notification`
remain top-level hyphenated commands (with matching ROOT skill names). These forms
stay as-is — they are embedded across every doc and skill name, and unifying them
would be churn for a cosmetic gain.

**B. Defaulted failure codes / `health reconcile` form — resolved: accepted.** The
`setup-details` failure table (setup, bootstrap, launch, resume, manager-close,
completion-review, shutdown) is authoritative and reused verbatim. The failure-code
sets marked **[default]** above for `manager acknowledge`, `send-lane-notification`,
`lane force-stop`, `lane retire`, `scan`/`watch`, and the `operator_launch health
reconcile` invocation form are accepted as specified — they are now part of this
contract (the `[default]` tag marks provenance, not an open question).

---

# Part XVIII — Cross-platform portability

The harness is cross-platform and targets Windows, macOS, and Linux equally. No component,
contract, helper, hook, or launcher may hardcode a platform assumption.

- **Paths.** Path examples in this document use forward-slash notation for readability; an
  implementation joins and stores paths with the host's native separator and must not assume
  a particular one. No drive-letter or platform-specific absolute-path form is normative.
- **Process identity and liveness.** A process is identified by its process ID plus its
  start/creation time and checked for liveness through a cross-platform process API — never a
  platform-specific call. (A reused PID with a different creation time is not the same
  process.)
- **Launcher and scripts.** "The launcher" and "a helper script" mean the platform-native
  entry point; no specific extension (`.cmd`, `.ps1`, `.sh`) is normative, and shell examples
  use platform-neutral syntax.
- **No platform-specific vocabulary is normative.** Terms such as reparse point, junction,
  drive letter, or a specific OS's environment-variable names must not appear as
  requirements; use neutral descriptions (symbolic link or path redirection; a system
  temporary directory; the operating system).
- **Filesystem semantics.** The harness relies only on portable guarantees — same-volume
  atomic rename/replace and advisory process-scoped file locks — not on any one OS's
  filesystem behavior.

Appendix A (historical) may name the prior system's platform specifics as a matter of
record; those are descriptions of the old system, not requirements of this design.

---

# Part XIX — Remaining work

The v2 **design** is complete and internally consistent; every mechanism, record, and
command above is specified. What remains is verification and a few optional refinements —
none blocking the design.

## XIX.1 Scoped tasks

1. **Epoch-breaking-change table** — ✅ complete (Part VII.2–VII.3).
2. **Versioned record schemas** — ✅ complete (Part XVI; all records, both prior decisions
   resolved: identity/hash = `sha256` over canonical JSON, integrity-only, no signing;
   `cleanup_unproven` = monitor-derived).
3. **One public CLI contract** — ✅ complete (Part XVII; both prior decisions resolved:
   command grouping kept as-is; defaulted failure codes / `health reconcile` form accepted).
4. **Native verification matrix** — ⚠️ **not done; requires real-CLI execution.** On actual
   Codex, Claude Code, and Qwen Code, prove: the Stop hook rejects unresolved ROOT/worker
   work and an invalid/missing `RESULT.json`; it permits a valid `PASS`/`FAIL`/`BLOCKED`
   terminal; one role's queue never blocks another; the monitor-liveness hook restarts a
   dead/hung monitor (and never a deliberately stopped one); and a lease is freed and reused
   in series across lanes. This is execution against a real environment; the test *plan* can
   be drafted, but running it is outside a documentation pass.

## XIX.2 Optional refinements (previously flagged; none required)

- A distinct `force_stopped` lane-lifecycle value vs plain `retired`, if force-stops should
  be auditable as such in `lane.json`.
- An explicit "these are the prior system's names, not v2" caveat at the old token names in
  Appendix A (they are already fenced by the appendix heading).
- An escalation timer that re-promotes a still-present condition after an interval even
  without a status change — recommended **against** (it fights the clean single-dedup rule,
  and the lease/shutdown backstops already catch the cases that matter).

---

# Appendix A — Historical diagnosis and candidate protocol (NOT the v2 spec)

**Everything in this appendix describes the prior/candidate system and is superseded by
Parts I–XIX.** It is preserved so this file can fully replace the original documents, but a
v2 implementer should use the body above and treat this appendix as background only. In
particular, the **coordinator, `REGISTRATION.json`, `DELIVERY.jsonl`, `WAKE.json`,
`STATE.json`, `QUEUE.jsonl`, the multi-file router, and the `adapter install`/`check`/`bind`
command protocol described here are NOT v2** — v2 uses a single authoritative `QUEUE.json`,
the monitor as sole producer, a `MONITOR.json`-based heartbeat, and binding folded into
setup/bootstrap (Parts IX–X). The one part that **does** carry into v2 is the live-proof
*evidence* that Codex, Claude Code, and Qwen Code natively execute PostToolUse and honor
Stop rejections (used by Part VI.3); the binding/coordinator *protocol* around that proof
does not.

## A.1 Subagent CLI hooks — compatibility evidence and candidate binding protocol

*(Verbatim, from `subagent_hooks.md`. Its PostToolUse/Stop proofs carry into v2; its
binding/coordinator protocol does not.)*


> **Status: historical compatibility evidence, not the v2 queue protocol.**
> This file proves the three native CLIs execute PostToolUse hooks. Its candidate
> binding, coordinator, and multi-file router details do not carry into v2.

## Firmware v2 candidate readiness

The new firmware v2 candidate (`harness-single`) now supports real
project-local subagent hooks on all three shipped CLI hosts: Codex, Claude
Code, and Qwen Code. This is no longer a proposed or synthetic capability: a
native headless launch of each CLI executed a tool and produced the harness's
durable PostToolUse delivery record.

That closes the hook-feasibility question for the new-harness design. We can
now specify the revamp on the assumption that a fresh, explicitly bound
subagent lane can notify its registered manager at PostToolUse. The remaining
specification work is the harness's control-plane and recovery design, not
whether these shipped CLIs can run the required hook.

This conclusion is intentionally narrow. It proves the notification premise,
not every lifecycle hook in every provider mode, and it does not make hook
delivery an acknowledgement, a scheduler, or a replacement for manager-owned
state.

## Revamp compatibility decision

The new harness starts fresh v2 runtime roots. It does not open, migrate, or
preserve an existing candidate queue, binding, coordinator, or in-flight lane
record. Those existing records remain only archival/forensic evidence. The
proven candidate supplies one native-provider fact to retain: a lane can use its
own provider-local binding and hook configuration. V2 keeps that lane-specific
binding, but ROOT does not inherit the candidate's queue bind/fresh-session
lifecycle: its static hook wrapper uses the fixed runtime manager queue and the
generic current-epoch marker. V2 therefore carries no compatibility code for the
candidate's multi-file `ManagerEventRouter` records.

## Scope and decision

This record covers the shipped subagent CLI resources in the current
`harness-single` candidate:

- Codex CLI (`--host codex`)
- Claude Code CLI (`--host claude`)
- Qwen Code CLI (`--host qwen` or `--host qwen-code`)

All three now use the same setup contract. Installing a project adapter only
writes that provider's project-local hook configuration. It does **not** guess
a manager, create a queue, or bind the project automatically. The manager must
create the real `ManagerEventRouter`, then explicitly bind the prepared project
to that registered queue before a fresh provider session starts.

```text
install provider project files
    -> manager creates/registers its queue
    -> adapter bind records that exact queue identity
    -> fresh CLI subagent session executes a tool
    -> PostToolUse hook delivers a sparse manager notice
    -> manager retains the original event until explicit acknowledgement
```

This is deliberately small. A hook is not a scheduler, a second queue, an
automatic repair service, or an acknowledgement path.

## Public setup surface

The caller uses the provider that matches the launched CLI:

```shell
python -m orchestrator_harness adapter install --host <codex|claude|qwen> --project-root $lane
python -m orchestrator_harness adapter bind --host <codex|claude|qwen> --project-root $lane --queue-root $managerQueue
```

`--coordinator-root` remains optional. If it is omitted, the binding creates
only the provider-specific coordinator directory beneath the already-existing
manager queue. It never creates a manager queue.

`adapter bind` is safely repeatable only when the existing record is byte-for-
byte the same binding. It rejects a missing manager registration, a stale or
cross-bound record, a changed project/queue/coordinator directory identity, an
adapter revision mismatch, or a changed manager registration. The recovery is
to use the actual current manager queue and start a fresh provider session.
The one exception is the exact pre-v1 Claude record for those same binding
facts: an explicit Claude `adapter bind` migrates it to the closed v1 record.
It does not migrate malformed, changed, or cross-bound legacy records.

## Binding contents and hook semantics

Each provider writes one closed binding record inside its project directory:

| Provider | Binding file | Default coordinator folder |
| --- | --- | --- |
| Codex | `.codex/orchestrator-harness-binding.json` | `codex-coordinator` |
| Claude Code | `.claude/orchestrator-harness-binding.json` | `claude-coordinator` |
| Qwen Code | `.qwen/orchestrator-harness-binding.json` | `qwen-coordinator` |

Every record includes the adapter schema/version/package revision; project,
queue, and coordinator paths plus filesystem identities; and the exact
`run_id`, `queue_id`, manager session/thread/invocation IDs, registration ID,
and registration generation. The hook re-checks those facts against
`REGISTRATION.json` before it sends anything.

At PostToolUse, the installed hook reads only that bound queue and produces a
content-free delivery notice: pending count, highest class/severity, binding
identity, and timestamp. The durable delivery receipt has `outcome:
"DELIVERED"` when the provider hook boundary ran. It does **not** carry an
event payload, mark work complete, or acknowledge the manager event. The event
stays pending until the manager explicitly handles and acknowledges its
top-level event ID.

An installed but unbound project is a setup error. Codex, Claude, and Qwen now
all fail loudly with an `installed <provider> hook has no harness binding`
error instead of silently pretending delivery occurred.

## Provider-specific repairs

### Codex

Codex already had project hook assets but needed an explicit queue-binding
setup path. The completed repair binds the lane to the real manager queue,
stores a closed identity-checked record, and configures the native Codex
session to load the owned project hook fragment. It was live-proven through
`operator_launch -> lane_controller -> codex exec` with GPT-5.6 Luna at medium
reasoning: one `git status --short` tool call produced a durable PostToolUse
delivery receipt.

### Claude Code

Claude had an installer and hook scripts, but no public `adapter bind` command.
The repaired path adds `activate_claude_binding`,
`bind_claude_project_from_queue`, and `adapter bind --host claude`. It uses the
same closed binding validation as Codex and Qwen. The former unbound-hook
no-op has been removed: missing binding is visible and recoverable.

Claude Code 2.1.239 was live-proven through the native launcher with `claude
--print`, model `sonnet`, and `Bash` allowed. It ran `git status --short`,
returned `CLAUDE_HOOK_PROOF_COMPLETE`, and produced a durable `DELIVERED`
PostToolUse receipt for a real pending manager event.

### Qwen Code

Qwen now has the same explicit binding API and CLI path. Its actual headless
command is `qwen`, not the obsolete `qwen exec` shape. The controller resolves
the Qwen launcher before creating the isolated child process,
which prevents command-discovery failure. The safe base child environment also
retains the minimal non-secret platform environment variables the launcher needs; otherwise the CLI creates a
literal unresolved-environment-variable cache directory in the lane.

Qwen Code 0.21.10 was live-proven with the existing local
Ollama-compatible configuration selecting `deepseek-v4-flash:0731-cloud`. It
ran `git status --short`, returned `QWEN_HOOK_PROOF_COMPLETE`, and produced a
durable `DELIVERED` PostToolUse receipt. The harness neither read nor wrote
provider credentials.

## Live-proof conditions and limits

Each proof used a fresh ignored runtime root, a fresh Git lane, one real
registered manager queue containing one pending `MANAGER_SIGNAL`, and the
native `operator_launch -> lane_controller` route. The provider performed
exactly one harmless Git status command. The proof criterion was independent
of transcript wording: the manager's durable `DELIVERY.jsonl` and the bound
coordinator both recorded a `post_tool_use` receipt with `outcome:
"DELIVERED"`.

The source-checkout proofs granted only `PYTHONPATH` so the project-local hook
scripts could import the uninstalled harness package. A normal installed
harness does not need that temporary grant. The proofs establish the
PostToolUse path; they do not claim that every provider invokes every hook type
in every interactive, safe-mode, or disabled-customization configuration.

## Observable acceptance criteria

The repair is complete only when all of these remain true:

1. `adapter install`, `adapter check`, and `adapter bind` accept each shipped
   provider host and operate only inside the caller-selected project plus the
   already-existing manager queue/coordinator location.
2. Binding to an absent, stale, cross-bound, symbolic-link, or unregistered
   queue fails without redirecting the project to a synthetic queue.
3. A real headless tool call for each provider writes a durable
   `post_tool_use`/`DELIVERED` receipt for a real pending event.
4. The event remains pending after delivery; only the manager can acknowledge
   it.
5. A missing binding is an actionable error, not a success or a fake delivery.
6. The provider-specific launch form stays native: `codex exec`, `claude
   --print`, and `qwen`.

The provider-specific reproducible proof contracts live in
`harness-single/docs/codex-headless-hook-proof.md`,
`harness-single/docs/claude-headless-hook-proof.md`, and
`harness-single/docs/qwen-headless-hook-proof.md`.

---

## A.2 Detailed architecture review (candidate diagnosis)

*(Verbatim, from `harness-detailed-architecture-review.md`. Diagnosis of the candidate/old
system; superseded by the v2 body above.)*


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

### Appendix (historical, within A.2): direct-English implementation description

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

---

## A.3 Executor, Stop-hook, and manager-queue coupling (candidate diagnosis)

*(Verbatim, from `harness-executor-stop-hook-manager-queue-coupling.md`. Diagnosis of the
candidate/old coupling; superseded by the v2 body above.)*


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

## A.4 Candidate condition/status names and rejected files (superseded)

For completeness, these are the prior/candidate code's internal names, preserved so no
source detail is lost. **They are superseded and not v2.** The v2 actionable-status set is in
Part IX (`review_pending`, `result_invalid`, `controller_exited`,
`provider_exited_no_result`, `status_transcript_contradiction`, `cleanup_unproven`,
`orphaned_lease`); the v2 failure codes are in Part XVII.

The candidate scan/watch/queue diagnostic used these condition names (v2 replaces them):
`CONTROLLER_EXITED` (provider/controller ended), `CODING_RESULT_INVALID` (result missing or
malformed), `RESULT_AVAILABLE` (a result appeared), `WAITING_RESOURCE` (a lane waiting for a
held resource), `STALE_STATUS` (status says running but transcript says terminal),
`LANE_STAGE_REPEAT`, `RELAY_READY`, `REQUEST_EXPIRING`, `REQUEST_STALE`, `RESOURCE_AMBIGUOUS`,
and `RESOURCE_CONFLICT`. The candidate global process shutdown used a single shared
`processes.json` process list — **explicitly rejected** in v2 (Part XIV.3: no global mutable
process list; each controller owns and cleans its own processes).

The candidate harness also used a sprawl of per-lane binding/config fields that v2's fixed
paths and derived runtime tree eliminate: `queue_root`, `coordinator_root`, `event_log_path`,
`resource_lock_root`, `output_dir`, `suite_root`, `run_globs`, `manager_queue_path`,
`manager_queue_id`, `manager_actionable` (old event flag), `codex_pid`, `launch_options`,
`idle_prompt`, and a `workspace_relpath` config value; and example bootstrap/cleanup function
names `bootstrap_coding_lane`, `cleanup_coding_lane`, and `my_cli_bootstrap`. (The escalation
helper's `--severity` argument — e.g. `blocking` — and the hook-dispatch `--boundary`
argument survive into v2 as ordinary invocation details; see Parts X.4–X.5.)

---

# Appendix B — Source-document to master-section map

Where each original document's content lives in this master. **Verbatim** = embedded
unchanged; **absorbed** = its v2 content is synthesized (and, per part, made more detailed
and reconciled) into the named parts.

| Source document | Location in this master | Mode |
| --- | --- | --- |
| `harness_single.md` (authority: R1–R16, principles, tasks, remediation, cross-platform) | Parts I, III, VII, IX–XV, XVIII, XIX | absorbed |
| `harness-record-schemas.md` | Part XVI | verbatim |
| `harness-cli-contract.md` | Part XVII | verbatim |
| `setup-details.md` | Parts V, VI | absorbed |
| `README.md` | Parts II, VI, VIII, X, XV | absorbed |
| `harness-epoch-runtime-record-location.md` | Parts II, VII, VIII, XVI | absorbed |
| `harness-scan-watch-queue-disconnection.md` | Parts IX, X | absorbed |
| `harness-completion-review-acceptance-mechanism.md` | Part XII | absorbed |
| `harness-resume-mechanism-repair.md` | Part XIII | absorbed |
| `harness-provider-adapter-materialization.md` | Parts IV, VI | absorbed |
| `harness-public-shutdown-process-ownership.md` | Part XIV | absorbed |
| `fix_overview.md` | Parts VIII, X, XI | absorbed |
| `fixing_reccomendations.md` | Parts V, VI, VIII, XI | absorbed |
| `subagent_hooks.md` | Part VI.3 (proof carried forward) + Appendix A.1 | verbatim (in A.1) |
| `harness-detailed-architecture-review.md` | Appendix A.2 | verbatim |
| `harness-executor-stop-hook-manager-queue-coupling.md` | Appendix A.3 | verbatim |

**How to use this file:** to implement any part of the v2 product, read Parts I–XVII (the
canonical spec), consult Part XVI for the exact record on disk and Part XVII for the exact
command surface, and treat Appendix A as background only. Parts I–XVII are the single source
of truth; if anything in Appendix A appears to conflict with them, Parts I–XVII win.

*End of master specification.*
