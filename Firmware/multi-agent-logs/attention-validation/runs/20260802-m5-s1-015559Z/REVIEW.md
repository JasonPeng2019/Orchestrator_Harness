# M5 Sprint 1 post-sprint result review

Scope: evidence-only review after the epoch was stopped. This review does not determine the
sprint disposition.

1. **Verified blocking-wait topology defect — repair required.** The quiet control's separate
   `watch --until-actionable` returned exit code 1 (`QUIET_CONTROL.json`) instead of the required
   `WATCH_TIMEOUT`; no worker was launched. The managed harness nevertheless committed scan 1 and
   scan 2 while the wait was active (`attention-events.jsonl`). This is consistent with the
   recorded failure that a second process tried to commit the managed scan chain. Therefore the
   production topology cannot supply a valid quiet control or wake challenge until the wait becomes
   a read-only consumer when a live managed watcher owns the root.

2. **The root repair plan correctly addresses Finding 1, with one test constraint.**
   `REPAIR_PLAN.md` is appropriately narrow: preserve standalone scanning, but make the separate
   blocking process consume only the managed owner's durable notification state and fail closed on
   invalid ownership. Its focused tests/smoke should also prove that a pending notification written
   by the managed process is returned with its exact event/wake identity, and that the consumer
   changes neither the notification file nor scan-chain/cursor/snapshot bytes. That prevents the
   repair from quietly becoming a second scanner or a hidden relay.

3. **Verified diagnostic-watcher false primary-loss evidence — add to the repair scope.** The
   watcher logged `PRIMARY_HARNESS_LOST` at `2026-08-02T01:57:46.707945+00:00` with reason
   `identity-incomplete`, although `primary-owner-identity.json` records a healthy owner and managed
   harness through normal cooperative stop. `harness_watcher_implementation/poller.py` requires
   `owner`, `managed_owner`, and `managed_watcher`, while the epoch identity file supplies only
   `owner` and `watcher`. Thus the watcher cannot truthfully verify primary-harness health in this
   topology. This is an evidence-invalidating watcher health defect, not an evaluator issue. Make
   the smallest single-schema correction (writer or reader), test healthy/absent/mismatched owner
   cases, and rerun M4 along with the harness repair.

4. **Diagnostic-only isolation otherwise held for this pre-worker epoch.** The watcher configuration
   has `evaluator_enabled: false` and an intentionally unusable evaluator command; its service log
   records diagnostic-only `EVALUATOR_SKIPPED` entries, no alert, and no evaluator child. The
   process registry records no watcher children and `evaluator_child_absent: true`. No external
   worker/controller was launched, so there is no evidence of a watcher relay, collaboration
   notification, user message, or transcript-based request discovery during the attempted control.

5. **No M5 wake conclusion is available from this epoch.** There are zero worker requests and zero
   six-stage challenge correlations. The attention report's four `INSUFFICIENT_EVIDENCE` rows are
   only lifecycle/control records, not a manager-wake result. The final `pending-notification.json`
   is empty; it cannot turn the failed quiet control into a valid timeout.

6. **Cleanup evidence is sufficient for this aborted pre-worker run.** Both service records show
   cooperative stop, the harness owner reports exit code 0, and `CLEANUP_PROOF.json` records every
   known epoch PID absent with no unexpected epoch process. The watcher attention cursor is drained
   without observation errors. This establishes safe cleanup, but does not cure Findings 1 or 3.

