# M5 Q8 publication-evidence repair

Validated: `2026-08-02`

Q8 proved that creation-before-exposure ordering needed one more passive causal boundary. The
watcher could otherwise blame the harness for time when final JSON was still unavailable.

The watcher/logger now supports `AGENT_SIGNAL_PUBLISHED` and exact captured
`--source-timestamp-utc`. Blocked-signal harness attribution requires one correlated publication
ordered creation <= publication <= observation and publication <= delivery deadline. Missing,
duplicate, mismatched, reversed, or post-deadline publication is insufficient evidence, never a
fabricated harness delay.

Verification:

- Terra coder focused: **36 passed, 3 subtests**.
- Independent Terra review: **PASS**; watcher **98 passed, 27 subtests**; practical **PASS**.
- Independent Luna high practical smoke: **PASS**.
- Root combined suite: **306 passed, 1 skipped, 42 subtests**.
- Luna separate suites: harness **209 passed, 1 skipped**; watcher **98 passed**.
- Attention practical and compileall: **PASS**.

Evidence: `multi-agent-logs/verification/m5-q8-publication-luna/SMOKE_REPORT.md`.
No runner, wrapper, relay, evaluator, hardware, provider, MCP, deploy, flash, commit, or push was
used. The comparable count remains 0/3; attempt 9/10 is next.
