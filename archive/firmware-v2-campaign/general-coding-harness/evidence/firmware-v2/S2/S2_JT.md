# S2.JT executor join

- Exact joined revision: `7a28b186e91f2945ea9c59869a216fa8caf8407e`
- D1 profile: GPT-5.6 Luna, high reasoning, default tier
- D2 profile: GPT-5.6 Luna, high reasoning, default tier
- Both lanes used isolated clean worktrees and mandatory `test_executor` finding gates.

## D1 host/MCP/isolation shard

- Command: `python -m unittest orchestrator_harness.tests.test_firmware_acceptance_host -v`
- Stable IDs: `S2_A1_001`, `S2_A1_002`
- Outcome: 2 passed; 0 failed/skipped/expected-failure.
- Result SHA-256: `cef745f37f51655410b1b3b043c627ebf5e338dec62f68987e7fb499ba9a6dbe`
- Empty findings SHA-256: `1129c40634460358770700be1cc44140f6dbf95cba56ca3131a759bbdcc7093b`
- Test report SHA-256: `6ee989a1fc14b2c4ac3dff222e7dd1d4da37d37f6d13e3beb429d67b8478f6e3`
- Reported dependency fingerprints: `6d1e5317...` and `58950773...`.

## D2 target/evidence/selective-rerun shard

- Command: `python -m unittest orchestrator_harness.tests.test_firmware_acceptance_target -v`
- Stable IDs: `S2.A2.T1`, `S2.A2.T2`, `S2.A2.T3`
- Outcome: 3 passed; no failure or skip.
- Result SHA-256: `87750b8419f7d1762f09e9f8c1d144ab9021f053a25a7687913d32361a64cb2f`
- Empty findings SHA-256: `9098e4ec9a7ee23b0a84432490d8017b8801c98d3a0b149b189e9723de4d31db`
- Test report SHA-256: `a16e9051b5fb0e0c50e319c8daba11677a26b1be9e23d4f9d6628123b611a79a`
- Reported dependency fingerprints: `965a4e2b...`, `fd6ede60...`, and `86e1febe...`.

Both gated finding sets are empty. ROOT-IM therefore has no gap to triage or route. Prior green
product/review/author IDs remain credited and were not rerun outside the topology-required independent
executor shards. Both exact controller/Codex identities exited normally, all test-shard claims were
released after exit, the resource-lock root is empty, and the watcher scan reports no process,
resource, MCP, or observation error.

No physical MCP, pyOCD, serial, probe, flash, reset, debug, RF, or hardware operation occurred. S2.JT
accepts the joined revision and returns it to S2.P only for a new exact-tip result envelope; no code
or test change is authorized.

## Post-join protected-baseline continuation

The final S2 merge changed shared `orchestrator_harness/lane_controller.py`, invalidating exactly the
19 protected baseline IDs named by `SHARED_CODE_DEPENDENCY_MAP.json` (SHA-256
`dbe652b34b7e61710de98784878b2fc9fe77089f2a2d4f8c3c33021fa6cbfa52`). ROOT retained the already-
green two-ID host shard and resumed the same S2.D1 Luna-high thread through the pinned clean detached
`4699d27` implementation runner.

The first real pinned attempt failed before Codex launch with `No module named '_ctypes'`; its exact
receipt/status are preserved in `D1_RESUME_ATTEMPT_1.json`. The outer runner's Windows standard-
library extension-root isolation was minimally repaired, independently reviewed, and the ordinary
repository verifier returned `VERIFY: PASS` before retry.

Attempt 2 passed all 19/19 dependency-invalidated IDs in exact dependency-map order at clean tip
`7a28b186e91f2945ea9c59869a216fa8caf8407e`; no skip or expected failure occurred. Result SHA-256 is
`e367e2feed36f2f39321e7aa547a663e4c090decc6146c557e1e3bd3874c973c`, empty findings SHA-256 is
`1129c40634460358770700be1cc44140f6dbf95cba56ca3131a759bbdcc7093b`, and test-report SHA-256 is
`4206af8f3e76c0827f86533e14f436c423ce8b4ad527d09a68be212fb24b5340`. Because the fixed runner
predates automatic finding-gate enforcement, ROOT independently compared the exact 19-ID set,
validated the empty finding envelope, accepted the result in `S2_D1_PROTECTED_TRIAGE.json`, and
confirmed zero remaining claims. No MCP or hardware operation occurred.
