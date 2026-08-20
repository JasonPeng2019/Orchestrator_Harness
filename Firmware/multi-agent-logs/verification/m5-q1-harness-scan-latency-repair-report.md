# M5 Q1 harness scan-latency repair verification

Status: **READY**

Verified defect: duplicate recursive workspace traversal caused a real Delta request to miss its 90-second delivery deadline in `20260802-m5-q1-115933Z`.

Repair: `orchestrator_harness.discovery.discover_run` now performs one `os.walk` per workspace, collects only the fixed helper/MCP record names from both file and directory candidates, globally sorts them, and preserves stable reads, arbitrary nesting, and class-specific errors. It adds no cache, index, config, wrapper, relay, or run-specific path rule.

Evidence:

- Focused discovery/reconcile: 74 passed.
- Full harness: 202 passed, 1 skipped.
- Full deterministic watcher: 95 passed.
- Attention practical: PASS.
- Compileall: PASS.
- Independent Terra review: no actionable findings after one valid directory-candidate correction.
- Independent Luna practical smoke: PASS; real four-root scans 28.805s and 18.821s versus 43.217s pre-repair; successful snapshot schema both times.
- Root real scans: 24.194s and 17.931s.
- Targeted Pyright retains one pre-existing unrelated nullable comparison at discovery.py:155; no new diagnostic from the repair.
- Autonomy audit: PASS.

Comparable count remains 0/3 and is refrozen on the repaired Python surface.
