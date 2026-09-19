# Most recent run: project-topology attribution

## Scope and attribution rule

This audit covers only the most recent long run ending at the human-intervention
checkpoint of **18 hours, 13 minutes, 38 seconds** of project wall-clock time. It
excludes earlier project history and anything that happened after that checkpoint.

This document uses the requested attribution rule:

- A defect in the external `project-topology` template is a project-topology issue.
- A defect in the generated Addendum 3 plan or coordination design that a better
  planning template or planning guide could reasonably have prevented is also a
  project-topology issue.
- A worker or ROOT mistake remains an agent issue when the template and generated
  plan already supplied the concrete prevention rule and execution simply failed to
  follow it.
- Necessary testing, real defect discovery, and assurance that found a material
  defect are not classified as inefficiency.

The named `project-topology` skill treats diagnosis as Level 0 and therefore does
not compile a new plan for this audit. Its tier-selection, lane-boundary, recovery,
parallelism, and delegation rules are used only as the comparison rubric.

## Attribution summary

> **Current conclusion: see the final evidence recheck below.** Both earlier
> numerical summaries are superseded. In particular, 5h30m-6h45m removable and
> 11h20m-12h30m necessary are not verified critical-path totals. The recheck
> distinguishes measured intervals, demonstrated failure mechanisms, existing
> rules that were ignored, and savings that remain unproven.

Of the directly verified **1h46m27s to 2h01m27s** of removable wall-clock time in
this run:

| Attribution | Verified wall-clock effect | Basis |
|---|---:|---|
| Project-topology/template or generated-plan issues | **1h36m47s to 1h51m47s** | No-progress repair lanes plus live-stall containment overshoot |
| Agent-only execution mistakes | **at least 9m40s** | Fixture staging, result-shape, BOM, and prelaunch serialization corrections |
| Potential additional topology savings | **Unquantified** | Fully serial live matrix, fixed capacity, and repeated formal gate administration |

The range for topology-attributed waste treats the first five minutes of each
failed repair lane as potentially useful diagnosis at the low end and treats the
whole failed lane as preventable at the high end. Under the requested rule, these
lanes count as topology issues because better task decomposition and mandatory
progress enforcement could have prevented the delay.

## External project-topology template issues

### PT-TEMPLATE-001: agent sessions are deliberately exempt from bounded execution

The formal compiler explicitly requires agent and subagent sessions and their
launch wrappers to remain unbounded. The generated plan therefore had no
supervisor-owned deadline for the sessions that actually wandered. P02 supplied a
semantic thrash test, but it relied on ROOT noticing and acting rather than on a
machine-enforced progress boundary.

Observed consequence in this run:

- Three repair sessions consumed **1h12m55s** and produced no accepted output.
- After allowing five diagnostic minutes per session, **57m55s** was clearly
  removable.

The template should distinguish an unbounded logical task from a supervised worker
invocation. A logical task may remain unbounded while each invocation is required
to publish progress milestones and undergo an automatic five-minute nonprogress
audit.

### PT-TEMPLATE-002: the recovery grammar mandates correction attempts without a productivity guard

The external recovery template requires two same-thread correction attempts after
an initial missing or malformed result, and the second attempt must be allowed even
when the first repeats the error or makes no progress. Preserving implementation
credit is valuable, but unconditional retry is an inefficient default when a
deterministic native emitter can construct and validate the envelope directly.

This rule was not a large measured source of delay in this run because most narrow
corrections succeeded on the first attempt. It is still a template-level latency
risk. The better rule is to use a deterministic emitter first, reserve same-thread
recovery for worker-authored semantic findings, and stop retrying agent-generated
serialization when the native emitter can finish it.

### PT-TEMPLATE-003: the formal fast lane has a fixed three-gate ceremony

The formal template requires every Series 1 correction to carry a motivating test,
changed-source compile, independent review, and separate integration. It also
requires every step to retain the full formal module and fast-lane structure with
no waiver for a smaller correction.

Independent review was useful in this project and cannot be discarded wholesale.
The template nevertheless lacks a distinct administrative/output-only path for
content-neutral result serialization, BOM removal, digest repair, or fixture
assembly. Requiring worker sessions and ROOT records for those operations creates
avoidable coordination latency. Administrative corrections should be performed by
trusted deterministic tooling, with byte/readback validation, without reopening a
product patch-review-integration cycle.

## Generated Addendum 3 plan and coordination issues

These are not necessarily defects in the base template text. They are generated
plan or task-card choices that count as project-topology issues under the requested
rule because the planning system should have prevented them.

### PT-PLAN-001: the live matrix was assigned to one serial executor

The generated role table explicitly directs one `PRACTICAL_EXECUTOR` to execute the
full Windows matrix serially. It also caps the workflow at four active contexts
including ROOT, gives every role capacity one, and states that nested provider
processes serialize.

Observed wall-clock consequence:

- Initial 96-cell live phase: approximately **4h52m**.
- Affected-only Series 2 live phase: approximately **1h59m**.
- Total live-execution wall clock: approximately **6h51m**.

