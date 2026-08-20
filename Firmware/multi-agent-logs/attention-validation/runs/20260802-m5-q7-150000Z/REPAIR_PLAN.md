# Q7 watcher deferral-metric repair plan

## Verified defect

`harness_watcher_implementation.attention` currently computes `explicit_deferral_seconds` from the
first deferral record and the pending record even when that deferral happened **after** the event
was already pending. This produces an impossible negative metric and invalidates an otherwise
usable request chain.

## Smallest repair

1. For `explicit_deferral_seconds`, use only a `HARNESS_EVENT_DEFERRED` endpoint at or before the
   selected pending/actionable endpoint. If no such pre-pending deferral exists, do not invent a
   deferral duration.
2. Add focused regression tests for: normal pre-pending deferral stays positive; after-pending
   deferral does not produce a negative metric or contradiction; truly reversed causal endpoints
   elsewhere still fail closed.
3. Do not change harness scheduling, wake transport, manager logic, worker code, other watcher
   classifications, or add assistance/wrappers.
4. Run focused/full tests, independent Terra review, Luna practical smoke, M4 readiness, and
   refreeze the Python surface before attempt 8.

Root owns acceptance. Reviewers advise and never block.
