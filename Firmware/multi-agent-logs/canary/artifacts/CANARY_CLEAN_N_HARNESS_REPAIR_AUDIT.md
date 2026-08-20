# Clean-N harness repair independent audit

**Verdict: PASS**

No hardware, server, firmware, provider/MCP public action, or external lane was run.

## Prior BLOCK resolution

The mutable-pending admission-time defect is fixed. When a stored deferred handoff is promoted,
`select_actionable_with_deferred()` now copies its original `admitted_utc` onto pending state.
`coalesce_mutable_handoffs()` compares pending with deferred by that admission fact rather than
the later notification `observed_utc`. Legacy pending state without the field ranks before any
explicit admission fact, with event-ID tie-breaking.

I reproduced the retained Clean-N ordering against the current function, read-only:

```text
legacy old pending has admitted_utc: None
winner: 1daf03f… (latest Boreal checkpoint)
superseded: 53c8d761…, a21b667e…
remaining Boreal deferred: []
```

This is the required reversal of the previous erroneous old-pending winner. Supersession metadata
is transitive: coalescing unions prior `superseded_event_ids` with all newly replaced IDs.

## Acceptance review

- The true promotion regression proves an old deferred checkpoint retains its original admission
  timestamp when selected later, then loses to a newer admission despite the later selection
  time.
- `test_managed_checkpoint_promotion_restart_and_exact_ack` uses four distinct bounded
  `watch_managed()` invocations against one durable state: admit behind high pending, promote old
  after exact high ack, replace with newer checkpoint on restart, reject canonical acknowledgement
  of the superseded old ID, accept the current ID, and restart without an obsolete wake.
- Coalescing occurs before the managed pending-event early continue. Its scope remains only
  `CHECKPOINT_UPDATED` and `RESULT_AVAILABLE`; immutable manager signals remain separate.
- Observation sampling remains discovery → process inventory → post-sample clock in both ordinary
  observation and managed watch. Focused live-identity coverage proves no false startup stale
  classification, while affected suites retain genuine stale/absent controls.

## Independent command result

```powershell
python -m unittest orchestrator_harness.tests.test_clean_n orchestrator_harness.tests.test_clean_m_handoffs orchestrator_harness.tests.test_manager_notifications orchestrator_harness.tests.test_active_manager_watch_smoke orchestrator_harness.tests.test_events_cli -v
```

Result: **71 passed** in 4.511 seconds.

The verification records the final full local suite as **173 passed, 1 skipped**. No process-
producing practical test was run by this audit; the managed lifecycle tests use fixture state only
and leave no process residue.
