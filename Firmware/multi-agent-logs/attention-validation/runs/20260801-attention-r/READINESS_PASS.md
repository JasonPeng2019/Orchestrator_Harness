# Sprint-R attention readiness

Status: **PASS**. Counter remains `0/3`; this is a host-only preflight, not a counted sprint.

The exact Sprint-R harness and watcher configs loaded successfully. A disposable integration
probe exercised all six configured producer inputs and the configured harness-attention source,
then deleted its temporary runtime. It proved:

- all six harness stages for a `MANAGER_SIGNAL` join on its stable `signal_id` while retaining the
  hashed harness ID and response deadline as provenance;
- `WAIT_STARTED -> deadline -> WAIT_FINISHED -> exact claim` is accepted when wake-to-claim is one
  second and rejected by the focused test when the sealed ten-second bound is exceeded;
- an attention-only append, a cursor reload, and a post-reload append cause zero ordinary Terra
  evaluator calls while producing eight canonical timeline records;
- all allowlisted manager/lane/watcher producer paths accept and ingest their permitted records;
- disabled watcher entry points remain no-ops.

Evidence: `READINESS_RESULT.json`, targeted tests (`47` pass), full harness suite (`179` pass,
`1` skip), full watcher suite (`53` pass), compileall, Ruff F, and Pyright on changed sources/tests.
The allowlist proxy relay test transiently exposed its known coalesced-read race, then passed a
focused retry and the full suite; it does not touch the attention paths.

No provider, MCP server, lane controller, or hardware action ran during readiness.
