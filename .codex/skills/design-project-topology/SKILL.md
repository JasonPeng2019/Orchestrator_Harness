---
name: design-project-topology
description: "Design a project-specific, compute-efficient multi-agent execution-plan topology for any project and its available runtime or harness. Use when asked to plan agent roles, lanes, gates, reviews, tests, repair loops, handoffs, locks, or practical validation without executing the work. Produces the smallest topology that preserves required product coverage and realistic release safety."
---

# Design a lean project topology

Produce one execution plan. Do not execute it, launch agents, change product code, create runtime state, or run product tests. Read, plan, write the plan, and validate the plan only.

## Inputs

Require:

- product goal/spec and acceptance criteria;
- reference plan, if one exists;
- project path, runtime/orchestrator path, and operative documentation;
- available slots and concrete agent/model choices for orchestrator, writer, reviewer, test author, and executor;
- output path;
- costly, scarce, destructive, or external resources.

If required inputs are absent, ask one consolidated question. Treat a reference plan as an outcome inventory, not a mandatory decomposition.

Read current authoritative files first. Read history only to resolve a named ambiguity. Inspect the live runtime/orchestrator before assigning it a capability; a harness is optional, never assumed.

## Rules

Every directive below is normative. Cite its ID wherever the emitted plan applies it.

### Product and complexity

**R1 — Preserve scope.** Implement every required outcome; do not weaken, reinterpret, or add product scope. Surface contradictions.

**R2 — Separate coverage from execution.** Give each requirement a stable coverage ID, then group IDs into coherent deliverables. Never create a lane merely because an item, file, or module exists.

**R3 — Make complexity earn its cost.** Start with `orchestrator -> one worker -> one check -> orchestrator`. Add a worker, fan-out, gate, artifact, lock, rehearsal, or loop only for a named realistic failure, safety need, or net wall-time gain. State the payoff. Omit it when rereading, coordination, merge, verification, and maintenance cost plausibly outweigh the benefit.

**R4 — Optimize for deployed behavior.** Admit realistic correctness, reliability, recovery, safety, security, evidence-integrity, and required-usability defects. Drop cosmetic, invisible, unreachable, speculative, duplicate-guard, and net-negative-complexity work to an out-of-scope ledger.

**R5 — Report truth.** Never fabricate evidence, infer success from missing data, or call uncertainty failure or success. Record `INCOMPLETE` or `INDETERMINATE` when the evidence cannot decide.

### Roles, context, and compute

**R6 — Keep one decision owner.** The persistent orchestrator alone accepts work, blocks progress, changes scope, triages findings, integrates tips, and releases resources. Other agents return evidence or recommendations.

**R7 — Keep product writing singular.** Use one serial production writer per coherent deliverable. Do not concurrently mutate one project tip. Split writers only across proven-independent deliverables with explicit ownership, merge order, and payoff.

**R8 — Default every pool to one.** Fan out only over disjoint conceptual surfaces that can run concurrently and whose time or isolation benefit exceeds startup and merge cost. Respect the available-slot cap. Every fan-out rejoins one orchestrator decision.

**R9 — Assign the cheapest adequate executor.** Use deterministic scripts for mechanical checks, focused economical agents for routine review/test work, and strongest reasoning only for planning, hard defects, risk judgments, and final acceptance. Record model, effort, and service tier; honor user/repository Fast or priority policy without silent substitution.

**R10 — Send bounded context and bound thread lifetime.** Give each focused worker one task card containing: objective, why now, current state, accepted prior results, dependencies, in/out scope, required behavior, exact inputs and lock identity, allowed actions, acceptance criteria, outputs, failure route, and the fewest useful initial entrypoints. Tell it not to reconstruct history or read other files unless the card is insufficient. Broad whole-product review may receive the governing set. Resume that thread only for unresolved criteria in the same card, R13 report recovery, R17 fast-lane correction, or another correction within the same unaccepted logical task. Once semantically accepted, the task and thread are terminal; unrelated later work starts from a new bounded card and thread.

**R11 — Price context.** Apply the runtime- or harness-provided entrypoint-count score when available. Record count, score, allowed range, and a concrete justification for every non-maximal score. If no scorer exists, record the count and justification in the plan; do not invent enforcement.

**R12 — Accept semantically.** A shape-valid result enters `ACCEPTANCE_PENDING`; it does not unlock dependents. Supply task-card, result, and required-evidence paths plus hashes. The orchestrator must issue exactly one verdict: `ACCEPTED`, `ACCEPT-WITHIN-TOLERANCE` with explicit waived criteria and product rationale, `CONTINUE` with exact missing work, or `INCOMPLETE`.

**R13 — Recover one malformed report cheaply.** On a missing or malformed terminal artifact, freeze the lane and inject the exact validator failure into the same worker once. Permit report-only repair from existing evidence: no code/test change, rerun, or invention. Validate again; on a second failure, mark incomplete or rerun only the evidence-producing check.

### Review, testing, and repair

