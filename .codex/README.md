# Portable bounded-test enforcement

To reuse `BOUNDED-TEST-v1` in another Windows repository, copy this `.codex` directory and the
repository-root `AGENTS.md`. The copied `AGENTS.md` explicitly scopes Orchestrator Harness rules to
repositories containing the named Plan 2 file; the bounded-test rule remains active everywhere.

Codex discovers `.codex/hooks.json`. Its `PreToolUse` matcher covers Codex's `shell_command` tool and
the compatible `Bash` alias. Its first matching hook calls
`scripts/bounded_test_adapter.py` directly. The adapter reads launcher names from
`policies/bounded-launchers.json` and lets Git evaluate `policies/bounded-exclusions.gitignore` against
resolved script paths. A directory rule excludes its complete tree, while a file rule can exempt only
one launcher. The adapter performs no semantic test detection and intentionally does not classify direct
executables such as `pytest.exe`, Ruff, BasedPyright, npm, or compiled binaries. Covered commands run through
`scripts/Invoke-BoundedTest.ps1`, which owns heartbeat polling, the hard deadline, process-tree
termination, cleanup verification, logs, terminal JSON, and the child exit code. The additional
destructive-command and changed-code Stop hooks are repository development conveniences; the Stop
verification hook becomes a no-op when the copied repository does not contain Plan 2.

For Codex subprocesses launched into an older or otherwise different worktree, the launcher must merge
the bounded `SessionStart` and `PreToolUse` entries into that worktree for the lifetime of the process
and restore the original hook bytes afterward. Any launcher can use the same two adapter commands
without copying product code.

The exclusion file is the sole path-exception source. It must explicitly list the supervisor entrypoint
and may list an orchestration bridge whose lifetime belongs to a lane or session owner. Each exclusion
is path-local: the adapter still evaluates every unquoted command-chain segment, so an excluded segment
never exempts an additional covered command appended after it. An injected agent-worktree hook applies
the same launcher and exclusion policy to commands the agent runs.

No hook can infer a command's true expected duration. The mechanical supervisor enforces the declared
upper bound, capped cleanup allowance, computed total, and heartbeat interval; `AGENTS.md` and
`policies/bounded-tests.md` require the declaration to be backed by measured history, a protocol or
resource bound, or an accepted plan bound. Review of that evidence is the orchestrator's responsibility.
