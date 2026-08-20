# Task: Phase 1, Area 1.H — Resource-lock invocation semantics (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests** using **filesystem-only resource
claims** + fabricated `ProcessSnapshot` inputs. You do NOT launch any `claude`/provider
subprocess, you do NOT modify any harness source module, and you do NOT "fix to green" — a test
that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_resource_locks -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_resource_locks.py` — **your primary model**: builds a temp
    root, `ResourceClaims(...)`, `ProcessInfo`/`ProcessSnapshot` via its `process()`/`snapshot()`
    helpers, `acquire_all(resources, on_wait=...)` with an `abort_wait` to avoid blocking, and
    inspects `_read_claim_evidence` / `claim_filename`. Copy this exactly (esp. the `AbortWait`
    non-blocking trick — NEVER block the test).
  - `orchestrator_harness/tests/test_reconcile.py` — model for the H10 reconcile fixture.
  - `orchestrator_harness/tests/support.py`.
- Code under test (grep bodies before asserting — do NOT guess args/messages):
  - `orchestrator_harness/resource_locks.py`: `ResourceClaims` (:317), `_create` (:362,
    returns a `Claim` or `None` when the resource is already held by a live owner), `acquire_all`
    (:599, `on_wait` callback), `release_all` (:411), `claim_filename` (:89),
    `_read_claim_evidence` (:100), `_owner_state` (:256), `ResourceLockError` (:33).
  - `orchestrator_harness/invocation.py`: `exclusive_resources` is canonicalized to `resources`
    at :687 (`resources` = `raw["resources"]` or `raw["exclusive_resources"]`); a coding-v1
    invocation with BOTH `resources` and `exclusive_resources` that DIFFER raises
    `InvocationValidationError("coding v1 resources and exclusive_resources conflict")` (:137-141).
  - H10 signal path: `reconcile.py:1424` sets `lane["resource_release_possible"]`; `events.py:222-226`
    emits the `RESOURCE_RELEASE_POSSIBLE` event from that flag.

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_resource_locks.py`

One test per item (filesystem-only; never block — use the `abort_wait`/`on_wait` idiom):

1. **H9a** `exclusive_resources` canonicalization: a canonical invocation declaring
   `exclusive_resources: ["gpu0"]` (no `resources`) → canonical `resources == ["gpu0"]`
   (`validate_*_invocation` / the canonicalization at invocation.py:687). A coding-v1 invocation
   with `resources` and `exclusive_resources` that DIFFER → `InvocationValidationError` conflict.
2. **H9b** exclusive claim blocks a second claimant: claimant A `acquire_all(["gpu0"], ...)`
   succeeds (claim file written); claimant B (different identity, A's owner PID live in the
   snapshot) attempting `gpu0` → `_create` returns `None` / `on_wait` fires (B blocks), and B does
   NOT get the claim. Assert exactly the declared resource(s) are claimed, nothing else.
3. **H10** release-possible on owner exit: build a reconcile fixture where a lane owns a resource
   claim and the owner PID is ABSENT from a complete snapshot (simulated owner exit) → the derived
   lane carries `resource_release_possible` truthy, and (drive `conditions_from_snapshot`/events)
   a `RESOURCE_RELEASE_POSSIBLE` event/condition fires. If the flag is set but no event is
   emitted at this layer, document the actual behavior and note it.

If behavior differs from H9/H10 (a second claimant is NOT blocked, or release-possible does not
fire on owner exit — a **fail-closed / safety-relevant** difference is HIGHER severity, flag it
clearly), **do not invent behavior** — document ACTUAL behavior in a green test and record a
FINDING (feature ID, input, expected vs. observed, `resource_locks.py`/`invocation.py`/
`reconcile.py`/`events.py:<line>`). Never edit source.

## Pass criterion

- New module green under the run command above.
- Re-run the model suites to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_resource_locks orchestrator_harness.tests.test_reconcile -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.H/`:
- `test-run.log` — full `-v` output of your new module.
- `locks-regression.log` — `-v` output of re-running the two model suites.

## Final report (return as your last message)

A markdown table: one row per feature ID (H9, H10 — split H9 into H9a/H9b if useful), each
`PASS` / `FINDING` (one-line what-differed) / `BLOCKED` (why). Then the exact commands run, the
test count, and the pass/fail tally. Do not modify any file outside your new test module and the
evidence dir.
