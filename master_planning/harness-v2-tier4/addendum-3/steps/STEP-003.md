# STEP-003 - Build and Accept Remaining-Gap Verification Assets

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-003 |
| Objective and independently decidable outcome | Produce DEL-002 assets that encode every SRC-009 gap, its SRC-002 behavior, and baseline-regression oracles independently of DEL-001 implementation |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-002, REQ-016, support for REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017 |
| Global policy and exception references | P01 through P10, P13 through P15 |
| Public compatibility boundary | Test mechanics may change; scenario, trigger, expected behavior, oracle strength, coverage mapping, and protected production scope invalidate acceptance when changed |

## Activation, inputs, and protected boundaries

EDGE-002 activates from the same accepted target base and frozen interpretation set as STEP-002. LANE-VERIFY-ASSETS may write only the independent acceptance-test, crash/concurrency fixture, platform-runner, and disposable live-fixture paths declared in M03. It must not modify production source, public policy, expected behavior, locked configuration, existing product branch, or frozen-harness.

## Normal and FAST_LANE_V2 entry flows

### FAST_LANE_V2 — canonical usage

Every STEP MUST contain both complete FAST_LANE_V2 rows and their configured, disjoint MI paths. This
is an unconditional plan-construction requirement. The runtime activation conditions below govern
only which configured path executes for a particular event; they can never remove, weaken, relabel,
reason away, or replace required plan content.

Activate `FAST_LANE_V2` only for a compatible set of small, scoped edits with deterministic impact and a
known motivating test. In an affected earlier step, `FAST_LANE_V2_SERIES_1` takes the distinct
`MI-FL2-S1-*` outbound-patch path to make the scoped repair, run only changed-source compile and
motivating tests, independently review and integrate the repaired output, and exit forward to the
current progress-bound step. At that current progress-bound step, `FAST_LANE_V2_SERIES_2` takes the
distinct `MI-FL2-S2-*` inbound-reconcile path to receive all accepted repairs, calculate invalidation,
preserve unaffected PASS credit, run only failed, unresolved, affected, uncertain, or uncredited
checks from the earliest required unit, and then continue normal forward progress. Use these paths to
avoid redoing heavy computations, broad review/test campaigns, or full restarts when their inputs and
PASS credit remain valid; if the activation predicate, deterministic impact, or safe credit reuse cannot be proven,
use R15's normal material classification for that event. That event-level route does not change either
required FAST_LANE_V2 row or its configured contract.

| Entry flow | Status and activation | Consumes | Ordered distinct MI-* path | Produces and exit | Destination or continuation | Checkpoint and invalidation rule | Concrete saved work | Failure/fallback route |
|---|---|---|---|---|---|---|---|---|
| NORMAL | Activates from EDGE-002 | Admitted base, normative claim/oracle matrix, and verification conventions | MI-NORMAL-VERIFY-ASSETS, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-ASSET-VERDICT | Accepted DEL-002 tip or one classified route | EDGE-004 on acceptance | Preserve asset PASS only while scenario, oracle, test source, runner, configuration, and environment remain unchanged | Original full independent-asset path; no fast-lane claim | LOOP-ASSETS for admitted strict test-only correction or exact product-finding handoff |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic DEL-002 asset correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-ASSET-PATCH, MI-FL2-S1-ASSET-REVIEW, MI-FL2-S1-ASSET-INTEGRATE | Accepted repaired DEL-002 asset output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids reconstructing the complete oracle matrix and rerunning the broad asset campaign | If semantics, impact, or rigor is uncertain—or any fast result fails—use NORMAL asset correction and campaign |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-003 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-ASSET-RECONCILE, MI-FL2-S2-ASSET-VERDICT | Updated DEL-002 checkpoint and accepted asset output or classified route | Return to the normal successor EDGE-004 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a full asset discovery and oracle-review restart | If reconciliation is indeterminate or remaining checks fail, return to NORMAL M05 classification without replaying unaffected assets |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-VERIFY-ASSETS | M03 | Admitted base and normative claim/oracle matrix | Reviewable independent asset tip | EDGE-002 |
| 2 | MI-NORMAL-ASSET-CAMPAIGN | M04 | Frozen reviewable asset tip | Complete oracle review/discovery pool | Asset handoff validates |
| 3 | MI-NORMAL-ASSET-VERDICT | M05 | Asset tip and complete campaign pool | Accepted DEL-002 tip or classified correction route | Campaign join completes |
| 4 | MI-FL2-S1-ASSET-PATCH | M03 | Complete scoped asset finding pool and accepted oracle contract | Repaired asset tip plus compile/discovery and motivating-test smoke | Series 1 guard passes |
| 5 | MI-FL2-S1-ASSET-REVIEW | M04 | Frozen repaired asset tip and smoke | Independent oracle review result | Series 1 patch publishes |
| 6 | MI-FL2-S1-ASSET-INTEGRATE | M06 | Reviewed repaired asset tip | Integrated repaired DEL-002 output and change map | Series 1 review passes |
| 7 | MI-FL2-S2-ASSET-RECONCILE | M04 | Accepted Series 1 exits and asset checkpoint | Complete affected-only asset result pool | STEP-003 is current progress bound |
| 8 | MI-FL2-S2-ASSET-VERDICT | M05 | Reconciled asset pool and preserved credit | Accepted updated DEL-002 output or classified route | Series 2 affected checks finish |

## Public outputs and successors

Acceptance publishes RESULT-ASSET-ACCEPTANCE for JOIN-001 and activates EDGE-004. A proven strict test-only defect returns to the same verification logical task under a new card and reruns only affected asset IDs. A discovered product defect is handed to ROOT for product classification; this step never edits DEL-001.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-ASSETS / LOOP-ASSETS | PRODUCT | One frozen DEL-002 tip | Whether independent verification capability faithfully proves the normative product claims | MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-ASSET-VERDICT | Scenario/oracle/coverage integrity of one acceptance asset set | Blocks only DEL-002 and consumers requiring its product-proof capability | only a failed or genuinely undecidable required product criterion may continue LOOP-ASSETS | EDGE-004 advances the accepted asset tip | MI-NORMAL-VERIFY-ASSETS same logical task and role for proven strict test-only faults; product findings return to ROOT | One oracle review and discovery pool avoids fragmented test repair | One verification writer owns the shared asset set without production authority | Preserve unaffected asset PASS by scenario and runner input map | Split only when assets require disjoint scenario owners; merge compatible test-only faults |

## Failure, continuation, and preserved results

All feasible review and discovery work completes. M05 distinguishes a product defect, strict test-only defect, and administrative runner fault. Only a proven semantic-preserving test correction returns here; any oracle ambiguity returns to ROOT. Continuation begins at the earliest affected asset/check.

## Concurrency, isolation, resources, and lifecycle

LANE-VERIFY-ASSETS is the only asset writer. Review and checker members use separate revision-pinned worktrees and result roots and launch together. STEP-003 overlaps STEP-002 but their write surfaces never overlap. ROOT retires review lanes after verdict and retains the asset tip through integration.

## Cost and critical-path effect

One asset writer avoids competing oracle definitions. It overlaps the larger product implementation, so its main critical-path risk is delayed JOIN-001 only when oracle ambiguity or product discoveries require ROOT classification.
