# Prompt to author a PLANNING skill (emits a multi-agent execution plan; does not execute)

> This is a PROMPT you hand to an agent so it authors a SKILL.md. Read the layers
> carefully — they are the whole point of this variant:
>
> - The agent you give this to → **writes a SKILL.md.**
> - That skill, when a downstream runner invokes it, is a **PLANNER**. Fed a spec,
>   a pre-modularized implementation plan, and the user's choice of which agent
>   backs each role, it **emits a multi-agent EXECUTION PLAN** — the serial step
>   flow, the skill's own pool-sizing and disjoint-by-concept work splits, and the
>   triage/merge rules — as its deliverable.
> - A FURTHER runner later executes that plan (spawning coders/reviewers/doers).
>
> The skill itself NEVER runs coder-main / reviewer-main / doer-main. It only
> plans how they will be run. The execution semantics below (serial flow, two
> series loops per step, Checkpoint A, final practical-test + nested static audit)
> describe the plan the skill must PRODUCE — not behavior the skill performs.

```markdown
You are going to author a reusable Skill FOR YOURSELF and save it into this
environment's skills directory. The skill is a PLANNER. It does NOT build, review,
test, or execute anything. Given (1) a product spec, (2) a fully pre-modularized
implementation plan, and (3) the user's choice of which concrete agent backs each
role, the skill PRODUCES A MULTI-AGENT EXECUTION PLAN describing how a downstream
runner should carry the work out. Its only deliverable is that plan document.
Read this whole brief, then follow it.

## STEP 0 — Discover before you write (do not skip)
Do not assume the skill format or API from memory. First:
1. Find where skills live here and open at least one existing SKILL.md to learn
   the exact frontmatter/format, and specifically the mechanism for marking a
   skill as MANUAL-INVOCATION ONLY (never auto-triggered). This skill must be
   manual-only.
2. Determine how a skill in this environment RECEIVES INPUTS at invocation (the
   spec, the pre-modularized plan, and the agent-per-role choices) and how it
   EMITS A FILE as its deliverable. This skill does not spawn subagents or call
   models — it only reads inputs and writes a plan — so you do NOT need the
   subagent-spawning API here. You DO need input-passing and file-output.
3. Only if you cannot discover 1 or 2, ask me before proceeding. Otherwise proceed.

## What this skill is and is NOT
- IS: a planner that turns a human-made reference implementation plan into
  a concrete multi-agent EXECUTION PLAN — with its own decomposition, optimized
  for parallel execution where safe, covering everything the reference plan required.
- IS NOT: an executor. It never writes code, never runs tests, never spawns
  coder/reviewer/doer agents, never loops over anything. All the loop/flow
  descriptions below are things the skill WRITES INTO THE PLAN, not things it does.
- The human's plan is a REFERENCE, not a fixed structure. The skill MAY completely
  rewrite the modules, phases, and decomposition — inventing its own breakdown
  optimized for the parallelized multi-agent flow. It is NOT bound to the human's
  module boundaries, ordering, or phasing.
- THE ONE HARD REQUIREMENT — COVERAGE: whatever decomposition the skill designs, it
  must still implement, test, and do EVERYTHING the original plan implemented,
  tested, and did. Nothing the original plan required may be dropped, weakened, or
  lost. The skill may change HOW and in WHAT ORDER and by WHICH agents, but never
  WHAT ultimately gets delivered. The reference plan defines the full set of
  required outcomes; the skill's plan must cover all of them.
- ASSESS-BEFORE-REBUILD — DO NOT re-decompose reflexively: re-decomposition is a
  LICENSE, not an obligation. Before rewriting anything, the skill must AUDIT the
  reference plan's existing structure and ask: is it already parallelized well? Do
  its modules/phases already make sense and map cleanly onto the multi-agent flow
  (disjoint conceptual slices, sane ordering, honored dependencies, pool-friendly)?
  If the existing decomposition is already good, REUSE IT — wholesale where it fits,
  partially where only parts fit. The skill only re-cuts a module/phase when it can
  ACTUALLY MAKE IT BETTER for this flow (more/safer parallelism, cleaner disjoint
  slices, better dependency ordering) — not just to have re-done it. "The work is
  already cut out and sensible" → keep it. Never automatically re-break a good plan
  into new chunks every time. The emitted plan must state, for each part, whether it
  was REUSED AS-IS, REUSED WITH MINOR ADJUSTMENT, or RE-DECOMPOSED — and for anything
  re-decomposed, a one-line reason it is genuinely better in the multi-agent flow.
- To make coverage auditable, the skill MUST, before designing anything, extract
  from the reference plan a COVERAGE CHECKLIST: every discrete thing the original
  plan implements / tests / does, as individual line items. Then its emitted plan
  must map EVERY checklist item to the place(s) in the new decomposition where that
  item is built and where it is tested. Any item not mapped is a coverage gap and
  the skill must not finalize a plan with gaps — either cover it or surface it.
- The skill still does not INVENT NEW product scope beyond the reference plan, and
  does not silently reinterpret requirements. If the reference plan is ambiguous
  or looks under-specified, it flags that rather than guessing. (Rewriting the
  DECOMPOSITION is allowed; expanding or narrowing the PRODUCT is not.)
- Code writing still stays SINGULAR and SERIAL (coder-main is one agent); no
  decomposition the skill invents may create concurrent coders. Parallelism is
  still only intra-stage fan-out of the DOING (test authoring, test execution)
  over disjoint conceptual slices, always merging back to one orchestrator triage.
- Preserve genuine DEPENDENCIES: the skill's invented ordering must never schedule
  work concurrently with (or ahead of) work it truly depends on. When two pieces
  are not truly independent, keep them serial. When in doubt about independence,
  keep it serial.

## Inputs the skill receives at invocation
1. PRODUCT SPEC — the description of the finished product.
2. REFERENCE IMPLEMENTATION PLAN — the human's breakdown of the work into
   modules/steps/tasks. Used as a REFERENCE defining the full set of required
   outcomes (everything that must be implemented/tested/done), NOT as a fixed
   structure. The skill may fully re-decompose it (see "What this skill is and is
   NOT"), subject to the coverage requirement.
3. AGENT-PER-ROLE MAPPING — the USER decides which concrete agent backs each role.
   The skill ASKS FOR / RECEIVES this at invocation. The user chooses ONLY the
   agent behind each role; the skill decides everything else (pool sizes, splits,
   flow). Roles to be filled by the user's chosen agents:
     - orchestrator/planner-executor (the runtime orchestrator; singular)
     - coder-main (singular)
     - reviewer-main (this is a POOL — see below; user picks the agent, skill
       picks the count)
     - doer-main (this is a POOL — see below; user picks the agent, skill picks
       the count)
     - final-reviewer (freshly spawned at final phase; user picks the agent)
   If a downstream role could be backed by a different agent than another, let the
   user specify per role. Prompt clearly for each.

## What the SKILL DECIDES (not the user, not at runtime)
- POOL SIZES: how many reviewer-main writers and how many doer-main runners the
  plan calls for, based on the shape of the skill's own decomposition (e.g. number
  of independent conceptual areas). Coder-main and the orchestrator are singular.
- DISJOINT WORK SPLITS, BY CONCEPT: for every stage that fans out across a pool,
  the skill decides — AT PLAN TIME — how the work is partitioned into
  NON-OVERLAPPING slices. The split is by CONCEPT: planned features, planned
  tests, planned actions, or module boundaries from the human's plan — NEVER by
  actual code or actual test files (none exist at planning time). This split is a
  fixed part of the emitted plan; it is not re-decided during execution.
- THE SERIAL FLOW ITSELF: the ordered step-by-step execution plan (below), written
  out concretely for the given modules.

## Serialism vs parallelism (the plan must encode this exactly)
- The overall FLOW is SERIAL. Steps run in order; step N fully completes before
  step N+1 begins.
- CODE WRITING is SERIAL and SINGULAR: coder-main is one agent. Never parallelize
  code writing (concurrent writers would collide).
- ORCHESTRATION / TRIAGE / DECISION-MAKING is SINGULAR: parallelism NEVER splits
  decision-making. All fan-out merges back to ONE orchestrator triage.
- The ONLY parallelism is intra-stage FAN-OUT of the DOING: multiple reviewer-main
  writers authoring tests concurrently over disjoint conceptual slices, and/or
  multiple doer-main runners executing disjoint conceptual slices concurrently.
- MERGE-THEN-TRIAGE: wherever a pool fans out, the plan specifies a merge point —
  the orchestrator waits for all pool members, concatenates + de-duplicates their
  outputs, and THEN triages once over the merged set. Fan-out for doing; single
  triage for deciding.

## Guiding principle to embed in the plan
The plan is for delivering a WORKING product EFFICIENTLY, not a perfect one. It
must instruct the runtime to fix real functional defects and NOT gold-plate: no
chasing speculative edge cases that already work in ~99.9% of real use, no rigor
for its own sake, no letting review or the suite grow just to keep a loop alive.
Every unit of work traces to the product spec's real functionality.

## Triage model to embed in the plan
The plan must specify that, at runtime, reviewer output is CLASSIFIED as:
- FUNCTIONAL DEFECT (broken behavior on a realistic, non-trivial usage path) →
  VALID, admit + fix.
- EXTRANEOUS / GOLD-PLATING (edge cases already fine in ~99.9% of real use,
  speculative hardening, stylistic rigor, hypotheticals, invented complexity) →
  INVALID for the goal; log to an out-of-scope ledger and drop.
The reviewer's label is a RECOMMENDATION; the single orchestrator decides, biasing
toward shipping. Include a user-tunable `scope_policy` knob in the plan.

## Scoping model to embed in the plan (passed tests locked; gap tests only)
The plan must specify: a persistent PASSED REGISTRY of test IDs; once a test
passes it is locked and NOT re-run; only GAP TESTS (currently failing, or newly
implicated by a triaged-in criticism or a specific change) are ever re-run; a
change re-runs ONLY the still-failing gap tests + failed unit tests + any new
tests for that specific change. Passed tests never re-run mid-loop. Include a
stable test-ID scheme (e.g. file::path::testname) and require each planned fix to
record which test ID(s) it must make pass. NOTE: since the skill only plans, it
expresses these as RULES the runtime follows, referencing PLANNED tests by concept
(actual test IDs are assigned at execution time from these rules).

## Termination rules to embed in the plan (no iteration cap)
The plan must specify that NO loop has a max-iteration cap. Loops end only on
SUCCESS, STALL/NO-PROGRESS, or UNRECOVERABLE ERROR. Include, as rules the runtime
applies per loop:
- STALL: `stall_threshold` consecutive no-progress iterations → stop + report.
- SAME-SIGNATURE FAILURE: identical error signature across fix attempts → stall.
- THRASH / OSCILLATION (soft): tests flipping pass↔fail without the passed set
  net-growing → treat as no progress, stop + report. Judgment-based; passed set
  should trend up.
- SCOPE-CREEP / GOLD-PLATING CHURN: only-extraneous findings across iterations →
  stop that loop, declare working.

## THE EXECUTION PLAN THE SKILL MUST PRODUCE
The skill's output is a plan describing this flow (serial, with the fan-out and
splits the skill decides). It must lay this out concretely for the given modules:

### Plan Phase A — Coverage extraction + audit + (re-)decomposition
First, extract the COVERAGE CHECKLIST from the reference plan: every discrete thing
it implements / tests / does, as individual line items. Next, AUDIT the reference
plan's EXISTING decomposition against the multi-agent flow: is it already well
parallelized, with sensible modules/phases, disjoint slices, sane ordering, and
honored dependencies? REUSE whatever already fits (as-is or with minor adjustment);
only RE-DECOMPOSE the parts you can genuinely improve for this flow. Do not re-cut a
good structure just to re-cut it. Then present the resulting ordered step list —
reused and/or newly designed. Attach: the skill's decided pool sizes, the
disjoint-by-concept split map for every parallelizable stage, a DISPOSITION note per
part (reused as-is / reused with minor adjustment / re-decomposed, with a one-line
reason for each re-decomposition), and a COVERAGE MAP proving every checklist item
is covered (which module builds it, which tests verify it). The skill must not
finalize a plan with any uncovered checklist item — cover it or surface it. Respect
genuine dependencies; when independence is uncertain, stay serial.

### Plan Phase B — Per-step (SERIAL across steps): TWO SERIES LOOPS
For each step, the plan specifies two back-to-back SERIES loops (not nested):

LOOP 1 — STATIC REVIEW (iterate until Checkpoint A is clean):
  planner writes/updates step spec + plan → coder-main (singular) writes/fixes
  code → reviewer-main POOL performs static review over disjoint conceptual slices
  (per the pre-decided split) → MERGE → single orchestrator triage.
    - valid static defects remain → fix → repeat LOOP 1.
    - only extraneous remain → exit.
  ═══ CHECKPOINT A ═══ static review CLOSES for this step, PERMANENTLY.

(after Checkpoint A) reviewer-main POOL writes SMOKE + UNIT tests over disjoint
  conceptual slices (per the split). These planned tests form the step's gap set.

LOOP 2 — TEST (iterate until green; NO static review):
  doer-main POOL runs the gap set over disjoint conceptual slices concurrently →
  MERGE findings → reviewer-main reviews/classifies → single orchestrator triage.
    - fail → planner + coder-main fix → re-run ONLY still-failing gap tests +
      failed unit tests + any new tests for that specific change → repeat LOOP 2.
    - pass (green / only extraneous) → STEP COMPLETE → next step.

### Plan Phase C — Final phase on the finished product
C0: SPAWN A FRESH final-reviewer (the user's chosen agent for that role).
C1: final-reviewer takes the prewritten final/acceptance spec, tweaks it only if
    genuinely needed, and (as a POOL if sized >1) writes the full UNIT + SMOKE set
    over disjoint conceptual slices of the whole product.
C2: FINAL TEST LOOP (series, no static review; mirrors Loop 2): doer POOL runs →
    merge → review → single triage → fix → repeat until pass.
C3: PRACTICAL TEST — doer-main launches the real end-to-end run.
    - pass → run Safeguard → DONE.
    - fail → enter C4.
C4: NESTED STATIC-AUDIT LOOP — the ONLY place static review is revived: reviewer
    finds defects → orchestrator audits + plans → coder-main fixes → REINTRODUCE
    the static audit reviewer (nested) until clean → new test(s) written → doer
    runs → review → (fail: back to top of C4 / pass: re-run practical test C3).
    Dormant during the whole build; exists solely for repeated real-product fails.

### Plan Phase D — Completion + Safeguard
Once the practical test passes, run the FULL accumulated suite EXACTLY ONCE
(user-toggle `final_full_verification`, default true) to catch regressions from
locked-passed tests; on regression, return the test to the gap set and resume the
relevant loop. Emit a final summary including the out-of-scope ledger.

## Config block the emitted plan must expose (user-editable)
- the agent-per-role mapping the user supplied at invocation (echoed back)
- the skill-decided pool sizes for reviewer-main and doer-main (clearly labeled as
  the skill's decision, editable by the user if they wish to override)
- the disjoint-by-concept split map for each parallelizable stage
- the COVERAGE CHECKLIST (extracted from the reference plan) and the COVERAGE MAP
  (every checklist item → where it is built + where it is tested in the skill's new
  decomposition), so the human can confirm nothing from the original plan was lost
- the DISPOSITION note per part (reused as-is / reused with minor adjustment /
  re-decomposed + one-line reason), so the human can see what was kept vs changed
- scope_policy, stall_threshold, gap_scope, final_full_verification
- pass_criteria, test-ID scheme, and the file-handoff paths (findings, reviews,
  out_of_scope ledger, passed registry, step/final artifacts)

## Deliverable
Write the SKILL.md (plus any supporting files) into the correct skills directory.
The skill, when invoked by a runner, must: (1) receive the spec + the reference
implementation plan; (2) ASK THE USER which agent backs each role; (3) extract the
coverage checklist, then itself decide the decomposition, pool sizes, and the
disjoint-by-concept splits; (4) EMIT the multi-agent execution plan described above
as a file, including the coverage map proving nothing from the reference plan was
lost. The skill must NOT execute the plan. The emitted plan MUST follow the fixed
template shape the human supplies alongside this brief (the "EXECUTION PLAN
TEMPLATE") — same sections, same order — so the downstream runner always receives a
predictable structure. Then reply to me with: (a) the path(s)
you created, (b) how a runner invokes the skill manually and how it supplies the
spec + reference plan, (c) exactly how/where the skill prompts the user for the
agent-per-role choices, and (d) what the emitted plan file looks like (its
structure/sections, including the coverage map) so I know what the downstream
runner will receive.
```
