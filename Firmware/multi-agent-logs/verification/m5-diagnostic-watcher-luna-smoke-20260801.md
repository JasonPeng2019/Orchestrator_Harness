# M5 diagnostic-only watcher smoke — GPT-5.6-luna advisory

Date: 2026-08-01 local run (UTC records are 2026-08-02).

Verdict: PASS for the requested host-only diagnostic-only prerequisite, advisory to root.

Scope was limited to the local watcher and host process lifecycle. No firmware, hardware,
provider, MCP, deployment, commit, push, or flash action was performed. No production code,
test, spec, PLAN, or HANDOFF file was edited.

## Canonical practical smoke

The canonical clean epoch was:

- Config: `multi-agent-logs/verification/m5-diagnostic-watcher-luna-smoke-20260801/watcher-config-clean.json`
- Runtime: `harness_watcher/m5-diagnostic-luna-clean-20260801/`
- Changed source: `changed-source-clean.jsonl`; baseline existed before start and the
  `changed-after-start` record was appended after READY.
- Evaluator command: `python -c ... evaluator-sentinel ...`; if invoked, it would create
  `multi-agent-logs/verification/m5-diagnostic-watcher-luna-smoke-20260801/evaluator-sentinel`.

Exact watcher commands issued by the lifecycle driver:

```powershell
python -m harness_watcher_implementation --config multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\watcher-config-clean.json start --owner-pid 177392
python -m harness_watcher_implementation --config multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\watcher-config-clean.json record-attention --role subagent --source-id luna-smoke --epoch-id m5-luna-diagnostic-clean-20260801 --event-id diagnostic-attention-clean-1 --kind AGENT_SIGNAL_CREATED --metadata-file multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\attention-metadata.json
python -m harness_watcher_implementation --config multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\watcher-config-clean.json status
python -m harness_watcher_implementation --config multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\watcher-config-clean.json stop
python -m harness_watcher_implementation --config multi-agent-logs\verification\m5-diagnostic-watcher-luna-smoke-20260801\watcher-config-clean.json status
```

Results:

- `start`: exit 0; published `READY`, watcher PID `190352`, owner PID `177392`, and
  `evaluator_enabled:false`.
- Running `status`: exit 0, `running:true`, `startup_status:"READY"`,
  `evaluator_enabled:false`.
- Runtime watcher events durably contain `SERVICE_STARTED`, `POLL`,
  `EVALUATOR_SKIPPED`, `STOP_REQUESTED`, and `SERVICE_STOPPED`. Every observed `POLL`
  has `evaluator_enabled:false`; skip records have `mode:"diagnostic-only"`.
- The normal source cursor points at the changed record with offset `78` (the source EOF);
  its context contains `phase:"changed-after-start"`.
- Attention was recorded successfully (exit 0). `attention-cursor.json` has one source at
  offset `361`, `partial_bytes:0`, and one deduplication entry.
- `attention-report.json` has `cursor_drained:true`, no observation errors, one event for
  `diagnostic-attention-clean-1`, and classification `NO_BLOCKING_IMPACT`.
- `stop`: exit 0 with `{"stop_requested":true}`. Terminal service state is
  `exit_reason:"stop-requested"`, `startup_status:"READY"`, and
  `evaluator_enabled:false`; final `status` reports `running:false`.
- The sentinel does not exist; `watcher/alerts.json` does not exist; no runtime file name
  contains `notification` or `pending`.
- A live WMI process query whose sentinel needle was assembled dynamically returned an empty
  list while the watcher was running. A delayed post-stop exact identity check returned
  `null` for watcher PID `190352` and owner PID `177392`, and both targeted process lookups
  were absent.

The retained evidence is under
`harness_watcher/m5-diagnostic-luna-clean-20260801/`.

## Focused tests

Commands and results:

```powershell
python -m unittest -v harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_diagnostic_only_poll_reads_and_never_invokes_evaluator harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_diagnostic_only_start_serve_never_runs_evaluator
```

Result: 2 tests, 2 passed.

```powershell
python -m unittest -v harness_watcher_implementation.tests.test_attention_ingestion harness_watcher_implementation.tests.test_attention_practical_retention
```

Result: 12 tests, 12 passed.

```powershell
python -m unittest -v harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_harness_attention_append_is_ingested_without_evaluator_work harness_watcher_implementation.tests.test_watcher_smoke.HarnessWatcherSmokeTests.test_primary_identity_terminal_is_logged_once_without_evaluator_work
```

Result: 2 tests, 2 passed.

Coverage inspection: the two diagnostic tests cover one-shot false-mode evaluator suppression
and the real `start`/`serve`/`stop` path with a sentinel command, cursor creation, skip logging,
and watcher PID cleanup. Attention-ingestion tests cover durable timeline/report generation,
cursor drain, malformed/partial input, restart/dedup, rotation, and fail-closed reports. The
practical smoke additionally covers the combined false-mode lifecycle with changed source,
attention report, service mode fields, alert/notification absence, live evaluator-process
absence, and exact owner/watcher identities.

## Gaps and harnessing notes

- The focused diagnostic test does not itself assert every service event payload, attention
  report field, or absence of manager notification; those are covered by the practical smoke.
- An exploratory first collection attempt had an inline JSON quoting error and a malformed
  temporary owner loop. It was not used for the verdict. A second exploratory epoch was also
  retained, but the clean epoch above is the canonical evidence.
- The first immediate owner identity read in the clean run raced the owner’s cooperative
  self-exit. The delayed exact-identity recheck was `null` for both processes. This is a
  collection timing nuance, not a watcher stop failure.
- No full watcher/harness suite, compile check, or M4 rerun was requested or performed in this
  smoke turn; root should use the prerequisite sequence if those gates are still outstanding.

No failure was fixed. This report is advisory and should be returned to root for acceptance.
