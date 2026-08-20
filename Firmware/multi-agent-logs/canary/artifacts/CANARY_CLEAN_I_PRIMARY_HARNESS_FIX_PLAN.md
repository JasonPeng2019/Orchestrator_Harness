# Clean-I primary-harness correlation/lifecycle repair plan

Date: 2026-07-31  
Author: current root/main orchestrator  
Scope: `orchestrator_harness` only; no watcher, server, lane-controller, experiment, catalog, or skill change

## Verified defects

The persistent Terra-medium Clean-I audit in `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_I.md` validated three related primary-harness defects:

1. `active_management._is_lane_match` permits session fallback even when a record explicitly declares a different lane, allowing historical requests/signals from a reused persistent session into the active lane projection.
2. `reconcile.reconcile` synthesizes a missing-MCP ambiguity for every declared MCP name even after a lane has terminally checkpointed before MCP creation.
3. `notifications._priority` makes any `RESOURCE_AMBIGUOUS` condition actionable without requiring that its lane/request/lifetime is current, so historical inactive-epoch ambiguity can wake a fresh managed watcher.

## Accepted one-way-door decisions

- An explicit non-empty `declared_lane_id` is authoritative. If absent, a non-empty direct `lane_id` is authoritative. Session fallback is permitted only when neither explicit lane field exists. This matches `reconcile._record_belongs_to_lane` and preserves legacy unlabelled records.
- A status declaration of an MCP server is a live expectation only while the reconciled lane process is active or unknown. If the lane has exited/checkpointed/resulted without an actual correlated MCP record, do not invent `MCP_STATE_UNKNOWN` or resource ambiguity. Existing correlated lifetime records remain observable after exit.
- `RESOURCE_AMBIGUOUS` is manager-actionable only when its named lane is currently active/unknown or when that lane has a current actionable request or live helper/MCP lifetime. Historical inactive ambiguity remains in snapshots/events for audit but cannot wake a fresh epoch.
- Do not delete history, alter stable event IDs, weaken real resource-conflict detection, suppress live missing-MCP detection, or change server/lane behavior.

## Implementation slices

### Slice 1 ? explicit lane authority in active management

Edit `orchestrator_harness/active_management.py`:

- make `_is_lane_match` check `declared_lane_id`, then direct `lane_id`; if either non-empty explicit field is present, return only its equality with the projected lane;
- use session/producer-identity fallback only when no explicit lane field exists;
- keep latest-current request selection by existing creation-time sort once the candidate set is correctly scoped.

Focused tests in `test_active_manager_watch_smoke.py`:

- a historical request with the same session but a different explicit lane does not enter the current lane;
- the current explicit-lane Clean-I request is selected;
- an unlabelled legacy record with the exact session still correlates.

### Slice 2 ? terminal pre-MCP lifecycle

Edit `orchestrator_harness/reconcile.py`:

- introduce one explicit local active/unknown lifecycle predicate and use it both for resource ownership/audit expectations and missing-MCP synthesis. It must include every state reconciliation already treats as current: `RUNNING_CODEX`, `WAITING_RELAY`, `HELPER_RUNNING`, `PROCESS_STATE_UNKNOWN`, and `UNKNOWN` when that is the reconciled unknown spelling;
- synthesize missing declared MCP identities/ambiguity only while that shared predicate is true;
- never synthesize it for `EXITED`/`CHECKPOINTED`/`TERMINAL_RESULT` lanes that have no actual MCP record;
- continue reconciling any real correlated MCP lifetime, including unknown/live records, regardless of controller exit.

Focused tests in `test_reconcile.py`:

- terminal checkpoint before MCP creation has no invented MCP record/ambiguity and can release resources;
- live/unknown lane declaring an MCP without lifetime evidence still gets the existing ambiguity/unknown MCP, with explicit positive controls for `RUNNING_CODEX`, `WAITING_RELAY`, `HELPER_RUNNING`, and `PROCESS_STATE_UNKNOWN`;
- terminal lane with a real live/unknown correlated MCP lifetime remains nonreleasable and observable.

### Slice 3 ? actionable currentness at bootstrap

Edit `orchestrator_harness/notifications.py`:

- for `RESOURCE_AMBIGUOUS`, determine whether the condition's lane is current using active/unknown lane process state, a current actionable same-lane request, or a live same-lane helper/MCP lifetime;
- return no priority for inactive historical ambiguity;
- leave `RESOURCE_CONFLICT`, duplicate-controller, request-expiry, and all other priority rules unchanged.

Focused tests in `test_manager_notifications.py` and/or `test_active_manager_watch_smoke.py`:

- clean epoch bootstrap ignores historical inactive-lane `RESOURCE_AMBIGUOUS`;
- active current-lane resource ambiguity remains actionable;
- inactive controller with a still-live exact request/lifetime remains actionable;
- historical ambiguity remains observable in conditions/events even when not selected.

## Verification

Run only focused changed tests first. Then run the ordinary primary harness unit suite once:

```powershell
python -m unittest orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_reconcile orchestrator_harness.tests.test_manager_notifications -v
python -m unittest discover -s orchestrator_harness/tests -t . -v
```

Add a small synthetic Clean-I-shaped control (no real agent, provider, server, or hardware): historical Clean-H lane + reused-session Clean-F request + current Clean-I request + terminal pre-MCP A24/A26. Assert fresh pending notification is null, current request wins, terminal lanes have no invented MCP ambiguity, and a separate live missing-MCP control remains actionable.

Do not rerun expensive real-agent tests or prior accepted canaries; the changed surface is deterministic read-only correlation. No production process, watcher service, lane, MCP, or hardware launch is permitted during repair verification.

## Acceptance

The repair is accepted only if:

- focused and ordinary harness tests are green;
- the synthetic Clean-I control proves all three defects fixed and the real-positive controls preserved;
- diff contains no watcher/server/lane/experiment changes;
- the same persistent Terra-medium auditor reviews the implementation and returns PASS or only advisory/nonfunctional criticism.
