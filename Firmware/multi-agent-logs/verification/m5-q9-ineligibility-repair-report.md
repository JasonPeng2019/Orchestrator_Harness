# M5 Q9 passive ineligibility-evidence repair

## Result

**PASS.** Q9 exposed a watcher attribution bug, not a native harness selection bug. When a worker
controller had already died, the harness correctly observed but did not make its later signal
actionable; the watcher incorrectly called that a harness delivery delay.

## Repair

- Native harness emits one passive `HARNESS_EVENT_INELIGIBLE` after observing an intentionally
  ineligible manager signal.
- Reasons are truthful and bounded: `ALREADY_ANSWERED`, `INVALID_LANE_ID`, `LANE_NOT_LIVE`.
- The record does not alter liveness, admission, pending state, scheduling, selection, or wake.
- Watcher accepts only one exact-event/exact-harness-event, post-observation, harness-provenance,
  supported reason with no actionable contradiction; otherwise it cannot suppress a supported
  delivery-delay diagnosis.

## Independent checks

- Terra coder: implementation plus focused/full tests.
- Terra reviewer: found false reason collapsing; root accepted it; coder corrected it; re-review
  PASS.
- Luna-high/default practical smoke: native non-live scan, analyzer, live control, truthful reason
  controls, adversarial mismatch/stale/duplicate/unsupported/actionable cases, and focused tests all
  PASS.
- Root combined suite: `309 passed, 1 skipped, 42 subtests passed`.
- Attention practical and compileall: PASS.

Evidence:

- `multi-agent-logs/attention-validation/runs/20260802-m5-q9-160750Z/REPAIR_PLAN.md`
- `multi-agent-logs/attention-validation/runs/20260802-m5-q9-160750Z/REPAIR_REVIEW.md`
- `multi-agent-logs/verification/m5-q9-ineligibility-luna/REPORT.md`

