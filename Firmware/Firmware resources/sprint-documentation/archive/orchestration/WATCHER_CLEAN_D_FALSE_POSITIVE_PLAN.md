# Plan - optional watcher pre-request false-positive repair

Accepted decision: keep the primary harness resource-ambiguity observations unchanged. They are
cautious raw evidence. Repair only the optional watcher's interpretation of that evidence.

## Demonstrated defect

Clean-D watcher alerts `hwa-9c5f620f26fcd62c54b404b0` and
`hwa-deb43a663920aab376166c67` classified normal pre-request/controller-start states as manager
failures solely because a request or MCP lifetime was not yet visible. A request cannot exist until
a permission-bearing boundary is reached.

## Implementation slice

1. In the optional watcher review packet and Terra-high evaluator instruction, make the phase rule
   explicit:
   - absence of request identity during ordinary setup/preparation is not a defect;
   - a declared MCP lifetime may be absent while the controller is still preparing to start it;
   - ownership failure requires explicit evidence that the lane is awaiting a permission relay,
     plus missing or inconsistent lane-correlated active lifetime/request evidence;
   - real duplicate ownership, resource conflict, stale/mismatched relay, and request-awaiting
     identity loss remain alertable.
2. Keep strict packet-bound evidence validation, alert persistence, primary harness behavior, and
   all lifecycle/recovery behavior unchanged.
3. Add focused tests that capture the real Terra evaluator input and prove the exact rule is present
   both in packet constraints and evaluator instructions. Add a small recorded-shape regression
   showing pre-request ambiguity is described as non-alertable input while explicit request-awaiting
   loss remains alertable to the evaluator.
4. Run only the focused watcher tests, then the existing watcher smoke suite. Do not rerun expensive
   WSL/real-agent/full-harness tests for this narrow prompt/packet change.

## Acceptance

- Focused and watcher smoke tests pass.
- No production harness file changes.
- No server, hardware, experiment evidence, or prior watcher runtime mutation.
- A fresh clean-E watcher runtime will provide the real deployment validation.
