# Task: Phase 1, Area 1.A — Invocation schema & validation unit tests (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated inputs**. You do NOT
launch any `claude`/provider subprocess, you do NOT modify any harness source module, and you
do NOT "fix to green" — a test that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (the disposable clone, already carries the phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests with this exact environment (harness has no third-party deps, Python 3.11+):
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_invocation_rules -v
  ```
- Model your fixtures on the EXISTING suite — read these first to copy the idioms exactly:
  - `orchestrator_harness/tests/test_s2_contract.py` (canonical invocation baseline, the
    `_canonical(root)` helper pattern, `InvocationValidationError` / `TaskValidationError`
    assertions, `SuiteFixture` from `orchestrator_harness/tests/support.py`)
  - `orchestrator_harness/tests/support.py` (fixture helpers)
- Code under test: `orchestrator_harness/invocation.py` and
  `orchestrator_harness/lane_controller.py` (`load_invocation`). Read the actual functions
  named below before asserting — use the REAL error types and messages the code raises, not
  guesses.

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_invocation_rules.py`

Build one valid canonical `orchestrator-worker-invocation/v1` baseline (copy the dict from
`test_s2_contract.py`), then **mutate one field per test** and assert the exact rejection.
Each item below is one test method. Use the real symbols from `invocation.py`
(`InvocationValidationError`, `parse_canonical_invocation`, `CANONICAL_INVOCATION_SCHEMA`,
`adapt_coding_v1`, and the private helpers named) — grep for them to confirm names/signatures.

1. **C2** `action` ∈ {start,resume}: `action:"foo"` → `InvocationValidationError`; valid `start`/`resume` accepted.
2. **C3** resume needs non-empty session/thread id: `action:"resume"` with empty/missing id → error.
3. **C4** a `start` cannot carry a `resume` block: add `resume:{...}` to a `start` → error.
4. **C5** `provider.notification` must be boolean: `"notification":"yes"` → error; `true`/`false` accepted.
5. **C6** `profile.role` must match invocation role: mismatch → error.
6. **C7** `profile.provider` must match `provider.id`: mismatch → error.
7. **C8** `profile.model` must match `provider.model`: mismatch → error.
8. **C9** `prompt_bundle` schema/version validation: wrong schema string / version → error.
9. **C10** `resume_identity` must be an object: pass a string → error.
10. **C11** unknown invocation-schema string: `schema:"bogus/v1"` → `load_invocation` rejects.
11. **C16** ambiguous coding-alias rejection (`_reject_ambiguous_coding_aliases`): conflicting aliases → error.
12. **C18** canonical output-path safety/uniqueness (`_validate_canonical_output_paths`): duplicate or `../` traversal output path → error; unique safe paths accepted.
13. **C19** SHA-256 hex-digest format: 63-char / non-hex digest → error; valid 64-hex accepted.
14. **C20** string-list no-duplicates (`_string_list`): `allowed_tools:["Read","Read"]` → error.
15. **C21** `isolated_coding_child_environment`: assert the returned env strips inherited secrets and sets only the declared vars (construction assertion).
16. **C22** prior canonical acceptance read/persist (`_read_canonical_prior_status`/`_persist_canonical_acceptance`): persist a status, read it back byte-stable.
17. **C23** canonical resume-admission path & amendment-claims (`_canonical_resume_admission_path`/`_canonical_resume_claims_accepted`): valid claims accepted, tampered claims rejected.
18. **C24** provider-operation classification & handoff-identity (`_classify_provider_operations`/`_provider_handoff_identity`): start→launch / resume→resume classification and a stable handoff identity.
19. **C13/C14/C1 guards** (already known-good): re-assert repo path + `worktree_root==run_root` + closed-shape as guard tests.

If a named helper does not exist or has a different name/signature than the plan implies,
**do not invent behavior** — grep the module, use what is actually there, and note the
discrepancy as a finding (see Findings below).

## Pass criterion

- New assertions green: your module runs clean under the command above.
- Existing suite still green for the touched module — also run `test_s2_contract` to confirm
  you did not disturb shared fixtures:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s2_contract -v`

## Findings (critical — this is a detection suite)

If any mutation is **NOT** rejected when the plan says it should be (or the validator behaves
differently than C2–C24 describe), that is a **FINDING**, not a failure to fix. Write a test
that documents the ACTUAL behavior (so the suite stays green), and record the gap in your
final report with: feature ID, the fabricated input, expected vs. observed, and the
`invocation.py:<line>` of the code under test. Never edit `invocation.py` to make a test pass.

## Evidence to leave behind

Write these into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.A/`:
- `test-run.log` — the full `-v` unittest output of your new module (redirect stdout+stderr).
- `s2-regression.log` — the `-v` output of re-running `test_s2_contract`.
- (the test module itself lives in the clone at
  `orchestrator_harness/tests/test_compat_invocation_rules.py` — leave it there.)

## Final report (return as your last message)

A markdown table: one row per feature ID (C2–C24 + guards), each `PASS` (mutation correctly
rejected / behavior as documented) / `FINDING` (with one-line what-differed) / `BLOCKED`
(with why). Then: the exact command(s) you ran, the count of tests, and the pass/fail tally.
Do not modify any file outside your new test module and the evidence dir.
