# Claude and Qwen Runner Parity - Modular Execution Plan

## 0. Plan contract and status

| Field | Value |
|---|---|
| Plan ID | claude-qwen-runner-parity-v2 |
| Plan version | 2.2 |
| Status | VALIDATED-DRAFT; this document plans work but does not start it |
| Decision owner | ROOT |
| Verification protocol | CHECKPOINTED_VERIFICATION_V1 |
| Operative document boundary | The direct request, `HANDOFF.md`, and active compatibility documents govern this work. Archived Firmware campaign material and the dirty `Firmware/` checkout are reference-only. |
| Change procedure | ROOT amends this plan only for a new behavior, source owner, acceptance oracle, or authorization boundary. Ordinary implementation/test failures use the declared M05 route. |
| Definition of valid | One local runner branch contains the selected Claude port and native Qwen parity changes; focused static checks and one disposable real Claude/Qwen lane each pass; ROOT accepts the complete result set; the local destination readback matches that accepted branch. |

## 1. Inputs, authority, and directive hierarchy

| Source | Authority | Path/reference | Supplies | Conflict rule |
|---|---|---|---|---|
| SRC-001 | Direct instruction | Current user request | Integrate the reconciled Claude work and remaining Qwen work into `firmware-v2-harness-runner`, with matching provider behavior. | Direct instruction wins. |
| SRC-002 | Repository instruction | `AGENTS.md` and `HANDOFF.md` | Active compatibility-only boundary, one decision owner, worktree safety, and bounded-test policy. | Applies unless SRC-001 narrows it. |
| SRC-003 | Claude source/finding | `active_docs/missing_claude_implementation.md` and `harness-single-worktrees/compat-test` commit `7a37c0a` | Proven Claude launch fixes, host adapter/installer, examples, and focused tests. | Port selected source/test assets, not historical evidence. |
| SRC-004 | Qwen finding | `active_docs/missing_qwencode_implementation.md` and `active_docs/qwencode_listed_features.md` | Native-Qwen requirement, silent option-loss defect, cancellation defect, fixture gap, and parity target. | Genuine gaps are required; generic design recommendations remain excluded. |
| SRC-005 | Qwen protocol reference | `Firmware/scripts/orchestration/qwen_provider_bootstrap.py` and `harness-single-worktrees/qwencode-test` commit `9e91618` | Existing CLI protocol and regression scenarios. | Read-only source; no Firmware/MCP route or dirty Firmware file is integrated. |
| SRC-006 | Destination source | `firmware-v2-harness-runner` at `cb5b568d5fc3f63a1fe037312894e9736a2f2db1` | Current registry, invocation/controller, host delivery, CLI, and tests. | Destination source decides integration mechanics. |
| SRC-007 | Role allocation | `SUBAGENT_ROLE_MODEL_MAPPING.json` | Sole ROOT launch allocation. | It controls allocation only, never product behavior or workflow. |

| Layer | Authority | May define | Must not override |
|---|---|---|---|
| 1 | Direct user instructions and goal/spec | Required outcome and authorization | N/A |
| 2 | This execution plan | Workflow, scope, checks, and routes | Layer 1 |
| 3 | Module instance | Bounded task mechanics | Layers 1-2 |
| 4 | Local task card | Concrete task inputs/actions | Layers 1-3 |
| 5 | Handoff/status | Current facts and already-authorized next edge | Layers 1-4 |
| 6 | Runtime results | Facts needed by a consumer | Any policy layer |
| 7 | Role-model mapping | Concrete launch selection only | Task semantics or graph order |

## 2. Goal, exclusions, and acceptance outcomes

| Outcome ID | Required behavior | Acceptance method | Decision owner | Status |
|---|---|---|---|---|
| OUT-001 | Claude Code has the reconciled native provider, host-adapter, installer, fixture, and CLI behavior from the compatibility worktree. | Ported focused Claude tests pass on the runner branch. | ROOT | OPEN |
| OUT-002 | Qwen Code is a native runner provider, not an external Firmware bootstrap: start/resume stream JSON works; unrepresentable options fail loudly; `interrupt` or exit 130 becomes `CANCELLED`. | New focused native-Qwen tests pass. | ROOT | OPEN |
| OUT-003 | Qwen has the same runner-owned adapter/installer public shape as Claude, including a project-local fixture/example and sparse delivery contract tests. | Focused Qwen host/installer tests pass without a real provider session. | ROOT | OPEN |
| OUT-004 | The harness drives one disposable Claude test orchestrator/doer lane and one disposable Qwen test orchestrator/doer lane through the integrated provider routes. | Each controller reaches the declared terminal result, and each doer performs only its predeclared disposable task. | ROOT | OPEN |
| OUT-005 | The local runner destination contains the accepted result without remote promotion, Firmware, MCP, or hardware activity. | Changed-code verifier, static and live lane checks, and local Git readback pass. | ROOT | OPEN |

| Boundary ID | Type | Included/excluded/authorization condition | Reason | Owner |
|---|---|---|---|---|
| BOUND-001 | Included | Claude selected source/test port, native Qwen adapter/installer/tests/examples, and matching public docs. | Required by SRC-001. | ROOT |
| BOUND-002 | Excluded | Firmware campaign, hardware, BYO MCP, all `Firmware/` writes, and its package-owned settings/MCP route. | Closed or outside active compatibility work. | ROOT |
| BOUND-003 | Excluded | Unrelated provider-neutral design recommendations and Claude U15 cancellation limitation. | They are not required Claude/Qwen parity work. | ROOT |
| BOUND-004 | Included | One disposable authenticated Claude lane and one disposable authenticated Qwen lane using the exact cards in MI-LIVE. | Required by the user's provider-test direction; each task uses a disposable Git worktree and no Firmware/MCP/hardware resource. | ROOT |
| BOUND-005 | Excluded | Real Qwen hook-profile exploration, remote push, and release/promotion. | The live lane proves the runner route, not every installed Qwen hook capability. | ROOT |

## 3. Requirement coverage map

| Requirement ID | Source | Deliverable ID | Implementation owner | Verification | Acceptance owner | Status |
|---|---|---|---|---|---|---|
| REQ-001 | SRC-003 §A-B | DEL-PARITY | PARITY_IMPLEMENTER | CHECK-CLAUDE | ROOT | OPEN |
| REQ-002 | SRC-004 F1.2.7/U4 and cancellation finding | DEL-PARITY | PARITY_IMPLEMENTER | CHECK-QWEN | ROOT | OPEN |
| REQ-003 | SRC-001 matching runner support plus SRC-004 fixture/host follow-through | DEL-PARITY | PARITY_IMPLEMENTER | CHECK-QWEN-HOST | ROOT | OPEN |
| REQ-004 | User provider-test direction and SRC-002 | DEL-LIVE | ROOT | CHECK-LIVE-CLAUDE and CHECK-LIVE-QWEN | ROOT | OPEN |
| REQ-005 | SRC-002 bounded test and verification rules | DEL-INTEGRATION | ROOT | CHECK-CHANGED and CHECK-SHARED | ROOT | OPEN |

## 4. Runtime and repository truth

| Capability/action | State | Source of truth | Invocation owner | Preconditions | How confirmed | Fallback |
|---|---|---|---|---|---|---|
| Claude built-in provider | RUNTIME_ENFORCED | `orchestrator_harness/provider.py` | Runner | Import built-ins. | Destination contains Claude adapter; SRC-003 supplies missing behavior. | Fail closed on invalid invocation. |
| Qwen built-in provider | UNAVAILABLE | SRC-005 currently registers Qwen in external process only. | ROOT | Add runner-native adapter/registration. | Destination has no native Qwen module. | Do not use Firmware bootstrap after integration. |
| Generic host delivery/installer | RUNTIME_ENFORCED | `host_adapters.py`, `codex_adapter.py`, and Claude source in SRC-003 | Runner | Project-local owned assets and manager binding. | Destination has generic coordinator and Codex route; Claude reference implements equivalent specialization. | Future fixture remains truthful for any unimplemented vendor operation. |
| Qwen real hook behavior | TARGET_TOOL_INVOKED | Installed Qwen CLI | Qwen CLI | Separate future authorization. | Active docs report hooks; no source-only check can establish an installed version's behavior. | Keep the code's capabilities conservative; do not make a live claim. |
| Source isolation | ORCHESTRATOR_ENFORCED | `.codex/scripts/worktree_task.py` | ROOT | Clean runner base and unique task name. | Helper records worktree and refuses dirty removal. | Stop before writing on a wrong/dirty coordinate. |
| Changed-code verifier | ORCHESTRATOR_ENFORCED | `.codex/scripts/verify_changed.py` | ROOT | Integrated branch and repository dev environment. | Repository Stop hook uses the same change-aware gate. | Classify a verifier fault; do not accept code. |
| Covered Python/PowerShell launches | ORCHESTRATOR_ENFORCED | `.codex/scripts/Invoke-BoundedTest.ps1` | ROOT | Unique result path and calibrated deadline. | BOUNDED-TEST-v1 is mandatory for recognized script launchers. | Preserve result and retry only after changed conditions. |
| Implementation-role launch allocation | TARGET_TOOL_INVOKED | `stable-general-harness-runner/orchestrator_harness/lane_controller.py` | ROOT dispatches PARITY_IMPLEMENTER through one exact stable-harness coding invocation. | Stable checkout is clean at `4699d27`; the invocation is derived from the mapping and contains the required full-access and compaction overrides. | The stable lane controller emits every invocation `config_overrides` as `codex exec -c` arguments and records the resolved argv in its status result. | Refuse an invalid invocation or unavailable stable checkout; do not substitute the generic collaboration launcher. |

## 5. Deliverable, dependency, risk, and cost model

