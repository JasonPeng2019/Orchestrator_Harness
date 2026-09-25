# STEP-11-2 — Capture source-native invocation and usage receipts

This step is a derivative of [original STEP-11](../../source-steps/STEP-11-native-usage-remains-attributable.md).

Owner: lane 2. This is the complete harness/provider receipt assignment.

Read native provider and harness receipts for APC child, worker, ROOT, reviewer, correction, and resumed calls. Preserve actual invocation and requested/resolved/native binding identities and provider counter semantics. Deliver a started call with missing usage as incomplete to lane 1's usage record; never synthesize zero. Distinguish outer implementation, product-test ROOT, and inner candidate work in native proof. Late receipts and cumulative intermediate updates must not count twice.

Evidence: lane-2-owned harness receipt/parser tests under `harness/orchestrator_harness/tests/` for missing, late, repeated, cumulative, and distinct same-count calls; run lane 1's `tests.local.usage.test_native_usage` read-only. Final provider-native attribution is observed in STEP-18.

Capture every known started product-harness/model/CLI call, including APC adaptation, worker, ROOT, reviewer, correction, and resume. Preserve native identity, stage, owning objective/decision or maintenance operation, and requested/resolved/native binding. Where the harness owns embedding or retrieval calls, pass their source-native counters through the same interface; lanes 3/4 expose adapter counters only where their sources provide them. Failed reuse plus fallback is work, not a replacement count. Do not add a separate telemetry ledger. A provider that exposes no counters yields incomplete usage while its real invocation and quality evidence remain valid. Run directly affected APC-child and dispatch tests when receipt parsing changes, plus source-shaped repeated/cumulative/late/missing/same-count cases. Never derive usage by counting an accepted outcome.

For a revisit, repair only the native receipt parser or exact invocation join and rerun focused usage cases, plus child/dispatch tests if parsing changed. Revisit STEP-15/18 only if the usage inputs they consume changed; retain valid quality evidence.
