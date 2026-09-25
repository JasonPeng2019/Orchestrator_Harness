# BEHAVIOR-08 - Snapshots restore isolated recoverable state

## Dictated outcome and source

An authorized operator can export a consistent logical synthetic state and
restore the capabilities it claims into a fresh isolated identity boundary.
Approval, current/revoked state, evidence, representation, usage, and pending
effects remain trustworthy or are explicitly incomplete. Feature Section 16.2
governs this outcome; binding shared-record and ownership contracts in
Implementation Sections 1-2 continue to apply.

## Actors, triggers, and preconditions

The operator identifies an exact owned product instance, application/project/
namespace/owner scope, local store, and any EverOS/Atlas dependencies. Writers
are quiesced or a supported consistent logical capture is available. Restore
targets a fresh compatible root and namespace unless an explicit tested remap
is supported.

## Behavioral flow and decision rules

1. Capture a consistent logical version of decisions, dispatches, outcomes,
   reviewed receipts, cases/procedures, approvals, current designations,
   revocations/tombstones, representation/configuration identity, native usage,
   and pending/uncertain operations needed for the claimed capabilities.
2. Keep protected source references resolvable or mark the affected capability
   incomplete. A pending remote effect remains pending with its exact
   dependencies; a snapshot never claims universal simultaneity across
   independent services or remote completion that was not observed.
3. Verify export integrity and explicit identity. A partial export is labeled
   partial, not complete runnable state.
4. Before target mutation, validate integrity, compatibility, required
   dependencies, and identity collision. Restore into a fresh namespace or use
   an explicitly tested remap; never silently merge independent outcomes or
   overwrite production state.
5. Recovery resumes only exact owned pending work under BEHAVIOR-04's safe
   reconciliation rules. Historical superseded failures do not become live
   blockers merely because they remain in the snapshot.

## State, data, and observable effects

The exported artifact identifies completeness, source identity and logical
capture, integrity, dependency references, and pending-state meaning. The
restored instance advertises only capabilities whose trust and evidence can be
resolved in its new identity. Operator recovery reports exact next action and
owned resource state.

## Edge, failure, and recovery behavior

An interrupted capture yields no trusted complete snapshot; live source state
remains authoritative. Corruption, missing approval/tombstone/receipt/
representation dependency, incompatible schema, or target collision fails
before partial trust or overwrite. A failed isolated run is recovered or cleaned
by recorded ownership, never broad process names or guessed remote state.

## Constraints and preserved behavior

Snapshot support is for current synthetic isolation, not benchmark execution or
future learned-policy storage. Ordinary procedure authorization and revocation
rules survive restore. The outer implementation harness and unrelated namespaces
remain untouched.

## Acceptance scenarios

- A quiesced synthetic state exports with approvals, current/revoked state,
  receipts, representation/configuration, usage, and pending dependencies and
  restores into a fresh namespace with equivalent eligible behavior.
- Corruption, a missing critical dependency, or identity collision is rejected
  before target mutation or automatic trust.
- A pending operation restores as pending and resumes through exact safe
  reconciliation, not as a fabricated completed effect.
- Recovery of an isolated failure leaves unrelated roots, remote partitions,
  production data, and the outer harness untouched.

## Implementation freedom and unresolved decisions

Encoding, storage consistency mechanism, and optional tested remapping are
implementation choices. Namespace-bound restore is sufficient. No product
decision remains unresolved.
