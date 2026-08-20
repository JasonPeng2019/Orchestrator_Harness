# Clean-K primary-harness repair plan review

## PASS

The spec and plan address the validated lifecycle/actionability failures without
weakening current safety signals.

- The suite `lifetime_binding` rule is appropriately fail-closed: exact server,
  PID, parseable creation time, and live-process reconciliation are required;
  mismatch or missing identity remains ambiguous/actionable.
- The plan correctly separates immutable exact relay proof from relay freshness.
  `BOUND_EXPIRED` / `RELAYED_EXPIRED` retains audit evidence while never making
  an expired approval reusable authority.
- Signal suppression relies on durable request ID or exact request-evidence-path
  correlation plus exact answered-relay evidence, not prose, mtime, or a
  checkpoint heuristic.  An unanswered HELP in a live lane remains a required
  positive control.
- Historical PID reuse is gated by lane/request correlation, while a newly
  observed genuinely uncorrelated exit remains alarmable.  Existing live
  missing/unbound/ambiguous request, warning/critical expiry, resource-conflict,
  and live HELP controls are explicitly retained.

The plan does not rely on nonexistent consumption evidence: its accepted
definition of “answered” is an exact immutable request/relay binding, which is
present in the retained Clean-K suite records.  Its no-write retained-data scan
and focused positive controls are sufficient for the bounded repair.

## Advisory (non-blocking)

Test the post-cleanup historical form of an exact expired relay as well as the
still-live form, so the retained-data scan locks in nonactionability after the
provider has exited.  This is coverage refinement; the plan already requires
the relevant expired-bound behavior and does not need scope expansion.

## Delta review — active-management consumer

**PASS.**  The amendment traces the real consumer:
`active_management._request_is_stage_complete` currently recognizes only
`BOUND` or an absent lifetime.  Adding `BOUND_EXPIRED` as an answered/completed
stage prevents a correctly answered historical request from generating false
stage-repeat/no-progress churn.  The plan expressly retains the distinction
from executable authority, so this does not authorize use of an expired relay.
