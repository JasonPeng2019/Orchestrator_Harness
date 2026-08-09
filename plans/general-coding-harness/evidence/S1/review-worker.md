# S1.R1 Review

Reviewed commit: `adfc26a5537b4c0256b5fccfc6cc22bc3fb93676`

## Admitted Findings

1. **High - prompt time-of-check/time-of-use gap.** Coding prompt bytes were hashed during parsing and read again during execution, permitting substitution between validation and launch. The controller must execute the already-verified bytes or immediately revalidate them.
2. **High - resume thread identity could be overwritten.** The JSONL drainer accepted any later `thread.started` ID and replaced the previously validated resume thread. Resume must reject a child-emitted mismatch.

## Deferred To Planned Test Authoring

- Update watcher evaluator-dependent fixtures to opt in explicitly after the default becomes false.
- Add the complete coding invocation parser, confinement, settings, status/event identity, and resume matrix.

## Triage

The two high findings are functional contract defects and return to S1.P. The test gaps belong to S1.A1 after Checkpoint A, so they do not expand the product repair.

## Repair Verification

Commit `54e9d14d7a865de3a5f7edd75108000423f565be` resolved both admitted findings. The reviewer confirmed that launch consumes the retained verified prompt bytes and that a resumed child thread mismatch fails without replacing persisted identity. Six legacy controller tests also passed. Checkpoint A is closed.
