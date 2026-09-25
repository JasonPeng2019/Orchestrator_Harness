# Memory-backed harness implementation plan

Status: accepted for execution  
Revision: R8  
Topology: Level 3 — fixed implementation lanes with one decision owner  
Decision owner and integrator: ROOT (the active assistant session)

## 1. Outcome and authority

Build and verify the complete current fixed-strategy memory-backed harness in
`development/product/worktree_example`.

The behavioral authority is
`new_harness_memory_docs/PRODUCT_FEATURE_SPEC_v65.md`. The binding engineering
and verification contract is
`new_harness_memory_docs/PRODUCT_IMPLEMENTATION_SPEC_v67.md`. Concepts and the
Detailed v72 ledger explain intent and source observations but add no
requirements. Direct user instructions and repository instructions remain
higher authority.

The delivered product includes reviewed local experience, cases and approved
skills, five local template families, scoped Atlas procedure publication and
Vector Search retrieval, Standard/Problem-focused/Deeper fixed search, APC
direct fill/light adaptation/fresh-plan fallback, exact context and dispatch
binding, trust/privacy/revocation, outcomes and usage, feature switches,
recovery, snapshots, operator commands, and one synthetic integrated demo.

The following are expressly outside this plan:

- every benchmark, benchmark subset, scored comparison, leaderboard run, or
  benchmark-specific runner;
- the learned search-strategy selector, including learner dependencies,
  policy storage, training, inference, updates, and replay;
- deployment, publication, or redistribution of the finished repository;
- a second scheduler, review system, memory engine, generic secret manager,
  dashboard, or generalized harness framework; and
- speculative hardening or frozen-harness enhancements not required by a
  reproduced blocker in this implementation run.

Implementation, local commits/worktrees, scoped synthetic service operations,
and the required native development verification are already authorized by the
user for this run. Push, public release, benchmark execution, and learned-selector
work are unreachable from this plan.

## 2. Starting point

- Product repository `P` is
  `development/product/worktree_example`, clean on `main` at `a54ad14` when this
  plan was written. No memory-product package exists yet.
- The dogfood builder is the frozen `references/harness-single` at `0bf0579`.
  Its narrow launch, bootstrap, and lease-lock manifest repairs are proven. Do
  not modify or broadly requalify it unless changed builder bytes or a reproduced
  defect invalidate that proof. Run-scoped resource declarations are not builder
  requalification; validate only their manifest load and first affected launch.
- The deployed outer harness is `development/dogfood/harness`; its
  `root_workspace` points at `P`. The abandoned formal-plan runtime is closed.
- Native implementation worktrees are created by that harness beneath
  `P/.harness-runtime/worktrees/<epoch>/<lane>`. Workers never create a second
  worktree scheme.
- `.plans/SUBAGENT_ROLE_MODEL_MAPPING.json` and
  `development/test-tools/resolve-role.py` are the existing single launch-binding
  source and projection. The mapping embodies the user's later development-run
  allocations where they differ from the specification's earlier named test
  matrix; evidence reports the binding actually launched and makes no broader
  model-support claim. Resolve only the role needed for the next lane. Do not
  repeat the old all-role admission sweep before ordinary work.
- Historical `development/evidence/STEP-001` records prove the builder and
  fixtures worked; they are history, not a new product milestone and not a
  reason to replay readiness work. The unfinished M08 report is abandoned with
  the retired plan.

## 3. Why Level 3 is sufficient

One agent plus review is too small because the EverOS experience path and Atlas
procedure path are substantial, source-distinct integrations that can be built
independently after a shared contract is frozen. They therefore get separate
writers and worktrees.

Tier 4 is not justified. This development has no live migration, irreversible
rollout, or continuously changing cross-lane authority. One ROOT can freeze the
shared schema, integrate two disjoint adapter lanes in a fixed order, and own the
remaining shared product seams serially. The nested candidate-harness test ROOT
is required by the product specification for development evidence; it is a
bounded test lane, not another project-management tier.

