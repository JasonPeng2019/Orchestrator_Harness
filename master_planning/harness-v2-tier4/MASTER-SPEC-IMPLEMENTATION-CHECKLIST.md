# Harness v2 master-spec implementation checklist

**Authority:** `new_harness_Docs/master_docs/harness-master-spec.md`, Parts I–XIX.
The master specification is authoritative; Appendix A is historical context only and
is deliberately excluded from this checklist. Part XIX.2 items are explicitly
optional and are likewise excluded from completion gating.

## How to use this checklist

- Mark an item complete only with implementation and proportionate automated or
  live evidence. Link the evidence in the implementation audit; a code reading alone
  is not proof for process, hook, lock, or provider behavior.
- Treat every `must`, ownership boundary, state transition, failure code, schema
  field, and explicitly forbidden alternate mechanism in the master specification as
  a completion requirement.
- Test managed and plain behavior separately wherever an item distinguishes them.
- Test each shipped provider (Codex, Claude Code, Qwen Code) where an item says
  provider-native, adapter, payload, hook, or launch binding.

## Current implementation audit notation

**Audited target:** `harness-single` commit `7d74fb64d5644d20f1d2697328fc2fb4929af09e`
on `working/firmware/v2-candidate`.

`[!]` marks an item that is **not complete** in this checkout. This includes
missing behavior, an implementation that violates part of the stated contract,
missing durable live evidence where the item requires it, and a master-spec
decision that remains unresolved. Unchanged `[ ]` rows were not found incomplete
by this audit; they are not an assertion that a future implementation audit may
not find a regression.

## A. Product boundary, actors, and global invariants (Parts I–III)

- [!] A1. The product is strictly a provider-agnostic orchestration harness; it does
  not perform hardware, device, firmware, MCP, environment, or campaign work.
- [!] A2. Runtime-mutated state exists only below the derived project-local
  `<root-workspace>/.harness-runtime/` tree, which is locally Git-excluded.
- [!] A3. Lane worktrees do not pollute ROOT's Git status or commits, and lane branches
  are never pushed by the harness.
- [ ] A4. ROOT remains the trusted decision-maker; the harness reports observed ground
  truth and never claims an unobserved ROOT action fixed a condition.
- [ ] A5. The short-lived launch routes own epoch/lane-record lifecycle only; they do
  not retain long-lived state or impersonate agents.
- [!] A6. Exactly one controller is live per running lane; it owns its provider,
  helpers, execution records, live leases, and cleanup proof.
- [ ] A7. Exactly one persistent monitor exists per runtime and it alone persists
  across lanes and epochs.
- [!] A8. A worker reads only its own managed inbox, writes only its worker-owned
  artifacts/outbox, never reads another lane's files, and never writes the manager queue.
- [!] A9. At most one epoch is active; parallelism is only among lanes within that epoch.
- [!] A10. Lane IDs are operator supplied and unique for the whole epoch, including
  retired lanes; generated IDs are opaque and never reused across epochs.
- [!] A11. Resume creates a fresh `run_id`, and all hooks/records reject or ignore
  stale-run artifacts.
- [ ] A12. Managed is the default profile; plain is an explicit, complete opt-out,
  not an error path or auto-accept path.
- [ ] A13. Records use SHA-256 content linkage for integrity only; no signing, PKI, or
  identity-proof claim is introduced.
- [!] A14. Every replaceable record uses a validated same-directory temporary sibling,
  short advisory process lock, and same-volume atomic rename.
- [!] A14a. Atomic-write recovery uses a unique temporary sibling, releases the lock in
  `finally`/process cleanup, has no durable `locked` field or ROOT lock-management path,
  and makes the next writer parse/health-check before continuing after a writer crash.
- [!] A14b. Failure-injection proof covers a writer crash before replacement: old/new
  complete-file visibility only, OS-lock release, rejected malformed residue, and a
  successful later writer without manual lock repair.
- [!] A15. Record locks follow one global order: runtime-state, manager-queue,
  lane-record, resource-lease, monitor-record.
- [!] A16. The three legitimate manager-queue writers use the same queue lock: monitor
  admission, ROOT state advancement, and PostToolUse delivery receipt only.
- [ ] A17. The controller and worker never write the manager queue; a delivery receipt
  never advances an event state.

## B. Filesystem layout, profiles, and materialization (Parts II–IV)

- [ ] B1. The shipped harness root has the documented config, resource manifest,
  README, adapters catalog, source super-cache, and implementation/launcher-binding tree.
- [ ] B2. Setup treats the harness root as read-only except custom-provider binding
  registration; shipped provider bindings are installed/checked, not rewritten.
- [ ] B3. Retired worktrees are never scanned, validated, or required by later setup,
  epoch, monitor, or lane activity; their removal is operator-permitted.
