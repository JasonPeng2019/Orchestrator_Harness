# M5 Latency Attribution Repair

Status: implemented, independently reviewed, practically smoke-tested, and rebaselined. The
90-second value remains a diagnostic target; M5 accepts an overrun only when gap-free canonical
evidence proves genuine manager work or handling an earlier genuine request.

## Verified problem

The deterministic watcher currently labels every blocked-HELP delivery deadline missed at
`HARNESS_EVENT_ACTIONABLE` as `HARNESS_DELIVERY_DELAY`. That is correct when the harness observes
the request late, but it can misattribute time after an on-time observation when the persistent
manager is demonstrably occupied with real work or a previously delivered request.

The repair must improve attribution without weakening the delivery deadline or hiding a real
harness failure.

## Minimal implementation plan

1. Change only the deterministic attention analyzer and its focused tests/documentation.
2. Preserve these rules:
   - observation after the delivery deadline remains `HARNESS_DELIVERY_DELAY`;
   - a late actionable endpoint while the manager is waiting for that native wake remains
     `HARNESS_DELIVERY_DELAY`;
   - missing or contradictory causal coverage remains `INSUFFICIENT_EVIDENCE`;
   - a successful on-time path remains `NO_BLOCKING_IMPACT`.
3. When the harness observed the exact blocked HELP on time but made it actionable late, inspect
   the complete explicit manager-activity interval covering the actual overrun from delivery
   deadline to actionability:
   - classify `BUSY_MANAGER_DELAY` only when logged genuine manager work fully explains the late
     interval;
   - otherwise retain harness-delay or insufficient-evidence attribution as the evidence requires.
4. Do not add a new classification, configurable timeout, wrapper, relay, runner, scheduler, or
   runtime assistance layer. Do not simply increase the 90-second experiment deadline.
5. Add focused tests for:
   - late harness observation;
   - on-time observation followed by fully evidenced manager-busy delay;
   - on-time observation followed by manager waiting on the harness;
   - incomplete/contradictory manager activity;
   - existing healthy and delivery-precedence cases.
6. Update the attention-logging contract in plain terms.

## Acceptance

- The focused tests demonstrate all cases above.
- Existing harness and watcher suites remain green.
- Pyright/compile checks remain green.
- Re-analysis of M5 epoch `20260802-m5-r1-110513Z` changes a classification only where the durable
  activity evidence actually supports it; late detection is not excused.
- A reviewer may criticize but cannot block. The root orchestrator decides which findings warrant
  another code turn.
- No commit or push.
