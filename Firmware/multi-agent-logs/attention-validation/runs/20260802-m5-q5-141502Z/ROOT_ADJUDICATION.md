# Q5 root adjudication

- **Attempt:** 5 of 10
- **Harness:** `HARNESS_BUG`
- **Watcher:** `WATCHER_PASS`
- **Manager evidence:** `MANAGER_EVIDENCE_INSUFFICIENT`
- **Disposition:** `RESET`; not qualifying; consecutive count remains 0/3.

## Basis

Four genuine worker requests completed and all workers recorded response receipt and resumed work.
The diagnostic-only watcher drained cleanly, retained contradictions, and produced no observation
errors. Finalization passed and all 10 registered processes plus all resources were exactly
cleaned.

The harness incorrectly ingested Boreal's hidden atomic `.tmp.json` signal file and its final JSON
as two path-derived native events for one signal. The duplicate survived acknowledgement. This is
a verified harness discovery defect and invalidates the harness gate.

Root also resumed attention during the live window following a user message/turn boundary. That
external influence independently violates the isolation rule, so Q5 cannot support the manager
architecture verdict.

The reviewer's second proposed harness defect is rejected: stdout
`MANAGER_WAKE_DELIVERED` and root `MANAGER_WAKE_RECEIVED` are deliberately separate stages. The
late receipt record reflects root execution/attention, not proof of false harness delivery.

The accepted repair is limited to excluding hidden atomic temporary signal files from native
signal discovery. See `REPAIR_PLAN.md`.
