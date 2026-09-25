# STEP-001 - Freeze the builder and qualify the development boundary

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-001 |
| Objective and independently decidable outcome | Freeze the builder and qualify the development boundary; DEL-001 public guarantee independent of unrelated cleanup. |
| Acceptance owner | root |
| Deliverable and requirement coverage | DEL-001; REQ-001, REQ-027, REQ-028, REQ-029 |
| Global policy and exception references | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15; EXC-BUILDER-BUG only for its exact proven trigger |
| Public compatibility boundary | Versioned schema/identity and native lifecycle remain stable; interface change returns ROOT and actual downstream consumers. |

## Activation, inputs, and protected boundaries

later user implementation authority, inspected seed and frozen source. Consume exact accepted public outputs; protect frozen builder and all source outside assigned development paths. The normal BUILD instance owns the complete domain brief; this step composes interfaces only.

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
| NORMAL | later user implementation authority, inspected seed and frozen source satisfies admission for STEP-001 | later user implementation authority, inspected seed and frozen source; REQ-001, REQ-027, REQ-028, REQ-029 | MI-NORMAL-001-ADMIT -> MI-NORMAL-001-BUILD -> MI-NORMAL-001-ASSETS -> MI-NORMAL-001-CHECK -> MI-NORMAL-001-ACCEPT -> MI-NORMAL-001-INTEGRATE -> MI-NORMAL-001-READY -> MI-NORMAL-001-REAL -> MI-NORMAL-001-GATE | STEP-001.accepted integrated output | normal outgoing EDGE-001 consumers when their inputs are satisfied | checkpoint every selected check unit and actual state consumed | original full deliverable path, no fast-lane claim | ROOT classification through MI-NORMAL-001-GATE; uncertain eligibility uses normal owning repair without waiving this entry |
| FAST_LANE_V2_SERIES_1 | ROOT's complete pool from every feasible source check establishes one compatible STEP-001 scoped correction objective and exact deterministic motivating test | STEP-001 accepted output, complete pool, motivating test, bounded production surface and ROOT-authored intended/protected behavior | MI-FL2-S1-001-PATCH -> MI-FL2-S1-001-REVIEW -> MI-FL2-S1-001-ACCEPT -> MI-FL2-S1-001-EXIT | STEP-001.accepted repaired output after independent review and separate integration, with changed-input map and smoke credit | ROOT-selected later current progress bound STEP through Series 2; the bound itself is a set member once if affected | preserve changed-source compile and motivating test smoke credit plus unchanged unrelated checks | saves full implementation, broad affected campaign, unchanged service/native observations and final safeguard | ROOT classification through MI-FL2-S1-001-ACCEPT; uncertain eligibility uses normal owning repair without waiving this entry |
| FAST_LANE_V2_SERIES_2 | ROOT selects STEP-001 as the current progress bound and receives all accepted Series 1 repair exits | accepted Series 1 exits, exact repair set and checkpoint input map | MI-FL2-S2-001-REMAIN -> MI-FL2-S2-001-CONTINUE | STEP-001.reconciled checkpoint and accepted output | normal successor route EDGE-001-002 after remaining checks and ROOT acceptance | calculate input invalidation, preserve unaffected PASS, start earliest required remaining failed/unresolved/affected/uncertain/uncredited unit | saves earlier green units, unrelated steps, full restart and duplicate smoke | ROOT classification through MI-FL2-S2-001-CONTINUE; uncertain eligibility uses normal owning repair without waiving this entry; affected required live credit exits the fast path to ROOT normal classification as declared in REMAIN; no normal MI executes inside Series2 |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-001-ADMIT | M01 | later user implementation authority, inspected seed and frozen source | MI-NORMAL-001-ADMIT.verified prerequisite | ROOT dispatch after later user implementation authority, inspected seed and frozen source verified |
| 2 | MI-NORMAL-001-BUILD | M02 | MI-NORMAL-001-ADMIT.typed output satisfying M02 public input | MI-NORMAL-001-BUILD.reviewable product tip and smoke | ROOT dispatch after MI-NORMAL-001-ADMIT.typed output satisfying M02 public input verified |
| 3 | MI-NORMAL-001-ASSETS | M03 | MI-NORMAL-001-BUILD.typed output satisfying M03 public input | MI-NORMAL-001-ASSETS.independent asset tip and discovery | ROOT dispatch after MI-NORMAL-001-BUILD.typed output satisfying M03 public input verified |
| 4 | MI-NORMAL-001-CHECK | M04 | MI-NORMAL-001-ASSETS.typed output satisfying M04 public input | MI-NORMAL-001-CHECK.complete campaign pool | ROOT dispatch after MI-NORMAL-001-ASSETS.typed output satisfying M04 public input verified |
| 5 | MI-NORMAL-001-ACCEPT | M05 | MI-NORMAL-001-CHECK.typed output satisfying M05 public input | MI-NORMAL-001-ACCEPT.ROOT verdict and credit map | ROOT dispatch after MI-NORMAL-001-CHECK.typed output satisfying M05 public input verified |
| 6 | MI-NORMAL-001-INTEGRATE | M06 | MI-NORMAL-001-ACCEPT.typed output satisfying M06 public input | MI-NORMAL-001-INTEGRATE.verified integrated coordinate | ROOT dispatch after MI-NORMAL-001-ACCEPT.typed output satisfying M06 public input verified |
| 7 | MI-NORMAL-001-READY | M08 | MI-NORMAL-001-INTEGRATE.typed output satisfying M08 public input | MI-NORMAL-001-READY.readiness observation | ROOT dispatch after MI-NORMAL-001-INTEGRATE.typed output satisfying M08 public input verified |
| 8 | MI-NORMAL-001-REAL | M09 | MI-NORMAL-001-READY.typed output satisfying M09 public input | MI-NORMAL-001-REAL.real observations and cleanup | ROOT dispatch after MI-NORMAL-001-READY.typed output satisfying M09 public input verified |
| 9 | MI-NORMAL-001-GATE | M05 | MI-NORMAL-001-REAL.typed output satisfying M05 public input | MI-NORMAL-001-GATE.ROOT verdict and credit map | ROOT dispatch after MI-NORMAL-001-REAL.typed output satisfying M05 public input verified |
| 10 | MI-FL2-S1-001-PATCH | M02 | ROOT-admitted compatible correction and complete source pool | MI-FL2-S1-001-PATCH.reviewable product tip and smoke | ROOT dispatch after ROOT-admitted compatible correction and complete source pool verified |
| 11 | MI-FL2-S1-001-REVIEW | M04 | MI-FL2-S1-001-PATCH.typed output satisfying M04 public input | MI-FL2-S1-001-REVIEW.complete campaign pool | ROOT dispatch after MI-FL2-S1-001-PATCH.typed output satisfying M04 public input verified |
| 12 | MI-FL2-S1-001-ACCEPT | M05 | MI-FL2-S1-001-REVIEW.typed output satisfying M05 public input | MI-FL2-S1-001-ACCEPT.ROOT verdict and credit map | ROOT dispatch after MI-FL2-S1-001-REVIEW.typed output satisfying M05 public input verified |
| 13 | MI-FL2-S1-001-EXIT | M06 | MI-FL2-S1-001-ACCEPT.typed output satisfying M06 public input | MI-FL2-S1-001-EXIT.verified integrated coordinate | ROOT dispatch after MI-FL2-S1-001-ACCEPT.typed output satisfying M06 public input verified |
| 14 | MI-FL2-S2-001-REMAIN | M04 | all accepted integrated affected repair exits plus bound checkpoint | MI-FL2-S2-001-REMAIN.complete campaign pool | ROOT dispatch after all accepted integrated affected repair exits plus bound checkpoint verified |
| 15 | MI-FL2-S2-001-CONTINUE | M05 | MI-FL2-S2-001-REMAIN.typed output satisfying M05 public input | MI-FL2-S2-001-CONTINUE.ROOT verdict and credit map | ROOT dispatch after MI-FL2-S2-001-REMAIN.typed output satisfying M05 public input verified |

