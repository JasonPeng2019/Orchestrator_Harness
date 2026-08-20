# Clean-K canary manager report

- Epoch: `20260731-s1-clean-k`
- Counter before/after manager review: `0/3` -> `0/3`
- Manager disposition: **NON-COUNTING; independent audit required**
- Live window: `2026-07-31T20:19:27Z` through clean shutdown at approximately `2026-07-31T21:04:31Z`
- Target: `.agent-workspace/CANARY_S1_CLEAN_K_TARGET.md`

## Benchmark disposition

Clean-K cannot count. Two of four bounded endpoints completed, while two run-local controllers
stopped before their required catalog endpoint. The primary harness also surfaced multiple
historical or already-consumed records as fresh manager actions. Useful catalog evidence is
preserved; no accepted evidence should be rerun merely because this sprint is non-counting.

## Lane outcomes

| Lane | Endpoint | Outcome | Evidence |
|---|---|---|---|
| Atlas / A22 / STM-A | B14 or first truthful populated request after null-first initialization | **Not reached.** The sole helper failed before MCP because its Windows `GetProcessTimes` recorder used an invalid handle signature. No board action and no retry. | `fresh-experiments/A22_20260726-062324/.agent-workspace/mcp-runtime/a22-b14-s1-clean-k/evidence/clean-k-launch-failure.json`; `clean-k-cleanup-audit.json` |
| Boreal / D31 / STM-B | Exactly one reviewed RST01, post-action state, stop before APP-1 | **Reached.** One `reset_and_run`; final state `SLEEPING`; no APP-1 or retry. | `fresh-experiments/D31_20260726-062325/.agent-workspace/CLEAN_K_LIVE_CHECKPOINT.md`; `.agent-workspace/mcp-runtime/d31-rst01-s1-clean-k/evidence/20260731T203323Z/` |
| Cygnus / A24 / NRF pair | Both retained artifacts flashed and first post-flash identity/UART checkpoints; no RF | **Reached.** One paired attempt; both checkpoints passed; RF stayed disabled; exact cleanup passed. | `fresh-experiments/A24_20260726-052146/.agent-workspace/CLEAN_K_LIVE_CHECKPOINT.md`; `.agent-workspace/canary/20260731-s1-clean-k/Cygnus/A24/PAIRED-FLASH/evidence/paired_result.json`; `truth_reconciliation.json` |
| Delta / A26 / STM-A | Prepared `+8/+1/+1/+0` counter/version measurement | **Not reached.** MCP initialization returned, but the run-local exact-process matcher rejected the actual launcher/uv ancestry before lifetime publication. No board/counter action and no retry. | `fresh-experiments/A26_20260726-062325/.agent-workspace/evidence/clean-k/s1k-bounded-functional-stop.json`; `s1k-cleanup-proof.json` |

All four lane controllers exited with code 0 after writing bounded checkpoint evidence. No
`RESULT.json` was created for these nonterminal endpoints.

## Primary harness observations requiring independent classification

1. A historical terminal D31 lifetime emitted a fresh `MCP_EXITED` manager action solely because
   its old PID had been reused by an unrelated process (`a3ee0d66...`).
2. A consumed Boreal setup-plan `HELP` signal resurfaced after the lane had advanced
   (`2e4029bf...`).
3. Exact A24 request/relay pairs were repeatedly classified `REQUEST_AMBIGUOUS`, including after
   consumption or supersession (`cfb6be68...`, `ce8d2e33...`, `3de6abdf...`, `4ee8fc16...`,
   `efbed949...`, `dd39eb39...`).
4. A consumed historical A24 setup request generated warning and critical expiry actions after the
   lane had advanced (`19f2ebe0...`, `024b9191...`).
5. The same consumed A24 setup `HELP` signal resurfaced after both paired post-flash endpoints had
   passed (`4545a3e6...`).

Each was reviewed and acknowledged rather than acted upon. Exact dispositions are append-only in
`.agent-workspace/ORCHESTRATOR_HARNESS/MANAGER_LOG.jsonl`. Pre-request ambiguity notifications for
currently starting hardware lanes and the scheduled manager-review notification are retained for
the auditor to classify separately; the manager does not pre-label them as defects.

## Optional watcher

The optional watcher ran for the live epoch, returned `defect:false` on every evaluator outcome,
stopped on request, and returned `{"alert": null}` on the final manual poll. Evidence is under
`harness_watcher/runs/20260731-s1-clean-k/`; final service state records
`exit_reason: stop-requested`.

## Shutdown and final state

- Primary pending notification: `null` after explicit review/acknowledgement.
- Primary watch: stopped by exact config.
- Optional watcher: stopped by exact config.
- Independent supervision loop: stopped by its exact stop file.
- Final relevant-process inventory: clean, zero matching processes.
- Final primary scan: `.agent-workspace/CANARY_S1K_FINAL_SCAN.json`.
- Final process inventory: `.agent-workspace/CANARY_S1K_FINAL_PROCESS_INVENTORY.json`.

## Next gate

The same persistent Terra-medium sprint auditor must independently assess Clean-K. If it validates
a primary-harness defect, the main model must author one narrow repair plan, have that plan reviewed,
and send implementation to the same persistent Terra-high coder. Preserve the accepted D31 and A24
progress. A successor sprint should rerun only unmet A22/A26 work plus dependency-ready forward
catalog work needed for a meaningful fresh benchmark.
