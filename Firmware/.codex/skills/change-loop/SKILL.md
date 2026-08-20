---
name: change-loop
description: "Define the future repair contract for verified BYO-Firmware-MCP production defects. Provider-adapter implementation is intentionally pending, so this skill cannot start a live role."
---

# Change Loop — BYO-Firmware-MCP server repairs only

## Scope boundary

This workflow is reserved for a verified production-code defect in the
`BYO-Firmware-MCP` server. It may be started only by the Firmware test
orchestrator after it has independently classified a `SERVER_FAILURE` as a
server defect.

The current main model inspects and plans against `BYO-Firmware-MCP` directly. The doer, spec
tester, and regression tester all run with that repository as their workspace/root. Their
commands, reads, and edits must stay there; they must not use a fresh-experiment directory as a
workspace. The scripts enforce this repository-root boundary before preparation, validation, or
execution.

## Current provider-adapter status

See the [Firmware provider-adapter contract](../../../PROVIDER_ADAPTER.md) for provider status and
logical role allocation. `agent.sh` and a normal `run_loop.sh` invocation deliberately refuse to
start or resume a provider session. This is not a temporary fallback runner: it prevents an
unreviewed provider configuration from becoming live.

The user will choose and implement the provider adapter later. Until then, use `plan-changes` to
prepare/validate a repair plan and `run_loop.sh --self-check` to validate the local repair assets;
do not attempt a live production-server repair from this package.

Do **not** use it for:

- fresh-experiment firmware, application tests, fixtures, wiring, SDK/toolchain, or infrastructure work;
- experiment specifications, evidence collection, reviewer feedback, or a missing proof;
- documentation-, metadata-, or repository-contract-only changes that do not alter server behavior; or
- a test agent's own repair attempt.

Fresh-experiment test agents must not invoke, read, or apply `$change-loop` or
`$plan-changes`. They report a well-evidenced `SERVER_FAILURE` to the main
model; only that model may initiate a server repair in the server repository.

## Start here

Prerequisites:

- Run the orchestration commands from the `Firmware/` suite root and set
  `CL_REPO_ROOT=BYO-Firmware-MCP`. Delegated roles are launched with that server repository as
  their working directory.
- Before a production repair, the main model reads `BYO-Firmware-MCP/README.md`,
  `BYO-Firmware-MCP/SERVER_GUIDE.md`, the applicable linked client/plan contract, and
  `Firmware resources/test-program/design_charter.md`. These are package-local inputs; do not
  substitute historical copies under `Firmware resources/test-program/`.
- Install Python 3, `git`, and Bash for the local plan and self-check commands. On Windows, run
  those Bash commands from Git for Windows (or another Bash distribution); do not translate them
  piecemeal into PowerShell.
- Keep the sibling repo-local `$plan-changes` skill at
  `.codex/skills/plan-changes`; its script scaffolds and validates the main-authored plan.
- The provider route is not configured yet; the provider-adapter contract owns its eventual
  selection. Do not start a live repair now.

Quick start after saving the request in `changes.md`:

```bash
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare changes.md
# The current main model inspects the repo and authors the external repair runtime's plan.md directly.
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --validate
# The package validates its local repair assets but deliberately does not launch a provider:
bash .codex/skills/change-loop/scripts/run_loop.sh --self-check
```

For a pasted request:

```bash
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/plan-changes/scripts/plan.sh --prepare --text \
  "Add JSON output while preserving text output."
```

The [Firmware provider-adapter contract](../../../PROVIDER_ADAPTER.md) owns the complete future
role allocation and adapter requirements. The later adapter must make its
unrestricted/no-command-approval configuration explicit and must not rely on parent configuration
or automatic approval review. That future launch policy does not weaken the plan review, neutral
test gate, or server behavioral safety constraints.

## Orchestrator workflow

1. **Author the plan as the current main model.** Use `$plan-changes` to prepare the narrow
   server-change request. Inspect the repository yourself, write `$CL_RUN_DIR/plan.md` directly,
   and run `plan.sh --validate`. Never launch a planner subagent or let the doer/testers author it.
2. **Review the plan once.** Reuse the selected sprint/module's contract-designated, read-only
   reviewer for one independent adversarial review of that exact plan, then
   reuse it for the terminal repair-evidence review. It never edits the server, firmware, harness,
   tests, or suite state.
   Record its risks and test targets in `$CL_RUN_DIR/plan-review.md`. This review is not a
   replanning loop: it must not regenerate or edit the plan, require repeated verdicts, or delay the
   repair. Feed its findings to the doer and testers as execution risks. The reviewer reports both
   actionable and advisory findings; only an evidenced requirement violation, credible
   safety/data-loss risk, reproducible failure, or likely production/orchestration failure is
   actionable. Style preferences, speculative hardening, vanishingly unlikely cases without
   evidence, and requests for unrelated features are advisory and do not block delivery.
