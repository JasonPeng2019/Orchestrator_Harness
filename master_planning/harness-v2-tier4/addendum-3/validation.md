# Harness v2 Tier 4 - Addendum 3 - Plan Validation

## 15. Rule application matrix

| Rule ID | Plan location | Concrete applied behavior |
|---|---|---|
| R1 | plan-workflow.md Sections 2-3; steps/STEP-002.md through steps/STEP-006.md | Every normative outcome is mapped to explicit requirements, deliverables, steps, checks, and ROOT acceptance. |
| R2 | plan-workflow.md Sections 5 and 10 | Identifiers exist only where graph, runtime correlation, or consumer provenance requires them. |
| R3 | plan-workflow.md Sections 7-8 | ROOT_DIRECT_WORKERS, singular writers, one join, and risk-based paired checks keep the topology minimal. |
| R4 | plan-workflow.md Section 14; modules/M02.md, modules/M04.md, modules/M05.md, modules/M07.md | Deployed behavior and realistic failure seams remain in scope while tolerance and out-of-scope entries stay explicit. |
| R5 | global-rules.md P02 and P09-P10; modules/M05.md | PASS requires evidence and a frozen-valid terminal result; missing, invalid, or undecidable facts produce explicit recovery or terminal classifications. |
| R6 | plan-workflow.md Section 7; global-rules.md P01; modules/M05.md | Exactly one ROOT owns cross-lane meaning, integration choices, verdicts, and acceptance. |
| R7 | plan-workflow.md Section 7; modules/M02.md and modules/M03.md | DEL-001 and DEL-002 each have one serial writer and disjoint mutable scope. |
| R8 | plan-workflow.md Section 8; global-rules.md P06; modules/M04.md, modules/M07.md, modules/M09.md | Pools default to one; independent review/check members fan out where useful, while each direct canary precedes its separate post-terminal record verifier and all results rejoin ROOT once. |
| R9 | plan-workflow.md BOUND-005 and Section 7; global-rules.md P02; modules/M01.md | User-owned role selections remain isolated in the mapping; every lane/module/launch retries its primary, invalid or missing terminal results use bounded same-thread correction while identity is intact, thrashing or identity drift produces a fresh structured same-role lane, and only a proved compute limit or exhausted current external impossibility permits a one-launch fallback. |
| R10 | modules/M01.md through modules/M09.md | Every selected instance has one ROOT governing card and at least one terminal worker member card using the ordered 20-field schema. |
| R11 | modules/M01.md through modules/M09.md | Every task card names concrete entrypoints and explains why its bounded seams are required. |
| R12 | global-rules.md P10; modules/M05.md | Shape validation precedes semantic adjudication and never substitutes for ROOT acceptance. |
| R13 | global-rules.md P02/P09; modules/M05.md | Administrative faults affect their exact consumer. Native result emission derives current identities, validates before publication and after readback, and preserves worker-authored outcomes and separate handoffs. Repeated launch failures receive a configuration repair and actual tool-action probe; replacement cards retain discovery and state what changed. |
| R14 | global-rules.md P04, P06-P07; modules/M04.md, modules/M07.md, modules/M09.md | Every feasible member completes before pooling, repair, or verdict. |
| R15 | global-rules.md P08-P10; modules/M05.md | Every follow-up receives an explicit production, strict-test, administrative, support, authorization, or operation classification. |
| R16 | steps/STEP-002.md, steps/STEP-003.md, steps/STEP-005.md; modules/M04.md and modules/M05.md | Compatible findings pool once per owner while independent review and deterministic checks share one frozen input. |
| R17 | global-rules.md P07-P08; steps/STEP-001.md through steps/STEP-006.md | Every step has configured NORMAL, Series 1 repair/exit, and Series 2 progress-bound re-entry paths with explicit fallback to NORMAL. |
| R18 | global-rules.md P09; modules/M05.md | Support faults block direct consumers while independently proven product credit remains reusable. |
| R19 | global-rules.md P04 and P11-P12; modules/M07.md through modules/M09.md | Deterministic, native-platform, and provider-boundary evidence binds conservative inputs, checkpoints, earliest-required restart, and unaffected PASS reuse. |
| R20 | plan-workflow.md Section 12; modules/M08.md | A read-only admission proves the accepted public canary commands, selected boundary identity, authorization/configuration, record paths, confinement, and cleanup contract before real allocation. |
| R21 | plan-workflow.md Section 10; modules/M01.md through modules/M09.md | Each of 48 member cards maps one lane, invocation, process identity, workspace-local root, and terminal handoff to ROOT. |
| R22 | plan-workflow.md Section 12; modules/M08.md | Read-only readiness stays distinct from deterministic product proof and native provider-boundary proof. |
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
| S10 | modules/M07.md | The static safeguard owns six safeguard units and two audit obligations, a conservative input map, checkpoint, and earliest-required resume. |
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
| V03 | PASS | plan-workflow.md Section 3 maps all eight tweak documents to 21 local requirements; DEL-001/002/003 and STEP coverage include deterministic Windows product proof, proportional provider-boundary proof, explicit native gaps, and repeated audits. |
| V04 | PASS | plan-workflow.md Section 6 and modules/M01.md through modules/M10.md declare each selected MI once and compose it in exactly one step. |
| V05 | PASS | plan-workflow.md Section 8 and steps/STEP-001.md through steps/STEP-006.md connect each declared output, input, edge, join, and gate. |
| V06 | PASS | modules/M10.md records the justified omission and plan-workflow.md contains zero M10 instances or execution edges. |
| V07 | PASS | plan-workflow.md Sections 5 and 8 plus every modules/M01.md through modules/M09.md cost section state dependency, payoff, or critical-path effect. |
| V08 | PASS | modules/M04.md and modules/M07.md require paired independent members to launch together on one frozen input with disjoint roots. |
| V09 | PASS | global-rules.md P04 and P07 require complete pools, ordinary-failure continuation, single batching, and configured Series 1 and Series 2 paths. |
| V10 | PASS | modules/M04.md fixes every review class, frozen input, requirements, surfaces, materiality rule, result, and handoff while leaving findings open. |
| V11 | PASS | modules/M07.md alone owns CHECK-U1..U5 and CHECK-FULL-SUITE; P11 and its audit member bind distinct initial/follow-up source observations and conservative reuse. |
| V12 | PASS | global-rules.md P04 and modules/M07.md through modules/M09.md require unchanged source, oracle, public boundary, record schema, provider/profile identity, authorization, and consumed external state for credit reuse, then earliest-required execution after invalidation. |
| V13 | PASS | modules/M01.md through modules/M09.md give every selected MI one ROOT governing card, at least one worker member card, and ordered recipe actions. |
| V14 | PASS | plan-workflow.md Sections 0 and 7 define ROOT_DIRECT_WORKERS with one ROOT and terminal workers that retain zero acceptance or routing authority. |
| V15 | PASS | global-rules.md P14 records zero preauthorized exception classes and requires a validated amendment for any future exception. |
| V16 | PASS | plan-workflow.md Section 4 distinguishes runtime enforcement, orchestrator policy, target-invoked checks, native-runner availability, workspace placement, and exact missing-capability recovery. |
| V17 | PASS | plan-workflow.md Section 4 and modules/M01.md attribute launcher capabilities only to the inspected frozen runtime revision and require fresh readback before the addendum epoch starts. |
| V18 | PASS | global-rules.md P02 and modules/M01.md require dispatch-time role resolution and exact current config_overrides propagation/readback; the unchanged canonical mapping owns concrete compaction limits. P02 also requires a frozen-valid terminal result, bounded identity-preserving result correction, evidence-based thrash detection, and fresh or split same-role recovery without treating malformed results as fallback eligibility. |
| V19 | PASS | plan-workflow.md Section 7 and modules/M02.md, modules/M03.md, modules/M06.md retain singular disjoint product, asset, and integration writers. |
| V20 | PASS | plan-workflow.md Section 10 gives all 48 member cards distinct lanes, invocations, process identities, handoffs, and BOUND-013 workspace-local roots; no addendum path reuses the completed prior epoch by contract. |
| V21 | PASS | modules/M01.md through modules/M09.md give each task card bounded concrete entrypoints and a specific reason for inclusion; M02 names the eight coupled source-entry groups and M07 names the real acceptance modules. |
| V22 | PASS | modules/M01.md through modules/M09.md tie operational tweak behavior and realistic crash, concurrency, lifecycle, rollback, platform, provider-boundary, truth, and cleanup failures to exact deterministic checks or proportional native canaries and ROOT routes. |
| V23 | PASS | global-rules.md P04/P10/P12 and plan-workflow.md BOUND-014/BOUND-020 separate absent macOS/Linux and provider support gaps from deterministic product correctness, preserve their unverified status, and allow EDGE-007 after executable-scope acceptance. |
| V24 | PASS | steps/STEP-001.md and steps/STEP-004.md use OPERATION_BOUNDARY gates; the other four step files use PRODUCT gates with bounded continuation. |
| V25 | PASS | global-rules.md P04 and every STEP file preserve unaffected credit and resume at the earliest invalidated action through configured Series 2 re-entry. |
| V26 | PASS | plan-workflow.md Section 10 retirement rows and modules/M06.md and modules/M09.md retain live, dirty, ambiguous, or consumed state until safe closure. |
| V27 | PASS | modules/M01.md through modules/M09.md task cards name actor, trigger, action, proof, scope, output, handoff, failure route, and terminal rule. |
| V28 | PASS | validation.md Section 15 maps R1-R30 followed by S1-S17 exactly once to concrete package artifacts. |
| V29 | PASS | plan-workflow.md Section 10 reciprocally maps every member lane and handoff to a mapped producer role and ROOT consumer with exact correlation IDs. |
| V30 | PASS | steps/STEP-001.md through steps/STEP-006.md contain the exact canonical fast block plus NORMAL, Series 1, and Series 2 configured entries; modules/M01.md through modules/M09.md give Series 1 scoped correction, motivating test, changed-source compile, independent review, separate integration, and smoke credit, then Series 2 re-entry at the current progress bound with only invalidated or uncredited work. |

