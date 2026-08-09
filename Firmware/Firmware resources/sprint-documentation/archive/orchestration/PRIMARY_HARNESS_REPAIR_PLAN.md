# Primary harness lane-identity and review-cadence repair plan

Created: `2026-07-31T14:38Z`  
Owner: main orchestrator  
Failed canary attempt: `20260731-long-canary-sprint-1` (counter remains `0/3`)

## Verified defects

1. The success contract requires each live HIL lane to be manager-reviewed at least every three
   minutes, but the active config uses `manager_review_interval_seconds: 300`. The manager also
   failed to durably log every manual inspection.
2. A checkpointed, exited A22 lane generated `LANE_NO_PROGRESS` because its declared MCP server
   remained `MCP_STATE_UNKNOWN`. The run had exact cleanup evidence, but no canonical correlated
   `mcp-lifetime.json` record was discoverable.
3. Code query proved a deeper identity mismatch: controller status carries the manager-assigned
   `declared_lane_id`, and helper/request records use it, but `reconcile._lane_id` ignores it and
   synthesizes `<run>:<doer>:<task>`. Therefore explicitly scoped request/MCP records can never
   correlate to their controller lane even though `_record_belongs_to_lane` declares explicit lane
   identity authoritative.

## Accepted decisions

- Make `_lane_id` prefer a nonempty controller `declared_lane_id`; retain the synthesized ID only
  as backward-compatible fallback when no explicit ID exists.
- Keep unknown-MCP fail-closed behavior. Do not mark a declared MCP absent without exact PID and
  creation-time evidence.
- Use the existing recognized `mcp-lifetime.json` record contract. Each HIL helper must write it
  atomically under its unique phase runtime before first board operation, with exact server name,
  manager-assigned lane ID, persistent session ID, MCP PID, and creation time. Cleanup leaves the
  immutable record; complete process observation then reconciles the exact PID as absent/mismatched.
- Change the active canary manager review interval to `180` seconds. The main manager must also
  append one durable per-lane inspection record on every active-HIL supervision pass; configuration
  alone is not proof.

## Implementation and verification

1. Update `_lane_id` and focused reconciliation tests:
   - explicit controller lane ID becomes the public lane ID;
   - a matching explicit terminal MCP record correlates and permits release for an exited checkpoint;
   - an explicit mismatch or missing record remains unknown/fail-closed.
2. Add an active-management regression proving an exited checkpointed lane with correlated
   `MCP_EXITED` evidence is not active and emits no `LANE_NO_PROGRESS`; preserve the unknown-MCP
   warning case.
3. Set this epoch's review interval to 180 seconds and add a focused configuration assertion.
4. Run compile, focused reconciliation/active-manager tests, and the ordinary primary harness host
   suite (exclude real-agent/WSL tests).
5. The manager reconstructs canonical lifetime records only from retained exact process and cleanup
   evidence for the completed A22/A24/D31 boundaries, then scans with the repaired harness and proves
   release/absence without weakening safety.
6. Restart exactly one primary harness and one optional watcher, close historical alert lifecycles,
   and begin a fresh clean success sprint from preserved checkpoints.

## Non-goals

Do not change server code, experiment results, hardware state, unknown-process safety, alert
severity, or restart completed work. Do not infer absence from checkpoint prose alone.