- [ ] B4. Setup installs all three ROOT payloads (`.codex`, `.claude`, `.qwen`) and
  creates only the profile-appropriate runtime directories and records.
- [ ] B5. Setup does not pre-create `CURRENT_EPOCH.json`, an epoch folder, or a lane
  worktree; epoch open/bootstrap creates them.
- [ ] B6. A managed worktree contains the documented controller artifacts, result,
  queue/outbox/helpers, hook binding/dispatcher/overlay receipt, selected provider
  payload, and exactly the two worker skills.
- [!] B7. A plain worktree has only the checkout, result, controller artifacts, and
  normal provider base content; it has no coordination queue, hooks, worker skills,
  worker outbox, or provider coordination payload.
- [!] B8. `lane.json`, completion review, and acceptance records live outside the
  worktree, so a worker cannot forge ROOT's review/acceptance decision.
- [ ] B9. The active super-cache is copied from shipped source into the runtime tree;
  its managed base, per-provider payloads, and optional custom area have the specified roles.
- [ ] B10. Only the selected provider payload is materialized into a managed lane;
  no lane receives all providers' worker payloads or skills.
- [!] B11. Bootstrap is one materialization action: common managed base + selected
  provider payload + generated lane-specific files/records.
- [ ] B12. Bootstrap creates the worker inbox/outbox, truthful-result template,
  worker prompt, invocation, and lane records fresh rather than copying stale state.
- [ ] B13. Each shipped adapter contains its ROOT payload, worker super-cache payload,
  `README`, shipped machinery guide, and `harness/launcher_binding.py`.
- [!] B14. Each launcher binding exports exactly `PROVIDER_ID`, `ADAPTER_VERSION`,
  `build_argv(...)`, and `parse_line(...)`; the controller verifies provider-ID match.
- [ ] B15. A custom stdio provider can be added with a file-only adapter without
  editing general harness code; no standalone public adapter install/check/bind command exists.
- [ ] B16. Every provider ROOT payload has the eight specified thin command-wrapper
  skills, and every managed worker payload has exactly `manager-notify` and
  `lane-assignment`.
- [ ] B17. Each ROOT skill directs use of its corresponding public command and does
  not implement polling, binding, hook configuration, or direct record mutation.
- [ ] B18. Watch skill instructions prevent concurrent/active-work watch use and
  require handling the returned actionable report before another wait.
- [ ] B19. Queue/review/resume/force-stop/shutdown skills prescribe only public routes,
  read-only queue inspection where appropriate, and no hand editing/broad process kill.
- [ ] B20. Worker skills require their helpers for escalation or assignment state and
  prohibit hand edits to either queue.
- [ ] B21. The watch skill says watch is a foreground, deliberately-idle operation;
  it is neither a background service nor a queue replacement and cannot be restarted
  before its actionable output is handled.
- [ ] B22. The acknowledge skill requires read-only fixed-queue inspection and one
  acknowledgement for each top-level event ROOT actually read—never a direct queue edit.
- [ ] B23. The close skill closes only an acknowledged ordinary event through the public
  route, never restarts a lane, and leaves completion-review event closure to that command.
- [ ] B24. The review skill handles stale source normally by resume, permits force
  acceptance only after current harmless-difference inspection, and gives the proper
  managed event/plain direct resume-required response after rejection.
- [ ] B25. Force-stop and shutdown skills preserve failure evidence, target only the
  documented scope, and never retry by broad process-name kill.
- [ ] B26. Worker escalation instructions require decision/action sought, relevant local
  evidence, and severity; a blocked assignment both records its required reason and escalates.

## C. Configuration and setup (Parts V–VI)

- [ ] C1. `harness-config.json` implements only required absolute `root_workspace`
  and optional `managed_coordination` (`enabled` default or `disabled`) under
  `harness-config/v1`.
- [ ] C2. The runtime root is always derived as `<root_workspace>/.harness-runtime`;
  no second runtime path, root provider/model, feature flag, profile override, or
  runtime CLI inference is accepted by later commands.
- [!] C3. Changing root workspace or managed/plain profile is rejected during an
  active epoch and requires shutdown before a new epoch.
- [ ] C4. `resource-manifest.json` is the sole ROOT-authored closed list of literal
  exclusive resource IDs, supports an empty list, and uses `resource-manifest/v1`.
- [!] C5. Setup atomically copies the active resource manifest; later bootstrap reads
  the active copy, and source-manifest changes are refused while an epoch/lease is live.
- [!] C6. Setup is idempotent, starts no lane/provider, accepts only `--overwrite`,
  and reports only planned overwrite targets.
- [ ] C7. Setup validates the absolute root workspace, derives the runtime path,
  rejects a symbolic-link root, and permits a nested runtime root as documented.
- [ ] C8. Setup validates configuration and source manifest before mutation and creates
  only required runtime parents, including manager only in managed mode.
