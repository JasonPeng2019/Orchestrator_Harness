# S2.R2 final targeted rereview — PASS

Reviewed only `d08b6ccf3d2e0eacd3686b01658645249dfcc0a0..66e053a3822a7769590266f977c266f33a520ed5`,
read-only, without tests, MCP, or hardware access. The previously accepted S2.R2 risks are resolved
within the requested compact acceptance-kit scope.

## Resolved risks

- The seed now carries exactly the five expected seed files, and validation consumes a closed
  18-entry per-ID campaign contract. It requires the exact gating IDs, a closed definition shape,
  nonempty dependency inputs, the canonical fingerprint algorithm, one of the three exact failure
  routes, and the passed-registry/rerun contract ([kit.py:69-99](../firmware_acceptance/kit.py#L69-L99)).
  The stored contract supplies all 18 selected entries; its explicitly excluded work remains
  non-gating ([TEST_CONTRACT.json:1](../firmware_acceptance/seed/TEST_CONTRACT.json#L1)).
- The evidence schema is closed at its top level and for provenance, oracle shape, and chain item
  records; stable test IDs and the three failure routes are constrained
  ([EVIDENCE_SCHEMA.json:1](../firmware_acceptance/seed/EVIDENCE_SCHEMA.json#L1)).
- The materialized target retains an initial seed commit identity and validates every seed blob
  against that original commit before use ([kit.py:172-213](../firmware_acceptance/kit.py#L172-L213)).
  It intentionally validates only the seed files: target-created application, test, and build
  content can live elsewhere in the disposable target tree and is not rejected. This is the
  requested seed-integrity boundary, not a whole-target immutability requirement.
- Opt-in child isolation is now applied to the actual `Popen` call, with a positive allowlist and
  physical-capability-prefix removal ([lane_controller.py:87-96](../orchestrator_harness/lane_controller.py#L87-L96),
  [lane_controller.py:773-778](../orchestrator_harness/lane_controller.py#L773-L778)). Its declared
  project-worker template records the same boundary ([LANE_TEMPLATES.json:1](../firmware_acceptance/LANE_TEMPLATES.json#L1)).
- Bound operation authority, pinned-server commit/cleanliness, and immutable-chain admission are
  checked narrowly rather than by adding a scheduler or hardware platform
  ([kit.py:36-66](../firmware_acceptance/kit.py#L36-L66), [kit.py:256-296](../firmware_acceptance/kit.py#L256-L296)).

## Scope confirmation

No finding is accepted. In particular, I reject reopening the prior pre-result manager-triage
proposal: `validate_finding_triage` remains a standalone validator and is not wired into the
pre-result path, matching the explicit direction not to implement it. I also reject requests for
a framework/scheduler, whole-target immutability, live hardware/MCP, manual oracles, or polish;
none is necessary to resolve the dependency-invalidated R2 risks.
