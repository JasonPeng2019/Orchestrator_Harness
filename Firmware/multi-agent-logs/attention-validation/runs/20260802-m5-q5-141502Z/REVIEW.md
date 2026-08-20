# Q5 post-sprint advisory review

**Epoch:** `20260802-m5-q5-141502Z`  
**Recommendation:** `HARNESS_BUG`, `WATCHER_PASS`, `MANAGER_EVIDENCE_INSUFFICIENT`; **not qualifying**.

Root additionally confirmed that a user-message/turn resumption influenced manager attention during
the live window. That forbidden discovery/attention assistance independently contaminates Q5; the
`ISOLATION.json` declaration is therefore not sufficient evidence of isolation.

## What worked

- The quiet control timed out normally. Four real external lanes ran, all four received the
  published response and recorded useful-work resume.
- The watcher stayed live, diagnostic-only (`evaluator_enabled: false`), drained its cursor, and
  stopped normally. It reported the contradictory/missing timing evidence rather than hiding it.
- No runner, wrapper, relay, watcher subagent, or evaluator is evidenced. Cleanup reports all 10
  registered processes gone and an empty host-only resource boundary. The user-message/turn
  resumption finding above means the discovery-isolation claim is false for this attempt.

## Verified native-harness defects

1. **Temporary signal files are treated as real signals.** Boreal's one logical signal
   `sig-...-boreal-d31-gate-001` was ingested twice: first from
   `.sig-...tmp.json` as harness event `0eb474...`, then from the final `.json` file as
   `7f0865...`. The two paths and IDs are preserved in
   `multi-agent-logs/orchestrator-harness/<epoch>/events.jsonl`. Only the final event was
   acknowledged; the temporary-file event remained pending at invocation finish. This is a real
   duplicate/queue-correlation defect, not a worker mistake.
2. **Checkpoint wake delivery is recorded before actual delivery to the manager.** The Cygnus
   checkpoint became actionable at `14:17:55`; the root entered native wait at `14:18:04`; the
   harness recorded wake attempted/delivered at `14:18:06`; but the root did not receive the
   returned event until `14:20:48`. The `MANAGER_WAKE_DELIVERED` timestamp therefore does not mean
   actual delivery, contrary to the six-stage contract. The checkpoint also preempted the genuine
   requests while the wait remained blocked. This is a native wake/logging defect; the raw
   `attention-events.jsonl`, `wait-001-output.json`, and root attention timeline establish it.

These defects make the harness gate fail and make this attempt unsuitable for architecture
conclusions. They should be repaired between sprints; do not compensate with a wrapper or relay.

## Manager evidence

All four genuine requests have a response/worker-resume record, but none is classifiable under the
required causal standard. The watcher report records `INSUFFICIENT_EVIDENCE` for Atlas and Cygnus
(missing complete manager-interval chains), Boreal (source observation precedes source record and
wake contradiction caused by the temporary-file duplicate), and Delta (negative deferral metric).
Thus Q5 has fewer than three classifiable lanes and cannot decide idle-manager inattention versus
busy-manager contention.

## Smallest justified next step

Root should write a narrow harness/wake-logging repair plan: ignore non-final temporary signal
files (or deduplicate by stable signal identity) and ensure `WAKE_DELIVERED` is emitted only when
the native wait actually returns to the manager. Then use the prescribed coder/reviewer/Luna smoke
loop, refreeze the surface, and restart the comparable three-sprint count.

This is advice only; root decides disposition and repair scope.
