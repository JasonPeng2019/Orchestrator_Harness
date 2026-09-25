# Goal: finish the fixed-strategy memory-backed harness

## Outcome and authority

Finish and verify only the unaccepted fixed-strategy behavior in
`development/product/worktree_example`. Accepted STEP-01 through STEP-03 and the
accepted retrieval, trust, and template slices remain inputs, not assignments.
The [remaining-work specification](.plans/memory-backed-harness/specification/SPEC.md)
governs product behavior; the [four-lane execution plan](.plans/memory-backed-harness/PLAN.md)
and its standalone lane steps plus shared STEP-16 through STEP-18 proof govern implementation. The
[archived predecessor](.plans/archive/2026-09-24-pre-remaining-replan/) has no
execution authority. `HANDOFF.md` records current native state, not a second plan.

## Resume point

The implementation run is paused for transfer to another machine. No native
lane-ROOT or repository-harness worker may be treated as live on resume; start
with read-only reconciliation and fresh role resolution.

The shared four-lane base is
`cc5b4f2d03626b393581c231303f5d79a4627cf2`. STEP-04 remains accepted
history at `a64ebfa9135960ad817752d447588feb5d782d80` and must not be reopened.
Lane 1 has closed STEP-05-1 and accepted the STEP-06-1 identity plus
freshness/procedure/compact slices through
`a1d07123422459293edcc90299faa0b2a9a3f003`; its separate STEP-06-1
privacy/credential-containment slice remains.
Lane 2 has accepted STEP-06-2 through STEP-08-2, closed STEP-12-2, and accepted
the bounded STEP-11-2 source-native receipt slice through
`fa0c32689fec57d1dd0240dcc96e3cc6aacb7340`; its lane-1 usage join and native
attribution proof remain pending. Its STEP-13-2 candidate
`288632862280a88676712137c0ffba065a8e16df` is preserved but unaccepted; its
fresh reviewer was stopped before producing a RESULT.
Lane 3 is accepted through `2e3ae85dfbbb05aaec10acee9fc106cd86857d3f`
and waits for its exact lane-1 joins. Lane 4 is accepted through
`871f21bd1b228a0279d6270d4c2054afcfd862b3` and waits for lane-1 interfaces.
`HANDOFF.md` holds the live run IDs and verification details. Product `main` at
`e2bd6bd` has two pre-existing setup-installed hook edits; preserve them.

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
are detached worktrees of `references/harness-single` at `5134f6c`; expand that
source only for a reproduced run-blocking defect or explicit user instruction.

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

## Boundaries and completion

Do not build another launcher, scheduler, reviewer, evidence ledger, or planning
tier. Do not run a benchmark or implement the learned selector. Do not push,
deploy, or publish outside an authorized synthetic Atlas namespace without a
separate user request. Completion requires the integrated candidate to satisfy
the remaining specification at its local, live-service, and native boundaries,
preserve accepted work, and clean owned resources. Close with
`benchmark execution: deferred/not run` and
`learned selector: deferred/not implemented`.

Every ROOT has a model-invocable `churn-watcher` skill. Invoke it whenever the
same repair or acceptance target has taken three or more implementation,
review, or correction tries. It validates the criticism chain, identifies the
shared failure mechanism, rejects reviewer overreach, and requires one bounded
root-cause correction plus preservation tests instead of serial symptom patches.