```text
A. contracts + executable thin slice
                  |
          +-------+-------+
          |               |
B. local experience   C. Atlas procedures
          |               |
          +-------+-------+
                  |
D. one shared-seam lane
   phase 1: search/templates/APC/context
   phase 2: recovery/usage/snapshots/operator surface
                  |
E. frozen-candidate verification and closeout
```

ROOT alone decides and authorizes shared-contract changes, accepts lane results,
integrates commits, authorizes live/scoped resources, and makes the final release
claim. Stage A's `complex_writer` is the sole writer of the initial shared-contract
implementation.
The B/C split is justified by disjoint ownership and failure isolation, not an
assumption that their preferred providers can run simultaneously.

## 4. Ownership and execution stages

`P/src/memory_harness/` is the new product package. The package layout below is
an ownership boundary, not a requirement to reproduce the prose specification
as modules. A writer may refine private filenames while preserving the named
public seam and its tests.

| Stage | Owner / lane | Finished outcome | Writer-owned paths | Primary verification obligations | Exit |
|---|---|---|---|---|---|
| A — contracts and thin slice | `complex_writer`; one implementation lane | Installable package, one schema owner, durable local decision/outcome store, privacy/config guards, exact harness handoff, and the smallest real path through reviewed evidence, a deterministic Atlas-adapter fixture, direct-fill/fresh fallback, one real configured APC child, linked outcome, and reconciliation | `P/pyproject.toml`, product lock, `P/src/memory_harness/{contracts,config,evidence,privacy,experience,atlas,templates,apc}/` for the minimum slice, shared package exports, `P/tests/local/{contracts,privacy,integration}/`, and only the minimum candidate-harness seams required by the slice. A then hands the four adapter/behavior directories to B, C, and D | Implementation T02, T03, T17, T18, T21; focused tests plus one narrow nested candidate smoke through the Section 6 chain | ROOT verifies the diff/checks through either a valid native result or the Section 8 administrative-recovery rule, runs the narrow nested smoke, integrates A, freezes the public contracts, and refreshes `HANDOFF.md` |
| B — local experience | `writer`; one implementation lane | Reviewed success/failure capture, recent evidence, EverOS case/skill extraction, exact provenance, and approved/generated-skill boundaries | `P/src/memory_harness/experience/`, `P/tests/local/experience/`, and demonstrably necessary focused changes/tests under `P/harness/vendor/everos/` | T04, T05; focused unit/source-adapter tests and one scoped real EverOS path | Clean commit plus either a valid native result or the Section 8 verified administrative-recovery path; ROOT integrates B first |
| C — shared procedures and Atlas | `writer`; one implementation lane | Procedure content/approval/current/revocation lifecycle, partitioned publication, exact reads, scoped Atlas Vector Search, representation identity, and reconciliation of ambiguous operations | `P/src/memory_harness/{procedures,atlas}/`, `P/tests/local/{procedures,atlas}/`, `P/tests/live/atlas/`, and scoped index/bootstrap definitions. C returns tested command contracts and integration notes; it does not write the user-facing runbook | T06–T09; focused unit/source-adapter tests and one scoped live Atlas adapter/lifecycle observation in a unique synthetic namespace | Clean commit plus either a valid native result or the Section 8 verified administrative-recovery path; ROOT integrates C after B |
| D phase 1 — search, templates, APC and context | `complex_writer`; phase 1 of one D implementation lane | Five templates, cross-store normalization, eligibility/freshness, fixed search recipes and budgets, APC branches, child delegation, context assembly, dispatch finalization, and feature resolution | `P/src/memory_harness/{search,templates,apc,context,composition}/`, template assets, `P/tests/local/{search,templates,apc,context,composition,features,security}/`, and serialized candidate-harness/provider composition seams | T10–T16; focused deterministic/fault tests and affected candidate-harness smoke | The D writer remains in the same worktree, runs focused phase-1 checks, and continues to phase 2 without an integration/result boundary |
| D phase 2 — recovery and operator completion | Same D writer, worktree, and result | Idempotent outcome/operation reconciliation, native usage accounting, crash/concurrency behavior, snapshots, network-mode truth, CLI/setup/readiness/demo operations, and operator documentation | `P/src/memory_harness/{evidence,reconcile,usage,snapshots,cli}/` including the final demo entrypoint, `P/tests/local/{recovery,usage,snapshots,cli}/`, `P/tests/native/`, the sole user-facing product README/runbook consuming C's tested commands, and shared evidence code handed off from A | T19, T20, T22–T24; focused restart/fault/concurrency tests and snapshot restore | D returns one clean commit and either a valid native result or the Section 8 verified administrative-recovery path; ROOT runs only D's focused phase checks, integrates once, and refreshes `HANDOFF.md` |
| E — integrated verification | `test_root`; one outer verification lane with only the required inner test roles/child | All-off baseline, isolated candidate product-harness execution, required development bindings, real configured APC child, actual scoped Atlas Vector Search demo, independent important-closeout review, exact cleanup, and reproducible operator path | Disposable fixture repositories, native run state, and scoped service namespaces only. Candidate product source and committed tests are frozen | T01 and T25–T29, plus integrated interactions whose earlier evidence remains input-compatible | Every current required claim has actual evidence; limitations are honest; resources are closed; final `HANDOFF.md` and operator docs agree |

