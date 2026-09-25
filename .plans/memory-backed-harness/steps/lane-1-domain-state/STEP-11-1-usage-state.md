# STEP-11-1 — Store and aggregate native usage once

This step is a derivative of [original STEP-11](../../source-steps/STEP-11-native-usage-remains-attributable.md).

Owner: lane 1. This is the complete usage contract, store, and aggregation assignment.

Add narrow usage contract and store methods in `src/memory_harness/contracts.py` and `store.py`, consuming source-native receipts from the existing harness/provider and adapter surfaces rather than creating a separate telemetry or learner ledger.

Add narrow usage record validation and storage keyed by actual native invocation and owning objective, decision, or maintenance operation. Represent a started call with absent counters as incomplete, not zero. Accept late authentic receipts idempotently; distinguish distinct same-count calls and cumulative receipts. Preserve provider input/output/cache/reasoning/total/cost semantics without double counting. Attribute the accepted APC child once to its parent and separate outer implementation, product-test ROOT, and inner candidate work.

Lane 2 captures harness/provider receipts; lanes 3 and 4 expose adapter-native counters only where their sources provide them. Evidence: focused source-shaped receipt, replay, correction/resume, and incomplete-usage tests; do not mutate fixed outcomes.

Track every known started model, CLI, embedding, retrieval, APC, worker, ROOT, reviewer, correction, and resume call by actual native identity, owning objective/decision or maintenance operation, stage, and requested/resolved/native binding. Failed reuse and subsequent fallback both contribute work; aggregate only compatible units and rates. Never sum counters already included in provider totals or cumulative intermediate receipts twice. Unknown provider counters limit only usage completeness, not valid quality evidence. Add `tests.local.usage.test_native_usage` using realistic receipt shapes for same-count distinct calls, repeated/cumulative/late receipts, missing counters, parent-child APC charging, correction/resume, and no quality-outcome mutation. STEP-18 later observes real provider-native attribution.

For a revisit, repair only the source parser or invocation join, retaining valid quality evidence, and rerun focused usage tests. Rerun child/dispatch checks only where receipt parsing changed; revisit STEP-15/18 only when their usage inputs changed.