### Execution-efficiency amendment validation (2026-09-16)

Scope: plan version 3.1 and the latest corrected audit ending at the unchanged
18h13m38s checkpoint. The following is a manual trace of **plan behavior**, not
execution evidence for the pending readiness or live matrix.

- M03/M08 require typed custom-adapter execution, wait-producer ordering, parser
  rejection, retired-epoch handling, mixed preserved credit, complete fixtures,
  semantic candidate binding and truthful cleanup. Thus string-only tests cannot
  grant the changed control readiness credit. Actual coverage is pending readback
  of the installed bundle and its tests on authorized execution resume.
- M05 compares the product clause with the assertion before assigning a mutation;
  uncertain Windows direct-reader guarantees get an open feasibility inquiry.
  Its dispatch rule preserves distinct repair mechanisms while batching compatible
  findings. This addresses records 212/213/223/231 without claiming their entire
  overlapping durations as saved time.
- M09 binds queue/terminal/publication owners and enforces one outstanding wait
  as an executor contract. Lost handles require checkpoint and identity
  reconciliation. P02/M09 explicitly classify current supervision as manual;
  no automatic scheduler/watchdog implementation is claimed.
- P02 carries completed questions through compaction to READY_TO_REPORT, retains
  both same-thread correction attempts, and excludes elapsed-only termination.
  P02/P12 use native errors and the actual credential home for launch diagnosis.
  P09 preserves substantive credit on encoding/envelope/digest correction and
  cannot rewrite intentionally malformed live-test evidence into PASS.
