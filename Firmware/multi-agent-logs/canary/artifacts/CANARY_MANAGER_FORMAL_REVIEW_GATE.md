# Canary manager formal-review gate

Applies to every successor canary used for the active `0/3 -> 3/3` acceptance goal.

1. The main manager owns a wall-clock review deadline independent of the primary harness pending
   notification. While any lane is live, inspect all lanes and write a compact whole-suite review
   no later than the configured manager-review interval.
2. A due review preempts ordinary `MANAGER_SIGNAL`, checkpoint, and result draining. Safety,
   permission, ownership-conflict, and process-identity events remain higher priority, but review
   them without artificial sleep and then immediately complete the whole-suite review.
3. After the review record exists, consume and acknowledge the exact `MANAGER_REVIEW_DUE` event as
   soon as it becomes pending and prove `review_baseline_utc` advanced. Do not treat a later
   `CONDITION_CLEARED` as a substitute.
4. Until the record and acknowledgement are complete, do not authorize a new lane, permission
   relay, or hardware phase. Existing atomic operations may reach their declared safe boundary.
5. During event draining, use the managed watcher/event file as the wake path and only the minimum
   reconciliation delay; do not add fixed 20-to-30-second sleeps per acknowledgement.
6. Every canary target must cite this gate and record review deadlines, review files, exact event
   IDs, acknowledgement times, baseline-before/after values, and any higher-priority event that
   temporarily preempted the review.

This gate fixes the Clean-O manager-procedure lapse. It does not change primary-harness priority or
claim that the primary harness was defective.