The table maps every Implementation Section 15.2 obligation exactly once to its
primary owner. A test can cover several rows, and a cross-stage integration test
can consume earlier behavior; neither fact creates a second checklist or evidence
copy. The Feature specification still governs behavior beyond the test labels.

Primary ownership does not erase cross-boundary assertions. Whenever B through D
adds a new consumer, that consumer gets path-local T17/T18 credential and privacy
checks; D phase 1 also proves T06 compact procedure meaning survives context
packing and T21 fixed strategies need no learner artifact. E observes the native
portions of T17, T20, T22, and T24 against the integrated candidate. These are
assertions in the owning path's focused test or the final native wave, not copied
suites or a second evidence ledger.

## 5. Lane contracts and integration order

Every implementation lane receives one native harness task card containing:

- the finished outcome from the table above;
- exact allowed write paths and protected paths;
- the frozen base commit and consumed public contracts;
- the focused checks it must run;
- the required native return: outcome, changed files, commands and actual
  results, assumptions/integration notes, and unresolved risks; and
- the rule that it may not merge, push, edit another lane, launch additional
  implementation agents, or broaden the frozen harness. Product/test children
  expressly named by A or E's acceptance check remain allowed only through
  ROOT-authorized scoped resources.

The native `RESULT.json` is the sole requested worker report and the preferred
native completion path; it is not an unconditional behavioral gate. ROOT uses the
harness's completion review and the Git commit/diff when valid. Under the narrow
Section 8 exception, ROOT may instead accept a verified clean implementation while
the harness truthfully retains an administrative lane failure. ROOT never requests
a second bespoke report, acceptance JSON, progress JSON, hash manifest, or copied
test transcript.

Execution order is fixed:

1. ROOT dispatches A serially, freezes its candidate commit, runs the narrow
   nested smoke, integrates A, then freezes its public contracts.
2. B and C branch from that exact integrated commit into independent worktrees.
   They may both be admitted, but provider sessions overlap only when their
   resolved bindings and resources are actually isolated; shared Ollama launches
   serialize through the Section 6 resource.
   Neither may edit the package manifest, common exports, shared schemas,
   candidate-harness code, or the other's directories.
   While they are active, ROOT launches the first of exactly two planned
   implementation-review points as one independent native `reviewer` lane
   against integrated A. It is read-only: inspect A's public contract,
   privacy/security boundary, diff, tests, and existing thin-slice evidence; make
   no edits, launch no children, and rerun no tests. Its native result returns
   PASS, concrete requirement/evidence findings, or a named missing-input BLOCKED
   state. ROOT adjudicates the response before D. A valid shared-seam finding does
   not authorize the reviewer to force B/C to replay unaffected work.
3. ROOT integrates B then C. After each integration it runs only the contract and
   adapter checks affected by that commit. A conflict or requested contract
   change returns to ROOT; the workers do not negotiate it.