| Deliverable ID | Behavioral output | Requirement IDs | Dependencies | Shared seams | Release unit |
|---|---|---|---|---|---|
| DEL-PARITY | One runner tip containing selected Claude support plus native Qwen provider/host/installer/examples/tests. | REQ-001, REQ-002, REQ-003 | MI-ADMISSION | Provider registry, invocation validation, controller, terminal outcomes, host adapter selection, CLI. | One local runner branch. |
| DEL-INTEGRATION | Accepted local runner coordinate and compact verification result. | REQ-005 | DEL-PARITY, DEL-LIVE | Public imports, CLI parser, provider contract, test configuration. | Local integration only. |
| DEL-LIVE | One Claude and one Qwen disposable test lane with explicit orchestrator/doer roles and terminal observations. | REQ-004 | DEL-PARITY | Native provider routes, lane controller, disposable worktrees, and result protocol. | One live-test checkpoint. |

| Deliverable ID | Realistic failure | Impact | Coupling | Expected range | Expensive operations | Cheapest adequate topology | Why |
|---|---|---|---|---|---|---|---|
| DEL-PARITY | Claude port loses a seam; Qwen silently accepts an option, misclassifies cancellation, depends on Firmware, or claims unproved host behavior. | Broken provider route or misleading audit state. | High: the same registry/CLI/controller code is shared. | 2.5-4.5 hours. | Focused deterministic tests and three ROOT checkpoint validations. | M01 → one M02 writer → M04 → M05. | One writer owns one coherent shared-code tip; the three checkpoint readbacks catch scope/contract drift before later Qwen work. |
| DEL-INTEGRATION | Source passes isolated checks but has a post-join import/CLI issue. | Local runner branch is not acceptable. | Medium: only destination coordinate changes. | 15-30 minutes. | Changed verifier and targeted shared seams. | M06 after one accepted check pool. | No full assurance or external validation is justified. |
| DEL-LIVE | A provider is unavailable, a lane violates its exact task card, or a controller misclassifies terminal state. | Runner route is unproven or wrong. | Medium: one provider lane per provider, isolated from source. | 15-25 minutes per provider. | Authenticated CLI sessions in disposable worktrees. | M08 readiness followed by M09 once. | Real provider behavior cannot be established by static tests. |

## 6. Workflow module selection manifest

| Module type | Decision | Instance IDs | Reason | Prerequisite/owner if deferred |
|---|---|---|---|---|
| M01 | SELECTED | MI-ADMISSION | Verify one clean runner worktree, source boundaries, stable harness checkout, and implementation-role invocation before writing. | N/A |
| M02 | SELECTED | MI-PARITY | One implementation writer must change the shared provider/CLI/host seams together; ROOT validates each of its three declared checkpoints. | N/A |
| M03 | OMITTED | N/A | Existing focused compatibility behavior supplies concrete test oracles; a second author adds no useful independence. | N/A |
| M04 | SELECTED | MI-CHECK | One focused deterministic campaign is required before acceptance. | N/A |
| M05 | SELECTED | MI-ADJUDICATE | ROOT must classify the one result pool and authorize any retry/repair. | N/A |
| M06 | SELECTED | MI-INTEGRATE | Local branch integration/readback is a distinct operation after acceptance. | N/A |
| M07 | OMITTED | N/A | M04 plus changed-code verification covers these narrow edits; an accumulated safeguard is net-negative complexity. | N/A |
| M08 | SELECTED | MI-READINESS | Verify the exact disposable CLI/backend/worktree prerequisites before real provider lanes. | N/A |
| M09 | SELECTED | MI-LIVE | Run the two specified disposable provider test routes after static acceptance. | N/A |
| M10 | OMITTED | N/A | Existing module shapes cover the work. | N/A |

## 7. Roles and role-model mapping boundary

| Workflow role | Responsibilities | Pool | Context class | Write authority | Resources | Activation | Lifetime |
|---|---|---|---|---|---|---|---|
| PARITY_IMPLEMENTER | Make only the ROOT-specified runner source, focused-test, example, and documentation changes for the current declared parity checkpoint; publish facts and stop for ROOT validation. | 1; one shared source writer. | MI-PARITY source/requirements/checkpoint card only. | WT-CLAUDE-QWEN-001 only. | LANE-IMPLEMENTER-001 and LOCK-RUNNER-WRITER-001. | EDGE-01, then only a separate ROOT card after checkpoint validation. | Prefer the active invocation across the three checkpoints; if unavailable or allocation changed, the same role resumes from a structured handoff and first unresolved checkpoint. |
| CLAUDE_TEST_ORCHESTRATOR | Materialize ROOT's fixed Claude disposable invocation, observe the exact controller state, and return facts only. | 1; one Claude lane. | MI-LIVE Claude card only. | Its disposable test root and result path only. | LANE-CLAUDE-ORCH-001 and WT-CLAUDE-LIVE-001. | MI-LIVE after readiness. | Terminal after one declared lane; cannot define or dispatch a follow-up. |
| CLAUDE_CLI_DOER | Execute the exact Claude CLI task supplied by the orchestrator and publish its declared result. | 1; paired with its Claude orchestrator. | Fixed prompt/task/result contract only. | WT-CLAUDE-LIVE-001 only. | LANE-CLAUDE-DOER-001. | Controller start state observed. | Terminal after the one declared task; no self-dispatch. |
| QWEN_TEST_ORCHESTRATOR | ROOT-driven translation channel: materialize ROOT's fixed Qwen invocation, observe controller state, and return facts only. | 1; one Qwen lane. | MI-LIVE Qwen card only. | Its disposable test root and result path only. | LANE-QWEN-ORCH-001 and WT-QWEN-LIVE-001. | MI-LIVE after readiness. | Terminal after one declared lane; cannot define or dispatch a follow-up. |
| QWEN_DOER | Execute the exact Qwen CLI task supplied through the Qwen test orchestrator and publish its declared result. | 1; paired with its Qwen orchestrator. | Fixed prompt/task/result contract only. | WT-QWEN-LIVE-001 only. | LANE-QWEN-DOER-001. | Controller start state observed. | Terminal after the one declared task; no self-dispatch. |

| Resolution rule | Unknown-role behavior | Mapping-update behavior |
|---|---|---|
| Resolve the five named non-ROOT roles at launch from the mapping in SRC-007; ROOT is the controlling authority and is intentionally not mapped. PARITY_IMPLEMENTER launches only through the stable harness with the mapping-derived invocation. | Reject before task start. | Change allocation only; plan behavior stays fixed. |

## 8. Composed execution graph and critical path

| Edge ID | From/output | To/input | Condition | Serial/parallel | Join ID | Failure branch |
|---|---|---|---|---|---|---|
| EDGE-01 | MI-ADMISSION clean source packet | MI-PARITY source allocation | Runner base is clean and source exclusions/allowlist are recorded. | Serial | N/A | INCOMPLETE to ROOT. |
| EDGE-02 | MI-PARITY frozen tip | MI-CHECK campaign input | All REQ-001 through REQ-003 changes/tests/docs are present on one tip. | Serial | JOIN-01 | All results go to MI-ADJUDICATE. |
| EDGE-03 | MI-CHECK complete result pool | MI-ADJUDICATE decision input | Every feasible focused unit has a terminal result or named dependency skip. | Serial | JOIN-01 | ROOT classifies result. |
| EDGE-04 | MI-ADJUDICATE static acceptance | MI-READINESS input | Required static product criteria are accepted. | Serial | N/A | One compatible material return to MI-PARITY only. |
| EDGE-05 | MI-READINESS verified disposable prerequisites | MI-LIVE input | Both named provider routes, disposable roots, and bounded launch records are ready. | Serial | N/A | Support INCOMPLETE holds only MI-LIVE. |
| EDGE-06 | MI-LIVE complete dual-provider result pool | MI-ADJUDICATE final input | Claude and Qwen lanes each terminate or return a named support result. | Serial | JOIN-LIVE-01 | Material live finding returns to MI-PARITY only through ROOT. |
| EDGE-07 | MI-ADJUDICATE final acceptance | MI-INTEGRATE input | Required static and live product criteria are accepted. | Serial | N/A | One compatible material return to MI-PARITY only. |
| EDGE-08 | MI-INTEGRATE readback | terminal acceptance | Exact local destination readback and affected checks pass. | Serial | N/A | Operation recovery to MI-INTEGRATE; no product loop. |

| Parallel group | Shared input | Member instance IDs | Writable-root isolation | Launch rule | Join ID | Serial exception |
|---|---|---|---|---|---|---|
| N/A | One PARITY_IMPLEMENTER source writer and limited provider capacity. | N/A — the three implementation checkpoints, static units, and the two fixed provider lanes run serially. | Unique bounded result paths and disposable worktrees. | ROOT validates each implementer checkpoint before issuing the next card; ROOT starts the Qwen lane only after the Claude lane has a terminal record. | JOIN-01 then JOIN-LIVE-01 | Serial execution avoids concurrent source mutation and provider-session ambiguity while adding only the three user-required ROOT checkpoint readbacks. |

