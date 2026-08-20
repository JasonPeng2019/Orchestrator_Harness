# Q5 verified harness repair plan

## Root adjudication

Q5 is **non-qualifying**: `HARNESS_BUG`, `WATCHER_PASS`, and
`MANAGER_EVIDENCE_INSUFFICIENT`. It was also contaminated when a user turn resumed root during
the live window.

Accepted defect: the harness discovers hidden atomic temporary files such as
`.sig-....tmp.json` as final manager signals. When the final file appears, one logical request can
acquire two path-derived native event IDs and survive acknowledgement as duplicate pending work.

Rejected reviewer claim: `MANAGER_WAKE_DELIVERED` preceding `MANAGER_WAKE_RECEIVED` is not itself
a harness defect. The contract intentionally distinguishes successful native stdout delivery from
the manager's later receipt record. In Q5, root failed to record receipt promptly after the tool
returned; that is execution/attention evidence, not proof that the harness falsified stdout
delivery.

## Smallest repair

1. In native manager-signal discovery, ignore hidden/atomic temporary JSON filenames while
   continuing to read ordinary final `*.json` signal files.
2. Add focused tests proving a hidden `.tmp.json` plus its final file yields exactly one signal and
   one stable native event, while existing identical-final-file compatibility remains intact.
3. Do not alter wake transport, notification scheduling, acknowledgement semantics, watcher
   analysis, worker code, or add any wrapper/relay/retry layer.
4. Run focused discovery/notification tests, the full harness/watcher suite, compile verification,
   independent code review, and Luna practical smoke. Re-freeze hashes and rerun M4 readiness
   before the next counted attempt.

Root owns final acceptance. Reviewers advise and never block.
