# Harness v2 STEP-006 Tier-2 Closure Plan

## Plan contract

| Field | Value |
|---|---|
| Plan ID | `HARNESS-V2-STEP-006-TIER2-CLOSURE` |
| Execution-plan revision | `T2-R4` |
| Status | `VALIDATED` |
| Reviewed execution snapshot | SHA-256 `CF918849948BBACD40297A5E2A389B975231B5AC44DD06F87558E091F2DFF429` |
| Plan writer and final decision owner | `/root` |
| Topology | Level 2: one delivery owner plus one purposeful read-only reviewer |
| Execution reviewer allocation | Codex native `spawn_agent`; model `gpt-5.6-terra`; reasoning effort `xhigh`; reuse the same reviewer with native `followup_task` at Checkpoint B when available |
| Allocation authority | Direct user instruction after T2-R4 review; this selects the concrete implementation of the already-reviewed single read-only reviewer role and does not add a role or lane |
| Prospective scope | Only the unfinished STEP-006 acceptance tail |
| Starting product coordinate | Accepted joint commit `a8d0382073377f3b7fc49ea426a30ef8d8429951` from decisions 707/709 |
| Supersession boundary | This plan replaces only the prospective unfinished route in `master_planning/harness-v2-tier4/addendum-3/`. It does not rewrite that package or its history. |

This is a compact Level-2 plan, not a reduced formal Level-4 package. The work
remaining is coherent enough for one delivery owner, but the previous acceptance
incident shows that its test oracles and native-evidence classifications need one
fresh independent review. No second writer, lane hierarchy, plan compiler, custom
runner, scheduler, observer, or matrix is justified.

## Outcome, authority, and protected progress

The outcome is to finish the remaining STEP-006 work truthfully and hand back one
terminal result: full acceptance, product-correct/native-incomplete, or an exact
product failure. Completion of the execution route does not convert unavailable
native evidence into PASS.

The following boundaries are fixed:

- STEP-001 through STEP-005 and their accepted product, review, integration, and
  test evidence are finished inputs. Do not edit their plans, rerun them, revert
  them, or reopen their decisions.
- Start from accepted joint commit `a8d0382073377f3b7fc49ea426a30ef8d8429951`.
  Decisions `ROOT-PRODUCT-INTEGRATION-707.json` and
  `ROOT-ASSET-INTEGRATION-709.json` accepted the intervening product and asset
  changes; do not reconstruct or revalidate them. Before writing, read back the
  object, the selected working coordinate, and a clean or explicitly inventoried
  diff.
- Pause record
  `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/PAUSE-SERIES13-REVIEW-RETURN-827.json`
  identifies the unaccepted Series13 changes as ignored/uncommitted custom-control
  files layered on `a8d0382...`. Preserve those files as history but do not integrate,
  repair, review, qualify, or execute them. The accepted tracked `a8d0382...` commit
  itself is protected input, not discarded control work.
- Preserve compatible retained native evidence claim by claim. A plan rewrite or
  regenerated view does not invalidate evidence; only a changed consumed product,
  hook/binding, provider/profile boundary, record contract, or relevant external
  state does.
- Do not commit, push, publish, deploy, or launch a provider unless current user
  authority at execution time expressly covers that action. This planning request
  authorizes the plan and its four planning reviews only.

### Binding sources for the unfinished work

| Source | Binding contribution |
|---|---|
| Active user instructions, September 18, 2026 | Use a new Tier-2 plan; touch only unfinished work; completed work is immutable; finish quickly without the oversized acceptance apparatus. |
| `new_harness_docs/master_docs/harness-master-spec.md`, Part XIX.1 | Real Codex, Claude Code, and Qwen Code native verification claims. |
| `new_harness_docs/tweaks/bounded-invalid-result-correction.md` | Five-correction limit, same-session native resume, cleanup/lease ordering, exact terminal behavior, and one real supported-CLI integration. |
| Accepted commit `a8d0382...` and ROOT decisions 707/709 | Actual accepted controller, process-boundary correction, assets, public CLI, records, hooks, tests, and provider bindings under test. |
| Existing product-native evidence and `harness-single/docs/*-headless-hook-proof.md` | Retained credit only for the exact claims and dependencies each artifact actually establishes. |
| `master_planning/harness-v2-tier4/addendum-3/plan-workflow.md` version 3.7 history | Accepted starting coordinate and the decision to retire the custom 96-case control path; it is not a requirement to execute that formal package. |

