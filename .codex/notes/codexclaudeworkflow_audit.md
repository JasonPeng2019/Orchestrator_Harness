# CodexClaudeWorkflow Development-Tool Audit

## Scope

This audit evaluates `buh07/CodexClaudeWorkflow` only as tooling for developing the portable harness. None of these components belong in the harness runtime or portable product.

Reference checkout:

- Path: `references/CodexClaudeWorkflow`
- Commit: `54b88c6fe47c7f76a0f8bb83b65a6879dd45054f`
- Date: 2026-07-31

The reference is inert. Its installer, attachment flow, hooks, launchers, modes, and skills have not been activated.

## Audit Results

- Internal Python implementation: about 14,251 lines.
- Tests: about 8,838 lines.
- Skills: 21.
- Modes: 11.
- Ruff: passes.
- BasedPyright: passes with zero findings.
- Native Windows pytest result: 226 passed, 224 failed, 1 skipped, and 27 errors.

The Windows failures include explicit Unix dependencies such as `fcntl`, Bash, `python3`, executable-bit behavior, symlinks, and POSIX path handling. Failures also occur across worktrees, multi-agent state, verification freshness, sessions, audit state, attachment, and workflow gates. This does not prove the intended Linux/WSL implementation is broken, but it does prove the repository is not a safe native-Windows drop-in.

One confirmed Windows defect is `internal/worktree_tasks.py` writing unescaped Windows paths into TOML basic strings. A path containing `C:\Users\...` fails `tomllib` parsing.

## Recommended Extraction

### 1. Ruff, Pyright, and Test Configuration

**Decision:** Adapt directly.

Useful source:

- `pyproject.toml`
- `pyrightconfig.json`

Keep the development dependency pattern and tool configuration. Change Python 3.12 to the harness's Python 3.11 target. Start Ruff with correctness rules rather than formatting the existing dense watcher files.

**Effort:** 30-60 minutes plus time to fix existing findings.

### 2. One Verification Command

**Decision:** Rewrite a small native version.

Useful source ideas:

- `bin/verify`
- `bin/verify-software`
- `internal/verify_backend.py`

The useful behavior is a single command that runs Ruff, Pyright, compile checks, and both unit-test suites and returns a clear pass or failure. The existing code is coupled to modes, structure manifests, risk checks, project attachment, and verification state, so copying it would pull in unnecessary dependencies.

Implement a small Python or PowerShell command for this repository instead.

**Effort:** 2-4 hours.

### 3. Post-Change Verification Rule

**Decision:** Use the rule, not the hook framework.

Useful source ideas:

- `instructions/common.md`
- `instructions/software.md`
- `hooks/posttooluse-verify.sh`

The useful rule is: finish one logical change, run verification, fix failures, then report completion. Put this directly in the development `AGENTS.md`. A PostToolUse hook that fires after every edit adds noise and does not run verification anyway.

**Effort:** 10-20 minutes.

### 4. Pre-Commit Check

**Decision:** Optional; rewrite minimally.

Useful source ideas:

- `internal/git_hooks.py`
- `bin/install-git-hook`
- `bin/commit-gate`

Preserving an existing project hook before running managed checks is a good pattern. The existing implementation generates Bash and pulls in plan, review, mode, and verification-freshness gates. If hard commit enforcement is desired, install a small cross-platform hook that calls only the local verification command.

Do not copy the full commit gate.

**Effort:** 1-2 hours.

### 5. Verification Freshness

**Decision:** Valuable but defer; rewrite if needed.

Useful source ideas:

- `internal/verify_state.py`

The good idea is to invalidate a successful check after relevant files or the toolchain change. The implementation is 876 lines and tightly coupled to runtime paths, modes, Git state, research smoke checks, and attachment behavior. It is excessive for the initial development setup.

For now, require verification immediately before completion. Add a small hash-based freshness record only if stale verification becomes a real failure mode.

**Effort:** 4-8 hours for a focused rewrite.

### 6. PLAN and HANDOFF

**Decision:** Adopt as plain optional Markdown.

Useful source ideas:

- `templates/PLAN.template.md`
- `templates/HANDOFF.template.md`
- `instructions/common.md`

These are useful for substantial changes and long sessions. They do not need task triage, semantic plan hashing, mandatory reviews, generated state, or skills.

Use them only when the work is large enough to need durable context.

**Effort:** 15-30 minutes.

### 7. Resume and Pre-Compaction Reminders

**Decision:** Optional pattern; do not copy current hook system.

Useful source ideas:

- `internal/hook_runner.py::sessionstart_resume`
- `hooks/sessionstart-resume.sh`
- `hooks/precompact-handoff.sh`

Bounded injection of HANDOFF and the head of PLAN is a sound idea. The current hook runner is 962 lines and imports audit, design, workflow, mode, and runtime-path systems. If context loss becomes a problem, implement a small standalone reminder later.

**Effort:** 2-4 hours for a minimal cross-platform implementation.