- Section 7 retains current serial capacity pending resource qualification;
  primary/fallback selection, independent substantive review, three STEP paths,
  accepted evidence and the paused state remain intact. No unsupported numeric
  savings claim or new telemetry artifact is introduced.

Focused commands run for this amendment:

```text
python .agents/skills/project-topology/references/level-4-design-project-topology/scripts/validate_execution_plan.py master_planning/harness-v2-tier4/addendum-3 --mapping (Resolve-Path master_planning/*ROLE*json).Path
  PASS (structural package checks; not runtime/control proof)
python -X utf8 C:/Users/Jason/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/project-topology
  PASS
python -X utf8 C:/Users/Jason/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/project-topology/references/level-4-design-project-topology
  PASS
git diff --check
  PASS (line-ending notices only)
```

No product suite or live/provider command was run: this amendment changes planning
guidance only. The structural validator does not execute the semantic scenarios
above. Implementation/readiness evidence remains a separate future obligation.

Independent read-only review: SHIP, no material findings. Its optional clarification
that the current outer-queue rehearsal is manual and disposable was incorporated
in M08; no automatic scheduler is required or claimed.

### Merged-skill review and resume preparation (version 3.2)

Independent read-only review identified three missing bindings: actual public
transport rehearsal, effective storage/child environment, and remaining-path cost
reassessment. Section 4 now selects existing host tools rather than adding a new
framework/profile/result format. M08 names the accepted candidate's actual public
entry, distinguishes parser/mocked/synthetic coverage from full boundary proof,
and assigns only missing properties through M03. P12 owns effective paths and
footprint limitations. Section 8 names the remaining dependency path, observed
local timing and P13 reassessment without inventing a live-duration estimate.

