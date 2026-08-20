# M5 Q7 post-sprint advisory review

**Epoch:** `20260802-m5-q7-150000Z`  
**Scope:** read-only review after stop/cleanup. This is advice; root decides the result.

## Recommendation

| Gate | Recommendation | Why |
|---|---|---|
| Harness | `HARNESS_PASS` | All four genuine HELP signals were observed, selected by the native blocking wait, returned with exact IDs/wake transport, claimed, responded to, and acknowledged. No native crash, loss, stale HELP selection, or queue/identity defect is evidenced. |
| Watcher | `WATCHER_BUG` | The diagnostic report contains an impossible negative Delta `explicit_deferral_seconds` (the first deferral is *after* the actionable event, but the report gives `-21.318…`). That is a sign/order analysis defect, so the report is materially misleading despite its otherwise healthy diagnostic-only operation. |
| Manager evidence | `MANAGER_EVIDENCE_INSUFFICIENT` | The raw logs contain four useful six-stage chains, but the watcher’s invalid timing computation cannot be used for the architecture decision. Separately, the root link into wait 003 points to the checkpoint **receipt** rather than the checkpoint-completion terminal record, leaving the busy/preemption continuity record noncanonical. |
| Sprint | **Nonqualifying; repair/reset required** | The watcher gate fails. Do not count Q7 toward the 3/3 surface. |

## Raw chain evidence

| Lane | Worker created | Harness observed | Wake delivered | Root received / claimed / response |
|---|---|---|---|---|
| Atlas A22 | 15:02:48.522 | 15:03:23.045 | 15:03:26.260 | 15:03:45.274 / 45.865 / 46.157 |
| Delta A26 | 15:03:01.526 | 15:04:05.307 | 15:04:34.380 | 15:04:50.626 / 51.263 / 51.582 |
| Cygnus A24 | 15:03:30.191 | 15:04:26.625 | 15:05:05.881 | 15:05:26.120 / 26.784 / 27.192 |
| Boreal D31 | 15:04:01.501 | 15:04:52.091 | 15:05:39.672 | 15:05:55.938 / 56.565 / 56.879 |

Sources: native wait outputs; root attention source under `harness_watcher/.../inputs/orchestrator/.../attention.jsonl`; worker attention sources.

## Other checks

- Quiet control timed out normally. Busy control is recorded and bounded.
- Watcher was live, `evaluator_enabled: false`, cursor drained, and its log shows `EVALUATOR_SKIPPED`; no AI relay, notification, acknowledgement, or repair path influenced discovery.
- The checkpoint preempted wait 002. Its old native acknowledgement file is empty/failed; the later HELP paths were not lost and all four HELP acknowledgements succeeded. This is not evidence of a HELP-harness defect, but it supports treating the root continuity record as insufficient rather than inventing a busy explanation.
- `FINALIZE_VALIDATION.json` passes (183 records). All ten registered processes are absent; leases, providers, MCP processes, hardware actions, and temporary owners are empty.
- I found no evidence of an unallowed runner, wrapper, watcher subagent, evaluator, collaboration notification, transcript inspection, or user-message discovery.

## Smallest next action

Repair only the watcher’s deferral-time ordering/sign calculation; smoke-test the affected report classification. Then refreeze the changed surface and restart the qualifying count as required. Also correct the **manual root procedure** so a post-checkpoint wait links to `MANAGER_CHECKPOINT_COMPLETED`, not the earlier receipt. No compensating runtime component is warranted.