The earlier exhaustive live-test document is background for required behavior, not
authority to revive its 96-cell implementation. The current user direction changes
the unfinished acceptance method while retaining the product contract and honest
native gaps.

## Acceptance claims

### A. Deterministic controller boundary

Add exactly two candidate-observing cases to
`orchestrator_harness/tests/test_addendum3_product.py` unless inspection finds an
already-equivalent candidate-observing test:

1. Attempts one through five leave invalid/missing results and produce exactly five
   corrective prompts. Provider attempt six uses the same native session and returns
   a valid result. The real controller reaches `review_pending`, emits no premature
   terminal no-result event, retains the same lane/run/provider identity, proves each
   exited process boundary clean before continuing, holds the lease between attempts,
   and releases it only after the valid-result cleanup boundary. The test reads the
   complete durable header and attempts 1–6, including attempt-specific command,
   transcript/stderr, result-validation, and cleanup facts.
2. Six consecutive invalid/missing exits produce exactly five corrective prompts,
   no sixth prompt, and exactly one `provider_exited_no_result`. The real controller
   retains lane/run/provider/native-session identity, keeps the lease through the
   correction sequence, proves cleanup before each continuation and before final
   release, and records the complete durable header and attempts 1–6 with the same
   attempt-specific facts.

Both cases read all five emitted correction-prompt files and assert the current
`lane_id`/`run_id`, `result/v1`, nonempty `summary`, allowed `PASS`/`FAIL`/`BLOCKED`
outcome, `evidence`, `completed_at`, and `content_hash` requirements. They assert
exact correction/result/terminal event counts and lease acquire/hold/release order,
not only final labels.

Both tests must call the candidate controller and inspect its durable state/events
and adapter invocations. A constructed array checked only by
`candidate_observations.assert_bounded_result_correction` is not acceptance evidence
for these two cases.

### B. Native claims

Build a claim ledger before reviewer Checkpoint A and before any external launch.
Credit an existing observation only when its candidate, hook/binding,
provider/profile, command path, schema, and claimed behavior remain compatible. For
every selected fresh bundle, the ledger fixes its claim IDs, retained versus missing
evidence, immutable task/nonce, exact public command and lane sequence, maximum
provider-process count, serial dependencies, shared credential/configuration claim,
terminal predicate, cleanup/lease steps, wait-window calculation, and expected
product records. The ledger owns one of `PROVED`, `FAILED`, or `INCOMPLETE` for every
claim; unavailable authentication, provider capacity, or host support is
`INCOMPLETE`, never product failure and never PASS.

The mandatory claim set is:

- On each actual Codex, Claude Code, and Qwen Code managed boundary, account
  claim-by-claim for provider-specific PostToolUse delivery; Stop refusal while ROOT
  work is unresolved; Stop refusal while worker work is unresolved; Stop refusal for
  invalid/missing result; Stop permission for each valid `PASS`, `FAIL`, and `BLOCKED`
  terminal kind; and role-queue isolation. Compatible retained evidence may supply a
  claim; every remaining claim is folded into that provider's one bounded fresh
  bundle. This requirement does not create feature-by-provider coordinates or repeat
  already compatible proof.
- Establish dead/hung monitor recovery without restarting a deliberately stopped
  monitor, and serial exclusive-lease release/reuse. These are provider-neutral
  product paths: one compatible retained or fresh native observation may cover all
  providers only when source/dependency inspection proves that no provider adapter
  participates in the observed decision. Queue-role isolation is still explicitly
  accounted for in each provider bundle because Part XIX.1 binds it to actual
  provider execution.
