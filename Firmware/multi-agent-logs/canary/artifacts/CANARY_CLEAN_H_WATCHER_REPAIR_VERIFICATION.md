# Clean-H optional-watcher repair verification

Plan: `.agent-workspace/CANARY_CLEAN_H_WATCHER_FIX_PLAN.md`  
Plan review: `.agent-workspace/CANARY_CLEAN_H_WATCHER_PLAN_REVIEW.md` (`PASS`)  
Implementation: same persistent Terra-high coder `/root/canary_harness_coder`

## Scope

Changed only:

- `harness_watcher_implementation/poller.py`
- `harness_watcher_implementation/__main__.py`
- `harness_watcher_implementation/tests/test_watcher_smoke.py`

The background `serve` path now initializes a missing runtime cursor at each existing source's EOF
before its first poll. Existing cursors are untouched. The seeded records contain no historical
tail context. Direct `poll()` is unchanged.

## Coder gate

- focused module: `28/28` passed;
- complete ordinary optional-watcher host discovery: `28/28` passed once;
- no primary harness, real evaluator, agent, server, provider, hardware, or experiment run.

## Independent manager gate

- `python -m unittest harness_watcher_implementation.tests.test_watcher_smoke -v`: `28/28`
  passed;
- `py_compile` for `poller.py` and `__main__.py`: passed;
- fresh synthetic cursor reproduction:
  - preexisting historical defect-shaped bytes skipped;
  - baseline offset exactly equaled preexisting EOF;
  - baseline retained no text context;
  - post-baseline append observed;
  - initialization against an existing cursor was a byte-for-byte no-op; and
  - post-baseline replacement/truncation content observed.

No accepted firmware/HIL evidence or unrelated expensive tests were rerun.

## Status

Implementation and manager verification are green. The same persistent Terra-medium auditor's
bounded post-implementation audit is also `PASS`:
`.agent-workspace/CANARY_CLEAN_H_WATCHER_REPAIR_AUDIT.md`. The repair gate is closed and a fresh
successor canary epoch may start.
