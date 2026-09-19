# Harness v2 Tier 4 - Addendum 3 - Global Workflow Rules

## 9. Global workflow policies and exceptions

### P01 Ownership and decisions

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Any activation, finding pool, conflict, role change, integration, live attempt, acceptance, or retirement decision | ROOT must author every complete card, preserve the directive hierarchy, decide all cross-lane routes, and never delegate task meaning, scope, success, acceptance, or self-dispatch authority | One already-declared edge, verdict, or exact incomplete fact | Retain only a result consumed by a later decision | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P02 Context and thread lifetime

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A workflow role starts or resumes an unaccepted logical task | Supply one bounded 20-field card that concretely fixes the problem, desired result, behavior/proof targets, target and protected scope, required and forbidden changes, inputs, checks, acceptance, pitfalls, stop routes, lane ID, Git-worktree ID, process-tree ID, provider-invocation ID, and handoff ID. A worker executes that contract, reports an insufficiency or contradiction, and terminates at each decision boundary; it never reconstructs missing semantics or self-dispatches. Logical tasks are unbounded, but every role launch must copy all current invocation_binding.config_overrides from its selected mapping entry into the frozen-controller invocation and read them back, including the mapped automatic-compaction threshold; retain native compaction rather than replacing it with an agent deadline or a task restart. Recheck and retry the mapping's primary at every new lane, module, and launch. Use the fallback only for that launch after the primary reports a compute/capacity limit or ROOT proves a current external impossibility by trying and reading back every concrete in-scope launch, authentication, configuration, and command workaround; ordinary command, policy, permission, configuration, authentication, result, or task failures remain primary-route diagnosis, not fallback eligibility. A controller exit or nominal completion is usable only when `result_validation.state=VALID`. If the result is `INVALID` or `MISSING` while the frozen thread, repository, worktree, selected model/configuration, worker invocation, and output-path identities remain intact, ROOT resumes that same frozen lane with a narrow card to correct the result or handoff, preserving those identities and all accepted progress. Allow two same-thread correction attempts after the initial invalid or missing result, stopping early when the result becomes valid. The second attempt does not require progress from the first: a repeated validator error or lack of progress after the first correction must not trigger a fresh lane. This budget tolerates an ineffective first model correction; record both attempts against the unresolved action and preserve that history across replacement lanes. For terminal-result recovery, exhaust both correction attempts before routing to a fresh lane for persistent malformed output or nonprogress. Outside terminal-result recovery, repeated discovery twice or five minutes of repetitive transcript activity without a relevant state or evidence change can establish thrashing; elapsed time alone cannot. When both correction attempts fail or other established thrashing requires intervention; ROOT then stops only exact owned processes, releases exact claims, and dispatches a fresh same-role primary lane from a structured handoff containing accepted state and the first unresolved action. Missing thread/worktree identity or verified repository drift requires that fresh lane immediately. An invalid or missing result never qualifies the fallback, and a fresh lane that also thrashes causes ROOT to split the task at the first unresolved action instead of replaying the monolith. Prefer the active invocation only while available and still selected by the user; otherwise dispatch the same role from a structured handoff with accepted state and the first unresolved action. Immediately after every completed MI and before a planned context transfer, refresh HANDOFF.md with exact source, accepted state, first unresolved action and old/new invocation correlation. Compaction preserves the same logical task and never justifies fallback or replay of accepted work. | One frozen-valid terminal worker handoff followed by a separate ROOT decision/card, or a durable thrash handoff to a fresh/split same-role lane. | Result-validation state, old/new invocation and thread IDs, preserved identities, correction attempts and progress evidence, thrash trigger when applicable, primary attempts, workaround/readback evidence, qualifying external cause, fallback outcome, and handoff ID when continuity changes | MI-NORMAL-PRODUCT, MI-NORMAL-VERIFY-ASSETS, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-INTEGRATE, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX |

P02 dispatch requirements for the workflow-reliability repair:

- ROOT supplies the exact current invocation/context path, worker facts path, separate task-handoff
  path, and absolute `frozen-harness/orchestrator_harness/result_emit.py` command in every new or
  resumed result-producing card. Workers author the facts and findings; the emitter supplies and
  validates the coding envelope. External workers use a ROOT-owned result context correlated with
  the frozen operator-launch receipt as documented in the frozen QUICK_START.
