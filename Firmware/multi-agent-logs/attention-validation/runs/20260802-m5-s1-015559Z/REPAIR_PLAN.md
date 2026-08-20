# Repair plan — managed-harness blocking-wait ownership

## Verified defect

In the first fresh M5 pre-worker quiet control, one managed harness already owned the output root and
committed the authoritative scan chain. A separate `watch --until-actionable` invocation found no
pending notification, performed and committed its own scan, and correctly failed with `prior
committed scan process identity changed`. This makes the M5-prescribed production topology
(managed scanner plus blocking manager consumer) unusable.

## Smallest repair

1. When a live managed watcher owns the output root, `watch_until_actionable` must become a
   read-only consumer of that owner's durable notification state. It must poll only the notification
   state until an exact pending actionable event exists or the bounded timeout expires. It must not
   observe runs, commit a scan, advance the scan chain/cursor, select events, acknowledge anything,
   or mutate notification state.
2. On an exact pending event, retain the existing stdout wake attempt/delivered-or-failed logging
   and return payload. On quiet timeout, retain `WATCH_TIMEOUT` with no wake ID/attempt/outcome.
3. Fail closed if managed runtime/owner identity is stale, absent, stopped, restarted, expired, or
   contradictory. Preserve the existing standalone `--until-actionable` scan path when no managed
   runtime exists.
4. Add focused tests for: quiet managed consumer; later pending delivery; no scan/cursor/state
   mutation; stale/dead managed owner; and unchanged standalone behavior.
5. Run the full harness/watcher suites, Pyright/compileall, independent review, Luna practical smoke
   using a real managed process plus separate blocking process, then rerun M4 readiness. This is a
   pre-count RESET, so the accepted counter remains 0/3.

## Accepted post-sprint review amendment

The fresh result reviewer found a second directly evidenced pre-count defect: the diagnostic
watcher recorded `PRIMARY_HARNESS_LOST: identity-incomplete` because the M5 owner writer published
`owner` + `watcher`, while the watcher health reader requires `owner` + `managed_owner` +
`managed_watcher`. The root accepts this finding. Align the two sides on one smallest canonical
identity contract, test healthy/absent/mismatched cases, and include this surface in review, Luna
smoke, full suites, and M4. Also prove the managed blocking consumer preserves notification,
scan-chain, cursor, and snapshot bytes while returning the exact durable pending event/wake IDs.

## Exclusions

No queue redesign, wake bridge, watcher change, retry framework, manager concurrency change,
firmware/server change, or relaxation of scan-chain identity.
