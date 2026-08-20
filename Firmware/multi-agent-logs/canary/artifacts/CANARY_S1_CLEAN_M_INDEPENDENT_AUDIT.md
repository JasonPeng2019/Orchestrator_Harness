# Clean-M independent audit

**Epoch:** `20260731-s1-clean-m`  
**Disposition:** **NONCOUNTING; counter remains `0/3`.**  
**Audit scope:** read-only evidence audit; no hardware, resume, retry, server repair, or source edit was performed.

## Verdict and ownership

| Finding | Verdict | Owner / required disposition |
|---|---|---|
| Lower-priority Delta checkpoint `e7d3c7d4d5845701f4051f9ea9079364e8f5a1322767ec2f7f73155cdb7fadd1` was not subsequently made pending | **Validated primary-harness defect** | Repair the notification/re-arm path and add a regression where a live-lane manager signal loses to a higher-priority event, the lane closes, and the unacknowledged signal still becomes pending for review. |
| First primary watcher, first Cygnus controller, and optional watcher were reaped by transient tool-shell jobs | **Validated manager launch-topology failure** | Use a durable manager-owned breakaway launcher for *every* long-lived owner/watcher/controller, with PID+creation and normal-exit/stop evidence. This is not a watcher product failure. |
| Formal review cadence/ack transition | **Manager-procedure supervision gap** | The durable history baseline remained `21:40:53Z`, while the same overdue review event reappeared at `21:47:41Z` and `22:03:30Z`; the log has no whole-suite review after `21:45:45Z`. Future runs must use the exact managed acknowledgement route and verify that it advances `review_baseline_utc`, then rescan. |
| `CODEX_EXITED` while exact process still existed | **No primary-harness defect established** | Conservative `STALE_STATUS` correctly prevented an early clean declaration and cleared once the exact identities disappeared. The observed five-second ordering race needs no lifecycle-grace change. |
| Optional watcher discontinuity | **No optional-watcher product defect established** | It completed five evaluated `defect=false` polls before the external job reaping; its absent stop record is explained by that host launch failure. |
| BYO-Firmware-MCP | **No production server defect established** | All four bounded failures were run-local/launcher/identity failures before their claimed endpoint. Do not open a server change-loop from this sprint. |

## Evidence

### Priority starvation is reproducible from the committed state and code

The Delta immutable `MANAGER_SIGNAL` was observed at `22:15:40Z` and retained in the final
snapshot.  The manager log records that it was never selected after the higher-priority
condition was acknowledged and was reviewed out of band at `22:17:44Z`.

The original explanation that this signal was filtered as a transition-only event was wrong and
is corrected here. `_TRANSITION_ONLY_TYPES` does **not** include `MANAGER_SIGNAL`; it includes
`CHECKPOINT_UPDATED` but not a manager-authored checkpoint signal. The two must not be conflated.

The actual cause is the liveness gate. A `MANAGER_SIGNAL` has priority 3 only while
`_manager_signal_is_live()` finds its lane RUNNING/WAITING/UNKNOWN, a current request, or a
running helper/MCP (`notifications.py:50-79, 139-140`). Once the lane closes, an unacknowledged
checkpoint signal has no priority and is never selected. The real final snapshot still contains
the Delta signal, but `select_actionable({signal}, final_snapshot, acknowledged=set(),
newly_observed_event_ids=set())` returns `None`.

A focused read-only function reproduction establishes the priority interaction: with a live
lane, a priority-2 `STALE_STATUS` and this priority-3 signal select the former; after acknowledging
the former, the still-live lane selects the Delta signal even with an empty `newly_observed` set.
Changing only that lane to `EXITED` makes selection return `None`. In contrast,
`CHECKPOINT_UPDATED` returns `None` with an empty `newly_observed` set and is selected only when
new, proving that transition filtering is real but was not the cause of this manager-signal loss.

The narrow repair must retain an unacknowledged manager signal that was actionable when observed
until it is selected/acknowledged, even if the producer lane closes after a higher-priority event
wins. It must continue to suppress historical signals at fresh-epoch bootstrap and must not alter
the separate transition-only behavior of `CHECKPOINT_UPDATED`.

### Launch and supervision

`CANARY_S1_CLEAN_M_MANAGER_REPORT.md` and manager log record recovery of the primary owner and
the unstarted Cygnus continuation using `CREATE_BREAKAWAY_FROM_JOB | CREATE_NO_WINDOW`.
The optional watcher service (PID `174288`) has five evaluated false polls through `21:52:00Z`,
then ends without `STOP_REQUESTED` or `SERVICE_STOPPED`; this matches the same external reaping,
not an evaluator decision. The recovered primary runtime records `stop-requested` at
`22:18:17Z` for owner `166056` / watcher `194608`.

The review record is independently inconsistent with the stated procedure: active-management
history still stores `review_baseline_utc: 2026-07-31T21:40:53.579941Z`, and events show the
same `MANAGER_REVIEW_DUE` event at `21:47:41Z` and `22:03:30Z`. The log contains exact
whole-suite reviews at `21:40:53Z` and `21:45:45Z`, but none for those later overdue sightings.
Whether the acknowledgement was bypassed operationally or overwritten is not resolved here; it
is a manager procedure failure, not evidence for an additional harness-code repair.

### Endpoints, retries, and cleanup

None of the four counting endpoints was met. Evidence agrees with the noncounting report:

- Atlas cleanup records no board action, no B14 request, no retry, and all owned PIDs absent.
- Boreal's sole provider attempt never obtained the expected provider identity; it stopped before
  public MCP/setup/UART/breakpoint work, with exact identities absent and no retry.
- Cygnus performed one no-flash/no-RF attempt, failed before a public MCP artifact, and both
  paired roots passed delayed-absence checks.
- Delta reached only the initialize artifact, then rejected invalid CIM `ProcessId` before
  lifetime/setup/request/board/UART/counter work; its cleanup shows no provider process and no
  retry.

No incomplete lane created `RESULT.json`. Current process inspection found no matching Clean-M
process and confirmed known optional/primary PIDs `174288`, `166056`, and `194608` absent.

## Required next actions

1. Treat the primary priority-starvation repair as a planned, adversarially reviewed, narrowly
   tested harness change before another counting sprint.
2. Make the breakaway launch contract durable manager infrastructure, apply it uniformly, and
   test survival past the transient invoking shell.
3. Before a successor is eligible to count, prove exact management acknowledgements advance the
   review baseline and produce a logged whole-suite review/rescan at every due interval.
