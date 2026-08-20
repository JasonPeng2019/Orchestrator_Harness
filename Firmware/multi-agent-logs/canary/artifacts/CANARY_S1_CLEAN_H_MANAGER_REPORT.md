# Clean-H manager report — `20260731-s1-clean-h`

## Verdict submitted for independent audit

- **Counting result:** non-counting; counter remains `0/3` pending the persistent auditor's
  independent decision.
- **Reason:** none of the four declared counting endpoints in
  `.agent-workspace/CANARY_S1_CLEAN_H_TARGET.md` was reached. The epoch nevertheless exercised four
  concurrent persistent lanes, serialized provider-enumeration releases, one exact live manager
  relay, disjoint hardware lifetimes, STM-A lease turnover, active supervision, and cooperative
  shutdown.
- **Server repair:** none proposed. All observed functional stops are presently classified as
  run-local controller/adapter or manager-prompt defects, not production `BYO-Firmware-MCP`
  defects.

## Lane outcomes

1. **Atlas / A22 / STM-A**
   - The first binding turn prepared the H adapter and exited; the manager resumed the same Atlas
     session for the live-only turn.
   - The only helper PID `170528` exited before initialization because Atlas inserted an artifact
     signal hook at the wrong indentation in generated Python. No MCP lifetime, provider
     enumeration, board operation, request, relay, B14, or B34 occurred. Atlas did not retry.
   - Evidence: `fresh-experiments/A22_20260726-062324/.agent-workspace/PARALLEL_CHECKPOINT.md`,
     `.agent-workspace/mcp-runtime/a22-b14-s1-clean-h/clean-h-launch-failure.json`, and
     `20260731-s1-clean-h-Atlas-A22-CHECKPOINT-launch-failure.json`.
2. **Boreal / D31 / STM-B**
   - The manager released provider enumeration only after Atlas reached a safe pre-initialization
     endpoint.
   - Boreal's single S1H helper recorded a lifetime, then stopped before initialization with
     `OSError(22)` because the derived wrapper bound `D31_S1_LAUNCHER` to the helper wrapper itself,
     recursively launching it. No public artifact, board setup, RST01 request/relay, or board action
     occurred. Exact descendants were absent at cleanup.
   - Evidence: `fresh-experiments/D31_20260726-062325/.agent-workspace/PARALLEL_CHECKPOINT.md` and
     `.agent-workspace/mcp-runtime/d31-rst01-s1-clean-h/evidence/20260731T190435Z/`.
3. **Cygnus / A24 / NRF-A+NRF-B**
   - The manager released the paired provider window only after Boreal recorded its lifetime and
     its failed descendants were absent, then resumed the same Cygnus session.
   - Both isolated MCP lifetimes and first public artifacts were recorded. The manager reviewed and
     approved exactly one hash-bound no-flash NRF-A `board_setup` request.
   - The live `continue_setup` response returned `status=setup_continuation_accepted` with an
     explicit `redirect` to `board_fix_setup`; the retained run-local parser did not recognize that
     field. The sole attempt stopped and cleaned both process trees without flash, RF, or mutation.
   - Evidence: `fresh-experiments/A24_20260726-052146/.agent-workspace/canary/20260731-s1-clean-h/Cygnus/A24/PAIRED-FLASH/evidence/paired_result.json`.
4. **Delta / A26 / STM-A**
   - Delta first completed the board-free H bind. After Atlas released STM-A, the manager created a
     fresh STM-A release and resumed the same Delta session.
   - Delta built a run-local H stdio controller, recorded the MCP lifetime and first public
     artifact, captured the live tool surface and setup route, then intentionally stopped before
     `board_setup-plan`. No request, relay, board action, or `+8/+1/+1/+0` measurement occurred.
   - Evidence: `fresh-experiments/A26_20260726-062325/.agent-workspace/hil/i1-stm-a/s1h-counter-delta-20260731/` and its current `PARALLEL_CHECKPOINT.md`.

## Manager/orchestrator issues

- The original Cygnus prompt said to publish `WAITING_PROVIDER_WINDOW` without distinguishing a
  phase from a valid signal kind. Cygnus emitted the unsupported kind twice. The manager preserved
  each original under `evidence/clean-h-invalid-signals/` and normalized each to an immutable HELP
  record.
- The Cygnus live-resume prompt then incorrectly stated that `FAIL` was a valid
  `manager-signal/v1` kind. The endpoint FAIL was preserved and normalized to CHECKPOINT.
- These are recorded in `.agent-workspace/CANARY_CLEAN_H_ISSUES.jsonl`; they make the orchestrator
  non-issue-free but do not presently justify a harness/watcher repair.
- The manager performed fresh scans throughout, serviced the exact A24 request before deadline,
  left unrelated lanes running through functional stops, never started duplicate live attempts,
  and did not touch the ambient unrelated MCP process.

## Harness and watcher observations requiring auditor disposition

- Final read-only scan: `.agent-workspace/CANARY_S1H_FINAL_SCAN.json` at
  `2026-07-31T19:21:31.792732Z`: all four lanes `CHECKPOINTED/EXITED`, zero duplicate attempts,
  no helpers, no manager requests, no conflicts, no observation errors, and no process errors.
- Primary managed watcher runtime exited cooperatively with `exit_reason=stop-requested` at
  `19:20:04Z`. The independent 75-second alarm produced fresh scans through the terminal lane
  boundary and then stopped from its exact sentinel. Optional watcher PID `196052` also exited
  cooperatively at `19:19:53Z`; exact process inventory found no suite lane/helper/MCP/watcher PID.
- The primary managed watcher retained a pending `STALE_STATUS` notification for Boreal observed at
  `18:54:12Z`, about two seconds before its new controller launch and before its fresh status became
  live. The foreground exec cell exposed that line only when stopped. Determine whether this is
  merely a pre-launch transient plus host streaming behavior, or a validated harness notification
  defect.
- The optional watcher emitted one warning at startup (`hwa-76af...`) claiming recycled historical
  PIDs could be misclassified because creation time was ignored. It cited old manager-log context,
  while the current primary code had already received the Clean-G historical-lifetime repair; all
  subsequent optional-watcher polls returned no defect. Determine whether this is stale-input noise,
  a watcher cursor/scope defect, or a valid remaining production defect.
- Primary events also recorded expected transient `STALE_STATUS`, `MCP_STATE_UNKNOWN`,
  `REQUEST_AMBIGUOUS`, and expiry warnings while status/lifetime/relay files were in flight. Each
  relevant condition cleared, and the final scan is clean. Grade only functional defects, not
  expected eventual-consistency transitions.

## Requested independent audit

Apply the fixed canary rubric and inspect source/evidence directly. Return:

1. counting verdict and exact counter;
2. issue classification by harness, optional watcher, manager/orchestrator, doer/run-local code,
   server, and hardware;
3. for each harness/watcher criticism, `VALIDATED_DEFECT`, `NONISSUE/EXPECTED_TRANSIENT`, or
   `ADVISORY`, with evidence;
4. whether a harness/watcher code repair is justified now and, if so, the minimal repair scope;
5. the next sprint's narrow prerequisites without rerunning locked evidence.
