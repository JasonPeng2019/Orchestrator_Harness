# General Multi-Agent Harness Retrofit - Modular Execution Plan

## 0. Plan contract and status

| Field | Value |
|---|---|
| Plan ID | GENERAL-HARNESS-PLAN-2 |
| Plan version | 3.9.23 |
| Verification protocol | `CHECKPOINTED_VERIFICATION_V1`; `FAST_LANE_V2` is available only under P04. |
| Status | Generic release and M07/M08 credit remain accepted. ROOT-IM reconciled the retained `055a5bd137039eaa1917e4a859a3d5bf30eb6444` watcher-repair boundary through empty final review 062, accepted proof 063, and integration/readback 064. The exact bound repair base is the clean `firmware/v2-candidate` and detached target at `dd673cb304501bfc2228b8c44f41df45a0c8608f` (tree `c18ccd0bc88de9c8fae1f98652a12fb5c1a951ae`). Suites 003-008 are stopped and exposed the contract defect recorded in `HANDOFF_SPRINT_FAILURE.md`: interruptions were terminalized instead of letting the same logical sprint complete and pool findings. No manager, provider, watcher, claim authority, lease, MCP action, or hardware action is live. `EDGE-010R` is ready for ROOT-IM to dispatch the one minimal continuation repair through the existing M02-M06 route plus one four-case no-hardware check; there is no separate recovery module, controller, gate, or protocol. Live work remains blocked until that repair is accepted and the affected M08 proof passes. The harness-clean streak is `0/3`. |
| Current-run support | The portable bounded-command adapter also tolerates the observed Windows `taskkill` enumeration/termination race without losing the terminal timeout record. The production delta is five lines scoped to that native call; the existing observed-PID check still decides `cleanup_verified`. A compact temporary-copy shim regression plus the six existing supervisor tests passed in both the support worktree and ROOT (7 each), and two real short timeout smokes returned `TIMED_OUT`/124 with cleanup verified. The change-aware verifier admits exactly `Invoke-BoundedTest.ps1` and selects its focused supervisor regression; 16 route tests passed in worktree and ROOT, the stable controller accepted commit `858d87c665ef432f9932ca4fc400894ad49edbf7`, and the final ROOT changed-code gate passed 99 focused tests in 72.371 supervisor seconds with verified cleanup. This remains current-run `.codex` support, not WIP product source. |
| Decision owner | ROOT-IM |
| Operative document boundary | This document is the sole current execution contract. It replaces the former bespoke physical-campaign graph. `goal.md` retains the product outcome and hardware authority; `HANDOFF.md` records accepted status and must not create a successor edge. |
| Change procedure | ROOT-IM classifies the semantic effect of a direct user change, preserves unaffected accepted work, amends and validates this plan before a new graph or authority route is used, and resumes the union of failed, unresolved, changed-input-affected, or uncertain check units from its earliest required unit. |
| Definition of valid | All Section 16 rows are PASS, the topology validator passes, no obsolete campaign edge remains live, and no plan action has been executed merely by this document change. |

Module catalog order is not execution order. Only Section 8 edges define runtime order.

## 1. Inputs, authority, and directive hierarchy

| Source | Authority | Path/reference | Supplies | Conflict rule |
|---|---|---|---|---|
| SRC-001 | OPERATIVE | Current direct user instruction | Preserve the previously accepted small-harness, retirement, hardware-authority, and role-boundary requirements. The declared live fixture remains authorized, but first correct the documentation/runtime lifecycle defect in the smallest effective way. A logical sprint must keep the same identity across manager/provider replacement, continue every feasible independent lane, and reach a completed terminal handoff despite administrative, provider, malformed-call, doer, specification, fixture, or harness errors. A genuine WIP target-v2 harness defect is recorded in the sprint's complete finding pool and reviewed/repaired only after that sprint completes; it earns no clean credit and resets the clean streak, but it does not turn the sprint into `INCOMPLETE` or trigger a cold restart. Suite-owned errors are corrected or recorded inside the same sprint and never masquerade as harness failures. Only explicit user cancellation, withdrawn authority, or live harm that cannot be isolated safely may end a sprint `INCOMPLETE`. Implement and perform one focused no-hardware continuation check after the current accepted M08 progress by reusing MI-HARNESS-REPAIR, the existing optional M03 asset route, MI-CANDIDATE-EVIDENCE, MI-CANDIDATE-DECIDE, MI-CANDIDATE-INTEGRATE, affected release assurance, and affected MI-FIRMWARE-HOST-READINESS. Concrete models remain solely in SRC-009. | Direct user instruction prevails. |
| SRC-002 | OPERATIVE | `goal.md` | General cross-provider product outcome and user-only hardware authority. | Current direct instruction supersedes only its obsolete campaign topology; hardware safety and fresh confirmation remain controlling. |
| SRC-003 | OPERATIVE | `AGENTS.md` | Repository development, bounded-execution, verification, and worktree rules. | Applies to repository development and all covered commands. |
| SRC-004 | STATUS | `HANDOFF.md` | Accepted coordinate, pause state, active-process state, and retained historical evidence. | Records facts and the next already-authorized edge; it cannot change this plan. |
| SRC-005 | REFERENCE | `chat_references/plan-2-firmware-validation-amendment-instructions.md` | The accepted simplification: external-suite validation and campaign retirement. | Consumed by this amendment; it is not a second runtime policy source. |
| SRC-006 | TARGET TOOL | `Firmware/.codex/skills/run-firmware-test-suite/SKILL.md` | External suite execution, review, leasing, watcher, retest, and repair process. | Governs the suite when invoked; it does not override user hardware authority or this plan's acceptance decision. |
| SRC-007 | TARGET TOOL | `Firmware/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` | Real experiment catalog, catalog eligibility, isolation cases, and real acceptance oracles. | ROOT-IM selects one eligible catalog scenario; catalog row order is not execution order. |
| SRC-008 | HISTORICAL STATUS | `Firmware/multi-agent-logs/HANDOFF.md`, `Firmware/multi-agent-logs/PROGRESS_REMAINING.md`, and `Firmware/multi-agent-logs/current-state/CURRENT_SUITE_STATE.json` | Imported safe resume boundary and closed historical validation facts. | Never becomes live authority, a live lease, or permission to resume a process. |
| SRC-009 | LAUNCH SELECTION ONLY | `plans/general-coding-harness/SUBAGENT_ROLE_MODEL_MAPPING.json` | The sole concrete provider allocation for workflow roles. | Resolves roles only at dispatch; it cannot alter task semantics, graph order, or authority. |
| SRC-010 | RUNTIME FACT | `stable-general-harness-runner/` and the accepted WIP candidate described by SRC-004 | Stable lane/session launching and the target product's actual provider, watch, watcher, and lifecycle behavior. | Source and executable behavior override prose claims about automation. |
| SRC-011 | TARGET CONFIGURATION | `Firmware/PROVIDER_ADAPTER.md` | Firmware-suite provider-role allocation, project-local Qwen Code/Ollama configuration, and the Firmware-owned external `qwen_provider_bootstrap.py` target-provider bridge. | The bridge registers `qwen-code` in the accepted target's existing external adapter registry in the same controller process; it does not modify the WIP core or create a second controller. Direct Qwen smokes passed for DeepSeek and Qwen 397B; the target-lane smoke then proved Qwen/DeepSeek session launch, local BYO MCP registration/listing, exact no-tool return, and owned cleanup. Codex is not an admitted route. |

| Layer | Authority | May define | Must not override |
|---|---|---|---|
| 1 | Direct user instructions and goal/spec | Required outcome and authority | N/A |
| 2 | This execution plan | Global workflow and selected graph | Layer 1 |
| 3 | Module instance | Its bounded project-specific behavior | Layers 1-2 |
| 4 | Local task card | Authorized task inputs/actions | Layers 1-3 |
| 5 | Handoff/status | Current facts and next authorized edge | Layers 1-4 |
| 6 | Runtime results | Materialized facts needed by a consumer | Any policy layer |
| 7 | Role-model mapping | Concrete launch selection only | Task semantics or graph order |

## 2. Goal, exclusions, and acceptance outcomes

Goal: Finish the small general, cross-provider coding harness without a second workflow engine or a built-in physical campaign. Preserve generic and schema-less firmware compatibility; have ROOT-IM inspect the already isolated opt-in `firmware_acceptance/` package and decide first whether each behavior genuinely belongs in a generic firmware-access harness. A behavior qualifies only when it accepts the caller's declared worktree, provider/server configuration, and resource selections; performs a reusable firmware-access responsibility such as process lifecycle, MCP connection or observation, lease/resource ownership, authorization propagation, handoff/cleanup, or schema-less invocation compatibility; and does not retain a fixed C1/C2/C3 scenario, fixture set, evidence graph, campaign controller, or duplicate of an existing harness or external-suite responsibility. Firmware-specific behavior is valid, including MCP/process, lease, and hardware-access behavior needed to reach hardware through the external Firmware MCP server. Apparent similarity to that server is not disqualifying because the package predates the copied server and the server is the required hardware-access route. Retired campaign control, fixed campaign topology/evidence, and other extraneous behavior do not belong. A current consumer cannot justify those rejected responsibilities, so its dependency is unwound; a qualifying firmware-access behavior may be retained or minimally rehomed, and if it has no current consumer it is wired through the smallest existing firmware compatibility seam and tested rather than kept dormant. Then one coding subagent implements the directive; the obsolete campaign remainder and its attachments are removed; the generic capability broker remains; one disposable host-only mapping-resolved harness-to-MCP connection simulation runs with no tool call; and the relevant real firmware behavior is validated through the existing external Firmware experiment suite only after the Firmware-specific adapter exists and the user later confirms a live fixture.

| Outcome ID | Required behavior | Acceptance method | Decision owner | Status |
|---|---|---|---|---|
| OUT-001 | The accepted generic candidate remains a small cross-provider coding harness with the completed adapter and workspace-overlay behavior. | Existing accepted integration result at the frozen coordinate; affected checks only after a later change. | ROOT-IM | COVERED |
| OUT-002 | The repository no longer carries or advertises the obsolete physical-campaign controller, fixed campaign topology/evidence, or other extraneous support. Firmware behavior found inside the isolated package survives when ROOT-IM establishes that it is useful to a generic firmware-access harness; MCP/process, lease, and hardware-access behavior may qualify even when related to the external Firmware MCP server. An existing consumer of rejected campaign/extraneous behavior is unwound from it; a legitimate behavior without a current consumer is wired into the existing firmware compatibility layer and tested. The coding subagent implements that directive without redefining the architecture; and the installed generic harness, generic capability broker, lifecycle behavior, and schema-less firmware invocation compatibility remain intact. | ROOT-IM responsibility-level legitimacy and consumer-routing directive, one serial implementation, focused independent review of both, and affected retained-component plus generic/compatibility checks. | ROOT-IM | COVERED |
| OUT-003 | The integrated candidate satisfies its already-declared UTF-8/format source contract, owns a stable high-value Ruff lint contract instead of inheriting changing tool defaults, and then receives proportionate final generic-harness assurance. | One exact lossless normalization of the sole non-UTF-8 tracked file, the existing Ruff-format correction, deterministic reproduction and no-new-lint comparison, one focused release-registry repair selecting `E9,F63,F7,F82`, ROOT-IM integration, final review, and the candidate-owned accumulated release safeguard. | ROOT-IM | COVERED |
| OUT-004 | Before any physical allocation, ROOT-IM resolves `acceptance-orchestrator` from the canonical mapping and the accepted WIP target launches one disposable provider session to prove its lane lifecycle, finite watch/watcher observation, harness-to-MCP stdio connection and negotiation, terminal handoff, and cleanup without invoking an MCP tool or initiating hardware discovery/access. | One M08 readiness simulation using the actual accepted target launcher and MCP connection path with disposable inputs; it is readiness evidence, not a product, Firmware-provider-adapter, MCP-tool, or hardware pass. | ROOT-IM | COVERED |
| OUT-005 | After one focused no-hardware continuation repair/check, three consecutive completed, accepted existing Firmware catalog logical sprints prove the relevant real multi-agent behavior without a WIP target-v2 harness error; concurrent-board isolation is claimed only when a selected case covers it. Every sprint continues until it publishes `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`. Harness findings are pooled at completion, then reviewed/repaired through the existing harness route; that sprint earns no clean credit and resets the streak. | The current defect uses the existing M02 -> optional M03 -> M04 -> M05 -> M06 path and the single `CHECK-SPRINT-CONTINUATION`, followed by affected release/M08 proof. Live sprints then use sealed specifications, independent reviews, execution evidence, cleanup, terminal ROOT-only review, and index-ordered streak decisions. | ROOT-IM | CONTINUATION REPAIR/NO-HARDWARE CHECK REQUIRED BEFORE LIVE SPRINT |
| OUT-006 | Only the accepted generic candidate and accepted external-suite result may be promoted; otherwise all accepted non-consuming work remains preserved. | Promotion readback and retained rollback state. | ROOT-IM | OPEN |

| Boundary ID | Type | Included/excluded/authorization condition | Reason | Owner |
|---|---|---|---|---|
| BOUND-001 | Authorization | The user has resumed the declared four-board hardware phase and ROOT-IM has bound the accepted base. Preserve accepted generic release and unaffected M08 credit. Before live behavior, accept/integrate the focused continuation repair, pass `CHECK-SPRINT-CONTINUATION` on the exact integrated target through affected M08, record the fresh invocation, and issue fresh authority for each new live action. Durable semantic checkpoints may be reused; stopped processes, sessions, plans, permissions, and leases are never treated as current merely because the logical sprint continues. | Keeps live authority exact without discarding valid sprint progress or adding a second recovery workflow. | ROOT-IM |
| BOUND-002 | Acceptance | Promotion requires three consecutive index-ordered, completed, accepted logical sprints with `harness_error_observed=false`. Administrative/provider/manager interruption, malformed calls, doer/specification/fixture/server faults, and claim waits do not terminate a sprint. Every feasible lane continues; the affected lane is corrected or records a terminal finding. A sprint with a genuine harness defect still completes, publishes the full harness finding pool, earns no clean credit, and resets the streak to `0/3`; only after completion may ROOT-IM dispatch the existing repair route. A suite-owned defect may count once corrected and the same sprint completes accepted without a harness defect. | Measures repeatable harness cleanliness without rewarding cold restarts or turning ordinary failures into abandoned sprints. | ROOT-IM |
| BOUND-003 | Scope | The general harness does not own boards, MCP calls, catalog scheduling, evidence authority, or firmware-server repair decisions. | The existing Firmware suite owns those campaign responsibilities. | ROOT-IM |
| BOUND-004 | Scope | Candidate inspection already establishes that `firmware_acceptance/` is a separate opt-in repository package: it is absent from the installed package list, generic runtime modules do not import it, and it imports the generic capability broker rather than owning it. The task therefore decides what deserves to survive from the isolated package; it does not separate campaign code from the core. Before allocating the writer, ROOT-IM reads every source responsibility and the current core/Firmware ownership contracts, then issues the complete retain/minimally-rehome/wire/unwind/delete directive. Architectural legitimacy is the first gate and is independent of current consumer status. A behavior has a legitimate harness home only when it accepts caller-declared worktree, provider/server, and resource inputs; provides a reusable process-lifecycle, MCP connection/observation, lease/resource, authorization, handoff/cleanup, or schema-less invocation responsibility; and neither retains a fixed C1/C2/C3 scenario, fixture set, evidence graph, or campaign controller nor duplicates an existing harness seam or external-suite responsibility. This can include MCP/process coordination, leases, and other hardware-access behavior related to the external Firmware MCP server, because that server is the required hardware-access path; apparent server similarity alone is not a rejection criterion. Retired campaign control, attempt/evidence machinery, fixed campaign topology, duplicate responsibilities, and other extraneous behavior do not have a legitimate harness home. If qualifying behavior has a current consumer, retain or minimally rehome it; if it has none, wire it into the smallest existing firmware compatibility seam and add one focused oracle. A current consumer cannot justify rejected campaign/extraneous behavior: change the harness seam to unwind that dependency and remove the rejected responsibility. Code is not preserved merely because it is well written or historically related. The writer implements that directive and returns any contradiction to ROOT-IM rather than making a new semantic choice. `orchestrator_harness.capability_broker` and its genuinely generic tests remain. | Put the high-context architectural decision with ROOT-IM while preserving one small serial implementation task and the existing independent review. | ROOT-IM |
| BOUND-005 | Historical | Imported Q10 state, prior PIDs, leases, configurations, watcher state, and absent run roots are not live state; the prohibited next historical attempt is never launched. | Imported records preserve history, not a resumable runtime. | acceptance-orchestrator |
| BOUND-006 | Scope | Direct executables remain outside the repository's mechanical bounded-launcher hook boundary. A configured PowerShell launch checks an executed `-File` path and mechanically inspects one ordinary `-Command`/`-c` body for the same configured Python, `.ps1`, and Bash/sh launchers; it does not parse encoded commands or infer command meaning. Agent/provider sessions remain lane-managed rather than test-bounded. | This exactly matches the small current adapter boundary and avoids semantic detection or a PowerShell-parser subsystem. | ROOT-IM |
| BOUND-007 | Prerequisite | The external Firmware route is package-owned: project-local Qwen Code/Ollama configuration plus the Firmware-owned bridge in SRC-011. It uses the accepted target's existing adapter registry and lane controller rather than changing the WIP core. Its focused unit test, direct local Qwen smokes, and no-tool target-lane MCP smoke passed. Fresh fixture identity, server plan, permission, and lease remain mandatory per sprint. | Preserves the proven connection-only proof while holding live operation on concrete, observed admission facts. | ROOT-IM |
| BOUND-008 | Recovery | A logical sprint is not a manager epoch or provider session. On interruption, preserve its ID/index, sealed specification, verified checkpoints, completed evidence, and accumulated findings. Replace dead runtime identities, verify the old owner/process tree and live action are absent, release/reassign a stale claim only when that absence makes it safe, and let uncertainty hold only the exact resource. Resume the affected unit and continue unrelated eligible lanes. Do not repair harness source mid-sprint: first complete the sprint and its pooled terminal handoff. | Directly prevents the suites 004-008 cold-start/terminalization pattern with one continuation rule. | ROOT-IM and Firmware suite manager |

## 3. Requirement coverage map

| Requirement ID | Source | Deliverable ID | Implementation owner | Verification | Acceptance owner | Status |
|---|---|---|---|---|---|---|
| REQ-G01 | SRC-002 outcome | DEL-GENERAL-FROZEN | coder-main | Existing accepted workspace-overlay integration; affected rerun only after changed input | ROOT-IM | COVERED |
| REQ-G02 | SRC-002 outcome | DEL-GENERAL-FROZEN | coder-main | Existing accepted provider-adapter and general lifecycle credit | ROOT-IM | COVERED |
| REQ-R01 | SRC-005 retirement directive and current direct instruction | DEL-CAMPAIGN-RETIREMENT | ROOT-IM semantic directive; coder-main implementation | ROOT-IM classifies every `firmware_acceptance/` source responsibility first by usefulness to a generic firmware-access harness and then by consumer route; coder-main implements the resulting retain/minimally-rehome/wire/unwind/delete directive; the generic capability broker remains | ROOT-IM | COVERED |
| REQ-R02 | SRC-005 retirement directive | DEL-CAMPAIGN-RETIREMENT | coder-main | Focused review plus affected legacy-compatibility and general-harness checks | ROOT-IM | COVERED |
| REQ-R03 | SRC-002 compatibility outcome | DEL-CAMPAIGN-RETIREMENT | coder-main | Affected generic lifecycle and schema-less firmware invocation checks | ROOT-IM | COVERED |
| REQ-A02 | Candidate-owned release safeguard and current Ruff evidence | DEL-RELEASE-FORMAT | coder-main mechanical source normalizer/formatter | Exact reproduction of the declared lossless encoding normalization and Ruff output from the parent, all-tracked-file UTF-8 scan, repository-wide format check, proof that the transformed tree introduces no Ruff finding absent from its parent, compilation, and whitespace-error check | ROOT-IM | COVERED |
| REQ-A03 | Candidate-owned release registry and current Ruff 0.16.1 evidence | DEL-RELEASE-LINT-CONTRACT | coder-main affected repair | The registry's Ruff command explicitly selects `E9,F63,F7,F82`; a focused registry oracle proves the exact command, the current formatted candidate passes it, format output remains unchanged, and the affected release-selector/safeguard checks pass | ROOT-IM | COVERED |
| REQ-A01 | SRC-002 product outcome | DEL-RELEASE-ASSURANCE | coder-main owns the admitted product corrections; final-reviewer and doer-main retain the Plan-wide M03/M04/M06 evidence roles | Accept generic release behavior only after the integrated candidate's checkpointed safeguard completes every required unit, its complete finding pool is decided, and the independent final review agrees | ROOT-IM | COVERED |
| REQ-A04 | `TOPOLOGY_VERIFICATION_EFFICIENCY.md` and current safeguard behavior | DEL-RELEASE-ASSURANCE | coder-main owns the one admitted safeguard-executor correction; doer-main proves it through ordinary candidate evidence | Existing candidate safeguard continues ordinary independent units after a failure, records check-unit outcome and first unresolved state, conservatively maps inputs to units, and on a later integrated change reuses only unaffected PASS credit while running the failed/unresolved/affected/uncertain union from its earliest unit | ROOT-IM | COVERED |
| REQ-H01 | Current direct instruction and SRC-011 | DEL-FIRMWARE-HOST-READINESS | acceptance-orchestrator | Disposable accepted-target launch through the mapping-resolved role, with finite observation, target-launched MCP initialization and `tools/list` protocol evidence, a no-tool provider alias/status handoff, provider events showing no tool execution, an absent-or-empty disposable server tool-event file, terminal handoff, and verified cleanup. ROOT's already accepted static registration/raw MCP comparison remains the exact catalog oracle because Codex defers custom tool definitions from the model's initial context. | ROOT-IM | COVERED |
| REQ-F01 | SRC-005 external-suite route and SRC-001 completion rule | DEL-FIRMWARE-VALIDATION | acceptance-orchestrator | Three consecutive index-ordered completed catalog sprints through the suite's sealed-spec/evidence process plus terminal ROOT-only harness-evidence review; each has `harness_error_observed=false`. | ROOT-IM | BLOCKED ON FOCUSED CONTINUATION PROOF |
| REQ-F02 | SRC-001, BOUND-002, BOUND-008, SRC-008 history, and SRC-011 adapter boundary | DEL-FIRMWARE-VALIDATION | coder-main for the focused product repair when needed; doer-main for verification assets/checking; acceptance-orchestrator for exact-target M08 and live sprints | Before live use, `CHECK-SPRINT-CONTINUATION` proves four no-hardware cases under generated `tmp/plan2-no-hardware-recovery/{invocation_id}/` state with zero MCP-tool/hardware events and exact cleanup. Then record `0/3` through `3/3` by sprint index; a completed harness-error sprint resets/no-counts but is never `INCOMPLETE`. | ROOT-IM | ACTIVE AFTER CURRENT M08 PROGRESS |
| REQ-P01 | SRC-002 product outcome | DEL-PROMOTION | ROOT-IM | Exact promotion readback after the required preceding acceptances | ROOT-IM | OPEN |

## 4. Runtime and repository truth

| Capability/action | State | Source of truth | Invocation owner | Preconditions | How confirmed | Fallback |
|---|---|---|---|---|---|---|
| Accepted generic candidate | RUNTIME_ENFORCED | SRC-004 status coordinate | ROOT-IM | Clean accepted source allocation | Existing post-join result and handoff | Preserve credit; rerun only affected checks after a change. |
| Required release-source formatting | TARGET_TOOL_INVOKED | Candidate-owned release registry and authoritative Ruff 0.16.1 | coder-main for one exact encoding normalization plus formatter; doer-main for deterministic reproduction/check execution; ROOT-IM for proof contract and decision | Clean canonical parent `3a73a7b`; one isolated writer worktree; unchanged Ruff configuration and release scope | Existing full-format check reports 93 format changes and then fails on the sole non-UTF-8 tracked file; CHECK-RELEASE-FORMAT reproduces its lossless Windows-1252-to-UTF-8 normalization, Ruff output, and conformance checks from the declared parent | Return only REQ-A02 to the same task; do not add an exclusion, change configuration, hand-edit content, or reopen accepted retirement/protocol work. |
| Stable release-lint contract | TARGET_TOOL_INVOKED | Candidate release registry plus current Ruff 0.16.1 parent/tip results | coder-main for one admitted affected repair; ROOT-IM for decision | REQ-A02 exact formatter tip is accepted and integrated; repair changes only the existing Ruff check specification and focused registry/safeguard tests | Untouched parent has 420 full-default findings, exact formatter output has 409, and the formatted output passes explicit high-value selectors `E9,F63,F7,F82`; CHECK-CANDIDATE-REPAIR proves the candidate owns those selectors without changing format output | Do not repair the 409 pre-existing style findings, add a configuration subsystem, or weaken any other release check; return only a failure of the explicit lint contract through EDGE-006B. |
| Retained attention practical, unit, and guide | TARGET_TOOL_INVOKED | Candidate `harness_watcher_implementation/tests/run_attention_practical.py`, `harness_watcher_implementation/tests/test_attention_practical_retention.py`, `harness_watcher_implementation/ATTENTION_LOGGING.md`, current S4 host-delivery tests, and the accepted removed-policy oracle | doer-main for the independent verification-asset correction, declared checks, and exact accepted integration mechanics; ROOT-IM for classification and decision | Initial clean canonical `c114d3f`; the accepted retry used the repaired canonical coordinate supplied by EDGE-007T; M03 remained limited to the three verification paths | The final safeguard first exposed five absent attention-policy helpers. The first clean M03 attempt then exposed removed manager flags and retired diagnostic-watch `MANAGER_WAKE_*` output in the practical/unit. Current S4 oracles prove sparse adapter delivery and idle-boundary wake; `test_FC5_removed_policy_has_no_live_output_surface` requires the old policy surface to stay absent. | The accepted change removed the stale policy block, replaced only the obsolete diagnostic-watch wake producer/assertions with current host-adapter delivery plus a fresh-empty-queue quiet proof, updated the guide, preserved unrelated practical checks, and did not restore or edit product APIs. |
| Stable lane/session launch | RUNTIME_ENFORCED | `stable-general-harness-runner/` | ROOT-IM | Declared lane, worktree, role, and result path | Existing completed lane-managed sessions | Use structured handoff when a provider invocation cannot continue. |
| Covered Python interpreter, PowerShell-file, and Bash/sh launch | RUNTIME_ENFORCED | SRC-003 and repository `.codex/` policy chain | ROOT-IM or covered executor | Resolved launcher category is not excluded; unique result path; credible upper bound and cleanup allowance | Hook, supervisor result, heartbeat, terminal status, and process-tree cleanup | Classify timeout as support; do not retry unchanged failure. |
| Firmware provider launch route | TARGET_TOOL_INVOKED | SRC-011 | Firmware suite manager through the target's provider/lane lifecycle | Project-local Qwen Code/Ollama configuration; `OLLAMA_API_KEY=ollama`; role-specific model from `PROVIDER_ADAPTER.md`; fresh run roots and ordinary suite admission | No-hardware DeepSeek and Qwen 397B MCP handshake/plan smoke passed through the local project configuration. | Treat a route failure as an external-operation condition; do not substitute Codex without a new successful local probe. |
| Disposable host-only Firmware readiness | TARGET_TOOL_INVOKED | Current direct instruction, SRC-006 connection procedure, SRC-007 Phase H connection checks, SRC-009 role mapping, and SRC-010 accepted target runtime | ROOT-IM materializes the mapped role into a canonical target invocation; the accepted target launches acceptance-orchestrator | Accepted generic release; clean package-local target; mapping-resolved role; disposable server/run roots; accepted static/raw 39-name catalog comparison; source trace proving startup and `tools/list` remain in process-hygiene/run-state/tool-metadata seams and do not call probe or serial inventory/open code | MI-FIRMWARE-HOST-READINESS exercises the accepted target's lane/watch/watcher/provider/MCP-connect/handoff/cleanup path; a task-local MCP launcher records target-startup and server protocol stderr, the target-launched server records `ListToolsRequest`, the no-tool provider returns only the configured alias/status, provider events show no tool execution, and the disposable server tool-event file is absent or empty | Hold readiness if the side-effect-free path, target protocol listing, or no-tool result cannot be established; do not launch, allocate a fixture, invoke an MCP tool, or infer product/hardware success. |
| External Firmware suite orchestration | TARGET_TOOL_INVOKED | SRC-006, SRC-007, SRC-011, BOUND-008, and EXC-SUITE-CONTINUATION | acceptance-orchestrator | Accepted connection/continuation proof; implemented Firmware provider route; current authority; predeclared logical sprint IDs/indices; package-local target; fresh authority per live action | Suite preflight, one completed terminal handoff per logical sprint, and complete finding pools | Keep each logical sprint active across recoverable interruption; continue feasible lanes, isolate exact hazards/resources, and publish `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`. |
| Interrupted-sprint continuation | TARGET_TOOL_INVOKED | `orchestrator_harness/resource_locks.py`, `resume.py`, `lane_controller.py`, `reconcile.py`, suite checkpoints, and `HANDOFF_SPRINT_FAILURE.md` | ROOT-IM for contract/acceptance; coder-main for admitted product change; doer-main for the one focused proof | Exact accepted base reconciled; no prior live authority; generated fake-only roots; existing M02-M06 route | `CHECK-SPRINT-CONTINUATION` plus affected M08 on the integrated target | If safe ownership cannot be proved, hold only the exact resource; never fabricate release or completion. |
| Package-local WIP target preparation | ORCHESTRATOR_ENFORCED | SRC-006 package boundary | External run owner | Exact accepted product worktree is selected or created below `Firmware/target-harness/` before suite launch | Git revision and dirty state recorded in the suite epoch ledger | Do not launch the suite until a fresh target is prepared. |
| Target bounded watch and deterministic watcher | TARGET_TOOL_INVOKED | SRC-006 watcher section | Firmware suite manager | Target exposes finite `orchestrator_harness watch --until-actionable --timeout` calls and one separate owner-bound `harness_watcher_implementation` process with evaluator disabled | Suite target preflight and epoch records | Mark the affected observation claim unavailable; do not invent a stable-only managed watch or heartbeat protocol. |
| Live hardware allocation | ORCHESTRATOR_ENFORCED | SRC-002 and BOUND-001 | Firmware suite manager | Current recorded user authorization, fresh selected-scenario assignment, stable electronic identity, server plan/permission, and exact resource leases | The current user authorization plus the suite's admission/readback records | Hold only the affected sprint if allocation facts are incomplete; no product loop. |
| Isolated campaign salvage and retirement | ORCHESTRATOR_ENFORCED | Candidate source, package configuration, tests, release registry, public docs, and current optional-firmware/external-suite seams | ROOT-IM semantic owner; coder-main implementation writer | User resumes; starting candidate is clean; ROOT-IM completes the responsibility-level legitimacy and consumer-routing directive before writer allocation | Candidate inspection shows `firmware_acceptance/` is not installed, has no generic-runtime reverse import, and consumes the generic `capability_broker`. Its firmware capability adapter/campaign-pack translation and process/MCP helpers require ROOT-IM judgment, not automatic retention; MCP/server relationship alone is not a rejection signal because server-backed access is how hardware is reached. The old controller, attempt/evidence chain, pinning, and fixed-fixture campaign topology have no current authority. | ROOT-IM retains `orchestrator_harness.capability_broker`; preserves other firmware-specific behavior when it is useful to a generic firmware-access harness; wires legitimate unused behavior into the existing firmware compatibility layer; and unwinds any consumer from rejected campaign/extraneous behavior before removal. coder-main performs the specified code/test/doc/release edits and focused oracles; any contradiction returns to ROOT-IM instead of expanding scope. |

## 5. Deliverable, dependency, risk, and cost model

| Deliverable ID | Behavioral output | Requirement IDs | Dependencies | Shared seams | Release unit |
|---|---|---|---|---|---|
| DEL-GENERAL-FROZEN | Accepted generic harness coordinate preserved as the input to all remaining work. | REQ-G01, REQ-G02 | Existing accepted integration | Provider adapter, lane lifecycle, workspace overlay, generic compatibility surface | General harness candidate |
| DEL-CAMPAIGN-RETIREMENT | ROOT-IM decides the responsibility-level retain/minimally-rehome/wire/unwind/delete boundary for the already isolated `firmware_acceptance/` package; one serial writer implements it, preserving useful generic firmware-access behaviorâ€”including qualifying MCP/process, lease, and hardware-access behaviorâ€”while removing obsolete campaign/extraneous machinery and its repository attachments. | REQ-R01, REQ-R02, REQ-R03 | DEL-GENERAL-FROZEN | Optional firmware capability seam, dedicated and mixed tests, release-check selection/compilation, public docs, and generic compatibility | General harness candidate |
| DEL-RELEASE-FORMAT | The sole non-UTF-8 tracked file is losslessly normalized from Windows-1252 to UTF-8, the clean accepted candidate is then transformed by Ruff's existing repository-wide formatter, and the result equals a fresh deterministic reproduction from its declared parent. | REQ-A02 | DEL-CAMPAIGN-RETIREMENT and the accepted protocol repair at canonical `3a73a7b` | Candidate source tree, named canary guide, existing Ruff configuration, and release format criterion | General harness candidate |
| DEL-RELEASE-LINT-CONTRACT | The candidate-owned release registry selects a stable, high-value Ruff correctness set instead of inheriting version-dependent default style rules. | REQ-A03 | DEL-RELEASE-FORMAT acceptance and integration | Existing release registry, selector, safeguard, and focused release tests | General harness candidate |
| DEL-RELEASE-ASSURANCE | The integrated candidate with its explicit release-lint contract, valid Codex assets, and truthful attention practical receives final general-harness assurance through a checkpointed, nonredundant candidate safeguard. | REQ-A01, REQ-A04 | DEL-RELEASE-LINT-CONTRACT acceptance/integration, accepted attention correction, and the checkpoint-safeguard correction accepted/integrated | Generic unit/integration suite, release-check registry, safeguard executor, retained attention practical/unit/guide, and public behavior | General harness candidate |
| DEL-FIRMWARE-HOST-READINESS | One disposable no-hardware run resolves `acceptance-orchestrator` from the canonical mapping and uses the accepted target launcher to prove the exact provider/lane/watch/watcher/MCP connection path before any physical allocation or MCP-tool call. | REQ-H01 | DEL-RELEASE-ASSURANCE acceptance | Package-local target, mapped provider lane lifecycle, finite watch/watcher observation, MCP stdio initialization/tool discovery, handoff, cleanup | External-operation readiness result |
| DEL-FIRMWARE-VALIDATION | The existing suite completes logical sprints across replaceable runtime invocations. Before live use, the existing repair/evidence/integration pipeline implements the smallest required target correction and one focused four-case no-hardware check. Thereafter each sprint publishes a complete finding pool before ROOT review: `COMPLETED_CLEAN` may earn indexed streak credit; `COMPLETED_WITH_FINDINGS` never becomes `INCOMPLETE`; a genuine harness finding resets/no-counts and is repaired only after completion through the existing route. | REQ-F01, REQ-F02 | DEL-FIRMWARE-HOST-READINESS pass, DEL-RELEASE-ASSURANCE acceptance, BOUND-001, BOUND-002, BOUND-007, and BOUND-008 | Package-local target, Firmware provider adapter, existing repair pipeline, suite checkpoints/leases/reviews, `CHECK-SPRINT-CONTINUATION`, and indexed ledger | External validation result |
| DEL-PROMOTION | Accepted candidate advances with rollback retained. | REQ-P01 | DEL-RELEASE-ASSURANCE and DEL-FIRMWARE-VALIDATION | Integrated coordinate, final verdicts, promotion destination | Released general harness |

