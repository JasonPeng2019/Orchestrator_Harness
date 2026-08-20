# M5 Q7 watcher deferral-metric repair

Validated: `2026-08-02`

## Defect and repair

Q7 proved the deterministic watcher could compute `explicit_deferral_seconds` from a deferral that
occurred after the event was already pending. That reversed subtraction produced an impossible
negative metric and made usable evidence insufficient.

`harness_watcher_implementation.attention._deferral_duration` now uses the latest explicit
`HARNESS_EVENT_DEFERRED` whose source timestamp is at or before the selected pending endpoint. If
none exists, the metric is absent rather than invented. No harness scheduling, wake transport,
manager, worker, or other watcher classification changed.

## Verification

- Terra-medium coder focused test: **28 passed**.
- Independent Terra-medium review: **PASS**; watcher suite **96 passed**, 27 subtests; attention
  practical **PASS**.
- Independent GPT-5.6-luna high practical smoke: **PASS**.
- Root full combined suite: **304 passed, 1 skipped, 42 subtests**.
- Separate harness suite: **208 passed, 1 skipped, 15 subtests**.
- Separate watcher suite: **96 passed, 27 subtests**.
- Host-only attention practical and compileall: **PASS**.

Evidence: `multi-agent-logs/verification/m5-q7-deferral-metric-luna/SMOKE_REPORT.md`.

## Scope and M5 consequence

No runner, wrapper, relay, evaluator, hardware, provider, MCP, deploy, flash, commit, or push was
used. Because watcher analysis changed, Q6 remains useful history but no longer counts toward the
comparable set. M5 restarts at `0/3`; attempt 8/10 is next.
