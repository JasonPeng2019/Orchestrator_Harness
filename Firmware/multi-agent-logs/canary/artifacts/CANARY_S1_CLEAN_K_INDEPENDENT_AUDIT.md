# Clean-K independent canary audit — `20260731-s1-clean-k`

## Verdict

**NON-COUNTING; counter remains `0/3`.**  D31 and A24 reached their bounded
endpoints, but A22 and A26 did not.  More importantly, the primary harness
repeatedly promoted historical or consumed state into manager-actionable work.
The evidence is useful and preserved; no consumed Clean-K lifetime should be
retried.

## Validated issues

| Severity / class | Finding and evidence |
|---|---|
| **Primary harness defect — high** | Historical terminal D31 lifetime PID reuse generated fresh actionable `MCP_EXITED` `a3ee0d66...`.  The event itself records PID `177940` with a creation time over six hours different from the recorded start and `state: MCP_EXITED`; it has no current Clean-K lane relation.  A PID-reuse observation of a closed historical lifetime must remain audit data, not wake an active epoch. |
| **Primary harness defect — high** | Consumed/superseded HELP signals resurfaced as current manager actions: D31 setup-plan `2e4029bf...` and A24 setup HELP `4545a3e6...`.  The manager log and retained D31/A24 records show their exact actions had already been relayed and the lanes advanced/passed.  This is a lifecycle/consumption correlation defect, not a missed doer request. |
| **Primary harness defect — high** | Exact A24 request/relay pairs were labelled `REQUEST_AMBIGUOUS` while the same observations say `relay_reason: manager request and exact approved relay binding match`; examples are `cfb6be68...`, `ce8d2e33...`, `3de6abdf...`, `4ee8fc16...`, `efbed949...`, and `dd39eb39...`.  The inspected request and relay have identical request ID, request hash, lane, assignment, snapshot, and tool-argument binding; the request's recorded lifetime points to the exact NRF-A lifetime.  A matching, consumed or superseded pair must not be presented as an unresolved ambiguity. |
| **Primary harness defect — high** | The consumed A24 setup request remained `lifetime_state: LIVE` for notification purposes and generated expiry actions `19f2ebe0...` and `024b9191...` after consumption/advancement.  Later repeated warning/critical/expired events in state confirm the same stale lifecycle treatment.  Expiry remains necessary for a live, unconsumed request, but not for a consumed/superseded exact request. |
| **Manager-procedure defect — medium** | Formal review cadence was not acknowledged/reset once the second review became due: `MANAGER_REVIEW_DUE` is emitted at 20:27:38 (then again for Boreal at 20:32:24 using the old 20:24 baseline) and is only cleared when lanes exit, with no corresponding review acknowledgement in `MANAGER_LOG.jsonl`.  The first review was properly logged at 20:24:30.  The manager did inspect higher-priority warnings, but that is not the configured 120-second review acknowledgement. |
| **Run-local defect — medium** | A22's one attempt failed in the local Windows `GetProcessTimes` identity recorder before MCP creation (`clean-k-launch-failure.json`).  No board action or retry occurred. |
| **Run-local defect — medium** | A26 received `initialize`, then its local exact-process matcher failed to find the provider below the launcher before lifetime publication (`s1k-bounded-functional-stop.json`).  No board/counter action or retry occurred. |

## Nonissues / expected observations

- The short active-lane pre-request/pre-lifetime `RESOURCE_AMBIGUOUS` notices
  for A22, D31, A24, and A26 are **expected transients**.  Each precedes the
  relevant publication or bounded stop and clears; they do not show a conflict.
- Boreal's initial `STALE_STATUS` is a **pre-spawn publication transient**: the
  exact controller/Codex identities subsequently matched.  It is not a harness
  repair target.
- D31's helper `exit_code: 1` is an **expected nonterminal-helper contract**.
  The controller completed with code 0, the checkpoint proves exactly one
  reviewed `reset_and_run`, final `SLEEPING`, and zero descendants.  It is not
  an unclean shutdown.
- A24's raw `firmware_mutated:false` is **not a functional endpoint failure**.
  `flash_executed:true`, exact relays, two post-flash identity/UART checkpoints,
  and clean delayed absence establish the actual result; the reconciliation
  preserves the raw default value.  Correcting that metadata is advisory
  evidence hygiene, not a primary/watcher repair prerequisite.
- Optional watcher is **clean**: first poll is unevaluated, all subsequent
  evaluator results are `defect:false`, stop is requested and observed, and the
  final manual poll has `alert:null`.  No watcher repair is justified.
- Final scans show zero duplicate live attempts, resource conflicts,
  observation/process errors, or matching processes.  All four final lanes are
  exited/checkpointed and resource-releasable.  No server or hardware defect is
  supported by this epoch.

## Repair decision

**One narrow primary `orchestrator_harness` repair is justified.**  It should
make notification/actionability lifecycle-aware without deleting historical
evidence: historical terminal MCP PID mismatch must not become a fresh action;
manager HELP signals must become nonactionable once their exact request/relay is
consumed or superseded; exact bound request/relay+lifetime records must not be
classified ambiguous; and expiry must apply only to current, unconsumed
actionable requests.  Preserve genuine live missing-MCP, unbound/ambiguous
request, current request-expiry, resource-conflict, and live helper/MCP alarms.

The review-cadence lapse is manager procedure, not a reason to broaden the
harness repair.  The next manager must explicitly acknowledge/reset each due
review even when a higher-priority notification is being handled.

## Successor constraints

1. Plan/review/test the narrow primary lifecycle-actionability repair using
   retained Clean-K-shaped controls before another counting epoch; include PID
   reuse, consumed HELP, exact bound relay, consumed expiry, and genuine live
   positive controls.
2. Preserve D31 and A24 endpoint evidence; do not repeat their completed Clean-K
   lifetimes, flash, reset, or setup work.
3. Repair and host-prove only A22's Windows identity recorder and A26's
   provider-ancestry matcher.  Resume them under fresh assignments/lifetimes;
   no retry in the consumed Clean-K attempts.
4. Start the successor with an explicit cadence/ack ledger.  Require a fresh
   review acknowledgement at each 120-second due point independent of warning
   priority, plus exact clean shutdown/process inventory.
