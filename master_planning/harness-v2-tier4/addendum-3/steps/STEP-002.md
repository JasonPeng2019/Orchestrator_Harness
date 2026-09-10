# STEP-002 - Implement and Accept the Remaining Product Gaps

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-002 |
| Objective and independently decidable outcome | Produce one coherent DEL-001 tip that closes every marked implementation gap in REQ-001 through REQ-015 while preserving the accepted baseline |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-001, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, OUT-001 |
| Global policy and exception references | P01 through P11, P13 through P15 |
| Public compatibility boundary | Internal implementation may change only where a marked gap or its shared invariant requires it; any unplanned change to accepted CLI, record, lifecycle, profile, adapter, portability, or documentation behavior invalidates this output |

## Activation, inputs, and protected boundaries

EDGE-001 activates this step with the admitted `f4328b177177a3aa71bf5f064b88ad6033b3d903` base, SRC-002 behavior contract, SRC-009 gap inventory, and BOUND-009 through BOUND-019. LANE-PRODUCT alone may mutate DEL-001 production, shipped-asset, packaging, and operator-document paths needed by those gaps. Independent acceptance-asset paths owned by STEP-003, frozen-harness, credentials, unrelated outer-workspace content, and external state are protected.

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
| NORMAL | Activates from EDGE-001 | Accepted base, DEL-001 gap contract, frozen interpretations, failure brief, and target truth | MI-NORMAL-PRODUCT, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-PRODUCT-VERDICT | Accepted baseline-preserving DEL-001 tip or one classified route | EDGE-003 on acceptance | Preserve prior and new self-check/campaign PASS only while their source, runner, configuration, environment, and contract inputs remain unchanged | Original full addendum product path; no fast-lane claim | LOOP-PRODUCT for a failed or undecidable required product criterion; otherwise exact incomplete/support route |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic DEL-001 product correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-PRODUCT-PATCH, MI-FL2-S1-PRODUCT-REVIEW, MI-FL2-S1-PRODUCT-INTEGRATE | Accepted repaired DEL-001 product output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids replaying the broad DEL-001 implementation and full product campaign | If scope, impact, test, or credit is uncertain—or any fast result fails—use NORMAL material repair and affected campaign |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-002 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-PRODUCT-RECONCILE, MI-FL2-S2-PRODUCT-VERDICT | Updated DEL-001 checkpoint and accepted product output or classified route | Return to the normal successor EDGE-003 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a full product implementation and broad campaign restart | If reconciliation is indeterminate or remaining checks fail, route through NORMAL M05 classification without replaying unaffected work |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-PRODUCT | M02 | Accepted target base, SRC-009 gap inventory, BOUND-009 through BOUND-019, and DEL-001 contract | Reviewable gap-closing DEL-001 tip and producer self-checks | EDGE-001 |
| 2 | MI-NORMAL-PRODUCT-CAMPAIGN | M04 | Frozen reviewable DEL-001 tip | Complete product review/check pool | Product handoff validates |
| 3 | MI-NORMAL-PRODUCT-VERDICT | M05 | Product tip and complete campaign pool | Accepted DEL-001 tip or classified correction route | Campaign join completes |
| 4 | MI-FL2-S1-PRODUCT-PATCH | M02 | Complete scoped product finding pool and accepted baseline | Repaired product tip plus compile and motivating-test smoke | Series 1 guard passes |
| 5 | MI-FL2-S1-PRODUCT-REVIEW | M04 | Frozen repaired product tip and smoke | Independent affected review result | Series 1 patch publishes |
| 6 | MI-FL2-S1-PRODUCT-INTEGRATE | M06 | Reviewed repaired product tip | Integrated repaired DEL-001 output and change map | Series 1 review passes |
| 7 | MI-FL2-S2-PRODUCT-RECONCILE | M04 | Accepted Series 1 exits and product checkpoint | Complete affected-only result pool | STEP-002 is current progress bound |
| 8 | MI-FL2-S2-PRODUCT-VERDICT | M05 | Reconciled product result pool and preserved credit | Accepted updated DEL-001 output or classified route | Series 2 affected checks finish |

## Public outputs and successors

Acceptance publishes RESULT-PRODUCT-ACCEPTANCE for JOIN-001 and activates EDGE-003. A material return goes to the same MI-NORMAL-PRODUCT logical task through a new ROOT card, then through the affected product campaign. Strict test-only and administrative faults follow P08 and P09 and cannot silently alter production behavior.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-PRODUCT / LOOP-PRODUCT | PRODUCT | One frozen addendum DEL-001 tip | Whether every SRC-009 gap in REQ-001 through REQ-015 is closed and accepted baseline behavior remains intact | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-PRODUCT-VERDICT | One coupled record, queue, lifecycle, CLI, and provider-boundary state machine | Blocks only DEL-001 and consumers requiring its product behavior | only a failed or genuinely undecidable required product criterion may continue LOOP-PRODUCT | EDGE-003 advances the accepted tip | MI-NORMAL-PRODUCT same logical task and role after ROOT authors the pooled repair card | One campaign and one pooled repair avoid repeated broad context and review | One product writer can repair the shared state machine coherently; incompatible asset faults split to STEP-003 | Preserve baseline and addendum PASS credit by declared input map | Split prospectively if findings require independent product criteria or source owners; merge only compatible material findings |

## Failure, continuation, and preserved results

All campaign members finish feasible work before M05 classification. Material findings batch once; strict test-only findings route to STEP-003 only when its semantic-preserving eligibility is proven; administrative faults block only their consumer. A repair starts from the earliest affected action/check and preserves unchanged PASS credit.

## Concurrency, isolation, resources, and lifecycle

LANE-PRODUCT is the only source writer. Its M04 review and check members use two revision-pinned read-only worktrees with disjoint result/cache roots and launch together. Runtime lane, invocation, process-tree, handoff, and worktree IDs come from Section 10 and frozen-harness records. ROOT retires review lanes after the verdict and the product lane after integration preserves its tip.

## Cost and critical-path effect

This is the likely longest construction step because the remaining gaps cross tightly coupled public state. It overlaps STEP-003 only where the verification writer's paths are disjoint. One serial writer and one two-member checking wave minimize merge risk while retaining independent judgment.