| Path ID | Ordered instance/edge IDs | Expected range | Overlap | Expensive operations | Why critical |
|---|---|---|---|---|---|
| PATH-01 | MI-ADMISSION, EDGE-01, MI-PARITY, EDGE-02, MI-CHECK, EDGE-03, MI-ADJUDICATE, EDGE-04, MI-READINESS, EDGE-05, MI-LIVE, EDGE-06, MI-ADJUDICATE, EDGE-07, MI-INTEGRATE, EDGE-08 | 4-6 hours plus live provider wall time. | None by default. | Changed verifier, focused tests, and two disposable provider lanes. | Source must be static-safe before a real CLI lane can make an acceptance claim. |

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-PARITY-01 | PRODUCT | MI-PARITY frozen tip and MI-CHECK result pool | Required Claude/Qwen provider, installer, and cancellation contract behavior is proven correct. | MI-CHECK, MI-ADJUDICATE | Native ownership, no silent option loss, accurate terminal outcome, and focused Claude regression invariants. | Blocks only OUT-001 through OUT-003 static acceptance; never blocks Firmware work or unaffected green credit. | Only a failed or undecidable required product criterion permits continuation to MI-PARITY. | EDGE-04 accepts and advances to MI-READINESS. | MI-PARITY with the one complete compatible material pool. | One repair avoids duplicate test/review cycles. | One writer/source context/acceptance set makes one tranche manageable. | Preserve checks whose source/configuration/runner inputs are unchanged; rerun affected or uncertain units. | Split only for a new user-authorized external scope; otherwise merge all compatible findings. |
| GATE-LIVE-01 | PRODUCT | MI-LIVE dual-provider result pool | Required Claude/Qwen disposable lane behavior agrees with the static provider contract. | MI-LIVE, MI-ADJUDICATE | Exact provider route, controller terminal state, doer task boundary, result validity, and cleanup. | Blocks only OUT-004 and final OUT-005 acceptance; never blocks static credit or Firmware work. | Only a failed or undecidable required product criterion permits continuation to MI-PARITY. | EDGE-07 accepts and advances to MI-INTEGRATE. | MI-PARITY with one complete compatible material pool. | One repair follows both provider facts rather than serial lane-specific repairs. | Both lanes consume one source tip and one shared acceptance contract. | Static credit is preserved unless source changes; live result is never reused across provider attempt/version changes. | Split only if a provider support fault leaves the other provider result decisive. |
| GATE-INTEGRATE-01 | OPERATION_BOUNDARY | MI-INTEGRATE accepted input | Local branch integration and readback are complete. | MI-INTEGRATE | Clean destination and exact coordinate readback. | Holds only the exact local integration operation and never product work/credit. | No product loop; ROOT resolves or reports the operation fault while preserving accepted product credit. | EDGE-08 terminal acceptance. | MI-INTEGRATE operation recovery or INCOMPLETE. | Keeps mechanical Git issues out of source repair. | One local destination and no remote action make it one bounded operation. | Product test credit is preserved unless join bytes affect a named check. | Any content conflict stops for ROOT; it is never delegated. |

## 9. Global workflow policies and exceptions

### P01 Ownership and decisions

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Before every module, implementation checkpoint, or retry | Supply exact behavior, scope, source/test entrypoints, non-goals, oracle, failure route, and next edge; after each of the three M02 checkpoints, validate the declared diff and shortest applicable producer check before issuing another implementation card. | Complete card, accepted checkpoint, or terminal insufficiency. | HANDOFF-PARITY-01. | All selected modules |

### P02 Context and thread lifetime

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Missing/contradictory fact, implementation checkpoint, or decision boundary | Return the exact insufficiency; stop; issue a separate ROOT card only after resolution. The same implementation invocation is preferred, never assumed. | No task crosses a decision boundary. | HANDOFF-PARITY-01. | All selected modules |

### P03 Failure-case selection

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | MI-PARITY starts | Fix the three implementation checkpoints: CP-01 reconciled Claude source/assets/tests; CP-02 native Qwen registration/adapter/CLI/cancellation plus focused tests; CP-03 Qwen host/installer/fixture/example/public docs plus focused tests. Cover only Claude launch regression, Qwen silent options, Qwen cancellation, native ownership, and Qwen installer config shape. | Each checkpoint has its matching shortest producer check. | Test diff. | MI-PARITY, MI-CHECK |

### P04 Check selection and green credit

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Implementation checkpoint, frozen tip, repair, or live-provider attempt | After CP-01/CP-02/CP-03, validate the declared diff and run the matching shortest producer check before a new implementation card. At the frozen tip, run CHECK-CHANGED, CHECK-CLAUDE, CHECK-QWEN, CHECK-QWEN-HOST, and CHECK-SHARED; live runs use CHECK-LIVE-CLAUDE and CHECK-LIVE-QWEN. Record an input map and checkpoint after each unit, including the first unresolved unit; reuse a PASS only when source/configuration/runner/environment/prerequisites are unchanged, and execute the earliest required affected unit after ordinary failure. | One complete result pool or one validated implementation checkpoint. | Unique results under `.codex/runtime/bounded-tests/claude-qwen-parity/`. | MI-PARITY, MI-CHECK, MI-READINESS, MI-LIVE |

### P05 Review classes and invalidation

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Frozen tip | Review the changed provider/CLI/installer surfaces against REQ-001 through REQ-004 and invalidate only consuming checks. | Findings join MI-CHECK result pool. | Diff and check outcomes. | MI-CHECK |

### P06 Parallel checks and results

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | MI-CHECK or MI-LIVE | Execute static checks and the two fixed provider lanes serially; start the Qwen lane only after the Claude lane has a terminal record, then join both results once. | JOIN-01 or JOIN-LIVE-01 complete. | Per-unit result. | MI-CHECK, MI-LIVE |

### P07 Finding pooling and material repair

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | MI-CHECK or MI-LIVE finishes | Pool/deduplicate all findings; one compatible material objective returns once to MI-PARITY. | Static acceptance advances to MI-READINESS; final ACCEPTED advances to MI-INTEGRATE; CONTINUE or INCOMPLETE is explicit. | HANDOFF-PARITY-01. | MI-CHECK, MI-LIVE, MI-ADJUDICATE |

### P08 Test-only correction

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Proven test-only fault | Repair only the known test asset and rerun the affected selector; reclassify before source repair. | Product behavior is either still decided or explicitly indeterminate. | Test result. | MI-ADJUDICATE |

### P09 Administrative recovery

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Worktree/supervisor/verifier fault | Preserve terminal evidence, classify, and retry only after changed conditions. A timeout is support evidence, not product failure or success. | Exact consumer proceeds or becomes INCOMPLETE. | Supervisor result. | All selected modules |

### P10 Semantic acceptance

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Complete MI-CHECK or MI-LIVE pool | Decide each required outcome against its named oracle and issue the applicable GATE-PARITY-01 or GATE-LIVE-01 verdict. | EDGE-04, EDGE-07, or one declared return. | HANDOFF-PARITY-01. | MI-ADJUDICATE |

### P11 Full-safeguard scope

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | This plan | N/A — M07 is omitted because M04 plus one M09 dual-provider live check is adequate. | N/A — no accumulated safeguard is launched. | N/A — reasoned omission. | N/A — M07 omitted |

### P12 External authorization and rehearsal

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | MI-LIVE is ready | Permit only the two named disposable provider lanes. A new provider, live hook exploration, target, credential source, retry, or task shape needs a separate ROOT card. | Both lanes complete or return explicit support state. | Bounded terminal results and lane handoffs. | MI-READINESS, MI-LIVE |

### P13 Gate/loop sizing, health, and topology reassessment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Complete pool adds a new source owner or external scope | Amend the plan; otherwise keep the single M02 repair tranche. | Existing route continues or plan becomes INCOMPLETE. | HANDOFF-PARITY-01. | MI-ADJUDICATE |

### P14 Exception classes

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | No declared alternate route is needed. | N/A — new scope requires a plan amendment, not an exception. | INCOMPLETE until amended. | N/A — reasoned absence. | All selected modules |

| Exception ID | Affected policy | Exact trigger | Decision owner | Allowed alternate action | Required confirmation | Preserved results | Invalidated results | Scope | Expiry |
|---|---|---|---|---|---|---|---|---|---|
| N/A | P14 | No exception class is selected; external Qwen work is a new authorization, not a runtime exception. | ROOT | Stop and amend plan. | Direct user authorization. | Existing deterministic credit. | Only work consuming the new scope. | No current alternate route. | Until plan amendment. |

### P15 Stop and live-harm containment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Any attempted Firmware/MCP/hardware, undeclared real-provider action other than the two named MI-LIVE lanes, or leaked credential | Stop, preserve redacted evidence, and report scope violation. | No integration from contaminated work. | Bounded result and handoff. | MI-PARITY, MI-CHECK, MI-READINESS, MI-LIVE, MI-INTEGRATE |

## 10. Lane, resource, result, and handoff manifest

| Lane ID | Module instance | Role | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| LANE-IMPLEMENTER-001 | MI-PARITY | PARITY_IMPLEMENTER | EDGE-01 and each ROOT-validated checkpoint handoff | WT-CLAUDE-QWEN-001 | ROOT then MI-CHECK | Three terminal checkpoint handoffs followed by one frozen parity tip. | ROOT validation or MI-ADJUDICATE/INCOMPLETE. |
| LANE-CLAUDE-ORCH-001 | MI-LIVE | CLAUDE_TEST_ORCHESTRATOR | EDGE-05 | WT-CLAUDE-LIVE-001 | ROOT/MI-ADJUDICATE | Exact disposable Claude controller state/result observed. | Support result to ROOT. |
| LANE-CLAUDE-DOER-001 | MI-LIVE | CLAUDE_CLI_DOER | Claude orchestrator launched | WT-CLAUDE-LIVE-001 | Claude orchestrator | Fixed doer task result published once. | Controller terminal failure. |
| LANE-QWEN-ORCH-001 | MI-LIVE | QWEN_TEST_ORCHESTRATOR | EDGE-05 | WT-QWEN-LIVE-001 | ROOT/MI-ADJUDICATE | Exact disposable Qwen controller state/result observed. | Support result to ROOT. |
| LANE-QWEN-DOER-001 | MI-LIVE | QWEN_DOER | Qwen orchestrator launched | WT-QWEN-LIVE-001 | Qwen orchestrator | Fixed doer task result published once. | Controller terminal failure. |

| Claim/lock ID | Resource | Owner | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| LOCK-RUNNER-WRITER-001 | Exclusive runner integration worktree/branch | ROOT | MI-ADMISSION | WT-CLAUDE-QWEN-001 | All selected modules | Worktree remains clean/retained until M06. | Stop on second writer or dirty state. |
| LOCK-LIVE-CLAUDE-001 | Disposable Claude worktree and result stem | ROOT | MI-READINESS | WT-CLAUDE-LIVE-001 | MI-LIVE | Claude lane terminal/cleaned. | Hold Claude lane only. |
| LOCK-LIVE-QWEN-001 | Disposable Qwen worktree and result stem | ROOT | MI-READINESS | WT-QWEN-LIVE-001 | MI-LIVE | Qwen lane terminal/cleaned. | Hold Qwen lane only. |