ROOT preparation evidence is `.plans/addendum3-resume-state.json` at the repository
root. All three reviewed replacements match decision 256, the other 14 assets
match the seed, and the candidate worktree is clean at the accepted tip. The
32 local control tests passed (native exit 0), and `validate_cell_controls.py`
passed (native exit 0). These checks were run from the installed matrix driver;
they do not grant all M08 properties or live acceptance.

The frozen native invocation parser, persisted-repository comparison, complete
process inventory and active-declaration check validate the prepared same-thread
continuation. The selected primary/configuration matches the current mapping and
the native session file exists. Actual provider resume/authentication remains
unexecuted. Exact Windows signaled termination was required because retained
process objects still expose creation identities; the single stale claim was
archived and natively reclaimed with that stronger proof. Zero claims remain at
the recorded preparation observation. No live work, source change or process kill
occurred; the old status and logs are archived before their eventual native reuse.

Historical version 3.2 remaining evidence (superseded by the version 3.3 checkpoint below): worker result/handoff publication and separate ROOT
integration acceptance; affected M08 property/public-path/environment/queue mapping;
current M09 target and credential-home admission; affected Windows cells and M05
verdict. The plan is prepared for non-live recovery, not admitted to live execution.



### Remaining-work scope audit (version 3.6; earlier audit history below)

The user's current instruction limits revision to unfinished work. STEP-001 through
STEP-005, their three entry paths and historical evidence are preserved, not
retrospectively re-audited. The reviewer inspects their interfaces only for
cross-step duplication or changed-input dependencies of the remaining STEP-006
work. This audit does not waive any requirement or grant product acceptance.

| Audit field | Value |
|---|---|
| Plan writer | /root |
| Independent reviewer | INVOCATION-PLANNING-V36-REVIEW-001, mapped fallback Terra/xhigh, thread 01a0b323-6e2d-7d02-95b4-b08dad69d629; same-thread focused follow-up; mapped primary attempted for both rounds and returned current API429 |
| Review evidence | Repository-root w/addendum-3-epoch-001/planning-v36-review/.agent-workspace/review.md and followup-review.md; native responses and launch records in .plans/addendum3-v3.6-local-concurrency/ |
| ROOT acceptance | ROOT accepts version 3.6 after F1/F2 corrections and independent focused SHIP; final decision below; no product acceptance |
| Audit status | ACCEPTED |

