# M5 Q1 harness scan-latency Luna smoke

**Result: PASS**

Scope was host-only harness validation. No production code was edited.

## Checks

- `python -m unittest orchestrator_harness.tests.test_discovery -v` - PASS; 1 test.
- `python -m unittest discover -s orchestrator_harness/tests -p 'test*.py' -v` - PASS; 202 tests, 1 intentional skip, 29.698 s.
- `python -m py_compile orchestrator_harness/discovery.py` - PASS.
- `pyright orchestrator_harness/discovery.py` - FAIL with one existing nullable-comparison diagnostic at `discovery.py:155` (`parse_utc(...)` values); unrelated to the repaired recursive discovery traversal. No other diagnostics.

## Real scans

Command used for both measurements:

```text
python -m orchestrator_harness --config multi-agent-logs/orchestrator-harness/20260802-m5-q1-115933Z/config.json scan --no-write
```

1. Exit 0; 28.805 s; JSON schema `orchestrator-watcher-snapshot/v1`.
2. Exit 0; 18.821 s; JSON schema `orchestrator-watcher-snapshot/v1`.

Both scans produced successful snapshots. The 18.821-28.805 s range is materially below the 43.217 s pre-repair reproducer and has substantial margin under the 90 s target.
