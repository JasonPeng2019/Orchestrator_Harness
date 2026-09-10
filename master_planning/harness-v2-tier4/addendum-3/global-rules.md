# Harness v2 Tier 4 - Addendum 3 - Global Workflow Rules

## 9. Global workflow policies and exceptions

### P01 Ownership and decisions

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Any activation, finding pool, conflict, role change, integration, live attempt, acceptance, or retirement decision | ROOT must author every complete card, preserve the directive hierarchy, decide all cross-lane routes, and never delegate task meaning, scope, success, acceptance, or self-dispatch authority | One already-declared edge, verdict, or exact incomplete fact | Retain only a result consumed by a later decision | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P02 Context and thread lifetime

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A workflow role starts or resumes an unaccepted logical task | Supply one bounded 20-field card that concretely fixes the problem, desired result, behavior/proof targets, target and protected scope, required and forbidden changes, inputs, checks, acceptance, pitfalls, stop routes, lane ID, Git-worktree ID, process-tree ID, provider-invocation ID, and handoff ID. A worker executes that contract, reports an insufficiency or contradiction, and terminates at each decision boundary; it never reconstructs missing semantics or self-dispatches. Logical tasks are unbounded, but every role launch must copy all current invocation_binding.config_overrides from its selected mapping entry into the frozen-controller invocation and read them back, including the mapped automatic-compaction threshold; retain native compaction rather than replacing it with an agent deadline or a task restart. Recheck and retry the mapping's primary at every new lane, module, and launch. Use the fallback only for that launch after the primary reports a compute/capacity limit or ROOT proves a current external impossibility by trying and reading back every concrete in-scope launch, authentication, configuration, and command workaround; ordinary command, policy, permission, configuration, authentication, result, or task failures remain primary-route diagnosis, not fallback eligibility. Prefer the active invocation only while available and still selected by the user; otherwise dispatch the same role from a structured handoff with accepted state and the first unresolved action. Immediately after every completed MI and before a planned context transfer, refresh HANDOFF.md with exact source, accepted state, first unresolved action and old/new invocation correlation. Compaction preserves the same logical task and never justifies fallback or replay of accepted work. | Terminal worker handoff followed by a separate ROOT decision/card. | Old/new invocation IDs, primary attempts, workaround/readback evidence, qualifying external cause, fallback outcome, and handoff ID when continuity changes | MI-NORMAL-PRODUCT, MI-NORMAL-VERIFY-ASSETS, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-INTEGRATE, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX |

### P03 Failure-case selection

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Before a high-coupling writer, review, safeguard, or real attempt is dispatched | Select realistic late-cost cases across target identity, grammar and paths, concurrency, lifecycle and cleanup, rollback, compatibility removal, external resources, truthful results, and usability; bind each selected case to a requirement, trigger, invariant, oracle, and owner | Complete card or exact insufficiency | Put selected cases in the owning card; create no generic checklist | MI-NORMAL-PRODUCT, MI-NORMAL-VERIFY-ASSETS, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX |

### P04 Check selection and green credit

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A deterministic campaign starts, resumes, or consumes a changed candidate | Use the checkpoint and conservative input map, including its first unresolved unit. Continue every runnable unit after ordinary failure and preserve unaffected PASS. Series 1 starts from a complete pool and one scoped correction, runs changed-source compile plus the motivating test, performs independent review and separate integration, retains reusable smoke credit, records concrete saved work, and exits to the ROOT-selected progress bound. Series 2 joins every accepted Series 1 exit at that progress bound, calculates invalidation, begins the remaining execution set at its earliest required unit, preserves unaffected PASS, records saved work, and continues the normal successor. The bounded-command manifest currently selects zero finite fragments, so target checks use their native commands; agent launches remain outside bounded execution. Treat unexecuted macOS/Linux matrix cells as recorded native gaps, outside the currently runnable execution set under BOUND-014. Preserve their unverified status and continue all independent Windows units; classify real code defects discovered through portable analysis and repair them even when their native platform cannot run. | Complete feasible unit pool or an exact prerequisite-blocked unit record. | Checkpoint stores unit state, consumed inputs, first unresolved unit, Series 1 smoke credit, and Series 2 invalidation | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-FL2-S1-PRODUCT-REVIEW, MI-FL2-S2-PRODUCT-RECONCILE, MI-FL2-S2-ASSET-RECONCILE, MI-NORMAL-FINAL-ASSURANCE, MI-FL2-S2-ASSURANCE-RECONCILE, MI-NORMAL-LIVE-READINESS, MI-FL2-S2-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

