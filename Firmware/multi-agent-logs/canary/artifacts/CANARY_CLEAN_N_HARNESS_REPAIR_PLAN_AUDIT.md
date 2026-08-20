# Adversarial review — Clean-N harness repair spec and plan

**Verdict: PASS**

The plan directly addresses both independently validated failures with bounded, convergent
semantics and preserves the accepted Clean-M handoff contract.

## Findings

- The specified discovery → process inventory → post-sample clock order is the correct
  one-way decision. Routing both `observe()` and managed-watch reconciliation through that one
  boundary fixes the factual Clean-N inversion without a grace period that could hide real stale
  identities. The absent/reused control prevents a blanket `STALE_STATUS` suppression.
- Mutable coalescing is correctly limited to `(type, identity)` for `CHECKPOINT_UPDATED` and
  `RESULT_AVAILABLE`. It explicitly leaves immutable `MANAGER_SIGNAL` entries and their exact
  answered-correlated pruning rule unchanged.
- The plan covers the essential cross-state case, not just deferred-list cleanup: a newer mutable
  event replaces an older **pending** event atomically, clears matching deferred versions, records
  superseded IDs, and does not treat those IDs as acknowledged. Therefore an acknowledgement of
  the obsolete ID cannot clear the replacement, and no obsolete wakeup can recur after restart.
- Deterministic newest selection (normalized admission timestamp, then event ID), state
  normalization before selection/restart, exact-ack behavior, and same-output restart tests make
  the durable notification state converge even from legacy duplicate state.
- The red/green regressions and practical local lifecycle smoke are proportional to the two
  defects. No hardware, server, or external-lane exercise is needed.

## Implementation audit points

At implementation review, verify the coalescing operation runs before managed watch takes its
existing pending-event early-continue, and that all managed ownership/lease/event timestamps use
the post-sample time. Those are already explicit plan requirements rather than unresolved design
gaps.
