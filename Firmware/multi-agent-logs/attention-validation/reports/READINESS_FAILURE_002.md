# Attention readiness failure 002

Counter: `0/3`; no counted sprint, lane controller, provider, MCP server, or hardware action
started.

The exact Sprint-R primary harness started, but the optional watcher exited twice within roughly
0.2 seconds of publication. Both `service.json` records contained exact owner/watcher identities
and ended `service-error`; the watcher log contained only `SERVICE_STOPPED`, with neither
`SERVICE_STARTED` nor `SERVICE_ERROR`. The read-only watcher subagent independently detected and
reported the coverage gap. The primary harness was then stopped cooperatively and its exact PIDs
were absent.

This falsifies the earlier host-only readiness result at the real detached-service boundary. The
counted window never opened, so no sequence reset beyond its existing `0/3` is required.

Accepted minimal repair: make optional-watcher startup publication/validation deterministic across
an existing terminal service record, fail closed on identity mismatch, log the exact early failure
reason, and add a regression that exercises restart after terminal state. A Terra-medium coder owns
the repair; exact service preflight and both host suites must pass before Sprint R is relaunched.
