# Q9 post-sprint review (advisory)

Reviewed after shutdown. This is an evidence review only; root retains the decision.

## Recommendation

| Independent gate | Recommendation | Basis |
|---|---|---|
| Harness | **HARNESS_PASS** | The four controller processes died immediately, leaving orphan Codex children. The harness correctly marked those lanes `STALE_STATUS`; their signals then failed the harness liveness predicate (`_manager_signal_is_live`) and were deliberately not actionable. Observation without actionability is expected for a non-live producer, not stale queue selection or a native delivery failure. |
| Watcher | **WATCHER_BUG** | The watcher accurately captured the raw source records, but its final report calls all four non-live signals `HARNESS_DELIVERY_DELAY`. That attribution is false: no live actionable request existed, and the harness correctly declined them. The report should fail closed as insufficient/non-live evidence, not diagnose harness delivery delay. |
| Manager architecture evidence | **MANAGER_EVIDENCE_INSUFFICIENT** | There are zero classifiable Q9 native delivery chains. Therefore the evidence cannot distinguish successful delivery plus idle inattention, genuine busy contention, or downstream response failure. It provides no usable basis for a `codex exec` bridge decision. |

**Recommended disposition: `WATCHER_BUG`** (and, independently, manager evidence insufficient; not qualifying). `FINALIZE_VALIDATION.json` independently fails because Delta lacks receipt/resume or a terminal expiration.

## Causal findings

### Controller/worker-liveness failure; no verified native harness failure

The intended Q9 gate signals were real blocked `HELP` signals from four distinct worker lanes. Each has the prescribed `AGENT_SIGNAL_CREATED` -> `AGENT_SIGNAL_PUBLISHED` -> `AGENT_WAIT_STARTED` publication evidence with distinct recorder IDs in `watcher/attention-timeline.jsonl`:

| Lane | Publication UTC | Harness observed UTC | Outcome |
|---|---:|---:|---|
| Delta/A26 | 16:11:25.3599135Z | 16:11:46.395234Z | Observed before its 16:11:58.1820127Z delivery deadline; never actionable. |
| Cygnus/A24 | 16:11:44.3142392Z | 16:12:10.762727Z | Observed before its 16:12:22.2132301Z deadline; never actionable. |
| Atlas/A22 | 16:15:05.4948547Z | 16:15:23.370602Z | Observed after its 16:15:15.2287434Z deadline; never actionable. |
| Boreal/D31 | 16:16:08.7786041Z | 16:16:24.601261Z | Observed before its 16:16:27.7253067Z deadline; never actionable. |

All four worker-controller PIDs terminated immediately while their Codex children remained orphaned. The harness final scan correctly records the resulting lane condition as `STALE_STATUS` (terminal `turn.completed` contradicts each persisted `RUNNING_CODEX` status). Under this condition `_manager_signal_is_live` returned false. The harness therefore observed the final ordinary signal files, but properly did **not** make them actionable or emit a Q9 native-wake chain. Its 13 wake sequences are for other eligible events and do not establish a Q9 delivery failure. This is not manager idling: the manager did not receive a native stdout wake for any live Q9 request.

The direct cause is controller/worker setup failure: the required controller lifetime ended, so no Q9 producer was live when selection was evaluated. This excludes these rows from a delivery/manager sample. The old eligible events explain what the manager did next, but are not evidence that the harness mis-selected a live Q9 event. The four workers' publication sequencing is not the cause.

### Verified watcher attribution defect

The canonical watcher report nevertheless labels all four Q9 rows `HARNESS_DELIVERY_DELAY`. This is a component-owned diagnostic attribution error, not an expected outcome: the evidence establishes non-live producer state and absence of actionability, so a harness-delay label asserts a cause contradicted by the native liveness gate. A conservative `INSUFFICIENT_EVIDENCE`/non-live result would preserve the observation without falsely implicating the harness. Thus raw watcher ingestion/cursor health passes, but the watcher gate fails on report accuracy.

### No valid busy or idle conclusion

`BUSY_MANAGER_RESOURCE_AUDIT.json` proves one 55.009-second genuine bounded audit (16:09:53.821973Z–16:10:48.830778Z). It ended before Delta created/published its Q9 signal, and the Q9 signals had no native delivery chains. It therefore is neither a busy-contention explanation nor an idle-manager-inattention sample. The repeated manager receipt records apply to old selected events, not the four Q9 signals.

## Publication and passive-topology assessment

The Q9 source records support passive publication evidence: all four signals have creation, captured publication, and wait-start records; the final ordinary JSONs were observed by the harness; the watcher merely recorded/canonicalized them. No `WATCHER_NOTIFICATION_SENT` record or evaluator activity appears in the Q9 path. They were never actionable because their controllers were no longer live, not because publication was missing, the harness failed, or the watcher failed to observe them. This is not a reason to add a relay, wake helper, or other assistance layer.

## Watcher, drain, and cleanup

`attention-report.json` records `cursor_drained: true`, an empty `observation_errors` list, and complete trusted coverage of all four subagent attention inputs, the orchestrator input, and the harness attention source (all generation 1, zero partial bytes/error). `WATCHER_PRESTOP_STATUS.json` records `evaluator_enabled: false`, `stop_requested: true`, and `exit_reason: stop-requested`; the service stopped at 16:32:41Z. Its events are consistently diagnostic-only (`EVALUATOR_SKIPPED`, `evaluated:false`).

`PROCESS_CLEANUP.json` verifies all 11 registered processes absent and no active resources; `RESOURCE_CLEANUP.json` verifies no active leases. These support a completed safe post-sprint boundary and make this review timely.

## Evidence reviewed

- `goal.md`; `AGENTS.md`; active M5 specifications/checklist; `harness_watcher_implementation/ATTENTION_LOGGING.md`
- Q9 `PREFLIGHT.json`, `INFRASTRUCTURE_START.json`, `BUSY_MANAGER_RESOURCE_AUDIT.json`, `FINALIZE_VALIDATION.json`, `WATCHER_PRESTOP_STATUS.json`, cleanup records, and wait/checkpoint artifacts
- `harness_watcher/20260802-m5-q9-160750Z/watcher/attention-timeline.jsonl`, `attention-report.json`, watcher event/cursor state
- `multi-agent-logs/orchestrator-harness/20260802-m5-q9-160750Z/{events.jsonl,attention-events.jsonl}`
