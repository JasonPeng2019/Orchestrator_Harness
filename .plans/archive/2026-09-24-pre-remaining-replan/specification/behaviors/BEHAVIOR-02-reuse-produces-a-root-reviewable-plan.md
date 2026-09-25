# BEHAVIOR-02 - Reuse produces a bounded ROOT-reviewable plan or fresh fallback

## Dictated outcome and source

When ordinary planning is needed, the product considers the five reviewed
template families and produces either a structure-preserving direct-fill proposal,
a bounded proposal from a real product-harness APC child, or a normal fresh-plan
request. Every proposal remains non-authoritative until ROOT accepts its exact
revision. Feature Sections 6–7 and Implementation Section 6.1 dictate this
outcome.

## Actors, triggers, and preconditions

ROOT triggers this behavior only when no accepted plan has precedence and the
current plan state permits planning or explicit replanning. It receives
BEHAVIOR-01's bounded eligible template shortlist, current trusted field evidence,
remaining time, allowed plan route, and resolved template/APC feature values.

The local library contains the regression-repair, public-interface-change,
dependency-upgrade, schema/data-migration, and integration-failure families and
works in restricted-local mode. Light adaptation additionally requires template
memory, APC, light adaptation, usable remaining time, and a complete explicit
`apc_adaptation_binding`.

## Behavioral flow and decision rules

1. Compare the bounded eligible shortlist using one canonical sanitized query,
   compatible representation/fingerprint/metric, and the configured calibrated
   thresholds. An incompatible top result does not prevent a lower-ranked
   eligible candidate from consideration.
2. A direct-fill candidate may populate only declared typed fields from trusted
   current evidence. Fixed structure, invariants, verification/stop intent, and
   forbidden carry-over remain unchanged. Missing critical facts or fields makes
   direct fill unavailable.
3. A permitted near match creates one bounded drafting-support task containing
   the exact parent objective/decision, template revision and optional draft,
   trusted current bindings/evidence, allowed edits, result contract, and remaining
   absolute deadline. The product harness resolves exactly the supplied
   `apc_adaptation_binding`, records launch intent and actual invocation, and owns
   correction and cleanup.
4. The child can read the supplied scoped material and return only the declared
   proposed-plan artifact. It cannot accept the parent plan, implement it, approve
   or publish memory, search recursively, launch children, create another harness,
   or claim the parent execution outcome.
5. Validate result identity, binding, template revision, field types, edit set,
   structure/invariants, output bound, native binding evidence, and cleanup before
   showing the proposal to ROOT. The total stage bound includes queueing, startup,
   model work, native corrections, collection, validation, and cancellation; a
   correction never renews the deadline.
6. No/incomparable match, unresolved fact, unavailable or invalid explicit
   binding, child launch ambiguity that cannot safely continue, timeout, invalid
   result, exhausted optional budget, or ROOT rejection takes the normal fresh
   planning path. There is no hidden model substitution, direct provider API,
   EverOS adaptation client, or stronger second planner.
7. ROOT applies the same applicable review and acceptance rules to direct-fill,
   adapted, and fresh plans. ROOT may revise a proposal and accept that exact new
   revision. Preserve initial reuse disposition and the final accepted/executed
   source; a reuse attempt followed by fresh planning is not a cache hit.

## State, data, and observable effects

The selected template remains immutable and identified by exact revision,
provenance, applicability, representation, required field policy, allowed edits,
and verification intent. Direct fill records the populated fields and source
template. An APC attempt records parent/template identity, requested and resolved
binding, launch/result/cleanup identity, native usage when observed, status, and
the exact proposal. The result has proposal authority only.

The final accepted plan has its own exact identity, revision, integrity, ROOT
acceptance, objective, route, and source lineage. Child completion is not parent
acceptance and is not an additional successful coding outcome.

## Edge, failure, and recovery behavior

- Missing or invalid `apc_adaptation_binding` makes light adaptation unavailable
  and selects fresh planning; it never inherits a lightweight-worker model.
- A lost child-launch acknowledgement must be reconciled by exact harness identity
  before another launch. Unresolved ownership blocks only conflicting reuse of
  that child's resource and remains visible.
- A child timeout or cancellation retires only the owned child if its identity is
  known. Failure to prove cleanup is retained and prevents conflicting reuse.
- Output that changes fixed ordering, removes an invariant, sources a binding from
  history as present fact, exceeds permitted edits, or claims acceptance is
  rejected and cannot be partially salvaged as an adapted plan.
- A direct-fill validation failure may still permit another eligible shortlist
  candidate or fresh planning within remaining bounds; it does not weaken field
  trust to preserve reuse.
- Optional adaptation failure does not block ordinary fresh planning or alter an
  already valid current task state.

## Constraints and preserved behavior

Template content and adaptation inputs follow the shared privacy and recipient
rules. Direct fill launches no child. The candidate product harness, not the outer
implementation harness or a standalone API client, owns the child in development
and deployment. Deployed roles remain independently configurable; no development
model name is hard-coded into product eligibility or fallback.

Accepted STEP-01 APC request/result identity and no-authority safeguards remain
compatible. This behavior adds the real owned launch and branch orchestration; it
does not replace the harness lifecycle.

## Acceptance scenarios

- Each of the five template families is discoverable through the supported local
  path and stops reuse at its declared missing-policy, unknown-state, unavailable-
  boundary, or redesign condition.
- A high compatible candidate with complete trusted fields direct-fills only
  declared fields, preserves fixed structure, and launches no APC child.
- A higher-ranked incompatible candidate is skipped and a lower-ranked eligible
  candidate remains usable.
- A low or incomparable score, missing current fact, or incompatible projection
  returns to fresh planning without presenting reuse as successful.
- A near match launches one child through the candidate product harness using the
  exact explicit binding, returns a bounded proposed artifact, records native
  identity/usage, and leaves ROOT acceptance separate.
- Two supported explicit binding configurations can be selected without source
  changes; neither becomes a named or inherited product default.
- Missing, invalid, silently substituted, timed-out, over-budget, over-editing, or
  recursive child behavior is rejected and takes fresh planning without a direct
  API fallback or leaked child.
- ROOT rejection records an initial reuse attempt and terminal fresh plan; ROOT
  revision creates and accepts a distinct exact plan revision.

## Implementation freedom and unresolved decisions

Template storage layout, structured edit representation, similarity algorithm,
and concrete harness adapter are implementation choices. Starting thresholds and
limits may use Implementation Section 16 and may be tuned on authorized synthetic
development evidence without weakening gates. No product decision remains
unresolved.