- Satisfy bounded-correction test 8 with exactly one supported real CLI in a
  disposable Git worktree. It must use the adapter-built saved-session native resume
  path. In one existing automated integration test, use public setup/bootstrap, then
  explicitly bypass detached public `lane launch` for this correction case only:
  start one bounded test-local child process whose target installs a
  `unittest.mock` patch of the candidate result validator and then calls candidate
  `controller.run_controller(lane_id)`. The patch returns invalid exactly once for
  attempt one and then delegates to the real validator. Installing it inside the
  child preserves it on Windows spawn while letting the controller record the
  child's truthful independent PID. The child controller starts the real supported
  CLI through its real adapter, captures its real native session, and resumes that
  session for attempt two. After durable `review_pending`, the parent invokes the
  existing public completion-review acceptance path, waits for normal controller
  exit, joins the child within the predeclared full two-attempt window, invokes public
  retirement with the acceptance reference, and proves the child PID plus both exact
  provider boundaries gone. On window exhaustion the parent uses exact public
  force-stop for that lane, then joins and verifies cleanup; it never attempts to
  kill a test-host PID or a thread. The ordinary immutable provider canary or
  compatible retained evidence remains responsible for the public `lane launch`
  claim. This fixture changes no product source/public API, adds no persistent helper,
  operational runner, or observer, and has a maximum of two provider processes. Do
  not depend on a prompt persuading the model to fail. Fold this observation into an
  otherwise-required managed-provider bundle when possible; reviewer Checkpoint A
  must approve the concrete fault-injection code before allocation.
- Treat plain profile as one provider-neutral path unless source or retained evidence
  identifies a materially different provider-specific plain seam. Use compatible
  retained credit first; otherwise run one representative plain lifecycle. Add no
  provider multiplier merely because three provider names exist.

Every fresh provider/profile lifecycle reuses one shared canary contract: before
launch the delivery owner fixes an immutable harmless task and nonce, expected
lane/run/task-card identities, result schema/hash, expected native tool action or
other fixed evidence, prohibited side effects, and exact completion-review,
acceptance, retirement, record, and cleanup readbacks. Providers receive no
provider-specific task variant, and a structurally valid but task-unrelated result
cannot pass review.

## Ownership and delegation

| Role | Authority | Concrete responsibility | Terminal output |
|---|---|---|---|
| Delivery owner (`/root` or the later primary native Codex session) | Sole writer and final decision owner | Read back accepted inputs; author any test and narrowly required product correction; run focused checks; operate authorized public native commands; classify evidence; integrate the final coordinate; issue the final verdict | Exact changed files/diff identity, commands and results, claim ledger, cleanup facts, unresolved risks, final verdict |
| Independent reviewer (one read-only Codex subagent identity) | No writes, launches, live allocation, acceptance, commit, or push | Launch with Codex native `spawn_agent` using `gpt-5.6-terra` at `xhigh`. At Checkpoint A inspect the concrete tests/oracles and proposed native claim map; at Checkpoint B reuse the same identity with native `followup_task` when available and inspect the final diff, check results, raw product records, retained-credit decisions, and proposed verdict. | Evidence-backed findings or explicit no-issue result at each checkpoint |

The reviewer is one purposeful support lane, not a second implementation owner. Its
two assignments concern the same risk—false acceptance from faulty or excessive
oracles—and are separated so the delivery owner can correct the concrete draft
before external evidence is consumed.

The Checkpoint-A launch binding is:

```text
spawn_agent(
  task_name="step006_independent_reviewer",
  fork_turns="none",
  model="gpt-5.6-terra",
  reasoning_effort="xhigh",
  message=<complete read-only task card plus all source and candidate references>
)
```

`fork_turns="none"` is intentional because the native launcher requires a bounded
fork when overriding model/reasoning; the assignment message must therefore carry
the complete task card and sources. Checkpoint B uses native `followup_task` on
`step006_independent_reviewer` so it remains one subagent. If that native session is
unavailable, launch one fresh replacement with the same model/reasoning and include
Checkpoint A's findings, dispositions, retained evidence, and first unresolved
action. Do not launch this reviewer through frozen-harness or a CLI wrapper.

