# Modular Execution Plan Template

This is the exact output skeleton for `design-project-topology`. It defines document shape, not a
default workflow. Module decisions and graph edges must be derived from the project.

## Contents

1. Authoring rules
2. Reference conventions
3. Exact plan skeleton
4. Module-instance block
5. Structural validation definitions

## 1. Authoring rules

1. Copy only the skeleton beginning with `# {{PROJECT_NAME}} - Modular Execution Plan` into the
   requested output file. Do not include this reference's introduction or contents list.
2. Preserve Sections 0-16, exact heading text, table headers, policy order, module-instance heading
   order, local-card field order, and structural-check IDs.
3. Replace every `{{UPPER_SNAKE_TOKEN}}` with project-specific content. Delete every line beginning
   `TEMPLATE NOTE:`. The validator rejects remaining tokens or notes.
4. Repeat table rows and module blocks only for real project items. Use the reference labels below only
   where cross-references make the plan clearer. Do not create labels, records, or tracking machinery
   merely because the template permits them.
5. Keep a required table even when its feature is inapplicable. Insert one row whose ID and applicable
   cells are `N/A`, and give the reason in the decision/reason cell. Never use N/A for required
   coverage, module-manifest rows, role resolution, rule mapping, or validation checks.
6. A table row must contain one decision. Put detailed executable behavior in its owning policy or
   module instance, then reference its label elsewhere when a cross-reference is useful.
7. The generated plan must contain no concrete provider, model, reasoning-effort, or service-tier
   selection. Those values live only in the separate canonical role-model mapping.
8. Classify every gate as `PRODUCT` or `OPERATION_BOUNDARY` by what failure disproves, not by whether
   the step is required. A product gate decides observable behavior, contract, capability, or
   correctness and may loop only for a failed or genuinely undecidable required product criterion. A
   required allocation, integration-coordinate mutation, deployment, promotion, readback, cleanup, or
   retirement is still an operation boundary when its failure leaves accepted behavior intact. An
   operation boundary may hold only its exact operation/resource and must leave every independent
   successor default-forward.
9. In each gate row, make those bounds mechanically visible. A `PRODUCT` continuation cell must say
   `only` and name the `required product` criterion that `failed` or is `undecidable`; its blocking scope
   must say `only`. An `OPERATION_BOUNDARY` scope must say `only` and `never product`, its continuation
   cell must say `No product loop`, and its failure target must not name M02/material/product repair.
   Every default-forward cell must name the successor/terminal action that still advances.
10. Keep logical-task continuity separate from persistence of a concrete provider invocation. P02 and
    every executable card must keep the functional role, bounded card, accepted state, complete
    accepted results, and first unresolved action continuous within one unaccepted task. They must prefer
    reuse of the active invocation only when it remains available and the current mapping and user
    direction still select it. They must instead require a recorded structured handoff when the user
    changes subagent/provider/allocation or the invocation cannot resume. Neither case by itself
    invalidates product credit, restarts completed work, or requires a product loop.

11. P02/P04/P09 must adopt the repository's discovered bounded-execution policy and mechanical
    launcher boundary for the orchestrator and every agent or nested subagent. Plans must name behavior and discovered
    sources, not mandate `.codex`, `.claude`, or another provider's filenames. Each check/card must
    carry a realistically calibrated expected upper bound, bounded cleanup allowance, computed maximum
    lifetime and basis, heartbeat no greater than 60 seconds, terminal
    result path, exact cleanup expectation, and timeout support-classification route. When an
    available provider hook can inspect commands, it must reject every direct invocation inside the
    declared launcher boundary without attempting semantic test or framework detection.
12. Assign an ID to every orchestrator/root, agent, or subagent process/process tree; provider
    invocation/session/thread; handoff; lane; claim/lock; and Git worktree. These are runtime instances
    whose exact lifecycle must be correlated. This mandatory rule does not make identity a general plan
    property. Plan-local labels are optional cross-references, and ordinary features, files, sources,
    caches, configurations, facts, checks, results, and non-agent workspaces need no ID merely because
    they exist. Add a revision, hash, receipt, immutable record, or evidence file only when a named
    operation or decision requires it. Hashes are reserved for byte-integrity or content comparison;
    immutability is reserved for records or history that must not change after acceptance.
13. Treat every executable card as a complete ROOT-authored dispatch contract. ROOT must state the
    problem/activation fact, desired result, exact behaviors or proof targets, target and protected
    surfaces, required and forbidden changes, authoritative inputs, checks, acceptance/tolerances,
    realistic pitfalls, outputs, failure/stop routes, and next handoff. The worker chooses mechanics
    only inside those bounds and returns any material omission or contradiction to ROOT. A review or
    audit card leaves findings open but still fixes the frozen input, class, investigation surface,
    governing invariants, watch areas, exclusions, materiality threshold, output, and handoff.
14. Interpret every worker-facing `define`, `select`, `choose`, `classify`, `resolve`, `decide`,
    `authorize`, `continue`, `resume`, `start`, or equivalent action as execution of a ROOT-owned
    decision or exact ROOT-supplied deterministic rule. It must not transfer task semantics. An
    undeclared behavior, test meaning, oracle, conflict, retry/new attempt, acceptance choice, scope
    expansion, or next edge returns to ROOT. Review/audit may determine findings independently only
    within its concrete assigned investigation boundary.
