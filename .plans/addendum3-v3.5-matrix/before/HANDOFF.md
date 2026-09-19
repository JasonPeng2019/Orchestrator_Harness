# Harness v2 Addendum 3 execution handoff

## Objective

Complete `goal.md` through EDGE-007 under Addendum 3 version
`3.4-addendum-3-functional-coverage-audit`. STEP-001 through STEP-005 remain
accepted; STEP-006 is active. The latest human-intervention runtime checkpoint
remains **18h13m38s**.

## Status

MI-FL2-S2-LIVE-READINESS is complete and accepted by decision579. The Series 9
practical-control bundle remains frozen at
`a5287f926b6e16d1e131791ac512d096edf06c6706a7d298be171312e1892c72`
(18 assets; exactly three changed from Series 8). The exact changed-input map
selects 12 failed rows and preserves the other 84 rows. The next module is
MI-FL2-S2-LIVE-RECONCILE. No writer, reviewer, integrator, checker, provider, target,
validator, observer, or resource-claim process remains active.

## Completed

- The VERIFICATION_WRITER implemented the four decision555 control corrections:
  durable CHECK11 native-session readiness, managed CHECK8 exact sixth-provider
  containment, Codex plain `-NoProfile -Command` transcript parsing, and cleanup
  fixture restoration before public force-stop.
- ROOT rejected the initial result because it searched `Path.home()/.codex` and
  `Path.home()/.qwen`, while admitted live runs use direct `CODEX_HOME` and
  `QWEN_HOME` roots. P02 same-thread correction 1 fixed the contract without
  changing the other three mechanisms.
- The corrected helper reads only `CODEX_HOME/sessions|archived_sessions` and
  `QWEN_HOME/projects/*/chats`; missing, blank, malformed, wrong-name, and
  mismatched stores fail closed. There is no user-profile fallback.
- ROOT audit562 passed 15 checks and accepted the correction in decision563.
  Both Series 9 watcher events were acknowledged only after their respective
  handling and audit.
- The mapped independent REVIEWER recomputed both complete inventories, examined
  all four corrected mechanisms and their regressions, and returned PASS with no
  material findings. Two missing-result corrections were output-publication
  recovery only; ROOT audit568 confirmed one substantive review, zero rereviews,
  and accepted the review in decision569.
- The mapped INTEGRATOR copied all 18 reviewed assets byte-for-byte, retained the
  Series 8 rollback inventory, ran exactly the six focused tests and three-file
  compile, and did not repeat the 983-check validator or launch live targets.
- ROOT audit573 passed 22 checks. It independently proved the exact bundle and
  three-file delta, a 96-row changed-input map with exactly 12 selected FAIL rows,
  and byte-for-byte preservation of the other 84 ledger rows (66 PASS / 18 FAIL).
  Decision574 accepted integration and the watcher event was acknowledged only
  after the audit.
- The mapped CHECKER audited the version-3.4 six-family readiness floor without
  rerunning tests, validators, compilation, providers, hooks, or targets. It bound
  changed CHECK8/CHECK11 assertions to the accepted Series 9 evidence and kept
  all native behavior for M09.
- ROOT audit578 passed 24 checks: exact bundles and input hashes, exact lossless
  12/84 row partition, all six readiness families, changed mechanism bindings,
  clean Git, no bytecode, and no real effect. Decision579 accepted readiness and
  the watcher event was acknowledged after audit.

## Verification

- Worker full validator: exit 0, terminal JSON PASS, 983 checks; its focused
  repair child ran 36 tests in 129.198s.
- ROOT focused audit: six CHECK8/CHECK11 tests passed in 0.124s; three changed
  files compiled; an extant Codex rollout and Qwen chat were accepted by exact
  session ID while mismatched IDs were refused.
- Integration focused tests passed 6/6 in 0.130s; the three changed files
  compiled. The full validator result was reused rather than replayed.
- Integration controller and Codex identities 51640/7276 are absent, the exact
  resource claim is released, the worktree is tracked-clean, and no live target
  was launched.
- Readiness controller and Codex identities 14636/55040 are absent, the exact
  claim is released, the readiness worktree is tracked-clean, and the checker
  executed zero tests and zero providers.

## Remaining

1. Recheck current target state, recorded authorization, and the mapped
   PRACTICAL_EXECUTOR/PRACTICAL_OBSERVER launch bindings.
2. Run the affected Series 9 Windows set only: four CHECK8, four CHECK11, and
   four dependent CHECK16 rows. Preserve the other 84 coordinate
   classifications and existing support holds.

## Important assumptions

- Candidate `cb01e41533b337d3dd344b89313f1c9062ee69f8`, frozen control plane
  `b8e1f7769d9fdc5a693151a0067522e07fc2ab40`, and Series 8 seed bundle
  `924f3d8a467e934f01a22fbe812ddca70df4ca144e0074f0786e82e740cb0a20`
  remain fixed.
- Product source, scenario meanings, oracle strength, six invalid shapes,
  public cleanup, all 66 PASS rows, raw failures, and recorded tolerance scope
  are protected. Any change to them leaves the fast lane.
- Native macOS/Linux gaps remain nonblocking under BOUND-014.

## Relevant files

- `goal.md`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-LIVE-SERIES9-PATCH-COMPLETE-563.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES9-PATCH-ROOT-AUDIT-562.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-LIVE-SERIES9-REVIEW-COMPLETE-569.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES9-REVIEW-ROOT-AUDIT-568.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-LIVE-SERIES9-INTEGRATION-COMPLETE-574.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES9-INTEGRATION-ROOT-AUDIT-573.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-LIVE-SERIES9-READINESS-PASS-579.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES9-READINESS-ROOT-AUDIT-578.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES9-PATCH-INITIAL-ROOT-AUDIT-559.json`
- `w/addendum-3-epoch-001/live-control-series9-patch-27/.agent-workspace/HANDOFF-FL2-S1-LIVE-SERIES9-27.json`
- `w/addendum-3-epoch-001/live-control-series9-integrate-29/.agent-workspace/HANDOFF-FL2-S1-LIVE-INTEGRATE-SERIES9-29.json`
- `w/addendum-3-epoch-001/live-control-series9-integrate-29/.agent-workspace/changed-input-map-series9-29.json`
- `w/addendum-3-epoch-001/live-control-series9-integrate-29/.agent-workspace/live-matrix/`
- `w/addendum-3-epoch-001/live-readiness-series9-affected-30/.agent-workspace/HANDOFF-FL2-S2-LIVE-READINESS-SERIES9-AFFECTED-30.json`
- `w/addendum-3-epoch-001/live-readiness-series9-affected-30/.agent-workspace/coverage-audit-series9-30.json`
- `master_planning/harness-v2-tier4/addendum-3/modules/M04.md`
- `master_planning/harness-v2-tier4/addendum-3/steps/STEP-006.md`

## Next action

Reread M09 and the Series 2 reconcile contract, verify current Windows target,
provider authorization and mapped executor/observer identities, then launch only
the 12 affected Codex/Qwen CHECK8/CHECK11/CHECK16 rows through frozen-harness.
