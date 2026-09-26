# Goal: finish the fixed-strategy memory-backed harness

## Outcome and authority

Finish and verify only the unaccepted fixed-strategy behavior in
`development/product/worktree_example`. Accepted STEP-01 through STEP-03 and the
accepted retrieval, trust, and template slices remain inputs, not assignments.
The [remaining-work specification](.plans/memory-backed-harness/specification/SPEC.md)
governs product behavior; the [four-lane execution plan](.plans/memory-backed-harness/PLAN.md)
and its standalone lane steps plus shared STEP-16 through STEP-18 proof govern implementation. The
[normal-operation acceptance policy](.plans/memory-backed-harness/NORMAL_OPERATION_ACCEPTANCE.md)
governs review strictness, proportionate validation, and whether a discovered
issue requires repair or documentation in
[KNOWN_ISSUES.md](.plans/memory-backed-harness/KNOWN_ISSUES.md). The
[archived predecessor](.plans/archive/2026-09-24-pre-remaining-replan/) has no
execution authority. `HANDOFF.md` records current native state, not a second plan.

## Resume point

The implementation run was paused by the user on 2026-09-26. No native
lane-ROOT or repository-harness worker remains live. Read-only scans show lanes
1 and 2 with empty active-lane registries and no orphaned leases; lanes 3 and 4
have no active epoch. On resume, reconcile first, resolve every role fresh, and
use ChatGPT subscription authentication without adding an API key.

The current authoritative accepted tips are lane 1
`70366af368940958aaae2373eb8d21add208227d`, lane 2
`3e0f7f18f937a33c1fa817ea81ead5f1d3753af6`, lane 3
`953bf2ea30f0a56fd68514787cf1582957ba41ff`, and lane 4
`871f21bd1b228a0279d6270d4c2054afcfd862b3`. Master integration
`integration/checkpoint-20260925` is pinned at
`9d9ca48cb7ce65e2b66b110ca5bf35601966582d`; it includes the accepted lane-1
STEP-08 provider and lane-4 privacy consumer join and passed the focused joined
checks recorded in `HANDOFF.md`.

Two current unaccepted worktrees are deliberately preserved. Lane 1 STEP-09
candidate `45e8e225089bd8d09ae689726a6fddfa5f742d9e` has a valid writer PASS
RESULT and no review verdict; resume it with one fresh exact-tip policy review,
not a new implementation. Lane 2 branch
`lane2/ki007-supersession-consumer-01` contains a transfer-only checkpoint of
the interrupted STEP-08/KI-007 consumer and has no RESULT or acceptance; resume
it as incomplete work on the exact integrated base and rerun its required
normal-path evidence before review. Lane 3 waits for lane 1's accepted STEP-09
effect interface; lane 4 waits for the STEP-10/11/13 lane-1 interfaces.

Only the current integration branch and those two active candidate branches are
transfer refs. Retired reviewer, correction, harness-repair, and historical
worktree branches are redundant and must not be recreated as transfer
submodules. Product `main` at `e2bd6bd` and its pre-existing setup hook edits
remain outside the lane bases and cleanup scope.

## Execution

Master-ROOT owns cross-lane scope, integration, live operations, and final
acceptance. Follow the [lane guide](.plans/memory-backed-harness/LANE_GUIDE.md).
MASTER-ROOT uses the Codex CLI's native subagent manager to launch and manage
four top-level `gpt-6-sol`/`max` lane-ROOTs, one per plan lane. MASTER-ROOT does
not use the repository harness itself. Each lane-ROOT exclusively uses its own
isolated frozen `harness-single` process to launch and manage that lane's
sub-subagents. Native lane-ROOT identity reuse never permits harness, runtime,
worktree, or acceptance-state sharing. The four lane-ROOTs use separate
product manager roots, runtime roots, active epochs, queues, lane identities,
worker worktree namespaces, and harness configurations. They share only the
frozen harness source revision and role mapping. Each lane pins its checkpoint
and continues without waiting; Master-ROOT integrates all four pins when
available, then merges lane tips in a separate integration worktree before
shared proof. The four outer harness roots are
`development/dogfood/lane-harnesses/lane-1` through `lane-4`, paired with
`development/product/lane-roots/lane-1` through `lane-4`. The candidate product
harness remains separate and is used only for product-owned APC and worker
execution. Every new native task card names the absolute product root, plan, and
assigned standalone lane STEP file because product worktrees do not contain
top-level `.plans`.
Keep each outer harness's existing nonempty `acceptance_criteria`, `deliverables`,
and `reason_for_acceptance_and_deliverables` fields; they are the task contract,
not another evidence layer.

