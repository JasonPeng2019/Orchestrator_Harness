# Task: Phase 2, Area 2.A — Workspace overlay edge cases (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests** that drive the real
`orchestrator_harness.workspace_overlay` seams over fabricated on-disk cache/worktree fixtures.
You do NOT launch any `claude`/provider subprocess, you do NOT modify any harness source module,
and you do NOT "fix to green" — a test that reveals a real gap is a valid, recorded outcome.
One item (I4) has a KNOWN plan-vs-reality divergence (below): pin ACTUAL behavior in a green test
and record the FINDING.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_workspace_overlay -v
  ```
- Model fixture — read FIRST to copy idioms exactly:
  `orchestrator_harness/tests/test_workspace_overlay.py` (how a super-cache dir + a target
  worktree + a receipt path are built and how `prepare_worktree`/`restore_worktree` are called).
  Also `orchestrator_harness/tests/support.py`.

## Code under test — `orchestrator_harness/workspace_overlay.py` (grep bodies before asserting)

Constants: `DECLARATION_NAME == ".super-cache.json"`,
`SUPER_CACHE_CONTROL_SCHEMA == "orchestrator-super-cache-control/v1"`,
`OVERLAY_RECEIPT_SCHEMA == "orchestrator-workspace-overlay-receipt/v1"`,
`SUPPORTED_ROLES == {"subagent","orchestrator"}`. Errors: `WorkspaceOverlayError`,
`OverlayCollisionError(WorkspaceOverlayError)`.

- `prepare_worktree(*, super_cache, target_worktree, role, receipt_path)` (:459): full collision
  PREFLIGHT before any mutation; creates missing files/dirs, merges dirs without overwrite, and an
  existing-file collision is rejected via `OverlayCollisionError` UNLESS the relative path is
  declared in the cache-root `.super-cache.json` `append_text` list. Writes a receipt (schema, the
  target ID, role, `completed:true`, `affected_paths`, `operations`, `created_paths`,
  `pre_overlay_bytes`, `post_prepare_bytes` — the last two base64). On a mid-apply failure it calls
  `_rollback_applied` and raises `WorkspaceOverlayError("...rolled back...")`.
- `restore_worktree(*, receipt_path)` (:717): re-reads + `_validate_receipt`, then for each
  affected file compares CURRENT bytes with the receipt's exact `post_prepare_bytes`
  (`:789-795`); a mismatch → the file is preserved and the outcome is `BLOCKED` with reason
  "later edit detected". Unchanged appends get pre-overlay bytes back; unchanged created files are
  removed; empty created dirs removed. **This is where byte-level corruption is detected.**
- `verify_overlay_receipt(*, receipt_path, expected_target_worktree_id, role="subagent")` (:854):
  a PRELAUNCH check (REQ-O41). `receipt_path is None` → `{present:False, verified:True}`. A present
  receipt must pass `_validate_receipt` (closed shape, `completed:true`, valid role, target ID),
  match the expected role, and match the expected target worktree ID → `verified:True`, else
  `verified:False` with a reason. **It NEVER reads the materialized worktree bytes** ("never
  compared with the current cache … no cache work is performed here").
- `_build_plan` (:349) / `_validate_append_targets` (:391): collision classification + the
  declared-append UTF-8-text requirement.
- `_is_reparse` (:64) / `_regular_directory` (:75): reject reparse points (symlinks/junctions)
  and non-directories before any copy.
- `_read_declaration` (:304): missing → `None`; present must be a regular file, UTF-8 JSON, closed
  `{schema, append_text}` shape, correct schema, `append_text` a list of unique safe relative
  paths — else `WorkspaceOverlayError`.
- `_encode_bytes` (:405) / `_decode_bytes` (:409): base64 (`validate=True`) round trip.
- `_rollback_applied` (:418): reverses recorded mutations (delete created files, replace appended
  files with pre-bytes) then removes empty created dirs.

## What to build

Create ONE new test module: `orchestrator_harness/tests/test_compat_workspace_overlay.py`.
One test per item (build cache/target/receipt under `tempfile.TemporaryDirectory()`):

1. **I4 / A9** independent receipt verification. After a real `prepare_worktree`, call
   `verify_overlay_receipt(receipt_path=…, expected_target_worktree_id=<target>, role=…)` →
   `verified:True` (WITHOUT calling restore). Then assert what verify ACTUALLY catches:
   structural/identity corruption of the *receipt* — flip `completed` to false, or use a wrong
   `expected_target_worktree_id`, or a wrong `role`, or corrupt the receipt JSON/schema → each
   returns `verified:False` with a reason. **Separately** assert that corrupting one *materialized
   worktree byte* is detected by `restore_worktree` (outcome `BLOCKED`, reason "later edit
   detected"), NOT by `verify_overlay_receipt` (which still returns `verified:True` because it
   never reads worktree bytes).
   > **PLAN-VS-REALITY DIVERGENCE — record as a FINDING (F2A-I4-1, note).** The plan's I4 says
   > "corrupt one materialized byte and re-verify [via verify_overlay_receipt] → verification
   > fails." Reality: `verify_overlay_receipt` is a structural/identity prelaunch check (REQ-O41)
   > that never reads materialized bytes; byte-integrity is enforced at `restore_worktree`
   > (`:789-795`). Pin both actual behaviors; do not force verify to read bytes.
2. **I5** append-only plan + collision detection. Materialize a cache whose file lands on a path
   that already exists in the target and is NOT declared for append → `OverlayCollisionError`;
   assert no partial write is left behind (target byte-identical to before, no receipt-created
   files). Then show the declared-append path succeeds (a `.super-cache.json` naming that relative
   path as `append_text` → the file is appended, not rejected).
3. **I7** reparse/regular-directory enforcement. Point the cache or target through a
   symlink/junction (or make a component a symlink) → rejected (`_regular_directory` /
   `_is_reparse` raise) before any copy. **If the OS/user cannot create a symlink/junction,
   `self.skipTest(...)`** — do NOT fail.
4. **I8** rollback on partial-apply failure. Build a multi-file cache so the apply loop performs
   ≥2 mutations, then inject a mid-apply failure by monkeypatching a mutation helper on the module
   to raise on the 2nd call (e.g. wrap `orchestrator_harness.workspace_overlay.mutation_replace`
   or `mutation_append_bytes` with a counter that raises `MutationError` on call N≥2; restore it in
   a `finally` / `addCleanup`). Assert `prepare_worktree` raises `WorkspaceOverlayError` mentioning
   "rolled back", the already-applied file(s) were reversed, and the **target is byte-identical to
   its pre-apply state** (no receipt published). (Patching an imported seam to inject a fault is a
   standard test technique — it is NOT a source edit.)
5. **I9** declaration read/validate. `_read_declaration` on: (a) no file → `None`; (b) malformed
   JSON / non-UTF-8 → error; (c) wrong closed shape / wrong schema / non-list or blank
   `append_text` / duplicate paths → error; (d) a valid declaration → normalized dict. 
6. **I10** byte encode/decode round trip. `_decode_bytes(_encode_bytes(b))` returns identical `b`
   for arbitrary bytes incl. non-UTF-8 (`b"\xff\xfe\x00"`), embedded NULs, and empty. Assert
   `_decode_bytes` rejects a non-str and an invalid-base64 str with `WorkspaceOverlayError`.

Never edit source. If any OTHER behavior differs (a collision NOT rejected, a reparse point NOT
rejected, rollback leaving the target changed, restore accepting corrupted bytes — any fail-open),
that is HIGHER severity — flag it clearly.

## Pass criterion

- New module green under the run command above.
- Re-run the model suite: `PYTHONPATH="$PWD:$PWD/.." python -m unittest
  orchestrator_harness.tests.test_workspace_overlay -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/2.A/`:
- `test-run.log` — full `-v` output of your new module.
- `overlay-regression.log` — `-v` output of `test_workspace_overlay`.

## Final report (return as your last message)

A markdown table: one row per feature ID (I4, I5, I7, I8, I9, I10), each `PASS` / `FINDING`
(one-line what-differed) / `BLOCKED`/`SKIPPED` (why) — I4 is EXPECTED to be a `FINDING` row; I7 may
be `SKIPPED` if symlinks are unavailable. Then the exact commands run, the test count, and the
pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
