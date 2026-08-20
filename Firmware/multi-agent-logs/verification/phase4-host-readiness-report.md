# Phase 4 host-only wake readiness report

Date: 2026-08-02  
Scope: validation-only rerun after the accepted evidence-retention repair. No production code,
tests, specs, or `PLAN.md` were edited.

## Advisory recommendation

**READY.** The exact external request returned through the real blocking harness wait without an
AI relay; the retained raw and machine-readable bundle independently reconstructs all six ordered
stages with one shared wake ID; the quiet control has no wake ID or wake records; focused, full,
static, and cleanup gates passed.

The broader watcher report also contains two `INSUFFICIENT_EVIDENCE` classifications: one unrelated
`HELPER_ACTIVE` event and the synthetic wake event's missing deadline/late endpoint. The
wake-specific `wake_evidence` is `COMPLETE`, the cursor is drained, observation errors are empty,
and the retention test and raw records independently prove the Phase 4 wake chain. These broader
attention classifications do not contradict the wake-readiness result and are reported explicitly
for root audit. This recommendation is advisory; root decides Phase 4 status.

## Preflight

Repository: `C:\Users\Jason\Documents\Jason\FirmCLI_Tester\Firmware-Test-Manual\MCP-Trial-3`

- Python: `C:\Users\Jason\Documents\Jason\FirmCLI_Tester\Firmware-Test-Manual\MCP-Trial-3\BYO-Firmware-MCP\.venv\Scripts\python.exe`
- Version: Python 3.12.13
- No actual Python practical or `orchestrator_harness ... watch` process was running. The initial
  process probe matched its own PowerShell command text; a name-filtered Python probe returned
  `NONE`.
- `orchestrator_harness/.state`: absent.
- Stale `multi-agent-logs/attention-runtime-*`, `practical-wake-*`, and practical quiet runtime
  directories: none.
- The required evidence destination was absent before the run and was therefore fresh/empty.

Implementation SHA-256 hashes, unchanged before and after validation:

| File | SHA-256 |
|---|---|
| `orchestrator_harness/cli.py` | `6E77F42870B7564A8F30BD2AB108112BB2E745882C69E005E899AFFA738D0CEE` |
| `harness_watcher_implementation/attention.py` | `D877ED285A522EA3E8ED7E460EB28C657E2668608C598C65D67FBDC1F38F1BF5` |
| `harness_watcher_implementation/tests/run_attention_practical.py` | `FB2414F89A844B79D5A934CC7E4B91E0A606466439127A2932BC6F3657C4968E` |

## Exact commands and results

### Practical

Command:

    python harness_watcher_implementation/tests/run_attention_practical.py --evidence-dir multi-agent-logs/verification/phase4-wake-evidence

Exit code: `0`. Stdout:

    {"disabled": true}
    attention practical host-only check: PASS (R10 deadline-origin + healthy blocking path, R9 continuity precedence, CLI disabled gate)

Stderr was empty. Retained bundle: `multi-agent-logs/verification/phase4-wake-evidence/` (20
files), including `wake-result.json`, `quiet-result.json`, separate wake/quiet harness trees,
separate wake/quiet watcher trees, producer JSONL, harness JSONL, watcher timeline, cursor, and
reports.

### Focused retention test

    python -m unittest harness_watcher_implementation.tests.test_attention_practical_retention -q

Exit code: `0`; `Ran 1 test in 5.686s`; `OK`.

### Full suites

    python -m unittest discover -s orchestrator_harness/tests -t . -q

Exit code: `0`; `Ran 191 tests in 28.541s`; `OK (skipped=1)`. Expected negative-path
lane-controller diagnostics were printed before the summary.

    python -m unittest discover -s harness_watcher_implementation/tests -t . -q

Exit code: `0`; `Ran 86 tests in 8.664s`; `OK`. Expected negative-path CLI/recorder diagnostics
were printed before the summary.

### Static validation

    python -m pyright orchestrator_harness/cli.py harness_watcher_implementation/attention.py

Exit code: `0`; `0 errors, 0 warnings, 0 informations`.

    python -m compileall -q orchestrator_harness harness_watcher_implementation harness_common scripts/orchestration

Exit code: `0`; stdout and stderr empty.

## Independently reconstructed successful wake

Sources independently read:

- `phase4-wake-evidence/wake-result.json` (machine-readable returned event, wake ID, analyzer,
  and ordered records);
- `wake-watcher/inputs/subagent/lane-d93244e7b08131ef/attention.jsonl`;
- `wake-watcher/inputs/orchestrator/root-4813494d137e1631/attention.jsonl`;
- `wake-watcher/watcher/attention-timeline.jsonl`, `attention-report.json`, and
  `attention-cursor.json`;
- `wake-harness/attention-events.jsonl` and `events.jsonl`.

The producer and watcher views were deduplicated by `record_id`; exactly six unique canonical
records remained. Exact identities:

- `epoch_id`: `A00_test`
- canonical `event_id`: `wake`
- returned harness event ID: `1be6120582cc50f3feaca34b15675723e81694802d1c8097dd24a73453cf9ddd`
- returned signal ID: `wake`
- shared `wake_id`: `a2aa1b8e-b125-40ae-908f-31af93b0af2a`
- lane: `A00_test:Atlas:A00`
- manager session/invocation: `practical-session` / `practical-invocation`
- component: `orchestrator_harness.watch_until_actionable`
- transport: `blocking_harness_wait_stdout`

