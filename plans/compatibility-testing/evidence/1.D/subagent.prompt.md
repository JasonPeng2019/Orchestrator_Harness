# Task: Phase 1, Area 1.D — Git safety & result-merge validation (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests** using **real disposable `git init`
worktrees** + fabricated result records. You do NOT launch any `claude`/provider subprocess,
you do NOT modify any harness source module, and you do NOT "fix to green" — a test that
reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_git_safety -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_git_results.py` (how it does `git init`, makes commits,
    builds worktrees, fabricates `orchestrator-lane-result/v1` records, asserts
    `GitSafetyError`)
  - `orchestrator_harness/tests/support.py`
- Code under test: `orchestrator_harness/git_safety.py`. Confirmed real symbols (grep to
  verify signatures/messages before use): `GitSafetyError`, `GitDeclaration`, `GitIdentity`,
  `validate_findings`, `declaration_from_invocation`, `declaration_from_status`,
  `inspect_repository`, `repository_status`, `active_declaration_conflicts`,
  `validate_coding_result`, `invalid_result_evidence`, `validate_task_result_repository`,
  and the module constants `_RESULT_OUTCOMES={PASS,FAIL,BLOCKED}`,
  `_CHECK_OUTCOMES={PASS,FAIL,SKIP,NOT_RUN}`. **Read the actual function bodies before
  asserting — use the REAL error types/messages the code raises.** On Windows, git worktree
  ops and read-only perms behave as on the existing suite; follow `test_git_results.py`'s
  exact setup/teardown (it already handles Windows temp-dir cleanup).

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_git_safety.py`

Use a real disposable `git init` worktree + fabricated result records. One test method per item:

1. **E4** repository-identity-must-be-reported: omit reported identity → error.
2. **E5** detached-HEAD rejection: put the worktree on a detached HEAD → coding-worktree validation error.
3. **E6** commit-identity format validation: malformed commit id (not 40/64 hex) → error.
4. **E7** duplicate active worktree/branch (`active_declaration_conflicts`): two declarations, same branch/worktree → conflict reported.
5. **E14** coding-result root-shape + `orchestrator-lane-result/v1` schema: malformed → error.
6. **E15** lane_id / branch / outcome-enum cross-match vs. current lane: mismatched lane_id → error.
7. **E16** per-check shape (name-or-command required, outcome enum): check missing both name and command → error.
8. **E17** commit-must-equal-branch-tip (dirty/stale-tree rejection): make the tree dirty / point at a non-tip commit → error.
9. **E18** `CODING_RESULT_INVALID` durable evidence + clearing: an invalid result writes evidence (`invalid_result_evidence`); a corrected result clears it. Assert both.
10. **E19** operational-state gate (accept only in `RUNNING_CODEX`/`RUNNING_PROVIDER`): offer a result while state is e.g. `EXITED` → rejected; while `RUNNING_PROVIDER` → considered.
11. **E20** too-many-JSON-candidates ambiguity: drop 2 candidate result JSONs under the result workspace → ambiguity rejection (`_MAX_JSON_CANDIDATES_PER_WORKTREE` is the bound; here it's the >1 ambiguity path).

If a validator behaves differently than E4–E20 describe (a mutation is NOT rejected, or an
enum/guard differs), **do not invent behavior** — write the test to document ACTUAL behavior
(so the suite stays green) and record a FINDING.

## Pass criterion

- New module green under the run command above.
- Re-run `test_git_results` to confirm you did not disturb shared git fixtures:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_git_results -v`

## Findings (detection suite)

Any mutation NOT rejected when the plan says it should be = a **FINDING**, not a fix target.
Document actual behavior in a green test; record with feature ID, fabricated input,
expected vs. observed, and `git_safety.py:<line>`. Never edit `git_safety.py`.

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.D/`:
- `test-run.log` — full `-v` output of your new module (stdout+stderr).
- `gitresults-regression.log` — `-v` output of re-running `test_git_results`.

## Final report (return as your last message)

A markdown table: one row per feature ID (E4–E20 in this area), each `PASS` / `FINDING`
(one-line what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and
the pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