### 8. Git Worktrees

**Decision:** Adopt the workflow; rewrite the helper.

Useful source ideas:

- `internal/worktree_tasks.py`
- `bin/worktree-task`

Worth keeping:

- One worktree and branch per independent implementation task.
- Optional owner label.
- List active task worktrees.
- Refuse to close a dirty worktree.
- Main developer agent reviews and integrates changes.

Do not copy the current helper unchanged. It is coupled to modes and attachment, uses symlinks, and has the confirmed Windows TOML escaping defect. A small PowerShell helper using standard `git worktree` commands is appropriate.

**Effort:** 2-4 hours.

### 9. Multi-Agent Development Rules

**Decision:** Adopt selected rules; reject the custom backend.

Useful source ideas:

- `internal/multi_agent.py`
- `skills-src/common/multi-agent/SKILL.md`
- `decisions/ADR-0008-coordinated-multi-agent-implementation.md`
- `decisions/ADR-0014-codex-exec-multi-agent-transport.md`

Worth keeping as concise development instructions:

- Give coding agents explicit, non-overlapping file ownership.
- Use worktrees when implementation needs isolation.
- Keep merge, push, and final integration with the main developer agent.
- Use an independent subagent to review risky parallel changes.
- Run authoritative verification after integration.

Do not copy the 2,135-line backend or its manual transport. It requires plan manifests, semantic coverage, ordered waves, model pinning, lifecycle declarations, detached worktrees, patch bundles, auditor transcripts, and manual Bash recipes. It also disables native Codex multi-agent features during child execution. On native Windows, its focused tests produced 40 failures, 6 passes, and 1 skip.

Use Codex's native subagents instead.

**Effort:** 30-60 minutes to write the useful rules; no backend implementation.

### 10. Independent Review

**Decision:** Adopt as a native subagent practice.

Useful source ideas:

- `agents/adversarial-critic.md`
- `skills-src/common/adversarial/SKILL.md`

Independent review is useful for risky diffs. It does not require a skill, frozen patch bundle, review receipt database, or mandatory verdict parser. Give a separate read-only subagent the diff and ask for findings.

**Effort:** None beyond concise instructions.

### 11. Dangerous-Command Guard

**Decision:** Keep as reference; do not activate initially.

Useful source ideas:

- `internal/hook_runner.py::guard_dangerous`
- `hooks/guard-dangerous.sh`

The guard blocks several obvious dangerous command shapes and correctly describes itself as an agent-error guard rather than a security boundary. Codex already has higher-level safety rules, and the implementation depends on Bash, modes, audit logging, design state, and workflow classification.

Record the important prohibitions in `AGENTS.md`. Add a standalone guard only after observing a concrete need.

### 12. Environment Doctor

**Decision:** Borrow a small subset later if useful.

Useful source:

- `bin/doctor`

Checking that Python, Ruff, Pyright, and required test commands exist is useful. The existing doctor is 757 lines and validates the entire workspace ecosystem. A few checks can live in the verification command instead.

### 13. ADRs

**Decision:** Adopt plain ADR files only when needed.

Useful source:

- `decisions/ADR-*.md`

Short architectural decision records are useful for durable protocol or schema decisions. The design ledger, generated indexes, visibility modes, and query integration are not required.

## Do Not Adopt

The following systems do not provide enough value for developing this harness relative to their cost and coupling:

- Mode hierarchy and generated projections.
- Project attachment and configuration composition.
- `codexas` dispatcher and named-session registry.
- Custom multi-agent backend and manual Codex transport.
- Skill catalog and skill-evaluation framework.
- Design-ledger implementation and generated indexes.
- Audit-trail implementation.
- Structure manifests.
- Project scaffolding.
- Research sweep tooling.
- Firmware development tools.
- Query backend; native repository search is sufficient.
- Tidy framework.
- Secret scanner; use a maintained scanner if this becomes necessary.
- Status backend and full commit-gate workflow.
- Repair-mode tooling.

## Activation Risk

Running `attach-project` would install or generate root Codex and Claude configuration, skills, hooks, VS Code settings, mode state, task files, a pre-commit hook, runtime directories, a design ledger, and multi-agent settings. That would expose the large instruction and skill surface the audit is trying to avoid.

Keep the reference checkout inert. Do not run its installer, attachment flow, renderers, hook installer, launchers, or dispatcher.

## Recommended Development Setup

Implement only this first:

1. Root development configuration for Ruff and Pyright.
2. One local verification command covering compile checks and both unittest suites.
3. A short `AGENTS.md` post-change verification rule.
4. Optional PLAN and HANDOFF Markdown templates.
5. A small PowerShell worktree helper when parallel implementation first requires isolation.
6. Concise native-subagent rules for file ownership, independent review, main-agent integration, and final verification.

Do not introduce hooks, skills, modes, generated configuration, or custom orchestration until a demonstrated development problem justifies them.
