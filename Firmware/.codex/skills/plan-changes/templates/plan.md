# Change implementation plan

## Source change list

- Source: `.change-loop/changes.md`
- Goal summary: <one concise paragraph>

## Repository context and assumptions

- Verified architecture and relevant entry points: <paths and relationships>
- Existing test/build commands relevant to the change: <commands or "not yet verified">
- <!-- Assumption: Record each necessary interpretation next to the item it affects. -->

## Plan items

### CL-001 — <short outcome>

- **What to change:** <concrete implementation change>
- **Where:** <verified file(s), module(s), or area(s)>
- **Exact intended behavior:** <observable post-change contract, including errors and edge cases>
- **Must remain intact:** <existing behavior, API compatibility, invariants, and adjacent features>
- **Objective verification:** <smallest targeted assertion, affected regression surface, and any genuinely necessary expensive acceptance check>
- **Existing pass invalidation:** <name only prior passing checks whose covered source/contract changes, or "none">

<!-- Repeat CL-NNN sections in dependency order. -->

## Out of scope / must not change

- <explicit exclusion>
- Existing contracts not named for change remain unchanged.
- No unrelated refactors, dependency upgrades, formatting sweeps, commits, or generated artifacts.
- Optional hardening and speculative edge cases without evidenced product impact remain advisory.

## Acceptance gate

- Every CL-NNN item has at least one automated spec assertion.
- Regression coverage exercises callers, shared modules, and adjacent behavior touched by the diff.
- Each tester suite has a current targeted pass or validated reuse of unchanged passing evidence.
- Failed checks and invalidated affected regressions are rerun; unrelated expensive passing checks
  are retained and are not restarted from scratch.
- The doer does not modify tester-owned files, manifests, or gate commands.
