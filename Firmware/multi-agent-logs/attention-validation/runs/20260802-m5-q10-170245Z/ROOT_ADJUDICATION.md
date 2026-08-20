# Q10 root adjudication

Date: `2026-08-02`

## Final gates

- `HARNESS_PASS`
- `WATCHER_PASS`
- `MANAGER_EVIDENCE_INSUFFICIENT`
- Disposition: `EVIDENCE_INSUFFICIENT`
- Active-goal attempt: `10/10`; comparable count remains `0/3`
- Next live attempt: **none**. Q11 is forbidden by the active attempt budget.

## Accepted reviewer findings

- The harness observed, selected, returned, and acknowledged all four genuine HELP requests without
  a verified native defect.
- The watcher stayed diagnostic-only, drained, and correctly failed closed instead of fabricating a
  causal classification.
- No forbidden assistance influenced discovery.
- Cleanup is exact and resources are empty.
- The final quiet timeout does not make the quiet control clean because four retained Q9 stale
  statuses surfaced first.
- The bounded busy interval is valid, but it does not cover the complete late request intervals.
- All four workers rejected the manager responses because every response contained an empty
  `lane_id`; therefore no worker truthfully recorded `AGENT_RESPONSE_RECEIVED` or
  `AGENT_WORK_RESUMED`.

## Rejected reviewer finding: native/source event identity

The reviewer attributed the finalizer and wake-correlation failures to use of each `data.signal_id`
instead of the native envelope's top-level hash `event_id`. Raw evidence disproves that diagnosis.

- Q8 used the same source signal ID for the manager attention chain and finalized successfully.
- The attention analyzer correlates the worker and manager causal chain by the source event ID.
- The top-level native hash is separately required for exact harness acknowledgement.
- All four genuine Q10 claims have complete `SELECT_ACTIONABLE` snapshots selecting their own source
  event IDs.

The finalizer failure came from four **pre-worker stale-status claims** whose snapshots used
`selection_reason: NATIVE_BLOCKING_WAIT`, not `SELECT_ACTIONABLE`. The immutable records and exact
offending IDs are preserved. This was a root recording-procedure error, not a harness or watcher
defect.

## Actual causal-record failures

For each genuine request, root recorded `MANAGER_WAIT_FINISHED` before
`MANAGER_WAKE_RECEIVED`. The required order is receipt first, then wait finish. The watcher therefore
correctly reported `manager acted before wake receipt` and classified the request as
`INSUFFICIENT_EVIDENCE`.

Separately, PowerShell response construction produced an empty `lane_id` in all four response
files. Workers correctly rejected the mismatched responses and created no receipt/resume records.
This downstream identity failure independently prevents a complete request chain.

## Architecture conclusion from Q10

Q10 proves that the unassisted native harness can surface four genuine multi-lane requests and that
the diagnostic watcher can expose malformed evidence without helping the manager. It does **not**
prove whether a persistent manager is sufficient or whether a `codex exec` bridge is needed,
because root's record ordering and response identity mistakes severed every end-to-end causal
chain. No Q10 delay may be excused as busy-manager contention.

No production-code repair is justified by Q10. Any future continuation requires explicit new user
authority and a new attempt budget; the procedural corrections are: receipt before wait-finish,
exact non-empty response lane validation before publication, exact `SELECT_ACTIONABLE` claim
snapshots, and a genuinely clean quiet-control surface.
