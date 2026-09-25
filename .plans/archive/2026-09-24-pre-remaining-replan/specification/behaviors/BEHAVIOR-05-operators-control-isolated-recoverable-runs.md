# BEHAVIOR-05 - Operators control isolated, snapshot-capable, recoverable runs

## Dictated outcome and source

An authorized operator can compose and inspect the product, choose a truthful
network profile, recover remaining product operations, and export or restore a
complete synthetic state into an isolated identity boundary. The operational
surface exposes actionable state without becoming a second scheduler or
overstating security, consistency, or remote completion. Feature Sections 13.3,
15, and 16.2 and binding Implementation Sections 10 and 12 dictate this outcome;
Implementation Sections 13 and 17 provide non-binding mechanism guidance.

## Actors, triggers, and preconditions

The operator acts in a ROOT-controlled environment with explicit product root,
application/project/namespace/owner identity, local state, optional EverOS and
Atlas configuration, supported provider bindings, and authorization for each
administrative action. Network mode resolves before a run. Snapshot export requires
owned writers to be quiesced or a storage mechanism that can provide a consistent
logical version.

Workers do not acquire operator authority through this surface. Procedure
publication, designation, withdrawal, and revocation retain the completed
STEP-03 authorization rules.

## Behavioral flow and decision rules

1. Before mutating a live workspace, preflight ownership overlaps between the
   harness command/provider lifecycle and the ROOT-suite skills/provider behavior.
   Compose a deterministic view that preserves both families, repository
   instructions, and provider-specific suppression. Validate the actual staged or
   launched worker payload, not only its source directory. Repeating setup is
   idempotent; a later upstream setup/overwrite that restores raw payloads requires
   recomposition. An interrupted partial commit blocks enhanced dispatch until
   exact validation or recovery completes.
2. Setup/readiness reports the exact product build and roots, composition state,
   schema and migration
   readiness, service and binding availability, network mode and enforcement
   source, pending/uncertain operations, and the next actionable step without
   exposing credentials.
3. Resolve one network profile per run:
   `soft_guardrail_network` suppresses supported provider-native general web tools
   while disclosing remaining shell egress; `atlas_memory_only` additionally
   requires independently enforced unrelated-destination blocking and verification
   of the actual launched surface; `restricted_local` makes no live Atlas task-path
   or retry call while allowing declared local/frozen memory. An outage is reported
   separately from the configured profile.
4. Let an authorized operator invoke the remaining setup/readiness, network-state
   inspection, pending-operation recovery, snapshot export/import, and usage
   ingestion outcomes through supported product surfaces. They call the same
   domain contracts used by the harness and do not implement another controller,
   launch loop, or review system. A new wrapper for completed procedure lifecycle
   or template administration is optional unless the chosen integration genuinely
   needs it.
5. Export a consistent logical state with the local memory/procedure content,
   decisions, dispatches, outcomes, reviewed receipts, approvals, current
   designations, tombstones, representation/configuration identity, usage, pending
   operations, and protected/resolvable provenance dependencies needed for the
   claimed restored capabilities.
6. Verify export integrity and explicit identity. A complete snapshot may preserve
   pending work only with its dependencies and replay semantics. A partial export
   is labeled partial and cannot claim complete runnable state.
7. Restore only into a fresh compatible root and namespace, or through an explicit
   tested identity/reference remapping. Refuse corruption, missing critical
   dependency, production/independent-trial overwrite, or silent outcome merging.
   Historical failures that were successfully superseded do not become live
   blockers merely because they remain in history.
8. Recovery inspects exact owned identities and resumes only safe pending work.
   It never uses broad process names, guesses remote completion, or deletes
   evidence simply to make a feature or run appear clean.

## State, data, and observable effects

Operators observe composition and actual-payload validity, requested and effective
feature/network state with reasons, service participation, pending and uncertain
operations, snapshot completeness, identity and integrity, recovery action, and
secret-free diagnostics. The product retains actual enforcement and unsuppressed
capability facts rather than only the requested label.

A restored run has a declared application/project/namespace/owner boundary and
resolvable dependencies. Restore never implies that a remote index and independent
local store were captured at one universal instant; any preserved pending sync is
explicit.

## Edge, failure, and recovery behavior

- If general tools cannot be suppressed or unrelated egress enforcement cannot be
  verified, the product refuses the `atlas_memory_only` claim and reports the
  strongest truthful profile.
- Restricted-local never attempts Atlas task retrieval, telemetry, publication
  retry, or another optional Atlas task operation. Authorized safety administration
  that cannot run remains pending for an authorized environment.
- An unavailable readiness dependency blocks only operations that require it and
  does not turn a fixture or cached payload into live evidence.
- An ownership conflict fails before mutation. An interrupted or overwritten
  composition prevents enhanced dispatch until the deterministic composed view and
  actual worker payload are restored and validated.
- Snapshot capture interrupted before its completion boundary yields no trusted
  complete snapshot. The prior live state remains authoritative.
- Missing approvals, tombstones, receipts, representation identity, source
  references, or pending-operation dependencies make the affected restored
  capability incomplete and prevent automatic trust.
- An identity collision or corrupted manifest refuses restore before mutating the
  target. Recovery or cleanup touches only the exact recorded product instance and
  owned subtree.
- CLI syntax or message defects can be corrected locally; they do not invalidate
  behavior already proved through unchanged domain interfaces.

## Constraints and preserved behavior

Operator output is actionable and secret-free. Authentication remains in approved
transport/configuration. Setup preserves both existing harness and ROOT-suite
behavior and existing repository instructions. Feature-off behavior reaches
actual services and pending submission paths. No operation installs a learner,
schedules a benchmark, or expands deployment into the development-only nested
harness topology.

## Acceptance scenarios

- Setup preflights an ownership collision before mutation, composes both behavior
  families, validates the actual worker payload, repeats idempotently, detects an
  upstream overwrite, and recovers an interrupted composition before enhanced
  dispatch.
- Readiness on a valid isolated root reports build, composition, schema, services,
  bindings, mode, pending work, and next action without credential content.
- The three network modes expose their actual launched tool/egress behavior;
  `restricted_local` produces no Atlas task call and an unenforced profile cannot
  claim `atlas_memory_only`.
- The supported operational surfaces expose remaining pending recovery, snapshot,
  network-state, readiness, and usage outcomes through the same domain services
  with consistent result semantics and no second controller.
- A quiesced synthetic state exports with approvals, current/revoked state,
  receipts, representation/configuration, usage, and pending dependencies and
  restores into a fresh namespace with equivalent eligible behavior.
- Corruption, missing dependency, or target identity collision fails before
  partial trust or overwrite.
- A snapshot containing a pending operation restores it as pending and resumes it
  through the same safe reconciliation rule; it does not claim the external effect
  already completed.
- Recovery of a failed isolated run leaves unrelated namespaces, production data,
  and the outer harness untouched.

## Implementation freedom and unresolved decisions

Whether the remaining operational outcomes use a unified CLI, existing harness
commands, library calls, or a small combination is implementation freedom.
Snapshot encoding, quiescence mechanism, remapping support, and enforcement
integrations are also implementation choices. Namespace-bound restore without
remapping is conforming. No product decision remains unresolved.
