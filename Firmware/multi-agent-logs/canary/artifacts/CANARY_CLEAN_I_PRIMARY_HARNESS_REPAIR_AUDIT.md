# Clean-I primary-harness repair audit

## PASS

The implementation conforms to the accepted repair plan and fixes all three
validated Clean-I defects without suppressing the required real positives.

- **Explicit lane authority:** `active_management._is_lane_match` now returns
  the equality result for the first non-empty `declared_lane_id` or `lane_id`;
  it uses session fallback only when neither exists.  The new focused controls
  cover reused-session historical exclusion, current explicit-lane selection,
  and legacy unlabelled-session correlation.
- **Terminal pre-MCP lifecycle:** `reconcile._lane_is_active_or_unknown` is the
  shared predicate for resource ownership and missing-MCP synthesis, covering
  `RUNNING_CODEX`, `WAITING_RELAY`, `HELPER_RUNNING`,
  `PROCESS_STATE_UNKNOWN`, and `UNKNOWN`.  Missing MCP state is therefore still
  synthesized for every required live/unknown state, but not invented for a
  terminal pre-MCP lane.  Tests also retain a correlated unknown MCP as
  nonreleasable after terminal controller state.
- **Historical ambiguity wake-up:** `notifications._priority` now calls
  `_resource_ambiguity_is_current` for `RESOURCE_AMBIGUOUS`.  It remains
  actionable for an active/unknown exact lane, actionable current request, or
  live exact helper/MCP; inactive historical ambiguity remains observable but
  cannot wake a fresh epoch.  Resource-conflict and the other priority branches
  are unchanged.

The repaired-code scan over retained Clean-I data reports all four Clean-I lanes
as `CHECKPOINTED`, with empty `resource_ambiguity` and
`resource_release_possible: true`; it has zero resource conflicts and zero
observation errors.  This directly removes the former A24/A26 terminal
false-positive state and does not fabricate a Clean-H bootstrap warning.

Reported verification is consistent with the changed surface: coder focused
tests **114 passed**; ordinary discovery **151 passed, 1 skipped**; manager's
independent targeted rerun **11 passed**.  The test additions include live
missing-MCP controls for running, waiting-relay, process-unknown, unknown, and
helper-running states, as well as current request/live-MCP ambiguity controls.

No functional blocker was found.  The plan-review suggestion to model the exact
Clean-I HELP/signal schema remains advisory coverage refinement, not a repair
requirement.
