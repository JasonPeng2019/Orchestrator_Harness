# M5 Q8 post-sprint review

**Epoch:** `20260802-m5-q8-152800Z`  
**Scope:** post-stop evidence review only. No code or runtime evidence was modified. The three
Boreal convenience `meta/stdout` files reconstructed by root are not used for the findings below;
canonical producer timeline records and the harness log are the basis.

## Evidence reviewed

- `harness_watcher/20260802-m5-q8-152800Z/watcher/attention-{timeline,report}.jsonl/json`
  and `service.json`;
- `multi-agent-logs/orchestrator-harness/20260802-m5-q8-152800Z/attention-events.jsonl`;
- this run's native wait/claim/response/ack artefacts, preflight, isolation, controls, and cleanup
  records; and
- worker-origin records copied under the epoch's watcher inputs.

The watcher was live from `15:29:08Z` to its intentional stop at `15:38:40Z`, had
`evaluator_enabled: false`, reported `cursor_drained: true`, and recorded no observation errors.
The managed harness stderr is empty. Finalization reports 183 records and `PASS`; all ten
registered epoch processes are absent and resource cleanup reports a safe boundary.

## Controls and isolation

- Quiet native wait: recorded `15:29:55Z`–`15:30:09Z`, ending in the expected `WATCH_TIMEOUT`.
- Busy-manager control: paired `MANAGER_TOOL_STARTED`/`FINISHED` at
  `15:30:54Z`–`15:31:49Z` with the declared `RUNNING_TOOL` state.
- Preflight records attempt **8/10**, frozen Python/policy baselines matching, and a safe starting
  boundary.
- `ISOLATION.json` records native blocking-harness wait as the only request-discovery path and
  records no runner, wrapper, relay, watcher subagent/evaluator, collaboration notification,
  transcript, or user-message discovery. The process inventory is consistent with the permitted
  root, harness, diagnostic watcher, and four external E2E worker/controller lanes.

## Genuine request chains

All four worker lanes have durable origin, native harness, wake, root receipt/claim, response,
acknowledgement, worker receipt, and work-resume records. Wake delivery and root receipt are
separate timestamps; root receipt-to-claim is about 0.59–0.61 s in each chain.

| Lane | Key source-time chain (UTC) | Watcher label / review classification | Finding |
|---|---|---|---|
| Delta A26 | created 15:32:10.802; observed/actionable 15:32:35.501; delivered 15:32:39.743; received 15:32:42.459; claimed 15:32:43.043; resumed 15:33:30.440 | `NO_BLOCKING_IMPACT` / **Healthy** | Complete six-stage chain, within its delivery target. |
| Atlas A22 | created 15:32:05.403; observed 15:32:58.822; actionable 15:33:22.357; delivered 15:33:36.177; received 15:33:38.854; claimed 15:33:39.461; resumed 15:34:20.122 | `HARNESS_DELIVERY_DELAY` / **Unclassifiable causal delay** | The 26.0-s deadline lateness is real, but canonical evidence lacks the timestamp at which the worker atomically exposed the final signal. The 53.4-s created-to-observed gap therefore cannot be attributed specifically to the harness rather than delayed worker publication. |
| Cygnus A24 | created 15:32:28.839; observed 15:32:58.822; actionable 15:34:02.778; delivered 15:34:13.706; received 15:34:16.120; claimed 15:34:16.710; resumed 15:35:49.459 | `BUSY_MANAGER_DELAY` / **Busy-manager contention** | Complete chain. It crossed the delivery target by 40.7 s; the recorded intervening root response/claim handling supplies a bounded competing-work explanation, not idle-manager inattention. |
| Boreal D31 | created 15:33:46.751; observed 15:34:02.778; actionable 15:34:51.238; delivered 15:34:55.933; received 15:34:58.581; claimed 15:34:59.169; resumed 15:35:45.890 | `HARNESS_DELIVERY_DELAY` / **Unclassifiable causal delay** | The 23.5-s deadline lateness is real. As with Atlas, there is no durable final-publication stage, so the watcher cannot truthfully attribute the 16.0-s created-to-observed segment to the harness. |

The Atlas and Boreal worker records also show that `AGENT_WAIT_STARTED` was not immediate after
`AGENT_SIGNAL_CREATED` (about 30.0 s and 22.1 s respectively). This is a worker/procedure
observation, not proof that the native harness delayed a signal after it was exposed.

## Gates (advice to root)

- **Harness — `HARNESS_PASS` advised.** Every actually observed signal was selected through the
  native wait, correlated, claimed, answered, and acknowledged without crash, loss, stale
  identity, queue corruption, or transport failure. The two late rows do not prove an in-scope
  harness defect because final-signal exposure is unrecorded.
- **Watcher — `WATCHER_BUG` advised.** Its reported `HARNESS_DELIVERY_DELAY` labels for Atlas and
  Boreal make a component-causal attribution that the available sources cannot establish. The
  watcher has the required worker-origin timestamp and harness-observation timestamp, but no
  durable final-publication timestamp between them. It should fail closed as insufficient causal
  evidence rather than call that segment a harness delay. This is a diagnostic-accuracy defect,
  not a runtime health or notification defect.
- **Manager evidence — `MANAGER_EVIDENCE_INSUFFICIENT` advised.** There are four genuine, complete
  chains across four lanes plus valid quiet/busy controls, and none shows idle-manager
  inattention after delivery: receipt followed within roughly 2.4–2.7 s and claim within roughly
  0.6 s. However, the missing publication stage leaves Atlas/Boreal causal classification
  unresolved and makes the evidence set insufficient for the required architecture verdict.

Thus I advise that Q8 not enter the comparable qualifying set. This is not a claim that a
`codex exec` bridge is justified: the delivered-to-received/claim evidence instead weighs against
an idle persistent-manager problem for the observable portions of this sprint.

## Minimal verified repair direction

Add a **passive, durable worker final-signal-publication stage/timestamp** correlated to the same
signal ID, and make watcher classification fail closed until that stage exists. Do not add any wake
or runtime assistance. Re-test the new passive chronology and refreeze before a later attempt.

This report advises only; root decides disposition and repair scope.
