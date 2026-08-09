---
name: plan-harness-workflow
description: "Author a complete multi-agent execution plan from a product spec, reference implementation plan, acceptance spec, and user-selected agents. Use only when explicitly invoked to design a workflow for the current Portable Harness Repo; compose code modules into a small number of coherent large feature steps, apply the full QA lane cycle once per large step, prefer a valid singleton lane over unnecessary parallel fan-out, preserve singular orchestrator planning, serial production coding, bounded disjoint test/documentation work, and an explicit low-overhead fast lane for strictly test-only corrections. Plans must use proportionate gates: full review for production risk, one batch/reconciliation per accepted production repair, and only deterministic eligibility checks plus exact affected-ID reruns for safe fixture corrections. Preserve native scan/wait/ack operation and the fixed execution-plan template. This skill plans but never executes work, launches agents, edits product code, or runs the generated workflow."
---

# Author a Portable Harness workflow

## Hold the boundary

Produce one execution-plan document. Do not execute the plan, launch or call agents, edit product code, run project tests, start the harness, create runtime state, or perform any loop described in the plan. Reading inputs, inspecting the repository read-only, writing the plan, and running the bundled plan validator are the only allowed actions.

Treat the reference implementation plan as the complete outcome contract, not necessarily the best decomposition. Never drop, weaken, silently reinterpret, or invent product scope. Use the product and acceptance specs to detect contradictions or ambiguity; surface those issues instead of guessing or silently expanding the reference plan.

## Collect inputs

Require:

- Product spec path.
- Reference implementation plan path.
- Final or acceptance spec path, or an explicit statement that the product spec contains it.
- Concrete agent choice for each role: orchestrator/planner-executor, coder-main, reviewer-main, doer-main, and final-reviewer.

Accept an optional output path and optional overrides for `scope_policy`, `stall_threshold`, `gap_scope`, and `final_full_verification`. Default `final_full_verification` to `true`.

If any required input or role is missing, ask one consolidated question that names all five roles separately, then wait. Do not select default agents. The user chooses agent implementations only; the skill decides the initial pool sizes, decomposition, conceptual splits, and serial flow. Record an explicit user override separately if the user later changes a skill decision. Default the output to `plans/<product-slug>/EXECUTION_PLAN.md`.

## Read authoritative material

Read, in order:

1. The supplied product, reference-plan, and acceptance files.
2. [references/execution-plan-template.md](references/execution-plan-template.md).
3. [references/current-portable-harness.md](references/current-portable-harness.md).
4. The live `stable-general-harness-runner/QUICK_RULES.md`, `QUICK_START.md`, and `orchestrator_harness/SPEC.md` when present.
5. The candidate source and tests under the explicitly named candidate worktree when present; do not infer the stable runner from a candidate path.

The live harness documentation overrides the bundled harness reference if the repository changed after this skill was authored.

Confirm every supplied path is readable. Inspect relevant source, tests, Git state, and existing plans read-only when needed to make paths and dependencies concrete. If the repository has no `HEAD`, put baseline creation before any worktree step.

## Build the plan

### 1. Extract coverage

Turn every discrete implementation, test, documentation, migration, validation, operational, and completion requirement in the reference plan into an atomic `C<number>` checklist item. Preserve source locations.

Do not combine independent requirements merely to shorten the checklist.

### 2. Audit the decomposition

Separate coverage granularity from execution granularity. Atomic checklist items prove that no requirement was lost; they are not automatically execution steps.

Classify every reference-plan part as:

- `reused as-is`
- `reused with minor adjustment`
- `re-decomposed`

Re-decompose when it improves dependency order, disjoint ownership, testability, safe parallelism, or avoids repeating the full workflow around small related changes. Give one concrete reason for every re-decomposition.

Create these levels:

