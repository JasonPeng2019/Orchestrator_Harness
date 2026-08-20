# M5 Q8 publication/logging repair - Luna smoke report

## Verdict

**PASS** - host-only validation completed on 2026-08-02. No hardware, providers, MCP,
wrappers, relays, runners, subagents, commits, or pushes were used. No production code or
requirements were edited.

## Reviewed surface

- `multi-agent-logs/attention-validation/runs/20260802-m5-q8-152800Z/REPAIR_PLAN.md`
- `REPOSITORY_LAYOUT.md` and `AGENTS.md`
- `harness_watcher_implementation/attention.py` (timeline schema, validation, analyzer)
- `harness_watcher_implementation/__main__.py` (CLI)
- `harness_watcher_implementation/verdict.schema.json`
- Attention, ingestion, recorder-CLI, retention, watcher-smoke, signal-correlation, and
  manager-notification tests.

Observed implementation facts: `AGENT_SIGNAL_PUBLISHED` is in the allowed vocabulary;
`record-attention --source-timestamp-utc` passes the supplied timestamp into the source record;
publication evidence requires exactly one correlated record ordered after creation and no later
than observation or delivery deadline; invalid publication evidence is converted to
`INSUFFICIENT_EVIDENCE`; native wake fields and manager wait flow remain unchanged.

## Commands and results

| Exact command | Result |
|---|---|
| `python -m unittest harness_watcher_implementation.tests.test_attention harness_watcher_implementation.tests.test_attention_recorder_cli orchestrator_harness.tests.test_attention_signal_correlation orchestrator_harness.tests.test_manager_notifications -v` | **PASS**, exit 0; 73 tests passed. Includes `test_publication_cli_preserves_captured_source_timestamp`, publication timing/fail-closed tests, signal correlation, and native wake/manager tests. |
| `$env:PYTHONUTF8='1'; python -m unittest discover -s harness_watcher_implementation/tests -t . -v` | **PASS**, exit 0; 98 tests passed. |
| `$env:PYTHONUTF8='1'; python -m unittest discover -s orchestrator_harness/tests -t . -q` | **PASS**, exit 0; 209 tests passed, 1 skipped. Native wake/manager regression surface remained green. |
| `$env:PYTHONUTF8='1'; python -m harness_watcher_implementation.tests.run_attention_practical` | **PASS**, exit 0; `attention practical host-only check: PASS (R10 deadline-origin + healthy blocking path, R9 continuity precedence, CLI disabled gate)`. |
| `$env:PYTHONUTF8='1'; python -m compileall -q harness_watcher_implementation orchestrator_harness` | **PASS**, exit 0. |
| `python -m compileall -q harness_common` | **PASS**, exit 0. |

Additional direct host-only analyzer matrix (stdin Python script; no file or support component
created):

```text
timely_unique HARNESS_DELIVERY_DELAY 6.0 [] []
missing INSUFFICIENT_EVIDENCE None ['unique AGENT_SIGNAL_PUBLISHED record'] []
duplicate INSUFFICIENT_EVIDENCE None ['unique AGENT_SIGNAL_PUBLISHED record'] []
mismatched INSUFFICIENT_EVIDENCE None [] ['publication contradicts signal lane_id']
post_observation INSUFFICIENT_EVIDENCE None [] ['publication follows harness observation']
post_deadline INSUFFICIENT_EVIDENCE None [] ['publication follows delivery deadline']
publication fail-closed matrix: PASS
```

## Acceptance mapping

1. **PASS** - exact captured UTC persisted by the publication CLI path; the focused test verifies
   the persisted `source_timestamp_utc` is byte-for-byte equal to the supplied timestamp.
2. **PASS** - unique timely publication produced truthful `publication_to_observation_seconds =
   6.0` and `creation_to_publication_seconds = 1.0`.
3. **PASS** - missing, duplicate, mismatched, post-observation, and post-deadline publication
   all failed closed as `INSUFFICIENT_EVIDENCE`; none became harness delay.
4. **PASS** - focused native wake/manager tests and the full watcher suite passed; no harness
   scheduling, transport, manager, or wake path was changed.

## Workspace note

At inspection time the checkout reported 20 pre-existing untracked paths and no tracked diff.
The only intentional file written by this validation is this report.
