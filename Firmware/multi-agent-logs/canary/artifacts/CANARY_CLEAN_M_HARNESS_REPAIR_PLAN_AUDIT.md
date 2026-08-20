# Adversarial review — Clean-M harness repair spec and plan

**Verdict: PASS**

The amended design resolves the prior blocking one-way-door ambiguity.

## Verified plan properties

- Deferred records now explicitly preserve the immutable event plus admission-time priority,
  normalized deadline/order key, identity, and admission timestamp. Deferred selection is
  explicitly forbidden from calling `_priority()` or current lane-liveness logic. This directly
  repairs the Clean-M case where a live `MANAGER_SIGNAL` lost to a higher-priority condition and
  then became non-live when the lane exited.
- The regression requires the decisive post-exit condition, not just a generic queue test:
  acknowledge the higher event after lane exit and deliver the stored handoff without a second
  filesystem transition.
- Same-output-state managed stop/restart is now explicitly tested both before and after the
  higher-priority acknowledgement. Fresh-output historical suppression remains separately tested.
  Together these cover persistence without allowing old files to awaken a fresh epoch.
- `MANAGER_SIGNAL` remains correctly distinct from transition-only `CHECKPOINT_UPDATED`.
  The backlog makes retention of file-backed handoff types an explicit new contract rather than
  relying on the incorrect old transition-only explanation.
- Exact acknowledgement, correlated-request supersession, and optional-field backward
  compatibility have focused coverage. The proposed tests are proportional to the changed
  durable-state behavior.
- The operator launcher remains a manager-only primitive, is unreferenced by watcher execution
  paths, and has no scheduling/lease/acknowledgement/hardware authority. It therefore preserves
  the primary watcher's non-negotiable read-only boundary. Its fail-closed receipt and harmless
  Windows survival smoke are adequate and do not require hardware testing.
- Retaining the current conservative exit-race behavior is correct; no exit-grace change is
  needed.

## Implementation guardrails

Implementation should preserve the stated rule that only a proven answered correlated request,
exact acknowledgement, or an explicitly specified validity rule removes a deferred entry. The
independent post-implementation audit should inspect the diff to ensure collection occurs even
while a different event is pending and that receipt cleanup in launcher tests remains exact-child
only.
