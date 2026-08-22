# TOPOLOGY TEMPLATE LAYOUTS for skill #8 (free-topology planner)

> This is the output-shape companion for `8-planner-free-topology-skill-authoring-prompt.md`,
> analogous to what `5a` is for #5/#6/#7 — but because #8 COMPOSES a topology per
> step, this template is a MENU OF PRESETS keyed to step complexity, not one fixed
> per-step block. The planner classifies each step's complexity, picks the matching
> preset (or hand-wires a variant), and records the choice in the plan.
>
> Hand this to the authoring agent alongside prompt #8 as the topology vocabulary +
> output shape. The presets are DEFAULTS under the anti-over-engineering bias: pick
> the LOWEST tier that adequately fits; every tier above "simple" needs a one-line
> complexity justification. Governance is fixed across ALL tiers: only the
> orchestrator blocks; reviewers/testers/doers give feedback/results only; the
> orchestrator audits every piece of feedback under the cost-benefit rule (real? →
> codebase-breaking must-fix? → else weigh fix cost/risk vs benefit, may rule
> "sufficient, not perfect").
>
> THE +1 DESIGN-PRINCIPLES REVIEWER: in every preset that has ANY review, there is a
> dedicated reviewer — shown as `R★` — that checks PURELY for design principles
> (correctness, simplicity/anti-overengineering, generalizability, neatness,
> usability, dynamism; see #8's DESIGN PRINCIPLES section / the design-principles
> skill). It is ADDITIONAL to (a "+1" on top of) the functional reviewers `R1..Rn`,
> and its feedback is audited under the same cost-benefit rule — it does not block.

---

## Part 1 — Plan-level sections (fill once, like 5a)

### 0. Metadata
- Plan title, source reference plan, product spec, final/acceptance spec, timestamp,
  generating skill/version.

### 1. Agent-per-component mapping (user-supplied at invocation)
| Component role | Agent chosen | Notes |
|----------------|--------------|-------|
| orchestrator | `<agent>` | singular; only component that blocks |
| code writer | `<agent>` | singular + serial per step |
| adversarial reviewer (functional) | `<agent>` | fannable |
| design-principles reviewer (R★) | `<agent>` | the mandatory +1; may be same agent as above with a design-principles brief, or a distinct agent |
| unit/smoke tester | `<agent>` | fannable |
| doer (tasks + long/practical tests) | `<agent>` | fannable |

### 2. Coverage checklist (extracted from the reference plan)
| ID | Item (what must be implemented/tested/done) | Source in reference plan |
|----|---------------------------------------------|--------------------------|
| C1 | `<...>` | `<ref>` |

### 3. Step breakdown + complexity tier + topology choice
| Step | Feature/deliverable | Complexity tier | Preset used | Complexity justification (if > Simple) |
|------|---------------------|-----------------|-------------|----------------------------------------|
| S1 | `<...>` | Trivial / Simple / Complex | `<preset id>` | `<one line, or n/a>` |

### 4. Coverage map (nothing lost)
| Checklist ID | Built in (step) | Verified by |
|--------------|-----------------|-------------|
| C1 | S1 | `<tests / practical>` |

Gaps (must be empty to finalize): `<none | list>`

### 5. Config block
agent-per-component mapping (§1); per-step preset choices (§3); pool sizes per fanned
component per step; scope_policy (tunes the cost-benefit threshold — how readily
"sufficient" is accepted); stall_threshold; pass/verify criteria; test-ID scheme;
file-handoff paths incl. the out-of-scope / "sufficient, not perfect" ledger.

---

## Part 2 — Complexity-tiered topology PRESETS (pick one per step)

Legend: `O` orchestrator · `CW` code writer · `Rn` functional reviewer(s) ·
`R★` design-principles reviewer (+1) · `Tn` unit/smoke tester(s) · `Dn` doer(s) ·
`⟲` loop · `→` handoff · `⇒MERGE⇒` fan-out merge into single orchestrator audit.

---

### PRESET T0 — TRIVIAL STEP (minimal; no review)
Use ONLY when the step is genuinely trivial (config change, tiny isolated helper,
mechanical edit) and carries no real design risk. This is the one tier with NO
reviewer — so there is NO design-principles check here. The plan MUST note the step
is trivial enough to need none.

```
O → CW → D1 (quick check) → O audit → done
```
- Components: orchestrator, 1 code writer, 1 doer. No reviewers, no loop (or a single
  optional re-run if the check fails).
- Design-principles reviewer: ABSENT (justified only by triviality).

---

### PRESET S — SIMPLE STEP  → mirrors FLOW 3 / #7 (build, then review once)
Low-risk step: build it, then do ONE review + test pass. No per-iteration gating
during the build.