| Deliverable ID | Realistic failure | Impact | Coupling | Expected range | Expensive operations | Cheapest adequate topology | Why |
|---|---|---|---|---|---|---|---|
| DEL-CAMPAIGN-RETIREMENT | A lower-context writer makes an architectural retention decision, useful generic firmware-access behavior is discarded because it resembles server-backed hardware access, campaign/extraneous behavior survives merely because something currently calls it, legitimate unused behavior remains dormant instead of being wired into the firmware compatibility layer, or a mixed test/release/doc reference becomes stale. | The harness loses earned generic firmware-access capability or continues carrying obsolete campaign complexity. | Isolated package plus repository tests, release registry, and docs; low coupling to installed runtime | 25-50 minutes | One ROOT-IM responsibility review, one serial implementation, and focused parallel evidence | ROOT-IM directive inside M02 admission -> M02 writer -> M04 -> M05 -> M06 | ROOT-IM already owns architecture and acceptance, so reading the isolated package once before dispatch avoids a likely semantic repair loop. The existing writer, reviewer, and gate remain sufficient; no extra module or agent is added. |
| DEL-RELEASE-FORMAT | Encoding normalization changes text, an exclusion/configuration change hides the failure, or formatter output contains an unintended semantic change. | The safeguard remains red or accepted product behavior/content is altered by a release-conformance correction. | One named 842-byte guide plus repository-wide source formatting; mechanically broad but semantically narrow | 10-25 minutes | One exact lossless transcoding, one formatter run, and one deterministic reproduction/check campaign | M02 source normalization/formatter -> existing M04/M05 candidate gate -> M06 | The file round-trips as Windows-1252 and has one non-ASCII em dash, so byte decoding/re-encoding is the smallest complete correction. Reproducing both transformations from the clean parent is stronger and cheaper than a broad static review. |
| DEL-RELEASE-LINT-CONTRACT | Ruff's changing default rule selection turns the release gate into hundreds of unrelated style findings or a future environment-dependent result. | The candidate safeguard cannot give a stable, meaningful lint verdict. | One existing release check tuple plus its focused registry/safeguard tests | 10-20 minutes | One two-file-or-smaller repair and affected evidence; no mass lint cleanup | Existing MI-HARNESS-REPAIR -> existing M04/M05/M06 | Explicitly selecting the already-proven critical rules `E9,F63,F7,F82` in the existing command is smaller and more reliable than adding configuration machinery or editing 409 unrelated findings. |
| DEL-RELEASE-ASSURANCE | An integrated change breaks a generic cross-seam behavior, retained verification assets exercise retired behavior, or the candidate safeguard loses useful credit by stopping early and restarting an unchanged prefix. | Wrong release acceptance or an accumulated gate that cannot decide efficiently. | Existing safeguard script/registry plus generic unit/integration and public behavior | 20-45 minutes for a cold complete run; later runs execute only required units | One narrow executor/registry correction, ordinary candidate evidence/integration, then one final review plus the candidate-owned checkpointed safeguard | M02 checkpoint correction -> existing M04/M05/M06 -> M07 -> M05 | The existing safeguard remains the right accumulated oracle, but its current fail-fast loop is not. Independent coarse check units, a conservative map, and a small checkpoint result add no scheduler or new service while preventing repeated unchanged work. The existing affected lifecycle supplies independent review before final assurance. |
| DEL-FIRMWARE-HOST-READINESS | The canonical role cannot be resolved, the accepted target cannot launch it, or the target/watch/watcher/MCP connection path cannot complete one disposable lifecycle without entering a hardware path. | A live sprint would spend scarce fixture time debugging control machinery that can be proven before the Firmware-specific adapter exists. | Mapped provider/accepted target/MCP connection integration | 5-15 minutes after generic release | One disposable mapped provider session and MCP server process; zero MCP tool calls and zero USB/fixture allocation | M08 | One connection-only simulation closes the useful pre-hardware control gap now. Firmware-adapter-specific role launch and tool execution remain honestly unproven until the hardware-sprint prerequisite is supplied. |
| DEL-FIRMWARE-VALIDATION | A dead controller leaves a stale claim, a replacement session cannot use verified progress, a correctable call/order fault terminalizes the epoch, or a harness defect cancels the sprint before the full pool exists. | The suites 003-008 pattern repeats and no sprint can finish. | Existing claim/resume/lane lifecycle plus suite contract | One focused repair/asset/evidence/integration pass and a 10-20 minute no-hardware M08 recheck; then three 20-40 minute live sprints | Four focused fake-runtime cases and only affected existing checks | Current M08 -> existing M02/M03/M04/M05/M06 -> affected M07/M08 -> M09/M05 until `3/3` | One check and the existing pipeline are sufficient; dedicated recovery modules, a second gate, and a second controller are explicitly omitted. |
| DEL-PROMOTION | Promotion/readback or cleanup cannot establish the intended destination. | Release operation is incomplete despite accepted behavior. | Destination coordinate | 5-10 minutes | One promotion and readback | M06 | It is an operation boundary, not a new product campaign. |

## 6. Workflow module selection manifest

| Module type | Decision | Instance IDs | Reason | Prerequisite/owner if deferred |
|---|---|---|---|---|
| M01 | DEFERRED | N/A | Generic work and host readiness need no prerequisite setup module. The later hardware sprint does require a Firmware provider adapter that does not exist yet, so that one prerequisite remains deferred without creating a live plan instance. | User/external run owner supplies the adapter and passes its local smoke before MI-FIRMWARE-SPRINT. |
| M02 | SELECTED | MI-CAMPAIGN-RETIRE, MI-HARNESS-REPAIR, MI-SAFEGUARD-CHECKPOINT-CORRECT, MI-RELEASE-FORMAT-CORRECT | ROOT-IM performs the high-context responsibility decision inside MI-CAMPAIGN-RETIRE admission, then one serial writer implements it. Historical release-lint and packaged-manifest repairs remain accepted. `MI-HARNESS-REPAIR` completed the combined one-file `stable_io.py` repair and its integration. Before assurance, `MI-SAFEGUARD-CHECKPOINT-CORRECT` makes the existing candidate safeguard incrementally reusable without a scheduler redesign: coarse existing checks become independently runnable, conservatively input-mapped checkpoint units that continue after ordinary failures. The release-format task remains distinct because it was a deterministic whole-source conformance operation rather than product repair or M03 test-asset work. | N/A |
| M03 | SELECTED | MI-ATTENTION-PRACTICAL-CORRECT, MI-VERIFICATION-ASSET-CORRECT | The current exact attention instance removes one obsolete policy exercise while preserving its wake/quiet oracle. The reusable instance supplies the previously missing typed route for any later Plan 2 product-repair or strict test-only loop whose ROOT-authored proof contract requires a verification-asset edit. It activates only with exact behaviors/goals, protected surfaces, allowed paths, classification, and acceptance criteria; otherwise a repaired tip uses existing trusted assets and proceeds directly to M04. | N/A |
| M04 | SELECTED | MI-CANDIDATE-EVIDENCE | The isolated-package salvage and retirement changes mixed tests, release selection, and public docs; one narrow independent review/check campaign covers those attachments and any admitted harness repair. Its format branch uses only deterministic reproduction and checks because Ruff already defines the transformation and a broad static review adds no stronger oracle. | N/A |
| M05 | SELECTED | MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-DECIDE | Every producer, assurance, and practical result needs one ROOT-IM semantic decision and classified route. | N/A |
| M06 | SELECTED | MI-CANDIDATE-INTEGRATE, MI-PROMOTE | Accepted source must be integrated before assurance; final promotion must retain rollback and read back destination state. | N/A |
| M07 | SELECTED | MI-RELEASE-ASSURE | The salvage/retirement change crosses optional-firmware, test, release, and documentation seams, so it warrants one proportionate accumulated safeguard over the integrated release unit. | N/A |
| M08 | SELECTED | MI-FIRMWARE-HOST-READINESS | The canonical mapping plus accepted target launcher can already prove target/provider, watch/watcher, and harness-to-MCP connection composition without invoking tools. One disposable no-hardware simulation is cheaper than waiting for the Firmware-specific adapter or debugging this shared path after fixture allocation. | N/A |
| M09 | SELECTED | MI-FIRMWARE-SPRINT | Real authorized Firmware catalog sprints are the practical oracle. The current first admission is blocked only on the focused continuation repair/check through existing modules; no separate recovery M09 or controller is added. | N/A |
| M10 | OMITTED | N/A | M01-M09 express every required behavior; a project-specific controller would duplicate M09 and the external suite. | N/A |

## 7. Roles and role-model mapping boundary

| Workflow role | Responsibilities | Pool | Context class | Write authority | Resources | Activation | Lifetime |
|---|---|---|---|---|---|---|---|
| coder-main | Serial implementer of ROOT-IM's isolated-package retention directive, any admitted generic-harness product defect, or the exact release-format command. This includes a real harness defect first exposed by candidate, release, or Firmware evidence after ROOT-IM classifies it and names the repair seam and proof contract. It reports contradictions instead of redefining semantics; on the format task it may run Ruff's formatter but may not hand-edit source or configuration. It terminates each card with a repair handoff to ROOT-IM and never launches checking or integration. | 1; source mutation is singular | Bounded change context | Declared candidate worktree only | One identified candidate worktree | MI-CAMPAIGN-RETIRE after ROOT-IM directive completion, any admitted MI-HARNESS-REPAIR, or EDGE-007F for MI-RELEASE-FORMAT-CORRECT | Keep the same provider session by default across implementation and every compatible material correction returned to the same unaccepted candidate gate. Each card still terminates at ROOT-IM; ROOT explicitly resumes the idle session with the next card. Retire it when that gate accepts or the logical task is otherwise terminal. If resume is unavailable or the mapping changed, replace it through the correlated handoff without blocking, restarting accepted work, or changing task meaning. |
| reviewer-main | Focused independent review of candidate retirement or repair evidence. | 1; one coherent review surface | Read-only bounded review | No product writes | Separate result root | MI-CANDIDATE-EVIDENCE | One review task; structured handoff preserves the frozen input if needed. |
| doer-main | Plan-wide verification implementer and deterministic executor. For every ROOT-IM proof contract, it chooses and implements the smallest selected verification assets and focused commands that prove every named behavior target while preserving every named no-change surface; it reports instead of guessing if that contract cannot be met. It owns every selected M03 verification-asset correction, including the reusable route after a coder-main repair or a later candidate/release/Firmware test-only classification; every generic M04 deterministic test/check path; and the M07 deterministic safeguard. Only after ROOT-IM accepts one frozen tip and issues a new integration card may a later doer-main invocation perform the exact M06 fast-forward/readback and declared post-join checks. It stops on a conflict, coordinate mismatch, or unexpected result and returns facts; it never classifies a loopback, accepts evidence, resolves a conflict, widens scope, performs generic product repair, or launches Firmware work. | 1; one executor per declared operation | Bounded verification/execution context | Declared verification worktree for M03; otherwise named read-only check roots or the declared clean candidate destination for an accepted fast-forward only | Declared verification worktree, isolated check roots, and accepted candidate destination | ROOT-IM's explicit proof contract for MI-ATTENTION-PRACTICAL-CORRECT or MI-VERIFICATION-ASSET-CORRECT; every generic PG-CANDIDATE/PG-RELEASE deterministic path; or a newly dispatched MI-CANDIDATE-INTEGRATE card after ROOT-IM acceptance | Every card run terminates at its own handoff to ROOT-IM. A later card may select the same mapped doer role and request available provider continuity, but it is a new invocation after ROOT-IM authorization; continuity is optional and never blocks a successor. |
| final-reviewer | Independent final review inside the accumulated release assurance campaign. | 1; one release input | Read-only accumulated review | No product writes | Separate final-review result root | MI-RELEASE-ASSURE | One release-assurance task; handoff retains the integrated candidate and first unresolved check. |
| acceptance-orchestrator | Executes disposable host-readiness/continuation proof and later owns the logical Firmware suite manager role; returns results but never issues ROOT-IM verdicts or promotes the harness. A manager/provider invocation is replaceable and cannot define sprint identity. | 1 authoritative logical manager; invocation replacement allowed | Bounded external-operation context | No generic-harness, promotion-destination, or firmware-server edits | Disposable readiness roots, replaceable suite epochs, stable logical-sprint state, and target worktree | MI-FIRMWARE-HOST-READINESS or MI-FIRMWARE-SPRINT | One operation card at a time; a correlated handoff preserves the same logical sprint while fresh live authority replaces dead runtime identity. |
| sprint-evidence-reviewer | ROOT-only review of each terminal selected-sprint evidence packet for a possible general-harness defect. It reports criticisms to ROOT-IM only. | 1; one completed sprint packet | Read-only bounded review | No product, firmware, server, or suite-state writes | Separate ROOT-owned result root | Immediately after terminal suite handoff, before MI-FIRMWARE-DECIDE issues its verdict | One review task per selected sprint; a replacement uses a correlated handoff. |

| Resolution rule | Unknown-role behavior | Mapping-update behavior |
|---|---|---|
| For implementation and review lanes, the stable runner resolves the workflow role at dispatch. For MI-FIRMWARE-HOST-READINESS only, ROOT-IM reads the same role entry, materializes its provider/model settings into the accepted target's canonical invocation, and the accepted target launches that concrete invocation; the target does not interpret or own the role mapping. | Reject the launch and report the exact unknown role; do not substitute a provider or hand-copy remembered settings. | A mapping change affects a later dispatch only; it does not edit this plan or invalidate accepted product credit. |

## 8. Composed execution graph and critical path

| Edge ID | From/output | To/input | Condition | Serial/parallel | Join ID | Failure branch |
|---|---|---|---|---|---|---|
| EDGE-001 | Frozen accepted generic candidate plus ROOT-IM retention directive | MI-CAMPAIGN-RETIRE implementation input | User explicitly resumes; candidate is clean and retained; ROOT-IM has read every isolated-package responsibility and issued the complete retain/minimally-rehome/wire/unwind/delete directive. Each behavior has a generic firmware-access usefulness decision; every legitimate behavior has an existing-consumer or firmware-compatibility-wiring route plus a focused oracle; and every rejected campaign/extraneous behavior has an unwind/delete route even when something currently consumes it. | Serial | N/A | Candidate mismatch blocks admission; an undecidable semantic item remains with ROOT-IM and prevents writer allocation rather than being delegated as an architectural guess. |
| EDGE-002 | MI-CAMPAIGN-RETIRE terminal retirement handoff accepted for checking by ROOT-IM | MI-CANDIDATE-EVIDENCE frozen candidate input | Retirement writer publishes one scoped tip and implementation trace, terminates, and returns HANDOFF-RETIRE to ROOT-IM; ROOT-IM inspects it against the retention directive and separately dispatches the doer-main evidence card. | Serial | JOIN-CANDIDATE | Writer self-check failure remains in MI-CAMPAIGN-RETIRE; a contradiction with the directive returns to ROOT-IM before another card. |
| EDGE-003 | MI-HARNESS-REPAIR or MI-SAFEGUARD-CHECKPOINT-CORRECT terminal repair handoff accepted for checking by ROOT-IM | MI-CANDIDATE-EVIDENCE frozen candidate input | EDGE-007L, EDGE-007E, EDGE-009P, MI-CANDIDATE-DECIDE on a repair repeat, MI-RELEASE-DECIDE, or MI-FIRMWARE-DECIDE admits a verified harness material defect; coder-main has terminated; ROOT-IM has inspected the repair handoff, preserved or revised the exact proof contract, established that existing trusted verification assets are sufficient and need no edit, and separately dispatched the doer-main evidence card. | Serial | JOIN-CANDIDATE | Repair failure remains within its originating M02 task; a contradiction, changed objective, or required verification-asset edit returns to ROOT-IM and takes EDGE-003V before checking. |
| EDGE-003V | MI-HARNESS-REPAIR terminal repair handoff plus ROOT-IM's exact verification-asset proof contract | MI-VERIFICATION-ASSET-CORRECT verification input | coder-main has terminated at HANDOFF-REPAIR; ROOT-IM has diagnosed the frozen repair, established that existing trusted assets cannot prove the named behavior without an edit, classified the asset change as verification-only, and named exact behaviors/goals, protected surfaces, allowed paths, mandatory checks, and acceptance criteria before dispatching doer-main. | Serial | N/A | Any product/API need, ambiguous expected behavior, or scope contradiction returns to ROOT-IM; existing sufficient assets take EDGE-003 instead. |
| EDGE-003F | MI-RELEASE-FORMAT-CORRECT terminal mechanical handoff accepted for checking by ROOT-IM | MI-CANDIDATE-EVIDENCE frozen candidate input | The writer losslessly normalized only the named Windows-1252 guide to UTF-8, ran the exact existing Ruff formatter over the declared repository scope, published a clean descendant of `3a73a7b`, supplied its terminal self-check, and stopped; ROOT-IM separately dispatches the doer-main deterministic evidence card. | Serial | JOIN-CANDIDATE | Normalization, formatter launch, or self-check failure remains within MI-RELEASE-FORMAT-CORRECT; any content or configuration contradiction returns to ROOT-IM before another card. |
| EDGE-003T | MI-ATTENTION-PRACTICAL-CORRECT terminal verification-asset handoff accepted for checking by ROOT-IM | MI-CANDIDATE-EVIDENCE frozen candidate input | doer-main publishes a clean descendant of the repaired canonical coordinate changing only the retained attention practical, retention unit, and guide, proves current host-only wake/quiet behavior and the accepted removed-policy oracle, terminates, and returns HANDOFF-ATTENTION-ASSET to ROOT-IM; ROOT-IM separately dispatches the M04 doer-main evidence card and reviewer. | Serial | JOIN-CANDIDATE | Asset self-check failure remains within MI-ATTENTION-PRACTICAL-CORRECT; any product/API change or semantic ambiguity returns to ROOT-IM before another card. |
| EDGE-003G | MI-VERIFICATION-ASSET-CORRECT terminal verification-asset handoff accepted for checking by ROOT-IM | MI-CANDIDATE-EVIDENCE frozen candidate input | doer-main has changed only ROOT-IM-authorized verification paths, run the card's self-checks, published HANDOFF-VERIFICATION-ASSET, and terminated; ROOT-IM has inspected the frozen tip and separately dispatched the M04 doer-main evidence card plus the one applicable reviewer path. | Serial | JOIN-CANDIDATE | Asset self-check failure remains in the same M03 logical task only after ROOT-IM classification; any product need, changed objective, or ambiguous oracle returns to ROOT-IM before another card. |
| EDGE-004 | MI-CANDIDATE-EVIDENCE complete findings | MI-CANDIDATE-DECIDE result input | Every selected evidence path reaches a terminal result and publishes HANDOFF-CANDIDATE-EVIDENCE; no evidence executor may dispatch a successor. | Serial | JOIN-CANDIDATE | Support faults still reach classification with decisive product facts preserved. |
| EDGE-005 | MI-CANDIDATE-DECIDE ACCEPTED candidate verdict and explicit ROOT-IM integration authorization | MI-CANDIDATE-INTEGRATE accepted source input | ROOT-IM has reviewed the terminal evidence pool, decided the active requirement, and issued a new exact integration card naming the accepted tip, destination, rollback base, and post-join checks. | Serial | N/A | Material findings take EDGE-006A, EDGE-006B, EDGE-006F, EDGE-006T, or EDGE-006V according to the originating task; without ROOT-IM's new authorization, no integration launch occurs. |
| EDGE-006A | MI-CANDIDATE-DECIDE admitted retirement material pool | MI-CAMPAIGN-RETIRE complete finding input | The unaccepted retirement task produced the tip and a required retirement criterion failed or is undecidable. | Repair return | N/A | Return the complete pool to the same retirement logical task; test-only and administrative issues use their classified non-material route. |
| EDGE-006B | MI-CANDIDATE-DECIDE admitted repair material pool | MI-HARNESS-REPAIR complete finding input | The reviewed input came from MI-HARNESS-REPAIR and its required affected criterion remains failed or undecidable. | Repair return | N/A | Return the complete pool to the same repair logical task; unrelated retirement, format, and other repair credit remains preserved. |
| EDGE-006E | MI-CANDIDATE-DECIDE admitted checkpoint-safeguard material pool | MI-SAFEGUARD-CHECKPOINT-CORRECT complete finding input | The reviewed input came from MI-SAFEGUARD-CHECKPOINT-CORRECT and its required executor/registry criterion remains failed or undecidable. | Repair return | N/A | Return the complete pool to the same checkpoint-correction logical task; unrelated integrated product and release credit remains preserved. |
| EDGE-006F | MI-CANDIDATE-DECIDE rejected release-format result | MI-RELEASE-FORMAT-CORRECT complete finding input | The exact reproduced normalization/formatter tree, UTF-8 scan, format check, no-new-lint comparison, compile, or whitespace check disproves REQ-A02 without establishing a different product defect. | Repair return | N/A | Return the complete source-conformance pool to the same task; a genuine separate product defect is classified through MI-HARNESS-REPAIR only after a plan-level ROOT-IM decision. |
| EDGE-006T | MI-CANDIDATE-DECIDE rejected strict test-only result | MI-ATTENTION-PRACTICAL-CORRECT complete finding input | The corrected practical, retention unit, or guide weakens the current adapter wake/quiet contract, still references removed policy or diagnostic-watch manager-wake behavior, fails its exact affected checks, or exceeds the declared three-file verification scope without establishing a product defect. | Repair return | N/A | Return the complete verification-asset pool to the same M03 logical task; a failed correction returns to classification and never becomes product repair without independent product evidence. |
| EDGE-006V | MI-CANDIDATE-DECIDE rejected reusable verification-asset result or newly classified generic strict test-only pool | MI-VERIFICATION-ASSET-CORRECT complete finding input | The active M03 proof contract remains valid, no product defect is established, and the required verification asset or its proof is still failed or undecidable. ROOT-IM names the complete strict test-only pool and issues a new doer-main card. | Repair return | N/A | Return only the active asset pool to the same M03 logical task; any product need takes a separately admitted M02 route after ROOT-IM classification. |
| EDGE-007 | MI-CANDIDATE-INTEGRATE terminal integration handoff accepted by ROOT-IM | MI-RELEASE-ASSURE release input | doer-main has terminated after exact fast-forward/readback/post-join facts, ROOT-IM has classified the integration operation, the checkpoint-safeguard correction is accepted/integrated, and no other admitted pre-assurance repair requirement remains open; ROOT-IM separately dispatches the assurance paths. | Serial | JOIN-RELEASE | Exact integration operation stays visible and holds only assurance input. |
| EDGE-007E | Accepted integrated `stable_io.py` repair plus the admitted fail-fast safeguard defect | MI-SAFEGUARD-CHECKPOINT-CORRECT checkpoint-correction input | The canonical environment-only post-join support condition is classified under P09 without inventing a product regression; the accepted `fd2761d` product credit is preserved; ROOT-IM confirms that the current candidate safeguard stops at an ordinary failed unit and starts selected units from the top on a later invocation; and ROOT-IM issues the exact executor/registry repair contract. | Serial | N/A | A missing environment fact remains P09 support. A contradiction in the existing registry/check semantics returns to ROOT-IM; no final assurance launches under the old monolithic behavior. |
| EDGE-007F | Integrated canonical candidate plus proven release-format failure | MI-RELEASE-FORMAT-CORRECT formatting input | Canonical is clean at `3a73a7b`; its rollback base remains available; the first formatter attempt is terminal, clean, and claim-free; ROOT has proven the exact one-file lossless normalization; and this validated amendment is active. | Serial | N/A | A source, encoding, configuration, or coordinate mismatch blocks continuation; no accepted semantic work is reopened. |
| EDGE-007L | Integrated accepted format coordinate plus ROOT-IM's admitted release-lint contract finding | MI-HARNESS-REPAIR complete finding input | REQ-A02 is accepted/integrated; full Ruff 0.16.1 defaults yield 409 findings versus 420 on the untouched parent; explicit `E9,F63,F7,F82` passes; and the candidate registry still leaves rule selection implicit. | Serial | N/A | Repair only the existing release-check command and its focused tests; no formatter/configuration change, mass lint cleanup, or release-assurance launch occurs first. |
| EDGE-007T | MI-CANDIDATE-INTEGRATE terminal handoff for the accepted packaged-asset manifest repair | MI-ATTENTION-PRACTICAL-CORRECT repaired verification input | The exact one-field manifest correction is accepted and integrated; package/install and S4 wake/idle oracles pass at the new clean canonical coordinate; the preserved M03 three-file diff and proof contract remain applicable; and ROOT-IM issues a fresh doer-main card rooted at that coordinate. | Serial | N/A | A package/install regression returns to ROOT-IM's M02 classification; a stale or non-applicable preserved diff returns to ROOT-IM before M03 mutation. No final assurance runs before M03 completes. |
| EDGE-008 | MI-RELEASE-ASSURE final result pool | MI-RELEASE-DECIDE release verdict input | All selected final paths terminate on the same integrated candidate. | Serial | JOIN-RELEASE | Support fault reaches classification. |
| EDGE-009 | MI-RELEASE-DECIDE admitted material pool | MI-HARNESS-REPAIR complete finding input | Only a failed or undecidable required generic product criterion permits continuation. | Repair return | N/A | Accepted release takes EDGE-010 when external authority is present. |
| EDGE-009T | MI-RELEASE-DECIDE admitted strict test-only pool | MI-ATTENTION-PRACTICAL-CORRECT verification input | The release safeguard's retained attention practical is the required oracle; ROOT-IM proves the product API absence is intentional, classifies only the practical, retention unit, and guide as stale, preserves all product and other safeguard credit, and this validated M03 amendment is active. | Serial | N/A | Any product/API edit, oracle weakening, or scope contradiction returns to ROOT-IM before source mutation. |
| EDGE-009P | MI-ATTENTION-PRACTICAL-CORRECT terminal dependency block classified by ROOT-IM | MI-HARNESS-REPAIR packaged-asset input | The mandatory S4 install-wake oracle fails identically on untouched `c114d3f` because the post-tool-use asset's actual SHA-256 is `d2ac4cd87cbab1c4000746a99ba142c2e55b6aa4794ffc7a7cae8b6ad659c667` while its manifest declares `1cf1592c1829fb953e927b5dd6727f946e3239be59838028ede04fe2ef335a71`; the M03 writer returned clean `BLOCKED` with no product edit and preserved its exact verified three-file diff. | Serial | N/A | If the clean-base reproduction changes or packaged asset intent is ambiguous, hold the repair for ROOT-IM classification. The M03 asset is neither accepted nor rejected by this dependency failure. |
| EDGE-009V | MI-RELEASE-DECIDE later admitted generic strict test-only pool plus exact ROOT-IM proof contract | MI-VERIFICATION-ASSET-CORRECT verification input | A required generic release oracle is missing or faulty; accepted product evidence independently fixes its expected behavior; ROOT-IM names the exact behavior/goals, protected surfaces, allowed paths, mandatory checks, and no-product-edit boundary before dispatch. | Serial | N/A | A product/API need takes EDGE-009 to MI-HARNESS-REPAIR; a support-only fact follows P09. |
| EDGE-010 | MI-RELEASE-DECIDE accepted generic release verdict | MI-FIRMWARE-HOST-READINESS readiness input | A clean package-local target and disposable roots are prepared; ROOT-IM can resolve `acceptance-orchestrator` from SRC-009; and source/contract inspection establishes that server startup, MCP initialization, and `tools/list` do not enter hardware discovery/open/claim paths. The Firmware-specific adapter is not an input. | Serial | N/A | A missing mapped route, unprepared target, or unproven side-effect-free MCP path holds only host readiness and the later sprint. |
| EDGE-010R | Accepted current M08 result, suites 003-008 evidence, bound `dd673cb...` base, and ROOT-IM's exact continuation repair contract | MI-HARNESS-REPAIR product input | M07/M08 credit is retained; all prior live processes are absent; ROOT-IM has reconciled the exact accepted base, identifies the claim/resume/lane seams, names the four-case no-hardware proof and protected hardware boundary, and separately dispatches coder-main. | Serial | N/A | This edge is ready for repair dispatch. Any newly observed coordinate ambiguity or live prior authority holds only repair allocation; it does not authorize a manager launch or a new recovery module. |
| EDGE-011 | MI-FIRMWARE-HOST-READINESS verified readiness/continuation result or an accepted harness-clean sprint below `3/3` | MI-FIRMWARE-SPRINT admission input | The focused continuation repair is integrated; `CHECK-SPRINT-CONTINUATION` and affected M08 pass; SRC-011's route smoke passes; current fixture authority exists; and every eligible logical sprint receives fresh live authority for its next action. | Serial | N/A | Missing admission holds only its consumer. A completed harness-error sprint goes to ROOT review/repair after completion; an accepted clean sprint below `3/3` admits the next indexed work without replaying green evidence. |
| EDGE-012 | MI-FIRMWARE-SPRINT completed logical-sprint handoff | MI-FIRMWARE-DECIDE practical result input | The logical sprint reached `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`, every feasible lane/unit has a terminal disposition, the complete finding pool is sealed, and cleanup/uncertainty is explicit. | Serial | JOIN-FIRMWARE | Interruption stays inside MI-FIRMWARE-SPRINT through EXC-SUITE-CONTINUATION; only explicit cancellation, withdrawn authority, or unisolatable live harm may produce `INCOMPLETE`. |
| EDGE-013 | MI-FIRMWARE-DECIDE complete post-sprint harness material pool and ROOT-IM repair contract | MI-HARNESS-REPAIR complete finding input | Only after the sprint's completed handoff and ROOT-only review, ROOT-IM classifies genuine WIP target-v2 harness defects, deduplicates the full pool, resets/no-counts that sprint, and dispatches coder-main with the responsible seams, protected behavior, and focused oracle. | Repair return | N/A | No harness repair starts mid-sprint. Suite-owned issues stay with the suite; strict generic verification-only material takes EDGE-013V. |
| EDGE-013V | MI-FIRMWARE-DECIDE admitted generic-harness strict test-only pool plus exact ROOT-IM proof contract | MI-VERIFICATION-ASSET-CORRECT verification input | The fault belongs to a required generic-harness verification asset rather than Firmware server, fixture, specification, support, or suite-owned test code; accepted product evidence independently fixes the expected behavior; ROOT-IM names exact goals, protected surfaces, allowed paths, mandatory checks, and acceptance criteria before dispatch. | Serial | N/A | A genuine generic product defect takes EDGE-013 to coder-main; every Firmware-owned asset remains with the suite. |
| EDGE-014 | MI-FIRMWARE-DECIDE harness-clean streak verdict | MI-PROMOTE accepted release inputs | Three consecutive index-ordered logical sprints are completed, accepted, and have `harness_error_observed=false`. | Serial | N/A | A completed harness-error sprint resets the streak and takes EDGE-013 only after its terminal pool; a suite-owned unresolved result does not earn credit. |
| EDGE-015 | MI-PROMOTE promotion readback | Terminal released coordinate | Destination matches the accepted coordinate and required cleanup remains visible. | Serial | N/A | Promotion mismatch holds only promotion/reuse. |

| Parallel group | Shared input | Member instance IDs | Writable-root isolation | Launch rule | Join ID | Serial exception |
|---|---|---|---|---|---|---|
| PG-CANDIDATE | One frozen retirement, admitted-repair, or corrected verification-asset tip | MI-CANDIDATE-EVIDENCE deterministic check and reviewer paths | Separate check cache and reviewer result root | On EDGE-002, EDGE-003, EDGE-003T, or EDGE-003G, launch both before awaiting either. EDGE-003F is deliberately outside this fan-out and runs one deterministic path. | JOIN-CANDIDATE | N/A |
| PG-RELEASE | One integrated release candidate | MI-RELEASE-ASSURE safeguard and final-review paths | Separate result/cache roots | Launch both before awaiting either. | JOIN-RELEASE | N/A |

