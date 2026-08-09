# Phase 3 Spec - Wake-Path Logging

## Plain goal

Add the minimum logging needed to prove exactly how an external worker request reaches and wakes
the orchestrator. The result must distinguish transport delay, manager-notice delay, and
manager-handling delay without guessing from nearby timestamps.

This phase implements `logging_additions_spec_2.md`. It does not run the three-sprint experiment or
choose the final manager architecture.

## Ownership and final authority

The current root orchestrator owns:

- the behavioral spec and implementation plan;
- every scope and design decision;
- the judgment of whether a reviewer finding is valid;
- the exact fix sent to the coder;
- the decision to repeat a loop or move on; and
- the final Phase 3 verdict.

Subagents advise or implement. They never take ownership of the plan and never decide whether the
phase is blocked, accepted, or complete.

## Required roles

### Coder subagent

Use one persistent **GPT-5.6-terra medium** coder in the current live repository.

The coder:

- reads this spec, `logging_additions_spec_2.md`, and `$always-keep-in-mind`;
- implements only the root orchestrator's current plan and accepted follow-up fixes;
- adds or updates focused tests for the changed behavior;
- runs the affected tests and reports exact results;
- does not broaden the architecture or independently redefine requirements; and
- does not commit, push, deploy, flash, or operate hardware.

Resume the same coder for ordinary fixes. Do not create a new coder for every review iteration.

### Code reviewer subagent

After each implementation slice, use an independent **GPT-5.6-terra medium** reviewer.

The reviewer:

- inspects the implementation and relevant tests;
- checks behavior against this spec and `logging_additions_spec_2.md`;
- identifies code-breaking errors, missing evidence, regressions, unnecessary complexity, and
  insufficient tests;
- returns numbered findings with exact file/evidence references; and
- does not edit the implementation.

**The reviewer is advisory and can never block.** A `BLOCK`, `FAIL`, severity label, or strong
recommendation from the reviewer is feedback only. The root orchestrator independently evaluates
each finding and has final say on whether a change is warranted and whether the work advances.

### Smoke-test subagent

After the root closes the code-review loop, use a **GPT-5.6-luna** smoke-test subagent to write and
run practical host-only smoke tests for the changed logging path. It reports evidence and failures
but does not fix code or decide whether the phase advances.

## Required behavior

Every tested blocking request must support this ordered durable chain:

1. `AGENT_SIGNAL_CREATED` - worker request created.
2. `HARNESS_SIGNAL_OBSERVED` - harness detected it.
3. `MANAGER_WAKE_ATTEMPTED` - a named component invoked a named wake transport.
4. Exactly one of:
   - `MANAGER_WAKE_DELIVERED`, or
   - `MANAGER_WAKE_FAILED`.
5. `MANAGER_WAKE_RECEIVED` - the manager's first logged action after the wake returned control.
6. `MANAGER_EVENT_CLAIMED` - the manager began handling the request.

Reuse existing records for stages 1, 2, and 6. Add only the missing records and correlations.

### Correlation contract

- All six stages use the same `epoch_id` and `event_id`.
- Stages 3-5 use the same `wake_id`.
- Every retry uses a new `wake_id`; it never overwrites an earlier attempt.
- Every attempt has exactly one delivered or failed outcome.
- A successful blocking `MANAGER_WAIT_FINISHED` names the triggering `event_id`, `wake_id`, and
  `wake_transport`.
- Manager receipt uses the wake ID supplied by the transport. It is never inferred from timing.

### Timestamp contract

- `source_timestamp_utc` records when the action actually happened.
- Watcher/canonical ingestion time remains separate.
- Attempt and outcome records are written at the action boundary, not reconstructed later.
- A successful chain must satisfy:

  `created <= observed <= attempted <= delivered <= received <= claimed`

- Equal timestamps are valid.
- Missing stages, mismatched IDs, duplicate outcomes, reused wake IDs, or impossible ordering yield
  `INSUFFICIENT_EVIDENCE`.
- The analyzer never fabricates a cause from silence or adjacent timestamps.

### Disabled watcher behavior

Watcher-specific logging remains conditional. When the deterministic watcher is disabled or not
included, watcher-owned behavior no-ops without breaking the harness or creating watcher output.
The production harness wake records required by this phase must not depend on an AI watcher
subagent.

## Implementation boundaries

