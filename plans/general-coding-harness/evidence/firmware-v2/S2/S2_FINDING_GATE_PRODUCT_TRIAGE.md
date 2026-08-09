# S2 finding-gate product triage

- Reviewed product result: schema-valid PASS at
  `3bb6f999fbb2399bdab361999d32ac6725282831`.
- Decision owner: `ROOT-IM`.
- Decision: result not yet accepted; preserve the two finding-gate commits and continue the same
  S2.P thread with a targeted repair.

## Accepted finding FG-PRODUCT-001

- Category: `FUNCTIONALITY_BREAKING`.
- Affected contract: the user-required rule that every project-created reviewer, test writer, and
  test executor is actually gated, plus C68/C72.
- Evidence: `firmware_acceptance/LANE_TEMPLATES.json` at `3bb6f99` contains only physical-board lane
  templates and no `finding_gate`; the five-file seed contract likewise has no mandatory findings or
  triage artifact; there is no manager-triage validator/API. The new optional controller field is
  therefore not enabled by the project that requires it.
- Observed versus expected: a reviewer/tester invocation can still complete without `FINDINGS.json`;
  the governing contract requires that project-created review/test lanes fail closed without it.
- No-fix consequence: inadmissible or net-negative review suggestions could still reach triage and
  trigger unnecessary complexity, regression risk, and retesting.
- Smallest sufficient fix: add closed review/test invocation templates, seed evidence/test-contract
  bindings, a narrow manager-triage validator, and focused integration/negative tests. Do not alter
  default coding behavior or physical board templates.
- Complexity/regression/verification cost: low and confined to additive plan-specific templates,
  one pure validator, seed-hash refresh, and focused unit tests.
- Benefit: makes the user-required safeguard operative and auditable before C1/C3.
- Alternatives: prompt-only enforcement is lower effort but not fail-closed and was explicitly
  rejected by the user; making the gate global would add unnecessary compatibility risk.
- Cost-benefit decision: `PROBLEM_OUTWEIGHS_FIX_RISK`; the bounded additive repair is worth doing.

## Rejected/non-finding scope

No numeric scoring engine, generalized review framework, scheduler, global mandatory behavior,
style cleanup, or unrelated validator refactor is justified. These would add more complexity and
risk than their benefit.

## Accepted finding FG-PRODUCT-002

- Category: `FUNCTIONALITY_BREAKING`.
- Evidence: at `b12c360`, `validate_finding_triage` compares two caller-supplied path/hash values but
  does not safely read and hash the referenced findings file; decision objects also accept unknown
  keys and unbounded rationales/IDs.
- Impact/no-fix consequence: stale, substituted, or padded manager-triage evidence could validate,
  so the gate would not prove the exact submission was independently decided.
- Smallest sufficient fix: safely read/hash the exact regular findings path, close/bound ACCEPT and
  REJECT decision shapes, and add compact negative coverage for hash substitution and decision
  coverage/shape. No framework or scoring.
- Complexity/regression/verification cost: low; one pure validator and focused subtests.
- Cost-benefit decision: `PROBLEM_OUTWEIGHS_FIX_RISK`.
