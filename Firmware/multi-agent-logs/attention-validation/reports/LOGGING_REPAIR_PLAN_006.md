# Logging repair plan 006 — isolate current-epoch attention evidence

## Observed failure

R5 proved the real collaboration wake path, but its `attention-report.json` contains 255 unrelated `INSUFFICIENT_EVIDENCE` rows from historical ordinary harness/lane events. Those records were observed during R5 and stamped into the R5 report even though their event IDs belong to older epochs. The current R5 signal is complete, but the report cannot satisfy the per-sprint no-unresolved-error gate while historical ordinary records become causal attention events.

## Required smallest repair

1. Trace which ordinary-source normalization path turns historical non-attention events into current-epoch attention-report rows.
2. Preserve ordinary inputs for the Terra evaluator and watcher diagnostics, but exclude them from the manager-attention causal timeline/report unless they are explicit `manager-attention-timeline/v1` records or exact current-epoch harness attention records.
3. Do not discard current-epoch explicit attention evidence, service-loss evidence, or ordinary watcher evaluator behavior.
4. Add regression tests using historical ordinary events plus one complete current-epoch signal: report contains only the explicit current-epoch attention event(s), cursor remains drained, ordinary changes may still drive evaluator behavior, and attention-only changes still do not.
5. Run the full watcher suite, full harness suite, compileall, and focused R5-style synthetic check. No hardware.

Counter stays `0/3`. A fresh epoch is required after independent review.

## Additional R5 service-liveness failure

The optional watcher exited at `2026-08-01T18:02:42.814396Z` with `SERVICE_ERROR: defect requires supported kind and evidence` after Terra returned `defect=true`, `kind=manager_failure` without supported evidence. This evaluator-output validation error must be contained as a durable rejected-evaluator/observation error; it must not terminate the watcher service. Add a regression proving malformed/unsupported evaluator output logs the failure and subsequent polling continues. A counted sprint still fails closed if the error prevents a trustworthy conclusion, but service liveness must be preserved.

## Root-cause refinement

The pollution originates upstream: the fresh primary harness `attention-events.jsonl` stamps old manager signals (for example a `20260731-long-canary` Atlas signal) with the configured R5 epoch when it rediscovers them. Therefore an optional-watcher epoch filter alone is insufficient. The primary harness must emit causal attention records only for source events that explicitly belong to the configured attention epoch; historical findings remain in ordinary scan/event outputs. The accepted epoch-membership rule must be explicit and tested without relying on substring guessing where structured lane/epoch data exists.

## Accepted epoch-membership contract (plan review resolution)

For a candidate harness event, structured `data.attention_epoch_id` has precedence: when present it must exactly equal the configured epoch, and a mismatch cannot be rescued by any lane string. Only when that field is absent may a structurally parsed `lane_id` or `declared_lane_id` establish membership by exact epoch component, not arbitrary substring. An event with neither proof stays in ordinary reconciliation/evaluator diagnostics and never enters causal attention output. Current primary-service loss remains emitted by its dedicated identity-loss path, not by weakening this membership rule.

Required tests include conflicting explicit epoch/lane, no membership fields, R5-shaped old signals and non-signals, preservation of every current signal lifecycle stage, ordinary evaluator visibility, and a true service-loop survival test for rejected evaluator output.