| Stage | Canonical kind | Exact `source_timestamp_utc` |
|---:|---|---|
| 1 | `AGENT_SIGNAL_CREATED` | `2026-08-02T01:02:11.177835+00:00` |
| 2 | `HARNESS_SIGNAL_OBSERVED` | `2026-08-02T01:02:12.632541Z` |
| 3 | `MANAGER_WAKE_ATTEMPTED` | `2026-08-02T01:02:12.632541Z` |
| 4 | `MANAGER_WAKE_DELIVERED` | `2026-08-02T01:02:12.632541Z` |
| 5 | `MANAGER_WAKE_RECEIVED` | `2026-08-02T01:02:13.039541+00:00` |
| 6 | `MANAGER_EVENT_CLAIMED` | `2026-08-02T01:02:13.518541+00:00` |

The source timestamps are nondecreasing; equal timestamps for detection, attempt, and delivery
are allowed by the logging specification. The shared wake ID is present on stages 3–5 and all
six records share the epoch and event IDs.

Manager raw producer order, including the wait boundary, was:

    MANAGER_WAIT_STARTED (2026-08-02T01:02:11.426836+00:00)
    -> MANAGER_WAKE_RECEIVED (2026-08-02T01:02:13.039541+00:00)
    -> MANAGER_WAIT_FINISHED (2026-08-02T01:02:13.278540+00:00)
    -> MANAGER_EVENT_CLAIMED (2026-08-02T01:02:13.518541+00:00)

Thus receipt was the first manager action after delivery/resumption. The wait-finish record carries
the same wake ID, event ID, activity `blocking-wait`, and transport.

Machine-readable wake analyzer result from `wake-result.json`:

    status: COMPLETE
    wake_id: a2aa1b8e-b125-40ae-908f-31af93b0af2a
    attempted_to_delivered_seconds: 0.0
    delivered_to_received_seconds: 0.407
    received_to_claim_seconds: 0.479

The watcher report has `cursor_drained: true`, `observation_errors: []`, and all three trusted
source coverages have `error: false` and `partial_bytes: 0`. The report's two broader
`INSUFFICIENT_EVIDENCE` findings are the expected non-wake helper/deadline classifications noted
above; the wake finding's nested `wake_evidence.status` is `COMPLETE` with the metrics shown here.

## Quiet-timeout control

`phase4-wake-evidence/quiet-result.json` independently contains:

- `event_id: WATCH_TIMEOUT`;
- `timeout_seconds: 0.3`;
- no `wake_id` field in the timeout event; and
- `wake_records: []`.

Independent traversal found zero quiet JSONL records and zero records with a `wake_id` or
`MANAGER_WAKE_*` kind. `quiet-watcher/watcher/attention-report.json` has `cursor_drained: true`,
`events: []`, `observation_errors: []`, and all classification counts zero.

## Failed-wake, fail-closed, and disabled controls

- `harness_watcher_implementation/tests/test_attention.py:51-77` proves a complete chain is
  `COMPLETE`; missing stages, duplicate delivery, reused wake IDs, and out-of-order timestamps
  are `INSUFFICIENT_EVIDENCE`; a failed wake is `FAILED` only with request creation and harness
  observation; a failed-only chain missing observation is insufficient; and a retry uses a new
  wake ID and can become complete.
- `harness_watcher_implementation/tests/test_attention.py:30-47` validates UUID/provenance,
  mutually exclusive delivered/failed outcomes, and exact wait-finish wake/transport linkage.
- `orchestrator_harness/tests/test_manager_notifications.py:100-130` proves two attempts have
  exactly one outcome each and that an explicit `MANAGER_WAKE_FAILED` preserves
  `delivery_succeeded: false` without a delivered record for that wake ID.
- `harness_watcher_implementation/tests/test_attention_ingestion.py:22-25` proves watcher-disabled
  ingestion is a clean no-op; `run_attention_practical.py:207-212` exercises the disabled recorder
  CLI gate.
- `harness_watcher_implementation/tests/test_attention_ingestion.py:26-49` proves malformed or
  impossible durable evidence is reported as `INSUFFICIENT_EVIDENCE`.
- The retention coverage at
  `harness_watcher_implementation/tests/test_attention_practical_retention.py:5-22` invokes the
  real practical with `--evidence-dir`, checks the six kinds, one shared wake ID, sorted source
  timestamps, fixed epoch/event IDs, and quiet absence of wake ID/records.

## Isolation

No hardware, firmware, provider, MCP server, deployment, commit, push, flash, collaboration
notification, watcher/observer/reviewer subagent, or AI relay was used. The practical alone
launched the real `python -m orchestrator_harness ... watch --until-actionable` subprocess and
published the synthetic external signal through its existing fixture.

## Cleanup proof

After all commands:

- no Python practical or blocking harness-watch process remained;
- no practical or quiet runtime directories remained under the repository's runtime owners;
- `orchestrator_harness/.state` remained absent;
- exactly 12 generated `__pycache__` directories were removed, each resolved and verified inside
  `orchestrator_harness`, `harness_watcher_implementation`, `harness_common`, or
  `scripts/orchestration`; and
- zero allowed-tree `__pycache__` directories remained.

The retained `phase4-wake-evidence` directory and report artifacts were preserved. No broad or
unrelated deletion was performed.

## Observed ambiguity

The initial preflight process probe matched its own PowerShell command text. This was not a
workload process; the subsequent Python-name-filtered probe returned `NONE`. It did not affect the
run. The broader watcher classifications and their non-wake deadline/helper causes are documented
above rather than omitted.