- [ ] C9. Setup creates/reopens `RUNTIME_STATE.json` as `OPEN`; managed creates a
  validated idle manager queue and plain creates neither queue nor active wrapper.
- [ ] C10. Setup stages, byte-verifies, and atomically installs missing shipped cache
  material, including all shipped adapter payloads.
- [ ] C11. Setup validates and preserves an already-valid cache without silently
  overwriting approved custom content.
- [ ] C12. Setup creates the empty lease directory and atomically installs the active
  manifest; conflicting manifest change refuses while epoch/lease state is live.
- [ ] C13. Setup installs all ROOT payloads plus provider catalog/bindings; normal
  collisions reject without partial copy, while `--overwrite` is narrow and reported.
- [ ] C14. Setup starts exactly one monitor under the monitor-record lock; a live
  identity returns informational `SETUP_MONITOR_ALREADY_RUNNING` without double start.
- [ ] C15. A stale/absent monitor identity is safely replaced; a live identity is
  matched by PID plus creation time.
- [!] C16. Before managed use, each provider passes a disposable, host-only, headless
  proof: configuration discovery, all ten skills, real PostToolUse, Stop rejection for
  unresolved work and invalid/missing result, binding on new/resumed launch, durable
  `DELIVERED` receipt, and collision rollback.
- [!] C17. Hook proof uses a fresh ignored runtime, fresh Git lane, and real registered
  manager queue; it does not require hardware, firmware, or MCP services.
- [ ] C18. Setup never migrates candidate-era queues, bindings, coordinators, or live
  state; v2 starts fresh and old runtime folders remain archival only.
- [ ] C19. Fresh run records, IDs, process identities, queues, bindings, controller
  records, and provider session IDs are generated for the current run, not templated.
- [ ] C20. Product inputs and executable bindings remain in the harness root rather
  than being copied as runtime state.

## D. Epoch and lane lifecycle (Parts VII–VIII)

- [ ] D1. There is no public epoch open/retire/edit command; the launcher exclusively
  opens, reuses, and closes epoch records.
- [!] D2. An epoch opens only if no epoch is active; the launcher publishes a generic
  current marker before first lane preparation and uses fresh IDs/ownership each time.
- [ ] D3. A managed epoch atomically stages a fresh manager queue and fresh `queue_id`;
  a plain epoch creates no manager queue.
- [!] D4. Epoch closure requires no active lanes and no unresolved manager event,
  except through shutdown/reconfiguration; late old-lane operations fail `EPOCH_RETIRED`.
- [!] D5. Epoch-breaking facts are exactly root workspace, profile, resource manifest,
  manager queue schema/ID, and runtime-record schema version.
- [ ] D6. Adding/retiring lanes, task content, ROOT identity, and lane provider/model
  choices do not break an active epoch.
- [ ] D7. `CURRENT_EPOCH.json` and `epoch-state.json` carry only their specified
  generic/config/lifecycle identity—not ROOT provider/session, binding, or queue path.
- [!] D8. Bootstrap validates lane ID, provider/model, active manifest resources,
  paths, and launch settings before creating a worktree.
- [ ] D9. Bootstrap uses a new Git branch/worktree at the controlled runtime location,
  creates `.agent-workspace`, applies the overlay/receipt, and updates controlled records/index.
- [!] D10. Managed bootstrap installs selected payload, hooks, worker skills, inbox,
  and outbox; plain bootstrap omits coordination material.
- [ ] D11. Bootstrap writes worker prompt, truthful-result template, invocation, and
  controller artifact paths; it returns `prepared` without provider start, lease,
  hardware action, or task execution.
- [ ] D12. Launch consumes, rather than rewrites, a valid invocation; the controller,
  not ROOT or the command, starts the provider and owns leases.
- [!] D13. Contended launch atomically obtains all resources or none, starts nothing,
  and returns `LAUNCH_LEASE_BUSY` synchronously.
- [ ] D14. The controller captures transcript/stderr/last message, writes status and
  append-only audit records, validates result, and records only its own worktree facts.
- [ ] D15. The controller records `review_pending` only for valid terminal result and
  `result_invalid` for missing/malformed/wrong-task/contradictory result.
- [ ] D16. Controller cleanup proof precedes normal release of leases, and valid ROOT
  acceptance is copied into controller status to prevent a later resume.
- [!] D17. Lane lifecycle supports exactly prepared → running → review_pending/result_invalid
  → accepted → retired, plus blocked and abandoned, with the specified owners.
- [!] D18. Resolve and record the authoritative resume-state rule before implementation
  sign-off: Part XIII.2 says resume sets `RESUMING`, but the Part XVI `lane.json` enum
  excludes it and says resume sets `running`. Decide whether `RESUMING` is persisted,
  transient/non-recorded, or added to the enum; then align schema/transitions, CLI success
  result, monitor behavior, recovery, and tests to that single decision.