### Reviewer task card A: oracle and claim-map review

- **Objective:** identify a required behavior that the new tests or planned native
  observations could let remain broken, and identify any stronger-than-contract or
  duplicated evidence.
- **Scope:** the accepted controller and bindings; the exact test diff; Part XIX.1;
  `bounded-invalid-result-correction.md`; the retained-evidence ledger; public CLI
  entrypoints and record contracts.
- **Write authority:** none.
- **Checks allowed:** read-only source/diff inspection and already-produced test
  output; do not run product tests or providers.
- **Deliverable:** findings with file/line or record evidence, the smallest correction,
  retained claims, and explicit PASS/BLOCK for the planned evidence boundary.
- **Completion:** both deterministic cases and every native claim have a sound,
  proportional observation contract, or the unresolved gap is named.

### Reviewer task card B: final evidence review

- **Objective:** determine whether the proposed final classifications follow from the
  exact diff, focused checks, product-owned records, hook receipts, process cleanup,
  and retained evidence.
- **Scope:** only artifacts produced or credited by this plan and the unchanged
  requirements above.
- **Write authority:** none.
- **Checks allowed:** read-only artifact/source inspection; no replay or live launch.
- **Deliverable:** claim-level corrections or explicit no-issue result and PASS/BLOCK
  for the proposed terminal handoff.
- **Completion:** every PASS has direct evidence, every unavailable observation is
  INCOMPLETE, product failures are separated from support/test-control failures, and
  cleanup is accounted for.

If the reviewer returns a missing or malformed task result and native same-thread
resume is safe, request only the result correction with the precise validation
errors, at most twice, preserving its work. A third malformed result uses one fresh
same-role recovery assignment with the same `gpt-5.6-terra`/`xhigh` native launch
binding, carrying prior findings and the first unresolved action. A substantive
FAIL/BLOCK is adjudicated, not retried until PASS.

## Ordered execution route

### 1. Admit the accepted base and retained evidence

The delivery owner records the accepted `a8d0382...` commit/worktree/diff state and
prepares the claim ledger. It excludes only the paused ignored/uncommitted Series13
custom-control delta, not accepted tracked history. It maps each
retained native artifact to the exact claim and dependency set it proves; a broad
historical PASS label is not enough. No product/provider command runs in this stage.

### 2. Write and run the deterministic delta

The delivery owner adds the two tests in Acceptance A and initially runs only:

- the two new test methods;
- adjacent existing methods
  `test_invalid_result_uses_native_session_for_at_most_five_corrections` and
  `test_valid_result_wins_over_nonzero_provider_exit`; and
- Python compilation for changed Python files.

If these pass, run the enclosing
`orchestrator_harness.tests.test_addendum3_product` module once against the same
coordinate. Do not run the repository-wide suite for a test-only delta.

If a new test fails, compare the exact requirement, observed controller behavior,
and assertion before changing production code. Fix a faulty test at the test owner.
If the candidate has an actual bounded-correction defect, the sole delivery owner
may make the smallest controller/binding repair and run the changed tests plus tests
that directly consume the changed source. A repair that changes a public record,
adapter, lifecycle, or shared contract beyond the bounded-correction requirement
stops this route for Tier reassessment; it does not reopen STEP-001 through STEP-005
or trigger a blanket replay.

### 3. Collect reviewer checkpoint A and freeze the candidate

The reviewer performs task card A on the exact diff and claim ledger. The delivery
owner dispositions every finding with source evidence, applies the accepted changes,
and reruns only checks whose inputs changed. When the tests and evidence contract
pass, freeze one execution coordinate as accepted commit plus exact diff identity.
A commit may be created only under separate current authorization.

### 4. Execute only missing native observations