### P05 Review classes and invalidation

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A reviewable product, asset, repair, or final tip freezes | Declare INITIAL_IMPLEMENTATION, AFFECTED_REPAIR, or FINAL_PRODUCT; bind one exact revision, requirements, invariants, watch areas, protected scope, materiality threshold, output shape, and handoff while leaving findings open | Complete assigned surface, including zero findings | Review result is bound to its frozen tip; changed consumed meaning invalidates only affected review credit | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-FL2-S1-ADMISSION-REVIEW, MI-FL2-S1-PRODUCT-REVIEW, MI-FL2-S1-ASSET-REVIEW, MI-FL2-S1-INTEGRATION-REVIEW, MI-FL2-S1-ASSURANCE-REVIEW, MI-FL2-S1-LIVE-REVIEW, MI-NORMAL-FINAL-ASSURANCE |

### P06 Parallel checks and results

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Independent review and deterministic checking consume the same frozen input | Give each member a distinct lane, worktree, cache, and result root; launch both before awaiting either; let all feasible paths finish; join exactly once | One complete campaign pool | Preserve each member handoff and the single joined result | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

### P07 Finding pooling and material repair

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | M04, M07, or M09 returns terminal findings | Build one complete pool, deduplicate once, classify once, and send each compatible material group to its declared same-owner correction path; split only incompatible owners, source contexts, or acceptance criteria. Every step carries a configured FAST_LANE_V2 Series 1 path with a complete pool, deterministic correction, motivating test, changed-source compile, independent review, separate integration, and retained smoke credit. Before another assurance run, join every accepted Series 1 exit once at the ROOT-selected current progress bound; its configured Series 2 path calculates invalidation, preserves unaffected PASS, runs the earliest required remaining work, records saved work, and continues the normal successor. A false activation predicate routes that event through normal R15 classification without altering either configured fast contract | Accepted result, one concrete repair card, or exact incomplete claim | Joined finding pool plus preserved/invalidated credit | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-MATRIX, MI-FL2-S1-PRODUCT-PATCH, MI-FL2-S1-ASSET-PATCH, MI-FL2-S1-ASSURANCE-PATCH, MI-FL2-S1-LIVE-PATCH, MI-FL2-S2-PRODUCT-RECONCILE, MI-FL2-S2-ASSET-RECONCILE, MI-FL2-S2-ASSURANCE-RECONCILE, MI-FL2-S2-LIVE-RECONCILE |

### P08 Test-only correction

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A failed asset, fixture, runner, metadata, test-code, or expected literal may be wrong | Prove the correction preserves scenario, required behavior, oracle, assertion strength, and coverage; authorize only the known asset change and exact affected rerun. Production source, policy, contract, locked configuration, and expected behavior must not change | Return to M05 classification after one terminal correction handoff and affected rerun | Preserve unrelated PASS results and record the deterministic admission basis | MI-NORMAL-VERIFY-ASSETS, MI-FL2-S1-ASSET-PATCH, MI-FL2-S1-ASSURANCE-PATCH, MI-FL2-S1-LIVE-PATCH, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P09 Administrative recovery

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A report, schema, path, runner, environment, supervision, result-shape, or cleanup fault occurs | Classify it as administrative/support; reconstruct or correct only when an exact consumer still needs it and correction is cheaper than recording the limitation. Reread the bounded-command manifest before commands; its current selection contains zero finite fragments. Preserve product facts and advance every nonconsumer | Corrected required fact or terminal recorded limitation | Exact support-dependent claim and affected consumers | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-INTEGRATE, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT |

