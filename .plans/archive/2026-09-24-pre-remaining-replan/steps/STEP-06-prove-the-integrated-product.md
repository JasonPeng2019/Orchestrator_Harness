# STEP-06 - One pinned candidate proves the integrated product path

## Outcome

Implement the development verification in
[BEHAVIOR-06](../specification/behaviors/BEHAVIOR-06-integrated-candidate-proves-the-real-product-path.md)
and exercise the integrated outputs of BEHAVIOR-01 through BEHAVIOR-05. One pinned
candidate has sufficient local evidence, one disposable live Atlas lifecycle, and
one native nested run in which the outer implementation harness delegates to a
product-test ROOT and the candidate product harness owns its workers, APC child,
review, outcomes, recovery, and cleanup.

## Scope and touchpoints

This is a verification step, not a third implementation lane. Freeze the candidate
source/install input, mapping revision, explicit APC binding, configuration,
isolated local roots, Atlas namespace, and cleanup ownership before a wave. Product
source remains read-only during that wave. The outer runtime is
`development/dogfood/harness`; the inner runtime is the harness shipped by the
candidate in `development/product/worktree_example`.

Use `.plans/SUBAGENT_ROLE_MODEL_MAPPING.json` for development roles and resolve each
role immediately before its first launch. `test_root` owns the delegated wave and
its synthetic brief. The candidate harness uses `test_routine`, `test_middle`,
`test_heavy`, and `test_reviewer` only where the required routine, middleweight,
heavyweight, and consequential closeout behavior is exercised. Any product or test
code gap returns to STEP-04 or STEP-05 before pinning. APC is not one of those roles:
select one explicit `apc_adaptation_binding` for the run.

## Implementation

1. Preflight the exact candidate install/entrypoint, complete local result on those
   bytes, role resolver and requested bindings, APC binding, child capacity,
   network profile, Atlas credentials/index/owned namespace, disjoint outer/inner
   runtime roots, and exact cleanup path. Before reporting Atlas or DeepInfra
   credentials unavailable, check the ignored repository `.secrets/creds/` source
   and securely map only the required values into the authorized process variables
   named in `PLAN.md`; never expose them to task cards or artifacts. Then verify
   actual connectivity, permissions, and isolation. Stop before only the affected
   live launch when a prerequisite remains absent; do not silently substitute or
   risk parent-child capacity deadlock.
2. Reuse STEP-05's complete local and isolated-install results when the candidate
   and all consumed packaging inputs are identical. Otherwise run the changed
   checks before native work. Confirm the invoked test manifest contains only source
   tests and synthetic/disposable tasks and cannot enqueue benchmarks, comparisons,
   learner work, or post-closeout follow-ups. Use STEP-04's actual
   bootstrap/resume/launch tests and STEP-05's completion-bridge tests as the
   cheap broken-wiring check. Add a narrow local cross-boundary regression only
   if those tests leave a specific dispatch-to-outcome gap; test that gap, not a
   second all-off/enhanced end-to-end journey. Local fixtures do not stand in for
   the live or native claims.
3. Against a uniquely scoped disposable Atlas partition, use the product adapter to
   publish and discover a synthetic procedure through actual Vector Search and
   perform the authoritative exact eligibility read. Keep that same eligible
   procedure for the enhanced native task. Reuse an earlier setup only when adapter,
   representation, lifecycle, dependency, service configuration, and candidate
   bytes are unchanged.
4. Through native `operator_launch`, the outer harness launches one resolved
   `test_root`. That product-test ROOT creates the isolated candidate product
   instance and invokes its recorded setup/readiness, launch, review, resume, and
   cleanup surfaces. Keep the outer delegation, candidate instance, inner worker,
   APC child, and closeout reviewer identities exact and disjoint.
5. In the candidate harness, complete one ordinary all-off synthetic task and one
   enhanced synthetic task. The all-off task must show no optional memory service,
   context, APC, or background effect. The enhanced task connects exact state,
   reviewed EverOS evidence, an eligible live Atlas procedure, template reuse,
   ROOT acceptance, finalized context, real worker dispatch, terminal review,
   immutable outcome, side-effect and usage reconciliation, restart/resume,
   snapshot/isolation, and owned cleanup.
6. Make the enhanced path use a real near-match APC child launched by the candidate
   harness through the selected explicit binding. Validate requested/resolved/native
   binding, parent/template identity, returned proposal, usage, deadline, and
   cleanup; ROOT accepts or rejects the parent plan separately. Establish direct
   fill and absent/invalid/timeout/ambiguity fallbacks with the focused STEP-04
   tests, not extra native provider runs. A deterministic configuration/launch
   contract may show a second supported APC binding can be selected without source
   edits; do not claim it was natively exercised unless it was.
