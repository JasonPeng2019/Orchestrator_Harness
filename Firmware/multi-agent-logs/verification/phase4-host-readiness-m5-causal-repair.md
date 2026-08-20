# M4 host-only readiness rerun — M5 causal-metrics repair

Date: 2026-08-02

## Root result

**READY.** The focused diagnostic-watcher repair is independently reviewed, practically tested,
and green across the affected full surface. No hardware, provider, MCP, evaluator, relay, runner,
commit, or push was used.

## Independent review

The persistent Terra reviewer reported no actionable or advisory findings. It verified that causal
durations use `source_timestamp_utc`, genuinely negative causal intervals become named
contradictions and `INSUFFICIENT_EVIDENCE`, and the two required regression cases are present.

## Luna practical

External GPT-5.6-luna, high reasoning, default tier ran the focused host-only smoke. Durable output:

- `multi-agent-logs/verification/m5-causal-repair-luna.jsonl`
- `multi-agent-logs/verification/m5-causal-repair-luna-last-message.md`
- `multi-agent-logs/verification/m5-causal-repair-luna-evidence/`

Results:

- focused causal regression: `1 passed, 25 deselected`;
- retained M5 events: nonnegative causal metrics under the repaired analyzer;
- inverted source order: named negative-metric contradiction and fail-closed classification;
- native wake practical: `PASS`, wake evidence `COMPLETE`;
- quiet control: `WATCH_TIMEOUT`, no wake records.

The Luna tester also reversed observed timestamps across repeated records from one ordered source
and observed a fail-closed negative `explicit_deferral_seconds`. The root rejects this as a repair
finding: the canonical ingester preserves byte order within one source, and the synthetic mutation
does not represent a reachable ingestion ordering. The analyzer still failed closed rather than
misreporting success.

## Root verification

Commands and results:

```text
python -m unittest discover -s orchestrator_harness/tests -t . -q
Ran 195 tests — OK (skipped=1)

python -m unittest discover -s harness_watcher_implementation/tests -t . -q
Ran 94 tests — OK

python -m pyright orchestrator_harness/cli.py harness_watcher_implementation/attention.py
0 errors, 0 warnings, 0 informations

python -m compileall -q orchestrator_harness harness_watcher_implementation harness_common scripts/orchestration
exit 0
```

No practical, harness, or watcher Python process remained afterward.

Key SHA-256 values:

| File | SHA-256 |
|---|---|
| `orchestrator_harness/cli.py` | `2ABF70FD743B8714DB9EFFA6A18A6CA99395CC63B56420A14DFA8CB93789898A` |
| `harness_watcher_implementation/attention.py` | `C55A11798B9A4B4076ED7D9B306681BD4E8DCB1AC843B83C4A4AC493BCC35898` |
| `harness_watcher_implementation/tests/run_attention_practical.py` | `203B672FBE2B5FE782BDDC562714FB769B0E80C0F09B057CC1B3CB715F51A78A` |
| `harness_watcher_implementation/tests/test_attention.py` | `16B2374B6EF5AA476BDBC6859AA284191426D868EAEC7819D78054F85739DC44` |

M5 must refreeze this repaired surface and restart its accepted count at 0/3.