3. **Stop at the prepared plan for now.** `scripts/run_loop.sh` has no live-provider path while the
   adapter is pending. After the user implements and validates the adapter, it must launch every
   role inside the server repository and preserve the ownership contract below.

The one-time review file must state the reviewed plan's SHA-256, reviewer identity, and numbered
risks/test targets. Do not replace a plan merely to seek another verdict. If execution proves a
**genuine plan mistake**, the main model may make a minimal amendment in
`$CL_RUN_DIR/plan-amendments.md` that records the evidence, exact changed requirement, and
preserved contracts. Review only that amendment once, append the targeted review to the same file,
then resume execution. Do not regenerate the whole plan or re-review unchanged plan items. The
loop's neutral gate and focused post-repair retest decide correctness.
4. **Preserve role identity when the adapter exists.** The future adapter must start one doer, one
   spec tester, and one regression tester on first use, record their provider-session IDs, and
   resume those same sessions on every later iteration and process restart.
5. **Trust the incremental neutral gate.** Tester prose and the one plan-review report are
   diagnostic only. Green means each tester suite has either a passing execution against the
   affected current behavior or a validated reuse of unchanged passing evidence. Never rerun a
   previously passing expensive suite merely because the other suite, an advisory criticism, or an
   unrelated check failed.
6. **Inspect honest stops.** On infrastructure failure, tampering, repeated identical failure, or
   `MAX_ITERS`, read the paths printed by the script rather than claiming partial success.

Stop immediately when the accepted product behavior is implemented and the incremental neutral
gate is green. Do not launch another adversarial turn to pursue perfection. A new criticism after
green is recorded as advisory unless it demonstrates a concrete failure of an accepted requirement
or invalidates evidence used by the gate.

The role order is always:

```text
doer -> spec tester -> regression tester -> neutral gate
```

Keep it sequential. Parallel persistent provider sessions can race on shared repair state. If
parallelism is added later, give every role an isolated provider state directory.

## Role and edit ownership

### Doer

- Implements `$CL_RUN_DIR/plan.md` and reads the latest `test_report.md` on later turns.
- Is the only role allowed to edit production source.
- Is the contract's only canonical server-source writer for that repair.
- Must not modify any tests, tester manifests/snapshots, test command/mode files, or neutral pass
  caches.

### Spec tester

- Attempts to disprove every `CL-NNN` plan item with automated tests.
- Uses the contract's test/scaffolding allocation.
- Edits tests only.
- Writes its exact isolated command to `$CL_STATE_DIR/spec_test_cmd`.
- Writes `RUN` or `REUSE` plus an evidence-based rationale to
  `$CL_STATE_DIR/spec_test_mode`. `REUSE` is allowed only after a prior pass when the current
  diff cannot affect the covered behavior.
- Lists its repo-relative test paths in `$CL_STATE_DIR/spec_tester.manifest`.

### Regression tester

- Traces the doer's diff through callers, shared modules, interfaces, and adjacent features.
- Uses the contract's test/scaffolding allocation.
- Edits tests only and does not alter the spec tester's files.
- Writes its command to `$CL_STATE_DIR/regression_test_cmd`.
- Writes `RUN` or `REUSE` plus an evidence-based rationale to
  `$CL_STATE_DIR/regression_test_mode` under the same unaffected-evidence rule.
- Lists its paths in `$CL_STATE_DIR/regression_tester.manifest`.

Both testers keep their scope proportional to the accepted plan and actual diff. They may report
nonblocking hardening ideas, but must not create blocking tests for speculative perfection,
unrelated features, or edge cases whose cost is disproportionate to their evidenced production
risk.

When the future adapter is implemented, the repair workflow must snapshot each manifested test
after its tester turn and reject a doer change to protected tests or gate controls. Any difference
forces the iteration red and becomes feedback for the next doer turn.

## Runtime state

All project-specific state stays outside the production server tree. For an experiment repair set
`CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<repair-id>`. If no
owning experiment exists yet, the temporary default is
`../.agent-workspace/server-repair-runtime/current`; relocate its concise terminal records to the
owning experiment when the repair closes.

```text
fresh-experiments/<run>/.agent-workspace/server-repairs/<repair-id>/
  changes.md
  plan.md
  plan-review.md
  plan-amendments.md # only when a genuine plan mistake is proven
  logs/<role>.turn-NNN.log # created only by a future provider adapter
  state/
    <role>.provider-session # created only by a future provider adapter
    *_test_cmd
    *_test_mode
    *.manifest
    *.manifest.snapshot
    *.pass-cache
    test_report.md
    non_convergence.md
```

Never copy provider-session IDs between roles. A future resume must preserve its recorded session
instead of silently opening a replacement session.

