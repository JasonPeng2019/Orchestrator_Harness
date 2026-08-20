## Mandatory bounded execution (`BOUNDED-TEST-v1`)

Route every command recognized by the repository's `bounded-launchers.json` through the bounded
supervisor unless its resolved script path matches `bounded-exclusions.gitignore`. This is a mechanical
boundary, not semantic test detection. Agent/provider sessions are lane-managed and must not receive a
bounded-test deadline. Direct executables such as `pytest.exe`, Ruff, BasedPyright, npm, or compiled
binaries are outside the hook boundary by design.

Before each covered execution, locate the applicable repository bounded-test policy and supervisor in
the active instructions and provider configuration, including `AGENTS.md`, `.codex/`, `.claude/`, or
another provider-specific directory. An injected worktree configuration must point to the operational
policy and supervisor owned by its launcher rather than to unrelated product code.

Invoke the supervisor with the exact command, working directory, result path, heartbeat interval,
evidence-backed expected upper-bound runtime, bounded cleanup allowance, their computed maximum
lifetime, and timeout basis. Never invent or pad an unexplained timeout, and never set a deadline below
the credible upper bound. On Windows, invoke it with
`powershell -NoProfile -ExecutionPolicy Bypass -File` so host execution policy cannot block startup.

- Use a unique task-specific result path; never share a result/log stem with another invocation.
- Never retry an unchanged supervisor failure; preserve and classify it first.
- Fix a general supervisor defect only with a small, low-risk shared change and focused proof.
- For a genuinely unique quoting/environment/exit case, use the smallest task-local `.ps1` wrapper
  through the same supervisor. Never copy or fork the supervisor, and never bypass it silently.

Preserve the supervisor's terminal JSON and logs in the task's declared evidence root. Treat
`TIMED_OUT` as a support result pending orchestrator classification, not as product pass or failure.