- Every replacement card preserves discovered entrypoints, partial work, reusable verification and
  the first unresolved action, and states the concrete change that makes this attempt productive
  (repaired prerequisite, narrower implementation seam, or explicitly authorized role-allocation
  change). Rewording the same failed assignment or repeating discovery is not that change.
- Repair a recurring headless permission/configuration cause in its authoritative configuration.
  Prove the exact tool command, readiness, result publication and cleanup using a disposable probe
  before allocating another real attempt. Authentication or a text-only response is insufficient.
  The PRACTICAL_OBSERVER mapping now scopes shell permission to the authorized
  `.agent-workspace/start-observer-*` startup command. ROOT inspects each startup script before
  dispatch; this permission does not grant new experiment authority or change model selection.
- For external reviews in a separate worktree, ROOT supplies explicit native read-directory scope
  for each named source outside that worktree and preserves it on resume. Test required reads as
  well as output permission; an unreadable target cannot produce independent-review acceptance.

P02 progress supervision is **ORCHESTRATOR_POLICY / MANUAL**, not an implemented
automatic watchdog. ROOT reads the lane's native transcript, command status and
task artifacts at command completion/error, notification, context recovery, and
before any continuation dispatch. Each card names its next evidence delta
(for example a RED regression, feasibility result, exact copied asset, or terminal
packet). Record RUNNING, WAITING_FOR_COMMAND, READY_TO_REPORT or BLOCKED in the
existing handoff when it affects continuation. Answered questions and the first
incomplete action survive compaction. READY_TO_REPORT proceeds to mechanical
validation/publication, not another discovery pass. Apply P02's existing evidenced
thrash rule and two result-correction attempts; no elapsed-only agent deadline.

Before repeating a failed launch, ROOT reads its native terminal error and the
exact credential/configuration home used. Authentication failure in a copied home
requires that context's admission to be corrected; it does not establish a stdio
or wrapper defect. Reuse only authorization and admission whose scope/freshness
still covers this launch. Inspect no credential contents in published evidence.

### P03 Failure-case selection

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Before a high-coupling writer, review, safeguard, or real attempt is dispatched | Select realistic late-cost cases across target identity, grammar and paths, concurrency, lifecycle and cleanup, rollback, compatibility removal, external resources, truthful results, and usability; bind each selected case to a requirement, trigger, invariant, oracle, and owner | Complete card or exact insufficiency | Put selected cases in the owning card; create no generic checklist | MI-NORMAL-PRODUCT, MI-NORMAL-VERIFY-ASSETS, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX |

### P04 Check selection and green credit

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A deterministic campaign starts, resumes, or consumes a changed candidate | Use the checkpoint and conservative input map, including its first unresolved unit. Continue every runnable unit after ordinary failure and preserve unaffected PASS. Series 1 starts from a complete pool and one scoped correction, runs changed-source compile plus the motivating test, performs independent review and separate integration, retains reusable smoke credit, records concrete saved work, and exits to the ROOT-selected progress bound. Series 2 joins every accepted Series 1 exit at that progress bound, calculates invalidation, begins the remaining execution set at its earliest required unit, preserves unaffected PASS, records saved work, and continues the normal successor. The bounded-command manifest currently selects zero finite fragments, so target checks use their native commands; agent launches remain outside bounded execution. Treat unexecuted macOS/Linux native portability and provider-boundary claims as recorded gaps outside the currently runnable execution set under BOUND-014. Preserve their unverified status and continue all independent Windows units; classify real code defects discovered through portable analysis and repair them even when their native platform cannot run. | Complete feasible unit pool or an exact prerequisite-blocked unit record. | Checkpoint stores unit state, consumed inputs, first unresolved unit, Series 1 smoke credit, and Series 2 invalidation | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-FL2-S1-PRODUCT-REVIEW, MI-FL2-S2-PRODUCT-RECONCILE, MI-FL2-S2-ASSET-RECONCILE, MI-NORMAL-FINAL-ASSURANCE, MI-FL2-S2-ASSURANCE-RECONCILE, MI-NORMAL-LIVE-READINESS, MI-FL2-S2-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