| Step | Evidence scope | Requirement and oracle | Dimension rationale | Cost basis | Review findings | Writer disposition | Final status |
|---|---|---|---|---|---|---|---|
| STEP-001 | Existing NORMAL and both FAST_LANE_V2 paths in steps/STEP-001.md; no new admission work | Existing admission identities and readbacks preserved; P04 changed-input boundary only | No new matrix or duplicate epoch admission | Zero newly scheduled executions; historical cost unchanged | No material dependency defect; completed scope preserved | Preserve completed scope per current user instruction; no retrospective approval claimed | ACCEPTED |
| STEP-002 | Existing NORMAL and both FAST_LANE_V2 paths in steps/STEP-002.md; M02/M04/M05 accepted product evidence | REQ-001..015 and existing product oracles unchanged | No newly proposed product tests absent a proved source defect | Zero newly scheduled work; any later product repair must price its actual delta | No material dependency defect; completed scope preserved | Preserve completed scope; no product repair inferred from control FAIL | ACCEPTED |
| STEP-003 | Existing three STEP-003 paths and accepted assets; prospective EDGE-CONTROL-DELTA activation only | REQ-016 and existing asset discovery/matrix completeness unchanged | No reconstruction of accepted scenarios; M03 normal work limited to the admitted matrix-control delta | Zero suite rebuilds scheduled; remaining control delta owned by STEP-006 | No material dependency defect; completed scope preserved | Preserve completed scope and evidence; no historical suite audit claimed | ACCEPTED |
| STEP-004 | Existing three STEP-004 paths and accepted integration; prospective M06 normal join binds retained product plus corrected controls | Existing candidate/input/readback oracles; new scoped integration only after admitted repair | One existing integration boundary per admitted repair, no global restart | Zero replay of completed integration; new delta cost unmeasured until scope is set | No material dependency defect; completed scope preserved | Preserve completed scope; separate integration owner remains | ACCEPTED |
| STEP-005 | Existing three paths; M07 CHECK-U1..U5, both CHECK-FULL-SUITE discovery commands and required implementation audits; scheduling changes only future invalidated units | Existing source/static and REQ-021 oracles preserved; P11 changed-input obligations remain | No new full-suite execution; economical future shards must reconcile complete discovery, fixtures and per-test outcomes | Zero newly scheduled broad campaigns; future selected commands bind measured/provisional budgets and K_local before admission | F2: static card named older checkout and inconsistent command flags | ACCEPT-REPLACE: frozen integrated WT-FINAL-CHECK cwd, python -B commands, isolated output/environment and separate discovery results; preserve accepted credit | ACCEPTED |
| STEP-006 | All three paths; M04 affected commands, M08 integrated proof, M09 residual native matrix and M05 cause-group verdict | Unchanged REQ-017/019/020 and CHECK-LIVE-1..16 assertions; local fakes do not replace native proof | Joined Series9 ledger597 remains 96 rows at 68 PASS / 28 FAIL; actual uncredited/invalidated selection recomputed after accepted repairs | No test replay from this edit; checker698 reports 0.313s/0.871s test bodies, excluding startup; M08 estimate 1-5min, max10+2 cleanup retained; local host rule K_local separate from live2; all future actual selections reprice graph/cleanup under P13 | F1: ignored driver source/provisioning insufficiently bound; coverage, collection, isolation and capacity contract otherwise pass | ACCEPT-ADD immutable producer695 inventory and Git tip provisioning/readback in M04; M08 consumes accepted M06 input identities; block exact missing consumer only; retain pending result/acceptance boundaries | ACCEPTED |

Version 3.3 structural validation passed; protected-file preservation was verified against the pre-edit snapshot. No product/live command is run
for this planning amendment, and no M05 semantic verdict is published.


#### Audit review record

Independent reviewer `/root/review_remaining_scope` returned **SHIP** after
comparing every current-task delta with the pre-edit backup and reading the full
STEP-006 paths, M03/M04/M05/M06/M08/M09 cards, P04/P08/P10/P11, CHECK-LIVE-1
through CHECK-LIVE-16 and platform/static/audit interfaces, both binding tweak
sources and the Series 4 15-group packet. Its review found no material scope,
coverage, oracle, cost-honesty or duplication defect. It confirmed the provisional
22 control + 7 dependent + 10 support/indeterminate + 1 deviation partition,
39 unresolved starting coordinates rather than a cap, continued independent
review/integration, and retention of actual provider/hook/resume requirements.
Completed STEP-001 through STEP-005 were checked only for preservation and
remaining-work dependencies, not given retrospective test-scope approval.

Finding and writer disposition: **ACCEPT-REPLACE** the low-severity `goal.md:1`
encoding error introduced during this edit; restore its original UTF-8 BOM and
heading. ROOT applied that exact correction. It changes no oracle, requirement,
case count or runtime cost. There were no scope-trimming recommendations to
accept or reject and no unresolved material findings. The single focused follow-up returned SHIP and verified the original UTF-8 BOM
and heading match the backup. The evidence scope is unchanged since initial review.

#### ROOT planning decision

ROOT accepts version 3.3's remaining-work evidence scope on the independent
review above and its direct source/packet readback. Preserve the accepted
exhaustive inventory and completed progress; trim only automatic duplication and
provider multiplication of local control proof, as specified in the owning P04,
P10, P11 and M03/M05/M08/M09 artifacts. No required native observation is replaced
by fixture evidence. M05 still must adjudicate the current pool before any new
repair/live selection; the 39-row starting set is not a release verdict.
Execution remains paused. This is planning acceptance only, with final package
structural validation reported separately below.


Final planning checks:

- `python .agents/skills/project-topology/references/level-4-design-project-topology/scripts/validate_execution_plan.py master_planning/harness-v2-tier4/addendum-3 --mapping (Resolve-Path master_planning/*ROLE*json).Path`: PASS, native exit 0.
- Pre-edit SHA-256 comparison: completed STEP-001 through STEP-005, untouched
  modules M01/M02/M04/M06/M07/M10, role mapping and snapshotted runtime checkpoint
  evidence are unchanged. Only the declared remaining-work owners were edited.
