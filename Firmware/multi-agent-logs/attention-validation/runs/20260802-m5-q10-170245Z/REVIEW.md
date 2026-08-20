# Q10 post-sprint review (advisory)

## Gate findings

- **HARNESS_PASS.** The native managed harness observed all four Q10 HELP signals, selected and returned each through the direct blocking wait (`wait-001`--`004`), and successfully acknowledged their returned harness event IDs. No harness stderr error or verified discovery, liveness, queue, or transport defect is present. The broken end-to-end causal record below is a root recorder/identity error, not evidence that the harness misdelivered.
- **WATCHER_PASS.** The watcher was diagnostic-only (`evaluator_enabled: false`), remained ready until intentional stop, had `cursor_drained: true`, reported no alert, and fail-closed each affected request as `INSUFFICIENT_EVIDENCE`. Its result is correct for the evidence supplied; no watcher defect is established.
- **MANAGER_EVIDENCE_INSUFFICIENT.** None of the four genuine requests has an exact native-wait -> root-receipt -> claim/response -> worker-receipt/resume chain. Thus the run cannot distinguish manager attention, delivery, and downstream worker handling as required.

## Exact failure and classification

The native waits returned harness event IDs:

| lane | native wait event ID | root recorded as wait/claim event ID |
|---|---|---|
| Delta | `e6fa6e...905cf4a0` | `sig-...-delta-a26-gate-001` |
| Cygnus | `f16746...92a7c081` | `sig-...-cygnus-a24-gate-001` |
| Atlas | `9fe704...4472198b` | `sig-...-atlas-a22-gate-001` |
| Boreal | `2241b6...641e5495` | `sig-...-boreal-d31-gate-001` |

The root substituted each source `signal_id` for the returned harness `event_id` while recording `MANAGER_WAIT_FINISHED`, `MANAGER_WAKE_RECEIVED`, and `MANAGER_EVENT_CLAIMED`. The claim snapshots consequently select the substituted ID, not the exact event returned by that wait. This is the direct cause of finalizer failure: **`manager claim requires its own exact complete event-selection snapshot`**.

This same identity substitution makes the watcher correctly report **"manager acted before wake receipt"**: the native `MANAGER_WAKE_DELIVERED` records are keyed by the harness IDs, whereas the root action records are keyed by `sig-*`; they cannot be correlated. The missing worker receipt/resume is also correctly fail-closed: all four acknowledgement artifacts say `watcher_received: false`. These are root/operator record-order/identity failures (and absent worker receipt/resume evidence), **not watcher-code defects** and not a basis to call a harness bug.

## Controls, assistance, drain

- **Quiet control: not valid as a clean quiet control.** It surfaced four Q9 `STALE_STATUS` action-required events before the final timeout. The final wait did time out, but the control did not begin from a quiet/drained signal surface.
- **Busy control: valid as a bounded activity record only.** `busy-manager-control-001` is paired and gap-free from `17:07:51.723Z` to `17:08:46.543Z` (55.34 s, hash audit PASS). It does not causally cover the later complete request intervals.
- **Forbidden external assistance: none evidenced.** Preflight records the allowed topology, `forbidden_runtime_absent: true`, and disabled evaluator; evidence shows one harness, one diagnostic-only watcher, and four allowed external controllers/Codex workers. No relay, wrapper, evaluator, or external discovery path is evidenced.
- **Drain/cleanup: exact.** Watcher stopped on request after final polls; managed harness stop was requested `17:24:10.416Z` and exited `17:24:16.776Z`; post-cleanup at `17:25:19.023Z` found all 11 registered PIDs absent, no active resources, no leases, tokens, or conflicts.

## Timing

The raw created-to-root-action spans exceed 90 seconds (Delta ~125 s, Cygnus ~138 s, Atlas ~132 s, Boreal ~163 s), but they do **not** have gap-free causal attribution. The only busy interval is short and ends before later request handling; the substituted IDs and missing worker receipts sever each genuine chain. Do not treat any >90-second span as excused by manager work or native waiting.

## Smallest corrections (between sprints only)

1. In the root recording procedure, copy the exact `event_id` from each native wait stdout into *every* matching wait-finished, wake-received, claim snapshot/selection, decision, response, and acknowledgement record; keep source `signal_id` only as a separate field.
2. Require a worker-side receipt/resume record keyed to that same exact harness event ID before classifying a request.
3. Drain or explicitly scope out pre-existing actionable statuses before running the quiet control; then require its first wait to time out cleanly.
4. No watcher or harness behavior change is supported by this evidence.