## E. Monitor and status truth (Part IX)

- [ ] E1. One monitor reads current epoch, epoch state, and active-lane index; it has
  no lane-dependent queue-path/provider binding discovery or per-lane restart requirement.
- [ ] E2. Each monitor pass inspects registered lanes only; it does not discover lanes
  by arbitrary filesystem scan.
- [ ] E3. The monitor takes controller-recorded `review_pending`/`result_invalid`
  directly and derives controller exit, provider exited/no result, transcript contradiction,
  cleanup-unproven, and orphaned-lease statuses from authoritative facts.
- [ ] E4. Resource contention never becomes a monitor status; it remains synchronous
  `LAUNCH_LEASE_BUSY` at launch.
- [!] E5. On each status change the monitor emits exactly one managed event or leaves
  status for plain watch, using `last_reported_actionable_status` under lane lock for dedup.
- [ ] E6. Status mapping is exact: review pending → completion review required; result
  invalid → lane result invalid; remaining statuses → lane status changed with
  `actionable_status`; resume-required remains a separate signal.
- [!] E7. The monitor consumes each worker-outbox escalation once into processed
  notifications; it never drains or uses controller event logs as manager input.
- [!] E8. Every pass updates `MONITOR.json` heartbeat timestamp and watched-lane count;
  it never creates heartbeat events in the manager queue.
- [ ] E9. Managed ROOT PostToolUse checks monitor PID+creation liveness and heartbeat
  freshness from only `MONITOR.json`, then directs ROOT through the locked monitor-start path.
- [ ] E10. Liveness recovery restarts dead/absent or hung monitor safely, stops an
  exact hung process first, and never starts a second monitor after a marked-stop-but-live case.
- [ ] E11. A stopped-and-dead monitor is recognized as deliberate and never resurrected;
  plain mode has manual scan/watch recovery because it has no ROOT hook.
- [!] E12. The staleness threshold is materially larger than the monitor pass interval
  and is made a verified/schema decision rather than a magic runtime guess.
- [ ] E13. Health reconciliation runs at monitor startup and every pass, rebuilds the
  index from controlled lane records, treats `lane.json` as authoritative, and is exposed
  through the public health command.
- [ ] E14. Monitor restart/replacement and monitor field updates share one lock;
  recovery is minimal health scan, not replay/supervisor service.

## F. Managed coordination and native hooks (Part X)

- [ ] F1. The manager queue is the only authoritative managed ROOT inbox at its fixed
  path, has fresh per-epoch `queue_id`, and is absent/unread in plain mode.
- [!] F2. Every manager queue mutation validates header and current-epoch ID pair,
  locks, reads whole file, changes authorized fields, and atomically replaces it.
- [!] F3. Manager event fields, types, histories, and state transitions match the
  master schema exactly; `BLOCKED` close has a reason.
- [ ] F4. The monitor alone creates events; ROOT alone advances their state; the hook
  records `DELIVERED` history only and never acknowledges/completes an event.
- [ ] F5. The design contains no `STATE.json`, `QUEUE.jsonl`, coordinator,
  `REGISTRATION.json`, second queue authority, or compaction subsystem.
- [!] F6. Queue health recovery creates an empty fresh-ID queue, atomically updates
  current epoch, returns `QUEUE_REPLACED` to stale writers, and never treats lost pending
  events as handled.
- [ ] F7. Managed ROOT receives content-free delivery notice, then reads queue read-only,
  acknowledges every event actually read, handles it, and closes ordinary events; completion
  review closes its own event.
- [ ] F8. Closing an event never changes underlying lane truth.
- [ ] F9. Each running managed lane has its own distinct inbox; it is never another
  lane's queue or the manager queue, and plain lanes have none.
- [ ] F10. Only `send-lane-notification` appends PENDING assignments; only the worker
  helper advances assignment state; monitor does not read worker inboxes.
- [ ] F11. Inbox hooks filter current run and resume replaces it with a fresh empty
  current-run queue.
- [!] F12. Worker escalation is a one-way file outbox; only monitor consumes it once
  and turns it into a ROOT event.
- [ ] F13. Controller-generated managed prompts always append the exact escalation
  instruction and helper path; task cards and skills cannot omit or replace it.
- [ ] F14. A blocking escalation tells the worker to stop safely and await ROOT rather
  than inventing a decision; plain lanes receive no escalation feature.
- [!] F14a. The controller appends the generated escalation block after every managed
  worker task prompt, not merely the initial prompt; neither task cards nor `AGENTS.md`
  can replace or suppress it.
- [!] F14b. The generated managed ROOT initial prompt contains the matching ROOT-handling
  block, so worker escalation yields a ROOT manager event that ROOT must inspect and
  acknowledge only by its top-level event ID.
- [ ] F15. Every managed provider has real native declarations for ROOT PostToolUse,
  ROOT Stop, worker PostToolUse, and worker Stop; a copied but unbound hook fails loudly.