- Independent initial audit SHIP; focused encoding-correction follow-up SHIP.
- `git diff --check -- master_planning/harness-v2-tier4/addendum-3 HANDOFF.md goal.md`: PASS, native exit 0.

These are planning/structure and preservation checks, not a product-suite run,
live proof, semantic M05 decision or guarantee of minimum runtime. Historical
version 3.1/3.2 validation above remains historical evidence.


### ROOT functional-adequacy audit (version 3.4)

ROOT inspected the normative remaining-live and bounded-correction requirements,
the full CHECK-LIVE-1..16 inventory and remaining M03/M05/M08/M09 scope, and
concrete candidate/control assertions. The suite has not been reduced to a smoke
test: the accepted candidate contains 265 test-function definitions recursively
in 38 orchestrator_harness test files (231 in 26 top-level files), plus separate
live-control tests and the retained 96 Windows coordinates. These are static
inventory counts, not executed-case counts, coverage percentages or proof of PASS.
No executable test was removed by versions 3.3 or 3.4.

Inspection sources are the accepted Series 4 worktree's
`orchestrator_harness/tests/` and `.agent-workspace/live-matrix/driver/`.
This is a focused assertion/plan adequacy audit of remaining risks, not a claim
that every historical test implementation has been exhaustively reviewed.

Findings and ROOT writer dispositions:

1. **ACCEPT-STRENGTHEN: coverage before cost in the skill.** The prior audit already
   protected binding requirements, but its removal/merge/sample vocabulary gave
   additions less explicit treatment. The skill now establishes a coverage floor,
   asks what broken behavior could still pass, and provides ACCEPT-ADD and
   ACCEPT-STRENGTHEN. Sampling needs a demonstrated equivalence argument; unknown
   interactions retain coverage. This adds no universal Cartesian test mandate.
2. **ACCEPT-STRENGTHEN: fixture and monitor caller proof.** In
   `test_live_control_repair.py`, the fixture-copy test at line 223 uses an ordinary
   temporary directory, while `run-cell.py:1108` resolves the destination before
   its lexical check. The monitor test at line 183 mocks healthy records and
   checks a source string. The CHECK13 test at line 451 substitutes transport and
   tests helpers; actual `scenario_13` calls custom-adapter isolation before setup.
   These useful narrow tests can pass without exercising the incident-producing
   junction or caller sequence. M08 now demands actual junction/source preservation
   and actual scenario setup ordering with positive, refusal and terminal cases.
3. **ACCEPT-STRENGTHEN: atomic reader and joins.** The reader tests execute generated
   code against fake paths and synthetic errors; its deadline test checks strings.
   Keep their negative assertions, add the affected real Windows child/file boundary
   and executable deadline/error exhaustion proof. For CHECK15/16, 96 coordinates
   and valid hashes cannot alone establish every required subcase. Preserve existing
   bad-hash/identity/failed-credit tests and require missing-subcase rejection plus
   explicit required observations before reusing aggregate credit. No native
   behavior is inferred from a fixture or family label.
4. **ACCEPT-ADD where missing: candidate correction-limit evidence.**
   `test_addendum3_product.py:338` calls the candidate controller but succeeds on
   the third attempt; its name does not prove the five-prompt/sixth-exit limit.
   `v2_acceptance/test_addendum_observation_oracles.py` exercises the limit oracle
   with constructed arrays; `test_check_u3.py` explicitly uses a reference runtime.
   Those do not substitute for candidate execution of exhaustion. M08 now checks
   for actual matching candidate-boundary evidence first, then requires only missing
   deterministic correction scenarios through M03. Retain native saved-session,
   provider/hook and adverse behavior in CHECK-LIVE-8; local proof cannot close it.

The actual defect here is insufficient specificity/strength of some proof paths,
not evidence that all tests are simplistic or that product acceptance is achieved.
Version 3.3 already requested realistic local branches; version 3.4 makes the
required observations and adjacent failures explicit and closes the retry-boundary
proof ambiguity. Six families may share scenarios and reuse adequate existing
assertions. Additional construction/runtime is unmeasured until the evidence map
identifies genuinely missing cases; no savings or test-count quota is asserted.
No product/driver tests are modified or executed during this paused planning task.
The existing M03/M04/M06/M08 path authors, reviews, integrates and executes any
missing proof on an authorized resume. Completed progress remains intact.

