# S2 Checkpoint A

- Decision: `PASS`; S2 is complete and only S3 is unlocked.
- Candidate/product tip: clean `7a28b186e91f2945ea9c59869a216fa8caf8407e`.
- Pinned MCP candidate: clean `f003f84a7df51cd8595a3203c62e225b21da2a22`.
- Hardware boundary: no physical MCP, flash, reset, debug, serial, probe, RF, or board operation occurred.
- Runtime boundary: all S2 controllers are terminal and all resource claims are released.

## Accepted execution evidence

- D1 host shard: `S2_A1_001` and `S2_A1_002`, 2/2 pass. Test-report SHA-256:
  `6ee989a1fc14b2c4ac3dff222e7dd1d4da37d37f6d13e3beb429d67b8478f6e3`.
- D2 target shard: `S2.A2.T1` through `S2.A2.T3`, 3/3 pass. Test-report SHA-256:
  `a16e9051b5fb0e0c50e319c8daba11677a26b1be9e23d4f9d6628123b611a79a`.
- Protected shared-code continuation: exactly 19/19 dependency-invalidated original IDs passed in
  dependency-map order with no skips, expected failures, or unexpected successes. ROOT triage
  SHA-256: `f65fe5c891b34c859fcc3ea52f042d6f3bcf8225a536d95185dbb966c91efe03`.
- Final S2.P exact-tip envelope SHA-256:
  `ef6afec76d93e769908ebc4523ff2fb1144b139bfcada9c21c372488ec2b19c6`.

The protected continuation reran only the 19 IDs invalidated by S2's shared-code dependency map.
The already-green two-ID host shard and all unrelated green tests retained their recorded credit.
No finding requested a repair; ROOT independently applied the codebase-breaking,
functionality-breaking, or clearly-worth-the-cost threshold and accepted the empty finding sets.

S3 must now produce the operator-ready dual-path release surface and disposable integration proof.
C0, all physical authorization, and C3 remain locked until their explicit later gates.