- [ ] F16. ROOT hooks provide delivery notice/monitor liveness and block unresolved
  ROOT obligations; worker hooks notify only local assignments and reject stop for
  unresolved local work or missing/invalid result.
- [ ] F17. Worker Stop permits valid PASS, FAIL, or BLOCKED result and never treats a
  successful process exit alone as valid completion.
- [ ] F18. Hook dispatcher/binding files, boundary selection, names, and provider-specific
  Qwen notification route are installed at the specified ownership boundaries.

## G. Resources, review, resume, and ending lanes (Parts XI–XV)

- [ ] G1. Bootstrap merely declares resources from the active manifest; launch creates
  deterministic per-resource leases only while the controller is live.
- [ ] G2. Controller-owned leases contain resource/lane/run and exact holder identity,
  are released after cleanup proof, and become immediately reusable in series.
- [ ] G3. Multi-resource acquisition is all-or-nothing, fail-fast, has no busy retry,
  no waiter, no partial hold, and needs no global acquisition order.
- [ ] G4. A stale lease is never auto-reclaimed; monitor surfaces it and ROOT may make
  the explicit force-release/risk decision before reuse.
- [!] G4a. Resolve the missing public orphaned-lease force-release contract before
  sign-off. The master requires explicit ROOT force release but provides no public command,
  while prohibiting hand-edited records. Specify the sole route, caller/record ownership,
  exact PID+creation and lease validation, lock/atomic behavior, stable success/failure
  contract, recovery semantics, and proof before implementing it.
- [ ] G5. Completion chain is task card → worker RESULT → outside-worktree factual
  review → outside-worktree ROOT acceptance, with complete hash/ID/commit linkage.
- [ ] G6. Worker result cannot self-accept; a missing pair is acceptance pending and
  a one-file review/acceptance pair is an error.
- [ ] G7. Completion review uses exactly one selector (`--event-id` managed or
  `--lane-id` plain), both factual `review_outcome` and separate `approval`, and
  never conflates review outcome with manager close outcome.
- [ ] G8. ACCEPTED requires PASS unless force accept has a non-empty reason and a
  structurally valid current chain; review performs final card/result/run currency check.
- [ ] G9. Completion-review is sole writer of both decision files, writes them as a
  pair, closes managed review event itself, advances accepted lane, and leaves rejected work resumable.
- [!] G10. Managed reconciliation replaces a lost review event only when the same current
  valid result has no pair/open matching event; evidence records it as a new request.
- [!] G11. Health recovery removes broken/incomplete review pair without inferring
  acceptance; plain restores direct review-pending without creating queue state.
- [!] G12. Resume applies only to stopped unaccepted lane and its same worktree/native
  session; it creates fresh run ID, task/instructions/rationale/invocation and never
  reconstructs missing process/session/worktree state.
- [!] G12a. Resume first records `RESUMING` and replaces the task, rationale, and
  instructions before it clears obsolete current-run artifacts and writes the fresh invocation.
- [ ] G13. Resume clears result, both review records, and managed inbox for fresh run;
  it refuses accepted/running/missing-worktree/no-session cases with documented paths.
- [ ] G14. Stale results never reach review; valid fresh terminal result re-enters
  managed event or plain direct review, and rejected work may resume repeatedly without
  an archive/new worktree/generation folder.
- [!] G14a. Once the resume-signal source rule is resolved, managed handling emits the
  exact permitted `LANE_RESUME_REQUIRED` event(s) and plain handling emits equivalent
  direct resume-required output while never creating a manager event.
- [!] G14b. Resolve the `LANE_RESUME_REQUIRED` production conflict before sign-off:
  Part IV.5 assigns it to rejected review, while Part XIII assigns it to managed resume.
  Define whether one or both transitions produce it, dedup/event lifecycle, when plain
  direct output occurs, and then align the review skill, review command, resume route,
  monitor/profile behavior, and real-provider proof to that single rule.
- [ ] G15. Force-stop targets only exact recorded PID+creation identities for one lane,
  force-releases its leases, retires it, and escalates an unkillable process to host/operator.
- [!] G16. Graceful retire requires an existing valid accepted chain, proves cleanup
  before lease release, retains branch/record, and force-stop is its narrow recovery path.
- [ ] G17. Retirement of final lane closes the epoch; it never builds archive/history/
  overlay-restore machinery, and an overlay receipt supports only narrow restoration.
- [ ] G18. Shutdown transitions OPEN → SHUTTING_DOWN → CLOSED, blocks new launches,
  lets each controller clean only its own exact processes, and never uses global process lists/broad kills.
- [ ] G19. Shutdown keeps monitor alive through lane cleanup, sets its exact
  `stop_requested` under lock, proves monitor exit, clears current epoch first, and leaves
  evidence intact on failure without broad-kill retry.