| Check | Proves | Dependencies | Result owner | Reuse condition | Rerun route | Result path if needed | Failure route |
|---|---|---|---|---|---|---|---|
| CHECK-CHANGED | Changed source passes repository static/targeted verification. | Frozen source, dev lock, verifier. | ROOT | Identical verifier inputs. | Earliest affected unit. | `.codex/runtime/bounded-tests/claude-qwen-parity/changed.json` | MI-ADJUDICATE. |
| CHECK-CLAUDE | Reconciled Claude argv/env/transcript/adapter/installer behavior. | Ported focused tests and runner source. | ROOT | Claude seams unchanged. | Earliest Claude unit. | `.codex/runtime/bounded-tests/claude-qwen-parity/claude.json` | MI-ADJUDICATE. |
| CHECK-QWEN | Native Qwen registry, argv, loud validation, cancellation, and no-bootstrap fixture behavior. | New native Qwen tests and runner source. | ROOT | Qwen/provider seams unchanged. | Earliest Qwen unit. | `.codex/runtime/bounded-tests/claude-qwen-parity/qwen.json` | MI-ADJUDICATE. |
| CHECK-QWEN-HOST | Qwen adapter/installer config uses owned project-local assets and sparse no-ack delivery semantics. | New Qwen host/installer tests. | ROOT | Host assets/config merger unchanged. | Earliest Qwen-host unit. | `.codex/runtime/bounded-tests/claude-qwen-parity/qwen-host.json` | MI-ADJUDICATE. |
| CHECK-SHARED | Shared registry/public seam tests remain coherent. | Provider registry/public seam source. | ROOT | Shared seam inputs unchanged. | Earliest shared unit. | `.codex/runtime/bounded-tests/claude-qwen-parity/shared.json` | MI-ADJUDICATE. |
| CHECK-LIVE-CLAUDE | The integrated runner launches/observes one exact disposable Claude orchestrator/doer lane. | MI-READINESS, WT-CLAUDE-LIVE-001, exact Claude card/backend. | ROOT | Never reused across a new provider attempt/backend/version. | New authorized Claude lane from first unresolved action. | `.codex/runtime/bounded-tests/claude-qwen-parity/live-claude.json` | MI-ADJUDICATE. |
| CHECK-LIVE-QWEN | The integrated runner launches/observes one exact disposable Qwen orchestrator/doer lane. | MI-READINESS, WT-QWEN-LIVE-001, exact Qwen card/backend. | ROOT | Never reused across a new provider attempt/backend/version. | New authorized Qwen lane from first unresolved action. | `.codex/runtime/bounded-tests/claude-qwen-parity/live-qwen.json` | MI-ADJUDICATE. |

| Result/handoff ID | Producer | Consumer | Path if durable | Correlation needed | Publication rule | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| HANDOFF-PARITY-01 | ROOT module task or PARITY_IMPLEMENTER checkpoint | ROOT next decision | Bounded terminal paths above only | LANE-IMPLEMENTER-001, LOCK-RUNNER-WRITER-001, WT-CLAUDE-QWEN-001, and module ID | Publish source/check/finding state before every decision edge. | Next decision is possible without historical reconstruction. | Exact missing fact as INCOMPLETE. |

| Source allocation ID | Mode | Source/worktree | Writer | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| WT-CLAUDE-QWEN-001 | Isolated Git worktree | New `compat/claude-qwen-runner-parity` branch from `firmware-v2-harness-runner` at `cb5b568`. | PARITY_IMPLEMENTER | Allocated worktree only. | MI-PARITY through MI-INTEGRATE. | Local integration/readback complete. | Preserve state; never write published checkout. |
| WT-CLAUDE-LIVE-001 | Disposable Git worktree | New disposable Claude fixture worktree from frozen MI-PARITY tip. | CLAUDE_CLI_DOER | Disposable root only. | CLAUDE_TEST_ORCHESTRATOR. | Lane terminal and result retained. | Preserve for diagnosis; ROOT retires only when clean. |
| WT-QWEN-LIVE-001 | Disposable Git worktree | New disposable Qwen fixture worktree from frozen MI-PARITY tip. | QWEN_DOER | Disposable root only. | QWEN_TEST_ORCHESTRATOR. | Lane terminal and result retained. | Preserve for diagnosis; ROOT retires only when clean. |

| Retirement ID | Target | Owner | Activation | What must be retained | Completion condition | Recovery visibility | Failure route |
|---|---|---|---|---|---|---|---|
| RETIRE-PARITY-01 | WT-CLAUDE-QWEN-001 | ROOT | After MI-INTEGRATE terminal success | Integrated commit and bounded results. | Clean and no named consumer. | Branch/worktree record remains visible. | Never remove dirty, ambiguous, or unaccepted state. |
| RETIRE-LIVE-CLAUDE-001 | WT-CLAUDE-LIVE-001 | ROOT | After final MI-ADJUDICATE decision | Terminal lane handoff, result, and Git readback. | Clean and no named consumer. | Result and source coordinate remain visible. | Preserve for diagnosis; never remove dirty or ambiguous state. |
| RETIRE-LIVE-QWEN-001 | WT-QWEN-LIVE-001 | ROOT | After final MI-ADJUDICATE decision | Terminal lane handoff, result, and Git readback. | Clean and no named consumer. | Result and source coordinate remain visible. | Preserve for diagnosis; never remove dirty or ambiguous state. |

## 11. Module instances

### MI-ADMISSION - M01: clean source admission

#### Purpose

Establish one clean runner worktree, explicit source boundaries, and a valid stable-harness implementation invocation before source changes begin.

#### Coverage

Supports REQ-001 through REQ-004 and protects BOUND-002 through BOUND-004 plus the requested stable-harness implementation allocation.

#### Selection basis

One fast precondition check prevents accidental edits to the published runner or dirty Firmware reference and confirms the stable harness will carry the requested implementation allocation.

#### Owner and roles

ROOT is sole decision owner/executor; pool one.

#### Preconditions

No target source has been edited for this work.

#### Inputs

SRC-001 through SRC-007, WT-CLAUDE-QWEN-001, LOCK-RUNNER-WRITER-001.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-ADMISSION-01; MI-ADMISSION; DEL-PARITY; COHORT-PARITY-01; GATE-PARITY-01; no loop |
| workflow_role | ROOT |
| objective | Create and verify one clean runner integration worktree with a source allowlist and a mapping-derived stable-harness implementation invocation. |
| why_now | A published destination and dirty historical Qwen source must remain separate, and the user-required implementation allocation must use the stable harness rather than an inferred generic launcher capability. |
| starting_state | Runner HEAD is `cb5b568`; Claude archive parent is `dd673cb`; Firmware is read-only. |
| dependencies_and_predecessor_outputs | SRC-001 and SRC-002; no prior module output. |
| working_scope | Read source and stable-harness metadata; create only WT-CLAUDE-QWEN-001 through the repository helper and construct one unlaunched implementation invocation; no product edit or provider launch. |
| required_behavior | Worktree starts at the published runner, is clean, Claude port is an explicit source/test allowlist, Qwen reference excludes Firmware/MCP settings/routes, and the stable harness has a valid exact implementation invocation derived from the mapping. |
| initial_entrypoints | `HANDOFF.md` (authority, score 1); active Claude/Qwen missing-implementation docs (requirements, score 2); `.codex/scripts/worktree_task.py` (allocation, score 3). |
| failure_case_brief | REQ-004; wrong/dirty base or invalid stable invocation; invariant is no published-runner/Firmware write and no implementation launch outside the stable harness; oracle is Git revision/status, worktree-helper readback, and stable invocation parse/argv construction; owner ROOT. |
| ordered_actions | M01-A1 reread downstream preconditions and authority, including implementation allocation; M01-A2 observe revision, cleanliness, source boundaries, stable checkout identity, and mapping-derived invocation shape; M01-A3 publish SATISFIED without duplicate setup only when every predicate holds; M01-A4 when the worktree is missing create only WT-CLAUDE-QWEN-001, never substitute a different allocation; M01-A5 read back branch/revision/clean status and stable invocation argv; M01-A6 publish admission result; M01-A7 publish INCOMPLETE with exact unresolved fact when unauthorized, indeterminate, or invalid. |
| allowed_tools_capabilities_resources | Read-only Git/PowerShell and one BOUNDED-TEST-v1 worktree helper: expected 60 seconds, cleanup 15, maximum 75, heartbeat 15, result `admission.json`, basis is accepted local-Git plan bound. |
| forbidden_actions_and_boundaries | No `Firmware/` write, hardware/MCP/provider launch, archive evidence import, published checkout edit, or remote action. |
| verification | Revision/cleanliness readback, bounded helper result, and stable invocation parse/argv readback. |
| deliverables_and_result_paths | Clean WT-CLAUDE-QWEN-001 and `.codex/runtime/bounded-tests/claude-qwen-parity/admission.json`. |
| acceptance_criteria_and_tolerances | Exact clean runner base and valid stable-harness invocation required; no tolerance for wrong coordinate, missing mapping-derived override, or direct generic launch. |
| completion_review_owner_and_handoff | ROOT publishes HANDOFF-PARITY-01 to MI-PARITY. |
| failure_classification_and_routes | Administrative INCOMPLETE to ROOT; no product route and no implementation-role substitution. |
| thread_resume_and_terminal_rule | ROOT resumes only after source condition changes; SATISFIED admission is terminal. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P09, P15; no exception. |

#### Outputs and results

Verified worktree, source allowlist, and admission result.

#### Concurrency and isolation

No concurrent writer; WT-CLAUDE-QWEN-001 is the only mutable source root.

#### Resources and side effects

Creates one Git worktree/branch record; ROOT later retires it safely.

#### Checks and acceptance

ROOT accepts exact revision and cleanliness only.

#### Failure and exception routes

Failure stops before M02 as an administrative source fact.

#### Prior results and change effects

No product credit exists; changed base invalidates only admission.

#### Repeat, join, and terminal behavior

SATISFIED activates EDGE-01; INCOMPLETE ends the run.

#### Cost and critical-path effect

1-5 minutes; prevents wrong-tree edits.

### MI-PARITY - M02: Claude port and native Qwen implementation

#### Purpose

Create one coherent runner tip with reconciled Claude support and the small native Qwen parity implementation through three ROOT-validated coding checkpoints.

#### Coverage

REQ-001, REQ-002, and REQ-003.

#### Selection basis