15. For every expensive multi-check gate, accumulated safeguard, or stateful practical/hardware
    attempt, P04/P11/P12 must name independently runnable check units,
    conservative source/configuration/runner/environment/external-state inputs, checkpoint owner,
    PASS reuse condition, first-unresolved checkpoint field, earliest-required-unit execution rule,
    and ordinary-failure continuation rule. The required execution set contains failed, unresolved,
    change-affected, and uncertain units; it begins with its earliest member and never replays an
    unaffected PASS. A checkpoint records only facts a later selector needs; a revision or external
    attempt state is used only when needed to decide reuse. Put
    `CHECKPOINTED_VERIFICATION_V1` in Section 0 when this protocol is selected; it is a plan
    protocol selector, not an identity or evidence artifact. P07 names its compatible-finding batch
    and the condition for resuming assurance.
16. A selected `FAST_LANE_V2` must begin from the originating check tranche's complete feasible pool
    containing one scoped compatible correction objective. It must name its observed defect,
    deterministic motivating test, changed-source compile smoke, frozen-tip review, separate
    integration, reusable smoke credit, and remaining incremental verification route. It must say why
    uncertain/broad/external work and a broader compatible batch are excluded.
17. A selected M04/M07 checking campaign or M09 practical attempt must finish every feasible check
    after ordinary failures, then return one complete pool. P07 must batch compatible material
    findings before another assurance run.

## 2. Reference conventions

Use these labels when the plan needs unambiguous cross-references. They are document references, not
claims of runtime identity or requirements to create persistent records. The numeric width is formatting,
not a count limit.

| Family | Meaning | Example |
|---|---|---|
| `SRC-*` | Authority/source | `SRC-001` |
| `OUT-*` | Acceptance outcome | `OUT-001` |
| `BOUND-*` | Exclusion/authorization boundary | `BOUND-001` |
| `REQ-*` | Atomic requirement | `REQ-001` |
| `DEL-*` | Coherent deliverable | `DEL-001` |
| `MI-*` | Selected module instance | `MI-001` |
| `EDGE-*` | Typed graph edge | `EDGE-001` |
| `PG-*` | Parallel work group | `PG-001` |
| `JOIN-*` | Join | `JOIN-001` |
| `GATE-*` | Decision/gate boundary | `GATE-001` |
| `LOOP-*` | Same-task repair return | `LOOP-001` |
| `LANE-*` | Executable lane | `LANE-001` |
| `LOCK-*` | Claim/lock | `LOCK-001` |
| `CHECK-*` | Named check when cross-reference is useful | `CHECK-001` |
| `HANDOFF-*` | Runtime handoff; always identified | `HANDOFF-001` |
| `RESULT-*` | Durable result reference only when a consumer needs one | `RESULT-001` |
| `ALLOC-*` | Source allocation | `ALLOC-001` |
| `RETIRE-*` | Retirement action | `RETIRE-001` |
| `EXT-*` | External/practical decision | `EXT-001` |
| `REL-*` | Integration/release decision | `REL-001` |
| `EXC-*` | Predeclared exception | `EXC-001` |
| `LEDGER-*` | Tolerance/unresolved/out-of-scope item | `LEDGER-001` |

## 3. Exact plan skeleton

# {{PROJECT_NAME}} - Modular Execution Plan

## 0. Plan contract and status

| Field | Value |
|---|---|
| Plan ID | {{PLAN_ID}} |
| Plan version | {{PLAN_VERSION}} |
| Status | {{DRAFT_OR_VALIDATED}} |
| Decision owner | {{DECISION_OWNER_ROLE}} |
| Verification protocol | {{CHECKPOINTED_VERIFICATION_V1_OR_NA}} |
| Operative document boundary | {{OPERATIVE_AND_SUPERSEDED_BOUNDARY}} |
| Change procedure | {{CHANGE_AND_AFFECTED_WORK_PROCEDURE}} |
| Definition of valid | {{SEMANTIC_AND_STRUCTURAL_VALIDITY_DEFINITION}} |

Module catalog order is not execution order. Only Section 8 edges define runtime order.

## 1. Inputs, authority, and directive hierarchy

| Source | Authority | Path/reference | Supplies | Conflict rule |
|---|---|---|---|---|
| SRC-001 | {{AUTHORITY_CLASS}} | {{SOURCE_PATH_OR_REFERENCE}} | {{FACTS_SUPPLIED}} | {{CONFLICT_RULE}} |

TEMPLATE NOTE: Add one `SRC-*` row per operative/reference source. Put the canonical role-model mapping
path in exactly one row and nowhere else in the plan.

| Layer | Authority | May define | Must not override |
|---|---|---|---|
| 1 | Direct user instructions and goal/spec | Required outcome and authority | N/A |
| 2 | This execution plan | Global workflow and selected graph | Layer 1 |
| 3 | Module instance | Its bounded project-specific behavior | Layers 1-2 |
| 4 | Local task card | Authorized task inputs/actions | Layers 1-3 |
| 5 | Handoff/status | Current facts and next authorized edge | Layers 1-4 |
| 6 | Runtime results | Materialized facts needed by a consumer | Any policy layer |
| 7 | Role-model mapping | Concrete launch selection only | Task semantics or graph order |