- [ ] G20. The only exceptional monitor-stop paths target exact PID+creation identities
  and honor stop request; no separate shutdown/evidence marker files exist.
- [!] G21. Runtime/lane worktrees are Git-excluded; retirement/shutdown runs Git worktree
  prune for each source repository and retains local lane branches.
- [!] G22. Operator remediation is implemented/documented for every actionable status,
  including the critical distinction that notification closure does not resolve truth and
  resume redoes work rather than cleanup.

## H. Record schema ledger (Part XVI)

- [!] H1. Every persistent JSON record has the exact lower-kebab filename-derived
  `/v1` schema, required typing/context checks, ISO-8601 UTC timestamps, and schema-major
  mismatch refusal rather than silent migration.
- [ ] H2. Canonical sorted-key UTF-8 JSON SHA-256 content hashes and linked ID+hash
  fields are implemented wherever the schema requires them.
- [ ] H3. `RUNTIME_STATE.json` has only allowed states/transitions, correct writers,
  idempotent recovery, and launch refusal unless OPEN.
- [!] H4. `CURRENT_EPOCH.json` is a small generic marker with correct managed/plain
  fields, fresh queue cross-check, runtime-state lock ownership, and stale-pair no-op recovery.
- [!] H5. `epoch-state.json` stores exact config identity/lifecycle/ownership data,
  validates current config, and supports opening-crash replacement.
- [ ] H6. `active-lanes.json` is a rebuildable index of lane records/runs, never a
  competing authority, and is regenerated from controlled lanes on disagreement.
- [!] H7. `lane.json` is authoritative, includes exact current run/artifact/provider/
  session/process/lifecycle/acceptance/dedup fields, constrains managed-only inbox fields,
  and is never silently regenerated when malformed.
- [!] H8. Manager queue header/events/transitions/writers/recovery exactly match §6,
  including delivery history separation and no compaction system.
- [!] H9. Worker inbox header/assignment fields/transitions/writers/current-run checks
  and resume reset exactly match §7.
- [ ] H10. `MONITOR.json` identity, health/heartbeat, stop lifecycle, single-lock writes,
  PID+creation checks, and dead/hung/deliberate-stop recovery exactly match §8.
- [ ] H11. `controller.status.json` has correct controller/provider/result/cleanup/
  recorded-status/acceptance fields; controller writes it and monitor derives—not copies—
  the additional actionable statuses.
- [ ] H12. `controller.events.jsonl` has first-line schema header, append-only single
  controller writer, advisory malformed/truncated-line tolerance, and is not monitor input.
- [!] H13. `RESULT.json` implements exact result fields/enums/hash/current-run validation,
  atomic worker write, no honored self-acceptance, and invalid/missing recovery.
- [!] H14. Completion review schema has factual fields, task/result/commit linkage,
  sole command writer, outside-worktree placement, paired health/recovery rules.
- [!] H15. Acceptance schema has independent approval, non-empty ROOT identity, review
  reference, conditional force reason, paired write/health/recovery rules.
- [ ] H16. Lease schema, deterministic filename, writer/reader/recovery boundaries, and
  persistent-file behavior exactly match §14.
- [ ] H17. Overlay receipt and invocation schemas have correct profile/provider/run
  fields, writers, atomic lifecycle, advisory/integrity handling, and resume refresh behavior.
- [!] H18. Worker prompt and truthful-result template follow the invocation's per-lane
  atomic write and resume-refresh lifecycle even though they are not separately schema'd.

### H.1 Schema field-and-contract audit detail

- [!] H19. Runtime state has only `schema`, `state`, and `updated_at`; its two writers,
  runtime-state lock, reader set, absent-state setup recovery, and all three allowed
  transitions are individually covered.
- [!] H20. Current epoch has only schema/epoch/lane mode/open time plus managed queue ID;
  it is written after staging queue/epoch record, cleared before closure, and verifies
  queue identity with dispatcher no-op on stale mismatch.
- [!] H21. Epoch state records config identity, lifecycle, lane directory, ownership, and
  opening/closing timestamps; launcher is its only writer and opening crash has retire/replace recovery.
- [ ] H22. Active-lane index has `{lane_id,lane_record_path,run_id}` entries; launch,
  resume, and retire update it; monitor rebuild verifies path/run against authoritative lane record.
- [!] H23. Lane record contains exact artifact paths, provider ID/model, session and
  PID/creation identity, lifecycle, acceptance advancement, and sole monitor dedup field;
  malformed lanes surface actionable error rather than regeneration.
- [!] H24. Manager events include IDs/type/lane/run/actionable status/summary/state/history/
  delivery history; every event links a live lane/run, state history is append-only, and
  hook mutation is restricted to delivery history.
