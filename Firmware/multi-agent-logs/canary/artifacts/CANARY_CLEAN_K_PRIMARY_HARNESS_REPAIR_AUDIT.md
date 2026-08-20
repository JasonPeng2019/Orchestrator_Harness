# Clean-K primary-harness repair audit — final disposition

**Audit date:** 2026-07-31  
**Disposition:** **PASS**

The narrow correction resolves the prior BLOCK without changing the accepted
repair scope.

- `reconcile._request_observation` now marks unresolved `RELAY_READY`,
  `RELAY_UNBOUND`, and `REQUEST_AMBIGUOUS` requests actionable when their
  lifetime is `LIVE`, or `UNKNOWN` while their expiry bucket is not `EXPIRED`.
- Direct reconciliation-plus-notification controls cover both missing creation
  evidence and partial lifetime evidence: each yields `UNKNOWN`, is selected
  before its deadline, and remains visible but is not selected after expiry.
  `test_unknown_request_event_uses_reconciled_actionability_boundary` confirms
  notification honors the reconciled true/false authority bit.
- Answered relay behavior remains nonactionable: `BOUND_EXPIRED` maps to
  `RELAYED_EXPIRED`; current exact bound relays remain answered, never renewed
  authority; and `active_management` treats `BOUND_EXPIRED` as a completed
  review stage only.
- Previously accepted behavior remains intact in the inspected code/tests:
  exact suite lifetime-binding proof requires server/PID/creation/live-process
  agreement; bad binding remains actionable; correlated answered HELP is
  suppressed; historical PID-reuse MCP exits require current lane/session
  correlation; current exit/resource/unbound/expiry positives remain covered.

Verification records **94 focused tests passed** for the correction and **158
passed, 1 skipped** for full discovery.  The prior retained Clean-K no-write
check remains applicable to unchanged lifecycle behavior: exit 0, 20 exact
expired-bound records retained with `manager_actionable:false`, and selected
notification `null`.  No hardware, external agent, watcher, server, or
experiment-evidence work was rerun or changed.

No remaining functional blocker was found.
