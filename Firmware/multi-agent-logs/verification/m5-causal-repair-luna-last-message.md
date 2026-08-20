Smoke testing complete.

- Focused regression:
  `python -m pytest -q harness_watcher_implementation/tests/test_attention.py -k causal_metrics_use_source_time_and_reject_negative_source_order`
  
  Result: `1 passed, 25 deselected`.

- Retained M5 S1 in-memory analysis: all four requested events had nonnegative causal metrics:
  - Atlas: 33.106137s
  - Boreal: 34.445612s
  - Cygnus: 0.0s
  - Delta: 41.439619s

- Inverted source order: correctly failed closed with `negative causal metric: observation_to_actionable_seconds`.

- Native practical:
  `python harness_watcher_implementation/tests/run_attention_practical.py --evidence-dir multi-agent-logs/verification/m5-causal-repair-luna-evidence`

  Result: `PASS`; wake evidence `COMPLETE`; quiet control returned `WATCH_TIMEOUT` with no wake records.

Evidence: [m5-causal-repair-luna-evidence](C:/Users/Jason/Documents/Jason/FirmCLI_Tester/Firmware-Test-Manual/MCP-Trial-3/multi-agent-logs/verification/m5-causal-repair-luna-evidence)

Additional actionable finding: reversing ingestion order across duplicate retained `HARNESS_EVENT_DEFERRED` records can still select a later duplicate and produce negative `explicit_deferral_seconds`; the analyzer fails closed.