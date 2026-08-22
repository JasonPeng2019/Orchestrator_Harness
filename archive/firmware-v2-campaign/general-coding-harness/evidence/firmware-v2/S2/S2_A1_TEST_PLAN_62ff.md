# S2.A1 host/MCP/isolation test plan

## Overlap audit

Reviewed `test_firmware_acceptance_kit.py`, route/lifecycle compatibility tests, the accepted `firmware_acceptance.kit` public validators, lane templates, and S2.CA/S2.JR contract material. Existing assertions covered basic ambient-capability rejection, worker environment blanks, policy bounds, stage ordering, and raw-result digest binding. They did not exercise a clean pinned Git worktree through `AcceptanceBroker.controller_config`, its resulting controller-only stdio/root/environment contract, or validly rehashed immutable-operation drift across a complete chain.

## Requirement mapping

| Stable ID | Requirements | Public path | Dependency fingerprint inputs |
|---|---|---|---|
| S2_A1_001 | S2; C4-C8; C31-C42; C49; C59; C65-C66 | `AcceptanceBroker.controller_config` / `validate_pinned_server` | `firmware_acceptance/kit.py`, `LANE_TEMPLATES.json`, `ACCEPTANCE_MANIFEST.json`, synthetic clean/dirty Git worktree, temporary corrected seed fixture |
| S2_A1_002 | S2; C31-C42; C49; C59; C65-C66 | `AcceptanceBroker.record` / `AcceptanceBroker.admit` | `firmware_acceptance/kit.py`, `MCP_METHOD_POLICY.json`, `LANE_TEMPLATES.json`, `ACCEPTANCE_MANIFEST.json`, temporary corrected seed fixture, synthetic immutable evidence chain |

The temporary fixture recalculates only its copied seed manifest so host-path tests remain scoped to their stated dependencies. The accepted checked-in seed itself is independently invalid and is recorded in `FINDINGS.json`.

## Execution

Executed only the owned module:

`python -m unittest orchestrator_harness.tests.test_firmware_acceptance_host -v`

Passed stable IDs: `S2_A1_001`, `S2_A1_002`.