| Path ID | Ordered instance/edge IDs | Expected range | Overlap | Expensive operations | Why critical |
|---|---|---|---|---|---|
| PATH-RETIRE-TO-ASSURE | ROOT-IM retention directive, EDGE-001, MI-CAMPAIGN-RETIRE, EDGE-002, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE | 60-130 minutes | Candidate and release evidence paths overlap internally; ROOT-IM's initial semantic read is serial because its output defines the writer task. | One high-context ROOT-IM decision, two independent review/check joins, and one integration. | It prevents the implementation agent from inventing the retention architecture and turns the frozen candidate into the first post-retirement accepted release input. |
| PATH-SAFEGUARD-CHECKPOINT-TO-ASSURE | ROOT-IM P09 classification, EDGE-007E, MI-SAFEGUARD-CHECKPOINT-CORRECT, EDGE-003, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE | 80-140 minutes through the first cold final assurance; later repair loops omit unchanged prefix units | The checkpoint correction, its evidence, decision, and integration are serial decision boundaries; review/check paths overlap only in PG-CANDIDATE and PG-RELEASE. | One small executor/registry correction, one affected evidence join, one exact integration, and one checkpointed assurance. | It replaces repeated 20-40 minute restart-from-top safeguard prefixes with a conservative incremental gate while retaining the existing oracle and independent review. |
| PATH-FORMAT-TO-ASSURE | EDGE-007F, MI-RELEASE-FORMAT-CORRECT, EDGE-003F, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007L, MI-HARNESS-REPAIR, EDGE-003, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE | 45-100 minutes | The mechanical writer/reproduction and the later focused lint-contract writer/evidence are serial because each consumes the prior accepted coordinate; final review and safeguard overlap only after both integrations. | One formatter task, one deterministic format decision, one minimal lint-contract repair with affected review/check, two cheap fast-forward integrations, and one final assurance join. | It accepts the exact machine-generated output without importing pre-existing style debt, then fixes the separately proven unstable release command before paying for the accumulated safeguard. |
| PATH-ATTENTION-ASSET-TO-ASSURE | MI-RELEASE-DECIDE, EDGE-009T, blocked MI-ATTENTION-PRACTICAL-CORRECT, EDGE-009P, MI-HARNESS-REPAIR, EDGE-003, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007T, retried MI-ATTENTION-PRACTICAL-CORRECT, EDGE-003T, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE | 35-70 minutes from the current block | The one-field product repair is serial before its affected review/check and integration; the preserved M03 diff then applies serially before its own affected join. Review/check members overlap only inside each declared M04 group, and final review/safeguard overlap after the three-file integration. | One one-field repair, two affected joins, two fast-forward integrations, reuse of one preserved verification diff, and one accumulated assurance repeat. | The current missing release fact remains the stale practical, but its mandatory product oracle exposed one independently reproduced package declaration defect. Repairing that exact prerequisite once is cheaper and more truthful than weakening the oracle or redesigning the already verified M03 change. |
| PATH-MATERIAL-REPAIR-WITH-ASSET | Any candidate, release, or Firmware M05 material decision, originating material edge, MI-HARNESS-REPAIR, EDGE-003V, MI-VERIFICATION-ASSET-CORRECT, EDGE-003G, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE | 25-70 minutes before affected assurance | coder-main product repair, ROOT-IM diagnosis, doer-main verification-asset construction, ROOT-IM evidence dispatch, affected review/check, ROOT-IM acceptance, and separately dispatched doer-main integration are serial boundaries; review/check paths overlap only inside PG-CANDIDATE. | One admitted product repair, one necessary verification-asset edit, one affected evidence join, and one exact integration. | This is the typed Plan-wide route that prevents a future product repairâ€”including one found by Firmwareâ€”from silently making ROOT-IM write tests or jumping directly from a test-editing worker into integration. Existing trusted assets bypass M03 through EDGE-003. |
| PATH-FIRMWARE-HARNESS-REPAIR | MI-FIRMWARE-DECIDE, EDGE-013, MI-HARNESS-REPAIR, then EDGE-003 directly when trusted assets suffice or PATH-MATERIAL-REPAIR-WITH-ASSET when they do not; MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE, then re-enter host readiness/sprint only for invalidated external consumers | 45-120 minutes before any affected external retest | ROOT-IM's Firmware ownership decision, coder-main repair, ROOT-IM's explicit asset-need decision, doer-main verification/evidence, ROOT-IM acceptance, and separately dispatched doer-main integration are serial decision boundaries; independent review/check paths overlap only inside their declared evidence groups. | One admitted product repair, zero or one required verification-asset edit, one affected evidence join, one exact integration, and one affected assurance/external return. | A real Firmware-discovered harness defect uses the same general product and verification pipeline as every other module while preserving all suite-owned fault boundaries and unaffected external credit. |
| PATH-SPRINT-CONTINUATION-TO-LIVE | Accepted current M08 checkpoint, EDGE-010R, MI-HARNESS-REPAIR, EDGE-003V, MI-VERIFICATION-ASSET-CORRECT, EDGE-003G, MI-CANDIDATE-EVIDENCE, EDGE-004, MI-CANDIDATE-DECIDE, EDGE-005, MI-CANDIDATE-INTEGRATE, EDGE-007, MI-RELEASE-ASSURE, EDGE-008, MI-RELEASE-DECIDE, EDGE-010, affected MI-FIRMWARE-HOST-READINESS, EDGE-011 | 70-140 minutes | Existing writer/asset/evidence/decision/integration boundaries remain serial; existing independent review/check paths overlap. | One focused repair, one four-case verification asset/check, one existing integration/release pass, and one affected M08 no-hardware readback. | Mandatory current path; it intentionally adds no recovery module, gate, scheduler, controller, or persistent fixture. |
| PATH-EXTERNAL-TO-PROMOTION | PATH-SPRINT-CONTINUATION-TO-LIVE, MI-FIRMWARE-SPRINT, EDGE-012, MI-FIRMWARE-DECIDE, repeated EDGE-011 -> M09 -> M05 until `3/3`, EDGE-014, MI-PROMOTE | 70-140 minutes for the focused repair/proof plus three live sprints and only post-completion harness repair time | The existing repair path runs once before live work; the suite then schedules every eligible nonconflicting logical sprint/lane. Each sprint completes and seals its pool before ROOT review or harness repair. | One focused no-hardware continuation proof, three harness-clean completed sprints, and promotion. | Directly prevents the failure-handoff pattern while retaining the smallest existing topology. |

| Gate/loop ID | Gate class | Shared input | Decided behavioral outcome | Checking module instances | Shared failure family/invariants | Blocking scope | Continuation/loop eligibility | Default-forward edge | Failure return target | Aggregation payoff | Manageability proof | Prior-result boundary | Split/merge trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GATE-CANDIDATE | PRODUCT | EDGE-002 supplies ROOT-IM's retention directive plus one frozen retirement candidate; EDGE-003 supplies one admitted ordinary or checkpoint-safeguard repair tip whose trusted assets need no edit; EDGE-003F supplies the declared format parent plus one frozen mechanical source-conformance candidate; EDGE-003T supplies the exact attention contract plus one frozen asset candidate; EDGE-003G supplies one frozen generic verification-asset candidate and its exact ROOT-IM contract, optionally layered on an admitted repair tip. | EDGE-002: did the candidate implement the directive and preserve generic compatibility? EDGE-003: did the candidate fix the admitted behavior without disturbing protected credit? EDGE-003F: does the candidate exactly equal the declared lossless normalization plus Ruff output and pass its conformance checks? EDGE-003T: does the attention practical retain wake/quiet behavior and truthful surviving documentation? EDGE-003G: do the authorized assets prove every named behavior/goal, preserve every no-change surface, stay within exact paths, and leave product semantics unchanged; when layered on repair, does that repair also satisfy its admitted invariant? | MI-CANDIDATE-EVIDENCE and MI-CANDIDATE-DECIDE | Each active edge keeps one failure family: retirement directive fidelity on EDGE-002; admitted ordinary or checkpoint-safeguard repair behavior on EDGE-003; source conformance on EDGE-003F; current attention asset fidelity on EDGE-003T; or the exact reusable asset contract plus any originating repair invariant on EDGE-003G. | The active branch blocks only its named requirement and consuming integration edge. EDGE-003G invalidates only the changed verification asset and, when applicable, the originating repair seam. | Only a failed or undecidable required product criterion permits continuation to its originating M02 task. The current attention strict test-only correction returns through EDGE-006T, and every other reusable verification-only correction returns through EDGE-006V while its no-product-edit classification remains valid. | EDGE-005 advances the accepted active candidate to integration. | EDGE-006A returns retirement material; EDGE-006B returns ordinary product-repair material; EDGE-006E returns checkpoint-safeguard material; EDGE-006F returns source conformance; EDGE-006T returns the current attention asset; EDGE-006V returns the active reusable verification asset. | One parameterized check/decision/integration lifecycle is cheaper than duplicate gates. M03 is paid only when ROOT-IM proves an asset edit is necessary. | ROOT-IM owns classification and acceptance; coder-main alone owns product source; doer-main alone owns selected verification assets and deterministic evidence. | Retain all credit outside the active branch's changed dependencies. | Split only if the correction needs a different source owner, independently useful deliverable, or broader architecture than the bounded proof contract. |
| GATE-INTEGRATION | OPERATION_BOUNDARY | Accepted candidate inputs | Can the accepted source be joined and read back at the declared candidate coordinate? | MI-CANDIDATE-INTEGRATE | Destination cleanliness, join, readback, and cleanup | Holds only integration/reuse of that coordinate and never product work or accepted credit. | No product loop; resume the exact integration operation at its first unresolved action. | EDGE-007L advances the historical integrated format coordinate to its admitted lint repair; EDGE-007T advances the current integrated manifest repair back to the preserved M03 task; EDGE-007E admits the checkpoint-safeguard correction before any next assurance; otherwise EDGE-007 advances the integrated coordinate to assurance. | Exact integration operation block or terminal-visible recovery. | One integration owner prevents conflicting joins. | The operation has one destination and one conflict owner. | Accepted source verdicts remain preserved. | Split only if a separate destination coordinate exists. |
| GATE-RELEASE | PRODUCT | One integrated candidate with an explicit release-lint contract, current verification assets, and accepted checkpoint-safeguard executor | Does the integrated candidate satisfy the required generic harness behavior? | MI-RELEASE-ASSURE and MI-RELEASE-DECIDE | Accumulated generic release behavior and public/verification surfaces | Only REQ-A01, REQ-A04, and consumers of the final generic verdict. | Only a failed or undecidable required product criterion permits material continuation to MI-HARNESS-REPAIR; the current attention fault takes EDGE-009T and any later proven generic strict test-only fault takes EDGE-009V without implying product failure. | EDGE-010 advances to host readiness when its external prerequisites are present. | EDGE-009 returns one complete pooled material set to MI-HARNESS-REPAIR; EDGE-009T returns the current attention asset; EDGE-009V returns a later exact asset contract to MI-VERIFICATION-ASSET-CORRECT. | The checkpointed safeguard continues every runnable unit, then one ROOT pool/classification batches compatible repairs before its next earliest-required incremental run. | One generic candidate, one release decision owner, and one source owner per classified change domain. | A PASS survives only while its declared inputs and prerequisites remain unchanged; failed, unresolved, affected, or uncertain units rerun from the earliest required unit. | Split only if an independently releasable product unit or a second independent verification gap emerges. |
| GATE-FIRMWARE-READINESS | OPERATION_BOUNDARY | Accepted generic release, SRC-009-resolved acceptance-orchestrator route, prepared target, side-effect-free MCP connection contract, accepted static/raw 39-name catalog comparison, and disposable host roots | Can the accepted target launch the mapped provider and complete its lane/watch/watcher/MCP-connect/handoff/cleanup path once, record target-launched MCP startup and `ListToolsRequest`, return the expected server alias/status without executing any provider tool, leave the disposable server tool-event file absent or empty, and avoid every hardware discovery or access path? | MI-FIRMWARE-HOST-READINESS | Role resolution, target launch/binding, finite observation, MCP stdio initialization/tool discovery, no-tool provider result, terminal handoff, and process cleanup | Holds only the exact readiness operation and later physical operation, never product work or accepted generic credit. | No product loop; repeat only the failed readiness action after a changed support condition. The missing Firmware-specific adapter is not a readiness failure. | EDGE-011 exposes the hardware admission boundary after readiness passes. | Terminal-visible readiness block; no source repair is inferred. | One exact connection simulation avoids debugging shared control machinery on scarce fixtures without waiting for adapter work that it does not consume. | ROOT-IM owns preparation/classification; one target-launched provider session exercises the actual control path without mixing product, Firmware-adapter, or server repair. | Generic release acceptance is preserved; M08-A1/A2 catalog credit is reused, and A3-A6 credit is invalidated only by a changed role mapping, target launch/control seam, task-local launcher, connection procedure, or MCP negotiation input. | Split only if provider launch and target/MCP connection prove to require different owners or independently resolvable change domains. |
| GATE-FIRMWARE-ADMISSION | OPERATION_BOUNDARY | Accepted host readiness/continuation proof, implemented Firmware provider route, user authority, predeclared logical sprint IDs/indices, fresh live authority, and exact target/resources | May each dependency-ready resource-compatible external action start or resume? | MI-FIRMWARE-SPRINT | Adapter, authorization, target, plan/permission/lease, continuation checkpoint, and resource availability | Holds only the exact affected operation/resource; never product work, the logical sprint, an unrelated lane, or accepted credit. | No product loop; wait/correct the exact missing fact or use EXC-SUITE-CONTINUATION without terminalizing the sprint. | EDGE-011 admits every eligible nonconflicting action in the same scheduling pass. | Exact resource/operation block. | One admission boundary protects hardware without a new recovery gate. | One logical manager owns scheduling; each sprint has stable identity across invocations. | Accepted generic/release/M08 and unaffected sprint evidence remain. | Split only by actual resource/dependency conflict. |
| GATE-FIRMWARE-RESULT | PRODUCT | One completed logical-sprint handoff, its complete finding pool, and the indexed harness-clean streak | Does the completed sprint behavior satisfy the required completion-and-finding-pool contract, and does the index-ordered sequence reach `3/3` with no harness error in the counted sprints? | MI-FIRMWARE-SPRINT and MI-FIRMWARE-DECIDE | Suite evidence/reviews, every unit disposition, cleanup/uncertainty, ROOT-only review, `harness_error_observed`, and indexed ledger | Only REQ-F01/REQ-F02 consumers. | Only a failed or undecidable required product criterion permits continuation after completion: genuine harness material takes EDGE-013, strict assets take EDGE-013V, and suite-owned findings stay external. Interruptions and ordinary defects stay inside M09 until completion. | EDGE-011 advances an accepted clean result below `3/3`; EDGE-014 advances `3/3`. | EDGE-013 or EDGE-013V only after the completed pool. | A single terminal pool avoids fail-fast diagnosis and mid-sprint repair churn. | ROOT-IM classifies only after the suite has completed; workers never dispatch repair. | Preserve all unaffected evidence and earlier accepted clean credit subject to indexed reset semantics. | Split only if the terminal pool contains independent product and verification-only owners. |
| GATE-PROMOTION | OPERATION_BOUNDARY | Accepted generic and external verdicts | Can the exact accepted coordinate be promoted and read back? | MI-PROMOTE | Destination targeting, promotion, readback, rollback, and retirement | Holds only promotion/reuse of the destination and never product work or accepted credit. | No product loop; resume exact promotion or retain terminal-visible recovery state. | EDGE-015 advances to the released-coordinate terminal action. | Exact promotion operation block. | One owner and one readback avoid promotion ambiguity. | One destination and one rollback coordinate are coherent. | All accepted source and external verdicts remain preserved. | Split only for an independently released destination. |

## 9. Global workflow policies and exceptions

### P01 Ownership and decisions

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Before any M02/M03/M04 work or when any producer, integration, assurance, readiness, or completed external sprint returns | Diagnose and define the exact problem, desired behavior, protected boundaries, proof, and next edge before dispatch. For the current suites 003-008 defect, reconcile the accepted base and issue one `EDGE-010R` contract limited to safe stale-claim recovery, runtime-invocation replacement with durable checkpoint continuity, feasible-lane continuation, and completed finding pooling. Reuse MI-HARNESS-REPAIR; after its terminal handoff, use existing checks directly only if sufficient, otherwise dispatch the existing M03 asset route, then M04/M05/M06. No worker self-dispatches. During live M09, ROOT does not review or repair harness findings until the sprint publishes its completed terminal pool. | The current worker has a complete contract or one declared successor/block exists. | Card/handoff only when consumed; no separate recovery design artifact. | Every selected M02-M09 instance and MI-PROMOTE |

### P02 Context and thread lifetime

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM and every executor | Agent, suite, or covered-command launch | Apply the existing bounded card/supervisor/role-resolution rules. Provider sessions remain lane-managed. A logical task or Firmware sprint is not a concrete invocation. Reuse the same coder-main provider session by default through every ROOT-dispatched card in its one unaccepted M02-to-M05 candidate loop, then retire it when GATE-CANDIDATE accepts or that logical task otherwise terminates. Reuse each Atlas-through-Nova named doer session across completed Firmware sprints when it remains available and its role/model mapping is unchanged. Every card still terminates at ROOT or the suite manager boundary and no idle session self-continues. When any manager/provider cannot resume, publish a correlated handoff, replace the invocation, preserve verified checkpoints and completed evidence, and resume the first affected action with fresh live authority. Invocation loss never blocks a ready edge, restarts green work, or terminalizes the logical task/sprint. Integration always uses a separately dispatched card. | Task/sprint reaches its declared semantic terminal handoff; invocation replacement is an internal continuation, while gate acceptance retires the coder-main session. | Handoff and terminal supervisor result only when consumed. | MI-CAMPAIGN-RETIRE through MI-PROMOTE |

### P03 Failure-case selection

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Before a writer, readiness run, or external sprint | Bind only realistic requirement-linked failures. The current continuation contract has exactly four no-hardware cases from `HANDOFF_SPRINT_FAILURE.md`: C1 manager/provider loss preserves the same sprint/checkpoint and uses fresh runtime authority; C2 a dead-owner retained claim is safely released/reassigned while uncertainty blocks only that resource and unrelated work continues; C3 a malformed first call, order/clarification mistake, or suite-owned doer/spec/fixture/provider fault is corrected or terminally recorded without ending the sprint; C4 a genuine harness defect lets every feasible unit finish, produces `COMPLETED_WITH_FINDINGS`, pools all harness findings, resets/no-counts, and starts no repair before completion. Every case uses fake identities and forbids MCP tool, USB/probe/serial/radio discovery/open, server plan/permission/lease, and hardware mutation. | Each case has one focused oracle, owner, and no hidden machinery. | `CHECK-SPRINT-CONTINUATION` plus the existing card/handoff. | MI-HARNESS-REPAIR, MI-VERIFICATION-ASSET-CORRECT, MI-CANDIDATE-EVIDENCE, MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-SPRINT |

### P04 Check selection and green credit

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Candidate change or result classification | Retain the existing focused/checkpointed rules and unaffected PASS credit. On EDGE-010R, `CHECK-SPRINT-CONTINUATION` is mandatory: M03 implements only the smallest missing fake-runtime asset, M04 executes all four feasible cases after ordinary failures, and the accepted integrated target repeats the affected check through M08 before EDGE-011. Generated state lives only below `tmp/plan2-no-hardware-recovery/{invocation_id}/`; permanent regression code lives only in ROOT-authorized existing test paths. During M09, an ordinary failure never cancels a later feasible lane/unit. Harness findings accumulate until the sprint completes; P04 does not authorize mid-sprint product repair. Covered commands follow P02 and never retry unchanged supervisor failures. `FAST_LANE_V2` remains available only under its existing narrow production-repair rules and is unavailable for this recovery asset/external proof. | Complete decisive facts reach M05 or the affected M08 consumer. | Existing result/checkpoint and the one joined continuation result when consumed. | Every selected M03 instance, MI-CANDIDATE-EVIDENCE, MI-RELEASE-ASSURE, MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-SPRINT |

`FAST_LANE_V2` smoke credit means the required changed-source compile and deterministic motivating test PASS results survive byte-identical integration, subject to their declared input map; no broad affected-check campaign is added for that narrow route.

### P05 Review classes and invalidation

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Candidate evidence, final assurance, or a completed suite sprint | Retain existing review classes. For EDGE-010R use `AFFECTED_REPAIR_WITH_ASSET` only if M03 was required and require the reviewer to check the four-case contract, no-hardware boundary, and absence of a second recovery mechanism. The sprint-evidence-reviewer launches only after `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`; it receives the sealed terminal packet and complete pool, reports only to ROOT-IM, and never causes a mid-sprint pause. ROOT admits a harness repair only from that completed pool and an identified harness seam. | Review credit remains until its frozen input/consumed invariant changes. | Review result supplied only to its named decision. | MI-CANDIDATE-EVIDENCE, MI-RELEASE-ASSURE, MI-FIRMWARE-SPRINT, MI-FIRMWARE-DECIDE |

### P06 Parallel checks and results

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM, doer-main, or suite manager | Independent checks consume one frozen input | ROOT-IM binds the behavior-proof contract, no-change surfaces, and mandatory plan checks; doer-main chooses and launches the smallest concrete generic test/check members that meet that contract before awaiting one, gives each a disjoint writable root, and publishes their joined facts. The suite controls its catalog-specific parallel lanes and leases. | One complete combined set reaches the decision owner. | Separate roots and one joined result when consumed. | MI-CANDIDATE-EVIDENCE, MI-RELEASE-ASSURE, MI-FIRMWARE-SPRINT |

### P07 Finding pooling and material repair

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Evidence finds possible material defect | Continue every feasible selected check/lane before classification, then deduplicate and partition the complete pool by coherent repair owner. For the current pre-live lifecycle defect, one EDGE-010R repair uses the existing coder -> ROOT -> optional M03 doer -> ROOT -> M04 -> ROOT -> separately authorized M06 route. During live Firmware work, never dispatch a harness repair from an intermediate event: the logical sprint first publishes `COMPLETED_WITH_FINDINGS`; ROOT then joins the suite pool and terminal reviewer, admits one compatible harness batch through EDGE-013, and resets/no-counts that sprint. Suite-owned findings remain with the suite. No worker repairs one comment/failure while other feasible work remains. | One completed pool has one classified route and every worker has stopped at ROOT. | Existing handoffs only. | MI-CAMPAIGN-RETIRE, MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-SPRINT, MI-FIRMWARE-DECIDE, MI-HARNESS-REPAIR, MI-VERIFICATION-ASSET-CORRECT, MI-CANDIDATE-EVIDENCE |

### P08 Test-only correction

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | A test/support failure or missing verification asset is proposed as semantic-preserving in any current or future Plan 2 module | First decide whether existing product evidence still settles the required behavior and whether the loopback is strict test-only or a real product repair. If existing evidence settles it, record the test fault under P09 and advance every nonconsumer. If the faulty or missing asset is a required oracle, select MI-ATTENTION-PRACTICAL-CORRECT for the current exact profile or MI-VERIFICATION-ASSET-CORRECT for any other Plan 2 module, only after proving its expected behavior from accepted product requirements and independent evidence. ROOT-IM must name the exact behaviors and goals to prove, every protected/no-change surface, the allowed verification-asset paths, the no-product-edit boundary, mandatory existing checks, and the acceptance owner. Every selected M03 route uses a newly dispatched terminal doer-main card; doer-main chooses and implements the minimal test/fixture/guide assets and focused commands within that contract, runs its declared self-checks, publishes the handoff, and stops. ROOT-IM then separately dispatches the M04 deterministic evidence card through EDGE-003T or EDGE-003G; after terminal review/check evidence, M05 either accepts the asset or returns the complete strict test-only pool through EDGE-006T or EDGE-006V to the same M03 logical task. Acceptance still returns to ROOT-IM, which alone may issue a later separate doer-main integration card. The current attention case instantiates this rule with one current sparse host-adapter wake, pending work preserved until acknowledgement, one empty-queue quiet result, preservation of unrelated practical checks, intentional absence of removed policy and diagnostic-watch wake APIs, truthful-guide goal, exact three-file scope, and CHECK-ATTENTION-PRACTICAL. A failed correction or rerun always returns to ROOT-IM classification; never send it to M02 without separate product evidence satisfying the product-loop rule. | The product result advances without the unneeded test, the exact criterion remains visibly indeterminate, or the selected M03 asset is accepted and integrated without changing product semantics. | Preserve unaffected accepted results; retain only the exact M03 handoff and affected evidence needed by decision, integration, or recovery. | Every selected M03 instance, MI-CANDIDATE-EVIDENCE, MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-DECIDE |

### P09 Administrative recovery

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM and Firmware suite manager | Malformed call/report, timeout, manager/provider/session exit, stale claim, suite setup/ordering/clarification fault, resource wait, or cleanup uncertainty | Correct only the affected fact. Keep the logical sprint active; preserve verified checkpoints/evidence; replace dead runtime identity with a correlated handoff and fresh live authority. After exact old-owner/process-tree and live-action absence proof, release/reassign a stale claim when safe; otherwise hold only that exact resource. Continue every unrelated feasible lane. Never classify support/admin failure as harness failure or `INCOMPLETE`. | Affected action resumes or exact resource remains visibly held while the sprint continues elsewhere. | Existing checkpoint/handoff/claim evidence only; no new recovery ledger. | MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-SPRINT, MI-FIRMWARE-DECIDE, MI-PROMOTE |

### P10 Semantic acceptance

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Shape-valid result reaches M05 or an external sprint reaches terminal publication | Decide from behavior, not shape. Generic modules retain `ACCEPTED`, `ACCEPT-WITHIN-TOLERANCE`, `CONTINUE`, or `INCOMPLETE`. A Firmware sprint must continue until `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`; a harness finding changes the latter's credit/repair route but never makes it `INCOMPLETE`. Use `INCOMPLETE` for a sprint only after explicit user cancellation, withdrawn authority, or live harm that cannot be isolated safely; ordinary uncertainty holds only its exact consumer. | Declared successor, completed finding pool, or exact user/safety terminal. | Verdict only when consumed. | MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-DECIDE |

### P11 Full-safeguard scope

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Candidate integration after retirement, admitted harness repair, or the selected format correction | Bind the exact candidate-owned safeguard input and authorize doer-main to run it from the candidate copy with `-Run`, `-RepositoryRoot`, `-ExpectedBranch`, and `-ExpectedTip` all present and bound to the integrated candidate; run one final review in parallel for that release-unit attempt. Never rely on the script's default branch. The release selector retains ownership of its existing coarse checksâ€”Ruff, format, retained-baseline BasedPyright, compile, fast/package/public checks, orchestrator and watcher units, real-agent isolation, attention retention, and synthetic cleanupâ€”but the checkpoint correction makes each selected registry entry independently runnable. Each entry declares a conservative input map: source path/domain, configuration, command/runner version and environment, fixture/temporary-state input, and any external state it consumes. Its checkpoint records only unit outcome (`PASS`, `FAIL`, `SKIP`, or `UNRESOLVED`), first unresolved unit, recorded skip reason, and the source/external attempt coordinate necessary to decide reuse. It does not hash or snapshot ordinary files. The executor continues every runnable later unit after an ordinary failure; only a declared prerequisite failure or P15 containment can skip it. On later input, it compares changed paths and declared inputs, reuses only PASS entries with unchanged inputs/prerequisites, selects the union of failed, unresolved, affected, or uncertain units, and executes that union in registry order from its earliest required member. The existing 1,800-second orchestrator estimate and 2,400-second cold-run aggregate remain history-based upper bounds; no ten-minute deadline is assigned to a twenty-minute operation. Every P02 lifetime is the selected expected total plus only `max(5, min(120, ceil(expected total * 0.25)))` cleanup, with a 30-second heartbeat. The first cold run may use 2,400/120/2,520; later incremental runs recalculate both expected total and cleanup from the selected units. Duration remains a selector cost input, not a requirement to preserve incidental order. No accumulated safeguard appears in writer cards. | M05 receives one joined final pool with every feasible unit disposition and checkpoint state. | One bounded aggregate result plus the consumed checkpoint, retained only while later release work needs it. | MI-RELEASE-ASSURE |

### P12 External authorization and rehearsal

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | After generic release and before any external catalog sprint | Preserve the accepted M08-A1/A2 source trace and exact static-registration/raw-MCP 39-name comparison while their inputs remain unchanged. Resolve `acceptance-orchestrator` from SRC-009, materialize that entry into the accepted target's canonical invocation, and prepare disposable roots. Configure the target's MCP command through one task-local launcher that changes no product/server code, records a startup marker, and captures server stderr separately from stdio protocol output. Start the owner-bound watcher before the provider can finish. Give the provider one no-tools task: use no shell, filesystem, network, or MCP tool and return only the configured server alias plus fixed `connection_ready` status. Accept only when the target-launched server marker exists, captured protocol stderr records `Processing request of type ListToolsRequest`, the alias/status handoff is exact, the provider event stream contains no tool invocation, the disposable server tool-event file is absent or empty, finite watch/watcher facts are usable, and exact target-owned process cleanup passes. This protocol trace proves target-side initialization/listing; the already accepted raw/static comparison remains the catalog oracle because Codex 0.147.0 forcibly defers custom tools from model context. Do not probe hardware to prove its absence and do not wait for SRC-011. After readiness passes, require SRC-011's implemented provider route and local smoke plus fresh user fixture confirmation and one selected catalog scenario before MI-FIRMWARE-SPRINT may invoke any MCP tool. | Connection readiness passes and the hardware admission boundary is exposed, or only the exact unavailable readiness/hardware operation remains blocked. | Readiness terminal result; later suite epoch admission record. | MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-SPRINT |

For every readiness or practical/hardware gate with more than one independently runnable unit, apply the same checkpointed rule as P04/P11. Retain a completed unit only while its declared target, firmware image, fixture, lease/resource, server behavior, and external-state inputs are verified unchanged; change to one of those inputs reruns that unit and its dependents, while an unrelated source edit does not restart the whole practical sequence. The external Firmware suite remains owner of its own unit map and checkpoint implementation; this plan consumes only its declared terminal/affected-retest results.

### P13 Gate/loop sizing, health, and topology reassessment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM | Material result, failed strict test-only correction, overrun beyond credible range, or changed external topology | Preserve work, reassess only the affected gate's failure family, and split a new unaccepted return when it needs a different owner or source context. Keep every semantic-preserving verification asset in M03 under doer-main; any production/API need returns to ROOT-IM classification and an admitted M02 coder-main task rather than widening the test task. Every different strict test-only asset requires an exact ROOT-IM proof contract and a newly dispatched terminal doer-main card through MI-VERIFICATION-ASSET-CORRECT before source mutation. A material repair requiring verification-asset edits takes EDGE-003V rather than hiding those edits in coder-main or ROOT-IM. Every resulting evidence run returns to ROOT-IM before a separately authorized integration run. No arbitrary iteration cap applies. | Existing graph remains adequate or a plan amendment is issued. | Decision note only when a later consumer needs it. | Every selected M03 instance, MI-CANDIDATE-DECIDE, MI-RELEASE-DECIDE, MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-DECIDE |

### P14 Exception classes

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM and Firmware suite manager | A logical sprint is interrupted before its completed terminal handoff | Use EXC-SUITE-CONTINUATION. Preserve semantic progress, replace dead runtime authority, isolate only exact uncertainty/harm, and continue the same sprint. No new graph or recovery controller is created. | The same sprint resumes or completes with a full finding pool. | Existing suite checkpoint/handoff and claim evidence. | MI-FIRMWARE-SPRINT |

| Exception ID | Affected policy | Exact trigger | Decision owner | Allowed alternate action | Required confirmation | Preserved results | Invalidated results | Scope | Expiry |
|---|---|---|---|---|---|---|---|---|---|
| EXC-SUITE-CONTINUATION | P02, P09, P10, P12 | Before a logical sprint's completed handoff, its manager/provider exits, a call/order/spec/fixture/doer/support fault interrupts one unit, a stale claim blocks it, or a harness defect is observed. | ROOT-IM with suite-manager evidence | Keep the same logical sprint ID/index; preserve verified checkpoints/evidence/findings; replace runtime identities; issue fresh authority for new live actions; safely release/reassign proven dead-owner claims; hold uncertain exact resources; continue every feasible lane. Record harness defects but do not repair them until the sprint completes. | Exact old owner/process tree and live action are absent or contained; adopted checkpoint is read back; every new live action has a fresh plan, permission, lease, and verified target. | Sealed spec, verified source/firmware checkpoints, completed units, accumulated findings, unrelated lanes, generic/M07/M08 credit, and earlier ledger credit subject to later harness-error reset. | Only interrupted/unsafe/changed-input units and current runtime identities. | One logical sprint across any number of replacement invocations/epochs. | `COMPLETED_CLEAN`, `COMPLETED_WITH_FINDINGS`, explicit user cancellation/authority withdrawal, or unisolatable live harm. |

### P15 Stop and live-harm containment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT-IM and suite manager | Observed unauthorized or wrong-resource action, unexpected hardware/USB visibility during host readiness, loss of process/resource containment, or irreversible loss of needed judgment information | Stop only identified descendants or resources, preserve diagnostic state, verify containment, then classify under P09/P10. | Exact live hazard is contained and affected operation is terminal-visible. | Required readiness, suite, or supervisor terminal result. | MI-FIRMWARE-HOST-READINESS, MI-FIRMWARE-SPRINT, MI-PROMOTE |

## 10. Lane, resource, result, and handoff manifest