The plan's ROOT/orchestrator decision owner must author every executable task contract completely
before dispatch. Workers execute and report within the stated problem, objective, desired behavior,
target/protected scope, proof, pitfall, acceptance, and failure boundaries; they do not invent missing
task meaning or authorize their own follow-up edge. Review/audit workers may discover new findings,
but only inside a concretely assigned investigation boundary and without a prescribed conclusion.

Worker implementation discovery is limited to learning how to realize the already-defined result
inside the named source seams. Card insufficiency never authorizes discovery of what the task should
mean. Any specialized recipe verb that appears to choose behavior, tests, conflicts, assurance paths,
retries, attempts, acceptance, or routing must name ROOT's prior decision or deterministic criterion;
otherwise the card is not dispatchable.

## 2. Goal, exclusions, and acceptance outcomes

Goal: {{FAITHFUL_GOAL_TEXT}}

| Outcome ID | Required behavior | Acceptance method | Decision owner | Status |
|---|---|---|---|---|
| OUT-001 | {{OBSERVABLE_REQUIRED_BEHAVIOR}} | {{DECISIVE_CHECK_OR_REVIEW}} | {{OWNER_ROLE}} | {{OPEN_OR_COVERED}} |

| Boundary ID | Type | Included/excluded/authorization condition | Reason | Owner |
|---|---|---|---|---|
| BOUND-001 | {{IN_SCOPE_OR_OUT_OF_SCOPE_OR_AUTHORIZATION}} | {{EXACT_CONDITION}} | {{SOURCE_BACKED_REASON}} | {{OWNER_ROLE}} |

## 3. Requirement coverage map

| Requirement ID | Source | Deliverable ID | Implementation owner | Verification | Acceptance owner | Status |
|---|---|---|---|---|---|---|
| REQ-001 | {{SOURCE_AND_LOCATION}} | DEL-001 | {{ROLE}} | {{CHECK_REVIEW_OR_EXTERNAL_VALIDATION}} | {{ROLE}} | {{STATUS}} |

## 4. Runtime and repository truth

| Capability/action | State | Source of truth | Invocation owner | Preconditions | How confirmed | Fallback |
|---|---|---|---|---|---|---|
| {{CAPABILITY_OR_ACTION}} | {{RUNTIME_ENFORCED_OR_ORCHESTRATOR_ENFORCED_OR_TARGET_TOOL_INVOKED_OR_UNAVAILABLE}} | {{SOURCE_PATH_OR_COMMAND}} | {{ROLE}} | {{PRECONDITIONS}} | {{OBSERVATION_OR_NA}} | {{HONEST_FALLBACK}} |

## 5. Deliverable, dependency, risk, and cost model

| Deliverable ID | Behavioral output | Requirement IDs | Dependencies | Shared seams | Release unit |
|---|---|---|---|---|---|
| DEL-001 | {{INDEPENDENTLY_USEFUL_OUTPUT}} | {{REQ_IDS}} | {{DEL_IDS_OR_NONE}} | {{SHARED_INVARIANTS_AND_INTERFACES}} | {{RELEASE_UNIT}} |

| Deliverable ID | Realistic failure | Impact | Coupling | Expected range | Expensive operations | Cheapest adequate topology | Why |
|---|---|---|---|---|---|---|---|
| DEL-001 | {{LATE_EXPENSIVE_FAILURE}} | {{PRODUCT_IMPACT}} | {{COUPLING}} | {{DURATION_RANGE}} | {{EXPENSIVE_ACTIONS_OR_NONE}} | {{MINIMAL_MODULE_COMPOSITION}} | {{PROJECT_SPECIFIC_REASON}} |

## 6. Workflow module selection manifest

| Module type | Decision | Instance IDs | Reason | Prerequisite/owner if deferred |
|---|---|---|---|---|
| M01 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M02 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M03 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M04 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M05 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M06 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M07 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M08 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M09 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |
| M10 | {{SELECTED_OMITTED_OR_DEFERRED}} | {{MI_IDS_OR_NA}} | {{PROJECT_SPECIFIC_REASON}} | {{PREREQUISITE_AND_OWNER_OR_NA}} |

## 7. Roles and role-model mapping boundary

| Workflow role | Responsibilities | Pool | Context class | Write authority | Resources | Activation | Lifetime |
|---|---|---|---|---|---|---|---|
| {{ROLE_KEY}} | {{RESPONSIBILITIES}} | {{POOL_SIZE_AND_REASON}} | {{BOUNDED_CONTEXT_CLASS}} | {{WRITE_AUTHORITY}} | {{RESOURCE_SCOPE}} | {{ACTIVATION_CONDITION}} | {{LOGICAL_TASK_LIFETIME_AND_INVOCATION_HANDOFF_RULE}} |

| Resolution rule | Unknown-role behavior | Mapping-update behavior |
|---|---|---|
| {{RUNTIME_RESOLUTION_RULE}} | {{FAIL_CLOSED_BEHAVIOR}} | {{NO_WORKFLOW_EDIT_REQUIRED_BEHAVIOR}} |