```
O → CW (build the step)
      → [ R1        ]              ┐
        [ R★ design ]  ⇒MERGE⇒  O audit (cost-benefit)
        [ T1 write+run smoke/unit ]┘
      → fix if orchestrator admits → re-run only affected checks ⟲ until sufficient/green
```
- Components: orchestrator, 1 code writer, 1 functional reviewer `R1`, the `R★`
  design-principles reviewer (+1), 1 tester `T1`. Optional single doer if a practical
  check is cheap.
- Fan-out: minimal (or none) — reviewers small.
- Loop: one lightweight fix loop, tests only.
- `R★` present: YES (any step with review carries the +1).

---

### PRESET C — COMPLEX STEP  → mirrors FLOW 4 / #5 (series loops + Checkpoint A + end audit)
High-risk / integration-critical step: one static-review loop that CLOSES at a
checkpoint, then a test loop (no re-review), and a heavy nested design audit held in
reserve.

```
O → CW
   LOOP 1 (static review, until Checkpoint A):
     ┌ R1..Rn ┐ functional, fanned
     │  R★    │ design principles (+1)
     └────────┘ ⇒MERGE⇒ O audit (cost-benefit) → fix ⟲ until only "sufficient" remains
   ═══ CHECKPOINT A ═══  (static review CLOSES for this step)
   → T1..Tn author smoke/unit (fanned)
   LOOP 2 (test, NO re-review):
     D1..Dn run checks (fanned) ⇒MERGE⇒ O audit → fix ⟲ until green/sufficient
   → (if this step includes the product's practical surface) D-practical runs the
     long/end-to-end test → O audit
       └ on repeated real failure: NESTED AUDIT LOOP revived →
            R★ + R1 find → O audits+plans → CW fixes → R★ re-audits (nested) ⟲ clean
            → new check written → D runs → O audit → (fail: back to find / pass: re-run practical)
```
- Components: orchestrator, 1 code writer, functional reviewers `R1..Rn` (fanned),
  `R★` (+1, present in LOOP 1 AND revived in the nested audit), testers `T1..Tn`,
  doers `D1..Dn` including a practical/end-to-end doer.
- Static review closes at Checkpoint A; nested deep audit is dormant unless the real
  product repeatedly fails.
- `R★` present: YES in LOOP 1, and specifically re-included in the nested audit loop
  (design principles matter most when the real product is fighting you).

---

## Part 3 — Per-step topology record (fill one per step, referencing the preset)

### Step `<S#>`: `<feature>` — tier `<T0/S/C>`, preset `<id>`
- Modules/scope covered: `<...>`
- Complexity justification (if tier > Simple): `<one line>`
- Components used: `<O, CW, R1.., R★, T1.., D1..>`
- Pool sizes: functional reviewers `<n>`, testers `<n>`, doers `<n>`
- Design-principles reviewer R★: `<present + where in the flow | absent because trivial>`
- Fan-out slices (disjoint, by concept — feature/test/module, never code files):
  | Component slot | Slice |
  |----------------|-------|
  | R1 | `<...>` |
  | R★ | design principles across the whole step's output |
  | T1 | `<...>` |
  | D1 | `<...>` |
- Loops wired: `<none | one test loop | LOOP A+B | LOOP 1→CkptA→LOOP 2(+nested audit)>`
- Governance confirmation: only O blocks ✔ · all feedback audited ✔ · cost-benefit on
  non-breaking issues ✔ · single-point decision (fan-out merges to one audit) ✔

---

## Part 4 — Whole-product close (planner's discretion, anti-over-engineering)
Only if warranted by the task: a final doer runs the long/practical end-to-end test
over the whole product; a functional reviewer + `R★` review the whole; the
orchestrator audits under cost-benefit. For simple products, keep this minimal or
fold it into the last step. Emit the final summary: out-of-scope / "sufficient, not
perfect" ledger (with cost-benefit reasoning), coverage map, and the per-step
topology + complexity justifications.

---

## Tier-selection quick guide (for the planner)
- **T0 Trivial:** no design risk, mechanical/isolated. No review (note triviality). No R★.
- **S Simple:** low risk; build then one review+test pass. R★ present.
- **C Complex:** high risk / integration-critical; series loops + Checkpoint A + reserved
  nested design audit + practical test. R★ in review loop and revived in nested audit.
Pick the LOWEST tier that adequately fits. Overshooting the tier is over-engineering
the process — itself a design-principles (simplicity) violation.

Deliberately EXCLUDED: the "full per-step QA" shape (flow 2/6) — review-and-test
gating at every step WITH re-review bounce-back. It is the most expensive topology of
all (strictly heavier than Complex/4-5, which caps static review at one pass per step)
and buys little over Complex. It is hyper-inefficient and not a useful default, so it
is not offered as a preset. If a step truly needs more than Complex, that is a signal
the step is mis-scoped — split it — not a reason to gate harder.
