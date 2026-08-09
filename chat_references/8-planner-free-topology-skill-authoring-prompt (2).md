# Prompt to author a PLANNER skill — FREE-TOPOLOGY (composes the flow per step)

> Companion to the planner trio (#5/#6/#7), but instead of emitting ONE fixed
> topology, this skill DESIGNS THE TOPOLOGY ITSELF, per step, from a kit of
> components. Same KIND (three layers: this prompt → an agent writes a SKILL.md →
> that skill is a PLANNER that emits an execution plan; a further runner executes
> it). The skill never executes; all flow language is what it WRITES INTO THE PLAN.
>
> The defining ideas: (1) the planner has FREEDOM to break the task into whatever
> steps it wants and to wire whatever topology each step needs from the component
> kit; (2) a HARD bias against over-engineering — complexity causes bugs, so the
> simplest topology that fits wins; (3) two fixed governance invariants that hold no
> matter what topology is chosen — ONLY the orchestrator can block, and its validity
> audit is a COST-BENEFIT judgment, not a mere valid/invalid check.

```markdown
You are going to author a reusable Skill FOR YOURSELF and save it into this
environment's skills directory. The skill is a PLANNER with FREE CHOICE OF TOPOLOGY.
It does NOT build, review, test, or execute anything. Given (1) a product spec, (2) a
reference implementation plan, and (3) the user's choice of which concrete agent
backs each component role, the skill DECIDES how to break the task into steps and, PER
STEP, COMPOSES a multi-agent topology from a fixed kit of components — then EMITS that
as an execution plan. Its only deliverable is the plan document. Read this whole
brief, then follow it.

## STEP 0 — Discover before you write (do not skip)
1. Find where skills live here; open an existing SKILL.md to learn the exact format
   and the mechanism for MANUAL-INVOCATION ONLY. This skill must be manual-only.
2. Determine how a skill RECEIVES INPUTS at invocation (spec, reference plan,
   agent-per-role choices) and how it EMITS A FILE. This skill does not spawn
   subagents or call models — it only reads inputs and writes a plan.
3. Only if you cannot discover 1 or 2, ask me. Otherwise proceed.

## What this skill is and is NOT
- IS: a planner that (a) decides the step breakdown and (b) designs a bespoke
  multi-agent topology for each step from the component kit, producing an execution
  plan optimized for the task at hand.
- IS NOT: an executor. It never writes code, runs tests, spawns agents, or loops. All
  topology/loop language is content it WRITES INTO THE PLAN.
- The human's plan is a REFERENCE of required outcomes, not a fixed structure. The
  skill may re-decompose it, subject to COVERAGE (below). It does not invent new
  product scope or silently reinterpret requirements; it flags ambiguity instead of
  guessing.

## The ANTI-OVER-ENGINEERING mandate (the primary design bias)
Overcomplexity causes bugs. The process itself is a source of risk, not just the
code. Therefore:
- The planner picks the SIMPLEST topology that adequately fits each step. More
  components, more loops, more fan-out, and more review stages are COSTS, justified
  only by a real need in that step.
- Default to less. A trivial step may need nothing more than: orchestrator → one
  code writer → one doer runs a check → done. Do NOT bolt on adversarial reviewers,
  fan-out, or extra loops unless the step's risk/complexity genuinely warrants them.
- Reserve heavy topologies (multiple fanned reviewers, nested audit loops, long
  practical tests) for genuinely high-risk, high-complexity, or integration-critical
  steps.
- The plan must JUSTIFY complexity: for any step whose topology is more than minimal,
  state in one line why the extra machinery is warranted. Unjustified complexity is a
  defect in the plan.
- This bias is not a suggestion; it is the planner's primary optimization target
  alongside coverage. When in doubt, choose the simpler wiring.

## The COMPONENT KIT (what the planner may wire per step)
Each step's topology is assembled from these parts. The planner chooses which to
use, how many, and how they connect.
- ORCHESTRATOR — always present; singular; the only component with blocking power
  (see governance). Owns step specs/plans, triage, and all decisions.
- CODE WRITER(S) — write/edit code. Code writing is SINGULAR + SERIAL per step; do
  not wire concurrent writers on the same code (they collide). (Distinct,
  non-overlapping code areas may be sequenced, but never concurrent on shared code.)
- ADVERSARIAL REVIEWERS (fannable) — read code/output and give FEEDBACK only. May be
  a pool over disjoint conceptual slices. No blocking power.
  MANDATORY DESIGN-PRINCIPLES COVERAGE: whenever a step has ANY review at all (a
  single reviewer or a fan-out), AT LEAST ONE reviewer in that step must be assigned
  to check the work against the DESIGN PRINCIPLES below. This is not optional and
  does not scale away: one reviewer, that reviewer covers design principles (among
  other things); a fan-out of many, at least one of them owns design principles. The
  reviewer should reference the DESIGN PRINCIPLES SKILL (a separate skill in this
  environment — reference it by name/path if present; otherwise apply the gist
  below). Its feedback, like all feedback, is audited by the orchestrator under the
  cost-benefit rule (it does not block).
- UNIT/SMOKE TESTERS (fannable) — author unit/smoke tests. May be a pool over
  disjoint slices. No blocking power.
- DOERS (fannable) — run tasks and tests, INCLUDING long/practical end-to-end tests.
  May be a pool over disjoint slices. Report results; no blocking power.
- LOOPS — the planner may wire loops among the above (e.g. review→fix→re-review,
  or test→fix→re-test), of whatever shape the step needs, subject to the governance
  and termination rules below. Loops are a cost; use the fewest that fit.

## DESIGN PRINCIPLES (what the mandatory design-principles reviewer checks)
Reference the environment's DESIGN PRINCIPLES SKILL if present; otherwise apply this
gist. These are the criteria the mandatory design-principles reviewer audits against
(and the orchestrator weighs under cost-benefit):
1. CORRECTNESS — behaves the way the idea intends.
2. SIMPLICITY — Occam's razor. NO overengineering; never overengineer, double-guard
   something that already passes, or add "just in case" engineering. If it works, it
   works; if it doesn't, it doesn't. Weigh every extra feature/change heavily: does
   its benefit vastly outweigh the added maintenance effort, bug-fix effort, and risk
   of breaking something else? If yes, add it; if the benefit:cost ratio is poor,
   don't. Keep the minimal subset of the most valuable changes and features. (Same
   discipline as the anti-over-engineering mandate — here an active review criterion,
   not just a planner-side bias.)
3. GENERALIZABILITY — works for situations it has never seen.
4. NEATNESS — organized for reader and maintainer alike.
5. USABILITY — the code teaches its user how to use it.
6. DYNAMISM — solve the novel case with the existing pieces, not a new code change.

Mandatory coverage restated: any step that has review at all must have at least one
reviewer assigned to these principles (see the ADVERSARIAL REVIEWERS component). If
the planner composes a step with NO reviewer at all (permitted for genuinely trivial
steps under the anti-over-engineering bias), that is a deliberate choice the plan must
note — there is simply nothing to carry the design-principles check there, which is
acceptable ONLY when the step is trivial enough to need no review. Any step that
touches non-trivial design SHOULD include review, and therefore the design-principles
reviewer.

Interaction with the cost-benefit audit: a design-principles criticism is still just
FEEDBACK. A SIMPLICITY criticism ("this is overengineered") and a proposed ADDITION
are treated symmetrically — the orchestrator weighs whether acting improves the
benefit:cost ratio, and may rule the current implementation "not perfect, but
sufficient" either way. The principles guide the judgment; they never override it or
grant blocking power.

## Governance INVARIANTS (hold for EVERY topology the planner composes)
These are fixed. No composed topology may violate them.
1. ONLY THE ORCHESTRATOR CAN BLOCK. Reviewers, testers, and doers NEVER halt or gate
   progress on their own. They only produce FEEDBACK / RESULTS. Nothing they say
   forces a fix or stops the flow by itself.
2. ALL FEEDBACK IS AUDITED FOR VALIDITY BY THE ORCHESTRATOR. Every reviewer criticism
   and every test-derived complaint passes through the orchestrator, which decides
   what (if anything) happens. Feedback is a recommendation, never a command.
3. THE VALIDITY AUDIT IS A COST-BENEFIT JUDGMENT, NOT JUST VALID/INVALID. When the
   orchestrator audits a piece of feedback it determines:
     a. Is the issue REAL / valid at all? (If not → discard, log to out-of-scope.)
     b. Is it CODEBASE-BREAKING (breaks real functionality on a realistic path,
        data loss, crash, security/integrity)? → must be fixed.
     c. If NOT codebase-breaking → weigh the ADDED COMPLEXITY, EFFORT, and RISK of the
        fix against the benefit. If fixing costs more (in complexity/risk/effort) than
        the issue is worth, the orchestrator declares the current implementation
        "NOT PERFECT, BUT SUFFICIENT," logs the decision + reasoning to the
        out-of-scope ledger, and moves on. A fix that adds more risk than it removes
        is not worth making.
   This cost-benefit stance is the runtime embodiment of the anti-over-engineering
   mandate: the process must not gold-plate the product any more than it over-builds
   the process.
4. Parallelism NEVER splits decision-making. Fan-out is only for the DOING (review,
   testing, task execution); all fan-out MERGES back to a single orchestrator audit.

## COVERAGE (the one hard requirement on decomposition)
Whatever step breakdown the planner chooses, the plan must still implement, test, and
do EVERYTHING the reference plan required. Before designing, extract a COVERAGE
CHECKLIST (every discrete thing the reference plan implements/tests/does). The emitted
plan must map EVERY item to where it is built and where it is verified. No unmapped
item may remain — cover it or surface it. The planner may change HOW / ORDER / WHICH
components, never WHAT ultimately gets delivered.

## Step breakdown (free, but coherent)
The planner has freedom to break the task into whatever steps best fit it. Guidance:
compose steps by COHERENCE (a feature/deliverable per step), reusing the reference
plan's structure where it is already sensible (assess before rebuilding; don't re-cut
a good structure just to re-cut it). Do NOT make the process run on trivially small
fragments — group fine-grained modules into coherent steps. Respect genuine
dependencies in ordering; when independence is uncertain, keep it serial.

## Inputs at invocation
1. PRODUCT SPEC.
2. REFERENCE IMPLEMENTATION PLAN — reference of required outcomes, re-decomposable
   subject to coverage.
3. AGENT-PER-ROLE MAPPING — the USER picks which concrete agent backs each COMPONENT
   role (orchestrator, code writer, adversarial reviewer, unit/smoke tester, doer).
   The skill ASKS FOR / RECEIVES this at invocation. The user chooses only the agents;
   the skill decides the step breakdown, which components each step uses, pool sizes,
   loops, and wiring. Prompt clearly per role.

## What the SKILL DECIDES
- The step breakdown.
- Per step: which components are used, how many of each fannable component (pool
  sizes), what loops (if any), and how they connect — i.e. the whole topology.
- The disjoint-by-concept work splits for any fanned component (by planned
  feature/test/action/module — never actual code/test files), fixed at plan time.
- All of the above under the anti-over-engineering bias: minimal that fits.

## Termination rules to embed in the plan (no iteration cap)
Any loop the planner wires has NO max-iteration cap. Loops end only on SUCCESS,
STALL/NO-PROGRESS, or UNRECOVERABLE ERROR. Embed, per loop: stall on `stall_threshold`
consecutive no-progress iterations; same-signature-failure → stall; thrash/oscillation
(soft — the set of satisfied checks must trend up, not churn) → stop; scope-creep /
gold-plating churn (only cost-benefit-rejected feedback across iterations) → stop and
declare the step sufficient. Passed/satisfied checks are locked and not re-run;
re-runs are scoped to the specific change.

## THE EXECUTION PLAN THE SKILL MUST PRODUCE
### Plan Phase A — Coverage + step breakdown + per-step topology design
Extract the COVERAGE CHECKLIST. Decide the step breakdown (coherent steps; reuse
sensible reference structure). For EACH step, DESIGN ITS TOPOLOGY from the component
kit under the anti-over-engineering bias, and record it explicitly:
  - which components, how many of each, what loops, how wired;
  - the disjoint-slice split for any fanned component;
  - a COMPLEXITY JUSTIFICATION line for any step whose topology exceeds minimal;
  - confirmation that any step with review includes at least one DESIGN-PRINCIPLES
    reviewer (and, for any step with NO reviewer, a note that the step is trivial
    enough to need none);
  - confirmation the governance invariants hold (orchestrator-only blocking; feedback
    audited; cost-benefit on non-breaking issues; single-point decisions).
Attach the COVERAGE MAP (every checklist item → built where + verified where + which
step). No unmapped item may remain.

### Plan Phase B — Per-step execution (serial across steps)
For each step in order, the plan describes the composed topology to run: the
orchestrator drives it, code writer(s) build, any reviewers/testers/doers produce
feedback/results over their slices, everything MERGES to the orchestrator, which runs
the cost-benefit validity audit and decides fixes vs "sufficient." Loops (if wired)
iterate under the termination rules until the orchestrator judges the step done —
either satisfied, or sufficient-by-cost-benefit. Then advance.

### Plan Phase C — Whole-product check (planner's discretion)
The planner decides whether the task warrants a final whole-product pass (e.g. a doer
running long/practical end-to-end tests, with a reviewer + orchestrator audit) and
wires it — or, for a simple task, keeps it minimal. Under the anti-over-engineering
bias, this is included only if warranted. If included and it surfaces issues, they go
through the same orchestrator cost-benefit audit.

### Plan Phase D — Completion
Emit a final summary including: the out-of-scope ledger (with each "sufficient, not
perfect" decision and its cost-benefit reasoning), the coverage map, and the per-step
topology + complexity justifications.

## Config block the emitted plan must expose
Agent-per-component mapping (echoed); per-step topology descriptions (components,
pool sizes, loops, wiring, complexity justifications); disjoint-slice split maps;
COVERAGE CHECKLIST + COVERAGE MAP; scope_policy (tunes the cost-benefit threshold —
how readily "sufficient" is accepted); stall_threshold; pass/verify criteria;
file-handoff paths (including the out-of-scope / "sufficient" ledger).

## Deliverable
Write the SKILL.md (plus any supporting files) into the correct skills directory. When
invoked, the skill must: (1) receive spec + reference plan; (2) ASK the user which
agent backs each component role; (3) extract the coverage checklist, decide the step
breakdown, and design each step's topology from the kit under the anti-over-engineering
bias; (4) EMIT the execution plan — including per-step topologies, complexity
justifications, the governance invariants, and the coverage map. The skill must NOT
execute. Then reply to me with: (a) the path(s) created, (b) how a runner invokes it
and supplies inputs, (c) how/where it prompts for the agent-per-component choices, and
(d) what the emitted plan looks like — especially how per-step topologies are
represented and how the plan records orchestrator-only blocking + cost-benefit audits.
```
