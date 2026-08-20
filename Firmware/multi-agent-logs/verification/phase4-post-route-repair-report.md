# M4 readiness rerun after watcher routing repair

Date: 2026-08-02  
Root disposition: **READY**

The reset-epoch watcher defects were repaired, independently reviewed clean,
and practically smoked by Luna. The required M4 host-only wake gate was then
rerun against the repaired code with a fresh retained evidence directory.

## Results

- Real host-only blocking-wait practical: PASS, exit 0.
  Evidence: `phase4-wake-evidence-post-route-repair/`.
- Retention reconstruction test: 1 passed.
- Orchestrator harness suite: 195 passed, 1 intentional skip.
- Deterministic watcher suite: 93 passed.
- Pyright on the affected harness/watcher files: 0 errors.
- Compileall on harness, watcher, common, and orchestration helpers: PASS.
- Independent Terra repair review: CLEAN.
- Luna real optional-watcher-owner topology smoke: PASS at
  `m5-watcher-repair-luna/REPORT.md`; scalar and oversized records were bounded,
  later valid records routed, 12 evaluator skips were recorded, no evaluator
  sentinel appeared, and exact owner/service identities were absent after
  cooperative stop.

## Root audit

The repair did not add a wake path or evaluator. It prevents diagnostic routing
input from terminating the watcher and rejects forged canonical provenance at
the producer boundary. The fresh practical still reconstructs the six-stage
blocking-wait chain and quiet timeout. M5 may restart from `0/3`; old reset
epochs remain non-counting evidence.