- [!] H25. Worker inbox records schema/lane/run/assignments and each assignment's ID,
  prompt, creation time, state/history; correct writer split, current-run health, and
  reset-on-resume behavior are independently tested.
- [ ] H26. Monitor record contains config identity, PID/creation/start, health,
  heartbeat, and stop request/derived stopped state; each setup/monitor/hook/shutdown
  writer is lock-coordinated and recovery discriminates crash, hang, and intentional stop.
- [ ] H27. Controller status contains exact controller/provider/result state, raw cleanup
  proof, limited recorded statuses, acceptance advancement, and update time; only controller
  writes it and transcript/liveness/lease-derived statuses remain monitor responsibility.
- [ ] H28. Controller JSONL starts with exactly its schema header and subsequent
  timestamp/run/event/detail entries; append-only partial-line tolerance cannot influence
  monitor decisions or block progress.
- [!] H29. Result has schema/lane/run/outcome/summary/evidence/content hash/completion time;
  controller validates all structural properties and the only worker write is per-run atomic.
- [!] H30. Review has all factual outcome/summary/evidence/card/result/commit/time/hash
  fields; acceptance has all decision/ROOT/review reference/card/result/commit/conditional
  force reason/time/hash fields; both are atomically paired and cross-linked.
- [ ] H31. Lease has schema/resource/lane/run/holder PID+creation/acquisition fields,
  deterministic filename, controller normal release, and explicit force-only stale clearing.
- [!] H32. Overlay receipt includes schema/lane/run/profile/base reference/managed payload/
  application time and remains advisory; invocation includes provider, resolved launch argv,
  child environment, CWD, paths, hash/time and fails launch when invalid.

## I. Public CLI, portability, and required proof (Parts XVII–XIX)

- [ ] I1. `operator_launch` is the only public entry point; no supported workflow
  requires ROOT to edit records manually or use a second provider-binding command.
- [ ] I2. Every public command supports `--json` as the machine-readable alternative;
  normal success exits 0 with a short human stdout status and every result contains
  `{ ok, code, summary, evidence_paths, next_action }`.
- [!] I2a. Every failure exits nonzero, emits exactly one stable contract code plus a
  human stderr message naming the applicable offending path/ID, never returns only a
  generic exception, and leaves prior state intact.
- [!] I3. Setup, shutdown, bootstrap, launch, review, resume, force-stop, retire,
  manager acknowledge/close, send notification, scan, watch, and health reconcile have
  exactly the documented arguments, outputs, ownership, selectors, failure codes, and next actions.
- [ ] I4. Bootstrap failure set includes invalid request/ID reuse/worktree/cache collision/
  missing adapter/undeclared resource; launch failure set includes invalid invocation,
  binding, lease busy, controller start, and provider start.
- [!] I5. Completion review rejects invalid/unacknowledged/stale/force-invalid/conflicting/
  failed-write cases; resume, force-stop, retire, manager, send, scan/watch, health,
  setup, and shutdown return their specified stable codes.
- [!] I6. `scan --no-write` is truly read-only; watch is blocking/return-on-actionable
  with documented timeout behavior and is the normal plain-mode polling mechanism.
- [ ] I7. Paths use host-native joining/storage; no drive letter, absolute platform form,
  shell extension, OS-specific API, hostname, port, credential, or platform vocabulary is normative.
- [ ] I8. Process liveness always uses cross-platform PID plus creation-time identity;
  file semantics rely only on same-volume atomic replace and advisory process locks.
- [!] I8a. Run a Windows/macOS/Linux portability matrix proving native path joining and
  storage, platform-native launcher/helper entry points, PID-plus-creation liveness,
  advisory locks, and same-volume atomic replacement on every supported target.
- [!] I9. For Codex, Claude Code, and Qwen Code, prove real native hook discovery and
  durable delivery receipt, ROOT/worker queue isolation, and binding on both new and
  resumed lane launches.
- [!] I9a. For each shipped provider, separately prove ROOT Stop rejects unresolved
  manager obligations and worker Stop rejects unresolved assignments in that worker's
  local inbox while the other role's queue cannot block it.
- [!] I9b. For each shipped provider, separately prove worker Stop rejects both missing
  and malformed `RESULT.json`, then permits each structurally valid PASS, FAIL, and BLOCKED result.
- [!] I10. Prove monitor liveness hook restarts a dead/hung monitor but never a
  deliberately stopped one, in a real provider environment.
- [!] I11. Prove an exclusive lease is cleanup-proven, freed, and reused serially by a
  later lane, including contention/all-or-nothing behavior.
- [!] I12. Confirm all design-completion claims exclude only Part XIX.2's explicitly
  optional force-stopped lifecycle distinction, Appendix-A labeling caveat, and rejected
  escalation timer—not any Part I–XVIII requirement.