Provider registry, invocation, controller, CLI, and host adapter selection are shared seams, so one writer is simpler and safer than split changes.

#### Owner and roles

ROOT is decision/acceptance owner; PARITY_IMPLEMENTER is the sole source writer; pool one.

#### Preconditions

MI-ADMISSION produced clean WT-CLAUDE-QWEN-001.

#### Inputs

SRC-003 selected source/tests, SRC-004 requirements, SRC-005 protocol reference, destination seams in SRC-006, and GATE-PARITY-01.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-PARITY-01; MI-PARITY; DEL-PARITY; COHORT-PARITY-01; GATE-PARITY-01; LOOP-PARITY-01 only after ROOT admits complete material findings |
| workflow_role | PARITY_IMPLEMENTER |
| objective | Implement the three ROOT-specified parity checkpoints: reconciled Claude source/assets/tests, native Qwen provider/CLI/cancellation/tests, then Qwen host/installer/fixture/example/docs/tests. |
| why_now | MI-ADMISSION established the sole safe source writer and exact reference boundary. |
| starting_state | Clean worktree at `cb5b568`; destination has Claude base adapter but no native Qwen route; archive Claude work is based on ancestor `dd673cb`; no coding checkpoint has ROOT validation yet. |
| dependencies_and_predecessor_outputs | MI-ADMISSION, SRC-003 source allowlist, SRC-004 requirements, and GATE-PARITY-01 behavior contract. |
| working_scope | Runner only, one ROOT-issued checkpoint at a time: CP-01 selected Claude source/assets/examples/focused tests; CP-02 Qwen provider/CLI/cancellation/focused tests; CP-03 Qwen host/installer/assets/examples/focused tests and matching public docs. |
| required_behavior | Port Claude verbose argv, default bypass, permission-denial failure, env override/reject-loud handling, fixture, host adapter, installer, and CLI route. Add built-in `qwen-code` registration and a Qwen adapter that uses normal command/model/stream-json/resume inputs, never imports Firmware route/settings/MCP code, rejects unsupported invocation/provider-spec fields rather than dropping them, maps `interrupt` or exit 130 to `CANCELLED`, and supplies project-local installer/fixture/example plus deterministic sparse no-ack host tests. |
| initial_entrypoints | Claude archive commit `7a37c0a` (source, score 1); destination `provider.py` (provider seam, score 2); `invocation.py`, `lane_controller.py`, `cli.py`, `codex_adapter.py`, `host_adapters.py` (integration seams, score 3); Qwen bootstrap as read-only protocol reference (score 4). |
| failure_case_brief | REQ-001 trigger is lost Claude behavior, oracle is ported focused test; REQ-002 trigger is silent Qwen option drop, wrong cancellation, or Firmware dependency, oracle is native test; REQ-003 trigger is malformed owned install/config or acknowledgement by delivery, invariant is project-local sparse receipt/no ack, oracle is deterministic host test; owner ROOT. |
| ordered_actions | M02-A1 verify clean worktree/lock and the current ROOT-issued checkpoint card; M02-A2 read only its named seams and requirements; M02-A3 convert named risks into code/test invariants; M02-A4 implement exactly CP-01, CP-02, or CP-03 serially as ROOT specified; M02-A5 run that checkpoint's shortest focused producer self-check through BOUNDED-TEST-v1; M02-A6 inspect that checkpoint diff for evidence/Firmware/MCP leakage and scope; M02-A7 publish a terminal checkpoint handoff with diff/check facts and stop for ROOT validation. ROOT validates CP-01/CP-02/CP-03 before issuing any next checkpoint card; CP-03 then supplies the one frozen reviewable tip to MI-CHECK. M02-A8 only after ROOT admits a complete material pool: repair the complete compatible pool, rerun implicated self-checks, and publish one replacement tip. |
| allowed_tools_capabilities_resources | Edit only WT-CLAUDE-QWEN-001 through the stable harness lane controller and the mapping-derived Codex invocation; direct Git read/commit; each focused Python command through BOUNDED-TEST-v1 with expected 240 seconds, cleanup 60, maximum 300, heartbeat 30, unique `producer-claude.json`, `producer-qwen.json`, or `producer-qwen-host.json`, basis accepted focused-suite plan bound. |
| forbidden_actions_and_boundaries | No Firmware route/settings/MCP copy, no user `.qwen`/`.claude` mutation, no real provider/hardware action, no remote push, no unrelated design recommendations. |
| verification | The implementation role runs the focused producer check and diff inspection before each M02-A7 handoff; ROOT validates that handoff before any later coding checkpoint. |
| deliverables_and_result_paths | Three terminal checkpoint handoffs, then one parity tip with named source/tests/assets/docs and unique producer result paths. |
| acceptance_criteria_and_tolerances | Every required behavior exists with focused oracle; untested live vendor hooks are not claimed. |
| completion_review_owner_and_handoff | PARITY_IMPLEMENTER publishes one terminal HANDOFF-PARITY-01 checkpoint record to ROOT; after CP-03 ROOT publishes the frozen tip/diff/checks to MI-CHECK. |
| failure_classification_and_routes | Product failure continues M02; test/support failure goes to MI-ADJUDICATE; external request is out of scope. |
| thread_resume_and_terminal_rule | Each checkpoint ends at ROOT. ROOT prefers the same active PARITY_IMPLEMENTER invocation for the next checkpoint, but an unavailable or allocation-changed invocation resumes only through a structured handoff at the first unresolved checkpoint. Only ROOT's complete material return card authorizes M02-A8; accepted tip is terminal until such a return. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P07, P09, P15; no exception. |

#### Outputs and results

Three ROOT-validated checkpoint handoffs and one frozen runner tip with Claude/Qwen source, examples, docs, and focused regression tests.

#### Concurrency and isolation

PARITY_IMPLEMENTER is the sole serial writer in WT-CLAUDE-QWEN-001; ROOT is read-only during M02 validation; each test gets its own bounded result path.

#### Resources and side effects

Only runner-source mutation; no external provider/hardware/service allocation.

#### Checks and acceptance

The matching focused producer check and ROOT diff/scope validation must pass after CP-01, CP-02, and CP-03; MI-CHECK then runs the frozen-tip campaign.

#### Failure and exception routes

Material failure is one M02 repair tranche; support failure is classified by M05.

#### Prior results and change effects

Replacement tips invalidate only checks consuming changed provider/host/CLI seams.

#### Repeat, join, and terminal behavior

CP-01 and CP-02 end at ROOT validation; CP-03 activates EDGE-02 after ROOT validation; M02-A8 is the sole product repair loop.

#### Cost and critical-path effect

2.5-4.5 hours serial; three small ROOT readbacks trade limited review time for early detection without a second source writer or merge.

### MI-CHECK - M04: focused parity check

#### Purpose

Run a small deterministic check campaign against the one frozen parity tip and return a complete result set.

#### Coverage

REQ-001 through REQ-004 and GATE-PARITY-01.

#### Selection basis

The changes touch public provider/CLI/installer seams, so independent focused checks are warranted; a full safeguard is not.

#### Owner and roles

ROOT runs the fixed serial campaign; pool one.

#### Preconditions

MI-PARITY published a frozen tip and producer self-check outcomes.

#### Inputs

CHECK-CHANGED, CHECK-CLAUDE, CHECK-QWEN, CHECK-QWEN-HOST, CHECK-SHARED, frozen source, and BOUNDED-TEST-v1 policy.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-CHECK-01; MI-CHECK; DEL-PARITY; COHORT-PARITY-01; GATE-PARITY-01; no loop |
| workflow_role | ROOT |
| objective | Decide the narrow Claude/Qwen parity claims on the frozen tip and publish every result. |
| why_now | M02 has one coherent implementation tip; acceptance needs independent focused proof. |
| starting_state | Frozen parity source with M02 self-checks and no integration mutation. |
| dependencies_and_predecessor_outputs | MI-PARITY tip, changed paths, and declared selectors. |
| working_scope | Read frozen runner source; write only unique bounded results; make no source/test edit. |
| required_behavior | Run change-aware verification, ported Claude focused tests, native Qwen adapter/host tests, and shared provider registry/public seam tests. Finish each feasible unit even when an earlier ordinary unit fails; no external Qwen CLI action. |
| initial_entrypoints | `.codex/scripts/verify_changed.py` (changed gate, score 1); focused Claude/Qwen tests (behavior oracles, score 2); provider registry/public seam tests (shared contract, score 3). |
| failure_case_brief | REQ-004 trigger is failing static or targeted unit; invariant is no unexecuted feasible unit is hidden by earlier failure; oracle is terminal result per selector; owner ROOT. |
| ordered_actions | M04-A1 verify every unit uses the frozen tip; M04-A2 select CHECK-CHANGED as the cheapest decisive path; M04-A3 allocate serial unique result paths for remaining deterministic paths; M04-A4 finish all feasible units and retain failure output; M04-A5 preserve terminal results; M04-A6 join once/deduplicate without repair; M04-A7 publish complete result set and preserved credit to MI-ADJUDICATE; M04-A8 after affected repair rerun only changed/invalidated selectors under a separate ROOT card. |
| allowed_tools_capabilities_resources | BOUNDED-TEST-v1: CHECK-CHANGED expected 480 seconds plus 120 cleanup equals 600 maximum with heartbeat 60; each focused selector expected 240 seconds plus 60 cleanup equals 300 maximum with heartbeat 30; basis is accepted plan bounds for current static gate/focused suites. |
| forbidden_actions_and_boundaries | No source edit, full product sweep, real Qwen/provider/hardware/MCP action, or unchanged supervisor retry. |
| verification | CHECK-CHANGED, CHECK-CLAUDE, CHECK-QWEN, CHECK-QWEN-HOST, and CHECK-SHARED terminal results. |
| deliverables_and_result_paths | Complete result pool and five unique Section 10 bounded paths. |
| acceptance_criteria_and_tolerances | Each unit has PASS, FAIL, or named dependency skip; absent result is INDETERMINATE. |
| completion_review_owner_and_handoff | ROOT joins once and publishes HANDOFF-PARITY-01 to MI-ADJUDICATE. |
| failure_classification_and_routes | All results go to MI-ADJUDICATE; a support timeout blocks only its direct consumer. |
| thread_resume_and_terminal_rule | Resume at earliest failed, unresolved, affected, or uncertain selector; reuse unchanged PASS credit only under P04. |
| cited_global_policy_ids_and_exception_ids | P01, P04, P05, P06, P07, P09, P10. |

