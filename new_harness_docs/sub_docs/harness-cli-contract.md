# Harness public CLI contract (task 3)

The single place that specifies every public `operator_launch` command: its purpose,
inputs, success output, stable failure codes, the next action each outcome implies,
and its ownership boundary. This is the task-3 consolidation called for in
`harness_single.md`.

Grounded in the existing contracts (the per-command failure-code table in
`setup-details.md`, the command forms used across the docs, R1–R16, the operator-
responses section, and the record schemas in `harness-record-schemas.md`). Where a
detail was not fixed by those docs it is a default, marked **[default]**. Genuine
open choices are collected at the end under "Decisions returned for your call."

> Path notation uses forward slashes; the implementation uses the host's native
> separator. `<rt>` = the runtime root `<root-workspace>/.harness-runtime`.

## Conventions (apply to every command)

- **Invocation.** All commands are subcommands of the one launcher binary,
  `operator_launch …`. There is no other public entry point; ROOT never edits
  records by hand.
- **Exit + output. [default]** Success = process exit `0` with a short human status
  line on stdout (bootstrap's is the documented `status: prepared`); every command
  accepts `--json` to emit a machine-readable result object instead. Failure =
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

## Decisions returned for your call

Everything above is assembled and defaulted. Two genuine choices remain:

**A. Command grouping is inconsistent, and it's your call whether to unify.** Most
lane operations are subcommands of `lane` (`lane bootstrap`, `lane launch`,
`lane completion-review`, `lane force-stop`, `lane retire`), but two are top-level
hyphenated commands (`resume-lane`, `send-lane-notification`) — and the ROOT skills
are named to match (`resume-lane`, `send-lane-notification`). Options: (i) **keep as
is** — my recommendation, because these forms and skill names are embedded across
every doc, so unifying is pure churn for a cosmetic gain; or (ii) unify under `lane`
(`lane resume`, `lane send-notification`), which cascades to those two skill names
and ~40 references. I documented the current forms; say the word if you want (ii).

**B. Several commands' failure codes and the `health reconcile` form are defaults,
not doc-sourced.** The `setup-details` failure table covered setup, bootstrap,
launch, resume, manager-close, completion-review, and shutdown — I reused those
verbatim. For **manager acknowledge, send-lane-notification, lane force-stop, lane
retire, scan/watch, and health reconcile** I supplied failure-code sets and (for
health reconcile) the invocation form as **[default]** in the sensible house style.
They're reasonable and self-consistent; confirm them, or hand me specific names/forms
and I'll swap them in.