The matrix used isolated scenario roots and distinct provider/profile manifests.
The plan did not establish that every provider/profile shard shared an indivisible
resource requiring global serialization. The external topology guidance says to
parallelize isolated work and serialize only shared real resources, but the
generated plan selected global serialization without documenting a shardability
analysis.

This is probably the largest remaining topology opportunity, but its exact savings
are not counted in the verified waste total. Safe parallelism must first prove
which provider homes, credentials, target roots, host resources, observers, and
cleanup boundaries are independent. Two safe executor shards could materially
reduce the 6h51m live critical path; claiming a precise saving without that proof
would be speculative.

### PT-PLAN-002: broad repair cards were split only after long nonprogress

The 53m21s product-repair card combined controller/retirement work with Windows
atomic-visibility work. Those batches had different source contexts and were later
split into disjoint lanes. The replacement topology succeeded in narrowing the
work, demonstrating that the split could have been selected before launching the
broad card.

Two other no-output repair cards lasted 13m28s and 6m06s. The final 6m06s attempt
issued 60 shell commands without creating the required first failing test; its
replacement card made writing that test the enforced first action and then
progressed.

This is a planning failure rather than unavoidable agent variance under the
requested classification. The topology guidance already calls for stable ownership
boundaries, one repairable product family per gate, and reassessment of card size.
The generated/runtime planner failed to apply that guidance before dispatch.

Measured topology-attributed effect:

- Gross duration of the three failed lanes: **1h12m55s**.
- Conservative removable duration after three five-minute diagnostic allowances:
  **57m55s**.

### PT-PLAN-003: the P02 threshold was advisory and manually enforced

P02 says repeated discovery twice or five minutes of repetitive activity can
establish thrashing, while elapsed time alone cannot. It does not require a polling
interval, deadline for ROOT action, automatic transcript-delta calculation, or
mandatory containment once the predicate becomes true.

Six live cells remained on the critical path after the existing five-minute
evidence threshold had already been satisfied:

- Codex managed CHECK8: **25m25s** excess.
- Qwen managed CHECK8: **8m08s** excess.
- Four other CHECK8/CHECK12/CHECK16 stalls: **5m19s** combined excess.
- Total verified threshold overshoot: **38m52s**.

The provider loops and impossible controller states were real test findings. The
time before the threshold was part of producing defensible evidence. The 38m52s
after the threshold was a coordination failure. The plan should have compiled P02
into an automatic watchdog that measures relevant transcript/state/evidence deltas
and requires containment or an explicit continue record immediately when the
predicate is satisfied.

### PT-PLAN-004: primary-provider retry was reset at every lane and launch

The generated global rule requires ROOT to recheck and retry the mapped primary at
every new lane, module, and launch. Prior nonprogress therefore does not create a
durable task-shape/provider-fit signal for the next closely related launch. This
contributed to repeated broad exploration by the same mapped route, although the
exact share of the 1h12m55s failed-lane total cannot be isolated because fresh
primary retries sometimes succeeded.

An efficient plan should preserve a bounded negative capability record keyed by
provider, task shape, repository surface, and failure class. It should retry when a
material prerequisite or task shape changed, rather than resetting provider
selection merely because a new lane ID was allocated.

### PT-PLAN-005: formal coordination work was required at too many small boundaries

The generated P02 rule requires a fresh `HANDOFF.md` update after every completed
module instance, and each correction or integration successor requires a separate
ROOT-authored card and decision boundary. P07 also requires patch, independent
review, and separate integration for each admitted Series 1 repair.

These rules preserve evidence and caught real defects, so the entire cost is not
waste. They do, however, make ROOT repeatedly assemble cards, validate result
shapes, hash artifacts, verify process absence, release claims, record decisions,
and refresh the handoff for very small changes. The evidence does not timestamp
these activities separately, so no honest wall-clock waste number is assigned.

The plan should batch compatible findings before entering Series 1, emit routine
records mechanically, and permit one content-addressed review/integration packet
for a group of disjoint low-risk control assets. Product behavior and independent
review obligations should remain separately gated where they address a real risk.

## Agent and harness mistakes that are not project-topology defects

### AGENT-001: result envelope, BOM, digest, and fixture errors

The generated plan already required every result-producing card to contain the
absolute native `result_emit.py` command and required emitter preflight,
publication, and readback. It also required administrative faults to preserve
product credit and correct only the affected consumer.

The actual run still produced malformed result envelopes, BOM-bearing JSON, an
incorrect digest, and an incomplete copied readiness fixture. These were worker or
ROOT execution mistakes made despite an adequate explicit prevention rule.

Measured serial wall-clock effect included in the verified waste total:
**at least 9m40s**. A separate one-minute digest correction overlapped the long
product repair and therefore added no demonstrable project critical-path time.

### AGENT-002: repetitive browsing and delayed first edits

The workers repeatedly traversed retained evidence, produced redundant summaries,
and sometimes failed to execute the requested first test or edit. That behavior is
an agent failure. For this audit, the prolonged effect is attributed to
project-topology because task sizing and automatic progress enforcement should
contain inevitable worker variance. The raw mistake is still useful to distinguish
from a requirement that inherently needed 53 minutes of analysis.

