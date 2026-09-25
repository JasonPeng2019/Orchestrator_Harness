# STEP-05 - Preparation preserves one budget and legacy state

## Outcome

An objective continues through retry, route correction, APC, and old durable records without renewing its budget or losing exact plan precedence. This closes [BEHAVIOR-01](../specification/behaviors/BEHAVIOR-01-preparation-continuity-stays-bounded-and-compatible.md).

## Scope and touchpoints

Review existing `PreparationService` in `src/memory_harness/preparation.py`, fixed resolution in `config.py`, stage timing in `search.py`, and compatible SQLite reads in `store.py`. Keep accepted retrieval ranking and adapter trust unchanged. Direct selectors exist in `tests/local/preparation/test_step04_search_deadline.py`, `test_step04_contract_corrections.py`, `tests/local/procedures/test_step04_migration_compatibility.py`, and `tests/local/contracts/test_step04_handoff_plan_state.py`.

## Implementation

Carry one captured configuration, decision identity, spent cost, trusted remaining-time source, and absolute stage deadline across restart and correction. Charge APC queue/launch/correction/validation and final freshness to their enclosing bounds with positive execution reserve. Unknown time permits only the cheap configured pass. Preserve accepted-plan precedence and candidate/reviewed-plan continuity; nonempty invalid references fail exact state. Late Level 0 permanently supersedes its old packet and permits only the bounded ordinary reprepare or explicit no-memory route. Add only the migration/read changes needed by these consumers; never replace an unreadable old database with empty state. Apply the canonical feature-off table at service entry, including APC and all-off.

## Dependencies and integration

Consumes STEP-04's child deadline/decision contract and accepted stores. Produces a stable preparation disposition for context finalization and a compatible state reader for later effects/snapshots. Do not reopen old adapter work without a reproduced consumer defect.

## Requirement-fit validation

Demonstrate that restart/route correction cannot reset spent time, invalid exact state is not treated as cache miss, accepted or pending review is not supplanted by template search, and an old accepted database remains readable. An optional timeout may reduce optional memory but cannot erase mandatory task state.

### Fast test suite

Run the four direct selectors named above with `python -m unittest <module> -q` from the candidate root; add focused cases for candidate/reviewed continuity, spent-budget restart, and switch-off suppression if absent. The fast result is invalidated by changed deadline, plan-state, configuration, or migration inputs, not unrelated adapters.

## Failure scope and recovery

An incompatible old schema preserves the database and blocks its affected operation until a narrow migration/read repair. A budget failure blocks only the affected optional stage and any context depending on its result.

### Fast lane for revisiting old work

Repair the failed budget/state/migration branch; retain prior valid candidate results. Rerun its direct selector and STEP-06 finalization only when the prepared disposition changed.