| Lane ID | Module instance | Role | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| LANE-RETIRE | MI-CAMPAIGN-RETIRE | coder-main | EDGE-001 after ROOT-IM directive completion | Identified candidate worktree | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE | Scoped retirement tip, complete implementation trace, and terminal HANDOFF-RETIRE published; coder-main has stopped | Writer self-check route or ROOT-IM semantic clarification; no direct checking/integration launch |
| LANE-REPAIR | MI-HARNESS-REPAIR | coder-main | EDGE-007L, EDGE-009P, EDGE-006B, EDGE-009, or EDGE-013 after ROOT-IM's repair contract | Identified repair worktree | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE through EDGE-003 when trusted assets suffice or MI-VERIFICATION-ASSET-CORRECT through EDGE-003V when they do not | One pooled harness repair tip and terminal HANDOFF-REPAIR published; coder-main has stopped | Same logical task stalls, fails, or returns to ROOT-IM classification; no direct test or integration launch |
| LANE-SAFEGUARD-CHECKPOINT | MI-SAFEGUARD-CHECKPOINT-CORRECT | coder-main | EDGE-007E after ROOT-IM's exact executor/registry contract | Identified candidate repair worktree | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE through EDGE-003 | One checkpoint-safeguard repair tip and terminal HANDOFF-REPAIR published; coder-main has stopped | Same logical task returns only to ROOT-IM; no assurance, test, or integration self-launch |
| LANE-RELEASE-FORMAT | MI-RELEASE-FORMAT-CORRECT | coder-main | EDGE-007F | Isolated format worktree rooted exactly at `3a73a7b` | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE | One clean descendant produced only by the exact named-file normalization and Ruff formatter plus terminal HANDOFF-RELEASE-FORMAT; coder-main has stopped | Same format task receives EDGE-006F only through ROOT-IM; encoding, configuration, parent, or content contradiction returns to ROOT-IM. |
| LANE-ATTENTION-ASSET | MI-ATTENTION-PRACTICAL-CORRECT | doer-main | EDGE-009T for initial entry or EDGE-007T for the repaired retry, after ROOT-IM's strict test-only proof contract | Identified verification worktree rooted at the canonical coordinate carried by the active edge | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE | One clean three-file verification-asset descendant plus terminal self-check and HANDOFF-ATTENTION-ASSET; doer-main has stopped | Same M03 task receives EDGE-006T only through ROOT-IM; a product/API need or semantic ambiguity returns to ROOT-IM. |
| LANE-VERIFICATION-ASSET | MI-VERIFICATION-ASSET-CORRECT | doer-main | EDGE-003V, EDGE-006V, EDGE-009V, or EDGE-013V after ROOT-IM's exact proof contract | Identified verification worktree rooted at the frozen product or repair tip named by ROOT-IM; writes limited to exact authorized verification paths | ROOT-IM, then separately dispatched MI-CANDIDATE-EVIDENCE through EDGE-003G | One clean verification-asset tip, declared self-checks, and terminal HANDOFF-VERIFICATION-ASSET; doer-main has stopped | Same M03 task receives EDGE-006V only through ROOT-IM; any product need or semantic ambiguity returns to ROOT-IM. |
| LANE-CANDIDATE-REVIEW | MI-CANDIDATE-EVIDENCE | reviewer-main | EDGE-002, EDGE-003, EDGE-003T, or EDGE-003G | Separate review result root | MI-CANDIDATE-DECIDE | Complete review result over declared frozen tip and active branch contract | P09 then MI-CANDIDATE-DECIDE |
| LANE-CANDIDATE-CHECK | MI-CANDIDATE-EVIDENCE | doer-main | EDGE-002, EDGE-003, EDGE-003F, EDGE-003T, or EDGE-003G | Separate deterministic-check result/cache root; EDGE-003F also owns its disposable reproduction root | MI-CANDIDATE-DECIDE | Declared branch-local checks finish and publish terminal facts over the frozen tip | P09 then MI-CANDIDATE-DECIDE; a material fact is classified only by ROOT-IM. |
| LANE-CANDIDATE-INTEGRATE | MI-CANDIDATE-INTEGRATE | doer-main | EDGE-005 after ROOT-IM authorizes one accepted tip | Declared clean candidate destination and separate post-join result roots | ROOT-IM, then MI-RELEASE-ASSURE or the declared admitted-repair edge | Exact fast-forward/readback and declared post-join facts plus terminal HANDOFF-CANDIDATE-INTEGRATE are published without a conflict or source edit; doer-main has stopped | GATE-INTEGRATION operation recovery; ROOT-IM classifies any conflict or product fact before a successor. |
| LANE-FINAL-REVIEW | MI-RELEASE-ASSURE | final-reviewer | EDGE-007 | Separate final-review result root | MI-RELEASE-DECIDE | Complete final review over integrated release input | P09 then MI-RELEASE-DECIDE |
| LANE-RELEASE-SAFEGUARD | MI-RELEASE-ASSURE | doer-main | PG-RELEASE after ROOT-IM binds the integrated release input and current checkpoint | Separate bounded safeguard result/checkpoint root | MI-RELEASE-DECIDE | One exact candidate-owned checkpointed safeguard result over the bound integrated coordinate, with every feasible selected unit disposition and first unresolved state | P09 then MI-RELEASE-DECIDE; ROOT-IM alone classifies any product implication. |
| LANE-FIRMWARE-HOST-READINESS | MI-FIRMWARE-HOST-READINESS | acceptance-orchestrator | EDGE-010 | Disposable Firmware readiness epoch, MCP state/artifact roots, and package-local target | GATE-FIRMWARE-READINESS and later MI-FIRMWARE-SPRINT | Readiness terminal result proves provider/lane/watch/watcher/MCP/handoff/cleanup without physical access | P09/P15 or terminal-visible readiness block |
| LANE-FIRMWARE-SPRINT | MI-FIRMWARE-SPRINT | acceptance-orchestrator | EDGE-011 or EXC-SUITE-CONTINUATION | `Firmware/` suite state with stable logical-sprint roots and replaceable epoch/provider roots | MI-FIRMWARE-DECIDE only after sprint completion | `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`, complete feasible-unit/finding pool, observer result, and explicit cleanup/uncertainty | Continue same sprint under P09/EXC-SUITE-CONTINUATION; P15 contains only exact live harm |
| LANE-PROMOTE | MI-PROMOTE | ROOT-IM | EDGE-014 | Promotion destination | Released-coordinate terminal action | Readback confirms declared accepted coordinate | Exact operation boundary recovery |

| Claim/lock ID | Resource | Owner | Activation | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| N/A | No plan-owned cross-process lock | N/A | N/A | N/A | N/A | The Firmware suite owns its actual resource leases, and promotion is serial under one declared owner. | A suite lease or promotion conflict is handled by its exact owner without a duplicate plan lock. |

| Check | Proves | Dependencies | Result owner | Reuse condition | Rerun route | Result path if needed | Failure route |
|---|---|---|---|---|---|---|---|
| CHECK-RETIRE-MAP | ROOT-IM has classified every `firmware_acceptance/` source responsibility first by usefulness to a generic firmware-access harness and then by consumer route. A qualifying responsibility accepts caller-declared worktree, provider/server, resource, and policy inputs; performs reusable process lifecycle, MCP observation/connection, lease/resource, authorization, handoff/cleanup, or schema-less invocation work; and neither preserves a fixed campaign/fixture/evidence graph nor duplicates an existing owner. MCP/process, lease, and hardware-access behavior may qualify even when related to the external Firmware MCP server; server relationship alone does not decide the classification. Each legitimate behavior is retained/minimally rehomed for an existing consumer or explicitly wired into the smallest existing firmware compatibility seam when no consumer exists, with one focused oracle. Retired campaign control/evidence/topology, duplicate machinery, dormant code, and other extraneous behavior are removed, and any current dependency on them has an explicit unwind route. The known one-way core boundary remains true, and every obsolete campaign-only test, documentation, and release-check attachment is included in cleanup. | Frozen candidate, package configuration, isolated package source, generic capability contract, current Firmware suite/MCP seams, tests, release registry, and public docs | ROOT-IM | Reuse until one of those exact surfaces changes. | ROOT-IM rechecks only the changed legitimacy decision, consumer/wiring route, or attachment before writer continuation. | The bounded coder task card and reviewer input; no separate permanent artifact. | Hold writer allocation or return the exact semantic question to ROOT-IM. |
| CHECK-CANDIDATE-AFFECTED | The candidate faithfully implements ROOT-IM's retention directive, every retained/rehomed or newly wired generic firmware-access behavior works, every directed dependency on campaign/extraneous behavior is unwound, obsolete campaign attachments are gone, and generic lifecycle, package/docs, and schema-less firmware compatibility survive the candidate change. | Candidate tip, ROOT-IM retention directive, implementation trace, exact changed paths/domains, focused oracle for every retained/rehomed/wired behavior, unwind-seam checks, and mapped affected tests | doer-main deterministic check executor | Reuse until candidate input, directive, selector registry, consumer/wiring route, focused oracle, or check semantics change. | Select and execute the smallest retained-component, new-consumer-integration, and unwind-seam focused commands that prove ROOT-IM's named behaviors and protected surfaces. Then run the candidate release selector with `--intent affected`, exact changed paths, and `legacy-compat`, `docs`, and `package` domains; execute every selected command, then run `orchestrator_harness.tests.test_firmware_route_compatibility` and `orchestrator_harness.tests.test_firmware_lifecycle_compatibility` explicitly. Each covered command uses P02; its expected bound is the command/selector estimate plus measured headroom and policy-capped cleanup. | Unique bounded terminal result path per command; one joined check result for the decision. | MI-CANDIDATE-DECIDE |
| CHECK-CANDIDATE-REPAIR | One admitted harness repair fixes its named required behavior in the existing seam without regressing the previously violated invariant or any release-selector consumer of the changed paths/domains. | Repair tip, admitted finding/reproducer, changed paths/domains, focused repair oracle, previously violated review invariant, and preserved credit | doer-main deterministic check executor | Reuse only for the same repair tip, admitted finding, and unchanged affected-check semantics. | Run the focused repair oracle, the candidate selector with `--intent affected` and exact changed paths/domains, and only the previously violated review invariant. Each covered command uses P02. | Unique bounded terminal result path per command; one joined repair-check result for the decision. | MI-CANDIDATE-DECIDE |
| CHECK-RELEASE-FORMAT | The candidate is exactly the output of the declared lossless encoding normalization followed by the existing Ruff formatter, remains valid source, and adds no lint finding to the pre-existing parent debt. | Declared clean parent, frozen source-conformance tip, authoritative Ruff/configuration, named guide, and a disposable reproduction root | doer-main deterministic check executor | Reuse only for the same parent, tip, source bytes, Ruff version, configuration, and release scope. | From a fresh disposable copy of the parent, prove the named file fails strict UTF-8, round-trips as Windows-1252, and contains only the observed `0x97` non-ASCII byte; decode Windows-1252 and encode UTF-8 without changing text or line endings, run the same formatter, and compare the resulting tree exactly with the frozen tip. Then prove all tracked files are strict UTF-8; run `ruff format --check .`; compare Ruff JSON findings for parent and tip as multisets of repository-relative path, rule code, and message so line shifts cannot fabricate a regression; require no tip-only finding; run the existing release compilation command and `git diff --check`. Every covered command uses P02 with measured bounds. | Unique bounded terminal result path per command plus one joined format result. | MI-CANDIDATE-DECIDE through EDGE-006F on a source-conformance failure; a separate pre-existing release-contract defect requires ROOT-IM plan-level classification and never expands this task. |
| CHECK-ATTENTION-PRACTICAL | The practical proves current host delivery: one actionable queue revision produces one sparse notice and a delivered synthetic Codex boundary receipt without acknowledging the pending event; a fresh empty queue produces no notice and no transport call; unrelated attention-analysis checks and the terminal PASS marker remain. The accepted product still exposes no removed attention-policy or diagnostic-watch manager-wake API, and the guide describes only current behavior. | Frozen EDGE-003T tip, updated `test_attention_practical_retention`, exact current product oracles `test_S4_CODEX_INSTALL_WAKE_001` and `test_S4_CODEX_IDLE_FINALIZE_001`, existing `test_FC5_removed_policy_has_no_live_output_surface`, exact three-file diff, and stale-name/obsolete-claim scan limited to those assets | doer-main deterministic check executor | Reuse only for the same asset tip, unchanged current product and removed-policy oracles, and unchanged three-file scope. | Run the retained attention-practical unit with expected upper bound 45 seconds, cleanup 11 seconds, lifetime 56 seconds, and heartbeat 15 seconds; run the two exact current product wake oracles together with 45/11/56/15 seconds; run the exact removed-policy oracle with 30/7/37/15 seconds; compile the practical and retention unit together with 10/5/15/5 seconds; give each covered command a unique P02 result path. Then use literal read-only searches to prove the five removed helper names and the two removed manager CLI flags are absent from all three assets, prove the guide no longer promises retired `wake_id`, `wake_transport`, or `MANAGER_WAKE_*` output from diagnostic watch, and run `git diff --check`. | Unique bounded terminal result path per covered command plus one joined asset result. | MI-CANDIDATE-DECIDE through EDGE-006T; a product/API contradiction returns to ROOT-IM classification. |
| CHECK-VERIFICATION-ASSET | The active reusable M03 tip proves every ROOT-IM-named behavior and test goal, preserves every named no-change surface, changes only exact authorized verification paths, and does not alter product semantics; when layered on a product repair, the original repair invariant remains proved. | Frozen EDGE-003G tip, ROOT-IM proof contract, accepted requirements/independent product evidence, exact verification-asset diff, mandatory existing checks, protected surfaces, and originating repair handoff when applicable | doer-main deterministic check executor | Reuse only for the same tip, proof contract, allowed paths, mandatory checks, product evidence, and originating repair invariant. | Independently rerun the smallest commands that prove every named target plus all mandatory existing checks; inspect exact path scope and `git diff --check`; when EDGE-003V supplied the input, also run CHECK-CANDIDATE-REPAIR. Every covered command uses P02 with a bound derived from its declared history or plan limit and a unique result path. | Unique bounded terminal result per covered command plus one joined reusable-asset result. | MI-CANDIDATE-DECIDE through EDGE-006V for a strict asset failure; a product contradiction returns to ROOT-IM and the originating M02 classification. |
| CHECK-RELEASE-ASSURANCE | Integrated generic harness release unit satisfies accumulated requirements without repeating unaffected proof. | Integrated candidate, final review, candidate-owned release registry/safeguard, prior checkpoint, changed paths/domains, and declared per-unit input map | final-reviewer and doer-main deterministic check executor | Reuse a unit PASS only when its declared inputs and prerequisites are unchanged; unknown state is not reusable. | Execute every failed, unresolved, changed-input-affected, or uncertain unit in declared registry order from the earliest required member. Continue later independent feasible units after ordinary failure; record a skip only for a named failed prerequisite or P15 containment. | Separate final-review result plus one bounded candidate-owned safeguard result/checkpoint with explicit integrated root, observed branch, accepted tip, selected-unit expected total, policy-capped cleanup, and unit dispositions. | MI-RELEASE-DECIDE |
| CHECK-FIRMWARE-HOST-READINESS | SRC-009 resolves `acceptance-orchestrator`; ROOT-IM materializes that role into the accepted target invocation; the target launches it; and the target/watch/watcher/MCP connection path records target-side initialization/listing, returns the expected server alias/status, hands off, and cleans up without executing a provider tool or entering hardware discovery/access. | Accepted generic release; accepted source trace and static/raw 39-name catalog comparison; mapped role; package-local target; disposable MCP inputs with no hardware identifier/lease/permission/endpoint; task-local launcher startup marker and captured `ListToolsRequest` stderr; provider event stream; disposable server tool-event file; and target process boundary | acceptance-orchestrator | Reuse the accepted result only while the role mapping, target launch/control seams, task-local launcher behavior, connection procedure, server registration/listing code, and MCP negotiation inputs are unchanged. | No rerun is pending. After a changed support input, repeat only the earliest failed/affected readiness action; never rerun generic assurance merely for a readiness operation. | Disposable readiness terminal result, launcher/protocol trace, provider event stream/final response, absent-or-empty server tool-event file result, target status/event facts, and verified process-tree cleanup. | GATE-FIRMWARE-READINESS |
| CHECK-SPRINT-CONTINUATION | The exact behavior that failed across suites 004-008: C1 manager/provider loss preserves the same logical sprint and verified checkpoint while fresh runtime identities resume the affected unit; C2 complete absence proof permits safe stale-claim release/reassignment while uncertainty holds only that resource and unrelated work continues; C3 malformed-call, ordering/clarification, and suite-owned doer/spec/fixture/provider faults are corrected or terminally recorded without sprint failure/cold restart; C4 a genuine harness defect lets every feasible unit finish, emits `COMPLETED_WITH_FINDINGS`, seals the complete harness pool, resets/no-counts, and starts no repair before completion. All cases prove exact cleanup with zero MCP tool, server plan/permission/lease, USB/probe/serial/radio discovery/open, or hardware mutation. | Reconciled accepted target; `HANDOFF_SPRINT_FAILURE.md`; ROOT's four-case contract; frozen repair/asset tip; fake process/session/claim/checkpoint inputs; forbidden-event sentinels; unique generated root `tmp/plan2-no-hardware-recovery/{invocation_id}/` | doer-main for deterministic pre-integration evidence; acceptance-orchestrator for affected exact-target M08 repetition | Reuse only for unchanged product/verification tip, four-case contract, fake fixture, runner, and forbidden-event boundary. | M03 implements/corrects only missing verification assets; M04 executes all four feasible cases after ordinary failure; after M06/M07, affected M08 repeats the check on the exact integrated target. Rerun only failed/unresolved/changed/uncertain cases. | Permanent assets only in ROOT-authorized existing verification paths; every runtime result/sentinel below the unique generated tmp root, deleted or visibly retained after classification | Product behavior returns as one complete pool to MI-HARNESS-REPAIR; strict asset-only failure returns to M03; support uses P09; any forbidden event uses P15 and blocks live admission. |
| CHECK-FIRMWARE-SUITE | Selected catalog scenario produces its declared real acceptance facts. | Fresh user authority, suite epoch, target worktree, and selected case | Firmware suite manager | Reuse only under the suite's own unchanged selected-case rules. | Suite affected retest route. | Suite-owned epoch evidence. | MI-FIRMWARE-DECIDE |

| Result/handoff ID | Producer | Consumer | Path if durable | Correlation needed | Publication rule | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| HANDOFF-RETIRE-DIRECTIVE | ROOT-IM | LANE-RETIRE and MI-CANDIDATE-EVIDENCE | The bounded coder task card/reviewer input | ROOT process, coder invocation, candidate worktree, and logical task IDs | Publish the complete responsibility-level retain/minimally-rehome/wire/unwind/delete directive. For each item, record whether it accepts caller-declared variable inputs, which reusable firmware-access responsibility it owns, and why that responsibility is not already owned elsewhere; do not reject MCP/process, lease, or hardware-access behavior merely because it resembles or relates to the external Firmware MCP server. For each legitimate item, record its existing consumer or exact smallest firmware-compatibility seam plus one focused oracle. For each rejected campaign/extraneous/duplicate item, record deletion and any required consumer-unwind seam. Include the exact tests, release checks, and public documentation to update before writer allocation. | coder-main can implement without making an architectural retention decision and reviewer-main can audit the same directive. | An undecidable semantic item remains with ROOT-IM and writer allocation does not start. |
| HANDOFF-RETIRE | LANE-RETIRE | ROOT-IM, then MI-CANDIDATE-EVIDENCE only after a new dispatch | Every retirement writer result | Writer invocation, worktree, and logical task IDs | Publish one tip, implementation trace against HANDOFF-RETIRE-DIRECTIVE, diff, and self-check state; terminate coder-main and emit no successor. | ROOT-IM can inspect one frozen input against its directive and separately dispatch doer-main evidence plus reviewer-main. | P09, ROOT-IM clarification, or MI-CANDIDATE-DECIDE after separately dispatched evidence |
| HANDOFF-REPAIR | LANE-REPAIR or LANE-SAFEGUARD-CHECKPOINT | ROOT-IM, then MI-CANDIDATE-EVIDENCE through EDGE-003 or MI-VERIFICATION-ASSET-CORRECT through EDGE-003V only after a new dispatch | Every product-repair task result | Prior/new coder invocation, repair worktree, logical task ID, originating M05 or EDGE-007E decision, failed behavior, responsible seam, protected surfaces, focused oracle, tip, and self-check state | Publish one pooled-finding repair tip and terminate coder-main. No checker, verification-asset writer, integration, or assurance successor is emitted by the writer. | ROOT-IM can diagnose the terminal repair, decide whether trusted assets suffice, and issue either a separate M04 evidence card or a separate M03 doer-main asset card over one frozen tip. | P09, ROOT-IM clarification, EDGE-003, or EDGE-003V |
| HANDOFF-RELEASE-FORMAT | LANE-RELEASE-FORMAT | ROOT-IM, then MI-CANDIDATE-EVIDENCE only after a new dispatch | Every format writer result | Writer invocation, format worktree, declared parent, and logical task IDs | Publish the exact named-file normalization and formatter commands, source encoding/round-trip facts, Ruff version, clean descendant tip, changed-path count, terminal self-check, and confirmation that no content/configuration edit was made; terminate coder-main and emit no successor. | ROOT-IM can bind one frozen tip and separately dispatch doer-main to reproduce both transformations and execute CHECK-RELEASE-FORMAT. | P09, ROOT-IM clarification, or EDGE-006F after separately dispatched evidence. |
| HANDOFF-ATTENTION-ASSET | LANE-ATTENTION-ASSET | ROOT-IM, then MI-CANDIDATE-EVIDENCE only after a new dispatch | Verification task result when consumed | doer-main invocation, verification worktree, prior/new invocation when replaced, and logical task IDs | Publish one clean tip, exact three-file diff, retained practical/current wake/removed-policy test results, compile/whitespace state, and confirmation that no product source/API or unrelated practical assertion changed; terminate the M03 doer run. | ROOT-IM can inspect the terminal asset handoff and separately dispatch reviewer-main plus the doer-main M04 evidence card over one frozen input. | P09, EDGE-006T, or ROOT-IM classification on a semantic contradiction. |
| HANDOFF-VERIFICATION-ASSET | LANE-VERIFICATION-ASSET | ROOT-IM, then MI-CANDIDATE-EVIDENCE through EDGE-003G only after a new dispatch | Every reusable verification-asset task result | doer-main invocation, verification worktree, logical task and originating edge IDs, frozen product/repair tip, proof contract, allowed paths, mandatory checks, exact diff, self-check results, and protected-surface state | Publish one clean tip and complete contract-indexed self-check facts, confirm no product source or semantics changed, terminate the M03 doer run, and emit no M04 or integration successor. | ROOT-IM can inspect the terminal asset handoff and separately dispatch reviewer-main plus the doer-main M04 evidence card over one frozen input. | P09, EDGE-006V, or ROOT-IM classification on a product/semantic contradiction. |
| HANDOFF-CANDIDATE-EVIDENCE | LANE-CANDIDATE-CHECK and optional LANE-CANDIDATE-REVIEW | MI-CANDIDATE-DECIDE | Branch-local terminal check/review results when consumed | Frozen tip, active edge, doer-main check invocation/process IDs, optional reviewer invocation ID, separate result roots, and logical task IDs | Publish each declared terminal fact against one frozen input, then terminate the check/review runs. ROOT-IM receives the complete joined pool and no executor emits an acceptance verdict or starts integration. | MI-CANDIDATE-DECIDE can decide the branch without reconstructing or rerunning unrelated facts. | P09 or MI-CANDIDATE-DECIDE. |
| HANDOFF-CANDIDATE-INTEGRATE | LANE-CANDIDATE-INTEGRATE | ROOT-IM, then MI-RELEASE-ASSURE or a declared admitted-repair successor | Every integration operation result | ROOT-IM's new integration authorization, accepted tip/verdict, doer-main invocation, destination worktree, rollback base, post-join result paths, and readback coordinate | Publish exact fast-forward/readback/post-join facts and the first unresolved operation if replacement is needed, then terminate doer-main. The preceding check run is already terminal; this is a separately dispatched invocation, which may use available provider continuity but never continues the prior run or emits its own successor. | ROOT-IM classifies the terminal operation and dispatches the next consumer over one verified integrated coordinate. | GATE-INTEGRATION or P09. |
| HANDOFF-RELEASE-SAFEGUARD | LANE-RELEASE-SAFEGUARD | MI-RELEASE-DECIDE | Safeguard result/checkpoint when consumed | Integrated coordinate, ROOT-IM binding, doer-main invocation/process ID, unique result path, changed paths/domains, declared unit input map, and consumed checkpoint | Publish every feasible selected unit's PASS/FAIL/SKIP/UNRESOLVED disposition, first unresolved unit, each justified skip reason, and the next consumed checkpoint state; final-reviewer remains independent and ROOT-IM joins/classifies both. | MI-RELEASE-DECIDE receives the complete PG-RELEASE pool without reconstructing an unchanged prefix. | P09 or MI-RELEASE-DECIDE. |
| HANDOFF-RELEASE | MI-RELEASE-ASSURE | MI-RELEASE-DECIDE | Final pool when consumer needs it | Review/check invocation IDs and integrated coordinate | Publish one joined final pool. | ROOT-IM can issue release verdict. | P09 or MI-RELEASE-DECIDE |
| HANDOFF-FIRMWARE-READINESS | MI-FIRMWARE-HOST-READINESS | ROOT-IM and later MI-FIRMWARE-SPRINT | Readiness result when later admission consumes it | Manager/provider invocation, target worktree, watcher, MCP process-tree, and handoff IDs | Publish role/target launch correlation; the accepted source/static/raw catalog preflight; task-local launcher marker and captured target-side `ListToolsRequest`; returned server alias/status; provider event/final-response paths; the absent-or-empty disposable server tool-event file; target status/event facts; and cleanup. Record that the invocation named no hardware identifier, lease, permission, or endpoint and that no provider tool event occurred. | ROOT-IM can expose or hold the hardware boundary without inferring a product pass. | P09, P12, or P15 |
| HANDOFF-FIRMWARE | MI-FIRMWARE-SPRINT | MI-FIRMWARE-DECIDE; a replacement manager consumes the checkpoint only before completion | Logical-sprint terminal result/checkpoint when needed | Stable sprint ID/index, hosting epochs, old/new runtime IDs, accepted checkpoint, exact claims/resources, fresh-authority facts, every unit disposition, `harness_error_observed`, and finding pool | Before completion publish only continuation checkpoints; at completion publish exactly one `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS` handoff with every feasible unit/finding and explicit cleanup/uncertainty. No mid-sprint handoff authorizes harness repair. | ROOT-IM can classify the complete sprint without reconstructing history. | P09, P10, EXC-SUITE-CONTINUATION, or P15 |

| Source allocation ID | Mode | Source/worktree | Writer | Mutable root | Consumer | Completion condition | Failure route |
|---|---|---|---|---|---|---|---|
| ALLOC-CANDIDATE | Identified linked worktree | Current accepted candidate, then exact repair worktree when a material return exists | coder-main | One writer worktree | Evidence and integration modules | Clean tip is published or dirty state remains visible. | Do not retire dirty or live worktree. |
| ALLOC-RELEASE-FORMAT | Identified linked worktree | Clean branch from canonical `3a73a7b` | coder-main | One source-conformance writer worktree; disposable reproduction root is separate | MI-CANDIDATE-EVIDENCE and MI-CANDIDATE-INTEGRATE | Exact normalization/formatter descendant and deterministic comparison result are published, or dirty/failed state remains visible. | Do not retire dirty/live state; do not reuse the root for a different source task. |
| ALLOC-ATTENTION-ASSET | Identified linked worktree | Clean branch from the canonical coordinate carried by EDGE-009T initially or EDGE-007T on the accepted retry | doer-main | One verification-asset worktree limited to the practical, its retention unit, and guide | MI-CANDIDATE-EVIDENCE and MI-CANDIDATE-INTEGRATE | Clean three-file descendant and affected result are published, or dirty/failed state remains visible. | Do not retire dirty/live state; do not widen the allocation to product source. |
| ALLOC-VERIFICATION-ASSET | Identified linked worktree | Clean branch from the exact frozen product or repair tip named in EDGE-003V, EDGE-006V, EDGE-009V, or EDGE-013V | doer-main | One verification-asset worktree limited to ROOT-IM's exact authorized paths | MI-CANDIDATE-EVIDENCE and MI-CANDIDATE-INTEGRATE | Clean verification-only descendant and contract-indexed results are published, or dirty/failed state remains visible. | Do not retire dirty/live state; any need to edit product source returns to ROOT-IM. |
| ALLOC-EVIDENCE | Read-only candidate plus separate writable roots | Frozen candidate for reviewer/checker | reviewer-main and final-reviewer | Separate result/cache roots | M05 decisions | Each result binds to one declared candidate input. | P09 support isolation. |
| ALLOC-FIRMWARE | Package-local target plus stable logical-sprint roots and replaceable runtime roots | `Firmware/target-harness/`; unique readiness/tmp roots; suite roots keyed by logical sprint with epoch/provider subroots | Firmware suite manager | Target watcher/MCP/artifact state and suite evidence; no shared recovery root | MI-FIRMWARE-HOST-READINESS and MI-FIRMWARE-SPRINT | Target coordinate recorded; fake recovery roots are unique/disposable; live runtime replacement never changes logical sprint identity. | No launch until exact admission; uncertain claim holds only its resource. |

| Retirement ID | Target | Owner | Activation | What must be retained | Completion condition | Recovery visibility | Failure route |
|---|---|---|---|---|---|---|---|
| RETIRE-CAMPAIGN | Obsolete remainder of the already isolated `firmware_acceptance/` package plus campaign-only tests, documentation, and release-check attachments after ROOT-IM's bounded retention decision | ROOT-IM semantic owner; coder-main executor | MI-CAMPAIGN-RETIRE after HANDOFF-RETIRE-DIRECTIVE | Every behavior ROOT-IM found useful to a generic firmware-access harness, including qualifying MCP/process, lease, and hardware-access behavior; its existing or newly wired firmware-compatibility consumer; the installed generic package; `orchestrator_harness.capability_broker`; genuinely generic broker tests; compatibility tests; and historical evidence needed by a named consumer | Retained/rehomed/wired generic firmware-access behavior passes its focused oracle; consumers no longer depend on rejected campaign/extraneous behavior; obsolete controller/evidence/topology code and stale attachments are gone. | ROOT-IM directive, implementation trace, diff, and integrated source coordinate remain visible to their named consumers. | MI-CANDIDATE-DECIDE material route or ROOT-IM semantic clarification. |
| RETIRE-LANES | Terminal candidate/review/format/assurance lanes | ROOT-IM | M05 acceptance or exact operation closure | Accepted tips/results and dirty/live state | Only clean, unclaimed lanes are retired. | Handoff and source allocation rows remain visible. | Leave terminal-visible for recovery. |
| RETIRE-FIRMWARE-HOST-READINESS | Disposable readiness provider, watcher, MCP process tree, and state roots | acceptance-orchestrator | MI-FIRMWARE-HOST-READINESS terminal closure | Readiness result and exact process/root correlation needed by later hardware admission | Every identified descendant has exited and disposable roots are retired or retained with their status visible. | HANDOFF-FIRMWARE-READINESS remains available to ROOT-IM. | Block only later physical-resource use. |
| RETIRE-SUITE-EPOCH | Replaced or completed external manager/provider epoch | Firmware suite manager | EXC-SUITE-CONTINUATION replacement or all hosted sprint work terminal | Durable sprint checkpoints/evidence/findings and exact cleanup facts | Old runtime authority is invalid, owned processes are absent/contained, and remaining uncertainty is scoped to exact resources; logical sprints continue or publish completed handoffs. | Existing epoch record remains available to the sprint/M05. | Block only exact uncertain resources; never terminate unrelated lanes/sprints. |

## 11. Module instances

### MI-CAMPAIGN-RETIRE - M02: Salvage useful firmware-layer behavior and retire the obsolete campaign

#### Purpose

Deliver DEL-CAMPAIGN-RETIREMENT through one high-context ROOT-IM legitimacy and consumer-routing decision followed by one serial writer: ROOT-IM inspects the already isolated package by responsibility and decides retain/minimally-rehome/wire/unwind/delete; coder-main implements that directive, removes the obsolete remainder, updates repository attachments and public scope, and publishes one reviewable tip.

#### Coverage

REQ-R01, REQ-R02, and REQ-R03; OUT-002. The generic `capability_broker` is already an independently installed/exported boundary and remains. ROOT-IM decides whether firmware-specific adapter, campaign-pack translation, MCP/process, lease, hardware-access, or policy behavior is useful to a generic firmware-access harness. Relationship or resemblance to the external Firmware MCP server does not count against it because that server is the required hardware-access path and the isolated package predates the copied server. Consumer status is evaluated only after that legitimacy decision: an existing consumer keeps or minimally rehomes legitimate behavior, an absent consumer triggers wiring into the existing firmware compatibility layer, and a consumer of rejected campaign/extraneous behavior is unwound. coder-main does not make those decisions merely because code exists or has a caller.

#### Selection basis

The package is not entangled with or installed as the generic runtime. Its roughly 3,800 lines may still contain useful generic firmware-access behavior even though all of it is firmware-related, and deciding what earns a harness home requires whole-architecture judgment. The decision removes campaign/extraneous machinery without mistakenly discarding the MCP/process, lease, and hardware-access capabilities that make generic firmware access work. ROOT-IM already owns that context and final acceptance, so one ROOT-IM source/responsibility pass followed by one bounded implementation is cheaper and safer than delegating the architecture and repairing it later. No separate discovery agent, module, or gate is added.

#### Owner and roles

ROOT-IM owns the complete responsibility-level retention directive, scope, semantic clarification, and acceptance; coder-main is the sole implementation writer under LANE-RETIRE.

#### Preconditions

The user has explicitly resumed execution; the accepted candidate is clean; ROOT-IM has read every isolated-package responsibility and the current core/Firmware ownership contracts; CHECK-RETIRE-MAP passes; and EDGE-001 supplies HANDOFF-RETIRE-DIRECTIVE before coder-main allocation.

#### Inputs