### HARNESS-001: cleanup falsely reported PASS with zero operations

Several contained live cells left exact provider/controller processes that the
outer cleanup reported as successfully handled despite performing zero operations.
ROOT then reconciled exact identities manually. This was a product/support defect
in the harness or live controls, not a project-topology template defect. Discovering
and repairing it was legitimate development work.

### PROVIDER-001: self-loops and unreachable controller states

Codex, Claude, and Qwen sessions exposed self-loops or controller states from which
the test predicate could not advance. Those behaviors were valid live findings.
They are not planning mistakes. Only the delay after enough evidence existed for
containment is attributed to project-topology under PT-PLAN-003.

## Work that should not be called inefficiency

- Establishing the first complete 96-cell Windows baseline.
- Executing affected cells whose inputs were genuinely invalidated by accepted
  product or control changes.
- Fixing actual atomic-visibility, controller-exit, cleanup, and retirement defects.
- Independent review and verification that exercised material product and control
  risks required by the acceptance contract.
- Exact process-identity and cleanup proof after the cleanup implementation itself
  had demonstrated false-positive behavior.
- Preserving 45 prior credits in Series 2 and planning to preserve 55 in the next
  pass. This is evidence that the topology's invalidation and replay controls worked.

## Conclusion

Using the requested attribution rule, the majority of the directly verified waste
in the most recent run was a project-topology or generated-plan problem:
**1h36m47s to 1h51m47s**, versus at least **9m40s** of agent-only administrative
mistakes. The strongest verified topology defects were delayed task splitting and
manual enforcement of the P02 progress boundary.

The largest additional topology concern is the generated plan's decision to run
all provider/profile cells through one serial executor. It occupied **6h51m** of
the run, but the safely parallelizable portion has not been proven, so it remains a
high-priority design finding rather than part of the verified waste subtotal.

The external template itself is specifically responsible for exempting agent
sessions from bounded supervision and for imposing a rigid recovery/gate grammar.
The generated Addendum 3 plan added the globally serial live executor, fixed
four-context capacity, primary reset on every launch, and insufficiently early
repair-card decomposition. The malformed envelopes, BOMs, digest, and missing
fixture were ordinary agent/ROOT mistakes because the plan already told the
executor exactly how to prevent them.

## Reassessment of the previously labelled "legitimate work"

> Historical estimate, superseded by the final evidence recheck. The timing
> ranges and confident causal claims below are retained for audit history, not
> endorsed as verified findings.

This section supersedes the earlier implication that the roughly sixteen hours
outside the first verified-waste subtotal was all necessary critical-path time.
The earlier subtotal was intentionally narrow: it counted only a few directly
isolated failures. It did not ask the stronger counterfactual question: **would
the useful work still have needed the same wall-clock time under a better
project-topology?**

The answer is no. Much of the work product was legitimate, but a material part of
its placement on the critical path was a planning choice. The corrected estimate
for this 18h13m38s interval is:

| Classification | Critical-path estimate | Confidence |
|---|---:|---|
| Truly necessary engineering, live runtime, defect investigation, and material assurance | **about 11h20m to 12h30m** | Moderate |
| Removable through better project-topology or generated-plan guidance | **about 5h30m to 6h45m** | Moderate; includes a modelled two-executor counterfactual |
| Agent-only administrative mistakes despite adequate plan instructions | **about 10m** | High lower bound |

These ranges are deliberately not added to more precision than the evidence
supports. Their central reading is approximately **12 hours legitimate and 6
hours topology-removable**. Thus a majority of the run was real necessary work,
but the earlier characterization understated avoidable planning latency by
several hours.

### Direct critical-path waste omitted or understated in the first audit

The directly evidenced topology-sensitive subtotal rises from the earlier range
once the remaining lane records and overlaps are reconciled:

- Four, rather than three, no-output product lanes consumed **1h26m23s** gross.
  Allowing five useful diagnostic minutes to each leaves **1h06m23s** clearly
  removable. The added lane is the cleanup repair from 10:41:08Z to 10:54:36Z;
  it repeated retained discovery, made no edit or failing test, and delayed the
  successful controller-exit repair.
- The initial matrix executor terminated at 01:33:31Z with five manifests
  complete, the sixth still pending, and an invalid outer result. Its recovery
  controller did not start until 02:31:11Z. That is **57m40s** of observed
  terminal-to-recovery latency with no accepted work artifact in the interval;
  even allowing five minutes for reconciliation leaves **52m40s** likely
  removable.
- The Series 2 executor completed its second shard at 07:46:11Z but repeatedly
  polled the already-dead session 963 times. The replacement controller began at
  07:53:41Z, making **7m30s** removable fixed-queue orchestration latency.
- The first live-verdict checker produced its last useful analysis artifact at
  03:44:24Z, then repeated completed inspection after compaction and failed to
  emit a terminal packet. The deterministic recovery completed at 03:51:10Z.
  This exposes **1m45s to 6m45s** of avoidable finalization latency, depending on
  whether a five-minute manual-containment allowance is retained.