For each claim still unproved after retained-credit review, use the product's public
commands and its durable records. The sole exception is the reviewed child-installed
one-shot validator patch for the required real-CLI correction integration: public
setup/bootstrap precedes one bounded test-local child that installs the patch and
calls the real controller, and public completion-review/retirement follows
`review_pending` and normal child exit. It is a test-local fault injection with a
truthful controller PID, not an operational launcher. Do not build or use a runner,
scheduler, background observer, scenario-timeout service, prompt-made invalid
fixture, or feature/provider matrix.

Execution rules:

- Combine compatible claims into at most one managed qualification bundle per
  provider. The maximum fresh managed bundle count is therefore three, and retained
  evidence reduces it. A bundle is not permission for hidden repetition: before
  Checkpoint A its ledger row fixes every public command, lane transition, provider
  process, terminal predicate, and cleanup point needed by its unproved claims.
  Checkpoint A rejects an unbounded or unexplained internal sequence.
- Run the supported-CLI bounded-correction integration once, folded into one managed
  bundle when possible. Its one-shot injected-invalid path has exactly two provider
  attempts: initial real adapter launch and saved-session native resume. Its ledger
  fixes the controller-child start/PID, `review_pending` predicate, public
  completion-review, normal child exit, finite join, acceptance-referenced
  retirement, timeout force-stop, and exact child/provider cleanup. Run at most one
  representative plain lifecycle when its distinct profile seam remains unproved.
  Do not repeat a truthful terminal external result for confidence.
- Serialize external bundles because they consume shared user credentials,
  configuration, runtime records, and cleanup authority. Use a fresh disposable Git
  worktree/runtime for each incompatible state boundary and never the user's unrelated
  projects.
- Predeclare each public `watch --until-actionable --timeout <window>` value from the
  ledger's complete critical path: every maximum provider process in the bundle plus
  review/record transitions and cleanup margin. Use retained provider-duration
  evidence when compatible; otherwise record a conservative finite provisional
  window and its uncertainty before launch. For the correction integration, budget
  both provider attempts and both cleanup boundaries. A timeout is an operator wait
  boundary, not proof of nonprogress or a product verdict. Exhausting the full-bundle
  window ends that single authorized observation: run final `scan --no-write`, use
  `lane force-stop --lane-id <exact-id>` if the exact lane remains live, and verify
  recorded PID-plus-creation cleanup before releasing or reusing a lease. Successful
  containment yields `INCOMPLETE`; only product records or failed exact
  containment/cleanup that contradict a required product contract yield `FAILED`.
  No unchanged retry follows.
- Use the public bootstrap, launch, manager event, completion-review, acceptance, and
  retire routes. The delivery owner reads product records after terminal state; no
  second observer process is created.
- One launch/authentication/capacity/support failure makes that exact claim
  `INCOMPLETE` and ends that external attempt. Do not retry unchanged setup. A direct
  product contradiction is `FAILED` and enters the focused repair rule; continue only
  independent claims whose inputs remain valid.

### 5. Collect reviewer checkpoint B and decide

The independent reviewer performs task card B. The delivery owner applies supported
classification corrections without replaying unchanged tests or native observations,
then emits exactly one terminal handoff:

- `ACCEPTED`: deterministic product checks pass and every mandatory native claim is
  `PROVED` with cleanup accounted for.
- `PRODUCT_PASS_NATIVE_INCOMPLETE`: deterministic product checks pass, no product
  contradiction exists, and one or more mandatory native claims remain unavailable.
  Execution is finished, but STEP-006 is not reported as a full native PASS.
- `FAILED`: a required product behavior is contradicted after oracle adjudication.

The final handoff names the starting and final coordinate, exact diff, tests and
results, native claim ledger, retained-credit sources, provider/support/platform
gaps, cleanup/lease state, and any authority-limited next action. It stops there.

## Verification and acceptance design

