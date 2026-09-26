# Lane 1 — domain and durable state

Lane 1 is the sole writer for the shared memory-harness record and transaction seams: `src/memory_harness/preparation.py`, `apc.py`, `search.py`, `context.py`, `privacy.py`, `runtime.py`, `contracts.py`, `store.py`, and `config.py`. It owns compatible schema changes and publishes the exact interfaces consumed by lanes 2–4. Preserve accepted STEP-04 behavior and the accepted STEP-05 Level 0 slice at cc5b4f2.

Checkpoint commit: finish STEP-05-1 through STEP-08-1 and state the exact outcome, effect-operation, and usage identities and status meanings needed by the other lanes. Focused tests must pass. This is a tested core checkpoint, not a claim that STEP-09–15 or the whole product is complete.

After pinning that commit, continue STEP-09-1, STEP-10-1, STEP-11-1, STEP-13-1, STEP-14-1, and STEP-15-1 without waiting for checkpoint integration. A change to a published interface requires notifying its consumers and repinning affected evidence. Only ROOT combines lane commits in the separate integration worktree. See [PLAN.md](../../PLAN.md) for ownership, checkpoint, and final proof rules.

Every worker and reviewer card must also name [NORMAL_OPERATION_ACCEPTANCE.md](../../NORMAL_OPERATION_ACCEPTANCE.md). Repair only reproduced normal-use, supported-recovery, compatibility, or critical-invariant defects; report other confirmed findings for the shared known-issues register without a correction loop.
