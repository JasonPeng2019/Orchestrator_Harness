# STEP-13-3 — Enforce EverOS task-path gates

This step is a derivative of [original STEP-13](../../source-steps/STEP-13-network-modes-are-enforced.md).

Owner: lane 3. This is the complete EverOS task-path gating assignment.

At EverOS experience, generated-skill, and submission entrypoints enforce lane 1's resolved feature and network state before work. All-off performs no optional EverOS task call. An unavailable service is reported as an outage, not as a permission decision. Previously submitted work retains its original configuration and uncertain state; no feature switch silently retries it. Keep explicit authorized safety/maintenance separate from ordinary task work.

Evidence: count actual forbidden calls in all-off/restricted profiles, exercise pending-write suppression and late acknowledgement, and report effective readiness without exposing credentials.

Consume the resolved per-objective requested/effective profile, enforcement source, captured configuration, and Feature Spec Section 15 switches. Gate reviewed-experience retrieval, generated-skill behavior, ingestion, publication, and pending retries before actual adapter work; a returned-content filter is insufficient. All-off makes no optional EverOS/APC memory call while the ordinary harness task still completes. A transition off blocks new/pending non-safety submissions but retains original attribution for in-flight acknowledgements until reconciled, drained, or isolated. Keep explicitly authorized safety/maintenance distinct from ordinary task effects. An outage is not permission denial, and a network profile cannot bypass a feature-off gate. Test actual call counts, pending suppression, late acknowledgement, no-secret readiness, and unaffected local reviewed evidence. Missing EverOS service blocks only EverOS-dependent actions.

For a revisit, repair only the affected service-entry gate and rerun direct forbidden-call and feature-off checks. Revisit STEP-15/17/18 only where the changed profile was consumed.
