# Development rules

The `BOUNDED-TEST-v1` rule below is portable and applies in any repository that receives this
`AGENTS.md` plus the `.codex` directory. The other rules govern this harness repository only; when
this file is copied elsewhere without `plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`,
ignore the harness-specific plan, handoff, baseline, worktree, and verification bullets.

- Read `HANDOFF.md` before changing the product; it records current status and agreed design direction.
- Treat `plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` as the sole current-run product and execution contract. `goal.md` and `HANDOFF.md` remain separate by design.
- Use `.codex/skills/design-project-topology` for current execution-plan design and validation. The unregistered `plan-harness-workflow` predecessor, archived V1 specs/roadmaps/plan, and `plans/general-coding-harness/steps/S1.md` through `S4.md` are historical only and must not supply live edges, gates, roles, or invalidation rules.
- No external workflow framework is active. The audited reference checkout was removed after the useful pieces were ported into `.codex/`.
- Treat new Ruff, BasedPyright, compilation, or unit-test failures as blocking.
- Existing BasedPyright findings are recorded in `.codex/dev/basedpyright-baseline.json`; do not expand the baseline.
- Every ROOT or subagent command recognized by `.codex/policies/bounded-launchers.json` must follow `BOUNDED-TEST-v1` in `.codex/policies/bounded-tests.md` and run through `.codex/scripts/Invoke-BoundedTest.ps1`, unless its resolved script path matches `.codex/policies/bounded-exclusions.gitignore`. This is a mechanical execution boundary, not semantic test detection. Agent/provider sessions are lane-managed, not test-bounded. Direct executables such as `pytest.exe`, Ruff, BasedPyright, npm, or compiled binaries are outside the hook boundary by design.
- Give every bounded invocation a unique task-specific result path; concurrent agents must never share one result or log stem.
- Base every timeout on measured history, a protocol/resource constraint, or an accepted plan bound. Maximum lifetime must equal that expected upper bound plus policy-capped cleanup.
- Never retry an unchanged supervisor failure. Classify it first, preserve its evidence, and retry only after a changed condition or justified correction.
- Treat bounded execution as a beta development feature. Fix a general supervisor defect only with a small, low-risk change and focused proof. Handle a genuinely case-specific launch complication with the smallest task-local wrapper run through the same supervisor; never fork or copy the supervisor. Every execution plan containing covered execution must adopt the policy by reference.
- Give parallel agents disjoint file ownership. Use `uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py` when isolated branches are useful.
- Across every current or future Plan 2 module and loopback, ROOT diagnoses and writes the exact behavior-proof/no-change contract. The mapped `coder-main` implements admitted product repairs and terminates back at ROOT. ROOT then either dispatches `doer-main` directly for deterministic tests/checks when trusted verification assets suffice unchanged, or first dispatches the Plan's reusable M03 `doer-main` route when verification assets must be implemented or corrected. Every worker terminates back at ROOT; no worker self-dispatches its successor.
- The main agent owns integration authorization, conflict classification, acceptance, and final verification. A mapped doer may execute only ROOT's separately dispatched exact fast-forward/readback/post-join mechanics after ROOT accepts terminal evidence; the doer never self-starts or decides integration.
- Project Codex hooks block selected destructive commands, restore handoff context, and verify changed repository state before Codex stops.