4. One D writer performs phases 1 and 2 serially in one worktree and returns one
   commit/result. ROOT integrates D once after its focused phase checks.
5. ROOT freezes one candidate. E may mutate disposable fixture repositories and
   its owned runtime/service namespaces, but not candidate product source.
   Product defects return to the owning implementation stage; a fix creates a
   newly identified candidate and reruns only invalidated evidence.

After ROOT preserves the commit and actual evidence, a valid accepted lane closes
with native `lane retire`; an administrative-failure lane closes with native
`lane force-stop --lane-id <exact-recorded-id>`. The applicable command must
confirm exact process cleanup and lease release before a dependent launch or
worktree removal. ROOT then inspects worktree status and removes only a clean,
disposable worktree; dirty or uncertain worktrees are never force-removed.

## 6. Harness and development-test topology

All coding workers run through the frozen outer harness at
`references/harness-single` as deployed in `development/dogfood/harness`. Native
platform subagents are not implementation substitutes. The existing role mapping
is read immediately before dispatch; ROOT explicitly selects any allowed fallback
only after the mapping's stated provider failure and cleanup rule.

Before the first outer Ollama-backed dispatch, ROOT ensures the deployed
`resource-manifest.json` contains exactly one
`{"id":"ollama-provider-home","exclusive":true}` entry: preserve an identical
entry on resume and reject a conflicting duplicate. Every resolved outer launch with
`launch_config.launcher=ollama` claims `ollama-provider-home` through the
native `exclusive_resources` field; direct fallbacks do not inherit that claim.
This is dogfood run configuration, not a frozen-harness source change.

A's narrow early smoke uses only the minimum binding topology:

```text
outer implementation ROOT and frozen harness
  -> delegated product-test ROOT
       -> isolated candidate product harness
            -> near-match preparation launches APC drafting child
            -> proposal returns to product-test ROOT
            -> ROOT validates and accepts the parent plan
            -> candidate dispatches one synthetic execution worker
            -> linked outcome and cleanup
```

The single A assurance review is the Section 5 review point; it is not another
inner closeout reviewer. E alone uses the complete final topology:

```text
outer implementation ROOT and frozen harness
  -> delegated product-test ROOT
       -> isolated candidate product harness
            -> required synthetic test workers
            -> APC drafting child from explicit apc_adaptation_binding
            -> important-closeout reviewer
```

The A wave proves only the shared handoff, deterministic Atlas-adapter fixture,
configured APC child, linked outcome, and cleanup; it makes no release claim and
does not exercise the full role matrix. The E wave proves the complete frozen
candidate. Before either launch, ROOT closes the implementation writer through
the applicable native retire/force-stop path and releases its shared claims. The
test ROOT preflights inner worker slots and provider-home
isolation so the parent holds no resource needed by its children. If capacity or
isolation is unavailable, only dependent native coordinates are BLOCKED while
independent checks finish.

The test ROOT owns only its candidate wave, test cards, synthetic fixtures,
service namespaces, children, and cleanup. It does not repair product code or
accept the release. No third orchestration tier is allowed. Ordinary deployed
startup must remain independent of this outer test arrangement.

For T26, deterministic configuration fixtures prove that two supported APC
bindings can be selected without source edits. Native evidence exercises only
the user's selected live tuple; identical selected A/B profiles do not become a
claim of live model diversity.

## 7. Verification design

Use the cheapest boundary that decides each claim:

- deterministic schemas, eligibility, fallback, privacy, retry, and fault
  behavior: focused unit/contract tests with independent expected values;
- EverOS and MongoDB package assumptions: focused source-adapter tests against
  the pinned copies;
- persistence, restart, concurrency, and cleanup: isolated local fault fixtures;
- Atlas publication/search/current-state behavior: uniquely namespaced synthetic
  live data and actual Vector Search only where the claim needs Atlas;
- worker launch, APC delegation, exact handoff, binding, review, and cleanup:
  actual candidate product-harness runs; and
- final product behavior: one purpose-built synthetic demo, never a benchmark.

