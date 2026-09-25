# BEHAVIOR-01 - Bounded preparation selects only eligible optional memory

## Dictated outcome and source

For one exact bounded objective, ROOT receives either a finite, provenance-rich set
of eligible cases, guidance, and templates or an explicit no-optional-memory
result. Preparation preserves accepted current plans, distinguishes the fixed
search strategy from topology routing, respects time and feature gates, and never
weakens eligibility to manufacture a hit. This is dictated by Feature Sections 2,
6.4, 7–9, 12.5–12.6, and 15 and the shared rules in
[SPEC.md](../SPEC.md).

## Actors, triggers, and preconditions

ROOT starts preparation with the exact task and bounded objective, intended
repository baseline, current plan state, constraints and failure context,
topology/admission evidence when applicable, resolved feature configuration,
network mode, available stores, and remaining time when known. The runtime may
query scoped EverOS cases/approved skills, local templates and procedures, and
Atlas procedures permitted by the configuration.

Preparation does not apply to the optional pipeline when all enhancements are
off. An execution-accepted same-objective plan also bypasses template selection
and adaptation, though eligible evidence or guidance may still be prepared around
that plan. A candidate plan continues its existing review unless ROOT explicitly
requests replanning.

## Behavioral flow and decision rules

1. Validate exact task, objective, repository baseline, current-plan identity and
   state, route/admission evidence, configuration, and budget source. A nonempty
   missing, unreadable, stale, wrong-objective, or wrong-route plan is an explicit
   mandatory-state inconsistency, not an absent plan.
2. Resolve topology admission before optional search when known. Level 0 uses the
   ordinary route. If Level 0 is discovered after topology-routed preparation,
   permanently abandon that packet and either perform at most one bounded
   ordinary-route preparation or continue explicitly without memory. Preserve
   lineage and all cost already spent.
3. Select at most one primary fixed recipe. Standard performs one inexpensive
   bounded pass. Problem-focused uses real failure/recovery context and otherwise
   falls back to Standard under Standard's gates. Deeper is a bounded adaptive
   local investigation with bounded Atlas participation when enabled; a healthy
   local-only Deeper path remains valid in restricted-local mode.
4. Admit each optional stage only when its full maximum duration and the positive
   execution reserve fit the trusted remaining time. Query construction,
   embeddings, retrieval, exact/freshness reads, scoring, queue delay, and any
   internal rounds count inside their enclosing stage. Unknown time permits only
   the configured cheap fixed pass; it masks Deeper and light adaptation.
5. Give every enabled participating store a bounded chance to start and give
   skills and templates independent candidate capacity. One slow or malformed
   store cannot consume the entire opportunity or invalidate valid completed
   results from another store.
6. Normalize and gate candidates before final ranking. Preserve source and
   provenance and keep historical cases, approved guidance, and templates as
   distinct kinds. Enforce scope, recipient authority, approval, current
   designation, revocation, predicates, conflicts, route/capability compatibility,
   integrity, representation comparability, and live or declared-frozen freshness.
7. Deduplicate the same logical revision across stores without a relevance bonus.
   Deliver at most one procedure revision per logical identity, using the declared
   trusted selection policy or the default local, project, then shared specificity
   order and a deterministic tie policy. Preserve the provenances and reasons for
   rejected alternatives.

## State, data, and observable effects

One durable preparation decision identifies the task, objective, repository
baseline, current plan, requested and effective fixed strategy, resolved feature
and network configuration, budget/deadline source, route/admission result, and any
superseded preparation. Its trace distinguishes disabled, unavailable,
unattempted-by-budget, timed-out, invalid, rejected, selected, and delivered
candidates without creating learner-policy state.

Each candidate retains its kind, origin, exact revision and payload reference,
scope and recipient boundary, provenance, eligibility/freshness mode,
representation identity where relevant, and selection disposition. No result is
authority merely because it ranked highly. Valid empty search is observable as
`no_optional_memory` or equivalent and preserves the exact-state baseline.

## Edge, failure, and recovery behavior

- An optional store outage, timeout, malformed result, or ineligible candidate is
  isolated. Return other valid completed results or no optional memory.
- When live shared freshness cannot be established within budget, omit that
  guidance. If a not-yet-accepted reused plan depends on it, return the affected
  plan to ROOT. Do not relabel a cached shared copy as local.
- An accepted current plan does not become invalid solely because its historical
  source template cannot be fetched. Known unsafe exposure still returns to ROOT.
- Stop scheduling and waiting at the stage deadline. Late or non-cancellable work
  remains attributable, but cannot enter the current packet after finalization.
- Repeated route correction, process restart, internal query, or correction attempt
  cannot reset the objective's budget or silently create a fresh decision.
- A mandatory identity, plan, or security inconsistency uses ROOT recovery; it is
  not downgraded to an optional-memory miss.

## Constraints and preserved behavior

The accepted EverOS and trusted-procedure authorization/lifecycle behavior remains
unchanged. Searches use sanitized query semantics before any remote representation
or comparison. Restricted-local mode performs no Atlas task-path call. Disabling a
read/use feature suppresses the actual service path rather than filtering its
output after work occurred. The all-off path performs no memory initialization,
query, context injection, APC launch, or background optional write.

## Acceptance scenarios

- With all enhancements off, preparing an ordinary task performs no EverOS,
  Atlas, template, or APC action and returns the inherited exact-state path.
- With an accepted same-objective plan, preparation preserves that exact plan and
  does not score templates even if its historical template is unavailable.
- A nonempty plan reference bound to another objective, route, or unreadable
  artifact fails as mandatory inconsistency rather than fresh-planning silently.
- Standard searches the enabled kinds once within its enclosing bound; a slow
  Atlas call does not prevent a local case or template attempt.
- Problem-focused uses the supplied real failure context, while its absence takes
  a gated Standard path without an extra classifier call.
- Deeper performs only bounded declared rounds, works locally in restricted-local
  mode, and is unavailable when the local adaptive path or sufficient budget is
  unavailable.
- A malformed candidate, unknown required predicate, revoked/current mismatch,
  incompatible representation, or unauthorized recipient is rejected without
  discarding an unrelated eligible candidate.
- A logical procedure visible locally and remotely contributes once to ranking
  while retaining both provenances; conflicts and competing revisions resolve
  deterministically without broadening authorization.
- A shared procedure changes current status after discovery but before final use;
  the stale item is rejected or the dependent plan returns to ROOT.
- Late Level 0 makes the topology packet non-dispatchable and leads to one bounded
  ordinary reprepare or an explicit no-memory continuation with cost and lineage
  intact.

## Implementation freedom and unresolved decisions

Store concurrency, quota implementation, local scoring, internal trace layout,
and the representation algorithm are implementation choices. They must preserve
fair attempt opportunity, type capacity, comparable reuse scoring, and bounded
behavior. No product decision remains unresolved.