7. Resolve and validate the actual requested/resolved/native model and effort for
   every launched development role. The consequential closeout uses
   `test_reviewer` over the candidate's actual inner results. After the enhanced
   task has consumed the live procedure, change current or revoke it through the
   product adapter, prove stale delivery is rejected, and clean the owned Atlas
   namespace. Product-test ROOT drains and retires its inner children, reconciles a
   recorded failure subtree if needed, and returns the result through the native
   outer lifecycle. ROOT closes only the outer lane after exact inner cleanup; no
   cleanup enumerates broad process names or touches unrelated roots.

## Dependencies and integration

The step starts only from integrated STEP-05 output. ROOT retains candidate pinning,
live-service authority, mapping/fallback decisions, outer-harness ownership, and
final acceptance. The delegated `test_root` owns only the isolated product-test
instance. Inner workers and reviewer are launched by the candidate harness, not by
the outer owner on its behalf. No product source is edited in a running wave.

## Requirement-fit validation

- The pinned candidate has the complete local-suite and isolated-install evidence
  described in `PLAN.md`, with actual counts and honest optional skips. Setup tests
  prove collision preflight, idempotent recomposition after overwrite, interrupted
  composition recovery, and validation of the actual launched payload.
- The single disposable Atlas lifecycle observes a real Vector Search hit and exact
  eligibility, supplies that procedure to the enhanced native task, then observes
  post-change/revocation rejection and owned cleanup. Secret-file presence alone,
  a fixture, or a credential that remains unusable after secure loading cannot
  satisfy this claim.
- Native evidence must show outer implementation-harness delegation to resolved
  `test_root`, invocation of the recorded candidate harness, real candidate-owned
  workers and APC child, actual role/APC bindings, linked review/outcome/usage, and
  exact cleanup. Direct provider CLI calls or outer-only narration do not count.
- The all-off and enhanced journeys decide BEHAVIOR-06's corresponding acceptance
  scenarios. Reuse focused STEP-04 and STEP-05 evidence for deterministic fault
  branches; the nested wave must still exercise their cross-boundary happy path,
  restart/recovery, ownership separation, and live Atlas participation.
- Before closeout, inspect the tasks and follow-up state actually invoked. State
  `benchmark execution: deferred/not run` and
  `learned selector: deferred/not implemented`; neither is a missing current test.

### Fast test suite

From the product worktree, select STEP-04's actual boundary test with
`python -m unittest discover -s harness/orchestrator_harness/tests -t harness -p "test_step04_launch_boundary.py"`
and STEP-05's completion-bridge test with
`python -m unittest discover -s tests/local/operations -t . -p "test_step05_outcomes_effects.py"`.
These must reject a bypassed memory dispatch or a child proposal counted as the
parent outcome. If a named cross-boundary gap remains, add and select only its
focused regression before native launch; do not build another journey by default.
From the repository root, use
`python -m unittest discover -s development/test-tools/tests -p "test_resolve_role.py"`
when role mapping or launch projection changes. A changed candidate harness seam
also selects its STEP-04/05 direct integration tests. For Atlas or native-boundary
changes, the single owned live lifecycle and the one exact `operator_launch`
nested task are the independently selectable focused checks for those claims;
they remain real service/provider operations, so run them only when their
consumed inputs changed or their earlier result is unresolved. No local fixture
is credited as live or native proof.

## Fast lane and failure recovery

A local regression returns to the owning STEP-04 or STEP-05 behavior before native
launch. An Atlas or provider outage leaves only its live/native claim unresolved
and retains unaffected local evidence. A product defect found during a wave is
repaired by its owning writer in a new implementation worktree because the pinned
candidate stays read-only; preserve unaffected local and live results, then pin
the corrected bytes and rerun only the fast-suite entries and live/native path
that consumed the change. For a launch or service failure without changed product
bytes, first verify the exact configuration, binding, credential home, provider
state, and owned process/operation identity; resume at that unresolved coordinate
after safe reconciliation. On product-test ROOT failure or a lost process handle,
reconcile its exact recorded inner subtree before replay or outer closeout. Keep
independent feasible checks moving and collect their failures before batching one
coherent correction. Never restart accepted work or broaden cleanup merely to make
the wave look clean.