Environment use is necessary only for the boundary it proves. Local tests cannot
claim live Atlas or native provider behavior; a live run is not repeated for
properties already established deterministically. The two material native uses
are the early thin-slice smoke that exposes the shared seam before broad work and
the final frozen-candidate wave that proves the complete product. A uses only a
deterministic Atlas-adapter fixture. C performs one scoped live adapter/lifecycle
observation, and E performs one scoped live whole-product demo; those two live
observations establish different boundaries.

Focused tests run after the owning change. After D is integrated and the candidate
is frozen, E runs the accumulated local product suite exactly once as E-LOCAL,
alongside the remaining native/service coordinates. A shared schema, runner,
configuration, fixture, or external-state change invalidates its actual
consumers; a documentation or report-only correction invalidates no behavioral
test. There is no full-suite rerun merely because a milestone or review occurred.

E-LOCAL is ordinary discovery rooted only at `P/tests/local/`, the A–D-owned
product-test paths in Section 4. Stateful tests own their temporary roots, ports,
stores, child cleanup, and deadlines inside their fixtures; all-off assertions
live in this same suite. C's scoped live tests under `P/tests/live/`, D's native
tests under `P/tests/native/`, and pre-existing frozen harness/vendor suites are
not swept into it. If a lane changes an upstream/vendor test, that lane runs its
focused source-adapter command and the compatible result is retained; no copy is
made under `P/tests/local/`. D owns the exact setup/readiness/demo entrypoints in
the operator runbook. E binds concrete configuration paths in its one native task
card; this table is the only final-matrix binding and creates no runner or report.
The frozen inputs are the candidate Git commit, its committed tests/runbook, the
selected role/APC configuration, and E's synthetic fixture configuration.

| Family | Runner / prerequisite graph | Isolation and scheduling | Terminal observation and cleanup | Provisional expected / maximum |
|---|---|---|---|---|
| `E-LOCAL` accumulated local product suite, including stateful fixtures and all-off assertions | In `P`: `python -m unittest discover -s tests/local -t . -p "test_*.py"`; independent root | Read-only candidate; each stateful fixture owns unique temp roots/ports/stores/child PIDs and cleanup; this one command may overlap Atlas preparation | Exit 0 after collecting at least one test is PASS; nonzero or zero collected tests is FAIL; process exit is immediate detection and fixture deadlines expose TIMEOUT | 3–8 min / 15 min + 2 min cleanup |
| `E-ATLAS-READY` scoped service preparation | D-owned exact setup/readiness command from the runbook; independent root producing `READY(namespace)` | One unique database/collection/index namespace; obey actual account limit; E owner holds it only for E-NATIVE | CLI READY is success; explicit auth/config/index rejection is terminal; transient build state is polled at no more than 30 s intervals; E owner drops only its namespace | 2–8 min / 15 min + 3 min cleanup |
| `E-NATIVE` full product-harness wave: ordinary all-off lifecycle plus enhanced integrated demo | Outer `operator_launch` runs the pinned `test_root` task card as an independent root. Its graph is `N-ROOT` → `N-BASELINE` (the required lightweight/test-routine worker); {`N-ROOT`, `E-ATLAS-READY`} → `N-APC` (candidate-harness child) → `N-ROOT-ACCEPT` (validation/acceptance action, not another agent) → `N-MIDDLE` (designated enhanced execution worker); {`N-BASELINE`, `N-MIDDLE`, `N-ROOT-ACCEPT`} → `N-HEAVY-CLOSE`. It calls the exact candidate entrypoint/demo config from D's runbook. `N-BASELINE` is one ordinary native all-off lifecycle; N-APC/acceptance/N-MIDDLE form the linked enhanced plan → dispatch → outcome chain | All outer implementation lanes/claims retired; inner state and provider homes isolated; ready siblings use only preflighted child capacity; any shared Ollama home serializes | Native events/results and candidate receipts decide each ID; incompatible terminal state ends that ID's wait within one watch interval (target ≤30 s), while independent IDs finish; test ROOT cleans inner resources, then ROOT retires the outer lane | 10–25 min / 45 min + 5 min cleanup |

