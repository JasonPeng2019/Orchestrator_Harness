# Clean-G primary historical-lifetime repair plan

Authority: current root manager  
Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_G.md`  
Scope: primary `orchestrator_harness` only; no optional watcher, production server, experiment,
MCP/provider, or hardware behavior

## Verified defect

The clean-G primary watcher treated two closed clean-D MCP lifetime records as current actionable
process uncertainty when Windows reused their old numeric PIDs:

1. A26's record explicitly says `lifetime_status: closed_before_board_action`. Its real launcher
   and MCP child were absent, but an unrelated reuse of an old nested `parent_pid` with no parsed
   expected creation time produced `MCP_STATE_UNKNOWN`, followed by a second historical
   `MCP_EXITED` notification when that unrelated process exited.
2. A24's record contains the real process creation time in `creation_utc` / `creation_time_raw`,
   but `_local_pid_identities()` accepts only `creation_time_utc`, `started_utc`, or `created_utc`.
   It therefore compared a recycled PID against `None` and produced another
   `MCP_STATE_UNKNOWN`.

This is one shared historical closed-lifetime PID-reuse defect. The optional watcher correctly
reported it; the lane doers, manager, firmware runs, and production server did not cause it.

## Required behavior

Implement the smallest primary-harness correction in `orchestrator_harness/reconcile.py` and
focused tests.

1. An explicitly terminal MCP lifetime record must remain terminal regardless of later numeric
   PID reuse. Recognize only explicit, strict terminal evidence actually supported by the record
   contract (including the observed `closed_before_board_action` value); do not infer closure from
   age, path, epoch name, or mere process absence.
2. When a nonterminal record is reconciled by PID, accept its role-local ISO creation evidence from
   the existing aliases plus `creation_utc`. If only the recorded Windows
   `creation_time_raw: /Date(<milliseconds>)/` form is available, parse that exact form safely.
3. A recycled PID whose observed creation differs from the recorded creation must be a mismatch,
   never `unknown` merely because a supported timestamp alias was ignored.
4. Preserve fail-closed behavior for genuinely live/uncertain nonterminal records: a record with
   no terminal marker and no usable creation evidence still remains `MCP_STATE_UNKNOWN` when its
   PID is present.
5. Preserve current-live lifetime detection, helper/controller reconciliation, event identities,
   discovery/path safety, manager notification semantics, and all retained historical records.
   The repair changes operational classification only; it does not delete or rewrite evidence.
6. Do not suppress all historical MCP events, weaken current-lifetime safety, special-case A24/A26
   paths, or change the optional watcher.

## Focused tests

Add focused regressions, using synthetic process snapshots rather than hardware:

- explicit A26-style `closed_before_board_action` plus a reused nested parent PID is always
  `MCP_EXITED` and cannot transition to actionable unknown/running;
- A24-style top-level `creation_utc` plus a recycled PID is `MCP_EXITED`/mismatch;
- the exact `creation_time_raw` millisecond form is understood when needed;
- A24-style creation evidence plus the matching live PID remains `MCP_RUNNING`;
- a nonterminal live PID with no usable creation evidence remains `MCP_STATE_UNKNOWN`; and
- existing nested `created_utc` and ordinary current-live coverage remain green.

Run the smallest focused reconcile/notification tests first. Then run the complete ordinary
primary host suite exactly once because lifetime reconciliation feeds shared events and manager
notifications. Do not run the optional-watcher suite unless optional-watcher code changes
unexpectedly. Do not rerun clean-G preparation or any accepted firmware/HIL evidence.

## Acceptance and next sprint

Accept only if:

- the focused regressions pass;
- the full primary host suite passes;
- a fresh no-write reproduction using copies of the exact A26 and A24 record shapes cannot emit
  `MCP_STATE_UNKNOWN` or a new actionable transition for a recycled PID;
- current-live and genuinely uncertain records retain their required classifications; and
- the diff contains no optional-watcher, production-server, experiment-result, MCP/provider, or
  hardware edits.

After acceptance, keep all four clean-G preparation checkpoints locked. Create an entirely fresh
clean-H epoch/config/runtime and proceed directly to the live A22/D31/A24/A26 target boundaries;
do not rerun the board-free prep turns merely because the harness changed.
