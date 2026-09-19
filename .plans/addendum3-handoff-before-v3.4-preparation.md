# Harness v2 Addendum 3 execution handoff

## Objective

Complete `goal.md` through EDGE-007 under Addendum 3 version 3.4 (remaining-work scope amendment). Execution is
**PAUSED AT THE MI-FL2-S2-LIVE-VERDICT ROOT DECISION BOUNDARY**. The latest human-intervention
checkpoint remains 18h13m38s of project runtime.

## Status

Decision 324 accepted affected readiness. M09 Series 4 attempt
`ATTEMPT-FL2-S2-LIVE-WINDOWS-014` completed for the exact 40 decision-320
affected Windows cells. Sequence 347 joins a complete 96-cell pool with 56 PASS
and 40 FAIL: one fresh PASS, 39 fresh FAIL, 55 preserved PASS, and the single
preserved nonblocking Qwen-managed CHECK-LIVE-2 deviation.

The corrected independent observer preceded target behavior and stopped
cooperatively after 5,010 snapshots. All six executor profiles are terminal. A
host interruption and a later native-result serialization fault were recovered
without replaying any terminal profile. Correction 3 published a valid outer
FAIL result, and sequence 346 proves the observer, executor, nine retained target
monitors, target processes, and resource claims absent.

The independent Series 4 CHECKER then completed normally at 2026-09-17
00:19:10Z. Its frozen result is valid and PASS, its worktree is clean, and its
decision-ready packet mechanically accounts for all 96 coordinates and all 40
FAIL rows in 15 groups without semantic classification. ROOT inspected the
packet but paused before publishing the semantic M05 verdict or authorizing any
repair. No Addendum 3 controller, provider, observer, target process, or resource
claim remains active.

## Planning amendment after the pause

Version 3.4 changes only remaining STEP-006 work: consume the completed checker
packet for ROOT adjudication, prove admitted control repairs locally, and execute
only required unresolved or invalidated live evidence. Completed STEP-001 through
STEP-005 and raw Series 4 evidence stay intact. Independent planning audit and
structural validation are recorded in the addendum's validation.md. This planning
task does not resume execution or publish the pending M05 semantic verdict.
Version 3.4 strengthens the remaining coverage floor: concrete positive/adverse
and recovery assertions, realistic caller/OS boundaries, and candidate retry-limit
proof where existing evidence is insufficient. No accepted suite or cell is reset
merely by this audit; required unproved subcases remain open.

## Completed since decision 324

- Created isolated Series 4 executor and observer worktrees at candidate
  `cb01e41533b337d3dd344b89313f1c9062ee69f8`.
- Installed and hash-verified the accepted 18-asset control bundle
  `49978bbb730d836fb5d39ee575697a6841ddb9a5c6baa0df5d02ea2791c2e448`.
- Built and side-effect-free validated six affected manifests/checkpoints:
  40 selected cells, 56 preserved classifications, 40 unique fresh target roots.
- Reverified provider versions and executable hashes, Qwen configuration, prior
  exact PID absence, zero target-root processes, and zero resource claims.
- Narrowed observation to roots created by this attempt while retaining exact
  process observation across the target namespace; six observer support tests
  pass. This avoids rehashing all retained historical evidence every second.
- The first observer startup reached READY but native publication failed because
  ROOT omitted its handoff parent directory. No target behavior ran. Sequence 326
  retains the terminal failure. ROOT created only the missing prerequisite and
  resumed the same Claude session `5604f4e8-1303-4a42-9968-935f1c7af79b`.
- Same-thread correction 1 published a valid PASS result and left the corrected
  observer running. Sequence 327 records exact readiness; sequence 328 admits M09.
- The initial executor start consumed the obsolete observer READY record and
  stopped before target behavior. Sequence 330 retains the failure; sequence 331
  corrected admission, and the same executor thread resumed under sequence 332.
- CHECK-LIVE-8 repeated the known Codex provider nonprogress pattern. ROOT used
  exact public containment and sequence 333 retains that support-failure proof.
- The Codex-managed profile is terminal: 8 fresh affected cells produced one
  PASS (CHECK-LIVE-12) and seven truthful FAIL rows. CHECK-LIVE-10/11 expose a
  fixture helper resolving the candidate junction before checking its lexical
  disposable-package destination; CHECK-LIVE-13/14 expose remaining monitor and
  Windows sharing-error control faults; CHECK-LIVE-15/16 are dependent failures.
- The Codex-plain profile is terminal with six truthful affected FAIL rows. The
  same fixture/monitor/Windows-reader faults recur and CHECK-LIVE-15/16 remain
  dependent failures.
- The host interruption left no native executor result and no live former
  executor or target process. ROOT retained both complete profile results, the
  Claude-managed CHECK-LIVE-8 checkpoint, and the stale claim bytes, then removed
  only the proven-dead controller claim. Two focused tests pass for validating and
  reusing complete profile results without touching their logs or accepting an
  incomplete result.
- Correction 2 resumed the same PRACTICAL_EXECUTOR thread under invocation 336.
  It reused both Codex terminal results without replay and continued
  Claude-managed at CHECK-LIVE-10.
- Both Claude profiles are terminal. Their fresh rows reproduce the deterministic
  fixture-path, monitor-order, and Windows-reader control faults plus provider
  support and dependent failures; neither profile produced a fresh PASS.
- Sequences 337 through 342 retain six exact Claude terminal-mismatch
  containments. For each one ROOT first proved the relevant controller and
  provider identities absent, used the public force-stop surface, and stopped
  only the cell runner whose readiness wait had become unreachable.
