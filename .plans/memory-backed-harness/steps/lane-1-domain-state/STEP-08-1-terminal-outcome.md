# STEP-08-1 — Fix one immutable terminal outcome

> **Time-crunch MVP acceptance:** Execute this step with [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Return work for repair only for a reproduced defect in desired normal supported behavior, credible regular recovery or compatibility, or a critical invariant. Record every other confirmed edge, theoretical, unsupported, or non-normal issue in [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md) without a correction or re-review gate.

This step is a derivative of [original STEP-08](../../source-steps/STEP-08-terminal-outcome-is-fixed-once.md).

Owner: lane 1. This is the complete durable-outcome assignment.

Extend `src/memory_harness/runtime.py` `record_outcome`, the existing `store.py` outcome transaction, and `contracts.py` validation; lane 2 supplies evidence at the existing `harness/orchestrator_harness/review.py` completion seam.

Consume STEP-07's observed native execution and lane 2's exact review/acceptance evidence. Validate the task, objective, decision, accepted plan, run, result, review, and acceptance join; reject wrong-run or APC-child evidence for the parent. Distinguish PASS, FAIL, BLOCKED, genuine terminal unknown, exceptional acceptance, and missing observation. Fix the local outcome transactionally once: identical replay returns the same row, contradictory replay reports conflict, linked supersession records a legitimate correction. Keep effects and usage outside the immutable quality outcome.

The checkpoint publishes the outcome identity and the effect/usage parent identities for lanes 2–4. Evidence: focused outcome/replay tests and directly affected review-boundary tests; missing evidence must remain missing.

An identity conflict blocks only the affected outcome and its dependent effects; unrelated outcomes and effects continue. Include a focused two-outcome conflict test that proves this isolation without changing the existing fixed row or native evidence.

Preserve accepted STEP-01 outcome records and reviewed-evidence provenance. Exercise crash both before and after the local fixation transaction: the former invents no terminal row and the latter replays to the identical row. A conflict preserves the fixed row and native evidence; never repair by assigning another outcome ID. A genuine terminal unknown requires terminal native evidence and is distinct from no observation. Use `tests.local.contracts.test_runtime_dispatch` or a focused `tests.local.outcomes.test_terminal_outcome` selector, plus affected harness review tests. Prove PASS/FAIL/BLOCKED, exceptional acceptance, wrong-run evidence, supersession, and separation of quality from optional effects; native completion-boundary proof remains for the integrated candidate.

For a revisit, repair only the exact evidence join or fixation transaction and retain valid dispatch evidence. Rerun focused outcome and affected review tests; revisit STEP-09/10 only if the outcome identity they consume changed.
