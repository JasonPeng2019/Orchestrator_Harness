# Task: Phase 1, Area 1.E — Reconcile state classification (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated `ProcessSnapshot` /
status / record inputs**. You do NOT launch any `claude`/provider subprocess or any real OS
process, you do NOT modify any harness source module, and you do NOT "fix to green" — a test
that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_reconcile_classify -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_reconcile.py` (uses `SuiteFixture.create()`,
    `self.fixture.status(...)`, `self.fixture.process_snapshot(...)`, then
    `reconcile(discover_suite(cfg), snapshot, cfg, now=NOW)` and asserts the derived
    `operational_state` / relay / request classifications). Copy this `observe()` helper.
  - `orchestrator_harness/tests/support.py` (SuiteFixture), `orchestrator_harness/models.py`
    (`ProcessInfo`, `ProcessSnapshot`).
- Code under test: `orchestrator_harness/reconcile.py` (and `discovery.py`). Real derived
  states confirmed present: `WAITING_RELAY`, `HELPER_RUNNING`/`HELPER_EXITED`/
  `HELPER_STATE_UNKNOWN`, `PROCESS_STATE_UNKNOWN`, `EXITED`/`UNKNOWN`, relay `BOUND`/
  `BOUND_EXPIRED`/`UNBOUND`/`ABSENT`, `RELAY_READY`/`RELAY_UNBOUND`/`REQUEST_AMBIGUOUS`,
  `_record_kind`, `_is_utc_timestamp`. **Read the actual classification code before asserting
  — drive states through the fixture the way `test_reconcile.py` does; do not hand-call
  private helpers unless the plan item explicitly names one (`_record_kind`,
  `_is_utc_timestamp`).**

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_reconcile_classify.py`

Fabricate the inputs (no live process) and assert the derived classification. One test method
per item:

1. **F3** `WAITING_RELAY`: fixture with an unbound relay + a pending request → lane's
   `operational_state` becomes `WAITING_RELAY`.
2. **F4** helper tri-state `HELPER_RUNNING`/`HELPER_EXITED`/`HELPER_STATE_UNKNOWN`: three
   fixtures → three classifications.
3. **F7** `PROCESS_STATE_UNKNOWN` fail-closed on incomplete evidence: omit process evidence →
   `PROCESS_STATE_UNKNOWN` (never a false "running").
4. **F8** `EXITED`/`UNKNOWN` terminal states: dead-PID / no-evidence fixtures → each.
5. **F10** relay-binding `BOUND`/`BOUND_EXPIRED`/`UNBOUND`/`ABSENT`: four relay fixtures →
   four states (BOUND_EXPIRED via an `expires` timestamp before `now=NOW`).
6. **F11** request-lifetime `LIVE`/`ABSENT`/`UNKNOWN`: three request fixtures.
7. **F12** expiry-bucket `WARNING`/`CRITICAL`/`EXPIRED`/`UNKNOWN`: vary timestamps across the
   bounds → each bucket.
8. **F14** `RELAY_READY`/`RELAY_UNBOUND`/`REQUEST_AMBIGUOUS`: ready / unbound / two-request
   fixtures.
9. **F16** duplicate coding worktree/branch at reconcile layer: assert
   `DUPLICATE_CODING_WORKTREE` / `DUPLICATE_CODING_BRANCH`.
10. **F19** record-kind classification (`_record_kind`): each declared kind → correct
    classification.
11. **F22** UTC-timestamp validation (`_is_utc_timestamp`): non-UTC / malformed timestamp →
    rejected; a valid UTC one accepted.
12. **F24** memoized coding/task-result validation cache: validate twice → assert the cached
    path is taken and a signature change invalidates it. (If no observable cache hook exists,
    record as BLOCKED with the reason.)

If a classification differs from F3–F24 (wrong state, or a false "running" where fail-closed
is expected), **do not invent behavior** — write the test to document ACTUAL behavior and
record a FINDING (fail-closed violations are higher severity — flag them clearly).

## Pass criterion

- New module green under the run command above.
- Re-run `test_reconcile` to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_reconcile -v`

## Findings (detection suite)

Any classification NOT matching the plan = a **FINDING**. Document actual behavior in a green
test; record with feature ID, fabricated input, expected vs. observed, and `reconcile.py:<line>`.
Never edit `reconcile.py`/`discovery.py`.

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.E/`:
- `test-run.log` — full `-v` output of your new module (stdout+stderr).
- `reconcile-regression.log` — `-v` output of re-running `test_reconcile`.

## Final report (return as your last message)

A markdown table: one row per feature ID (F3–F24 in this area), each `PASS` / `FINDING`
(one-line what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and
the pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
