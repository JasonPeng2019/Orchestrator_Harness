# Harness record schemas (task 2)

This is the versioned-record schema ledger called for by task 2 in
`harness_single.md`. It defines, for every persistent record, its schema/version,
required fields, state transitions, writer, reader, lock/atomic-write rule, health
check, and recovery behavior.

Everything here is grounded in the existing contracts (`harness_single.md`,
`harness-epoch-runtime-record-location.md`, `harness-completion-review-acceptance-mechanism.md`,
`harness-scan-watch-queue-disconnection.md`, `harness-public-shutdown-process-ownership.md`,
`setup-details.md`). Where a detail was not fixed by those docs I have filled it
with a default and marked it **[default]**. Two points that were genuine design
decisions rather than fill-in are recorded, now resolved, at the end under
"Decisions (both resolved)" — everything else is settled inline.

> Paths use forward slashes for readability; the implementation uses the host's
> native separator. `<rt>` abbreviates the runtime root `<root-workspace>/.harness-runtime`.

## Conventions that apply to every record

- **Version string.** Every JSON record carries a top-level `schema` field of the
  form `<record-name>/v1` (matching the existing `manager-queue/v1`,
  `current-epoch/v1`, `harness-resource-manifest/v1`, `harness-config/v1`). The
  `harness-` prefix used by two of the existing strings is dropped for uniformity;
  the canonical names are those in each section below. **[default]**
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
