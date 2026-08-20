# Independent watcher report — 20260801-attention-r9

**Verdict: FAIL — logging-insufficient; this epoch is not counted.**

**Counter effect:** R9 cannot become sprint 1 of 3. The consecutive count remains
`0/3`; a logging repair and a fresh successor epoch are required before a counted
sprint can start. This epoch supplies no verdict for either the persistent manager
or a `codex exec` bridge.

## Coverage that did pass

- During live observation, the exact primary and optional watcher identities remained
  live. The optional watcher started `READY`.
- The final `attention-report.json` says `cursor_drained: true` and has no
  `observation_errors`.
- The independent watcher forwarded each of the three durable blocking signals once
  and, after each successful send, wrote the exact-event
  `WATCHER_NOTIFICATION_SENT` record with the required provenance.

Those health checks do **not** make the causal evidence sufficient.

## Exact blocking-signal timing

All timestamps below are host UTC source timestamps unless marked *canonical
observed*. The cited source records are in the canonical attention timeline.

| Lane/event | Signal / response deadline | Durable successful notification | Manager claim / response | Analyzer result and assessment |
| --- | --- | --- | --- | --- |
| Cygnus / `sig-20260801-attention-r9-cygnus-a24-gate-001` (signal `9f448808-e64d-4217-ab40-0f318c6e391e`) | Signal `19:20:20.5241495`; deadline `19:22:20.5241495` | Notification `3bf063aa-418d-48a1-aa15-2a05c34c8cda`: `19:22:33.061089` (**12.537 s after** deadline); canonical observed `19:22:45.273213` (**24.749 s after**). | Wait finished `19:22:07.436944`; claim `19:22:07.652942`; response `19:22:21.674776` (**1.151 s after** deadline). | `INSUFFICIENT_EVIDENCE`. The claim/response precede the durable notification record, so this record set cannot prove timely successful notification to the manager. It must not be attributed to manager idleness or busyness. |
| Atlas / `sig-20260801-attention-r9-atlas-help-001` (signal `322ba852-2dc9-44b4-8fc3-45c30b174ac1`) | Signal `19:21:25.529934`; deadline `19:22:58.6555648` | Notification `f2110615-1596-4ec3-bcff-4df57f621ca7`: `19:22:43.526599` (**15.129 s before**); canonical observed `19:22:45.273213`. | Claim `19:22:49.883972`; response `19:22:50.349884` (**8.306 s before** deadline). Agent receipt/resume source time `19:23:15.532331` / `19:23:15.754333`. | `HARNESS_DELIVERY_DELAY`, with 119.339080 s explicitly blocked and 37.719231 s canonical response-to-receipt. It is not a busy-manager or idle-manager classification. |
| Boreal / `29b1ca25-9b40-469b-82e7-23f2274aa04e` (signal `3e81e177-2f55-442f-ac33-3ab5898a993e`) | Signal `19:21:50.178429`; deadline `19:23:25.8469336` | Notification `5ad3a6b3-cd34-48b2-a3e1-14034d89ce7f`: `19:23:26.135609` (**0.289 s after**); canonical observed `19:23:28.910148` (**3.063 s after**). | Claim `19:23:33.765341`; response `19:23:51.158363`; agent receipt `19:24:21.898938`. No matching `AGENT_WORK_RESUMED` was recorded. | `HARNESS_DELIVERY_DELAY`, with truthful 3.063215 s deadline lateness and 30.832897 s canonical response-to-receipt. Timely notification was not proven, so this cannot be used to blame manager state. |

### What Atlas and Boreal do — and do not — distinguish

The analyzer distinguishes these two events from a **manager-state** delay: both are
classified `HARNESS_DELIVERY_DELAY`, not `BUSY_MANAGER_DELAY` or
`IDLE_OR_ABSENT_MANAGER_DELAY`. That is the correct direction of attribution under
Repair 008-A when the notification/delivery boundary itself is late or otherwise the
causal limiting step.

It does **not** establish that the manager was busy, and it does not establish that
the manager was idle. Atlas also shows a timely notification and timely manager
response but a slow downstream receipt/resume path; Boreal's notification itself is
late. They are different delivery-path failures, not evidence for the wake-bridge
question.