Accepted generic candidate, candidate worktree ID, writer invocation/process IDs, HANDOFF-RETIRE-DIRECTIVE, only the source responsibilities and current contracts needed to implement it, affected tests, release-check registry, and public documentation.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-RETIRE; MI-CAMPAIGN-RETIRE; DEL-CAMPAIGN-RETIREMENT; retirement; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR |
| workflow_role | coder-main |
| objective | Implement ROOT-IM's retention directive exactly: preserve and consume the named generic firmware-access behavior, unwind rejected campaign/extraneous dependencies, remove the obsolete campaign controller/evidence/topology remainder, and preserve generic compatibility. |
| why_now | The generic candidate is frozen and ROOT-IM has completed the architectural retention decision required before implementation. |
| starting_state | Clean accepted candidate, identified worktree and writer invocation IDs, no active campaign lane, and complete HANDOFF-RETIRE-DIRECTIVE. |
| dependencies_and_predecessor_outputs | EDGE-001 accepted candidate, BOUND-001 user resume, CHECK-RETIRE-MAP, and HANDOFF-RETIRE-DIRECTIVE. |
| working_scope | The isolated `firmware_acceptance/` package, optional firmware capability seam, its dedicated/mixed tests, release-check attachments, and public documentation; no external Firmware suite, provider configuration, MCP-server, or hardware edits. |
| required_behavior | Follow HANDOFF-RETIRE-DIRECTIVE exactly. Retain or minimally rehome each behavior ROOT-IM identified as useful generic firmware-access capability, including directed MCP/process, lease, and hardware-access behavior. Preserve its existing consumer, or create the directed integration with the smallest existing firmware compatibility seam when no consumer exists, and implement one focused oracle. Any retained behavior whose worktree, provider/server, resource, or policy value varies must receive that value from the existing invocation/configuration path rather than a fixed local constant. Do not add a second controller, registry, configuration source, or ownership layer. For rejected campaign/extraneous behavior with a current consumer, implement the directed unwind. Preserve the generic capability broker. Remove the directed C1/C2/C3 controller, attempt/evidence/pinning/fixed-fixture campaign machinery and other rejected code, then remove or update its tests, release checks, and public usage/recovery documentation. If source facts contradict the directive or a semantic choice is missing, stop that item and return the exact contradiction to ROOT-IM; do not make a new architectural retention decision. |
| initial_entrypoints | HANDOFF-RETIRE-DIRECTIVE; the `firmware_acceptance/*.py` responsibilities it assigns; named generic destination seams such as `orchestrator_harness.capability_broker`; assigned dedicated/mixed tests; candidate release registry; public docs. Count 6 because these are the minimum implementation, verification, and cleanup surfaces after ROOT-IM has already made the usefulness/ownership decision. |
| failure_case_brief | REQ-R01: implementation could diverge from ROOT-IM's directive, discard a named behavior, retain rejected campaign machinery, or reveal a source contradiction; oracle is directive-to-diff traceability plus retained-component and affected compatibility tests; ROOT-IM decides any semantic contradiction. |
| ordered_actions | M02-A1: verify candidate/worktree ownership and HANDOFF-RETIRE-DIRECTIVE completeness; M02-A2: read the directive, its assigned source entrypoints, and governing requirement/acceptance rows without reconstructing the architectural decision; M02-A3: convert the directive and failure brief into implementation invariants and focused self-check targets, returning any semantic contradiction to ROOT-IM; M02-A4: implement the complete minimal salvage and obsolete-code/test/doc/release cleanup serially; M02-A5: run retained-component and shortest affected generic/compatibility self-checks; M02-A6: inspect the final diff for directive divergence, lost named behavior, dead moved code, and stale references; M02-A7: publish one tip and complete implementation trace; M02-A8: on admitted material return repair the complete pool once within the directive, returning any required semantic change to ROOT-IM. |
| allowed_tools_capabilities_resources | Read-only source search, Git diff/status, candidate writer tools, and covered command supervisor where the launcher policy applies. |
| forbidden_actions_and_boundaries | No hardware, external Firmware suite/MCP-server changes, provider mapping edits, broad campaign recreation, architectural reclassification, blanket deletion outside the directive, duplicate controller/registry/configuration ownership, fixed current-machine/provider/fixture/catalog values, preservation solely because a current consumer exists, or dormant retention without the ROOT-directed consumer/wiring route and focused oracle. |
| verification | CHECK-RETIRE-MAP, focused tests for every retained/rehomed/wired generic firmware behavior and every unwind seam, and the shortest affected generic/compatibility self-checks through P02/P04. |
| deliverables_and_result_paths | One reviewable tip, complete directive-to-diff implementation trace, diff summary, and task-local result paths only when consumers need them. |
| acceptance_criteria_and_tolerances | Every directive item is implemented or returned to ROOT-IM with an exact contradiction; every retained/rehomed behavior is useful generic firmware-access capability with an existing or newly wired firmware-compatibility consumer and passing focused oracle; every rejected campaign/extraneous behavior is absent and any directed consumer dependency is unwound; obsolete campaign machinery and stale attachments are gone; no retained generic behavior breaks. No tolerance for unexplained divergence, deletion, or dead-code preservation. |
| completion_review_owner_and_handoff | coder-main publishes HANDOFF-RETIRE and terminates. ROOT-IM inspects it against HANDOFF-RETIRE-DIRECTIVE and separately dispatches MI-CANDIDATE-EVIDENCE; an admitted retirement finding returns through EDGE-006A to a new card for this same logical task. |
| failure_classification_and_routes | Implementation divergence, lost directed behavior, or retained rejected behavior remains writer work; a semantic contradiction returns to ROOT-IM before writer continuation. Report a strict test-only or support fault without editing it in M02; ROOT-IM applies P08/P09. Later material evidence goes MI-CANDIDATE-DECIDE. |
| thread_resume_and_terminal_rule | Every coder-main retirement card terminates at HANDOFF-RETIRE. Keep and resume the same provider session by default for every admitted material return to this unaccepted candidate gate, but dispatch a new ROOT card each time. Retire the session when GATE-CANDIDATE accepts or the task otherwise terminates. If it is unavailable or no longer matches the mapping, use HANDOFF-RETIRE replacement correlation without blocking or reopening accepted work. No invocation self-crosses ROOT-IM's classification or dispatch boundary. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P07, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One scoped candidate tip and its concise implementation trace against HANDOFF-RETIRE-DIRECTIVE for MI-CANDIDATE-EVIDENCE; the directive lives in the task/reviewer input and no separate immutable design artifact is created.

#### Concurrency and isolation

One writer owns ALLOC-CANDIDATE. Review and deterministic checks start only after the frozen tip exists.

#### Resources and side effects

Source retention/rehoming, deletion, test/release cleanup, and documentation updates occur only inside the identified candidate worktree. ROOT-IM retires no dirty worktree.

#### Checks and acceptance

CHECK-RETIRE-MAP proves ROOT-IM made the complete retention decision before dispatch. Focused self-checks prove the writer implemented it without discarding named behavior, retaining rejected machinery, or breaking generic compatibility; MI-CANDIDATE-DECIDE owns acceptance.

#### Failure and exception routes

A material implementation self-check failure continues inside this task. A semantic contradiction returns to ROOT-IM without writer improvisation. MI-CANDIDATE-DECIDE returns a complete admitted retirement implementation pool through EDGE-006A to this same logical task; no local exception exists.

#### Prior results and change effects

The accepted generic coordinate is preserved. Only ROOT-classified campaign/optional-firmware source, its repository attachments, and selected affected checks are invalidated by the change.

#### Repeat, join, and terminal behavior

GATE-CANDIDATE receives one candidate evidence pool. EDGE-006A returns an admitted pool to this same retirement task, which repairs the full pool once; acceptance makes the retirement task terminal.

#### Cost and critical-path effect

Expected 25-50 minutes including ROOT-IM's one-time source/responsibility decision; one writer launch and no extra discovery lane; it starts the retirement-to-assurance critical path and reduces likely semantic repair cycles.

### MI-HARNESS-REPAIR - M02: Repair a verified affected harness defect

#### Purpose

Use the existing serial repair route for the current suites 003-008 continuation defect and for any later ROOT-IM-admitted harness defect. The current task adds no recovery framework: it changes only the target seams necessary to preserve durable work across dead runtime identities and to make a stale claim recoverable after exact absence proof.

#### Coverage

REQ-F02 and OUT-005 for the current activation; later activations carry only their originating affected requirement. Accepted historical uses of this module remain closed.

#### Selection basis

`HANDOFF_SPRINT_FAILURE.md` shows six non-harness interruptions and two harness defects all terminalized because runtime identity validity was treated as a prerequisite for logical-sprint continuity. The target already has claim, reconcile, resume/handoff, and lane-controller seams. Extending those seams plus the suite contract is cheaper and safer than a new controller, disposition subsystem, or dedicated recovery module.

#### Owner and roles

ROOT-IM has reconciled the exact accepted base and authors the repair/proof contract. coder-main owns one serial repair worktree under LANE-REPAIR and returns terminally to ROOT-IM.

#### Preconditions

EDGE-010R ready; current M07/M08 credit retained; suites 003-008 and their processes stopped; no live claim authority, lease, MCP action, or hardware action; ROOT-IM reconciled the retained `055a5bd...` boundary through review 062, proof 063, and integration 064 and bound clean `dd673cb...`, tree `c18ccd0...`, as the exact repair base.

#### Inputs

Exact base/tree, `HANDOFF_SPRINT_FAILURE.md`, affected target files `orchestrator_harness/resource_locks.py`, `resume.py`, `lane_controller.py`, and `reconcile.py`, existing related tests, ROOT's four-case contract, protected live-hardware boundary, repair worktree/invocation IDs, and HANDOFF-REPAIR.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-REPAIR; MI-HARNESS-REPAIR; DEL-FIRMWARE-VALIDATION; sprint-continuation; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR |
| workflow_role | coder-main |
| objective | Implement the smallest target repair that lets an interrupted logical sprint use verified durable progress under a replacement runtime identity and safely reacquire a dead owner's stale claim after complete absence proof, while uncertainty continues to block only that exact resource. |
| why_now | Suites 004-008 repeatedly preserved useful work but could not continue because fail-closed claims and exact-session resume rules had no safe replacement path; the current streak therefore remains `0/3`. |
| starting_state | Exact ROOT-bound clean candidate; stopped suite processes; accepted M07/M08 credit; existing claim/reconcile/resume/lane-controller implementation and tests; no live/hardware authority. |
| dependencies_and_predecessor_outputs | EDGE-010R, BOUND-008, HANDOFF_SPRINT_FAILURE.md, exact base reconciliation, and ROOT's CHECK-SPRINT-CONTINUATION proof/no-hardware contract. |
| working_scope | Inspect and edit only the smallest necessary subset of `orchestrator_harness/resource_locks.py`, `resume.py`, `lane_controller.py`, and `reconcile.py`; add or adjust only directly affected target tests. Provider adapters, Firmware server/source, catalog logic, hardware code, release selection, unrelated lifecycle behavior, and public APIs are protected unless ROOT separately proves one is the responsible seam. |
| required_behavior | Preserve the logical task's accepted repository/task checkpoint while treating controller PID, provider session, plan, permission, lease, and live claim ownership as replaceable. Permit stale-claim reacquisition only when a complete current inventory proves the exact old owner and every recorded retained process absent; retain fail-closed waiting when proof is incomplete. Emit an ordinary structured handoff/fresh start for an unavailable exact session instead of requiring it. Do not implement sprint scheduling, streak policy, or a second recovery ledger in product code. |
| initial_entrypoints | `resource_locks.py` `_retained_state`, `_owner_state`, `_reclaim_stale`, and `acquire_all`; `resume.py` `make_resume_admission`/handoff behavior; `lane_controller.py` resume/handoff and retained-boundary publication; `reconcile.py` exact process/resource release observations; related resource-lock/lane-controller/reconcile tests. Count 5 because these are the smallest observed ownership, continuity, and oracle seams. |
| failure_case_brief | C1 exact-session loss must hand off verified progress without reusing dead authority. C2 `MAY_EXIST_INCOMPLETE`/`INVENTORY_UNKNOWN` may be reclaimed only after complete exact absence proof, while an incomplete inventory remains blocked. C3 correction of a non-mutating call/order fault must not corrupt checkpoint identity. C4 the product must expose facts needed for a completed finding pool without adding sprint policy. CHECK-SPRINT-CONTINUATION decides all four with fake state and zero hardware/tool events. |
| ordered_actions | M02-A1: verify exact source ownership/base. M02-A2: read the named affected entrypoints and existing tests. M02-A3: bind the admitted continuity and safe-reclaim invariants. M02-A4: implement the smallest complete repair. M02-A5: run focused self-checks through P02. M02-A6: inspect the exact diff and protected surfaces. M02-A7: publish one clean repair tip and HANDOFF-REPAIR. M02-A8: consume any later complete material return once; never repair individual findings while a pool is incomplete. |
| allowed_tools_capabilities_resources | Candidate writer tools, Git inspection, focused diagnostics, and P02-bounded no-hardware commands only. |
| forbidden_actions_and_boundaries | No new scheduler/controller/protocol/status subsystem, three-way claim taxonomy, second ledger, copied supervisor, manual claim deletion, PID-name inference, hardware/MCP tool/server plan/permission/lease action, Firmware server/app edit, speculative provider registry change, or test weakening. |
| verification | Focused existing resource-lock, resume/lane-controller, and reconcile tests; compile changed production/test source; self-check the safe wait when inventory remains incomplete; then ROOT separately dispatches M03 if the four-case asset is missing and M04 runs CHECK-SPRINT-CONTINUATION plus CHECK-CANDIDATE-REPAIR. |
| deliverables_and_result_paths | One clean repair tip and HANDOFF-REPAIR binding base/tip, exact diff, self-checks, protected surfaces, and any remaining verification-asset need. |
| acceptance_criteria_and_tolerances | Complete absence proof permits safe stale-claim reacquisition; incomplete/contradictory proof leaves the exact claim held; unavailable runtime identity yields a handoff/fresh-authority route without discarding verified checkpoint state; no extra recovery machinery or live side effect exists; all focused checks pass. |
| completion_review_owner_and_handoff | coder-main terminates at ROOT-IM. ROOT inspects the handoff and, for the current path, dispatches MI-VERIFICATION-ASSET-CORRECT through EDGE-003V because the four-case integrated oracle does not yet exist; only after that terminal handoff does ROOT dispatch M04 through EDGE-003G. |
| failure_classification_and_routes | A product failure returns as one complete compatible pool to the same M02 task after ROOT classification. A strict asset-only issue stays M03; support uses P09. Coordinate contradiction or unexpected source owner returns to ROOT without widening scope. |
| thread_resume_and_terminal_rule | Every coder card ends at HANDOFF-REPAIR. ROOT resumes the same idle coder-main provider session by default for each compatible material pool returned to this unaccepted candidate gate and retires it only when the gate accepts or the repair task otherwise terminates. If resume is unavailable or the mapping changed, a correlated replacement consumes the handoff without blocking or restarting the loop. No invocation self-crosses ROOT's decision boundary into testing or integration. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P07, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One reviewable focused repair tip and terminal HANDOFF-REPAIR.

#### Concurrency and isolation

One serial writer in one repair worktree; no overlapping writer on the candidate.

#### Resources and side effects

Only the named source/test worktree may change. No provider, server, MCP tool, fixture, USB, probe, serial, radio, plan, permission, or lease action is authorized.

#### Checks and acceptance

Focused self-checks precede independent M03/M04 evidence. ROOT accepts only through MI-CANDIDATE-DECIDE.

#### Failure and exception routes

Return complete product material to ROOT/M02, strict asset material to M03, and support to P09. Never manufacture success from missing absence proof.

#### Prior results and change effects

Preserve M07/M08 and all unrelated candidate credit. Invalidate only changed claim/resume/reconcile/lane-controller consumers and the affected M08 continuation action.

#### Repeat, join, and terminal behavior

One complete current finding pool yields one repair tip; ROOT then uses the existing M03/M04/M05/M06 path. No dedicated recovery loop exists.

#### Cost and critical-path effect

Expected 20-45 minutes for a small target repair before the independent four-case proof. The existing pipeline supplies all coordination cost.

### MI-SAFEGUARD-CHECKPOINT-CORRECT - M02: Make the existing candidate safeguard resumable and complete-pool

#### Purpose

Replace only the candidate safeguard's fail-fast/restart-from-top behavior with independently runnable coarse check units, a conservative input map, and a small checkpoint result so later assurance runs preserve unaffected PASS credit.

#### Coverage

REQ-A04 and the execution efficiency portion of REQ-A01/OUT-003. It does not change generic harness behavior, Firmware behavior, provider configuration, or the content of any existing release check.

#### Selection basis

The paused safeguard currently accepts changed paths and a credit-file input but throws on its first failed check and does not use either input to resume. That makes later ordinary repairs re-pay a 20-40 minute unchanged prefix and prevents ROOT-IM from receiving the complete feasible finding pool. The smallest useful correction is inside the existing candidate safeguard and release-check registry: retain the coarse existing checks, add their conservative declared inputs, record their outcomes, continue later runnable checks, and select only the required union later. A scheduler, new artifact service, per-test process fan-out, hash snapshot, or new verification framework is not justified.

#### Owner and roles

ROOT-IM supplies the exact executor/registry contract and acceptance decision. coder-main owns one serial candidate worktree under LANE-SAFEGUARD-CHECKPOINT and terminates at ROOT-IM. Existing doer-main evidence and reviewer-main review remain separate through EDGE-003.

#### Preconditions

EDGE-007E supplies the accepted `fd2761d` product coordinate, the P09 classification of the canonical-worktree environment-only post-join support condition, and ROOT-IM's proof contract. The old safeguard has not been used as incremental evidence.

#### Inputs

The current candidate `tools/Invoke-CandidateSafeguard.ps1`, its current release-check registry and existing safeguard tests, the observed fail-fast result, changed-path/credit-file interfaces already present, ROOT-IM's required unit/input-map contract, a repair worktree ID, and writer invocation/process IDs.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-SAFEGUARD-CHECKPOINT; MI-SAFEGUARD-CHECKPOINT-CORRECT; DEL-RELEASE-ASSURANCE; safeguard-checkpoint; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR |
| workflow_role | coder-main |
| objective | Produce one small candidate-owned safeguard/registry tip that collects every feasible unit result and resumes only the failed, unresolved, affected, or uncertain units from the earliest required unit. |
| why_now | The old script's first-failure throw and restart-from-top loop make a narrow repair repeatedly pay an unchanged 20-40 minute prefix and hide later feasible findings. |
| starting_state | Clean integrated `fd2761d` candidate credit, terminal old-safeguard result, P09 support classification, ROOT-IM proof contract, no live claim, and no incremental safeguard claim. |
| dependencies_and_predecessor_outputs | EDGE-007E, ROOT-IM executor/registry contract, old safeguard result, and accepted `stable_io.py` integration handoff. |
| working_scope | Only the existing candidate safeguard, its release-check registry/selection data, and their existing focused tests. Keep every current check command, selection meaning, `-ChangedPaths`/credit-file public interface, branch/tip binding, and P02 invocation path unless the checkpoint behavior requires a directly adjacent correction. |
| required_behavior | Represent each existing coarse selected check as one independently runnable unit with a conservative input map. Record PASS/FAIL/SKIP/UNRESOLVED, first unresolved, and skip reason; continue every later independent runnable unit after ordinary failure. On later invocation, compare changed paths and declared inputs, reuse only unchanged PASS entries, select failed/unresolved/affected/uncertain units, and run that set in registry order from its earliest member. |
| initial_entrypoints | Existing safeguard script; existing release registry; current safeguard tests; the old failed result; `-ChangedPaths` and credit-file inputs; ROOT-IM contract. Count 6 because they define the current behavior, compatible surface, observed defect, and proof boundary. |
| failure_case_brief | The correction could change command selection, falsely reuse a stale PASS, skip a runnable later unit, or turn a normal failure into a fabricated pass. Focused cold-run, ordinary-failure-continuation, changed-input resume, and uncertain-input tests are the oracles; a need to change a release check's behavior returns to ROOT-IM. |
| ordered_actions | M02-A1: confirm the old executor/registry ownership and freeze the exact existing check list; M02-A2: add one conservative input map per coarse existing unit, including runner/config/environment and practical inputs where relevant; M02-A3: add the smallest checkpoint read/write shape needed by the current credit-file interface; M02-A4: make ordinary failure record FAIL and continue later runnable units, recording only justified SKIP; M02-A5: make later selection the failed/unresolved/affected/uncertain union from its earliest required unit; M02-A6: add only focused existing-suite tests for cold behavior, continuation, reuse, affected rerun, and uncertainty; M02-A7: run the focused self-checks and inspect the exact diff; M02-A8: publish one repair tip and HANDOFF-REPAIR. |
| allowed_tools_capabilities_resources | Candidate writer tools, existing focused safeguard tests, Git inspection, and P02 supervisor for covered commands. |
| forbidden_actions_and_boundaries | No scheduler, daemon, new artifact store, hash/snapshot scheme, per-test fan-out, changed release-check semantics, new provider/hardware behavior, broad test rewrite, FAST_LANE_V2 use, or full final assurance from this writer card. |
| verification | Compile every changed production source and run the focused existing safeguard tests proving: (1) cold complete selection, (2) ordinary failure still runs a later independent unit, (3) unchanged PASS is reused, (4) a changed declared input and a failed/unresolved unit rerun from the earliest required unit, and (5) unknown input reruns conservatively. Then run CHECK-CANDIDATE-REPAIR and MI-CANDIDATE-EVIDENCE under P04. |
| deliverables_and_result_paths | One repair tip, focused test results, and HANDOFF-REPAIR when ROOT-IM needs durable correlation. |
| acceptance_criteria_and_tolerances | Existing coarse checks and public arguments are preserved; ordinary failure never cancels a later independent feasible unit; no PASS is reused when an input/prerequisite is changed or unknown; an invalidated earlier unit runs before the prior first unresolved unit; the complete focused proof passes; and no new runtime service or hashing machinery appears. |
| completion_review_owner_and_handoff | coder-main publishes HANDOFF-REPAIR and terminates. ROOT-IM inspects the tip against this contract and separately dispatches MI-CANDIDATE-EVIDENCE through EDGE-003 when existing assets suffice, or MI-VERIFICATION-ASSET-CORRECT through EDGE-003V only if a genuine additional verification asset is required. |
| failure_classification_and_routes | A failure in the exact checkpoint behavior remains in this M02 task after ROOT-IM pools it. A changed release-check behavior, new architecture, or ambiguous input dependency returns to ROOT-IM; strict test-only/support facts use P08/P09. |
| thread_resume_and_terminal_rule | Every coder-main card terminates at HANDOFF-REPAIR. A complete compatible material pool receives a new ROOT card that resumes the same idle provider session by default until this candidate gate accepts; unavailable or remapped sessions use correlated replacement without losing loop state. Gate acceptance retires the coder session. No writer self-continues into evidence, integration, or assurance. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P07, P08, P09, P10, P11, P13, P15; no exception. |

#### Outputs and results

One reviewable safeguard/registry repair tip and terminal HANDOFF-REPAIR. No checkpoint is release evidence until independent candidate evidence and later integration accept the implementation.

#### Concurrency and isolation

One serial writer uses its own candidate worktree. It does not overlap another source writer or a final assurance attempt.

#### Resources and side effects

Only the identified candidate worktree mutates. Checkpoint files are result state consumed by later safeguard selection, not a persistent content identity system. External suite, MCP, fixture, and hardware resources remain untouched.

#### Checks and acceptance

The focused tests prove the small executor correction; MI-CANDIDATE-EVIDENCE independently reviews the diff and executes CHECK-CANDIDATE-REPAIR. ROOT-IM accepts only a complete pool under GATE-CANDIDATE.

#### Failure and exception routes

No assurance is retried under the old runner. P09 handles only the canonical-worktree support defect; a semantic failure returns through the normal M05/P07 complete-pool route.

#### Prior results and change effects

Preserve accepted `stable_io.py` product credit and every unaffected historical check. The new runner has no credit until its focused evidence succeeds; it invalidates only release-safeguard executor/registry consumers.

#### Repeat, join, and terminal behavior

The first accepted implementation follows the normal `EDGE-003 -> EDGE-004 -> EDGE-005 -> MI-CANDIDATE-INTEGRATE` route. Its accepted integration then satisfies the new prerequisite in EDGE-007; future material returns batch under P07 before the next earliest-required safeguard run.

#### Cost and critical-path effect

Expected 20-40 minutes including focused implementation, evidence, review, and integration. This one-time correction is smaller than repeated 20-40 minute unchanged safeguard prefixes and preserves the existing release oracle rather than replacing it.

### MI-RELEASE-FORMAT-CORRECT - M02: Normalize source encoding and apply the release formatter mechanically

#### Purpose

Satisfy the candidate-owned repository-wide Ruff format criterion by losslessly normalizing the sole non-UTF-8 tracked file and then applying exactly the existing formatter, with no content, configuration, or scope change.

#### Coverage

REQ-A02 and the source-conformance portion of OUT-003 only.

#### Selection basis

The required correction mutates documentation, production, and test source, so it is not M03 test-asset work and cannot be hidden inside MI-HARNESS-REPAIR. The first exact formatter attempt proved one tracked guide blocks Ruff because it is Windows-1252; ROOT proved it round-trips losslessly and contains only one non-ASCII em dash. One asserted byte-preserving transcode followed by Ruff now defines the complete transformation. Reproducing both is stronger and cheaper than broad static review.

#### Owner and roles

ROOT-IM binds the parent, exact named-file normalization, formatter command, tool environment, scope, and prohibitions; coder-main runs them in LANE-RELEASE-FORMAT and publishes one clean descendant.

#### Preconditions

EDGE-007F proves canonical is clean at `3a73a7b`, the first attempt restored that parent and released its claim, ROOT proved the exact lossless normalization, the existing release registry and Ruff configuration are unchanged, and this amendment has passed structural validation.

#### Inputs

Declared parent coordinate, isolated writer worktree and branch IDs, coder invocation/process IDs, the exact guide path/source-byte facts, authoritative Ruff version/tool environment, existing formatter scope, first blocked result, and preserved semantic credit.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-RELEASE-FORMAT; MI-RELEASE-FORMAT-CORRECT; DEL-RELEASE-FORMAT; release-format; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR |
| workflow_role | coder-main |
| objective | Produce one clean descendant that differs from `3a73a7b` only by the declared lossless guide normalization plus Ruff's deterministic repository-wide output. |
| why_now | The first attempt proved Ruff's 93-file correction cannot finish until the sole non-UTF-8 tracked guide is normalized; ROOT proved that normalization is exact and lossless. |
| starting_state | Clean isolated worktree restored to the exact parent, terminal blocked result with released claim, fixed existing Ruff configuration/scope, preserved semantic verdicts, and no active source writer. |
| dependencies_and_predecessor_outputs | EDGE-007F; accepted retirement/protocol integration; first blocked format result; ROOT's one-file encoding proof. |
| working_scope | `harness_watcher_implementation/CANARY_GUIDE.md` for the exact encoding-only normalization, followed by exactly the files changed by `python -m ruff format .`. No other file or setting is writable. |
| required_behavior | Through P02 and the repository UV tool environment, run one Python command that asserts the guide's only non-ASCII byte is `(26, 0x97)`, asserts Windows-1252 round-trip equality, and writes the same decoded text as UTF-8 without newline transformation; then run exactly `python -m ruff format .` once. Make no hand/content edit and do not change configuration, exclusions, release checks, dependencies, or semantics. Prove all tracked files strict UTF-8; run format-check and existing compile check; inspect diff; commit one complete descendant; report any new contradiction. |
| initial_entrypoints | Declared parent status; first blocked result; named guide/source-byte proof; Ruff configuration/release entry; repository source tree; bounded-command policy. Count 6 because they bind source identity, admitted normalization, exact formatter, scope, and execution. |
| failure_case_brief | Wrong parent/path/bytes, non-lossless normalization, content/configuration edit, incomplete formatter output, new lint finding versus the parent, failed UTF-8/format/compile check, or extra path invalidates REQ-A02. Exact source assertions, fresh reproduction, parent/tip Ruff finding comparison, and declared checks are the oracles; ROOT-IM owns classification. |
| ordered_actions | M02-A1: verify exact clean restored parent and isolated allocation; M02-A2: bind the prior blocker and exact source-byte assertions; M02-A3: bind unique bounded paths; M02-A4: normalize only the named guide; M02-A5: run Ruff format once; M02-A6: run UTF-8, format-check, compile, and diff self-checks; M02-A7: inspect and commit one clean descendant; M02-A8: publish the complete handoff or return one new contradiction. |
| allowed_tools_capabilities_resources | Exact asserted Python transcode, Ruff formatter/check, tracked-file UTF-8 scan, existing compile check, read-only Git inspection, commit, and P02 supervisor for every covered Python command. |
| forbidden_actions_and_boundaries | No hand/content edit, formatter/configuration/exclusion/release-registry change, broad encoding cleanup, semantic redesign, generated-file cleanup, unrelated fix, test rewrite, broad verifier, MCP/server action, or hardware action. |
| verification | Writer self-check proves all tracked files strict UTF-8, repository-wide Ruff format-check, existing release compilation, `git diff --check`, and clean committed state; independent acceptance reproduces both transformations under CHECK-RELEASE-FORMAT. |
| deliverables_and_result_paths | One clean source-conformance tip and HANDOFF-RELEASE-FORMAT with exact normalization/formatter/tool/parent/self-check facts. |
| acceptance_criteria_and_tolerances | The tip is a direct clean descendant of the parent; the guide's decoded text and line endings are unchanged while its bytes become UTF-8; every other change comes from Ruff; UTF-8, format, compile, and whitespace checks pass; no Ruff path/code/message finding exists on the tip unless the same finding existed on the parent; no configuration/content edit exists; no tolerance is permitted. |
| completion_review_owner_and_handoff | coder-main publishes HANDOFF-RELEASE-FORMAT and terminates. ROOT-IM freezes and inspects the tip, then separately dispatches doer-main through EDGE-003F to MI-CANDIDATE-EVIDENCE. |
| failure_classification_and_routes | Launch/support faults follow P09; source-conformance failure returns through EDGE-006F; an apparent content or configuration need stops and returns to ROOT-IM rather than expanding this task. |
| thread_resume_and_terminal_rule | Every coder-main format card terminates at HANDOFF-RELEASE-FORMAT or an honest contradiction. The same idle provider session receives each new ROOT-IM correction card for this unaccepted candidate gate by default, with the complete blocker classification. Gate acceptance retires it; unavailability or a mapping change uses correlated replacement without blocking or losing task state. No invocation self-crosses into deterministic evidence or integration. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P07, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One clean, mechanically normalized/formatted descendant plus the exact transformation/self-check handoff consumed by MI-CANDIDATE-EVIDENCE.

#### Concurrency and isolation

One serial source writer owns one isolated worktree. No other source writer or deterministic reproduction runs against that mutable root.

#### Resources and side effects

Only the isolated format worktree mutates. The named guide is transcoded once and Ruff may rewrite every file in its existing scope; no external process, server, suite, or hardware resource is touched.

#### Checks and acceptance

The writer establishes clean UTF-8 and formatter results; CHECK-RELEASE-FORMAT independently reproduces the same tree from the parent, runs UTF-8/format/compile/whitespace checks, and proves the tip introduces no Ruff finding absent from the parent before ROOT-IM decides REQ-A02.

#### Failure and exception routes

A support fault follows P09. A source-conformance mismatch returns once through EDGE-006F. The separately proven implicit release-lint rule-selection defect is not fixed here; after accepted format integration it follows the already-declared EDGE-007L to MI-HARNESS-REPAIR.

#### Prior results and change effects

All retirement, protocol-repair, focused-review, and affected-check credit remains. Only source-format conformance, integration, and the final assurance release unit are invalidated.

#### Repeat, join, and terminal behavior

Success takes EDGE-003F into the existing candidate evidence/decision/integration lifecycle. One complete source-conformance finding pool may return through EDGE-006F; no reviewer-comment loop exists.

#### Cost and critical-path effect

Expected 10-25 minutes. The formatter itself is short; deterministic reproduction and conformance checks dominate the bounded task and avoid a low-value 93-file review.

### MI-VERIFICATION-ASSET-CORRECT - M03: Construct or correct an exact required verification asset

#### Purpose

Provide the reusable Plan-wide verification-asset route for any current or future module when ROOT-IM proves that existing trusted assets cannot establish the named behavior without a test, fixture, guide, or other verification-only edit.

#### Coverage

Only the active affected requirement and proof gap named by ROOT-IM. The current attention correction uses its dedicated instance instead; this instance covers later candidate, release, product-repair, and Firmware-discovered generic-harness verification gaps.

#### Selection basis

P08 already required every verification-asset mutation to use doer-main, but a prose rule alone did not provide a typed route from a later product repair or M05 strict test-only decision. This instance closes that graph gap without adding work when existing trusted checks suffice: direct repair evidence still takes EDGE-003, while only a proven asset need takes EDGE-003V, EDGE-006V, EDGE-009V, or EDGE-013V.

#### Owner and roles

ROOT-IM diagnoses the proof gap and owns its exact behavior/goals, protected surfaces, classification, allowed paths, mandatory existing checks, and acceptance criteria. doer-main alone chooses and implements the minimal verification assets and self-check commands inside that contract. reviewer-main later reviews the frozen verification diff inside MI-CANDIDATE-EVIDENCE.

#### Preconditions

Exactly one of EDGE-003V, EDGE-006V, EDGE-009V, or EDGE-013V is active; the product or repair tip is frozen; accepted requirements and independent evidence fix the expected behavior; ROOT-IM has classified the work as verification-only and supplied the complete proof contract; and LANE-VERIFICATION-ASSET plus its worktree, invocation, and handoff IDs are allocated.

#### Inputs