- [!] I13. Resolve the master-spec inconsistency before declaring CLI completeness:
  Part IV.5 directs `manager close ... --summary`, while Part XVII omits that argument.
  Record the authoritative interpretation and verify the public signature, event reason,
  help text, JSON result, and skills against that resolution.
- [!] I14. After resolving orphaned-lease force release, add its public launcher command
  (or formally selected existing route) to the one-command CLI contract with exact arguments,
  selectors, JSON/human output, stable failures, next action, and no-record-hand-edit guarantee.

## Current implementation audit evidence

The `[!]` marks above were assessed against commit `7d74fb6`. These are the
principal evidence groups; the relevant checklist IDs are listed explicitly so a
repair can be scoped without reinterpreting the audit.

- **Boundary, record safety, and setup:** `A1-A3`, `A6`, `A8-A11`, `A14-A16`,
  `B7-B8`, `B11`, `B14`, `C3`, `C5-C6`, `C16-C17`, `D2`, `D4-D5`, `D8`,
  `D10`, `D13`, `D17-D18`. Source: MCP handling remains in
  `orchestrator_harness/events.py`; runtime exclusion is absent from `.gitignore`;
  epoch open and lane-ID checks are not a single protected transaction in
  `epochs.py`/`bootstrap.py`; record and queue writes frequently read before acquiring
  their mutation lock; setup re-reads the source manifest and is not idempotent without
  overwrite; native proof documents are assertions/instructions, not retained proof packets.

- **Monitor and coordination:** `E5`, `E7-E8`, `E12`, `F2-F3`, `F6`, `F12`,
  `F14a-F14b`. Source: `monitor.py` performs dedup/promotion/update as separate
  operations, moves outbox files even after failed promotion, and records no watched-lane
  heartbeat count; its 30/180 second values are hard-coded. `manager_queue.py` locks
  final write rather than read-modify-write, permits blocked closure without a reason,
  has no queue-health replacement, and sends follow-up prompts without the mandatory
  generated escalation block. No generated matching ROOT prompt exists.

- **Review, resume, retirement, and hygiene:** `G4a`, `G10-G12a`, `G14a-G14b`,
  `G16`, `G21-G22`. Source: `leases.py` exposes an internal lane-wide force release
  but `operator_launch.py` exposes no orphan-lease-only public route; reconciliation
  does not repair lost review events or broken pairs; `resume.py` ignores `rationale`,
  has no persisted `RESUMING` step, and emits no resume signal; `launch.py` retirement
  checks only acceptance schema/approval rather than a full linked chain. The runtime
  root is not Git-excluded and operator remediation remains undocumented.

- **Schema, CLI, and proof gates:** `H1`, `H4-H5`, `H7-H9`, `H13-H15`, `H18-H21`,
  `H23-H25`, `H29-H30`, `H32`, `I2a`, `I3`, `I5-I6`, `I8a-I14`. Source:
  `records.py`, `epochs.py`, `lanes.py`, `manager_queue.py`, `review.py`, and
  `launch.py` do not provide the complete schema health/lock/pair-atomicity contracts.
  The public parser also exposes non-spec `health monitor-recover`; several error paths
  collapse to generic codes; watch/scan flags are not fully enforced. Checked-in proof
  documents cover narrow Windows PostToolUse claims only, while the required all-provider
  Stop/new-resume/queue-isolation proof and Windows/macOS/Linux matrix are absent.

- **Checks run during this audit:**
  `python -m unittest discover -s orchestrator_harness/tests -v` passed (192 tests,
  2 skipped). The full repository discovery run did not pass: 291 passed, 2 skipped,
  and `harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.
  test_diagnostic_only_start_serve_never_runs_evaluator` failed because the watcher did
  not publish its exact startup identity. The focused harness result does not substitute
  for the live-provider or multi-platform evidence required by the marked items.

## Independent completeness review log

Three independent read-only passes were completed while constructing this checklist:
an end-to-end negative-space pass, a schema/CLI pass, and a final traceability pass.
Their material findings were incorporated; the final traceability verdict was `SHIP`.
The four source-contract ambiguities remain intentionally unchecked above (`D18`, `G4a`,
`G14b`, `I13`) because they require an authoritative specification decision before an
implementation can be signed off.

- [x] R1. Traceability review: every normative Part I–XIX clause and every v2-required
  validation proof maps to one or more checklist items.
- [x] R2. Negative-space review: every explicit prohibition/no-go in the master spec is
  represented (no historical candidate mechanisms accidentally promoted to v2).
- [x] R3. Lifecycle review: setup → epoch → bootstrap → launch → monitor/coordination →
  review/resume → retire/shutdown transitions, crashes, and recovery all have coverage.
- [x] R4. Provider/profile review: managed/plain differences and each shipped provider's
  native adapter/hook obligations have coverage.
- [x] R5. Schema/CLI review: all records, state transitions, writers/readers, lock/recovery
  rules, public commands, and stable failure contracts have coverage.
