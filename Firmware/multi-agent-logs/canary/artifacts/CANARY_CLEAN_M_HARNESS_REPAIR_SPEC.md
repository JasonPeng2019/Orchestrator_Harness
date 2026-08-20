# Clean-M harness repair specification

Status: proposed for independent plan review  
Scope: primary `orchestrator_harness` plus an explicitly manager-invoked launch utility  
Out of scope: BYO-Firmware-MCP, optional watcher evaluator logic, firmware, hardware, lane evidence,
and retrying any Clean-M endpoint

## Problem 1 — a valid handoff can lose its wake-up

In Clean-M, Delta's current `MANAGER_SIGNAL` was actionable while Delta was live, but a
higher-priority condition occupied the one pending slot. Delta exited before that condition was
acknowledged. `_manager_signal_is_live()` then made the still-unacknowledged handoff ineligible,
so it never became pending. The event remained observable in `events.jsonl`, but the manager had
to find it out of band.

### Required behavior

1. A handoff that was genuinely actionable when observed must not be lost merely because another
   event won the pending slot or because its lane subsequently exited.
2. Persist unselected actionable handoffs across scans and managed-watcher restart in the same
   output state.
3. After the current pending event is acknowledged, select the highest-priority still-valid
   deferred handoff without requiring a second filesystem transition.
   “Still-valid” does **not** mean rerunning current lane-liveness gating: each deferred entry
   captures its admission-time priority, deadline/order key, identity, and admission timestamp,
   and selection uses those stored admission facts after lane exit.
4. Durable handoffs are limited to explicit file-backed `MANAGER_SIGNAL`, `CHECKPOINT_UPDATED`,
   and `RESULT_AVAILABLE` events. Do not make transient process/resource/request warnings durable.
5. A deferred request-correlated manager signal whose request is now answered may be discarded as
   superseded. An uncorrelated checkpoint/pass/feedback/instruction signal remains reviewable.
6. Preserve fresh-epoch historical suppression: an already-exited historical lane/signature must
   not seed a new output state's deferred queue merely because old files exist.
7. Exact acknowledgement removes only the acknowledged pending event. Deferred events remain
   ordered and durable until selected, acknowledged, or explicitly proven superseded.
8. Existing notification state files without the new optional field remain readable.
9. A managed-watcher stop/restart against the same output state must preserve a deferred handoff
   after its lane exits and must deliver it after the higher-priority pending event is acknowledged.

## Problem 2 — long-lived processes were launched from transient tool jobs

The first primary owner, optional watcher, and Cygnus controller were reaped when their transient
invoking tool-shell job ended. The successful recovery used Windows
`CREATE_BREAKAWAY_FROM_JOB | CREATE_NO_WINDOW` directly from an ad hoc Python snippet.

### Required behavior

1. Provide one durable, manager-invoked process-launch utility for all long-lived manager-owned
   owners, optional watchers, and lane controllers.
2. On Windows, launch without a shell using `CREATE_BREAKAWAY_FROM_JOB | CREATE_NO_WINDOW`; on
   POSIX, use a new session. The launched process must survive normal exit of the short-lived
   launch utility.
3. Atomically write a launch receipt containing label/role, exact argv, cwd, PID, provider process
   creation time, launch time, platform/flags, and optional expected status/runtime path.
4. Fail closed if argv/cwd is invalid, the receipt already exists, creation identity cannot be
   captured, or the child exits before its identity is proved. Never silently fall back to an
   attached process.
5. The utility never schedules work, selects a lane, grants a lease, acknowledges a notification,
   kills a process, or performs hardware/server action. The main manager remains the sole caller
   and authority.
6. The primary watcher remains read-only and must never import or invoke the launch utility. This
   is an operator-side primitive colocated with the harness, not a watcher capability.
7. Test that a harmless child remains live after the utility exits, then clean up only the exact
   test child from the test fixture.

## Manager review-cadence contract

No additional product defect was established for Clean-M's formal-review gap. The next canary
must nevertheless enforce this operational contract:

1. At every exact `MANAGER_REVIEW_DUE`, the manager writes a whole-suite review record first.
2. It invokes the canonical `ack --event-id ...` route while that event is exactly pending.
3. It immediately verifies that `active-management-history.json` advanced
   `review_baseline_utc`, logs the new baseline, and rescans eligibility.
4. A sprint with a missed review, nonadvancing baseline, or out-of-band pseudo-ack cannot count.

## Acceptance

- Focused regression reproduces the Clean-M ordering: a higher-priority event and a current Delta
  handoff arrive together; the higher event becomes pending, the handoff is deferred, Delta exits,
  the higher event is acknowledged, and the handoff becomes pending without another transition.
- The same regression stops and restarts managed watch after Delta exits but before/after the
  higher-priority acknowledgement, proving admission priority/order and delivery survive restart.
- Fresh-output historical files do not seed deferred handoffs.
- Superseded correlated signals are dropped; uncorrelated checkpoint signals are retained.
- Notification-state backward compatibility passes.
- Real Windows launch smoke proves a harmless child survives launcher exit and the receipt has an
  exact PID+creation identity; invalid/reused receipt cases fail closed.
- Existing focused harness tests and the full harness suite remain green.
- No hardware, external agent lane, server edit, or retained Clean-M run is executed during repair.

## Independent-audit amendment — validated post-spawn failure gap

The first implementation audit reproduced one functional fail-closed defect: after the detached
child was spawned, a failed creation-identity proof wrote a failed receipt and returned nonzero
but left that exact child alive. The audit removed the exact test PID and found no residue.

The accepted repair therefore additionally requires:

1. Any exception after `Popen` succeeds but before a successful launch receipt is finalized must
   terminate and reap the exact `Popen` child before `launch_process()` returns or raises. A short
   bounded graceful wait followed by an exact-child forced termination is allowed; no name-based
   or broad process kill is allowed.
2. The failed receipt must truthfully record whether exact-child cleanup completed. If cleanup
   itself cannot be confirmed, surface that fact in both the receipt and raised error rather than
   claiming a clean failure.
3. A focused regression must force identity proof to fail after a harmless child is spawned and
   prove that exact child is absent when the launcher returns failure.
4. The lifecycle acceptance test must actually stop and start distinct `watch_managed()`
   invocations against the same output state, covering persistence before acknowledgement and
   delivery after acknowledgement. Reloading `SafeOutput` alone is insufficient lifecycle proof.

## One-way-door decisions

1. **Use a small durable handoff backlog, not permanent liveness for every historical signal.**
   This preserves current-epoch delivery without waking fresh epochs from old files.
2. **Keep the launcher operator-side and unreferenced by watcher execution paths.** The watcher
   remains read-only; the manager gains a reliable primitive without turning the harness into a
   scheduler.
3. **Do not add exit grace.** Clean-M's brief terminal-status/live-process overlap was correctly
   fail-closed and cleared on exact absence.
