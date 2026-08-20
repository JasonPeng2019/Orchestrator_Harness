# Advisory post-sprint review — 20260802-m5-s3-101953Z

## Scope
Read-only review against `goal.md`, the M5 spec/checklist, and `ATTENTION_LOGGING.md`. Raw sources reviewed: the epoch watcher timeline/report/cursor and input JSONL, harness stdout/stderr/attention JSONL, and the run-local audit, isolation, process-cleanup, resource-cleanup, and checklist files.

## Advisory gates

| Gate | Result | Evidence-based rationale |
|---|---|---|
| Harness | **HARNESS_BUG** | Delta was observed at `10:29:05.723786Z` but remained deferred until actionable `10:30:06.825464Z`, after its `10:29:29.835149Z` delivery deadline. The independent watcher report classifies this exact event `HARNESS_DELIVERY_DELAY`, 44.100780 s late. A root native blocking wait was active from `10:28:45.633763Z`, so neither busy work nor idle-manager inattention explains the late delivery. |
| Watcher | **WATCHER_PASS** | Cursor is drained; all six watched sources show `error:false`, zero partial bytes, and final offsets; no observation-errors file exists. Timeline IDs/timestamps agree with raw sources and the report accurately distinguishes three healthy chains and Delta's harness delay. `ISOLATION.json` records diagnostic-only operation. The report's 34 unrelated conservative `INSUFFICIENT_EVIDENCE` entries are not a coverage/correlation defect in these four chains. |
| Manager evidence | **MANAGER_EVIDENCE_SUFFICIENT** | Four genuine external-lane chains are classifiable. Atlas/Boreal/Cygnus give waiting-manager healthy samples. Delta is a paired genuine busy-manager sample, then shows a later harness-side delay while root is in native wait. These distinguish healthy operation, busy activity, harness delay, and no idle-manager inattention. This independent gate does not make the sprint qualifying. |

## Four genuine request chains

The six stages are worker creation; harness observation/actionable selection; wake attempt; wake delivery; manager receipt; and manager claim. All use root session/invocation `019fbbc1-63ba-7140-ab1d-46bf412596e9` / `root-20260802-m5-s3-101953Z-001`; each wake has the exact ID through receipt and matching wait finish, component `orchestrator_harness.watch_until_actionable`, transport `blocking_harness_wait_stdout`, and claim selection snapshot.

| Lane | Six-stage UTC chain | Response / resume | Classification |
|---|---|---|---|
| Atlas A22 | create `10:24:31.172768`; observe/actionable `10:24:45.165594`; attempt/deliver `10:24:49.728049` wake `17949c58-1fe5-4e47-bc91-675988ab5cb4`; receipt `10:25:14.315472`; claim `10:25:15.131569` | publish `10:25:15.547569`; ack `10:25:24.070940`; receipt `10:25:44.749022`; resume `10:25:51.761035` | Healthy / `NO_BLOCKING_IMPACT` |
| Boreal D31 | create `10:25:17.917311`; observe `10:25:31.522116`, actionable `10:26:14.076176`; attempt/deliver `10:26:18.057849` wake `abc68791-9645-46ed-ad5f-997c96311941`; receipt `10:26:37.786853`; claim `10:26:38.409585` | publish `10:26:38.749716`; ack `10:26:47.108778`; receipt `10:27:44.901447`; resume `10:27:50.427109` | Healthy / `NO_BLOCKING_IMPACT` |
| Cygnus A24 | create `10:24:31.3652774`; observe/actionable `10:25:31.522116`; attempt/deliver `10:25:35.666772` wake `d73b15ff-ae24-4f9c-b2b9-e8e1b2af9faf`; receipt `10:25:56.170376`; claim `10:25:56.845027` | publish `10:25:57.156337`; ack `10:26:05.538081`; receipt/resume `10:26:11.3964529` | Healthy / `NO_BLOCKING_IMPACT` |
| Delta A26 | create `10:27:59.835149` (raw record field; recorder entry `10:28:33.307960`); observe `10:29:05.723786`; actionable `10:30:06.825464`; attempt/deliver `10:30:11.712615` wake `a6dd7f0c-5ab2-41e9-912d-1973adbb2e4a`; receipt `10:30:34.665990`; claim `10:30:35.411989` | publish `10:30:35.744990`; ack `10:30:44.160458`; receipt `10:31:14.540212`; resume `10:31:14.962705` | Harness delay / `HARNESS_DELIVERY_DELAY` |

No event loss, stale wake-ID mixup, response loss, or acknowledgement failure is evidenced for the four chains.

## Delta busy activity and causal attribution

**Delta creation at `10:27:59.835149Z` is covered by paired busy work.** Raw Delta records carry that `created_utc`. `busy-manager-resource-readiness-audit-001` begins `10:27:04.304481Z` (record `fe5bcae5-a762-4d4d-9d38-d1868f2a2a84`) and ends `10:28:35.938693Z` (record `0f1a1ff6-d14f-4f6b-8df7-70dc62635957`), same session/invocation/activity ID and `RUNNING_TOOL`. It also covers the actual signal-recorder timestamp `10:28:33.307960Z`. `BUSY_MANAGER_RESOURCE_AUDIT.json` substantiates real resource/snapshot work and no live hardware/provider/MCP action.

Busy work does **not** explain Delta's breach: it ends at `10:28:35.938693Z`; root starts native wait at `10:28:45.633763Z`; Delta is observed before deadline at `10:29:05.723786Z` but not actionable until `10:30:06.825464Z` (37.0 s after deadline). After delivery, root receipt is 22.953375 s later and claim follows receipt by 0.745999 s; response, ack, worker receipt, and resume all succeed before the response deadline. Therefore this is neither idle-manager inattention, busy-manager contention, nor downstream response failure; it is harness selection/delivery delay with deadline precedence.

## Isolation and cleanup

`ISOLATION.json` records native blocking harness wait as the only discovery path and no watcher evaluator, AI watcher/relay, runner/wrapper, collaboration/user wake, or transcript/direct-signal discovery. `PROCESS_CLEANUP.json` records all 12 registered PIDs absent at `10:33:51.824542Z`. `RESOURCE_CLEANUP.json` records all workers exited, no leases/board tokens/MCP servers, no hardware action, and `SAFE_BOUNDARY`.

## Advisory disposition

Do **not** count this sprint as qualifying: the independent harness gate is `HARNESS_BUG`. This is advisory only; root retains repair-scope and final-verdict decisions.