#### Outputs and results

Complete focused result pool and reusable PASS credit.

#### Concurrency and isolation

Serial campaign; source is read-only and result stems do not collide.

#### Resources and side effects

Only local bounded test processes/results.

#### Checks and acceptance

MI-CHECK supplies the focused tests; it does not accept or repair.

#### Failure and exception routes

All results route to MI-ADJUDICATE.

#### Prior results and change effects

P04 input comparison controls reuse; changed seams rerun their consumers.

#### Repeat, join, and terminal behavior

JOIN-01 occurs once; EDGE-03 always follows.

#### Cost and critical-path effect

20-40 minutes; avoids an unnecessary whole-suite/full-assurance phase.

### MI-ADJUDICATE - M05: static then final parity verdicts

#### Purpose

Give ROOT one place to issue the static verdict, then the final live verdict, or authorize one bounded repair.

#### Coverage

GATE-PARITY-01, GATE-LIVE-01, and REQ-001 through REQ-004 decisions.

#### Selection basis

An implementation writer must not decide whether a test/support failure changes the product requirement.

#### Owner and roles

ROOT alone adjudicates; no delegated writer.

#### Preconditions

MI-CHECK or MI-LIVE has one complete declared result pool.

#### Inputs

The applicable gate, result pool, source diff, P04 reuse facts, and Section 14 ledger.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-ADJUDICATE-01; MI-ADJUDICATE; DEL-PARITY/DEL-LIVE; COHORT-PARITY-01; GATE-PARITY-01 or GATE-LIVE-01; LOOP-PARITY-01 when continuation is admitted |
| workflow_role | ROOT |
| objective | Issue one evidence-based verdict for the current static or live pool and one declared next route. |
| why_now | MI-CHECK or MI-LIVE has completed; code must not self-repair or integrate before ROOT classifies the evidence. |
| starting_state | One frozen tip, one complete static or live pool, no active repair/integration. |
| dependencies_and_predecessor_outputs | MI-CHECK or MI-LIVE result pool, applicable gate criteria, P04 input facts, and Section 14 ledger. |
| working_scope | Read results/source diff and publish decision; no source/test edit or Git integration. |
| required_behavior | Deduplicate results, classify material/test-only/support states, preserve unaffected credit, activate M08 only from static acceptance, and return one complete compatible material group to M02 only when a required product criterion failed or is undecidable. |
| initial_entrypoints | MI-CHECK or MI-LIVE terminal results (evidence, score 1); REQ map/applicable gate (oracles, score 2); Section 14 (boundary, score 3). |
| failure_case_brief | REQ-004 trigger is a verifier/test/supervisor or live-lane fault; invariant is it cannot become product repair without a failed/undecidable requirement; oracle is classification linked to terminal evidence; owner ROOT. |
| ordered_actions | M05-A1 validate result shape without inferring success; M05-A2 pool/deduplicate findings once; M05-A3 classify material, test-only, and support; M05-A4 decide product-invalidating, nonblocking-test-error, or indeterminate for each test/support fault; M05-A5 reject nonrequired gold-plating to Section 14; M05-A6 calculate preserved/invalidated credit; M05-A7 send one compatible material pool to MI-PARITY when required; M05-A8 route proven test-only correction to its test asset; M05-A9 recover an administrative artifact only for named consumer; M05-A10 publish static ACCEPTED to EDGE-04, final ACCEPTED to EDGE-07, or CONTINUE, ACCEPT-WITHIN-TOLERANCE, or INCOMPLETE. |
| allowed_tools_capabilities_resources | Read-only source/result inspection and ROOT decision recording only. |
| forbidden_actions_and_boundaries | No repair, check rerun, live-lane launch, integration, remote action, or acceptance oracle change. |
| verification | Every disposition references a result, requirement, and declared graph edge. |
| deliverables_and_result_paths | HANDOFF-PARITY-01 with verdict, complete dispositions, and credit state. |
| acceptance_criteria_and_tolerances | One disposition/route per finding; no unobserved external behavior becomes a pass. |
| completion_review_owner_and_handoff | ROOT accepts static evidence to activate MI-READINESS, accepts final evidence to activate MI-INTEGRATE, or issues a new full M02 card. |
| failure_classification_and_routes | Material required failure returns once to M02; test/support takes its own route; new scope is INCOMPLETE/plan amendment. |
| thread_resume_and_terminal_rule | Accepted task is terminal; later repair begins from first unresolved action under a new ROOT card. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P07, P08, P09, P10, P13; no exception. |

#### Outputs and results

One authoritative static or final verdict, pooled findings, and retained/invalidated credit.

#### Concurrency and isolation

Decision-only; no mutable source root.

#### Resources and side effects

Only the handoff needed by M02, M08, or M06.

#### Checks and acceptance

ROOT verifies all dispositions and gate criteria.

#### Failure and exception routes

Only declared material/test/support routes are allowed.

#### Prior results and change effects

Unrelated accepted credit stays closed; P04 identifies changed consumers.

#### Repeat, join, and terminal behavior

CONTINUE returns once to M02; static ACCEPTED activates EDGE-04 and final ACCEPTED activates EDGE-07.

#### Cost and critical-path effect

5-15 minutes; avoids ad hoc repair loops.

### MI-READINESS - M08: disposable provider-lane readiness

#### Purpose

Prepare and verify the exact disposable prerequisites for one Claude and one Qwen live harness lane, without changing runner source or user configuration.

#### Coverage

REQ-004 and the readiness input for GATE-LIVE-01.

#### Selection basis

Real authenticated provider lanes need isolated worktrees, exact cards, bounded result paths, and a current CLI/backend observation; this small preflight prevents an ambiguous live failure.

#### Owner and roles

ROOT owns readiness; the four live-provider roles are not launched until it publishes SATISFIED.

#### Preconditions

MI-ADJUDICATE has accepted GATE-PARITY-01 static behavior and the frozen tip is unchanged.

#### Inputs

Frozen MI-PARITY tip, exact Claude/Qwen invocation templates, WT-CLAUDE-LIVE-001, WT-QWEN-LIVE-001, LOCK-LIVE-CLAUDE-001, LOCK-LIVE-QWEN-001, and BOUND-004.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-READINESS-01; MI-READINESS; DEL-LIVE; COHORT-PARITY-01; GATE-LIVE-01; no loop |
| workflow_role | ROOT |
| objective | Establish two clean disposable worktrees, exact fixed test cards, executable provider routes, and isolated bounded result paths. |
| why_now | Static implementation is accepted; live testing must be prepared without conflating a missing route/backend with a product result. |
| starting_state | Frozen source tip with no live lane; no disposable worktree, provider session, or result path is shared. |
| dependencies_and_predecessor_outputs | MI-ADJUDICATE static ACCEPTED verdict, BOUND-004, and CHECK-LIVE-CLAUDE/CHECK-LIVE-QWEN definitions. |
| working_scope | Create/use only two disposable Git worktrees and bounded runtime paths; do not edit runner source or global/user provider configuration. |
| required_behavior | Verify current CLI command availability, declared backend authentication route, clean disposable worktrees, exact one-file doer task cards, status/result paths, and controller bindings; no real agent prompt starts in M08. |
| initial_entrypoints | Active Claude/Qwen fixtures and examples (fixed invocation shape, score 1); integrated provider/CLI source (route, score 2); `.codex/scripts/worktree_task.py` and bounded policy (isolation, score 3). |
| failure_case_brief | REQ-004 trigger is missing CLI/backend/worktree or result-path collision; invariant is no live lane begins against unverified prerequisites; oracle is preflight readback; owner ROOT. |
| ordered_actions | M08-A1 verify exact readiness claims and BOUND-004; M08-A2 inspect CLI/backend/worktree prerequisites without provider prompt; M08-A3 allocate two disposable roots and locks; M08-A4 materialize the predeclared invocation/task/result paths; M08-A5 read back route, identities, clean roots, and result isolation; M08-A6 publish SATISFIED or INCOMPLETE readiness result for the exact affected provider lane. |
| allowed_tools_capabilities_resources | Read-only provider CLI version/help and bounded worktree helper calls: each expected 60 seconds, cleanup 15, maximum 75, heartbeat 15; unique results `readiness-claude.json` and `readiness-qwen.json`; basis is accepted local preflight bound. |
| forbidden_actions_and_boundaries | No prompt/model turn, source edit, global config write, Firmware/MCP/hardware action, remote action, or cross-provider worktree/result sharing. |
| verification | CLI/backend/worktree/card/status-path readback for both named lanes. |
| deliverables_and_result_paths | Two SATISFIED/INCOMPLETE readiness records and the two disposable roots/locks. |
| acceptance_criteria_and_tolerances | A provider lane may launch only when its own prerequisite predicate is SATISFIED; no assumed credential/backend state. |
| completion_review_owner_and_handoff | ROOT publishes HANDOFF-PARITY-01 and activates only the ready MI-LIVE route. |
| failure_classification_and_routes | Administrative/provider support failure holds only its corresponding live lane; it never invalidates static parity credit. |
| thread_resume_and_terminal_rule | A changed CLI/backend/worktree condition requires a new ROOT readiness card; SATISFIED readiness is terminal for its frozen source/attempt. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P09, P12, P15; no exception. |

#### Outputs and results

Two independently verified disposable lane-ready records, or one exact provider-specific INCOMPLETE result.

#### Concurrency and isolation

Two disjoint disposable roots/locks/results; no source writer and no provider process in this module.

#### Resources and side effects

Creates reversible disposable worktrees and task files only; ROOT owns cleanup.

#### Checks and acceptance

ROOT accepts readiness separately for Claude and Qwen; either support failure is not a product verdict.

#### Failure and exception routes

Support failure holds the exact M09 lane consumer and is classified under P09.

#### Prior results and change effects