Use the smallest change that fulfills the logging contract.

In scope:

- the missing wake attempt/outcome/receipt records;
- `wake_id` generation and propagation;
- exact blocking-wait linkage;
- analyzer validation of complete and invalid chains;
- focused tests and practical host-only smoke coverage; and
- narrowly necessary documentation/config updates.

Out of scope unless a focused test proves it is unavoidable:

- a new manager-state system;
- a queue redesign;
- a general retry framework;
- crash/restart recovery;
- a logging-schema rewrite;
- new polling modes;
- a `codex exec` manager bridge;
- unrelated harness/watcher cleanup; or
- changes to firmware experiments.

## Root-authored implementation plan

Before launching the coder, the root orchestrator must inspect the current code paths and write a
concrete plan that identifies:

1. the existing producers for request-created, harness-observed, wait, and claim records;
2. the exact component and transport responsible for stages 3 and 4;
3. how the blocking wait returns the `wake_id` to the root manager;
4. where `MANAGER_WAKE_RECEIVED` is emitted before any scan/claim/decision action;
5. the analyzer entry point that validates the six-stage chain; and
6. the focused tests changed or added.

The coder may report a contradiction discovered in the code, but the root revises the plan. Plan
authorship is not delegated.

## Coder-reviewer loop

1. The root writes the implementation plan and sends one focused slice to the coder.
2. The persistent Terra-medium coder implements the slice and runs affected tests.
3. The independent Terra-medium reviewer reviews the resulting code and tests.
4. The root audits every numbered reviewer finding:
   - **Accept** when evidence shows code-breaking behavior, a required logging/evidence gap, a
     credible regression, or a simple fix clearly worth its risk.
   - **Reject or defer** when the finding is unsupported, stylistic, speculative, out of scope, or
     would add disproportionate complexity.
5. The root records its rationale for every material accepted or rejected finding.
6. For accepted findings, the root writes the exact smallest fix and resumes the same coder.
7. Repeat coder implementation, reviewer feedback, and root adjudication until the root decides:
   - all objective requirements are implemented;
   - affected tests pass; and
   - no reviewer finding accepted by the root remains unresolved.

The reviewer cannot keep this loop open. Once required evidence is green and only rejected or
advisory findings remain, the root moves on. Conversely, the root must not ignore a verified
code-breaking finding merely because the reviewer cannot formally block.

## Smoke-test loop

1. After code review closes, the Luna subagent writes/runs focused host-only smoke tests.
2. The root audits each failure and decides whether it exposes a real Phase 3 defect.
3. Accepted defects return to the persistent coder with a root-authored focused fix.
4. The changed behavior returns to Luna for the smallest affected retest.
5. Repeat until the root decides all accepted smoke failures are resolved.

Phase 4 owns the formal host-only production-wake readiness gate. Phase 3 smoke tests prepare that
gate but do not substitute for it.

## Minimum test coverage

Tests must cover:

1. a complete ordered successful chain;
2. an explicit failed wake;
3. a missing stage producing `INSUFFICIENT_EVIDENCE`;
4. out-of-order timestamps producing `INSUFFICIENT_EVIDENCE`;
5. a mismatched or reused `wake_id` being rejected;
6. zero or multiple outcomes for one attempt being rejected;
7. blocking-wait finish linked to the exact wake/event/transport;
8. manager receipt occurring before scan, claim, decision, or response;
9. retry attempts retaining separate wake IDs and outcomes; and
10. watcher-disabled behavior remaining a clean no-op.

Then run the complete harness and deterministic-watcher suites plus relevant compile/static checks.
Pre-existing unrelated lint/type failures must be reported honestly but do not require a mass
cleanup.

## Phase 3 exit gate

The root orchestrator may mark Phase 3 complete only when:

- all required records and correlation fields are implemented;
- the analyzer fails closed as `INSUFFICIENT_EVIDENCE` for incomplete or contradictory chains;
- focused tests and accepted smoke tests pass;
- full harness and deterministic-watcher suites pass, apart from documented intentional skips;
- watcher-disabled behavior is unchanged;
- every accepted reviewer/smoke finding is resolved;
- rejected material findings have recorded root rationale; and
- no relevant process or temporary runtime is left behind.

The root then updates `PLAN.md` and advances to Phase 4 host-only readiness. No reviewer approval is
required to advance; the root's evidence-backed decision is final.
