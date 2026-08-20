# Task: Phase 2, Area 2.D — Operator launch & exact-identity process supervision (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** that drive the real
`orchestrator_harness.operator_launch` seams by launching a short-lived, harmless stand-in child
(`[sys.executable, "-c", "import time; time.sleep(...)"]`). No real lane, no `claude`/provider.
You do NOT modify any harness source module and you do NOT "fix to green". Pin ACTUAL behavior.

**SAFETY (critical):** every child you launch MUST be reliably cleaned up. Use short sleeps
(≤4s) and `self.addCleanup(...)` that terminates the exact launched PID (via
`_cleanup_exact_posix` on POSIX, or `os.kill(pid, 9)` best-effort inside a try/except). Never
launch anything but a `sleep` stand-in. Never signal a PID you did not launch.

## Where you are

- Working dir: `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run: `cd` there, then
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_operator_launch -v`
- **Idiom model — READ FIRST:** `orchestrator_harness/tests/test_operator_launch.py`
  (how `launch_process(...)` is called, how `detached_owner_snapshot()` is drained, the
  `sys.executable, "-c", "import time; time.sleep(2)"` stand-in, and the `process_snapshot()`
  liveness check via `orchestrator_harness.processes`).

## Code under test — `orchestrator_harness/operator_launch.py`

- `launch_process(*, receipt, label, role, cwd, argv, expected_state_path=None, environment=None)`
  (:284) → dict `{schema, status:"launched", label, role, argv, cwd, pid, created_utc,
  launched_utc, platform, creationflags, ownership_strategy, ...}`. `receipt` must NOT already
  exist (its parent must); `cwd` must be an existing dir; `argv` nonempty strings. It records the
  `(pid, created_utc)` into an in-module `_DETACHED_RECORDS` ledger and writes the receipt file
  atomically. **This is O7 / A35** (exact creation identity captured).
- `detached_owner_snapshot()` (:74) → list of live records `{pid, created_utc, label, role,
  ownership_strategy, state:"live"}`; a record whose PID is gone OR whose `created_utc` no longer
  matches is pruned as stale. **This is O8.**
- `_cleanup_exact_posix(pid, created_utc)` (:108) → `(confirmed: bool, error: str|None)`. If the
  live process's `created_utc` does NOT equal the argument it returns `(False, "POSIX process
  identity was reused")` and **does NOT signal** — the exact-identity guard. If it matches, it
  `os.kill(pid, 15)` and waits. **This is O9 (POSIX).**
- `_terminate_windows_exact(process_handle, pid)` (:251) terminates by the exact native handle
  (not the PID) → PID alone cannot address it. **This is O9 (Windows).**

## What to build — ONE module `orchestrator_harness/tests/test_compat_operator_launch.py`

1. **O7 / A35** launch a sleep stand-in via `launch_process(...)` into a `TemporaryDirectory` cwd
   with a fresh receipt path → assert `status == "launched"`, `pid` is a positive int,
   `created_utc` is a non-empty ISO string, and the receipt file on disk parses to the same
   `pid`+`created_utc` (exact creation identity recorded). Confirm the PID is actually live via
   `orchestrator_harness.processes.process_snapshot()` / `targeted_process_query`. addCleanup to
   terminate it.
2. **O8** immediately after launch, `detached_owner_snapshot()` contains a row whose
   `pid`+`created_utc` equal the launched identity and `state == "live"`. Then let the child exit
   (poll up to a few seconds) and assert the snapshot drains that row (pruned once the PID is
   gone). Model the drain loop on `test_operator_launch.py`.
3. **O9 exact-identity termination + decoy protection (the key security property):**
   - Launch a sleep stand-in. Call `_cleanup_exact_posix(pid, "1999-01-01T00:00:00+00:00")`
     (a deliberately WRONG creation time = a PID-reuse decoy) → assert it returns
     `(False, <reused/identity message>)` and the child is **STILL LIVE** afterwards (it was NOT
     signaled). This proves a PID-reuse decoy is not touched.
   - **Positive leg:** on POSIX, call `_cleanup_exact_posix(pid, <the real created_utc>)` →
     `(True, None)` and the PID is gone. **On Windows** (`os.name == "nt"`), the exact positive
     kill requires the native process handle held only inside `launch_process`, so
     `self.skipTest("windows exact-handle termination is internal to launch_process")` for the
     positive leg — but STILL run the decoy-protection leg above (it is cross-platform: a wrong
     `created_utc` returns early without signaling). Clean up the real child in `addCleanup`.

Never edit source. If the decoy IS signaled, if a snapshot reports a dead PID as live, or if a
wrong `created_utc` leads to a kill — that is a FAIL-OPEN, HIGHER severity: flag it loudly.
If `launch_process` cannot spawn in this environment at all, `self.skipTest` with the reason
(do not fail) and report BLOCKED.

## Pass criterion

- New module green (or clear FINDING/SKIPPED rows) under the run command above.
- Regression: `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_operator_launch -v`

## Evidence into `.../evidence/2.D/`

- `test-run.log` — `-v` of your new module.
- `operator-launch-regression.log` — `-v` of `test_operator_launch`.

## Final report

Markdown table, one row per item (O7/A35, O8, O9), each PASS / FINDING / SKIPPED (why). Then exact
commands, test count, pass/fail tally. Do not modify any file outside your new test module and the
evidence dir.
