# Clean-N manager report

Epoch: `20260731-s1-clean-n`  
Counter before/after manager review: `0/3` / `0/3`  
Manager verdict: `NONCOUNTING_PENDING_INDEPENDENT_AUDIT`

## Scope and progress

Clean-N started only after the Clean-M harness repair independently passed. The successor gates
passed: the standalone operator launcher survival/cleanup smoke left no residue, and an exact
synthetic `MANAGER_REVIEW_DUE` acknowledgement advanced its baseline. The primary owner, optional-
watcher owner, and all four lane controllers were launched through the new operator launcher.

All four persistent Luna-high/default sessions completed one concurrent host-only preparation
turn and exited zero:

- Atlas/A22 prepared classified setup-response capture and a fresh N B14 entry.
- Boreal/D31 prepared bounded exact provider-ancestry polling and a fresh N APP-1 entry.
- Cygnus/A24 replaced the short-lived paired call-operator launcher with separate durable stdio
  relays and a fresh N no-flash/no-RF entry.
- Delta/A26 made malformed CIM rows ignorable while retaining exact valid ancestry and prepared a
  fresh N counter entry.

The manager reviewed each `CLEAN_N_PREPARED.md`; focused host checks were green and no board,
provider public operation, MCP hardware action, request/relay, flash, RF, or `RESULT.json` occurred.
No live endpoint was started after the primary harness exposed the findings below. This preserves
all four prepared boundaries for the successor epoch.

## Provisional primary-harness findings for independent audit

### 1. Startup scan used a pre-sample observation time and emitted false `STALE_STATUS`

The primary scan's event was observed at `2026-07-31T22:44:08.551455Z`, but its own event data
contained Boreal controller/process creation at `22:44:15.248843Z` and Codex creation at
`22:44:16.843055Z`. A later complete scan proved all four exact identities current with no
conflict/error. This can occur because the watcher captures `observed = clock()` before a slow
Windows process inventory and reads status/processes created during that inventory against the
earlier timestamp. The false error occupied the pending slot until manager review/ack.

Evidence: event ID
`a41cde939e256d4d95050cf42faaad28a372ce5b6fee3b889999a76bf85b1305`,
`orchestrator_harness/canary-20260731-s1-clean-n-state/events.jsonl`, and
`.agent-workspace/CANARY_CLEAN_N_MANAGER_REVIEW_001_SCAN.json`.

### 2. Deferred checkpoint versions were not superseded by newer content at the same identity

While the review notification was pending, Boreal updated the same
`PARALLEL_CHECKPOINT.md` identity three times. The deferred backlog retained all three event IDs/
hashes. After current manager signals were reviewed, it made the oldest Boreal checkpoint hash
`862bbc...` pending even though later hashes `57382a...` and `6594bf...` were already queued and the
file's current content was the latest. That creates redundant, obsolete manager wake-ups and can
grow the queue during normal checkpoint refinement. Explicit manager signals remained distinct
and were correctly delivered; only same-identity checkpoint/result versions should coalesce to the
latest unacknowledged version.

Evidence: final
`orchestrator_harness/canary-20260731-s1-clean-n-state/pending-notification.json` and checkpoint
events for identity `lane:20260731-s1-clean-n:Boreal:D31:checkpoint` in `events.jsonl`.

## Manager procedure and watcher

The manager inspected every lane at the required cadence, reviewed/acked the transient stale event,
performed one whole-suite formal review, acknowledged its exact event, and immediately proved
`review_baseline_utc` advanced from `22:44:39.179210Z` to `22:49:33.359272Z`. Durable deferred
signals survived lane exits and were delivered, confirming the Clean-M lost-handoff repair.

The optional watcher ran three real Terra-high evaluations; every outcome was `defect=false`. It
stopped cooperatively with `exit_reason: stop-requested`. No optional-watcher defect is claimed.

## Shutdown and retained evidence

All four controllers/Codex children had already exited zero. The optional watcher and primary
owner/watcher stopped cooperatively. Exact relevant inventory is empty at
`.agent-workspace/CANARY_S1N_FINAL_PROCESS_INVENTORY.json`. No hardware lease, provider/MCP child,
request, relay, or server repair is active. The counter remains `0/3`; the next live phase must wait
for independent classification and any accepted narrow harness repair.
