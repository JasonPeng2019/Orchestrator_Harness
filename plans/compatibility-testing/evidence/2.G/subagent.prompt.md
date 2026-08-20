# Task: Phase 2, Area 2.G — Watcher recovery projection & condition merging (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** over the real
`orchestrator_harness.watcher_integration` module. No subprocess, no source edits, no
"fix to green". Pin ACTUAL behavior.

> **READ THIS FIRST — PLAN-VS-REALITY DIVERGENCE (you MUST record it as a FINDING).**
> The plan item **A39 / T3** describes a "watcher alert / recovery **ledger**
> (`STOP_ASSIGNING → … → RESOLVED`)" with "each transition admitted only in order". **No such
> ordered state-machine ledger exists in this module.** The module docstring is explicit: "Recovery
> is a small **open/acknowledged/resolved projection only**" and "watcher alerts do not become
> harness queue events". Pin the ACTUAL projection behavior and file the divergence as
> **F2G-A39-1 (note)** — do NOT invent a `STOP_ASSIGNING` ledger or ordered-admission API.

## Where you are

- Working dir: `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run: `cd` there, then
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_watcher_integration -v`

## Code under test — `orchestrator_harness/watcher_integration.py` (read the WHOLE 58-line module)

- `WATCHER_RECOVERY_SCHEMA == "orchestrator-watcher-recovery/v1"`;
  `WATCHER_RECOVERY_STATES == frozenset({"open","acknowledged","resolved"})`.
- `watcher_recovery_projection(records: Iterable[Mapping]) -> dict`: for each record, keep it only
  if `alert_id` is a non-empty str AND `state` (default `"open"`) is in `WATCHER_RECOVERY_STATES`;
  otherwise **silently skip** it. Returns
  `{schema: WATCHER_RECOVERY_SCHEMA, states: [{alert_id, state, observed_utc} …in input order…],
    actionable: [alert_id for rows whose state == "open"]}`. There is NO ordering/transition
  admission and NO STOP_ASSIGNING state.
- `merge_watcher_conditions(snapshot: dict) -> dict[str, dict]`: delegates to
  `orchestrator_harness.events.conditions_from_snapshot(snapshot)` — returns a dict **keyed by
  condition identity** (`"lane:{lane_id}:process"`, and `":coordination-failure"` /
  `":resource-wait"` when those lane fields are present). Two spellings of the same lane collapse
  under the same identity key (dedup by identity; last write wins). This is A31 "condition merging".

## What to build — ONE module `orchestrator_harness/tests/test_compat_watcher_integration.py`

1. **A31 condition merging (PASS):** build a fabricated snapshot
   `{"lanes": [ {lane_id:"L1", operational_state:"RUNNING", process_state:"RUNNING", ...},
   {lane_id:"L2", operational_state:"STALE_STATUS", process_state:"STALE_STATUS", ...} ]}`
   (grep `conditions_from_snapshot` / `PROCESS_EVENT_TYPES` in `orchestrator_harness/events.py`
   to supply the minimal required lane fields — at least `lane_id` and one of
   `process_state`/`operational_state`). Assert `merge_watcher_conditions(snapshot)` is a dict
   keyed by `"lane:L1:process"` and `"lane:L2:process"`, that a `STALE_STATUS` lane yields
   `severity == "error"`, and that **dedup by identity** holds (calling twice, or two lanes sharing
   an id, yields one keyed entry per identity). Then assert a **cleared** condition drops out:
   remove a lane from the snapshot (or drop the `coordination_failure`/`waiting_resource_claim`
   field that produced an extra identity) → that identity key is absent from the new result.
2. **A39 / T3 actual recovery projection (PASS, replacing the non-existent ledger):**
   feed records `[{alert_id:"A1", state:"open", observed_utc:"…"},
   {alert_id:"A2", state:"acknowledged"}, {alert_id:"A3", state:"resolved"}]` →
   assert `schema == "orchestrator-watcher-recovery/v1"`, `states` lists all three in order, and
   **`actionable == ["A1"]`** (only the `open` one). Then assert a resolved alert is present in
   `states` but NOT in `actionable` (i.e. resolving clears it from the actionable set), and that
   invalid records are silently dropped: `{alert_id:"", state:"open"}` (blank id),
   `{alert_id:"A4", state:"STOP_ASSIGNING"}` (state not in the allowed set),
   `{"state":"open"}` (no alert_id), and a non-Mapping like `"nope"` → none appear in `states`.
3. **F2G-A39-1 (the FINDING, record clearly):** there is no ordered `STOP_ASSIGNING → … →
   RESOLVED` ledger and no in-order transition admission; recovery is a stateless
   open/acknowledged/resolved *projection* that filters+labels records with no ordering guard
   (e.g. a "resolved" record with no prior "open" is accepted). Pin this by asserting that a lone
   `{alert_id:"A9", state:"resolved"}` (never previously "open") is accepted into `states`
   (no ordering rejection) — demonstrating the absence of a transition ledger.

Never edit source. If `watcher_recovery_projection` admits a truly invalid `state` string into the
projection, or `merge_watcher_conditions` fails to key/dedup by identity, flag it as HIGHER
severity.

## Pass criterion & regression

- New module green (with F2G-A39-1 documented) under the run command above.
- Regression: `PYTHONPATH="$PWD:$PWD/.." python -c "import orchestrator_harness.watcher_integration, orchestrator_harness.events"`
  confirms clean import. (No dedicated sibling suite; if you find one referencing
  `watcher_recovery_projection`, run it too.)

## Evidence into `.../evidence/2.G/`

- `test-run.log` — `-v` of your new module.

## Final report

Markdown table: **A31** row = PASS (condition merging + dedup + cleared-drops-out); **A39 / T3**
row = PASS for the actual projection PLUS an explicit **F2G-A39-1** FINDING row (no ordered
STOP_ASSIGNING ledger; stateless projection instead). Then exact commands, test count, pass/fail
tally. Do not modify any file outside your new test module and the evidence dir.
