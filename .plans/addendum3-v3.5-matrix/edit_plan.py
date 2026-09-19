from pathlib import Path
root=Path.cwd()
base=root/'master_planning/harness-v2-tier4/addendum-3'
def read(name): return (base/name).read_text(encoding='utf-8-sig')
def write(name,s): (base/name).write_text(s,encoding='utf-8')
def replace(s,a,b):
    assert a in s, a[:100]
    return s.replace(a,b)
s=read('plan-workflow.md')
s=replace(s,'3.4-addendum-3-functional-coverage-audit','3.5-addendum-3-matrix-execution')
a=s.index('### Paused execution and this amendment');b=s.index('\n## ',a)
s=s[:a]+"""### Current execution and remaining-work amendment (version 3.5)

STEP-001 through STEP-005 remain accepted and STEP-006 remains the progress bound.
The human-intervention runtime checkpoint remains **18h13m38s**. This revision
changes only unfinished work and future invalidated evidence; it grants planning
acceptance, not product acceptance or permission to restart an active attempt.

Decision579 accepted Series 9 readiness after decisions563/569/574 accepted its
control repair, review and integration. Candidate
`cb01e41533b337d3dd344b89313f1c9062ee69f8`, frozen control plane
`b8e1f7769d9fdc5a693151a0067522e07fc2ab40`, and 18-asset Series 9 bundle
`a5287f926b6e16d1e131791ac512d096edf06c6706a7d298be171312e1892c72`
remain the accepted starting inputs. Series 8 pool/ledger547 is the last joined
96-coordinate baseline: 66 PASS / 30 FAIL. Series 9 selects 12 Codex/Qwen
CHECK-LIVE-8/11/16 rows and preserves 84 classifications (66 PASS / 18 FAIL).
Preserved FAIL is history and an outstanding M05 disposition, never PASS credit.

ATTEMPT-FL2-S2-LIVE-WINDOWS-019 started after the old handoff. Invocation591 is its
first correction; receipt592 and watcher593 bind the current executor. Before any
future dispatch reconcile its retained profile results/checkpoints and observer,
then close/join and adjudicate the feasible collection. Do not replay completed
rows, change controls beneath it, reset its deadlines, or infer termination from
an old handoff. Current process/result observations are in the refreshed HANDOFF.

Future controls and remaining-matrix execution use the existing owners in M03,
M08, M09 and M05 under P04/P06/P07/P12/P13/P15. The scheduling/selection change is a
NORMAL asset-control delta, not an invented fast-lane waiver; preserve completed
source/static/audit work and apply its changed-input map only to actual consumers.
The exact remaining set is recomputed after the Series 9 join; 12 is this attempt's
selection, not a permanent cap or all outstanding Windows work. Required Windows
failures still block EDGE-007; BOUND-014 native gaps remain nonblocking.
"""+s[b:]
s=replace(s,'Execute the full authorized Windows matrix serially and retain other native-platform gaps and report terminal facts','Execute the authorized remaining Windows matrix with qualified concurrent test processes under P06/P12 and retain native-platform gaps and terminal facts')
a=s.index('Total capacity is four active contexts');b=s.index('\n## 8.',a)
s=s[:a]+"""Total capacity remains four active orchestration/worker contexts including ROOT;
each mapped role has capacity one. Keep ROOT_DIRECT_WORKERS and the frozen-harness
control plane. One PRACTICAL_EXECUTOR schedules finite test subprocesses, one
PRACTICAL_OBSERVER covers every active coordinate, and no lane sub-orchestrator or
additional implementation writer is introduced. Nested test-provider processes are
separately accounted resources, not additional workflow-role assignments.

For the future residual Codex/Qwen matrix, reserve at most two active coordinate
processes, at most one per provider credential/configuration home. Profiles sharing
one provider home serialize; distinct providers run concurrently only after the
M08 isolation/capacity proof. ROOT records peak nested child-process counts from
the selected scenarios, memory and provider capacity and admits both only within
observed host limits; scenario-internal child fanout consumes this same allocation.
Shared mutable fixture/package/cache writes and final pool publication serialize
only their affected operations. LOCK-LIVE-MATRIX remains one outer attempt claim;
it does not force that attempt's isolated test coordinates into a serial queue.
M09 owns the concrete graph and budgets; P12 owns qualification and exception routes.

The two-coordinate schedule is planned, not implemented or already qualified.
M03 owns the minimal existing-runner change and M08 its proof before new live use.
A capacity-one fallback requires a recorded actual conflict or failed qualification,
its release condition and recalculated cost, reviewed by ROOT; file/list order or
an unchanged old serial wrapper is insufficient justification. No resource increase
applies retroactively to the running Series 9 attempt. Completed delivery/review
joins stay intact; no guaranteed wall-clock saving is claimed.
"""+s[b:]
write('plan-workflow.md',s)
s=read('global-rules.md')
pos=s.index('### P07 Finding pooling')
s=s[:pos]+"""Remaining-matrix scheduling (3.5): bind each substantial remaining post-step
matrix to its frozen inputs, command/oracle, prerequisite graph, resource ownership,
result locations and per-coordinate/total budgets in the existing owning card.
Ready independent finite tests run concurrently within Section 7 capacity; serialize
only actual dependency or resource conflicts. Each coordinate exits on an observed
scenario-incompatible terminal state, records evidence and performs bounded owned
cleanup immediately instead of waiting for its success deadline. Expected failure
and in-scenario recovery remain valid paths. Coordinate failure does not stop other
feasible coordinates. Collect passed, failed, timed-out, dependency-blocked and
unrun-with-reason outcomes for every selected coordinate before repairs; incomplete
coverage cannot authorize acceptance. P15 containment remains authoritative.

"""+s[pos:]
pos=s.index('### P08 Test-only correction')
s=s[:pos]+"""For remaining matrices, group the complete collection by evidenced shared cause
before mutations; distinguish product, control/oracle, environment and uncertain
causes. Give each cause group one coherent repair assignment and owner, retaining
all member failures. Similar messages alone do not establish a shared cause. A failed
repair returns new evidence to M05; do not repair-and-rerun after each individual
test. P04 selects changed-input consumers and dependents, including invalidated
prior PASS and outstanding blocked/unrun work, while retaining compatible credit.

"""+s[pos:]
s=replace(s,'M09 serializes platform and provider target sets, starts independent observation first','M09 schedules qualified independent coordinates under P06 and Section 7 resource limits, starts independent observation first')
s=replace(s,"""The schedule remains serial under the current
resource contract; Section 7 of plan-workflow.md records the qualification needed
before any concurrency amendment.""","""The old admitted Series 9 attempt retains its frozen schedule. Before future
concurrent execution, M08 must prove Section 7 isolation/capacity and M09 terminal
exit/collection controls. Shared credential refresh, cache writes or cleanup hazards
block only conflicting coordinates; record any justified serial fallback. No new
live attempt begins solely because this planning amendment passed.""")
pos=s.index('### P14 Exception classes')
s=s[:pos]+"""For substantial remaining matrices, the existing independent scope reviewer rejects
unnecessary serialization, waits after incompatible terminal states, matrix-wide
ordinary-failure exits, repair-after-each-test loops and unjustified full reruns.
Review per-coordinate expected/maximum duration, terminal-detection latency,
cleanup and total critical-path budget before admission. Estimates are provisional;
ROOT must resolve a material capacity/budget gap before launch. Record actual elapsed
intervals without adding overlapping durations. Budget exhaustion records incomplete
coverage and performs owned cleanup; no silent timer reset or weakening of assertions.
Finite-test budgets never become agent-session timeouts. Host finite-command policy
still controls which commands use the bounded runner.

"""+s[pos:]
write('global-rules.md',s)
s=read('steps/STEP-006.md')
a=s.index('### Current continuation');b=s.index('\n## Normal',a)
s=s[:a]+"""### Current continuation (version 3.5)

Decision579 completed Series 9 readiness; the selected 12-row M09 attempt019 was
subsequently launched. Reconcile that attempt's durable results and exact live
identities before any new work. Preserve its 84 unselected classifications, every
completed selected observation and accepted STEP-001 through STEP-005 evidence.
The current baseline and routing are in plan-workflow.md Section 0; M09 owns the
remaining-matrix bindings and M05 the collection decision. Scheduling controls
must be implemented and qualified before their future use. All three configured
entry paths and their guards remain intact; no attempt restart is authorized here.
"""+s[b:]
s=replace(s,'One executor and one observer can decide the shared practical boundary while runner and target sets serialize','One executor and one observer decide the practical boundary under Section 7 capacity and M09 coordinate isolation')
s=replace(s,'split real attempts by runner/target identity and serialize them under one matrix','split conflicting runner/target resources under the qualified M09 dependency graph')
s=replace(s,'Target sets execute serially under LOCK-LIVE-MATRIX.','LOCK-LIVE-MATRIX protects one outer attempt; its isolated coordinates use P06/P12 and the M09 graph after readiness qualification.')
s=replace(s,'One reusable disposable fixture, one serialized executor, and one observer are the smallest safe topology.','One reusable disposable fixture, one executor scheduling qualified concurrent finite tests, and one observer retain the existing role topology. M09 owns coordinate and total wall-clock budgets.')
write('steps/STEP-006.md',s)