E-LOCAL and E-ATLAS-READY may run together as the provisional two finite command
trees; native children use only separately preflighted capacity. N-ROOT/N-BASELINE
do not wait for Atlas; only E-NATIVE's APC → acceptance → designated execution chain consumes
`E-ATLAS-READY`. Every family and named inner ID ends PASS, FAIL, TIMEOUT,
dependency-BLOCKED, or NOT-RUN with a reason. The E native result and underlying
candidate receipts are the result location; the final handoff summarizes them
once. Ordinary failures do not stop independent feasible coordinates, and no
product/test repair begins until that collection completes. ROOT then groups
evidenced causes under one writer each and reruns only changed-input consumers
and newly ready dependents.

Existing dogfood timings support a provisional 15–40 minute expected critical
path and 68 minute finite-test maximum including cleanup (Atlas readiness gates
the enhanced native subgraph; the local suite and N-BASELINE overlap). Actual
first-run timings replace the estimate.
An overrun records incomplete evidence, performs bounded cleanup, and triggers
ROOT to reassess scope/scheduling in place before another expensive cycle; it
never silently resets a budget, drops coverage, or shortens an agent session.

Only commands explicitly selected in `.agent/bounded-commands.txt` use
`.agent/run-bounded.ps1`; the file currently selects none. Agent/provider sessions
are never wrapped in that finite-command runner.

No `project-topology` execution-block profile is added. The native harness
already owns worktree isolation, lane lifecycle, and results; product tests own
the required footprint/recovery assertions; ROOT's changed-input reasoning owns
affected reruns. Adding a second readiness, environment, result, or selection
record would duplicate those controls. A shipped block is introduced later only
if a concrete missing control has a named consumer and is smaller than the host
mechanism.

## 8. Repair, review, and continuity rules

- A defect confined to a lane returns to that lane's owner. A test-only defect
  returns to the test owner. A shared-contract, package, candidate-harness,
  privacy, or cross-lane defect stops parallel writing and returns to ROOT under
  one writer.
- Review findings block only when they identify a violated current requirement or
  invalidate required evidence. Genuine improvements outside the current scope
  are nonblocking notes and create no repair lane.
- There are exactly two planned implementation-review points. The A review covers
  shared public contracts plus privacy/security and the early thin-slice evidence.
  The E heavyweight review covers candidate-harness integration plus final
  closeout. Another review occurs only if a changed binding or dependency
  invalidates one of those decisions—not for routine patches or passing tests.
- If one repair leaves the same cause and failure unchanged twice, stop replaying
  it. Preserve the evidence, diagnose the prerequisite or narrow/replan the
  unresolved seam under ROOT, while unrelated work continues.
- A missing or malformed native worker result gets at most two narrow same-thread
  corrections when safe. Corrections touch only the result. They never repeat
  discovery, implementation, review, or tests whose inputs are unchanged. If both
  fail, ROOT verifies invocation/worktree/branch/base/tip identity, cleanliness,
  the actual diff, and the actual test evidence. When those facts decide the
  implementation, ROOT may integrate it while the native lane remains truthfully
  recorded as an administrative failure; report prose never converts passing
  behavior to failure. ROOT then uses the Section 5 administrative-failure
  force-stop path so the failed lane cannot retain a process or resource lease.
  A fresh same-role lane is allowed only when a substantive fact or action
  remains unresolved, never merely to re-emit a report. Required
  native product behavior and inner identities for T25–T29 still need actual
  evidence; this exception cannot manufacture them.
- A valid FAIL/BLOCKED result is substantive evidence, not something to retry
  until it says PASS. A changed source, configuration, external state, or role
  selection is explicit in the recovery handoff.

## 9. Anti-ceremony rules

These rules are part of the execution contract:

1. Facts live once. Code and tests own behavior; Git owns changes; the native
   harness owns lane lifecycle/results; `HANDOFF.md` summarizes current state.
2. Do not create parallel evidence ledgers, copied native results, per-checkpoint
   progress JSON, bespoke acceptance records, review databases, hash inventories,
   or reports that restate those owners.
3. Hash only where the product's identity/integrity contract or the native result
   schema requires it. Do not repeat the same hash across planning/status files.