- Series 2 observer admission spent about eleven minutes reaching readiness.
  The later record corrected the original diagnosis: all failed launches were
  actually caused by an expired workspace-local Claude credential, not stdio
  handling. An admission-time credential-validity probe and refresh would likely
  save **about five to seven minutes** while retaining the successful startup.
- The previously measured **38m52s** of live-cell time after decisive stall
  evidence and **9m40s** of serial administrative correction remain valid. The
  latter stays attributed to agent/ROOT execution rather than project-topology
  because the existing plan already prescribed the native emitter and readback.

After overlap correction, the strong direct-waste estimate is approximately
**3h02m to 3h34m**. About ten minutes is agent-only; the rest is preventable by
task decomposition, automatic progress supervision, deterministic queue
execution, and admission preflight. The long 53-minute product-repair failure is
still on the project critical path despite overlapping the control repair: its
replacement product sequence began roughly 53 minutes later and remained the
last branch to finish.

### Useful live work was unnecessarily serialized

The six provider/profile shards were useful and required. Their global serial
ordering was not. The observed shard durations support a concrete two-executor
counterfactual within the plan's existing four-context ceiling (ROOT, observer,
and two executors):

- In the initial matrix, the six observed shard durations total about **3h48m**.
  They partition almost evenly across two workers at about **1h54m** each. After
  discounting already-counted stall overshoot to avoid double counting, safe
  two-way sharding would still save roughly **1h30m to 1h35m**.
- In Series 2, the six shard durations total about **1h48m**. A two-worker
  partition has an approximately **58-minute** makespan, saving about **50m**
  before the separately counted dead-session recovery delay.

The additional non-overlapping saving is therefore about **2h20m to 2h30m**.
This is a modelled planning saving rather than a replayed measurement, but it is
grounded in the actual shard completion times. The shards used distinct target
roots, manifests, and evidence trees; the plan-created global matrix lock, rather
than a demonstrated indivisible host resource, forced serialization. Provider
credential/rate limits still require a short concurrency qualification, so the
estimate assumes only two executors rather than unrestricted six-way execution.

The external topology guide should require a shardability and resource-conflict
proof before a generated plan may assign a globally serial executor. If two
shards are safe, the compiler should emit two deterministic queue workers and a
single join. An LLM worker should not own the loop that advances a fixed command
list, polls process sessions, and emits the aggregate envelope.

### Reclassification of the other major work blocks

The roughly 3h49m pre-live construction and review block was mostly legitimate.
It built missing CHECK14-16 controls and the independent observer and found
material defects. It already used useful overlap between construction and review
lanes. The 27-minute CHECK15 review wandered after finding its mismatch, but its
recovery completed alongside the independent CHECK16 review, so most of that
local waste did not extend the project critical path. Better cards and mechanical
finalization could save tens of minutes here, not hours.

The Windows atomic-visibility investigation was also legitimate. The 28-minute
lane proved that the requested zero-error raw-reader oracle was infeasible under
Windows sharing semantics, and the independent reviewer converted that evidence
into the correct strict-test-only route. A better planner should have labelled it
a feasibility spike before requesting a product mutation, but the experiment
itself still had to be performed and ran in parallel with the controller repair.
It therefore contributes little demonstrable critical-path waste.

The successful controller-exit, cleanup, retirement, and control fixes were real
development. Their focused tests and independent reviews caught material errors,
including a stale candidate check that passed only because the old hash survived
in a comment. Removing all review gates would therefore be a false optimization.
The planning opportunity is narrower: batch compatible findings, use one
content-addressed integration for disjoint low-risk control assets, and handle
serialization/BOM/digest operations with deterministic tooling. That likely
removes another **20m to 50m**, but this range is lower-confidence because ROOT
administration is not separately timestamped at every boundary.

### Planner guidance that would remove the measured delay

The project-topology compiler should add five enforceable requirements:

1. **Compile a resource graph before choosing serial execution.** Require an
   explicit indivisible-resource proof for global serialization; otherwise shard
   by provider/profile and schedule within the declared capacity.
2. **Use deterministic supervisors for deterministic protocols.** Fixed command
   queues, session advancement, checkpoint aggregation, result envelopes, hash
   readback, and mechanical verdict deduplication should be native scripts. Agents
   should interpret findings and change code.
3. **Turn P02 into a machine-enforced progress lease.** Each worker publishes an
   expected next artifact or state delta. A supervisor contains or re-cards the
   lane when the delta is absent after the threshold, without waiting for ROOT to
   notice transcript repetition manually.
4. **Select feasibility before mutation for uncertain platform primitives.** A
   read-only spike should precede a PRODUCT_WRITER card when the requested
   behavior depends on undocumented or adversarial OS semantics.
5. **Preflight expiring execution prerequisites at admission.** Credential
   validity, exact emitter availability, output encoding, fixture completeness,
   and observer readiness should be machine-checked before the critical live
   allocation starts.