1. **Preflight gates:** evidence-only setup such as recording commits, checking tools, or proving the frozen checkout is clean. A preflight has commands, evidence, and a pass/fail gate, but no product-coder/reviewer/author/doer cycle unless it actually changes the product.
2. **Modules:** bounded implementation pieces from the reference plan, such as storage, token handling, session lifecycle, or an API surface. A module may contain several atomic checklist items, but it is not automatically a full execution step.
3. **Large steps:** meaningful, independently testable features or deliverables that bundle multiple related modules and end at a useful integration checkpoint. Group primarily by coherence and feature boundary, not by file layout or equal size. For example, an `authentication` large step may contain user storage, password handling, tokens, sessions, middleware, and auth API modules. Apply the full QA lane cycle once to the complete large step.
4. **Small changes:** ordered tasks inside a module and the large step's singular product lane. A configuration edit, helper, schema field, documentation adjustment, individual test file, or single checklist item does not receive its own full cycle.

Use the smallest number of large steps that preserves clear feature, dependency, risk, and subsystem boundaries. Do not combine unrelated features merely to reduce step count, but do not promote every module, file, commit, requirement, or minor change into a step. For every large step, list its included modules, its ordered serial tasks, the coherent feature or deliverable they form, and why that unit justifies one full QA pass.

### 3. Map dependencies and ownership

Keep large steps serial. A large step begins only after all dependencies and its prior step are complete.

For each large step, define:

- One manager-authored step spec.
- One production-code owner.
- The multiple modules bundled into the step and their shared feature or deliverable.
- An ordered list of the small implementation changes completed serially by that owner across those modules.
- The smallest useful set of disjoint conceptual slices for static review, test authoring, documentation authoring, and test execution.
- Exact planned file ownership when the repository already exists, used only as a collision-control overlay.
- A merge point followed by one orchestrator triage.
- One explicit lane topology that shows direct singleton lanes and only the branch-and-join points that actually exist.

Define every fan-out by non-overlapping concepts such as features, behaviors, planned tests, actions, or module responsibilities. Never use file paths alone as the work split. Fix the conceptual split in the emitted plan; the runtime must not re-decide it. Add exact paths only after the conceptual split to prevent writers from colliding. When independence is uncertain, serialize it.

Do not use role slots such as `R1` or `D1` as substitutes for lanes. Give every planned worker invocation a stable, step-scoped lane ID such as `S2.P`, `S2.R1`, `S2.A1`, or `S2.D1`. Give every actual multi-lane split a stable gate ID such as `S2.SR`, `S2.SA`, or `S2.ST`, and every review-triage, author-integration, or test-triage handoff a gate such as `S2.JR`, `S2.JA`, or `S2.JT`. Do not invent a split gate for a singleton pool.

For every large step, emit both a compact arrow graph and a lane manifest. Do not emit one for each module or small change inside it. The graph must show the exact direct handoffs, any real splits and joins, the repair loop, and the next-step path. Every manifest row must state:

- Stable lane ID and concrete assigned task.
- Agent role and wave.
- Start gate and required predecessor or branch base.
- Exact branch/worktree for writers, or exact read-only/run root for non-writers.
- Conceptual and path ownership.
- Required output or evidence handoff.
- Join gate, serial merge destination and order when applicable, and failure route.

The product lane must be singular and must complete the large step's bundled modules and ordered small changes before publishing one coherent reviewable tip. With one reviewer, hand that tip directly to the single review lane and then to the review-triage gate; with two or three, use a real review split and join. Apply the same cardinality rule to author and test pools. Author lanes begin only after Checkpoint A, branch from the recorded Checkpoint-A tip, and integrate serially when more than one writes. Test lanes begin only after author integration and run against the same recorded candidate tip in isolated state. An admitted defect returns to the singular product lane; the plan names which triage and gap lanes repeat. A completed large step names the next product lane it unlocks.

Also emit a section-wide lane-flow summary covering all steps. It must show which step unlocks which later step and where every fan-out rejoins. Do not make the reader reconstruct topology from separate role tables.