Remaining-work amendment (3.7): apply the current Section 16 scope audit to newly
scheduled work only. A documentation revision does not invalidate product, static,
audit or native credit. Record each proposed family against its requirement,
observation oracle, changed consumed input, distinct confidence and estimated
construction/execution/repair cost. Reuse existing tests before authoring more and
group equivalent control cases locally. Never multiply a provider-independent
product assertion across live providers. Deterministic tests decide product
behavior; compatible retained evidence or one direct public-path canary decides
each shipped provider/profile boundary under BOUND-020. Any evidence expansion
returns to ROOT for a concrete missing claim and cost decision.

Functional-coverage floor for remaining work: before eliminating or reusing a
case, identify the required assertion and implementation boundary it observes.
Keep normal and adverse/recovery observations distinguishable in the deterministic
evidence map; missing, failed and unobserved product claims remain open. Reuse
requires adequate original assertions and unchanged inputs. Oracle/reference-model
tests alone do not prove candidate behavior. For a shared product helper change,
examine every affected caller and both profile paths. Provider/profile equivalence
is claimed only for product-independent behavior; actual provider traversal keeps
its own boundary canary. Preserve unaffected completed credit.

REQ-008/009 candidate boundary: constructed attempt arrays and a third-attempt
controller success do not establish the accepted five-correction limit. The
remaining deterministic scope includes two focused candidate-controller cases:
valid result after the fifth correction on the sixth provider attempt, and six
invalid exits with exactly five prompts, no sixth prompt, exactly one final
provider_exited_no_result, same-session/lease continuity, and cleanup evidence.
These are local controlled-provider cases, never live-provider scenarios.

### P05 Review classes and invalidation

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A reviewable product, asset, repair, or final tip freezes | Declare INITIAL_IMPLEMENTATION, AFFECTED_REPAIR, or FINAL_PRODUCT; bind one exact revision, requirements, invariants, watch areas, protected scope, materiality threshold, output shape, and handoff while leaving findings open | Complete assigned surface, including zero findings | Review result is bound to its frozen tip; changed consumed meaning invalidates only affected review credit | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-FL2-S1-ADMISSION-REVIEW, MI-FL2-S1-PRODUCT-REVIEW, MI-FL2-S1-ASSET-REVIEW, MI-FL2-S1-INTEGRATION-REVIEW, MI-FL2-S1-ASSURANCE-REVIEW, MI-FL2-S1-LIVE-REVIEW, MI-NORMAL-FINAL-ASSURANCE |

### P06 Parallel checks and results

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | Independent review and deterministic checking consume the same frozen input | Give each member a distinct lane, worktree, cache, and result root; launch both before awaiting either; let all feasible paths finish; join exactly once | One complete campaign pool | Preserve each member handoff and the single joined result | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

Historical matrix scheduling (3.5): these rules describe completed and paused
matrix evidence only. BOUND-020 removes that scheduler, coordinate graph, custom
terminal predicate, and per-coordinate timeout apparatus from future dispatch.
The proportional path binds each direct canary to one provider/profile boundary,
public command sequence, product-owned record paths, exact cleanup identity, and
native lane/result lifecycle. A canary failure is terminal evidence for M05; it
does not trigger an automatic replay. P15 containment remains authoritative.

Local suites (3.6): the existing CHECKER binds exact commands/shards, cwd,
environment, prerequisites, per-command budgets and Section 7 `K_local` before
launch. Separate isolated local, stateful local and live-resource consumers;
serialize only actual fixture/port/cache/provider conflicts. Determinism alone
does not prove isolation. Parallel review/check agents do not parallelize their
scripts. Use supported native parallel mode or economical stable module/test-ID
shards; preserve discovery, fixture setup/teardown, assertions and individual
outcomes. Small suites may stay together when startup costs exceed savings.
No ordinary assertion failure enables suite-wide fail-fast. End unreachable
scenario waits promptly, continue independent tests, refill each freed slot and
collect the complete feasible pool before P07 repairs and P04 affected reruns.
List order and earliest-unresolved checkpoints never serialize independent roots.

Dispatch independent finite commands through CHECKER's existing native command
tools with isolated stdout/stderr, TEMP/TMP, cache and result roots, one wait per
handle and owned cleanup. This is MANUAL/ORCHESTRATOR_POLICY, not an automatic
scheduler supplied by frozen-harness or unittest. ROOT supplies the concrete
selection and budget; the worker applies them mechanically. Missing economical
sharding/isolation/control capability returns only its consumer to the existing
M03 NORMAL asset route and affected review/readiness. Do not add a harness or
another agent per test. Existing tiny checks need no new scheduling framework.