With those changes, the defensible conclusion is that approximately two-thirds
of this run was necessary work and approximately one-third was removable through
better topology and planner guidance. The majority remains legitimate, but it is
closer to **11-12.5 hours**, not the previously implied sixteen hours.

## Evidence recheck: corrections and targeted skill changes

This is the latest assessment, made on 2026-09-16. It covers the same run ending
at the 18h13m38s human-intervention checkpoint, not subsequent development.
The checkpoint has not moved. The incident records, actual worker prompts,
retained runner and tests, native tool transcripts, generated global policies,
and current topology skill were reread. Current skill files contain pre-existing
working-tree changes; their current wording is a comparison target, not proof of
the exact historical skill revision used to generate the run's plan.

### Corrections to the earlier answers

- **Withdraw the precise 5h30m-6h45m saving and its 11h20m-12h30m remainder.**
  The earlier calculation converted gross failed-lane durations into project
  savings, assumed two-way matrix isolation, and added an unsupported 20m-50m
  paperwork estimate. Subtracting those guesses from total runtime does not
  establish necessary development time. Even the earlier "verified" two-hour
  subtotal used a five-minute useful-discovery allowance rather than locating
  the actual start of every unproductive segment.
- **The 57m40s executor gap is measured; 52m40s removable is not.** Record 143
  gives termination at 01:33:31.815Z; record 144 gives recovery-controller birth
  at 02:31:11.325Z. This establishes a recovery gap. Those boundary records do
  not establish what ROOT did throughout it or how quickly safe recovery could
  have completed. No fresh replay of the remaining test group happened in that
  interval, but that is not proof of 58 minutes of idleness.
- **963 was not the count of invalid Series 2 polls.** A fresh scan of the native
  session finds three running responses, one terminal response, and **959
  Unknown process id responses**. Calls were issued while earlier waits were
  unresolved; some call timestamps precede the terminal result. Thus "963 calls
  after the agent saw the process exit" was inaccurate. The retained initial
  executor session also contains **1,583 Unknown process id responses** before
  its 01:33:31Z termination. These counts demonstrate repeated misuse; they do
  not by themselves measure added elapsed time.
- **The skill already supplies an administrative route.** Current R13/R18,
  M05-A9, and generated P09 explicitly support narrow report-only recovery and
  preserving product credit. There is no basis for claiming that every BOM or
  digest correction was required to repeat product patch/review/integration.
- **Some supposedly missing worker instructions already existed.** Cleanup
  repair 3 explicitly says not to traverse raw evidence and to write/run a RED
  regression. Retirement repair 4 specifies the first mutation, failure code,
  expected behavior, source boundary, and tests. Both still stalled. More copies
  of that prose cannot be counted as preventing their whole duration.
- **Primary selection was a direct user constraint.** BOUND-005 labels retrying
  the mapped primary on each launch as such. A topology skill cannot silently
  replace it with a new provider-selection policy.
- **The stale-hash-in-a-comment review example was outside this run.** It comes
  from records 250-256 after the checkpoint. It must not support this interval's
  timing or review-value claims. The in-window atomic feasibility review and
  CHECK14-16 reviews provide separate evidence that some review was useful.

### 1. Changed live controls were not rehearsed deeply enough

Record `DECISION-LIVE-SERIES2-VERDICT-CONTINUE-212.json` identifies:

- Six CHECK13 failures because the new control accesses `Target.args`, although
  Target has no such field. The retained Series 2 driver actually references
  `custom.args.provider` at lines 3195, 3226 and 3237. Its Target dataclass at line
  381 has a provider field but no args field.
- A CHECK16 circular wait: the provider waits for a release marker; the runner
  waits for a Stop event before writing that marker; the provider cannot reach
  the Stop event while waiting.
- A CHECK16 queue read after retirement already closed the active epoch.
- Six blank-argument failures where the oracle expected a product JSON error
  even though argument parsing rejected the invocation first.

The retained `test_live_control_repair.py` CHECK13 test at line 135 only uses
`inspect.getsource` and string-order assertions for the force-stop change. It
does not execute the custom-adapter branch where the invalid attribute lives.
This is a concrete mismatch between what the control does and what its tests
establish. Source inspection remains useful, but it did not prove this branch
could run. Dependent CHECK15/16 rollups then remained unobserved as well.

**Attribution:** the immediate mistakes are test-authoring errors. Under the
requested broader attribution rule, a better planning guide could have selected
checks that catch these before multiplying them across provider/profile cells.

**Specific skill change:** extend M03/M08 and their compiler checks to require a
changed-control-to-executable-test mapping before expensive live reuse. Each
changed control branch must execute with realistic typed fakes or disposable
fixtures; the test must reach its decision and cleanup boundary. For waits, name
the actor that produces each awaited event and test the dependency ordering.
Source-string checks alone cannot establish executable readiness. Rehearse only
changed paths and preserve unaffected readiness credit. A representative live
canary is appropriate only when the relevant property cannot be tested locally;
it is not an automatic extra gate for every scenario.

**Timing:** the failures and their spread are confirmed. The records do not
isolate the net project savings from catching them earlier. Do not count the
entire Series 2 run as wasted: it also exercised required behavior and found real
controller/retirement defects.

