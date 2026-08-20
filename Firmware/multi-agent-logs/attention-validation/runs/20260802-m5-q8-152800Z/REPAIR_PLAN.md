# Q8 final-publication evidence repair plan

## Verified gap

A durable creation record now intentionally precedes exposure of final manager-signal JSON, but no
record marks the actual atomic publication. Therefore created-to-observed time can include worker
publication delay while the watcher labels it as harness delay.

## Smallest repair

1. Add passive subagent record kind `AGENT_SIGNAL_PUBLISHED`, correlated to the same epoch, event,
   lane, signal, and deadlines. It records the source timestamp captured at the atomic final-file
   exposure. It never wakes, notifies, acknowledges, or controls anything.
2. For blocked-signal harness attribution, require a unique causally ordered publication record.
   Use publication-to-harness-observation for detection latency. If publication is missing,
   contradictory, or after the declared delivery deadline, fail closed as insufficient evidence;
   never blame the harness for time when the final signal was unavailable.
3. Preserve the user's six primary wake stages. Publication is a narrow causal boundary between
   worker creation and harness detection, not a new wake mechanism.
4. Update focused tests for timely publication, delayed publication, missing publication,
   reversed publication order, and unchanged native wake/manager behavior. Do not change harness
   scheduling, transport, manager logic, or add helpers/wrappers.
5. Update worker procedure: prepare staging; record creation; capture publication UTC; atomically
   rename; record publication with that captured UTC; record wait-start. All may occur in one
   worker-owned bounded shell operation, with each recorder result verified.
6. Terra coder implements; independent Terra reviewer advises; root adjudicates; Luna-high runs a
   practical smoke; then full tests, M4 readiness, docs/state synchronization, and refreeze.

Attempts 9-10 remain. This relevant logging/watcher change keeps the comparable count at 0/3, so
the active 10-attempt budget cannot now produce the required 3/3. Continue only through attempt 10
as authorized; never launch attempt 11.