Frozen product or repair tip, originating M02/M05 result, exact ROOT-IM proof contract, allowed verification paths, named protected/no-change surfaces, mandatory existing checks, accepted product evidence, prior relevant credit, verification worktree ID, doer invocation/process IDs, and P02 execution contract. Firmware server, fixture, specification, support, suite-owned tests, MCP operations, and hardware are never inputs.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-VERIFICATION-ASSET-CORRECT; MI-VERIFICATION-ASSET-CORRECT; active affected deliverable carried by the originating edge; verification-asset; GATE-CANDIDATE; LOOP-VERIFICATION-ASSET |
| workflow_role | doer-main |
| objective | Produce one clean verification-only descendant that proves every ROOT-IM-named behavior and goal, preserves every named no-change surface, and changes only the exact authorized asset paths. |
| why_now | ROOT-IM has established that the active required claim cannot be decided from unchanged trusted assets and has classified the missing or faulty oracle as verification-only. |
| starting_state | One frozen product or repair tip, exact proof contract, accepted expected behavior, preserved unrelated credit, identified verification worktree, and no active source writer. |
| dependencies_and_predecessor_outputs | Exactly one of EDGE-003V, EDGE-006V, EDGE-009V, or EDGE-013V; HANDOFF-REPAIR is also required on EDGE-003V. |
| working_scope | Only the exact verification-asset paths and test goals named by ROOT-IM. doer-main chooses the concrete test/fixture/guide implementation within them. No product source, API, release policy, server, fixture ownership, suite state, or unrelated verification asset is writable. |
| required_behavior | Implement the smallest independent oracle that proves every named behavior/goal and preserves every protected surface. Keep product semantics unchanged; preserve the originating repair invariant when EDGE-003V is active; run every mandatory existing check plus the smallest selected self-checks; report any contradiction instead of changing the contract or product. |
| initial_entrypoints | ROOT-IM proof contract; frozen product/repair diff; allowed asset paths; accepted expected-behavior evidence; mandatory existing checks; prior relevant result (maximum count 6). These bind the complete proof gap without importing unrelated module context. |
| failure_case_brief | The asset may encode a guessed expectation, weaken an oracle, touch product source, exceed authorized paths, duplicate a trusted check, or fail to prove the originating repair. Exact contract review, path diff, independent expected-behavior evidence, self-checks, and later CHECK-VERIFICATION-ASSET decide those cases; ROOT-IM owns classification. |
| ordered_actions | M03-A1: confirm unchanged trusted assets cannot close the exact proof gap; M03-A2: bind ROOT-IM's behaviors/goals, expected evidence, protected surfaces, allowed paths, classification, and mandatory checks; M03-A3: choose the smallest concrete verification implementation and focused commands; M03-A4: edit only authorized verification assets; M03-A5: run every mandatory and selected self-check through P02; M03-A6: inspect exact scope, proof strength, protected surfaces, and no-product-edit state; M03-A7: publish one clean tip and HANDOFF-VERIFICATION-ASSET, then stop without launching M04 or integration. |
| allowed_tools_capabilities_resources | Read/write the declared verification worktree and exact authorized paths; read the frozen product, requirements, and accepted evidence; run Git inspection and P02-supervised focused checks. |
| forbidden_actions_and_boundaries | No product/API/configuration/registry change; no requirement or acceptance decision; no new framework or broad fixture system; no unrelated test cleanup; no Firmware server, suite-owned test, MCP, network, provider-tool, or hardware action; no M04 or M06 self-dispatch. |
| verification | Run every mandatory existing check in ROOT-IM's card plus the smallest selected focused commands proving all named targets; verify exact authorized paths and `git diff --check`. On EDGE-003V, include the originating repair's focused oracle. Every covered command uses a unique P02 result path and a history- or plan-derived bound. MI-CANDIDATE-EVIDENCE later independently runs CHECK-VERIFICATION-ASSET and, for EDGE-003V, CHECK-CANDIDATE-REPAIR. |
| deliverables_and_result_paths | One clean verification-only descendant, exact diff, contract-indexed self-check results, and HANDOFF-VERIFICATION-ASSET. |
| acceptance_criteria_and_tolerances | Every named behavior/goal is proved; every protected surface remains unchanged; only authorized verification paths differ; product semantics and source remain unchanged; mandatory checks pass; the originating repair invariant remains true when applicable. No tolerance permits guessed semantics, weakened proof, product edits, or scope expansion. |
| completion_review_owner_and_handoff | doer-main publishes HANDOFF-VERIFICATION-ASSET to ROOT-IM and terminates. ROOT-IM inspects the frozen tip and separately dispatches MI-CANDIDATE-EVIDENCE through EDGE-003G for reviewer-main plus a new doer-main deterministic-check run. |
| failure_classification_and_routes | A still-valid strict asset failure returns through EDGE-006V only after ROOT-IM classification. A product/API need or ambiguous expected behavior returns immediately to ROOT-IM and may enter M02 only with separate material evidence. Administrative faults follow P09; Firmware-owned assets return to the suite. |
| thread_resume_and_terminal_rule | Every reusable M03 doer-main card terminates at HANDOFF-VERIFICATION-ASSET. A corrected card may request the same mapped role or available provider continuity only after ROOT-IM issues a new exact dispatch; continuity is optional. No invocation crosses into M04, acceptance, or M06 integration. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P05, P07, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One frozen verification-only tip, exact authorized-path diff, terminal self-check facts, and HANDOFF-VERIFICATION-ASSET for ROOT-IM. MI-CANDIDATE-EVIDENCE receives it only through a later EDGE-003G dispatch.

#### Concurrency and isolation

One doer-main invocation owns one identified verification worktree. It does not overlap a product writer or another source writer on the same tip. Later M04 review/check paths consume the frozen tip read-only with disjoint roots.

#### Resources and side effects

Only the declared verification worktree and unique bounded-result paths are mutable. No Firmware, MCP, provider-tool, network, or hardware resource is touched.

#### Checks and acceptance

Card-local self-checks must pass before publication. MI-CANDIDATE-EVIDENCE independently runs CHECK-VERIFICATION-ASSET and the applicable repair check/review; ROOT-IM alone accepts the joined result in MI-CANDIDATE-DECIDE.

#### Failure and exception routes

A strict verification-only defect returns through EDGE-006V. A product/API need, semantic ambiguity, scope conflict, or suite-owned fault returns to ROOT-IM for the correct owner and never widens M03. Administrative faults follow P09. No exception applies.

#### Prior results and change effects

Preserve all product and evidence credit outside the changed verification paths and their direct consumers. On EDGE-003V, the originating repair tip remains frozen while only its verification-asset and evidence consumers are added or invalidated.

#### Repeat, join, and terminal behavior

Success takes EDGE-003G into the existing candidate evidence/decision/integration lifecycle. One complete strict test-only pool may return through EDGE-006V to the same logical M03 task. Every asset and M04 evidence invocation stops at ROOT-IM; only an accepted evidence verdict permits a separate M06 doer-main card.

#### Cost and critical-path effect

Expected 5-20 minutes plus branch-specific M04 evidence. The branch is free when trusted assets suffice and prevents ROOT-IM, coder-main, or Firmware workers from absorbing verification-authoring work during future loopbacks.

### MI-ATTENTION-PRACTICAL-CORRECT - M03: Correct the stale attention practical, retention unit, and guide

#### Purpose

Restore the accumulated safeguard's only attention-retention oracle by removing its obsolete policy-helper exercise and replacing only its removed diagnostic-watch manager-wake scenario with a current host-adapter wake/quiet proof, while making the retention unit and guide describe that actual behavior and leaving production code unchanged.

#### Coverage

The attention-practical portion of REQ-A01 and no product requirement beyond it.

#### Selection basis

The safeguard failure was strict test/docs-only. An accepted product oracle required the former policy API to remain absent. The first M03 attempt proved that removing that import exposed a second obsolete asset contract: the practical and its retention unit called removed diagnostic-watch manager flags and required retired `MANAGER_WAKE_*` evidence that current production cannot emit. The corrected writer then completed the coherent three-file replacement and passed its practical, removed-policy, and compile checks. Its only block was the independently reproduced stale packaged-asset manifest routed through EDGE-009P; the accepted repaired retry reused the preserved exact diff and existing proof contract instead of redesigning or re-authoring the change.

#### Owner and roles

ROOT-IM owns the explicit proof contract and semantic classification: it names current sparse adapter delivery, pending-work preservation, empty-queue quiet behavior, preservation of unrelated practical checks, removed-policy and removed diagnostic-watch wake absence, truthful-guide target, three-file scope, no-product-edit boundary, strict test-only classification, and acceptance decision. doer-main owns one independent verification-asset worktree and chooses/implements the smallest concrete practical/unit/guide changes and focused commands that prove every named target, including the mandatory retained and current-product oracles. reviewer-main later performs the independent `VERIFICATION_ASSET` review inside MI-CANDIDATE-EVIDENCE.

#### Preconditions

Initial entry used EDGE-009T at clean canonical `c114d3f074de01918c1753ea3583431df79f005c`. The accepted retry used EDGE-007T after the one-field manifest repair was accepted and integrated and its package/install and S4 wake/idle oracles passed. ROOT-IM issued a fresh doer-main card rooted at that repaired canonical coordinate; the corrected writer's valid earlier `BLOCKED` result, exact verified three-file diff, proof contract, final reviewer pass, intentional API-removal oracle, and unaffected safeguard green credit were preserved.

#### Inputs

The three declared verification paths, preserved exact verified diff, corrected writer's blocked dependency trace, exact current S4 host-delivery oracles, exact removed-policy oracle, final safeguard failure, repaired canonical parent carried by EDGE-007T, and P02 bounded-command contract. No product source, manifest, release registry, Firmware path, MCP process, or hardware resource is an editable input.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-ATTENTION-PRACTICAL-CORRECT; MI-ATTENTION-PRACTICAL-CORRECT; DEL-RELEASE-ASSURANCE; attention-verification; GATE-CANDIDATE; LOOP-ATTENTION-ASSET |
| workflow_role | doer-main |
| objective | Produce one clean three-file verification-asset descendant that proves current host-adapter wake/quiet, removed-policy/obsolete-wake absence, preserved unrelated practical behavior, and guide truthfulness without changing product code. |
| why_now | The accumulated safeguard could not decide REQ-A01 because its required practical imported APIs that accepted product behavior intentionally removed. This verification-only correction is now accepted and integrated. |
| starting_state | Clean repaired canonical parent supplied by EDGE-007T; final reviewer PASS remains valid; safeguard green credit through synthetic cleanup is preserved; only the attention-practical criterion is indeterminate. |
| dependencies_and_predecessor_outputs | EDGE-007T for the accepted retry, the exact safeguard failure, the corrected writer's valid earlier `BLOCKED` result/dependency trace and preserved exact diff, accepted `test_FC5_removed_policy_has_no_live_output_surface`, passing exact current S4 wake tests after the manifest repair, and the retained practical/unit/guide triplet. Initial entry history remains EDGE-009T. |
| working_scope | Write only `harness_watcher_implementation/tests/run_attention_practical.py`, `harness_watcher_implementation/tests/test_attention_practical_retention.py`, and `harness_watcher_implementation/ATTENTION_LOGGING.md`. In the practical, remove the retired attention-sprint policy block and replace only `production_wake_smoke`'s obsolete diagnostic-watch manager-flag/output route with the smallest host-only use of current public host-delivery/Codex synthetic seams. Update the retention unit to assert that current evidence. Correct the guide's obsolete blocking-watch and sprint-boundary claims. Preserve every unrelated practical analysis scenario and its terminal PASS marker. |
| required_behavior | The wake case admits one actionable event, produces one sparse notice with no event payload/ID, records a delivered boundary receipt, leaves the event pending until explicit acknowledgement, and records the current synthetic transport boundary. The quiet case begins from a fresh empty queue/coordinator and proves no notice and no transport call. The practical's unrelated deadline, continuity, classification, validation, disabled-gate, and PASS-marker checks remain. The guide points to the practical and distinguishes current host-adapter delivery from the historical attention-timeline decoder. No removed helper, removed manager CLI flag, or retired diagnostic-watch wake output is called or advertised, and no production API is restored. doer-main chooses the concrete three-file implementation and focused commands needed to prove these targets. |
| initial_entrypoints | Final safeguard attention failure; first M03 dependency trace; practical; retention unit; guide; exact current S4 and removed-policy oracles (count 6). This is the minimum context that proves both stale surfaces and the accepted replacement behavior. |
| failure_case_brief | REQ-A01 trigger: deleting too much could weaken unrelated attention analysis or turn the replacement into a fabricated wake; the retained unit plus exact current product oracles decide it. Quiet trigger: reusing the wake queue could hide a spurious notice; the fresh-empty-queue assertion decides it. Accepted-removal trigger: restoring or continuing to call retired policy/diagnostic-watch wake behavior contradicts the product contract; the removed-policy oracle and literal scans decide it. Documentation trigger: the guide could still promise removed behavior; focused scans plus independent review decide it. ROOT-IM owns classification. |
| ordered_actions | M03-A1: bind EDGE-007T, the corrected writer's blocked facts, and current product oracles; M03-A2: verify the preserved exact three-file diff still applies cleanly to the repaired canonical coordinate and still matches the proof contract; M03-A3: apply that diff without redesign, changing it only if the repaired base creates a concrete conflict that ROOT-IM has classified; M03-A4: confirm only the three verification assets changed and unrelated practical checks remain; M03-A5: run CHECK-ATTENTION-PRACTICAL without external resources; M03-A6: inspect exact scope, current-oracle fidelity, unrelated-check preservation, and no product/API/manifest edit; M03-A7: publish one clean asset tip and HANDOFF-ATTENTION-ASSET. |
| allowed_tools_capabilities_resources | Read/write the declared verification worktree and three paths; read candidate tests/product contract; use current public host-delivery/Codex synthetic seams from the verification code; run Git read-only checks and P02-supervised Python checks. |
| forbidden_actions_and_boundaries | No edits outside the three declared paths; no production/API/configuration/release-registry change; no restoration of manager flags or `MANAGER_WAKE_*` diagnostic-watch output; no new test framework, wrapper, fixture, dependency, or safeguard command; no MCP, network, Firmware, WSL, provider-tool, or hardware action. |
| verification | Run CHECK-ATTENTION-PRACTICAL's mandatory retained practical, exact current S4 wake pair, removed-policy, compile, literal stale/obsolete-claim scans, scope, and whitespace checks. doer-main may add only the smallest focused command needed to prove a ROOT-IM-named target; it reports any need to change the target, protected surface, or classification. Use the calibrated bounds in CHECK-ATTENTION-PRACTICAL and a unique P02 result path per covered command. Literal searches and Git diff/status/whitespace checks are read-only shell operations. |
| deliverables_and_result_paths | One clean descendant commit, exact three-file diff, unique bounded self-check results, and HANDOFF-ATTENTION-ASSET at the lane's declared result path. |
| acceptance_criteria_and_tolerances | Exactly the three declared paths change; all CHECK-ATTENTION-PRACTICAL checks pass; current sparse delivery/pending/quiet assertions are strong and match existing product oracles; unrelated practical checks and the terminal PASS marker remain; the five stale helper names and removed manager flags are absent from all three assets; the guide contains no retired diagnostic-watch wake promise; no product source/API/configuration changes. No tolerance permits a fabricated event, reused quiet queue, weaker unrelated analysis, or product restoration. |
| completion_review_owner_and_handoff | doer-main publishes HANDOFF-ATTENTION-ASSET to ROOT-IM and terminates. ROOT-IM inspects the frozen tip and separately dispatches MI-CANDIDATE-EVIDENCE for reviewer-main plus a new doer-main deterministic-check run; ROOT-IM later decides in MI-CANDIDATE-DECIDE. |
| failure_classification_and_routes | Asset/self-check failure remains strict test-only and returns through EDGE-006T only after MI-CANDIDATE-DECIDE; product/API need or ambiguous expected behavior returns immediately to ROOT-IM; runner/report/timeout fault follows P09; no result enters MI-HARNESS-REPAIR without separate product evidence. |
| thread_resume_and_terminal_rule | Keep the same logical M03 task and complete asset pool. Its doer-main run terminates after HANDOFF-ATTENTION-ASSET. A later strict test-only correction receives a new doer-main invocation and correlated handoff only after ROOT-IM issues the return command. Plan-wide, the same mapped doer-main role owns every selected M03 verification-asset implementation, every M04 deterministic test/check path, and every separately authorized M06 integration execution; each card is terminal at ROOT-IM, available continuity is optional, and no run emits its own successor. Acceptance makes the M03 task terminal. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P05, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One clean verification-asset tip changing only the practical, retention unit, and guide, its exact affected self-check results, and HANDOFF-ATTENTION-ASSET for MI-CANDIDATE-EVIDENCE.

#### Concurrency and isolation

One doer-main invocation writes one identified worktree. No peer writer or shared mutable result root exists. After publication, MI-CANDIDATE-EVIDENCE uses the frozen tip read-only and gives reviewer/checker disjoint roots.

#### Resources and side effects

Only the identified verification worktree and unique bounded-result paths are mutable. The task launches no provider beyond its lane-managed author session, no MCP/server process, and no external or hardware resource.

#### Checks and acceptance

CHECK-ATTENTION-PRACTICAL must pass before publication. MI-CANDIDATE-EVIDENCE then repeats that check independently and reviews exact scope, fidelity to current adapter delivery/quiet behavior, preservation of unrelated practical assertions, accepted removed-policy and removed diagnostic-watch consistency, and guide truthfulness. ROOT-IM accepts only the joined result.

#### Failure and exception routes

A strict test-only defect returns through EDGE-006T. A production/API need, semantic ambiguity, or weakened oracle returns to ROOT-IM classification and cannot be solved inside M03. Administrative faults follow P09. No exception applies.

#### Prior results and change effects

Preserve the final reviewer pass, safeguard stages before attention, accepted product/API-removal credit, and every earlier integration. This task invalidates only the attention-practical result and consumers of the incomplete final assurance. It does not invalidate product-source review or affected product checks.

#### Repeat, join, and terminal behavior

Success takes EDGE-003T into the existing candidate evidence/decision/integration lifecycle. One complete strict test-only pool may return through EDGE-006T to the same logical task. The earlier packaged-asset repair uses EDGE-007T only once to re-enter this task; after the accepted three-file integration, EDGE-007 repeats final assurance once. No intermediate revision is reviewed.

#### Cost and critical-path effect

Expected 8-18 minutes for authoring and self-checks, plus 8-15 minutes for affected evidence/integration. The narrow route adds one necessary verification writer but reuses current public seams, existing product oracles, and every existing gate; it avoids restoring retired product machinery or repeating unaffected producer work.

### MI-CANDIDATE-EVIDENCE - M04: Focused candidate review and affected checks

#### Purpose

Run the selected evidence path for one frozen retirement, repair, format, current attention-asset, or reusable verification-asset tip, then publish one complete result set.

#### Coverage

REQ-R01, REQ-R02, REQ-R03, REQ-A02, REQ-A03, REQ-A04, the attention-practical portion of REQ-A01, and any requirement explicitly invalidated by MI-HARNESS-REPAIR, MI-SAFEGUARD-CHECKPOINT-CORRECT, or an active MI-VERIFICATION-ASSET-CORRECT proof contract.

#### Selection basis

Removal, material repair, and verification-asset corrections need independent review plus checks; formatting needs exact deterministic reproduction plus checks. One branch-selected campaign reuses their frozen-input, result, decision, and integration lifecycle without pretending that every branch needs the same review class.

#### Owner and roles

ROOT-IM owns campaign assembly, proof-contract targets/protected surfaces/classification, worker dispatch, and result acceptance. Plan-wide, doer-main chooses the smallest concrete deterministic test/check implementation that proves that contract, executes mandatory named plan checks, and publishes facts only. On EDGE-003 it begins only after ROOT-IM receives coder-main's terminal repair handoff; on EDGE-003T or EDGE-003G it begins only after ROOT-IM receives the applicable terminal M03 asset handoff. reviewer-main performs read-only review on EDGE-002, EDGE-003, EDGE-003T, or EDGE-003G; EDGE-003F has no reviewer session.

#### Preconditions

EDGE-002, EDGE-003, EDGE-003F, EDGE-003T, or EDGE-003G supplies exactly one frozen candidate tip and its matching terminal writer handoff; ROOT-IM has issued the separate evidence dispatch and exact proof contract.

#### Inputs

Frozen candidate plus exactly one active branch input: ROOT-IM retention directive and writer trace; admitted repair pool and writer trace; declared source-conformance parent and HANDOFF-RELEASE-FORMAT; current attention contract and HANDOFF-ATTENTION-ASSET; or reusable asset contract and HANDOFF-VERIFICATION-ASSET, including HANDOFF-REPAIR when EDGE-003V originated it. Include the selected check, check process-tree ID, and separate roots; reviewer invocation/process ID exists on every branch except EDGE-003F.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-CANDIDATE-EVIDENCE; MI-CANDIDATE-EVIDENCE; EDGE-002 uses DEL-CAMPAIGN-RETIREMENT, EDGE-003 carries the admitted affected deliverable, EDGE-003F uses DEL-RELEASE-FORMAT, EDGE-003T uses DEL-RELEASE-ASSURANCE, and EDGE-003G carries the originating active deliverable; candidate-evidence; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR, LOOP-ATTENTION-ASSET, or LOOP-VERIFICATION-ASSET |
| workflow_role | doer-main concrete test/check selector and executor on every branch; reviewer-main on EDGE-002, EDGE-003, EDGE-003T, or EDGE-003G; ROOT-IM proof-contract, dispatch, and acceptance owner. Any verification-asset source edit occurs only in a separately selected M03 doer-main card before this frozen-input M04 card. |
| objective | Produce one complete branch-appropriate evidence result for the frozen candidate. |
| why_now | A writer tip exists and must be independently assessed before integration. |
| starting_state | One declared frozen tip, matching writer handoff, check process-tree ID, and disjoint roots; reviewer invocation ID exists on every branch except EDGE-003F. |
| dependencies_and_predecessor_outputs | EDGE-002, EDGE-003, EDGE-003F, EDGE-003T, or EDGE-003G and the exact branch handoff. |
| working_scope | EDGE-002 covers the retention directive and affected compatibility. EDGE-003 covers only the admitted repair invariant, changed harness seam, focused oracle, and previously violated review invariant. EDGE-003F covers only deterministic normalization/formatter conformance. EDGE-003T covers only the exact attention three-file contract and CHECK-ATTENTION-PRACTICAL. EDGE-003G covers only ROOT-IM's exact reusable asset contract; when EDGE-003V originated it, include the admitted repair seam and invariant without adding another product objective. Never mix branches or mutate the frozen candidate. |
| required_behavior | On EDGE-002, review directive fidelity and run affected checks. On EDGE-003, review the admitted repair and run CHECK-CANDIDATE-REPAIR. On EDGE-003F, reproduce and run CHECK-RELEASE-FORMAT without reviewer-main. On EDGE-003T, launch `VERIFICATION_ASSET` review and CHECK-ATTENTION-PRACTICAL together. On EDGE-003G, launch CHECK-VERIFICATION-ASSET with one `VERIFICATION_ASSET` review for a strict test-only origin or one `AFFECTED_REPAIR_WITH_ASSET` review plus CHECK-CANDIDATE-REPAIR when EDGE-003V originated the asset. |
| initial_entrypoints | EDGE-002 count 6; EDGE-003 count 5; EDGE-003F count 6; EDGE-003T count 5 as declared above. EDGE-003G: exact proof contract; verification diff; accepted expected-behavior evidence; protected surfaces; mandatory checks; originating repair handoff when applicable (maximum count 6). The active edge chooses one set only. |
| failure_case_brief | On EDGE-003G originating from EDGE-010R, the repair may mirror its oracle, reclaim an uncertain claim, discard a checkpoint during invocation replacement, cancel later cases after one failure, or touch a hardware/tool seam. Independent review plus CHECK-SPRINT-CONTINUATION and CHECK-CANDIDATE-REPAIR decide those risks; other branches retain their existing briefs. |
| ordered_actions | M04-A1: verify one frozen input and active edge; M04-A2: enumerate every feasible independent review/check path before awaiting any result; M04-A3: on EDGE-002/003/003T launch every feasible independent review and check with disjoint roots, or on EDGE-003F run only deterministic reproduction/checks; M04-A4: complete assigned surfaces even when an ordinary peer failure is already known, unless a named prerequisite or P15 containment blocks one; M04-A5: preserve path results; M04-A6: join/deduplicate once when multiple paths exist; M04-A7: publish complete set to M05; M04-A8: after changed input, repeat only the failed, unresolved, affected, or uncertain branch-local surface from its earliest required unit. |
| allowed_tools_capabilities_resources | Read-only review tools, affected deterministic checks, and P02 supervisor for covered commands. |
| forbidden_actions_and_boundaries | No product edits, no full generic campaign without changed-input reason, no hardware, and no early repair. |
| verification | Run the active branch's declared checks. For EDGE-003G originating from EDGE-010R, CHECK-SPRINT-CONTINUATION and CHECK-CANDIDATE-REPAIR are mandatory; execute all four feasible continuation cases after ordinary failure and verify zero forbidden events/exact cleanup. |
| deliverables_and_result_paths | One complete candidate result set; review/check paths remain separate when present. |
| acceptance_criteria_and_tolerances | Every active path returns terminal facts on one frozen tip. The current continuation branch requires all four cases and focused affected checks PASS, no material review finding, zero tool/hardware events, exact cleanup, exact authorized paths, and no second recovery mechanism. |
| completion_review_owner_and_handoff | ROOT-IM receives the complete pool through MI-CANDIDATE-DECIDE. |
| failure_classification_and_routes | Result/report fault goes P09; material candidate fact goes MI-CANDIDATE-DECIDE; no local repair. |
| thread_resume_and_terminal_rule | The doer-main check run and reviewer run each terminate after publishing HANDOFF-CANDIDATE-EVIDENCE. ROOT-IM decides that complete pool before issuing any new card. A later doer-main integration run receives the frozen tip, authorization, and first unresolved action from that decision; it may use available continuity but never continues a still-running evidence invocation. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P05, P06, P07, P09, P10, P13, P15; no exception. |

#### Outputs and results

One complete branch-local evidence pool bound to one frozen candidate and published to MI-CANDIDATE-DECIDE.

#### Concurrency and isolation

On EDGE-002, EDGE-003, EDGE-003T, or EDGE-003G, PG-CANDIDATE launches review and deterministic checking together with separate writable roots. On EDGE-003F, one deterministic path mutates only its disposable reproduction root. The frozen candidate remains read-only.

#### Resources and side effects

Only result/cache roots and the EDGE-003F disposable reproduction root are mutable. No claim/lock is needed because the candidate is read-only and the reproduction root has one owner.

#### Checks and acceptance

EDGE-002 uses CHECK-CANDIDATE-AFFECTED, EDGE-003 uses CHECK-CANDIDATE-REPAIR, EDGE-003F uses CHECK-RELEASE-FORMAT, EDGE-003T uses CHECK-ATTENTION-PRACTICAL, and EDGE-003G uses CHECK-VERIFICATION-ASSET plus the repair check when applicable. ROOT-IM decides the complete result in MI-CANDIDATE-DECIDE.

#### Failure and exception routes

Support/report faults are isolated by P09. A genuine product finding is not repaired until ROOT-IM has pooled and admitted it.

#### Prior results and change effects

Earlier accepted results remain green unless the changed source, test semantics, or consumed compatibility surface affects them.

#### Repeat, join, and terminal behavior

One terminal evidence set goes to GATE-CANDIDATE. A retirement finding distinguishes semantic directive from implementation; a repair repeat covers only changed seams; a format repeat covers deterministic conformance; the current attention repeat returns through EDGE-006T; every reusable verification-asset repeat returns through EDGE-006V while strict eligibility remains true.

#### Cost and critical-path effect

Expected 8-20 minutes on review branches and 5-15 minutes on the deterministic format branch; each uses the cheapest decisive oracle before integration.

### MI-CANDIDATE-DECIDE - M05: Candidate semantic decision and correction routing

#### Purpose

Classify the complete candidate evidence pool and issue one semantic verdict or one exact correction route.

#### Coverage

REQ-R01, REQ-R02, REQ-R03, REQ-A02, REQ-A03, REQ-A04, and any affected generic requirement from MI-HARNESS-REPAIR, MI-SAFEGUARD-CHECKPOINT-CORRECT, or MI-VERIFICATION-ASSET-CORRECT.

#### Selection basis

Retirement, later admitted-repair, deterministic release-format, and current or reusable verification-asset results each need one ROOT-IM decision before integration; one edge-selected decision module prevents ad hoc repair, mixed branch scope, and broad reruns.

#### Owner and roles

ROOT-IM alone decides; no product writer runs inside this module.

#### Preconditions

EDGE-004 supplies the complete MI-CANDIDATE-EVIDENCE pool.

#### Inputs

Gate question, candidate tip, complete evidence pool, the active branch's retention directive, admitted repair pool, declared source-normalization/format contract, or exact verification-asset proof contract, matching writer handoff, and preserved credit.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-CANDIDATE-DECIDE; MI-CANDIDATE-DECIDE; EDGE-002 uses DEL-CAMPAIGN-RETIREMENT, EDGE-003 carries the admitted affected deliverable, EDGE-003F uses DEL-RELEASE-FORMAT, EDGE-003T uses DEL-RELEASE-ASSURANCE, and EDGE-003G carries the originating active deliverable; candidate-decision; GATE-CANDIDATE; LOOP-CANDIDATE-REPAIR, LOOP-ATTENTION-ASSET, or LOOP-VERIFICATION-ASSET |
| workflow_role | ROOT-IM decision owner; no provider session or mapping resolution |
| objective | Decide the active EDGE-002 retirement, EDGE-003 affected-repair (including checkpoint-safeguard correction), EDGE-003F release-format, EDGE-003T attention-asset, or EDGE-003G reusable verification-asset claim without importing another branch's scope. |
| why_now | The candidate evidence campaign has produced its complete joined result. |
| starting_state | One frozen candidate, exactly one active branch input (ROOT-IM retention directive, admitted repair pool, declared source-normalization/format contract, current attention contract, or reusable verification-asset contract), matching writer trace, complete evidence pool, and prior accepted generic credit. |
| dependencies_and_predecessor_outputs | EDGE-004 from MI-CANDIDATE-EVIDENCE. |
| working_scope | Classification, verdict, credit calculation, and declared correction routes for the one edge that produced the evidence pool; no source edits and no retirement re-review during an EDGE-003 repair repeat. |
| required_behavior | Pool once, distinguish material, strict test-only, and administrative facts, and issue one verdict. |
| initial_entrypoints | Active branch's candidate evidence pool; its directive or admitted repair pool; affected requirement rows; candidate diff; prior verdicts (count 5). The inactive branch is not an entrypoint. |
| failure_case_brief | The active requirement may be decided while one check is support-faulted; oracle is the remaining independent product evidence, and ROOT-IM determines only branch-local invalidation. |
| ordered_actions | M05-A1: validate result shape; M05-A2: pool and deduplicate findings; M05-A3: classify every follow-up; M05-A4: decide product impact of test/support faults; M05-A5: assess the exact required behavior; M05-A6: compute preserved and invalidated credit; M05-A7: for material product work, name the failed behavior, responsible seam, protected surfaces, and oracle, then return the complete pool once to the originating M02 coder-main task; after its terminal handoff choose EDGE-003 when trusted assets suffice or EDGE-003V when an asset edit is required; EDGE-006F remains source conformance; M05-A8: for strict test-only work, the current attention asset returns through EDGE-006T and every reusable asset returns or first activates through EDGE-006V after ROOT-IM names its exact proof contract; M05-A9: recover only consumed administrative facts; M05-A10: issue one verdict and, on acceptance only, a separate integration authorization. |
| allowed_tools_capabilities_resources | Read-only result inspection, requirement/diff review, and ROOT-IM decision authority. |
| forbidden_actions_and_boundaries | No source repair, no unpooled return, no full rerun without changed input, and no external-suite launch. |
| verification | Evidence-pool completeness, requirement mapping, and GATE-CANDIDATE classification. |
| deliverables_and_result_paths | One verdict and HANDOFF-REPAIR only if material continuation changes writer invocation. |
| acceptance_criteria_and_tolerances | On EDGE-002, ACCEPTED requires REQ-R01 through REQ-R03 decided; on EDGE-003, the admitted repair behavior and protected surfaces; on EDGE-003F, exact REQ-A02 conformance; on EDGE-003T, the exact attention contract; on EDGE-003G, every ROOT-IM-named behavior/goal, protected surface, authorized path, no-product-edit criterion, and originating repair invariant when applicable. Any tolerance requires explicit user-authorized product rationale. |
| completion_review_owner_and_handoff | On acceptance, ROOT-IM publishes the explicit new CARD-CANDIDATE-INTEGRATE authorization and activates EDGE-005. It returns retirement material through EDGE-006A, ordinary repair material through EDGE-006B, checkpoint-safeguard material through EDGE-006E, source-conformance material through EDGE-006F, current attention material through EDGE-006T, or reusable verification-asset material through EDGE-006V. |
| failure_classification_and_routes | Retirement implementation material returns to MI-CAMPAIGN-RETIRE; later ordinary product repair material returns to MI-HARNESS-REPAIR; checkpoint-safeguard executor material returns to MI-SAFEGUARD-CHECKPOINT-CORRECT; source conformance returns to MI-RELEASE-FORMAT-CORRECT; current attention returns to MI-ATTENTION-PRACTICAL-CORRECT; reusable verification-only material returns to MI-VERIFICATION-ASSET-CORRECT; test/support follows P08/P09; an indeterminate required claim is CONTINUE or INCOMPLETE under P10. |
| thread_resume_and_terminal_rule | Decision task is terminal on verdict. Material continuity belongs to the originating M02 logical task: a material return resumes its idle coder-main provider session by default under a new ROOT card, or uses correlated replacement if resume is unavailable or remapped. An accepted GATE-CANDIDATE verdict retires that coder session. Every coder-main card and every M03/M04 doer-main invocation terminates back at ROOT-IM; only acceptance permits the separate M06 integration card. |
| cited_global_policy_ids_and_exception_ids | P01, P04, P07, P08, P09, P10, P13, P15; no exception. |

#### Outputs and results

One `ACCEPTED`, `ACCEPT-WITHIN-TOLERANCE`, `CONTINUE`, or `INCOMPLETE` result with exact preserved and invalidated credit.

#### Concurrency and isolation

Decision is serial after the one candidate join. It writes no source or external resources.

#### Resources and side effects

No lock beyond runtime correlation is required; decision records are retained only for their named consumers.

#### Checks and acceptance

GATE-CANDIDATE is satisfied only when every finding has one disposition and no material pool is fragmented.

#### Failure and exception routes

Administrative facts use P09. A new graph, authority, or undefined ownership is `INCOMPLETE` or an amendment, never local invention.

#### Prior results and change effects

Retain accepted generic candidate credit outside explicit changed dependencies. EDGE-006A, EDGE-006B, EDGE-006E, EDGE-006F, EDGE-006T, or EDGE-006V invalidates only the active candidate evidence path.

#### Repeat, join, and terminal behavior

