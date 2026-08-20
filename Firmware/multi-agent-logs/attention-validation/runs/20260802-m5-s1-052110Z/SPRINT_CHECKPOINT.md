# M5 sprint checkpoint — 20260802-m5-s1-052110Z

## Root disposition

**RESET — accepted count remains 0/3.**

This attempt directly exercised the native production harness and standalone diagnostic watcher,
with four external E2E worker lanes and no runner, wrapper, relay, evaluator, watcher subagent,
transcript-discovery path, or collaboration notification. The raw evidence shows four complete,
on-time six-stage wake chains. The sprint nevertheless cannot count because the diagnostic watcher
reported impossible negative causal durations without identifying contradictory evidence.

## Challenge result

The authoritative machine-readable table is `CHALLENGES.json`.

| Worker | Control | Six stages ordered | Response before deadline |
|---|---|---:|---:|
| Atlas/A22 | waiting manager | yes | yes |
| Boreal/D31 | waiting manager | yes | yes |
| Cygnus/A24 | waiting manager | yes | yes |
| Delta/A26 | busy manager | yes | yes |

The raw production chains support harness observation, wake attempt, delivery, root receipt, root
claim, response publication, worker receipt/resume, and exact acknowledgement. The native sprint
finalizer also passed. These facts are diagnostic evidence only; they do not override the reset.

## Controls and health

- Quiet control: valid `WATCH_TIMEOUT`, no wake identity or claim.
- Busy control: Delta's genuine request arose inside the recorded bounded manager audit interval.
- Harness: one native managed process, orderly scans/wakes/acks, no crash or restart, empty final
  pending notification, cooperative stop.
- Watcher runtime: diagnostic-only, no evaluator/notifier child, trusted error-free coverage,
  drained cursor, cooperative stop.
- Isolation: request discovery used only blocking harness wait output. No forbidden runtime role or
  notification path influenced discovery.
- Cleanup: all recorded sprint processes were absent by PID and creation identity; no lease,
  provider, MCP, or hardware lifetime remained.
- Freeze: Python source fingerprint and every sealed input matched after cleanup.
- Firmware/E2E results were workload only and did not affect this disposition.

## Reviewer findings and root audit

1. **Accepted — watcher causal metrics are materially false.** The final watcher report contains
   Cygnus `signal_to_observation_seconds = -14.808474` and negative
   `response_to_ack_seconds` for Atlas, Cygnus, and Delta while `contradictory_evidence` is empty.
   Raw source timestamps show valid positive ordering. Code inspection confirms `_duration` uses
   watcher observation time, so cross-source ingestion order leaks into causal metrics. Repair is
   required before another counted sprint.
2. **Accepted as a procedure correction — normalized request deadlines.** Boreal, Cygnus, and
   Delta worker requests left native `deadline_utc` null even though their worker attention records
   retained real response deadlines. This is not a demonstrated harness data-loss bug, but the next
   prompts/checklist must require the exact request-schema field so every layer retains it.
3. **Accepted as a procedure correction — final boundary order.** The root emitted invocation
   finish after stopping the watcher and used a final native one-shot poll after cleanup; the
   reviewer was launched before that last poll finished, although it was told not to finalize.
   The next sprint must finish invocation, drain, stop, prove cleanup, and only then launch review.
4. **Accepted as a procedure correction — timeout wait pairing.** `drain-wake-010` has a wait-start
   record but no wait-finished record after `WATCH_TIMEOUT`. Every wait outcome must be paired next
   sprint. No late record was fabricated for this attempt.
5. **Accepted — raw chains, controls, runtime isolation, freeze, and cleanup otherwise pass.** The
   review's positive findings were independently checked against the timeline, reports, process
   registry, and sealed hashes.

## Smallest response and next action

Apply `active-working-spec/m5-watcher-causal-metrics-repair.md`: use source timestamps for reported
causal durations and fail closed on any truly negative causal interval. After independent review,
Luna smoke, affected full tests, and M4 readiness, refreeze and start a new S1 epoch at 0/3. The
three root procedure corrections above require no harness support layer and no production-code
change.
