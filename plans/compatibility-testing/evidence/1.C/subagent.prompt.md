# Task: Phase 1, Area 1.C — Task & result lifecycle validation (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated inputs**. You do NOT
launch any `claude`/provider subprocess, you do NOT modify any harness source module, and you
do NOT "fix to green" — a test that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries the phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests with this exact environment (no third-party deps, Python 3.11+):
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_task_lifecycle -v
  ```
- Model fixtures on the EXISTING suite — read these FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_s2_contract.py` (canonical baseline, card/result dicts,
    `TaskValidationError` assertions, `SuiteFixture` from `tests/support.py`)
  - `orchestrator_harness/tests/support.py`
- Code under test: `orchestrator_harness/task.py`. Confirmed real symbols (grep to verify
  signatures before use): `TASK_CARD_SCHEMA`, `TASK_RESULT_SCHEMA`, `COMPLETION_REVIEW_SCHEMA`,
  `ORCHESTRATOR_ACCEPTANCE_SCHEMA`, `TaskValidationError`, `validate_task_card`,
  `validate_task_result`, `validate_completion_review`, `validate_orchestrator_acceptance`,
  `advance_task`, `read_task_advancement`, `record_sha256`. **Read the actual function bodies
  before asserting — use the REAL error types/messages the code raises, not guesses.**

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_task_lifecycle.py`

Fabricate a valid task card (D1/D2 already pass — copy the card dict from `test_s2_contract`),
then a task result / completion review / acceptance record; **mutate one field per test** and
assert the validator's behavior. No live lane — validators take records directly. One test
method per item:

1. **D3** task-result schema validation: malformed root shape → error; valid accepted.
2. **D4** result↔card identity cross-match: result referencing a different card id → error.
3. **D5** `.outcome` enum ∈ {PASS,FAIL,BLOCKED}: `"outcome":"DONE"` → error.
4. **D6** `.checks[]` shape + per-check outcome enum {PASS,FAIL,SKIP,NOT_RUN}: bad check outcome → error.
5. **D7** `.acceptance_state` enum {PENDING,ACCEPTED,REJECTED}: bad value → error.
6. **D8** completion-review schema validation: malformed → error.
7. **D9** completion-review result-identity cross-match: mismatched result id → error.
8. **D10** completion-review owner-must-own-task-card: foreign owner → error.
9. **D11** completion-review `.verdict` enum {PASS,FAIL,BLOCKED}: bad verdict → error.
10. **D12** orchestrator-acceptance schema validation: malformed → error.
11. **D13** orchestrator-acceptance identity cross-match: mismatch → error.
12. **D14** orchestrator-acceptance `.verdict` enum {ACCEPTED,REJECTED}: bad verdict → error.
13. **D15** `advance_task` state machine (`ACCEPTANCE_PENDING`→`ACCEPTED`/`REJECTED`): drive both transitions; assert resulting state.
14. **D16** advancement result-must-match-supplied-card: mismatched card → error.
15. **D17** advancement review/acceptance-identity cross-match: mismatch → error.
16. **D18** advancement acceptance-commit-must-match-result: mismatched commit → error.
17. **D20** schema-string constant surface: assert the 4 schema constants equal their documented `orchestrator-*/v1` strings.
> D19 already TESTED-PASSED (canonical_record) — re-assert as a guard only if trivial.

If a named validator behaves differently than D3–D20 describe (a mutation is NOT rejected, or
the enum set differs), **do not invent behavior** — write the test to document the ACTUAL
behavior (so the suite stays green) and record it as a FINDING.

## Pass criterion

- New module green under the run command above.
- Re-run `test_s2_contract` to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s2_contract -v`

## Findings (this is a detection suite)

Any mutation NOT rejected when the plan says it should be = a **FINDING**, not a fix target.
Document actual behavior in a green test; record in your report with feature ID, fabricated
input, expected vs. observed, and `task.py:<line>`. Never edit `task.py`.

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.C/`:
- `test-run.log` — full `-v` output of your new module (stdout+stderr).
- `s2-regression.log` — `-v` output of re-running `test_s2_contract`.
- (test module stays in the clone.)

## Final report (return as your last message)

A markdown table: one row per feature ID (D3–D20), each `PASS` / `FINDING` (one-line
what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and the
pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
