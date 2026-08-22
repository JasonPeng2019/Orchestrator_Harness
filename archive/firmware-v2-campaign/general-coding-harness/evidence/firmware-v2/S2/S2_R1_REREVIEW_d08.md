# S2.R1 superseding repaired-tip rereview — FAIL

Reviewed candidate: `d08b6ccf3d2e0eacd3686b01658645249dfcc0a0` on `firmware/v2-s2-r1`.
I read the refreshed governing-input observation record, full repair diff, original R1 review,
S2 triage evidence, current acceptance kit, and pinned MCP source at `f003f84…`. No tests,
MCP, pyOCD, serial interface, or hardware were run.

## Recheck outcome

- Resolved: legacy MCP names were replaced with guarded names; the manifest now contains four
  datasheets, fixture identity, and toolchain hashes; seed creation is confined/create-new; lane
  configuration declares per-lane roots and controller ownership; the chain requires all named
  stages; and RF checks include bandwidth, coding-rate, and spreading-factor limits.
- Residual accepted gaps: the three reproducible findings in `FINDINGS.json` remain.

## Residual evidence

1. `MCP_METHOD_POLICY.json:9` claims `read_memory_address(board_id,address,size)`, but the pinned
   registered handler accepts `board_id,address,width,length` at
   `src/pyocd_debug_mcp/tools/memory.py:475-480`. The evaluator rejects fields omitted by policy
   (`firmware_acceptance/kit.py:254-256`), so `width` is denied and `size` is invalid at MCP.

2. `AcceptanceBroker.admit()` compares only limited identity keys (`kit.py:209-211`) and verifies a
   signature over the proposal alone (`:212-214`); it never compares method, normalized arguments,
   policy, plan, permission, authorization, or admission fields across the artifacts.
   `evaluate_call()` accepts free-standing hashes and caller-created permission/RF objects
   (`:230-266`). `validate_manifest()` only type-checks stated identities (`:70-79`), while
   `controller_config()` only checks that the pinned-server directory exists (`:160-162`).

3. The coding gate validates `FINDINGS.json` only when the invocation voluntarily supplies
   `finding_gate` (`orchestrator_harness/lane_controller.py:419-429`, `:604-610`). No production
   path invokes `validate_finding_triage`; its callers are only its unit test
   (`orchestrator_harness/tests/test_finding_gate.py:44-58`). Thus the target contract's
   `manager_triage_required: true` (`firmware_acceptance/seed/TEST_CONTRACT.json:1`) is not a
   fail-closed manager completion boundary.

## Rejected criticisms

- No speculative MCP-server edit is hidden: the repair diff changes no MCP-server source and the
  pin remains `f003f84…`.
- The opt-in coding gate itself is appropriate for backward compatibility; only the missing
  project-specific manager-triage enforcement is a finding.
- The former target-root/reparse concern is resolved by `kit.py:118-150`.
- No evidence indicates physical mutation by this review or a hidden MCP launch.