### P07 Finding pooling and material repair

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | M04, M07, or M09 returns terminal findings | Build one complete pool, deduplicate once, classify once, and send each compatible material group to its declared same-owner correction path; split only incompatible owners, source contexts, or acceptance criteria. Every step carries a configured FAST_LANE_V2 Series 1 path with a complete pool, deterministic correction, motivating test, changed-source compile, independent review, separate integration, and retained smoke credit. Before another assurance run, join every accepted Series 1 exit once at the ROOT-selected current progress bound; its configured Series 2 path calculates invalidation, preserves unaffected PASS, runs the earliest required remaining work, records saved work, and continues the normal successor. A false activation predicate routes that event through normal R15 classification without altering either configured fast contract | Accepted result, one concrete repair card, or exact incomplete claim | Joined finding pool plus preserved/invalidated credit | MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-MATRIX, MI-FL2-S1-PRODUCT-PATCH, MI-FL2-S1-ASSET-PATCH, MI-FL2-S1-ASSURANCE-PATCH, MI-FL2-S1-LIVE-PATCH, MI-FL2-S2-PRODUCT-RECONCILE, MI-FL2-S2-ASSET-RECONCILE, MI-FL2-S2-ASSURANCE-RECONCILE, MI-FL2-S2-LIVE-RECONCILE |

For deterministic pools or direct canaries, classify the complete current result
before mutation and distinguish product, test/oracle, provider support, environment,
and uncertain causes. Give each material product cause one coherent owner while
retaining every raw finding. Similar messages alone do not establish a shared cause.
P04 selects changed-input consumers and dependents while retaining compatible
credit. Test-control defects from the retired matrix have no prospective consumer
and therefore do not enter a repair/replay loop.

### P08 Test-only correction

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A failed asset, fixture, runner, metadata, test-code, or expected literal may be wrong | Prove the correction preserves scenario, required behavior, oracle, assertion strength, and coverage; authorize only the known asset change and exact affected rerun. Production source, policy, contract, locked configuration, and expected behavior must not change | Return to M05 classification after one terminal correction handoff and affected rerun | Preserve unrelated PASS results and record the deterministic admission basis | MI-NORMAL-VERIFY-ASSETS, MI-FL2-S1-ASSET-PATCH, MI-FL2-S1-ASSURANCE-PATCH, MI-FL2-S1-LIVE-PATCH, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

### P09 Administrative recovery

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A report, schema, path, runner, environment, supervision, result-shape, or cleanup fault occurs | Classify it as administrative/support; reconstruct or correct only when an exact consumer still needs it and correction is cheaper than recording the limitation. Reread the bounded-command manifest before commands; its current selection contains zero finite fragments. Preserve product facts and advance every nonconsumer | Corrected required fact or terminal recorded limitation | Exact support-dependent claim and affected consumers | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-CAMPAIGN, MI-NORMAL-ASSET-CAMPAIGN, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-INTEGRATE, MI-NORMAL-FINAL-ASSURANCE, MI-NORMAL-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-NORMAL-LIVE-VERDICT |

P09 result prevention: use the native emitter's preflight/publication/readback rather than manual
envelope construction or per-lane finalizer variants. Keep only outcome, summary and checks in the
worker facts JSON; keep detailed findings in the assigned handoff. Preserve the actual outcome,
including FAIL/BLOCKED, and validate any task-specific handoff with its existing checker when one
exists. Correct a local validator error before finishing the card, within P02's finite recovery
budget. If completion still returns INVALID/MISSING, use P02 recovery; never silently repair an
independent review or a deliberately malformed live-test result to claim PASS. Retain existing
worker assignments and substantive review gates; this change does not remove them.

P09 dispatch preflight must confirm that the native emitter command contains the
actual current context, facts, result and handoff paths, without placeholder
arguments. Use the existing emitter/schema and canonical bundle-digest mechanism;
read back strict UTF-8 without BOM and the exact consumer shape. Correct only the
failed envelope, encoding or digest consumer while preserving substantive evidence.
This never rewrites an intentional malformed-result scenario or changes a FAIL
finding into PASS. P02 owns the unchanged same-thread correction budget.