Version 3.4 independent initial review completed; focused follow-up SHIP. Final structural checks recorded below.


Version 3.4 independent initial review: `/root/review_coverage_floor` corroborated
ROOT's concrete findings and preservation checks, with one material addition:
M08's generic later recovery left the last-valid-attempt branch underspecified.
**ACCEPT-STRENGTHEN:** require a valid result on the fifth correction/sixth provider
attempt to enter review_pending, no premature terminal event after the first five
invalid exits, and exactly one provider_exited_no_result monitor event after the
sixth invalid exit. This directly implements bounded-correction Required tests
1, 3 and 4 at the candidate controller's validity-versus-limit branch. Existing
adequate evidence can satisfy it; no provider multiplier or new requirement is
introduced. Additional runtime remains unmeasured and limited to missing proof.
ROOT also accepted the optional M03 routing clarification: additions outside P08's
unchanged-strength/coverage guard use NORMAL even if the product contract is fixed.
A single focused follow-up covers these corrections; no other scope change.


#### Final version 3.4 decision and validation

ROOT accepts the strengthened planned coverage. The independent focused follow-up
returned **SHIP**, confirming the retry-limit success/failure boundaries, terminal
monitor event, explicit P08 routing and accurate dispositions. No material finding
remains in this reviewed delta. This accepts a plan for sufficient evidence, not
an unexecuted test result or a guarantee that the product currently works.

The pre-edit SHA-256 comparison confirms all five completed STEP files, untouched
modules M01/M02/M04/M05/M06/M07/M10 and the user-owned role mapping are unchanged.
The 96-cell requirement, raw Series 4 findings and paused M05 decision boundary
remain intact. Implementation of missing tests belongs to the next authorized
execution of their declared owner; no product/provider tests ran in this audit.

Final version 3.4 checks, all native exit 0:

- Formal execution-plan validator with the canonical role mapping: PASS.
- Skill-creator quick validation of project-topology and its formal Tier 4
  entrypoint: both PASS.
- `git diff --check` for the edited skill, plan, goal and handoff paths: PASS.

These checks establish package/skill structure and clean patch formatting; they
cannot establish functional test results. Those remain explicitly pending where
required in the execution plan.

### Version 3.5 remaining-matrix review and stop checkpoint

This amendment preserves accepted execution while changing prospective unfinished
work. STEP003/004 and M06 edits add only the review-required normal correction
return; they do not revoke the original accepted steps or broaden checks. The
96-coordinate Windows inventory, all native subcase oracles and BOUND014 stay intact.
Pause594 retains all 12 Series9 raw results (2 PASS / 10 FAIL), exact process absence
and claim release. Their M09 join/M05 semantic decision is still pending.

Independent initial reviewer INVOCATION-PLANNING-V35-REVIEW-001 returned REVISE
with a frozen-valid result. Exact review: repository-root
`w/addendum-3-epoch-001/planning-v35-review/.agent-workspace/review.md`. Durable
launch/auth/response records are in repository-root `.plans/addendum3-v3.5-matrix/`.
The mapped primary was attempted first; native auth refresh failed and auth status
confirmed no login, so the mapped fallback performed this review. The user later
reauthenticated and authorized run-local repair; the mapped primary completed
the single focused follow-up. This is planning review only, not execution authority.

- F-01, ACCEPT-ADD: declare EDGE-CONTROL-DELTA and prospective STEP003/004/M06
  bindings; retain the accepted product input, integrate corrected assets, publish
  an exact changed-input map, retain unaffected STEP005 acceptance and return via
  EDGE006 to affected M08/M09. No accepted campaign replay or fast-guard waiver.
- F-02, ACCEPT-SCHEDULE: remove remaining task-card serialization and concurrent-
  target bans; require graph-ready execution within resource limits, per-coordinate
  cleanup and observer-ready activation. Preserve CHECK16 evidence dependencies.
- F-03, ACCEPT-REPLACE: replace the obsolete Series4 critical path with stopped
  Series9 reconciliation, one cause-group decision, scoped control return, affected
  readiness, authorized residual matrix and final acceptance.