## Scripts

### `scripts/run_loop.sh`

Purpose: validate local repair assets and explicitly block an unimplemented live-provider loop.

```bash
bash .codex/skills/change-loop/scripts/run_loop.sh --dry-run
bash .codex/skills/change-loop/scripts/run_loop.sh --self-check
```

- Parameters: `--dry-run` prints the logical role allocation without touching a repository;
  `--self-check` checks layout, every shell script with `bash -n`, prompt construction, and a
  temporary two-command neutral gate.
- No-argument use returns a clear pending-adapter error before any provider session or repair
  runtime state exists. It does not run a server repair.

### `scripts/agent.sh`

Purpose: validate one future persistent loop-role request without launching it.

```bash
bash .codex/skills/change-loop/scripts/agent.sh --dry-run doer prompt.md
```

- Parameters: `ROLE` (`doer`, `spec_tester`, or `regression_tester`) and a nonempty prompt file.
- `--dry-run` prints the selected model and reasoning level. Without it, the script fails clearly
  before it writes a provider session, log, or role state.

### `scripts/run_tests.sh`

Purpose: run the two tester-authored commands independently of agent claims.

```bash
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/change-loop/scripts/run_tests.sh
CL_REPO_ROOT=BYO-Firmware-MCP bash .codex/skills/change-loop/scripts/run_tests.sh --dry-run
```

- Parameters: none, or `--dry-run` to print commands.
- Reads: `spec_test_cmd` and `regression_test_cmd`.
- Reads each tester's `RUN`/`REUSE` decision and rationale. `REUSE` succeeds only when a prior PASS
  cache exists and the command and manifested test-file fingerprints are unchanged.
- Writes: one output log per executed/reused suite, pass caches, and deterministic
  `test_report.md` with mode, result, exit code, and output tail.
- Returns: `0` when both suites have current run-passes or validated unaffected-pass reuse, `1`
  when an executed suite fails, and `2` for missing/invalid configuration.
- Recovery: have the responsible tester write a valid isolated command; run it manually from the
  repo root if framework setup is failing.

### `scripts/lib.sh`

Purpose: centralize local runtime paths and neutral-gate settings. Provider allocation belongs only
to `PROVIDER_ADAPTER.md`; this helper contains no provider executable, provider CLI flags, or
provider-session parser. Source it; do not execute it as a workflow.

## Configuration

All defaults live in `scripts/lib.sh` and are overridden through environment variables:

| Variable | Default | Effect and recovery |
|---|---|---|
| `CL_RUNTIME_DIR` | `../.agent-workspace/server-repair-runtime/current` | Runtime directory outside the server tree but inside `Firmware/`. For experiment repairs set it to `../fresh-experiments/<run>/.agent-workspace/server-repairs/<repair-id>`. |
| `MAX_ITERS` | `8` | Positive iteration ceiling. Raising it does not bypass identical-failure stopping. |
| `CL_TEST_TAIL_LINES` | `120` | Positive number of lines retained per suite in the report. |
| `CL_PYTHON_BIN` | `python3` | Python 3 executable used by the package-local prompt-policy helper. |
| `CL_BASH_BIN` | `bash` | Bash executable name/path for commands and checks. |
| `CL_REPO_ROOT` | Git top level | Optional explicit target root; it still must be a Git repository. |

Example:

```bash
MAX_ITERS=5 bash .codex/skills/change-loop/scripts/run_loop.sh --dry-run
```

## Incremental retest and review budget

- Preserve a passing suite's evidence across iterations. Rerun it only when its command or tests
  changed, the production diff reaches behavior it covers, its evidence became invalid, or it
  previously failed.
- After a failure, rerun the failed check and the smallest affected regression surface. Do not
  restart the change-loop, discard valid pass caches, or rerun every expensive test from scratch.
- The one plan review and any one-time amendment review are the complete adversarial review budget.
  Tester iterations exist to validate functional changes, not to reopen accepted requirements or
  accumulate optional robustness work.
- The main orchestrator classifies reviewer findings. It fixes actionable product defects and
  records but declines advisory perfection work. Green objective gates end the loop immediately.

## Termination conditions

- **Green:** both suites have current or validated reused passes and no doer tamper is detected.
- **No progress:** the complete failure-report signature is identical twice consecutively; exit 3.
- **Iteration bound:** iteration `MAX_ITERS` remains red; exit 4.
- **Infrastructure stop:** a role, event schema, prerequisite, manifest, or command is invalid; exit
  2 with the recovery path.

When the user later implements the adapter, validate it with a host-only smoke test before any
server, MCP, or hardware action. Do not start a live role merely to discover provider settings.

The workflow never commits, pushes, deploys, or treats an agent's self-report as test evidence.
