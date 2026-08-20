# Clean-O optional-watcher repair specification

## Trigger and scope

Independent audit `.agent-workspace/CANARY_S1_CLEAN_O_INDEPENDENT_AUDIT.md` made Clean-O
noncounting at `0/3`. It validated two issues:

1. the optional watcher converted a normal 20-to-25-second controller-exit/final-status
   publication interval into two durable `manager_failure` alerts; and
2. the manager allowed a later `MANAGER_REVIEW_DUE` condition to clear on lane exit without a
   second whole-suite review/acknowledgement.

This repair changes only `harness_watcher_implementation` code/tests and the canary manager's
operational gate. It must not edit `BYO-Firmware-MCP`, firmware, experiment evidence, the primary
`orchestrator_harness`, or historical Clean-O watcher state.

## Required watcher behavior

### One-poll exact-identity quarantine

- A newly observed `STALE_STATUS` is a conservative primary-harness fact, but by itself is not yet
  optional-watcher evidence of `manager_failure`.
- The optional watcher must quarantine the first occurrence by exact condition identity for one
  configured watcher poll interval. It must not expose that first occurrence to the evaluator.
- The quarantine must survive watcher poll calls and a normal service restart through durable
  cursor state. Existing cursor files without the new state remain readable.
- If the same exact identity is followed, in the same or a later poll, by `CONTROLLER_ACTIVE`,
  `CONTROLLER_EXITED`, or `CONDITION_CLEARED` whose `cleared_type` is `STALE_STATUS`, discard the
  quarantine without an evaluator alert. An unrelated identity or unrelated cleared condition
  must not clear it.
- If no exact recovery occurs for one full configured poll interval, expose the preserved stale
  fact exactly once to the evaluator as a persisted condition. The review packet must retain a
  valid source path/SHA-256/offset tuple so strict evidence validation still works.
- A repeated same-identity `STALE_STATUS` may establish persistence, but must not create duplicate
  evaluator work or duplicate alerts. Existing stable alert deduplication remains intact.
- Raw observed logs, cursor offsets, manager evidence, and historical alert files are never
  rewritten. Watcher-originated recursive-input filtering and no-progress behavior remain intact.

### Evaluator contract

- The packet/prompt must make the policy explicit: a single quarantined stale transition is not
  alertable; only a stale condition released after the full quarantine interval is eligible for
  `manager_failure` classification.
- Genuine duplicate ownership, resource conflict, request/relay identity loss, sustained stale
  status, loop, starvation, regression, and manager failures remain alertable.
- Do not add a broad `STALE_STATUS` ignore rule and do not weaken the primary harness's immediate
  fail-closed reporting.

## Required manager-procedure behavior

- The successor canary uses an independent wall-clock formal-review gate, not pending-notification
  delivery as its timer.
- When active lanes reach the configured review deadline, the main manager immediately writes a
  compact whole-suite review before continuing ordinary checkpoint/signal draining.
- It drains already-reviewed higher-priority events without artificial 20-to-30-second sleeps. As
  soon as the exact `MANAGER_REVIEW_DUE` becomes pending, it acknowledges it and verifies the
  baseline advanced.
- No new lane launch, permission relay, or hardware phase may be authorized while a due formal
  review is unwritten. This is an operational gate, not a primary-harness code change.

## Verification

Add focused deterministic tests for:

1. same-delta stale then exact recovery: hidden;
2. stale in poll N then exact recovery in poll N+1: no evaluator call/alert;
3. stale in poll N, service/cursor reload, no recovery for a full poll interval: released exactly
   once and capable of producing one durable alert;
4. unrelated identity and unrelated `CONDITION_CLEARED`: do not suppress a genuine stale;
5. the actual Clean-O event shapes (`STALE_STATUS` followed by `CONTROLLER_EXITED`) replay without
   an alert, while a sustained stale control alerts;
6. legacy cursor compatibility, cursor offsets, recursive watcher filtering, and strict evidence
   validation remain green.

Run only the focused changed tests first, then the affected optional-watcher smoke suite once. Do
not rerun live firmware endpoints, hardware, real evaluator calls, or unrelated expensive harness
acceptance tests. A later fresh successor canary is the real operational verification.

## Acceptance

- Focused and affected tests pass.
- Independent Terra-medium review finds no functional defect in the change.
- No relevant process remains.
- The Clean-O counter remains `0/3`; accepted lane evidence is preserved.
- A fresh successor epoch is not started until the repair and manager-review gate are accepted.

## One-way-door decisions

- Use temporal exact-identity quarantine, not a blanket stale suppression.
- Do not retroactively dismiss or rewrite the two Clean-O alerts.
- Do not modify primary-harness notification priority on the current evidence; the independent
  audit classified the second issue as a manager-procedure lapse, not a proven harness defect.
- Do not add a new invalid-alert state machine in this slice; preventing the demonstrated false
  alert is the narrow functional repair the auditor required.