| Activity | Necessity and observed boundary | Multiplicity | Proportionality and invalidation |
|---|---|---|---|
| Two controller tests | The accepted suite lacks direct candidate execution at both retry-limit edges required by the bounded-correction tweak. They observe controller calls, durable records/events, cleanup, leases, and lifecycle. | Exactly two distinct boundaries: valid after correction five, and exhaustion after invalid exit six. Existing neighboring tests are retained, not copied per provider. | Cheapest deterministic proof of provider-neutral behavior. A test-only edit invalidates only the new/adjacent test evidence, not accepted product work. |
| Enclosing test module | Detects interaction with neighboring controller/monitor behavior after the concrete delta passes. | Once per final local coordinate; rerun only after a consumed input changes. | Prior evidence records a 66-test focused suite completing in about 150 seconds; this is a cost basis, not a guarantee. No repository-wide replay is scheduled. |
| Managed native provider seam | Native hook invocation and CLI Stop behavior cannot be established by mocks. Provider bindings and native hook systems differ across Codex, Claude Code, and Qwen Code. Each provider row accounts for PostToolUse, both unresolved roles, invalid/missing result, every valid terminal kind, and queue-role isolation. | At most one pre-enumerated bundle for each provider lacking compatible credit; internal provider-process count is fixed in the reviewed ledger; no repeated run and no feature cross-product. | Reuse exact retained proof first and combine missing claims per provider. This preserves Part XIX.1 while replacing the 96-cell apparatus with at most three bounded bundles. |
| Provider-neutral native lifecycle claims | Monitor recovery/refusal and lease reuse require real native/process state but share a product path when inspection proves no adapter participation. | One compatible native observation per actual distinct source path; multiply only if inspection proves adapter participation. | Avoids falsely treating provider names as a behavior dimension while retaining evidence for real native semantics. Queue isolation remains accounted per provider as required above. |
| Real correction integration | Required test 8 explicitly needs a supported real CLI and saved-session native resume. | Exactly one supported CLI and two provider attempts: public bootstrap, test-local child running the real controller/adapter, then native resume; finite process join and exact cleanup. | Fold into a managed bundle; the child installs the reviewed one-shot validator patch inside its own process, preserving a truthful controller PID without product changes, prompt randomness, persistent helpers, or retry-until-failure behavior. Ordinary canary evidence separately proves public detached launch. |
| Plain profile | Needed only for a distinct managed-vs-plain path not already proved. | Zero with compatible credit; otherwise one representative unless a provider-specific plain branch is demonstrated. | Cheapest adequate profile evidence; no automatic three-provider multiplication. |

There is no substantial matrix: claims are grouped by real implementation seam, live
resources serialize, and every pre-enumerated native subcase runs once. Matrix-runner
controls are therefore inapplicable. The expected critical path is the deterministic
delta and its review, followed by zero to three missing managed bundles and at most
one plain bundle. Bundle count is not used as a proxy for command count: the reviewed
ledger supplies the exact provider-process count and full-path time budget. External
duration remains unknown until the retained-evidence map and provider-duration
records are read; the plan makes no wall-clock promise.

Reassess the topology before continuing if a repair changes a shared public contract,
requires a second implementation writer, or reveals more than one previously unknown
native seam whose interactions cannot be held by the delivery owner. Provider slowness
or a truthful INCOMPLETE result alone is not an escalation trigger.

## Planning review

All planning reviewers inspect the same execution-plan snapshot, the active user
instructions, repository rules, the project-topology rules, Part XIX.1, the
bounded-correction tweak, accepted joint commit `a8d0382...`, decisions 707/709/820
and pause827, retained native proofs, and relevant public CLI/test source. Reviews
are read-only and run no product tests or providers.

### Initial `T2-R1` review and writer dispositions

