# Independent watcher report — Sprint R10

## Verdict

**FAIL — counter remains 0/3.**

The watcher ran throughout epoch `20260801-attention-r10`, observed all four blocking lane gates,
successfully notified the persistent root for each, and retained a drained final cursor with no
observation errors. The sprint is nevertheless not logging-sufficient. The durable record accepts
an impossible Atlas delivery deadline, misclassifies completed on-time blocking events, and lacks
the required formal-review baseline record. R10 therefore cannot count toward the required three
consecutive sprints.

This is an instrumentation verdict, not a firmware-experiment failure and not evidence that an
idle manager missed a lane. The two measurable formal-review misses are classified as manager-busy,
not idle/absent.

## Durable runtime state

- Epoch: `20260801-attention-r10`
- Manager session: `019fbbc1-63ba-7140-ab1d-46bf412596e9`
- Manager invocation: `root-attention-r10-001`
- Final invocation record: `331a9ea7-377e-4935-8e72-7b6426d995aa`
- Final invocation snapshot: complete, empty, `ALL_LANES_BOUNDED_ENDPOINT`
- Final report generated: `2026-08-01T20:06:39.130960+00:00`
- Cursor drained: yes
- Observation errors: none
- Primary and optional watcher identities remained continuous; no watcher restart was observed.

Final classification counts were two `BUSY_MANAGER_DELAY`, two
`HARNESS_DELIVERY_DELAY`, zero `IDLE_OR_ABSENT_MANAGER_DELAY`, four
`NO_BLOCKING_IMPACT`, and 27 incidental or unresolved `INSUFFICIENT_EVIDENCE` rows. The four lane
gate rows are discussed below; unrelated scan/wait/invocation point rows must not be treated as
manager-attention outcomes.

## Blocking-event reconstruction

All timestamps below are source timestamps except the watcher-observed column.

| Lane/event | Signal created | Watcher observed | Watcher notification sent | Manager claimed | Manager response | Response deadline | Final analyzer label |
|---|---:|---:|---:|---:|---:|---:|---|
| Delta `sig-20260801-attention-r10-delta-a26-gate-001` | 19:58:50.216589 | 19:58:52.938800 | 19:59:37.769983 | 19:59:42.767759 | 19:59:43.272747 | 20:00:34.722905 | `INSUFFICIENT_EVIDENCE` |
| Boreal `sig-20260801-attention-r10-boreal-d31-gate-001` | 19:59:32.213774 | 19:59:36.303982 | 20:00:09.010500 | 20:00:12.259386 | 20:00:12.797385 | 20:01:09.0275847 | `INSUFFICIENT_EVIDENCE` |
| Cygnus `sig-20260801-attention-r10-cygnus-a24-gate-001` | 19:59:11.4255918 | 19:59:42.230670 | 20:00:09.246503 | 20:00:25.427645 | 20:00:26.115644 | 20:01:11.4255918 | `HARNESS_DELIVERY_DELAY` |
| Atlas `sig-20260801-attention-r10-atlas-a22-gate-001` | 20:00:28.113945 | 20:00:34.556439 | 20:00:47.796394 | 20:00:53.375723 | 20:00:53.834721 | 20:01:03.7334773 | `HARNESS_DELIVERY_DELAY` |

Each notification was recorded by the allowlisted subagent producer `watcher-observer` only after
successful `collaboration.send_message`, using `--metadata-file`,
`wake_transport=collaboration.send_message`, and `delivery_succeeded=true`:

- Delta: `e95030e3-c12b-4b89-aa7a-3e91f314894a`
- Boreal: `42dae821-4a07-4dbb-865d-3ea6628bf2d0`
- Cygnus: `9ea42a4d-c1bb-451c-bf70-3ef607479faf`
- Atlas: `3fb1765b-bcae-46bb-8ce2-31bc6191f349`

Every manager claim and response shown above preceded its response deadline. Delta and Boreal
nevertheless fall to `INSUFFICIENT_EVIDENCE` with “matching stage deadline and late endpoint.” An
on-time completed blocking event should be a deterministic non-impact result, not insufficient
merely because no late endpoint exists.

Cygnus is labeled `HARNESS_DELIVERY_DELAY` even though its signal was observed, notified, claimed,
responded to, and received by the agent before its `20:01:11.4255918Z` deadline. Later stale harness
deferrals continued after terminal response/resume and appear able to manufacture the delivery
label. The label has `deadline_lateness_seconds: null`, so it does not name a truthful late stage.

Atlas contains the clearest hard contradiction. Source record
`88077113-4a79-4a3f-b26d-7eabd7ac6a40` was created at `20:00:28.113945Z` but declares
`delivery_deadline_utc=19:59:13.7334773Z`, about 74.38 seconds before the signal existed. The
canonicalizer accepted this impossible deadline, the observation-error log remained empty, and the
analyzer emitted `HARNESS_DELIVERY_DELAY` with `deadline_lateness_seconds: null`. That result is not
usable causal evidence.