## 8. Composed execution graph and critical path

| Edge ID | From/output | To/input | Condition | Serial/parallel | Join ID | Failure branch |
|---|---|---|---|---|---|---|
| EDGE-001 | {{MI_ID_AND_OUTPUT}} | {{MI_ID_AND_INPUT}} | {{EXACT_CONDITION}} | {{SERIAL_OR_PARALLEL}} | {{JOIN_ID_OR_NA}} | {{DECLARED_FAILURE_ROUTE}} |

| Parallel group | Shared input | Member instance IDs | Writable-root isolation | Launch rule | Join ID | Serial exception |
|---|---|---|---|---|---|---|
| PG-001 | {{SHARED_INPUT}} | {{MI_IDS}} | {{DISJOINT_ROOTS_OR_LOCK}} | {{LAUNCH_ALL_BEFORE_WAIT}} | {{JOIN_ID}} | {{EXCEPTION_ID_OR_NA}} |

| Path ID | Ordered instance/edge IDs | Expected range | Overlap | Expensive operations | Why critical |
|---|---|---|---|---|---|
| {{PATH_ID}} | {{ORDERED_IDS}} | {{DURATION_RANGE}} | {{PARALLEL_OVERLAP}} | {{COUNT_AND_ACTIONS}} | {{DEPENDENCY_REASON}} |

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-001 | {{PRODUCT_OR_OPERATION_BOUNDARY}} | {{SHARED_INPUT}} | {{ONE_GATE_QUESTION}} | {{MI_IDS}} | {{COHERENT_FAILURE_FAMILY}} | {{EXACT_OUTCOME_OPERATION_OR_RESOURCE_ONLY}} | {{REQUIRED_PRODUCT_CRITERION_OR_NARROW_NONPRODUCT_CONTINUATION_RULE}} | {{SATISFIED_SUCCESSOR_EDGE}} | {{SAME_LOGICAL_TASK_ROLE_OR_EXACT_BLOCK_TARGET}} | {{SAVED_REPEAT_COST}} | {{ONE_REPAIR_OBJECTIVE_PROOF}} | {{AFFECTED_AND_PRESERVED_RESULTS}} | {{OBSERVED_TRIGGER}} |

## 9. Global workflow policies and exceptions

TEMPLATE NOTE: Preserve these P01-P15 headings in order. Put one or more rows under each table. Cite
selected module IDs; use N/A only when the policy genuinely has no selected-module consumer.

### P01 Ownership and decisions

TEMPLATE NOTE: Include a ROOT/orchestrator row making task definition non-delegable: before dispatch,
ROOT must concretely name the problem/activation fact, desired result, exact behavior/proof targets,
target and protected boundaries, required/forbidden changes, pitfalls, acceptance/tolerances, and
handoff/next-edge decision. For review/audit, ROOT must bound the investigation without prescribing
its findings.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P02 Context and thread lifetime

TEMPLATE NOTE: State that an insufficient card permits only a bounded insufficiency report and
terminal handoff, not worker reconstruction of missing goals, desired behavior, change/protected
scope, test meaning, oracle, acceptance, or routing. Require a separate ROOT decision/card for any
nontrivial conflict, changed proof meaning, new attempt, or follow-up edge.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P03 Failure-case selection

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P04 Check selection and green credit

TEMPLATE NOTE: For a multi-check gate, accumulated safeguard, or stateful practical/hardware attempt,
state the unit/input map, checkpoint and resume owner, PASS reuse rule, the failed/unresolved/affected/
uncertain execution set beginning at its earliest unit, and continuation after ordinary failure. If
`FAST_LANE_V2` is selected, state its complete pool prerequisite, compile-plus-motivating-test smoke,
reusable smoke credit, and retained incremental checks.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P05 Review classes and invalidation

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P06 Parallel checks and results

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P07 Finding pooling and material repair

TEMPLATE NOTE: Require every feasible selected result before classification. State how compatible
material findings are batched into one writer tranche and when differing owners/source contexts/criteria
require separate tranches. Do not permit another safeguard merely because one member was repaired.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P08 Test-only correction

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P09 Administrative recovery

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P10 Semantic acceptance

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P11 Full-safeguard scope

TEMPLATE NOTE: For each selected accumulated safeguard, name its check units, conservative input map,
checkpoint owner, first-unresolved checkpoint field, earliest-required failed/unresolved/affected/
uncertain execution route, and terminal complete-pool behavior.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P12 External authorization and rehearsal

TEMPLATE NOTE: For stateful M09 work, state each practical unit's consumed target/resource state,
PASS reuse condition, checkpoint/resume owner, and the safe close-and-ROOT-reauthorization route when
that state no longer holds.

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P13 Gate/loop sizing, health, and topology reassessment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

