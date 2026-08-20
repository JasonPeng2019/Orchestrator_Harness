# M5 Q5 temporary-signal discovery repair

Validated: `2026-08-02`  
Verdict: **REPAIR ACCEPTED**

Q5 proved that a hidden atomic staging file such as `.sig-....tmp.json` could be discovered as a
final manager signal and then rediscovered under a different native event ID after final rename.
The native discovery path now excludes hidden and `*.tmp.json` signal files before parsing while
preserving ordinary final JSON and existing identical-final duplicate compatibility.

Root rejected a broader wake-transport change: `MANAGER_WAKE_DELIVERED` records successful native
stdout delivery; `MANAGER_WAKE_RECEIVED` separately records when root notices that output. Their
separation is intentional and is the evidence needed to measure manager-attention delay.

Verification:

- Terra coder focused suite: **36 passed, 11 subtests passed**.
- Independent Terra review: **accepted; no concrete defect**.
- Luna practical smoke: **PASS** (`multi-agent-logs/verification/m5-q5-temp-signal-luna/`).
- Full native harness suite: **208 passed, 1 skipped, 15 subtests passed**.
- Full watcher suite: **95 passed, 27 subtests passed**.
- Host-only attention practical: **PASS**.
- Compileall: **PASS**.
- No hardware, provider, MCP, wrapper, runner, relay, commit, or push was used.

The repaired 68-file Python surface is frozen in
`multi-agent-logs/current-state/M5_PYTHON_BASELINE.json`, whose SHA-256 is
`139bfdff4132e5cc7a9c58cd03c884046d4e88652b246ed9d3265a13c4d60577`.
