# Bounded execution policy (`BOUNDED-TEST-v1`)

Every configured Python-script, executed `.ps1`, and POSIX-shell invocation launched by an agent or
orchestrator must run through the repository's bounded-test supervisor unless its resolved script path
matches `bounded-exclusions.gitignore`. This is a mechanical process boundary; the hook does not guess
a command's meaning. Agent/provider sessions are lane-managed and receive no test deadline. Direct executables such as `pytest.exe`,
Ruff, BasedPyright, npm, or compiled binaries are outside this boundary by design. Read-only PowerShell
built-ins, Git, `rg`, and filesystem inspection remain unwrapped unless they launch a covered process.

## Required workflow

1. Discover and reuse the repository's existing bounded-execution architecture. Repository instructions
   and provider-specific configuration commonly live in `AGENTS.md`, `.codex/`, `.claude/`, or an
   equivalent provider directory. Do not create a parallel supervisor or policy when one already
   exists.
2. Before launch, declare the exact command, working directory, unique task-specific result location, heartbeat interval,
   expected upper-bound runtime, cleanup allowance, maximum lifetime, and the evidence-backed basis for
   the expected upper bound. Use the worst credible runtime under the named conditions, not a typical
   or optimistic runtime. The basis must come from a real protocol/resource constraint, an accepted plan
   bound, or measured history with stated headroom. An unexplained estimate is invalid.
3. The supervisor mechanically requires `maximum lifetime = expected upper bound + cleanup allowance`.
   Cleanup allowance is capped at the smaller of 120 seconds or 25% of the expected upper bound, with a
   five-second minimum cap for short commands. Thus a two-minute operation cannot be padded to ten
   minutes, while a credible twenty-minute operation cannot be assigned a ten-minute deadline. Change
   the estimate only when new evidence or operating conditions justify it; never enlarge a deadline just
   because a run timed out.
4. Launch the command once through the bounded supervisor. On Windows, use the process-local form
   `powershell -NoProfile -ExecutionPolicy Bypass -File .codex/scripts/Invoke-BoundedTest.ps1 ...`
   so a restrictive host execution policy cannot prevent the repository-owned supervisor from
   starting. The supervisor, not the calling agent, owns polling and the hard deadline.
5. While the command is live, the supervisor emits and flushes a `RUNNING` heartbeat no less often
   than the declared interval. The interval must not exceed 60 seconds so a live run cannot become
   invisible to the orchestrator and user.
6. On ordinary completion, the supervisor preserves stdout and stderr, writes a terminal result bound
   to the command and timing inputs, and returns the command's exit code with status `PASSED` or
   `FAILED`.
7. At the deadline, the supervisor terminates the exact launched process tree, verifies that the
   observed identities are absent, preserves partial output, writes `TIMED_OUT`, and exits nonzero.
8. A timeout is an administrative/support result pending impact classification. It is not a product
   pass or failure by itself, and retry is allowed only after classification identifies a changed
   condition or a justified correction.
9. The orchestrator consumes each heartbeat and terminal result, relays progress, and preserves green
   credit. If the orchestrator stops polling, the supervisor still enforces the deadline.

## Result isolation and retry discipline

- Every bounded invocation uses a unique result path in its task's existing evidence or runtime
  directory. Concurrent agents must not share a result path or its derived stdout/stderr stem.
- Never retry an unchanged supervisor failure. Preserve its output, classify whether the cause is a
  general supervisor defect, a case-specific launch incompatibility, or an external/support condition,
  and retry only after the relevant condition changes.
- A timeout does not justify enlarging the deadline by itself. Recalibrate only from new measured or
  authoritative evidence.

## Beta recovery and special cases

Treat the supervisor as a beta development feature without creating a second implementation:

1. When evidence proves a general supervisor defect, change the shared supervisor only if the repair is
   small, local, and low-risk. Add the narrow regression that proves that defect and rerun affected
   verification.
2. When only one command has unusual quoting, environment setup, or exit normalization, create the
   smallest task-local `.ps1` wrapper in that task's runtime/evidence directory and run the wrapper
   through the same supervisor. The wrapper adapts the command; it does not own polling, timeout,
   process cleanup, or terminal evidence.
3. Do not copy, fork, or reimplement the supervisor for a special case. Do not add a general feature
   for a one-off launch shape.
4. If the case cannot truthfully run through the supervisor, stop and record the exact incompatibility
   for orchestrator classification. Never bypass the bound silently.

Examples: put a heavily quoted command or temporary environment setup in one task-local wrapper;
choose a new unique result path after a path collision; correct the shared supervisor only when the
same evidenced defect applies generally.

## Plan adoption

Every execution plan that includes a covered Python, `.ps1`, or Bash/sh execution must adopt
`BOUNDED-TEST-v1` by reference. Each planned run or run group must declare its justified expected upper
bound, bounded cleanup allowance, computed maximum lifetime, heartbeat interval, unique result/evidence
location, timeout classification route, and the same single-supervisor special-case route. A plan must discover the
repository's current instruction, hook, and supervisor locations rather than assume one provider's
filenames.

## Enforcement pipeline

Repository instructions require the policy. A pre-execution command hook or equivalent provider
guard loads launcher names from `bounded-launchers.json`, resolves any script operand against the
command working directory, and rejects covered commands that neither use the supervisor nor match
`bounded-exclusions.gitignore`. The exclusion file uses ordinary Git-ignore patterns: a file pattern
excludes one launcher, while a directory pattern excludes that tree. Use the narrowest truthful rule;
do not exclude a general maintenance-script directory merely to free one orchestration launcher. Python
`-c`/`-m` and shell `-c` have no excludable script path. Missing or malformed configuration fails
closed. The supervisor itself must be an explicit script-path exclusion, not a broad command-string
bypass; an additional covered command appended after it remains blocked. The guard performs no semantic test classification. A PowerShell `-Command`/`-c` body is mechanically inspected for the same configured launchers. The
supervisor enforces runtime behavior. The orchestrator validates terminal evidence and classifies any
timeout. Hooks are a mistake guard, not the deadline owner and not a complete security boundary.

## Portable installation

On Windows, copying the repository-root `AGENTS.md` and the `.codex` directory carries this policy,
the Codex command guard, and the PowerShell supervisor without requiring the repository's product code
or execution plan. The bounded `PreToolUse` entry invokes the standard-library-only adapter directly.
Repository-specific Stop verification is conditional on the Plan 2 marker and is inactive in a copied
repository without that plan. The destination must be a Git repository because Git itself evaluates
the exclusion patterns. See `.codex/README.md` for the exact boundary and subagent-worktree rule.
