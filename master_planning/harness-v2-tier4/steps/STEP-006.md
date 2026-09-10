# STEP-006 - Prove Real Target-CLI Behavior and Close

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-006 |
| Objective and independently decidable outcome | Prove the Part XIX native matrix on every shipped target CLI and issue the final DEL-003 verdict |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-003, REQ-017, OUT-004, OUT-005 |
| Global policy and exception references | P01 through P15 |
| Public compatibility boundary | Readiness and live credit are bound to the accepted candidate, target CLI identity/configuration, control fixture, host environment, authorization, and consumed external state |

## Activation, inputs, and protected boundaries

EDGE-006 activates with static acceptance. M08 may use only disposable local fakes. M09 also requires explicit user authorization, exact installed target/config identities, and LOCK-LIVE-MATRIX. Live execution must use the accepted candidate and disposable repositories, never the user's unrelated projects or credentials beyond the authorized CLI profile.

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
| NORMAL | Activates from EDGE-006 and pauses before real allocation until user authorization | Static acceptance, candidate, readiness fixture, live scenario matrix, target identities, and authorization | MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT | Final accepted DEL-003 result or exact incomplete/failed live claim | EDGE-007 on acceptance | Reuse readiness only under unchanged inputs; for live units require verified unchanged candidate and consumed target/resource state, then resume at earliest required unit | Original full practical path; no fast-lane claim | LOOP-LIVE for classified product behavior; support or authorization faults hold only affected live claims |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic practical-control correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-LIVE-PATCH, MI-FL2-S1-LIVE-REVIEW, MI-FL2-S1-LIVE-INTEGRATE | Accepted repaired practical-control output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids rebuilding the broad product and asset deliverables and replaying unaffected readiness/live units | If the issue changes product behavior, external state, authorization, scenario meaning, or has uncertain impact, use the owning STEP NORMAL route; failed fast work returns to NORMAL classification |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-006 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-LIVE-READINESS, MI-FL2-S2-LIVE-RECONCILE, MI-FL2-S2-LIVE-VERDICT | Updated readiness/live checkpoint and final DEL-003 verdict or exact incomplete claim | Return to the normal successor EDGE-007 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a full readiness rehearsal and complete multi-target live-matrix restart | If state, authorization, impact, or cleanup is uncertain, close safely and use NORMAL from the earliest uncertain practical unit; failures return to NORMAL M05 classification |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-LIVE-READINESS | M08 | Static candidate and exact disposable control fixture | Current readiness result | EDGE-006 |
| 2 | MI-NORMAL-LIVE-MATRIX | M09 | Readiness PASS, user authorization, target identities, scenario contract, and exclusive claim | Complete correlated live result pool | All M09 preconditions pass |
| 3 | MI-NORMAL-LIVE-VERDICT | M05 | Static acceptance and complete live pool | Final DEL-003 verdict | Live attempt and observer join completes |
| 4 | MI-FL2-S1-LIVE-PATCH | M03 | Complete scoped control-asset finding pool and fixed scenario/oracle contract | Corrected control asset plus compile and motivating disposable-test smoke | Series 1 guard passes |
| 5 | MI-FL2-S1-LIVE-REVIEW | M04 | Frozen corrected control asset and smoke | Independent review result | Series 1 patch publishes |
| 6 | MI-FL2-S1-LIVE-INTEGRATE | M06 | Reviewed corrected control asset | Integrated correction and changed-input map | Series 1 review passes |
| 7 | MI-FL2-S2-LIVE-READINESS | M08 | Accepted Series 1 exits and prior readiness checkpoint | Affected-only disposable readiness result | STEP-006 is current progress bound |
| 8 | MI-FL2-S2-LIVE-RECONCILE | M09 | Readiness result, live checkpoint, verified target state, and authorization | Complete remaining practical result pool | Affected readiness passes |
| 9 | MI-FL2-S2-LIVE-VERDICT | M05 | Reconciled practical pool and preserved credit | Final DEL-003 verdict or classified route | Series 2 remaining practical units finish |

## Public outputs and successors

RESULT-FINAL-ACCEPTANCE reaches the terminal user handoff through EDGE-007. It includes the accepted integrated coordinate, static verdict, live claims, target identities, and cleanup disposition. If authorization or a target CLI cannot be supplied for the attempt, the output truthfully preserves static acceptance and marks only REQ-017 incomplete.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-LIVE / LOOP-LIVE | PRODUCT | One statically accepted candidate and one complete authorized live pool | Whether every required real target-CLI capability and cleanup contract is proved | MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT | Native hooks, role isolation, monitor liveness, lease reuse, and truthful cleanup | Blocks only REQ-017 and final consumers requiring real product capability proof | only a failed or genuinely undecidable required product criterion may continue LOOP-LIVE; missing authority remains INCOMPLETE | EDGE-007 advances the accepted DEL-003 result to the user | Affected MI-NORMAL-PRODUCT or exact support/external prerequisite; a new real attempt always requires ROOT authorization | One retained attempt per target set amortizes setup across four related scenarios | One executor and one observer can decide the shared native boundary while target sets serialize | Static acceptance and unaffected live unit PASS remain; practical PASS requires verified unchanged external state | Split future repair by product versus support; split real attempts by target identity and serialize them under one matrix |

## Failure, continuation, and preserved results

The observer starts before the behavior it observes. Ordinary failures do not cancel feasible live units. Immediate stop is limited to P15. Every attempt ends in verified cleanup or terminal-visible uncertainty. M05 pools and classifies once; a product repair returns through its owning source step and affected static/live units, while support and authorization gaps never fabricate a product verdict.

## Concurrency, isolation, resources, and lifecycle

Readiness finishes before real allocation. LANE-LIVE-EXECUTION and LANE-LIVE-OBSERVATION use separate worktrees and results; observation is read-only. Target sets execute serially under LOCK-LIVE-MATRIX. Frozen-harness owns the execution workers' controller and exact process cleanup; the target candidate owns only the nested v2 scenarios being validated. ROOT owns attempt authorization and final retirement.

## Cost and critical-path effect

Real target-CLI execution is the only external cost and is required by SRC-002. One reusable disposable fixture, one serialized executor, and one observer are the smallest safe topology. A second material live cycle triggers P13 reassessment; this is not an iteration limit.