**R14 — Pool before repair.** Each reviewer, test selection, and observer finishes its assigned surface, except under R23. Merge and deduplicate once; the orchestrator triages once; the writer repairs accepted findings once as a batch. Do not stop on the first ordinary finding or reopen review after every edit.

**R15 — Classify every follow-up.** Route it as `production/material`, `strict test-only`, or `administrative/support`. A product repair requires evidence tying the failure to product behavior, contract, oracle, or coverage—not merely a broken support process.

**R16 — Use one material route.** For an accepted production change, run the shortest affected smoke first. Then run the complete affected review and focused tests on one frozen tip; parallelize only disjoint slices. Join once, batch repairs once, and repeat only affected work. Do not review intermediate repair revisions.

**R17 — Use the strict test-only fast lane.** Admit only a fixture, mock, setup, runner, or test-metadata diff that changes no production/policy/contract/locked configuration, oracle, assertion strength, expected result, stable ID, or coverage obligation. Continue the same worker/thread, verify eligibility deterministically, and rerun exactly the known failed IDs once. Preserve every unrelated pass. Any semantic change or repeated failure exits to R16.

**R18 — Isolate administrative and support failures.** Correct reconstructable path, schema, report, fixture, runner, watcher, executor-environment, supervision, or cleanup faults in place when product outcome remains decidable. Otherwise invalidate only the affected evidence/check/attempt and rerun only that incomplete work. Never relock, repair, or fail the product merely because support code failed.

**R19 — Preserve green credit.** Use stable check IDs and a passed registry. Rerun only failures and checks implicated by changed dependencies. Run a full accumulated suite once at final safeguard when the product risk warrants it; never use an unrelated smoke as substitute credit.

**R20 — Preflight only fragile expensive runners.** Before an expensive selection that depends on custom runner or child-process evidence, use one side-effect-free disposable fake to prove inputs, IDs, folders, arguments, process identity, start, recording, outputs, and exit. Bind the pass to runner/procedure/configuration/environment fingerprint. Reuse it until that fingerprint changes. Record `not applicable` for ordinary runners.

### Locks, practical work, and stopping

**R21 — Invalidate by dependency, not document.** Keep whole-file hashes for audit, but define project-specific lock domains and each gate's domain dependencies. Classify every governing change append-only: changed requirements/domains, invalidated gates, preserved evidence, reason. Rerun only consumers; use a documented conservative route only when classification is genuinely uncertain.

**R22 — Rehearse costly external control flow.** Before scarce, irreversible, hardware, service, or other external allocation, run the exact project and control flow against disposable fakes. Prove only the control properties the real attempt depends on. Reuse rehearsal under an unchanged dependency fingerprint; never count it as real-world pass evidence. Name one owner for attempt state, abort/stop evidence, observer report, and cleanup. Record `not applicable` when no such resource exists.

**R23 — Stop immediately only to contain live harm.** Immediate stop requires exact evidence of unauthorized/wrong-resource action, loss of live-process containment or cleanup, or irreversible corruption of evidence needed for judgment. Preserve evidence, contain safely, then apply R18. Pool every other observation through R14.

**R24 — End loops on evidence.** Do not impose arbitrary iteration caps. End on success, unrecoverable error, or stall: repeated failure signature, no passed-set growth, pass/fail oscillation, or scope-only churn. Stop and report a stall; never hide it by restarting broadly. Explicit one-shot routes in R13 and R17 remain bounded.

### Design and runtime truth

**R25 — Review proportionately.** Trivial mechanical work may omit review with a reason. Any non-trivial design review assigns at least one existing reviewer—not an automatic extra worker—to correctness, simplicity, generalizability, organization, usability, and composability. Guard verified caller mistakes and real trust boundaries; do not add speculative abstraction, hostile-input defenses outside the threat model, arbitrary limits, double guards, or paternalistic blocks on intended correctly targeted work.

**R26 — Plan only real runtime behavior.** Inspect current docs/source and distinguish runtime-enforced rules from orchestrator policy. Use the actual launch, wait, event, acknowledgement, isolation, result, and cleanup mechanisms available in the project; if a harness exists, inspect its real behavior rather than assuming it. State manual responsibilities. Never name a fictional feature as automatic enforcement.

### Runtime footprint and concurrent evidence

**R27 — Allocate only necessary source isolation.** Give a lane a full linked worktree only when it may mutate source or its execution writes source-local state. A static read-only lane uses an exact immutable source view plus a separate writable result root. A test lane uses the cheapest mode that still prevents source, cache, output, and peer contamination. Record the chosen mode and reason; if the inspected runtime lacks it, plan the capability before relying on it.

**R28 — Retire terminal lanes.** After semantic acceptance and durable evidence preservation, remove the lane from active discovery, close any clean registered worktree through verified Git operations, retain required transcript/result evidence in an archive-only location, and discard disposable caches. Never delete unpreserved evidence, an unretained revision, a dirty worktree, or a path used by a live process. Archival failure leaves the lane terminal and visible for recovery; it never reopens accepted product work.

