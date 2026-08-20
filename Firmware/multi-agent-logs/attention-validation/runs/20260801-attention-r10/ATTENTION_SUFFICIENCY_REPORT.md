# Sprint R10 attention-logging sufficiency report

## Verdict

**FAIL — counter remains 0/3.** R10 proves Repair 009's explicit continuity chain works in a
real run: both late formal-review events classify `BUSY_MANAGER_DELAY`. It also exposes two
remaining analyzer defects that prevent a clean sprint.

## What ran

Atlas/A22, Boreal/D31, Cygnus/A24, and Delta/A26 resumed their same persistent Luna sessions in one
concurrent batch. Each created a real blocking HELP, received an exact manager decision, performed
a bounded read-only E2E state/next-plan reconciliation, wrote `ATTENTION_R10_CHECKPOINT.md`, emitted
a nonblocking completion signal, and exited. No provider, MCP lifetime, lease, or hardware action
was permitted or started.

The watcher stayed live, delivered and recorded all four exact notifications, and the final cursor
is drained.

## Successful Repair 009 evidence

- Review event `r10-review-001`: `BUSY_MANAGER_DELAY`, 120.962 seconds late.
- Exact harness review event `83aa83985ea0f2de916f6b41f9a30ae682b179ab0019768ab03291154adb0938`:
  `BUSY_MANAGER_DELAY`, 196.678 seconds late.

These were covered by explicit wait and event-handling intervals joined through strict-prior
`continuous_from_record_id` links. No silence inference was used. This validates the Repair 009
mechanism, but R10 still cannot count.

## Blocking defects

### 1. Impossible signal deadline is accepted

Atlas signal source record `88077113-4a79-4a3f-b26d-7eabd7ac6a40` was created at
`20:00:28.113945Z`, but its declared delivery deadline is `19:59:13.7334773Z`, about 74 seconds
before creation. That is impossible source evidence. Validation accepted it, and the analyzer
reported `HARNESS_DELIVERY_DELAY` rather than contradiction/insufficient.

A signal's delivery/response deadline must never predate that signal's own source creation. This
check must be scoped to deadline-originating records: later notification/receipt/review records may
legitimately carry an already-expired original deadline.

### 2. Timely blocking manager responses fall through to insufficient

Boreal and Delta had timely canonical watcher notification, claim, decision, and manager response,
but both report `INSUFFICIENT_EVIDENCE` with “matching stage deadline and late endpoint.” A complete
on-time blocking response path should classify `NO_BLOCKING_IMPACT`; otherwise an ordinary healthy
attention event can never satisfy a sprint gate.

Atlas/Cygnus downstream receipt timing is a separate harness/agent-delivery observation. The
manager-attention verdict must use deterministic precedence and must not relabel an on-time manager
claim/response as manager idle/busy.

## Seven gates

1. Fresh epoch/config/manifest: PASS.
2. Primary/optional watcher continuity and drained cursor: PASS.
3. Four real blocking challenges and exact notifications: PASS.
4. Correlated manager claims/decisions/responses and four lane checkpoints: PASS.
5. Formal-review causal classification: PASS; both late reviews are busy-manager delays.
6. Valid source deadline semantics and complete healthy-event classification: **FAIL**.
7. Exact lane endpoint/cleanup: PASS after final service shutdown proof.

R10 is rejected. Repair 010 is required, then the three-sprint sequence restarts at zero.