Any source/CLI/backend/card/root change invalidates that provider's readiness and live result only.

#### Repeat, join, and terminal behavior

Both ready results activate EDGE-05; MI-READINESS never repairs product source.

#### Cost and critical-path effect

5-10 minutes; it eliminates ambiguous live-lane setup failures.

### MI-LIVE - M09: two disposable provider acceptance lanes

#### Purpose

Run the smallest real acceptance proof: one fixed Claude orchestrator/doer lane and one fixed ROOT-driven Qwen orchestrator/doer lane.

#### Coverage

REQ-004, OUT-004, GATE-LIVE-01, and final OUT-005 input.

#### Selection basis

Static tests cannot prove that the integrated runner actually drives either installed provider route through the controller/doer boundary.

#### Owner and roles

ROOT owns test meaning and observation; CLAUDE_TEST_ORCHESTRATOR/CLAUDE_CLI_DOER run one Claude lane; QWEN_TEST_ORCHESTRATOR/QWEN_DOER run one Qwen lane.

#### Preconditions

MI-READINESS marked both exact provider lanes SATISFIED, and no source changed after MI-CHECK.

#### Inputs

The two readiness records, exact provider invocations, fixed doer prompts, disposable worktrees/locks, live result paths, and GATE-LIVE-01.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-LIVE-01; MI-LIVE; DEL-LIVE; COHORT-PARITY-01; GATE-LIVE-01; no product loop inside M09 |
| workflow_role | ROOT |
| objective | Prove one real Claude and one real Qwen controller/doer lane against their integrated native provider routes. |
| why_now | Static contract is accepted and both disposable prerequisites have been read back; live behavior is the remaining parity claim. |
| starting_state | Two clean isolated roots, exact cards, no running provider process, and no accepted live evidence. |
| dependencies_and_predecessor_outputs | MI-READINESS SATISFIED records, GATE-LIVE-01, LANE-CLAUDE-ORCH-001/LANE-CLAUDE-DOER-001/LANE-QWEN-ORCH-001/LANE-QWEN-DOER-001, and the frozen source tip. |
| working_scope | Run exactly one Claude and one Qwen disposable task: each doer creates one named text file with the exact required content, commits it in its own disposable worktree, and writes the canonical result. |
| required_behavior | ROOT supplies both fixed one-file task cards; each orchestrator launches only its paired doer; each doer makes the named file/commit/result and no other source change; each controller reaches an observed terminal status with matching provider ID, valid result, and cleanup/readback. Qwen test orchestration is a ROOT-driven translation channel, not independent task planning. |
| initial_entrypoints | Integrated canonical invocation/runner controller (launch, score 1); Claude/Qwen focused fixture examples (task/result shape, score 2); live lane status/result contract tests (oracle, score 3). |
| failure_case_brief | REQ-004 trigger is wrong provider route, missing terminal state, invalid result, doer writes outside its named file, or leaked cross-lane state; invariant is one fixed lane per provider with no self-dispatch; oracle is status/result/Git diff/readback; owner ROOT. |
| ordered_actions | M09-A1 revalidate both readiness records, frozen source, roots, locks, and exact task cards; M09-A2 start the Claude test orchestrator with its preassigned lane/session/process IDs; M09-A3 start the Claude CLI doer only through that controller and observe terminal status/result/diff; M09-A4 start the ROOT-driven Qwen test orchestrator with its preassigned lane/session/process IDs; M09-A5 start the Qwen doer only through that controller and observe terminal status/result/diff; M09-A6 continue observing every runnable lane despite ordinary failure in the other lane; M09-A7 read back each result, provider ID, terminal outcome, commit, cleanup, and forbidden-change boundary; M09-A8 join once into a complete dual-provider result pool; M09-A9 publish the pool and terminal handoffs to MI-ADJUDICATE without repair or acceptance. |
| allowed_tools_capabilities_resources | Two lane-managed provider sessions only. Claude expected upper bound 480 seconds plus cleanup 120 equals maximum 600 with heartbeat 60 and result `live-claude.json`; Qwen expected upper bound 600 seconds plus cleanup 120 equals maximum 720 with heartbeat 60 and result `live-qwen.json`; bases are accepted real single-lane provider bounds, including controller cleanup. |
| forbidden_actions_and_boundaries | No task meaning change, self-dispatch, source worktree write, global config write, Firmware/MCP/hardware use, remote action, second attempt, cross-lane file/resource use, or unbounded retry. |
| verification | Each provider: terminal controller status, matching provider ID, valid canonical result, exact named file/commit, clean boundary/readback, bounded terminal result; then one joined pool. |
| deliverables_and_result_paths | CHECK-LIVE-CLAUDE and CHECK-LIVE-QWEN result paths, two terminal handoffs, and joined live pool. |
| acceptance_criteria_and_tolerances | Both fixed lanes pass exactly, or ROOT classifies a complete pool. No provider success may be inferred from a missing transcript/status/result. |
| completion_review_owner_and_handoff | Both orchestrators/doers publish terminal HANDOFF-PARITY-01 facts; ROOT forwards only the joined pool to MI-ADJUDICATE. |
| failure_classification_and_routes | Product failure/undecidable required claim goes to MI-ADJUDICATE; provider/backend/supervisor support fault blocks only its lane/OUT-004 consumer; no worker retries. |
| thread_resume_and_terminal_rule | Each role/task ends after one attempt. A new attempt needs ROOT authorization, new process/session/lane IDs, a new bounded result path, and fresh M08 readiness; no prior live PASS is reused across attempts. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P06, P07, P09, P10, P12, P15; no exception. |

#### Outputs and results

One complete pair of provider-lane observations and terminal handoffs, each correlated to its controller/doer/worktree/result IDs.

#### Concurrency and isolation

Claude and Qwen lanes use disjoint worktrees, locks, result stems, sessions, and provider processes; ROOT starts Qwen only after the Claude lane has a terminal record, and no source writer runs.

#### Resources and side effects

Two authenticated but disposable provider sessions and Git worktrees; ROOT owns post-readback cleanup.

#### Checks and acceptance

CHECK-LIVE-CLAUDE and CHECK-LIVE-QWEN prove the exact fixed task boundary and controller result; MI-LIVE does not accept findings.

#### Failure and exception routes

One ordinary lane failure never cancels the other; complete results go to MI-ADJUDICATE, while support faults use P09.

#### Prior results and change effects

Static credit remains valid unless source changes; live PASS is attempt/version/backend/root specific and never reused after change.

#### Repeat, join, and terminal behavior

JOIN-LIVE-01 publishes one complete pool. M09 ends at ROOT and cannot retry, repair, integrate, or dispatch follow-up work.

#### Cost and critical-path effect

Up to 22 minutes provider wall time; these two lanes are the minimum real proof requested for Claude and Qwen routes.

### MI-INTEGRATE - M06: local integration/readback

#### Purpose

Integrate the accepted local parity tip into the runner destination and read it back; do not promote remotely.

#### Coverage

OUT-004 and REQ-004 operation boundary.

#### Selection basis

Local Git integration changes destination state and needs a separate mechanical readback after source acceptance.

#### Owner and roles

ROOT accepts inputs and performs conflict-free local mechanics; pool one.

#### Preconditions

MI-ADJUDICATE issued final ACCEPTED for GATE-LIVE-01 after static GATE-PARITY-01 acceptance.

#### Inputs

Accepted parity tip, clean local destination, rollback base `cb5b568`, and affected check credit.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | execution-card/v1; CARD-INTEGRATE-01; MI-INTEGRATE; DEL-INTEGRATION; COHORT-PARITY-01; GATE-INTEGRATE-01; no loop |
| workflow_role | ROOT |
| objective | Apply the accepted local parity tip to the intended runner branch and prove the exact readback coordinate. |
| why_now | Required deterministic and live provider behavior is accepted; this is the only remaining local operation. |
| starting_state | Destination is clean at declared base/accepted descendant; no remote action occurred. |
| dependencies_and_predecessor_outputs | MI-ADJUDICATE final ACCEPTED verdict, accepted parity tip, live lane evidence, and rollback base. |
| working_scope | Local Git branch/worktree integration and readback only; no content conflict resolution or remote action. |
| required_behavior | Revalidate accepted tip/destination cleanliness, record rollback base, perform only conflict-free local integration, inspect readback, and run only checks whose inputs changed during integration. |
| initial_entrypoints | MI-ADJUDICATE verdict (accepted input, score 1); destination Git status/log/diff (safety, score 2); Section 10 check map (affected check, score 3). |
| failure_case_brief | OUT-004 trigger is destination mismatch/content conflict; invariant is no unapproved resolution/push; oracle is exact Git readback; owner ROOT. |
| ordered_actions | M06-A1 revalidate accepted input/verdict; M06-A2 verify clean destination and record rollback base; M06-A3 perform declared conflict-free local integration; M06-A4 inspect combined diff and run only integration-affected checks; M06-A5 publish coordinate/readback; M06-A6 omit promotion under BOUND-004; M06-A7 retain rollback/acceptance results; M06-A8 retire only clean unclaimed temporary worktree state. |
| allowed_tools_capabilities_resources | Local Git mechanics; any affected Python check uses its declared BOUNDED-TEST-v1 path/bound. |
| forbidden_actions_and_boundaries | No content conflict resolution, remote push/release, Firmware/MCP/hardware/real provider activity, or dirty state deletion. |
| verification | Exact destination revision/readback and only integration-affected selected checks. |
| deliverables_and_result_paths | Local integrated coordinate and HANDOFF-PARITY-01 terminal record. |
| acceptance_criteria_and_tolerances | Exact accepted content/readback required; no tolerance for conflict or uncertain destination. |
| completion_review_owner_and_handoff | ROOT reads back then accepts terminal outcome. |
| failure_classification_and_routes | GATE-INTEGRATE-01 fault remains M06 operation recovery and never enters M02 product repair. |
| thread_resume_and_terminal_rule | Resume only after ROOT names a conflict-free operation; successful local integration is terminal. |
| cited_global_policy_ids_and_exception_ids | P01, P04, P09, P10, P13, P15; no exception. |

#### Outputs and results

Exact local integrated coordinate, retained rollback base, and readback.