### P10 Semantic acceptance

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A producer, campaign, integration, assurance, or live pool reaches ROOT | Validate shape without equating shape with success; decide behavior from requirements and observations; emit exactly ACCEPTED, ACCEPT-WITHIN-TOLERANCE with explicit rationale, CONTINUE only for a failed or undecidable required product criterion, or INCOMPLETE. Apply BOUND-014 to final acceptance: decide the executable implementation/audit/Windows scope separately from cross-platform qualification; retain the two native gaps and advance EDGE-007 after executable criteria pass. A Windows failure or undecidable Windows result keeps its consuming Windows criterion failed or incomplete. | One verdict or one separately authored correction card. | Durable verdict only when a downstream consumer requires it | MI-NORMAL-PRODUCT-VERDICT, MI-FL2-S2-PRODUCT-VERDICT, MI-FL2-S2-ASSET-VERDICT, MI-FL2-S2-ASSURANCE-VERDICT, MI-FL2-S2-LIVE-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P11 Full-safeguard scope

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | The integrated release unit reaches STEP-005 | Run the required FINAL_PRODUCT audit rounds and CHECK-U1 through CHECK-U5 plus CHECK-FULL-SUITE against the same revision. Each unit owns its source, configuration, runner, environment, prerequisites, dependents, checkpoint state, and ordinary-failure continuation; complete all feasible units and join once. On Series 2 re-entry, form the failed, unresolved, change-affected, or uncertain set from the conservative input map and begin at its earliest required unit without replaying unaffected PASS. REQ-021 requires CHECK-AUDIT-INITIAL and a separately dispatched CHECK-AUDIT-FOLLOWUP after ROOT dispositions, even when the initial audit finds zero issues. Review actual implementation and relevant tests/records against Parts I-XIX as amended by SRC-009; admit only direct requirements, plainly broken flows or demonstrated obvious-design violations. Each finding must cite requirement, code, minimal failure sequence, smallest correction and why it is required; label missing native proof separately. ROOT reads each finding and records Valid, Invalid/overcorrected or Needs evidence with rationale; only valid findings enter repair. Resolve Needs evidence through focused code/test evidence before clearing its consuming criterion; implement and verify every valid finding or retain a specific operator-authorized deferral. Repeat until a follow-up has no undispositioned valid gaps or the operator explicitly defers a specific item. Reviewers advise and never veto. Finish each pool, integrate admitted repairs, and re-enter M07 for uncredited/invalidated audit and safeguard units; a follow-up due solely to this rule does not invent a product defect or trigger M02. Only ROOT grants live admission. | Complete final pool for M05. | One checkpoint with first unresolved unit and conservative input map | MI-NORMAL-FINAL-ASSURANCE, MI-FL2-S2-ASSURANCE-RECONCILE |

### P12 External authorization and rehearsal

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | STEP-006 would consume a native platform runner, real installed target CLI, or user credential | Require the exact native identity only for the platform currently being executed, applicable recorded provider authority, current target/config identity, an unconflicted claim, BOUND-013 confinement, REQ-021 audit clearance and current M08 readiness. Windows is admitted without macOS/Linux runners under BOUND-014; record those two gaps and keep executing all available units. Reuse the recorded provider authorization after scope comparison; ask only for genuinely new external authority. M08 never counts as product proof. M09 serializes platform and provider target sets, starts independent observation first, records each unit's consumed runner/target/resource state, and retains cleanup facts. ROOT owns checkpoints and resumes only when that consumed state is verified unchanged; otherwise it closes the attempt safely and separately authorizes the affected declared work. Maintain one complete feature/command/provider/profile/platform map. Every real scenario retains actual prompt, provider/model identity, transcript/tool activity, changes, result, hook/queue evidence and ROOT response; label expectations Observed, Not observed or Deviation. A prompt, file existence, mock or authentication probe is never native proof. No worker silently fixes an agent result to create PASS. Live failures finish all feasible independent units, close safely, return to M05, repair through the source owner and repeat affected observation with a separate ROOT card. | Authorized terminal attempt or exact incomplete platform/external claim. | Readiness result, attempt ID, claim ID, runner and target identities, observer result, checkpoint, and cleanup state | MI-NORMAL-LIVE-READINESS, MI-FL2-S2-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

### P13 Gate/loop sizing, health, and topology reassessment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A gate is designed, a result pool crosses its boundary, or observed work exceeds the expected range and another material cycle is required | Keep each gate to one repairable product family or exact operation. Batch compatible findings, preserve unaffected credit, stop on success, unrecoverable error, or stall, and reassess module choice, card size, review surface, and role allocation before another material launch; never use an arbitrary iteration cap | Same graph, prospectively split/merged unaccepted graph, or plan amendment | Record only a changed topology decision and its affected edges | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-INTEGRATE, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P14 Exception classes

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A proposed route is outside the declared material, test-only, administrative, readiness, live-harm, or operation-boundary behavior | Stop and amend the plan before use; this project declares zero preauthorized exception classes | Validated plan amendment or INCOMPLETE | Preserve all unaffected accepted results | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-INTEGRATE, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

| Exception ID | Affected policy | Exact trigger | Decision owner | Allowed alternate action | Required confirmation | Preserved results | Invalidated results | Scope | Expiry |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | No exception class is selected because every anticipated route is an ordinary classified path | ROOT | No alternate action is authorized | A new route requires a validated plan amendment | All unaffected accepted results | Only inputs changed by the amendment | No current execution scope | Ends when this plan version is replaced |

### P15 Stop and live-harm containment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Observed wrong-target or unauthorized live action, lost process/resource containment, or irreversible corruption of information needed for judgment | Stop the exact identified process tree or attempt, preserve only diagnosis/recovery facts, verify containment and cleanup by runtime IDs, then classify support impact. Ordinary failures and findings must continue to the complete pool | Verified containment or terminal-visible cleanup uncertainty | Exact process, attempt, lane, worktree, claim, and affected-resource identities | MI-NORMAL-LIVE-READINESS, MI-FL2-S2-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |
