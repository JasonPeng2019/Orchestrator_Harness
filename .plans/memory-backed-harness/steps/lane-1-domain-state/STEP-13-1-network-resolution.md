# STEP-13-1 — Resolve truthful network state

This step is a derivative of [original STEP-13](../../source-steps/STEP-13-network-modes-are-enforced.md).

Owner: lane 1. This is the complete network-mode resolution assignment.

Use the existing `src/memory_harness/config.py` resolved configuration; lane 2 applies provider/tool settings in the installed launch payload, and lanes 3/4 enforce service entry gates.

Resolve requested mode, effective mode, and enforcement source before an objective, retaining configuration attribution. The supported profiles are soft_guardrail_network, atlas_memory_only, and restricted_local. Do not assert Atlas-only isolation without independent unrelated-destination blocking and launched-payload evidence; downgrade the claim when absent. Restricted-local blocks optional Atlas task-path activity at service entry, including retrieval, telemetry, publication retry, and pending task work. Keep feature-off rules independent and distinguish outage from permission denial.

Lane 2 owns launched provider/tool settings; lanes 3 and 4 own their service entry gates. Evidence: direct config-resolution and forbidden-call tests plus installed-payload inspection.

Resolve the profile before an objective and retain requested mode, effective mode, enforcement source, and captured-configuration attribution through retries. Soft guardrails may suppress supported provider-native general web/fetch/search tools but must disclose remaining shell egress. `atlas_memory_only` is a truthful claim only after independent blocking of unrelated destinations and verification of the actual launched payload; otherwise downgrade, never call same-user process settings a hardened sandbox. `restricted_local` prevents Atlas retrieval, optional telemetry, publication retries, and all optional Atlas task-path work at service entry. Safety administration that lacks reachability remains pending for an authorized environment. Feature Spec Section 15 off rules are separate from network mode; outage is not permission denial. Extend `tests.local.contracts.test_config` with resolution cases and require adapter/launch-payload forbidden-call tests. Only measured egress permits an Atlas-only claim.

For a revisit, repair only the specific mode resolver or consumed enforcement fact and rerun direct resolution and affected forbidden-call checks. Revisit STEP-15/17/18 only where the changed profile was consumed.