### P10 Semantic acceptance

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A producer, campaign, integration, assurance, or live pool reaches ROOT | Validate shape without equating shape with success; decide behavior from requirements and observations; emit exactly ACCEPTED, ACCEPT-WITHIN-TOLERANCE with explicit rationale, CONTINUE only for a failed or undecidable required product criterion, or INCOMPLETE. Apply BOUND-014 to final acceptance: decide the executable implementation/audit/Windows scope separately from cross-platform qualification; retain the two native gaps and advance EDGE-007 after executable criteria pass. A Windows failure or undecidable Windows result keeps its consuming Windows criterion failed or incomplete. | One verdict or one separately authored correction card. | Durable verdict only when a downstream consumer requires it | MI-NORMAL-PRODUCT-VERDICT, MI-FL2-S2-PRODUCT-VERDICT, MI-FL2-S2-ASSET-VERDICT, MI-FL2-S2-ASSURANCE-VERDICT, MI-FL2-S2-LIVE-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

For the remaining live verdict, distinguish product correctness, actual provider
compatibility, and control validity. Compare the exact source clause with the
failed assertion before assigning a writer. A broken fixture or reader is not
product-defect proof. Deterministic malformed-output injection may decide a
harness invariant; it cannot prove unobserved native provider/hook/resume behavior.
Correct containment does not turn a failed compatibility claim into PASS. Retain
raw failures and classify nonblocking only with a cited independently satisfied
claim or governing exception; uncertainty remains incomplete. ROOT adjudicates
review criticism and repeated findings for validity; reviewers do not enlarge the
contract or restart accepted campaigns by default.

### P11 Full-safeguard scope

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | The integrated release unit reaches STEP-005 | Run the required FINAL_PRODUCT audit rounds and CHECK-U1 through CHECK-U5 plus CHECK-FULL-SUITE against the same revision. Each unit owns its source, configuration, runner, environment, prerequisites, dependents, checkpoint state, and ordinary-failure continuation; complete all feasible units and join once. On Series 2 re-entry, form the failed, unresolved, change-affected, or uncertain set from the conservative input map and begin at its earliest required unit without replaying unaffected PASS. REQ-021 requires CHECK-AUDIT-INITIAL and a separately dispatched CHECK-AUDIT-FOLLOWUP after ROOT dispositions, even when the initial audit finds zero issues. Review actual implementation and relevant tests/records against Parts I-XIX as amended by SRC-009; admit only direct requirements, plainly broken flows or demonstrated obvious-design violations. Each finding must cite requirement, code, minimal failure sequence, smallest correction and why it is required; label missing native proof separately. ROOT reads each finding and records Valid, Invalid/overcorrected or Needs evidence with rationale; only valid findings enter repair. Resolve Needs evidence through focused code/test evidence before clearing its consuming criterion; implement and verify every valid finding or retain a specific operator-authorized deferral. Repeat until a follow-up has no undispositioned valid gaps or the operator explicitly defers a specific item. Reviewers advise and never veto. Finish each pool, integrate admitted repairs, and re-enter M07 for uncredited/invalidated audit and safeguard units; a follow-up due solely to this rule does not invent a product defect or trigger M02. Only ROOT grants live admission. | Complete final pool for M05. | One checkpoint with first unresolved unit and conservative input map | MI-NORMAL-FINAL-ASSURANCE, MI-FL2-S2-ASSURANCE-RECONCILE |

For version 3.4, preserve completed CHECK-U1 through CHECK-U5, full-suite and
initial/follow-up implementation-audit credit under their consumed-input maps.
A control-only repair selects its motivating tests and affected neighbor/boundary
checks; do not repeat the complete product suite or source-audit loop solely
because the next live attempt or this plan has a new revision. Product changes
still invalidate dependent static/audit evidence and retain all binding safeguards.
M04 reviews actual changed deterministic assertions for requirement fit. M08
performs only the read-only direct-canary admission checks whose consumed inputs
changed before M09 uses external resources.

