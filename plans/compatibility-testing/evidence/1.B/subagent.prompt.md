# Task: Phase 1, Area 1.B — CLI subcommands (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests** that drive the CLI **in-process**
(call the handler functions / `cli.main(argv)` directly against a fabricated suite dir). You do
NOT launch any `claude`/provider subprocess, you do NOT modify any harness source module, and
you do NOT "fix to green" — a test that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_cli_subcommands -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_events_cli.py` — drives `scan_command` / `watch_once` /
    `watch_until_event` **directly** with `stream=io.StringIO()` and a `SuiteFixture`. Copy this.
  - `orchestrator_harness/tests/test_handoff_preflight.py` — for B8.
  - `orchestrator_harness/tests/test_s4_contract.py` / `test_workspace_overlay.py` — exercise
    `allocate_immutable_source_view` / `retire_terminal_lane` (B15/B16).
  - `orchestrator_harness/tests/support.py` (`SuiteFixture`, `NOW`).
- Code under test: `orchestrator_harness/cli.py`. **Confirmed real symbols (grep bodies before
  asserting — do NOT guess args):**
  - `scan_command(config, *, process_provider=, clock=, stream=sys.stdout)` → prints snapshot,
    returns `EXIT_OK`. **NOTE:** `scan_command` has **no** `no_write` parameter — the `scan
    --no-write` flag is parsed but the handler never persists anything regardless. Verify what
    `scan` actually writes (it calls `observe(...)`, no store); if `--no-write` is a pure no-op,
    that is a legitimate **FINDING** for B2 — document actual behavior.
  - `watch_once(config, *, no_write, process_provider=, clock=, stream=, store_factory=)` →
    `(exit, ...)`; `no_write=True` passes `store=None` so nothing persists.
  - `watch_until_event(config, *, no_write, timeout_seconds, ...)`; `EXIT_TIMEOUT` constant exists.
  - `main(argv)` (cli.py:349) → `build_parser().parse_args(argv)` then dispatch. Use for
    subcommand-dispatch coverage (`view`/`source`/`lane`/`handoff-preflight`).
  - B8: `preflight_handoff(task_card_path=, invocation_path=, result_path=, dependency_map_path=,
    worktree=, evidence_root=, required_evidence=)` + `handoff_preflight_exit_code(result)`
    (imported in cli.py from `.handoff_preflight`).
  - B15: `allocate_immutable_source_view(source_root, revision=, retained_ref=, view_root=,
    result_root=, cache_root=, view_id=)` → `.as_record()` (from `.lane_lifecycle`).
  - B16: `retire_terminal_lane(lane_root, archive_root, lane_id=, task_ref=, result_ref=,
    findings_ref=, acceptance_ref=, transcript_ref=, dependency_ref=, overlay_receipt=)` →
    `.outcome` (success starts with `"CLOSED"`) (from `.lane_lifecycle`).

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_cli_subcommands.py`

Drive the CLI in-process against a fabricated suite dir (`SuiteFixture`). One test per item:

1. **B1** `scan` one-shot: run `scan_command` against a fixture run-root → snapshot printed to
   the stream (parse the JSON). Assert what it writes/does not write (record the actual behavior).
2. **B2** `scan --no-write` diagnostic-only: snapshot the run-root dir tree before/after → assert
   **no** mutation. If `scan_command` never persists anyway (no `no_write` param), document that
   as the actual behavior (and flag the parsed-but-ignored flag as a FINDING).
3. **B3** `watch --once` single pass: `watch_once(config, no_write=False, stream=...)` → exactly
   one reconcile pass then returns; assert exit and a single snapshot printed.
4. **B4** `watch --until-event` returns on a new event: start from a baseline, fabricate an event
   (touch/write a record), call `watch_until_event` with a short timeout → returns promptly with
   that event (not `EXIT_TIMEOUT`). Use a deterministic clock/short timeout — do NOT block long.
5. **B7** `watch --no-write`: `watch_once(config, no_write=True, ...)` → reconcile runs but the
   dir tree is unchanged (diff before/after; `store=None`).
6. **B8** `handoff-preflight`: valid bundle → OK exit (`handoff_preflight_exit_code`==0);
   missing evidence → non-zero + a reason in the record. (Model on `test_handoff_preflight.py`.)
7. **B15** `view` / `source allocate`: allocate an immutable view of a fixture repo at a revision
   → the view exists and is read-only (assert the record fields + that the view path is
   read-only, the way `test_s4_contract`/`test_workspace_overlay` assert it). Function-level is fine.
8. **B16** `lane retire` archive-first: retire a fabricated terminal lane → assert the **archive
   is written before the worktree is closed** (outcome starts `CLOSED`; the archive artifact
   exists). If ordering is not observable at this layer, assert the record and note it BLOCKED.

If a subcommand behaves differently than B1–B16 describe (a flag ignored, no persistence where
expected, ordering not enforced), **do not invent behavior** — write the test to document ACTUAL
behavior and record a FINDING (feature ID, input, expected vs. observed, `cli.py:<line>` or the
handler module:line). Never edit any source module.

## Pass criterion

- New module green under the run command above.
- Re-run the model suite to confirm shared fixtures undisturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_events_cli -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.B/`:
- `test-run.log` — full `-v` output of your new module.
- `cli-regression.log` — `-v` output of re-running `test_events_cli`.

## Final report (return as your last message)

A markdown table: one row per feature ID (B1,B2,B3,B4,B7,B8,B15,B16), each `PASS` / `FINDING`
(one-line what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and the
pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
