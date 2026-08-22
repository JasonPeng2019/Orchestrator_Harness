# Development rules

The `BOUNDED-TEST-v1` rule below is portable and applies in any repository that receives this
`AGENTS.md` plus the `.codex` directory. The Firmware Plan 2 campaign is closed and preserved at
`archive/firmware-v2-campaign/general-coding-harness/`; it is historical evidence, not a live
execution contract. The active compatibility follow-through is documented under
`plans/compatibility-testing/` and `active_docs/`.

- Read `HANDOFF.md` before changing the product; it records current status and agreed design direction.
- Treat `archive/firmware-v2-campaign/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` as historical only; it must not restart a Firmware sprint, repair, or promotion. `HANDOFF.md` is the current status record.
- The compatibility plans and the Claude/Qwen feature inventories remain active until their source changes are merged into `firmware-v2-harness-runner`; they do not reopen the closed Firmware hardware campaign.
- Use `.codex/skills/design-project-topology` when a newly authorized execution plan needs to be designed or validated. The archived Plan 2 and V1 documents must not supply live edges, gates, roles, or invalidation rules.
- No external workflow framework is active. The audited reference checkout was removed after the useful pieces were ported into `.codex/`.
- Treat new Ruff, BasedPyright, compilation, or unit-test failures as blocking.
- Existing BasedPyright findings are recorded in `.codex/dev/basedpyright-baseline.json`; do not expand the baseline.
- Every ROOT or subagent command recognized by `.codex/policies/bounded-launchers.json` must follow `BOUNDED-TEST-v1` in `.codex/policies/bounded-tests.md` and run through `.codex/scripts/Invoke-BoundedTest.ps1`, unless its resolved script path matches `.codex/policies/bounded-exclusions.gitignore`. This is a mechanical execution boundary, not semantic test detection. Agent/provider sessions are lane-managed, not test-bounded. Direct executables such as `pytest.exe`, Ruff, BasedPyright, npm, or compiled binaries are outside the hook boundary by design.
- Give every bounded invocation a unique task-specific result path; concurrent agents must never share one result or log stem.
- Base every timeout on measured history, a protocol/resource constraint, or an accepted plan bound. Maximum lifetime must equal that expected upper bound plus policy-capped cleanup.
- Never retry an unchanged supervisor failure. Classify it first, preserve its evidence, and retry only after a changed condition or justified correction.
- Treat bounded execution as a beta development feature. Fix a general supervisor defect only with a small, low-risk change and focused proof. Handle a genuinely case-specific launch complication with the smallest task-local wrapper run through the same supervisor; never fork or copy the supervisor. Every execution plan containing covered execution must adopt the policy by reference.
- Give parallel agents disjoint file ownership. Use `uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py` when isolated branches are useful.
- For any newly authorized multi-agent repair, ROOT diagnoses and writes the exact behavior-proof/no-change contract. The implementation worker terminates back at ROOT; ROOT owns any subsequent test dispatch, integration authorization, and acceptance. No worker self-dispatches its successor.
- The main agent owns integration authorization, conflict classification, acceptance, and final verification. A mapped doer may execute only ROOT's separately dispatched exact fast-forward/readback/post-join mechanics after ROOT accepts terminal evidence; the doer never self-starts or decides integration.
- Project Codex hooks block selected destructive commands, restore handoff context, and verify changed repository state before Codex stops.
