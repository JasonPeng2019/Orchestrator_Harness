# Clean-O optional-watcher repair plan

## Accepted decision

Implement one-poll, exact-identity stale quarantine inside `harness_watcher_implementation` and
enforce the successor's manager formal-review gate operationally. Do not change the primary
harness or historical evidence.

## Steps

1. **Lock the reproduction.** Add focused tests that replay a first-poll `STALE_STATUS` and a
   later exact `CONTROLLER_EXITED`/clear, plus a sustained-stale control. Prove the current code
   fails the cross-poll transient case before implementation.
2. **Persist quarantine state.** Extend the watcher cursor compatibly with the minimum durable
   exact-identity record needed to retain first-seen time, source evidence tuple, and raw stale
   record. Legacy v2 cursor files must load without migration work.
3. **Filter and mature.** During packet construction, reconcile new exact recovery records against
   quarantined stale records. Hide recovered transitions; release an unrecovered record once after
   one configured poll interval with valid evidence metadata and no duplicate release.
4. **Bind evaluator policy.** Add the precise quarantine/persistence rule to packet constraints and
   Terra evaluator instructions without weakening other defect categories.
5. **Verify narrowly.** Run the newly added test IDs, then the affected
   `harness_watcher_implementation.tests.test_watcher_smoke` suite once. Record commands and exact
   results in `.agent-workspace/CANARY_CLEAN_O_WATCHER_REPAIR_VERIFICATION.md`; do not rerun
   unrelated expensive tests.
6. **Self-review and cleanup.** Review the diff for exact-identity behavior, legacy compatibility,
   one-time release, raw-log immutability, and test realism. Prove no watcher/test process remains.
7. **Independent gate.** The persistent Terra-medium auditor reviews the diff, focused tests, and
   actual Clean-O replay. Fix only validated functional gaps. Once accepted, write the successor
   target with the independent wall-clock formal-review gate and start a fresh epoch; never reuse
   Clean-O runtime authority.

## Scope guard

No server, firmware, catalog, skill, primary-harness, historical alert, board, deployment, commit,
or real model-evaluator change is in scope. Do not add speculative alert taxonomies, autonomous
recovery, or a generalized workflow engine.
