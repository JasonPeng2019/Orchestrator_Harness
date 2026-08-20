# 1.G coordinator note — subagent cut off, module completed by coordinator

The `deepseek-v4-flash:0731-cloud` subagent (task `b1253dkb1`, `--effort high`, local Ollama,
env-scoped launcher) **authored the full 42 KB module** `test_compat_resume_admission.py`
(K2–K8 + K10) but hit the Ollama session usage limit (HTTP 429,
"you (jasonpeng2019) have reached your session usage limit") **before it could run the module
once**. It left no `test-run.log`, no regression log, and returned only the 429 in its result
envelope. `subagent.stdout.jsonl` / `subagent.stderr.log` capture the truncated run.

## What the coordinator did (detection-only discipline preserved)

The subagent's module had 7 failing tests (5 fail + 2 error), all from **fixture-authoring
mistakes the subagent never got to run and correct** — not source gaps:

1. **K4/K5/K6 identity gate (all 7 originally).** `_same_job_identity` hardcoded
   `continuation_start_commit = "0"*40`, but `validate_resume_amendment_review` derives the
   expected value from `persisted["repository"]["starting_commit"]` — which the fixtures set to
   `"a"*40` via `canonical.identity(starting_commit="a"*40)`. The identity gate at
   `resume.py:306-316` therefore raised `same-job identity mismatch: continuation_start_commit`
   before any test reached its actual target. **Fix:** align the fixture constant to `"a"*40`
   (the value the resume identity actually carries). One line.

2. **K5 case (2) digest-consistent tamper.** The test rewrote `new_card` with an
   identity-tampered payload (`card_id="card-2"`) and rebuilt the review so the review's own
   `new_sha256` matched — but left `requested["task_card_sha256"]` on the original hash, so the
   **outer** requested-identity digest binding (`resume.py:397`) fired first with
   "new identity does not match requested resume identity" instead of the intended payload
   cross-pair check. **Fix:** advance `requested["task_card_sha256"]` to the tampered hash too,
   so the tamper clears BOTH digest gates and is caught by the payload cross-pair identity check
   (`resume.py:431`, "changed across the pair") — the guard the test set out to prove. This is
   the faithful realization of the test's own stated intent ("digest-consistent payload tamper").

Both edits are test-fixture corrections that make the assertions match **actual** source
behavior. No source module was touched (git shows only the pre-existing phase-0 `M` files plus
the new untracked test module). No behavior was invented.

## Finding filed

- **F1G-K8-1** (note): the coding-v1 adapter fails *closed* on conflicting resume thread IDs
  (`invocation.py:716-722`) rather than "canonical wins" as the plan described. The subagent had
  pinned this inline in `test_k8_...` but 429'd before filing it in `FINDINGS.md`; the
  coordinator recorded it.

## Verification

- `test_compat_resume_admission` → 11/11 OK (`test-run.log`).
- Regression `test_s2_contract` + `test_handoff_preflight` → 27/27 OK (`resume-regression.log`).
- `git status` → only phase-0 `M` files + the new untracked module. No leak, no source edit.
