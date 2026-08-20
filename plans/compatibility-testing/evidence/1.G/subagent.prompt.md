# Task: Phase 1, Area 1.G — Resume & handoff admission (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated identity / amendment /
invocation / preflight-bundle inputs**. You do NOT launch any `claude`/provider subprocess, you
do NOT modify any harness source module, and you do NOT "fix to green" — a test that reveals a
real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_resume_admission -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_s2_contract.py` — **your primary model**. Lines ~170-410
    build fabricated review cards, call `make_resume_admission(identity, persisted, live)` and
    assert `.admitted` (True for matching identity + live/non-terminal; False for wrong identity
    or terminal persisted), and drive `validate_resume_amendment_review` with card/prompt
    amendments. Copy its `_amendment_review` helper and workspace setup.
  - `orchestrator_harness/tests/test_handoff_preflight.py` — model for K10.
  - `orchestrator_harness/tests/support.py`.
- Code under test (grep bodies before asserting — do NOT guess args/messages):
  - `orchestrator_harness/resume.py`: `ResumeAdmission` (class, :566), `_compare_identity`
    (:611), `make_resume_admission` (:633), `require_resume_admission` (:720),
    `validate_resume_amendment_review` (:224), `_review_card_payload` (:135),
    `_review_path_digest` (:127), `_validate_review_diff_command` (:146), `_review_job_identity`
    (:192), `ResumeAdmissionError` (:37).
  - `orchestrator_harness/handoff_preflight.py`: `preflight_handoff` (:410).
  - **K8 precedence lives in `orchestrator_harness/invocation.py:698-722`** (NOT resume.py):
    `resume_thread_id` is the legacy field; `resume_identity.thread_id` is canonical. The actual
    logic is: if BOTH are set and they DIFFER → raise
    `InvocationValidationError("conflicting requested resume thread IDs")`; if non-conflicting,
    `requested_thread = requested_thread or identity_thread_text` (legacy value used when both
    equal). **This is a conflict-rejection, not "canonical silently wins" — verify the real
    behavior and, if it differs from the plan's "canonical wins per precedence", record a FINDING.**

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_resume_admission.py`

Fabricate identity / amendment / invocation inputs (no live lane). One test per item:

1. **K2** identity-matching gate: `make_resume_admission(identity, persisted, live)` with
   matching identity + non-terminal persisted → `.admitted` True. (Model on test_s2_contract:289.)
2. **K3** identity-mismatch rejection (`_compare_identity`): wrong manager/session identity →
   `.admitted` False (or `require_resume_admission` raises `ResumeAdmissionError`).
3. **K4** amendment diff-based review validation (`validate_resume_amendment_review`): a valid
   diff-review accepted; a missing/altered review → rejected.
4. **K5** review-card payload + digest (`_review_card_payload`/`_review_path_digest`): tamper the
   payload so the digest no longer matches → rejected.
5. **K6** diff-command safety (`_validate_review_diff_command`): a diff command with shell
   metacharacters / a non-git command → rejected; a safe `git diff …` accepted.
6. **K7** job-identity derivation (`_review_job_identity`): assert it is stable and matches the
   amendment's declared identity.
7. **K8** thread-id precedence: build an invocation with BOTH `resume_thread_id` and
   `resume_identity.thread_id`. (a) equal values → accepted, resolved thread == that value;
   (b) DIFFERING values → `InvocationValidationError("conflicting requested resume thread IDs")`.
   Assert the ACTUAL behavior; if it is not "canonical wins", record a FINDING.
8. **K10** handoff preflight gate (`preflight_handoff`): missing invocation file / amendment
   identity mismatch / missing required evidence → each blocks with a DISTINCT reason; a complete
   bundle passes. (Model on test_handoff_preflight.py.)

If a validator behaves differently than K2–K10 describe, **do not invent behavior** — document
ACTUAL behavior in a green test and record a FINDING (feature ID, input, expected vs. observed,
`resume.py:<line>` / `invocation.py:<line>` / `handoff_preflight.py:<line>`). Never edit source.

## Pass criterion

- New module green under the run command above.
- Re-run the model suites to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s2_contract orchestrator_harness.tests.test_handoff_preflight -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.G/`:
- `test-run.log` — full `-v` output of your new module.
- `resume-regression.log` — `-v` output of re-running the two model suites.

## Final report (return as your last message)

A markdown table: one row per feature ID (K2–K8, K10), each `PASS` / `FINDING` (one-line
what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and the pass/fail
tally. Do not modify any file outside your new test module and the evidence dir.
