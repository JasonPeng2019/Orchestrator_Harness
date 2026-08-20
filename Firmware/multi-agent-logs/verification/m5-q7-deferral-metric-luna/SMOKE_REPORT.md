# M5 Q7 deferral-metric smoke report

Date: 2026-08-02  
Tester: independent GPT-5.6-luna practical smoke test  
Scope: host-only; no hardware, providers, MCP, wrappers, relays, or subagents used. The requested repository practical entry point was invoked directly.

## Result

**PASS**

The repaired `_deferral_duration` uses only deferrals whose source time is at or before pending and selects the latest eligible endpoint.

- Pre-pending deferral: `explicit_deferral_seconds = 6.0` (nonnegative). **PASS**
- Post-pending-only deferral: `explicit_deferral_seconds = None`; no invented negative metric or contradiction. **PASS**
- Reversed independent causal stage (`HARNESS_SIGNAL_OBSERVED` before `AGENT_SIGNAL_CREATED`): classification `INSUFFICIENT_EVIDENCE` with `negative causal metric: signal_to_observation_seconds`. **PASS**

## Commands and results

| Check | Exact command | Result |
|---|---|---|
| Focused Q7 pytest | `$env:PYTHONUTF8='1'; pytest -q harness_watcher_implementation/tests/test_attention.py::AttentionContractTests::test_explicit_deferral_metric_requires_pre_pending_endpoint` | **PASS** — `1 passed in 0.06s`, exit `0` |
| Watcher suite | `$env:PYTHONUTF8='1'; pytest -q harness_watcher_implementation/tests` | **PASS** — `96 passed, 27 subtests passed in 12.07s`, exit `0` |
| Host-only attention practical | `$env:PYTHONUTF8='1'; python -m harness_watcher_implementation.tests.run_attention_practical` | **PASS** — printed `attention practical host-only check: PASS ...`, exit `0` |
| Changed-file compile | `$env:PYTHONUTF8='1'; python -m py_compile harness_watcher_implementation/attention.py` | **PASS**, exit `0` |
| Package compile | `$env:PYTHONUTF8='1'; python -m compileall -q harness_watcher_implementation` | **PASS**, exit `0` |

No production code or requirements were edited. No commit or push was performed.
