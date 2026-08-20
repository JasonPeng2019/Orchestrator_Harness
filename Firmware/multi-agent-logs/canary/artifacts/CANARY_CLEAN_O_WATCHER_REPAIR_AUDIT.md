# Clean-O optional-watcher repair independent audit

**Verdict: PASS**

## Verified behavior

- `STALE_STATUS` is quarantined by exact identity and is not shown to the evaluator on first
  sighting. Exact same-identity `CONTROLLER_ACTIVE`, `CONTROLLER_EXITED`, or stale-clearing
  `CONDITION_CLEARED` removes an unreleased quarantine entry; unrelated identity or unrelated
  clear does not.
- Quarantine persists additively in the v2 cursor with original source path/SHA-256/offset and
  raw record. A legacy v2 cursor without the new field loads and is rewritten compatibly.
- A stale surviving one complete configured poll interval matures once even with no new bytes:
  its synthetic evaluator observation uses the preserved evidence tuple, sets `changed:true`, and
  marks the entry released to prevent duplicate evaluator work/alerts. Strict packet-evidence
  validation still accepts only tuples present in the packet.
- Recursive watcher-input filtering, source cursor advancement, retained-context/no-progress
  behavior, alert deduplication, and non-stale defect categories remain covered by smoke tests.
  The primary harness is not modified by this repair.
- The evaluator packet and instructions state the bounded quarantine rule; this is not a blanket
  stale-status ignore rule.

## Manager procedure gate

`.agent-workspace/CANARY_MANAGER_FORMAL_REVIEW_GATE.md` adequately resolves the Clean-O lapse as
an operational issue: wall-clock review is independent of notification delivery, must be written
before ordinary draining continues, blocks new authority, and still requires canonical exact-ID
acknowledgement plus baseline proof when pending. It correctly avoids claiming a primary-harness
defect.

## Independent commands

```powershell
python -m unittest harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_same_delta_stale_then_exact_recovery_is_hidden_from_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_stale_in_one_poll_then_exact_exit_in_next_poll_never_calls_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_sustained_stale_reloads_cursor_then_releases_once_with_valid_evidence harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_unrelated_identity_or_clear_does_not_suppress_stale_release harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_legacy_v2_cursor_without_quarantine_state_remains_readable -v
```

Result: **5 passed**.

```powershell
python -m unittest harness_watcher_implementation.tests.test_watcher_smoke -v
```

Result: **31 passed**.

These tests use faked evaluators and fixture state only. No real evaluator, endpoint, hardware,
server action, or watcher/test-process residue was created by this audit.
