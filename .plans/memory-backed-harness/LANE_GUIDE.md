# Four-lane execution guide

## Authority and status

[PLAN.md](PLAN.md) is the execution index; the [remaining-work specification](specification/SPEC.md) and its governing product documents retain product authority. The numbered files in the four [steps](steps/) lane folders are complete implementation assignments when read with [NORMAL_OPERATION_ACCEPTANCE.md](NORMAL_OPERATION_ACCEPTANCE.md). That policy governs validation breadth and repair-versus-document disposition; [KNOWN_ISSUES.md](KNOWN_ISSUES.md) is the monotonic register for deferred findings. Each lane step identifies its derivative original in [source-steps](source-steps/) for provenance and the [old-to-new coverage audit](COVERAGE_AUDIT.md). Those originals remain intact but are not needed to execute a lane step and have no separate authority. [STEP-16–18](verification/) are shared post-merge proof, not coding lanes. Accepted STEP-04 is in [finished history](../finished/memory-backed-harness/steps/STEP-04-apc-child-produces-reviewable-proposal.md).

The four lanes were paused for this policy revision with no live subordinate controller/provider accepted as running. Preserved candidate commits and worktrees remain evidence, not accepted tips. Relaunch uses fresh native processes and fresh repository-harness identities from each lane's authoritative accepted tip; product main at e2bd6bd and its two pre-existing setup-installed hook edits are not lane bases or cleanup targets.

## Master-ROOT and lane-ROOT hierarchy

Master-ROOT is the current top-level Codex session and the manager of all four plan lanes. Master-ROOT launches one lane-ROOT per lane through Codex's native subagent launcher. The repository multi-agent harness must not launch, resume, replace, or supervise these lane-ROOTs. Master-ROOT assigns their lane boundaries, monitors their progress, coordinates interface changes, owns the checkpoint and final integration worktree, and makes cross-lane and final acceptance decisions.

Each lane-ROOT is a native Codex subagent launched with model `gpt-6-sol` and `reasoning_effort=max`. It is the persistent manager for exactly one plan lane. It operates that lane's repository harness, breaks the standalone lane steps into bounded assignments, launches and manages the lane's worker/test/reviewer/correction subagents, classifies findings under the normal-operation policy, maintains one authoritative tested lane tip, and reports pins, repair-required blockers, and documented-only issues to master-ROOT. A lane-ROOT neither manages a peer lane nor writes in the integration worktree.

The repository harness has a one-persistent-manager-per-active-epoch contract. Create four unique harness roots/configurations, runtime roots, active epochs, manager queues, and worktree namespaces, one for each lane-ROOT. All four harnesses must use the same frozen harness source revision and the same [.plans/SUBAGENT_ROLE_MODEL_MAPPING.json](../SUBAGENT_ROLE_MODEL_MAPPING.json); do not fork the harness implementation or copy and drift the mapping. Each lane-ROOT resolves that shared mapping independently before launching a subordinate role. The mapping governs only the sub-subagents inside the four lane harnesses; it does not govern or provide fallback for the lane-ROOTs themselves. No active epoch, runtime state, manager queue, lane identity, or product worktree is shared between lane-ROOTs.

## Parallel worktrees and ownership

Run at most four plan lanes concurrently, one under each lane-ROOT. Each lane-ROOT's isolated harness manages that lane's coding branch/worktree and subordinate lifecycle. Keep one writer for overlapping lane-owned files and one authoritative tested tip per plan lane; subordinate test or review work cannot create a competing implementation tip. Master-ROOT owns scope across lanes and integration in a separate product Git branch/worktree where no lane worker writes. Do not reuse a live or retired harness identity, branch, worktree, epoch, or runtime. Resolve current subordinate development roles at each harness launch. Product-managed APC and workers still run through the candidate product harness when their assigned behavior requires it.

| Plan lane | Native manager | Folder | Exclusive product source ownership |
| --- | --- | --- | --- |
| 1 — domain and durable state | lane-ROOT 1 | [lane-1-domain-state](steps/lane-1-domain-state/) | memory_harness preparation, APC/search timing, context, privacy, runtime, contracts, store, config, and narrow snapshot/domain services |
| 2 — product harness and setup | lane-ROOT 2 | [lane-2-product-harness](steps/lane-2-product-harness/) | memory_harness native bridge/child adapters plus product harness handoff, bootstrap, resume, launch, review, setup, installed payload, operator entrypoint |
| 3 — experience and EverOS | lane-ROOT 3 | [lane-3-experience-everos](steps/lane-3-experience-everos/) | memory_harness experience and EverOS adapters |
| 4 — Atlas and procedures | lane-ROOT 4 | [lane-4-atlas-procedures](steps/lane-4-atlas-procedures/) | memory_harness Atlas and procedure services/adapters |

Focused tests follow the implementation they exercise, with distinct test modules when several lanes exercise one behavior. A lane-ROOT may run another lane's selector read-only but neither it nor its harness subagents may edit that lane's files. Master-ROOT owns cross-lane joined tests in the integration worktree. An unlisted shared file gets one explicit owner from master-ROOT before editing; a second lane-ROOT requests the change from that owner. One lane may define an interface while another consumes it, but they do not edit the same product file. No new controller, file-ownership database, receipt layer, or reviewer is needed.

