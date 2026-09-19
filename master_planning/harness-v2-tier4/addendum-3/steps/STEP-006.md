# STEP-006 - Complete Proportional Product and Provider-Boundary Acceptance

## Step contract

| Field | Value |
|---|---|
| Step ID | STEP-006 |
| Objective and independently decidable outcome | Preserve accepted deterministic product evidence, reuse compatible native provider-boundary PASS credit, run only missing direct provider/profile canaries, retain exact support/macOS/Linux gaps, and issue the scoped DEL-003 verdict under BOUND-014/020 |
| Acceptance owner | ROOT |
| Deliverable and requirement coverage | DEL-003, REQ-017, REQ-019, REQ-020, OUT-004, OUT-005 |
| Global policy and exception references | P01 through P15 |
| Public compatibility boundary | Product credit is bound to its source/test inputs; provider-boundary credit is bound to the accepted candidate, provider/profile binding, complete public bootstrap/start/valid-result/completion-review/acceptance/retire path, managed hook contract when applicable, record schema, authorization, and consumed external state |

## Activation, inputs, and protected boundaries

EDGE-006 activates with static acceptance. SRC-010 and BOUND-020 retire the custom live-matrix controls from the prospective path. M08 is consumed only if the direct public canary entrypoint or its deterministic-record inputs lack unchanged readiness credit. M09 first reuses compatible retained native PASS and allocates only a missing provider/profile canary. BOUND-014 controls unexecuted platform gaps. Every runtime, result, cache, and disposable repository must resolve beneath the project workspace under BOUND-013. Practical execution must use the accepted candidate and never the user's unrelated projects or credentials beyond the authorized CLI profile.

### Current continuation (version 3.7)

Decision820 established that the remaining failures were acceptance-control,
fixture, provider-capacity, or downstream artifacts and established no product
defect. Retain all trustworthy product/static/native evidence. The pending review
of the corrected custom control closure and all downstream control integration,
readiness, and matrix replay are removed because this step no longer consumes
that apparatus. ROOT begins with an evidence-equivalence inventory for each
provider/profile boundary, then authorizes only the missing direct canaries. No
new attempt is authorized by this plan amendment itself.

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
| NORMAL | Activates from EDGE-006 or EDGE-CONTROL-DELTA; deterministic acceptance is retained and only unproved provider/profile boundaries are eligible for direct canaries | Static acceptance, accepted candidate, deterministic proof map, retained native evidence, direct public canary contract, and applicable authorization | MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT | Final accepted DEL-003 result or exact provider/platform support gap | EDGE-007 on scoped acceptance under BOUND-014/020 | Reuse deterministic and native PASS only under unchanged consumed inputs; run one direct canary for a boundary lacking compatible credit | Original proportional practical path; no fast-lane claim | LOOP-LIVE only for an actual failed/undecidable product criterion; support or authorization faults hold only their boundary claim |
| FAST_LANE_V2_SERIES_1 | Configured; activates only when a complete pool establishes one scoped deterministic correction to the direct public-canary fixture or record reader, with a known motivating local test and unchanged acceptance meaning | Complete pool, scoped correction objective, motivating test, frozen accepted baseline, and current checkpoint | MI-FL2-S1-LIVE-PATCH, MI-FL2-S1-LIVE-REVIEW, MI-FL2-S1-LIVE-INTEGRATE | Accepted repaired canary fixture/reader after independent review and integration, with changed-input map and smoke credit | Later current progress bound FAST_LANE_V2_SERIES_2 selected by ROOT | Changed-source compile and motivating test smoke credit are recorded once; only consuming boundary credit is invalidated | Avoids rebuilding product/assets and replaying unaffected deterministic or provider-boundary evidence | A product behavior, external state, authorization, acceptance-semantic, or uncertain-impact change uses the owning STEP NORMAL route; failed fast work returns to NORMAL classification |
| FAST_LANE_V2_SERIES_2 | Configured; activates when STEP-006 is the current progress bound and all accepted Series 1 exits for this repair set are integrated | All accepted Series 1 exits, prior deterministic/provider-boundary checkpoint, invalidation map, and protected baseline | MI-FL2-S2-LIVE-READINESS, MI-FL2-S2-LIVE-RECONCILE, MI-FL2-S2-LIVE-VERDICT | Updated checkpoint and final DEL-003 verdict or exact provider/platform support gap | Return to the normal successor EDGE-007 after the remaining affected deterministic or direct-canary boundary passes | Join accepted Series 1 exits, calculate invalidation, preserve unaffected PASS credit, and run remaining affected deterministic units or one affected boundary canary from the earliest required unit | Avoids repeating deterministic suites and every unaffected provider boundary | If state, authorization, impact, or cleanup is uncertain, close safely and use NORMAL from the earliest uncertain unit; failures return to NORMAL M05 classification |

## Ordered M-module composition

