# Clean-N primary-harness repair plan

Plan/spec/scope owner: current main orchestrator  
Implementation agent after independent plan acceptance: persistent
`/root/canary_harness_coder` (gpt-5.6-terra, high reasoning)  
Independent plan/result auditor: persistent `/root/canary_sprint_auditor`
(gpt-5.6-terra, medium reasoning)

## Slice 1 — focused red regressions

1. Add deterministic observation tests with an injected discovery/process/clock trace. Make a
   declared controller appear after discovery begins but before the process provider returns; prove
   current code uses a pre-sample time and falsely emits `STALE_STATUS` in both ordinary observe
   and managed watch. Retain a control for an actually absent or reused identity.
2. Add notification tests for three successive same-identity `CHECKPOINT_UPDATED` versions behind
   a higher-priority pending event. Assert current code retains all versions and later selects the
   oldest.
3. Add pending-plus-deferred tests for both `CHECKPOINT_UPDATED` and `RESULT_AVAILABLE`, exact ack
   of old versus replacement IDs, deterministic ordering, same-output restart persistence,
   fresh-output suppression, separate identities, and non-coalesced `MANAGER_SIGNAL`s.
4. Run only these tests and record the expected red baseline before production edits.

## Slice 2 — coherent observation boundary

1. Refactor the narrow observation path so a sample consists of `discover_suite(config)`, then
   `process_provider()`, then `clock()`, followed by reconciliation using those captured inputs.
   Keep discovery and process providers injectable for deterministic tests if necessary.
2. Route `observe()` and each `watch_managed()` iteration through that same ordering. Managed
   ownership, stop/heartbeat/lease checks, reconciliation, events, active management, and writes
   use the post-sample timestamp. Preserve initial watcher ownership claiming and all exit reasons.
3. Make the temporal regressions green and verify genuine stale detection still passes.

## Slice 3 — latest-version mutable handoff state

1. Introduce a small helper that identifies mutable handoffs only when type is
   `CHECKPOINT_UPDATED` or `RESULT_AVAILABLE`, keys them by exact `(type, identity)`, and compares
   normalized admission timestamps with event-ID tie-breaking.
2. During deferred admission, normalize any pre-existing duplicates and replace older deferred
   versions with the newly admitted newer version. Do not alter manager-signal admission or
   request-correlated signal pruning.
3. Before saving notification state, coalesce mutable versions across pending plus deferred. If a
   newer matching deferred version exists, replace pending atomically, remove all matching
   deferred versions, and add a deterministic `superseded_event_ids` list to the replacement's
   notification metadata/data without marking those IDs acknowledged.
4. Preserve exact ack behavior: an old superseded ID does not clear current pending; the current
   replacement ID does. Ensure the same normalization runs after restart and before selection so
   legacy duplicate state self-heals deterministically.
5. Make the focused tests green, then run affected notification, stable-I/O, CLI/watch, and active
   management suites.

## Slice 4 — bounded verification and independent audit

1. Run the focused Clean-N regressions.
2. Run the affected local harness suites only once after focused green.
3. Run the full local `orchestrator_harness` suite once after affected green.
4. Run one board-free practical same-output watch lifecycle smoke: queue successive checkpoint
   versions behind unrelated pending work, restart the watcher, acknowledge in exact order, and
   prove only the newest checkpoint is delivered once with no process residue.
5. Update the existing verification evidence and return the diff, commands, outputs, and smoke
   artifacts to the same persistent independent auditor. Fix only validated functional gaps.

## Successor canary gate

Do not start Clean-O until the same auditor passes the repair. Preserve the four Clean-N prepared
lane boundaries but create a fresh epoch config, output state, assignments, leases, controller
lifetimes, request/relay state, and notifications. Clean-N remains noncounting and the consecutive
counter remains `0/3`.

## Audit-block resolution — preserve admission order through promotion

The first implementation audit reproduced the original Clean-N state and proved that a promoted
old deferred checkpoint lost its admission time. Its selection-time `observed_utc` then compared
newer than later-admitted deferred versions, so the coalescer retained the obsolete event.

1. When `select_actionable_with_deferred()` promotes a mutable stored handoff, copy its normalized
   `admitted_utc` (and deterministic tie-break fact if represented separately) onto pending. When
   a current mutable event is selected in the same scan as its deferred admission, bind and remove
   that matching deferred record and carry the same admission fact onto pending.
2. Compare mutable pending/deferred versions only by preserved admission time plus event-ID
   tie-break. Never use selection-time `observed_utc` as the version order.
3. For legacy pending records with no admission field, rank the missing fact before any explicit
   admission for the same `(type, identity)`; this deterministically migrates old state without
   allowing a late selection timestamp to discard explicitly newer evidence.
4. Preserve the transitive union of any prior `superseded_event_ids` when a further version
   replaces pending. Superseded IDs remain audit metadata, never acknowledged IDs.
5. Add a true same-output lifecycle regression reproducing the retained Clean-N ordering: admit an
   old version, promote it later, admit newer versions, restart, and prove the newest alone remains
   pending/deliverable. Invoke the real acknowledgement route and assert old-ID ack fails while
   current-ID ack succeeds. Assert no obsolete later wake-up and manager signals remain separate.
6. Run the focused regression and affected notification/watch suites. Production changes require
   one final full local harness run after focused green. Return the corrected evidence to the same
   persistent auditor; do not run hardware, server, or external lanes.
