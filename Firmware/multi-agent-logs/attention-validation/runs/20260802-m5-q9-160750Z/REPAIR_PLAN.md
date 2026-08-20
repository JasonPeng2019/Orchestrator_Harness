# M5 Q9 Watcher Attribution Repair Plan

## Verified defect

When the harness observes a `MANAGER_SIGNAL` but correctly finds its producer
lane/request/helper non-live, no canonical attention record explains why the
signal is ineligible. With otherwise trusted scan coverage, the watcher then
misclassifies the missing actionable transition as `HARNESS_DELIVERY_DELAY`.

## Required behavior

1. Keep the existing native liveness and actionability decisions unchanged.
2. At observation time, emit one passive, exactly correlated harness attention
   record when a manager signal is ineligible because its producer is not live.
   The record must identify the signal event and carry one bounded canonical
   reason such as `LANE_NOT_LIVE`. It must not enqueue, wake, relay, schedule,
   retry, or otherwise affect runtime behavior.
3. In watcher analysis, accept that reason only when it exactly correlates to the
   analyzed signal and occurs no earlier than the harness observation. In that
   case, fail closed as `INSUFFICIENT_EVIDENCE`; do not blame the harness.
4. Missing, mismatched, contradictory, stale, or unsupported reasons must not
   suppress a real `HARNESS_DELIVERY_DELAY`.
5. Preserve the current classification for a live blocked signal that misses
   actionability with complete trusted coverage.

## Smallest implementation

Prefer a dedicated passive attention kind (for example
`HARNESS_EVENT_INELIGIBLE`) over overloading deferred-queue semantics. Put the
single liveness-reason decision in the harness notification owner and call it
from the native managed scan loop immediately after the corresponding observed
record. Extend only the watcher schema/analyzer paths needed to consume it.

## Tests

- Non-live producer: observed + exact ineligibility evidence becomes
  `INSUFFICIENT_EVIDENCE`, never `HARNESS_DELIVERY_DELAY`.
- Live producer: selection/actionability behavior is unchanged.
- Live blocked signal with complete coverage and no actionability remains
  `HARNESS_DELIVERY_DELAY`.
- Wrong event ID, wrong reason, wrong ordering, or duplicate/contradictory
  evidence cannot suppress the delivery-delay classification.
- Existing harness and watcher suites remain green.

## Explicit exclusions

No controller fix, sprint runner, wrapper, relay, scheduler, evaluator, AI
watcher, wake helper, or manager-behavior change. Q10 launch quoting is an
operator-procedure correction, not production code.
