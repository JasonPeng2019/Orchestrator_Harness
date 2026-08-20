# Clean-I manager report ? `20260731-s1-clean-i`

## Verdict submitted for independent audit

- **Counting result:** non-counting; counter remains `0/3` pending the persistent auditor's independent decision.
- **Reason:** none of the four declared endpoints in `.agent-workspace/CANARY_S1_CLEAN_I_TARGET.md` was reached. Each lane used one bounded live attempt, preserved prior evidence, stopped without a retry, and cleaned its exact process scope.
- **Server repair:** none proposed. All live functional stops are run-local launcher/adapter defects. No evidence identifies a production `BYO-Firmware-MCP` defect.

## Lane outcomes

1. **Atlas / A22 / STM-A**
   - One helper/MCP lifetime was attempted. The adapter called populated `board_setup-plan` before the required all-NULL initialization call; the server correctly refused it.
   - Atlas stopped and cleaned the exact lifetime. No hardware action, B14, B34, or retry occurred.
   - Evidence: `fresh-experiments/A22_20260726-062324/.agent-workspace/PARALLEL_CHECKPOINT.md` and `.agent-workspace/mcp-runtime/a22-b14-s1-clean-i/clean-i-helper.stderr.log`.
2. **Boreal / D31 / STM-B**
   - One live lifetime reached initialization. The manager reviewed and relayed exactly four calls before their deadlines: `board_setup-plan`, `board_setup`, retained-pack `continue_setup`, and the server-returned paired `board_fix_setup`.
   - Setup completed and validated the assigned STM-B. The helper then incorrectly required another redirect in the truthful terminal `setup_completed` response and stopped before the RST01 request/action.
   - No retry, APP-1 work, or `RESULT.json`; all exact descendants exited.
   - Evidence: `fresh-experiments/D31_20260726-062325/.agent-workspace/mcp-runtime/d31-rst01-s1-clean-i/evidence/20260731T194545Z/final-record.json` and current `CLEAN_I_LIVE_CHECKPOINT.md`.
3. **Cygnus / A24 / NRF-A+NRF-B**
   - The single paired controller attempt failed before either MCP lifetime because the fresh route-adapter import path did not register its module before `dataclass` evaluation.
   - No provider process, board action, flash, RF, request, relay, or retry occurred. The endpoint was checkpointed without a terminal result.
   - Evidence: `fresh-experiments/A24_20260726-052146/.agent-workspace/PARALLEL_CHECKPOINT.md` and `cygnus_a24_s1_clean_i_live_last_message.txt`.
4. **Delta / A26 / STM-A**
   - The single live command stopped before MCP initialization because the launcher compared equivalent runtime paths without normalizing slash direction.
   - Delta repaired and host-tested the guard, but correctly did not open a replacement lifetime. No board action, request, relay, measurement, or retry occurred.
   - Evidence: `fresh-experiments/A26_20260726-062325/.agent-workspace/evidence/clean-i/s1i-bounded-functional-stop.json` and current `PARALLEL_CHECKPOINT.md`.

## Manager/orchestrator observations

- All four same-session prep turns ran concurrently; live provider windows were released serially while unrelated board-disjoint work continued. STM-A transferred only after Atlas released it.
- The manager serviced every D31 exact live request before deadline and approved only the named call. No broad approval, flash, RST01, APP-1, or retry was implied.
- The initial Cygnus prep prompt used an ambiguous relative target path; the live prompt corrected it. This is a manager-procedure issue and makes the epoch non-issue-free independently of endpoint failures.
- No duplicate controller, duplicate live attempt, lease conflict, concurrent same-task process, or server mutation occurred.

## Primary harness observations requiring auditor disposition

1. A brand-new Clean-I managed watcher surfaced a historical Clean-H Atlas `RESOURCE_AMBIGUOUS` notification at bootstrap. The manager classified it as stale history and acknowledged the exact event.
2. For active D31, the snapshot's manager-review data selected a historical Clean-F request even while current Clean-I HELP/request records existed. It also emitted `RESOURCE_AMBIGUOUS` stating no current request identity despite those records.
3. For terminal A24 and A26 attempts that truthfully failed before MCP creation, the final scan still reports missing lane/session-correlated MCP-lifetime ambiguity. These were not real conflicts or leaked resources.
4. Every notification was reviewed and acknowledged. Final pending notification is null, resource conflicts are empty, duplicate attempts are zero, and observation/process errors are empty. See `.agent-workspace/CANARY_S1I_FINAL_SCAN.json`.

The auditor should decide whether these are one correlation/lifecycle defect family or expected declared-server eventual-consistency. If validated, repair only primary harness epoch/request/lifecycle correlation; do not change lane controllers or server behavior as part of that repair.

## Optional watcher result

- The repaired startup baseline behaved as designed: the first service poll was `evaluated=false`, so pre-existing history was not evaluated.
- Eight subsequent polls evaluated only new activity and every Terra-high outcome reported `defect=false`; no `alerts.json` was created.
- Optional watcher exited cooperatively with `reason=stop-requested`. No exact watcher PID remained.
- Evidence: `harness_watcher/runs/20260731-s1-clean-i/watcher/events.jsonl`.

## Cleanup

- Primary managed watcher and optional watcher exited by their explicit stop commands; the 75-second supervision loop exited by its sentinel.
- All recorded lane controller/Codex/helper/MCP identities are absent. PID `174004` is a later unrelated VS Code terminal PowerShell, not the historical Atlas helper.
- Narrow command-line scan found no Clean-I controller, watcher, or MCP process. Ambient root Codex PID `99828` remains intentionally.
- Primary pending notification is null.

## Requested independent audit

Apply the fixed canary rubric and return:

1. counting verdict and exact counter;
2. issue classification by primary harness, optional watcher, manager/orchestrator, doer/run-local code, server, and hardware;
3. for each harness/watcher criticism, `VALIDATED_DEFECT`, `NONISSUE/EXPECTED_TRANSIENT`, or `ADVISORY`, with evidence;
4. whether a harness/watcher repair is justified and the minimal repair scope;
5. narrow successor prerequisites without rerunning accepted evidence.