### P14 Exception classes

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{TRIGGER}} | {{MANDATORY_ACTION_OR_NA}} | {{EXIT_CONDITION}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

| Exception ID | Affected policy | Exact trigger | Decision owner | Allowed alternate action | Required confirmation | Preserved results | Invalidated results | Scope | Expiry |
|---|---|---|---|---|---|---|---|---|---|
| EXC-001 | {{POLICY_ID}} | {{EXACT_TRIGGER}} | {{OWNER}} | {{BOUNDED_ACTION}} | {{CONFIRMATION_OR_NA}} | {{PRESERVED}} | {{INVALIDATED}} | {{SCOPE}} | {{EXPIRY}} |

### P15 Stop and live-harm containment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| {{OWNER}} | {{EXACT_LIVE_HARM_TRIGGER}} | {{CONTAIN_PRESERVE_AND_CLASSIFY}} | {{SAFE_BOUNDARY}} | {{OPTIONAL_PATH_RECORD_OR_NA}} | {{MI_IDS_OR_NA}} |

## 10. Lane, resource, result, and handoff manifest

| Lane ID | Module instance | Role | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| LANE-001 | {{MI_ID}} | {{ROLE}} | {{ACTIVATION}} | {{ROOT_OR_READ_ONLY}} | {{CONSUMER}} | {{COMPLETION}} | {{FAILURE_ROUTE}} |

| Claim/lock ID | Resource | Owner | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| LOCK-001 | {{RESOURCE}} | {{OWNER}} | {{ACTIVATION}} | {{ROOT_OR_NA}} | {{CONSUMER}} | {{RELEASE_CONDITION}} | {{FAILURE_ROUTE}} |

| Check | Proves | Dependencies | Result owner | Reuse condition | Rerun route | Result path if needed | Failure route |
|---|---|---|---|---|---|---|---|
| CHECK-001 | {{ACCEPTANCE_CLAIM}} | {{DEPENDENCIES}} | {{OWNER}} | {{WHEN_PRIOR_PASS_REMAINS_USEFUL}} | {{AFFECTED_ONLY_ROUTE}} | {{OPTIONAL_PATH_OR_NA}} | {{FAILURE_ROUTE}} |

| Result/handoff ID | Producer | Consumer | Path if durable | Correlation needed | Publication rule | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| HANDOFF-001 | {{PRODUCER}} | {{CONSUMER}} | {{OPTIONAL_PATH_OR_NA}} | {{PROCESS_THREAD_HANDOFF_CORRELATION}} | {{PUBLICATION_RULE}} | {{COMPLETION}} | {{FAILURE_ROUTE}} |

TEMPLATE NOTE: Use one row with a mandatory `HANDOFF-*` ID for every handoff. Use a `RESULT-*`
reference only when a durable result has a named consumer; an ordinary output needs no result ID.

| Source allocation ID | Mode | Source/worktree | Writer | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| ALLOC-001 | {{WORKTREE_VIEW_OR_CURRENT_WRITER}} | {{SOURCE_OR_WORKTREE_ID_WHEN_REQUIRED}} | {{ROLE_OR_NONE}} | {{ROOT}} | {{CONSUMER}} | {{COMPLETION}} | {{FAILURE_ROUTE}} |

| Retirement ID | Target | Owner | Activation | What must be retained | Completion condition | Recovery visibility | Failure route |
|---|---|---|---|---|---|---|---|
| RETIRE-001 | {{LANE_ROOT_OR_RESOURCE}} | {{OWNER}} | {{ACTIVATION}} | {{REQUIRED_RESULTS_OR_CHANGES_OR_NONE}} | {{SAFE_TERMINAL_STATE}} | {{ARCHIVE_OR_RECOVERY_PATH}} | {{FAILURE_ROUTE}} |

## 11. Module instances

TEMPLATE NOTE: Repeat the exact block in Section 4 of this reference once for every selected `MI-*`,
ordered by `DEL-*` and then topologically for presentation. Delete this note and the placeholder block
after instantiating all selected modules.

{{MODULE_INSTANCE_BLOCKS}}

## 12. External and practical validation

| Decision ID | Module type | Decision | Authority/resource | Synthetic proof | Real proof | Owner | Failure route |
|---|---|---|---|---|---|---|---|
| EXT-001 | {{M08_OR_M09}} | {{SELECTED_PROFILE_OR_OMITTED_REASON}} | {{AUTHORITY_AND_RESOURCE_OR_NA}} | {{READINESS_CLAIM_OR_NA}} | {{REAL_ACCEPTANCE_RESULT_OR_NA}} | {{OWNER}} | {{FAILURE_ROUTE}} |

## 13. Integration, safeguard, promotion, rollback, and retirement

| Decision ID | Module type | Decision | Accepted input | Action/order | Checks | Promotion/rollback/retirement | Owner |
|---|---|---|---|---|---|---|---|
| REL-001 | {{M06_OR_M07}} | {{SELECTED_PROFILE_OR_OMITTED_REASON}} | {{ACCEPTED_MI_OUTPUT_OR_NA}} | {{ORDERED_ACTION_OR_NA}} | {{AFFECTED_OR_FULL_CHECKS_OR_NA}} | {{COORDINATE_AND_ROLLBACK_OR_NA}} | {{OWNER}} |

## 14. Tolerances, unresolved decisions, and out-of-scope ledger

| Item ID | Type | Exact condition | Consequence | Owner | Resolution boundary |
|---|---|---|---|---|---|
| LEDGER-001 | {{TOLERANCE_UNRESOLVED_OR_OUT_OF_SCOPE}} | {{EXACT_CONDITION}} | {{CONSEQUENCE}} | {{OWNER}} | {{WHEN_AND_HOW_RESOLVED}} |

## 15. Rule application matrix

| Rule ID | Plan location | Applied behavior or justified N/A |
|---|---|---|
| R1 | {{LOCATION}} | {{BEHAVIOR}} |
| R2 | {{LOCATION}} | {{BEHAVIOR}} |
| R3 | {{LOCATION}} | {{BEHAVIOR}} |
| R4 | {{LOCATION}} | {{BEHAVIOR}} |
| R5 | {{LOCATION}} | {{BEHAVIOR}} |
| R6 | {{LOCATION}} | {{BEHAVIOR}} |
| R7 | {{LOCATION}} | {{BEHAVIOR}} |
| R8 | {{LOCATION}} | {{BEHAVIOR}} |
| R9 | {{LOCATION}} | {{BEHAVIOR}} |
| R10 | {{LOCATION}} | {{BEHAVIOR}} |
| R11 | {{LOCATION}} | {{BEHAVIOR}} |
| R12 | {{LOCATION}} | {{BEHAVIOR}} |
| R13 | {{LOCATION}} | {{BEHAVIOR}} |
| R14 | {{LOCATION}} | {{BEHAVIOR}} |
| R15 | {{LOCATION}} | {{BEHAVIOR}} |
| R16 | {{LOCATION}} | {{BEHAVIOR}} |
| R17 | {{LOCATION}} | {{BEHAVIOR}} |
| R18 | {{LOCATION}} | {{BEHAVIOR}} |
| R19 | {{LOCATION}} | {{BEHAVIOR}} |
| R20 | {{LOCATION}} | {{BEHAVIOR}} |
| R21 | {{LOCATION}} | {{BEHAVIOR}} |
| R22 | {{LOCATION}} | {{BEHAVIOR}} |
| R23 | {{LOCATION}} | {{BEHAVIOR}} |
| R24 | {{LOCATION}} | {{BEHAVIOR}} |
| R25 | {{LOCATION}} | {{BEHAVIOR}} |
| R26 | {{LOCATION}} | {{BEHAVIOR}} |
| R27 | {{LOCATION}} | {{BEHAVIOR}} |
| R28 | {{LOCATION}} | {{BEHAVIOR}} |
| R29 | {{LOCATION}} | {{BEHAVIOR}} |
| R30 | {{LOCATION}} | {{BEHAVIOR}} |
| S1 | {{LOCATION}} | {{BEHAVIOR}} |
| S2 | {{LOCATION}} | {{BEHAVIOR}} |
| S3 | {{LOCATION}} | {{BEHAVIOR}} |
| S4 | {{LOCATION}} | {{BEHAVIOR}} |
| S5 | {{LOCATION}} | {{BEHAVIOR}} |
| S6 | {{LOCATION}} | {{BEHAVIOR}} |
| S7 | {{LOCATION}} | {{BEHAVIOR}} |
| S8 | {{LOCATION}} | {{BEHAVIOR}} |
| S9 | {{LOCATION}} | {{BEHAVIOR}} |
| S10 | {{LOCATION}} | {{BEHAVIOR}} |
| S11 | {{LOCATION}} | {{BEHAVIOR}} |
| S12 | {{LOCATION}} | {{BEHAVIOR}} |
| S13 | {{LOCATION}} | {{BEHAVIOR}} |
| S14 | {{LOCATION}} | {{BEHAVIOR}} |
| S15 | {{LOCATION}} | {{BEHAVIOR}} |
| S16 | {{LOCATION}} | {{BEHAVIOR}} |

## 16. Structural validation result

TEMPLATE NOTE: Use the exact V01-V29 definitions in Section 5 of this reference. Replace this token
with all 29 completed rows, delete the note, and end with exactly one terminal marker.

{{STRUCTURAL_VALIDATION_ROWS}}

PLAN_STRUCTURE={{VALID_OR_INVALID}}

## 4. Module-instance block

Use this exact 16-heading block for each selected instance. The first heading plus the 15 subheadings
form the schema. Replace every token and delete every template note.

### {{MI_ID}} - {{MODULE_TYPE}}: {{PROJECT_SPECIFIC_NAME}}

#### Purpose

{{MODULE_TYPE_DELIVERABLE_OBJECTIVE_AND_PAYOFF}}

#### Coverage

{{REQUIREMENT_IDS_AND_ACCEPTANCE_CLAIMS}}

#### Selection basis

{{INCLUDE_CONDITION_BASIS_AND_CHEAPER_ALTERNATIVE_REJECTION}}

#### Owner and roles

{{DECISION_OWNER_EXECUTING_ROLES_POOL_AND_THREAD_RULE}}

#### Preconditions

{{PREDECESSOR_OUTPUTS_SOURCE_AUTHORITY_CAPABILITIES_AND_LOCKS}}

#### Inputs

{{PATHS_OPTIONAL_REQUIRED_REVISIONS_ARTIFACTS_FACTS_AND_MANDATORY_RUNTIME_INSTANCE_IDS}}

#### Local instructions

TEMPLATE NOTE: Use this table for every executable instance. A non-executable decision-only instance
keeps the table and uses reasoned N/A only for task-specific action fields.

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | {{REQUIRED_DOCUMENT_AND_RUNTIME_REFERENCES}} |
| workflow_role | {{ROLE_ONLY}} |
| objective | {{BOUNDED_OBJECTIVE}} |
| why_now | {{ACTIVATION_REASON}} |
| starting_state | {{ROOT_BRANCH_OR_WORKTREE_CURRENT_STATE_PRIOR_RESULTS_AND_CLAIMS}} |
| dependencies_and_predecessor_outputs | {{EXACT_DEPENDENCIES}} |
| working_scope | {{CONCEPTUAL_IN_OUT_AND_EXACT_WRITE_SCOPE}} |
| required_behavior | {{REQUIRED_BEHAVIOR}} |
| initial_entrypoints | {{PATH_REASON_FIRST_ACTION_COUNT_SCORE_AND_JUSTIFICATION}} |
| failure_case_brief | {{REQUIREMENT_TRIGGER_INVARIANT_ORACLE_OWNER_OR_REASONED_NA}} |
| ordered_actions | {{ALL_RECIPE_ACTION_IDS_IN_ORDER_WITH_PROJECT_SPECIFIC_ACTION_TEXT_OR_AUTHORIZED_NA}} |
| allowed_tools_capabilities_resources | {{ALLOWED_SET}} |
| forbidden_actions_and_boundaries | {{FORBIDDEN_SET}} |
| verification | {{SHORTEST_DECISIVE_AFFECTED_CHECKS}} |
| deliverables_and_result_paths | {{OUTPUTS_AND_OPTIONAL_RESULT_PATHS}} |
| acceptance_criteria_and_tolerances | {{CRITERIA_AND_AUTHORIZED_TOLERANCES}} |
| completion_review_owner_and_handoff | {{OWNER_CONSUMER_AND_PUBLICATION_RULE}} |
| failure_classification_and_routes | {{MATERIAL_TEST_ONLY_ADMIN_AND_INCOMPLETE_ROUTES}} |
| thread_resume_and_terminal_rule | {{SAME_LOGICAL_TASK_PREFERRED_INVOCATION_REUSE_STRUCTURED_HANDOFF_AND_ACCEPTED_TERMINAL_RULE}} |
| cited_global_policy_ids_and_exception_ids | {{POLICY_AND_EXCEPTION_IDS}} |

TEMPLATE NOTE: Read these 20 values together as one ROOT-authored dispatch contract. A non-review
worker must be able to execute without discovering the task's problem, goals, desired result,
permitted/protected scope, proof obligations, pitfalls, or success criteria. A review/audit worker
must receive a frozen input, exact investigation surface, governing requirements/invariants, watch
areas, exclusions, materiality threshold, output, and handoff while remaining free to return no
finding or newly discovered in-boundary findings. A material omission, contradiction, bare `N/A`,
`TBD`, `TODO`, `UNKNOWN`, or appeal to worker judgment makes the card undispatchable unless the
selected recipe explicitly permits and explains that N/A.

TEMPLATE NOTE: Audit action verbs as well as fields. A worker may choose implementation mechanics
inside the complete contract, but every semantic `define`, `select`, `resolve`, `continue`, `resume`,
or `start` must point to ROOT's already-stated decision or deterministic rule. M03 behavior/oracle,
M06 conflicts, M07 assurance-path selection, and M09 new attempts may not be delegated. Review/audit
findings remain independent inside the stated boundary.

#### Outputs and results

{{EXACT_OUTPUTS_OPTIONAL_RESULTS_OWNER_AND_WRITE_ROOT}}

#### Concurrency and isolation

{{PARALLEL_GROUP_PEERS_MUTABLE_ROOTS_CACHE_AND_RESULT_SEPARATION}}

#### Resources and side effects

{{CLAIMS_PERMISSIONS_EXPENSIVE_ACTIONS_AND_CLEANUP_OWNER}}

#### Checks and acceptance

{{FOCUSED_CHECKS_CRITERIA_TOLERANCE_AND_ACCEPTING_OWNER}}

#### Failure and exception routes

{{CLASSIFIED_EXITS_AND_PREDECLARED_EXCEPTION_IDS}}

#### Prior results and change effects

{{PRIOR_RESULTS_CHANGED_INPUTS_RERUNS_AND_PRESERVED_WORK}}

#### Repeat, join, and terminal behavior

{{GATE_LOOP_QUESTION_COMPLETE_POOL_RETURN_REPEAT_SUCCESSOR_JOIN_AND_RETIREMENT}}

#### Cost and critical-path effect

{{EXPECTED_RANGE_LAUNCHES_GATES_OVERLAP_AND_CRITICAL_PATH_DELTA}}

## 5. Structural validation definitions

Place these exact rows under Section 16's table header:

`Check ID | Result | Basis`

Every result is `PASS` or `FAIL`. Basis is one concise project-specific pointer or explanation; it does
not require a durable evidence artifact.

Evaluate V10, V13, V14, and V27 under the recipe-verb rule: field presence is insufficient when a
specialized action still asks a worker to decide unstated task semantics. Review/audit finding judgment
is permitted only within its explicit boundary and does not include scope, editing, acceptance, or
routing authority.

| Check ID | Definition |
|---|---|
| V01 | Exact plan title and Sections 0-16 exist once and in order. |
| V02 | Every required table has exact columns and every permitted inapplicable table has one reasoned N/A row. |
| V03 | Every requirement maps to one deliverable, verification path, and acceptance owner. |
| V04 | M01-M10 each have one decision and every selected instance uses the exact 16-heading schema and module recipe. |
| V05 | Every graph edge connects a declared output to a declared input; every fan-out joins or has independently terminal outputs. |
| V06 | No omitted module appears in graph, cards, gates, or handoff routes. |
| V07 | Every non-minimal module and serial edge has a concrete payoff or dependency. |
| V08 | Selected review/check instances on one shared input use a parallel group unless a real dependency or exception is cited. |
| V09 | Every material repair consumes one complete pooled finding set, every feasible selected check continues after ordinary failures, compatible findings batch before another assurance run, and no intermediate repair revision is reviewed. |
| V10 | Every review instance declares class, boundary, scope, shared input, and affected prior results. Its ROOT-authored card fixes the governing requirements/invariants, watch areas, exclusions, materiality threshold, output, and handoff without prescribing findings or allowing silent scope expansion. |
| V11 | Full-safeguard commands occur only in selected M07 instances, each names one release unit, and each expensive multi-check safeguard declares check units, a conservative input map, checkpoint owner, and complete-pool behavior. |
| V12 | A prior PASS is reused only when its declared source/configuration/runner/environment/external inputs and prerequisites are unchanged; the required execution set contains every failed, unresolved, affected, or uncertain unit and begins with its earliest member, while unaffected PASS units are never replayed merely because an earlier unit failed. |
| V13 | Every module instance contains all 20 local task-card fields, all recipe action IDs in order, and applicable global-policy citations. Their material values collectively form a complete ROOT-authored dispatch contract covering the problem, desired result, behavior/proof targets, target/protected scope, required and forbidden changes, authoritative inputs, checks, acceptance, realistic pitfalls, outputs, failure/stop routes, and handoff. |
| V14 | No local instruction changes global scheduling, review, gate, authority, resource, or result-handling rules. No worker is assigned task-definition, scope-definition, success-definition, acceptance, or self-dispatch authority. |
| V15 | Every exception has trigger, owner, action, required confirmation, preserved/invalidated results, scope, and expiry. |
| V16 | Runtime, orchestrator, target-tool, and unavailable capability classes are distinguished. |
| V17 | Stable launcher behavior is not attributed to target work-product code. |
| V18 | Every executable role exists exactly once in the mapping; the plan contains no concrete launch selection and mentions the mapping path once. |
| V19 | Source writers are singular unless proven independence and merge order justify fan-out. |
| V20 | Concurrent result writers have disjoint roots or one correct shared append lock. |
| V21 | Context bounds include necessary seams and every non-maximal entrypoint score is justified. |
| V22 | Failure cases are realistic, requirement-linked, oracle-backed, and not generic hardening. |
| V23 | Test/support/report failures, including a failed strict test-only correction/rerun, return to classification, block only exact consumers, never become material repair without a failed or undecidable product criterion, and activate every independently satisfied successor. |
| V24 | Every gate declares `PRODUCT` or `OPERATION_BOUNDARY` according to the fact its failure disproves, exact blocking scope, continuation/loop eligibility, default-forward edge, and return/block target; no pure allocation/join/deployment/promotion/readback/cleanup/retirement failure is labeled PRODUCT while accepted behavior remains intact; each gate passes aggregation/manageability and explains why it is neither smaller nor larger. |
| V25 | A product loop is entered only for a failed/genuinely undecidable required product criterion; continuation executes from the earliest failed, unresolved, affected, or uncertain action/check in the same logical role/task, reuses the active invocation only when available and still selected or records a structured handoff, preserves unaffected credit, prospectively splits/merges unaccepted work, and never reopens unrelated accepted work. |
| V26 | Cleanup never deletes unpreserved, dirty, live, ambiguous, or unretained state. |
| V27 | Executable instructions contain no banned vague phrase or undefined owner/trigger/action/exit. A worker is never told to discover material task meaning or decide an unstated goal, desired result, boundary, proof obligation, pitfall, or acceptance criterion. |
| V28 | R1-R30 and S1-S16 each map once to behaviorally consistent plan content. |
| V29 | Every process/process tree, agent/subagent invocation/session, handoff, lane, claim/lock, and Git worktree has a runtime ID; ordinary plan content has no ID/hash/receipt/immutable evidence artifact without a named operational need. |

In the generated plan, render:

| Check ID | Result | Basis |
|---|---|---|
| V01 | {{PASS_OR_FAIL}} | {{PROJECT_SPECIFIC_BASIS}} |

TEMPLATE NOTE: Repeat through V29 with the exact definitions above. `PLAN_STRUCTURE=VALID` is permitted
only when all 29 rows say PASS and deterministic validation succeeds.
