# Clean-F canary repair plan

Authority: root manager  
Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_F.md`  
Verdict: `ACCEPTED_NONCOUNTING`; counter remains `0/3`

## Objective

Make the primary read-only harness observe the request/relay directories actually used by current
suite lanes. Preserve legacy request discovery, exact sidecar/hash checking, historical-signal
filtering, scheduler/relay authority boundaries, and all accepted experiment evidence. Do not edit
the optional watcher, production server, firmware, hardware state, or closed clean-F evidence.

## Validated defect

`orchestrator_harness/discovery.py` scans only each run's
`.agent-workspace/permission-requests`. During clean-F, D31 wrote three live, sidecar-bound requests
under `.agent-workspace/manager-requests` and their exact approved relays under
`.agent-workspace/manager-relays`. The harness retained matching HELP signals but reported
`requests: []` and emitted `RESOURCE_AMBIGUOUS`, so it could not reconcile request lifetime,
deadline, relay, or request-derived resource identity.

## Slice 1 — discover current manager request and relay roots

Change only primary-harness discovery/reconciliation tests and the smallest discovery code needed.

1. Continue scanning legacy `permission-requests` exactly as before, including its existing
   request-vs-relay classification and required sidecar behavior.
2. Also scan `manager-requests/*.json` as requests and `manager-relays/*.json` as relays.
3. For the two current directories, validate a `.sha256` sidecar whenever present. Accept an
   atomically written relay without a sidecar because current manager relays bind the request hash,
   tool/argument hash, lane, snapshot, exact call, and expiry in their content. Do not weaken
   validation of any present sidecar.
4. Keep every discovered path confined to its run workspace, deduplicate by resolved path, and
   preserve observation errors for malformed JSON or invalid sidecars.
5. Do not infer authorization, publish relays, change leases, or add scheduler behavior.

## Focused tests

Add regressions proving:

- a live sidecar-bound `manager-requests` record is discovered and lane-correlated;
- its separate `manager-relays` record is discovered and produces the existing relayed state;
- a manager request with an invalid present sidecar remains an observation error;
- a manager relay without a sidecar is accepted only as an observation and still must pass the
  existing request/relay content binding before it can be `RELAYED`;
- legacy `permission-requests` behavior remains unchanged; and
- the clean-F-shaped D31 case no longer has an empty request set or the false
  "active hardware lane has no current request identity" ambiguity.

Run the focused discovery/reconciliation tests first, then the complete existing primary-harness
host suite once because discovery is a shared core surface. Do not run the optional-watcher suite,
firmware, MCP, provider, or hardware tests for this change.

## Run-local follow-up (owned by persistent lane doers, not the harness coder)

- Boreal/D31: update the run-local helper to follow the explicit accepted
  `board_fix_setup` / load-`board_validate` redirect before validation; add a focused route test.
- Cygnus/A24: derive the server project root from the fresh manager assignment and render launchers
  against the existing root `BYO-Firmware-MCP`, never the nonexistent run-local path; focused-test
  without starting MCP.

These run-local corrections enter the next fresh epoch only after host checks. A22 and A26 remain
at their accepted clean-F preparation boundaries. No clean-F request, relay, PID, runtime, or
closed evidence is reused.
