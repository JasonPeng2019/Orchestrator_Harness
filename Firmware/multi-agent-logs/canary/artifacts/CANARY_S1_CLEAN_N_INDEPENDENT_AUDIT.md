# Clean-N independent audit

**Epoch:** `20260731-s1-clean-n`  
**Verdict:** **NONCOUNTING — counter remains `0/3`.**

No live endpoint, hardware, provider/MCP public operation, request/relay, flash, RF, or server
repair was run during this audit.

## Validated primary-harness defects

### 1. Startup temporal-coherence false `STALE_STATUS` — validated

Event `a41cde939e256d4d95050cf42faaad28a372ce5b6fee3b889999a76bf85b1305` was emitted at
`22:44:08.551455Z` for Boreal as a `STALE_STATUS`, yet the same event data records controller
creation at `22:44:15.248843Z` and Codex creation at `22:44:16.843055Z`. The independently
captured review scan then proves all four controllers/Codex identities live and exact, with no
conflict or observation error. This is a false alarm, not a real stale process declaration.

The current managed-watch sequence makes the cause credible and reproducible from source:
`watch_managed()` captures `observed = clock()` before calling the potentially slow Windows
`process_provider()`, then reconciles the later sample with that earlier `observed_at`.
`observe()` has the same pre-sample ordering. A process/status produced during sampling can
therefore appear to have a creation time in the future relative to the observation used for
lifecycle comparison.

**Narrow repair scope:** establish the observation timestamp at the end of the relevant process /
status sample (or carry an explicit sample interval and avoid classifying an identity as stale
solely because it began within that interval). Add a deterministic slow-provider/status-start
regression that proves no false `STALE_STATUS`, while retaining genuine stale-status detection.

### 2. Same-identity deferred checkpoint versions do not coalesce — validated

For identity `lane:20260731-s1-clean-n:Boreal:D31:checkpoint`, events record successive content
hashes `862bbc…` (`22:50:09Z`), `57382a…` (`22:51:10Z`), and `6594bf…` (`22:51:30Z`). Final
notification state has the obsolete first version pending and the two later versions deferred.
This is direct evidence of redundant/obsolete manager wakeups.

The cause is also visible in the accepted Clean-M backlog code: admission deduplicates only by
event ID; `_prune_deferred()` removes only acknowledgements and answered correlated
`MANAGER_SIGNAL`s. Neither coalesces newer `CHECKPOINT_UPDATED`/`RESULT_AVAILABLE` versions of
the same identity. This is a functional orchestration defect, not a manager acknowledgement
error.

**Narrow repair scope:** coalesce unacknowledged deferred versions of the same identity for
`CHECKPOINT_UPDATED` and `RESULT_AVAILABLE` to the newest content/version. Define explicitly how
an already pending older version is superseded so that acknowledgement remains exact and the
manager is not woken for stale content. Do **not** coalesce distinct `MANAGER_SIGNAL`s: their
immutable handoffs remain separately reviewable. Add tests for deferred-only and pending-plus-
deferred replacement, ordering, exact acknowledgement, restart persistence, fresh-output
suppression, and non-coalescing manager signals.

Either validated defect is enough to disqualify the sprint; both require a narrow primary-harness
repair before another counting sprint.

## Progress and procedure

- All four host-only Luna lanes exited code 0 and left new `CLEAN_N_PREPARED.md` checkpoints:
  Atlas classified malformed populated setup responses; Boreal added bounded exact
  launcher/uv/provider ancestry polling; Cygnus replaced the short-lived paired launcher with
  durable per-board stdio relays; Delta ignores malformed CIM rows while retaining an exact valid
  ancestry requirement. These are useful catalog preparations, **not** live endpoint completions.
- The target's no-repeat boundaries held: no `RESULT.json`, board/probe/serial/provider public
  operation, request/relay, flash, RF, or same-epoch live retry is evidenced.
- Manager procedure was otherwise sound. The formal review record precedes its exact ack; durable
  history shows `review_baseline_utc` advanced from `22:44:39.179210Z` to
  `22:49:33.359272Z`. The manager correctly stopped live escalation after the harness findings.
- Launcher durability is supported: the successor launcher gate passed with empty residue, and
  receipts for primary owner, optional owner, and all four controllers record Windows breakaway /
  no-window flags and exact PID+creation identities. This is a manager-launch success, not a
  launcher defect.

## Watcher and subagent classifications

- **Optional watcher: no defect.** It ran three evaluated polls at `22:45`, `22:48`, and `22:51`;
  each recorded `defect=false`, then it recorded `STOP_REQUESTED` and `SERVICE_STOPPED`.
  `service.json` confirms cooperative `stop-requested` exit.
- **Lane/subagent behavior: no defect established.** Four isolated host-preparation controllers
  have exact exit-zero statuses and their checkpoints match the stated bounded scope. The startup
  alert is a primary timestamp defect, not a Boreal/subagent failure.
- **Manager: no additional procedural defect established.** It acknowledged the false error and
  formal review through the canonical path, verified the baseline, and did not start live work.

## Cleanup

`CANARY_S1N_FINAL_PROCESS_INVENTORY.json` is `[]`. The primary runtime records cooperative
`stop-requested` exit for owner `10248` / watcher `179232`; optional runtime records the same for
owner `186104` / watcher `86984`. A current exact-PID query found no live owner, watcher,
controller, or Codex child from the receipts/statuses. No cleanup residue was found.

## Required next step

Plan and adversarially review one narrow primary-harness repair covering temporal-coherent
observation timestamps and checkpoint/result version coalescing. Preserve the Clean-M durable
manager-signal contract and the operator-side, read-only watcher boundary. Clean-N remains
noncounting at `0/3`.