## Review and issue disposition

Every worker and reviewer card names its standalone step and [NORMAL_OPERATION_ACCEPTANCE.md](NORMAL_OPERATION_ACCEPTANCE.md). Required evidence is proportionate: one ideal supported path, affected legacy/all-off preservation, one credible regular recovery when central, and focused critical-invariant checks. Reviewers return `REVISE` only for a reproduced failure of normal operation, supported recovery, compatibility, or a critical invariant. They report all other confirmed issues for addition to [KNOWN_ISSUES.md](KNOWN_ISSUES.md) and return `SHIP` when required behavior otherwise passes. A documented-only issue launches neither a correction worker nor a second review. A missing dependency or required normal-path proof returns `BLOCK` for only that claim; it is never reported as passing.

## Numbering and source coverage

A suffix identifies the writer: STEP-07-1 is lane 1's domain work, STEP-07-2 is lane 2's harness work. The prefix groups related behavior; it is not a serial execution barrier. A numbered behavior may appear in several lane folders only where each file has a distinct deliverable, tests, and owner. The behavior closes only when all assigned slices pass together on the merged candidate. Each new step states its own scope, rules, evidence, and recovery; do not consult the old source documents to execute it.

STEP-04 and the first STEP-05 Level 0 slice are accepted inputs. Preserve them. Do not relaunch APC implementation or requalify accepted adapter/trust work absent a concrete defect exposed by a remaining consumer.

## Asynchronous checkpoint

All four lane-ROOTs start their isolated harnesses from the same accepted product baseline. Lane-ROOT 1 publishes the exact task/plan/context/dispatch/outcome and effect/usage identity and status meanings that other lanes consume; record interface changes in the relevant lane step and report them through master-ROOT before a consumer relies on them. Initial downstream adapter tests may use deterministic fixtures, but a fixture cannot prove the integrated harness path.

Each lane pins a tested checkpoint commit when it reaches its own target:

1. Lane 1: STEP-05-1 through STEP-08-1, plus the published outcome/effect/usage interface needed downstream.
2. Lane 2: STEP-06-2 through STEP-08-2 and STEP-12-2, including the actual launched-payload contract, tested against lane 1's published contract or a faithful fixture; the joined native path is checked in integration.
3. Lane 3: independently testable STEP-09-3/STEP-10-3/STEP-13-3 adapter operations and fault cases; no premature outcome-linked STEP-09/10 completion claim.
4. Lane 4: independently testable STEP-10-4/STEP-13-4 exact remote identity, readback, fault, and service-gate cases; no live Atlas claim.

A lane-ROOT with a passing checkpoint commits its bounded result, reports the exact pin and direct checks to master-ROOT, and continues its remaining assignments. It does not wait for another lane. The pinned commit remains a fixed checkpoint ancestor while the branch advances. If a published interface or consumed input changes, rerun its directly affected checks and repin the affected checkpoint. If a lane exhausts independent work before a required interface exists, its lane-ROOT reports that exact dependency; the no-wait rule does not license guessed records or false PASS.

When all four valid pins exist, master-ROOT merges those exact commits in a dedicated integration branch/worktree and runs focused cross-lane context→native launch→outcome and adapter-interface checks. This checkpoint attempt is required once all pins exist, but it is not a barrier for coding lanes or a release claim. If a pin is missing, master-ROOT defers the attempt while ready lanes continue. If the attempt fails, master-ROOT returns only an exact repair-required defect to its owning lane-ROOT and keeps unaffected lane work; documented-only findings are registered without holding the checkpoint. If it passes, retain the integration commit; later branch commits are merged as deltas. Do not mutate product main or the pinned lane commits to make the attempt pass.

## Final integration and proof

The final merge is required after each lane-ROOT finishes its assigned STEP-05–15 implementation and passes the direct checks possible on its own branch. A lane-ROOT reports cross-lane checks that require unmerged code as pending, never PASS; those are not a reason to delay the merge. Master-ROOT merges the four remaining lane tips into the dedicated integration worktree, verifies exact scope and changed-file ownership, and runs the pending joined checks there. A repair-required failure returns the exact defect to its owning lane-ROOT for a narrow branch fix and revised merge; a documented-only failure enters the known-issues register without a correction. Only the joined candidate can close split behavior. Candidate bytes and configuration are then pinned for [STEP-16](verification/STEP-16-pinned-candidate-passes-local-checks.md). [STEP-17](verification/STEP-17-live-atlas-eligibility-is-proven.md) proves actual scoped Atlas eligibility on disposable data. [STEP-18](verification/STEP-18-native-candidate-lifecycle-is-proven.md) proves the candidate harness's all-off and enhanced native lifecycle; all-off may proceed while Atlas is unavailable, while enhanced consumes STEP-17's eligible fixture. Master-ROOT owns final review, fixture cleanup, and acceptance.

Each lane runs only focused direct checks for its changed inputs. STEP-16 runs the curated integrated normal-operation and critical-invariant gate, with any broader suite treated as best-effort diagnostic evidence whose failures are classified. Missing live service or native provider readiness leaves its dependent proof open, not passing. Preserve accepted product work, ordinary legacy cards, isolated resources, and the no-benchmark/no-learned-selector boundary.
