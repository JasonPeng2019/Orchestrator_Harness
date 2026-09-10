# Harness v2 Tier 4 - Addendum 2 - Plan Validation

## 15. Rule application matrix

| Rule ID | Plan location | Concrete applied behavior |
|---|---|---|
| R1 | plan-workflow.md Sections 2-3; steps/STEP-002.md through steps/STEP-006.md | Every normative outcome is mapped to explicit requirements, deliverables, steps, checks, and ROOT acceptance. |
| R2 | plan-workflow.md Sections 5 and 10 | Identifiers exist only where graph, runtime correlation, or consumer provenance requires them. |
| R3 | plan-workflow.md Sections 7-8 | ROOT_DIRECT_WORKERS, singular writers, one join, and risk-based paired checks keep the topology minimal. |
| R4 | plan-workflow.md Section 14; modules/M02.md, modules/M04.md, modules/M05.md, modules/M07.md | Deployed behavior and realistic failure seams remain in scope while tolerance and out-of-scope entries stay explicit. |
| R5 | global-rules.md P09-P10; modules/M05.md | PASS requires evidence; missing or undecidable facts produce explicit terminal classifications. |
| R6 | plan-workflow.md Section 7; global-rules.md P01; modules/M05.md | Exactly one ROOT owns cross-lane meaning, integration choices, verdicts, and acceptance. |
| R7 | plan-workflow.md Section 7; modules/M02.md and modules/M03.md | DEL-001 and DEL-002 each have one serial writer and disjoint mutable scope. |
| R8 | plan-workflow.md Section 8; global-rules.md P06; modules/M04.md, modules/M07.md, modules/M09.md | Pools default to one; independent review/check and executor/observer members fan out and rejoin ROOT once. |
| R9 | plan-workflow.md BOUND-005 and Section 7; global-rules.md P02; modules/M01.md | User-owned role selections remain isolated in the mapping; every lane/module/launch retries its primary, and only a proved compute limit or exhausted current external impossibility permits a one-launch fallback. |
| R10 | modules/M01.md through modules/M09.md | Every selected instance has one ROOT governing card and at least one terminal worker member card using the ordered 20-field schema. |
| R11 | modules/M01.md through modules/M09.md | Every task card names concrete entrypoints and explains why its bounded seams are required. |
| R12 | global-rules.md P10; modules/M05.md | Shape validation precedes semantic adjudication and never substitutes for ROOT acceptance. |
| R13 | global-rules.md P09; modules/M05.md | Administrative faults affect their exact consumer and remain separate from product meaning. |
| R14 | global-rules.md P04, P06-P07; modules/M04.md, modules/M07.md, modules/M09.md | Every feasible member completes before pooling, repair, or verdict. |
| R15 | global-rules.md P08-P10; modules/M05.md | Every follow-up receives an explicit production, strict-test, administrative, support, authorization, or operation classification. |
| R16 | steps/STEP-002.md, steps/STEP-003.md, steps/STEP-005.md; modules/M04.md and modules/M05.md | Compatible findings pool once per owner while independent review and deterministic checks share one frozen input. |
| R17 | global-rules.md P07-P08; steps/STEP-001.md through steps/STEP-006.md | Every step has configured NORMAL, Series 1 repair/exit, and Series 2 progress-bound re-entry paths with explicit fallback to NORMAL. |
| R18 | global-rules.md P09; modules/M05.md | Support faults block direct consumers while independently proven product credit remains reusable. |
| R19 | global-rules.md P04 and P11-P12; modules/M07.md through modules/M09.md | Static, native-platform, and real-provider units bind conservative inputs, checkpoints, earliest-required restart, and unaffected PASS reuse. |
| R20 | plan-workflow.md Section 12; modules/M08.md | A disposable rehearsal proves fragile runner and external-control properties before real allocation. |
| R21 | plan-workflow.md Section 10; modules/M01.md through modules/M09.md | Each of 47 member cards maps one lane, invocation, process identity, workspace-local root, and terminal handoff to ROOT. |
| R22 | plan-workflow.md Section 12; modules/M08.md | Fake rehearsal evidence stays distinct from real product proof. |
| R23 | global-rules.md P15; modules/M09.md | Immediate containment is limited to observed wrong-target, containment-loss, or decision-data corruption conditions. |
| R24 | steps/STEP-001.md through steps/STEP-006.md; global-rules.md P13; modules/M05.md | Product continuation requires failed or undecidable required behavior; operation failures retain operation-only routes. |
| R25 | plan-workflow.md Section 1; modules/M02.md, modules/M04.md, modules/M07.md | Implementation and review apply correctness, simplicity, generality, organization, usability, composability, trust, and proportionality. |
| R26 | plan-workflow.md Section 4; modules/M01.md | Runtime enforcement, ROOT policy, target checks, and missing capabilities retain distinct owners and proofs. |
| R27 | plan-workflow.md Section 10; modules/M02.md through modules/M09.md | Each worker uses the smallest isolated mutable or result root required by its card. |
| R28 | plan-workflow.md Section 10; modules/M06.md and modules/M09.md | ROOT retires terminal clean unclaimed allocations only after retaining required revisions, results, and recovery facts. |
| R29 | plan-workflow.md Section 3; modules/M02.md and modules/M07.md | The shared short lock and its concurrency regression proof cover required concurrent queue and log writes. |
| R30 | plan-workflow.md Section 1; global-rules.md P02, P04, P09 | The finite-command manifest currently selects zero fragments; agent sessions remain unbounded and outside the finite-command wrapper. |
| S1 | plan-workflow.md Section 0; validation.md | The package has one composition root, one global policy artifact, six steps, ten module files, and one validation artifact. |
| S2 | plan-workflow.md Section 6; modules/M01.md through modules/M10.md | Every module has an explicit selection decision and every selected instance belongs to exactly one step. |
| S3 | plan-workflow.md Sections 6 and 8; steps/STEP-001.md through steps/STEP-006.md | Declared outputs connect to exact inputs and accepted outputs advance through named edges. |
| S4 | plan-workflow.md Section 0 | Global policy, steps, modules, mapping, and validation each have one authoritative artifact and edit boundary. |
| S5 | global-rules.md; modules/M01.md through modules/M09.md | Policies and task cards use explicit actors, conditions, actions, evidence, and terminal routes. |
| S6 | steps/STEP-001.md through steps/STEP-006.md; modules/M01.md through modules/M09.md | Steps compose module interfaces while instances retain project-specific scope and workers cannot change graph policy. |
| S7 | modules/M04.md and modules/M07.md | Review cards bind review class, frozen input, surfaces, invariants, materiality, output, and invalidation rules. |
| S8 | global-rules.md P06; modules/M04.md and modules/M07.md | Independent review/check members launch before either is awaited and write disjoint result roots. |
| S9 | global-rules.md P07-P08; modules/M05.md | Compatible complete findings batch once before ROOT issues a correction card to the same logical role. |
| S10 | modules/M07.md | The static safeguard owns five independent units, a conservative input map, checkpoint, and earliest-required resume. |
| S11 | modules/M02.md through modules/M09.md | Failure briefs cover realistic authority, path, concurrency, lifecycle, rollback, compatibility, external, truth, and usability seams. |
| S12 | plan-workflow.md Sections 5 and 8; global-rules.md P13; modules/M01.md through modules/M09.md | Relative cost, launches, overlap, expensive work, critical path, and observed-range reassessment are explicit. |
| S13 | global-rules.md P14 | The preauthorized exception set is empty and any future exception requires a validated amendment with complete fields. |
| S14 | plan-workflow.md; global-rules.md; validation.md | Graph, policies, steps, modules, roles, cards, lanes, handoffs, gates, and results have one consistent authority structure. |
| S15 | plan-workflow.md Section 4 and BOUND-013 | Every runtime capability, native platform runner, and workspace-placement rule has a named enforcement state, owner, proof, fallback, and product-code boundary. |
| S16 | steps/STEP-001.md through steps/STEP-006.md; plan-workflow.md Section 8 | Six gates each own one product family or exact operation with bounded blocking and named forward and return routes. |
| S17 | steps/STEP-001.md through steps/STEP-006.md | Every step has three ordered configured entries; both fast series have concrete MI paths, activation, invalidation, saved work, fallback, and progress-bound behavior. |

