# Lane 3 — experience and EverOS

Lane 3 is the sole writer for src/memory_harness/experience.py, everos_adapters.py, and their focused tests. It consumes lane 1's exact outcome/effect/usage contracts and does not edit shared contracts.py, store.py, runtime.py, or config.py. It preserves accepted reviewed-experience provenance and generated-skill approval gates.

Checkpoint commit: provide independently testable local/remote adapter behavior and deterministic fault cases from STEP-09-3, STEP-10-3, and STEP-13-3. Do not claim outcome-linked effect completion before the shared outcome/operation records are combined. Pin the tested commit and continue. After the checkpoint, finish those same steps against the published lane 1 interface without waiting for checkpoint integration. Supply EverOS dependency and readiness facts for the lane 1 snapshot and lane 2 operator projection.

See [LANE_GUIDE.md](../../LANE_GUIDE.md) for the nonblocking checkpoint and final merge.
