# Clean-K primary harness lifecycle/actionability repair plan

## Inputs and scope

- Spec: `.agent-workspace/CANARY_CLEAN_K_PRIMARY_HARNESS_REPAIR_SPEC.md`
- Audit: `.agent-workspace/CANARY_S1_CLEAN_K_INDEPENDENT_AUDIT.md`
- Code scope: `orchestrator_harness/` only
- Explicit exclusions: optional watcher, BYO-Firmware-MCP, lane/run-local A22/A26 code, experiment
  evidence, hardware, catalog status, docs/skills, commits

## Accepted one-way-door decisions

1. **Preserve evidence; gate actionability.** Historical records and ordinary events remain in the
   snapshot/event log. The repair changes only their lifecycle classification and notification
   eligibility.
2. **Binding and freshness are distinct.** Split relay evaluation so an exact-but-expired relay is
   represented as `BOUND_EXPIRED` and its request as `RELAYED_EXPIRED`. This proves the manager
   answered the immutable request while making clear that the relay cannot be consumed now.
3. **No heuristic consumption inference from prose or file mtime.** A request is answered only by
   an exact relay binding. A signal is correlated through an exact request ID or exact request
   evidence-path identity, not merely because a later checkpoint happens to exist.
4. **Fail closed on lifetime proof.** The suite `lifetime_binding` form is accepted only with an
   exact live PID/creation/server reconciliation; otherwise existing ambiguity remains.
5. **Current-lane correlation controls exit alarms.** A closed historical lifetime does not become
   actionable merely because some unrelated lane is active. Genuine current correlated exits and
   genuine newly observed uncorrelated exits retain alarms.
6. **Unknown current requests fail toward manager review, not silence.** A current, unexpired,
   unresolved request whose lifetime remains `UNKNOWN` is manager-actionable. Expired unknown
   history is not. Answered relay states remain nonactionable regardless of lifetime ambiguity.

## Implementation slices

### Slice 1 — reconcile exact suite lifecycle and relay state

In `orchestrator_harness/reconcile.py`:

1. Extend explicit MCP lifetime proof to the `suite-manager-request/v1.lifetime_binding` shape.
   Require a non-empty server name, PID, parseable creation time, and a reconciled live process for
   that exact binding. Preserve the stricter existing `live_lifetime` run/session proof.
2. Split exact relay field/hash/call binding from `expires_utc` freshness. Preserve all current
   exact-field checks, including the two documented singular/plural suite key variants already
   present in real records. Return `BOUND` only while current, `BOUND_EXPIRED` for the same exact
   immutable binding after expiry, `UNBOUND` for a candidate that fails binding, and `ABSENT` when
   no candidate exists.
3. Classify a live/absent/unknown request with `BOUND_EXPIRED` as `RELAYED_EXPIRED`, not ambiguous
   or unbound. Add an explicit boolean `manager_actionable`: false for `RELAYED`,
   `RELAYED_INACTIVE`, and `RELAYED_EXPIRED`; true only for current unresolved states that already
   require review. Keep expiry bucket as observation data.
4. While projecting manager signals, correlate each signal to a same-run request by exact
   `request_id` or an exact request-file evidence-path match. Add the correlated request ID/path and
   whether that request is already answered; retain the raw signal.

### Slice 2 — notification and active-management eligibility

In `orchestrator_harness/events.py`, `orchestrator_harness/notifications.py`, and
`orchestrator_harness/active_management.py`:

1. Include request actionability and MCP lane/session correlation fields in condition data.
2. Make request-state and request-expiry priority consult `manager_actionable`; retain backward
   compatible fail-closed behavior for synthetic/older snapshots without the new field.
3. Make manager-signal selection reject a signal correlated to an answered request before applying
   the broader live-lane fallback. Preserve current unanswered request and current lane signals.
4. Make helper/MCP exit selection require current matching lane/request correlation when such
   identity exists. Retain transition-only gating and the existing positive path for a truly new
   uncorrelated exit.
5. Treat `BOUND_EXPIRED` as an answered/completed manager-review stage in active-management
   projections so an already-answered request cannot fuel `LANE_STAGE_REPEAT` or no-progress churn.
   Do not treat the expired relay as executable authority.

### Slice 3 — focused regression tests

Add or extend only primary tests in:

- `orchestrator_harness/tests/test_reconcile.py`
- `orchestrator_harness/tests/test_manager_notifications.py`
- `orchestrator_harness/tests/test_active_manager_watch_smoke.py`
- `orchestrator_harness/tests/test_events_cli.py` only if required for additive event fields

Required cases:

1. Clean-K-shaped `lifetime_binding` + exact current suite relay -> `PROVEN`, `BOUND`, `RELAYED`,
   nonactionable.
2. Same exact relay after expiry -> `BOUND_EXPIRED`, `RELAYED_EXPIRED`, retained expiry evidence,
   nonactionable.
3. Same request with PID/creation/server mismatch -> unproven/ambiguous and actionable.
4. Bad request hash or exact-call mismatch -> `UNBOUND` and actionable.
5. HELP correlated to an answered request remains observable but is not selected, even while its
   lane runs; an unanswered HELP in the same live lane is selected.
6. A closed historical MCP with PID reuse and a different active lane remains observable but is not
   selected; a newly exited MCP correlated to the active lane is selected.
7. Genuine live unanswered request warning/critical expiry, live missing relay, resource conflict,
   and current live HELP positive controls remain selected.
8. Missing or partial creation evidence that yields an `UNKNOWN` lifetime remains selected while
   the unresolved request is current and unexpired, but is not selected after its deadline.

## Focused audit correction

The first implementation pass incorrectly required `lifetime_state == LIVE` for every explicit
`manager_actionable` request. This suppresses a genuine current unresolved request when incomplete
identity evidence correctly leaves its lifetime `UNKNOWN`. Correct only that predicate so the
unresolved operational states `REQUEST_AMBIGUOUS`, `RELAY_UNBOUND`, and `RELAY_READY` are actionable
while unexpired when lifetime is `LIVE` **or** `UNKNOWN`. Preserve nonactionability for
`RELAYED`, `RELAYED_INACTIVE`, `RELAYED_EXPIRED`, and expired `UNKNOWN` history. Add direct
reconcile-plus-notification tests for both sides of this boundary; do not rerun hardware or agents.

## Verification gate

Run once after implementation:

```powershell
python -m unittest `
  orchestrator_harness.tests.test_reconcile `
  orchestrator_harness.tests.test_manager_notifications `
  orchestrator_harness.tests.test_active_manager_watch_smoke `
  orchestrator_harness.tests.test_events_cli -v
python -m unittest discover -s orchestrator_harness/tests -t . -v
python -m orchestrator_harness --config orchestrator_harness/canary-20260731-s1-clean-k.json scan --no-write
```

Save focused/full results and one retained-data selection check in
`.agent-workspace/CANARY_CLEAN_K_PRIMARY_HARNESS_REPAIR_VERIFICATION.md`. Do not rerun hardware,
external agents, or already-passed expensive tests.

## Review and handoff

1. The same persistent Terra-medium auditor reviews this plan before implementation. A blocking
   functional finding must be resolved in this plan; advisory/gold-plating notes are logged and do
   not expand scope.
2. The same persistent Terra-high coder implements the accepted plan and nothing else.
3. The same auditor reviews the diff and focused/full/retained-data evidence. The main agent makes
   the final validity decision.
4. Only after acceptance may a fresh successor canary start. The successor must preserve D31/A24
   Clean-K progress, host-fix only A22/A26, and use an explicit 120-second review acknowledgement
   ledger.