Focused follow-up returned REVISE solely because CARD-LIVE-EXECUTION still said
"do not run target sets concurrently". It confirmed F-01/F-03 and every other F-02
correction, found no other material defect, and explicitly said a further review
was unnecessary after the one-line alignment. ROOT accepts that concrete finding,
replaces the phrase with a ban on concurrent access to the same provider home or
other exclusive mutable state, and verifies the required/forbidden fields now agree.
This is ACCEPT-SCHEDULE, not a fabricated reviewer SHIP or waived finding.

ROOT accepts the final version 3.5 planning scope. All review findings have concrete
dispositions; functional/native assertion coverage and all six step entry paths are
retained. STEP003/004 and M06 changes specialize only the future correction return;
accepted history remains accepted. The required runner changes and resource proof
are still future work; this decision cannot qualify runtime concurrency or pass a
failed Windows claim. The run remains paused and authenticated for a later resume.

Final commands: `python -X utf8 .agents/skills/project-topology/references/level-4-design-project-topology/scripts/validate_execution_plan.py master_planning/harness-v2-tier4/addendum-3 --mapping $mappingPath`
where `$mappingPath` resolves the single Agent mapping entry in plan-workflow.md Section 1,
returned native exit 0, `execution plan validation: PASS`.
`git diff --check -- master_planning/harness-v2-tier4/addendum-3 goal.md HANDOFF.md`
returned native exit 0. No product-suite/native matrix rerun was used for validation.

Final validation evidence is recorded in `.plans/addendum3-v3.5-matrix/`:
structural validator, diff whitespace check and final-preservation-check.json.
The preservation check verifies nine untouched protected files, unchanged requirement
and live/platform-check rows, all six canonical/three-entry paths and execution
scope authority. Other prospective owner edits are the reviewed delta above.


Resumption preparation: M09 join598 and M05 decision606 close attempt019 with
pool/ledger597 at 68 PASS / 28 FAIL. ROOT audited CHECKER599 in605 and staged the
next NORMAL asset card607/invocation608 without starting development or live tests.
The final verification also removed the duplicate mapping filename in the command
example above; the single authoritative mapping entry and role assignments did
not change. See runtime record610 for final preparation evidence.

### Version 3.6 local-test scheduling decision

ROOT accepts the prospective remaining-work amendment. Independent initial review
returned REVISE with two concrete input-binding defects; the single focused
same-thread follow-up returned SHIP with no remaining material finding.

- F1, ACCEPT-ADD: M04 binds the pending producer Git tip and full ignored-asset
  inventory695, provisions/verifies it before dispatch and blocks only missing
  consumers. M08 consumes accepted M06 identities and candidate rebind694 instead
  of confusing the old Series4 controls with the new Series10 assertion set.
- F2, ACCEPT-REPLACE: M07's card consistently uses the integrated WT-FINAL-CHECK,
  python -B unittest commands, command-owned environment/output and separately
  reported discovery results. No assertion, suite or required audit was removed.

P06 and Section 7 distinguish host-sized local command concurrency from live2.
M04/M07/M08 bind concrete selectors, isolation, graph readiness and immediate
capacity refill; economical sharding preserves discovery and fixtures. P13 reviews
local-capacity assumptions, budgets and unjustified serialization. Existing
terminal exits, complete feasible collection, cause-group repairs and affected-only
reruns remain binding. The host sizing formula is a dispatch prerequisite, not a
claim that unittest or the frozen harness gained an automatic scheduler.

Primary Claude was attempted in each planning-review round and returned API429
session capacity, not an OAuth failure. The mapped Terra/xhigh reviewer completed
both rounds on thread 01a0b323-6e2d-7d02-95b4-b08dad69d629. Evidence is in
`.plans/addendum3-v3.6-local-concurrency/` and the review worktree named above.
The failed first follow-up launcher receipt is retained: missing prompt_sha256
was corrected before the successful same-thread launch; it was not a review round.

SHA-256 comparison against this amendment's pre-edit snapshot preserves all six
STEP files, modules M01/M02/M03/M05/M06/M10 and the user-owned role mapping exactly.
Completed steps, Series9 ledger597 (68 PASS / 28 FAIL), published checker698 evidence
and pending product/asset review decisions retain their status. No product test,
worker recovery, integration or live matrix was launched by this planning update.
Final structural/format checks are recorded with the amendment evidence.

PLAN_STRUCTURE=VALID
