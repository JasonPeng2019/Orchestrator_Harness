# BEHAVIOR-07 - Network-mode claims match actual enforcement

## Dictated outcome and source

Each run resolves a requested and effective network profile before work and
reports what the actual launched worker and product services can do. Restricted
local work makes no Atlas task-path call; an Atlas-only claim requires verified
unrelated-destination blocking, not just prompt instructions. Feature Section
13.3 and binding Implementation Section 12 govern this outcome.

## Actors, triggers, and preconditions

ROOT/operator selects a supported profile with provider/tool configuration,
Atlas participation, and any external egress enforcement. The product can
inspect the actual launched tool/network surface. Outage and permission state
are distinct from the requested profile.

## Behavioral flow and decision rules

1. Resolve `soft_guardrail_network`, `atlas_memory_only`, or
   `restricted_local` before preparation and capture requested/effective values
   and enforcement reason with the run.
2. In soft guardrail mode, suppress supported provider-native general
   web/search/fetch tools and disclose unsuppressed capability and shell egress;
   do not claim hard isolation.
3. Claim Atlas-only only when unrelated destinations are independently blocked
   while required services remain permitted, and verify the actual launched
   payload/tool surface. If suppression or egress proof is missing, report the
   strongest truthful effective profile instead.
4. In restricted-local mode, prevent Atlas task retrieval, optional telemetry,
   publication retries, and other optional Atlas task-path operations at the
   service boundary. Local and declared-frozen memory remain available. A
   safety administration operation that cannot run remains pending for an
   authorized environment.
5. Report a service outage separately from the permission profile. Neither
   fallback nor administration may silently bypass the effective restrictions.

## State, data, and observable effects

The run retains requested and effective mode, source of enforcement, actual
available tools and egress limitations, and service participation/outage status.
An operator can inspect the same facts without credential disclosure.

## Edge, failure, and recovery behavior

Unverified egress prevents an Atlas-only claim but does not erase valid local
work. A provider version that cannot suppress a general tool must be reported
honestly. A pending revocation in restricted-local mode does not turn into a
completed remote effect or a task-path exception.

## Constraints and preserved behavior

The mode is an operational permission profile, not a guarantee that Atlas or a
model provider responds. Same-user coding processes are not represented as a
hardened sandbox. All-off and feature-off controls still suppress actual
optional service work.

## Acceptance scenarios

- Soft guardrail reports suppressed native tools and remaining shell egress
  without claiming hard isolation.
- Atlas-only is reported only after actual unrelated-destination enforcement
  and launched-payload verification; missing proof yields a truthful downgrade.
- Restricted-local performs no Atlas task-path call, including retry or
  telemetry, while usable local/frozen memory remains available.
- An Atlas outage changes service availability but does not relabel the
  configured permission profile or authorize a forbidden fallback.

## Implementation freedom and unresolved decisions

Provider-specific suppression and egress-enforcement integrations are
implementation choices constrained by truthful observation. No product decision
remains unresolved.
