# Clean-N primary-harness repair specification

Status: proposed for independent plan review  
Owner: current main orchestrator  
Scope: `orchestrator_harness` observation sampling and durable handoff notification state  
Out of scope: BYO-Firmware-MCP, optional watcher evaluator, firmware, hardware, prepared Clean-N
lane evidence, and any retry of a Clean-N live endpoint

## Validated defect 1 — temporally incoherent observation sampling

Clean-N emitted a false startup `STALE_STATUS`: the event's observation time preceded the
creation times of the exact controller and Codex processes described by that event. The managed
watcher sampled the clock before a slow process inventory and then discovered status files after
that inventory, so reconciliation compared facts gathered later with an earlier timestamp.
`observe()` has the same process-before-discovery ordering and pre-sample timestamp.

### Required behavior

1. A reconciliation observation must use one explicit sample order: discover run/status files,
   then collect the process inventory, then capture the observation timestamp.
2. The timestamp passed to reconciliation, lifecycle classification, event generation, active
   management, lease checks, and persisted output must be the post-sample timestamp.
3. A status/process that begins during discovery and exists in the following process inventory
   must not be classified stale merely because it began after the scan started.
4. Genuine stale declarations—running status with an exact process absent or identity-reused in
   the completed process inventory—must remain detectable.
5. Apply the same coherent sampling rule to one-shot observation commands and managed watch. Do
   not add timing grace, sleep, retry loops, or suppress `STALE_STATUS` generally.

## Validated defect 2 — obsolete checkpoint/result versions remain queued

Clean-N retained three event versions for one Boreal checkpoint identity. After higher-priority
work was acknowledged, the oldest obsolete version became pending while two newer hashes remained
deferred. Durable admission currently deduplicates only event IDs and does not coalesce mutable
file-backed handoffs by identity.

### Required behavior

1. Treat `CHECKPOINT_UPDATED` and `RESULT_AVAILABLE` as mutable, latest-version handoffs. At most
   one unacknowledged version per exact `(type, identity)` may remain across pending plus deferred
   notification state.
2. When a newly admitted mutable version supersedes deferred versions of that exact type and
   identity, retain only the newest event and its admission-time rank. Never coalesce across
   identities or across types.
3. When a newer mutable version supersedes an already-pending older version of the same exact type
   and identity, atomically replace pending with the newest event, remove matching deferred
   versions, and record the superseded event ID(s) on the replacement for auditability. The old
   event is superseded, not acknowledged; exact acknowledgement applies only to the current
   pending event ID.
4. A manager that reads durable pending state after a notification must therefore review and
   acknowledge the newest event. No obsolete version may later cause another wake-up.
5. Distinct `MANAGER_SIGNAL` events remain immutable and separately reviewable even when their
   identities match. Preserve the Clean-M rule that only an exactly answered correlated manager
   signal may be pruned.
6. Preserve admission-time priority/order for the retained newest version, exact acknowledgement,
   restart persistence, notification-state backward compatibility, and fresh-output historical
   suppression.
7. Coalescing must be deterministic even if an old state file already contains multiple mutable
   versions: choose the greatest normalized admission timestamp, breaking ties by event ID.

## Acceptance

- A deterministic slow-sample regression creates a controller/status after scan start but before
  the completed process inventory and proves no false `STALE_STATUS` in both `observe()` and
  managed watch.
- A control test still detects a genuinely absent/reused declared process.
- Deferred-only tests prove three same-identity checkpoint versions collapse to the newest hash;
  distinct identities and manager signals remain separate.
- Pending-plus-deferred tests prove a newer checkpoint/result atomically replaces an older pending
  version, exposes supersession metadata, accepts only the replacement's exact acknowledgement,
  and never later delivers an obsolete version.
- Stop/restart against the same output state retains only the newest version and delivers it once.
- Fresh-output historical suppression remains green.
- Focused tests, affected harness tests, and one final full local harness suite pass. No external
  agent lane, hardware, firmware server, or retained Clean-N endpoint is run during repair.

## One-way-door decisions

1. **Use ordered end-of-sample time, not a grace window.** Discovery-before-process-before-clock
   gives reconciliation a coherent boundary without hiding real stale identities.
2. **Coalesce only mutable checkpoint/result handoffs.** Manager signals remain immutable because
   different messages can require distinct decisions even when they share a lane.
3. **Supersession is not acknowledgement.** Replaced event IDs are recorded on the newest pending
   event; the manager must acknowledge that exact current ID.

