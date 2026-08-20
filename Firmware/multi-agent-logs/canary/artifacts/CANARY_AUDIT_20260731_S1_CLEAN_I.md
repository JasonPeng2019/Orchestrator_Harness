# Clean-I independent canary audit — `20260731-s1-clean-i`

## Counting verdict

**NON-COUNTING; counter remains `0/3`.**  None of the four declared endpoints
was reached: Atlas stopped before B14, Boreal stopped before RST01,
Cygnus stopped before either MCP lifetime, and Delta stopped before MCP
initialization/counter measurement.  In addition, the primary harness produced
validated false resource/correlation warnings.  The bounded attempts and their
cleanup evidence remain useful; this verdict does not authorize a retry in any
consumed lifetime.

## Classification by area

| Area | Classification | Evidence/disposition |
|---|---|---|
| Primary harness | **DEFECTS VALIDATED** | The three correlation/lifecycle findings below are real false-positive behavior, not a server or hardware condition. |
| Optional watcher | **NONISSUE / EXPECTED TRANSIENT** | `watcher/events.jsonl` starts with `evaluated:false`, then has eight new-activity evaluations, each `defect:false`; it stops cooperatively.  The Clean-H historical-content startup defect is not reproduced. |
| Manager/orchestrator | **PROCEDURE DEFECT, non-counting** | The original Cygnus prep used an ambiguous relative target path; the live prompt corrected it.  The D31 HELP sequence was relayed before the recorded deadlines, and the manager acknowledged every harness notification. |
| Doer/run-local | **DEFECTS, bounded and correctly stopped** | Atlas called populated `board_setup-plan` before the required null initialization; Boreal treated terminal `setup_completed` with no redirect as an error; Cygnus's loader failed to register its module before dataclass evaluation; Delta compared equivalent slash spellings without normalization.  Each used one attempt and did not retry. |
| Server | **NO VALIDATED DEFECT** | Atlas's required null setup-plan gate and D31's `setup_completed` response are truthful server behavior.  No production-server repair is supported. |
| Hardware | **NO VALIDATED DEFECT / no unsafe action** | Atlas, Cygnus, and Delta reached no board action.  D31 completed the bounded setup/fix route only; no RST01, APP-1, flash, or RF work ran.  Final scan reports no resource conflict, duplicate attempt, observation/process error, or remaining exact lane process. |

## Primary-harness and watcher findings

1. **VALIDATED_DEFECT — historical Clean-H resource ambiguity woke the new epoch.**
   At Clean-I bootstrap the primary state recorded event
   `6562a47a...`, a `RESOURCE_AMBIGUOUS` for
   `20260731-s1-clean-h:Atlas:A22`, although that was historical
   Clean-H state.  It was later cleared, but the startup notification violated
   the epoch-baseline expectation.  The underlying lifecycle rule is visible in
   `reconcile.py`: it synthesizes a missing-MCP ambiguity from declared MCP
   names without requiring a current/live relevant lifetime, while notification
   priority treats `RESOURCE_AMBIGUOUS` as actionable.  This is not an optional
   watcher alert; the optional watcher correctly skipped its initial history.

2. **VALIDATED_DEFECT — D31 request correlation admits historical work through a reused session.**
   The Clean-I D31 route has four current, exact HELP/request/relay records in
   `.../d31-rst01-s1-clean-i/evidence/20260731T194545Z/final-record.json`.
   Nevertheless primary state retained a Clean-F request in the Clean-I D31
   activity/history and emitted the no-current-request resource ambiguity
   (`838f774b...`).  `active_management._is_lane_match` falls back to session
   equality even after a record declares a different lane, unlike
   `reconcile._record_belongs_to_lane`, which correctly makes an explicit lane
   authoritative.  That code and the captured state validate the defect.

3. **VALIDATED_DEFECT — terminal pre-MCP lanes are reported as missing MCP lifetimes.**
   A24 and A26 truthfully checkpointed before MCP creation: A24's checkpoint
   records the import/dataclass failure and no provider/MCP lifetime; A26's
   `s1i-bounded-functional-stop.json` records the pre-provider launcher gate.
   The final snapshot nevertheless retains `MCP_STATE_UNKNOWN`/missing declared
   MCP-lifetime ambiguity for both, producing events `01b65ebd...` and
   `5f1a5666...`.  This follows the unconditional `missing_mcp_names` branch in
   `reconcile.py`; it is a false lifecycle expectation, not a leak/conflict.

4. **NONISSUE / EXPECTED_TRANSIENT — early active-lane "no current request"
   notices before a request identity is published.**  The first short windows
   for Atlas/Boreal/Cygnus/Delta had no current request yet.  They are useful
   advisory observations while a live lane is genuinely awaiting its first
   request; they are not evidence of a resource conflict.  They must not be
   confused with findings 1–3 or promoted into a counting failure on their own.

5. **NONISSUE / EXPECTED_TRANSIENT — optional watcher activity.**  The repaired
   watcher recorded its baseline poll as unevaluated and only assessed appended
   activity afterward; all evaluator outcomes were `defect:false`.  No watcher
   alert, stuck PID, or cleanup failure exists.

## Repair decision and narrowest scope

**A primary-harness repair is justified; no watcher, controller, or server
repair belongs in that change.**  Limit it to epoch/request/lifecycle
correlation in `orchestrator_harness` and focused synthetic tests:

1. make active-management matching honor an explicit, different
   `declared_lane_id` before any session fallback, and prefer the exact current
   Clean-I request/signal identity for an active lane;
2. gate missing-MCP-lifetime ambiguity on an MCP lifetime that is actually
   expected/claimed by the current lane, suppressing terminal, explicitly
   pre-MCP checkpoints while retaining detection for a live/claimed lifetime;
3. prevent stale/inactive-epoch resource ambiguities from becoming actionable
   bootstrap notifications.

The repair must preserve genuine active-lane resource conflict, missing-live-MCP,
and request-expiry detection.  Do not broaden it into deleting historical
observations or changing server route semantics.

## Successor prerequisites (without rerunning accepted evidence)

1. Implement and adversarially test the narrow primary-harness repair with
   synthetic controls for: historical explicit-lane request versus reused
   session, current Clean-I HELP/request selection, terminal pre-MCP A24/A26,
   genuine live missing-MCP, and a clean epoch bootstrap.
2. Retain all Clean-I lane, setup, cleanup, watcher, and accepted prior evidence;
   do **not** rerun any consumed Clean-I lifetime or accepted preparation.
3. Before a new counting epoch, complete only the run-local corrections and
   host proofs for the four lane-specific failures, then issue fresh assignments
   and fresh lifetimes.  Atlas must begin with null setup-plan; Boreal must
   accept terminal setup completion and then request RST01; Cygnus must register
   the dynamically loaded module; Delta must use the normalized launcher guard.
4. Start a fresh managed/optional watcher epoch only after the repair accepts
   the synthetic controls; the next audit should require no stale actionable
   history, no false terminal pre-MCP ambiguity, and the normal exact cleanup
   evidence.