| Order | Instance ID | Module type | Consumes | Produces | Activation/condition |
|---|---|---|---|---|---|
| 1 | MI-NORMAL-LIVE-READINESS | M08 | Static candidate and direct public canary contract | Reused or focused current readiness result | EDGE-006 or EDGE-CONTROL-DELTA; runs only when consumed canary inputs changed |
| 2 | MI-NORMAL-LIVE-MATRIX | M09 | Deterministic acceptance, retained native evidence, readiness when required, provider authorization, and ROOT-selected missing boundaries | Complete proportional provider-boundary pool | At least one boundary lacks compatible retained PASS; otherwise publishes the retained-credit pool without external allocation |
| 3 | MI-NORMAL-LIVE-VERDICT | M05 | Static acceptance and proportional provider-boundary pool | Final DEL-003 verdict | Retained-credit inventory and any authorized direct canaries complete |
| 4 | MI-FL2-S1-LIVE-PATCH | M03 | Complete scoped descriptor/parser finding pool and fixed public-boundary or record-schema contract | Corrected boundary-evidence adapter plus compile and deterministic fake-record smoke | Series 1 guard passes |
| 5 | MI-FL2-S1-LIVE-REVIEW | M04 | Frozen corrected descriptor/parser and smoke | Independent fixed-semantics review result | Series 1 patch publishes |
| 6 | MI-FL2-S1-LIVE-INTEGRATE | M06 | Reviewed boundary-evidence adapter | Integrated adapter and exact affected-boundary map | Series 1 review passes |
| 7 | MI-FL2-S2-LIVE-READINESS | M08 | Accepted Series 1 exits and prior readiness checkpoint | Affected-only disposable readiness result | STEP-006 is current progress bound |
| 8 | MI-FL2-S2-LIVE-RECONCILE | M09 | Affected readiness result, retained boundary-credit map, selected provider/profile state, and authorization | One affected direct-canary result joined with retained practical credit | Affected readiness passes |
| 9 | MI-FL2-S2-LIVE-VERDICT | M05 | Reconciled practical pool and preserved credit | Final DEL-003 verdict or classified route | Series 2 remaining practical units finish |

## Public outputs and successors

RESULT-FINAL-ACCEPTANCE reaches the terminal user handoff through EDGE-007. It includes the accepted integrated coordinate, deterministic product verdict, retained or fresh provider-boundary facts, exact provider/platform support gaps, BOUND-014/020 readback, and cleanup disposition. Missing macOS/Linux runners retain REQ-019/020 native gaps. A provider-capacity/authentication gap stays support-only; an actual product contradiction follows M05.

## Gate, completion, and return boundary

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-LIVE / LOOP-LIVE | PRODUCT | One statically accepted candidate, deterministic proof map, and proportional provider-boundary pool | Whether required product behavior is decided and each shipped provider/profile boundary is either natively proved or truthfully recorded as a support gap | MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT | Deterministic product correctness plus direct bootstrap/start/valid-result/completion-review/acceptance/retire boundary, managed PostToolUse/Stop hook evidence, and truthful cleanup | Blocks only a failed or undecidable required product criterion; provider capacity/authentication and unexecuted native-platform gaps never become product failure | only a failed or genuinely undecidable required product criterion may continue LOOP-LIVE; support/native gaps remain explicit under BOUND-014/020 | EDGE-007 advances the scoped DEL-003 result with exact gaps | Affected MI-NORMAL-PRODUCT only for product evidence; exact support prerequisite for a boundary-only gap | Reusing accepted deterministic/native evidence avoids rebuilding or replaying equivalent proof | One executor runs only missing canaries and one read-only verifier checks durable product records after terminal state; no live observer process exists | Static acceptance and unaffected boundary PASS remain; reuse requires unchanged candidate/binding/full public path/managed-hook contract/record schema | Split future repair by product versus support; never reintroduce a feature/provider Cartesian matrix without a new user instruction |

## Failure, continuation, and preserved results

The direct canary produces one valid result, uses the profile-correct public completion-review and acceptance route before retirement, and uses the product's own durable records. Managed mode includes one harmless native tool action plus PostToolUse and valid-result Stop-hook evidence unless compatible retained hook PASS supplies those observations. The independent verifier reads records only after terminal retirement and launches no background observer. Ordinary failures do not cancel other authorized missing-boundary canaries. Immediate stop is limited to P15. M05 classifies once; product repair requires product evidence, while support and authorization gaps never fabricate a product verdict.

## Concurrency, isolation, resources, and lifecycle

Readiness is reused unless the direct-canary entrypoint or consumed record inputs changed. LANE-LIVE-EXECUTION owns one disposable public product canary at a time; LANE-LIVE-OBSERVATION performs post-terminal read-only record verification in a separate result root. LOCK-LIVE-MATRIX retains compatibility as the single practical-closure claim but does not authorize a matrix. ROOT owns authorization and final retirement.

## Cost and critical-path effect

External cost is limited to provider/profile boundaries lacking compatible retained PASS credit. At most one complete direct lifecycle canary per such boundary is eligible, with no feature multiplier, prompt-dependent fixture, repeated-launch scenario, scheduler, or background observer. A second material product cycle triggers P13 reassessment; support-only repetition is not authorized.
