# STEP-15-2 — Expose thin operator commands

This step is a derivative of [original STEP-15](../../source-steps/STEP-15-operator-controls-expose-truth.md).

Owner: lane 2. This is the complete product operator-entrypoint assignment.

Use the existing harness operator entrypoint for setup, native launch, and concise readiness/status/recovery commands. Project lane 1's exact domain state plus installed composition, provider binding, network enforcement, usage, snapshot, and pending-operation information into actionable output without secret values. Delegate domain recovery by exact operation ID; do not duplicate ROOT approval, scheduling, or review authority. Document minimal supported invocation at the real entrypoint.

This surface preflights the integrated local/install, live Atlas, and nested native proof steps. Do not add a dashboard or parallel scheduler.

Evidence: focused operator-launch tests for ready and blocked states, installed payload, pending/uncertain next action, no credential leak, and non-mutating reads.

Through the existing harness entrypoint expose setup, preparation/finalization, native launch, requested/effective network state, pending/recovery, snapshot, and usage actions or reads. Route each to its existing owner: setup and launch remain harness-owned; exact preparation, outcome, recovery, snapshot, and usage state come from lane 1's domain facade. Show exact build/root, installed composition, compatible schema, service/provider binding availability, feature and network enforcement source, pending operation IDs, and one actionable next step without secret values. A missing dependency blocks only its action. Snapshot mutation and recovery require explicit operator authorization; readiness and usage reads do not mutate task state or trigger implicit effects. Choose concrete command names only as an automation consumer needs them and document the minimal invocation at the real entrypoint. Run and extend lane-2-owned `harness/orchestrator_harness/tests/test_operator_launch.py` for ready/blocked, pending/uncertain, supported recovery/snapshot/usage, no credential leak, and non-mutating reads; run lane 1's domain-readiness selector read-only where relevant. Do not duplicate ROOT approval, scheduling, or review.

For a revisit, repair only the changed domain-to-operator projection or command presentation and rerun focused operator/readiness checks. Revisit only the integrated proof step whose preflight consumed the changed result.