### 2. An overstrong test oracle was treated as a required product fix

Record 212 classified Windows reader PermissionError observations as a product
defect. The product-repair-2 prompt consequently demanded continuous old/new
visibility from direct readers. The atomic repair lane spent **28m15s** exploring
replacement APIs. Record 231 then reclassified all six cells as STRICT_TEST_ONLY:
the zero-error, non-retrying reader condition exceeded the product's actual
old/new-complete and crash/retry requirement. The product route closed without
a code change. Record 228 preserves useful experiments, as well as repeated
experiments and incorrect API-class/buffer attempts.

**Specific skill change:** strengthen M05 classification before a product writer
is dispatched. Require the violated product clause, observed behavior, and exact
test assertion to be compared explicitly. When the assertion adds an uncertain
platform guarantee, use a focused contract/feasibility inquiry before freezing
the mutation goal. Permit "the oracle exceeds the contract" as an output of
that inquiry; it must not automatically weaken a valid product requirement.

This is more precise than merely telling the writer to investigate feasibility.
The original mutation card had already decided the answer. Research still costs
time; the 28m15s lane overlapped other work and is not 28m15s of proven savings.

### 3. Dispatch merged repair groups the verdict had already separated

Record 212 already lists two material batches: controller/retirement cleanup and
Windows atomic visibility. Invocation 213 nevertheless combined them in one
PRODUCT_WRITER card. Record 223 documents **53m21s**, 694 completed items, 27 tool
errors, useful retained findings, and zero tracked product edits. It explicitly
attributes the failed assignment to distinct source contexts combined in one
card. ROOT then split those contexts into invocations 224 and 225.

**Specific skill change:** extend the compiler's existing aggregation/manageability
test to runtime repair-card creation. Preserve the adjudicated mechanism groups
when dispatching; sharing one workflow-role name does not justify merging them.
If a card crosses mechanisms, require the concrete shared invariant that makes
one writer beneficial. Supply retained findings and one next executable action
for each accepted card. Allow sequencing when files overlap; do not mechanically
require one file or one failure per lane, which would create unnecessary gates.

The subsequent 13m28s cleanup and 6m06s retirement stalls show the limit of this
fix: those cards were already narrower and had explicit first-test instructions.
Their agent noncompliance needs supervision or better execution reliability.
The full 53-minute interval also overlapped control repair and cannot simply be
added to a counterfactual critical path without rescheduling the dependent work.

### 4. Fixed command advancement was left to a repeatedly failing agent loop

The initial executor stopped with five manifests complete, a sixth pending, and
a stale outer result rejected for lane identity (record 143). Its native session
contains the 1,583 invalid-session responses above. The Series 2 native session
contains 959, followed by containment and a replacement. The second manifest
file was written at 07:46:11.954Z and the replacement controller started at
07:53:41.700Z: **7m29.746s** between these milestones, including recognition,
containment, reconciliation and relaunch.

**Specific skill change:** make R9's existing preference for deterministic scripts
concrete at M09 dispatch. For a fixed approved command list, name the queue
executor, checkpoint store, terminal-result handler, and aggregate publisher.
The required invariant is **one outstanding wait per process handle**. Terminal
exit or Unknown process id requires checkpoint reconciliation, not another blind
poll. Advance only preauthorized commands; a new attempt or changed scenario
still returns to ROOT. Check failure/resume behavior in M08 before using the queue.

A small native runner could implement this; a new orchestration service is not
inherently necessary. If unavailable, say supervision is manual and supply the
same wait/terminal rules. The tool already returns an explicit terminal/error
signal, so the earlier claim that the API needed to invent one was wrong.
Reliable automatic advancement requires code, not just a stronger markdown rule.

### 5. Existing progress rules depended on ROOT noticing repetition

Records 154, 223, 226 and 238 document repeated reading/summarizing with no required
test or edit. Record 149 documents completed mechanical evidence work being
reopened after compaction instead of emitted as a terminal packet. CHECK15
record 120 likewise preserves a finding before repeated rediscovery. Its fresh
finalizer finished at 20:48:58Z, essentially alongside the independent CHECK16
review at 20:49:00Z; its local wasted effort cannot all be added to project time.

**Specific skill change:** P02 should name who observes progress, what counts as
new evidence for that task, how observations arrive, and what action follows a
repeated unchanged failure. Distinguish RUNNING, WAITING_FOR_COMMAND,
READY_TO_REPORT, and BLOCKED so completed discovery does not reopen itself.
Recovery handoffs should carry completed questions and the first unanswered one.
For mechanical verdicts, reuse a validator/aggregator and make its terminal
publication a separate explicit last action.

The current policy expressly disallows stopping solely for elapsed time. A
universal five-minute kill timer would contradict it and could terminate useful
research. Automated monitoring is a possible runtime improvement with its own
implementation cost; skill-only guidance can make manual supervision explicit
but cannot promise automatic enforcement. The two-correction-attempt grammar
was not demonstrated to be a major source of delay in this interval.

### 6. Observer failures were retried under the wrong diagnosis

