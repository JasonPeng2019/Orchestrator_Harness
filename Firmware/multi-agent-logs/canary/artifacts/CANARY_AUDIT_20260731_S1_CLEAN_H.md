# Canary audit — 20260731-s1-clean-h

## Verdict

**ACCEPTED_NONCOUNTING; counter remains 0/3.** All four counting endpoints were missed. The stop was safe and retained useful live-route evidence; no production-server or hardware defect is validated.

## Classification

| Area | Finding | Disposition / evidence |
|---|---|---|
| Manager/orchestrator | Cygnus received two prompts naming unsupported `manager-signal/v1` kinds (`WAITING_PROVIDER_WINDOW`, then `FAIL`). Originals were quarantined and normalized. | **Manager-procedure issue.** `.agent-workspace/CANARY_CLEAN_H_ISSUES.jsonl`; primary `MANAGER_SIGNAL_READ_ERROR` events. Future prompts must enumerate valid kinds only. |
| Run-local/doer | A22 generated helper had an incorrectly indented artifact hook; D31 recursively launched its wrapper via `D31_S1_LAUNCHER`; A24 failed to parse returned `redirect: board_fix_setup`; Delta stopped before its measurement. | **Run-local/doer issues**, not server outcomes. Four `STATUS.md`/`PARALLEL_CHECKPOINT.md`; A22 `mcp-runtime/a22-b14-s1-clean-h/clean-h-launch-failure.json`; D31 `mcp-runtime/d31-rst01-s1-clean-h/evidence/20260731T190435Z/`; A24 paired `evidence/paired_result.json`; A26 S1H checkpoint. |
| Primary harness | Boreal `STALE_STATUS` at `18:54:12Z` preceded its new controller start at `18:54:14Z` and cleared through ordinary status/exit reconciliation. The retained terminal pending line surfaced only on foreground shutdown; no duplicate action, bad lease, false request, or final residue occurred. | **NONISSUE / EXPECTED_TRANSIENT.** Clean-H primary events, managed runtime, final scan. No primary repair justified. |
| Optional watcher | Startup warning `hwa-76af…` evaluated old manager-log material and alleged pre-repair creation handling although primary already had the clean-G repair; later polls reported no defect. | **VALIDATED optional-watcher defect.** `harness_watcher/runs/20260731-s1-clean-h/watcher/{alerts.json,events.jsonl}` and clean-G repair evidence. Minimal repair: baseline/filter input to watcher epoch at startup (or mark earlier records historical) before evaluator submission; retain current-epoch fault detection. |
| Primary transient states | In-flight `MCP_STATE_UNKNOWN`, `REQUEST_AMBIGUOUS`, expiry, and finalization observations cleared as lifetime/relay/status files stabilized. | **NONISSUE / EXPECTED_TRANSIENT.** primary events and final scan. |
| Server/hardware | A24's `continue_setup` redirect was valid; the parser failed to consume it. No flash/RF/campaign mutation occurred; other lanes stopped before board action or measurement. | **No production-server or hardware defect.** Per-lane paired/runtime evidence. |

## Manager and shutdown

Manager fresh scans were about 75–91 seconds apart, the one hash-bound A24 request was serviced before deadline, and no duplicate attempt was started. Final scan at `2026-07-31T19:21:31.792732Z` shows exited/checkpointed lanes, zero duplicate attempts/helpers/current requests/conflicts/observation errors/process errors. Optional watcher stopped at `19:19:53Z`; primary stopped at `19:20:04Z`; final inventory has no suite process. See `.agent-workspace/CANARY_S1H_FINAL_SCAN.json`, final process inventory, and primary managed runtime.

## Narrow next prerequisites

1. Fix and focused-test watcher startup epoch/cursor filtering only: old-log fixture emits no alert; current regression still alerts.
2. Correct only A22 hook indentation, D31 launcher variable binding, A24 redirect parser, and manager signal-kind prompt template; focused host tests each.
3. Use a fresh epoch/lifetimes/requests after fixes. Preserve locked catalog and clean-H route/cleanup evidence; do not rerun terminal work or enter a production-server repair loop.
