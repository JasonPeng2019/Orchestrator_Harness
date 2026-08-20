# Clean-K primary harness lifecycle/actionability repair spec

## Source defect

The independent Clean-K audit in
`.agent-workspace/CANARY_S1_CLEAN_K_INDEPENDENT_AUDIT.md` validated four related
primary-harness failures:

1. a closed historical MCP lifetime became manager-actionable after its PID was reused;
2. already-answered HELP signals resurfaced while their lanes were still active;
3. exact suite request/relay/lifetime records were labelled ambiguous;
4. answered requests continued to generate expiry actions.

The optional watcher, production firmware server, hardware, and accepted D31/A24 results are out of
scope. The manager review-cadence lapse is a successor-run procedure correction, not code scope.

## Required behavior

1. Keep all historical MCP, request, relay, signal, and expiry observations visible in the read-only
   snapshot and ordinary event history.
2. A terminal MCP exit is manager-actionable only when it is correlated to a currently active or
   unknown lane, or is a genuine newly observed uncorrelated transition. PID reuse in a closed
   historical lane must not wake an unrelated epoch.
3. Recognize the documented `suite-manager-request/v1.lifetime_binding` form as proven MCP
   lifetime evidence only when server name, PID, and creation time reconcile to the live process.
   Mismatch, absence, missing creation evidence, or conflicting identity must fail closed.
4. Separate exact relay binding from authorization freshness. An expired but otherwise exact relay
   is historical proof that the manager answered that immutable request; it is not reusable
   authority and must be labelled explicitly as expired.
5. An exact answered request (current-bound or expired-bound) is not manager-actionable and does not
   emit actionable request-expiry work. Unanswered live requests, bad hashes, unbound relays,
   ambiguous lifetimes, and current warning/critical expiry remain actionable.
6. Correlate a manager signal to its exact request using durable identifiers/evidence paths. Once
   that request is answered, the signal remains observable but cannot wake the manager. A signal
   with no answered request correlation in a current live lane remains actionable.
7. Do not change the server, watcher, lane workspaces, experiment evidence, hardware state, or
   permission/relay files.

## Compatibility decision

This repair may add fields to the v1 snapshot records and may introduce explicit internal snapshot
states `BOUND_EXPIRED` and `RELAYED_EXPIRED`. It must not remove or rewrite existing fields. The
read-only harness never treats an expired relay as executable authority; the new state makes that
fact clearer than silently calling it `BOUND` or `UNBOUND`.

## Acceptance

- Focused synthetic tests cover every validated defect and genuine-live positive controls.
- Existing primary harness tests remain green.
- A no-write scan over retained Clean-K data completes without observation errors or resource
  conflicts and does not select the validated historical/answered conditions as fresh actions.
- No test starts provider/MCP/hardware or mutates experiment evidence.

