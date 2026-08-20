# Luna practical watcher repair report

Result: **PASS**

- Practical isolated runtime: runtime/
- Practical topology: one JSONL source, evaluator disabled, sentinel command configured and absent.
- Owner: hidden external scripts/orchestration/optional_watcher_owner.ps1; exact PID plus creation identity retained.
- Routing: scalar rejected, routed wrapper over 65,536 bytes rejected once, following valid record routed, and later append routed.
- Continuity: owner and watcher exact identities remained live across multiple poll cycles.
- Shutdown: stop token used; exact owner and watcher identities absent afterward; no broad process kill used.
- Focused tests: harness_watcher_implementation.tests.test_watcher_smoke => PASS.

Evidence: raw config/source/service/events/identity/process checks and command results are under runtime/.