| Group | Reviewer | Initial verdict | Findings and writer disposition in `T2-R2` |
|---|---|---|---|
| SCOPE_AUTHORITY | `/root/v37_scope_authority` | BLOCK | `SA-T2-01` ACCEPT: corrected base to accepted `a8d0382...` and excluded only pause827's ignored/uncommitted delta. `SA-T2-02` ACCEPT: every provider bundle now accounts for queue isolation and each valid terminal kind. `SA-T2-03` ACCEPT: final plan acceptance refreshes `HANDOFF.md` to this route without rewriting history. |
| TOPOLOGY_SIMPLICITY | `/root/v37_topology_simplicity` | PASS | No initial finding. Final carry-forward is required because the accepted coordinate, claim detail, and resource ledger changed without changing the Tier-2 ownership graph. |
| VERIFICATION | `/root/v37_test_scope_audit` | BLOCK | `V-01` ACCEPT: both tests now inspect all prompts, complete ledgers, event counts, and lease order. `V-02` ACCEPT: every fresh lifecycle uses one immutable task/nonce and exact independent review/readback contract. |
| EXECUTION_RESOURCES | `/root/v37_execution_resources` | BLOCK | ACCEPT: bound a test-local one-shot validator fault injection with two real provider attempts; required exact per-bundle command/process/dependency/cleanup/time fields before Checkpoint A; full-path finite windows end in scan/exact force-stop and `INCOMPLETE` after successful cleanup, with no unchanged retry. |

The focused `T2-R2` reviews passed SCOPE_AUTHORITY, TOPOLOGY_SIMPLICITY, and
EXECUTION_RESOURCES. VERIFICATION passed `V-01` and `V-02` but found that a
parent-process mock cannot affect detached public `lane launch`. `T2-R3` moved the
real controller under an in-process patch; SCOPE_AUTHORITY, TOPOLOGY_SIMPLICITY, and
VERIFICATION approved that observation contract, but EXECUTION_RESOURCES found that
a test thread would record the test-host PID and make public retirement/force-stop
unsafe. `T2-R4` accepts the smallest correction: a test-local child installs the
patch and runs the real controller with its own truthful PID; the parent performs
bounded public review, exit, retirement or exact timeout force-stop, join, and
cleanup. Ordinary canary evidence retains responsibility for public detached launch.

### Final `T2-R4` binding

| Group | Reviewer | Reviewed revision | Evidence | Verdict |
|---|---|---|---|---|
| SCOPE_AUTHORITY | `/root/v37_scope_authority` | `T2-R4` / `CF918849...` | PASS carry-forward: accepted `a8d0382...` base, completed-work boundary, claims, authority, classifications, and stopping point remain correct. | PASS |
| TOPOLOGY_SIMPLICITY | `/root/v37_topology_simplicity` | `T2-R4` / `CF918849...` | PASS carry-forward: the child is private test-fixture mechanics; one writer/reviewer topology and change-locality boundary remain unchanged. | PASS |
| VERIFICATION | `/root/v37_test_scope_audit` | `T2-R4` / `CF918849...` | PASS: prompt/ledger and sentinel findings remain resolved; child-installed injection preserves the real CLI/session oracle and exact cleanup without extra multiplicity. | PASS |
| EXECUTION_RESOURCES | `/root/v37_execution_resources` | `T2-R4` / `CF918849...` | PASS: truthful child PID resolves retirement/force-stop; ledger, full-path budgets, serial resources, timeout classification, and no-matrix findings remain approved. | PASS |

Plan review verdict: `PASS`. All four distinct reviewers approved execution snapshot
`T2-R4` / `CF918849...`; every material finding is dispositioned. `/root` accepts this
plan. This approval-log and status update changes no reviewed execution instruction.
The later user-directed `gpt-5.6-terra`/`xhigh` native-launch allocation concretizes
the already-approved single reviewer role without changing its authority, topology,
evidence duties, or resource count.
`/root` refreshes `HANDOFF.md` so its next action points to this compact plan while
preserving the old v3.7 pause facts as history.

## Execution handoff

Planning is the only currently authorized action. Do not resume PAUSE827, launch
providers, modify the product, run product tests, commit, push, or publish from this
planning turn. A later executor must re-read current user authority before Stage 1
and again before external Stage 4. Once authorized, the accepted deliverable is only
the STEP-006 result above; the executor stops after the final handoff and does not
revive the formal Tier-4 workflow or perform optional broader campaigns.