### 4. Size pools

The orchestrator occupies one of four available agent slots. Set every reviewer, doer, documentation, or final-review pool to at most three concurrent workers.

Pool size may be 1, 2, or 3. Size 1 is fully valid, is often the correct choice, and means a direct serial lane with no parallel fan-out. Use one worker by default for each review, authoring, or test-execution function. Increase a pool to two or three only when the plan names genuinely independent slices and explains the concrete time, coverage, or isolation benefit. The limit of three is a cap, not a target. Never invent duplicate slices or split one coherent task merely to fill available slots. If more than three independent slices exist, create ordered waves; never exceed three workers beside the orchestrator.

Keep production coding singular and serial. Parallelism is limited to pre-split static review, smoke/unit test authoring, reference-required documentation authoring, and isolated test execution. Permit concurrent test or documentation authoring only for manager-assigned, non-overlapping conceptual slices with non-overlapping paths. Never parallelize planning, triage, decisions, production coding, integration, or shared-file edits.

### 4a. Optimize the safety-to-time ratio

Plan for deployed-product reliability, not for maximum ceremony. Before emitting lanes, classify every possible follow-up as `production/material`, `strict test-only`, or `administrative`. Put this classification table and its exact routes in the plan's runner rules.

Make and record these three topology decisions before assigning any doer lane. They are required
because a test executor can be wrong even when the candidate is not. Do not add a reusable product
framework or a new gate when the executor does not create custom inner-process evidence; record
`not applicable` with the reason instead.

1. **Executor self-check:** For every expensive selected test set whose result relies on a custom
   runner or per-check child-process evidence, require one cheap same-lane recordability preflight
   before the real selection. It uses a disposable/local fake and performs no product, MCP,
   hardware, or external-side-effect operation. It proves one complete record can be written and
   read: stable ID, exact inputs, process/worker creation identity, timing, command, outputs, and
   exit outcome. A preflight failure or reconstructable report/path/schema error is a same-lane
   procedure correction, not a candidate defect and not a reason to spend the expensive selection.
   If the raw identity evidence cannot be reconstructed after a run, rerun only that affected stable
   ID on the unchanged lock.
2. **Pooled process-environment correction:** When one selected set exposes only classified
   fixture, mock, runner, or executor-environment defects, collect the complete set first, repair it
   as one test-only batch, then rerun that selection once. Do not repeat the broad selection after
   each individual process/setup correction. A candidate, contract, oracle, expected-behavior, or
   coverage finding leaves this route for the material flow. Purely administrative corrections with
   already-complete raw evidence resume in place and do not invalidate product credit.
3. **Pooled finding disposition:** For every review, selected test set, and observer/watch lane,
   complete the assigned affected surface or selection, collect its full finding set, deduplicate it
   at one triage gate, and make one bounded repair batch. A finding alone does not stop peer checks,
   restart a review, or cause a repair/rerun during that gate. The only immediate-stop exception is
   exact evidence that continuing can cause an unauthorized or wrong-resource operation, loss of
   containment/cleanup of a live process, or irreversible corruption of the evidence needed to judge
   later work. Record all other observations and let the gate complete. The plan must name the
   exception owner, the stop condition, the preserved evidence, and the post-gate pooled route.
4. **Operational-failure isolation:** A bug or mistake in test setup, fixture, runner, watcher,
   report writer, process supervision, evidence collection, or other supporting test infrastructure
   never blocks, invalidates, relocks, or reruns a product gate merely because the support code
   failed. Correct it in place and continue when the result remains determinable; otherwise mark only
   the affected test/attempt result `INCOMPLETE` or `INDETERMINATE`, preserve all valid immutable
   product credit, and run only the incomplete work in a fresh support attempt. Escalate a support
   failure to a product-gate blocker only when exact evidence shows it prevents determining whether
   the product behavior or test outcome passed. A real safety interlock may stop live operations, but
   after containment it follows this same isolation rule unless it proves a product defect.