## Formal-review cadence: real lateness, no usable classification

The original orchestrator producer records contain `formal_review_due_utc`, but the
canonical events retain it only as an auxiliary field. The analyzer treats every
`r9-review-*` event as `INSUFFICIENT_EVIDENCE` with `matching stage deadline and late
endpoint` missing; it does not evaluate `formal_review_due_utc` as a review deadline.

| Review | Declared due UTC | Review-start UTC | Start minus due | Analyzer |
| --- | --- | --- | ---: | --- |
| `r9-review-001` | `19:22:16.733044` | `19:24:07.976102` | +111.243058 s | `INSUFFICIENT_EVIDENCE` |
| `r9-review-002` | `19:27:37.608997` | `19:27:42.611925` | +5.002928 s | `INSUFFICIENT_EVIDENCE` |
| `r9-review-003` | `19:31:24.764653` | `19:31:30.286186` | +5.521533 s | `INSUFFICIENT_EVIDENCE` |
| `r9-review-004` | `19:34:12.768660` | `19:34:40.915326` | +28.146666 s | `INSUFFICIENT_EVIDENCE` |
| `r9-review-005` | `19:41:05.8614828` | `19:38:46.146508` | −139.714975 s | `INSUFFICIENT_EVIDENCE` |

Thus four records declare a late review start, but the experiment cannot classify
the cause. There are no `HANDLING_OTHER_EVENT` intervals at all. The timeline shows
discrete Cygnus, Atlas, and Boreal work during the first missed review interval, but
not an explicit continuous busy interval. Silence cannot fill that gap. This is not
evidence of idleness, and it is not evidence of continuous busyness; it is missing
causal instrumentation.

## Delta A26 pre-gate timeout

Delta's controller did run (`CONTROLLER_ACTIVE` at `19:33:50.498267`) and later
exited (`CONTROLLER_EXITED` at `19:40:05.933854`). However, Delta produced no R9
attention producer stream, blocking signal, manager request, lease, runtime, or MCP
lifetime. `FORMAL_REVIEW_005.md` truthfully calls this a pre-gate controller timeout.

That is a real endpoint, not a Delta manager-attention challenge. It cannot prove a
manager response path, and it leaves the required per-lane producer-liveness/event
inventory incomplete.

## Seven-gate sufficiency assessment

| Gate | Result | Independent basis |
| --- | --- | --- |
| 1. Continuous primary/optional identity coverage | PASS | Exact identities remained live while observed; optional service was `READY`; no watcher-loss report occurred before the declared close. |
| 2. Drained, clean watcher cursor | PASS | Final report: `cursor_drained: true`, zero observation errors. |
| 3. End-to-end correlation for every manager-relevant signal and formal-review due event | FAIL | Delta has no attention producer stream; Boreal lacks `AGENT_WORK_RESUMED`; formal review events lack a canonical deadline/late-endpoint join usable by the analyzer. |
| 4. Every late completed event causally classified, never `INSUFFICIENT_EVIDENCE` | FAIL | Cygnus and all five formal-review events are `INSUFFICIENT_EVIDENCE`; 38 report events total have that classification. |
| 5. Paired manager intervals with no contradictory activity over the deadline | FAIL | Waits are paired, but no `HANDLING_OTHER_EVENT` coverage exists for the late formal-review intervals; notification/claim order is not provable for Cygnus. |
| 6. Bounded pending snapshots at start/end, selection, and formal-baseline advance | FAIL | Invocation start/end have snapshots, but the three claims and all review/checkpoint records have no `pending_work_snapshot`. |
| 7. Independent watcher can reconstruct the same complete pending/response-delay table | FAIL | I can reconstruct the raw timings and analyzer output, but cannot reconstruct causal manager state for Cygnus/formal reviews or a Delta attention path from durable records alone. |

The required non-vacuous formal-review challenge is therefore not accepted, and the
required wake challenge cannot support a manager-state conclusion. R9 must be treated
as **logging-insufficient**, not as evidence that a persistent manager is sufficient
and not as evidence that `codex exec` is required.