After ROOT-IM publishes the new integration authorization, EDGE-005 default-forwards an accepted tip to the separately dispatched integration card. EDGE-006A returns retirement material; EDGE-006B returns ordinary product repair material; EDGE-006E returns checkpoint-safeguard material; EDGE-006F returns source conformance; EDGE-006T returns the current attention asset; EDGE-006V returns reusable verification-only material to its same logical M03 task.

#### Cost and critical-path effect

Expected 5-10 minutes; one decision replaces multiple repair/review cycles.

### MI-CANDIDATE-INTEGRATE - M06: Integrate an accepted candidate change

#### Purpose

Integrate an accepted retirement, ordinary repair, checkpoint-safeguard repair, mechanical source-conformance, or verification-asset tip into the candidate coordinate, run branch-appropriate post-join checks, retain rollback state, and expose one integrated input to release assurance.

#### Coverage

REQ-R01 through REQ-R03, REQ-A01 through REQ-A04, and any accepted harness repair claim.

#### Selection basis

One integration boundary is required between accepted writer output and accumulated assurance; it also keeps repair integration narrow.

#### Owner and roles

ROOT-IM authorizes the exact accepted integration, retains conflict classification and acceptance, and doer-main executes only the declared fast-forward/readback and post-join commands. No executor resolves a conflict or edits source during integration.

#### Preconditions

EDGE-005 supplies an M05-accepted candidate tip, its verdict, and ROOT-IM's separate exact integration authorization.

#### Inputs

Accepted tip, decision verdict, ROOT-IM integration authorization, destination worktree ID, rollback base, changed dependency domains, and post-join check selection.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-CANDIDATE-INTEGRATE; MI-CANDIDATE-INTEGRATE; EDGE-005 carries DEL-CAMPAIGN-RETIREMENT after EDGE-002, the admitted affected deliverable after EDGE-003, DEL-RELEASE-FORMAT after EDGE-003F, DEL-RELEASE-ASSURANCE after EDGE-003T, or the originating active deliverable after EDGE-003G; integration; GATE-INTEGRATION; no-loop |
| workflow_role | doer-main integration executor; ROOT-IM operation authority and conflict classifier |
| objective | Integrate exactly one accepted candidate change and publish a read-back integrated coordinate. |
| why_now | MI-CANDIDATE-DECIDE accepted the source tip and ROOT-IM issued this new exact integration card. |
| starting_state | Terminal HANDOFF-CANDIDATE-EVIDENCE, accepted candidate tip, ROOT-IM integration authorization, clean destination, rollback base, and a new integration process ID. |
| dependencies_and_predecessor_outputs | EDGE-005, accepted candidate verdict, and ROOT-IM integration authorization. |
| working_scope | Declared destination coordinate and affected post-join checks; no new product scope. |
| required_behavior | Join accepted input in order, verify destination state, and preserve rollback before retirement. |
| initial_entrypoints | ROOT-IM integration authorization; accepted verdict; candidate diff; destination status; affected checks; rollback base. Count 6 because the new authorization prevents a test/check run from self-starting this operation. |
| failure_case_brief | Destination mismatch is an operation failure; readback is the oracle; ROOT-IM owns recovery. |
| ordered_actions | M06-A1: revalidate accepted input; M06-A2: verify destination and rollback base; M06-A3: integrate serially; M06-A4: inspect combined diff and affected checks; M06-A5: publish integrated coordinate; M06-A6: omit promotion here; M06-A7: retain rollback and results; M06-A8: retire only clean terminal temporary state. |
| allowed_tools_capabilities_resources | Git integration/readback, affected checks, and P02 supervisor for covered commands. |
| forbidden_actions_and_boundaries | No promotion, no broad release check, no hardware, and no deletion of dirty/live state. |
| verification | Perform exact authorized fast-forward/readback and branch post-join checks. For the EDGE-010R descendant, rerun the focused deterministic CHECK-SPRINT-CONTINUATION smoke before returning to ROOT; affected M08 later repeats the exact-target fake-runtime proof. |
| deliverables_and_result_paths | Integrated coordinate and post-join result for MI-RELEASE-ASSURE. |
| acceptance_criteria_and_tolerances | Destination equals accepted input with affected checks decided; no tolerance for unverified merge. |
| completion_review_owner_and_handoff | doer-main publishes HANDOFF-CANDIDATE-INTEGRATE and terminates. ROOT-IM activated EDGE-007L after the historical accepted format integration because REQ-A03 was then open; activated EDGE-007T after the accepted packaged-asset manifest repair so the preserved M03 change could be retried; activates EDGE-007E after the accepted `stable_io.py` integration because REQ-A04 is now open; and activates EDGE-007 only after the checkpoint-safeguard correction, REQ-A03, and any required verification integration are accepted. |
| failure_classification_and_routes | Integration mechanics use GATE-INTEGRATION; a product regression returns through M05 classification. |
| thread_resume_and_terminal_rule | This separately dispatched doer-main integration run terminates at HANDOFF-CANDIDATE-INTEGRATE. After an interruption, ROOT-IM may issue a new integration card for only the first unresolved operation; accepted source verdict remains preserved. Available continuity from the terminal evidence run is optional and never a prerequisite. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P09, P10, P13, P15; no exception. |

#### Outputs and results

One integrated candidate coordinate, retained rollback base, and required post-join check facts.

#### Concurrency and isolation

Integration is serial because it mutates one destination. Read-only checks use separate roots.

#### Resources and side effects

The destination worktree and rollback base are the only source resources. Temporary lanes close only when clean and unclaimed.

#### Checks and acceptance

Affected post-join checks decide the integration seam. MI-RELEASE-ASSURE consumes only an integrated coordinate.

#### Failure and exception routes

GATE-INTEGRATION blocks only this coordinate operation. A proven product regression returns to its owning M05 classification route.

#### Prior results and change effects

Accepted writer result is retained. Only integration-dependent assurance must rerun after a new repair input.

#### Repeat, join, and terminal behavior

The historical accepted format integration took EDGE-007L, accepted REQ-A03 integration then took EDGE-007, the accepted packaged-asset repair took EDGE-007T exactly once, and accepted attention-asset integration then took EDGE-007. Any interrupted future integration resumes at the first unresolved M06 action and never reopens accepted source behavior by itself.

#### Cost and critical-path effect

Expected 5-15 minutes; one serial join is necessary before a single final assurance run.

### MI-RELEASE-ASSURE - M07: Final generic-harness assurance

#### Purpose

Run one independent final review and one checkpointed accumulated generic-harness safeguard over the integrated release unit after the explicit release-lint contract and checkpoint-safeguard correction are accepted and integrated.

#### Coverage

REQ-A01, REQ-A04, and OUT-003.

#### Selection basis

The safeguard's existing coarse checks remain proportionate release evidence, but its old fail-fast/restart behavior does not. One checkpointed final assurance run preserves the same oracle while retaining unaffected credit and collecting a complete feasible pool.

#### Owner and roles

ROOT-IM binds the release input and owns semantic acceptance; final-reviewer owns read-only review, and doer-main executes the separately bounded deterministic safeguard.

#### Preconditions

EDGE-007 supplies an integrated candidate and post-join facts after the checkpoint-safeguard correction is accepted and integrated.

#### Inputs

Integrated coordinate, accepted deliverable verdicts, changed paths/domains, consumed safeguard checkpoint, unresolved ledger, final review invocation/process ID, check process-tree ID, and isolated result roots.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-RELEASE-ASSURE; MI-RELEASE-ASSURE; DEL-RELEASE-ASSURANCE; final-assurance; GATE-RELEASE; LOOP-CANDIDATE-REPAIR, LOOP-ATTENTION-ASSET, or LOOP-VERIFICATION-ASSET |
| workflow_role | final-reviewer review executor; doer-main deterministic safeguard executor; ROOT-IM release-input and acceptance owner |
| objective | Decide accumulated generic-harness release behavior on one integrated candidate without repeating unchanged completed units. |
| why_now | Candidate integration has read back the active coordinate with REQ-A02 source conformance, REQ-A03 stable release lint, and REQ-A04 checkpointed safeguard behavior accepted. |
| starting_state | One integrated candidate, accepted inputs, consumed checkpoint state, final reviewer invocation ID, check process-tree ID, and disjoint roots. |
| dependencies_and_predecessor_outputs | EDGE-007 from MI-CANDIDATE-INTEGRATE. |
| working_scope | Accumulated generic product behavior and public surface; no campaign controller or hardware execution. |
| required_behavior | Run one final review and one checkpointed accumulated safeguard on the same release input, collect every feasible unit disposition, then join once. |
| initial_entrypoints | Integrated diff; accepted candidate verdict; changed paths/domains; prior checkpoint; candidate-owned `tools/Invoke-CandidateSafeguard.ps1`; candidate-owned release-check registry; public docs; unresolved ledger. Count 8 because they bind the release input, input invalidation, authoritative accumulated gate, public surface, and remaining decision constraints. |
| failure_case_brief | REQ-A01/REQ-A04: accumulated compatibility regression or stale credit; oracle is final review plus complete safeguard pool/input-map selection; ROOT-IM decides materiality. |
| ordered_actions | M07-A1: confirm declared release input and checkpoint applicability; M07-A2: compute failed/unresolved/affected/uncertain selected units from the conservative input maps and identify the earliest required member; M07-A3: launch independent final review and safeguard paths concurrently; M07-A4: review accumulated product only; M07-A5: execute every selected safeguard unit, continuing after ordinary failure unless a named prerequisite or P15 containment blocks it; M07-A6: join the final review with the complete unit pool; M07-A7: deduplicate/partition the final pool and send it to M05. |
| allowed_tools_capabilities_resources | Read-only final review, accumulated generic-harness check, and P02 supervisor for covered commands. |
| forbidden_actions_and_boundaries | No product edit, physical campaign, promotion, stale-PASS reuse, or duplicate unaffected safeguard unit. |
| verification | CHECK-RELEASE-ASSURANCE under PG-RELEASE: doer-main runs the exact candidate-owned `tools/Invoke-CandidateSafeguard.ps1 -Run` with explicit integrated repository root, observed branch, accepted tip, changed paths, and current checkpoint through P02. A cold run may use P11's 2,400-second expected upper bound plus 120-second cleanup, 2,520-second lifetime, and 30-second heartbeat; an incremental run uses the selected-unit expected total plus only `max(5, min(120, ceil(expected total * 0.25)))` cleanup. |
| deliverables_and_result_paths | One final joined review/checkpointed-unit pool for HANDOFF-RELEASE. |
| acceptance_criteria_and_tolerances | All selected paths decide the same release input; every feasible selected unit has a disposition; no tolerance for a fabricated pass or unexplained skip. |
| completion_review_owner_and_handoff | doer-main publishes HANDOFF-RELEASE-SAFEGUARD; ROOT-IM joins it with the independent final-review result in HANDOFF-RELEASE and routes that pool to MI-RELEASE-DECIDE. |
| failure_classification_and_routes | Material result returns only through MI-RELEASE-DECIDE; support result follows P09. |
| thread_resume_and_terminal_rule | The final-reviewer and doer-main safeguard paths are separate terminal runs. ROOT-IM joins their terminal handoffs before issuing a repair/test return. A repair/test loopback preserves only PASS units whose declared inputs/prerequisites are unchanged and starts a newly dispatched executor from the earliest failed/unresolved/affected/uncertain unit; it never restarts an unchanged prefix. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P05, P06, P07, P09, P10, P11, P13, P15; no exception. |

#### Outputs and results

One joined final-review/checkpointed-safeguard pool over the integrated release unit for MI-RELEASE-DECIDE.

#### Concurrency and isolation

PG-RELEASE launches the independent reviewer and safeguard before awaiting either, with separate result roots. The safeguard continues its independent selected units rather than allowing one ordinary failure to cancel later feasible units.

#### Resources and side effects

No source or hardware mutation. The check's temporary output is retained only while MI-RELEASE-DECIDE consumes it.

#### Checks and acceptance

CHECK-RELEASE-ASSURANCE supplies the final generic evidence. MI-RELEASE-DECIDE owns release semantic acceptance.

#### Failure and exception routes

Support faults do not fabricate a pass or hold independent product facts. Material findings are pooled by M05.

#### Prior results and change effects

Focused green credit and individual safeguard PASS credit remain valid only while their consumed inputs remain unchanged; a new integrated repair reruns only the failed, unresolved, affected, or uncertain units from the earliest required unit.

#### Repeat, join, and terminal behavior

One complete joined pool takes EDGE-008. ROOT-IM batches compatible admitted material findings through MI-HARNESS-REPAIR and returns only after the accepted batch integrates.

#### Cost and critical-path effect

Expected 35-45 minutes for a cold complete run with parallel review/check overlap; later runs cost only the selected incremental units. The cold 42-minute supervisor maximum is the measured 40-minute safeguard bound plus two minutes of cleanup, not an arbitrary wait.

### MI-RELEASE-DECIDE - M05: Final generic release verdict

#### Purpose

Classify final generic-harness assurance and unlock the external-suite admission boundary only after a valid release verdict.

#### Coverage

REQ-A01, REQ-A04, and OUT-003.

#### Selection basis

Final review/check results need one release decision that preserves green credit and does not confuse support failure with a product defect.

#### Owner and roles

ROOT-IM decides; no source mutation occurs here.

#### Preconditions

EDGE-008 supplies the complete final pool from MI-RELEASE-ASSURE.

#### Inputs

Integrated coordinate, final evidence pool, accepted prior results, unresolved ledger, and release-unit gate question.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-RELEASE-DECIDE; MI-RELEASE-DECIDE; DEL-RELEASE-ASSURANCE; final-decision; GATE-RELEASE; LOOP-CANDIDATE-REPAIR, LOOP-ATTENTION-ASSET, or LOOP-VERIFICATION-ASSET |
| workflow_role | ROOT-IM decision owner; no provider session or mapping resolution |
| objective | Issue the final generic release verdict and preserve the exact candidate eligible for external validation. |
| why_now | MI-RELEASE-ASSURE completed all selected final paths. |
| starting_state | Integrated release candidate, complete final pool, and accepted focused credit. |
| dependencies_and_predecessor_outputs | EDGE-008 from MI-RELEASE-ASSURE. |
| working_scope | Semantic release decision and declared repair route; no promotion or external allocation. |
| required_behavior | Distinguish material generic failure from support/process failure and issue exactly one verdict. |
| initial_entrypoints | Final result pool; integrated coordinate; acceptance requirements; unresolved ledger; affected prior results. Count 5 because all decide final credit. |
| failure_case_brief | REQ-A01: final check timeout without product evidence; oracle is remaining decisive evidence; ROOT-IM isolates support fault. |
| ordered_actions | M05-A1: validate final result shape; M05-A2: pool final findings; M05-A3: classify follow-ups; M05-A4: decide support/test product impact; M05-A5: assess the exact required release behavior; M05-A6: calculate invalidation; M05-A7: for material product work, name the complete repair contract and dispatch coder-main through MI-HARNESS-REPAIR; after its terminal handoff choose direct EDGE-003 evidence only when trusted assets suffice or EDGE-003V when an asset edit is required; M05-A8: for strict test-only work, ROOT-IM names the full proof contract and dispatches the current attention card through EDGE-009T or every later exact reusable M03 card through EDGE-009V; M05-A9: recover only consumed administrative fact; M05-A10: issue one release verdict and no worker successor directly. |
| allowed_tools_capabilities_resources | Read-only result and requirement inspection; ROOT-IM acceptance authority. |
| forbidden_actions_and_boundaries | No source repair, no user-confirmation inference, no suite launch, and no promotion. |
| verification | GATE-RELEASE evaluates the joined final pool. |
| deliverables_and_result_paths | Final generic verdict and, only when required, repair handoff correlation. |
| acceptance_criteria_and_tolerances | ACCEPTED requires REQ-A01 satisfied; tolerance requires explicit user-authorized rationale. |
| completion_review_owner_and_handoff | ROOT-IM takes EDGE-009 on material result, EDGE-009T on the current admitted attention asset, EDGE-009V on any later scoped generic strict test-only asset, or exposes EDGE-010 after release acceptance when external prerequisites are present. Each worker return terminates at ROOT-IM before the next card. |
| failure_classification_and_routes | Material goes MI-HARNESS-REPAIR; current attention uses MI-ATTENTION-PRACTICAL-CORRECT; later generic strict test-only evidence uses MI-VERIFICATION-ASSET-CORRECT; support goes P09; missing product proof is CONTINUE or INCOMPLETE. |
| thread_resume_and_terminal_rule | Decision is terminal on verdict. A product repair uses a terminal coder-main card under P02/P07, then a separately dispatched terminal doer-main evidence card; a test-only correction uses terminal doer-main M03/M04 cards. Any accepted candidate still requires a separate ROOT-authorized doer-main integration card. |
| cited_global_policy_ids_and_exception_ids | P01, P04, P07, P08, P09, P10, P11, P13, P15; no exception. |

#### Outputs and results

One final generic verdict that preserves the integrated candidate as input to the later external boundary.

#### Concurrency and isolation

Serial decision after JOIN-RELEASE; no mutable source or external resource.

#### Resources and side effects

No external fixture claim is acquired. A lack of user confirmation does not change this verdict.

#### Checks and acceptance

GATE-RELEASE accepts only behavior decided by the final pool, not paperwork completion.

#### Failure and exception routes

EDGE-009 returns only a verified generic material pool. Administrative defects advance every non-consuming successor.

#### Prior results and change effects

Accepted candidate and unaffected final paths remain preserved. A repair returns through integration before another final assurance.

#### Repeat, join, and terminal behavior

The release decision is terminal for the generic task. External validation is a separate authorized attempt, not a continuation of final review.

#### Cost and critical-path effect

Expected 5-10 minutes; it prevents physical work from being used to compensate for undecided generic release behavior.

### MI-FIRMWARE-HOST-READINESS - M08: Prove the external control path and sprint continuation without hardware

#### Purpose

Preserve the accepted connection-readiness result and, after the focused lifecycle repair integrates, repeat only the affected target actions to prove `CHECK-SPRINT-CONTINUATION` on the exact installed target with generated fake runtime state and zero MCP-tool/hardware access.

#### Coverage

REQ-H01, REQ-F02, OUT-004, and the pre-live portion of OUT-005.

#### Selection basis

The original M08 connection proof remains accepted. Suites 003-008 changed only the interruption/claim/session consumers, so the smallest adequate response is one affected rerun inside this existing M08 instance, not a second rehearsal module or recovery gate.

#### Owner and roles

ROOT-IM binds the exact integrated target and no-hardware contract; acceptance-orchestrator executes the target lifecycle and returns facts only.

#### Preconditions

EDGE-010 after the EDGE-010R repair path; accepted M07 verdict; clean exact integrated target; implemented four-case verification asset; unique generated tmp/result roots; fake identities/endpoints only; no live suite authority/action.

#### Inputs

Accepted connection-readiness evidence and unchanged-unit map; exact integrated target/tree; mapped acceptance-orchestrator role; task-local MCP launcher; CHECK-SPRINT-CONTINUATION asset; fake process/session/claim/checkpoint inputs; forbidden-event sentinels; unique `tmp/plan2-no-hardware-recovery/{invocation_id}/` root; invocation/process/handoff IDs.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-FIRMWARE-HOST-READINESS; MI-FIRMWARE-HOST-READINESS; DEL-FIRMWARE-HOST-READINESS; host-readiness-continuation; GATE-FIRMWARE-READINESS; no-product-loop |
| workflow_role | acceptance-orchestrator |
| objective | Reuse unchanged connection proof and prove the repaired exact target handles all four fake interruption cases without a tool/hardware event, leaked process/claim, cold sprint restart, or extra recovery mechanism. |
| why_now | M07/M08 are accepted, but suites 003-008 proved that the target/suite contract terminalized interruptions. The focused repair and deterministic evidence must be read back on the exact integrated target before live admission. |
| starting_state | Clean integrated target after the existing repair/evidence/integration/release path; accepted prior M08 units; no live manager/provider/lease/claim authority/MCP action/hardware action. |
| dependencies_and_predecessor_outputs | EDGE-010, accepted repair/asset/evidence/integration/release handoffs, CHECK-SPRINT-CONTINUATION asset/result, mapped role, and fake-only tmp/sentinel contract. |
| working_scope | Read-only target source and exact generated fake runtime below the unique tmp root; disposable provider/watcher/MCP-connect processes only when needed for unchanged connection readback. No product/server/firmware/config/global-settings edit. |
| required_behavior | Preserve accepted target launch/MCP-list/no-tool/cleanup behavior. Execute C1 dead manager/provider replacement with the same logical sprint/checkpoint and fresh runtime IDs; C2 safe dead-owner claim release/reassignment plus exact-resource-only uncertainty; C3 correctable malformed/order/clarification or suite-owned fault without sprint terminalization; C4 completed-with-harness-findings after all feasible work, complete pool, no mid-sprint repair, reset/no-credit classification. All identities/endpoints are fake and every forbidden-event sentinel stays empty. |
| initial_entrypoints | Accepted M08 handoff; exact integrated `resource_locks.py`, `resume.py`, `lane_controller.py`, and `reconcile.py`; CHECK-SPRINT-CONTINUATION asset; task-local launcher/protocol trace; unique fake root/sentinels. Count 5 because they bind prior credit, repaired seams, oracle, real lifecycle, and containment. |
| failure_case_brief | A case could silently restart the sprint, reuse dead authority, reclaim an uncertain resource, stop unrelated work, dispatch repair before completion, omit a later failure after an early one, or touch a real MCP/hardware seam. The four case outputs, event sentinels, complete pool, and cleanup decide these risks. |
| ordered_actions | M08-A1: read back the exact target/tree, accepted M08 checkpoint, mapping, unique fake root, and zero-live-authority boundary. M08-A2: validate fake identities/endpoints and arm MCP-tool/server-plan/permission/lease/USB/probe/serial/radio/hardware sentinels. M08-A3: run the affected target lifecycle plus C1 and C2, preserving unrelated progress. M08-A4: run C3 and C4 and continue every feasible case after ordinary failure. M08-A5: record every case disposition, completed pool/streak result, target observation, forbidden-event state, and first unresolved fact. M08-A6: stop/reap every owned process, remove or visibly retain the tmp root, publish HANDOFF-FIRMWARE-READINESS, and launch no live manager. |
| allowed_tools_capabilities_resources | Exact target launcher/watch/watcher and generated fake-runtime tools; P02-bounded covered commands; no live MCP tool or hardware capabilities. |
| forbidden_actions_and_boundaries | No provider tool call, server plan/permission/lease, USB/probe/serial/radio enumeration/open, firmware/server/product edit, real resource ID, live manager, hardware action, global configuration edit, new recovery status system, or inferred cleanup. |
| verification | CHECK-FIRMWARE-HOST-READINESS unchanged units as selected by P04 plus exact-target CHECK-SPRINT-CONTINUATION, forbidden-event sentinels, target cleanliness, and owned-boundary cleanup. |
| deliverables_and_result_paths | Updated HANDOFF-FIRMWARE-READINESS with exact target/readback, reused and rerun unit map, C1-C4 results, old/new fake identity trace, completed-pool/streak facts, sentinel paths, cleanup, and tmp retention/removal state. |
| acceptance_criteria_and_tolerances | Every required affected case PASS; unchanged connection credit remains input-valid; zero forbidden events; no real identity/endpoint; every owned process absent; stale fake claim released only after complete absence proof; uncertain fake resource remains isolated; exact target clean. No tolerance for missing cleanup or premature repair. |
| completion_review_owner_and_handoff | acceptance-orchestrator terminates at ROOT-IM. ROOT accepts or holds the operation; only acceptance exposes EDGE-011, and it never self-launches M09. |
| failure_classification_and_routes | Product behavior returns to ROOT for one complete EDGE-010R/M02 pool; strict asset-only failure returns to M03; support uses P09; forbidden/live event uses P15. No failure starts a live sprint. |
| thread_resume_and_terminal_rule | One M08 operation ends at HANDOFF-FIRMWARE-READINESS. A replacement invocation consumes its correlated checkpoint; it does not rerun unaffected accepted units or become the logical sprint manager. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P09, P10, P12, P13, P15; no exception. |

#### Outputs and results

One exact-target no-hardware readiness/continuation result for ROOT-IM.

#### Concurrency and isolation

One acceptance-orchestrator operation. Fake cases may overlap only when their roots/inputs are disjoint; no live suite lane exists.

#### Resources and side effects

Only generated fake state, disposable target processes, and result/sentinel files may change. Every owned process/root is closed or terminal-visible.

#### Checks and acceptance

CHECK-SPRINT-CONTINUATION is the single new proof surface. Existing M08 credit reruns only affected units.

#### Failure and exception routes

P09 handles support, P15 handles forbidden/live effects, and ROOT classifies product versus asset failures. No second gate exists.

#### Prior results and change effects

Preserve accepted M07 and unchanged M08 catalog/connection evidence. Invalidate only the changed lifecycle/claim/resume actions and their dependents.

#### Repeat, join, and terminal behavior

One terminal result reaches ROOT. Acceptance exposes EDGE-011; failure remains outside live hardware.

#### Cost and critical-path effect

Expected 10-20 minutes after integration because only one four-case fake-runtime check and changed M08 consumers run.

### MI-FIRMWARE-SPRINT - M09: Complete authorized Firmware logical sprints

#### Purpose

Delegate catalog execution to the existing Firmware suite while ensuring every logical sprint survives replaceable runtime invocations, continues all feasible work, and publishes one complete terminal finding pool before any ROOT harness review or repair.

#### Coverage

REQ-F01, REQ-F02, and OUT-005.

#### Selection basis

Real hardware/MCP behavior needs M09, but recovery does not need another module. The suite already owns scheduling, checkpoints, leases, reviews, and cleanup; BOUND-008 plus EXC-SUITE-CONTINUATION correct only the over-strict terminal rule.

#### Owner and roles

acceptance-orchestrator is the authoritative logical manager role. Concrete manager/provider invocations are replaceable. ROOT-IM alone reviews completed pools, classifies harness ownership, updates the streak, and dispatches later repair.

#### Preconditions

EDGE-011; accepted generic release and exact-target readiness/continuation result; current fixture authority; implemented provider route/smoke; predeclared logical sprint IDs and sequence indices; prepared package-local target; fresh plan/permission/lease/identity for each next live action; no unresolved conflicting exact claim.

#### Inputs

Accepted target/tree; current indexed ledger; selected dependency-ready catalog work; stable logical sprint IDs; suite specs/checkpoints/findings; manager/provider/lane/process IDs; resource claims/leases; watcher/MCP roots; HANDOFF-FIRMWARE.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-FIRMWARE-SPRINT; MI-FIRMWARE-SPRINT; DEL-FIRMWARE-VALIDATION; external-suite; GATE-FIRMWARE-ADMISSION and GATE-FIRMWARE-RESULT; LOOP-SAME-LOGICAL-SPRINT |
| workflow_role | acceptance-orchestrator |
| objective | Schedule every eligible nonconflicting logical sprint/lane, keep each sprint alive across correctable faults/runtime replacement, and publish exactly one `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS` pool per sprint. |
| why_now | The focused continuation repair/check and affected M08 passed, hardware authority is current, and the harness-clean streak is below `3/3`. |
| starting_state | Accepted exact target/readiness/continuation result; no imported live authority; stable sprint IDs/indices and verified durable checkpoints; fresh manager epoch and action-level authority; streak `0/3` or later recorded value. |
| dependencies_and_predecessor_outputs | EDGE-011, BOUND-002, BOUND-008, SRC-011-ready route, suite admission facts, and EXC-SUITE-CONTINUATION. |
| working_scope | Firmware suite manager state, isolated application/run roots, package-local target observation, server plans/permissions, exact leases, and selected catalog evidence. No generic-harness source edit, ROOT-only review access, undeclared hardware, or global configuration. |
| required_behavior | On every scheduling pass launch/resume every dependency-ready resource-compatible lane. Keep stable logical sprint identity across manager/provider replacement. Administrative/provider/malformed-call/order/clarification/doer/spec/fixture/server faults pause/correct only affected work; continue unrelated feasible work. If a harness defect is observed, contain only exact live harm, record it, and continue every feasible unit; do not dispatch harness repair before the sprint completes. A sprint completes when every declared unit is PASS/FAIL/BLOCKED with an exact reason and the full finding pool/cleanup state is sealed. |
| initial_entrypoints | `Firmware/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`; suite skill; provider adapter; current coordination ledger; prepared target; accepted CHECK-SPRINT-CONTINUATION result; selected specs/checkpoints/resource map. Count 7 because they bind catalog, workflow, route, state, product, proof, and resources. |
| failure_case_brief | HANDOFF_SPRINT_FAILURE suites 004-008 are mandatory pitfalls: stale dead-owner claim, unavailable exact session, launch/validator or ROOT-clarification drift, malformed first call/order fault, manager/provider exit, unrelated lanes canceled, and harness repair before terminal pooling. The suite checkpoint, stable sprint IDs, complete unit/pool matrix, and cleanup decide them. |
| ordered_actions | M09-A1: verify exact authorization, target, continuation proof, stable sprint IDs/indices, checkpoints, claims, and fresh action authority. M09-A2: create/refresh correlated logical-sprint and replaceable-epoch records; resume each available unchanged Atlas-through-Nova named session from its terminal inter-sprint handoff, otherwise record and launch its correlated replacement. M09-A3: launch every eligible nonconflicting suite lane in the same scheduling pass. M09-A4: start finite target observation before relevant behavior. M09-A5: execute all feasible selected catalog work and accumulate findings. M09-A6: on interruption apply EXC-SUITE-CONTINUATION to the affected lane/sprint without canceling others. M09-A7: contain only observed live harm and keep every safe feasible unit running. M09-A8: finish every unit disposition and verify exact cleanup/uncertainty. M09-A9: publish one completed HANDOFF-FIRMWARE per sprint; only then may ROOT dispatch terminal review/M05. Preserve available named sessions idle for the next sprint, but never make their survival an admission condition. |
| allowed_tools_capabilities_resources | Suite-declared provider/firmware/MCP/hardware tools under current plans/permissions/leases, target finite watch/watcher, and isolated roots. |
| forbidden_actions_and_boundaries | No unassigned hardware, missing plan/permission/lease, cold restart that discards verified work, sprint failure for recoverable interruption, mid-sprint ROOT harness review/repair, test orchestrator access to ROOT-only report, unselected Q11 work, new scheduler/controller, or fabricated completion/cleanup. |
| verification | CHECK-FIRMWARE-SUITE; sealed spec and independent pre-review; structural/evidence review; every unit/finding disposition; exact resource/process cleanup; one terminal ROOT-only review only after completion. |
| deliverables_and_result_paths | Continuation checkpoints while active; exactly one terminal HANDOFF-FIRMWARE with status, full evidence/finding pool, `harness_error_observed`, stable ID/index, hosting runtime IDs, cleanup/uncertainty, and no repair authorization. |
| acceptance_criteria_and_tolerances | Every feasible declared unit has a truthful terminal disposition; unrelated eligible work was not canceled by another lane's fault; all live actions had exact authority; one completed pool exists. `COMPLETED_WITH_FINDINGS` is valid completion but earns no clean credit when a harness finding exists. No tolerance for missing authorization, fabricated observation, or premature repair. |
| completion_review_owner_and_handoff | acceptance-orchestrator publishes HANDOFF-FIRMWARE and terminates the completed sprint boundary. ROOT then dispatches sprint-evidence-reviewer and decides through MI-FIRMWARE-DECIDE; no suite worker self-dispatches repair or the next graph edge. |
| failure_classification_and_routes | Before completion, every recoverable fault uses P09/EXC-SUITE-CONTINUATION and exact P15 containment. After completion, ROOT classifies the full pool: harness product EDGE-013, generic strict asset EDGE-013V, suite-owned external route, clean EDGE-011/014. |
| thread_resume_and_terminal_rule | Manager/provider invocation loss is internal continuation. The logical sprint ends only at `COMPLETED_CLEAN`, `COMPLETED_WITH_FINDINGS`, explicit user cancellation/authority withdrawal, or unisolatable live harm under P10. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P03, P04, P05, P06, P07, P09, P10, P12, P13, P14, P15; EXC-SUITE-CONTINUATION. |

#### Outputs and results

One continuation checkpoint while active and one completed terminal pool per logical sprint.

#### Concurrency and isolation

The manager schedules every eligible nonconflicting lane/sprint; each has isolated roots and exact leases. A waiting/failed lane does not stop another.

#### Resources and side effects

Only suite-authorized actions within current exact plans, permissions, leases, identities, and selected catalog scope.

#### Checks and acceptance

Suite structural/evidence checks and terminal ROOT-only review decide truth. Completion and clean credit are separate.

#### Failure and exception routes

P09/EXC-SUITE-CONTINUATION handles correctable interruption; P15 contains exact harm. Harness repair starts only after completed EDGE-012/M05 classification.

#### Prior results and change effects

Preserve verified checkpoints, completed evidence, unaffected lanes, generic/release/M08 credit, and ledger credit subject only to index-ordered harness-error reset.

#### Repeat, join, and terminal behavior

Each sprint may span many runtime invocations but emits one terminal pool. Clean completions advance; harness-error completions reset/no-count and take post-completion repair.

#### Cost and critical-path effect

Expected 20-40 minutes per logical sprint plus only actual waits and post-completion repair. Continuation prevents repeated cold-start cost.

### MI-FIRMWARE-DECIDE - M05: Classify a completed external sprint

#### Purpose

After a logical sprint completes, join its sealed suite pool with the terminal ROOT-only review, classify ownership once, update indexed clean credit, and dispatch only the existing post-completion repair or next-sprint/promotion edge.

#### Coverage

REQ-F01, REQ-F02, and OUT-005.

#### Selection basis

ROOT acceptance is still required, but it must occur after—not during—the sprint. One decision over the complete pool prevents the fail-fast repair/churn documented in HANDOFF_SPRINT_FAILURE.

#### Owner and roles

ROOT-IM is sole decision owner. sprint-evidence-reviewer is read-only and runs only after completed HANDOFF-FIRMWARE.

#### Preconditions