5. **External-attempt rehearsal:** When the final practical phase consumes scarce or irreversible
   resources (for example hardware, an MCP service, a target repository, an outside watcher, or an
   attempt namespace), require a host-only rehearsal against disposable local fakes before allocating
   them. Name what it proves for that product's control plane—normally admission, retained-session
   authorization, process/identity binding, duplicate refusal, observer correlation,
   recovery/idempotence, cleanup, and terminal closure. A green rehearsal unlocks the real attempt;
   it is never evidence that the real external behavior passed. If the practical phase has no such
   resources, record `not applicable` with the reason.

- **Production/material:** any production source, policy, public/operative contract, locked configuration, acceptance/evidence contract, coverage obligation, test oracle, assertion strength, or expected behavior changes. Use the normal bounded repair batch: shortest affected smoke first; then a complete fresh read-only review and the remaining focused test execution may run in parallel on the same frozen tip; join them before advancing. Repair all accepted findings as one serial batch and perform dependency-map, registry, and aggregate-evidence reconciliation once on the accepted batch tip. Do not create a fresh review for an intermediate repair revision.
- **Strict test-only fast lane:** use only when the diff is limited to synthetic fixture/setup or test metadata and all of the following are proven: no production/policy/contract/locked-configuration files changed; no test oracle, assertion, expected outcome, stable ID, or coverage obligation was weakened or changed; the exact failing IDs are already known; and the correction restores an unchanged governing requirement. The route is one same-thread test-author continuation, a deterministic diff/eligibility checklist, and one rerun of exactly those failed IDs. It has no fresh C0, no ordinary static review, no registry/dependency/aggregate reconciliation, and no unrelated smoke or work may intervene before that rerun. If the rerun passes, preserve unrelated green credit; if it fails or eligibility is not proved, leave the fast lane and use the normal focused/material route.
- **Administrative:** result-envelope, path, command, metadata, or evidence-field corrections that do not change operative product or test meaning resume in the same lane. They need neither a product review nor a green-test rerun.

Put the selected self-check, pooled-correction, pooled-finding disposition, operational-failure isolation, and external-operation readiness decisions in the
relevant gate topology, runner rules, and config block. A plan is incomplete if it merely says
"preflight" without stating
what the executor verifies, what is prohibited during that preflight, and the exact correction/rerun
route.

### 4b. Scope lock invalidation by dependency

Do not use a whole governing-document hash as the only invalidation decision. Record whole-document
hashes for audit, then identify the smallest project-specific **lock-input domains** whose change
could affect a gate. Typical domains may include candidate behavior, product contract, test
semantics, test-execution procedure/evidence, external-operation topology, or external authority;
choose only domains that the project actually needs and name them for their purpose, not an assumed
stage.

For every gate, emit a **gate dependency matrix** that states the exact lock-input domains it
consumes. For every governing change, require an append-only **governing-change classification**
record containing the prior/new document hashes, changed requirement IDs, changed domains,
invalidated gates, preserved evidence, and reason. Invalidate only gates that consume a changed
domain. Preserve other green evidence. If the change cannot be classified confidently, use the
documented **conservative fallback** route rather than guessing.

Do not prescribe a project-specific stage, external system, model, or hardware pattern for this
mechanism. The plan must choose the appropriate narrow revalidation for its own topology. State
whether this is plan-level governance only or is also enforced by the runner; a plan-level rule must
not pretend to be automatic runtime enforcement.

Require the plan to finish a qualifying fast lane before dispatching unrelated work. Never use a passing smoke for a different ID as credit for the failed ID. Prefer the existing lane/thread and worktree for a strict test-only continuation so it does not reread the full plan or reconstruct topology.