## Public outputs and successors

STEP-001.accepted integrated output supplies EDGE-001-002; repaired output goes only to ROOT-selected progress-bound Series2 before normal continuation. At the terminal bound self-membership is deduplicated, not a new later step.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-001 / LOOP-001 | PRODUCT | STEP-001 declared integrated candidate and consumed state | Does the observable behavior and proof contract of DEL-001 satisfy its explicit stage-local acceptance boundary? | MI-NORMAL-001-CHECK, MI-NORMAL-001-REAL, MI-FL2-S1-001-REVIEW, MI-FL2-S2-001-REMAIN | REQ-001, REQ-027, REQ-028, REQ-029; exact stage public guarantee | DEL-001 dependent product consumers only; operation/readiness/cleanup holds only its exact operation | only a failed or genuinely undecidable required product criterion; no product loop for independent support fault | outgoing EDGE-001 consumers once required public input is accepted | P07 originating production or asset owner; observing STEP keeps the current progress bound; P08 test-only and P09 operation routes remain separate | shared candidate, invariants and setup make one pool cheaper than per-file gates | one ROOT can triage the declared surface and one writer can repair; split at changed authority/contract | preserve all unchanged input/state PASS; run earliest required affected/unresolved unit | split if newly independent acceptance/authority or incoherent finding pool; no iteration-count cap |

## Failure, continuation, and preserved results

P04/P07/P08/P09/P10 govern exact criterion and consumer classification; the normal BUILD brief owns this step's explicit acceptance slice. Resume earliest failed/unresolved/affected/uncertain action; preserve unrelated accepted credit. No gate turns a non-product operational fault into product repair.

## Concurrency, isolation, resources, and lifecycle

One source writer at this step's shared seams. Independent frozen-tip reviews and test processes overlap under Section10 capacity; native lanes and service targets have exact ownership. No result overwrites or broad process cleanup.

## Cost and critical-path effect

0.5–2 engineering days unmeasured; source in root cost model. The full route builds one useful deliverable; Series1/2 retain unchanged implementation, review and check credit and avoid broad restarts. Reassess after observed control/estimate failure, not elapsed time alone.
