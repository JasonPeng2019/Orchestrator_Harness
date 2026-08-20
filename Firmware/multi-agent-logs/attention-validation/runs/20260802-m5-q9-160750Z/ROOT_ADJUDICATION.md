# M5 Q9 Root Adjudication

## Decision

- `HARNESS_PASS`
- `WATCHER_BUG`
- `MANAGER_EVIDENCE_INSUFFICIENT`
- Sprint disposition: `WATCHER_BUG`
- Active-goal attempt: **9/10**
- Comparable qualifying count: **0/3**

The root accepts the post-sprint review. The four external worker-controller
processes died because the root launched arguments containing spaces incorrectly.
Their Codex children continued and later published genuine HELP signals, but the
native harness correctly refused to make those signals actionable because their
producer lanes were no longer live. This is correct fail-closed harness behavior,
not a harness delivery failure.

The deterministic watcher nevertheless classified all four signals as
`HARNESS_DELIVERY_DELAY`. Its evidence model knows that the signals were observed
and never became actionable, but has no canonical record explaining that the
harness intentionally rejected them as non-live. That is a verified diagnostic
bug. Q9 contains no valid manager receipt, claim, response, or resume chain and
therefore says nothing reliable about persistent-manager idling or the need for a
`codex exec` bridge.

## Scope decision

Repair only the missing passive eligibility evidence and watcher attribution.
Do not change native selection, scheduling, wake behavior, worker/controller
logic, or manager behavior. Correct controller argument quoting as an operator
procedure for Q10; do not add a runner, wrapper, relay, or retry controller.

## Cleanup

Q9 reached its natural boundary. The native harness and diagnostic watcher
stopped cooperatively. All 11 registered epoch processes are absent, watcher
input is drained, and the resource inventory is empty.