**R29 — Serialize shared append-only evidence.** Concurrent processes writing one event log use one cross-process lock keyed to that log. A writer waits for the lock, appends one complete record, flushes it, and releases the lock; it never interleaves or drops a record. Require a concurrent-process regression test. Do not invent per-controller logs or a merge layer when a lock is sufficient.

## Portable optimization patterns

Apply these as defaults when the project has the corresponding risk. They are patterns, not mandatory stage names; R3 decides whether each earns its cost.

- **Bounded task card and thread** `[R10-R13]`: give a worker the smallest complete context, let it resume only unresolved work in that card, and start a fresh card/thread for unrelated work after acceptance.
- **Pool, then repair once** `[R14-R19]`: let each assigned review/test surface finish, deduplicate findings, and make one bounded repair batch; rerun only affected IDs.
- **Cheap first, expensive once** `[R17,R20]`: preflight only fragile expensive runners with disposable fakes, reuse the pass by fingerprint, and use the narrow fast lane only for proven test-only corrections.
- **Scope revalidation by dependency** `[R19,R21]`: preserve valid evidence and rerun only gates that consume changed inputs; never relock merely because a document changed.
- **Rehearse before scarce allocation** `[R22]`: prove the exact external control flow with fakes before claiming scarce or irreversible resources, with one owner for setup, stop, observation, and cleanup.
- **Minimal isolation, then retirement** `[R27-R28]`: avoid full source worktrees for static readers and remove accepted terminal lanes from active discovery after preserving recoverable evidence.
- **Serialize shared evidence at the write point** `[R29]`: make concurrent writers wait on one lock; do not create a log-merging architecture when append serialization is sufficient.
- **Match model strength to uncertainty** `[R8-R9,R25]`: use scripts or economical agents for mechanical/focused work, reserve the strongest reasoning for planning, hard defects, risk judgments, and final acceptance.
- **Keep support noise out of product loops** `[R18,R23-R24]`: correct process/report/fixture/cleanup faults in place when product behavior remains decidable; mark only undecidable work incomplete and never restart broadly.

## Method

1. **Extract coverage** `[R1,R2]`. Build an atomic checklist with source and acceptance evidence. Resolve or surface gaps.
2. **Measure risk and cost** `[R3-R5,R9]`. For each coherent deliverable, record realistic failure impact, external cost, expected runtime, context cost, and cheapest adequate topology.
3. **Compose freely** `[R6-R11,R25-R29]`. Choose only needed roles. Keep steps serial unless independence and payoff are explicit. Use the smallest lane graph that preserves ownership and evidence. Specify source-allocation mode, terminal retirement, and any shared-log lock.
4. **Route findings** `[R12-R20,R23,R24]`. Define semantic acceptance, pooling, repair class, preflight reuse, narrow reruns, and stall handling before execution starts.
5. **Scope locks and practical work** `[R21,R22]`. Map domains to consumers; name external-state owners and rehearsed flow only when applicable.
6. **Audit** `[R1-R29]`. Remove every lane, gate, artifact, reread, rerun, worktree, or active-state retention without a concrete rule-backed purpose. Do not finalize with an unmapped coverage ID, missing owner, fictional runtime capability, unsafe concurrent evidence writer, or unexplained non-minimal topology.

## Plan format

Emit these sections; adapt detail to the task rather than copying a fixed stage layout.

1. **Inputs, authority, assumptions** — sources, hashes/versions when needed, user role mapping, runtime/orchestrator capabilities, unresolved questions.
2. **Coverage checklist and map** — requirement ID, source, deliverable, implementation owner, verification, completion evidence.
3. **Cost/risk decomposition** — coherent deliverables, dependencies, risk, expected expensive operations, chosen topology, one-line justification for every non-minimal element.
4. **Role and launch table** — role, agent/model, effort, tier, pool size, context class, write authority, resources.
5. **Whole-plan flow** — one compact arrow graph showing serial path, actual fan-outs, joins, repair routes, and completion.
6. **Per-deliverable topology** — graph plus lane manifest: stable lane ID, task, predecessor, source-allocation mode and reason, run/result/archive roots, conceptual and path ownership, task-card entrypoints, required output/evidence, join, terminal-retirement route, failure route.
7. **Runner rules** — R12-R24 and R27-R29 routes, stable IDs, registry, preflight fingerprints, lock-domain matrix, support-failure isolation, external ownership/rehearsal, thread closure, terminal archival, shared-log locking, stop conditions.
8. **Final validation and definition of done** — realistic release behavior, affected checks, any one-time safeguard, evidence, cleanup, out-of-scope and tolerance ledger.
9. **Rule application** — map every `R1`-`R29` to the exact plan section, lane, gate, or explicit `not applicable` reason.

The plan is invalid if its Rule application table omits a rule or uses vague claims such as “standard review,” “appropriate testing,” “as needed,” or “best practices” without a concrete owner, trigger, action, and exit.

## Deliver

Write the plan to the requested path. Report the path, input sources, role mapping, topology summary, non-minimal complexity decisions, uncovered ambiguities, and validation result. Do not start the plan.
