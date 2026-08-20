# Formal canary audit — 20260731-s1-clean-b

Auditor: persistent `/root/canary_sprint_auditor` (`gpt-5.6-terra`, medium reasoning)  
Decision: **NON-COUNTING**  
Counter after audit: `0/3`

## Valid findings

1. **Manager/orchestrator operational defect.** The configured review interval was 120 seconds,
   but the `15:24:35.268Z` to `15:27:50.417Z` lane-supervision gap was 195.149 seconds. One manager
   state record also used a cached scan and reported Boreal running after its controller had
   interrupted. The optional watcher correctly reported this. Smallest repair: an independent
   90–120 second alarm, a fresh no-write scan immediately before every log record, and no reuse of
   cached scan output. No primary-harness code change is justified.
2. **A22 run-local helper defect.** The one clean-B lifetime reached initialization, but the
   recorder selected the helper-owned MCP executable plus Python wrapper/child instead of the exact
   executable and therefore wrote no atomic lifetime record before setup. Atlas retained a useful
   executable-only selector fix and focused regressions. Exact descendants cleaned; no B14 or board
   action occurred. Smallest repair: reconcile the closed missing-terminal record, verify the
   narrowed selector, and use one newly assigned lifetime.
3. **D31 run-local helper defect.** `os.kill(existing_pid, 0)` was used as a Unix-style liveness
   check on Windows and interrupted the controller. No MCP, request, or RST01 action began. The
   watcher alert is valid and remains paused pending repair. Smallest repair: exact Windows-safe PID
   plus creation-time identity checking and only the focused one-outstanding-helper test.
4. **A24 run-local paired launcher/helper defect.** Both launcher PIDs were spawned and then absent
   before any public MCP artifact or provider session, producing `OSError(22)`. This is not a
   provider datapoint. One attempt only; cleanup and both delayed absence checks passed. Smallest
   repair: instrument/classify and minimally fix the paired host boundary before one new assignment.

## Non-issues

- Historical manager signals were epoch-labeled and non-live; no false assignment or duplicate
  live lane resulted.
- A22/D31 `RESOURCE_AMBIGUOUS` states truthfully describe missing terminal/no-start evidence, not
  live leases. Reconcile before re-lease; never invent evidence.
- Primary harness delivery and cooperative shutdown were correct. Final scan: no live helper,
  request, conflict, process error, or observation error.
- Optional watcher alerting, deduplication, and recovery were correct. **No watcher code change is
  justified.**

## Progress retained

- A22: B12/B15/B35/B36 and existing B14 NO_MATCH evidence.
- D31: previously accepted JSON-RPC, setup, and routing evidence.
- A24: both single-board no-flash PASS canaries.
- A26: board-free R16 and counter preparation; Delta was not launched in clean-B.

## Evidence reviewed

`orchestrator_harness/canary-20260731-s1-clean-b.json`, clean-B primary state files, manager and
monitor JSONL logs, `.agent-workspace/CANARY_S1B_SCAN_005.json`, all three clean-B controller status
and lane JSONL files, all current lane checkpoints, A24 paired-result evidence, watcher alerts and
events, `HANDOFF.md`, and the clean-B target.