Notification latency from watcher observation to the notification source record was approximately
44.83 seconds (Delta), 32.71 seconds (Boreal), 27.02 seconds (Cygnus), and 13.24 seconds (Atlas).
All four notifications still preceded the relevant response deadline. These durations should remain
visible in later sprints; they must not be mistaken for manager idle time.

## Formal-review cadence

The repaired multi-interval analyzer successfully classified both late formal-review starts:

- `r10-review-001`: due `2026-08-01T19:59:20.013113Z`, started
  `2026-08-01T20:01:20.129112Z`, `BUSY_MANAGER_DELAY`, 120.961999 seconds late.
- Harness review event `83aa83985ea0f2de916f6b41f9a30ae682b179ab0019768ab03291154adb0938`:
  due `2026-08-01T19:58:52.947799Z`, started `2026-08-01T20:02:07.591658Z`,
  `BUSY_MANAGER_DELAY`, 196.677801 seconds late.

This is useful R10 evidence: the persistent manager was occupied with the concurrent lane gates and
review work rather than proven idle/absent. It is not yet an overall bridge/no-bridge verdict because
R10 fails the logging-sufficiency gate.

## Lane endpoints

All four lanes reached the bounded read-only checkpoint and exited without provider, MCP, lease, or
hardware action:

- Boreal/D31: completion signal `58c9caee-5cc8-4069-ae8d-40411e441569`, source time
  `20:02:20.863321Z`; controller exited `20:03:14.1608903Z`.
- Cygnus/A24: completion signal `2a303243-72d1-41d5-8c77-d7a6a04b6262`, source time
  `20:01:30.6981624Z`; controller exited `20:03:41.2485335Z`.
- Atlas/A22: completion signal `88682f26-e39f-46c1-9c9a-c08bdd550e6c`, source time
  `20:04:09.486457Z`; controller exited `20:04:56.7372195Z`.
- Delta/A26: completion signal `f4f97d9c-9369-48ac-a528-33fd818668b1`, source time
  `20:05:37.690095Z`; controller exited `20:05:58.2297469Z`.

## Seven-gate audit

1. **PASS — continuous identities.** Primary harness and optional watcher coverage remained live
   without an unexplained restart.
2. **PASS — durable watcher state.** The final cursor is drained, the observation-error list is
   empty, and no partial backlog was reported.
3. **FAIL — stable truthful end-to-end correlation.** IDs join, but Atlas's impossible deadline was
   accepted as valid causal data, and resolved events continued to receive post-terminal deferrals.
4. **FAIL — deterministic causal/non-impact outcomes.** Delta and Boreal completed on time but are
   `INSUFFICIENT_EVIDENCE`; Cygnus and Atlas have unsupported delivery labels with null lateness.
5. **PASS — explicit activity pairing.** The four manager wait intervals are paired, continuity
   links are present at the relevant transitions, and no contradictory manager activity is reported.
6. **FAIL — required snapshots/baseline.** Invocation start/end snapshots are complete, but there is
   no canonical `FORMAL_REVIEW_BASELINE_ADVANCED` record, and the first harness pending snapshot for
   Delta is explicitly incomplete/unknown.
7. **FAIL — independent reconstruction.** The durable timeline can reconstruct timestamps, but it
   cannot support the analyzer's Atlas/Cygnus delivery labels or turn both on-time completions into a
   stable non-impact result.

Therefore the sprint does not count and the sequence remains **0/3**.

## Smallest required repair

1. Validate temporal ordering at source-record creation and canonicalization. A delivery or response
   deadline earlier than its signal creation timestamp must fail closed and become durable
   insufficient/observation-error evidence; it must never produce a causal delay label.
2. Make a completed, on-time blocking chain deterministic: successful notification plus on-time
   manager claim/response and terminal agent receipt/resume should classify
   `NO_BLOCKING_IMPACT`, not `INSUFFICIENT_EVIDENCE` for lack of a late endpoint.
3. Emit `HARNESS_DELIVERY_DELAY` only when a specific valid stage deadline and a specific late
   endpoint are present. The selected outcome must carry non-null `deadline_lateness_seconds` and
   cite those records.
4. Stop or neutralize exact-event harness pending/deferred emissions after terminal manager response
   plus agent receipt/resume. A later stale scan must not override an already completed on-time chain.
5. Require and verify `FORMAL_REVIEW_BASELINE_ADVANCED` with a bounded complete snapshot before a
   sprint can pass; event-selection snapshots must not remain unknown at acceptance.
6. Add focused regressions reproducing the exact Atlas impossible deadline, the Cygnus post-terminal
   stale-deferral shape, and the Delta/Boreal on-time-no-late-endpoint shape. Then rerun a fresh
   metadata-file readiness case before starting the next counted epoch.

