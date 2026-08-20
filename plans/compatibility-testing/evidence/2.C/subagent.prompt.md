# Task: Phase 2, Area 2.C — Lane lifecycle: immutable views & archive-first retirement (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** that drive the real
`orchestrator_harness.lane_lifecycle` seams over a fabricated disposable git repo + linked
worktree. You do NOT launch any `claude`/provider subprocess (a tiny synthetic fake-provider .py
stub written to a temp dir is fine — that is not a lane), you do NOT modify any harness source
module, and you do NOT "fix to green" — a test that reveals a real gap is a valid, recorded
outcome. Pin ACTUAL behavior; if the real code does something other than the item description,
pin what it ACTUALLY does and flag the divergence — never invent behavior.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run your new tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_lane_lifecycle -v
  ```
- **Idiom model — READ FIRST and copy verbatim:** `orchestrator_harness/tests/test_s4_contract.py`
  - lines **391-470** = the `_publish_lifecycle_record(root, lane, *, lane_id, revision, ...)`
    staticmethod that admits a real lifecycle registry record (P3/P4) — **copy it wholesale**;
    a retirable lane needs it.
  - lines **687-722** = `test_S4_IMMUTABLE_VIEW_001` — exact `allocate_immutable_source_view(...)`
    call shape + `view.assert_read_only()` + `view.write_source(...) -> ImmutableViewError` (P1/P2).
  - lines **724-807** = `test_S4_LANE_RETIREMENT_001` — building main repo + linked worktree,
    the six evidence refs, `_publish_lifecycle_record`, then `retire_terminal_lane(...)` under
    `patch("orchestrator_harness.lane_lifecycle.process_snapshot",
    return_value=ProcessSnapshot(True, (), (), "synthetic-test"))` (P6/P11), `result.outcome`,
    `validate_lane_archive(result.archive_path)["schema"] == "orchestrator-lane-archive/v1"` (P9),
    and the VISIBLE/dirty-worktree blocked path.
  - Import `ProcessSnapshot` the same way that file does.

## Code under test — `orchestrator_harness/lane_lifecycle.py` (grep bodies before asserting)

Errors: `LaneLifecycleError(ValueError)`, `ImmutableViewError`, `RetirementBlocked`, `ArchiveFailed`.
Public seams: `allocate_immutable_source_view` (:942), `retire_terminal_lane` (:1768),
`validate_lane_archive` (:2173). Internal seams to target directly where noted:
`_separate_root` (:180), `_retained_commit` (:214), `_assert_retained` (:222), `_safe_member`
(:243), `_set_read_only` (:252), `_canonical_registry_identity` (:305), `_admit_lifecycle_registry`
(:648), `_update_lifecycle_registry` (:790), `_process_proof` (:1418), `_validate_lane_binding`
(:1623), `_archive_digest` (:1733), `_copy_member` (:1743).

## What to build — ONE module `orchestrator_harness/tests/test_compat_lane_lifecycle.py`

One test per item (use `tempfile.TemporaryDirectory()`; real `git` via subprocess like the model):

1. **P1** allocate a read-only immutable source view at a committed revision → the view exists and
   `view.retained_commit == revision`, `VIEW_READY.json` present.
2. **P2** read-only enforcement: `view.assert_read_only()` is True and `view.write_source(rel, b"x")`
   raises `ImmutableViewError` (validates B15).
3. **P3** `_admit_lifecycle_registry`: via `_publish_lifecycle_record`, assert a registry row with a
   process-boundary record is created (inspect the registry file/dir it writes; grep the seam to
   learn the path + shape). If admission is only reachable through the controller path, drive it
   through `_publish_lifecycle_record` and assert the resulting on-disk record.
4. **P4** `_update_lifecycle_registry` on transition: cause a state transition and assert the
   registry row updates atomically (row reflects the new state; grep for how state is stored).
5. **P5** retained/separate-root safety: allocate against a commit NOT reachable by the retained ref
   (e.g. `retained_ref` pointing to a branch that does not contain the revision) → rejected
   (`ImmutableViewError`); and a same-root view/result/cache collision → `_separate_root` rejects.
6. **P6** `retire_terminal_lane` archive-first (B16): retire a clean admitted lane (patch
   `process_snapshot` as the model does) → `result.outcome == "CLOSED"`, the archive file exists and
   its digest is bound **before** the worktree is removed. Assert ordering: the archive path is a
   real file AND `lane.exists()` is False afterwards. If you can observe ordering only indirectly,
   assert the archive is complete/valid (validate_lane_archive OK) and the lane is gone.
7. **P7** `_validate_lane_binding`: retire with a mismatched lane binding (wrong `lane_id` vs the
   admitted record) → rejected (`RetirementBlocked` or a blocked outcome — pin which).
8. **P8** `_archive_digest` / `_copy_member` integrity: after a good retirement, recompute the
   archive digest over its members and assert it matches what the archive records.
9. **P9** `validate_lane_archive`: a good archive → returns schema `orchestrator-lane-archive/v1`;
   corrupt one member's bytes inside the archive on disk → `validate_lane_archive` raises/fails.
10. **P10** `_canonical_registry_identity`: two different path spellings of one lane root (e.g. with
    `.`/redundant separators, or `os.path.normpath`-differing) collapse to ONE canonical identity
    dict (equal output).
11. **P11** `_process_proof`: retire WITHOUT valid process proof (do NOT patch `process_snapshot`,
    or patch it to `ProcessSnapshot(False, ...)`) → retirement is rejected/blocked (pin the outcome).
12. **P12** `_safe_member`: assert `_safe_member("../evil")` is False (and other traversal/absolute
    names), `_safe_member("ok/rel.txt")` is True; then confirm the retirement/extraction path refuses
    a crafted `../` member (either `_safe_member` returns False or `validate_lane_archive` rejects an
    archive containing such a member). Path-traversal guard must hold.

Never edit source. If any behavior FAILS CLOSED differently than described, pin the actual outcome.
If any behavior FAILS OPEN (a non-retained commit accepted, a corrupted archive validated, a `../`
member extracted, retirement without process proof succeeding, an immutable view writable), that is
HIGHER severity — flag it loudly in your report.

## Pass criterion

- New module green (or with clearly-reported FINDING/divergence rows) under the run command above.
- Regression: `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s4_contract -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/2.C/`:
- `test-run.log` — full `-v` output of your new module.
- `s4-regression.log` — `-v` output of `test_s4_contract`.

## Final report (return as your last message)

A markdown table: one row per item (P1…P12), each `PASS` / `FINDING` (one-line what-differed) /
`BLOCKED`/`SKIPPED` (why). Then the exact commands run, the test count, and pass/fail tally. Do not
modify any file outside your new test module and the evidence dir.