4. An administrative or prose defect never invalidates observed passing behavior.
   Correct essential identity/outcome facts narrowly; record nonessential report
   imperfections as such and continue.
5. No admission, readiness, build, assets, check, accept, integrate, or gate
   ceremony is repeated per stage. A stage exits when its code is integrated and
   its named behavior checks actually pass.
6. Do not rerun a broad suite, live service, native worker, or independent review
   solely because an artifact was reformatted, moved, summarized, or reviewed.
7. Do not create a new agent when ROOT can perform a mechanical integration,
   inspect a diff, run a focused check, or correct a status summary directly.
8. Do not expand `references/harness-single`. A real run-blocking harness bug gets
   the smallest reproducer and repair; otherwise work around nothing and continue.
9. `HANDOFF.md` is refreshed only at the four material boundaries: A integrated,
    B+C integrated, D integrated, and E/final closeout (plus interruption or
   compaction). It is not an event log.
10. Reassess this topology only if a shared contract cannot be frozen, lane writes
    overlap, a required external operation proves irreversible/unsafe, the native
    test hierarchy cannot be isolated, or the same repair cause repeats without
    progress. File count, elapsed time, or a reviewer preference alone is not a
    trigger.

## 10. Definition of done and stop

The implementation is complete only when:

- every current Feature requirement and binding Implementation contract is
  implemented in the integrated product;
- T01–T29 have truthful actual evidence at the appropriate boundary, with no
  required failed, unrun, or unavailable item called passing;
- the all-enhancements-off path remains the ordinary harness path;
- the candidate product harness—not the outer coding harness—has launched the
  required test workers and configured APC child, linked the accepted plan to the
  actual execution/outcome, and cleaned its owned resources;
- the integrated synthetic demo materially uses scoped Atlas Vector Search and
  durable memory/reuse or rejection without claiming benchmark improvement;
- setup, operator, recovery, privacy, configuration, limitations, and license
  documentation match the implemented behavior; and
- the product main branch is integrated and clean, temporary resources are closed
  or explicitly retained, and the final handoff distinguishes product evidence
  from unavailable or deferred work.

Stop at development closeout with the exact statements:

- `benchmark execution: deferred/not run`
- `learned selector: deferred/not implemented`

Do not automatically start either successor effort.

## 11. Planning review

Level 3 requires four independent read-only planning assignments:
SCOPE_AUTHORITY, TOPOLOGY_SIMPLICITY, VERIFICATION, and EXECUTION_RESOURCES.
TOPOLOGY_SIMPLICITY is also the user's adversarial bullshit checker. It must keep
challenging coordination and acceptance machinery until the final revision has no
valid over-ceremony criticism. ROOT validates every finding against the request,
specifications, repository evidence, and the smallest adequate remedy before
changing this plan.

Final R8 panel:

| Assignment | Independent reviewer | Result |
|---|---|---|
| SCOPE_AUTHORITY | `/root/scope_authority_review` | PASS — authorized fixed-strategy scope, role precedence, and exclusions are intact |
| TOPOLOGY_SIMPLICITY | `/root/bullshit_checker` | PASS — no remaining valid ceremony, duplication, or simpler adequate topology |
| VERIFICATION | `/root/verification_review` | PASS — T01–T29 boundaries, oracles, native chain, and retained evidence are adequate |
| EXECUTION_RESOURCES | `/root/execution_resources_review` | PASS — lanes, matrix, resources, budgets, terminal paths, and cleanup are executable and proportional |

ROOT accepted every valid finding through R8; all four assignments pass the same
revision. The plan is accepted for Stage A. No separate review package exists.

## 12. Execution handoff

Once the final planning panel passes, resume ordinary implementation at Stage A.
The executor rereads `HANDOFF.md`, this plan, the two normative specifications,
the product and harness `AGENTS.md` files, and the focused source/tests for the
next owned seam. It does not replay the archived formal plan or its STEP-001
administration. Execution stops at the definition above or at a genuine missing
authority/input decision; ordinary defects follow the repair rule without asking
for redundant permission.