Records 183 and 185 blamed stdio/launch handling. Record 187 corrected them:
three native sessions had authentication_failed before tool use. Refreshing the
workspace-local credential copy allowed startup (record 188).

**Specific skill change:** recovery must inspect the native terminal error before
changing launch mechanics or repeating an unchanged attempt. An admission check
must name the exact credential home and freshness conditions consumed by that
launch, rather than inherit an old authentication success from another context.
Probe only what is necessary and already authorized. This improves diagnosis;
the earlier five-to-seven-minute saving is an estimate, not a measured quantity.

### 7. Matrix parallelism remains an opportunity requiring proof

The generated plan sets PRACTICAL_EXECUTOR capacity to one and orders the six
manifests serially. The two live-phase envelopes occupy about **6h51m**, including
stalls and recovery. The external M09-A3 recipe already says to parallelize
isolated work and serialize shared resources.

Distinct target/evidence paths support investigating concurrency. However,
ADMISSION.json binds shared per-provider homes; scenario harnesses junction to
shared candidate/package/cache roots; and nested scenarios can create several
processes. This does not prove concurrency unsafe, but neither the spare context
slot nor separate worktree paths proves it safe or equally fast. Same-provider
credential refresh, cleanup ownership, shared cache writes, and provider limits
were not qualified by the earlier two-bin timing calculation.

**Specific skill change:** extend the existing resource/pool-capacity pass with a
short explicit scheduling comparison. For each proposed serial edge, name the
dependency, shared mutable resource, authorization constraint, or unresolved
isolation question. Consider separate provider groups first, and record the
smallest qualification that would permit concurrency. Increase pool capacity
only after this analysis; keep within actual resource and authority limits.
Do not state 2h20m-2h30m as a proved saving or default automatically to two workers.

### Evidence locations and disposition

All numbered incident files above are under
`.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/`.
Worker prompts are under `w/addendum-3-epoch-001/<lane>/.agent-workspace/`.
The retained controls and tests are under
`w/addendum-3-epoch-001/live-execution-series2/.agent-workspace/live-matrix/driver/`.
The two native sessions rescanned are:

- `live-provider-homes/codex/sessions/2026/09/14/rollout-2026-09-14T18-14-26-01a0a1fc-5ea8-7783-8540-717fe83c4788.jsonl`
  (initial executor; counted only events before 2026-09-15T01:34Z).
- `live-provider-homes/codex/sessions/2026/09/15/rollout-2026-09-15T02-57-23-01a0a3db-2578-7cd1-b054-e5d4aa5d1af3.jsonl`
  (Series 2 executor; matched calls to session 31147 with their actual outputs).

These paths are relative to that incident directory. Current guidance comparison
used top-level project-topology, Level 4 R8/R9/R13/R18/R30, compiler aggregation,
resource and dispatch passes, worker continuity, and M03/M05/M08/M09 recipes.

The recommended priorities are executable control rehearsal, contract-to-oracle
classification, preserving repair mechanism boundaries at dispatch, and a correct
fixed-command wait/advance loop. Supervision and concurrency qualification follow.
Do not add blanket five-minute deadlines, remove useful review, override the
user-owned model mapping, or require a new runtime service for every plan.
Only this audit document was changed; the skill and paused project were not
modified or resumed. No live tests or providers were launched for the recheck.

## Post-checkpoint resumed-run assessment: topology, future harness, and test strictness

This section was added after the later resumed run and is separate from the
18h13m38s checkpoint analysis above. It covers the approximately **7h36m** run
from the Series 3 native-boundary preparation through the terminal Series 4
mechanical verdict checker. The project was paused at the
`MI-FL2-S2-LIVE-VERDICT` ROOT decision boundary; no later repair or live attempt
is included.

### Estimated time attribution

| Category | Estimated wall-clock time | Share |
|---|---:|---:|
| Necessary execution, diagnosis, repair, and proof | 3h40m-4h30m | 48%-59% |
| Difficult-to-avoid agent/provider mistakes and useful rework | 45m-1h15m | 10%-16% |
| Readily preventable workflow/topology waste | 2h-2h40m | 26%-35% |

The largest preventable block was admitting Series 4 after readiness checks had
not executed the changed controls through realistic decision and cleanup paths.
Four locally detectable control defects were consequently multiplied across a
serialized six-provider/profile live campaign. The current topology guidance now
requires a changed-control branch-to-executable-test mapping with realistic typed
objects or disposable fixtures and says source-string checks cannot establish
readiness. That requirement remains prose: the plan validator does not
mechanically reject a readiness plan or result that lacks the mapping.

An evidence-based allocation of the readily preventable portion is:

- **1h30m-2h15m:** most of the invalid Series 4 live cycle, preventable through
  executable changed-branch readiness before real allocation.
- **20m-35m:** provider waiting after sufficient nonprogress or terminal-state
  evidence existed, reducible through task-specific progress signals and prompt
  exact containment.
- **10m-20m:** checker rediscovery and small administrative transitions after
  the necessary mechanical accounting was complete.