#### Concurrency and isolation

One destination writer; no concurrent merge/source writer.

#### Resources and side effects

Local branch/worktree mutation only; remote state remains unchanged.

#### Checks and acceptance

ROOT accepts GATE-INTEGRATE-01 only after readback.

#### Failure and exception routes

Operation recovery preserves accepted product credit.

#### Prior results and change effects

Only checks whose inputs changed in the join rerun; other green credit remains.

#### Repeat, join, and terminal behavior

EDGE-05 ends the local plan; no product loop follows integration.

#### Cost and critical-path effect

5-15 minutes; one bounded destination operation.

## 12. External and practical validation

| Decision ID | Module type | Decision | Authority/resource | Synthetic proof | Real proof | Owner | Failure route |
|---|---|---|---|---|---|---|---|
| EXT-LIVE-01 | M08/M09 | One disposable authenticated Claude lane and one disposable authenticated Qwen lane are selected; installed-Qwen hook-profile exploration remains omitted. | Two named disposable worktrees, their declared provider sessions, and BOUND-004 authorization. | M08 reads back CLI/backend/auth/result-path prerequisites without prompting a provider. | M09 runs the one fixed controller/doer task for Claude, then Qwen, and reads back status/result/task-file/Git boundary. | ROOT | Provider/backend/supervisor support fault holds only its named lane; a product finding goes to MI-ADJUDICATE. |

## 13. Integration, safeguard, promotion, rollback, and retirement

| Decision ID | Module type | Decision | Accepted input | Action/order | Checks | Promotion/rollback/retirement | Owner |
|---|---|---|---|---|---|---|---|
| REL-LIVE-01 | M08/M09 | Two disposable provider lanes selected; hook exploration and promotion omitted. | Static GATE-PARITY-01 acceptance and verified readiness records. | Create isolated roots, run one fixed Claude lane and one fixed ROOT-driven Qwen lane, join results, then classify. | Exact status/result/task-file/Git-readback checks for each lane. | Retain terminal evidence; retire only clean disposable roots; no remote action. | ROOT |
| REL-LOCAL-01 | M06 | Local integration selected; safeguard/promotion omitted. | Final MI-ADJUDICATE accepted parity tip. | Revalidate, conflict-free integrate, read back. | Only check inputs changed by integration; reuse other credit. | Retain `cb5b568` rollback base; retire only clean worktree; no remote push. | ROOT |

## 14. Tolerances, unresolved decisions, and out-of-scope ledger

| Item ID | Type | Exact condition | Consequence | Owner | Resolution boundary |
|---|---|---|---|---|---|
| LEDGER-U15 | Out-of-scope | Claude exposes no reliable cancellation signal distinct from generic failure. | No fabricated Claude `CANCELLED` claim. | ROOT | New upstream protocol signal. |
| LEDGER-QWEN-LIVE | Out-of-scope | Installed-Qwen hook-profile behavior is not exercised. | The fixed Qwen lane proves only its declared controller/doer route; no broad hook capability claim. | ROOT | Separate direct authorization. |
| LEDGER-FIRMWARE | Out-of-scope | Firmware/hardware/BYO MCP and package route remain closed/inactive. | No mutation or proof dependency. | ROOT | Separate project. |

## 15. Rule application matrix

| Rule ID | Plan location | Applied behavior or justified N/A |
|---|---|---|
| R1 | Sections 2-3 | Required Claude/Qwen parity is preserved; unrelated scope excluded. |
| R2 | Sections 3, 10 | IDs exist only where workflow/runtime consumers need them. |
| R3 | Sections 5-6 | One implementation writer/check campaign is the cheapest adequate topology; the three user-required ROOT readbacks stay inside M02. |
| R4 | Sections 2, 14 | Real gaps included; speculative/generic work omitted. |
| R5 | Sections 4, 14 | Live Qwen uncertainty is reported, never passed. |
| R6 | Sections 7, 9 | ROOT alone owns decisions, checkpoint validation, and integration authorization. |
| R7 | Sections 7, 10 | One serial implementation writer owns shared source. |
| R8 | Sections 8-9 | Static checks/source writes and the two fixed provider lanes are serial; results join once. |
| R9 | Sections 1, 7 | One mapping has one executable role; plan contains no allocation values. |
| R10 | Section 11 | Each task has complete ROOT-authored scope, proofs, and routes. |
| R11 | Sections 2, 12 | Only the authorized fixed Qwen lane is included; hook exploration remains excluded. |
| R12 | Sections 8-9 | Product return requires failed/undecidable required criterion. |
| R13 | Section 11 | M02 performs short producer self-checks. |
| R14 | Section 9 | Test/support faults are classified before repair. |
| R15 | Sections 8-9 | Complete pool and preserved credit control continuation. |
| R16 | Section 9 | Test-only correction cannot silently become product repair. |
| R17 | Sections 8-9 | Ready successor advances without unrelated support wait. |
| R18 | Sections 8, 11 | Product return stays in same M02 task/role. |
| R19 | Section 9 | PASS reuse needs unchanged declared inputs. |
| R20 | Section 10 | Single source root and unique results prevent collisions. |
| R21 | Section 10 | Source and two disposable worktrees, lanes, locks, and handoffs have IDs; ordinary content does not. |
| R22 | Section 10 | Dirty or ambiguous worktree is retained. |
| R23 | Section 9 | Scope/live-harm trigger stops exact work and retains evidence. |
| R24 | Section 8 | Product and integration operation gates are distinct. |
| R25 | Sections 2, 14 | Only observed realistic gaps guide work. |
| R26 | Section 5 | Every selected module has a stated payoff. |
| R27 | Section 8 | Typed serial graph follows source/output dependencies. |
| R28 | Section 13 | Integration uses readback and rollback retention. |
| R29 | Sections 12, 14 | The two narrow live lanes are proved; broad external hook behavior remains omitted honestly. |
| R30 | Sections 4, 9-11 | Covered launches use BOUNDED-TEST-v1 and unique calibrated results. |
| S1 | Sections 5-6 | Modules selected by actual need/cost. |
| S2 | Section 3 | Requirements have deliverable, oracle, and owner. |
| S3 | Sections 7, 10 | One source writer plus four live-lane roles is sufficient. |
| S4 | Sections 8-9 | M04 returns one complete check set. |
| S5 | Sections 8-9 | M05 owns verdict/routing. |
| S6 | Section 13 | M06 is local integration only after the live-lane verdict. |
| S7 | Sections 6, 12 | M07 is omitted with reasoned N/A; M08/M09 supply only the requested provider proof. |
| S8 | Sections 8-9 | Serial policy avoids unnecessary provider-lane fan-out. |
| S9 | Sections 8-9 | Compatible findings batch once to M02. |
| S10 | Section 11 | Cards state entrypoints/boundaries/oracles. |
| S11 | Sections 9, 12 | Fixed live lanes are authorized; any new external scope requires amendment. |
| S12 | Section 10 | Source/disposable worktree and result lifecycle preserves recovery. |
| S13 | Section 4 | Capability classes are distinguished. |
| S14 | Sections 9-11 | Bounded static and live timing/heartbeat/retry rules are declared. |
| S15 | Sections 13-14 | Promotion and hook exploration are omitted; local rollback and lane evidence are retained. |
| S16 | Section 8 | Gate questions, scope, loop rule, and returns are explicit. |

## 16. Structural validation result

| Check ID | Result | Basis |
|---|---|---|
| V01 | PASS | One title and Sections 0-16 appear once in order. |
| V02 | PASS | All required template tables are populated with reasoned N/A rows. |
| V03 | PASS | Every REQ has a deliverable, check, and ROOT acceptance owner. |
| V04 | PASS | M01-M10 decisions are listed; selected modules have exact instance schema. |
| V05 | PASS | Each graph edge consumes declared output; static JOIN-01 and live JOIN-LIVE-01 are explicit. |
| V06 | PASS | Only M03, M07, and M10 are omitted; they have no instances or graph edges. |
| V07 | PASS | Selected modules and serial edges have explicit cost payoff. |
| V08 | PASS | Serial execution is justified by one writer, limited provider capacity, and simple terminal attribution. |
| V09 | PASS | M04 complete pool and one M02 repair return are explicit. |
| V10 | PASS | M04 card fixes input, boundary, risks, oracle, output, and handoff. |
| V11 | PASS | M07 omitted; M08/M09 provide only the specified narrow live proof. |
| V12 | PASS | P04 declares conservative input-based reuse and earliest affected rerun. |
| V13 | PASS | All seven selected modules have all task-card fields and recipe actions; M02 has three ROOT-validated checkpoints without adding a second writer. |
| V14 | PASS | ROOT retains scope, acceptance, routing, and integration decisions. |
| V15 | PASS | No exception selected; P14 provides a reasoned amendment route. |
| V16 | PASS | Section 4 distinguishes runtime/orchestrator/target-tool/unavailable facts. |
| V17 | PASS | Qwen installed behavior is target-tool fact, not inferred runner proof. |
| V18 | PASS | Five non-ROOT roles are mapped; ROOT is intentionally unmapped and the mapping filename appears once. |
| V19 | PASS | PARITY_IMPLEMENTER is the one writer for every shared provider/CLI source seam. |
| V20 | PASS | Results are unique; one source root and two disposable live roots are isolated. |
| V21 | PASS | Cards list focused entrypoints with scores/reasons. |
| V22 | PASS | Failure cases are realistic, requirement-linked, and oracle-backed. |
| V23 | PASS | P07-P09 classify test/support faults without automatic material repair. |
| V24 | PASS | Static PRODUCT, live PRODUCT, and integration OPERATION_BOUNDARY gates declare exact scope/routes. |
| V25 | PASS | Only product failure/uncertainty returns to same M02 task. |
| V26 | PASS | Retirement refuses unclean/ambiguous state. |
| V27 | PASS | Cards contain no vague worker delegation or undefined action. |
| V28 | PASS | Section 15 maps R1-R30 and S1-S16 once. |
| V29 | PASS | Runtime IDs are assigned to source and live allocation/coordination objects only. |

PLAN_STRUCTURE=VALID