- Qwen managed and plain completed naturally. Qwen-managed CHECK-LIVE-16 ran the
  full worker/ROOT native-hook flow; the deterministic CHECK-LIVE-10/11/13/14
  control faults remained reproducible.
- Sequence 343 retains the first native publication failure: reused-profile fact
  rows had one unsupported key. Three focused tests passed after the shape and
  outcome correction; sequence 344 admitted same-thread correction 3, which
  reused all six terminal results and published a valid outer FAIL.
- The observer stopped cooperatively after 5,010 snapshots and 22 transient read
  races. Public shutdown closed nine retained target runtimes; sequence 346 proves
  exact cleanup, clean worktrees, and zero claims.
- Sequence 347 joins the complete Series 4 ledger and result pool: 56 PASS / 40
  FAIL, with one fresh PASS and 39 fresh FAIL.
- Invocation 348's CHECKER exited 0 with a frozen-valid result. It verified both
  input digests, six profile results, the 5,010-snapshot observer log, containment
  records, exact cleanup, interruption recovery, 96 unique coordinates, and 15
  mechanical failure groups totaling 40 members. Its handoff explicitly leaves
  semantic classification to ROOT.
- ROOT's pending classification has four deterministic strict-control mechanisms:
  interrupted attempt-root reuse (1 row), lexical fixture-junction validation
  (11 rows), CHECK13 setup ordering (6 rows), and Windows PermissionError retry
  handling (4 rows). Seven CHECK15/16 rows are downstream-dependent, ten rows are
  provider/support-indeterminate, and the preserved Qwen-managed CHECK-LIVE-2
  deviation remains nonblocking. This analysis is not yet a published M05
  decision and must be revalidated on resume.

## Current evidence

- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-NATIVE-BOUNDARY-325-pre.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/OBSERVER-SERIES4-START-FAIL-326.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/OBSERVER-SERIES4-READY-327.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/M09-SERIES4-ADMISSION-328.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/M09-SERIES4-ADMISSION-CORRECTION-331.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CHECK8-NONPROGRESS-CONTAINMENT-333.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/EXECUTOR-SERIES4-INTERRUPTION-334.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/M09-SERIES4-ADMISSION-CORRECTION-335.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-MANAGED-CHECK12-TERMINAL-MISMATCH-337.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-MANAGED-CHECK14-TERMINAL-MISMATCH-338.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-MANAGED-CHECK15-TERMINAL-MISMATCH-339.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-MANAGED-CHECK16-TERMINAL-MISMATCH-340.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-PLAIN-CHECK14-TERMINAL-MISMATCH-341.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-CLAUDE-PLAIN-CHECK15-TERMINAL-MISMATCH-342.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/EXECUTOR-SERIES4-NATIVE-EMISSION-FAILURE-343.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/M09-SERIES4-ADMISSION-CORRECTION-344.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-TERMINAL-CLEANUP-346.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/SERIES4-WINDOWS-CELL-LEDGER-347.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/RESULT-FL2-S2-LIVE-POOL-SERIES4-347.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-verdict-evidence-series4-348.invocation.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/PAUSE-SERIES4-VERDICT-349.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-allocation-014/ADMISSION.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-execution-series4-correction-1-332.invocation.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/live-execution-series4-correction-2-336.invocation.json`
- `w/addendum-3-epoch-001/live-execution-series4/.agent-workspace/live-matrix/selected-commands-series4-014.json`
- `w/addendum-3-epoch-001/live-execution-series4/.agent-workspace/live-matrix/results/result-windows-codex-managed-series4-014.json`
- `w/addendum-3-epoch-001/live-execution-series4/.agent-workspace/live-matrix/results/result-windows-codex-plain-series4-014.json`
- `w/addendum-3-epoch-001/live-execution-series4/.agent-workspace/live-matrix/results/result-windows-claude-code-managed-series4-014.json`
- `w/addendum-3-epoch-001/live-execution-series4/.agent-workspace/live-matrix/results/result-windows-claude-code-plain-series4-014.json`
- `w/addendum-3-epoch-001/live-observation-series4/.agent-workspace/RESULT.json`
- `w/addendum-3-epoch-001/live-verdict-evidence-series4/.agent-workspace/RESULT.json`
- `w/addendum-3-epoch-001/live-verdict-evidence-series4/.agent-workspace/HANDOFF-FL2-S2-LIVE-VERDICT-EVIDENCE-SERIES4.json`
- `w/addendum-3-epoch-001/live-verdict-evidence-series4/.agent-workspace/fail-groups-series4.json`

## Remaining

1. Complete ROOT's MI-FL2-S2-LIVE-VERDICT (M05) semantic classification against
   the accepted invocation-348 packet and publish one verdict. Do not relaunch
   the CHECKER or replay Series 4.
2. If ROOT confirms CONTINUE, dispatch one tightly bounded M03 control correction
   for the four deterministic mechanisms, with executable realistic regressions
   for each changed branch before review/integration/readiness. Preserve the 56
   PASS rows and the exact CHECK-LIVE-2 deviation unless their inputs change.
3. Complete EDGE-007 with the Windows verdict, separate macOS/Linux BOUND-014 gap
   ledgers, exact cleanup disposition, and terminal handoff.

## Next action

Validate pause record 349 and the invocation-348 CHECKER result/handoff, then
publish ROOT's M05 semantic verdict. The expected evidence supports CONTINUE for
four deterministic control repairs, but the verdict remains ROOT-owned and has
not been written. Do not relaunch the CHECKER or replay any Series 4 target set.