- **10m-20m:** observer/executor admission corrections, stale readiness
  consumption, and result-envelope mistakes that stronger deterministic
  preflight could have caught.

These ranges are estimates and partly overlap. They should not be summed as
independent exact savings. Agent implementation mistakes, surprising Windows
error shapes, useful review findings, and provider variability remain difficult
to eliminate completely. Better topology should catch them cheaply before they
fan out rather than assume agents will stop making them.

### What the future harness implementation would prevent

The ideal harness in `new_harness_docs/master_docs/harness-master-spec.md` would
materially improve runtime administration compared with the current outer frozen
harness. Its persistent monitor and manager queue surface terminal and actionable
lane state; strict current-run result validation prevents stale acceptance;
same-session resume preserves interrupted work; cleanup-proof-first leases and
exact lane force-stop reduce manual process/claim reconciliation; and bounded
invalid-result correction can repair some malformed worker results inside the
lane.

For this 7h36m interval, those implementation features would likely remove or
shorten approximately **30-60 minutes**. The estimate covers stale/ambiguous
terminal-state handling, some polling and containment delay, interrupted-lane
reconciliation, exact cleanup/lease administration, and some result-shape
recovery.

The future harness does not by itself solve the largest delay. Its specification
deliberately reports ground truth and leaves remediation and semantic acceptance
to ROOT. It has no general semantic nonprogress detector for a provider process
that remains alive while repeating itself. It does not author correct fixtures,
select proportional oracles, validate project-specific changed-branch coverage,
choose repair groupings, or prove that provider/profile shards can safely run in
parallel. The current generated plan also labels P02 progress supervision
`ORCHESTRATOR_POLICY / MANUAL` and explicitly keeps M09 serial under the current
resource contract.

Accordingly, the future harness implementation alone does not replace a better
topology. A reasonable combined estimate is:

- **Future harness runtime mechanics:** about 30-60 minutes saved.
- **Better topology, readiness, and acceptance design:** roughly another
  1h30m-2h15m saved.
- **Combined likely runtime for comparable work:** approximately 4h30m-5h30m,
  assuming the same provider availability and no new product defect.

### Whether the product or the tests are failing

The recent evidence does not show a bad product implementation. ROOT's pending
Series 4 classification accounts for the 40 FAIL rows as:

| Failure source | Rows |
|---|---:|
| Deterministic test/control defects | 22 |
| Downstream failures dependent on those controls | 7 |
| Provider/support behavior leaving claims undecided | 10 |
| Preserved known nonblocking Qwen CHECK-LIVE-2 deviation | 1 |
| Newly proved product-source defects | 0 |

Series 3 reached the same broad conclusion: its failures were control, oracle,
provider/support, or dependent failures, with no new product defect proved. The
candidate had also passed the static implementation review and safeguards.
Therefore the raw count of 40 failures substantially exaggerates the current
product defect count. The product appears materially functional on the paths for
which valid evidence exists, while full live acceptance remains unproved because
the controls did not decide every required claim.

Some acceptance logic has been too strict or incorrectly framed:

- A previous Windows oracle demanded zero sharing errors from a raw non-retrying
  reader even though the product contract required complete old/new data with a
  supported bounded retry. It was correctly reclassified as an overstrong test.
- CHECK-LIVE-8 attempts to make each real provider emit a prescribed series of
  malformed results. Repetition, refusal, or incomplete shape coverage can fail
  the cell even when the harness safely exhausts corrections, cleans up, and
  escalates.
- Some CHECK-LIVE-12/14/15 results conflate provider failure to follow a scripted
  task with product failure, even when the harness records the deviation and
  fails closed correctly.
- The complete provider/profile/check Cartesian grid is stronger than proving
  every harness feature and every adapter. It repeatedly tests provider obedience
  in scenarios whose product invariant may already be decided elsewhere.

The future live-integration specification explicitly requires real agent behavior
to be classified as `Observed`, `Not observed`, or `Deviation`. Acceptance should
therefore keep three decisions separate:

1. **Harness correctness:** whether the harness reached the required safe state,
   preserved evidence, cleaned up, and escalated truthfully.
2. **Provider compatibility:** whether the particular provider followed its task,
   hooks, and correction instructions.
3. **Control validity:** whether the test actually exercised the promised
   condition with a sound oracle.

A provider deviation should block product acceptance only when it leaves a
provider-specific required capability unproved. When a provider misbehaves and
the harness correctly fails closed, the honest result is often successful
harness evidence plus a provider deviation, rather than a product defect.

The independent reviews are not the principal source of excess runtime. A recent
review found a real control defect before integration. Removing review would save
tens of minutes while increasing the risk that another invalid control consumes
hours of live execution. The more effective correction is stronger executable
readiness and a verdict model that separates product behavior from provider
obedience and test-control validity.

The direct conclusion for this interval is that the repository likely contains
a substantially working product inside a still-unreliable and occasionally
overstrict acceptance campaign. It should not yet be called fully accepted,
because several live integration claims remain undecided. Repeated matrix failure
is currently stronger evidence against the controls and acceptance topology than
against the product implementation.
