from pathlib import Path
base=Path('master_planning/harness-v2-tier4/addendum-3')
def read(n):return (base/n).read_text(encoding='utf-8-sig')
def write(n,s):(base/n).write_text(s,encoding='utf-8')
def replace(s,a,b):
 assert a in s,a[:100]
 return s.replace(a,b)
s=read('modules/M09.md')
s=replace(s,'Platform runner sets and provider target sets serialize; ordinary failures complete the feasible matrix; all cleanup is exact-identity based.','P06/P12 and Section 7 govern qualified concurrent coordinates and real resource conflicts; all cleanup is exact-identity based.')
s=replace(s,'Launch only executor plus observer and serialize the declared platform runner and shipped provider target sets under one claim','Launch only executor plus observer; schedule finite coordinates by the qualified dependency/resource graph under one outer claim')
a=s.index('### Fixed command advancement');b=s.index('## Configured module instances',a)
s=s[:a]+"""### Remaining-matrix driver binding (version 3.5)

This governs future remaining matrices in both configured instances. Preserve the
already admitted Series 9 controls until its feasible collection closes. Concrete
starting assets are `examples/v2_live_matrix.py`, `.agent-workspace/live-matrix/driver/`
(`run-cell.py`, `cleanup-cell.py` and imported helpers), profile manifests,
checkpoints/results and `.agent-workspace/execute-series9-correction1.py` in
`w/addendum-3-epoch-001/live-execution-series9/`. The last script uses serial
`subprocess.run`; `wait_lane_status` returns only desired statuses and defaults to
1800 seconds. These are observed capability gaps, not implemented concurrency or
terminal-failure detection. M03 owns the smallest adaptation of those mechanics;
no new harness, scheduler service or runtime registry is required.

PRACTICAL_EXECUTOR drives the accepted finite matrix runner; ROOT remains authority
for selection, new attempts, exceptional containment and the single aggregate join.
Bind the exact accepted runner, inputs and selected coordinate commands in the
existing manifest/card at admission, with one outstanding wait per process handle.
A coordinate key is its existing platform/provider/profile/CHECK-LIVE identity.
Result/checkpoint writers must have disjoint paths; merge their complete outputs
once after collection. `execution_blocks.py` selection/recording may be reused but
provides neither dispatch, terminal monitoring nor cleanup. The host implementation
must prove those controls through M08 before a future live attempt uses them.

**Dependency and resource graph.** Admission plus current readiness and observer
coverage precede all live coordinates. For each selected Codex/Qwen profile,
CHECK-LIVE-8 and CHECK-LIVE-11 have no evidence dependency on each other; both use
isolated scenario roots. They currently contend for that provider's writable home,
so only one runs at a time per provider. Managed/plain profiles also share this
home and serialize within that provider. Different-provider ready coordinates run
concurrently up to Section 7's qualified two-coordinate ceiling. Freeze/prestage
shared candidate/package inputs before dispatch; any mutable package copies,
super-cache, journals and temporary paths must be coordinate-owned or explicitly
serialized. Cleanup targets only that coordinate's recorded descendants/resources.

CHECK-LIVE-16 consumes current terminal evidence from CHECK-LIVE-8/11 and other
required same-candidate/provider/profile facts, including preserved CHECK-LIVE-7
and existing hook evidence. Its prerequisite is complete correlated evidence,
not unconditional PASS of every earlier scenario. After failed prerequisite
observations it may still collect its independent native hook/cleanup assertions,
but cannot claim the dependent acceptance assertion passed. Missing required
artifacts block the dependent assertion explicitly. Preserve those subcase outcomes;
do not rerun earlier native scenarios to populate an aggregation field. Any other
residual family selected by M05 must bind its actual prerequisites and consumer
edges before dispatch; numeric CHECK order alone is never a dependency.

**Terminal predicates.** Read the scenario's actual lane/run/session and controller
state, not only a PID or status label. When awaiting `review_pending`, a correlated
`result_invalid`/`provider_exited_no_result`, terminal controller failure, lost
required native session or a proved absent producer with no allowed transition
ends that success wait immediately. Capture the failed claim and enter bounded
owned cleanup on the next observation, target detection latency at most 5 seconds.
The deliberately invalid states in CHECK-LIVE-8 and injected failures/recovery in
CHECK-LIVE-11 are expected until their scenario-defined bound/recovery is exhausted;
never classify those as incompatible solely by name. A transient missing record
or active allowed recovery is not a terminal failure. A timeout records which
assertion remains unobserved; it cannot synthesize success. P15 still owns whole
attempt harm containment; ordinary coordinate completion/failure is not a P15 stop.

**Collection and resumption.** P06/P07 own continuation and cause grouping. Keep
frozen inputs while independent feasible rows run. Every selected coordinate gets
one terminal disposition, including timeout, dependency block or unrun reason.
Do not begin runner, fixture or product repairs during this collection. Preserve
raw failures, cleanup uncertainty and individually proved assertions. Existing
profile-level terminal files alone are insufficient to resume a partially finished
profile: retain each valid coordinate checkpoint and continue only uncompleted or
invalidated coordinates. Unknown process handle triggers exact identity/checkpoint
reconciliation, never a replay. Native outer RESULT correction follows P02/P09
without changing test outcomes, restarting tests or resetting finite budgets.

**Wall-clock binding.** These are initial engineering estimates, not performance
claims, and ROOT reviews them against the implemented runner and final selection
before admission. Per coordinate: CHECK-LIVE-8 expected 1-8 minutes, maximum 20;
CHECK-LIVE-11 expected 5-12 minutes, maximum 25; CHECK-LIVE-16 expected 0.5-4
minutes, maximum 10. Add up to 2 minutes of exact cleanup per coordinate; expected
ranges include ordinary cleanup, maxima reserve it separately. The observed Series 9
Codex completion intervals were about 7.2 minutes for CHECK11 and 0.6-2.6 minutes
for CHECK16; Qwen managed CHECK11's roughly 34-minute interval includes an
incompatible-state wait and is not a successful-run baseline. CHECK8 and future
successful CHECK11 ranges remain uncertain and require readiness/actual measurement.

For a full new 12-coordinate affected set, two provider branches each containing
two resource-serialized profiles imply roughly 15-60 minutes expected elapsed and
a 140-minute maximum including up to 10 minutes common setup/join and per-coordinate
cleanup: two profiles times (20+25+10+6) plus 10 = 132 minutes before small scheduling
slack. This is the maximum branch, not the sum of both branches. A qualified
capacity-one fallback is roughly 30-110 minutes expected and 260 minutes maximum
(4 times 61 plus 10 = 254, rounded up). These are post-readiness matrix budgets;
authoring/review/integration effort is separate and not an agent deadline. Price
a smaller or expanded residual graph anew rather than charging this entire budget
or treating 12 as a cap. The matrix maximum includes exceptional cleanup reserve;
stop launching when remaining time cannot cover a coordinate and its cleanup,
mark unrun rows explicitly, and classify incomplete coverage. Reaching a coordinate
maximum stops that finite coordinate with owned cleanup; incompatible terminal
states exit early regardless of remaining budget. ROOT reviews overruns and their
causes before any subsequent attempt; no timer resets or automatic retries.

**Future activation.** First reconcile the in-flight Series 9 collection, preserve
valid fresh and prior evidence and obtain its M05 decision. For a changed runner
selection/scheduling interface use the declared STEP-003 NORMAL asset path scoped
to this delta, its independent M04 review/check and M06 integration, retaining
unaffected acceptance. M08 proves the changed controls; ROOT then selects and
admits only residual required native coordinates. A scoped P08 correction uses the
existing fast path only if its unchanged-selection/semantics guard actually holds.
The planning edit itself runs no tests, changes no live assets and grants no new
attempt authority. A control gap leaves that future admission pending, not PASS.

"""+s[b:]
s=replace(s,'serialize runner/target sets','schedule qualified coordinates by the remaining-matrix graph')
s=replace(s,'Execute every required Windows feature/provider/profile cell serially under the declared authority','Execute every required Windows feature/provider/profile cell under the qualified graph and declared authority')
s=replace(s,'execute runner and target sets serially in the declared topology','execute qualified independent coordinates concurrently within the declared resource limits')
s=replace(s,'Target sets serialize inside the executor under one exclusive claim.','Finite coordinates use the remaining-matrix graph and Section 7 capacity under one exclusive outer claim.')
s=replace(s,'three serialized shipped-provider target sets crossed with applicable profiles','qualified shipped-provider target sets crossed with applicable profiles')
s=replace(s,'Observer overlaps executor; target units serialize; roots are disjoint.','Observer overlaps executor; qualified independent coordinates run concurrently under the remaining-matrix graph and Section 7 limits; conflicting provider homes serialize and roots are disjoint.')
a=s.index('**Remaining Windows selection after Series 4**');b=s.index('##### Governing task card: CARD-FL2-S2-LIVE-RECONCILE',a)
s=s[:a]+"""**Current remaining Windows selection (version 3.5)**

Retain 16 families x 3 providers x 2 profiles = 96 Windows coordinates and the
original subcase oracles. Series 8 pool/ledger547 (66 PASS / 30 FAIL) is the last
joined baseline. Series 9's unchanged 12 selected Codex/Qwen CHECK8/11/16 rows and
84 preserved classifications are in its correction1 selected-command manifest.
Its unjoined new results are evidence to reconcile, not an accepted aggregate.
Decision579 readiness and decisions563/569/574 are complete; no replay merely for
this amendment. Preserve valid completed Series 9 coordinates after exact input,
subcase, observation and cleanup comparison, even when an outer profile/worker is
incomplete. Collect and join once before M05 determines residual causes and scope.

The 18 unselected prior FAIL rows keep their original M05 routes and any precisely
accepted deviation scope; they do not disappear from final Windows accounting.
Required support/indeterminate claims remain unresolved until evidence or an
existing valid disposition decides them. Recompute all remaining failed, blocked,
unrun or invalidated claims after the join; never reduce requirements to 12 rows
or launch all 96 by default. Native macOS/Linux ledgers remain BOUND-014 gaps.

Use the remaining-matrix driver binding above for the future graph, terminal
predicates, resources and budgets. Preserve each required invalid-result,
same-native-session, hook, public command, failure/recovery and cleanup assertion.
Local runner readiness is not native provider proof. Reuse partial observations
only when their input and semantic equivalence are established; a family PASS
cannot conceal a missing subcase. Required missing observations remain selected.

"""+s[b:]
s=replace(s,'Runs only affected practical units, avoiding complete matrix/readiness restart.','Uses the remaining-matrix driver binding and its reviewed graph budget; runs only residual or invalidated practical units, avoiding complete matrix/readiness restart.')
write('modules/M09.md',s)
s=read('modules/M03.md');pos=s.index('## Configured module instances')
s=s[:pos]+"""### Remaining matrix-control work (version 3.5)

After the current M09 collection closes and M05 supplies its cause groups, one
VERIFICATION_WRITER owns the smallest changes to the existing live-matrix driver,
profile assembly/runner and outer finite-command wrapper. Implement the M09
remaining-matrix binding: ready-node scheduling, coordinate checkpoints, isolated
outputs, shared-provider resource exclusion, incompatible-terminal detection,
complete outcome collection and finite coordinate/total budgets. Reuse the existing
runner, state readers, cleanup and result emitter. No replacement harness or new
workflow-agent scheduler is authorized. Keep actual assertions, scenario meanings,
six invalid shapes, public recovery behavior and oracle strength unchanged.

Scheduling/runner-selection changes use MI-NORMAL-VERIFY-ASSETS and its existing
review/check/integration successors on this delta; do not force them through a
Series 1 guard that excludes changed selection/configuration or uncertain impact.
The completed baseline stays accepted: retain unchanged assets, discovery, checks,
reviews and integrated source, and bind only changed consumers. At future admission,
ROOT supplies the accepted Series 9 control directory and delta files in the
allocated asset worktree as this instance's additional practical-control write
scope; production/frozen-harness/user mapping and active Series 9 roots are protected.
The existing card fields consume this specialization, not the original full-gap
construction objective. M08 defines the changed-control proof obligations; reuse
M03 proof there when inputs match. Preserve failed attempts as evidence.

"""+s[pos:];write('modules/M03.md',s)
s=read('modules/M08.md');pos=s.index('## Configured module instances')
s=s[:pos]+"""### Remaining scheduling-control readiness (version 3.5)

Decision579 accepted the six-family floor above for Series 9. Preserve its unchanged
properties. Only changed M03 controls need additional proof, through real installed
runner/cleanup boundaries with disposable deterministic children and synthetic homes:

- Two independent ready coordinates overlap, while a same-provider writable-home
  conflict cannot overlap. Unique outputs/checkpoints remain intact, child settings
  inherit the effective roots and no credential access is needed for this proof.
  Account for actual nested child fanout, candidate/package junctions and cache
  writes; a copied path string alone cannot prove containment or capacity.
- A scenario-incompatible terminal failure exits within the planned detection bound,
  retains its failing assertion and cleans its own children while an independent
  coordinate continues. Expected invalid states and legitimate in-scenario recovery
  still reach their required next assertion; no global failure-label shortcut.
- Ordinary failure, a launch/runner exception, timeout and missing result each leave
  a truthful collected outcome; ready independent rows finish. A success-dependent
  child blocks, while a failure-evidence consumer runs when its actual inputs exist.
- Resume a partial profile with mixed fresh/preserved rows without rerunning completed
  valid coordinates; reject stale/mismatched credit and preserve required subcases.
  Exercise actual total-budget exhaustion, stop-new-launch decisions and bounded
  cleanup without leaking processes or erasing results. Do not reset budgets on
  administrative report correction.

These are behavior obligations, not an arbitrary case count or provider Cartesian
product. Run independent local proof coordinates concurrently under isolated roots;
resource-sharing negative cases have explicit graph edges. Review an initial local
readiness budget of 1-5 minutes expected, 10 minutes finite maximum plus 2 minutes
cleanup, based on earlier 36-test control proof taking about 129 seconds; new runner
branches are unmeasured and the bound must be reassessed against authored fixtures.
No hard timeout applies to the CHECKER agent. One M03 proof can satisfy M08 without
re-execution if the integrated controls and consumed environment remain identical.
P12 still requires current live credential/configuration/host capacity readback;
synthetic homes prove isolation mechanics, not real provider quota or authorization.
Unproved concurrent qualification blocks that schedule and returns the exact gap;
ROOT may admit only a reviewed genuinely constrained fallback under Section 7.

"""+s[pos:];write('modules/M08.md',s)
s=read('modules/M05.md');a=s.index('**Current Series 4 ROOT decision input**');b=s.index('##### Governing task card: CARD-FL2-S2-LIVE-VERDICT',a)
s=s[:a]+"""**Current ROOT decision input (version 3.5)**

Series 4 verdict/checker history is closed; do not relaunch invocation348 or revisit
its 15 groups. Decision555 already classified the Series 8 complete 17-group / 30-FAIL
pool, and decisions563/569/574/579 accepted the Series 9 control repair through
readiness. The next pool is attempt019 after its feasible collection and observer
join, preserving ledger547 plus valid current observations. A running controller,
partial checkpoint or profile result alone is not a new complete M05 input.

Use the existing CHECKER evidence card once for the new complete pool; it validates
accounting/provenance without repeating product tests. ROOT audits its findings for
validity, compares each required clause with actual assertion/observation and groups
by evidenced cause under P07. Retain uncertain diagnoses and the existing support
routes, tolerance limits and all raw failures. Assign one coherent repair per cause
group, split incompatible ownership, and join accepted repairs before affected
reruns. The known scheduling/terminal-wait control gap does not establish that every
native failure is a control defect. New product defects use their owning source
route and invalidate only real consumers.

The M09 remaining-matrix binding defines the future control delta and proof graph;
M03/M08 implement and qualify it before another admission. Selection changes take
NORMAL scoped asset work, not a guard waiver. Keep prior PASS and independently
valid fresh Series 9 assertions under P04. Include the 18 prior unselected FAIL rows
in final accounting and retain every required unresolved Windows claim. Only
accepted implementation/static and complete required Windows evidence plus cleanup
and durable BOUND-014 gap ledgers permit RESULT-FINAL-ACCEPTANCE / EDGE-007. A plan
revision, bounded collection or timeout is never product acceptance.

"""+s[b:];write('modules/M05.md',s)
