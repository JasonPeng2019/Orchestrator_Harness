# Task: Phase 2, Area 2.F — Attention-sprint historical decoder (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** over the real
`orchestrator_harness.attention_sprint` module. No subprocess, no source edits, no "fix to green".
Pin ACTUAL behavior.

## Where you are

- Working dir: `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run: `cd` there, then
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_attention_sprint -v`
- There is **no** `test_attention_sprint.py` model fixture — write from scratch, `import`ing from
  `orchestrator_harness.attention_sprint`.

## Code under test — `orchestrator_harness/attention_sprint.py` (read the WHOLE 44-line module)

`decode_historical_attention_record(value: Mapping[str, Any]) -> dict` returns a **bounded inert
projection** of one legacy record. Behavior:
- `HISTORICAL_ATTENTION_SCHEMA == "orchestrator-historical-attention-record/v1"`; `_MAX_RECORD_KEYS == 32`.
- If `value` is not a `Mapping` OR `len(value) > 32` → `ValueError("historical attention record is
  oversized or malformed")`.
- `event_id = value.get("event_id")`, `kind = value.get("kind")`. If either is not a non-empty
  (post-`.strip()`) `str` → `ValueError("historical attention record has no bounded identity")`.
- Otherwise returns exactly:
  `{schema: HISTORICAL_ATTENTION_SCHEMA, event_id, kind,
    observed_utc: value.get("source_timestamp_utc") or value.get("observed_utc"),
    historical_only: True, actionable: False, acknowledgeable: False}`.
- **Note the intent (module docstring):** it is inert — never actionable, never acknowledgeable,
  no validator/selector/timeline/heartbeat. It only extracts a bounded identity + timestamp.

## What to build — ONE module `orchestrator_harness/tests/test_compat_attention_sprint.py`

1. **A30 / T6 valid decode:** feed a valid record
   `{"event_id":"E-1","kind":"stall","source_timestamp_utc":"2026-01-02T03:04:05+00:00", ...a few
   extra harmless keys...}` → assert the returned dict has `schema ==
   "orchestrator-historical-attention-record/v1"`, `event_id == "E-1"`, `kind == "stall"`,
   `observed_utc == "2026-01-02T03:04:05+00:00"`, and **`actionable is False` and
   `acknowledgeable is False` and `historical_only is True`** (the inertness guarantee). Also
   assert the `observed_utc` fallback: a record with only `observed_utc` (no
   `source_timestamp_utc`) returns that value; a record with neither → `observed_utc is None`.
2. **A30 / T6 corrupt/oversized decode → clear error (no silent partial):** each of the following
   raises `ValueError` (assert the message distinguishes the two guard classes where relevant):
   - not a Mapping: pass a `list`, a `str`, `None`.
   - oversized: a dict with 33 keys (incl. valid event_id/kind) → the "oversized or malformed" guard.
   - missing/blank identity: `{}`; `{"event_id":"E-1"}` (no kind); `{"kind":"stall"}` (no event_id);
     `{"event_id":"  ","kind":"stall"}` (blank after strip); `{"event_id":"E-1","kind":123}`
     (non-str kind). Each → the "no bounded identity" guard.
   Assert that NO partial/half-populated dict is ever returned on these paths (the call raises).

Never edit source. If a malformed record decodes to a partial dict instead of raising, or if any
returned projection is ever `actionable`/`acknowledgeable` True, that is a FAIL-OPEN / correctness
issue, HIGHER severity — flag it loudly.

## Pass criterion & regression

- New module green under the run command above.
- Regression (sanity, module imports cleanly): re-run the new module a second time, or run
  `PYTHONPATH="$PWD:$PWD/.." python -c "import orchestrator_harness.attention_sprint"` and confirm
  no error. (There is no sibling model suite to regress.)

## Evidence into `.../evidence/2.F/`

- `test-run.log` — `-v` of your new module.

## Final report

Markdown table with an **A30 / T6** row = PASS (valid decode + inertness + fail-closed on
corrupt/oversized) or FINDING if anything differs. Then exact commands, test count, pass/fail
tally. Do not modify any file outside your new test module and the evidence dir.
