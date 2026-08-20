# Clean-F repair-epoch notification fix plan

Authority: root manager  
Validated reproduction: `orchestrator_harness/canary-20260731-s1-clean-f-repair-state/pending-notification.json`

## Objective

Prevent closed, expired manager signals from old lane epochs from occupying the durable actionable
notification slot after current `manager-requests` discovery is enabled. Preserve complete
read-only observation, exact live-lane signals, current unexpired unknown-lifetime safety signals,
current live requests, stable event identities, acknowledgement semantics, and all scheduler/relay
authority boundaries.

## Validated defect

The clean-F discovery repair correctly exposed historical `manager-requests`. During the fresh
host-only repair epoch, the primary managed watcher immediately selected old clean-D A24 HELP
signals whose ten-minute deadlines expired more than an hour earlier and whose producer lifetimes
are closed. Acknowledging one selected another expired clean-D signal, delaying the live repair
epoch's review notification.

`notifications._manager_signal_is_live()` treats any exact-lane request with
`lifetime_state == "UNKNOWN"` as current without consulting the request's `expiry_bucket` or
deadline. Before current request discovery, those old records were invisible; after the valid
discovery change, they can incorrectly wake every fresh epoch.

## Narrow implementation

Change only primary notification selection and focused tests.

1. Keep every manager signal in snapshots/events; this is actionability filtering only.
2. An exact currently live/unknown lane remains actionable exactly as today.
3. An exact request makes its signal actionable when:
   - the request lifetime is `LIVE`; or
   - the request lifetime is `UNKNOWN` and the request is not expired.
4. `expiry_bucket == "EXPIRED"` (or an already-past parsed deadline when the bucket is absent)
   must never make a historical signal actionable merely because lifetime identity is unknown.
5. Preserve current unexpired `UNKNOWN` request signals as actionable so uncertain live authority
   remains fail-closed and visible.
6. Do not delete, rewrite, acknowledge, or mutate any signal/request record. Do not change event
   generation, request discovery, active-management cadence, the optional watcher, lane code,
   production server, MCP/provider, or hardware.

## Focused verification

Add regressions proving:

- an expired historical HELP signal with an exact `UNKNOWN` request is retained but not selected;
- acknowledging one expired signal does not expose another expired signal ahead of a live review;
- an exact unexpired `UNKNOWN` request signal remains actionable;
- an exact `LIVE` request signal remains actionable;
- an exact live lane signal remains actionable; and
- historical records still appear in snapshots/events.

Run the focused manager-notification tests first, then the full primary host suite once because
notification selection is shared core. No optional-watcher, firmware, MCP/provider, or hardware
tests are warranted.
