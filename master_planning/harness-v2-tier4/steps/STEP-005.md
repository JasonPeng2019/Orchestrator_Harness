# STEP-005 - Perform Accumulated Static Assurance

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-005 |
| Objective and independently decidable outcome | Decide the complete static v2 product contract on one integrated release unit |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-003 static portion, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, OUT-001, OUT-002 |
| Global policy and exception references | P01 through P11, P13 through P15 |
| Public compatibility boundary | The accepted output is bound to one integrated revision, FINAL_PRODUCT surface, CHECK-U1 through CHECK-U5 input map, and checkpoint; a changed consumed input invalidates only its dependents |

## Activation, inputs, and protected boundaries

EDGE-005 activates with HANDOFF-INTEGRATION and the complete normative requirement set. Review and deterministic assurance are read-only against the same integrated revision with disjoint result/cache roots. No assurance lane may edit product, tests, policy, acceptance, or the integration coordinate.

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
| NORMAL | Activates from EDGE-005 | Integrated revision, accepted input verdicts, requirements, and prior credit | MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-STATIC-VERDICT | Static acceptance and complete checkpoint or classified route | EDGE-006 on acceptance | Run CHECK-U1 through CHECK-U5 on cold entry; later run only failed, unresolved, affected, uncertain, or uncredited units from the earliest required one | Original full assurance path; no fast-lane claim | LOOP-STATIC to the affected product or asset logical task only for failed or undecidable required product criteria |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic assurance correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-ASSURANCE-PATCH, MI-FL2-S1-ASSURANCE-REVIEW, MI-FL2-S1-ASSURANCE-INTEGRATE | Accepted repaired assurance output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids reopening product implementation and replaying the full final audit/safeguard | If oracle meaning, product behavior, or impact changes—or any fast result fails—route to the owning earlier STEP NORMAL path or NORMAL assurance as classified |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-005 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-ASSURANCE-RECONCILE, MI-FL2-S2-ASSURANCE-VERDICT | Updated static checkpoint and acceptance or classified route | Return to the normal successor EDGE-006 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a cold CHECK-U1-through-U5 restart and a repeated whole-product audit when its inputs are unchanged | If invalidation or reuse is uncertain, run NORMAL assurance from the earliest uncertain unit; failures return to NORMAL M05 classification |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-FINAL-ASSURANCE | M07 | Frozen integrated release unit and complete acceptance set | Complete FINAL_PRODUCT review and safeguard pool | EDGE-005 |
| 2 | MI-NORMAL-STATIC-VERDICT | M05 | Final pool, checkpoint, integrated revision, and tolerances | Static acceptance or classified route | Final assurance join completes |
| 3 | MI-FL2-S1-ASSURANCE-PATCH | M03 | Complete scoped assurance-asset pool and fixed oracle contract | Corrected assurance asset plus compile/discovery and motivating-test smoke | Series 1 guard passes |
| 4 | MI-FL2-S1-ASSURANCE-REVIEW | M04 | Frozen corrected assurance asset and smoke | Independent review result | Series 1 patch publishes |
| 5 | MI-FL2-S1-ASSURANCE-INTEGRATE | M06 | Reviewed corrected assurance asset | Integrated correction and change map | Series 1 review passes |
| 6 | MI-FL2-S2-ASSURANCE-RECONCILE | M07 | Accepted Series 1 exits and final checkpoint | Complete affected-only assurance pool | STEP-005 is current progress bound |
| 7 | MI-FL2-S2-ASSURANCE-VERDICT | M05 | Reconciled final pool and preserved credit | Static acceptance or classified route | Series 2 remaining assurance finishes |

## Public outputs and successors

RESULT-STATIC-ACCEPTANCE activates STEP-006 through EDGE-006. A material product finding returns through the owning M02 task, affected M04 campaign, reintegration, and only invalidated M07 units. A strict test-only finding returns through the owning M03 task and affected units. Support faults hold only claims that cannot otherwise be decided.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-STATIC / LOOP-STATIC | PRODUCT | One integrated release revision | Whether the whole static v2 behavior, contract, portability, packaging, and usability set is satisfied | MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-STATIC-VERDICT | Cross-deliverable release correctness under one normative specification | Blocks only the static release outcome and consumers requiring it | only a failed or genuinely undecidable required product criterion may continue LOOP-STATIC | EDGE-006 advances the static acceptance | Affected MI-NORMAL-PRODUCT or MI-NORMAL-VERIFY-ASSETS logical task, then reintegration and invalidated assurance units | One whole-product audit and checkpointed suite catch cross-seam defects once | Findings share one release decision but are split to their existing owner before repair | Unaffected accepted tips and CHECK-U PASS credit remain; changed dependencies alone invalidate | Split repair by product versus strict test-only ownership; merge only compatible findings within one owner |

## Failure, continuation, and preserved results

Both assurance members complete feasible surfaces and join once. ROOT classifies the complete pool, preserves unaffected unit PASS, and starts with the earliest failed, unresolved, affected, or uncertain unit after a repaired coordinate arrives. Ordinary failure never cancels independent checks.

## Concurrency, isolation, resources, and lifecycle

LANE-FINAL-REVIEW and LANE-FINAL-CHECK use separate revision-pinned worktrees and result/cache roots. ROOT launches both before waiting and is the checkpoint owner. The integrated candidate remains retained through STEP-006.

## Cost and critical-path effect

This is the broad deterministic cost center, justified by the replacement of a 65,005-line candidate with a cross-process lifecycle product. Parallel audit/check execution and unit checkpoints are the only added machinery; no duplicate full suite appears elsewhere.