## 16. Structural validation result

| Check ID | Result | Basis |
|---|---|---|
| V01 | PASS | plan-workflow.md Section 0 and its package-dependency table enumerate the authoritative root, global rules, six step files, ten module files, mapping, and validation artifact. |
| V02 | PASS | plan-workflow.md and modules/M01.md through modules/M10.md use the canonical table schemas with populated selected contracts, no undefined selected-instance fields, and an explicit M10 omission decision. |
| V03 | PASS | plan-workflow.md Section 3 maps all 82 exact SRC-009 `[!]` IDs through REQ-001 through REQ-017 to one DEL row, verification, implementation role, acceptance owner, and COVERED status; REQ-018 separately covers execution integrity. |
| V04 | PASS | plan-workflow.md Section 6 and modules/M01.md through modules/M10.md declare each selected MI once and compose it in exactly one step. |
| V05 | PASS | plan-workflow.md Section 8 and steps/STEP-001.md through steps/STEP-006.md connect each declared output, input, edge, join, and gate. |
| V06 | PASS | modules/M10.md records the justified omission and plan-workflow.md contains zero M10 instances or execution edges. |
| V07 | PASS | plan-workflow.md Sections 5 and 8 plus every modules/M01.md through modules/M09.md cost section state dependency, payoff, or critical-path effect. |
| V08 | PASS | modules/M04.md and modules/M07.md require paired independent members to launch together on one frozen input with disjoint roots. |
| V09 | PASS | global-rules.md P04 and P07 require complete pools, ordinary-failure continuation, single batching, and configured Series 1 and Series 2 paths. |
| V10 | PASS | modules/M04.md fixes every review class, frozen input, requirements, surfaces, materiality rule, result, and handoff while leaving findings open. |
| V11 | PASS | modules/M07.md owns CHECK-U1 through CHECK-U5, binds them to the existing `test_check_u1` through `test_check_u5` module commands, and defines their conservative inputs, checkpoint, and ROOT-controlled full static execution. |
| V12 | PASS | global-rules.md P04 and modules/M07.md through modules/M09.md require unchanged source, scenario, runner, environment, authorization, and consumed external state for credit reuse, then earliest-required execution after invalidation. |
| V13 | PASS | modules/M01.md through modules/M09.md give every selected MI one ROOT governing card, at least one worker member card, and ordered recipe actions. |
| V14 | PASS | plan-workflow.md Sections 0 and 7 define ROOT_DIRECT_WORKERS with one ROOT and terminal workers that retain zero acceptance or routing authority. |
| V15 | PASS | global-rules.md P14 records zero preauthorized exception classes and requires a validated amendment for any future exception. |
| V16 | PASS | plan-workflow.md Section 4 distinguishes runtime enforcement, orchestrator policy, target-invoked checks, native-runner availability, workspace placement, and exact missing-capability recovery. |
| V17 | PASS | plan-workflow.md Section 4 and modules/M01.md attribute launcher capabilities only to the inspected frozen runtime revision and require fresh readback before the addendum epoch starts. |
| V18 | PASS | plan-workflow.md BOUND-005 and Section 7, global-rules.md P02, and modules/M01.md preserve eight user-owned role selections, retry the primary on every lane/module/launch, reject ordinary failures as fallback grounds, require retained workaround/readback proof for external impossibility, and limit a qualifying fallback to one launch. |
| V19 | PASS | plan-workflow.md Section 7 and modules/M02.md, modules/M03.md, modules/M06.md retain singular disjoint product, asset, and integration writers. |
| V20 | PASS | plan-workflow.md Section 10 gives all 47 member cards distinct lanes, invocations, process identities, handoffs, and BOUND-013 workspace-local roots; no addendum path reuses the completed prior epoch by contract. |
| V21 | PASS | modules/M01.md through modules/M09.md give each task card bounded concrete entrypoints and a specific reason for inclusion; M02 names the eight coupled source-entry groups and M07 names the real acceptance modules. |
| V22 | PASS | modules/M01.md through modules/M09.md tie all 82 gap families and realistic crash, concurrency, lifecycle, rollback, platform, provider, truth, and cleanup failures to exact gates, checks, evidence, and ROOT routes. |
| V23 | PASS | global-rules.md P08-P09 and modules/M05.md classify strict-test and support faults while preserving unaffected consumers. |
| V24 | PASS | steps/STEP-001.md and steps/STEP-004.md use OPERATION_BOUNDARY gates; the other four step files use PRODUCT gates with bounded continuation. |
| V25 | PASS | global-rules.md P04 and every STEP file preserve unaffected credit and resume at the earliest invalidated action through configured Series 2 re-entry. |
| V26 | PASS | plan-workflow.md Section 10 retirement rows and modules/M06.md and modules/M09.md retain live, dirty, ambiguous, or consumed state until safe closure. |
| V27 | PASS | modules/M01.md through modules/M09.md task cards name actor, trigger, action, proof, scope, output, handoff, failure route, and terminal rule. |
| V28 | PASS | validation.md Section 15 maps R1-R30 followed by S1-S17 exactly once to concrete package artifacts. |
| V29 | PASS | plan-workflow.md Section 10 reciprocally maps every member lane and handoff to a mapped producer role and ROOT consumer with exact correlation IDs. |
| V30 | PASS | steps/STEP-001.md through steps/STEP-006.md contain the exact canonical fast block plus NORMAL, Series 1, and Series 2 configured entries; modules/M01.md through modules/M09.md give Series 1 scoped correction, motivating test, changed-source compile, independent review, separate integration, and smoke credit, then Series 2 re-entry at the current progress bound with only invalidated or uncredited work. |

PLAN_STRUCTURE=VALID
