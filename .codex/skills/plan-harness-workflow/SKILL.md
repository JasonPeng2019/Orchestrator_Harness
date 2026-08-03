---
name: plan-harness-workflow
description: Author a coverage-complete, detailed multi-agent execution-plan file from a product spec, reference implementation plan, acceptance spec, and user-selected agents. Use only when explicitly invoked to design a workflow for the current Portable Harness Repo; preserve singular orchestrator planning, serial production coding, bounded disjoint test/documentation fan-out, native scan/wait/ack operation, and the fixed execution-plan template. This skill plans but never executes work, launches agents, edits product code, or runs the generated workflow.
---

# Author a Portable Harness workflow

## Hold the boundary

Produce one execution-plan document. Do not execute the plan, launch agents, edit product code, run project tests, start the harness, or create runtime state.

Treat the reference implementation plan as the complete outcome contract, not necessarily the best decomposition. Never drop, weaken, or invent product scope.

## Collect inputs

Require:

- Product spec path.
- Reference implementation plan path.
- Final or acceptance spec path, or an explicit statement that the product spec contains it.
- Concrete agent choice for each role: orchestrator/planner-executor, coder-main, reviewer-main, doer-main, and final-reviewer.

Accept an optional output path and optional overrides for `scope_policy`, `stall_threshold`, `gap_scope`, and `final_full_verification`.

If any required input or role is missing, ask one consolidated question and wait. The user chooses agent implementations, not pool sizes or work splits. Default the output to `plans/<product-slug>/EXECUTION_PLAN.md`.

## Read authoritative material

Read, in order:

1. The supplied product, reference-plan, and acceptance files.
2. [references/execution-plan-template.md](references/execution-plan-template.md).
3. [references/current-portable-harness.md](references/current-portable-harness.md).
4. The live `frozen-harness-to-use/QUICK_RULES.md`, `QUICK_START.md`, and `orchestrator_harness/SPEC.md` when present.
5. The candidate source and tests under `harness-in-progress/` when present.

The live harness documentation overrides the bundled harness reference if the repository changed after this skill was authored.

Inspect relevant source, tests, Git state, and existing plans read-only when needed to make paths and dependencies concrete. If the repository has no `HEAD`, put baseline creation before any worktree step.

## Build the plan

### 1. Extract coverage

Turn every discrete implementation, test, documentation, migration, validation, operational, and completion requirement in the reference plan into an atomic `C<number>` checklist item. Preserve source locations.

Do not combine independent requirements merely to shorten the checklist.

### 2. Audit the decomposition

Classify every reference-plan part as:

- `reused as-is`
- `reused with minor adjustment`
- `re-decomposed`

Re-decompose only when it improves dependency order, disjoint ownership, testability, or safe parallelism. Give one concrete reason for every re-decomposition.

### 3. Map dependencies and ownership

Keep steps serial. A step begins only after all dependencies and its prior step are complete.

For each step, define:

- One manager-authored step spec.
- One production-code owner.
- Exact disjoint conceptual slices for static review, test authoring, documentation authoring, and test execution.
- Exact planned file ownership when the repository already exists.
- A merge point followed by one orchestrator triage.

When independence is uncertain, serialize it.

### 4. Size pools

The orchestrator occupies one of four available agent slots. Set every reviewer, doer, documentation, or final-review pool to at most three concurrent workers.

Use the smallest useful pool. If more than three independent slices exist, create ordered waves; never exceed three workers beside the orchestrator.

Keep production coding singular and serial. Permit concurrent test or documentation authoring only for manager-assigned, non-overlapping files or conceptual slices.

### 5. Encode the loops

For every step, emit two series loops:

1. Static review loop until permanent Checkpoint A.
2. Test loop after Checkpoint A, with no ordinary static review.

Use merge-then-triage after every pool fan-out. The single orchestrator classifies findings as functional defects or extraneous/gold-plating and makes every decision.

Maintain a passed-test registry. During a loop, rerun only failing or newly implicated tests. Run the complete accumulated suite once in the final safeguard when enabled.

Use no iteration cap. Stop a loop only for success, stall/no progress, or unrecoverable error. Include same-signature failure, oscillation, and scope-churn rules.

### 6. Bind to the current Portable Harness

Do not assume a scheduler, task database, automatic worker launcher, generic resource-lock service, generalized coding invocation, or merge-ready result validator exists.

The emitted plan must state that:

- The persistent orchestrator plans, launches workers through the available external mechanism, makes decisions, integrates branches, and manages resources.
- The known-good runtime is executed from `frozen-harness-to-use`; product changes and candidate verification target `harness-in-progress`.
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

### 7. Prove coverage

Map every checklist ID to both its build step and planned tests. Do not finalize with an unmapped ID or unresolved gap. Surface ambiguity to the user instead of guessing.

### 8. Fill and validate

Use the template's sections 0 through 11 in exactly the same order. Replace every angle-bracket placeholder. Repeat the per-step block for every serial step.

Run:

```powershell
python .codex/skills/plan-harness-workflow/scripts/validate_execution_plan.py <output-plan>
```

Fix validation failures before reporting completion.

## Report the deliverable

Return:

- Output plan path.
- Input spec and reference-plan paths used.
- Recorded role mapping and skill-decided pool sizes.
- Whether the original decomposition was reused or changed.
- Validator result.

Do not begin executing the emitted plan.