Resolve development roles from the current
[role mapping](.plans/SUBAGENT_ROLE_MODEL_MAPPING.json) with
`development/test-tools/resolve-role.py` before each launch; do not carry
forward a prior run's binding or silently substitute. Product APC uses its separate explicit lower-capability
`apc_adaptation_binding`, with no named default. All four outer dogfood harnesses
derive from frozen `references/harness-single` at `5134f6c` plus the reviewed
run-blocking controller/provider lifecycle repair `cfca0458`, propagated to the
exact lane harness commits recorded in `HANDOFF.md`. Expand that source no
further absent another reproduced implementation-blocking defect or explicit
user instruction.

Before declaring Atlas, MongoDB, or DeepInfra credentials unavailable, check
ignored `.secrets/creds/`. Load only values needed by the authorized process;
for Atlas, use `MEMORY_HARNESS_ATLAS_URI`, an isolated
`MEMORY_HARNESS_ATLAS_LIVE_DATABASE`, and explicit live-test opt-in. Map any
DeepInfra key only to required EverOS service variables. Never copy values into
cards, prompts, plans, logs, or committed configuration. Credential files alone
do not prove service, index, namespace, network, or provider readiness.

Execute the new plan's dependency order within and across lanes with focused
step checks, scoped repair, and one pinned integrated candidate for final local,
live Atlas, and native proof. A behavior defect blocks only its affected outcome and consumers;
administrative imperfections cannot overturn passing behavior.

Every new worker and reviewer card must name the normal-operation acceptance
policy alongside its standalone STEP file. Reviewers request repair only for a
reproduced normal-use, regular-recovery, compatibility, or critical-invariant
defect. They report other confirmed issues for the lane-ROOT/Master-ROOT to add
to `KNOWN_ISSUES.md`, then return `SHIP` when required behavior is otherwise
met. A documented-only finding never launches a correction or re-review.

## Boundaries and completion

Do not build another launcher, scheduler, reviewer, evidence ledger, or planning
tier. Do not run a benchmark or implement the learned selector. Do not push,
deploy, or publish outside an authorized synthetic Atlas namespace without a
separate user request. The first completion milestone is the minimal MVP: the
integrated candidate performs the remaining ideal normal product behavior at its
local, live-service, and native boundaries, preserves the policy's critical
invariants and accepted work, cleans owned resources, and records every known
deferred issue. Documented-only edge cases do not gate that MVP milestone under
the normal-operation acceptance policy.

After the MVP milestone passes STEP-16 through STEP-18, keep the run open for a
post-MVP deferred-repair pass. Work through `KNOWN_ISSUES.md` monotonically and
repair every actionable code issue that was deferred only because it was an
edge, theoretical, unsupported, or non-product-use case. Give each repair one
owner, focused evidence, and a fresh review; integrate it without reopening the
MVP's accepted product meaning. Resolve non-code environment/access entries with
concrete evidence rather than inventing a code change. The full active goal is
complete only after this deferred-repair pass is exhausted. Close with
`benchmark execution: deferred/not run` and
`learned selector: deferred/not implemented`.

Every ROOT has a model-invocable `churn-watcher` skill. Invoke it whenever the
same repair or acceptance target has taken three or more implementation,
review, or correction tries. It validates the criticism chain, identifies the
shared failure mechanism, rejects reviewer overreach, and requires one bounded
root-cause correction plus preservation tests instead of serial symptom patches.
