# STEP-004 - Integrate Accepted Product and Assets

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-004 |
| Objective and independently decidable outcome | Combine exactly the two accepted tips at one clean target coordinate without changing accepted semantics |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-003 integration portion, REQ-018, OUT-003 |
| Global policy and exception references | P01, P02, P04, P09, P10, P13 through P15 |
| Public compatibility boundary | Mechanical join order and destination may change only by ROOT; changed accepted input, content conflict, or changed post-join seam invalidates the operation output |

## Activation, inputs, and protected boundaries

JOIN-001 activates only when RESULT-PRODUCT-ACCEPTANCE and RESULT-ASSET-ACCEPTANCE identify clean accepted revisions from the same admitted base. LANE-INTEGRATE alone may mutate WT-INTEGRATE. It must not resolve content conflicts, redefine tests, repair product behavior, alter accepted inputs, push, publish, or promote.

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
| NORMAL | Activates when JOIN-001 has both accepted tips | Accepted revisions, verdicts, base, order, destination, and post-join checks | MI-NORMAL-INTEGRATE | Integrated candidate coordinate or exact incomplete operation | EDGE-005 | Preserve accepted input credit; rerun only affected join/check action after an operation repair | Original full integration path; no fast-lane claim | Retry only the normal integration operation after ROOT resolves its exact prerequisite |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic integration correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-INTEGRATION-PATCH, MI-FL2-S1-INTEGRATION-REVIEW, MI-FL2-S1-INTEGRATION-INTEGRATE | Accepted repaired integration output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids rebuilding either accepted deliverable and replaying the full two-input integration | If correction changes product behavior, has a content conflict, or lacks deterministic impact, route to the owning earlier STEP NORMAL path; other fast failure returns to NORMAL integration |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-004 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-INTEGRATION-RECONCILE | Updated integrated coordinate and post-join checkpoint | Return to the normal successor EDGE-005 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a full two-branch reintegration and preserves unchanged accepted-input work | If input identity, conflict resolution, or impact is uncertain, use NORMAL integration from its earliest affected action |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-INTEGRATE | M06 | Two accepted revisions and verdicts, base, destination, and integration order | Integrated candidate coordinate and post-join result | JOIN-001 complete |
| 2 | MI-FL2-S1-INTEGRATION-PATCH | M02 | Complete scoped integration-owned finding pool and frozen accepted inputs | Corrected integration-owned tip plus compile and motivating-test smoke | Series 1 guard passes |
| 3 | MI-FL2-S1-INTEGRATION-REVIEW | M04 | Frozen corrected integration-owned tip | Independent review result | Series 1 patch publishes |
| 4 | MI-FL2-S1-INTEGRATION-INTEGRATE | M06 | Reviewed corrected tip and accepted inputs | Integrated corrected coordinate and changed-input map | Series 1 review passes |
| 5 | MI-FL2-S2-INTEGRATION-RECONCILE | M06 | All accepted Series 1 exits and prior integration checkpoint | Reconciled integrated coordinate | STEP-004 is current progress bound |

## Public outputs and successors

HANDOFF-INTEGRATION identifies the exact integrated revision and affected seam-check result. EDGE-005 activates STEP-005. Any destination mismatch, dirty state, altered input, content conflict, or interrupted join holds only GATE-INTEGRATION while accepted DEL-001 and DEL-002 credit remains intact.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-INTEGRATION / LOOP-INTEGRATION | OPERATION_BOUNDARY | Exact accepted product and asset revisions | Whether the declared integration operation produced the exact clean combined coordinate | MI-NORMAL-INTEGRATE | One join order, base, destination, and conflict-free seam | Holds only the exact integration operation and never product work or accepted product credit | No product loop; continue only the first unresolved integration action after ROOT resolves the operation fact | EDGE-005 advances the verified coordinate | MI-NORMAL-INTEGRATE exact operation block or ROOT conflict decision | One join avoids duplicated candidate coordinates and full checks | One integrator can perform the declared mechanical order; any semantic conflict stops | Both accepted input verdicts remain valid unless their revisions change | Split only if ROOT proves independent release units; merge no additional inputs without plan change |

## Failure, continuation, and preserved results

Operation faults preserve both accepted tips. A content conflict, changed input, or ambiguous destination terminates the worker handoff for ROOT; no worker chooses a resolution. Only an actual post-join product failure is classified by ROOT and routed to the affected accepted input owner.

## Concurrency, isolation, resources, and lifecycle

One integration writer owns WT-INTEGRATE. No concurrent writer may touch its branch. Frozen-harness validates its terminal result, while ROOT owns Git integration authorization and later retirement. Input and review lanes may retire only after their required revisions and verdicts are retained.

## Cost and critical-path effect

One serial join is unavoidable after the parallel build steps. It runs only seam-implicated checks; the broader safeguard remains in STEP-005.