### P12 External authorization and rehearsal

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | STEP-006 would consume a native platform runner, real installed target CLI, or user credential | Require the exact current platform and provider/profile identity, applicable recorded provider authority, current configuration identity, BOUND-013 confinement, REQ-021 audit clearance, deterministic canary-path proof, a compatible-credit comparison, and current M08 read-only readiness. Windows is admitted without macOS/Linux runners under BOUND-014, which records those native gaps. Reuse recorded authorization after scope comparison and ask only for genuinely new authority. M08 never counts as product or provider proof. Under BOUND-020, M09 runs at most one direct public bootstrap/start/record/retire canary for each boundary lacking compatible native PASS. Product-owned durable records are inspected after terminal state; no background observer, scheduler, custom timeout, prompt-produced fixture, or feature/provider matrix is created. ROOT owns authorization and checkpoints; resume only when consumed state is unchanged. A prompt, file existence, mock, configuration readback, or authentication probe is never native provider PASS. A product-path failure closes safely and returns to M05; provider capacity or authentication failure remains a boundary-specific support result and does not trigger automatic replay. | Authorized terminal direct canary or exact provider/platform support claim. | Readiness result, canary ID, provider/profile identity, product-record verdict, checkpoint, and cleanup state | MI-NORMAL-LIVE-READINESS, MI-FL2-S2-LIVE-READINESS, MI-NORMAL-LIVE-MATRIX, MI-FL2-S2-LIVE-RECONCILE |

P12 admission binds the exact provider credential/configuration identity and
relevant freshness evidence to the next direct canary. Existing authorization is
reused within scope. A refreshed configuration or changed permission invalidates
only its dependent readiness and canary credit. M08 owns read-only admission;
M09 owns one public canary and exact cleanup. Historical Series 9 scheduling is
frozen evidence rather than a future execution template. No new canary begins
solely because this planning amendment passed.

P12 effective-path binding: for this epoch, the prior admission's workspace homes
are `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-provider-homes/`
with `CODEX_HOME=codex`, `CLAUDE_CONFIG_DIR=claude`, `QWEN_HOME=qwen`, and
`TEMP`, `TMP`, `CLAUDE_CODE_TMPDIR` pointing to its `temp` child (all values resolved
absolutely from that parent). These are historical bindings to compare, not
current authentication proof. M08 reads only non-secret identities and authority
metadata; M09 must read back the effective binding inherited by the selected
direct canary without exposing secret values. Bind each canary root beneath the
workspace and use the accepted product's own durable-record paths. Directory
naming alone does not prove containment.

Reuse existing source/path/archival proof only for its declared coverage. If a
shared-store write observation is missing, ROOT names the exact non-secret store,
quiescent snapshot points and consumer before selecting the skill's snapshot/compare
helper; retain its output outside the watched root. The helper rejects junctions
and cannot prove absence of transient writes. Do not scan provider credential
contents or recursively traverse shared source junctions. An unresolved inheritance,
cache ownership or footprint fact blocks only the affected canary admission. Any
missing product assertion returns to its deterministic owner; no generic live
control asset is created.

### P13 Gate/loop sizing, health, and topology reassessment

| Owner | Trigger | Required action | Exit | Result/record if needed | Module IDs |
|---|---|---|---|---|---|
| ROOT | A gate is designed, a result pool crosses its boundary, or observed work exceeds the expected range and another material cycle is required | Keep each gate to one repairable product family or exact operation. Batch compatible findings, preserve unaffected credit, stop on success, unrecoverable error, or stall, and reassess module choice, card size, review surface, and role allocation before another material launch; never use an arbitrary iteration cap | Same graph, prospectively split/merged unaccepted graph, or plan amendment | Record only a changed topology decision and its affected edges | MI-NORMAL-ADMISSION, MI-NORMAL-PRODUCT-VERDICT, MI-NORMAL-ASSET-VERDICT, MI-NORMAL-INTEGRATE, MI-NORMAL-STATIC-VERDICT, MI-NORMAL-LIVE-VERDICT |

For proportional provider validation, the independent scope reviewer rejects any
reintroduction of feature/provider multiplication, custom runner scheduling,
background observation, scenario timeout machinery, repair-after-each-result loops,
or unjustified replay. Review the number of unproved boundaries, public canary
sequence, provider support prerequisites, cleanup, and critical-path estimate before
admission. A product command uses its native lane/result lifecycle; no planning
budget becomes an agent-session timeout or a substitute result. Host finite-command
policy still controls which commands use the bounded runner.

The same reviewer also checks scheduling inside local suites: reject leaked
provider/agent caps, unjustified serial order or wave barriers, ignored economical
parallel modes/shards, and unproved fixture isolation. Review local and live host
contention together; a document revision does not invalidate accepted test credit.

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
