# Clean-G primary lifetime-reconciliation repair verification

Verified: `2026-07-31T18:37:45Z`  
Plan: `.agent-workspace/CANARY_CLEAN_G_FIX_PLAN.md`  
Scope: primary `orchestrator_harness` only

## Implemented

- `orchestrator_harness/reconcile.py` now keeps strictly terminal MCP lifetime records terminal
  across later numeric PID reuse.
- Role-local PID identity parsing accepts `creation_utc` and the exact Windows
  `/Date(<milliseconds>)/` `creation_time_raw` form.
- A nonterminal present PID without usable creation evidence remains fail-closed
  `MCP_STATE_UNKNOWN`.
- Focused regressions are in `orchestrator_harness/tests/test_reconcile.py`.

No optional-watcher, production-server, experiment-result, MCP/provider, or hardware code was
changed for this repair.

## Verification

- Persistent Terra-high coder focused run: **83 passed**.
- Persistent Terra-high coder complete ordinary primary suite, run once: **136 passed** in
  13.058 seconds.
- Main-manager independent focused controls: **5 passed** (A26 terminal PID reuse, A24 recycled
  PID, raw Windows timestamp, matching live PID, and fail-closed unknown).
- Fresh no-write scan:
  `.agent-workspace/CANARY_CLEAN_G_REPAIR_NO_WRITE_SCAN.json`
  (`70cc27f71c58372346200cccf418515d40511ff9f237c102741f45948dde8a31`).
  Exact historical `a24_pair_a_s1d_mcp`, `a24_pair_b_s1d_mcp`, and
  `a26_counter_s1d_mcp` records all classify `MCP_EXITED`; none classifies
  `MCP_STATE_UNKNOWN`.
- No clean-G prep, firmware test, HIL action, MCP/provider process, optional-watcher test, or
  production-server test was rerun.

## Accepted boundary

The Clean-G repair gate is green. Preserve all four accepted Clean-G board-free prep checkpoints.
The next live work must use a wholly fresh Clean-H config, monitor output, assignments, requests,
relays, lifetimes, and process identities; do not reuse Clean-G authority or rerun its prep.

