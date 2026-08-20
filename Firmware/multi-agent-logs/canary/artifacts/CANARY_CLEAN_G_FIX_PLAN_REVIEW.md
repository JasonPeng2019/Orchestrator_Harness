# Adversarial review — Clean-G primary historical-lifetime repair plan

## ACCEPT

The plan is accepted.  It addresses the validated shared defect in the smallest justified primary
surface (`orchestrator_harness/reconcile.py`) and does not weaken the required fail-closed handling
of genuinely live or uncertain lifetimes.

### Verification basis

* The reproducer records show the same failure in two shapes: A26's explicit
  `lifetime_status=closed_before_board_action` was probed through a recycled nested PID, while
  A24's real `creation_utc` / `creation_time_raw` was discarded into a null expected time.  See
  `.agent-workspace/CANARY_CLEAN_G_ISSUES.jsonl` events `f2f2c803…`, `2d8bc0d5…`, and
  `949b065d…`, plus clean-G primary events.
* The plan requires explicit terminal evidence only, prohibits age/path/absence inference, and
  preserves `MCP_STATE_UNKNOWN` for a nonterminal present PID without usable identity evidence.
  That is the necessary safety boundary.
* It preserves PID creation-time comparison for nonterminal records, including the existing
  aliases and the actual `creation_utc` / Windows raw-date forms implicated by the reproducer.
* It explicitly keeps optional watcher, server, hardware, experiment evidence, and scheduling out
  of scope; the clean-G audit found no reason to change them.
* The focused tests cover terminal reuse, creation aliases/raw date parsing, matching current-live
  identities, and fail-closed uncertainty, followed by one ordinary primary-suite run.  They are
  sufficient and avoid unnecessary HIL/preparation reruns.

### Required acceptance checks

Execute the listed focused tests and full primary host suite; verify a no-write copied-record
reproduction emits no active unknown/actionable transition for either closed A26/A24 shape while a
nonterminal unknown record remains `MCP_STATE_UNKNOWN`.  Confirm the diff is confined to primary
reconciliation/tests.  Then start a fresh epoch; retain all clean-G prep checkpoints.

No blocking concern and no advisory polish item is required before implementation.
