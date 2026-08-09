# S2.R1 final targeted rereview — FAIL

Reviewed only `d08b6ccf3d2e0eacd3686b01658645249dfcc0a0..66e053a3822a7769590266f977c266f33a520ed5` at candidate `66e053a3822a7769590266f977c266f33a520ed5`. No tests, MCP, pyOCD, serial access, or hardware were run.

## Targeted recheck

- **Read-memory signature/bounds:** resolved. The policy now uses `width` and `length`
  (`firmware_acceptance/MCP_METHOD_POLICY.json:10`) matching the pinned handler signature
  (`src/pyocd_debug_mcp/tools/memory.py:475-480`); the policy narrows the server's positive-length
  surface with explicit allowed widths and a maximum, which is a fail-closed policy restriction.
- **Clean server and canonical operation continuity:** partially resolved. `validate_pinned_server()`
  now verifies the exact clean Git revision (`firmware_acceptance/kit.py:36-44`) and the same bound
  operation/hash is required in each stage (`:247-280`).  However, its claimed
  `raw_result_sha256` is never checked against the raw-result record bytes, so a fabricated hash can
  survive the full chain. This remains an accepted finding in `FINDINGS.json`.
- **Opt-in child environment isolation:** resolved. The controller creates an allowlisted environment
  after removing physical capability prefixes (`orchestrator_harness/lane_controller.py:87-96`) and
  passes it directly to the launched child when the opt-in field is true (`:773-778`). The project
  target-worker template opts in (`firmware_acceptance/LANE_TEMPLATES.json:1`).
- **Rejected pre-result manager-triage proposal:** not implemented by this repair; no new finding was
  opened for it, as directed.

The pinned MCP worktree remains clean at `f003f84a7df51cd8595a3203c62e225b21da2a22`; no speculative
server edit or physical mutation is evidenced by this diff.
