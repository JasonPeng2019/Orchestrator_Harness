# STEP-001 - Admit the Execution Contract

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-001 |
| Objective and independently decidable outcome | Prove the exact prerequisites for later frozen-harness execution without performing product work |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | OUT-003, REQ-018, BOUND-002, BOUND-005, BOUND-006 |
| Global policy and exception references | P01, P02, P09, P10, P13, P14 |
| Public compatibility boundary | Internal admission observations may change; any change to target revision, frozen runtime revision, role set, or required user authority invalidates the admitted output |

## Activation, inputs, and protected boundaries

The step activates from SRC-001 through SRC-007 before any execution lane exists. It consumes the clean target and frozen revisions, the exact eight-role set, the user's recorded assignment authority, the finite-command manifest, and later Git/live authorization facts. It may read all sources and may update only ROOT-owned planning/runtime inputs after user direction. It must not edit either codebase, create a worktree, alter the user-owned assignment map, or launch frozen-harness.

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
| NORMAL | Activates before all execution work | Sources, observed clean revisions, role inventory, and user authority | MI-NORMAL-ADMISSION | Admitted execution contract | EDGE-001 and EDGE-002 | Recheck only a prerequisite whose source changed | Original full admission path; no fast-lane claim | Hold the exact missing prerequisite inside the normal admission route |
| FAST_LANE_V2_SERIES_1 | Configured; activates when a complete pool establishes one scoped deterministic admission correction objective with a known motivating test and unchanged protected contracts | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-ADMISSION-PATCH, MI-FL2-S1-ADMISSION-REVIEW, MI-FL2-S1-ADMISSION-INTEGRATE | Accepted repaired admission output after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test run once as reusable smoke credit; declared changed inputs invalidate only dependent credit | Avoids replaying the complete repository, runtime, role, authority, and command-policy admission audit | If the scoped/deterministic guard fails or any fast result fails, use NORMAL admission from the earliest affected prerequisite |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-001 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior checkpoint, deterministic changed-input map, and protected baseline | MI-FL2-S2-ADMISSION-RECONCILE | Updated admission checkpoint and admitted execution contract | Return to the normal successor EDGE-001 and EDGE-002 after remaining required checks pass | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining failed, unresolved, affected, uncertain, or uncredited units from the earliest required unit | Avoids a full admission restart and preserves every unchanged prerequisite observation | If impact or credit reuse is uncertain, use NORMAL admission from the earliest uncertain prerequisite |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-ADMISSION | M01 | SRC-001 through SRC-007 and current user-supplied launch authority | Admitted execution contract or exact incomplete prerequisite | STEP-001 NORMAL activates |
| 2 | MI-FL2-S1-ADMISSION-PATCH | M01 | Complete scoped admission finding pool and unchanged admitted facts | Corrected admission candidate plus parse/compile and motivating readback smoke | Series 1 guard passes |
| 3 | MI-FL2-S1-ADMISSION-REVIEW | M04 | Frozen corrected admission candidate and smoke result | Independent review result | Series 1 patch publishes |
| 4 | MI-FL2-S1-ADMISSION-INTEGRATE | M06 | Reviewed corrected admission candidate | Integrated corrected admission output and changed-input map | Series 1 review passes |
| 5 | MI-FL2-S2-ADMISSION-RECONCILE | M01 | Accepted Series 1 exit set and prior admission checkpoint | Reconciled admitted execution contract | STEP-001 is current progress bound |

## Public outputs and successors

The sole success output states that all workflow roles have user-owned launch selections, the next required role primaries have passed their current launch recheck, each required review/check pair has two concurrently launchable selections, both repositories still match their admitted clean revisions, frozen-harness capabilities still match Section 4, the finite-command manifest has been reread, and the user has authorized the next exact Git/runtime operation. EDGE-001 and EDGE-002 activate STEP-002 and STEP-003 together. An incomplete prerequisite blocks only execution that consumes it.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-ADMISSION / LOOP-ADMISSION | OPERATION_BOUNDARY | Current prerequisite observations | Whether the exact execution-admission operation is proven | MI-NORMAL-ADMISSION | Missing authority, changed source, unresolved role selection, or changed runtime capability | Holds only the affected launch or Git operation and never product work or credit | No product loop; reread or establish only the failed prerequisite after ROOT or user supplies it | EDGE-001 and EDGE-002 advance on success | MI-NORMAL-ADMISSION exact prerequisite block | One read pass avoids repeated preflight in every lane | One ROOT decision owns all launch prerequisites without product semantics | No product credit exists; unchanged prerequisite observations remain usable | Split only if a later prerequisite gains a distinct authority or consumer |

## Failure, continuation, and preserved results

SATISFIED advances. MISSING may be established only by its named owner and only after user authority. INDETERMINATE or unauthorized state produces an exact incomplete result. Continuation starts with the first changed or unresolved prerequisite; unchanged clean-revision and runtime observations are preserved.

## Concurrency, isolation, resources, and lifecycle

ROOT alone decides admission. Each selected M01 instance uses one workspace-local CHECKER evidence lane with read-only inputs and a result root; it receives no product worktree or external claim. The evidence handoff must finish before ROOT records admission or activates construction. The observed frozen revision remains protected.

## Cost and critical-path effect

One read-and-decision pass is the cheapest prerequisite closure. It is serial because every worker launch consumes it, but it performs no expensive check or external allocation.