State the selected launch speed profile in the role table and every launch template. When the user or repository policy requires Fast, every launched child uses the selected ordinary model plus explicit Fast/priority tier; do not silently substitute models, efforts, or tiers. When no such policy is supplied, record the chosen tier rather than assuming a provider-specific mode.

### 5. Encode the loops

For every large step, emit exactly two back-to-back series loops. Run this cycle once for the complete coherent feature or deliverable, not once for each included module, small change, commit, file, or checklist item:

1. Loop 1: the orchestrator writes or updates the large-step spec, included-module list, and ordered small-change list; singular coder-main implements or fixes the complete feature; reviewer-main reviews it using the selected pool size; and one orchestrator triages. Merge and de-duplicate findings only when the pool has multiple reviewers. Repeat valid defects until only extraneous findings remain, then record permanent Checkpoint A.
2. After Checkpoint A, reviewer-main authors the required smoke and unit tests over the fixed conceptual slices. These become the step's gap set.
3. Loop 2: doer-main runs the gap set over fixed conceptual slices, results merge, reviewer-main classifies them, and one orchestrator triages. Singular coder-main fixes admitted failures. Repeat until green or only extraneous findings remain.

Checkpoint A permanently closes ordinary static review for that large step. Do not restart Loop 1 merely because the coder implemented several planned modules or internal changes. Do not nest the two loops and do not revive ordinary static review during Loop 2. After a real multi-worker fan-out, wait for all members, concatenate and de-duplicate their outputs, then make one decision. Reviewers complete their assigned affected surface after finding a defect unless the defined immediate-stop exception applies. After a singleton lane, hand its output directly to the same triage gate without pretending a merge occurred.

Keep the lane graph synchronized with the loop prose and assignment tables. A lane named in a graph must have a manifest row, and every reviewer, author, doer, repair, merge, or transition in the prose must identify its lane or gate.

### 6. Embed triage, scoping, and termination rules

State that the goal is a working product delivered efficiently, not perfection. Every admitted task must trace to realistic product functionality. Do not grow review or tests merely to keep a loop alive.

Classify each finding as one of:

- `functional defect`: broken behavior on a realistic, non-trivial usage path; admit and fix.
- `extraneous / gold-plating`: speculative hardening, style-only rigor, hypotheticals, invented complexity, or negligible edge behavior already adequate for roughly 99.9% of real use; log it to the out-of-scope ledger and drop it.

The reviewer recommends; the singular orchestrator decides under the user-editable `scope_policy`, biased toward shipping working behavior.

Require a persistent passed registry with stable test IDs such as `path::class::test`. The plan names tests by concept; the runtime assigns their actual stable IDs. Each admitted fix records the exact IDs it targets. Lock passed tests during ordinary loops. Rerun only still-failing gap tests, failed unit tests, and tests newly implicated by that specific finding or change. The strict test-only fast lane reruns only its known failed IDs and never substitutes an unrelated smoke. The final safeguard is the only routine full-suite rerun.

Give loops no iteration cap. End only on success, unrecoverable error, or stall/no progress. A stall includes `stall_threshold` consecutive no-progress iterations, identical failure signatures across fix attempts, pass/fail oscillation without net passed-set growth, or iterations producing only extraneous scope churn. Report rather than hide a stall.

### 7. Encode the finished-product phase

Emit the complete final flow:

1. C0: spawn a fresh final-reviewer invocation using the user's selected agent; do not reuse a build-phase reviewer invocation.
2. C1: give it the prewritten final/acceptance spec and finished product. Permit spec tweaks only when genuinely required and recorded. It authors the complete final unit and smoke set over fixed conceptual slices.
3. C2: run the final test loop in series with no static review: doer fan-out, merge, reviewer classification, one triage, singular fix, and gap-only rerun until pass.
4. C3: doer-main launches the real end-to-end practical test. Pass proceeds to the safeguard; failure enters C4.
5. C4: revive static review only for repeated practical-product failure. Reviewer audits, one orchestrator plans, singular coder fixes, the nested static audit repeats until clean, new regression tests are authored and run, then C3 is rerun. C4 remains dormant during the ordinary build.