EDGE-012 supplies `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`, every feasible unit/finding, exact cleanup/uncertainty, and terminal reviewer result. All producer invocations are terminal.

#### Inputs

Completed HANDOFF-FIRMWARE; terminal reviewer result; exact target/tree; stable sprint ID/index; suite specs/evidence/reviews; unit/finding pool; `harness_error_observed`; cleanup/uncertainty; current indexed ledger.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-FIRMWARE-DECIDE; MI-FIRMWARE-DECIDE; DEL-FIRMWARE-VALIDATION; external-decision; GATE-FIRMWARE-RESULT; LOOP-CANDIDATE-REPAIR or LOOP-VERIFICATION-ASSET |
| workflow_role | ROOT-IM |
| objective | Decide one completed logical sprint from its full pool, update harness-clean credit by index, and route any post-completion harness batch through the existing repair pipeline. |
| why_now | The sprint and terminal reviewer are complete; no further feasible suite evidence may arrive for this sprint. |
| starting_state | One `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS` packet with stable identity/index, full evidence/findings, explicit ownership candidates, and cleanup/uncertainty. |
| dependencies_and_predecessor_outputs | EDGE-012, completed HANDOFF-FIRMWARE, terminal sprint-evidence review, BOUND-002, and GATE-FIRMWARE-RESULT. |
| working_scope | Read-only suite/target evidence, finding ownership, indexed streak ledger, and dispatch decisions. No source/test edit, suite-state rewrite, integration, or mid-sprint action. |
| required_behavior | Validate completion and pool completeness; classify each finding as WIP target-v2 harness product, generic strict verification asset, Firmware server/firmware/specification/fixture/doer, support/admin, or live-harm/authority. A genuine harness finding sets `harness_error_observed=true`, resets/no-counts the completed sprint, and yields one deduplicated post-completion EDGE-013 batch. A clean accepted completion adds credit by index. |
| initial_entrypoints | HANDOFF-FIRMWARE; terminal reviewer result; suite sealed spec/pre-review/post-review; selected catalog acceptance oracle; target coordinate; current ledger. Count 6 because these independently establish completion, criticism, intended behavior, suite findings, product identity, and streak state. |
| failure_case_brief | An intermediate event could be mistaken for completion, suite-owned failure mislabeled harness, a harness finding omitted from the batch, a completed-with-findings sprint marked INCOMPLETE, or repair dispatched before the full pool. Exact terminal status, unit matrix, ownership seams, timestamps, and dispatch records decide these risks. |
| ordered_actions | M05-A1: validate completed result shape, producer termination, identity/index, and cleanup/uncertainty. M05-A2: join every suite finding with the terminal ROOT-only review. M05-A3: classify each finding by responsible seam. M05-A4: separate product, strict asset, suite-owned, and support/live facts. M05-A5: admit harness product work only for failed required behavior with exact seam, protected surfaces, and oracle. M05-A6: update indexed credit: accepted clean `+1`; any genuine harness finding `reset/no credit`; unresolved suite-owned/support result `no credit` without fabrication. M05-A7: after completion only, dispatch one complete compatible harness pool through EDGE-013. M05-A8: route strict generic assets through EDGE-013V and keep suite-owned findings external. M05-A9: reconstruct only an exact consumed support fact; never reopen the completed sprint merely for ceremony. M05-A10: issue one verdict: EDGE-011 below `3/3`, EDGE-014 at `3/3`, EDGE-013/013V, or terminal-visible noncredit result. |
| allowed_tools_capabilities_resources | Read-only evidence/Git inspection, ledger update, and dispatch authority after classification. |
| forbidden_actions_and_boundaries | No mid-sprint decision, source/test edit, provider/manager/hardware action, fabricated PASS/cleanup, worker self-dispatch, finding-by-finding repair, or conversion of completed findings into INCOMPLETE. |
| verification | GATE-FIRMWARE-RESULT, completed status/unit-matrix checks, terminal reviewer correlation, source-owner classification, and index-ordered ledger calculation. |
| deliverables_and_result_paths | One external verdict with completed status, full ownership partition, `harness_error_observed`, preserved/invalidated credit, streak decision, and exactly one declared successor/block. |
| acceptance_criteria_and_tolerances | The completed pool is exhaustive for feasible work; every finding has an owner; harness errors reset/no-count and route only after completion; clean credit requires accepted `COMPLETED_CLEAN`; no tolerance for missing proof or fabricated cleanliness. |
| completion_review_owner_and_handoff | ROOT-IM takes EDGE-013, EDGE-013V, EDGE-011, EDGE-014, or a terminal-visible noncredit route. Every dispatched worker later terminates back at ROOT before another edge. |
| failure_classification_and_routes | Harness product -> EDGE-013/MI-HARNESS-REPAIR; generic strict asset -> EDGE-013V/M03; suite-owned -> suite route; support -> P09. Missing required terminal proof is a noncredit completed/indeterminate decision unless P10's explicit user/safety `INCOMPLETE` condition applies. |
| thread_resume_and_terminal_rule | This ROOT decision is one terminal turn over a completed sprint; it never resumes the suite manager or reopens its runtime authority. |
| cited_global_policy_ids_and_exception_ids | P01, P04, P05, P07, P08, P09, P10, P12, P13, P14, P15; no exception after completion. |

#### Outputs and results

One classified completed-sprint verdict and exact successor.

#### Concurrency and isolation

None. ROOT decides after the suite and reviewer terminate.

#### Resources and side effects

Read-only evidence plus the existing ledger/dispatch decision. No hardware or product mutation.

#### Checks and acceptance

GATE-FIRMWARE-RESULT requires a completed status, complete feasible-unit pool, terminal reviewer, exact ownership, and truthful credit.

#### Failure and exception routes

Harness and strict-asset batches use existing routes after completion; suite/support facts remain with their owners.

#### Prior results and change effects

Preserve generic/release/M08 and unaffected sprint evidence. Apply the indexed harness-error reset exactly once.

#### Repeat, join, and terminal behavior

One completed sprint yields one ROOT verdict. Clean below `3/3` advances; clean at `3/3` promotes; harness findings reset/no-count then repair.

#### Cost and critical-path effect

Expected 5-10 minutes because the suite already pooled the evidence; no mid-sprint review/repair loop exists.

### MI-PROMOTE - M06: Promote the accepted coordinate and retire terminal state

#### Purpose

Advance the exact accepted candidate after generic and external acceptance, read back the destination, retain rollback state, and retire only safe terminal resources.

#### Coverage

REQ-P01 and OUT-006.

#### Selection basis

Promotion is a distinct required operation after acceptance. It must not be disguised as a product test or become an excuse to reopen green behavior.

#### Owner and roles

ROOT-IM performs and verifies the declared operation directly. No provider session or role-mapping lookup is needed for a single repository-coordinate mutation.

#### Preconditions

EDGE-014 supplies the accepted generic verdict plus the `3/3` target-clean external verdict, and destination authority is present.

#### Inputs

Accepted coordinate, generic/external verdicts, promotion destination, rollback base, promotion process ID, and terminal lane/resource IDs.

#### Local instructions

| Field | Value |
|---|---|
| schema/card_id/module_instance_id/deliverable_id/stage_cohort_id/gate_id/loop_id | plan-v3.9.23; CARD-PROMOTE; MI-PROMOTE; DEL-PROMOTION; promotion; GATE-PROMOTION; no-loop |
| workflow_role | ROOT-IM operation owner; no provider session or mapping resolution |
| objective | Promote exactly the accepted coordinate and prove destination readback without reopening accepted product work. |
| why_now | Generic release and selected external validation are both accepted. |
| starting_state | Accepted coordinate, required verdicts, clean destination state, rollback base, and promotion process ID. |
| dependencies_and_predecessor_outputs | EDGE-014 and accepted M05 verdicts. |
| working_scope | Declared promotion destination, rollback, readback, and terminal cleanup only. |
| required_behavior | Promote one accepted coordinate, read it back, retain rollback state, and retire only clean terminal allocations. |
| initial_entrypoints | Accepted coordinate; generic verdict; external verdict; destination status; rollback base. Count 5 because each is promotion-critical. |
| failure_case_brief | REQ-P01: promotion destination mismatch; oracle is readback; ROOT-IM holds only promotion/reuse. |
| ordered_actions | M06-A1: revalidate accepted inputs; M06-A2: verify destination and rollback base; M06-A3: integrate/promote in declared order; M06-A4: inspect destination and affected checks; M06-A5: publish promoted coordinate; M06-A6: advance and read back destination; M06-A7: retain rollback and verdicts; M06-A8: retire only clean terminal state. |
| allowed_tools_capabilities_resources | Declared promotion mechanism, readback, lifecycle cleanup, and P02 supervisor for covered commands. |
| forbidden_actions_and_boundaries | No promotion of another tip, no source repair, no hardware action, and no deletion of needed/dirty/live state. |
| verification | Destination readback and GATE-PROMOTION operation decision. |
| deliverables_and_result_paths | Promoted coordinate, rollback state, and terminal operation result. |
| acceptance_criteria_and_tolerances | Destination exactly matches accepted coordinate; no tolerance for a mismatched or unreadable promotion. |
| completion_review_owner_and_handoff | ROOT-IM confirms EDGE-015 terminal released coordinate. |
| failure_classification_and_routes | Operation mismatch blocks only promotion/reuse; a separate product regression must enter M05 classification. |
| thread_resume_and_terminal_rule | Resume only first unresolved promotion action and retain every accepted verdict; terminal after readback/retirement. |
| cited_global_policy_ids_and_exception_ids | P01, P02, P04, P09, P10, P12, P13, P15; no exception. |

#### Outputs and results

One promoted coordinate with readback, retained rollback state, and safe terminal resource disposition.

#### Concurrency and isolation

Promotion is serial because one declared owner mutates one destination. No parallel source mutation exists.

#### Resources and side effects

Mutates only the declared destination. Terminal suite/candidate lanes retire only after their named consumers no longer need them.

#### Checks and acceptance

GATE-PROMOTION validates operation truth, not product behavior; ROOT-IM preserves accepted behavior on an operation failure.

#### Failure and exception routes

Destination mismatch is terminal-visible operation recovery. It never enters MI-HARNESS-REPAIR without a separate failed product criterion.

#### Prior results and change effects

All accepted product and external results remain preserved. No full test rerun follows a promotion-only recovery.

#### Repeat, join, and terminal behavior

Successful readback takes EDGE-015. Failed cleanup blocks resource reuse only and leaves state visible.

#### Cost and critical-path effect

Expected 5-10 minutes; the final serial operation after all product and external claims are decided.

## 12. External and practical validation

| Decision ID | Module type | Decision | Authority/resource | Synthetic proof | Real proof | Owner | Failure route |
|---|---|---|---|---|---|---|---|
| EXT-FIRMWARE-READINESS | M08 | SELECTED: preserve accepted generic release and M08-A1/A2 catalog preflight, then resume A3-A6 by resolving `acceptance-orchestrator` from SRC-009, materializing its settings into one canonical target invocation, and invoking the accepted target launcher for one disposable host-only proof of the exact provider/lane/watch/watcher/MCP-connect/handoff/cleanup path. Do not wait for the Firmware-specific adapter. | Accepted generic release; accepted static/raw 39-name comparison; mapped role; clean package-local target; disposable roots; task-local launcher marker/protocol stderr; invocation with no hardware identifier, lease, permission, or endpoint. | One actual accepted-target lifecycle records target-side `ListToolsRequest`, returns the exact server alias/`connection_ready` status without any provider tool event, leaves the disposable server tool-event file absent or empty, and proves finite observation and exact cleanup; it establishes shared operational connection readiness only. | None; it deliberately cannot establish Firmware-adapter behavior, MCP-tool behavior, firmware behavior, or fixture behavior. | ROOT-IM prepares/invokes; target-launched acceptance-orchestrator executes | GATE-FIRMWARE-READINESS; hold only readiness and later physical use. |
| EXT-FIRMWARE | M09 | SELECTED after PATH-SPRINT-CONTINUATION-TO-LIVE: schedule every eligible nonconflicting predeclared logical sprint/lane through the existing Firmware suite. | Accepted focused continuation check/M08, provider route smoke, current authority, stable sprint IDs/indices, package-local target, and fresh action authority. | Suite preflight/spec review is admission only. Each sprint survives runtime replacement and finishes every feasible unit before its terminal handoff. | `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`, complete pool, cleanup/uncertainty, terminal suite review, then ROOT-only review/classification. Harness repair begins only after completion. | acceptance-orchestrator with Firmware suite manager; ROOT owns terminal reviewer/decision | GATE-FIRMWARE-ADMISSION or MI-FIRMWARE-DECIDE; preserve unrelated work and same-sprint continuity. |

## 13. Integration, safeguard, promotion, rollback, and retirement

| Decision ID | Module type | Decision | Accepted input | Action/order | Checks | Promotion/rollback/retirement | Owner |
|---|---|---|---|---|---|---|---|
| REL-CANDIDATE | M06 | SELECTED candidate integration | MI-CANDIDATE-DECIDE accepted tip from EDGE-002, EDGE-003, EDGE-003F, EDGE-003T, or EDGE-003G | Only after terminal M03/M04 evidence returns and ROOT-IM accepts it does ROOT-IM issue a new card authorizing doer-main to fast-forward the exact accepted retirement, repair, release-format, or verification-asset tip. doer-main reads back, runs branch-appropriate post-join checks, publishes its handoff, and stops. The historical accepted format tip took EDGE-007L. The accepted one-field manifest repair took EDGE-007T so a fresh doer-main could apply the preserved M03 diff at the repaired coordinate. Every accepted attention-asset or other tip with no open pre-assurance prerequisite takes EDGE-007. | Branch-appropriate post-join checks, including CHECK-VERIFICATION-ASSET and the repair smoke for an accepted EDGE-003G tip when applicable | Retain rollback base; RETIRE-LANES only when safe. | ROOT-IM acceptance; separately dispatched doer-main execution |
| REL-ASSURANCE | M07 | SELECTED final generic assurance | MI-CANDIDATE-INTEGRATE coordinate with REQ-A02, REQ-A03, and REQ-A04 integrated | Run one final review and the exact candidate-owned checkpointed safeguard concurrently in PG-RELEASE; the safeguard completes its feasible unit pool, then M05 decides one joined result. | CHECK-RELEASE-ASSURANCE | No promotion occurs here. | ROOT-IM |
| REL-PROMOTION | M06 | SELECTED final promotion | MI-RELEASE-DECIDE and MI-FIRMWARE-DECIDE `3/3` target-clean verdict | Promote exact accepted coordinate, then read back. | Destination readback only | Retain rollback; retire only terminal clean state. | ROOT-IM |

## 14. Tolerances, unresolved decisions, and out-of-scope ledger

| Item ID | Type | Exact condition | Consequence | Owner | Resolution boundary |
|---|---|---|---|---|---|
| LEDGER-PAUSE | EDGE-010R READY; FOCUSED CONTINUATION PROOF PENDING | M07/M08 remain accepted, the exact `dd673cb...` base is bound, and user delegation remains recorded, but suites 003-008 and all epoch-specific live authority are stopped. | Execute PATH-SPRINT-CONTINUATION-TO-LIVE. Do not launch a live manager first. | ROOT-IM | Closed by accepted integrated `CHECK-SPRINT-CONTINUATION` plus affected M08 result. |
| LEDGER-SPRINT-CONTINUATION | ACTIVE | `HANDOFF_SPRINT_FAILURE.md` shows six non-harness interruptions and two harness defects all ended epochs before sprint completion. | Use one existing repair pipeline and one four-case no-hardware check. No dedicated recovery modules/gate/controller/status taxonomy. | ROOT-IM | Closed by EDGE-011 admission after the accepted affected M08 result; reopen only on changed consumed seams or contrary live evidence. |
| LEDGER-RELEASE-FORMAT | RESOLVED | Clean direct descendant `29ad3c6773cf305ad8f248412268014a545b8e85` exactly matched ROOT's disposable reproduction from `3a73a7b` over 94 paths. Strict UTF-8, format, compile, whitespace, and no-new-finding evidence passed; REQ-A02 was accepted and integrated. | Preserve the accepted source-conformance credit unless one of its consumed inputs changes. | ROOT-IM | Closed at accepted REQ-A02 integration. |
| LEDGER-RELEASE-LINT | RESOLVED | After format integration, the candidate release registry's bare `ruff check .` inherited changing defaults. The accepted repair bound the existing command to explicit critical rules `E9,F63,F7,F82`, and its affected review/checks passed. | Preserve accepted REQ-A03 credit; do not reopen the 409 pre-existing style findings or add configuration machinery. | ROOT-IM | Closed at accepted REQ-A03 integration. |
| LEDGER-ATTENTION-MANIFEST | RESOLVED | The corrected three-file M03 change initially exposed the stale packaged post-tool-use asset manifest SHA on untouched canonical `c114d3f`. | The one-field manifest repair passed existing package/install and S4 wake/idle oracles, was accepted/integrated, and EDGE-007T reused the preserved M03 diff without redesign; the attention asset was then accepted/integrated. Preserve that credit unless a consumed input changes. | ROOT-IM | Closed before final-assurance attempt 006. |
| LEDGER-S3-LOCK | RESOLVED | Attempt 006's unchanged S3 same-path concurrency oracle reproduced `PermissionError(13)` seven times in ten runs because two router instances in one process could enter the same queue transaction before the cross-process kernel lock serialized publication. | The accepted one-path repair added per-canonical-path in-process serialization while preserving the kernel lock and public API; ten repeated oracles, focused lock/safety checks, independent review, and exact integration passed. | ROOT-IM | Closed at canonical `58e533e5cccffbf9f1412c557124e43ea4a4124b`. |
| LEDGER-RELEASE-DURATION | RESOLVED | Attempt 006 remained inside the 478-test orchestrator unit after 1,334.858 supervisor seconds, disproving the registry's 120-second component and 1,200-second aggregate estimates without disproving product behavior. | The accepted metadata-only repair set the component to 1,800 seconds and the aggregate safeguard to 2,400 seconds. MI-RELEASE-ASSURE uses 2,400 expected plus 120 cleanup, for 2,520 maximum and a 30-second heartbeat. Because duration is the existing selector cost key, the shorter watcher suite now precedes the longer orchestrator suite; the selected set and sequential execution are unchanged, and no fixed-order mechanism or false duration is permitted. | ROOT-IM | Closed at canonical `ccbf1913348bb6a86e384b63c5ce7db6fa50a3f7`; attempt-011 ordering objection resolved by plan v3.9.18. |
| LEDGER-RELEASE-STATIC | RESOLVED | `fd2761d` retained the local-handle typing correction and deleted only the three-line pre-lock sentinel block. Independent BasedPyright, compile, same-process, ten repeated cross-process, path-safety, critical Ruff, format, and whitespace checks passed; independent review passed; exact integration succeeded. | Preserve the accepted product credit. Its canonical post-join wrapper timeout is a separate P09 environment support condition, not a retry or product regression. | ROOT-IM | Closed at accepted `fd2761d` integration. |
| LEDGER-SAFEGUARD-CHECKPOINT | RESOLVED | The accepted candidate safeguard checkpoints independently runnable units, continues its complete feasible pool, and conservatively reuses unchanged PASS credit. Its final run completed 16 PASS units with no unresolved result. | Preserve REQ-A04 and M07 acceptance unless a consumed input changes. | ROOT-IM | Closed at accepted generic release `1302d90b2e1439c6f7f66031821a8f452a159f78`. |
| LEDGER-M08-CATALOG-PRESENTATION | RESOLVED | The first M08-A3 provider could not enumerate custom MCP tools without a tool invocation because Codex 0.147.0 forcibly defers them from initial model context, while the same accepted preflight proved the exact 39-name catalog by static registration and raw MCP `tools/list`. | Plan v3.9.23 preserved the no-tool boundary. Attempt 053 passed with target-launched startup/`ListToolsRequest` protocol evidence, the accepted raw/static comparison, an exact alias/status handoff, finite observation, and verified cleanup; no product or server repair occurred. | ROOT-IM | Closed at accepted `FIRMWARE_READINESS_DECISION_055.json`; invalidate only if its target/control/protocol inputs change. |
| LEDGER-FIRMWARE-ADAPTER | RESOLVED | The external run owner implemented the project-local Qwen Code/Ollama route in `Firmware/.qwen/settings.json`. Its DeepSeek and Qwen 397B no-hardware MCP probes passed; Codex is explicitly not admitted. | The provider-route prerequisite is satisfied. Hardware/MCP-tool execution proceeds only after fresh epoch/target preparation and ordinary suite admission complete. | User/external run owner | Preserve the local route; do not substitute Codex without a new successful no-hardware probe. |
| LEDGER-HARDWARE | AUTHORIZED; GATED | The declared four-board fixture is authorized and the harness-clean streak is `0/3`. | No live action until PATH-SPRINT-CONTINUATION-TO-LIVE completes. Then each live action uses exact plan/permission/lease/identity and each sprint continues to `COMPLETED_CLEAN` or `COMPLETED_WITH_FINDINGS`. | ROOT-IM | Closed by `3/3` index-ordered harness-clean completed sprints or explicit user stop/authority withdrawal. |
| LEDGER-Q10 | OUT_OF_SCOPE | Historical M5/Q10 evidence names exhausted attempts, absent run roots, and no verified current harness/watcher defect. | No historical attempt or process is resumed; no repair is inferred. | acceptance-orchestrator | New bounded user goal and explicit authorization, if ever requested. |
| LEDGER-BESPOKE-HISTORY | OUT_OF_SCOPE | Historical custom campaign evidence may aid debugging but cannot accept this plan's external-suite route. | Retain only for history until named consumers no longer need it. | ROOT-IM | Retirement and normal retention policy. |
| LEDGER-SUITE-OWNERSHIP | OUT_OF_SCOPE | Firmware server, fixture, SDK, host, catalog specification, and evidence-only defects are not general-harness product defects. | They follow the suite's owner-specific repair/retest process. | Firmware suite manager | The suite's documented classification and repair process. |

## 15. Rule application matrix

| Rule ID | Plan location | Applied behavior or justified N/A |
|---|---|---|
| R1 | Sections 2-3 | Preserves generic outcome, external real validation, and hardware boundary without adding a controller. |
| R2 | Sections 2-3 | Plan labels are navigation only; no ordinary content receives identity machinery. |
| R3 | Sections 5-8 | Uses the smallest retirement, deterministic format-conformance, assurance, exact host-readiness, and external-suite graph with stated payoffs. |
| R4 | Sections 5 and 14 | Excludes duplicate controller, speculative suite machinery, and non-harness external repairs. |
| R5 | Sections 4, 9, and 16 | Uses honest unavailable, incomplete, and operation-block states. |
| R6 | Sections 7-11 and every M05/M06 instance | ROOT-IM alone diagnoses, names proof and no-change targets, accepts, classifies, and authorizes each successor, integration, or promotion operation. Every coder-main and doer-main work card terminates back at ROOT-IM; doer-main may execute integration only from ROOT-IM's later exact accepted fast-forward/readback/post-join card and returns facts rather than a verdict. |
| R7 | Sections 7 and 11 | Source writers are singular: coder-main owns admitted product/source implementation and doer-main owns selected M03 verification-asset implementation. A worker terminates before a different source owner or evidence phase receives the frozen tip; the format writer and its reproduction checker never share a mutable root. |
| R8 | Sections 7-8 | Pools default to one; only independent check paths overlap. |
| R9 | Sections 1 and 7 | Role-only plan uses one mapping and runtime resolution. |
| R10 | P02 and Sections 10-11 | Cards bind context, IDs, first unresolved action, and terminal handoffs. Coder-main session reuse is the default only through its one unaccepted candidate gate; Atlas-through-Nova session reuse is the default across sprints when available. Every continuation still requires a new owner-issued card/handoff, and unavailable or remapped sessions use nonblocking correlated replacement. No invocation self-crosses a ROOT-IM or suite-manager decision boundary. |
| R11 | Section 11 | Each nonminimal entrypoint set has count and reason. |
| R12 | P10 and M05 instances | ROOT-IM issues exact semantic verdicts. |
| R13 | P09 | Support recovery is narrow and does not decide product behavior. |
| R14 | P07 and M05 instances | Every feasible deterministic result is collected, deduplicated, and partitioned before a compatible material batch returns to one writer. |
| R15 | P08-P10 | Material, mechanical source conformance, test-only, administrative, and external ownership routes are explicit and distinct. |
| R16 | Sections 8 and 11 | Every candidate, release, or Firmware-discovered material product defect returns to its responsible M02 coder-main task as one pool; coder-main terminates at ROOT-IM. ROOT-IM then takes direct EDGE-003 evidence when trusted assets suffice or the typed EDGE-003V -> MI-VERIFICATION-ASSET-CORRECT -> EDGE-003G route when a verification-asset edit is required. |
| R17 | P01, P02, P08, and every selected M03/M04/M06 instance | Plan-wide, ROOT-IM must name the behavior-proof contract, explicit targets/goals, protected surfaces, test-only versus product-repair classification, allowed verification paths, mandatory checks, and acceptance owner before verification work. Every semantic-preserving verification-asset edit uses doer-main in MI-ATTENTION-PRACTICAL-CORRECT or the reusable MI-VERIFICATION-ASSET-CORRECT; every generic deterministic test/check path uses doer-main; every such run terminates back at ROOT-IM. Only after acceptance may ROOT-IM issue a separate doer-main integration card. Any product need returns to classification and coder-main M02; the current attention correction is one exact profile, while EDGE-003V/006V/009V/013V make the assignment executable for later modules. |
| R18 | P09 | Support faults block only direct consumers. |
| R19 | P04, P11, and Section 10 | Every multi-check gate uses conservative input maps, preserves only unchanged PASS credit, continues after ordinary failure, and reruns the failed/unresolved/affected/uncertain union from its earliest required unit; the broad formatter diff gets deterministic equivalence/conformance before release assurance. |
| R20 | Sections 5, 6, and 12 | M08 is selected only for the concrete unproven current-provider/target/harness/watch/watcher/MCP connection lifecycle; it uses one exact disposable path rather than a broad rehearsal campaign or premature adapter implementation. |
| R21 | Sections 7, 10, and 11 | Runtime processes, sessions, handoffs, lanes, locks, and worktrees require IDs; ordinary content does not. |
| R22 | P12 and Section 12 | One earned no-tool/no-hardware connection-readiness operation uses the canonical role mapping and accepted target launcher. Accepted source/static/raw preflight establishes the side-effect-free path and exact 39-name catalog; target-launched startup and `ListToolsRequest` protocol evidence proves actual negotiation; the provider returns only the configured alias/status; and provider events, the disposable server tool-event file, the invocation, observation, and cleanup decide that no provider tool or hardware path ran. It remains distinct from later adapter-local smoke and real suite proof. |
| R23 | P15 | Immediate stop is limited to observed live harm. |
| R24 | Sections 8-9 | Product loop requires failed/undecidable criterion, batches compatible material findings, and preserves unrelated/unchanged unit credit. |
| R25 | Sections 5 and 11 | Independent static review is limited to salvage/retirement or semantic repair and one final release input; deterministic source-normalization/Ruff reproduction replaces low-value review of mechanical output. |
| R26 | Section 4 | Stable launcher, target harness, and Firmware suite are truthfully distinguished. |
| R27 | Section 10 | One writer worktree; read-only evidence roots; package-local external target. |
| R28 | Section 10 | Retire only clean, unclaimed terminal state. |
| R29 | Section 10 | The suite owns its required append/log locking; no duplicate plan log exists. |
| R30 | P02 and Section 4 | The mechanical hook covers configured direct Python, executed `.ps1`, and Bash/sh launches, including those found in one ordinary PowerShell `-Command`/`-c` body. Configured exclusions remain path-based; direct executables and encoded-command parsing are deliberately outside scope. Root and worker inner commands use the supervisor, while provider sessions remain lane-managed and unbounded. |
| S1 | Sections 0-16 | Fixed plan envelope is preserved. |
| S2 | Section 6 | Every module has explicit selected or omitted decision. |
| S3 | Section 8 | Typed outputs and conditions define every edge, including the optional M02-to-M03 asset branch and candidate/release/Firmware strict test-only returns. |
| S4 | Section 9 | Global policy is defined once and cited by cards. |
| S5 | Sections 8-11 | Mandatory actions use concrete triggers, owners, and exits. |
| S6 | Section 11 | Cards customize scope without altering global graph. |
| S7 | P05 | Review classes and invalidation boundaries are explicit. |
| S8 | PG-CANDIDATE and PG-RELEASE | Independent selected paths launch before waiting; the single-path format evidence is correctly excluded from artificial fan-out. |
| S9 | P07 | Material repair receives one complete feasible pool through coder-main, terminates at ROOT-IM, and only then receives a separately dispatched doer-main affected-evidence path; individual safeguard defects are not repaired ahead of later runnable units. |
| S10 | P11 | One final safeguard applies to one release unit as checkpointed coarse units; it resumes at the earliest required unit and never repeats an unchanged prefix. |
| S11 | P03 and Section 5 | Failure briefs are realistic and oracle-backed. |
| S12 | Section 8 and P13 | Ranges and critical paths are stated; overrun triggers reassessment. |
| S13 | P14 | One concrete suite-checkpoint exception is fully bounded. |
| S14 | Sections 8-11 | Graph, policy, lanes, checks, handoffs, allocations, and cards use the same direct-M04 or required-M03 routes. |
| S15 | Section 4 | Capability classes distinguish runtime, orchestrator, target tool, and unavailable behavior. |
| S16 | Section 8 | Product and operation gates have exact scopes, loops, default-forward edges, and split triggers. |

## 16. Structural validation result

| Check ID | Result | Basis |
|---|---|---|
| V01 | PASS | One title and Sections 0-16 appear once in order. |
| V02 | PASS | All required tables use the fixed headers and populated rows. |
| V03 | PASS | Every REQ row names one deliverable, verification route, and ROOT-IM acceptance owner. |
| V04 | PASS | M01-M10 are decided; every selected instance, including both exact and reusable M03 instances, the distinct mechanical source-conformance M02, and the checkpoint-safeguard M02, uses the 16-heading schema and recipe actions. |
| V05 | PASS | Section 8 connects the current M08 checkpoint through one EDGE-010R into the existing M02/M03/M04/M05/M06 and affected M07/M08 path; M09 interruptions stay internal through EXC-SUITE-CONTINUATION and only completed pools reach EDGE-012/013. |
| V06 | PASS | Deferred M01 and omitted M10 do not appear as live instances or graph edges; every M03 activation requires an exact ROOT-IM proof contract and a terminal doer-main card. |
| V07 | PASS | Every selected module and serial edge has dependency or risk payoff in Section 5. |
| V08 | PASS | Candidate review/check and release independent paths use explicit parallel groups; the format branch correctly remains one deterministic path. |
| V09 | PASS | M04/M07 collect every feasible result; M05 pools, deduplicates, and batches compatible findings before one material writer return. |
| V10 | PASS | Existing review classes remain frozen/scoped; the continuation change adds only CHECK-SPRINT-CONTINUATION, and sprint-evidence review occurs only after a completed terminal pool. |
| V11 | PASS | The candidate-owned accumulated safeguard occurs only in MI-RELEASE-ASSURE for one release unit, retains its existing registry, and uses the accepted checkpointed executor rather than a reconstructed plan list. |
| V12 | PASS | P04/P11 preserve only valid green credit, declare conservative inputs, continue after ordinary failures, and rerun failed/unresolved/affected/uncertain units from the earliest required member. |
| V13 | PASS | Every selected instance retains all 20 task-card fields; current M02/M08/M09/M05 cards bind the focused continuation behavior without adding an instance. |
| V14 | PASS | Cards cite global policy and do not create new graph or authority behavior. |
| V15 | PASS | EXC-SUITE-CONTINUATION has exact trigger, owner, action, confirmation, preserved/invalidated credit, scope, and expiry; it reuses the suite checkpoint/handoff rather than adding machinery. |
| V16 | PASS | Section 4 distinguishes runtime, orchestrator, target-tool, and unavailable states. |
| V17 | PASS | Stable implementation runner, canonical role mapping, accepted target launcher, pending Firmware-specific adapter, and suite tooling are separate; connection-only readiness tests the target launcher and does not claim adapter or MCP-tool behavior. |
| V18 | PASS | Role table equals the canonical mapping role set and the mapping filename appears once. |
| V19 | PASS | Source mutation is singular: coder-main owns product source and doer-main owns one selected verification worktree; the format reproduction mutates only its disposable check root; all concurrent review/check paths have separate roots. |
| V20 | PASS | Concurrent results have disjoint roots; suite locks remain suite-owned. |
| V21 | PASS | Each entrypoint count is bounded and justified. |
| V22 | PASS | Failure briefs assign high-context retention judgment to ROOT-IM and name realistic implementation, format-equivalence, and connection-readiness triggers, invariants, focused oracles, and owners. |
| V23 | PASS | P08-P10 keep support and true test-only faults out of product M02 tasks, require the typed reusable M03 route before any later test-asset edit, route source conformance through its mechanical M02 task, and keep the clean-base manifest defect separate from the preserved M03 asset. |
| V24 | PASS | Every gate has one class, exact scope, default-forward behavior, and justified repair or operation route; the accepted `stable_io.py` integration returns through EDGE-007E before release assurance, and host readiness cannot become a product loop. |
| V25 | PASS | Product returns preserve completed work, use the same functional role, and split only by real ownership/context boundary; source-conformance failure returns only to its originating mechanical task, while the one-field packaged-asset repair returns to the same preserved attention proof contract. |
| V26 | PASS | Retirement retains dirty/live/needed state and leaves failed cleanup visible. |
| V27 | PASS | Executable cards use explicit owners, triggers, actions, and exits. |
| V28 | PASS | Section 15 maps R1-R30 and S1-S16 once to concrete behavior. |
| V29 | PASS | Runtime instances and required ROOT-to-coder/doer proof-contract, HANDOFF-REPAIR asset-need decision, terminal M03/M04 evidence, and later integration-authorization handoffs are correlated in Sections 7, 10, and 11 without assigning IDs or hashes to ordinary content. |

PLAN_STRUCTURE=VALID
