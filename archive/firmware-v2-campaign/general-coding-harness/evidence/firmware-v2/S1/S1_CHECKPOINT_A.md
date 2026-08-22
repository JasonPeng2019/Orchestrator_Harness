# S1 Checkpoint A

Status: **GREEN; S2 UNLOCKED**  
Recorded: `2026-08-04T01:35:31.6379390Z`

- Candidate branch/worktree: `firmware/v2-candidate` at
  `5d7c36e3dd38dc813c91f4462f4298c73883c59a`, clean.
- Persistent product branch: `firmware/v2-s1-product` at the same revision, clean.
- Accepted product/reviewer/test-author joins: `S1_CA.md`, `S1_JR.md`, and `S1_JA.md`.
- Final test join and selective-retest decision: `S1_JT.md`.
- Stable test registry:
  `plans/general-coding-harness/runtime/firmware-v2/passed-tests.json`, SHA-256
  `06dddcb44d804bc2114b41d9554dc72b66c2406ca1ff78fac91c7645b7123cce`.
- Dependency map: `SHARED_CODE_DEPENDENCY_MAP.json`, SHA-256
  `dbe652b34b7e61710de98784878b2fc9fe77089f2a2d4f8c3c33021fa6cbfa52`.
- Test-ID scheme represented here: retained baseline node IDs, new route/lifecycle node IDs, and
  `S1::ruff::firmware-route-compatibility` for the affected static check.
- C9-C18 are covered by the accepted route loader/result implementation, retained fixtures/docs,
  production characterization, and cross-route tests.
- C19-C30 are covered by retained exact-lifecycle behavior plus dependency-mapped controller,
  cleanup, integration, route, and lifecycle tests; S2 owns the new physical MCP substrate beyond
  this no-hardware boundary.
- The S1 portion of C73 is covered by the 248-ID baseline manifest, conservative changed-file map,
  all 19 invalidated protected IDs green, nine new S1 unit IDs green, no deleted/skip/expected-fail
  baseline ID, and no assertion weakening.
- All exact S1 controllers and Codex workers exited and were reaped; claims and actionable
  notifications are empty.
- Hardware mutation: none.
- Next gate: `S2.P` from exact candidate revision
  `5d7c36e3dd38dc813c91f4462f4298c73883c59a` under the fixed S2 two-loop topology.