Give C0-C4 their own explicit lane topology. In C3, predefine the acceptance orchestrator lane, isolated watcher lane, serialized target-production lanes, permitted test/documentation fan-outs, merge lane, shutdown lane, evidence joins, and the pass/fail routes. The candidate orchestrator may make local tactical decisions inside those assignments, but it may not invent a different topology at runtime. The outside writer-manager remains outside the candidate topology.

Apply the same cardinality rule to C0-C2 and permitted C3 author/test pools: size 1 is a direct lane without a split; sizes 2 or 3 require genuinely independent work and an explicit split and join.

After practical success, run the full accumulated suite exactly once when `final_full_verification` is true. A regression returns its IDs to the gap set and resumes the relevant loop; do not count the later post-repair safeguard as the same attempt. Finish with pass evidence and a summary of the out-of-scope ledger.

### 8. Bind to the current Portable Harness

Do not assume a scheduler, task database, automatic worker launcher, generic resource-lock service, generalized coding invocation, or merge-ready result validator exists.

The emitted plan must state that:

- The persistent orchestrator plans, launches workers through the available external mechanism, makes decisions, integrates branches, and manages resources.
- The implementation runner is pinned to `stable-general-harness-runner`; the independently recoverable rollback is `pre-conversion-rollback`. Any former physical aliases are non-operational and documented in the outer checkout map.
- The harness observes and returns durable events through its native blocking wait.
- The deterministic watcher is diagnostic-only with `evaluator_enabled: false`.
- Every live epoch has fresh configuration, output, watcher, cursor, event, and acknowledgement state.
- `scan --no-write` succeeds before workers launch.
- Actionable work is discovered only through `watch --until-actionable` or the documented native managed-watch flow.
- Handling finishes before `ack --event-id` uses the top-level native event ID.
- Each lane has its own run root and `.agent-workspace`.
- Workers use `PARALLEL_CHECKPOINT.md`, `RESULT.json`, and valid `manager-signals` where appropriate.
- The orchestrator validates result contents because the current harness observes `RESULT.json` but does not enforce the future coding-result schema.
- Git branches and worktrees are created explicitly by the orchestrator; the current harness does not isolate them automatically.
- Resource ownership is explicit manager policy; do not assume the future generic named lock.
- Code and configuration remain frozen during a live epoch. Repair begins only after safe shutdown and preserved evidence.

### 9. Prove coverage

Map every atomic checklist ID to its module, containing large step, and planned tests. Multiple modules and many checklist IDs should normally map to one large step. Do not finalize with an unmapped ID or unresolved gap. Surface ambiguity to the user instead of guessing.

### 10. Fill and validate

Use the template's sections 0 through 11 in exactly the same order. Replace every angle-bracket placeholder. List evidence-only setup as preflight gates. Repeat the per-step block only for large steps that bundle multiple coherent modules. Do not create a full step block for an individual module, configuration edit, helper, schema field, documentation adjustment, test file, or atomic checklist item. Fill every lane graph, stable lane/gate ID, manifest field, conceptual split, pool/wave assignment, test concept, handoff path, merge order, failure route, final-phase action, and current-harness command concretely; do not treat unchanged template prose as a complete plan.

Run:

```powershell
python .codex/skills/plan-harness-workflow/scripts/validate_execution_plan.py <output-plan> --require-scoped-locks
```

Fix validation failures before reporting completion.

## Report the deliverable

Return:

- Output plan path.
- Input spec and reference-plan paths used.
- Recorded role mapping and skill-decided pool sizes.
- The explicit lane topology and where its parallel lanes split and rejoin.
- Whether the original decomposition was reused or changed.
- Validator result.

Do not begin executing the emitted plan.
