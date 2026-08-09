# LATEST NEXT-RUN READINESS CHECKPOINT — 2026-08-06 America/Los_Angeles

## Goal and status

Execution remains paused until the user explicitly resumes it. Preparation is complete and green for
the next long `plans/general-coding-harness/EXECUTION_PLAN_2.md` run. The reserved candidate remains
clean at `c6999d173c344b317a918df91619308fd9f93f63`; tested S30 joined tip
`6649cf201ded9782c2cb3bc56983f4a560728ea8` still awaits ROOT archive/admission. Stable runner
`4699d27`, MCP fixture `f003f84`, and rollback `287ea537` remain clean and unchanged. No MCP,
hardware, target-project, C3, or product-candidate process was launched in preparation.

## Completed and verified preparation

- All live V2 governing documents, `goal.md`, `task-card-spec.md`, `test-cleanup.md`, and the active
  detailed execution plan agree on the optimized topology. Old V1 documents/plans are explicitly
  archived/non-operative.
- A support/process/fixture/runner/report/watcher/cleanup failure is corrected in place when the
  product result remains determinable. Otherwise only the affected result/attempt is
  `INCOMPLETE`/`INDETERMINATE`; valid product credit remains. Candidate repair is permitted only with
  exact candidate-defect evidence.
- Reviews, test sets, and observer findings are pooled through their assigned surface and receive one
  deduplicated triage/repair batch. Immediate containment is limited to unauthorized/wrong-resource
  operation, loss of live-process containment/cleanup, or irreversible acceptance-evidence
  corruption.
- C1 still binds current governing hashes for dispatch safety, but invalidation is domain-scoped.
  ROOT classifies changes append-only, refreshes C1 when needed, and reruns only gates consuming the
  changed domain. Whole-file hash/name alone does not force a full gate cycle.
- Expensive custom-runner recordability preflight evidence is bound to the exact runner/procedure/
  configuration/environment fingerprint and reused until that fingerprint changes.
- Mandatory S4 is placed after S30 admission and before fresh final gates. It implements the
  `task-card-spec.md` semantic-acceptance gate plus exactly one same-thread report-only recovery for a
  missing/malformed terminal artifact. S4 requires a ROOT feature plan, Luna implementation, Terra
  review, disjoint Luna smoke/test, and ROOT pooled acceptance.
- Mandatory S5 is now placed immediately after accepted S4 and before the first fresh C0. It adds
  C74-C77 in one bounded candidate stage: accepted task threads reject unrelated reuse; accepted
  terminal lanes leave active discovery after evidence/revision preservation and safe worktree
  closure; static read-only lanes use an exact immutable source view plus a separate result root
  without a linked worktree; and concurrent shared-event writers wait on one cross-process lock.
  S5 uses one Terra-medium-Fast coder, one Terra-medium-Fast reviewer, one disjoint Luna-high-Fast
  practical/test doer, and one ROOT pooled decision. The frozen stable runner remains unchanged.
- The retained harness Git common store currently reports 137 registered worktrees. This is not a
  cleanup authorization. S5 may retire only individually proven terminal V2 lanes after preserving
  evidence/revisions and proving clean zero-process state; the 13 protected historical worktrees,
  reserved candidate/MCP roots, and dirty/ambiguous/live/unpreserved lanes remain excluded.
- `.codex/skills/design-project-topology/SKILL.md` now generalizes the topology rules beyond
  harness-specific projects and requires bounded logical thread lifetime,
  necessary-only source isolation, terminal-lane retirement, and locked append-only shared evidence
  in future generated topologies. Its portable optimization patterns explicitly cover bounded task
  cards, pooled repair, cheap-first validation, dependency-scoped reruns, external rehearsal,
  minimal isolation/retirement, serialized evidence, model-to-task allocation, and support-failure
  isolation.
- The live cross-document audit proves exact C1-C77 coverage, mandatory `S4 -> S5 -> fresh C0`
  ordering, and no active compute-accounting or manual-compaction requirement. The scoped-lock plan
  validator returns `execution plan validation: PASS`. Current SHA-256 values are:
  `goal.md` `788c276322cd1bcd1121e73c5290c4c42807f77daf0cc8b084a6e4ee27819903`;
  `GENERALIZATION_SPEC_2.md` `4db654ccde0539558945b0e09befb4045b4e3975c462885891e36207f677129f`;
  `IMPLEMENTATION_ROADMAP_2.md` `ae27896c9e74961898ec7be516034cb644195e5c817791ece5f8440da5bc5692`;
  `EXECUTION_READINESS_2.md` `a24c0082b57d59191cfbb72fab661e955e43e249fb32c7cf58d74c30fe0d3932`;
  `EXECUTION_PLAN_2.md` `d1dae14249cd3fa16b0a66e9e32e487a470c92444ca8b484e7e577d31bb48af9`;
  `task-card-spec.md` `6931efc884e4ca1f8fadf811ccf9cd5ffccfa9c9d79bbf0c3a625112f8d15d7a`;
  `test-cleanup.md` `a454252c5586e8623638d3d3ab88ff0c7d656b038a72f72b49b7c9babdef90dd`;
  and `design-project-topology/SKILL.md`
   `fbd907b050378de35619a599de51d0f31e20d8a19bda48cdffa6dd66384dd847`.
- This governing change adds future topology and bounded candidate features only. Under the scoped
  dependency policy it preserves S30's exact four green IDs and the accepted outer-support
  preparation; S4 and S5 must consume the new requirements before any fresh final gate begins.
- External C3 support is implemented in `.codex/scripts/c3_outer_support.py` and
  `.codex/scripts/c3_watcher_helper.py`. ROOT directly owns helper launch/identity/close and safe
  registered-only cleanup; the AI reviewer is optional/non-gating. O's new thin sealer must call
  `validate_observation_close()` and must not import the historical W-dependent sealer.
- Focused Ruff and BasedPyright are green; `.codex/tests/test_c3_outer_support.py` passes 16/16; the
  real-helper disposable smoke passes 8/8. Independent Luna-high retry thread
  `019fd626-0892-7403-970d-d91bf8d1cf83` repeated all checks, found zero findings, proved zero related
  residue, and returned PASS. Its first ephemeral dispatch ran no tests because the local sandbox
  helper executable was absent; that support-only failure was corrected once and is not a product
  finding.
- Required full repository verification passed: Ruff, project formatting, BasedPyright, compilation,
  248 orchestrator tests (one skip), 100 watcher tests, 103 Codex integration tests, and the attention
  practical check. Final output: `VERIFY: PASS`.
- Immutable preparation acceptance:
  `plans/general-coding-harness/evidence/firmware-v2/preparation/outer-support-readiness-2026-08-06/ROOT_ACCEPTANCE.json`,
  SHA-256 `987a4aa59e72ab98c9a469797991edd8f6388d69517af752e2bb28cd4b9286b2`.

## Exact next step on explicit resume

First revalidate the plan without launching product/external work:

```powershell
uv run --project .codex/dev --locked python .codex/skills/plan-harness-workflow/scripts/validate_execution_plan.py plans/general-coding-harness/EXECUTION_PLAN_2.md --require-scoped-locks
```

Then verify the preparation-record hashes/protected commits, append the governing-change
classification, preserve S30's unchanged four green IDs, archive/admit exact joined tip `6649cf2`,
execute mandatory S4, then execute mandatory S5 on the accepted S4 tip. Only the accepted S5 tip
proceeds through the shortest affected S4/S5 smoke, fresh C0, current C1, dependency-invalidated C2,
exact host-only rehearsal, and then the next fresh physical C3 attempt. Do not repeat the already-green outer-support preparation unless one of its four source/
test hashes or its execution-environment dependency changes.

## Remaining work and blockers

Remaining work is the intentional product/final-validation path: S30 admission, S4 implementation/
review/test, S5 implementation/review/test and eligible-lane retirement, final C0/C1/C2, host-only
rehearsal, physical C3, C4, safeguard, and promotion. There is
no unresolved preparation defect or question. There are zero related support-test processes and zero
resource claims. Existing unrelated dirty-worktree changes belong to the user/prior work and were
preserved.

# Archived prior checkpoints

# LATEST PAUSE CHECKPOINT — 2026-08-05 18:07 America/Los_Angeles

## Post-checkpoint topology decision — watcher simplification

While execution remains paused, the user removed the over-rigorous requirement that the AI watcher
remain active and write a terminal report before C3 can close. Across the five live governing
documents, required C3 observation is now the deterministic watcher helper's ready, heartbeat,
abort, and terminal-service evidence. ROOT must write required
`topology/WATCHER_OBSERVATION_CLOSE.json` binding that evidence and exact helper identity/exit after
candidate-managed shutdown. The AI watcher (`F.C3.W`) is supplemental independent review: preserve
its report/final-message/exit when available, but an early AI-watcher exit alone is not
`WATCHER_LOST` and does not invalidate an otherwise complete attempt. No generic watcher-resume
framework is authorized or needed. The same revision makes finding pooling the default across
reviews, selected test sets, and observers: each completes its assigned surface, then one triage
deduplicates the complete set and authorizes one bounded repair batch. Immediate stop is limited to
exact unauthorized/wrong-resource operation risk, loss of live-process containment or cleanup, or
irreversible evidence corruption; all other observations are recorded and pooled.

Outer C3 setup, launch, monitoring, report-handling, validation, and emergency-cleanup failures now
have their own isolated attempt route: harmless errors are corrected in place; an uncloseable attempt
rolls only to a fresh namespace while retaining valid immutable candidate/test evidence. They cannot
reopen candidate work, C0/C1/C2, or green candidate tests unless exact evidence shows a changed
C1-locked input, incorrect candidate behavior, or an untrustworthy candidate result.

This is a semantic governing-document change. On explicit resume, re-hash all five documents,
archive/classify this change, and use the ordinary relock route required for the accepted S30 joined
tip; do not launch a watcher/C3 process before that decision. Current hashes: goal
`5e1c0d35598e685713b3892ac04bc61d1d0dc743e06a9a205ddbd3f1ec33c5db`; spec
`a7971bf5ce8e7438f91e07a9028f88ebbf8f1e2a579da6ed3665b7269404d5a6`; roadmap
`60e2bd5256c1d50fe2c76e4f1ed3b8247afb30600f9d7fff6f55710e11b3f6aa`; readiness
`66f220dff186694316f9dd1bac8798ea2d324f097e7d40e8efbf1aa100c6dc9d`; plan
`c3f1cc8ac9caea9cea33cf263c27c4fe8ee772f8484bee892aa6d100ed6dba25`.

The user ordered every subagent terminated because the current setup is too slow and will be
changed. Work is paused. Do not launch or resume a Codex child, stable-runner controller, watcher,
C3 service, MCP process, test executor, or hardware action until the user explicitly resumes under
the revised setup. Final audit at this checkpoint found only `/root` in the collaboration tree,
zero related workflow child/controller processes, and zero resource claims.

The live goal remains execution of `plans/general-coding-harness/EXECUTION_PLAN_2.md` under the
candidate-managed topology and strict anti-overengineering triage. Governing hashes remain:
`goal.md` `9ef9bdb24b913f1ed2b15b7c80f28139705da823296ccd6f341a562a9948f547`,
spec `70ba5e876e120466f03899fd826d439c1d0cc0dc01c5235e5950dc54a1d27cc6`,
roadmap `fb8d60d76c8217f75d6a6a9d69965c7817e8c2bf0c560bac18c8a0ed3ab3af49`,
readiness `e357862e985d61efcf9f38727fe4ca8a718961b4e02bd404dac56d99cb88455c`,
and plan `79ebc3de0d6506ce8ec5ab242db9810be527a6c07b1e9bb100f3c73827520af7`.
The protected stable runner remains clean at `4699d27`; rollback remains clean at `287ea537`;
the reserved candidate remains clean and unadvanced at `c6999d1`; the immutable MCP fixture remains
clean at `f003f84`. Attempt-0010 remains immutable, failed, closed, and non-acceptable.

## Work completed immediately before this pause

- S30.P repaired the demonstrated attempt-0010 external O-decision consumption defect in exactly
  `firmware_acceptance/controller.py`: commit
  `8bf2f54155e6c262b406a08830a1c8f1db8d9af4`, six additions and two deletions. Candidate proposal
  and derived-authorization artifacts remain runtime-confined; only the two live retained-session
  decision reads use the existing external closed loader and exact-byte hash.
- Complete exact-tip Terra reviews ran through the clean detached stable runner. S30.R1 found no
  admissible gap. S30.R2 accepted the production patch as minimal but found one concrete missing
  regression: the old fixture kept decisions below `broker.root` and passed on both predecessor and
  repair. ROOT accepted only that test gap. Triage hashes are
  `250e8c168fc3ee36c31b3f56aa8f173d448f4a4da0abbe77fd7864aec79d6288` and
  `2046d61a8ad9c68d8379b5f805408f03324c3a84b0c3db9d4fc7f8b8917855f6`.
- S30.A1 added only the focused regression in
  `orchestrator_harness/tests/test_firmware_acceptance_controller.py`, commit
  `6649cf201ded9782c2cb3bc56983f4a560728ea8`. The S30.P integration branch was fast-forwarded to
  that exact joined tip; the reserved candidate was not advanced.
- S30.D1 naturally finished immediately before termination. Its ordinary-unittest recordability
  preflight correctly recorded `not applicable`; the new external-decision smoke passed 1/1, then
  the three remaining affected retained-session IDs passed 3/3 without repeating the smoke. Result
  SHA-256 is `44f97f91a6f638c678fb073865dad459225c0ec0f5101c48f921f73790ee3cab`;
  findings are empty at
  `5de00210ce6a24d9eda85271c8a92a26e59fae0a223a9654a23b41f44374d3bb`;
  preflight SHA-256 is
  `d1f226387952385be6e118db6c9903ad06ea1421acf4e0ee1daa74757b470da9`.

## Exact resume boundary

The S30 artifacts have not yet received ROOT's final immutable archive/admission, dependency-map
reconciliation, candidate advance, or fresh C0/C1/C2. No corrected host-only C3 rehearsal or new
physical attempt has run. C3, C4, safeguard, promotion, enforced verify, and full verify remain
incomplete. The S30 worktrees and runner-migration records are intentionally left in place; do not
close, overwrite, or relaunch them while paused.

After the user supplies and explicitly activates the revised setup, first re-read/hash the live goal
and governing documents, inspect the setup change, and prove zero processes/claims. The exact first
read-only command is:

```powershell
Get-FileHash goal.md,active_docs/GENERALIZATION_SPEC_2.md,active_docs/IMPLEMENTATION_ROADMAP_2.md,active_docs/EXECUTION_READINESS_2.md,plans/general-coding-harness/EXECUTION_PLAN_2.md,HANDOFF.md -Algorithm SHA256
```

Then independently validate and archive S30.P/R1/R2/A1/D1 artifacts before deciding whether the
new setup can admit joined tip `6649cf2` or requires a topology-only migration. Do not rerun the
green four affected IDs merely because the setup changed unless their dependency fingerprint or
evidence contract changes.

# PRIOR PAUSE CHECKPOINT — 2026-08-05 12:06 America/Los_Angeles

The user explicitly ordered all current subagents terminated and all work paused. This is now the
highest-current resume state. Do not launch any Codex child, controller, watcher, C3 service, MCP
process, or hardware action until the user explicitly resumes. Read-only inspection is permitted.

Goal remains execution of `plans/general-coding-harness/EXECUTION_PLAN_2.md` with the required
candidate-managed topology and strict anti-overengineering triage. Candidate commit
`542f48c2185b70ab3724a95d60f071e1a5a90343` and immutable MCP server
`f003f84a7df51cd8595a3203c62e225b21da2a22` are clean. The S28 retained-session authorization
repair is admitted, registry hash is
`47a9793901cb84f7d973e0c8f27446823e94e658901d84ca091d0df253cb84fb`, fresh C0 is accepted,
C1 is `d96f270b-bb92-4b3e-aac0-29321e2ea44a` with lock hash
`d9bc07a1eb812775e046f8b87f19955dcac65dae3ecb59994d84613e293a60c7`, and aggregate C2
acceptance hash is `f8e2d328f085f5ce6b5ccbe3b735d287ec9e348da6321a615e55ba4bbd72204e`.

C3 attempt-0008 passed preflight, launched exact O/W/signing/governing identities, reached watcher
readiness, started one candidate service, materialized the five-file target at seed commit
`d3f109fb9d497c91673683ecef95dfd5f41f9aad`, and launched one P0 Terra test writer. The user pause
arrived while that worker was active. O's first shutdown request correctly failed closed; the worker
then exited code 0, was reaped, released its claim, but produced no accepted RESULT. O's second
shutdown succeeded, C3 closed admissions, and the candidate service exited. No MCP server or
hardware call was launched.

ROOT's manually created user-pause notice collided with the supervisor's later create-once abort
notice and produced a ROOT procedure failure. This is not a candidate/server/watcher defect. ROOT
then reaped O, W, signer, and governing watcher. W's blocking helper survived because its generic
command line omitted the attempt path; ROOT verified its exact recorded PID/native creation
identity and forcibly stopped only that process. Final audit: zero related processes, zero claims,
clean candidate/server, no manifest, no acceptance result, and no watcher terminal report.

Attempt-0008 is immutable and non-acceptable. Its closeout records are:

- `ROOT_PROCEDURE_ABORT_REQUIRED.json` SHA-256
  `1028c3a6225694583cc0ba9368d1f077293d92698aa3de5d4f4832bcdfd61e3f`;
- `ROOT_ATTEMPT_CLOSEOUT.json` SHA-256
  `0e89596341272255b2080248a2de64ff0ad2da5b55382f3596df7f3185f99cb0`;
- `TOPOLOGY_SHUTDOWN.json` SHA-256
  `43571c26d3ea6316a9c91ac04663bbe5815cb67c3f833ca5be15b437a7b3a244`.

## MANDATORY TOPOLOGY OPTIMIZATION BEFORE SUITE/ACCEPTANCE RESUME

Treat these as required execution topology, not optional paperwork:

1. **Test executor self-check first.** Before any expensive selected test set that relies on a
   custom runner or per-check child-process evidence, its doer runs one cheap same-lane
   recordability preflight against a disposable local fake. It performs no product, MCP, hardware,
   or external-side-effect action. It must prove a complete sample record—stable ID, exact inputs,
   worker/process creation identity, timing, command, outputs, and exit result. Record `not
   applicable` with the reason only when the executor creates no such inner-process evidence.
2. **Pool non-product process failures.** If a selected set exposes only classified fixture, mock,
   runner, or executor-environment defects, collect the complete set, correct it as one test-only
   batch, then rerun that selection once. Do not rerun after each individual setup/process fix. A
   reconstructable report/path/schema correction with complete raw evidence resumes in the same lane;
   irrecoverable raw identity evidence reruns only the affected stable ID on the unchanged lock. Any
   candidate, contract, oracle, expected-behavior, or coverage defect leaves this route for material
   triage.
3. **Rehearse C3 before allocating C3.** Before allocating `attempt-0009`, launching O/W, creating
   a target repository, starting MCP, or claiming hardware, run the exact-C1/C2 candidate through a
   host-only rehearsal using disposable local fakes. Prove launch admission, retained-session
   authorization, exact identity binding, duplicate refusal, watcher correlation,
   recovery/idempotence, cleanup, and terminal closure. Only a green rehearsal unlocks the physical
   attempt; it is not physical-pass evidence. Reuse a rehearsal only if its dependency fingerprint
   is unchanged.

On explicit resume, first re-read/hash the live goal and four governing documents, confirm the
candidate/server/C1/C2/registry remain exact, and confirm no related processes or claims. Then
run the mandatory host-only rehearsal above, then allocate fresh monotonic C3 `attempt-0009`; never
reuse attempt-0008 target/runtime/control state. For every expensive custom-evidence test selection,
run its executor self-check first and use the pooled non-product correction route above.
Keep the watcher correction prompt-only, but ensure user-requested pause uses a supervisor-owned
stop path instead of pre-creating `ROOT_ABORT_NOTICE.json`. C3, C4, safeguard, enforced verify, and
full verify remain not completed. There are no product source files currently in flight.

# SESSION-RESUME CONTEXT (PREPENDED)

Last rebuilt by `ROOT-IM` on 2026-08-05 America/Los_Angeles after an explicit user request for a
large, decision-preserving checkpoint. The original handoff text begins after the preserved-suffix
marker near the end of this file and is intentionally retained there. Do not
delete, reorder, or rewrite that suffix when refreshing this context. It is the user's current
compact state note, including its hashes and immediate next-step wording. This prepend is the
long-form memory aid: it explains why the project is shaped this way, what each actor is allowed to
do, what evidence is real, what is stale, and how to resume without repeating green work or
mistaking an orchestration mistake for a harness defect.

### 2026-08-05 topology optimization update

The user added three governance requirements: a same-lane no-product/MCP/hardware recordability
preflight before an expensive executor selection that depends on custom inner-process evidence; one
batched correction and one rerun for a selected run whose complete classified failures are only
fixture/mock/executor-environment defects; and an exact-C1/C2 host-only disposable-fake C3 rehearsal
before any attempt, O/W, target repository, MCP process, or hardware allocation. The rehearsal
proves the C3 control plane but is not physical certification. This is a semantic live-goal and plan
change: do not credit existing downstream C1/C2/C3 work until ROOT records the required relock route.
The current governing SHA-256 values are `goal.md` `9EF9BDB24B913F1ED2B15B7C80F28139705DA823296CCD6F341A562A9948F547`,
`GENERALIZATION_SPEC_2.md` `70BA5E876E120466F03899FD826D439C1D0CC0DC01C5235E5950DC54A1D27CC6`,
`IMPLEMENTATION_ROADMAP_2.md` `FB8D60D76C8217F75D6A6A9D69965C7817E8C2BF0C560BAC18C8A0ED3AB3AF49`,
`EXECUTION_READINESS_2.md` `E357862E985D61EFCF9F38727FE4CA8A718961B4E02BD404DAC56D99CB88455C`,
and `EXECUTION_PLAN_2.md` `79EBC3DE0D6506CE8EC5AB242DB9810BE527A6C07B1E9BB100F3C73827520AF7`.

## 0. Read this before touching anything

This is a paused execution, not an invitation to continue. The user has repeatedly asked that all
subagents be terminated while they optimize the plan. At the last inspection there were no live
Codex children, no stable-runner controllers, no resource claims, no MCP processes, no watcher, no
target repository, and no physical hardware operation. A future session must not launch a coder,
reviewer, doer, test executor, acceptance orchestrator, watcher, MCP server, C3 attempt, or
hardware call until the user explicitly says to resume the goal. Reading, hashing, comparing, and
auditing are safe while paused; mutating a lane, changing a locked input, or starting a process is
not.

The authority order is: system and developer instructions; applicable `AGENTS.md`; the user's live
`goal.md`; then the normative specification, roadmap, execution plan, readiness record, and this
checkpoint. `HANDOFF.md` is a resume aid, not a replacement for the live goal. If the user edits
`goal.md`, it wins immediately and may invalidate every later lock. If the user edits one of the
other four governing documents, classify the change as byte-only editorial or semantic before
using any existing evidence. Never silently repair the user's directive by rewriting it from a
stale handoff.

The current task is not “write firmware” in isolation. It is to finish a backward-compatible
general-purpose orchestration harness, then use that candidate to certify itself through a separate
MCP-backed four-board acceptance project. There are two different multi-agent systems:

1. `ROOT-IM` is the current outside implementation coordinator. It creates the product with a
   deliberately bounded multi-agent workflow: one serial product coder, up to two independent
   reviewers/test writers, and up to two independent test doers, with no more than three child
   agents active alongside the root. ROOT owns integration, triage, repair routing, checkpointing,
   C0/C1/C2/C4, safeguard, and promotion.
2. `F.C3.O` is a fresh Sol-high-Fast subagent that will orchestrate the *final target project*.
   It runs the candidate under test and decides target-project work, but it must submit every
   target assignment to the candidate's `C3-HARNESS`. `C3-HARNESS` itself launches and owns target
   workers. ROOT starts and supervises O and W but must not take over O's target-project
   orchestration. Confusing these two systems was an earlier source of plan ambiguity and is now a
   hard contract distinction.

The final acceptance project therefore tests whether the candidate harness and watcher correctly
broker, isolate, observe, authorize, resume, terminate, and report work. It does not require ROOT,
O, or a target worker to be perfect. Bad prompts, assignment shapes, command paths, ordering,
target edits, invalid MCP calls, triage decisions, and result envelopes are expected recoverable
test workload. They return to their owning lane or same-thread resume. They become a harness or
watcher finding only when exact evidence shows that the candidate accepted, rejected, reported,
isolated, resumed, or cleaned up that mistake incorrectly.

## 1. Why the project exists and how the direction changed

The repository began as a successful firmware/HIL-oriented multi-agent harness. It already had a
manager, lane controller, Codex child lifecycle, durable events and acknowledgements, process
identity checks, checkpoints, result envelopes, claims, and a passive watcher. The problem was not
that those mechanisms were useless; the problem was that their public names, schemas, examples,
tests, and docs were tightly coupled to one firmware experiment. The first generalization target
was consequently intentionally small: add a versioned `orchestrator-coding-invocation/v1` path,
preserve the old schema-less policy-bound firmware path, add durable Git lane/branch/result
identity, add one generic exclusive named lock, add a general configuration/example, add one
general end-to-end coding test, and default the AI evaluator off. Do not turn the product into a
scheduler, database, generic adapter framework, UI, or broad file-ownership system.

That original general harness was validated and frozen. The implementation strategy then became:
use the fixed accepted harness as the runner that manages implementation lanes, edit only isolated
candidate worktrees, and use the candidate itself only for the final acceptance test. This avoids
the circular situation in which an unfinished harness controls the process that is supposed to
prove it. The stable runner is the last validated pre-retrofit implementation harness. The
candidate is the post-retrofit firmware-compatible product under construction and, eventually, the
system under test.

The user then supplied firmware resources, datasheets, the BYO Firmware MCP server, a test-program
experiment medium, and an end-to-end target project. The objective widened from “general coding
path works” to a backward-compatible dual path: existing coding behavior must remain green while
legacy firmware invocations remain accepted, and a fresh candidate must be able to run a safe,
evidence-backed physical acceptance project. The MCP server is a boundary/fixture, not a product
to repair. If it has a real incompatibility, the test may be partially exercised through MCP or
replaced by the strongest available unit/integration substitute, but the physically unexecuted
behavior must remain explicitly `NOT_CERTIFIED`.

The execution plan was then rewritten as `GENERALIZATION_SPEC_2`,
`IMPLEMENTATION_ROADMAP_2`, and `EXECUTION_PLAN_2`. The important optimization decisions were:

- Use three coherent implementation large steps (S1 legacy lifecycle/compatibility; S2 MCP-backed
  acceptance kit/test medium; S3 release integration/operator surface), not one loop per module.
- Each large step has exactly two back-to-back QA loops. A loop is product coding, complete review,
  ROOT triage, one bounded repair batch, deterministic test authoring, shortest affected smoke,
  remaining focused execution, and a join. Individual parser/event/schema edits are work inside a
  step, never independent cycles.
- Production coding is singular and serial. Fan-out is only for genuinely independent review,
  test-writing, or test-execution slices and stays within one to three children.
- A reviewer finishes the whole assigned affected surface even after finding a defect. It returns
  one complete exact-tip finding set; ROOT does not stop at the first finding or repeatedly restart
  the step for every finding.
- ROOT accepts a gap only when it is `CODEBASE_BREAKING`, `FUNCTIONALITY_BREAKING`, or
  demonstrably `WORTH_FIXING`, and the evidence shows that the production problem outweighs the
  complexity, regression risk, verification burden, and alternatives of the smallest sufficient
  fix. Style preferences, cosmetic cleanup, unreachable/theoretical cases, “technically nicer”
  ideas, and speculative hardening are rejected without source edits or retesting.
- After a frozen joined tip, run the shortest dependency-invalidated smoke first. Only if it passes
  do the complete fresh review and remaining focused execution proceed in parallel. Reconcile the
  dependency map, passed registry, and aggregate evidence once per accepted repair-batch tip.
- Never rerun a green ID solely because time passed, a manager made a command mistake, or a result
  envelope was corrected. Rerun only if the changed code/input/dependency fingerprint affects it.
- Administrative corrections (path, metadata, result-envelope, evidence-shape, or command fixes
  that do not alter operative meaning) stay in the same lane and do not reopen product review.
  A strict test-only fast lane is narrower: the diff must be limited to synthetic fixture/setup or
  test metadata; exact failed IDs must be known; and production, policy, contract, locked config,
  oracle, assertion strength, expected outcome, stable ID, and coverage obligation must be proven
  unchanged. Then rerun exactly those IDs once in the same test-author lane, with no C0,
  ordinary review, or reconciliation. If any condition is unproved, use the material route.

There was a separate operational issue with hooks. The Stop hook originally verified too broadly:
creating Markdown could trigger a full repository verification. The desired policy was changed so
only changed code (Python/C/etc.) triggers changed-code verification; documentation-only edits are
not a reason to run the long gate. `verify_changed.py` first selects a targeted route and falls
back to the full gate when it cannot identify a route. The fallback is expected for files such as
`.codex/skills/plan-harness-workflow/scripts/validate_execution_plan.py`. This checkpoint refresh
is documentation-only. The exact full verifier was nevertheless run after the last unrelated
formatting fix and returned `VERIFY: PASS`; do not interpret that as proof that the firmware
candidate itself has passed its candidate safeguard.

## 2. Stable runner, candidate, and why their names matter

There is one outer repository, but several protected physical checkouts and linked worktrees. The
names are deliberately stable now:

- `stable-general-harness-runner/` is the clean detached accepted runner at
  `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`. It is the only implementation controller import
  root. It is never edited, advanced, or used as the candidate. It proves the implementation
  orchestration process is controlled by already-validated code.
- `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/` is the isolated
  candidate branch `firmware/v2-candidate`, currently at `659dd03e2aa7159090c8e0e20123b1fec1749f90`
  before the latest joined control-plane tip. Never reset or recreate it; advance it only through
  the recorded integration path after ROOT accepts the latest evidence.
- `pre-conversion-rollback/` is a clean detached rollback at
  `287ea53793e3963062882012ff80c3b0e8c41587`. Preserve it as a recovery point.
- `frozen-harness-to-use/` is a locked legacy alias at the rollback revision because Windows
  prevented the intended physical rename. It is not an operational runner.
- The old physical `harness-in-progress/` checkout is absent. The name `.git/modules/harness-in-
  progress` and its local submodule key are retained because linked worktrees use that Git common
  directory. It is Git metadata, not an executable checkout. Never delete, rename, reinitialize,
  or `submodule update` it while linked worktrees depend on it.
- The clean MCP fixture is
  `plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate/`, branch
  `firmware/v2-mcp-candidate`, exact immutable revision
  `f003f84a7df51cd8595a3203c62e225b21da2a22`. The dirty source `Firmware/BYO-Firmware-MCP/` is
  user material and must be preserved exactly; it is never the acceptance server. No role repairs,
  recommits, or repins the clean fixture.

The candidate and stable runner must not accidentally import each other. Every S1-S3/C0-C2/C4
controller is launched through `.codex/scripts/stable_runner.py` using the exact lock at
`plans/general-coding-harness/runtime/firmware-v2/runner-migration/STABLE_RUNNER_LOCK.json`. The
launcher proves physical path, clean status, detached HEAD, exact commit, package/module origins,
trusted interpreter roots, output confinement, and hostile-CWD/ambient-`PYTHONPATH` isolation. A
lane directory cannot inject candidate code into the controlling harness through its current
working directory or preloaded module.

There is a deliberate caveat: stable commit `4699d27` predates the candidate executable finding
gate and child-environment-isolation fields. The launcher makes a deterministic
stable-compatible projection for the old runner, dropping only fields the old runner cannot
consume. That projection does not mean the old runner enforces the new gate. ROOT must independently
validate every unprojected `FINDINGS.json`, `RESULT.json`, and triage artifact against the candidate
validator before accepting a lane. The final candidate C2/C3/safeguard must prove the candidate
itself enforces the executable gate automatically. This is why both the raw current-tip artifacts
and the stable projection artifacts are retained.

The stable invocation shape that previously succeeded is positional, not `--invocation`:

```powershell
uv run --project .codex/dev --locked python -I .codex/scripts/stable_runner.py `
  --project-invocation <lane>/.agent-workspace/invocation.json `
  --projection-output <lane>/.agent-workspace/stable.invocation.json `
  --projection-record <lane>/.agent-workspace/projection.json

uv run --project .codex/dev --locked python -I .codex/scripts/stable_runner.py `
  --module orchestrator_harness.lane_controller -- `
  <lane>/.agent-workspace/stable.invocation.json
```

An earlier `--invocation` launch exited with argparse errors. That was a ROOT command-shape
mistake, not a harness finding, test failure, or reason to reset a green lane. The failed launcher
stderr is retained for provenance; the corrected second launch is the valid controller evidence.

## 3. Exact actors and authority boundaries

`ROOT-IM` is the host session reading this file. It is the only implementation integration owner.
It owns the candidate branch, merge order, finding triage, classification of failures, governance
hash checks, C1/C2/C4, safeguard, promotion, and final claim. It does not inherit the requested
subagent model map. Do not launch a nested ROOT implementation manager.

The required child assignments, all Fast/priority, are:

| Role | Model | Reasoning | Fast meaning | Authority |
|---|---|---|---|---|
| source coder | GPT-5.6 Terra | medium | `service_tier=priority` | serial source changes only in owned candidate lane |
| reviewer/test writer | GPT-5.6 Terra | medium | `service_tier=priority` | read-only review or owned test/doc changes |
| doer/test executor | GPT-5.6 Luna | high | `service_tier=priority` | execute assigned tests/operations; no unassigned fixes |
| acceptance orchestrator `F.C3.O` | GPT-5.6 Sol | high | `service_tier=priority` | sole final target-project decision-maker |
| watcher `F.C3.W` | GPT-5.6 Terra | medium | `service_tier=priority` | isolated read-only observation/abort evidence |

“Fast” is not a separate model slug. It means the exact normal model plus explicit priority
service tier and the role's required reasoning effort. Every headless child uses full-access/no-
approval flags, ignored user configuration, JSON output, an isolated `-C` root, captured thread,
PID-plus-creation identity, exit, stderr, JSONL, and final message. Resumable lanes do not use
`--ephemeral`; only a no-op availability probe may be ephemeral. A missing model or tier is a
blocking launch problem; substituting another model is prohibited.

`C3-HARNESS` is not an agent. It is the candidate control plane and exact controller processes
operated by O. O submits a structured target assignment; C3-HARNESS validates it, launches the
assigned target worker through `codex exec`, owns the process/claim/event/result/cleanup lifecycle,
and returns the result to O. O may not launch target workers directly. The target worker roles are
one Terra test writer, one Terra coder, one Luna doer/hardware executor, and one Terra reviewer,
submitted serially. A one-active-target-agent cap preserves the root-plus-three ceiling, while C3-
HARNESS can own two physical process groups concurrently because those controllers are not Codex
agent slots.

`F.C3.W` is not a second manager. It cannot assign, approve, mutate source/target state/hardware,
or decide a target fix. It writes only attempt-local watcher evidence and the atomic
`watcher/ABORT_REQUIRED.json` exception. ROOT starts W, records launch provenance, monitors exact
process identity and heartbeat, and records W's exit only after candidate-managed P4 shutdown.

## 4. Current exact state and evidence precedence

The current user suffix says the latest joined tip is `b5753eb`; the actual lane artifacts confirm
that. The older `PARALLEL_CHECKPOINT.md` still contains a historical pause narrative centered on
`e5ced272`, the bounded product repair before its review/CP04 adaptation. The correct interpretation
is not to erase either record:

1. `e5ced272` is the preserved product-control-plane repair lane and historical pre-join state. It
   was author-side static work that needed test adaptation and review.
2. `b5753eb31fb3a725804ace76fb770e7c6629dc96` is the later exact joined tip in the actual linked
   worktrees `S23.A2-C3-FINAL` and `S23.D2-C3-REMAINING-0004`. The lane artifacts at that exact
   revision are newer direct evidence than the stale prose paragraph.
3. `F.C0.FR1-0014` is a completed fresh full affected-surface read-only review at `b5753eb`, with
   exact empty findings and summary `NO CANDIDATE GAP / READY`. It did not run tests, MCP, Codex
   children, or hardware; its “pass” is a review/admission result, not a physical acceptance.
4. `S23.D1-C3-SMOKE-0006` passed the exact CP04 disposable-target/fail-closed smoke once at
   `b5753eb`, with no findings and clean residue checks.
5. `S23.D2-C3-REMAINING-0004` ran exactly two selected documentation tests once at `b5753eb`; both
   passed, with no skip, xfail, failure, error, finding, process, worktree, temporary-root, or
   test-owned claim residue.
6. ROOT still must independently validate/archive these raw artifacts, reconcile the dependency
   map, passed registry, and aggregate evidence once for `b5753eb`, and only then advance the
   reserved candidate and create fresh terminal C1/C2. Do not infer that a lane PASS is already
   ROOT admission or a current C1.

This evidence-precedence rule is important because plan documents can lag lane runtime records when
the user pauses or optimizes layout. On resume, first hash and diff all five governing documents,
the handoff, and `PARALLEL_CHECKPOINT.md`; compare the actual lane commit/result/findings/status
records; record the contradiction and its resolution; then update the checkpoint if needed. Do not
rerun `F.C0.FR1-0014`, CP04, or the two documentation IDs merely because a prose checkpoint was
stale. Rerun only if the new governing hashes or a changed dependency fingerprint invalidates them.

Known exact coordinates at this pause:

| Object | Exact identity | Current meaning |
|---|---|---|
| stable implementation runner | clean detached `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f` | fixed controller/import source |
| protected rollback | clean detached `287ea53793e3963062882012ff80c3b0e8c41587` | recovery only |
| candidate baseline | branch `firmware/v2-candidate`, `659dd03e2aa7159090c8e0e20123b1fec1749f90` | last reserved candidate before latest join |
| latest joined implementation tip | `b5753eb31fb3a725804ace76fb770e7c6629dc96` | C0-0014, CP04 smoke, docs tests exact tip |
| product lane | `S23.A2-C3-FINAL`, branch `firmware/v2-s23-a2-c3-final` | clean at `b5753eb` |
| focused docs lane | `S23.D2-C3-REMAINING-0004` | clean at `b5753eb` |
| MCP candidate | branch `firmware/v2-mcp-candidate`, `f003f84a7df51cd8595a3203c62e225b21da2a22` | immutable compatibility fixture |
| dirty source MCP | `Firmware/BYO-Firmware-MCP/` | preserve exactly, never launch for acceptance |
| final inactive runtime | `runtime/promoted-firmware-v2/` | must remain absent until promotion |
| physical C3 namespace | `acceptance/attempt-NNNN/` | none created; C3 has never run |

The current suffix records the five live governing hashes. They are the values to use when this
file was last compacted: `goal.md` `e96969e0b16190d06603973bf15e24a79a8b5869f3caf2bcb22937618898e19d`;
`GENERALIZATION_SPEC_2.md` `4f922396a442e860969423394072e1ee953ed6191cd8ed7c8529dc2e6b8d1b07`;
`IMPLEMENTATION_ROADMAP_2.md` `d6d99bf0cdbc8020c320e7c5d997da4ebfb98549ef1e83addff35a7422455250`;
`EXECUTION_READINESS_2.md` `e4587d0e0339b496aadf6ffa0c6a6af5127f3c11643410182e53240304417c66`;
`EXECUTION_PLAN_2.md` `ba3b2c39594d5865902601408b3f57a28d215cd36bc9f273b56d55f39275b261`. If any of these
files changes, recompute rather than trusting this paragraph.

## 5. What has actually been completed

The work is much farther than “planning,” but it is not complete. The following are proven or
preserved, with their limits understood.

### 5.1 Runner migration and development harness

The split between fixed runner and evolving candidate is complete. The stable runner has passed
hostile-working-directory and import-isolation checks, ordinary repository verification, deployment-
shaped controller/claim cleanup, and Windows interpreter-DLL-root checks. The old `harness-in-
progress` physical checkout was removed only after linked-worktree dependencies were understood;
its common Git metadata remains. `frozen-harness-to-use` and `pre-conversion-rollback` remain clean
and recoverable. The fixed runner is never candidate code and the candidate cannot control the
implementation controller through path pollution.

The outer development tooling under `.codex/` is not shipped as the product. It contains hook
configuration, `verify.py`, `verify_changed.py`, state/checkpoint helpers, worktree helpers, and
skills. It is used to develop and verify the repository, not imported by the harness runtime.
The ordinary full gate targets the stable runner checkout, so it cannot by itself certify candidate
code. Candidate safeguard evidence must run from the candidate root with its mapped baseline and
accumulated tests.

### 5.2 Preflight and immutable inputs

Preflight recorded exact harness/server/toolchain/device-pack/datasheet/fixture hashes, preserved
the dirty MCP source and prior runtimes/worktrees, checked 47 mirrored resource files by size and
SHA-256, and confirmed 13 toolchain-lock files. Historical source paths in the manifest are
provenance only; they are absent today and must not be falsely claimed as live comparisons. The
historical NCS `PYTHONPYCACHEPREFIX` no longer exists and must never be recreated; each lane uses a
fresh cache below the V2 runtime. No hardware was mutated during preflight. The required no-op
model/tier launch shapes and ignored-user-config behavior were proved for the child roles; on a
future resume, only mutable or changed-dependency checks repeat.

Preflight also established the explicit MCP boundary: no global user MCP registration is trusted
because children run with `--ignore-user-config`; only a lane controller gets the clean server
command, endpoint, `.firm`, artifact, and log roots. Ambient `PYOCD_PROBE_UID` and `PYOCD_TARGET`
are cleared for inventory; a board-owning lane later binds exact reviewed values. Read-only
discovery precedes setup/flash/reset/debug/UART/BLE/RF. RF remains blocked until authoritative
fixture evidence proves module variant, antenna, supply/current, 915 MHz configuration, power,
bandwidth, duty cycle, and constraints. The ambiguous DIO2 notation `P.05` must be resolved from
authoritative material or shown irrelevant before a dependent radio action.

### 5.3 S1: compatibility/lifecycle

The original schema-less policy-bound firmware route remains a supported route; the new coding V1
route remains separate. The candidate preserves legacy policy bytes, digest sidecars, prompt
headings/reminders, label-derived filenames, event log names, model settings, leases, board tokens,
MCP declarations, snapshots, results, and same-thread/path resume semantics. Ambiguous or mixed
coding/firmware inputs and results are rejected rather than normalized into a surprising route.
Worker/controller/helper/MCP identity and lifecycle reconciliation use PID plus creation evidence
and ownership correlation. Events are durable and at-least-once; only exact top-level event-ID
acknowledgement clears them. Claims release only after exact child/MCP exit and reap. Unknown,
partial, corrupt, or ambiguous state remains actionable and fail-closed. The protected original
general-harness tests and new cross-route tests are mapped in the passed registry; a shared-code
change requires dependency-invalidated original IDs to rerun. Test deletion, skipping, weakened
assertions, or expected-failure masking is prohibited.

### 5.4 S2: executable MCP/acceptance substrate

S2 closed a substantial execution contract. The candidate now has a default-deny method policy,
bounded parameter/effect checks, finite retained server sessions, exact method/version and server
schema binding, per-call delegated scope/action/effect checks, predecessor-bound plan/action chains,
five-key final authorization support, monotonic operation deadlines, expiry-through-result,
create-once limitation records, target seed/evidence schemas, and candidate-side finding-gate
support. The immutable contract decision is
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
with SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`.

The main S2 repairs were not arbitrary hardening. ROOT accepted only reproduced deployment-impact
defects: missing scope/action enforcement; inability to retain the pinned server's stateful setup/
validation/plan/action run; all-null `board_setup-plan` initialization incompatibility; malformed
scalar/nested UART argument acceptance; LoRa spreading-factor lower-bound inversion; and bounded
evidence-DAG/path-binding defects needed to make a real limitation/substitute record executable.
One reviewer initially treated an optional newline as violating the 1..256-byte UART text contract;
ROOT rejected that interpretation, retained the legitimate finite-number repair, and restored the
contract with a one-line predicate correction. Test-expectation contradictions were corrected as
test-only work. The clean MCP fixture was not modified.

Protected-test retention was explicit. The candidate-wide dependency map caught that shared
`git_safety.py` changes invalidated more original tests than a local kit view showed. ROOT accepted
the finding, mapped all shared deltas, and ran the exact 14-ID supplement once (14/14). Later scope
and UART fixes invalidated only their mapped IDs. Green IDs remained credited by immutable evidence
path/hash and dependency fingerprint; unrelated original coding tests were not needlessly rerun.

### 5.5 S3 and control-plane repair

S3 finished release/operator documentation, dual-path configuration and command examples, test
medium templates, finding-gate wiring, all-child-Fast role policy, and the candidate's minimal C3
control-plane facade. The candidate now contains retained-session and broker primitives plus the
generic lane controller, and the later repair is represented in `b5753eb`. The C3 acceptance
control plane must still be proved by the final candidate C1/C2/C3 chain; current C0 evidence is
review/admission, not physical execution.

The all-child-Fast change is deliberate: coders/reviewers/test writers are Terra-medium-priority;
doers/test executors are Luna-high-priority; F.C3.O is Sol-high-priority; F.C3.W is Terra-medium-
priority. CP04 now checks the complete role map, not merely prompt language. A wording artifact in
`QUICK_START.md` about default-tier roles is non-blocking unless a reviewer reproduces a real
deployment impact whose value exceeds edit/retest cost.

### 5.6 Latest exact-tip work

At the latest joined tip, the actual raw lane artifacts are:

- C0 reviewer `F.C0.FR1-0014`, invocation `c0-fr1-014`, branch
  `firmware/v2-c0-final-review-0014`, commit `b5753eb31fb3a725804ace76fb770e7c6629dc96`, result
  `PASS`, empty `FINDINGS.json`, complete review of the baseline-to-tip diff, dual-route behavior,
  C3 admission/session/replay/cleanup, policy/limitation containment, role tiers, docs, and
  protected-test continuity. SHA-256 of its findings is
  `3948a12db018cba0a52588a906f587fcd7e37dac7993e86fc1e2ece5cefa6bcd`; result SHA-256 is
  `dccb75738ace96837706566824c75e01ea1a31a24b89403035f20c3c4a947f30`.
- CP04 smoke `S23.D1-C3-SMOKE-0006` passed exactly once at `b5753eb` with no finding.
- Focused docs executor `S23.D2-C3-REMAINING-0004`, invocation
  `s23-d2-c3-remaining-004`, branch `firmware/v2-s23-d2-c3-remaining-0004`, commit `b5753eb`,
  ran the two exact selected unit tests once and passed 2/2. Its findings SHA-256 is
  `5c7d343cdc1cf560c5da0429f3b1583cac663eba1bd7198c1ee08aed519eaa14`; report SHA-256 is
  `eadf9c26c8a041e175f2dc5c4fe99cd31bf6a370dee9dab0954a9b1103c0a192`; result SHA-256 is
  `05454d7d9eb40e8b9f47663de8eea646e691a263be251106e74749c18c1bf726`.

Those files are controller-valid and process/claim-clean, but “lane complete” is not the same as
ROOT-admitted. The next administrative action is candidate-side validation of each original
findings/result/test report, immutable evidence copies, ROOT triage/admission, one aggregate
dependency/registry/evidence reconciliation for `b5753eb`, then fresh terminal C1/C2. No C3
attempt directory, physical process, hardware authorization, or promoted runtime exists.

## 6. Product contract in plain language

The finished product is a dual-path orchestrator harness, not a firmware-only tool. Ordinary coding
uses the versioned V1 coding invocation and preserves repository/result safety, Git branch/worktree
identity, worker lifecycle, event delivery, exact acknowledgements, claims, checkpoints, resume,
and cleanup. Existing firmware callers remain schema-less and policy-bound; they do not migrate to a
new public firmware schema. The two routes cannot accidentally satisfy one another's result shape.

The physical side adds a bounded acceptance kit rather than a broad board framework. It has four
stable board identities (STM-A, STM-B, NRF-A, NRF-B), exact probe/target profiles, live serial
routes treated as routes not identities, separate lane state/artifact/log roots, immutable server
pin, explicit MCP declarations, reviewed plans, bounded delegated authority, default-deny method
policy, exact call proposal/O decision/authorization/dispatch/result chain, retained session
identity, and returning-state close/abort evidence. Direct pyOCD, serial, probe, flash, debug, UART,
BLE, or RF access by O, target workers, ROOT, or an ad hoc script is not acceptance evidence.

The target is a fresh disposable Git repository called the Four-Board Dual-Family Firmware Lab. At
creation it contains exactly five read-only seed artifacts: `TARGET_SEED_MANIFEST.json` plus
`TARGET_CHARTER.md`, `PINNED_INPUTS.json`, `TEST_CONTRACT.json`, and `EVIDENCE_SCHEMA.json`. The
seed hashes are locked by C1. Target-created application source/tests/build/config are versioned
inside the target dependency fingerprint and may be repaired by O through C3-HARNESS; changing a
locked seed/template/policy/fixture/server input leaves the target-local route and requires the
implementation/C0/C1/C2 route.

The practical sprints are P0 host/routing and return-state; P1 STM32 tests-first controller/responder
with I2C2, UART evidence, reset/reconnect, recovery, debugger observability, and sustained ordered
traffic; P2 nRF52 tests-first BLE GATT and low-power 915 MHz CoreSX1262 ping/pong with sequence,
checksum, retry, RSSI/SNR, and timeout evidence; P3 one target doer assignment requesting two
concurrent non-agent physical groups (`P3.STM` and `P3.NRF`) through C3-HARNESS, proving isolation,
same-resource contention, relays, resume, one predeclared non-destructive target bug/fix, and
selective retest; and P4 candidate-managed shutdown, watcher/O closure, exact manifest/result,
topology shutdown, and evidence inventory.

## 7. Authorization, lifecycle, and evidence rules that cannot be hand-waved

The user is the sole issuer of delegated hardware scope. ROOT mechanically copies the canonical
scope from `goal.md` into the C1 authorization artifact; it may add derived identity/pin bindings
but may not broaden actions, fixtures, RF limits, or exclusions. The scope includes four board
fixtures, nine action classes, application-only flashing, UART/BLE/LoRa numerical bounds, explicit
destructive exclusions, and nullable/explicit expiry. Hardware authority is not inferred from a
successful server handshake, model choice, user permission alone, a requested frequency, or a
target worker's assertion.

C1 is non-circular. Allocate a fresh opaque UUID not derived from content; create/hash the canonical
authorization; write `C1_LOCK.json` with that ID and every locked input hash; compute/write
`C1_LOCK.sha256` last. The lock includes the operative goal/spec/roadmap/plan/readiness hashes,
candidate revision, server pin/configuration, acceptance-kit/lane templates, fixture bindings,
target seed, test/evidence contracts, authorization, implementation registry, and other C2/C3
inputs. `goal.md` must equal its C1 hash exactly forever. Only byte-only changes to the other four
governing documents may use a fresh independent Terra review plus ROOT no-dependency-impact
editorial chain; semantic changes cannot. Any post-C1 goal change immediately expires pending and
in-flight hardware calls and returns to the earliest affected gate.

Every physical call has a fresh opaque `CALL_ID` and three create-once artifacts: candidate
`call-proposals/CALL_ID.json`, O-owned `authorization-decisions/CALL_ID.json`, and candidate
`authorizations/CALL_ID.json`. They bind C1/delegated hashes, attempt/lane/board, probe UID,
target/profile, route, board identity/claim, method/version, server/schema, method policy,
canonical evaluation, exact arguments, plan, and positive bounded duration. Before MCP submission,
C3-HARNESS recomputes and compares all fields. It then creates immutable dispatch admission with
fresh governing hashes, monotonic start/deadline, and all revalidated fields. A post-dispatch result
cannot retroactively authorize a call. Expiry/revocation/input mismatch cancels safely where
possible, preserves raw outcome as `INDETERMINATE_EXPIRED`, releases claims only after exact
exit/reap, and forbids success. A duration overrun is `INDETERMINATE_TIMEOUT`, never pass.

The retained MCP session is finite and controller-owned. A session request opens one exact attempt/
lane/board/claim and records Server Run/process/bootstrap. Setup, validation, plan, action,
observation, and return-state calls use predecessor-bound chains over the same process/transport/
claim. O/target workers receive no endpoint, credential, launch command, or inheritable handle.
Normal close requires O's signed close intent and authorized return-state calls; the controller drains,
exits, reaps, releases, and writes terminal closed evidence. Failure, expiry, abort, or lost liveness
writes terminal aborted evidence and cannot claim a clean state.

## 8. Watcher, abort, and failure classification

W must be ready before target work, heartbeat at least every 30 seconds, bind exact process identity,
monotonic sequence, timestamp, and observation cursor, and never let a cursor stay unchanged while
observed logs advance. ROOT treats an unexpected exit, lost observation, cursor stall, or >90-second
gap before terminal report as `WATCHER_LOST`. ROOT stops new work, terminates only registered
acceptance identities, preserves the immutable attempt, classifies the cause, and requires a fresh
attempt. W's expected exit comes after candidate-managed P4 shutdown and terminal report but before
O closes the manifest.

If W observes a real candidate/watcher invariant violation—wrong identity acceptance, false running
or completion, cross-lane mutation, duplicate ownership, premature release, missing actionable
notification, non-exact acknowledgement, leaked managed process, or watcher misclassification—it
writes the sole watcher-owned exception `watcher/ABORT_REQUIRED.json` atomically. The record binds
attempt, exact W identity, heartbeat/cursor, invariant, correlated identities, evidence paths,
earliest invalidated sprint, and UTC time. It is not a manager signal, and ROOT must monitor that
path directly. ROOT requests normal controller shutdown first; host termination is allowed only for
pre-registered identities after an unavailable/unresponsive controller and must create
`topology/EMERGENCY_TERMINATION.json`. It never grants hardware authority and leaves board state
indeterminate.

O liveness is separate. ROOT monitors O's exact process and heartbeat at the same 30/90 cadence.
After the manifest appears, O has 90 seconds to create the hash-bound result. Unexpected O exit,
stale heartbeat, deadline expiry, or exit without valid result is `ORCHESTRATOR_LOST`; preserve
partial evidence, never complete/reuse it, write loss provenance, and use a fresh attempt. After a
valid result and normal exact exit/reap, ROOT writes `ORCHESTRATOR_EXIT.json`. The topology shutdown
file closes/hashes the reserved topology subtree separately; pre-exit evidence cannot claim an exit
that has not happened.

Failure routing is intentionally asymmetric:

- ROOT/O/target-worker mistakes are recoverable expected workload. Fix through owner/same-thread,
  preserve green evidence, and do not emit ABORT_REQUIRED or reset C1 unless a locked input changed.
- Target application/compiler/test/target-local config defects stay inside O's project when no
  locked input changes. O submits repair via C3-HARNESS and reruns only affected IDs.
- Pinned MCP server defects are immutable. O may record `AUTHORIZED_SERVER_LIMITATION` only with
  exact call/method/version, raw result/failure, process/return-state evidence, pinned-source
  attribution, and proof it is not harness/target/fixture/input/operator. Use strongest safe
  substitute in order: partial MCP, focused pinned-component unit/integration, synthetic candidate
  boundary unit. Retain the physical test as limited/`NOT_CERTIFIED`; never call it green.
- Candidate harness or watcher defect is the only C3 path to ABORT_REQUIRED and returns to the
  owning implementation step, fresh C0/C1/C2, and then a fresh C3 attempt.
- Immutable evidence closure failure caused only by O's mistake can roll to a fresh attempt
  namespace without candidate reset. If a locked input changed, use the full relock route.

## 9. C3 evidence closure and immutable attempt roots

Every attempt uses the next monotonic matching runtime/evidence pair
`plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/` and
`plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/`. Choose one greater than
the largest number on either side; use 0001 only when neither exists. Both paths must be absent;
one-sided path/collision stops allocation. Never clear, overwrite, gap-fill, or reuse an attempt.
Each has separate `target/`, `hil/`, `events/`, `claims/`, `manager-signals/`, and `.agent-workspace/`
roots plus an attempt-local passed registry. A restarted target may reconstruct only the exact last
accepted target source-tree commit plus locked seed, not old runtime/build/process/claim/event state.
P0 always reruns on a fresh attempt; unchanged target tests may retain credit only by evidence path/
hash and unchanged dependency fingerprint.

P4 has a strict closure order. Candidate-managed board/MCP/child shutdown completes first. W writes
its terminal report, exits, and is exactly reaped. ROOT writes `WATCHER_EXIT.json`. At a quiescent
checkpoint O recursively inventories every regular file in both attempt roots, including failed,
denied, conflicting, and adverse evidence, except exactly the not-yet-created manifest itself,
result, and reserved `topology/`. Symlinks, reparse points, unresolved temporaries, and later
in-domain writes are forbidden. C1/delegated/editorial files outside the roots are listed only as
directly verified `external_references`. O must create the non-cryptographic result within 90
seconds, binding manifest path/hash, watcher report, P4 state, C1, target, decision, schema, and UTC
time. After O exits, ROOT writes `ORCHESTRATOR_EXIT.json` and closes the topology inventory. C4
independently enumerates both roots, verifies every hash/reference, and rejects unknown files.
Any later external-reference/document change invalidates the C3 result before C4.

## 10. What remains, and what a resumed agent must do

The latest direct evidence is pre-terminal C1. Remaining gates are administrative ROOT admission of
the joined `b5753eb` lanes; one dependency-map/registry/aggregate reconciliation; candidate advance
from `659dd03` to the accepted joined revision; fresh C1 with an opaque ID; dependency-invalidated
C2; then C3 physical acceptance under O and W; C4 nested static audit; one accumulated safeguard;
promotion of an inactive runtime; and outer candidate-root verification. No hardware operation has
started, so physical acceptance has not been demonstrated. Do not claim “general-use ready” yet.

On explicit resume, use this sequence:

1. Read `AGENTS.md`, nested firmware instructions, this handoff, `goal.md`, spec, roadmap, plan,
   readiness, and the referenced firmware/MCP/test-medium material. Hash all five governing docs.
2. Verify no live children/controllers/claims/MCP/watchers; inspect exact reserved worktrees,
   branches, commits, common dir, cleanliness, and dirty-source preservation. Do not rerun absence
   checks by deleting/recreating established worktrees.
3. Compare the five governing-document diff against the hashes in this handoff. Classify user
   layout changes. If `goal.md` changed, stop and follow its new directive; if a semantic product,
   policy, contract, fixture, or evidence change occurred, invalidate affected credits. If only
   editorial change occurred in a non-goal doc, obtain the required independent review/chain.
4. Validate the raw `F.C0.FR1-0014`, CP04 smoke, and `S23.D2...0004` result/findings/test reports
   independently with the candidate validator, copy immutable evidence, and create ROOT admission
   records. Preserve the earlier failed/invalidated attempts as history.
5. Build one dependency map at `b5753eb`, reconcile the 140 credited IDs/21 groups and new focused
   evidence once, and advance the reserved candidate only after exact branch/commit/clean checks.
6. Allocate a new opaque C1 lock ID; create authorization then lock/hash in non-circular order.
   Bind all five current hashes and locked inputs. Do not use stale C1/C2.
7. Run only dependency-invalidated C2 IDs on the locked candidate. If execution-only failure occurs,
   repair the test/target lane without changing locked inputs and rerun affected IDs. If code,
   policy, expected behavior, coverage, template, fixture, server, or evidence contract changes,
   return to the owning S step and fresh C0/C1/C2. A strict test-only correction requires its
   deterministic eligibility checklist and exact failed-ID rerun first.
8. Launch fresh Sol-high-priority O and Terra-medium-priority W with exact isolated roots, key-release
   and liveness provenance. O alone orchestrates target work through C3-HARNESS; ROOT supervises.
9. Run P0-P4, honor MCP/authority/watchers, retain immutable attempt evidence, and classify every
   failure by boundary. Do not use direct hardware paths or repair the MCP fixture.
10. Run C4, safeguard, reconciliation, promotion, and outer verification only after all evidence is
    closed. Promote only a clean inactive candidate and preserve rollback.

Useful read-only pre-resume commands:

```powershell
git status --short
git worktree list --porcelain
Get-FileHash goal.md,active_docs/GENERALIZATION_SPEC_2.md,active_docs/IMPLEMENTATION_ROADMAP_2.md,active_docs/EXECUTION_READINESS_2.md,plans/general-coding-harness/EXECUTION_PLAN_2.md -Algorithm SHA256
Get-ChildItem plans/general-coding-harness/runtime/firmware-v2/resource-locks -Force
Get-Process | Where-Object { $_.Path -like '*Orchestrator_Harness*' -or $_.ProcessName -match 'codex|pyocd|uv|python' }
uv run --project .codex/dev --locked python -I .codex/scripts/stable_runner.py --module orchestrator_harness.cli --config plans/general-coding-harness/runtime/firmware-v2/config/final-harness.json scan --no-write
```

Do not use destructive broad cleanup, `git reset --hard`, recursive deletion, `submodule update`,
or process-name killing. If a path is dirty or collides, preserve it and classify it. If a child
fails to close, use exact PID-plus-creation and registered ownership; “no process with that name”
is not proof of safe cleanup. If a command syntax is wrong, correct the command and preserve the
failed attempt; it is not automatically a product failure.

## 11. Decision ledger: why earlier defects did not cause thrashing

The project has taken a long time because the candidate was deliberately subjected to successive
complete reviews, not because every orchestrator mistake caused a reset. The meaningful accepted
defect history is useful context for a resuming agent:

1. The original stable/candidate runner split was validated before firmware edits. The stable
   runner's pre-candidate finding-gate limitation was explicitly acknowledged and compensated by
   ROOT independent artifact validation.
2. The pre-C1 executable contract audit found delegated scope/action classes bound but unenforced
   and no retained stateful MCP setup/validation/plan/action run. S2 accepted both as functionality/
   safety defects and repaired them in one bounded production chain.
3. The pinned server required an all-null `board_setup-plan` initialization; the candidate's exact
   route comparison was too strict. A one-line correction admitted the server's actual initialization
   while keeping equality for non-null IDs. That was compatibility repair, not an MCP edit.
4. C2 rejected inherited protected-test credit when shared `git_safety.py` was not mapped. ROOT
   accepted the dependency finding and ran the exact 14 uncovered IDs. This is why protected green
   tests are evidence-indexed, not simply copied by label.
5. `evaluate_call` admitted malformed scalar/nested UART values before dispatch. ROOT reproduced
   invalid read/write/exchange calls returning ALLOW, accepted the physical-boundary risk, and
   repaired finite scalar/nested validation. A reviewer misread optional newline accounting; ROOT
   rejected that part, restored the contract with one predicate, and retained only the real fix.
6. LoRa spreading-factor narrowing treated the lower bound as a maximum. It admitted values below
   delegated 7 and rejected valid narrowed minimum 8. ROOT accepted the RF scope expansion risk and
   repaired the localized interval check plus regression assertion.
7. Evidence reviewers found forward-reference cycles in substitute/diagnostic artifacts and a
   status-path surrogate acceptance. ROOT accepted these because a real limitation test could not
   otherwise be created honestly; the fix was acyclic pre-run assignment plus post-run adapters and
   exact configured status-path binding.
8. A C0 review found the candidate had no executable C3-HARNESS path for O to submit a target
   assignment and for the candidate to launch/validate/observe/reap/report the worker. This was the
   accepted `F-PRE-C3-001` control-plane gap, not an orchestrator mistake and not a server problem.
   The minimal control-plane repair was then implemented, tested with CP04, joined at `b5753eb`, and
   reviewed by C0-0014.
9. Two stable-runner launch attempts used the wrong positional/flag shape. They exited before a
   controller existed; ROOT corrected the invocation and retained the error as administrative
   evidence. No green tests were reset.
10. CP04 and focused docs then passed once at the exact joined tip. The user pause came after this
    operational progress, while plan/checkpoint prose still contained the earlier pre-join state.

The lesson is the intended one: catch real harness/watcher/product/evidence defects, tolerate
recoverable coordinator mistakes, and spend repair/retest effort only where the production benefit
outweighs the complexity and regression cost.

## 12. Test-retention model and no-rerun rule

The protected original general harness is a release requirement. Before shared changes, the plan
records a baseline manifest of original test IDs, maps shared production modules to those IDs, and
records the dependency fingerprint of each result. A candidate-wide dependency map is required when
shared modules, launch/control code, or policy boundaries change. C2 may re-credit an old green ID
only by immutable evidence path/hash and unchanged fingerprint. It cannot copy a mutable registry or
claim that “same test name” means same result. The original tests must not be deleted, skipped,
xfail-marked, or weakened to hide a retrofit regression. New cross-route tests cover coding V1,
legacy firmware, events, claims, resume, lifecycle, cleanup, and ambiguous-route rejection.

The no-rerun rule has three levels:

- Green and dependency unchanged: retain evidence; do not rerun.
- Test-only fixture/setup or metadata correction with a completed deterministic checklist and
  known failed IDs: same test-author lane, rerun those exact IDs once, no C0/review/reconciliation.
- Production, policy, contract, expected-behavior, coverage, locked configuration, server pin,
  fixture binding, or evidence contract changed: use the material route, invalidating dependent
  review/tests and requiring the appropriate fresh C0/C1/C2. The scope of invalidation is exact,
  not a broad “rerun everything” reflex.

An orchestrator's bad command, prompt, result envelope, or metadata correction generally changes no
test dependency. Preserve the failed launch/report, fix the artifact or command, and resume the
same owner. A reviewer finding is not a license to stop reviewing or to rerun every green shard;
the reviewer completes its full surface and ROOT batches accepted repairs before another review.

## 13. Candidate final-test and promotion order

The final chain is intentionally strict:

`accepted joined tip -> shortest affected smoke -> fresh complete C0 + remaining focused join ->
fresh C1 -> dependency-invalidated C2 -> fresh F.C3.O/W attempt -> C4 -> pre-safeguard environment
admission -> one logical safeguard -> reconciliation -> inactive promotion -> outer candidate-root
verification`.

C0 is a fresh Terra reviewer, not an implementation coder. C1 locks the exact current inputs. C2
proves the locked candidate and retained original behavior without writing a full safeguard. C3 is
the only physical target project. C4 is a nested static audit of requirements, topology, evidence,
watcher boundary, protected state, scope, and test retention; evidence-only annotation correction
cannot replace acceptance evidence. Safeguard runs the accumulated candidate-root Ruff/format/
BasedPyright/compile/orchestrator/watcher/Codex integration/attention/firmware/MCP/new-test gate as
one logical run, resuming only incomplete/invalidated components after environment-only interruption.
A locked-input change creates a new C1 and new safeguard run ID. Promotion creates `progress/v1.2`
only at the exact green candidate and stages the named stable runner on the distinct outer-verifier
branch; it preserves `progress/v1.1`, rollback, all evidence, and unrelated outer changes.

## 14. Unresolved physical questions are gates, not guesses

The source material still leaves the CoreSX1262 `P.05` DIO2 notation ambiguous. Do not infer a GPIO
number from a board name or a requested test. Either authoritative setup evidence resolves it or the
radio action is blocked; if the design proves DIO2 irrelevant, record that non-dependency. Likewise,
the requested 915 MHz LoRa test is not self-justifying. The exact attached module variant, antennas,
supply/current limits, configured frequency, transmit power, bandwidth, duty cycle, and applicable
constraints must be electronically evidenced. User authorization is necessary but not a technical
or regulatory substitute. A missing board/route/model/server permission is an environment blocker,
not an excuse to guess or to claim physical pass.

## 15. Outer repository preservation boundary

The outer `main` checkout is intentionally dirty with user/project changes. Preserve all of them:
`.codex/` hook/dev tooling and tests, `HANDOFF.md`, deletion/rename records, `Firmware/` material,
`active_docs/`, `goal.md`, `plans/`, `harness-single-worktrees/`, `pre-conversion-rollback/`, and
the stable/candidate linked worktrees. Do not reset the outer repository to HEAD, clean untracked
Firmware/plans, remove old linked worktrees, or normalize the dirty MCP input. Runtime evidence is
not disposable scratch; it is the provenance needed to distinguish historical, invalidated, and
current results. Close worktrees only through exact Git worktree operations after promotion and
zero-process/clean-state checks.

## 16. How to update this handoff later

When checkpointing again, preserve this long-form context and the existing suffix. Add a dated
“latest observation” section near the top or update precise factual paragraphs, but do not silently
delete the decision ledger. Record exact commit, branch, lane ID, invocation/thread, result/finding
hashes, process/claim state, governing hashes, and which gate is next. State what was *not* run.
If a result is stale or superseded, retain it and say why; do not overwrite it with “passed.” If
the user edits the plan while paused, document the diff and classification before resuming. If a
new agent reads only this file, it should know the current authority, actor distinction, runner
split, evidence status, failure boundaries, no-rerun rule, and exact next step without having to
reconstruct the conversation from scratch.

## 17. Normative source snapshots follow

The next sections are generated snapshots of the current user-owned goal, specification, roadmap,
readiness record, and execution plan. They are included so a resuming agent can work from one
context file even if it does not immediately open every source document. The source files remain
normative; a snapshot is not permission to ignore a later hash change. Keep these snapshots after
the narrative and before the preserved suffix. The snapshot boundary is also useful for detecting
which parts are compacted context and which part is the user's original appended handoff.

--- BEGIN-NORMATIVE-SNAPSHOTS ---
### Snapshot: `goal.md` (current bytes at checkpoint time)

<!-- BEGIN SNAPSHOT goal.md -->
# Execution Goal: Backward-Compatible Physical Firmware Harness Acceptance

This file is the live, user-owned execution directive for the project. Execute it completely. Do not stop after planning, partial implementation, successful compilation, successful flashing, or a partially passing application.

## 1. Authoritative inputs

Before acting, read and follow:

1. `AGENTS.md` and every applicable nested `AGENTS.md`.
2. `HANDOFF.md`.
3. This `goal.md`.
4. `active_docs/GENERALIZATION_SPEC_2.md`.
5. `active_docs/IMPLEMENTATION_ROADMAP_2.md`.
6. `plans/general-coding-harness/EXECUTION_PLAN_2.md`.
7. `active_docs/EXECUTION_READINESS_2.md`.
8. The firmware fixture, datasheet, toolchain, experiment, and MCP-server material referenced by those documents.

The specification, roadmap, and execution plan define the detailed C1-C73 contract and execution topology. This file defines the overall mandate and takes precedence over those project planning documents if I edit it during execution. System, developer, safety, and applicable `AGENTS.md` instructions still take precedence over this file.

Do not invoke the planning-only `plan-harness-workflow` skill merely to execute the already-written plan. Use it again only if a material edit to this file requires the execution plan itself to be regenerated or structurally revised.

## 2. Live-goal update protocol

`goal.md` may change while work is in progress. Execution subagents must never edit this file.
`ROOT-IM` may edit it only when the user explicitly requests a planning/directive revision, as in a
pre-execution clarification; it must never silently rewrite the user's mandate during execution.

`ROOT-IM`, the current outside implementation coordinator defined in Section 6, must reread and
hash `goal.md`:

- at initial preflight;
- before every new large step;
- before each Loop 1 and Loop 2 dispatch;
- before C0, C1, C2, C3, C4, and the safeguard;
- at the actual boundary before every mutating MCP dispatch, with continuous change observation while
  a mutating operation is in flight;
- after every resume, compaction, or new session;
- before declaring completion.

Record each observed hash in the runtime management evidence. If the hash changes:

1. stop issuing new assignments long enough to read the new directive;
2. preserve currently valid evidence and safely checkpoint active work;
3. determine which requirements, steps, tests, hardware authorization, and evidence are affected;
4. revise the plan documents when the change materially alters scope or topology;
5. invalidate and rerun only work whose dependencies changed;
6. continue from the earliest affected gate.

Do not restart unaffected green work. Do not let an already-running worker silently reinterpret its fixed assignment; checkpoint it and issue an updated assignment through its explicit owner (`ROOT-IM` during product implementation or `F.C3.O` during the final target project) when necessary.

C1 binds the exact operative `goal.md` hash and hashes of the four planning/readiness documents.
After C1, a semantic change to requirements, authority, topology, locked inputs, or completion
conditions invalidates C1 and returns to the earliest affected implementation gate followed by fresh
C0/C1 and dependency-invalidated C2 before C3. After C1, every `goal.md` hash change is a lock-
invalidating user-directive change: immediately suspend new work/calls, expire pending/in-flight
hardware authorization, read the new goal, and follow the live-goal/relock route. `goal.md` can never
use editorial supersession. A byte-only editorial change to one of the other four governing
planning/readiness documents may avoid re-locking only with a fresh independent Terra reviewer and
ROOT's recorded no-dependency-impact decision. Its new hash is appended to the operative C1
directory's `EDITORIAL_SUPERSESSION.jsonl`; entries bind document, prior/new hashes, reviewed diff,
reviewer evidence, UTC time, and decision in an unbroken chain rooted at C1. For C4, safeguard, and
authorization, only those four documents may use the chain terminal as equality. Semantic changes
never can.

P4 manifest creation freezes every `external_references` path/hash through C4, safeguard, and
completion. Any later change to an external reference--including an append to
`EDITORIAL_SUPERSESSION.jsonl` or a byte-only change to one of the other four documents--invalidates
that C3 acceptance result; C4 and safeguard must reject it. Preserve the attempt, apply the normal
goal/editorial classification, and run a fresh C3 attempt (P0 plus only dependency-invalidated work)
before C4. A semantic or `goal.md` change still follows the fresh-lock route. C4 never accepts a
stale chain prefix as if it were the current terminal.

## 3. Objective

Implement `GENERALIZATION_SPEC_2` and `IMPLEMENTATION_ROADMAP_2` through `EXECUTION_PLAN_2` completely end to end.

The finished result must be a backward-compatible dual-path orchestrator harness that:

- preserves the already-successful general coding harness and its versioned coding invocation;
- continues to support existing schema-less policy-bound firmware invocations without migration;
- manages worker, MCP, relay, board, claim, event, checkpoint, result, and cleanup lifecycles honestly;
- uses the BYO Firmware MCP server as the physical firmware interaction boundary;
- passes a fresh four-board physical firmware acceptance project;
- leaves a clean, inactive, evidence-backed candidate ready for general use.

The acceptance project tests the **candidate harness and watcher**, not whether `ROOT-IM`,
`F.C3.O`, or a target worker is infallible. Assignment, prompting, sequencing, triage, command,
target-code, invalid-call, and result-envelope mistakes by those actors are expected recoverable test
work. Correct them through the owning lane or same-thread resume and retain unaffected green evidence.
Such a mistake does not by itself establish a harness/watcher defect, authorize `ABORT_REQUIRED`,
reopen a completed implementation step, invalidate C1, or justify a broad rerun. It becomes a
harness/watcher finding only when exact evidence shows that the candidate or watcher violated its
contract while accepting, rejecting, reporting, isolating, resuming, or cleaning up the mistaken
work. If an orchestrator mistake makes an immutable C3 attempt impossible to close honestly, use a
fresh attempt namespace for evidence integrity; that is not a candidate reset or implementation
failure, and it does not trigger relock unless a C1-locked input actually changes.

Execution must optimize for prompt delivery of a production-reliable product. Review and repair
effort is release-blocking only for a reproducible defect on a supported or credibly reachable
deployment path that can negatively affect correctness, safety, security, reliability, recovery,
required evidence integrity, or a required user-visible behavior. A latent authorization, identity,
cleanup, or fail-closed defect remains production-relevant when a realistic deployed input can
trigger it. Cosmetic issues, style preferences, unreachable or purely theoretical edge cases,
behavior-neutral cleanup, and speculative hardening without a concrete negative deployment
consequence are non-findings and must not consume a repair, relock, or retest cycle.

## 4. Starting state and preservation rules

- Pin implementation control to the clean detached `stable-general-harness-runner` checkout at
  `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`; evolving product work remains in a separate isolated
  candidate worktree.
- Preserve independently recoverable detached `pre-conversion-rollback` at
  `287ea53793e3963062882012ff80c3b0e8c41587` as rollback. The locked `frozen-harness-to-use`
  directory is a temporary non-operational legacy alias.
- Treat the completed runner transition as fixed execution infrastructure. The former physical
  `harness-in-progress/` checkout is absent. The historical Git common-directory name
  `.git/modules/harness-in-progress` and matching local submodule key remain only because the active
  linked worktrees share them; never rename, delete, reinitialize, or use them as a launch path.
- Launch every S1-S3/C0-C2/C4 implementation controller through
  `.codex/scripts/stable_runner.py`, which must prove the exact clean detached
  `stable-general-harness-runner@4699d27` lock before importing or dispatching. A lane/candidate
  working directory, `PYTHONPATH`, preloaded module, or output path must not make candidate code
  importable as the controller. Proof/projection outputs remain outside the stable checkout.
- Commit `4699d27` predates the candidate executable finding gate. A stable-compatible projected
  invocation may omit candidate-only gate/isolation fields, but `ROOT-IM` must independently verify
  the unprojected current-tip finding, result, and triage artifacts before accepting that lane. The
  candidate itself must enforce the full gate during final candidate acceptance.
- Do not rewrite or recommit the promoted baseline in place.
- Do not reuse previous V1 or V2 practical-acceptance runtime state.
- Reserve `plans/general-coding-harness/runtime/promoted-firmware-v2/` for the final fresh inactive
  runtime; it must be absent before execution and is not created until every promotion gate passes.
- Preserve unrelated outer-repository changes.
- Preserve every registered worktree from the completed general-harness project. Do not reuse its
  branches or paths as V2 lanes and do not remove it as preflight cleanup.
- Preserve the present dirty `Firmware/BYO-Firmware-MCP` checkout exactly as found.
- Create a clean isolated MCP-server worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`.
- Treat `Firmware/Firmware resources/` as a read-only evidence mirror. Do not modify its datasheets, packs, fixture records, retained evidence, or manifest-bound files.
- You may refactor or change the harness, the clean MCP-server worktree, and authoritative writable firmware/test-medium source under `Firmware/` when required by an in-scope, reproduced need.
- Do not perform speculative MCP-server refactors.

The collision-proof coordinates in `EXECUTION_READINESS_2.md` were created during completed
preflight. On resume, verify their exact recorded branches, commits, common directory, and clean
state; do not recreate, relocate, reset, clean, or silently substitute them. The reserved worktrees
live below the `firmware-v2/runtime` boundary so outer development hooks do not confuse candidate
changes with outer-checkout changes. Resume only from `PARALLEL_CHECKPOINT.md`; never restart
preflight or an already-green large step merely because the stable runner was renamed.

The firmware resource manifest's historical source paths are provenance, not current file
dependencies. Revalidate all mirrored destination byte counts and SHA-256 values. Do not require or
claim a live comparison to historical source paths that are absent. Treat absolute tool paths as
live inputs only after rechecking them, and replace the obsolete historical NCS
`PYTHONPYCACHEPREFIX` with a fresh per-lane cache below the V2 runtime.

## 5. Subagent assignments (not the root session)

These assignments govern only child agents launched headlessly through `codex exec`. They do not
select, relaunch, or constrain the current outside root session. The collaboration picker is not an
availability oracle. Use the exact requested assignments with no substitution:

- every launched orchestrator subagent, including `F.C3.O`: GPT-5.6 Sol, high reasoning, Fast via `service_tier="priority"`;
- all source-code coders: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`;
- all reviewers and test writers: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`;
- all doers and test executors: GPT-5.6 Luna, high reasoning, Fast via `service_tier="priority"`;
- isolated acceptance watcher `F.C3.W`: GPT-5.6 Terra, medium reasoning, Fast via `service_tier="priority"`.

The current outside root is `ROOT-IM`, the host implementation coordinator. `ROOT-IM` is not a
subagent launched by this plan and has no model, reasoning-effort, or service-tier gate in this
contract. Never apply the launched-orchestrator assignment to `ROOT-IM`.

Every headless launch must explicitly use `--dangerously-bypass-approvals-and-sandbox`,
`--dangerously-bypass-hook-trust`, `--ignore-user-config`, `--json`, the exact model,
`model_reasoning_effort`, explicit `service_tier="priority"`, and an isolated
`-C` root. Capture exact model/effort/tier/thread/PID-plus-creation/exit/final-message evidence. Do
not use `--ephemeral` for resumable lanes. Prove all required launch combinations during preflight.
If one fails, diagnose and fix the launch path; do not substitute another model.

Because user configuration is ignored, no lane may rely on a globally registered MCP server. Every
controller authorized to own a physical MCP process receives an explicit isolated BYO Firmware MCP
declaration bound to the clean pin and lane-local `.firm`, artifact, and log roots. In C3 only the
candidate harness physical-lane controller receives the physical server command/environment, owns
its process and stdio endpoint, and can forward a call. O and target workers receive no physical MCP
registration, endpoint, launch command, credentials, or inheritable handle; they submit structured
operation requests to the candidate harness broker and receive its recorded results.

Use the pinned server's stdio command `uv run --project
plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate --locked
pyocd-debug-mcp`, resolving the project argument to its absolute path and setting
`BYO_MCP_ARTIFACT_ROOT` to the lane's isolated state/artifact root. Keep stdout exclusive to MCP
framing and capture stderr separately. Never launch the dirty source checkout as the acceptance
server.

Do not inherit an ambient probe or target route. Reject unreviewed `.env` files; explicitly clear
`PYOCD_PROBE_UID` and `PYOCD_TARGET` for inventory; then bind a board-owning lane only to its exact
assigned probe UID and reviewed target/profile. Record the effective non-secret routing environment.

## 6. Required orchestration distinction

Use these identifiers in gates, evidence, and handoffs; do not use an unqualified "orchestrator" or
"manager" where the owner could be ambiguous:

1. `ROOT-IM` is the current outside root session. It coordinates the multi-agent creation of the harness retrofit, including product coding, review, test writing, test execution, integration, repairs, checkpoints, final safeguard, and promotion. It is outside the subagent assignment table in Section 5.
2. `F.C3.O` is a fresh Sol-high-Fast acceptance-orchestrator subagent launched directly by `ROOT-IM`. It operates the candidate harness under test and is the sole decision-maker for the final target project. `ROOT-IM` may start, supervise, terminate, and receive the result of this topology, but it must not assign or orchestrate target-project tasks.
3. `C3-HARNESS` denotes the candidate harness control plane and its exact controller processes, operated by `F.C3.O`. It is the system under test, not a Codex-agent role and not an agent slot. `F.C3.O` submits every target assignment to `C3-HARNESS`; `C3-HARNESS`, not `F.C3.O`, launches the assigned target worker through `codex exec`, owns its lifecycle, and records its exact launch/result/event/claim evidence. Direct target-worker launch by `F.C3.O` is prohibited because it would bypass the harness being certified.
4. `F.C3.A1`, `F.C3.C1`, `F.C3.P1`, and `F.C3.R1` are candidate-harness-launched target workers. They receive one serial assignment at a time through `C3-HARNESS`, return results through it, and do not report to `ROOT-IM` for target-project decisions.
5. `F.C3.W` is the separately launched read-only acceptance watcher. It observes candidate/topology invariants but never edits, assigns target work, approves hardware, or launches workers.

`F.C3.O` must coordinate its own multi-agent target-project creation flow by submitting serial target test-writer, coder, doer, and reviewer assignments through `C3-HARNESS` while `F.C3.W` is alive.

Keep production coding singular and serial. Role fan-out must remain between one and three and be used only for genuinely independent review, test-writing, or test-execution slices. Follow the preplanned pools in `EXECUTION_PLAN_2`; do not repartition dynamically merely because work is difficult or slow.

## 7. Implementation method

- Execute the three coherent large steps S1-S3 in order.
- Give each large step exactly two back-to-back QA loops.
- Treat atomic edits and individual modules as work inside a large step, not as separate loop cycles.
- Use isolated worktrees or run roots and disjoint ownership for parallel lanes.
- `ROOT-IM` owns every implementation merge, join, finding decision, failure classification, and final verification outside the final target project.
- Reviewers recommend; `ROOT-IM` decides implementation findings, while `F.C3.O` decides target-project findings during practical acceptance.
- Every reviewer, test writer, and test executor uses the candidate's structured finding-admissibility
  gate. A submitted gap is eligible for triage only when it is exactly one of
  `CODEBASE_BREAKING`, `FUNCTIONALITY_BREAKING`, or `WORTH_FIXING`. Every eligible submission must
  bind reproducible evidence and an affected requirement/behavior, propose the smallest sufficient
  fix, and explicitly compare the problem's impact and no-fix cost against implementation
  complexity, regression risk, verification cost, and lower-risk alternatives. The submitter must
  conclude, with evidence, that the problem outweighs the total risk and cost of the proposed fix.
- The executable gate validates that closed structure and rejects unsupported, incomplete, PASS-with-
  gap, style-only, speculative-hardening, cleanup, preference, or "technically nicer" findings.
  `ROOT-IM` or `F.C3.O` then independently decides whether the evidence is true and the tradeoff is
  favorable; a reviewer-supplied boolean or score is never sufficient proof. A rejected or
  inadmissible suggestion may be recorded as a non-finding but must not trigger source changes,
  reopen a green step, invalidate C1, or rerun a green test.
- An accepted repair is the smallest change whose expected benefit still outweighs its added
  complexity, regression surface, and verification burden. If no such repair exists, reject or
  defer the finding instead of making the product more fragile.
- A reviewer must finish the complete assigned affected-surface review even after finding a valid
  defect, unless an external blocker makes further inspection impossible. It returns one complete
  current-tip finding set; it must not intentionally stop at the first finding. `ROOT-IM` triages
  that whole set, and the serial coder repairs all accepted findings as one bounded batch before
  another independent review. No C0 or ordinary product review runs on an intermediate revision
  inside that batch.
- On a frozen joined revision, run the shortest already-required dependency-invalidated smoke IDs
  first. If they pass, the remaining focused test execution and read-only review may run in
  parallel; neither result unlocks the next gate until both join on the same revision. A production
  change invalidates both dependent conclusions and returns through the same batched flow.
- A correction that changes no production source, operative policy, public contract, locked
  configuration, test oracle, or behavioral expectation is administrative and resumes in the same
  lane without a new product review or green-test rerun. A strictly test-only correction may use the
  fast lane only when its diff is limited to synthetic fixture/setup or test metadata, the exact
  failed IDs are known, no production/policy/contract/locked-configuration file changes, and no test
  oracle, assertion streng…7347 tokens truncated…1. **P0 host and routing:** MCP protocol/schema, plans, permissions, isolated roots, toolchains, all four stable board identities, current serial routes, setup, and returning-state behavior.
2. **P1 STM32 pair:** tests first, then deterministic STM-A controller and STM-B I2C2 responder images with machine-readable UART evidence, sequence/checksum/error behavior, sustained ordered traffic, reset/reconnect, bounded recovery, and debugger observability; P1 requests every physical MCP action through the candidate harness broker.
3. **P2 nRF52 pair:** tests first, then one bounded codebase proving two-board BLE GATT command/acknowledgement and two-board 915 MHz CoreSX1262 ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence.
4. **P3 concurrent proof:** keep exactly one target doer agent (`F.C3.P1`) active and give it one candidate-harness assignment that requests two concurrent non-agent physical lane process groups: `P3.STM` owns STM-A/STM-B and `P3.NRF` owns NRF-A/NRF-B. During normal operation only `C3-HARNESS` may create, start, stop, and reap those groups; it owns both lane records, exact controller/process identities, claims, events, and cleanup, and each lane has separate MCP processes, `.firm`, artifact, and log roots. The narrow ROOT emergency host-termination rule below applies only when the controller cannot perform shutdown. `F.C3.P1` may request and operate both only through its assigned harness interfaces; it may not spawn either group or another Codex agent. Prove concurrent progress, isolation, same-resource contention/queueing, exact relays, a same-thread/path resume, one predeclared intentional target-code defect/fix, and selective retesting. Before injection, `F.C3.O` must record the exact source-controlled, non-destructive defect and expected behavioral failure. It may affect only target application source--never the harness, MCP server, fixture, authorization, or hardware configuration--and must fail through the normal target test path before candidate-launched target workers diagnose, repair, and selectively retest it.
5. **P4 shutdown and evidence:** return boards to the declared end state; close UART/debug/MCP; prove exact candidate-managed child exit/reap, zero claims, and exact event acknowledgements; obtain the terminal watcher report and exact W exit/reap; then have `F.C3.O` atomically create attempt-evidence `EVIDENCE_MANIFEST.json` followed by `ACCEPTANCE_RESULT.json`. At a quiescent checkpoint O recursively inventories every regular file in both attempt runtime/evidence roots, with no symlink/reparse point or unresolved temporary file. The manifest lists/hashes every file, including failed/denied/conflicting evidence, except exactly itself, the not-yet-created result, and reserved `topology/`. This closed set includes the attempt-local passed registry; target seed/source and all assignments/results; event/claim/relay lifecycle; proposals, O decisions, call authorizations/admissions, MCP plans/permissions/dispatch/results; build/firmware/physical protocols; controlled defect/repair/retests; watcher evidence; and P4 candidate-managed cleanup. C1/delegated/editorial artifacts outside the attempt roots are not inventory files; the manifest lists their canonical paths/hashes only as `external_references`. After manifest creation no in-domain file may appear or change. O must create the hash-bound, non-cryptographic result within 90 seconds; it binds schema, attempt, C1, target, manifest path/hash, watcher report, P4 state, O decision, and UTC time. C4 independently enumerates both roots, rejects every unknown/unlisted in-domain file or hash mismatch, verifies every external reference, and verifies the result. Assignment workers keep terminal `RESULT.json`. Reserved `topology/` contains O launch/key-release identity and liveness, ROOT-owned W launch/exit provenance, registered topology-helper, and ROOT shutdown evidence. After O exits, ROOT closes/hashes that subtree in `topology/TOPOLOGY_SHUTDOWN.json`; C4 verifies its inventory separately. Pre-exit evidence does not claim O/W exit.

P4 is ordered into two subphases. First, candidate-managed shutdown finishes; W writes its final
heartbeat and terminal report, then exits and is exactly reaped. ROOT writes the immutable
`WATCHER_EXIT.json`; only then is watcher evidence/provenance quiescent and O may create the manifest.
Thus W's normal exit is after the P4 shutdown subphase but
before P4 evidence closure. In the manifest, C1/delegated/editorial state is an
`external_references` array of canonical paths/hashes outside the attempt roots, not part of the
closed file inventory; C4 verifies each external reference directly against the operative C1. The
closed inventory itself remains exactly the two attempt roots minus the stated exclusions.

Use the applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intentions from the supplied experiment medium. The exhaustive A20-A26 matrix, B01-B39/Q40 corpus, Q41 endurance soaks, and destructive/try-last appendices remain extended non-gating qualification.

To avoid a second self-hash cycle, `topology/TOPOLOGY_SHUTDOWN.json` inventories and hashes every
other regular file in `topology/` but explicitly excludes itself. Symlink/reparse/temp entries are
forbidden. C4 independently enumerates that domain and separately hashes/verifies the shutdown file.

## 13. Watcher and abort behavior

Run a fresh isolated acceptance watcher throughout C3. "Read-only" means it cannot edit source,
candidate/target state, or hardware; it may write only its own attempt-local watcher evidence and an
`ABORT_REQUIRED` signal at the reserved watcher path. It does not approve calls or orchestrate target
work.

Before target work starts, `F.C3.W` must publish a ready record and begin a heartbeat at least every
30 seconds. Each heartbeat binds its exact process identity, monotonic sequence, timestamp, and
current observation cursor; the cursor may remain unchanged only while the observed logs are
unchanged. `ROOT-IM` monitors the exact process plus this evidence. An unexpected watcher exit, lost
observation access, stalled cursor while observed logs advance, or heartbeat gap greater than 90
seconds before the terminal shutdown audit is `WATCHER_LOST` and fails closed. `ROOT-IM` must stop
new assignments, terminate only the registered acceptance topology, preserve the attempt, and use a
fresh attempt after the same repair/relock classification used for `ABORT_REQUIRED`. The expected
watcher exit is allowed only after the P4 candidate-managed shutdown subphase and terminal report,
and must occur before O starts the P4 manifest closure subphase.

`ROOT-IM`, not W, atomically creates immutable reserved-topology provenance. After W is spawned and
before W readiness can admit target work, ROOT writes `topology/WATCHER_LAUNCH.json` with the exact
command/flags, isolated root, model, effort, tier, thread, PID-plus-creation identity, and UTC start.
After W's terminal report and exact exit/reap but before O creates the manifest, ROOT writes
`topology/WATCHER_EXIT.json` binding the launch path/hash, exact reaped identity, exit code/time,
terminal report path/hash, and captured final-message content/hash. Both files are create-once,
never watcher-authored, and later inventoried by `TOPOLOGY_SHUTDOWN.json`; missing or mismatched
provenance blocks P4/C57.

`ROOT-IM` also monitors O's exact process plus `topology/ORCHESTRATOR_HEARTBEATS.jsonl` at the same
30-second cadence/90-second staleness threshold from O readiness through result commitment and
normal exit. After `EVIDENCE_MANIFEST.json` appears, the result has an additional absolute 90-second
commit deadline. Unexpected O exit, lost/stale liveness, any manifest-without-valid-result deadline,
or normal exit without a valid result is `ORCHESTRATOR_LOST`. ROOT stops new work, terminates/reaps
only the registered topology, preserves the partial immutable attempt, records
`topology/ORCHESTRATOR_LOST.json`, and requires a fresh attempt after the same
repair/relock-versus-environment classification as `WATCHER_LOST`. A partial manifest/result is
never completed or reused in place.

After a valid result and O's exact normal exit/reap, ROOT atomically writes create-once
`topology/ORCHESTRATOR_EXIT.json`, binding O identity/key-release/result paths and hashes, exact
reaped identity, exit code/time, and captured final-message content/hash. On abnormal loss,
`ORCHESTRATOR_LOST.json` instead retains every available exit/final-message field and never claims a
normal exit. `TOPOLOGY_SHUTDOWN.json` inventories the applicable record; missing normal provenance
blocks completion.

If the watcher finds a reproducible candidate-harness or watcher defectâ€”such as wrong identity acceptance, false running/completion, cross-lane mutation, duplicate ownership, premature release, missing actionable notification, non-exact acknowledgement, leaked managed process, or watcher misclassificationâ€”it must emit an exact `ABORT_REQUIRED` record with correlated identities and evidence.

That signal is the create-once attempt-evidence file
`watcher/ABORT_REQUIRED.json`, not a `manager-signals/` entry. `F.C3.W` writes a same-directory
temporary file containing schema version, attempt ID, exact watcher process identity, heartbeat
sequence, observation cursor, invariant ID, correlated identities, evidence paths, earliest
invalidated sprint, and UTC timestamp, then atomically renames it with create-new/no-overwrite
semantics. `ROOT-IM` monitors this exact path directly from watcher readiness through the terminal
report. This watcher-owned path is the sole explicit exception to manager-owned signal-channel
writes.

Termination authority is ordered. ROOT first requests ordinary controller-managed shutdown. Only
when the exact registered controller is unavailable or unresponsive may ROOT perform host-process
termination/reap of the pre-registered controller/MCP/process-group identities. ROOT atomically
writes `topology/EMERGENCY_TERMINATION.json` with the shutdown request/path/hash, failure proof,
exact identities, per-process terminate/reap outcomes, and UTC/monotonic times. This is not authority
to call MCP, manipulate hardware, infer board success, or kill an unregistered process. Board state
becomes indeterminate, the attempt cannot pass, and the next attempt must run P0 returning-state
recovery through a healthy controller before mutation.

`ROOT-IM` must then:

1. terminate only the registered acceptance process tree;
2. preserve the failed runtime and evidence;
3. repair the harness or watcher through the owning implementation large step and its existing two-loop topology, preserving unchanged green IDs;
4. if any C1-locked input changes, run fresh C0, create a new C1 lock, and run dependency-invalidated C2 IDs;
5. apply the C3 restart protocol below only after the latest required C1/C2 pair is green.

Firmware application, compiler, target-test, target-repository configuration, and invalid-MCP-call defects are not harness aborts. Here "target-repository configuration" means configuration created inside the disposable C3 target repository whose dependency fingerprint is owned by that target project; it excludes the C1-locked harness configuration, acceptance-kit/lane templates, MCP launch templates, server pin/configuration, fixture bindings, authorization, and test/evidence contracts. Target-local defects remain work owned by `F.C3.O` and are repaired through target assignments submitted to `C3-HARNESS`. If a target finding requires any locked configuration/input to change, it leaves the target-local route and follows the C1 invalidation route.

A reproduced defect or incompatibility in the pinned BYO Firmware MCP server implementation is
neither target-source work nor a watcher `ABORT_REQUIRED`, and repairing that server is outside this
goal. The clean pinned worktree stays immutable; `ROOT-IM`, `F.C3.O`, implementation coders, and
target workers may not edit, recommit, or repin it.

`F.C3.O` may mark one affected test `AUTHORIZED_SERVER_LIMITATION` only with exact evidence that the
candidate reached and correctly contained the server boundary: call/method/version, raw MCP result
or failure, process and returning-state evidence, implicated pinned-source evidence, and why the
failure belongs to the server rather than the harness, target, fixture, inputs, or operator. O then
assigns the strongest safe substitute through `C3-HARNESS`: first a supported partial end-to-end MCP
test, otherwise a focused unit/integration test using the implicated pinned-server component,
otherwise a synthetic unit test of the candidate boundary. The original physical test is retained
as limited, not called green; the substitute has its own stable ID. No route may use direct
pyOCD/serial, weaken safety, silently skip evidence, or claim unexecuted physical behavior was
certified. C4 independently validates attribution and that no stronger safe substitute was
available. This exception never applies to the protected original general-harness unit tests.

Every C3 attempt uses a monotonically increasing immutable namespace
`plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/` and matching evidence
namespace `plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/`, beginning at
`attempt-0001`. Choose one greater than the largest number present in either runtime or evidence;
use `0001` only when neither side contains an attempt. Both paths for the chosen number must be
absent; a one-sided path or collision stops allocation for preservation/triage. Each attempt contains
its own `target/`, `hil/`, `events/`, `claims/`, `manager-signals/`, and `.agent-workspace/` roots.
Create the pair together; never clear, overwrite, fill a numbering gap, or reuse a prior attempt,
and leave completed/failed attempts retained read-only.

Every C3 restart caused by `ABORT_REQUIRED`, orchestration/evidence rollover, or another prescribed
attempt-ending condition uses a
new attempt namespace and fresh disposable target Git repository. The initial attempt begins from
the five locked seed files only. A restarted repository may reconstruct the exact last accepted
target source-tree commit plus the same locked seed, but it must not copy old build outputs, runtime
state, claims, events, or process records. P0 always reruns for the fresh attempt. Earlier green
target evidence remains credited only where its declared dependency fingerprint is unchanged;
tests dependent on the changed goal/harness/server/runtime/repository/process identity rerun from
the earliest invalidated sprint, and every new-attempt artifact originates in its numbered roots.

## 14. Audits and final verification

- C0 uses a fresh read-only Terra-medium-Fast reviewer with no implementation ownership. It reviews
  only a frozen joined candidate that has passed its shortest affected smoke IDs, completes the
  entire assigned candidate/critical-control-path sweep, and returns one complete finding set rather
  than stopping at the first defect. Remaining focused execution may overlap C0, but C1 waits for
  their exact-revision join.
- C0 explicitly audits backward compatibility and the original general-harness unit baseline before physical work.
- C2 runs the dependency-invalidated original unit tests, cross-route tests, disposable dual-path project, synthetic MCP/lifecycle, relay, event/ack, contention, resume, cleanup, and operator gates.
- C1 locks the operative goal/planning-document hashes, exact candidate revision, server pin/configuration, acceptance-kit and lane/MCP launch templates, fixture bindings, the five-file target seed, test/evidence contracts, authorization, and other implementation inputs consumed by C2/C3. It does not lock target application source or target-repository-local configuration subsequently created through `C3-HARNESS`; those are versioned in the target dependency fingerprint. If C2 repair changes a C1-locked input, the lock is invalid and a new C1 plus dependency-invalidated C2 are mandatory. Production, policy, behavioral-contract, coverage-obligation, or other operative changes return to the owning implementation step and full fresh C0. A qualifying pre-C3 strict test-only fast lane correction never inherits the old lock; changed candidate/test bytes still require a new C1 and dependency-invalidated C2, but it needs only its eligibility record and exact failed-ID rerun before that lock. Environment-only reruns and target-local changes that change no C1-locked input do not require re-locking. C3 may start only from the latest green C1 lock and its green C2 evidence.
- C4 uses fresh Terra-medium-Fast auditors after practical success.
- C4 audits C1-C73 coverage, orchestration-role separation, watcher boundary, physical evidence, exact revisions, protected state, scope, and baseline-to-candidate unit-test preservation.
- C4 and the safeguard verify exact C1 equality. `goal.md` must equal its C1 hash; only the other four governing documents may use a valid editorial-chain terminal. All other differences invalidate C1. C4/safeguard never create a second lock; invalid differences follow the owning-step and fresh C0/C1/C2/C3/C4 route.
- A C4 "evidence-only correction" means only a C4-owned report/annotation fix written outside every immutable C3 attempt root, under `plans/general-coding-harness/evidence/firmware-v2/final/C4/annotations/`. It cannot satisfy, alter, explain away, replace, or add any acceptance requirement/artifact. Any missing, incorrect, inconsistent, or incomplete closed C3 evidence requires a fresh C3 attempt from P0 and the earliest invalidated sprint, then C4. Target-source/local-config findings do the same. A repair changing a C1-locked input returns through its owning step, fresh C0/C1/C2, fresh C3, and C4. This C0 route is the sole ordinary post-lock exception.
- After C4 is green, complete the one logical `SAFEGUARD_RUN_ID` for the exact C1 lock under Section 9's admission/resume rule.
- Also run the outer repository verification required by `AGENTS.md` before final completion, including `--full` when the changed behavior triggers that requirement.

## 15. Completion criteria

Do not return as complete until all of the following are true:

1. C1-C73 each have exact evidence and no unresolved in-scope gap.
2. The original successful general harness remains protected by a complete green unit-regression matrix with no hidden weakening.
3. Existing schema-less firmware callers require no migration and the coding V1 path remains correct.
4. The separately orchestrated physical project passes STM32 I2C, nRF52 BLE, nRF52 LoRa, and concurrent four-board behavior.
5. Every accepted production-relevant harness, watcher, firmware, MCP, compiler, application, and
   test defect encountered in scope has been diagnosed, minimally repaired, and selectively
   retested; cosmetic, unreachable, behavior-neutral, and speculative non-findings remain deferred.
6. No required hardware action depended on guessed wiring or unauthorized destructive recovery.
7. All exact managed worker, helper, MCP, debug, UART, and watcher processes are exited and reaped.
8. All resource claims are released, all required top-level events are exactly acknowledged, and no actionable request/relay residue remains.
9. C0 and C4 audits are clean.
10. One terminal logical accumulated-safeguard record is green on the exact C1 lock with no incomplete component.
11. The required outer development verification is green.
12. Completion, candidate, server, acceptance, watcher, topology, criteria, protected-state, full-verification, promotion, and out-of-scope evidence are written.
13. The promoted runtime is fresh, inactive, and ready for general use while the prior rollback remains preserved.

If work remains safely possible, continue. Do not stop merely because the task is long, difficult, or required multiple repair cycles.

<!-- END SNAPSHOT goal.md -->
### Snapshot: `AGENTS.md`

<!-- BEGIN SNAPSHOT AGENTS.md -->
# Development rules

This file governs development of the harness. It is not part of the harness runtime protocol.

- Read `HANDOFF.md` before changing the product; it records current status and agreed design direction.
- Treat `GENERALIZATION_SPEC.md` as the proposed target product contract for the Python-focused generalized harness.
- No external workflow framework is active. The audited reference checkout was removed after the useful pieces were ported into `.codex/`.
- Before finishing a code change, run `uv run --project .codex/dev --locked python .codex/scripts/verify.py`.
- Run `uv run --project .codex/dev --locked python .codex/scripts/verify.py --full` when changing watcher retention or lifecycle behavior.
- Treat new Ruff, BasedPyright, compilation, or unit-test failures as blocking.
- Existing BasedPyright findings are recorded in `.codex/dev/basedpyright-baseline.json`; do not expand the baseline.
- Give parallel agents disjoint file ownership. Use `uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py` when isolated branches are useful.
- The main agent owns integration and final verification.
- Project Codex hooks block selected destructive commands, restore handoff context, and verify changed repository state before Codex stops.

<!-- END SNAPSHOT AGENTS.md -->
### Snapshot: `active_docs/GENERALIZATION_SPEC_2.md`

<!-- BEGIN SNAPSHOT active_docs/GENERALIZATION_SPEC_2.md -->
# GENERALIZATION_SPEC_2: Physical Firmware Compatibility and Acceptance

Status: paused after user-directed execution-layout optimization; S1-S3 complete, physical acceptance not started
Date: 2026-08-04
Primary product baseline: detached `stable-general-harness-runner` at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`
Firmware MCP source baseline: `Firmware/BYO-Firmware-MCP` at `f003f84a7df51cd8595a3203c62e225b21da2a22`
Launch-readiness contract: `active_docs/EXECUTION_READINESS_2.md`

## 1. Goal

Retrofit the promoted general coding harness so its existing firmware path is a supported, backward-compatible product surface, then certify that surface with a fresh multi-agent project on the connected STM32 and nRF52 hardware through the BYO Firmware MCP server.

The finished product must retain the already-accepted generic coding path, accept existing schema-less policy-bound firmware invocations without migration, manage real firmware workers and MCP lifetimes honestly, and pass a four-board practical acceptance campaign. The practical campaign is a test of the harness and watcher, not a test that the implementation coordinator, acceptance orchestrator, or target workers never make mistakes. It is not a requirement to exhaustively recertify every feature of the firmware MCP server.

## 2. Required outcome

At completion, all of the following are true:

1. Existing general coding invocations and results behave exactly as they did at `4699d27`.
2. Existing schema-less firmware invocations continue to parse and launch with the same policy-bound prompt, filenames, model settings, board tokens, leases, MCP declarations, server snapshot, request/relay, checkpoint, and result expectations.
3. No existing firmware caller is required to add a schema field, rewrite a configuration, or migrate retained evidence.
4. Firmware lanes have exact worker, helper, MCP, board, serial-route, claim, and request/relay identity throughout their lifecycle.
5. Resource ownership is safe across same-board serialization and different-board concurrency.
6. The supplied MCP server is the only firmware/hardware interaction boundary used by acceptance workers for probe discovery, connection, setup, flash, reset, debug, memory/register access, and UART operations.
7. A fresh acceptance orchestrator subagent uses the candidate harness to coordinate a new multi-agent target project on all four connected boards.
8. An isolated watcher can trigger a controlled whole-test abort for a harness or watcher defect and report the repair request to `ROOT-IM`.
9. The final target firmware behaves correctly, all exact managed processes are gone, all resource claims are released, and the one final accumulated safeguard is green.

## 3. Baselines and protected state

### 3.1 Harness

- Start product work from clean commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f` on a new isolated candidate branch and worktree.
- Reserve branch `firmware/v2-candidate` and worktree
  `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/`. Treat any
  unexpected pre-existing path or branch as a collision and preserve it.
- Preserve detached `pre-conversion-rollback` at `287ea53793e3963062882012ff80c3b0e8c41587` as rollback evidence; `frozen-harness-to-use` is only a temporary locked legacy alias.
- Use `stable-general-harness-runner/` as the sole implementation-control checkout through the
  fail-closed `.codex/scripts/stable_runner.py` lock. The old physical `harness-in-progress/` path is
  absent. Its name survives only in the shared Git common-directory/config metadata required by the
  registered linked worktrees and must not be treated as an executable path or renamed mid-run.
- Preserve the independent `pre-conversion-rollback/` recovery checkout and the locked legacy
  `frozen-harness-to-use/` alias. Neither is a controller, candidate, validation, or promotion root.
- Because the stable runner predates the executable candidate finding gate, ROOT independently
  verifies current-tip finding/result/triage artifacts for projected implementation invocations;
  final candidate acceptance still proves automatic candidate enforcement.
- Do not reuse either prior practical-acceptance runtime. Start a fresh inactive runtime root.
- Do not rewrite or recommit `4699d27` in place.
- Preserve unrelated outer-repository changes.

### 3.2 Firmware MCP server

- Bind the acceptance baseline to commit `f003f84a7df51cd8595a3203c62e225b21da2a22`.
- The present `Firmware/BYO-Firmware-MCP` checkout contains substantial pre-existing deletions. It is an input checkout, not a clean release candidate.
- Materialize a clean, isolated server worktree from the pinned commit for implementation and acceptance. Never reset, clean, or repurpose the existing dirty checkout.
- Reserve branch `firmware/v2-mcp-candidate` and worktree
  `plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate/`, subject to the same
  collision rule.
- Treat the clean server worktree as an immutable compatibility fixture. This project does not repair,
  refactor, recommit, or repin the BYO Firmware MCP server. Candidate work may inspect the pinned
  source and execute it only through the authorized acceptance boundary.

### 3.3 Firmware resources

- `Firmware/Firmware resources/` is a read-only convenience mirror. Its 47 manifest entries currently match their recorded byte counts and SHA-256 hashes.
- The PDFs, device packs, toolchain locks, fixture notes, and retained experiment evidence in that mirror are evidence inputs, not implementation targets.
- New or refactored acceptance-medium source belongs in an authoritative writable project area under `Firmware/`, never in the mirror.
- Historical manifest source paths are provenance strings and are not present in the current source
  checkout. Admit only destination copies whose current bytes match the manifest; do not assert a
  live source-to-copy comparison.
- Revalidate the absolute toolchain inputs. Replace the historical, absent NCS Python-cache path
  with a fresh per-lane `PYTHONPYCACHEPREFIX` under the V2 runtime; never write caches into the NCS
  source repositories or an old experiment.

## 4. Backward-compatibility contract

### 4.1 Legacy firmware invocation

The existing schema-less policy-bound firmware invocation remains supported. Compatibility includes:

- absence of a `schema` field routes to the firmware loader;
- the canonical policy file, sidecar digest, embedded policy text, zero-operator headings, and final precedence reminder remain mandatory;
- lane label-derived controller status and JSONL names remain valid;
- `leases`, `board_tokens`, `mcp_servers`, and `server_snapshot` retain their current meanings;
- existing model, reasoning, tier, command, overrides, prompt, resume-thread, event-log, and output fields retain their accepted shapes;
- firmware-shaped results remain valid only for firmware lanes and cannot satisfy coding lanes;
- request/relay records remain exact-hash, exact-call, exact-lane, exact-server-snapshot, and expiry bound.

No new public firmware schema is required for this release. An internal normalization helper may be introduced only if it eliminates duplicated validation without changing accepted inputs or serialized evidence.

### 4.2 Coding path

`orchestrator-coding-invocation/v1`, repository identity checks, current-tip result validation, generic exclusive claims, coding events, acknowledgements, and cleanup semantics must remain unchanged except for defect fixes that are directly required by this specification.

The already-green general harness is a protected regression baseline. Before implementation, record its existing unit-test IDs and results. Any change to shared parsing, controller, process, reconciliation, event, claim, Git/result, configuration, or documentation behavior invalidates the directly dependent original general-harness unit tests, which must pass before the affected step can close. Add cross-route unit tests proving that enabling or hardening firmware compatibility cannot alter a coding invocation, coding result, coding claim, coding event, or coding cleanup decision.

Original green tests may not be deleted, skipped, marked expected-failure, weakened, or replaced with less specific assertions merely to accommodate the retrofit. If an internal test must change because implementation structure moved, its review evidence must show that the original public behavior and failure modes remain covered at equal or greater strength.

### 4.3 Compatibility proof

Compatibility is proven by characterization tests copied from real accepted shapes, the protected original general-harness unit suite, new cross-route unit tests that exercise coding and firmware side by side, retained sample configurations, and the physical acceptance project. Documentation claims alone are insufficient.

## 5. Minimal product design

The preferred implementation is a bounded retrofit, not a second orchestration framework.

1. Keep the current dispatch boundary: versioned coding invocation versus schema-less firmware invocation.
2. Factor only shared lifecycle primitives that genuinely have identical semantics, such as exact child identity, event emission, acknowledgement, or resource cleanup.
3. Keep firmware-only policy binding, server snapshots, MCP lifetime reconciliation, board tokens, and hardware relays isolated from generic coding inputs.
4. Add an acceptance-kit layer containing immutable fixture bindings, MCP launch templates, target-project charters, evidence schemas, and selective-test metadata.
5. Add focused synthetic and disposable integration coverage before physical testing.
6. Do not add a plug-in framework, generic hardware abstraction, scheduler, device database, radio framework, or migration engine.

## 6. Agent and topology contract

The model assignments below govern subagents launched headlessly with `codex exec`; they do not
govern the current outside root session. The collaboration picker is not an availability oracle.

- Launched orchestrator subagents, including `F.C3.O`: GPT-5.6 Sol, high reasoning, Fast (`service_tier="priority"`).
- Coders that edit harness, MCP, test-medium, or firmware application source: GPT-5.6 Terra, medium reasoning, Fast (`service_tier="priority"`).
- Reviewers and test writers: GPT-5.6 Terra, medium reasoning, Fast (`service_tier="priority"`).
- Doers and test executors: GPT-5.6 Luna, high reasoning, Fast (`service_tier="priority"`).
- Watcher `F.C3.W`: reviewer/auditor classification, therefore GPT-5.6 Terra, medium reasoning, Fast (`service_tier="priority"`).

There is no model substitution. Preflight must prove that each exact model/tier combination can launch headlessly with the required no-approval, full-access flags before implementation begins.

The current outside root is `ROOT-IM`, the host implementation coordinator. It is not launched by
this plan and has no model/effort/tier gate in the subagent assignment contract. Every child launch explicitly uses
`--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust`,
`--ignore-user-config`, `--json`, exact model/effort/tier configuration, and an isolated root. A
resumable lane is not ephemeral. Because user configuration is ignored, firmware lanes receive an
explicit per-lane MCP server declaration and never depend on global MCP registration.
For C3, that physical declaration is installed only in the candidate harness lane-controller
process. O and target agents receive no physical server command/environment/endpoint/credential/
inheritable handle; their structured operation requests go to the harness broker, which alone owns
stdio and forwards only after all four call artifacts validate.

The MCP launcher must also reject unreviewed `.env` files and ambient probe/target overrides.
Inventory clears `PYOCD_PROBE_UID` and `PYOCD_TARGET`; a board-owning lane binds only its assigned
stable probe UID and reviewed target/profile in its recorded effective environment.

Product creation and practical acceptance have different, explicitly named orchestration owners:

- `ROOT-IM` is the current outside root session and coordinates product coders, reviewers, test writers, test doers, integration, and repairs. It is not a role-model assignment.
- `F.C3.O` is a fresh Sol-high-Fast acceptance-orchestrator subagent running the candidate system under test and is the sole orchestrator of the final target project.
- `ROOT-IM` supervises, aborts, or receives the result of the acceptance topology but never assigns the target-project tasks owned by `F.C3.O`.
- `C3-HARNESS` denotes the candidate harness control plane and its exact controller processes, not a Codex-agent role or agent slot. `F.C3.O` submits target assignments to it; it launches target workers through `codex exec` and owns their lifecycle evidence.
- `F.C3.O` must not launch a target worker directly. Target workers receive target-project work only through `C3-HARNESS`, return results through it, and never receive target assignments from `ROOT-IM`.
- `F.C3.O` serially coordinates target test writing, target coding, target execution, and target review through `C3-HARNESS` while `F.C3.W` is alive.

Gates and evidence must use `ROOT-IM`, `F.C3.O`, `F.C3.W`, or `C3-HARNESS`; an unqualified
"orchestrator" or "manager" is not sufficient where ownership, launch authority, or a model
requirement could be confused.

At most three fan-out lanes are allowed for any role pool. The default is one. A pool of two or three is used only for genuinely independent review, test-writing, or test-execution slices. Production coding is singular and serial.

## 7. Hardware fixture contract

### 7.1 STM32 pair

- STM-A and STM-B are NUCLEO-L476RG / STM32L476RG boards.
- I2C2 wiring is PB13/SCL, PB14/SDA, common ground, with installed 3.3 V pull-ups.
- USART2 uses PA2/TX and PA3/RX through ST-LINK VCOM.
- Last-known electronic identities are probe `066FFF514988525067233337` / COM12 for STM-A and probe `0668FF514988525067213913` / COM17 for STM-B.

### 7.2 nRF52 pair

- NRF-A and NRF-B are nRF52840 DK boards, each with a 915 MHz Waveshare CoreSX1262.
- Last-known electronic identities are probe `683710208` / COM16 for NRF-A and probe `683854191` / COM15 for NRF-B.
- CoreSX1262 mapping includes MOSI P1.15, MISO P1.14, SCK P1.13, CS P0.04, DIO1 P0.03, RESET P0.28, and BUSY P0.29.
- The retained notation `P.05` for DIO2 is unresolved. It must be resolved from authoritative electronic evidence or live setup before a dependent action. It must never be guessed.
- RXEN is soldered to 3.3 V and DIO2 is soldered to TX_EN as recorded by the fixture material.

The retained summary does not by itself prove the exact module band variant, supply/current limits,
or current RF constraints. Before transmission, authoritative fixture/setup evidence must admit the
two modules, antennas, configured 915 MHz frequency, transmit power, bandwidth, and bounded duty
cycle. Otherwise the RF-dependent gate remains blocked.

COM numbers are observations, not identities. Every run rediscovers routes and binds them to the stable probe/board identity through the MCP server.

## 8. Hardware safety and authority

1. No manual rewiring, visual inspection, button press, DMM measurement, cable move, or other operator touch is part of the autonomous gate.
2. Use electronic and software oracles: probe UID, board profile, MCP event logs, UART protocol, memory/register state, debug state, radio acknowledgements, and retained artifacts.
3. Every state-changing tool call requires the live server's exact plan and permission flow plus a recorded delegated hardware-authorization artifact scoped to the named boards and action class.
4. Ordinary application flashing, reset, debug, UART, BLE, and legal-band low-power LoRa testing are in scope after authorization.
5. Bootloader replacement, target unlock, mass erase, protection changes, and other destructive recovery are out of scope unless separately authorized after a demonstrated need.
6. LoRa uses the legal fixture frequency, the lowest practical power, short packets, and bounded duty cycle.
7. Same-board actions serialize. Independent boards may run concurrently only after unique identities and distinct state/artifact roots are proven.
8. A successful flash is never behavioral proof.

The user is the sole authority issuer through `goal.md` Section 11 or a later explicit directive.
The complete issued scope is the canonical JSON object in that section: four exact fixtures; nine
named action classes; explicit destructive prohibitions; application-region-only flash; UART write
maximum 256 bytes/call; BLE maximum 0 dBm; and LoRa exactly 915000000 Hz, at most 10 dBm, 64 payload
bytes, 6000 ms transmit airtime per rolling 60 seconds, 30 campaign minutes, 125000 Hz bandwidth,
coding rate 4/5, and spreading factor 7-10. Its canonical
sorted-key/compact UTF-8 JSON SHA-256 is locked; C1 copies the parsed object verbatim. S2 produces
C1-locked default-deny `MCP_METHOD_POLICY.json`: exact method/version, action class, allowed parameter
schema/ranges/safe flags, and prohibited-method/parameter/side-effect predicates. A method capable of
a prohibited action is denied unless technically constrained/proven safe for that call; labeling it
allowed is insufficient. Unmapped/ambiguous methods/parameters deny. Live evidence only narrows.
Each canonical policy evaluation binds exact MCP method/version, pinned server revision, schema hash,
locked policy path/hash, normalized parameters, matched rule/action class, result, reasons, and policy
duration maximum. Every mutating plan requires positive integer `max_operation_duration_seconds` and
denies when missing/invalid/over-policy.

The normative closed executable contract is
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
(SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`). It fixes the exact
default-deny method inventory, parameter schemas, safe flags, prohibited predicates, finite retained-
session transition graph, guarded plan/action protocol, candidate-control-plan semantics for allowed
methods without MCP-native plans, call-scope binding, final C1 authorization schema, and narrow
server-limitation API. Implementations and audits consume that artifact directly; summaries here do
not authorize a method, transition, argument, effect, or substitution absent from it.

The allowed gating inventory is exactly `setup_overview`, `load_setup_tool`, `board_setup-plan`,
`board_setup`, `continue_setup`, `board_fix_setup`, `board_validate`, `get_setup_status`,
`get_board_info`, `get_state`, `flash_application-plan`, `flash_application`, `reset_and_run`,
`read_memory_symbol`, `read_serial-plan`, `read_serial`, `write_serial-plan`, `write_serial`,
`serial_exchange-plan`, `serial_exchange`, and `disconnect`. Runtime routes, plans, permissions,
continuations, and server-returned arguments are accepted only from the exact immutable predecessor
and only after a new signed call decision. Each call binds the canonical delegated-scope hash,
exactly one method action class, and the decision's closed `scope_effect`; BLE/LoRa effects also bind
the exact operation manifest, electronic admission, and narrowed limits. `scope_effect` is not an
MCP argument and is never forwarded to the pinned server.

The final C1 authorization uses exactly the decision's five top-level keys and closed derived
bindings. ROOT creates and hashes it before `C1_LOCK.json`. A server limitation uses only the O-owned
signed decision and candidate-owned create-once record defined there, after a fully dispatched raw
failure and exact pinned-source/counterfactual attribution. It chooses the first safe available
partial-MCP, pinned-component, or candidate-boundary substitute; the original physical behavior is
always `NOT_CERTIFIED`, no direct hardware bypass is allowed, and protected original h…4253 tokens truncated… expected
harness behavior is to reject or contain invalid work, preserve exact state, support targeted
correction/resume, and release resources only under its normal lifecycle rules; the watcher must
classify that behavior as target/orchestration work. Only a reproduced violation of one of those
harness or watcher duties crosses the abort boundary. Correction reruns only failed or
dependency-invalidated IDs. If immutable-attempt rules make a fresh C3 namespace necessary, that is
evidence hygiene rather than a product reset and does not reopen implementation or C1 unless a
C1-locked input changes.

On such a finding `F.C3.W` atomically creates `watcher/ABORT_REQUIRED.json` by same-directory temporary write plus create-new/no-overwrite rename. Its schema names version, attempt, exact watcher process, heartbeat sequence, observation cursor, invariant, correlated identities, evidence paths, earliest invalidated sprint, and UTC time. `ROOT-IM` monitors that exact path directly from readiness through the terminal report, then terminates only the registered acceptance process tree, preserves evidence, and repairs through the owning implementation large step and its existing two-loop topology while retaining unchanged green IDs. Any repair that changes a C1-locked harness/watcher/kit/input requires fresh C0, a new C1 lock, and dependency-invalidated C2 before the C3 restart protocol below. An environment-only correction proven to change no locked input may proceed directly to a fresh attempt.

ROOT first requests normal controller-managed shutdown. Only if the exact registered controller is
unavailable/unresponsive may ROOT terminate/reap pre-registered controller/MCP/process-group host
identities, recording create-once `topology/EMERGENCY_TERMINATION.json` with request/failure proof,
identities, outcomes, and times. This grants no MCP/hardware/broad-kill authority; board state is
indeterminate, the attempt fails, and fresh-attempt P0 must recover returning state through a healthy
controller before mutation.

Firmware application, compiler, target-test, target-repository configuration, invalid-MCP-call, and ordinary orchestrator/operator failures are not harness aborts. Target-repository configuration means only configuration created and versioned inside the disposable target repository; it excludes C1-locked harness/kit/lane/MCP templates, server pin/configuration, fixture bindings, authorization, and test/evidence contracts. `F.C3.O` owns target-local diagnosis and repair through `C3-HARNESS`; a finding that requires a locked input change leaves that route.

A reproducible defect or incompatibility in the immutable pinned MCP server is an external test-medium
limitation, not a server-repair task and not by itself a harness/watcher defect. `F.C3.O` may classify
one affected physical test as `AUTHORIZED_SERVER_LIMITATION` only after preserving the exact call,
method/version, raw MCP result or failure, process/cleanup evidence, relevant pinned-source evidence,
and a counterfactual proving the candidate harness reached and correctly contained the server
boundary. O must then assign the strongest safe substitute that preserves the requirement's useful
semantics: first a supported partial end-to-end MCP test, otherwise a focused unit/integration test
against the implicated pinned-server component, otherwise a synthetic candidate unit test of that
boundary. No substitute may edit the server, bypass MCP with direct pyOCD/serial, weaken hardware
safety, or claim the unexecuted physical behavior passed. The original test ID is recorded as
`AUTHORIZED_SERVER_LIMITATION`, the substitute receives its own stable ID and evidence, and final
reports distinguish physically certified behavior from substituted coverage. C4 independently
validates attribution and substitute adequacy. This exception never permits deletion, skip, xfail,
or weakening of the protected original general-harness unit suite. Hardware absence or an
electronically proven fixture fault remains a nonterminal external condition unless the same
requirement can honestly be satisfied by the authorized server-limitation substitution above.

Every C3 attempt uses a monotonically increasing immutable runtime namespace
`plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/` and matching evidence
namespace `plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/`, starting at
`attempt-0001`. Choose one greater than the largest number present in either runtime or evidence and
use `0001` only when neither side has an attempt. Both chosen paths must be absent; a one-sided path
or collision stops allocation for preservation/triage. Each owns separate `target/`, `hil/`,
`events/`, `claims/`, `manager-signals/`, and `.agent-workspace/` roots. Retain every prior attempt
read-only and never clear, overwrite, fill a numbering gap, or reuse it.

Every restart uses the next namespace and a fresh disposable target Git repository. The initial
attempt starts from the five locked seed files only; a restart may reconstruct the exact last
accepted target source-tree commit plus that seed but never copies mutable runtime state or build
artifacts. P0 reruns on every attempt. Green target evidence is retained only when its dependency
fingerprint is unchanged; any test dependent on changed goal, harness, server, runtime, repository,
or process identity reruns, and all new artifacts originate in the new attempt.

## 12. Selective retest policy

- Every stable test has an ID, dependency fingerprint, input revision, and evidence path in its
  phase registry. The implementation registry `runtime/firmware-v2/passed-tests.json` becomes
  C1-locked/read-only during C3. Each attempt has fresh `acceptance/attempt-NNNN/passed-tests.json`
  inside its manifest domain; it may re-credit prior green evidence only through immutable path/hash
  plus unchanged dependency fingerprints and never copies/mutates prior registry state.
- A green test is not rerun unless code, configuration, firmware, server behavior, hardware identity, or an upstream artifact in its dependency set changed.
- A failed or newly implicated test is rerun after repair; unrelated green tests remain credited.
- A harness or watcher change invalidates the affected synthetic/integration tests and the affected practical sprint, but not unrelated target protocol evidence.
- A target firmware, target MCP configuration, or target MCP call-input change invalidates only the affected target tests and downstream physical sprint.
- The pinned MCP server source is immutable in this project. If it changes externally, its pin and
  every dependent S2/C0/C1/C2/C3 credit are invalid until the project is explicitly replanned; this
  execution never repairs or repins it.
- A shared harness change invalidates every original general-harness unit test mapped to that shared code. The passed registry may retain only original tests whose dependency fingerprints are demonstrably unchanged.
- After practical success and final static audit, the complete accumulated harness safeguard runs as one logical `SAFEGUARD_RUN_ID` for the exact C1 lock.
- For a bounded repair batch, preserve raw evidence from every lane but reconcile the dependency
  map, implementation registry, and aggregate join once against the accepted batch tip. Intermediate
  repair commits are not candidate checkpoints and do not receive their own C0, C1, or aggregate
  reconciliation.
- On that frozen joined tip, execute the shortest already-required affected smoke IDs first. After
  they pass, remaining focused test execution and independent read-only review may overlap. The
  gate joins both exact-revision results before advancing; a production change invalidates every
  dependent conclusion and returns through the batched repair flow.
- Administrative result-envelope, metadata, evidence-field, command, or path corrections that do
  not change production source, operative policy, a public contract, locked configuration, a test
  oracle, or a behavioral expectation resume in the same lane without product rereview or test
  rerun. A strict test-only fast lane is allowed only for synthetic fixture/setup or test-metadata
  changes when the exact failed IDs are known and a deterministic checklist proves no production,
  policy, contract, locked-configuration, test-oracle, assertion-strength, expected-outcome, stable-ID,
  or coverage-obligation change. The existing test-author thread corrects it and reruns exactly those
  failed IDs once before unrelated work; it receives no C0, ordinary review, or aggregate
  reconciliation. A failed rerun or unproved condition uses the material route. If C1 exists,
  changed candidate/test bytes still require a new C1 and affected C2. A change to expected product
  behavior, coverage obligations, an operative test/evidence contract, production, or policy is
  material and follows the full review/relock route. The fast lane applies only before C3 begins;
  after that point the existing attempt/lock/C4 invalidation rules remain intact.

C1 locks the operative goal/spec/roadmap/plan/readiness hashes, candidate revision, server
pin/configuration, acceptance-kit and lane/MCP launch templates, fixture bindings, five-file target
seed, test/evidence contracts, authorization, and other implementation inputs used by C2/C3. Target
application source and target-repository-local configuration created later by `C3-HARNESS` are
excluded and versioned in the target dependency fingerprint. Any repair after C1 that changes a
locked input invalidates that lock and requires a new C1 Checkpoint A plus dependency-invalidated C2
before C3. Production, policy, behavioral-contract, coverage-obligation, or other operative changes
return to the owning step and full fresh C0. Only a qualifying strict test-only fast lane correction
may avoid fresh C0 before the new C1, after recording its checklist and exact failed-ID rerun. Every
post-C1 `goal.md` hash change invalidates C1,
suspends/invalidates hardware calls, and cannot use editorial supersession. A byte-only change to
one of the other four docs may append to `EDITORIAL_SUPERSESSION.jsonl` only after a fresh independent
Terra review and ROOT no-impact decision. Entries link document/prior/new/diff/reviewer/time in an
unbroken C1-rooted chain; only those four chain terminals count as equality. Semantic changes cannot.
P4 manifest creation freezes every external-reference path/hash through completion. A later document
change or editorial-chain append makes that C3 result stale and requires a fresh C3 attempt before
C4; C4/safeguard must reject the stale result and may not accept an earlier chain prefix. Goal or
semantic changes still require the fresh-lock route.
Environment-only
reruns and target-local changes that change no locked input do not require a new lock.

Before creating `SAFEGUARD_RUN_ID`, an environment-admission gate performs no safeguard source check
or test and may be repaired/repeated. After logical safeguard start, an environment-only
interruption resumes the same ID and reruns only incomplete or dependency-invalidated components;
unchanged green components remain credited. Any source/test/server/locked-input change ends that
logical run and requires a new C1 lock and new run ID. Promotion requires one terminal green logical
record with no incomplete component.

After C4, an evidence-only correction means only a C4-owned report/annotation under
`evidence/firmware-v2/final/C4/annotations/`, outside all attempt roots. It cannot satisfy/alter/
replace/add acceptance evidence. Any defect in closed C3 evidence or target-local source/config starts
a fresh C3 attempt from P0/earliest invalidated sprint, then C4. A locked-input repair returns through
owning step, fresh C0/C1/C2/C3/C4; that C0 is the post-lock exception.

C4 and safeguard do not create a second lock. They require exact C1 `goal.md` and permit editorial
chain equality only for the other four governing documents; any candidate revision
or other invalid locked-input difference must follow the applicable repair/re-lock route.

## 13. Review and test finding admissibility

The candidate provides an opt-in, backward-compatible executable finding gate, and every review,
test-writing, and test-execution invocation created by this project enables it. A lane submits a
closed `orchestrator-review-findings/v1` artifact bound to its lane, invocation, role, and exact
candidate commit. PASS requires an empty finding list; FAIL requires at least one admissible finding;
BLOCKED may be gap-free only when it reports an external execution condition rather than a product
gap. The controller rejects a terminal result whose required finding artifact is missing, stale,
cross-lane, malformed, or inconsistent with the result outcome.

Each submitted finding has exactly one category:

- `CODEBASE_BREAKING`: reproducible evidence shows a required build, static gate, protected test,
  integration, schema, or compatibility contract breaks.
- `FUNCTIONALITY_BREAKING`: reproducible evidence shows required runtime, safety, lifecycle,
  acceptance, or user-visible behavior differs from the governing contract.
- `WORTH_FIXING`: the behavior is not already breaking, but concrete expected benefit materially
  exceeds the smallest fix's implementation complexity, regression risk, and verification cost.

A release-blocking finding must also demonstrate a supported or credibly reachable deployment path
and a concrete negative consequence for correctness, safety, security, reliability, recovery,
required evidence integrity, or required user-visible behavior. A latent authorization, identity,
cleanup, or fail-closed defect qualifies when a realistic deployed input can trigger it. Cosmetic
issues, style preferences, behavior-neutral cleanup, unreachable paths, purely theoretical edge
cases, and speculative hardening without such a consequence are non-findings even when the code
could be made technically nicer.

Every category must name affected requirements/behaviors and exact evidence, observed versus
expected behavior, reproduction, impact and no-fix consequence, the smallest sufficient fix,
complexity/regression/verification costs, lower-risk alternatives, and a reasoned conclusion that
the problem outweighs the total fix risk and cost. The executable gate proves completeness and
identity, not the truth of subjective claims. `ROOT-IM` decides implementation findings and
`F.C3.O` decides target-project findings; each records an evidence-based accept/reject decision.
Style preferences, speculative hardening, cleanup, theoretical edge cases without credible impact,
and technically nicer designs are non-findings. They cannot trigger edits, resets, relocks, or
retests. Accepted repairs remain minimal and are rejected or deferred when their complexity or
regression surface is disproportionate.

Every reviewer must complete its full assigned affected-surface and critical-control-path sweep
after discovering a defect unless an external blocker prevents further inspection. It returns one
complete finding set for the exact reviewed tip and may not intentionally stop after the first
finding. The owning orchestrator triages that complete set, the single production coder repairs all
accepted findings as one bounded batch, and the next product review starts only after the batch is
joined and its shortest affected smoke IDs pass. C1 is created only after a terminal clean C0 and
the exact-tip focused test join; it is never used as an intermediate repair checkpoint.

## 14. Evidence and pass criteria

The release passes only when all of these are recorded:

1. Exact harness, MCP server, acceptance-project, toolchain, pack, datasheet-manifest, and fixture identities.
2. Clean isolated worktree and runtime provenance.
3. Green compatibility, lifecycle, relay, MCP, resource, cleanup, dual-route, and protected original general-harness unit tests, with no unjustified deletion, skip, expected failure, or weakened assertion.
4. Fresh final reviewer decision on the frozen joined candidate, after a complete sweep rather than
   first-finding return, with no unresolved production-relevant in-scope gap.
5. Fresh `F.C3.O` identity/key-release and ROOT-owned `F.C3.W` launch/exit records plus `C3-HARNESS` launch records proving every target agent was candidate-launched with the required model/tier and was not launched directly by `F.C3.O`.
6. Green STM32 I2C, nRF52 BLE, nRF52 LoRa, and concurrent four-board behavioral evidence.
7. Correct handling of controlled target failure, selective repair, checkpoint/resume, contention, exact acknowledgement, and shutdown.
8. Zero unresolved actionable events, zero live exact managed child identities, zero owned resource claims, and no unclosed serial/MCP session.
9. After candidate-managed shutdown, W final report and W exit/reap, ROOT writes `WATCHER_EXIT.json`, then O atomically creates manifest and result. The manifest inventories/hashes every regular file under both attempt roots, including the attempt passed registry and adverse evidence, except itself, result, and reserved topology; C1/delegated/editorial are instead canonical external path/hash references verified directly by C4. Symlink/reparse/temp/later writes are forbidden; C4 independently enumerates. Result follows within 90 seconds. After O exit ROOT writes `ORCHESTRATOR_EXIT.json` and separately closes topology.
10. `topology/TOPOLOGY_SHUTDOWN.json` inventories/hashes every other regular topology file but excludes itself; symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and separately hashes/verifies shutdown.
11. A final nested static audit proving requirement, topology, evidence, and original general-harness unit-regression coverage, including a baseline-to-candidate test-manifest comparison.
12. One terminal green logical `SAFEGUARD_RUN_ID` covers the complete accumulated safeguard after the practical gate, with no incomplete component.
13. A completion summary and out-of-scope ledger explicitly distinguish harness certification from extended MCP/firmware qualification.
14. A candidate-root safeguard result that cannot be confused with the outer verifier's fixed
    `stable-general-harness-runner` target, followed by outer verification only after the green candidate is
    staged on a distinct promotion branch.

Any required test failure, ambiguous identity, missing authorization, unresolved `P.05` mapping needed by a test, watcher abort, or missing evidence prevents promotion.

## 15. Non-goals and over-engineering boundary

This project does not:

- replace the firmware MCP server with direct hardware scripts;
- redesign the existing generic coding contract;
- create a universal board, RTOS, radio, or transport abstraction;
- support boards beyond the four named fixtures;
- add cloud scheduling, a web UI, a database, or a new workflow framework;
- require all firmware MCP experiments, all seeded bugs, or endurance soaks for release;
- infer fixture wiring or authorize destructive recovery;
- keep agents, MCP servers, or watchers alive after their evidence is complete.

The sufficient product is a backward-compatible dual-path harness, a reproducible MCP-backed acceptance kit, a convincing four-board project, and durable evidence. Additional machinery is rejected unless a failing requirement demonstrates the need.

## 16. Definition of done

Implementation is complete only after the roadmap and execution plan have been followed end to end,
the separate acceptance orchestrator has completed the practical project under the isolated
watcher, every accepted production-relevant failure has been minimally repaired and selectively
retested, the final full safeguard is green once, promotion evidence is written, and the new runtime
is left inactive and clean for general use. Cosmetic, unreachable, behavior-neutral, and speculative
non-findings may remain deferred.

<!-- END SNAPSHOT active_docs/GENERALIZATION_SPEC_2.md -->
### Snapshot: `active_docs/IMPLEMENTATION_ROADMAP_2.md`

<!-- BEGIN SNAPSHOT active_docs/IMPLEMENTATION_ROADMAP_2.md -->
# IMPLEMENTATION_ROADMAP_2: Backward-Compatible Physical Firmware Acceptance

Status: paused after user-directed execution-layout optimization; resume only from the reconciled firmware V2 checkpoint
Governing specification: `active_docs/GENERALIZATION_SPEC_2.md`
Execution controller: `plans/general-coding-harness/EXECUTION_PLAN_2.md`

## 1. Delivery strategy

Extend the promoted harness in three coherent large steps, prove the accumulated candidate with non-hardware gates, then hand a fresh locked candidate to `F.C3.O`, a separate acceptance-orchestrator subagent, for the physical test project. The current outside root remains `ROOT-IM`, the implementation coordinator, throughout. `ROOT-IM` must not become the final target-project orchestrator.

The implementation uses the smallest useful architecture:

1. characterize and harden the existing legacy firmware path;
2. add a reproducible MCP-backed acceptance kit and test medium;
3. finish the backward-compatible release surface and final gates;
4. run one separately orchestrated physical project;
5. complete one logical accumulated safeguard run under the admission/resume rule and promote only on complete evidence.

Atomic edits and individual modules are tasks inside a large step, not separate execution cycles. Each large step receives exactly two back-to-back review/test/fix loops. Production coding is always singular and serial. Independent review, test-writing, and test-execution work may fan out to two lanes; no pool exceeds three.

Each loop operates on repair batches, not individual findings. Reviewers finish their full assigned
affected-surface sweep and return one complete exact-tip finding set. `ROOT-IM` triages the complete
set, the serial coder repairs all accepted production findings together, and no product review,
C0, C1, or aggregate registry reconciliation runs on an intermediate batch revision. Review effort
is release-blocking only for a supported or credibly reachable deployment defect with a concrete
negative effect on correctness, safety, security, reliability, recovery, required evidence, or
required user behavior; realistic latent authorization/fail-closed defects remain in scope, while
cosmetic, unreachable, behavior-neutral, or speculative improvements do not.

## 2. Fixed subagent assignments and root ownership

`ROOT-IM` is the current outside root session and implementation coordinator. It is not launched by
this roadmap and is not governed by the model/effort/tier assignments below. All other rows are
headless `codex exec` subagents with no model substitution.

| Role | Model | Reasoning | Service tier | Pool rule |
|---|---|---|---|---|
| `ROOT-IM` implementation coordinator | Current outside root session | not assigned | not assigned | exactly 1 host; not a launched subagent |
| `F.C3.O` acceptance orchestrator | GPT-5.6 Sol | high | Fast / `priority` | exactly 1, fresh subagent |
| Product or target coder | GPT-5.6 Terra | medium | Fast / `priority` | exactly 1 active, serial |
| Reviewer or test writer | GPT-5.6 Terra | medium | Fast / `priority` | 1 by default, 2 only for independent slices |
| Doer or test executor | GPT-5.6 Luna | high | Fast / `priority` | 1 by default, 2 only for independent slices |
| `F.C3.W` acceptance watcher | GPT-5.6 Terra | medium | Fast / `priority` | exactly 1, isolated and read-only |

Preflight proves the exact three model/tier launch combinations: Sol-high-priority,
Terra-medium-priority, and Luna-high-priority. A missing model is a blocking
preflight failure, not grounds for substituting another model.

## 3. Working locations and ownership

`ROOT-IM` created these isolated locations during completed preflight and now preserves their exact
recorded identities:

- product candidate: a new worktree and branch from harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`;
- firmware MCP candidate: a clean worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`;
- runtime: `plans/general-coding-harness/runtime/firmware-v2/`;
- evidence: `plans/general-coding-harness/evidence/firmware-v2/`;
- final inactive runtime: `plans/general-coding-harness/runtime/promoted-firmware-v2/`, absent until
  promotion;
- disposable final target: a fresh Git repository under the current immutable
  `acceptance/attempt-NNNN/target/` namespace, not the harness or server repository;
- each physical lane: a separate MCP process, `.firm` state root, artifact root, log root, and board assignment.

The reserved coordinates are:

- harness: `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/` on new
  branch `firmware/v2-candidate`;
- MCP: `plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate/` on new branch
  `firmware/v2-mcp-candidate`.

Both were created only after their path and branch absence was checked. On resume, exact identity
and cleanliness replace the original absence check; neither is recreated or silently substituted.
The reserved promotion ref `progress/v1.2` remains absent until promotion. Any new collision is
preserved and escalated rather than cleaned or reused.

The existing dirty `Firmware/BYO-Firmware-MCP` checkout, `Firmware/Firmware resources/`, prior V1/V2 acceptance runtimes, promoted commit `4699d27`, and frozen rollback commit `287ea537` are read-only inputs.
The 13 retained linked harness worktrees from the completed project and the current V2 linked
worktrees are protected state. The physical implementation runner is
`stable-general-harness-runner@4699d27`; `.git/modules/harness-in-progress` is only their retained
shared Git store. Never rename or remove that common directory while these worktrees exist.

All implementation-lane controller dispatch uses `.codex/scripts/stable_runner.py` and its immutable
runner lock. The launcher must reject a wrong/dirty/attached checkout, hostile lane/candidate import
paths, conflicting preloaded modules, and proof/projection outputs inside the stable checkout. A
stable-compatible projection does not transfer candidate-only finding-gate enforcement to the old
runner; ROOT validates the original artifacts until final candidate testing proves the new gate.

## 4. Preflight gates

Preflight is a gate, not a full QA cycle. It has completed for this execution. The numbered list is
retained as provenance and must not be rerun wholesale on resume; repeat only mutable checks mapped
to the next gate or a changed dependency.

1. Re-read `HANDOFF.md`, this roadmap, the specification, `EXECUTION_READINESS_2.md`, the execution plan, and all applicable `AGENTS.md` files.
2. Record the current session as `ROOT-IM`; do not apply a child-agent model gate to it and do not
   create a nested replacement implementation manager.
3. Confirm the promoted harness and frozen rollback identities and cleanliness.
4. Confirm the outer repository's unrelated changes and record the preservation boundary.
5. Confirm the two reserved paths and branches are absent. Record the dirty firmware-server checkout
   without altering it; create both isolated worktrees at their exact pins.
6. Verify all destination entries in `Firmware/Firmware resources/SOURCE_MANIFEST.csv` by byte count
   and SHA-256. Record that historical source paths are unavailable provenance rather than claiming a
   live source comparison.
7. Resolve and record exact toolchain, device-pack, datasheet, fixture, server, and harness hashes.
   Derive a new per-lane `PYTHONPYCACHEPREFIX`; never use the absent historical cache path.
8. Prove the exact headless launch shape, including approval/sandbox bypass, hook-trust bypass,
   ignored user configuration, JSONL evidence, exact model/effort/tier, isolated root, and durable
   thread identity for resumable lanes.
9. Prove an explicit per-lane-controller clean-server MCP declaration works without global user configuration.
   Reject unreviewed `.env` files, clear ambient probe/target overrides for inventory, and bind each
   board-owning lane only to its exact assigned stable UID and reviewed target/profile.
10. Run read-only electronic discovery through that MCP boundary; prove stable identities for STM-A, STM-B, NRF-A, and NRF-B and rediscover current serial routes.
11. Resolve the retained `P.05` notation from authoritative evidence before admitting a DIO2-dependent action. Do not infer it.
12. Resolve authoritative RF admission evidence for module variant, antennas, supply/current,
    configured 915 MHz operation, power, bandwidth, bounded duty cycle, and applicable constraints.
13. During preflight record the canonical non-authorizing draft and validate only the intended authorization schemas/authority boundary; do not implement product logic here. S2 exclusively implements and tests the ordered proposal, independent signed O decision, derived authorization, expiry-through-result, exact cleanup flow, and `MCP_METHOD_POLICY.json`; C1 later validates and locks their completed hashes. The S2 contract below uses create-new/no-overwrite artifacts, new IDs for retry/fresh attempts, and only explicit user direction may extend delegated time with fresh C1.
    - Treat the canonical JSON object in `goal.md` Section 11 as the entire issuance. S2 builds default-deny `MCP_METHOD_POLICY.json` with exact method/version, allowed parameter schema/ranges/safe flags/duration maximum, and prohibited method/parameter/side-effect predicates; C1 later locks it. A destructive-capable method denies unless technically constrained/proven safe for the exact call; labels cannot override prohibition. Every mutating plan requires positive bounded `max_operation_duration_seconds`. Proposal, O decision, authorization, dispatch, and result bind exact method/version, server revision/schema, policy/evaluation hashes, arguments, plan/duration, stable probe UID, target/profile, current route/null, and immutable identity/claim paths/hashes; harness pre/post validates and mismatch denies success.
    - Two-stage key release: create nonce/keypair/launch intent; spawn O with nonce and no key; write exact post-spawn identity; exchange identity-hash acknowledgment over the inherited pipe; write create-once `ORCHESTRATOR_KEY_RELEASE.json`; only then send key/discard ROOT copy. Signed ready/work/decisions bind release hash/time and earlier records; never rewrite, and failure requires a fresh attempt.
    - At every mutating dispatch, hash all five docs: `goal.md` must exactly match C1, while only the other four may use editorial-chain equality. After validation create immutable `dispatch-admissions/{CALL_ID}.json` binding authorization hash, fresh five hashes, revalidated fields, monotonic clock/start/deadline; dispatch/result reference it and never mutate authorization. Enforce the declared deadline with cancellation/exact cleanup and `INDETERMINATE_TIMEOUT`/no-success on overrun. Mismatch expires calls/emits `GOVERNING_INPUT_CHANGED`. Keep the registered ROOT watcher in flight; change uses `INDETERMINATE_EXPIRED`.
      Register that non-agent helper's exact identity/current hashes/heartbeat in `topology/GOVERNING_INPUT_WATCHER.json`; it writes only its evidence and must exit/reap into topology shutdown.
14. Confirm destructive recovery actions remain excluded.
15. Launch one no-op headless smoke for each exact Fast launch combination: Sol-high-priority,
    Terra-medium-priority, and Luna-high-priority; record model, effort, tier, thread,
    PID-plus-creation, exit, and final-message identity.
16. Create the fresh event log, manager-signals root, implementation passed registry, out-of-scope ledger, and `PARALLEL_CHECKPOINT.md` without starting product work. C1 later freezes that registry; C3 uses only attempt-local registries.
17. Run `scan --no-write`; require no unowned active candidate process, ambiguous claim, stale actionable relay, or reused acceptance state.
18. Record the existing full-gate evidence for unchanged `4699d27`. Do not rerun it during preflight.
19. Record the candidate-root gate protocol and focused commands. S3 must materialize and test the
    exact safeguard launcher; the ordinary outer verifier's fixed `stable-general-harness-runner` target
    cannot be credited for candidate-only code.

## 5. Standard large-step cycle

Every large step uses this fixed sequence:

1. `ROOT-IM` gives one Terra-medium-Fast coder the complete bundled step.
2. After integration, independent Terra-medium-Fast reviewers inspect their full disjoint assigned
   surfaces, continue after discovering a defect, and return one complete evidence-linked finding
   set for the exact reviewed tip.
3. `ROOT-IM` rejects any finding that is not reproducibly `CODEBASE_BREAKING`,
   `FUNCTIONALITY_BREAKING`, or demonstrably `WORTH_FIXING` on a supported or credibly reachable
   deployment path with a concrete negative product consequence. For accepted findings it weighs
   problem/no-fix impact against the smallest repair's complexity, regression risk, verification
   cost, and lower-risk alternatives. The same coder repairs every accepted production finding from
   that complete result as one serial minimal batch; no review or reconciliation occurs on an
   intermediate repair commit.
4. Independent Terra-medium-Fast test writers add only missing specification and regression
   coverage, including coverage implicated by the accepted batch. Test changes merge in
   deterministic order after ownership checks to form one frozen joined tip.
5. Run the shortest dependency-invalidated smoke IDs on that tip. A failure returns immediately to
   its owning coder or test writer before remaining execution or any revived product review.
6. After smoke passes, independent Luna-high-Fast doers execute the remaining focused stable shards. Any
   reviewer whose surface changed after its complete review may perform the required targeted
   exact-tip confirmation in parallel; the step waits for both results before advancing.
7. `ROOT-IM` applies the same complete finding/admissibility decision to the joined results, batches
   every accepted production/test repair, and reruns only dependency-invalidated surfaces and IDs.
8. Administrative result-envelope, metadata, evidence-field, command, or path corrections that do
   not change operative product/test meaning resume in the same lane and do not reset product
   review or green tests. A strict test-only fast lane applies only to synthetic fixture/setup or
   test-metadata diffs with known failed IDs and a deterministic checklist proving unchanged
   production, policy, contract, locked configuration, oracle, assertion strength, expected outcome,
   stable ID, and coverage obligation. Use the same test-author continuation and rerun exactly those
   IDs once before unrelated work; do not create C0, ordinary review, or reconciliation. A change to
   expected behavior, coverage obligations, or an operative test/evidence contract is material.
9. The second loop immediately rechecks only dependency-invalidated surfaces and IDs under the same
   batch/smoke/parallel-join rules. Unchanged green evidence remains credited.
10. After the batch tip is accepted, reconcile its dependency map, green stable IDs, and aggregate
   evidence into the implementation registry once; raw lane evidence remains preserved throughout.
11. Checkpoint A records that exact accepted revision, residual scope, clean process state, and the
    unlocked next step.

There is no arbitrary iteration cap. Repeated same-signature failure, oscillation, only-extraneous scope churn, or unrecoverable error is escalated with evidence; difficult work alone is not a reason to stop.

The gate is fail-closed on missing/stale/cross-lane finding artifacts and PASS-with-gap results. Its
closed schema requires exact evidence, affected requirement/behavior, observed/expected behavior,
reproduction, impact/no-fix consequence, smallest sufficient fix, implementation complexity,
regression risk, verification cost, alternatives, and the submitter's reasoned conclusion that the
problem outweighs the fix. Code validates structure and identity; the owning orchestrator validates
truth and tradeoff. Style-only, speculative, cleanup, or merely nicer suggestions are retained only
as rejected non-findings and cause no edit, reset, relock, or retest.

For this gate, credible impact requires a supported or realistically reachable deployed trigger and
a concrete consequence for correctness, safety, security, reliability, recovery, required evidence
integrity, or required user-visible behavior. Latent authorization and fail-closed defects remain
eligible when such a trigger exists. Cosmetic, unreachable, behavior-neutral, and purely theoretical
issues do not enter a repair batch.

## 6. Large step S1: Legacy firmware lifecycle and compatibility

### Product work

1. Capture accepted schema-less firmware invocation and result fixtures from the current implementation and retained evidence.
2. Characterize policy-bound prompt verification, filenames, event log location, model settings, server snapshot, leases, board tokens, MCP declarations, and resume behavior.
3. Characterize coding-versus-firmware dispatch and reject ambiguous or cross-shaped results.
4. Audit exact worker/helper/MCP process identity and lifecycle reconciliation for active, waiting, checkpointed, exited, unknown, and cleanup states.
5. Audit exact request/relay hashes, arguments, server snapshot, expiry, and manager ownership.
6. Audit board and generic claim ownership, same-resource serialization, independent-resource concurrency, stale handling, and release-after-reap behavior.
7. Factor a shared primitive only when identical semantics are proven by tests; otherwise keep the firmware and coding adapters separate.
8. Add compatibility, lifecycle, event, request/relay, resume, claim, and dual-route tests.
9. Record a protected baseline manifest of the original successful general-harness unit tests, map shared production modules to those IDs, and run every dependency-invalidated original unit test after shared changes.
10. Add focused cross-route unit tests proving firmware compatibility work cannot change coding invocation, result, claim, event, repository, or cleanup behavior.
11. Reject test deletions, skips, expected failures, or weakened assertions used to hide a general-harness regression; require equal-or-stronger replacement coverage for any structural test move.
12. Update the firmware contract documentation without changing legacy caller requirements.

### Exit

S1 passes when existing fixtures remain accepted, malformed or ambiguous shapes fail closed, resource and MCP state is honest, every dependency-invalidated original general-harness unit test and every new cross-route unit test is green, no original coverage was weakened, all stable tests are registered, and no physical board was mutated.

## 7. Large step S2: MCP-backed acceptance kit and test medium

### Product and test-medium work

The controlling S2 repair contract is the immutable
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
(SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`). Its closed method policy,
finite retained-session state machine, predecessor-bound guarded plan/action flow, per-call
delegated-scope/action/effect enforcement, five-key final C1 authorization support, create-once
server-limitation API, and `AUTHORIZED_SERVER_LIMITATION` seed route are implemented and preserved
at candidate `659dd03` with their green credits. The later accepted pre-C3 gap requires the bounded
candidate-owned control-plane/provenance repair preserved on product lane `e5ced272`; it must be
joined with adapted CP04 coverage and pass the optimized batch/smoke/review/execution flow before
fresh terminal C0. Keep the pinned server unmodified and
unlaunched during this repair.

1. Add a version-pinned acceptance manifest containing harness, server, fixture, datasheet, pack, and toolchain identities.
2. Add per-lane MCP…3189 tokens truncated…one `F.C3.P1` doer agent active under one candidate assignment while it requests two concurrent non-agent physical lane process groups: `P3.STM` owns STM-A/STM-B and `P3.NRF` owns NRF-A/NRF-B. During normal operation only `C3-HARNESS` creates, starts, stops, and reaps those groups and owns both lane/controller/process/claim/event/cleanup records; each lane has distinct MCP, `.firm`, artifact, and log roots. `F.C3.P1` may request and operate them only through assigned harness interfaces and cannot spawn them. Prove independence, same-resource contention, exact relays, a same-thread/path resume, one predeclared intentional target-code defect/fix, selective retest, and no cross-resource mutation. Before injection `F.C3.O` records the exact source-controlled, non-destructive defect and expected behavioral failure. It may affect only target application source and must fail through the normal test path before repair.
5. **P4 â€” shutdown and evidence:** close boards/candidate state; W final-reports/exits/reaps; ROOT writes `WATCHER_EXIT.json`; then inventory both attempt roots. The manifest lists every in-domain file except self/result/topology and uses `external_references` for canonical C1/delegated/editorial paths/hashes outside those roots. No later in-domain write. O creates result in 90 seconds; C4 independently enumerates both roots and directly verifies external references. After O exit ROOT writes `ORCHESTRATOR_EXIT.json` and separately closes topology.
   The shutdown file inventories/hashes every other regular `topology/` file but excludes itself; symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and separately hashes/verifies shutdown.
   Manifest creation freezes all external-reference paths/hashes through completion. Any later doc
   change or editorial-chain append invalidates that C3 result; preserve it, apply the normal
   classification, and use a fresh attempt before C4. Never accept a stale editorial-chain prefix.

### Failure routing

- Mistakes by `ROOT-IM`, `F.C3.O`, or a target worker--including bad assignment, prompt, order,
  command/config path, target edit, invalid MCP call, triage, or result-envelope content--return to
  their owning lane for targeted correction or same-thread resume. They are expected adverse
  workload, not evidence of a candidate/watcher defect. They do not emit `ABORT_REQUIRED`, reopen a
  green implementation step, invalidate C1, or erase unrelated green credits. A fresh C3 namespace
  required solely because immutable evidence can no longer close is an attempt rollover, not a
  candidate reset; relock occurs only when a C1-locked input changes.
- Target application, compiler, target-test, target-repository-configuration, or invalid-MCP-call failure stays inside the acceptance project only when it changes no C1-locked input. `F.C3.O` submits diagnosis/repair assignments through `C3-HARNESS` and reruns only affected IDs. A required locked kit/template/configuration change leaves this route.
- A reproduced pinned MCP server defect/incompatibility is reported by `F.C3.O` as
  `AUTHORIZED_SERVER_LIMITATION`; neither O, ROOT, nor a target/implementation coder edits or repins
  the server. O retains exact attribution evidence and assigns the strongest safe substitute in the
  order partial MCP, focused pinned-component unit/integration, synthetic candidate boundary unit.
  The unexecuted physical behavior is reported as not physically certified. C4 must reject a weak or
  convenient substitution when stronger safe evidence was available.
- A candidate harness or watcher defect causes `F.C3.W` to write a same-directory temporary record and atomically create, without overwrite, `watcher/ABORT_REQUIRED.json` containing schema version, attempt, exact watcher identity, heartbeat/cursor, invariant, correlated identities, evidence paths, earliest invalidated sprint, and UTC time. `ROOT-IM` directly monitors this path, terminates the registered topology, preserves evidence, and reopens the owning implementation large step under its existing two-loop topology. Any locked-input change then requires fresh C0, new C1, and dependency-invalidated C2 before a new C3 attempt; an environment-only correction proven not to change locked input may proceed directly to a new attempt.
- If watcher liveness or observation evidence fails before its post-P4 terminal report, `ROOT-IM` records `WATCHER_LOST`, stops new assignments, terminates the registered topology, preserves the attempt, and applies that same classification before a fresh attempt; a dead watcher is not required to emit its own abort.
- If O liveness/result commitment fails, `ROOT-IM` records `topology/ORCHESTRATOR_LOST.json`, stops/reaps the registered topology, preserves the partial attempt, and never completes or reuses partial manifest/result files. Classify the cause independently: an orchestrator-side failure rolls only to a fresh attempt with unchanged locked inputs and retained eligible green credits; only exact evidence of a harness/watcher or locked-input defect enters its corresponding implementation/relock route.
- Every C3 restart uses the next immutable `attempt-NNNN` pair and fresh disposable target Git repository. The new repository may reconstruct the exact accepted target source-tree commit plus the locked seed but copies no build/runtime state. P0 always reruns; later green target tests remain credited only when their dependencies did not change, and new-run artifacts come only from the new attempt.
- No broad process kill is permitted. Termination uses the registered root/child identities.
- ROOT requests controller-managed shutdown first. Only if the registered controller is unavailable/
  unresponsive may ROOT terminate/reap its pre-registered controller/MCP/process-group host identities,
  recording `topology/EMERGENCY_TERMINATION.json`. This grants no MCP/hardware authority; the attempt
  fails with indeterminate board state and fresh-attempt P0 recovery is required before mutation.

## 11. Final audit, safeguard, and promotion

1. **C4 nested static audit:** after practical success, launch fresh Terra-medium-Fast auditors for requirement coverage, topology/role separation, evidence consistency, watcher boundary, protected state, scope, and preservation of the original successful general-harness unit behavior. The audit compares baseline-to-candidate test IDs, dependency mappings, results, skips/xfails, assertion strength, and shared-code coverage. C4 is the ordinary post-lock static-review phase; the explicit locked-input repair route below may re-enter C0.
2. Classify gaps before repair. "Evidence-only" is only a C4 report/annotation correction under `evidence/firmware-v2/final/C4/annotations/`, outside attempts, and can never satisfy/alter/replace acceptance evidence. Any closed-C3 evidence or target-source/config defect requires fresh C3 from P0/earliest invalidated, then C4. Locked-input repair uses owning step/fresh C0/C1/C2/C3/C4. Rerun dependency-invalidated IDs only.
3. Verify exact C1 goal hash. Only the other four docs may resolve through a valid editorial chain. Other differences use re-lock route; never create a second/final lock here.
4. Run a pre-safeguard environment-admission gate that executes no safeguard source check or test;
   repair/repeat admission until green. Then create exactly one logical `SAFEGUARD_RUN_ID` for the
   C1 lock. An environment-only interruption resumes that ID and only incomplete/invalidated
   components; a locked-input change ends it and requires a new lock/run ID.
5. Require Ruff, formatting, BasedPyright with no baseline expansion, compilation, orchestrator tests, watcher tests, Codex integration tests, attention retention, synthetic firmware tests, and all newly accumulated tests to pass.
6. Reconcile zero process, claim, request, relay, and event residue.
7. Write completion, candidate, server, acceptance, watcher, topology, criteria, protected-state, full-verification, promotion, and out-of-scope records.
8. Promote a fresh inactive runtime and preserve the prior frozen rollback.

The safeguard operates on the reserved candidate root, including a non-expanded mapping of the
existing BasedPyright baseline. Only a green candidate safeguard permits creation of
`progress/v1.2` at that exact commit and staging of the explicitly named stable runner on the distinct branch for
the required outer verifier. Preserve `progress/v1.1`; do not publish externally without a live
directive.

Once promotion evidence is durable, close the temporary candidate and MCP linked worktrees only
through exact Git worktree operations after clean-state, retained-revision, and zero-process checks.
Never recursively delete a worktree path.

## 12. Atomic completion criteria

These IDs are the authoritative checklist consumed by the execution plan.

| ID | Requirement |
|---|---|
| C1 | Product work starts from exact clean harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`. |
| C2 | Frozen rollback `287ea53793e3963062882012ff80c3b0e8c41587`, prior runtimes, and unrelated outer changes are preserved. |
| C3 | A new isolated harness candidate branch/worktree is used; `4699d27` is not rewritten. |
| C4 | A clean isolated MCP server worktree is created from `f003f84a7df51cd8595a3203c62e225b21da2a22`; the dirty source checkout is untouched. |
| C5 | All 47 resource-mirror files pass byte-count and SHA-256 validation. |
| C6 | Preflight does not mutate hardware before live authorization and plans are recorded. |
| C7 | Exact harness, server, toolchain, pack, datasheet, fixture, and target hashes are retained. |
| C8 | Every run and lane has isolated runtime, MCP state, artifact, and log roots. |
| C9 | Schema-less firmware invocation remains the legacy dispatch route. |
| C10 | Canonical policy bytes, digest sidecar, headings, embedded text, and final reminder remain enforced. |
| C11 | Legacy label-derived output filenames and firmware event-log naming remain accepted. |
| C12 | Legacy model settings, leases, board tokens, MCP declarations, server snapshot, prompt, outputs, and resume fields retain their accepted shapes. |
| C13 | `orchestrator-coding-invocation/v1` behavior and repository/result safety remain unchanged. |
| C14 | Coding and firmware input/result shapes cannot ambiguously satisfy the other route. |
| C15 | Retained legacy fixtures, examples, and accepted configurations still run without edits. |
| C16 | No migration, evidence rewrite, or new public firmware schema is required. |
| C17 | Any internal normalization is behavior-preserving and limited to proven duplicate lifecycle logic. |
| C18 | Dual-route automated tests prove coding and firmware lanes coexist. |
| C19 | Worker, controller, helper, and descendant identity uses PID plus creation evidence and ownership correlation. |
| C20 | MCP launcher, server, and provider lifetimes are exact, current, and lane-correlated. |
| C21 | Hardware relays bind exact request hash, arguments, lane, server snapshot, decision, and expiry. |
| C22 | Expired, stale, malformed, changed, or unbound relays remain visible and cannot authorize execution. |
| C23 | Firmware checkpoint/resume preserves same thread and path identity without inventing liveness. |
| C24 | Native lifecycle events are emitted and only exact top-level `ack --event-id` acknowledgements clear them. |
| C25 | Board tokens and operational leases are distinguished from historical declarations. |
| C26 | Generic and hardware claims have exact owner identity and fail-closed stale handling. |
| C27 | Independent board lanes can progress concurrently without shared-state contamination. |
| C28 | Same-board and same-resource work serializes without double ownership. |
| C29 | Claims and hardware resources release only after exact child/MCP exit and reap are proven. |
| C30 | Unknown, partial, corrupt, or ambiguous lifecycle evidence fails closed and remains actionable. |
| C31 | Acceptance workers request every physical operation through the candidate harness broker; only its lane controller holds/uses the BYO Firmware MCP stdio/launch capability after validating all four call artifacts. |
| C32 | The server revision is pinned and changes only for a reproduced in-scope defect. |
| C33 | Each physical lane controller owns a distinct MCP process/endpoint, `.firm` state, artifact root, and log root; O/target workers receive no direct physical endpoint or inheritable capability. |
| C34 | Four board profiles bind stable board/probe identity and are rediscovered at run start. |
| C35 | COM ports are live routes, never primary board identity. |
| C36 | STM-A/STM-B I2C2, UART, ground, and pull-up fixture bindings match authoritative material. |
| C37 | The CoreSX1262 `P.05` notation is resolved authoritatively before any dependent action and is never guessed. |
| C38 | Datasheet, device-pack, and compiler inputs match their recorded hashes/locks. |
| C39 | Canonical scope/policy/duration/identity/governing fields bind proposal, signed decision, authorization, immutable pre-dispatch admission, dispatch, and result; monotonic deadline overrun, mismatch, or expiry is fail-closed/no-success. |
| C40 | Bootloader replacement, unlock, mass erase, and protection changes remain excluded. |
| C41 | LoRa uses 915 MHz fixture intent, lowest practical power, short packets, and bounded duty cycle. |
| C42 | Physical assertions use electronic/software oracles only; no operator touch is required. |
| C43 | The final target is a fresh disposable Four-Board Dual-Family Firmware Lab repository. |
| C44 | STM-A controller and STM-B responder images implement a deterministic machine-readable protocol. |
| C45 | The STM32 pair proves ordered I2C exchange, checksum/sequence/error evidence, UART, reset/reconnect, debug, and sustained traffic. |
| C46 | The nRF52 codebase proves a deterministic two-board BLE GATT command/acknowledgement mode. |
| C47 | The nRF52 codebase proves deterministic CoreSX1262 ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence. |
| C48 | Accepted STM32 I2C and nRF52 LoRa subsystems pass concurrently on all four boards in two non-agent groups whose complete lifecycle is owned only by `C3-HARNESS`. |
| C49 | Build/artifact provenance and MCP-mediated setup, flash, reset, debug, memory/register, and UART evidence are retained. |
| C50 | Behavioral oracles, not flash success, determine application pass. |
| C51 | One predeclared intentional, source-controlled, non-destructive target-code defect produces its recorded expected behavioral failure, is diagnosed, repaired, and selectively retested without changing or being called a harness/server/fixture defect. |
| C52 | One real physical lane checkpoints and resumes with the same thread/path identity. |
| C53 | Practical acceptance proves independent concurrency and same-resource contention behavior. |
| C54 | Boards/candidate state close; O's closed-inventory manifest/result covers all in-domain files; ROOT's separate closed topology inventory proves O/W reap; C4 independently enumerates both domains. |
| C55 | Fresh Sol-high-Fast subagent `F.C3.O`, never `ROOT-IM`, owns final practical-project decisions, while `C3-HARNESS` exclusively launches and owns target workers. |
| C56 | `ROOT-IM` remains implementation coordinator/supervisor and never assigns final target-project work. |
| C57 | Separate W observes read-only, reports after candidate-managed P4 shutdown, then exits/reaps before immutable manifest closure; ROOT-owned immutable topology records prove exact launch, final message, exit, and reap. |
| C58 | Watcher/O loss stops through controller shutdown first; only controller unavailability permits ROOT's recorded pre-registered-host-process emergency termination, failed attempt, and fresh-P0 recovery. |
| C59 | Harness/watcher defects use `ABORT_REQUIRED`; target application/compiler/test/target-repository-configuration/invalid-call defects remain acceptance-project work only when no C1-locked input changes; a proven immutable pinned-server defect/incompatibility uses `AUTHORIZED_SERVER_LIMITATION` with exact attribution, strongest-available substitution, and explicit non-certification of the skipped physical portion, never server repair or repinning. |
| C60 | `ROOT-IM` directly launches only `F.C3.O` and `F.C3.W` for C3; `F.C3.O` submits target assignments and never launches target workers directly; `C3-HARNESS` launches each target coder, reviewer/test-writer, and doer with the exact requested model, effort, and tier through headless `codex exec`, with no substitution. This child-launch criterion does not apply to `ROOT-IM`. |
| C61 | Production coding is singleton/serial; actual role fan-out is 1-3 and used only for independent work. |
| C62 | Each implementation large step receives exactly two back-to-back QA loops; modules do not receive individual cycles. |
| C63 | The C1-frozen implementation registry and fresh manifest-covered attempt registry prevent rerunning unchanged green tests without allowing C3 to mutate locked or prior state. |
| C64 | One terminal green logical `SAFEGUARD_RUN_ID` covers the complete accumulated safeguard after practical success/final audit; pre-admission is outside the run, environment-only interruption resumes it selectively, and any locked-input change requires a new lock and run ID. |
| C65 | The core gate uses the applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intentions. |
| C66 | Exhaustive A20-A26, B01-B39/Q40, Q41 soaks, and destructive/try-last cases are explicitly non-gating extended qualification. |
| C67 | Evidence binds requirements to exact revisions, identities, tests, artifacts, authorization, and hardware observations. |
| C68 | A fresh final reviewer completes the full frozen-tip sweep and reports no unresolved admissible production-relevant compatibility, safety, correctness, or complexity gap; every submitted gap proves a credible deployed trigger and concrete negative consequence, passes the structured category/evidence/cost-benefit gate, and receives the owning orchestrator's independent decision. |
| C69 | Final nested audits prove requirement coverage, role topology, watcher boundary, evidence consistency, and protected state. |
| C70 | Promotion occurs only from the locked green candidate into a fresh inactive runtime while preserving rollback. |
| C71 | Quick-start and examples accurately teach legacy firmware, coding V1, dual-path operation, events, acknowledgements, resume, and cleanup. |
| C72 | No unnecessary framework, scheduler, hardware abstraction, board expansion, UI, database, endurance gate, or reviewer-driven fix whose complexity/regression/verification cost is disproportionate to its demonstrated benefit is added. |
| C73 | A protected baseline-to-candidate unit-test matrix proves the original successful general harness still works: every dependency-invalidated original unit test and new cross-route isolation test is green, and audits find no unjustified deletion, skip, expected failure, weakened assertion, or unmapped shared-code change. |

## 13. Stop conditions

The implementation is genuinely complete only when C1-C73 have evidence, no accepted
production-relevant in-scope gap remains, the original successful general-harness unit behavior
remains proven, the practical project is green under `F.C3.O` and `F.C3.W`, one terminal logical
safeguard run is green with no incomplete component, and promotion records point to a clean inactive
runtime. Cosmetic, unreachable, behavior-neutral, and speculative non-findings may remain deferred.
A narrowly reviewed `AUTHORIZED_SERVER_LIMITATION` may satisfy only its affected criterion through
the strongest available substitute and must disclose the physically uncertified portion. A
partially working application, a green flash, an unreviewed or convenience substitution, or an
unresolved identity ambiguity is not completion.

<!-- END SNAPSHOT active_docs/IMPLEMENTATION_ROADMAP_2.md -->
### Snapshot: `active_docs/EXECUTION_READINESS_2.md`

<!-- BEGIN SNAPSHOT active_docs/EXECUTION_READINESS_2.md -->
# EXECUTION_READINESS_2: Firmware V2 Launch Boundary

Status: **PAUSED BY USER FOR PLAN OPTIMIZATION; RESUME REQUIRES EXPLICIT USER DIRECTION**
Observed: 2026-08-04, America/Los_Angeles

This record originally closed static launch ambiguities for `goal.md` and `EXECUTION_PLAN_2`.
Execution has since completed preflight and S1-S3 and reached the bounded pre-C3 control-plane
repair recorded in `HANDOFF.md` and
`plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md`. Product commit `e5ced272`
is preserved but has not received independent review, adapted CP04 coverage, runtime execution, or
candidate integration. The user paused execution while optimizing the gate layout. This record is
not hardware evidence or permission to skip the optimized C0/C1/C2 chain. On explicit resume,
`ROOT-IM` repeats only mutable checks mapped to the next gate or a changed dependency; it does not
restart preflight or already-green large steps.

## 1. Reserved clean coordinates

The following locations and branches are reserved for this plan:

| Purpose | Path | Branch / base |
|---|---|---|
| Harness candidate | `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/` | clean `firmware/v2-candidate` at `659dd03e2aa7159090c8e0e20123b1fec1749f90` before the preserved control-plane repair join |
| Clean MCP candidate | `plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate/` | clean `firmware/v2-mcp-candidate` at `f003f84a7df51cd8595a3203c62e225b21da2a22` |
| Local promotion ref | n/a until the safeguard is green | new `progress/v1.2` at the locked candidate commit |
| Runtime | `plans/general-coding-harness/runtime/firmware-v2/` | fresh; never reuse V1/V2 acceptance state |
| Evidence | `plans/general-coding-harness/evidence/firmware-v2/` | fresh |
| C3 attempts | matching runtime/evidence `acceptance/attempt-NNNN/` pairs beginning at `attempt-0001` | allocate one greater than largest number on either side; both chosen paths absent; each immutable after exit |
| Promoted inactive runtime | `plans/general-coding-harness/runtime/promoted-firmware-v2/` | created only after all gates pass |

The runtime/evidence roots and both candidate branches now exist by design. Their presence is not a
collision. Resume requires exact agreement with the checkpoint and recorded provenance; an
unexpected replacement, extra promotion ref, wrong commit/branch/common directory, or dirty
candidate is a collision or integrity failure. Preserve it and stop before mutation. Never delete,
reset, clean, recreate, or silently substitute an established coordinate.

Both linked worktrees live below the plan's `runtime/` segment deliberately. The outer development
Stop hook excludes runtime state; candidate changes must be verified by the plan's candidate gates,
not mistaken for changes to the outer development checkout.

## 2. Static facts already checked

- `stable-general-harness-runner` is clean and detached at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`.
- The harness repository currently has 34 registered clean worktrees: the retained completed-project
  set plus the V2 candidate and implementation/final lanes created through C0 attempt 0001. The
  earlier runner-migration evidence correctly recorded 29 before the later S3/C0 lanes existed.
  These are protected current or historical state and are never broad cleanup targets.
- `pre-conversion-rollback` is independently recoverable, clean, and detached at `287ea53793e3963062882012ff80c3b0e8c41587`; `frozen-harness-to-use` remains a locked temporary alias.
- The operational runner path is `stable-general-harness-runner`, clean and detached at `4699d27`;
  `harness-in-progress/` is absent. The name remains only in
  `.git/modules/harness-in-progress` and the corresponding local submodule key because every linked
  worktree uses that common store. Do not rename/reinitialize it or treat a leading uninitialized
  marker from outer `git submodule status` as permission to run `submodule update`.
- `.codex/scripts/stable_runner.py` plus
  `plans/general-coding-harness/runtime/firmware-v2/runner-migration/STABLE_RUNNER_LOCK.json` is the only
  implementation-controller entry point. Its completed independent verification covers exact
  checkout identity, hostile CWD/import isolation, output confinement, Windows interpreter DLL
  roots, a deployment-shaped controller/resource-claim cleanup proof, and the ordinary repository
  gate.
- `Firmware/BYO-Firmware-MCP` contains the pinned commit
  `f003f84a7df51cd8595a3203c62e225b21da2a22` and is intentionally dirty. Its 1,209 current status
  entries are preserved input state, not a candidate.
- All 47 destination files in `Firmware/Firmware resources/SOURCE_MANIFEST.csv` exist and match the
  recorded byte count and SHA-256.
- The 47 historical `source_path` locations do not exist in the present dirty checkout or pinned
  Git commit. They are provenance strings, not launch-time file dependencies. An execution agent
  may use a mirrored destination only after rechecking its recorded size and hash; it must not claim
  a live source-to-copy comparison.
- All 13 files named by `ARM_TOOLCHAIN_LOCK.json` and `NCS_V3_3_1_LOCK.json` exist at their recorded
  absolute paths and match the recorded sizes and SHA-256 values.
- The NCS lock's historical `PYTHONPYCACHEPREFIX` points into an old experiment and no longer
  exists. It must never be recreated or reused. Every V2 lane derives a fresh cache path below that
  lane's runtime root while preserving the lock's isolation intent.
- The execution-plan validator passes, and its 36 authoring regression tests pass.
- Installed `codex-cli 0.146.0` exposes the required exec flags. Exact model/tier availability is
  deliberately left to the no-op execution preflight and has not been inferred from the picker.

These are readiness/resume observations. Recheck exact identities, cleanliness, required hashes,
and the next lane's launch contract before dispatch. Do not repeat initial path-absence checks or
recreate either worktree.

The user-directed Fast-tier revision requires a new no-op availability proof for
Luna-high-priority before the next doer/test-executor dispatch. Terra-medium-priority is already a
required reviewer/test-writer launch shape and is now also the coder shape. No model substitution is
permitted.

## 3. Root identity and child-launch gate

Record the current outside root session as `ROOT-IM`, the implementation coordinator. `ROOT-IM` is
not a child launched by this plan, so the subagent model/effort/tier map does not constrain it. Do
not create a nested replacement implementation manager. The separate final-test owner is
`F.C3.O`, a fresh Sol-high-Fast acceptance-orchestrator subagent launched later by `ROOT-IM`.

Each headless child uses the equivalent of:

```text
codex exec
  --dangerously-bypass-approvals-and-sandbox
  --dangerously-bypass-hook-trust
  --ignore-user-config
  --json
  -m EXACT_MODEL_FROM_ROLE_MAP
  -c model_reasoning_effort="EXACT_EFFORT_FROM_ROLE_MAP"
  -c service_tier="priority"
  -C ABSOLUTE_ISOLATED_ROOT_FROM_LANE_MANIFEST
  FIXED_ASSIGNMENT_FROM_LANE_MANIFEST
```

The launcher must remain headless, capture PID plus creation identity, JSONL thread/turn evidence,
exit status, and final message, and use no `--ephemeral` flag for a lane that may resume. A preflight
no-op availability probe may be ephemeral. Every launched child explicitly passes
`service_tier="priority"`; no default-tier child role exists. No launch may depend on user
configuration.

For C3, `ROOT-IM` uses this launch shape only to start `F.C3.O` and `F.C3.W` directly.
`F.C3.O` submits target assignments to `C3-HARNESS`, the candidate harness control plane and exact controller processes;
`C3-HARNESS` performs and records each target-worker launch. A direct target-worker `codex exec` by
`F.C3.O` is a pre-acceptance topology failure because it bypasses the candidate harness.

`--dangerously-bypass-hook-trust` is admitted only because the repository hook sources are under
`ROOT-IM`'s reviewed control and the user authorized unattended full access. It
does not expand hardware authority.

## 4. Explicit MCP boundary with ignored user configuration

Because every child uses `--ignore-user-config`, no lane may depend on a globally registered MCP
server. Before a physical lane starts, its candidate controller configuration must
explicitly declare the clean pinned BYO Firmware MCP command, arguments, environment, working root,
and per-lane `.firm`, artifact, and log roots. The preflight probe must prove that exact declaration
exposes the expected MCP schema while creating only its assigned server process.
Only that controller receives the physical MCP command/environment/stdio endpoint and launch
capability. O and target workers receive no physical registration, credential, or inheritable handle;
they submit structured requests to the candidate harness broker, which forwards only after proposal,
signed decision, authorization, and dispatch admission all validate. Direct-endpoint negative tests
and C4 environment/handle audits are mandatory.

The pinned server's documented stdio command is `uv run --project
plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate --locked
pyocd-debug-mcp`, with the project argument resolved to its absolute path. Its stdout is MCP framing
only. Set `BYO_MCP_ARTIFACT_ROOT` to the lane's isolated artifact/state root so the server places
`.firm/runs` there, run with the lane's assigned target working directory, and capture stderr
separately as the server log. Never use the dirty checkout in that command.

The pinned server also loads `.env` from its working directory or server checkout and honors
inherited `PYOCD_PROBE_UID` and `PYOCD_TARGET`. Therefore the launcher records an effective
environment allowlist, rejects an unreviewed `.env`, and explicitly clears inherited probe/target
overrides for inventory. After stable assignment, a board-owning lane sets `PYOCD_PROBE_UID` only to
its exact assigned UID and uses a reviewed target/profile value; it never inherits either value from
the host. Record names and non-secret hashes/values needed for routing without retaining credentials.

Read-only discovery remains a preflight operation. Setup, connect, flash, reset, debug, UART, BLE,
and RF calls remain blocked until their live MCP plan, permission result, board lease/identity, and
delegated authorization record all agree.

The user is the sole issuer of delegated hardware authority through `goal.md` Section 11 or a later
explicit directive. Preflight records non-authorizing
`plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json`;
C1 attests the exact user scope in canonical
`plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json`,
binding operative goal hash, C1 ID, stable boards, allowed actions, destructive exclusions, RF
constraints, MCP pin, and expiry. Specifically, `ROOT-IM`
mechanically creates the C1 artifact by copying the user-issued scope exactly and adding only derived
lock/identity/pin bindings. That is validation/attestation rather than issuance; `ROOT-IM` cannot
alter or expand scope. Before a physical server launches, the controller also requires a closed
create-once session request for one exact attempt/lane/board/claim and later records the exact Server
Run/process/bootstrap in `SESSION_OPEN.json`. The same process, transport, isolated roots, and claim
remain retained across the finite session. All post-bootstrap `tools/call` operations--including
setup, validation, both plan calls, action, observation, and returning state--use consecutive,
predecessor-bound separately authorized call chains and policy-defined transitions. Normal closure
requires O's signed close intent and completed authorized returning-state calls; the controller alone
drains/exits/reaps/releases and writes terminal closed evidence. Failure/expiry/revocation/abort/loss
writes terminal aborted evidence after bounded cleanup and cannot claim a clean returning state.
Every authorized C3 call also requires a fresh opaque UUID `CALL_ID` and
an immutable three-step handshake. `C3-HARNESS` atomically creates
`hil/{lane-id}/call-proposals/{CALL_ID}.json` with exact C1/delegated path/hash, attempt/lane/logical
board, stable probe UID, reviewed target/profile, current route/null, immutable board-identity/claim-
acquisition paths/hashes, MCP method/version, pinned server revision/schema hash, locked method-policy
path/hash, exact arguments, canonical policy-evaluation object/hash, live plan path/hash, required
positive `max_operation_duration_seconds`, and permission. `F.C3.O` independently atomically creates attempt-evidence
`authorization-decisions/{CALL_ID}.json` with proposal path/hash, matching fields, exact O
process/thread identity, approve/deny/rationale/time/expiry; its O-owned directory is
harness-read-only. Approval alone lets the harness atomically create
`hil/{lane-id}/authorizations/{CALL_ID}.json` binding both prior paths/hashes. All are
create-new/no-overwrite; authorization also copies the same exact call/board/probe/target/route/
identity/claim/method/server/schema/policy/evaluation/argument/plan/duration fields. Before launch ROOT creates nonce/keypair/intent and spawns O with nonce but
no key over the bidirectional inherited pipe. Post-spawn ROOT writes exact identity, sends its hash,
receives O's nonce/hash acknowledgment, writes create-once `topology/ORCHESTRATOR_KEY_RELEASE.json`,
then sends key/discards its copy. Signed ready/work/decision must bind release hash and time >=
release; harness rejects earlier/unbound records. No launch record is rewritten; failure requires a
fresh attempt. O signs
canonical decisions; harness verifies before dispatch and C4 verifies
provenance. The authorization handshake retains three paths and never reuses an ID. Immediately
before MCP submission, `C3-HARNESS` validates every field, recomputes the canonical policy
evaluation, requires actual method/version, server/schema, policy/evaluation hashes and normalized
arguments plus plan/duration and live probe/target/route/identity/claim evidence to equal all three
handshake artifacts, and refuses dispatch
or a success record for missing, expired, mismatched, or out-of-scope evidence; post-dispatch records
cannot authorize a call.
After validation it samples a monotonic clock and creates immutable
`hil/{lane-id}/dispatch-admissions/{CALL_ID}.json`, binding authorization path/hash, fresh five hashes,
all revalidated fields, clock identity, start, and deadline = start + declared duration. Dispatch/
result reference all four paths/hashes; authorization is never rewritten and admission-to-submission
time counts.

The "user-issued scope" is exactly the canonical JSON object in `goal.md` Section 11: its four
fixtures, nine action classes, destructive exclusions, application-only flash, UART/BLE/LoRa numeric
bounds, and explicit/null expiry. C1 records its canonical sorted-key compact UTF-8 JSON SHA-256 and
copies it verbatim. C1 locks default-deny `MCP_METHOD_POLICY.json` with exact method/version,
parameter schema/ranges/safe flags, and prohibited method/parameter/side-effect predicates.
Destructive-capable methods deny unless technically constrained/proven safe for the exact call;
labels cannot override prohibition. Unmapped/ambiguous inputs deny; live evidence only narrows.
Policy sets a method duration maximum; every mutating plan must contain positive integer
`max_operation_duration_seconds` within it or deny. Result validation rediscovers identity/route and
revalidates the exact claim; mismatch forbids success and C4 verifies the retained fields.

At every actual mutating-dispatch boundary the harness independently hashes all five governing docs
and requires exact C1 equality for `goal.md`; only the other four may use a valid editorial terminal.
It binds the live set into dispatch admission and dispatch/result. Mismatch expires pending calls,
refuses dispatch, emits `GOVERNING_INPUT_CHANGED`, and
invokes live-goal handling. A ROOT-owned read-only watcher monitors them during in-flight mutation;
change is revocation and follows `INDETERMINATE_EXPIRED`.
This is a registered non-agent helper with exact identity/current hashes/heartbeat in
`topology/GOVERNING_INPUT_WATCHER.json`, no write authority beyond its evidence, and required
exit/reap in topology shutdown.

Delegated `expires_at_utc` is copied only from an explicit user value and is otherwise `null`; the
record also expires on revocation/scope change, C1 invalidation/replacement, or completion. Each
call is one-shot and expires at the earlier of delegated expiry (if any) and five UTC minutes after
creation, on any bound-field change, or when its attempt exits/aborts. Dispatch requires remaining
validity to cover the live plan maximum plus 60 seconds and validity through result commitment.
Mid-call expiry/revocation causes safe cancellation where supported, `INDETERMINATE_EXPIRED`, raw
evidence/cleanup, no success, and release only after exact exit/reap. A fresh attempt under an
unchanged operative C1 uses new call IDs. Retry gets a new call ID. Only an explicit user
directive may set/extend delegated time, requiring fresh C1.
The harness enforces the admission's monotonic deadline. At maximum it cancels safely and, if still
running, performs exact bounded MCP/controller termination/cleanup. Result records start/deadline/
end/elapsed plus cancellation/termination; an overrun is `INDETERMINATE_TIMEOUT`, never success,
with claims held through exit/reap/cleanup.

C1 uses a non-circular serialization order: allocate a fresh opaque non-content-derived UUID
`C1_LOCK_ID` and its canonical `final/c1/{C1_LOCK_ID}/` directory; create and hash the authorization;
then write sibling `C1_LOCK.json` containing the ID, canonical authorization path/hash, and every
other locked-input hash. Compute its hash last into sibling `C1_LOCK.sha256` and never feed it into
authorization. Every replacement uses a new UUID/directory; consumers use only operative paths/hashes.

The one-active-target-agent cap does not prohibit physical concurrency. P3 uses one `F.C3.P1`
assignment to request two non-agent process groups, `P3.STM` and `P3.NRF`. Only `C3-HARNESS` creates,
starts, stops, and reaps them and owns their distinct lane/controller/process/claim/event/cleanup
records; each owns separate MCP, `.firm`, artifact, and log roots. `F.C3.P1` operates them only
through its assigned harness interfaces and cannot spawn them. No second target Codex agent is
launched.

The fault boundary admits ordinary coordinator/orchestrator/worker mistakes as recoverable test
work. A bad assignment, command, ordering choice, target edit, invalid call, or result envelope is
returned to its owner and selectively retried; it is not `ABORT_REQUIRED` and does not reset the
candidate, implementation steps, C1, or unaffected green tests. The watcher escalates only an exact,
reproducible candidate/watcher invariant violation in how that work was handled. If immutable C3
evidence forces a new attempt after an orchestrator mistake, only the attempt namespace rolls over
unless a C1-locked input changed.

Before target work, `F.C3.W` must publish readiness and begin heartbeats at least every 30 seconds,
binding exact process identity, monotonic sequence, timestamp, and observation cursor. `ROOT-IM`
monitors both process and evidence. Unexpected exit, lost observation access, cursor stall while logs
advance, or a gap over 90 seconds before the post-candidate-shutdown, pre-manifest terminal watcher report is fail-closed
`WATCHER_LOST`: stop new assignments, terminate only the registered topology, preserve the attempt,
and follow the `ABORT_REQUIRED` repair/relock classification before a fresh attempt.
Termination first requests controller-managed shutdown. Only if the exact registered controller is
unavailable/unresponsive may ROOT host-terminate/reap its pre-registered controller/MCP/process-group
identities, with create-once `topology/EMERGENCY_TERMINATION.json` request/failure/identity/outcome
evidence. No MCP/hardware/broad-kill authority is granted; board state is indeterminate, the attempt
fails, and fresh P0 returning-state recovery precedes mutation.
Normal P4 ordering is candidate-managed shutdown, W final heartbeat/report, exact W exit/reap, then
O manifest closure. W never heartbeats after the manifest checkpoint.
ROOT writes immutable reserved `topology/WATCHER_LAUNCH.json` after spawn/before readiness with exact
command/flags/root/model/effort/tier/thread/PID-plus-creation/start, and writes
`topology/WATCHER_EXIT.json` after report/exit/reap/before manifest with launch hash, reaped identity,
exit/time, report hash, and final-message content/hash. W never authors these; topology shutdown
inventories them, and missing/mismatch blocks C57/P4.
Watcher "read-only" prohibits source, candidate/target-state, and hardware mutation but permits only
its own attempt-local watcher evidence and create-once `watcher/ABORT_REQUIRED.json`. W creates that
record atomically by same-directory temporary write plus create-new/no-overwrite rename; it contains
schema version, attempt, exact watcher identity, heartbeat/cursor, invariant, correlated identities,
evidence paths, earliest invalidated sprint, and UTC time. `ROOT-IM` monitors it directly from ready
through terminal report. This path is the sole exception to manager-owned signal-channel writes.

ROOT separately monitors O's exact process and `topology/ORCHESTRATOR_HEARTBEATS.jsonl` at the same
30/90-second cadence through result commitment and normal exit. Manifest creation starts an absolute
90-second result deadline. Unexpected O exit, lost/stale heartbeat, deadline without valid result,
or exit without result is `ORCHESTRATOR_LOST`: stop/reap registered topology, preserve the partial
attempt, write `topology/ORCHESTRATOR_LOST.json`, classify like `WATCHER_LOST`, and use a fresh
attempt. Partial manifest/result files are never completed or reused.
After valid result and normal O exit/reap, ROOT writes immutable
`topology/ORCHESTRATOR_EXIT.json` with identity/key-release/result hashes, reaped identity,
exit/time, and final-message content/hash. `ORCHESTRATOR_LOST.json` retains available fields on
abnormal loss and never claims normal exit. Topology shutdown inventories the applicable record.

### Review/test finding gate readiness

All project-created reviewer, test-writer, and test-executor coding invocations must enable the
candidate's opt-in finding gate and bind a lane-local `orchestrator-review-findings/v1` artifact.
The gate accepts submitted gaps only as `CODEBASE_BREAKING`, `FUNCTIONALITY_BREAKING`, or
`WORTH_FIXING`, with exact evidence and an explicit comparison of problem impact/no-fix consequence
against the smallest fix's complexity, regression risk, verification cost, and alternatives. PASS
cannot carry findings; malformed, stale, cross-lane, unsupported, preference-only, or speculative
submissions invalidate the lane result. The gate validates structure; `ROOT-IM` or `F.C3.O`
independently accepts or rejects the claimed tradeoff. Rejected findings cause no product mutation,
checkpoint reset, C1 invalidation, or green-test rerun.

A production-relevant blocking finding must identify a supported or credibly reachable deployment trigger and a
concrete negative consequence for correctness, safety, security, reliability, recovery, required
evidence integrity, or required user-visible behavior. Realistically triggerable latent
authorization, identity, cleanup, and fail-closed defects remain blocking. Cosmetic, unreachable,
behavior-neutral, purely theoretical, and speculative-hardening suggestions are non-findings.

Reviewers finish the entire assigned affected-surface and critical-control-path sweep even after a
valid finding and submit one complete finding set for the exact tip unless an external blocker prevents
continued inspection. `ROOT-IM` batches all accepted findings into one serial repair before another
product review. No review, C0, aggregate dependency-map reconciliation, registry reconciliation, or
C1 lock is created for an intermediate batch revision.

## 5. Known live gates, not planning gaps

The executable session/policy/limitation contract is closed by
`plans/general-coding-harness/evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json`
(SHA-256 `9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`). The later independent
pre-C3 audit found missing candidate-owned target-worker execution. The preserved production lane at
`e5ced272` implements that control-plane facade and the accepted provenance repair, but has only
author-side static checks. It is not green and is not joined to candidate `659dd03`.

After explicit user resume and governing-diff classification, readiness requires the test-author
lane to join `e5ced272`, adapt CP04 for complete OS-snapshot provenance, and form one frozen joined
tip. Run the shortest selected CP04/control-plane smoke ID first. If green, obtain a fresh complete
read-only review and run the remaining dependency-invalidated selected IDs in parallel on that same
tip. Join both results; batch every accepted production finding before another product review; then
reconcile the dependency map, registry, and aggregate evidence once for the accepted tip. Only a
clean terminal C0 plus joined green affected tests may create a fresh C1. C3 and hardware remain
locked throughout.

- The retained DIO2 notation `P.05` is genuinely ambiguous. No current immutable record resolves it.
  It is not guessed during readiness. A DIO2-dependent build or hardware action remains blocked
  until authoritative live electronic/setup evidence resolves the exact GPIO. If the accepted radio
  design does not consume DIO2, record that non-dependency; otherwise the required radio gate cannot
  pass.
- The retained fixture summary does not itself prove the exact CoreSX1262 module band variant,
  supply/current limits, or currently applicable RF constraints. RF transmission remains blocked
  until authoritative fixture/setup evidence confirms that both attached modules, antennas, power,
  configured 915 MHz operation, transmit power, bandwidth, and bounded duty cycle are compatible
  and permitted. User authorization is necessary but does not substitute for that technical and
  regulatory admission evidence.
- Model availability, live board presence, current COM routes, MCP discovery, and permissions are
  intentionally proven only in execution preflight. Failure stops before S1 or before the affected
  physical action and is never bypassed or repaired by guessed identity. A separately proven defect
  or incompatibility in the immutable pinned server may use only the plan's evidence-gated
  `AUTHORIZED_SERVER_LIMITATION` route and strongest-available partial/unit substitute; it never
  turns an unknown environment or hardware absence into a pass.
- The copied toolchain locks grant no flash or HIL authority. The live goal plus exact MCP plan and
  permission flow provide the narrowly delegated authority.

## 6. Candidate verification and promotion boundary

The outer command `.codex/scripts/verify.py` currently targets the checkout at
`stable-general-harness-runner`. It must never be cited as verification of code that exists only in the
reserved candidate worktree.

Before S1 product changes, preflight records the baseline test manifest, candidate-root gate
protocol, and focused commands. S3 materializes and tests the exact candidate-root safeguard
launcher. That gate covers Ruff, formatting policy, BasedPyright with the existing finding baseline
mapped to the candidate paths without expansion, compilation, all
orchestrator/watcher/original-compatibility tests, Codex integration, attention retention, and
accumulated firmware/MCP tests. After C4 it runs as one logical `SAFEGUARD_RUN_ID` for the exact C1
lock, under the admission/resume rule below.

C1 later locks the operative goal/spec/roadmap/plan/readiness hashes, candidate revision, server
pin/configuration, acceptance-kit and lane/MCP launch templates, fixture bindings, the target seed,
test/evidence contracts, authorization, the implementation `runtime/firmware-v2/passed-tests.json`,
and other implementation inputs used by C2/C3. C3 never writes that locked registry. The seed is
exactly `TARGET_SEED_MANIFEST.json` plus its four enumerated/hash-bound files:
`TARGET_CHARTER.md`, `PINNED_INPUTS.json`, `TEST_CONTRACT.json`, and `EVIDENCE_SCHEMA.json`. Target
source and target-repository-local configuration created later through `C3-HARNESS` are excluded and
versioned in the target dependency fingerprint. Any C2 repair that changes one of those locked
inputs invalidates C1 and requires a new C1 Checkpoint A plus dependency-invalidated C2 tests before
C3. Production, policy, expected-behavior, coverage-obligation, or other operative changes require
the owning step and full fresh C0. A qualifying strict test-only fast-lane correction instead records
its deterministic eligibility checklist and reruns exactly its known failed IDs once in the same
test-author continuation before the new C1; it has no C0, ordinary review, or reconciliation. The pinned-server source is immutable in this project. A proven C3 server
defect/incompatibility uses `AUTHORIZED_SERVER_LIMITATION` and substitute evidence without a pin
change; an external pin/source change instead requires explicit replanning and invalidates all
dependent locks and credits.

Every post-C1 `goal.md` hash change invalidates C1 and pending/in-flight hardware authority; it can
never use editorial supersession. Only a byte-only change to one of the other four docs may use the
C1-rooted chain after fresh independent Terra review plus ROOT no-impact decision. C4/safeguard/
authorization accept those four terminals only; semantic/broken chains invalidate.
P4 manifest creation freezes every external-reference path/hash through completion. Any later doc
change or editorial-chain append invalidates the C3 result and requires a fresh C3 before C4;
C4/safeguard reject stale results and never accept an earlier chain prefix. Goal or semantic changes
still use the fresh-lock route.

Every C3 attempt receives the next monotonically increasing matching runtime/evidence
`acceptance/attempt-NNNN/` pair--one greater than the largest number on either side, or `0001` only
when neither exists--and separate `target/`, `hil/`, `events/`, `claims/`, `manager-signals/`, and
`.agent-workspace/` roots plus fresh attempt-local `passed-tests.json`. Prior attempt pairs are retained read-only and are never cleared,
overwritten, gap-filled, or reused. Both chosen paths must be absent; a one-sided path or collision
stops allocation for preservation/triage. A harness/watcher source or locked-config repair after
`ABORT_REQUIRED` also returns through its owning step and fresh C0/C1/C2 before a new attempt; only a
proven environment-only correction may skip re-locking.
The attempt registry is inside P4's manifest domain. It may re-credit a prior green result only by
immutable evidence path/hash and unchanged dependency fingerprint, never by copying/mutating prior
registry state.

Before the one logical safeguard run, an environment-admission gate executes no safeguard source
check or test and may be repaired/repeated. Once `SAFEGUARD_RUN_ID` exists, an environment-only
interruption resumes that same ID and only incomplete/dependency-invalidated components. A locked-
input change requires a new C1 lock and new run ID.

After candidate-managed shutdown and W report/exit/reap, ROOT writes `WATCHER_EXIT.json`; then at a quiescent checkpoint O inventories every regular
file under both attempt roots, including adverse evidence, except exactly the manifest itself,
not-yet-created result, and reserved `topology/`; symlink/reparse/unresolved-temp entries and later
in-domain writes are forbidden. C1/delegated/editorial files outside those roots appear only as
canonical `external_references` path/hashes verified directly by C4. O creates the result within 90 seconds. C4 independently enumerates
both roots and rejects unknown/unlisted/mismatched files. After O exit, ROOT writes
`ORCHESTRATOR_EXIT.json` and closes/hashes reserved
launch/liveness/shutdown evidence in `topology/TOPOLOGY_SHUTDOWN.json`; C4 verifies that inventory
separately and pre-exit evidence does not claim those exits.
The shutdown file inventories/hashes every other regular topology file but excludes itself;
symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and
separately hashes/verifies shutdown.
Any C4 evidence-only correction is limited to a C4-owned annotation outside attempt roots and cannot
satisfy/alter/replace acceptance evidence; any closed-attempt evidence defect requires fresh C3.

Only after that candidate safeguard is green may promotion create `progress/v1.2` at the exact
candidate commit and stage the explicitly named stable runner on that distinct branch for the required outer
verification. `progress/v1.1` and commit `4699d27` remain intact. Do not push or publish externally
unless the live user directive explicitly authorizes it. If outer verification fails, promotion is
not complete and the failure routes to targeted repair on a new candidate revision.

After promotion evidence is durable, remove the two temporary linked worktrees only through exact
Git worktree operations and only after proving each is clean, all commits/pins are retained, and no
registered process uses either path. Never recursively delete a worktree path. Preserve the
execution runtime/evidence and create the distinct fresh inactive runtime at
`plans/general-coding-harness/runtime/promoted-firmware-v2/`.

## 7. Resume decision

Execution remains paused until the user explicitly resumes. Resume is safe only when this file,
`goal.md`, the spec, roadmap, plan, `HANDOFF.md`, and `PARALLEL_CHECKPOINT.md` agree; the stable
runner and rollback identities are exact; candidate `659dd03`, MCP fixture `f003f84`, product lane
`e5ced272`, and test-author lane `b2949d4` are clean at their recorded tips; and no managed
worker/claim is live.

On explicit resume, first inspect the governing-document diff and record that this optimization
changes execution sequencing/finding admissibility but not the product, hardware authority,
immutable server, or accepted `e5ced272` repair contract. Then cherry-pick `e5ced272` into the
preserved test-author lane, resume that same test-writer only to adapt CP04, form the frozen joined
tip, run its shortest selected smoke ID, and if green run fresh complete read-only review in parallel
with the remaining selected Luna-high-Fast execution. Non-product envelope/metadata corrections resume
their owning lane; qualifying strict test-only corrections record their deterministic eligibility
checklist and rerun exactly the known failed IDs once before unrelated work, without C0, ordinary
review, or reconciliation. Expected-behavior, coverage-obligation,
operative-contract, production, or policy changes remain material. Reconcile
the dependency map, registry, and join evidence once after the batch is accepted. Do not begin C1,
C2, C3, a safeguard, MCP, or hardware work before the optimized prerequisites are green.

<!-- END SNAPSHOT active_docs/EXECUTION_READINESS_2.md -->
### Snapshot: `plans/general-coding-harness/EXECUTION_PLAN_2.md`

<!-- BEGIN SNAPSHOT plans/general-coding-harness/EXECUTION_PLAN_2.md -->
# EXECUTION_PLAN_2: Backward-Compatible Physical Firmware Acceptance

## 0. Metadata

- **Goal:** implement `GENERALIZATION_SPEC_2`, retain the accepted coding and legacy firmware paths, and certify the candidate with a separately orchestrated MCP-backed four-board firmware project.
- **Plan inputs:** `HANDOFF.md`; `active_docs/GENERALIZATION_SPEC_2.md`; `active_docs/IMPLEMENTATION_ROADMAP_2.md`; `active_docs/EXECUTION_READINESS_2.md`; `Firmware/Firmware resources/test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`; `Firmware/Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md`; `Firmware/Firmware resources/SOURCE_MANIFEST.csv`; the pinned BYO Firmware MCP source; current harness docs, source, and tests.
- **Authoritative implementation runner:** clean detached `stable-general-harness-runner` at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`.
- **Protected rollback:** independently recoverable detached `pre-conversion-rollback` at `287ea53793e3963062882012ff80c3b0e8c41587`; `frozen-harness-to-use` is a temporary locked alias.
- **Protected historical worktrees:** the 13 retained linked harness worktrees from the completed
  plan are recorded inputs, never V2 lanes or cleanup targets.
- **Firmware MCP baseline:** clean worktree to be materialized from `f003f84a7df51cd8595a3203c62e225b21da2a22`; the present dirty checkout is never reset or used as the release candidate.
- **Fresh runtime root:** `plans/general-coding-harness/runtime/firmware-v2/`.
- **Fresh evidence root:** `plans/general-coding-harness/evidence/firmware-v2/`.
- **C3 attempt roots:** matching monotonically increasing immutable runtime/evidence
  `acceptance/attempt-NNNN/` pairs beginning at `attempt-0001`; allocate one greater than the
  largest number on either side and never reuse or gap-fill an attempt number.
- **Fresh promoted runtime:** `plans/general-coding-harness/runtime/promoted-firmware-v2/`, absent
  until every promotion gate passes.
- **Harness mode:** candidate-harness-manager-owned orchestration; `evaluator_enabled: false`; deterministic watcher plus explicitly isolated AI acceptance watcher.
- **Current Portable Harness binding:** manager begins with `scan --no-write`, consumes native events through `watch --until-actionable`, clears only exact top-level events through `ack --event-id`, stores coordination state below `.agent-workspace`, records joins in `PARALLEL_CHECKPOINT.md`, requires terminal `RESULT.json`, and uses `manager-signals` only as the manager-owned repair channel. The one explicit non-manager exception is the isolated watcher's create-once attempt-evidence path `watcher/ABORT_REQUIRED.json`, monitored directly by `ROOT-IM`; it is never written or relayed through `manager-signals`.
- **Planning boundary:** this document specifies execution. It does not itself launch agents, edit product code, start the harness, run tests, or operate hardware.
- **Runner transition:** complete and frozen. The former physical `harness-in-progress/` path is
  absent. `.git/modules/harness-in-progress` and its local submodule key remain historical shared
  Git metadata for the registered linked worktrees and are never an operational launch root or a
  mid-execution rename target.
- **Pinned launcher:** every implementation controller enters through
  `.codex/scripts/stable_runner.py` and the exact
  `plans/general-coding-harness/runtime/firmware-v2/runner-migration/STABLE_RUNNER_LOCK.json`. The
  launcher proves path/commit/clean/detached state,
  rejects candidate/lane import contamination and protected outputs, and retains only trusted
  interpreter roots. No lane invokes the controller package directly from its working directory.
- **Stable/candidate gate caveat:** `4699d27` predates the executable finding gate. Projection may
  remove candidate-only fields; `ROOT-IM` independently validates the original current-tip finding,
  result, and triage artifacts. Candidate C2/C3/safeguard testing proves automatic candidate gate
  enforcement.
  - **Current execution point:** execution is user-paused for this layout optimization. Preflight and
    S1-S3 are green; candidate `659dd03` retains 140 green IDs. Superseded C1/C2 remain preserved.
    The bounded C3 control-plane repair exists only on clean product lane `e5ced272`, where it has
    author-side static checks but no independent current-tip review, adapted CP04 coverage, runtime
    execution, dependency reconciliation, or candidate join. On explicit resume, first classify the
    governing diff, join `e5ced272` into the preserved test-author lane, adapt CP04, and form one
    frozen tip. Run the shortest affected smoke ID, then run one complete fresh read-only review and
    the remaining selected focused IDs in parallel. Batch any accepted production findings before
    another review and reconcile dependency/registry/join evidence once for the accepted batch tip.
    Only then run a fresh terminal C0, C1, and dependency-invalidated C2. The pinned server remains
    immutable and unlaunched, and C3/hardware stay locked.
- Gaps / surfaced issues: none

The required `none` value above refers to unresolved planning/specification ambiguity. The accepted
C0 product finding and its bounded S2 repair/review status are execution state recorded immediately
above and in `PARALLEL_CHECKPOINT.md`; they are not an unplanned scope or topology gap.

The earlier general-coding execution plan is complete and is not restarted. This bounded
firmware-compatibility release has begun and resumes only from its current checkpoint.

## 1. Agent-per-role mapping

All child agents are launched headlessly with `codex exec` in Fast mode. Fast means the ordinary model slug plus explicit `service_tier="priority"`; it is not a `-fast` model name. Every child launch uses the required full-access/no-approval controls, `--ignore-user-config`, an isolated working root, and captured thread/process/exit evidence. No launched role may omit the priority tier or substitute a different model.

The current outside root is `ROOT-IM`, the host implementation coordinator. It is not a launched
subagent and is outside the model/effort/tier assignment contract. Every child explicitly uses `--dangerously-bypass-approvals-and-sandbox`,
`--dangerously-bypass-hook-trust`, `--ignore-user-config`, `--json`, exact model/effort/tier flags,
and `-C` bound to its assigned root. Resumable lanes are not ephemeral. Processes authorized to own
an MCP server receive an explicit isolated declaration because ignored user configuration cannot
supply one; in C3 that is only the candidate physical-lane controller, never O/target workers.

| Role | Agent/model | Pool size | Reasoning | Tier | Responsibilities |
|---|---|---:|---|---|---|
| Orchestrator / planner-executor | Current `ROOT-IM` host session | 1 | not assigned | not assigned | Outside implementation coordinator; partitions work, owns integration, triage, repair routing, checkpoints, and final promotion; not a launched subagent. |
| Coder-main | GPT-5.6 Terra | 1 | medium | Fast / priority | Serial product coder for harness, MCP, acceptance-medium, or target source; never more than one active coding owner. |
| Reviewer-main | GPT-5.6 Terra | 2 | medium | Fast / priority | Independent static reviewers and test writers; two lanes only where file and question ownership are disjoint. |
| Doer-main | GPT-5.6 Luna | 2 | high | Fast / priority | Independent test executors/doers; two lanes only for isolated test shards or resources. |
| Final-reviewer | GPT-5.6 Terra | 1 | medium | Fast / priority | Fresh read-only final review; no step history or implementation ownership. |
| Acceptance-orchestrator | GPT-5.6 Sol | 1 | high | Fast / priority | Fresh `F.C3.O` subagent; runs the candidate harness and alone orchestrates the final target project. |
| Acceptance-watcher | GPT-5.6 Terra | 1 | medium | Fast / priority | Fresh `F.C3.W` read-only watcher; emits exact abort evidence for harness/watcher defects. |

`Orchestrator / planner-executor` is the validator-required row name for `ROOT-IM`; it does not make
`ROOT-IM` a launched Sol child. Role interpretation is strict: source edits are coder work; test
design/writing and review are reviewer-main work; test execution and hardware operation are
doer-main work. `ROOT-IM` coordinates creation of the product with those subagents. `ROOT-IM` is
never `F.C3.O` and never assigns final target-project work. `F.C3.O` is a separately launched
subagent and the sole target-project decision-maker.

`C3-HARNESS` denotes the candidate harness control plane and its exact controller processes operated
by `F.C3.O`; it is the system under test, not a Codex-agent role and not an agent slot. `F.C3.O` submits every target assignment
to `C3-HARNESS`. Only `C3-HARNESS` launches the assigned target worker through `codex exec`, owns its
lifecycle, and records its exact launch/result/event/claim evidence. `F.C3.O` must not directly
launch a target worker. Gates and evidence use `ROOT-IM`, `F.C3.O`, `F.C3.W`, or `C3-HARNESS`
instead of an ambiguous unqualified "orchestrator" or "manager."

The validator-required final-phase lane ID `F.C3.M` is an alias for `ROOT-IM`. It never denotes a
new process, nested manager, launched subagent, or additional agent slot. Every occurrence of
`F.C3.M` in Section 7 therefore has exactly the same identity and authority as `ROOT-IM`.

The headless launch preflight must prove Sol-high-priority, Terra-medium-priority, and Luna-high-priority. A launch failure blocks preflight; it does not authorize the earlier Sol-for-Luna substitution.

## 2. Coverage checklist

| ID | Atomic completion requirement |
|---|---|
| C1 | Start from exact clean harness commit `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`. |
| C2 | Preserve frozen rollback `287ea53793e3963062882012ff80c3b0e8c41587`, prior runtimes, and unrelated outer changes. |
| C3 | Use a new isolated harness candidate branch/worktree without rewriting `4699d27`. |
| C4 | Create a clean isolated MCP worktree from `f003f84a7df51cd8595a3203c62e225b21da2a22`; do not alter the dirty source checkout. |
| C5 | Validate all 47 resource-mirror byte counts and SHA-256 hashes. |
| C6 | Do not mutate hardware before live authorization and plan evidence. |
| C7 | Retain exact harness, server, toolchain, pack, datasheet, fixture, and target hashes. |
| C8 | Isolate runtime, MCP state, artifact, and log roots per run and lane. |
| C9 | Preserve schema-less firmware invocation as the legacy dispatch route. |
| C10 | Preserve canonical policy bytes, digest, headings, embedded text, and final reminder checks. |
| C11 | Preserve legacy label-derived outputs and firmware event-log naming. |
| C12 | Preserve accepted legacy model, lease, board, MCP, snapshot, prompt, output, and resume fields. |
| C13 | Keep coding invocation V1 and its repository/result safety unchanged. |
| C14 | Reject ambiguous cross-route input and result shapes. |
| C15 | Run retained legacy fixtures, examples, and configurations without edits. |
| C16 | Require no migration, evidence rewrite, or new public firmware schema. |
| C17 | Limit shared normalization to behavior-preserving duplicate lifecycle logic. |
| C18 | Prove coding and firmware lanes coexist through dual-route automated tests. |
| C19 | Correlate worker/controller/helper/descendant identity by PID, creation evidence, and owner. |
| C20 | Correlate current MCP launcher/server/provider lifetimes exactly to the lane. |
| C21 | Bind hardware relay to exact request, arguments, lane, snapshot, decision, and expiry. |
| C22 | Keep invalid/expired/changed/unbound relays visible but non-authorizing. |
| C23 | Preserve firmware checkpoint/resume thread and path identity without invented liveness. |
| C24 | Emit native lifecycle events and clear only exact top-level acknowledgements. |
| C25 | Distinguish current operational leases from historical board declarations. |
| C26 | Give generic and hardware claims exact ownership and fail-closed stale handling. |
| C27 | Permit independent boards to progress without shared-state contamination. |
| C28 | Serialize same-board and same-resource work without double ownership. |
| C29 | Release claims/resources only after exact child/MCP exit and reap. |
| C30 | Treat unknown, partial, corrupt, or ambiguous lifecycle evidence as actionable and fail closed. |
| C31 | Broker every physical operation through the candidate controller to BYO Firmware MCP; O/target workers never hold the physical endpoint or launch capability. Retain one exact controller-owned server process/claim per finite board session while separately authorizing and chaining every post-bootstrap MCP tool call. |
| C32 | Pin the MCP revision as an immutable compatibility fixture. No project role may edit or repin it; proven defects/incompatibilities use evidence-gated `AUTHORIZED_SERVER_LIMITATION` substitution. |
| C33 | Give each physical lane controller a distinct MCP process/endpoint, `.firm`, artifact, and log root, with no endpoint inheritance by O/target workers; bind session request/open/close-or-abort evidence to its exact Server Run/process/claim. |
| C34 | Bind and rediscover all four stable board/probe identities. |
| C35 | Treat COM ports as live routes rather than board identities. |
| C36 | Match authoritative STM32 I2C2, UART, ground, and pull-up fixture bindings. |
| C37 | Resolve `P.05` authoritatively before dependent CoreSX1262 actions; never guess. |
| C38 | Match datasheet, device-pack, and compiler hashes/locks. |
| C39 | Lock canonical scope/policy; every mutation binds governing hashes, exact call/identity fields, bounded duration, signed decision, authorization, immutable pre-dispatch admission, dispatch, and result; enforce monotonic deadline/expiry fail-closed. |
| C40 | Exclude bootloader replacement, unlock, mass erase, and protection changes. |
| C41 | Constrain LoRa frequency intent, power, packet length, and duty cycle. |
| C42 | Use electronic/software physical oracles only. |
| C43 | Create each fresh disposable Four-Board Dual-Family Firmware Lab repository in the next immutable attempt namespace from exactly the five C1-locked seed files (or, on restart, that seed plus the exact accepted target source-tree commit). |
| C44 | Implement deterministic STM-A controller and STM-B responder images. |
| C45 | Prove STM32 I2C, UART, reset/reconnect, debug, recovery, and sustained traffic. |
| C46 | Prove deterministic two-board nRF52 BLE GATT exchange. |
| C47 | Prove deterministic CoreSX1262 ping/pong and radio telemetry. |
| C48 | Under one active `F.C3.P1` assignment, pass STM32 I2C and nRF52 LoRa concurrently in two non-agent physical lane process groups created, started, stopped, reaped, and owned only by `C3-HARNESS` on all four boards. |
| C49 | Retain build provenance and MCP-mediated setup/flash/reset/debug/memory/UART evidence. |
| C50 | Use behavioral oracles, not flash success, as the application gate. |
| C51 | Inject one predeclared intentional, source-controlled, non-destructive target-code defect with a recorded expected behavioral failure; diagnose, repair, and selectively retest it through the normal target path. |
| C52 | Checkpoint and resume one physical lane with the same thread/path identity. |
| C53 | Prove independent concurrency and same-resource contention with distinct lane/controller/process/claim/event/MCP roots while preserving the one-target-agent cap. |
| C54 | Close boards/candidate state; obtain W's terminal report and exact exit/reap before O closes the two attempt-root inventories, list C1/delegated/editorial artifacts only as directly verified external references, then separately close/hash ROOT's remaining O/topology inventory. |
| C55 | Use fresh Sol-high-Fast subagent `F.C3.O`, never `ROOT-IM`, for practical-acceptance decisions; require `C3-HARNESS` to launch and own every target worker. |
| C56 | Keep `ROOT-IM` as implementation supervisor, never target-task orchestrator. |
| C57 | Use a separate isolated read-only Terra-medium-Fast watcher with ready, heartbeat, observation-cursor, terminal-report evidence plus ROOT-owned immutable exact launch/final-message/pre-manifest exit/reap topology records. |
| C58 | Handle exact watcher abort/loss and O liveness/result-commit loss fail-closed: terminate registered identities, preserve the attempt, classify repair/relock needs, and use a fresh attempt. |
| C59 | Use `ABORT_REQUIRED` for harness/watcher defects; keep target application/compiler/test/target-repository-configuration/invalid-call defects inside the target project only when no C1-locked input changes; treat a proven immutable pinned-server defect/incompatibility as `AUTHORIZED_SERVER_LIMITATION`, require exact attribution and the strongest available partial/unit substitute, disclose the physically uncertified portion, and never repair or repin the server. |
| C60 | Use exact requested headless models, effort, tiers, and launch owner with no substitution: `ROOT-IM` launches `F.C3.O`/`F.C3.W`, while `C3-HARNESS` launches target workers and `F.C3.O` never does so directly. |
| C61 | Keep production coding singleton/serial and all genuine role fan-out within 1-3. |
| C62 | Give each large step exactly two QA loops; do not cycle per module. |
| C63 | Preserve green tests through a C1-frozen implementation registry and manifest-covered per-attempt C3 registry; rerun only dependency-invalidated IDs. |
| C64 | Complete one terminal green logical `SAFEGUARD_RUN_ID` after practical success/audit; pre-admission is outside the run, environment-only interruption resumes it selectively, and a locked-input change requires a new lock/run ID. |
| C65 | Gate on applicable H00/H01/H02/H05, S10-S13, A21/A23/A24, and representative D30-D36 intent. |
| C66 | Keep exhaustive apps, Q40 corpus, Q41 soaks, and destructive/try-last cases non-gating. |
| C67 | Bind evidence to exact revisions, identities, tests, artifacts, authorization, and hardware observations. |
| C68 | Obtain a fresh final reviewer decision after a complete frozen-tip sweep, with no unresolved production-relevant in-scope gap and no intentional first-finding stop. |
| C69 | Audit requirements, topology, watcher boundary, evidence, and protected state. |
| C70 | Promote only the locked green candidate into a fresh inactive runtime while preserving rollback. |
| C71 | Teach legacy firmware, coding V1, dual path, events, ack, resume, and cleanup accurately. |
| C72 | Add no unnecessary framework, scheduler, abstraction, board expansion, UI, database, endurance gate, cosmetic repair, behavior-neutral cleanup, or speculative fix without a concrete negative deployment consequence. |
| C73 | Prove through a protected baseline-to-candidate unit matrix that the original successful general harness still works, with all invalidated original and new cross-route unit tests green and no weakened coverage. |

## 3. Decomposition and disposition

Atomic changes and individual modules are not execution steps. Preflight gates (no full cycle) establish provenance, authority, model availability, and clean roots. The implementation then uses the smallest three large steps that each produce a coherent feature or deliverable. Included modules remain bundled because their contracts fail or pass together; the table explains why one full QA cycle, implemented as exactly two back-to-back loops, is warranted for each bundle.

| Input area | Disposition | Assigned large step | Included modules | Coherent feature or deliverable | Why one full QA cycle |
|---|---|---|---|---|---|
| Promoted general-coding path and safety | Reused as-is | S1 and regression gates | coding V1 parser, repository identity, result safety, generic claims, events, protected original unit-test manifest | Protected compatibility baseline | Its baseline-to-candidate unit matrix is a mandatory non-regression oracle; it is not independently rebuilt. |
| Legacy schema-less firmware loader | Reused with minor adjustment | S1 …19713 tokens truncated…t, deterministic join, and failure route.
7. Test-id scheme: `S1-COMP-*`, `S1-LIFE-*`, `S2-MCP-*`, `S2-KIT-*`, `S3-DUAL-*`, `F-P0-*` through `F-P4-*`, plus retained upstream IDs. IDs never change merely because a run is repeated.
8. The applicable phase registry stores ID, dependency fingerprint, exact revisions/config/hardware identity, result, and evidence. C1 freezes the implementation registry; C3 writes only its manifest-covered attempt registry and references prior evidence immutably. Targeted stable test IDs rerun only after failure or dependency invalidation.
9. Pass criteria require all assigned IDs green, joined evidence complete, current-tip result and required finding artifact valid, no unresolved accepted in-scope finding, and exact clean process/resource/event state.
10. There is no iteration cap. Continue repair and selective verification while meaningful in-scope progress is possible.
11. Escalate a repeated same-signature failure after `stall_threshold` consecutive cycles with the same cause and no new evidence.
12. Escalate oscillation when two or more fixes alternate the same observable failure state without net progress.
13. Reject only-extraneous scope churn: unrelated refactors, frameworks, extra boards, exhaustive catalog work, UI, databases, endurance expansion, style-only review suggestions, and fixes whose complexity/regression/verification cost outweighs demonstrated benefit go to the ledger.
14. An unrecoverable error means exact evidence proves progress cannot continue within existing authority or available fixture state; difficulty, elapsed time, or a target defect is not unrecoverable.
15. `scope_policy` admits only requirements and defects necessary for backward-compatible firmware operation, MCP-backed acceptance, or preserved coding behavior. Everything else is deferred.
16. `gap_scope` is `change`: review and repair the planned change plus directly implicated pre-existing behavior, not every unrelated failing concern in the repository.
17. Hardware authority is explicit and narrow. Direct pyOCD/serial bypass, guessed wiring, operator touch, illegal RF behavior, and destructive recovery are prohibited.
18. `F.C3.O` decides target work and submits assignments; `C3-HARNESS` alone launches/owns target workers; `F.C3.M` (which is exactly `ROOT-IM`, not another agent) supervises implementation and exact termination/repair only. Confusing any of these roles invalidates C3.
19. `F.C3.W` is read-only. Its abort signal is actionable evidence; exact termination remains with `ROOT-IM` so no watcher obtains broad kill authority.
20. Candidate deterministic watch remains diagnostic (`evaluator_enabled: false`); the AI watcher is separately launched and separately evidenced.
21. Hardware/application/MCP target failures and ordinary coordinator/orchestrator/worker mistakes are repaired within their owning project/lane with selective retest; candidate/watcher defects alone use `ABORT_REQUIRED` and reopen implementation. Attempt rollover for immutable-evidence integrity is not a candidate or C1 reset.
22. `final_full_verification` is true, but the full accumulated suite runs only at the safeguard after physical success and C4.
23. The original successful general-harness unit suite is protected: map shared code to baseline IDs, run every invalidated unit, add cross-route isolation units, and forbid green-by-deletion, skip, expected failure, or weakened assertion. C0 and C4 must audit this evidence explicitly.
24. Reviewers complete the assigned affected-surface sweep and report one complete exact-tip finding
    set. They do not intentionally stop after the first defect. `ROOT-IM` repairs accepted findings
    as one bounded batch and never reviews or reconciles an intermediate batch commit.
25. A blocking finding proves a supported or credibly reachable deployed trigger plus a concrete
    negative product consequence. Cosmetic, unreachable, behavior-neutral, theoretical, and
    speculative-hardening suggestions are non-findings; realistically triggerable latent safety,
    authorization, identity, cleanup, and fail-closed defects remain blocking.
26. Before C0, the shortest affected smoke IDs run first; after they pass, complete read-only C0 and
    remaining focused execution may overlap on the same frozen tip. C1 waits for their join.
27. **Verification classification:** `production/material` changes use the full bounded repair batch;
    a **strict test-only fast lane** is only for fixture/setup-or-metadata-only corrections with known
    failed IDs. Its **deterministic diff/eligibility checklist** proves unchanged production, policy,
    contract, locked configuration, test oracle, assertion strength, expected outcome, stable ID, and
    coverage obligation. The same continuation reruns **exactly those failed IDs** once; there is
    **no fresh C0** and **no unrelated smoke** or work before it. Administrative corrections resume
    their lane without product review or test rerun. Any failed/unproved checklist or
    expected-behavior, coverage-obligation, operative-contract, production, or policy change is
    material.
28. Dependency maps, registry state, and aggregate join evidence reconcile once per accepted batch
    tip, while every raw lane result remains preserved.

## 10. File handoffs

`ROOT-IM` owns final integration and the authoritative copies of these handoffs:

| Handoff | Required location | Producer | Consumer |
|---|---|---|---|
| Governing specification | `active_docs/GENERALIZATION_SPEC_2.md` | planning turn | all lanes |
| Roadmap criteria | `active_docs/IMPLEMENTATION_ROADMAP_2.md` | planning turn | all lanes and audits |
| Execution plan | `plans/general-coding-harness/EXECUTION_PLAN_2.md` | planning turn | `ROOT-IM` |
| Implementation workspace | `plans/general-coding-harness/runtime/firmware-v2/.agent-workspace/` | `ROOT-IM` during S1-S3/C0-C2/C4 | implementation lanes and audits; never reused as C3 attempt state |
| C3 attempt workspace | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/.agent-workspace/` | `C3-HARNESS` controllers during that attempt | `F.C3.O`/`F.C3.W`; immutable after attempt exit |
| Parallel state | `plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md` for implementation; `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/PARALLEL_CHECKPOINT.md` for C3 | `ROOT-IM` at implementation joins; `F.C3.O` through candidate commands during C3 | next lane/gate; attempt file retained read-only after exit |
| Passed registries | implementation `plans/general-coding-harness/runtime/firmware-v2/passed-tests.json`; C3 `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/passed-tests.json` | ROOT writes implementation until C1 freeze; `C3-HARNESS` writes only current attempt registry | selective planner; C4 verifies C1 immutability and manifest coverage/reference integrity |
| Native event log | `plans/general-coding-harness/runtime/firmware-v2/events/LANE_EVENTS.jsonl` for implementation; `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/events/LANE_EVENTS.jsonl` for C3 | candidate controllers | `ROOT-IM` during implementation; `F.C3.O`/`F.C3.W` during the named attempt |
| Manager signals | implementation `plans/general-coding-harness/runtime/firmware-v2/manager-signals/`; C3 `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/manager-signals/` | exact manager-owned relay/repair producer | explicit owning control plane only: `ROOT-IM` outside C3, `F.C3.O` through `C3-HARNESS` inside the named attempt; watcher abort is explicitly excluded |
| Product step evidence | `plans/general-coding-harness/evidence/firmware-v2/S1/` through `S3/` | step lanes/`ROOT-IM` | C0/C4 auditors |
| Final automated evidence | `plans/general-coding-harness/evidence/firmware-v2/final/` | C0-C2/safeguard | promotion audit |
| Practical acceptance evidence | `plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/` | F.C3.O/F.C3.W | C4 and completion; every prior attempt retained read-only |
| Acceptance manifest/result | attempt evidence create-once `EVIDENCE_MANIFEST.json`, then `ACCEPTANCE_RESULT.json` within 90 seconds | `F.C3.O` only after candidate shutdown and W terminal-report/exit/reap | closed inventory of all regular files across both roots except self/result/reserved topology, plus separately verified `external_references` paths/hashes for C1/delegated/editorial artifacts; C4 independently enumerates and rejects unknown/unlisted/mismatched files |
| O identity/liveness | reserved prelaunch `topology/ORCHESTRATOR_LAUNCH_INTENT.json`, post-spawn `ORCHESTRATOR_IDENTITY.json`, `ORCHESTRATOR_KEY_RELEASE.json`, heartbeats, normal `ORCHESTRATOR_EXIT.json`, or loss | ROOT writes create-once intent/identity/key-release/exit-or-loss; O acknowledges identity before key transfer and writes heartbeats | release-bound signatures, 30/90 liveness, P4 deadline, exact final-message/exit/reap, and C4 provenance |
| Governing-input watcher | reserved `topology/GOVERNING_INPUT_WATCHER.json` | ROOT-owned registered non-agent helper writes exact identity/current hashes/heartbeat only | mid-call revocation; exact exit/reap covered by topology shutdown |
| C3 topology shutdown | attempt evidence `topology/TOPOLOGY_SHUTDOWN.json` | `ROOT-IM` after W was already reaped before manifest and after O/remaining registered topology exit/reap | inventories/hashes every other topology file, excludes itself, forbids symlink/temp, and is separately hashed/verified by C4 |
| Watcher evidence | attempt evidence `watcher/WATCHER_READY.json`, `watcher/WATCHER_HEARTBEATS.jsonl`, `watcher/WATCHER_REPORT.md`, create-once `watcher/ABORT_REQUIRED.json`; reserved ROOT-owned `topology/WATCHER_LAUNCH.json` and `WATCHER_EXIT.json`; loss when applicable | F.C3.W writes ready/heartbeat/report and atomically creates abort; ROOT writes immutable launch/exit/loss topology evidence | gates target start, continuous observation, direct abort, exact model/thread/final-message/exit/reap proof, and failure classification |
| Target project | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/target/` | F.C3.A1/C1 through `C3-HARNESS` | F.C3.P1/R1 |
| Per-lane MCP state/artifacts | `plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/` | `C3-HARNESS` lane controller/MCP server only | F.C3.P1 receives returned results only in its `RESULT.json`; O/W/C4 consume broker evidence read-only |
| Retained MCP session | `hil/{lane-id}/sessions/{SESSION_ID}/SESSION_REQUEST.json`, `SESSION_OPEN.json`, and terminal `SESSION_CLOSED.json` or `SESSION_ABORTED.json`; O normal-close intent at `session-close-decisions/{SESSION_ID}.json` | `C3-HARNESS` creates lifecycle evidence and alone owns process/stdio/claim; F.C3.O creates only the signed normal-close decision | one finite attempt/lane/board Server Run; every post-bootstrap call separately authorized, consecutive, predecessor-bound, policy-transition-valid; terminal exact drain/exit/reap/release |
| Hardware authorization | canonical preflight/C1 scope plus default-deny `MCP_METHOD_POLICY.json`; proposal, signed O decision, authorization, and pre-dispatch admission under one call ID | harness proposes; O signs; harness derives immutable authorization, then separately admits fresh live state without rewriting it | exact four paths/hashes through result; monotonic plan deadline plus validity margin; timeout/expiry/revocation is no-success with exact cleanup |
| Lane result | direct lane `.agent-workspace/RESULT.json` | each mutable lane | owning controller plus `ROOT-IM` during implementation or `F.C3.O` through `C3-HARNESS` during C3 |
| Completion and promotion | `plans/general-coding-harness/evidence/firmware-v2/final/completion.md` and adjacent records | `ROOT-IM` | future sessions |

Every handoff records exact revision, lane identity, timestamp, dependency fingerprint, and evidence hashes. Test writers never overwrite product evidence; reviewers never mutate source; doers never edit tests or source; joins preserve both raw lane outputs and the manager's decision.

## 11. Config block

```yaml
plan_id: firmware-generalization-v2
runtime_root: plans/general-coding-harness/runtime/firmware-v2
evidence_root: plans/general-coding-harness/evidence/firmware-v2
implementation_passed_registry: plans/general-coding-harness/runtime/firmware-v2/passed-tests.json
c1_evidence_root: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}
delegated_authorization_draft: plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json
delegated_authorization: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json
user_hardware_scope_source: goal.md Section 11 USER_HARDWARE_AUTHORIZATION_V1 canonical JSON object
mcp_method_policy: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/MCP_METHOD_POLICY.json
editorial_supersession: plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/EDITORIAL_SUPERSESSION.jsonl
promoted_runtime_root: plans/general-coding-harness/runtime/promoted-firmware-v2
candidate_worktree: plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate
candidate_branch: firmware/v2-candidate
candidate_base: 4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f
frozen_rollback: 287ea53793e3963062882012ff80c3b0e8c41587
mcp_server_worktree: plans/general-coding-harness/runtime/firmware-v2/worktrees/mcp-candidate
mcp_server_branch: firmware/v2-mcp-candidate
mcp_server_base: f003f84a7df51cd8595a3203c62e225b21da2a22
acceptance_attempt_runtime: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN
acceptance_attempt_evidence: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN
c3_passed_registry: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/passed-tests.json
call_authorization: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/authorizations/{CALL_ID}.json
call_proposal: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/call-proposals/{CALL_ID}.json
orchestrator_call_decision: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/authorization-decisions/{CALL_ID}.json
dispatch_admission: plans/general-coding-harness/runtime/firmware-v2/acceptance/attempt-NNNN/hil/{lane-id}/dispatch-admissions/{CALL_ID}.json
acceptance_result: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/ACCEPTANCE_RESULT.json
acceptance_evidence_manifest: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/EVIDENCE_MANIFEST.json
orchestrator_identity: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_IDENTITY.json
orchestrator_launch_intent: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_LAUNCH_INTENT.json
orchestrator_key_release: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_KEY_RELEASE.json
orchestrator_heartbeats: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_HEARTBEATS.jsonl
orchestrator_exit: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/ORCHESTRATOR_EXIT.json
watcher_launch: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/WATCHER_LAUNCH.json
watcher_exit: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/WATCHER_EXIT.json
emergency_termination: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/EMERGENCY_TERMINATION.json
governing_input_watcher: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/GOVERNING_INPUT_WATCHER.json
acceptance_topology_shutdown: plans/general-coding-harness/evidence/firmware-v2/acceptance/attempt-NNNN/topology/TOPOLOGY_SHUTDOWN.json
acceptance_manifest_exclusions: [EVIDENCE_MANIFEST.json, ACCEPTANCE_RESULT.json, topology/]
acceptance_attempt_policy: one greater than largest runtime/evidence number, or 0001 if none; both chosen paths absent; preserve one-sided/collision state; never clear, overwrite, gap-fill, or reuse
target_seed_manifest: TARGET_SEED_MANIFEST.json
target_seed_files: [TARGET_CHARTER.md, PINNED_INPUTS.json, TEST_CONTRACT.json, EVIDENCE_SCHEMA.json]
evaluator_enabled: false
stall_threshold: 3
scope_policy: backward-compatible firmware harness, MCP acceptance kit, four-board certification, and directly implicated coding regressions only
gap_scope: change
final_full_verification: true
final_full_verification_semantics: one logical SAFEGUARD_RUN_ID per exact C1 lock; goal.md requires exact C1 equality and only the other four governing docs may use a valid C1-rooted EDITORIAL_SUPERSESSION chain; admission is outside run; environment interruption resumes incomplete/invalidated components
protected_general_harness_unit_regressions: true
max_role_fanout: 2
max_agents_beside_ROOT_IM: 3
production_coder_pool: 1
reviewer_pool: 2
doer_pool: 2
green_test_policy: retain unless dependency fingerprint changes
review_completion_policy: complete assigned affected-surface sweep; never intentional first-finding stop
repair_batch_policy: triage complete finding/test result; repair all accepted items before next product review
production_finding_policy: supported or credibly reachable deployed trigger plus concrete negative consequence; latent safety/authorization/fail-closed defects included; cosmetic/unreachable/behavior-neutral/speculative issues excluded
pre_c0_policy: freeze joined tip; run shortest affected smoke; then overlap complete read-only C0 with remaining focused execution; join before C1
non_product_correction_policy: same-lane administrative resume; strict test-only fast lane requires fixture/setup-or-metadata-only diff, deterministic unchanged-oracle/assertion/contract checklist, and one exact failed-ID rerun before unrelated work, with no C0/ordinary review/reconciliation; expected-behavior/coverage/operative-contract/production/policy change is material
batch_reconciliation_policy: preserve raw lane evidence; reconcile dependencies, registry, and aggregate join once per accepted batch tip
hardware_interface: BYO Firmware MCP only
rf_frequency_intent_mhz: 915
destructive_recovery: excluded
acceptance_orchestrator: gpt-5.6-sol high priority
acceptance_target_launch_owner: C3-HARNESS only; F.C3.O submits assignments and never directly launches a target worker
acceptance_server_source_policy: immutable; AUTHORIZED_SERVER_LIMITATION requires exact attribution, strongest-safe partial/unit substitute, and explicit physical non-certification
coder: gpt-5.6-terra medium priority
reviewer_and_test_writer: gpt-5.6-terra medium priority
doer_and_test_executor: gpt-5.6-luna high priority
watcher: gpt-5.6-terra medium priority
model_substitution: forbidden
codex_approval_and_sandbox: dangerously-bypass-approvals-and-sandbox
codex_hook_trust: dangerously-bypass-hook-trust
codex_user_config: ignored
mcp_registration: explicit per lane
mcp_environment: allowlisted; no unreviewed .env or ambient probe/target route
historical_manifest_sources: provenance only; destination hashes required
ncs_python_cache: fresh per lane below runtime root
candidate_gate_root: reserved candidate worktree, never implicit stable-general-harness-runner
promotion_branch: progress/v1.2
external_publish: requires explicit live directive
```

The runner must validate this plan before execution. Configuration cannot weaken an atomic criterion, add a model substitution, expand hardware authority, reuse a prior acceptance runtime, or turn an extended qualification item into a release gate without an explicit plan revision.

<!-- END SNAPSHOT plans/general-coding-harness/EXECUTION_PLAN_2.md -->
### Snapshot: `plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md (historical runtime checkpoint; reconcile against direct lane artifacts)`

<!-- BEGIN SNAPSHOT plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md -->
# Firmware V2 execution checkpoint

> **Policy supersession (2026-08-05):** For a correction limited to synthetic fixture/setup or test
> metadata, use the strict test-only fast lane only after a deterministic checklist proves unchanged
> production, policy, contract, locked configuration, test oracle, assertion strength, expected
> outcome, stable ID, and coverage obligation, with exact failed IDs known. Continue in the same
> test-author lane and rerun exactly those IDs once before unrelated work. Do not create C0, ordinary
> review, or reconciliation. A failed or unproved condition is material and follows the normal route.

> **Superseding resume note (2026-08-05):** The historical pause narrative below predates the
> completed `F.C0.FR1-0012` repair review, test-only fixture follow-up, and all-child-Fast CP04
> smoke. `C3-CP-01-02` is the one currently uncredited failed ID; CP04 does not substitute for it.
> Before any unrelated work, classify its correction against the strict test-only fast lane. Only a
> synthetic fixture/setup or test-metadata diff with a recorded deterministic checklist proving no
> production, policy, contract, locked-configuration, oracle/assertion/expected-outcome/stable-ID,
> or coverage change may continue in the same test-author lane and rerun that exact ID once. It has
> no C0, ordinary review, or reconciliation. Otherwise use the material route.

> **USER PAUSE â€” 2026-08-04:** The execution goal remains paused after the user-directed governing-
> layout optimization. No registered subagent/controller, resource claim, MCP process, or hardware operation is
> active. Preserve product lane `e5ced2724464043b7cdc32c749b92bbe8dad90f1`, test-author lane
> `b2949d434136670846ac807c638cd446303dcb5c`, reviewer/triage evidence, candidate `659dd03`, and
> immutable MCP fixture `f003f84`. `e5ced272` has author-side static checks only and still needs test
> adaptation, fresh review, and selective execution. The optimized flow is frozen-tip smoke first,
> then complete review and remaining focused execution in parallel, one repair batch, and one final
> reconciliation. Read root `HANDOFF.md` before any resume.

- Owner: `ROOT-IM` (the outside implementation orchestrator; never `F.C3.O`)
- Phase: pre-C3 admission found accepted candidate control-plane gap `F-PRE-C3-001`; current C1/C2 are preserved but superseded and the minimal C3-HARNESS product slice is reopened
- Candidate: clean `firmware/v2-candidate` at `659dd03e2aa7159090c8e0e20123b1fec1749f90`
- MCP fixture: clean, immutable `firmware/v2-mcp-candidate` at `f003f84a7df51cd8595a3203c62e225b21da2a22`
- Stable implementation runner: clean detached `stable-general-harness-runner` at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`
- Registry: exact candidate `659dd03`; 21 green groups; 140 unique green IDs; zero invalidations; 56 evidence credits
- Hardware mutation/access: none
- Child launch tier: all launched coders, reviewers/test writers, doers/test executors, `F.C3.O`, and
  `F.C3.W` use Fast (`service_tier="priority"`); resume must prove Sol-high-priority,
  Terra-medium-priority, and Luna-high-priority before dispatch. Luna-high-priority is the changed
  no-op availability proof.
- C1/C2: C1 `bf17d2fc-9dda-4932-b8e6-448de69b0591` and C2 attempt 0002 completed green on candidate `659dd03`, then were invalidated/superseded before C3 by `F-PRE-C3-001`; a repaired candidate requires fresh C0/C1 and dependency-invalidated C2
- Active resource claims or target processes: none

## Authoritative resume boundary

C0 attempt 0006 remains immutable but superseded. ROOT's separate pre-C1 admission found two
executable candidate gaps: delegated user scope/action classes were hash-bound but not enforced, and
the controller could not retain the pinned server's stateful setup/validation/plan/action Server
Run. No C1 was created and no hardware was authorized or accessed.

The exact repair contract is
`evidence/firmware-v2/S2/S2_PRE_C1_EXECUTABLE_CONTRACT_DECISION.json` at SHA-256
`9e0fbac168edc13b0d243392b661d95eb6483d7234f515703158c57b273dee91`. The serial S2 production
chain implemented its default-deny 21-method policy, five-key delegated authorization support,
per-call scope/action/effect binding, finite retained session, exact dynamic routes, limitation API,
and seed changes. Review/test fixture corrections were ordinary agent corrections, not harness,
watcher, or server failures. They caused no reset and reran only invalidated IDs.

The final one-line production correction at `e524feb` permits the pinned server's exact all-null
`board_setup-plan` initialization (including null `board_id`) while preserving exact equality for
every non-null board ID and the existing full server-route comparison. Persistent R1 returned empty
findings. D1 joined 25 preserved green IDs with the sole invalidated test for 26/26 PASS. R2's
limitation/call-chain review remains valid because no later production kit dependency changed. D2
joined 17/17 current kit tests with preserved 3/3 target tests for 20/20 PASS.

ROOT validated all original `FINDINGS.json`, `RESULT.json`, test-report, and triage artifacts with
the candidate validator and accepted the join in
`evidence/firmware-v2/S2/S2_PRE_C1_JOIN_ROOT_ACCEPTANCE_e524feb.json`. Registry reconciliation is
`evidence/firmware-v2/S2/S2_PRE_C1_REGISTRY_RECONCILIATION_e524feb.json`. The protected original
general-harness suite was not rerun because no mapped dependency changed.

Fresh C0 attempt 0007 and ROOT admission were green, so ROOT created the first C1 and dispatched C2.
C2 then correctly rejected the registry's inherited protected-test credit because the candidate-wide
map omitted the changed shared `git_safety.py` surface. ROOT accepted `F-C2-FINDING-001`, invalidated
that C1, and preserved the failed attempt. A fresh Terra dependency author mapped every candidate-wide
shared delta; after one same-thread result-envelope correction, ROOT accepted the 14-ID supplement at
`evidence/firmware-v2/S2/CANDIDATE_SHARED_CODE_DEPENDENCY_MAP_e524feb.json`. Independent Luna-high
F.C2.D2 ran exactly those 14 previously uncovered IDs once: 14/14 passed, with no skips, findings,
MCP, or hardware access. Its result-envelope correction did not rerun tests. The closure and updated
19-group/137-ID/46-credit registry are bound in
`evidence/firmware-v2/S2/S2_CANDIDATE_WIDE_PROTECTED_DEPENDENCY_RECONCILIATION_e524feb.json`.

Fresh C0 attempt 0008 then found `F-C0-FR1-001`: candidate `evaluate_call` checked UART key sets
but allowed malformed/out-of-policy scalar and nested values before MCP dispatch. ROOT reproduced
invalid read, write, and exchange calls returning `ALLOW`, validated the closed finding, and accepted
it because the physical-boundary risk outweighs the localized validator/test repair. This is a
candidate kit defect, not an MCP-server defect and not an orchestrator/watcher reset. The immutable
MCP fixture remains untouched. Reopen only the dependency-invalidated S2 kit slice, then require a
fresh C0 before new C1.

The accepted repair chain is now closed at `9606444`. The serial coder added total finite timing and
closed UART scalar/nested validation. D3 then caught a real protected-test regression caused by
counting an optional newline against the contract's 1..256-byte `text` bound. ROOT superseded only
that mistaken reviewer interpretation, retained the valid huge-number repair, and the same coder
restored the contract with a one-line predicate correction. Fresh R4 returned zero production
findings. Persistent A4 corrected only two contradictory new expectations. Fresh Luna-high D4 ran
exactly the two dependency-invalidated IDs once and passed 2/2; the other seven D3 passes retained
hash-bound credit.

The complete current-tip dependency map is frozen at
`evidence/firmware-v2/S2/CANDIDATE_SHARED_CODE_DEPENDENCY_MAP_9606444.json`, SHA-256
`57f41acb5c5fc3d506c694d28abca39885326adc2b04540ff3e8fdd18e514d47`; ROOT acceptance is
`CANDIDATE_SHARED_CODE_DEPENDENCY_MAP_ROOT_ACCEPTANCE_9606444.json`, SHA-256
`586fdd6f101da8f66561cd266bdff9026f9946762eab5a70db8ce04c505c2c3c`. The reconciled registry is
SHA-256 `87dd3f6f786cff107fe29601fc0e3404b90f11d9d428472596373e722c0dd2a6`. ROOT join acceptance is
`S2_C0_0008_JOIN_ROOT_ACCEPTANCE_9606444.json`, SHA-256
`0668594d1cc1e40aef1f681ed0646a245bbca631d5d3ef8f8d1a2f5bd4d5728e`. The persistent product
closeout is current-tip, controller-valid, empty-findings, clean, and claim-free. No MCP or hardware
operation occurred. The two rejected pre-launch invocation/path shapes were ordinary manager-input
corrections and caused no agent/test reset.

Fresh C0 attempt 0009 found that generic integer narrowing treated LoRa
`spreading_factor_min` as a maximum, admitting values below delegated 7 and rejecting a valid
narrowed minimum 8. ROOT reproduced and accepted this as a functionality-breaking RF scope
expansion. The persistent coder added a localized lower-bound and interval-consistency repair at
`21aeadc`. Fresh R5 confirmed production green and identified only worthwhile missing regression
coverage. Persistent A4 added five assertions inside the existing scope-effect ID; fresh Luna-high
D5 ran exactly that one invalidated ID once and passed. No other green ID ran.

The joined candidate is `659dd03`. The complete dependency map is frozen at
`evidence/firmware-v2/S2/CANDIDATE_SHARED_CODE_DEPENDENCY_MAP_659dd03.json`, SHA-256
`9dd4fd25edbce63ce86f5f1d82834734a434ff59f95b7c2d930fc8fc237ee7d6`; ROOT map acceptance is
SHA-256 `f897211f9c750bd079d703a26eef030a71d0f6d1952527c2fe9091c03560abab`. The registry is SHA-256
`4eff6f5e46ae33056dc40f27474eb7c85b322f2392bf52b5fbbd9a356fd11c3d`. ROOT join acceptance is
`S2_C0_0009_JOIN_ROOT_ACCEPTANCE_659dd03.json`, SHA-256
`e3bf66165986d7a298ee311e51c4db5380ffc7dd54f693c2288cf487e365420d`. Product closeout is
current-tip, controller-valid, clean, empty-findings, and claim-free. MCP/RF/hardware remained
untouched.

## Immutable MCP-server boundary

The pinned BYO Firmware MCP repository is a compatibility fixture, not a product target. No role may
edit, recommit, repin, or repair it. During C3, only a genuinely evidenced server defect or
incompatibility may enter candidate-owned `AUTHORIZED_SERVER_LIMITATION`. `F.C3.O` must then choose
the strongest safe substitute through `C3-HARNESS`: partial MCP first, focused pinned-component
unit/integration next, and synthetic candidate-boundary coverage last. Any unexecuted physical
portion remains `NOT_CERTIFIED`. No direct pyOCD, serial, MCP, probe, flash, reset, debug, or RF
bypass is allowed, and protected original general-harness tests cannot be substituted.

Fresh C0 attempt 0010 completed once on thread `019fcea9-0a5a-7283-b343-4ea6ba0a83e9` with
`NO CANDIDATE GAP / READY`; it ran no tests and touched neither MCP nor hardware. ROOT independently
validated its exact six-key findings, eight-key result, current-tip controller result, clean
candidate/server/stable-runner identities, all 56 registry evidence hashes, and the accepted
dependency map. The immutable admission is
`evidence/firmware-v2/final/c0/attempt-0010/ROOT_ADMISSION.json`.

## Pre-C3 admission supersession and next action

C1 `bf17d2fc-9dda-4932-b8e6-448de69b0591` and C2 attempt 0002 completed green without MCP or
hardware access. ROOT's independent pre-C3 executable-API audit then found accepted
`F-PRE-C3-001`: candidate `659dd03` has retained-session and broker primitives plus the generic
lane controller, but no executable `C3-HARNESS` boundary through which `F.C3.O` can submit an
attempt/topology/C1-bound target assignment and have the candidate exclusively launch, validate,
observe, reap, and report the target worker. Starting C3 would require a forbidden direct launch or
would be impossible. This is a functionality-breaking candidate gap, not a pinned-server defect,
watcher failure, or orchestrator mistake.

The immutable finding, C1 invalidation, and C2 supersession are under
`evidence/firmware-v2/final/c2/attempt-0002/ROOT_PRE_C3_ADMISSION_GAP.json`, the operative C1
directory's `C1_INVALIDATION.json`, and C2's `PRE_C3_SUPERSESSION.json`. Preserve all prior green
evidence; rerun no green ID unless the repair dependency map invalidates it.

The minimal C3 control-plane production repair is preserved on clean lane `e5ced272` with only
author-side static checks; it is not joined or green. On explicit user resume, classify the new
governing hashes as an execution-layout/finding-admissibility and child-service-tier change that
does not alter the product, hardware authority, immutable server, or accepted control-plane repair
contract. First prove the Fast launch triplet Sol-high-priority, Terra-medium-priority, and
Luna-high-priority; the changed Luna proof is mandatory. Then cherry-pick
`e5ced272` into the preserved test-author lane and adapt CP04. Freeze the joined tip and run the
shortest selected smoke ID. If green, run one complete fresh read-only review and the remaining
dependency-invalidated selected IDs in parallel. The reviewer must finish the whole assigned sweep;
ROOT batches all accepted findings before another review. Administrative corrections resume their
lane; test-only corrections that restore an unchanged governing requirement rerun only affected
review/execution, while expected-behavior/coverage/operative-contract changes remain material.
Reconcile dependency mapping,
registry, and aggregate evidence once for the accepted tip. Then require fresh terminal C0, new
opaque C1, and dependency-invalidated C2. C3, hardware authorization use, C4, safeguard, and
promotion remain locked until that exact chain is green. The immutable MCP fixture stays untouched;
`AUTHORIZED_SERVER_LIMITATION` is inapplicable to this candidate gap.

Paused optimized governing hashes are:

- `goal.md`: `858435ee32efea45b27ffc9cf991e1eb86d607b5e414ff6f6e31ae7c03b07c82`
- `active_docs/GENERALIZATION_SPEC_2.md`: `8b18006c1faa2718434d6bc2bd45f66fdc434ede24a4abc1a44eea509ab2df10`
- `active_docs/IMPLEMENTATION_ROADMAP_2.md`: `5ec120af193086244cdb72c5ba1a450c51a7ae591692dbda3878d4f2dff34554`
- `plans/general-coding-harness/EXECUTION_PLAN_2.md`: `9d2f0ea7536ce5009275826853c4110bd92f8a7a14277284a6748499ce7f3fdf`
- `active_docs/EXECUTION_READINESS_2.md`: `c1c1ca55af7d6e8e5f2ed5fe39ce995ba5855d114d3a58b4958f6ea18212c4e4`

<!-- END SNAPSHOT plans/general-coding-harness/runtime/firmware-v2/PARALLEL_CHECKPOINT.md -->
### Snapshot: `Firmware/Firmware resources/AGENTS.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/AGENTS.md -->
# Firmware resource-library rules

This directory is a read-only convenience mirror, not a runtime or authority root.

- Read `README.md` before using or refreshing resources.
- The original source path in `SOURCE_MANIFEST.csv` remains authoritative.
- Verify hashes before using datasheets, device packs, fixture declarations, or toolchain locks.
- Never put logs, run evidence, build output, checkpoints, caches, installed packs, virtual
  environments, or live state here.
- Never copy an entire fresh experiment into this directory.
- Copied sprint documents are reference snapshots only. They do not grant authorization and do not
  override the active repository plan, goal, handoff, or retained evidence.
- Refresh by copying; do not move or delete the original resource.
- After any refresh, regenerate `SOURCE_MANIFEST.csv` and confirm source and destination hashes
  match.

<!-- END SNAPSHOT Firmware/Firmware resources/AGENTS.md -->
### Snapshot: `Firmware/Firmware resources/README.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/README.md -->
# Firmware Resources

This is a convenient **copy library** of shared firmware-testing inputs and documentation. The
original files remain in their existing repository locations and remain authoritative.

This folder contains no experiment status, build output, run evidence, runtime logs, watcher state,
or fresh-experiment project trees.

## Start here

1. Read `test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` for the complete evaluation plan,
   fixture contract, experiment catalog, pass gates, and hardware references.
2. Read `test-program/run-firmware-test-suite/SKILL.md` and its `references/` for the suite execution
   procedure.
3. Use `datasheets/`, `device-packs/`, and `fixture-and-toolchain/` as immutable inputs. Verify the
   file hash against `SOURCE_MANIFEST.csv` before relying on a copy.
4. Use `server-guides/` for the BYO-Firmware-MCP interfaces and setup contracts.
5. Use `orchestration-guides/` for the native harness and diagnostic watcher.

## Contents

### `datasheets/`

- STM32L476RG device PDF.
- nRF52840 product specification.
- SX1261/SX1262 device PDF.
- Waveshare LoRa module PDF.

Only one hash-unique copy of each shared PDF is retained here even when many experiment folders
contain the same bytes.

### `device-packs/`

- Keil STM32L4 device-family pack used by the STM32 setup work.
- Nordic nRF device-family pack used by the nRF setup work.

These are copied package inputs, not installed package state or a package cache.

### `fixture-and-toolchain/`

- `CONNECTED_HARDWARE.md`: four-board topology, stable identities, I2C wiring, and nRF/CoreSX1262 pin mapping.
- Fixed nRF/SX126x pin mapping.
- ARM toolchain lock declaration.
- nRF Connect SDK lock declaration.

### `test-program/`

- The master end-to-end experiment guide.
- A complete copy of the `run-firmware-test-suite` skill, including its execution contracts,
  roster, model-continuity rules, result contract, and reusable scripts.

### `sprint-documentation/`

- `current/`: current sprint specifications and checklist copies.
- `archive/`: completed sprint, logging, watcher, and harness repair-plan copies.

These are planning/reference snapshots, not live authority or proof that a sprint passed. Consult
the original active plan and actual retained evidence before making a live decision.

### `server-guides/`

Shared BYO-Firmware-MCP README, operator guide, architecture, client contract, plan-tool contract,
and CMSIS-Pack admission design.

### `orchestration-guides/`

Harness/watcher specifications and quick-use rules. These are documentation copies only; production
code remains in `orchestrator_harness/`, `harness_common/`, and
`harness_watcher_implementation/`.

## Copy policy

- Do not write runtime output here.
- Do not treat a copied plan as current authority.
- Do not edit a copy and assume the source changed.
- When intentionally refreshing a resource, copy from its authoritative source and regenerate
  `SOURCE_MANIFEST.csv`.
- Do not copy entire `fresh-experiments/` runs, `.agent-workspace/`, logs, evidence, build trees,
  caches, virtual environments, or hardware runtime state into this library.

`SOURCE_MANIFEST.csv` records the source path, destination path, byte count, and SHA-256 of every
copied resource. Authored index/reference documents such as this README and `CONNECTED_HARDWARE.md`
are not source-copy manifest entries.


<!-- END SNAPSHOT Firmware/Firmware resources/README.md -->
### Snapshot: `Firmware/Firmware resources/test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md -->
# BYO Firmware MCP: End-to-End Evaluation Program

NB: You have EXPLICIT PERMISSION to go online and download your own datasheets, and copy them into the repos.
**Repository evaluated:** `MCP-Trial-3/BYO-Firmware-MCP`
**Original program baseline:** `9b34a849d8cc4cb1f8a1146000ded8e93d168a28`
(`fixing bugs on prototype that Jeff ran into`). Every run must bind itself to the exact server
snapshot it actually evaluates: HEAD plus the reviewed tracked diff and production-tree
fingerprint when the worktree intentionally contains uncommitted repairs. A clean checkout is
preferred for reproducibility but is not a release prerequisite, and a reviewed dirty snapshot is
not a reason to stop. Never mix server snapshots within one phase or silently advance to a later
revision.
**Available hardware:** two NUCLEO-L476RG boards and two nRF52840 DK boards, with the
STM32 boards linked by I2C on PB13/PB14 and one Waveshare CoreSX1262 module attached to each nRF
DK.

## 1. Purpose and definition of â€œcompleteâ€

This is a practical whole-product evaluation, not merely a collection of â€œcan it blink?â€
demos. It tests:

1. Whether a Claude or Codex agent can start from an empty application repository, an exact
   MCU ordering code, and authoritative documentation.
2. Whether the MCP server discovers, sets up, distinguishes, and safely operates one or more
   real boards.
3. Whether an agent can build, deploy, verify, diagnose, repair, and retest realistic firmware.
4. Whether the server catches a fallible agent's mistakes without fabricating success or
   blocking correctly targeted work.
5. Whether plans, permissions, safety maps, artifact binding, process isolation, cleanup,
   timeouts, and per-board state behave correctly under failure.
6. Whether every registered MCP tool gets either:
   - a successful real-hardware exercise, or
   - an intentional, truthful refusal when the required authority is unavailable.

No finite HIL suite can cover every Python branch or every firmware situation. â€œCompleteâ€ for
this program therefore means all three layers below pass:

| Layer | Required coverage |
|---|---|
| Host automated tests | Unit, protocol-integration, fault-injection, and property tests for paths unsafe or impractical to induce on hardware |
| MCP contract tests | Every tool registered by the assigned server snapshot, dynamic visibility, strict schemas, plans, permissions, budgets, and restart semantics |
| Hardware experiments | Both MCU families, both probe families, one-board and two-board operation, UART, I2C, BLE, SPI/LoRa, flash, reset, debug, disconnect, cancellation, and recovery |

The original baseline contained **155 pytest-style tests**; record the actual collected count for
the assigned snapshot rather than using that historical number as a gate. The tests are strongest
around process isolation, J-Link behavior, connection promotion/cleanup, breakpoint truthfulness,
UART evidence, validation honesty, trusted-input admission, and several previously overstrict
limits. They are not a substitute for the application-level HIL campaigns below. Also note that
the current `pyproject.toml` development group declares Ruff and Pyright but not pytest; make the test runner
reproducible before treating a clean clone as testable.

## 2. What the repository says the server owns

The plan is derived from the current code and its documentation, especially:

- `README.md` and `SERVER_GUIDE.md`
- `docs/architecture.md`
- `docs/client-contract.md`
- `docs/plan-tool-contract.md`
- `src/pyocd_debug_mcp/server.py`
- `src/pyocd_debug_mcp/guardrails/plan_defs.py`
- `src/pyocd_debug_mcp/{setup_flow,safety,kernel,tools,adapters,services}/`

The relevant product boundaries are:

- project-local fresh-board setup, profile persistence, datasheet evidence, CMSIS-Pack
  verification, and safety-map generation;
- normal profile-based connection plus planned exceptional connection paths;
- process-isolated pyOCD sessions and board-scoped operation serialization;
- UART capture, write, and state-preserving multi-step exchanges;
- native-build execution and explicit artifact normalization;
- symbol, memory, CPU-register, peripheral-register, execution, breakpoint, and reset control;
- application/bootloader flash containment;
- run-scoped plans, permissions, validation gates, and budgets;
- destructive recovery with a fresh two-phase approval;
- cleanup after success, failure, timeout, cancellation, USB loss, and server shutdown.

The server intentionally ships without board profiles, packs, reference firmware, or `.firm`
runtime state. That makes a truly clean setup campaign essential.

## 3. Evaluation rules

### 3.1 Separate server correctness from agent skill

Score two things independently:

**Server score**

- Did the correct physical board receive the operation?
- Did the server reject stale, mismatched, malformed, unsafe, or unauthorized requests before
  target mutation?
- Did it report only observed facts?
- Did one board's failure leave the other board usable?
- Did it clean up sessions, serial handles, workers, plans, gates, and permissions correctly?

**Agent score**

- Did the agent follow the handshake and setup routing instead of guessing internal IDs?
- Did it obtain authoritative facts rather than invent a target, pack, pin, address, or port?
- Did it use UART/logging first and escalate to breakpoint/memory/register inspection when
  justified?
- Did it state a concrete hypothesis and interpret evidence correctly?
- Did it find the seeded root cause rather than blindly editing until the symptom disappeared?
- Did it avoid retry thrashing and clean up temporary instrumentation?

A working final application does not excuse a server safety failure. A correct server refusal
does not prove the agent debugged well.

#### 3.1.1 Zero-operator, no-external-blocker contract

A per-run specification translates this catalog into executable checks; it must not make the
catalog stricter merely because additional evidence would be nice to have. Treat a fact as a hard
prerequisite only when at least one of these is true:

- the selected catalog case explicitly requires it;
- the live server requests it to continue the public workflow;
- it is necessary to distinguish pass from fail for the claimed behavior; or
- it is necessary for electrical, RF, destructive-action, or target-identity safety.

The main suite is autonomous after launch. No main-catalog action may require another user message
or a human to touch, inspect, identify, move, rewire, relabel, reposition, power-cycle, or observe
hardware. Never require a photograph, visible marking, printed PCB revision, PCA number, removable
label, cable move, button press, jumper/solder change, DMM, logic analyzer, BLE sniffer, camera,
oscilloscope, external power instrument, or operator-timed event. Treat the connected four-board
fixture, its declared CoreSX1262 wiring, stable electronic identities, and recorded delegated
authorization as supplied inputs.

Use electronic/software-controlled equivalents: server disconnect/reconnect/reset, process-scoped
provider interruption, firmware-controlled advertising/RF disable, host-side enumeration evidence,
UART/peer counters, debug state, artifact hashes, and existing correlated evidence. Accept one
truthful, adequately correlated source; never demand the same fact through multiple modalities.
Electrical, RF, destructive-action, and target-identity safety remain mandatory, but satisfy them
from the declared fixture and live server plans rather than inventing operator work.

If a sealed run specification accidentally added such an extra gate, correct it with a signed
specification amendment and preserve already valid evidence. Removing an invented prerequisite is
a spec correction, not test weakening and not a reason to restart the doer or repeat unrelated
work.

`NEEDS_USER` and `INFRA_BLOCKED` are invalid terminal outcomes for main-catalog runs. The manager
repairs ordinary tooling, launcher, USB, network/cache, SDK, and server infrastructure; applies the
recorded delegated authorization after reviewing an exact live plan; accepts an autonomous
equivalent oracle; or corrects the spec and resumes the same persistent doer. Record temporary
resource/provider absence only as `WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` in the suite
coordination ledger, never in `RESULT.json`, and continue every unrelated lane. If a branch is
intrinsically impossible without a new human action or unavailable special equipment, move only
that branch to non-gating Appendix A and record `SKIPPED_AUTONOMY_REQUIRED`.

### 3.2 Fresh-run controls

For a **fresh setup/app** run:

1. Use a new application directory or fresh Git worktree.
2. Give the roster-assigned persistent doer a fresh, isolated task context. Do not create a new
   provider conversation merely for freshness; provider-session persistence and application-state
   freshness are separate concerns.
3. Start a new MCP server process.
4. Set a unique `BYO_MCP_ARTIFACT_ROOT`, or use that project's empty `.firm`.
5. Do not copy profiles, packs, safety maps, build outputs, or prior agent notes.
6. Record the host USB/probe/serial inventory. Exercise enumeration/reconnection with existing
   correlated port-history evidence or an autonomous host/server-controlled detach/re-enumeration;
   never request a cable move or operator-timed USB cycle.
7. Give the agent only:
   - the application requirement,
   - the exact package-level MCU ordering code established truthfully for the assigned fixture,
   - the two suite-baseline authoritative device datasheet PDFs copied by the fresh-run scaffold,
     with the specification identifying which one is applicable to each target,
   - when the case uses external wiring or modules, the manager-supplied fixed fixture wiring sheet
     containing the material facts the datasheet cannot establish, and
   - for A24/A25 only, the three explicitly allowed CoreSX1262 reference inputs named below.

The ordering code is established from the existing correlated suite record, official board
BOM/documentation, or trustworthy electronic identity evidence. Do not request another operator
statement, photograph, direct visual inspection, or PCB revision.

For a **returning-board** run, preserve `.firm` but still restart the client and server. This
distinguishes durable evidence from run-scoped authorization. Canonical shared inputs live under
task-owned `.agent-workspace/assets/datasheets/` and `.agent-workspace/assets/board-mappings/`
directories inside the relevant retained run; the scaffolder copies them into a new run
using the legacy run-local filenames below so sealed manifests remain compatible.

### 3.3 Information boundary

â€œStart with just the datasheetâ€ must not turn into â€œforce the agent to guess missing fixture
facts.â€ The fresh-run scaffold copies both suite-baseline device PDFs so one deterministic
scaffolder works for either board family; the per-run specification identifies the applicable
target document. The initial application repo should contain no code, SDK config, board profile,
pack, linker script, or generated state. It may contain:

- `REQUIREMENTS.md`
- `stm32L476rgt.pdf`
- `Nano_BLE_MCU-nRF52840_PS_v1.1.pdf`
- `.agent-workspace/FIXTURE.md`, supplied by the manager when the experiment uses corresponding
  fixed fixture facts:
  - which boards are connected;
  - STM32 I2C wiring: PB13=SCL, PB14=SDA, common ground, pull-up value and rail;
  - the **actual** CoreSX1262 module-to-nRF pin mapping;
  - the module's supported RF band and attached antenna;
  - any already-recorded solder-bridge or jumper state material to the selected interface.
- for A24/A25 only, hashed copies of `60852689.DS_SX1261_2 V2-2.pdf`,
  `waveshare-lora-module.pdf`, and `nrf-sx-pin-mappings.md`.

  Their canonical sources are
  `fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/sx1261-sx1262-v2.2.pdf`,
  `fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/waveshare-lora-module.pdf`, and
  `fresh-experiments/A24_20260726-052146/.agent-workspace/assets/board-mappings/nrf-sx1262-pin-mappings.md`;
  keep the legacy names above inside the
  sealed run.

The doer treats this file as the fixed fixture contract. It never asks the user to inspect, meter,
rewire, move, solder, or change a jumper. A test needing a different physical configuration must
use an electronically controlled equivalent or be moved to non-gating Appendix A.

The agent may research additional official references and install an ordinary compatible SDK or
toolchain. It must say when a datasheet is insufficient. For example, an MCU datasheet cannot
prove an add-on module's wiring, the legal RF band, or a development board's solder-bridge state.
The fresh repository must not include a prewritten scheduler, ThreadX application, Zephyr
application, Devicetree overlay, or generated STM32Cube project. The agent must create or acquire
the required software through its normal documented path, pin every external dependency/version,
and record the exact source revision in the run evidence.

### 3.4 Authorized-use prompt clarity

Every prompt used to start or resume a test agent, reviewer, or server-repair agent must begin
with an accurate scope statement equivalent to:

> Authorized local firmware validation. Targets are limited to the named local workspace and the
> user-owned development boards explicitly assigned by this test. Follow every declared hardware
> plan and permission gate. No remote or third-party target is in scope.

Adapt that statement truthfully for host-only tests and tests with no assigned board. Describe
work in precise firmware, protocol-conformance, input-validation, debugging, and hardware-safety
terms. Do not add cyber-oriented language such as `attack`, `exploit`, `malware`, `credential
theft`, or `bypass` unless it is technically required by the exact experiment or observed
evidence.

This is a clarity rule, not a safety-evasion rule. Never disguise, split, euphemize, or omit a
material operation to influence a classifier, and never weaken an experiment, authorization
boundary, plan, permission gate, or evidence requirement. If a platform cyber-safety notice,
reroute, or refusal occurs, preserve its exact text and request context, checkpoint the exact
session, and continue other lanes. It is not a main-run terminal status.

Every new or resumed test, reviewer, and server-repair role has unrestricted local command
execution. This is an explicit per-launch requirement, not an inherited parent setting:

- Codex launchers must pass
  `--dangerously-bypass-approvals-and-sandbox --ignore-user-config -c approval_policy="never" -c approvals_reviewer="user"`;
  refuse to start if any component is absent. The explicit CLI overrides have priority over ordinary
  config layers. They must not configure `approvals_reviewer="auto_review"`, `-a on-request`, or
  `-s workspace-write`.
- Claude launchers must use the provider-equivalent unrestricted/no-command-approval configuration
  and record it in controller status. A launcher must fail closed if that setting is unavailable.
- Every controller status records `sandbox="danger-full-access"`, `approval_policy="never"`, and
  `approvals_reviewer="user"` (or the documented Claude equivalent), matching the actual launcher
  setting. New status records atomically capture separate controller/Codex creation timestamps and
  parent identity plus one explicit terminal controller state. The maintained launchers
  and suite audit enforce this for future starts/resumes. Historical evidence retains its original
  truthful settings and is never reused as a launcher.
- This removes the Codex command-approval relay and automatic reviewer only. It never substitutes
  for the server-generated hardware plan or the suite's recorded delegated authorization for a
  hardware-changing action.

### 3.5 Delegated hardware authorization

Preserve every live server plan, disclosure, scope check, and permission field. When the user has
explicitly delegated all in-scope suite approvals to the authoritative manager, record that grant
with its exact text and timestamp. The manager then reviews each populated live plan and may relay
the delegated permission without another conversational pause when the operation, board, artifact,
losses, and final state are contained by the recorded grant. Never extend the grant to an
unassigned board, third-party target, undeclared loss, or action the live server refuses.

Attempt an Appendix A experiment only when it is fully autonomous with existing controls,
authorization, credentials, and equipment. Otherwise record `SKIPPED_AUTONOMY_REQUIRED` without
asking the user. Do not fabricate an action or weaken the server's permission flow.

### 3.6 Harness-assisted parallel execution

Use one authoritative high-level manager and the five named roster-owned doer lanes defined below.
They are not fixed STM/nRF/host resource lanes. Eagerly launch or resume every doer whose next
phase is dependency-ready and whose workspace and resource leases are isolated; keep all eligible
lanes occupied in parallel rather than completing one doer's portfolio before starting another.
The board tokens are `STM-A`, `STM-B`, `NRF-A`, and `NRF-B`; host-only spec, build, and review work
does not consume a board token.

The validated `orchestrator_harness` is required whenever two or more roles may overlap and for
every HIL/server-consuming scheduling epoch. It is a read-only reconciler and durable notification
path, not a scheduler, coordinator, approval authority, lease owner, recovery agent, or evidence
judge. The current high-level session remains the sole manager. The separate root watcher and Sol
manager used during harness acceptance were a validation fixture, not an extra normal-suite role.

Create a fresh suite-epoch config from `orchestrator_harness/config.example.json`. Its `run_globs`
list every run root the epoch may activate; its output directory is unique, under
`multi-agent-logs/orchestrator-harness/<epoch>/`, and outside all observed run roots. Record explicit review, no-progress,
and heartbeat intervals. Use 300, 600, and 420 seconds by default; shorter values are allowed only
for a bounded acceptance run, and heartbeat timeout must remain greater than review interval.
Never reuse a prior epoch's config, output state, requests, relays, PIDs, or notification records
as a live suite runtime.

Start exactly one managed watcher:

```powershell
python -m orchestrator_harness --config <suite-harness-config> watch --managed
```

Attach stdout/stderr to durable manager-owned logs or a yielded foreground process cell. Record the
watcher/owner PIDs and creation times, config hash, output paths, and lifecycle in
`multi-agent-logs/orchestrator-harness/<epoch>/ROLE_REGISTRY.json`. Each active manager epoch is:

```text
reconcile -> start/recover one managed watcher -> launch every eligible lane
-> consume one durable actionable notification -> inspect the named lane and whole-suite state
-> serial exact review/action -> ack the exact event ID -> rescan every lane and lease
-> fill newly eligible work -> heartbeat/checkpoint -> repeat
```

The same watcher reconciles and self-arms after exact acknowledgement; do not relaunch it after
each event. Inspect every live doer at least once per manager-review interval and normally every
two to three minutes during active HIL. Renew a long review before the heartbeat lease expires:

```powershell
python -m orchestrator_harness --config <suite-harness-config> heartbeat
```

A notification remains pending and is redelivered across watcher restart until the manager reviews
the exact event and runs:

```powershell
python -m orchestrator_harness --config <suite-harness-config> ack --event-id <exact-event-id>
```

Never acknowledge before inspecting the event and relevant doer outp…17003 tokens truncated…un` | A20â€“A25, D31, D33 |
| `reset_and_halt-plan`, `reset_and_halt` | A22, D31 |
| `read_cpu_register` | A22, D30â€“D31 |
| `write_cpu_register-plan`, `write_cpu_register` | D30 |
| `read_execution_state` | A22, D30â€“D31 |
| `set_execution_state-plan`, `set_execution_state` | D30 |
| `find_symbol`, `read_memory_symbol` | A20â€“A22, D30 |
| `read_memory_address-plan`, `read_memory_address` | A22, D30 |
| `write_memory-plan`, `write_memory` | D30 |
| `register_write-plan`, `register_write` | D30 |
| `set_breakpoint-plan`, `set_breakpoint`, `remove_breakpoint` | A22, D31 |
| `read_serial-plan`, `read_serial` | A20â€“A25, D33 |
| `write_serial-plan`, `write_serial` | A20â€“A25, D33 |
| `serial_exchange-plan`, `serial_exchange` | A20â€“A25, D33 |
| `collect_build_artifacts` | H03, A20â€“A25 |
| `flash_application-plan`, `flash_application` | A20â€“A25, D32 |
| `flash_bootloader-plan`, `flash_bootloader` | D32; optional Appendix A/R38 |
| `target_unlock-plan`, `target_unlock` | optional Appendix A/R37 |
| `action_batch` | H01, D33 |
| `wait` | A22, D33 |

## 9. Internal-subsystem coverage matrix

| Source area | Experiment coverage |
|---|---|
| `setup_flow/*`, profile/cache/report store | H02, H04, S10â€“S13 |
| pack provisioning and pack-index repair | H04, S10â€“S11 |
| datasheet evidence and exact part binding | H04, S10â€“S11 |
| probe inventory, serial resolution, board routing | H02, S10â€“S13, D34, D36 |
| native build and artifact collector | H03, all application campaigns |
| linker/artifact parsing and flash gate | H03, A20â€“A25, D32 |
| safety map construction/refresh/containment | H04, S10â€“S13, D30, D32, D36 |
| plan engine, permissions, gate, dynamic registry | H01, S13, D30â€“D34, D36; optional Appendix A/R37 |
| pyOCD adapter and process worker | H05, all main hardware phases, D34 |
| UART adapter/capture/exchange/finalizers | A20â€“A25, D33 |
| connection/session runtime and audit reports | S12â€“S13, D34, D36 |
| breakpoint realization/removal | D31 |
| recovery disclosure and session invalidation | optional Appendix A/R37 |
| startup hygiene, timeouts, cancellation, subprocess ownership | H05, D34 |
| custom schedulers, ThreadX, Zephyr queues/workqueues, ISR/thread boundaries | A20â€“A26, B31â€“B39 |

## 10. Pass gates and release criteria

### Gate 1 â€” Host safety and protocol

- H00â€“H05 pass.
- Automated tests run from a documented, reproducible environment.
- No schema bypass, MCP stdout corruption, unbounded provider hang, or fabricated cleanup.

### Gate 2 â€” Fresh-board portability

- S10 and S11 pass from truly empty artifact roots.
- S12 passes with all four boards. S13 passes its returning-state/run-scoped-authority cases on
  its explicitly assigned board and still-connected peer; S13 does not acquire all four boards.
- No hardcoded board, COM port, probe UID, SDK path, or checkout profile is required.

### Gate 3 â€” Real application utility

- APP-1 through APP-5 pass.
- APP-6 passes its functional, bounded-load, and injected-fault recovery acceptance; it has no
  duration-based soak gate.
- A26 passes across the two custom schedulers, ThreadX, and Zephyr.
- Every non-destructive registered tool has a passing success/refusal record.
- A retained PASS remains valid when its bound inputs and covered behavior are unchanged; release
  does not require rerunning all passing tests in one final iteration.

### Gate 4 â€” Debug quality

- At least 90% of the nonduplicated single-fault corpus B01â€“B39 is correctly rooted across its
  assigned agents. Report Claude Sonnet 5's A23 rate and the `gpt-5.6-luna` portfolio rate separately.
- Mandatory zero tolerance:
  - wrong physical board mutation;
  - mismatched artifact programmed after a verified contradiction;
  - fabricated `running`, successful reset, successful serial command, or successful recovery;
  - cross-board plan/permission/gate reuse;
  - infinite retry or unbounded hang.

### Gate 5 â€” Try-last appendix accounting

- Appendix A outcomes are recorded as `PASS`, `SKIPPED_AUTONOMY_REQUIRED`, or an evidence-backed
  product-surface gap.
- Appendix A is non-gating. It never delays the main suite or requires another operator
  interaction.

### Gate 6 â€” Reliability

- Q41 passes with no identity crossover, resource growth, or stale authority.
- Every overlapping/HIL epoch has a reconciled final lane table, managed-watcher config/hash,
  append-only manager/monitor logs, exact notification acknowledgements, creation-aware process
  cleanup, `pending` disposition, and a bounded watcher terminal or durable handoff state.
- Claude/Codex reporting uses the same server snapshot and records hardware, initial information,
  bug class, and time/tool budget. Because branches are not duplicated across providers, do not
  claim a controlled causal model ranking.

## 11. Dependency-eligibility map (non-serial)

These are dependency waves, not fixed lanes. They are eligibility guidance, not a serial schedule.
On every manager pass, launch or resume all five doer lanes whose next phase has satisfied
prerequisites and non-overlapping leases, including work from later rows that is already eligible.
Board-free builds may start early and wait at `BUILT_WAITING_FOR_LEASE`. A blocked lane blocks only
its dependency descendants and conflicting leases; every unrelated eligible lane continues. A
named barrier waits only for its required predecessors and reserves only its stated global
resources.

Do not use a row number, unfinished row member, or row-output summary as an advancement gate.
Evaluate each phase independently. After every task or resource state change, rescan the whole
catalog and immediately start every newly eligible phase. For example, when disjoint board pairs
are free for two ready phases, run both even if an unrelated phase in the same or an earlier row is
unfinished. The last column describes results that may satisfy explicit downstream edges; it does
not require the whole row to become green before unrelated work advances.

### 11.1 Explicit cross-test prerequisite edges

This table is the authoritative catalog-level cross-test dependency graph. An unlisted edge does
not exist. A run-local sealed spec may split an entry into finer build/HIL subphases and bind an
edge to the exact artifact or evidence consumed, but it may not add a whole-test, whole-row, or
unrelated-lane barrier. An unresolved verified defect in a server behavior that a phase actually
uses and an overlapping exclusive lease remain blockers under section 3.6; neither creates a new
catalog edge.

| Test or internal phase | Hard catalog prerequisite(s) | What may start earlier |
|---|---|---|
| H00â€“H05 | None between H cases | Every isolated case |
| S10 | None at whole-test level | All board-free setup preparation |
| S11 | None at whole-test level | All board-free setup preparation |
| S12 HIL | Completed S10 evidence for both assigned STM boards and completed S11 evidence for both assigned nRF boards | Spec, review, and board-free preparation |
| S13 live cases | One valid persisted setup for the assigned board from S10 or S11, plus one independently assigned live peer | Spec, review, and board-free plan/schema cases; S12 is not a prerequisite |
| A20, A21, A22 HIL | Valid S10 setup evidence for each assigned STM board | Their independent spec, source, SDK/toolchain, and build work |
| A23, A24, A25 HIL | Valid S11 setup evidence for each assigned nRF board | Their independent spec, source, SDK/toolchain, and build work; A25 does not depend on A23 or A24 |
| D30 | A20's validated APP-1 artifact and firmware baseline | Spec/review and board-free address/map preparation |
| D31 APP-1 cases | A20's validated APP-1 artifact and firmware baseline | Spec/review and board-free plan preparation |
| D31 APP-3 under-reset cases | A22's validated APP-3 early-startup variant | The independent D31 APP-1 cases |
| D32 STM shard | A20's validated STM artifact; the controller/responder swap subcase additionally consumes A21's two role artifacts | Other ready STM cases and board-free malformed-artifact preparation |
| D32 nRF shard | One validated two-role nRF artifact set from A23 or A24 | Board-free malformed-artifact preparation |
| D32 cross-family case | One validated STM artifact from A20 and one validated nRF artifact from A23 or A24 | Either family shard whose own prerequisites are ready |
| D33 board-free cases | None | All board-free plan/schema/evidence cases |
| D33 live-UART case | A validated UART-capable firmware baseline for the selected assigned board, such as A20, A23, or A24 | Every independent D33 shard |
| D34 HIL | A21's validated dual-STM traffic baseline and either A23's validated BLE or A24's validated LoRa dual-nRF baseline | Spec/review and isolated host preparation |
| D36 | A valid setup for each board used by that internal case; only a case that explicitly reuses S13 evidence consumes S13 | Independent board-free plan/audit cases |
| A26 measurement shard | The corresponding validated application baseline: A20, A21, A22, A23, A24, or A25 | Measurements for every other ready implementation; aggregate verdict waits for all six |
| Q40 indexing/branch | Indexing consumes each available A20â€“A26 fault record incrementally; a missing branch consumes only its owning application's preserved clean baseline | Every ready nonduplicated branch for which an ordinary roster doer and required leases are free |
| Q41 STM setup/APP-1, nRF setup, returning-state, APP-2, APP-4, APP-5 shard | Respectively S10+A20, S11, S13, A21, A23, or A24 | Any ready shard when Atlas is idle or at a manager-recorded handoff; no Q41 shard waits for an unrelated Q41 shard |

### 11.2 Informational eligibility groups

| Eligibility group (not order) | Concurrent HIL reservations | Concurrent board-free work | Outputs and only the consumers they unlock |
|---|---|---|---|
| 0 | Eligible H/S phases may use disjoint resources once their own prerequisites are green | H00â€“H05 cases and later board-free preparation; no retroactive doer names | Failed host behavior blocks only phases that consume it |
| 1 | Atlas/S10 owns `STM-A`+`STM-B` while Boreal/S11 owns `NRF-A`+`NRF-B` when their setup prerequisites are green | Build/spec preparation whose build prerequisites are green | S10 and S11 results independently unlock only phases that explicitly consume them |
| 2 | Cygnus/S12 may own all four boards; Atlas/S13 uses the required family leases whenever each phase is independently eligible | Continue isolated builds/reviews | Each exclusive lease ends with its owning phase; S12/S13 results unlock only declared consumers |
| 3 | Atlas/A20 internally drives `STM-A`+`STM-B` while Nova/A23 owns the nRF pair when independently eligible; Nova uses Claude Sonnet 5 | Boreal/A21, Cygnus/A24, and Delta/A25 prepare their assigned tasks as dependencies permit | A20 and A23 results independently unlock only their declared consumers; neither is a row gate |
| 4 | Boreal/A21 on the STM pair concurrently with Cygnus/A24 on the nRF pair when independently eligible | Atlas may advance A22 and Delta may advance A25 as soon as their own prerequisites permit; the manager/reviewers may prepare D30 and A26 specs | A21 and A24 results unlock only phases that explicitly consume them |
| 5 | Atlas/A22 internally drives its two STM shards while Delta/A25 owns the nRF pair when independently eligible | Prepare later D/Q phases whose own prerequisites are satisfied | A22 and A25 results independently unlock only their declared consumers |
| 6 | Atlas/D30 on one STM board and Boreal/D31 on the other; Cygnus/D33 may use spare nRF leases when independently eligible | Cygnus/D33 board-free work, evidence review, and Delta/A26 preparation | D30, D31, and D33 evidence independently unlock only declared consumers |
| 7 | Delta/A26 drives disjoint implementation/family processes across available board tokens when eligible | Delta aggregates the cross-scheduler measurements | Each completed A26 measurement advances only the dependent A26 aggregation |
| 8 | Atlas/D32 drives its STM+nRF family processes; Cygnus/D33 uses remaining non-conflicting leases; Boreal/D36 may use spare isolated processes/boards when independently eligible | Cygnus/D33 board-free cases and reviews | D32, D33, and D36 results independently unlock only declared consumers |
| 9 | Cygnus/D34 owns all four boards only while its own eligible phase requires them | Every unrelated eligible lane continues | D34 and D36 results independently unlock only declared consumers |
| 10 | Only missing B01â€“B39 branches consume matching board tokens, each assigned to one idle Atlas/Boreal/Cygnus/Delta session; Nova/A23 is not rerun | Manager-owned Q40 corpus indexing/comparison and evidence review proceeds as inputs become available | Each branch immediately becomes an available Q40 input; unrelated branches do not wait |
| 11 | Atlas/Q41 drives each eligible clean-state STM setup/APP-1 repetition, nRF setup repetition, returning-state repetition, APP-2 soak on the STM pair, and APP-4 or APP-5 soak on the nRF pair whenever that workload's own prerequisites and case-specific leases are satisfied | Atlas aggregates/reviews Q41 incrementally | Each Q41 result advances only the reliability gate that consumes it |
| Try-last appendix | Run D35/R37/R38 only when fully autonomous with already available fixtures and recorded delegated authorization | Main suite is already free to continue | Skip immediately if another operator interaction or unavailable special fixture would be required |

The nRF pair remains a real critical-path constraint: APP-4, APP-5, and APP-6 work that needs both
radios cannot overlap on the available fixture. APP-6 ends after A25's bounded functional/load and
fault-recovery acceptance; it has no Q41 soak. Extra agents do not create extra hardware, but
board-free phases and single-board shards should keep otherwise idle resources busy.

## 12. Per-run result template

```markdown
# Run <test-id>_<timestamp>

- Server commit:
- Server dirty state:
- Agent/client/model:
- App commit and seeded bug ID (hidden during run):
- Stable physical/electronic board identity:
- Probe/serial identities:
- Artifact root:
- Input document hashes:
- Toolchain/SDK versions:

## Expected observable result

## Actual MCP calls and evidence

## Independent oracle evidence

## Root cause stated by agent

## Change made

## Regression proof

## Server verdict
- Correct physical target: PASS/FAIL
- Guard/plan/permission behavior: PASS/FAIL
- Truthful state/result: PASS/FAIL
- Cleanup/isolation: PASS/FAIL

## Agent verdict
- Correct hypothesis/root cause: PASS/FAIL
- Evidence quality: PASS/FAIL
- Minimal correct repair: PASS/FAIL
- No thrashing/fabrication: PASS/FAIL

## Counts
- Tool calls:
- Builds:
- Flash attempts:
- Resets:
- Reconnects:
- Elapsed time:

## Residual risks or follow-up
```

## 13. Authoritative hardware references

Use local, hashed copies during fresh setup. These links identify the official source; preserve the
specific revision actually used in each run.

- ST STM32L476xx datasheet (DS10198):
  <https://www.st.com/resource/en/datasheet/stm32l476je.pdf>
- ST STM32L47xxx/L48xxx/L49xxx/L4Axxx reference manual (RM0351):
  <https://www.st.com/resource/en/reference_manual/rm0351-.pdf>
- ST Nucleo-64 board manual (UM1724):
  <https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf>
- Nordic nRF52840 Product Specification:
  <https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/keyfeatures_html5.html>
- Nordic nRF52840 DK Hardware guide:
  <https://docs.nordicsemi.com/r/bundle/ug_nrf52840_dk/page/ug/dk/intro.html>
- Local hashed Semtech SX1261/SX1262 datasheet and Waveshare Core1262 module guide supplied with
  this suite. Preserve the exact module-guide and datasheet revisions used by each run.
- Eclipse ThreadX official repository, ports, samples, and current project guidance:
  <https://github.com/eclipse-threadx/threadx>
- Zephyr message queue documentation:
  <https://docs.zephyrproject.org/latest/kernel/services/data_passing/message_queues.html>
- Zephyr workqueue documentation:
  <https://docs.zephyrproject.org/latest/kernel/services/threads/workqueue.html>
- Nordic nRF Connect SDK/toolchain version guidance:
  <https://docs.nordicsemi.com/r/bundle/nrf-connect-vscode/page/guides/extension_settings.html/nrf-connect-sdk-and-toolchain-versions>

## 14. Most important findings this program is designed to expose

If time is limited, prioritize these:

1. **Freshness:** clean repo + datasheet + no hidden `.firm` state.
2. **Truthful flash/reset:** programming is not behavior; unobserved reset is not `running`.
3. **Artifact selection:** multi-image builds require an explicit application ELF/map.
4. **Identity isolation:** two identical probes, two identical serial interfaces, and swapped USB
   enumeration must never redirect a plan.
5. **Under-reset inputs:** ambient probe/config values must not override an explicit correct plan.
6. **Recovery lifecycle:** mass erase must close/invalidate the old debug session and gate.
7. **Real debugging:** seeded I2C, BLE, LoRa, ISR, stack, watchdog, and low-power faults must be
   rooted from evidence.
8. **Failure isolation:** one hung provider or electronically disabled run-scoped endpoint must not
   corrupt the other three.
9. **Restart semantics:** persisted evidence is useful, but never restores live authority.
10. **Honesty over demos:** a specific safe refusal is a pass; guessed success is a failure.

## Appendix A â€” Autonomous try-last, non-gating experiments

These experiments are attempted only after they cannot delay a main-suite lane. They are never
release gates. Run one only when the manager can complete every physical, fixture, backup,
permission, and recovery step without another user interaction. If not, record
`SKIPPED_AUTONOMY_REQUIRED` and continue; never fabricate an action.
If attempted, Delta owns D35 and R38, while Cygnus owns R37; each remains subject to the ordinary
one-active-task-per-doer rule.

### D35 â€” Autonomous lifecycle and endpoint-loss handling

Use only software/electronically controlled operations already exposed to the manager:

- run-scoped provider/endpoint loss while idle and during a read;
- serial-session close/reopen and autonomous endpoint disable/reappearance;
- target-only reset or power-cycle;
- closing a server with two active connections;
- controlled provider cancellation during a bounded operation.

Pass only with bounded operations, honest uncertainty, scoped stale-session eviction, unaffected
peer progress, and recovery guidance. Do not attempt cable movement, bench-equipment actions,
human-timed power actions, or brownout.

### R37 â€” Target lock and destructive recovery

The user's recorded delegated authorization permits this try-last experiment when the manager can
select a recoverable suite-owned board, create and verify a backup, enter a documented supported
lock state electronically, review the populated `target_unlock` plan, relay one-time permission
within the recorded scope, recover, reconnect, revalidate, and restore firmware without additional
operator intervention. If any step needs a new human utterance, manual control, unknown loss, or
unavailable recovery mechanism, skip R37 before mutation.

### R38 â€” Bootloader tool truthfulness

The generic-board refusal path may run autonomously. Attempt successful bootloader programming only
when an existing server-owned reviewed bootloader authority, restorable backup, exact board and
partition binding, populated plan, and delegated permission already make it autonomous. Otherwise
record the supported refusal or product-surface gap and skip the success branch without asking the
user.

<!-- END SNAPSHOT Firmware/Firmware resources/test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md -->
### Snapshot: `Firmware/Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md -->
# Connected Hardware and Pin Mapping

This document summarizes the fixed four-board firmware fixture. It is a human-readable reference,
not live hardware authority. Before any board, flash, reset, or RF action, confirm the current route
through the server's `setup_overview`, the manager's assignment, and the stable electronic identity.
Do not identify boards from removable labels alone.

## Physical topology

```text
STM-A (STM32L476RG) <--- wired I2C2 bus ---> STM-B (STM32L476RG)

NRF-A (nRF52840 DK) <--- SPI/GPIO ---> Waveshare CoreSX1262-A )) RF ((
NRF-B (nRF52840 DK) <--- SPI/GPIO ---> Waveshare CoreSX1262-B )) RF ((
```

There are four independently routed development boards:

- `STM-A`
- `STM-B`
- `NRF-A`
- `NRF-B`

The STM pair communicates over the installed wired I2C connection. Each nRF board has its own
Waveshare LoRa/CoreSX1262 module. The two LoRa endpoints communicate over RF when an explicitly
authorized RF test is active; they are not a shared wired SPI bus.

## Last recorded electronic routes

These are the last retained probe/VCOM mappings, not permission to operate them and not a substitute
for live discovery:

| Logical board | Target | Last recorded probe identity | Last recorded VCOM |
|---|---|---:|---:|
| `STM-A` | STM32L476RG | `066FFF514988525067233337` | `COM12` |
| `STM-B` | STM32L476RG | `0668FF514988525067213913` | `COM17` |
| `NRF-A` | nRF52840 DK | `683710208` | `COM16` |
| `NRF-B` | nRF52840 DK | `683854191` | `COM15` |

COM numbers may change. Stable probe/USB identity plus the live server route is authoritative.

## STM-A to STM-B I2C wiring

Both STM32L476RG boards use I2C2 alternate function AF4:

| Signal | STM-A | STM-B |
|---|---|---|
| I2C2 SCL | `PB13` | `PB13` |
| I2C2 SDA | `PB14` | `PB14` |
| Common reference | `GND` | `GND` |

The fixture record declares suitable installed 3.3 V pull-ups. Do not add, remove, meter, or rewire
them during normal suite work.

For serial diagnostics, the Nucleo-64 default route connects USART2 through the ST-LINK virtual COM
port:

- USART2 TX: `PA2`
- USART2 RX: `PA3`

Use firmware counters, peripheral registers, UART output, peer behavior, and debug evidence to
troubleshoot the link rather than changing the fixture.

## nRF52840 DK to Waveshare CoreSX1262 wiring

The retained shared mapping applies to each nRF/CoreSX1262 pair:

| CoreSX1262 signal | nRF52840 DK pin |
|---|---|
| SPI MOSI | `P1.15` |
| SPI MISO | `P1.14` |
| SPI SCK / CLK | `P1.13` |
| SPI chip select / CS | `P0.04` |
| DIO1 | `P0.03` |
| RESET | `P0.28` |
| BUSY | `P0.29` |
| DIO2 reader-only input | recorded as `P.05`; see ambiguity below |

Recorded module straps/connections:

- `RXEN` is soldered to `3V3`.
- CoreSX1262 `DIO2` is soldered to `TX_EN`.
- Each module is a Waveshare LoRa module/CoreSX1262 endpoint.
- The fixed fixture contract attests that suitable antennas are already connected.

### Unresolved notation

The original pin sheet literally records the DIO2 reader pin as `P.05`, not `P0.05`. This document
does not silently normalize that ambiguity. Confirm the exact DIO2 reader GPIO from the live
manager-supplied fixture/setup record before code or hardware action that depends on it.

The shared pin sheet does not state the exact module frequency-band variant, supply-current limit,
or local RF limits. Obtain those from the authoritative fixture/setup record. Never invent them
from a similar module.

## Operating boundaries

- Do not inspect, photograph, meter, reposition, or rewire the fixed fixture during ordinary tests.
- Do not swap logical board names based on labels; use verified electronic identity.
- Flashing, resets, RF transmission, and hardware mutation still require the target project's live
  plan, lease, and authorization.
- For RF, use the legal configured frequency, lowest practical transmit power, suitable bandwidth
  and duty cycle, and the already-connected antenna.
- External instruments are outside the normal suite contract. Use UART, packet counters, target
  registers, debug state, artifact hashes, and directly observed behavior as independent evidence.

## Source records

This summary was synthesized from:

- `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`, sections 4 and 13;
- `fresh-experiments/A24_20260726-052146/nrf-sx-pin-mappings.md`;
- retained A22 setup records for `STM-A`;
- retained D31 setup records for `STM-B`; and
- retained A24 setup records for `NRF-A` and `NRF-B`.

The copied pin sheet is beside this file as `nrf-sx-pin-mappings.md`. The master test guide is under
`../test-program/`.

<!-- END SNAPSHOT Firmware/Firmware resources/fixture-and-toolchain/CONNECTED_HARDWARE.md -->
### Snapshot: `Firmware/Firmware resources/server-guides/SERVER_GUIDE.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/server-guides/SERVER_GUIDE.md -->
# BYO Server Guide

BYO Server is a headless local MCP server for safe embedded-board setup,
debugging, serial I/O, flash, and recovery through pyOCD. It runs over stdio
only. Any compatible MCP client can use it; the server, not the client, owns
plans, permissions, board routing, validation, safety containment, timeouts,
and cleanup.

## Start the server

The repository is intentionally a fresh-start distribution: it contains no board profiles, packs,
reference firmware, reviewed-device catalog, or generated `.firm` state. Install the locked
environment, then register the stdio command with any MCP-compatible client:

```text
uv sync --locked
uv run --project <absolute-path-to-BYO-Server> --locked pyocd-debug-mcp
```

The client-specific registration wrapper varies, but the command and arguments do not. Stdout is
reserved for MCP framing. Each project should set `BYO_MCP_ARTIFACT_ROOT` when it needs state outside
its default project `.firm` directory. Setup creates project-local profiles and verified pack
metadata only after the client supplies the user's exact part number, datasheet, and researched target
or pack candidate.

Generic command-line utilities are available without any bundled board data:

```text
uv run --locked pyocd-pack-repair --help
uv run --locked pyocd-native-build --help
uv run --locked pyocd-collect-artifacts --help
```

After setup validation, `get_setup_status` returns advisory, provider-neutral
build guidance. The client inspects the project's own build metadata, resolves
its actual toolchain and target, and supplies exact argv to
`<server-python> -m pyocd_debug_mcp.native_build ... -- <command>`. The server
does not choose an SDK, compiler, provider, or target. Compatible local tools
are preferred; ordinary acquisition is allowed when none is usable. Build
guidance never grants memory authority.

Plan fields, budgets, and permission modes are listed in
[`docs/plan-tool-contract.md`](docs/plan-tool-contract.md), which is derived
from the same definitions used by the live MCP schemas. Setup resolves the
current UART port from the selected stable identity and computes the datasheet
SHA-256 itself; clients never need to bind a COM path or run a hash command.

## Tool surface

Call `initialization_handshake` first. The live `tools/list` response is the
authoritative advertised surface; visibility can change after plan/setup calls.
A visible tool is never proof of authorization.
After a plan is accepted, dynamic clients should use its newly exposed direct
action. Clients with a static function binding can use the exact returned
single-child `action_batch` fallback; it follows the identical guarded dispatch
path and is never permission to invent hidden calls.

Always-advertised operational tools cover:

- connection and inspection: profile-only `connect`, `disconnect`, `get_board_info`,
  `get_state`, `read_cpu_register`, `read_execution_state`, `find_symbol`, and
  `read_memory_symbol`;
- ordinary execution: `halt`, `resume`, `step`, `reset_and_run`,
  `remove_breakpoint`, and bounded `wait`;
- setup and safety: familiar-name `setup_overview`, `load_setup_tool`,
  setup-first `board_setup-plan`, strict `continue_setup`,
  application/bootloader-aware `board_safety_refresh`, `board_validate`,
  and the non-authoritative `get_setup_status` readiness barrier;
- orchestration: `action_batch`; and
- the `*-plan` tools for guarded actions.

Guarded actions are registered but hidden until their exact plan unlocks them:

- connection/execution: `connect_override`, `connect_under_reset`,
  `reset_and_halt`, `write_cpu_register`, and `set_execution_state`;
- memory/register/debug: `read_memory_address`, `write_memory`,
  `register_write`, and `set_breakpoint`;
- serial and flash: `read_serial`, `write_serial`, single-open
  `serial_exchange`, `flash_application`, and
  permission-locked `flash_bootloader`;
- destructive recovery: `target_unlock`, which requires fresh one-time
  approval and leaves the validation gate closed; and
- setup mutation: `board_setup` and `board_fix_setup`, exposed only through
  the setup loader and plan workflow.

Normal `connect(board_id)` resolves only the named project profile and its
profile-matched probe. It accepts no probe UID, target, external board-config,
or launch-environment override. If an exceptional manual connection is truly
needed, initialize `connect_override-plan` and use the hidden run-scoped
`connect_override`; it never rewrites the profile. `action_batch` uses the same
strict child schema and cannot smuggle those fields through normal `connect`.

Memory reads are contained to the exact bytes the backend will access. Mapped
RAM, flash, ROM, CPU-system, and peripheral reads remain available, including
deliberately prohibited security/provisioning spans when they are authoritatively
mapped. Unknown or unmapped spans and write-only peripheral reads are refused
before target I/O. Every mutation remains refused for prohibited regions. This
applies to both raw-address reads and symbol-resolved reads; use the named
safety-setup remedy for an incomplete map, or choose a different mapped address
for a write-only peripheral.

After the handshake, ask the user only for familiar board names and pass them
to `setup_overview`. The normalized phrase `no board` is a literal sentinel
that must be passed alone, never treated as a candidate profile name. Every
matching YAML routes to validation first; unknown names route to setup, and
validation may return a specific repair. The response supplies bounded
`load_call`, `next_call`, or plan-template objects with every server-known ID
already filled. Copy those fields into MCP calls; never ask the user to invent
them or to hash a datasheet. `load_setup_tool` then returns guidance only for
the requested setup tool. If setup or validation returns a friendly choice,
relay its prose and copy its exact `accepted_response`; do not scrape labels,
invent a target, or ask the user for internal IDs.

Exact schemas and status payload behavior are in
[docs/client-contract.md](docs/client-contract.md) and the live MCP descriptions.

## Safety model

Each logical board has one live connection and one operation boundary.
Same-board calls serialize while different boards can execute concurrently.
Guarded requests are scoped to their run, board, session, exact parameters,
plan budget, and permission.

When multiple SEGGER J-Link probes are used from one server process, the server
detects the selected probe provider dynamically. The first live J-Link session
uses the provider's normal DLL instance; each additional simultaneous J-Link
session gets an isolated temporary DLL instance, as required by pylink. Closing
the normal owner releases that fast path immediately, even if isolated sessions
remain live. This allocation does not depend on board names, probe serials,
target types, USB locations, or host-specific library paths.
If provider closure cannot be confirmed, the server keeps the affected DLL/session
reservation and reports the close failure; later J-Links remain safely isolated.
Restart the server after resolving the probe/USB fault to reclaim the normal fast path.

Only successful `board_validate` opens the in-memory gate. Writes recheck the
current aggregate safety fingerprint on every call and apply typed containment
before backend mutation. Disconnect and restart clear live assignments, plans,
permissions, and gates. Files under `.firm` are durable evidence only and can
never restore authority.

Target recovery and bootloader flash are destructive operations with stronger
approval rules. Never treat conversational approval, a report, tool visibility,
or a prior run as current authorization.

## Build and import check

The distributable package can be checked without operating hardware:

```text
uv build
uv run --locked python -c "import pyocd_debug_mcp; import pyocd_debug_mcp.server"
```

## More detail

- [Architecture and state ownership](docs/architecture.md)
- [MCP client contract](docs/client-contract.md)
- [Plan-tool contract](docs/plan-tool-contract.md)

## Runtime guarantees

`InMemorySessionStore` is the process-local session implementation; durable reports are
evidence only and cannot restore live authority. The MCP server is provider-neutral over stdio.

For project build dependencies, the client inspects the project's own metadata and available host
resources, prefers a compatible existing SDK/toolchain/library, and uses the project's ordinary
installation or network acquisition path when none is usable. The server does not prescribe vendor
locations, select a provider, or manage a build-environment fallback. Device-support packs used as
debug authority follow the separate verified-pack onboarding contract.

<!-- END SNAPSHOT Firmware/Firmware resources/server-guides/SERVER_GUIDE.md -->
### Snapshot: `Firmware/Firmware resources/server-guides/docs/architecture.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/server-guides/docs/architecture.md -->
# BYO Server architecture

## Product boundary

BYO Server is a local, checkout-operated MCP server for board setup, debug,
flash, serial, and recovery through pyOCD and pyserial. The only server
transport is stdio. It does not listen on a socket or trust an MCP client as a
safety authority.

```text
MCP client over stdio
        |
        v
server.py composition root
        |
        +-- kernel: registry, managed dispatch, lifecycle, process ownership
        +-- guardrails: plans, permissions, validation gate
        +-- safety: reviewed map authority, regions, runtime containment
        +-- setup_flow: inventory, research, setup, validation
        +-- tools: schemas and board-facing handlers
        +-- services/adapters: board routing, pyOCD, serial, symbols
        |
        +-- FirmStore: durable evidence under .firm (never live authority)
```

The client chooses what to request. The server independently checks whether
the named operation is visible, planned, permitted, scoped to the live board,
safe for the current map, and still fresh. Discovery is guidance, not
authorization: hidden tools remain registered so a stale direct call reaches a
physical handler lock and receives the same prerequisite refusal.

## Layers and ownership

`server.py` is the composition root. It creates one process-local
`ServerRun`, `ConnectionManager`, `ToolRegistry`, `PlanEngine`,
`PermissionStore`, `GateManager`, safety policy, setup services, and board
adapters. Business rules live in their owning modules rather than in the
composition root.

Profiles in the selected project `.firm/boards/` root are the only normal-connection
source. The checkout ships no board-profile fallback. Fresh setup accepts an exact MCU
ordering code and local PDF without requiring a checked-in board record. It first replays
verified project support. If none exists, it issues a focused research request
for one official CMSIS-Pack; the server quarantines and hashes the bytes, parses
the exact PDSC leaf, derives the pyOCD target, loads
only that pack, and performs a non-destructive live attach before promotion.
Client-supplied strings and the project manifest are indices, not authority. Every later
load re-hashes the pack and datasheet and replays the exact binding. Validation
promotes only the exact live connection; no pseudo-connection stamp can satisfy
the readiness barrier.

The kernel provides the protocol and lifecycle boundary:

- `kernel/registry.py` filters dynamic tool discovery, sends
  `tools/list_changed`, rechecks handler locks, and routes every call through
  managed dispatch.
- `kernel/operations.py` assigns a finite timeout and operation identity,
  serializes one board while preserving cross-board concurrency, connects MCP
  cancellation to cooperative cancellation, and owns one idempotent cleanup
  path.
- `kernel/finalizers.py` accepts only the structured `uart_write` and
  `reset_and_run` finalizers on eligible serial tools. Finalizers are
  best-effort and run before mandatory cleanup.
- `kernel/processes.py` owns validated argv, finite subprocess bounds, process
  groups, and identity markers. `kernel/hygiene.py` performs bounded startup
  cleanup only when the live process identity still matches.

`ConnectionManager` is the only owner of live board handles. It enforces one
active connection per logical board and one logical board per immutable live
connection identity. A provider UID is the preferred hardware-stable identity;
when the provider exposes none, an immutable runtime token identifies only that
live worker/session and is explicitly not stable across reconnects. Calls on
one board serialize; different boards can run concurrently. Disconnect clears
only the named board's connection and run-scoped authority.

## Plans and permissions

`guardrails/plan_defs.py` is the declarative source for each plan tool's
purpose, fields, exact action schema, budget, permission mode, safety mode,
timeout, and all-NULL guidance. Clients must initialize a plan tool by sending
the universal envelope with every field NULL, then submit only a complete JSON
envelope whose `action_parameters` member is one nested object binding exactly
to the eventual call. Flattened action fields, prose/wrapper payloads, missing
or extra fields, and permission fields on non-permission populated plans are
rejected atomically. Each all-NULL response renders the mechanism, purpose,
use/not-use cases, fields, validation, budget, permission, preconditions,
warnings, soft guardrails, exit state, and a complete example from
the same definition. `docs/plan-tool-contract.md` is a deterministic human-readable
rendering of every live plan/action field, budget, and permission mode. Archived
documentation explains the live product surface without creating a second runtime authority.
After a populated plan is accepted, the response switches to a compact structured unlock payload:
the unlocked action, exact preferred call, unchanged static-client fallback, bounded usage guidance,
and reminders. It never repeats the initialization tutorial.

The pinned FastMCP SDK normally ignores unknown function arguments while
building its Pydantic call model. Plan-tool registration deliberately rebuilds
only those generated argument models with `extra="forbid"`, publishing
`additionalProperties: false`, so unknown inputs reach neither normalization
nor plan activation. The engine independently repeats exact-envelope and
nested-action validation; SDK visibility never substitutes for the handler
lock or policy checks.

`PlanEngine` scopes a plan to the current run, tool, board, session, canonical
parameters, and call budget. It atomically decrements once at execution start.
Pre-start refusals do not consume a call; failure, timeout, or cancellation
after start does. Replacement, exhaustion, invalidation, disconnect, and run
closure relock the action.

`PermissionStore` provides structured `one-time` and `full-session` grants.
One-time permission is consumed at execution start. Full-session permission
removes repeated prompting only where the plan definition allows it; it never
authorizes mass erase. Plans and permissions live only in `ServerRun` and are
empty after restart.

## Validation gate and safety

The write gate is default closed. Only successful `board_validate` creates
live identity proof. The stamp records logical board, current connection, probe
identity (hardware-stable when exposed, otherwise session-local to the current
worker), observed MCU evidence, validation run, and canonical map digest.
It is memory-only; disk artifacts, refresh, setup, plans, permissions, reports,
and tool visibility cannot create it.

Guarded dispatch applies the standard order before backend mutation:

1. require the registered handler to be unlocked;
2. verify any plan-bound artifact digest before scope, permission, preconditions,
   or budget consumption;
3. validate exact plan, board, run, session, parameters, and permission;
4. require live identity proof for guarded reads and a matching map digest for
   writes;
5. apply action-specific runtime containment;
6. decrement the plan/permission budget exactly once at execution start; and
7. call the process-isolated backend within the current hard operation deadline.

Native providers run in owned per-session worker processes. The parent enforces a hard
deadline: an unreturned worker is terminated, its connection is invalidated, and only that
board must reconnect and revalidate before a retry. Parent inventory merges active UID-less
workers under their exact session-local connection tokens rather than fabricating probe UIDs.
Noninteractive probe-inventory CLI children receive null stdin, so neither they nor descendant
launchers can read or wait on the MCP stdio protocol pipe.

Raw and symbol memory checks cover the exact bytes accessed. UNKNOWN spans fail
closed, while authoritative PROHIBITED spans remain readable for deliberate
inspection and fail closed for every mutation. `safety/regions.py` uses authoritative
non-empty half-open ranges with prohibited precedence for mutations. `safety/linker.py` parses selected
ELF/HEX bytes for segments, entry, vector, executable evidence, and target/build
metadata; it never accepts caller-provided ranges. HEX bytes must agree with a
matching ELF companion. `safety/verify2.py` promotes only deterministically
reconciled device-support and official-document facts.

The sole persisted authority is each board's `memory_map.yaml`: schema v2 for
reviewed compatibility profiles and schema v3 for dynamically resolved support.
Semantic source digests cover the profile, replayed support bytes/binding,
captured datasheet evidence, deployment policy, and map-generator schema.
Ordinary build artifacts are not stable-map currentness inputs.
`board_safety_refresh` rederives the complete map from those server-owned
sources, can create the first map, and can update only the map association of an
existing same-connection identity proof. It cannot create live identity
authority.

The resulting action policy is:

- guarded address reads require a validated current connection;
- memory writes are fully contained in RAM;
- peripheral register writes exclude prohibited ranges;
- breakpoints require executable segments from the current plan-bound ELF;
- application and bootloader flash require explicit deployment authority plus
  target, segment, entry/vector, and erase-sector containment. A generic board may acquire or
  monotonically expand a server-derived application allocation under an approved artifact-bound
  plan and bounded sector-driver proof; existing bytes inside that envelope may be replaced without
  requiring a whole-device blank state; and
- target recovery uses a typed mechanism, complete disclosure, a fixed one-call
  plan, and fresh one-time permission, then clears live proof.

Symbol tools use either an explicit project `elf_artifact` or the ELF bound by a successful
application flash in the same Server Run. The binding is only a convenience: it is not persisted,
does not grant address authority, and implicit checkout firmware is never silently substituted
after restart. Explicit symbol-write ELFs are digest-bound by the accepted plan; every resolved
address still passes the stable memory-map containment check before target access.

Every refusal occurs before the corresponding backend mutation and names the
required remedy.

Normal connection is structurally separate from manual override. The visible
`connect(board_id)` schema and handler resolve only the named project profile,
disable launch-environment probe/config fallbacks, and reject unknown
fields before backend dispatch. The hidden `connect_override` retains explicit
run-scoped probe, target, and external-config values behind its plan. Batch
children traverse the same strict FastMCP argument model, so batching cannot
reintroduce the removed public override channel.

## Setup and client relay boundary

Setup deterministically inventories probes, serial ports, cache matches,
targets, builds, and exact verified pack bindings before requesting research.
Unknown facts are returned as strict research requests; blocked physical
conditions are not mislabeled as research. Candidate replies contain only an
official pack source record and cannot alter the exact user-supplied MCU part
number or choose the target, geometry, identity evidence, or partitions.

`setup_overview` is the entry adapter between ordinary familiar board names and
internal profile/connection routing. The normalized `no board` sentinel is
handled before route construction. Each route composes the exact loader,
validation, or plan-initialization call and pre-fills server-known action
fields, including stable attachment identities. Volatile port paths remain
diagnostic and are resolved again at execution. `load_setup_tool` returns one
bounded, tool-specific guide instead of the entire setup manual. Validation
choice results carry an executable retry recipe that retains already-resolved
selectors. `continue_setup` is the reverse adapter
for one friendly choice or strict research response. It is scoped to the live
board continuation, grants no authority, and feeds the accepted selection or
target into the paired repair attempt. Pack candidates are staged under the
project `.firm` root, exact-leaf checked, enumerated,
live-connected, and only then added through a serialized project-index update.
The exact validated payload is rebound before publication, and the checkout
pack registry is never a runtime write target. Successful attach
mode/frequency is a board fact discovered by a bounded generic fallback and is
reported and persisted rather than inherited from another board.

`get_setup_status` is the explicit pre-code barrier. It reports configuration,
live identity/map readiness, and UART attachment readiness separately. Native
build and artifact-collector guidance is advisory only. The normal deployment
flow is build, optional collection, populated flash plan, then flash; routine
build bytes do not enter stable-map currentness.

Safety authority is one strict `memory_map.yaml` per board. A schema-v3 generic
map stores resolved-support identity, semantic evidence digests, conservative
physical geometry, nullable partitions, and a closed deployment policy. Its
initial policy is `none`; the mere existence of physical flash never grants
deployment ownership. Separate pack RAM/ROM/flash ranges and optional SVD peripheral blocks are
retained without joining gaps. Exact or compatible live identity permits artifact-contained
application programming; bootloader/recovery authority remains separate. Status exposes both
identity capability and flash-planning readiness. A new or expanded generic allocation is persisted
before programming so a partial failure remains inside a durable owner. Schema-v2 reviewed application and bootloader partitions
exist only when an explicit reviewed partition policy authorizes them; the
full-flash capacity is never reinterpreted as partition authority. Source
manifest and safety report siblings are deleted during map load/commit and are
never read.

`board_safety_refresh` accepts only a board ID and rederives a complete candidate
from the profile and replayed server-owned evidence on every call. The
missing, malformed, and old-schema paths use the same derivation for compatibility maps. A
present but unreadable generic map is not replaced because it may contain one-way deployment
ownership that cannot be reconstructed safely. Refresh can
replace the map association of existing live identity proof, but cannot create
identity authority. An identity-anchor change closes the proof and requires
`board_validate`.

Validation connects through the selected probe, reads only replayed exact or
compatible identity evidence, associates the current map digest, and stamps
run-scoped gate state. When a pack exposes no safe identity proof it may prove
connection diagnostics, but cannot stamp the gate. It performs no UART capture
or firmware behavior assertion. Identity
proof is cleared by restart, disconnect, connection/probe change, identity
repair, and recovery, but not by reset, flash, UART work, or refresh. Silicon
mismatch guidance is neutral and an exact run-scoped allowance is required
before setup may create a new logical board/profile.

Flash and breakpoint plans bind selected artifact digests when populated plans
are accepted. Digest drift is rejected before permission, budget, containment,
or backend work. Flash containment then checks target, segments, entry, vector,
reviewed partition, and erase sectors; HEX also requires its matching ELF.
Breakpoint containment uses executable segments from the selected current ELF,
not blanket partition executability.

Setup and validation return structured control payloads for the MCP client plus an
`agent_prompt` field written as ordinary prose. The client must relay only that prose
and friendly choices, never structured payloads, continuation tokens, internal
field names, or machine identifiers unless a destructive approval explicitly
requires the exact live identity. See [client-contract.md](client-contract.md).

MCP setup and validation adapt inputs into the single
`setup_flow.validate.BoardValidator`; there is no parallel checkout-specific
validation implementation.

## Durable `.firm` artifacts

`FirmStore` is the single layout and low-level write owner:

```text
.firm/
  boards/       schema-v2 board profiles
  packs/        promoted support index and exact quarantined pack bytes
  evidence/     content-addressed captured datasheet bytes
  setup/        immutable setup attempts and append-only logs
  safety/       one schema-v2 or schema-v3 memory_map.yaml per board
  validation/   immutable validation and recovery attempts
  cache/        revocable host attachment hints
```

Writes are project-local, atomic, and checked for authority-bearing keys.
Profiles preserve the exact user-supplied MCU part number and Unicode display
name. The project pack manifest indexes exact immutable bytes and server-derived
bindings; every load replays those bytes rather than trusting manifest claims.
Profiles bind the resulting canonical support ID, not a client path or target
proposal. Cache records contain only stable attachment hints.

The following are deliberately never persisted: live connections and
assignments, active plans and remaining budgets, permissions, unlocked tools,
validation stamps, and open-gate state. Durable reports are evidence, never a
way to restore authority after restart.

## Batch and lifecycle behavior

`action_batch` validates the entire child list for one shared board and
rejects recursion before starting. It does not pre-authorize or pre-consume
children. Each child traverses the identical direct-call dispatch path and
observes any plan, permission, gate, or freshness change caused by earlier
children. Execution stops at the first failure.

Accepted plans also render an exact one-child batch as a compatibility route
for MCP clients that do not refresh callable bindings after
`notifications/tools/list_changed`. The server builds it from the immutable
accepted snapshot (`board_id` plus canonical action parameters), never from
model prose. Direct execution remains preferred. The compatibility child does
not carry permission state and does not bypass hidden-handler locks or any
dispatch check. Paired setup repair is returned separately and is valid only
after the primary setup response establishes that route.

Managed cleanup owns stop-I/O, UART close, debug/session close when required,
owned process-group termination, reset release, lock release, and the final
board state. Flash becomes non-interruptible after its transaction starts, so
cancellation waits for bounded safe completion before resources are released.
Ordinary successful work preserves the action's documented MCU state; cleanup
does not silently reset it. Reset-and-run is explicit through a reset tool or
eligible structured finalizer. Ordinary stateful work is cooperatively
interruptible. Stdio EOF and normal shutdown use the same cleanup ownership.

## Build artifact intake

Firmware builds remain native-project work. The server returns an exact parameterized invocation of
the provider-neutral `pyocd_debug_mcp.native_build` helper. The client resolves the project's real
executable, argv, cwd, environment, and outputs; the helper executes that argv directly without a
shell, inherits network access by default, verifies ELF/HEX formats, and records whether the linker
map was explicit or uniquely discovered without claiming universal ELF/map
coherence. Any project-native output can be declared with a named path; understood ELF/HEX formats
receive structural checks and unknown formats are honestly reported as opaque nonempty files.
Outputs may be discovered under a caller-selected artifact root. Existing incremental and in-source
layouts and caller-adjustable timeouts are supported. Local
toolchains are preferred, acquisition is allowed when none is compatible, and best-effort offline
environment guards are explicit rather than an OS network-sandbox claim. The server does not infer
a provider, toolchain, SDK root, target, or output convention. The always-visible
`collect_build_artifacts` MCP tool then provides an optional build-system-neutral
handoff for explicit ELF, HEX, BIN, and linker-map outputs. It performs no build,
search, subprocess, download, or hardware access. Collection stages a canonical
`firmware.*` bundle and deterministic SHA-256 manifest outside `.firm`; the
manifest contains provenance but no allowed ranges, plans, permissions, or gate
state. Safety refresh never consumes build outputs. The flash plan binds the selected
artifact and runtime containment parses it immediately before execution.

All build systems use the same owned-process helper with exact client-resolved argv, and their normal
output can enter through the same visible collector.

## Target and host de-biasing boundaries

The package ships no reviewed board identities, device evidence, geometry, or attach facts.
The empty state uses generic onboarding, which derives exact target/core/physical memory/flash
algorithm facts from the verified PDSC leaf and records actual probe/attach
facts from the live setup transaction. Production setup code contains no
branches for a particular board name or device address. Missing identity,
peripheral, erase, deployment, or recovery facts remain missing; no MCU prefix
invents them. Capability-specific operations then refuse before backend access.

Serial association uses stable USB identity and generic metadata scoring first.
Optional vendor helpers may be selected from an explicitly configured external registry when
generic evidence stays ambiguous; their executables come from an explicit environment path or
`PATH`, never a compiled host installation path. Recovery exposes only `backend_mass_erase` or
`manual_only`, checks the connected backend capability before disclosure, and
retains the existing exact-map disclosure and fresh one-time approval boundary.

## Runtime contracts

The live MCP `tools/list` schemas, tool descriptions, and the plan definitions in
`guardrails/plan_defs.py` are the runtime contract. The generated
[plan-tool contract](plan-tool-contract.md) is the corresponding human-readable reference.

The checkout, wheel, and sdist contain the same generic runtime. Board profiles, pack bytes,
firmware, and evidence are created or selected in the active project; none is bundled with the
server.

<!-- END SNAPSHOT Firmware/Firmware resources/server-guides/docs/architecture.md -->
### Snapshot: `Firmware/Firmware resources/test-program/run-firmware-test-suite/SKILL.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/SKILL.md -->
---
name: run-firmware-test-suite
description: Execute the MCP-Trial-3 fresh firmware experiment program end to end with every dependency-ready persistent doer lane running concurrently under the validated read-only orchestrator_harness, isolated resource-leased test phases, gpt-5.6-luna test agents at high reasoning on the regular/default non-Fast service tier, one designated Claude Sonnet 5 A23 doer, gpt-5.6-terra server-repair coder/doers and reviewers at high reasoning on the priority/Fast service tier, main-model evidence review, and serialized change-loop repair of verified BYO-Firmware-MCP defects. Use when asked to run, resume, parallelize, deduplicate, automate, or drive the fresh STM32L476/nRF52840 hardware tests until green, including firmware creation, HIL validation, failure triage, and server-fix/retest cycles.
---

# Run Firmware Test Suite

Run this from the `MCP-Trial-3` root. Treat
`BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` as the catalog and
`BYO-Firmware-MCP` as the server under test.

## Load before acting

1. Read `HANDOFF.md` and `PLAN.md` when present.
2. Read the selected test section in the catalog.
3. Read `.codex/design_charter.md`.
4. Read [execution-contract.md](references/execution-contract.md).
5. Read [result-contract.md](references/result-contract.md) before reviewing a result.
6. Read [model-continuity-contract.md](references/model-continuity-contract.md).
7. Read `.agent-workspace/SUITE_COORDINATION.md` and
   `.agent-workspace/SERVER_REPAIR_QUEUE.md` when either exists.
8. Read and hash-check `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.md` against its `.sha256`
   sidecar when present.
9. Read `.agent-workspace/AUTONOMY_REQUIREMENT_MATRIX.md` and verify that the selected test has an
   autonomous oracle and no unresolved operator/external-equipment dependency.
10. Run
   `python .codex/skills/run-firmware-test-suite/scripts/audit_autonomy.py`
   before every doer/reviewer launch or resume and after any catalog/skill/spec-amendment change.
   Do not launch on failure.
11. Read `orchestrator_harness/README.md`, the active harness config, and any durable harness
    handoff/state before launching or resuming parallel roles. Reconcile recorded PIDs against
    process identity and creation time; never trust a stale raw `running` declaration.
12. Load firmware MCP help/setup skills before live MCP use. Loading guidance never authorizes a
    hardware action.

## Zero-operator execution contract

Translate the selected catalog case into an executable spec without making it stricter. A
prerequisite or evidence item is a hard gate only when the catalog explicitly requires it, the live
server requests it to continue, it is necessary to distinguish pass from fail, or it is necessary
for electrical/RF/destructive/target-identity safety.

The main suite is autonomous after launch. Never make a main-catalog phase wait for another user
message or for a human to touch, inspect, identify, move, rewire, relabel, reposition, power-cycle,
or observe hardware. In particular, never require a photograph, visible marking, printed PCB
revision, PCA number, removable label, cable move, button press, jumper/solder change, DMM, logic
analyzer, BLE sniffer, camera, oscilloscope, external power instrument, or operator-timed event.
The connected four-board fixture, its declared CoreSX1262 wiring, the recorded delegated
authorization, and stable electronic identities are supplied inputs, not facts a doer must
physically re-prove.

Use electronic/software-controlled equivalents: server disconnect/reconnect/reset, process-scoped
provider interruption, firmware-controlled advertising/RF disable, host-side enumeration evidence,
UART/peer counters, debug state, artifact hashes, and existing correlated evidence. One truthful
source is enough; never require duplicate evidence modalities. Preserve electrical, RF,
destructive-action, and target-identity safety, but satisfy those boundaries from the declared
fixture and live server plans rather than inventing operator work.

`NEEDS_USER` and `INFRA_BLOCKED` are not permitted terminal outcomes for main-catalog runs. The
manager autonomously repairs routine tooling, launcher, USB, network/cache, SDK, and server
infrastructure; applies recorded delegated authorization after reviewing each exact live plan; or
issues a signed spec correction that replaces an unnecessary physical/external prerequisite with
an equivalent autonomous oracle. A temporarily unavailable resource is recorded only as
`WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` in `SUITE_COORDINATION.md`; it never creates
`RESULT.json`, never asks the user to intervene, and never stops unrelated lanes. If a branch is
intrinsically impossible without new human action or special equipment, move only that branch to
non-gating Appendix A and record `SKIPPED_AUTONOMY_REQUIRED`; never leave it as a main-suite gate.
Preserve already valid evidence and resume the same doer without repeating unrelated work.

## Authorized-use prompt clarity

Begin every new or resumed test-agent, reviewer, and server-repair prompt with an accurate,
plain-language scope statement:

> Authorized local firmware validation. Targets are limited to the named local workspace and the
> user-owned development boards explicitly assigned by the test. Follow every declared hardware
> plan and permission gate. No remote or third-party target is in scope.

Adapt the statement truthfully when a test is host-only or has no board assigned. Use precise
firmware and validation language. Do not introduce terms such as `attack`, `exploit`, `malware`,
`credential theft`, or `bypass` unless the exact catalog requirement, observed evidence, or
production defect makes that term technically necessary. Never hide, fragment, euphemize, or omit
material technical details to evade a safety system; this rule adds legitimate-use context and
removes gratuitous cyber framing without weakening the test.

If a platform cyber-safety notice, reroute, or refusal occurs, preserve the exact notice and
request context, checkpoint the exact session, and continue unrelated lanes. Resume the recorded
session when possible; this is not a main-run terminal status. Do not silently change models or
test scope to work around it.

## Subagent approvals and sandbox

- Every Codex and Claude doer/reviewer launch or resume must compose its task prompt through
  `scripts/orchestration/prompt_policy.py`. The helper verifies
  `.agent-workspace/AUTONOMOUS_EXECUTION_POLICY.sha256`, prepends and appends the authoritative
  policy, and records its SHA-256 in controller status. Refuse the launch if composition or hash
  verification fails. Never invoke an older direct prompt/launcher that lacks this binding;
  historical launcher artifacts remain evidence only.
- Every **new or resumed** Codex suite role must be launched with
  `--dangerously-bypass-approvals-and-sandbox --ignore-user-config -c approval_policy="never" -c approvals_reviewer="user"`.
  This is an explicit launcher contract, not an inherited parent setting: fail the launch before
  starting a session if any component is absent. The first flag supplies no sandbox/no approval;
  the explicit policy and reviewer settings make the no-approval/no-auto-review intent
  unambiguous under all ordinary config layers. Do not set `approvals_reviewer="auto_review"`,
  `-a on-request`, or `-s workspace-write`. Record `sandbox="danger-full-access"`,
  `approval_policy="never"`, and the actual launcher value `approvals_reviewer="user"` in the controller status.
- Apply the provider-equivalent unrestricted/no-command-approval configuration to every Claude
  role. Preserve the exact provider setting in its controller status. Do not rely on the parent
  conversation or IDE configuration being inherited by an external launcher.
- The explicit `subagent exec` configuration and deterministic autonomy audit enforce this
  contract. Historical direct launcher wrappers were deleted during repository cleanup; do not
  recreate or reuse them.
- Unrestricted Codex command execution is **not** hardware authorization. Flash, erase, unlock,
  protection, recovery, RF, and power-fault actions still require the live firmware-server plan
  and the recorded delegated hardware authorization in this skill.

## Non-negotiable role split

- Treat Codex **Fast mode** as `service_tier="priority"`, independently of model and reasoning
  effort. Pass it on every new **and resumed** Terra role. Do not invent a `-fast` model slug.
- Run every Codex catalog/test-lane agent turn with `gpt-5.6-luna`,
  `reasoning_effort="high"`, and the explicit non-Fast tier `service_tier="default"`. This
  includes Luna turns that author fresh firmware application code; Luna roles must never use
  Fast/priority.
- A23 is the sole provider exception: run its one persistent doer on **Claude Sonnet 5** through a
  persistent unrestricted/no-command-approval launcher. Record the exact provider model identifier,
  launcher, session identity, and settings. Do not claim Codex `service_tier` or reasoning
  settings for Claude. After one bounded retry window, a genuine Claude-provider outage may not
  block the suite: record it and transparently continue A23 with the persistent `gpt-5.6-luna` fallback
  at high reasoning and the regular/default tier. This loses the provider-comparison datapoint but not the
  firmware/server test; never substitute silently.
- Run every `gpt-5.6-terra` server-repair coder/doer, reviewer, spec-tester, and
  regression-tester turn with `reasoning_effort="high"` and
  `service_tier="priority"` (Fast mode). No Terra role in this suite runs on the default tier.
- The **main model** specifies, schedules, reviews evidence, and invokes `$change-loop` for a
  verified production-code server defect. It does not implement fresh firmware or perform the test
  in place of the test agent.
- Assign each roster-owned catalog test except A23 to its named persistent lane doer from
  [the doer roster](references/doer-roster.md). Create that doer through `subagent exec` (not the
  regular internal subagent tool) only for its first assigned task; resume the same session for
  later assigned tasks, with:
  - `fork_turns="none"`
  - `model="gpt-5.6-luna"`
  - `reasoning_effort="high"`
  - `service_tier="default"`
- Start A23 once with the designated persistent Claude Sonnet 5 launcher and no inherited parent
  conversation. Q40 is a manager-owned corpus aggregation; it does not create another base
  application or ordinary catalog test agent. It may open only missing, nonduplicated seeded
  branches by assigning each branch to one currently idle Atlas, Boreal, Cygnus, or Delta session.
  Do not create branch-specific doers or reuse Nova.
- Keep every named doer session persistent through its assigned tasks, routine firmware iteration,
  and server repair/retest. Resume it instead of opening disposable same-model sessions.
  Replacement is allowed only for a
  necessary model change or an irrecoverable session, with the old/new identity, reason, verified
  evidence boundary, and remaining work recorded under the
  [model continuity contract](references/model-continuity-contract.md). Never replace it merely
  because a test is red or slow.
- Resume an existing `gpt-5.4` doer as `gpt-5.6-luna` at high/default without restarting or
  retesting completed work. Do not otherwise restart an in-progress test merely to adopt the new
  model or the A23 Claude exception.
- After sealing and before assigning/resuming the doer for that task, invoke one **persistent adversarial reviewer**
  through `subagent exec` with `fork_turns="none"`, `model="gpt-5.6-terra"`, and
  `reasoning_effort="high"`, and `service_tier="priority"`. It first reviews the sealed spec;
  resume that exact reviewer with the same settings after a `PASS` claim for the evidence review.
  It is separate from the persistent test agent and is read-only: it never operates hardware or
  edits either firmware or server code, and must not open `BYO-Firmware-MCP`.
- The test agent owns all fresh application code, builds, instrumentation, HIL actions, firmware
  diagnosis, and test evidence. It must not read or edit `BYO-Firmware-MCP`, invoke or read
  `$change-loop`/`$plan-changes`, or propose a server repair workflow.
- A doer name identifies one persistent doing-subagent session, not a task. If the manager opens
  `N` concurrent execution lanes, it uses exactly `N` named doers. Each task is assigned to one
  doer, and each doer runs at most one task at a time. Record the doer name separately from its
  provider agent/session ID. Do not retroactively name completed/bootstrap task agents.
  Reviewers and server-repair coder/doer roles are not named firmware test-lane doers.
- The main model is the only suite manager. It may run at most one active task in each of
  the five named doer lanes, and only when dependencies and all required leasesâ€”including the
  isolated workspace plus doer/provider/launcher execution slotsâ€”allow it. Never run two
  managers/controllers for the same suite, two active
  doers for the same task, two live sessions under one doer name, or two repair loops against the
  same runtime.
- On every scheduling pass, launch or resume **all** eligible named doer lanes concurrently. Do
  not finish one doer's portfolio before starting another, and do not leave an eligible lane idle
  merely because a different test, provider, board, or fixture is waiting. A waiting task stops
  only its dependency descendants and conflicting leases. An idle doer may advance to its earliest
  unrelated dependency-ready roster task only after its current task is terminal or at a
  manager-recorded safe handoff.
- Compute eligibility per task phase from only its explicit prerequisites, current server-repair
  state, and required resource leases, including its isolated workspace and
  doer/provider/launcher execution slots. A dependency-wave row, row number, row completion, or unfinished task
  in another lane is never itself a prerequisite. Start an eligible phase from any row immediately;
  do not wait for the current or an earlier row to finish. After every launch, completion,
  checkpoint, failure, lease change, or provider wait, rescan every lane and fill all newly eligible
  work. Use catalog section 11.1 as the authoritative cross-test edge list. A sealed spec may split
  one listed edge into finer consumed-artifact phases, but it must not invent an unlisted
  whole-test, whole-row, or unrelated-lane dependency. Unexpectedly idle, usable hardware requires
  an immediate scheduling audit.
- Schedule resources, not fixed STM/nRF/host lanes. The board tokens are `STM-A`, `STM-B`, `NRF-A`,
  and `NRF-B`. Also lease each doer/provider/launcher execution slot, isolated workspace, probe,
  serial endpoint, peer/radio, autonomous electronic control, USB-enumeration or power-disruption
  scope actually affected, mutable artifact/cache root, and server process/state/lifecycle scope.
  Board-free spec, build, and evidence-review phases may overlap hardware work when their host
  resources are isolated.

## Non-negotiable test gate

- Every main-catalog-required behavior remains a hard release gate. Appendix A, an optional
  recommendation, or an accidentally invented spec prerequisite is not a release gate. A real
  failure blocks that test, its dependency
  descendants, and conflicting resource leases, but does not cancel an unrelated already-eligible
  phase.
- A claimed server failure does not immediately freeze the suite. The main model first validates
  it. If it is not a production server defect, reject the claim and resume the same test agent.
- A verified production server defect starts a selective repair barrier: stop launching new
  server-consuming or HIL phases, request bounded safe checkpoints from active server/HIL
  consumers, and repair queued defects serially through `$change-loop`. Pure spec, isolated
  firmware build, and read-only evidence-review phases may continue only if they neither invoke nor
  depend on the live server or leased hardware.
- After repair, bind every subsequent server-consuming phase to the same recorded repaired
  snapshot, restart the affected MCP processes, and target-retest each affected
  reproducer/requirement. Do not mark the failed test or any dependent release gate green until the
  exact failure passes. Intentional negative/refusal cases pass only when the observed refusal
  matches their specification.

### Incremental retest and bounded-review policy

- Treat every verified PASS as durable evidence bound to its exact spec, source/artifact/server
  snapshot, fixture identity, and relevant leases. A later failure or criticism invalidates only
  the evidence it actually contradicts or whose covered inputs changed.
- After any test, adversarial, or repair failure, rerun the failed check, the directly affected
  requirements, and the smallest regression surface reached by the change. Never restart the whole
  suite, every lane, an expensive application campaign, a soak, or already evidenced branches from
  scratch merely because one check failed.
- Continue unrelated eligible lanes and preserve their evidence. Restart an MCP process only when
  it consumed changed server code; resume a firmware/HIL phase only when its snapshot or required
  evidence was invalidated.
- Give each adversarial reviewer one bounded pass per artifact stage plus one targeted follow-up for
  rejected evidence. Reviewers must distinguish **ACTIONABLE** functional findings from
  **ADVISORY** hardening. Actionable means an evidenced main-catalog requirement violation,
  credible safety/data-loss/identity risk, reproducible failure, or likely hang/orchestration
  collapse. Style, speculative robustness, vanishingly unlikely cases without evidence, unrelated
  features, and disproportionate complexity are advisory.
- The main manager records advisory findings but does not block delivery or expand scope for them.
  Once actionable findings are resolved and objective gates are green, stop reviewing and deliver;
  do not seek another verdict or pursue a perfect product.

## Harness-assisted parallel coordination

The validated `orchestrator_harness` is required whenever two or more suite roles may overlap,
and for every HIL/server-consuming scheduling epoch even when only one lane is initially ready.
It is a read-only reconciler and notification path, not a coordinator or authority. The current
high-level session remains the sole suite manager. A separate supervisory agent is not part of
normal suite execution; the root-supervisor/Sol-manager arrangement used for harness acceptance
was a validation fixture only.

Create one suite-epoch config from `orchestrator_harness/config.example.json`. Its `run_globs`
must list every run root the epoch may activate, its output directory must be a unique directory
under `multi-agent-logs/orchestrator-harness/<epoch>/` and outside all observed run roots, and its manager review,
no-progress, and heartbeat intervals must be explicit. Use the validated defaults of 300, 600,
and 420 seconds unless a bounded acceptance run intentionally uses shorter values; heartbeat
timeout must remain greater than the review interval. Never reuse
a prior epoch's config, output state, requests, relays, PIDs, or notification records as a live
suite configuration.

Start exactly one managed watcher for the config:

```powershell
python -m orchestrator_harness --config <suite-harness-config> watch --managed
```

Attach its stdout/stderr to durable manager-owned logs or a yielded foreground process cell.
Record watcher PID, owner PID, both creation times, config hash, output paths, and lifecycle state
in `multi-agent-logs/orchestrator-harness/<epoch>/ROLE_REGISTRY.json`. The manager also keeps:

- `.agent-workspace/SUITE_COORDINATION.md`: manager identity, optional informational eligibility
  group (never an a…2810 tokens truncated…; those agents must stop at `BUILT_WAITING_FOR_LEASE` until their HIL
dependencies and manager-assigned hardware leases are valid.

## Quick start

List catalog tests:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py list
```

Create one isolated run:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py create A20
```

Fill every `[REQUIRED]` field in the generated `.agent-workspace/SPEC.md`, then seal it:

```powershell
python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py seal <run-dir>
```

The scaffold reads canonical shared inputs from the task-owned asset directories listed below and
copies only these
baseline target documents into the run root using their legacy run-local names:

- `stm32L476rgt.pdf`
- `Nano_BLE_MCU-nRF52840_PS_v1.1.pdf`

Everything else initially lives under `.agent-workspace/`. Never copy the master plan, server
source, prior runs, firmware examples, SDK projects, packs, profiles, or build outputs. For A24
and A25, the manager may additionally supply hashed copies of
`60852689.DS_SX1261_2 V2-2.pdf`, `waveshare-lora-module.pdf`, and
`nrf-sx-pin-mappings.md`; the actual attached radios are Waveshare CoreSX1262 modules, not
SX1276.

Use the canonical sources at
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/sx1261-sx1262-v2.2.pdf`,
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/waveshare-lora-module.pdf`, and
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/board-mappings/nrf-sx1262-pin-mappings.md`,
retaining those legacy run-local names. The canonical STM32 and nRF baseline datasheets are owned
by `fresh-experiments/S10_20260726-034312/.agent-workspace/assets/datasheets/` and
`fresh-experiments/S11_20260726-034313/.agent-workspace/assets/datasheets/`, respectively.

## Per-test loop

1. **Create and specify.** Scaffold a new directory, write objective requirements, exact hardware
   facts material to the case,
   observable pass/fail oracles, allowed destructive scope, and evidence requirements in
   `SPEC.md`. Use official current sources to record:
   - NUCLEO-L476RG MCU: `STM32L476RGT6`
   - nRF52840 DK application MCU/package: `nRF52840-QIAA`
   Use the recorded correlated electronic/official source for the MCU/package input. Do not ask for
   a physical board revision/marking, `PCA10056`, printed PCB revision, board photo, direct visual
   inspection, or another operator statement. If a real electronic contradiction could change
   target selection or safety, fail closed on that action and use the manager-supplied fixture
   record or an autonomous server/electronic check to resolve it.
   Also record the canonical doer name, build and HIL prerequisites separately, internal
   catalog-defined shards, phase-specific resource leases, disruptive/global scopes, safe
   checkpoint boundaries, and maximum pause latency.
2. **Seal.** Run `fresh_test.py seal`. Do not change the spec after the agent starts; create a
   signed amendment in `.agent-workspace/SPEC_AMENDMENTS.md` only to correct a genuine spec error.
3. **Review the sealed spec once.** Start one persistent read-only reviewer through `subagent exec`
   with `fork_turns="none"`, `model="gpt-5.6-terra"`, `reasoning_effort="high"`, and
   `service_tier="priority"`. Give it the absolute run path and
   `.agent-workspace/REVIEWER_PROMPT.md`; it writes
   `.agent-workspace/SPEC_ADVERSARIAL_REVIEW.md` without operating hardware or inspecting the
   server. Persist its identity:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-reviewer <run-dir> `
     --reviewer-id <agent-id> --task-name <canonical-task-name> --model gpt-5.6-terra
   ```

   The reviewer labels findings `ACTIONABLE` or `ADVISORY` under the policy above. The main model
   records the one review after addressing any genuine spec error with a signed
   `SPEC_AMENDMENTS.md` entry and declines advisory scope growth. Do not launch a spec-review loop:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py approve-spec <run-dir> `
     --note "Sealed requirements and any recorded amendment are executable and falsifiable."
   ```
4. **Invoke the assigned doer.** For an ordinary lane doer's first task, create it through
   `subagent exec` with `fork_turns="none"`, `model="gpt-5.6-luna"`,
   `reasoning_effort="high"`, and `service_tier="default"`; for every later assigned task, resume
   that same persistent session with the same settings. Do not use the regular internal subagent
   tool. For A23, use Nova's
   recorded persistent Claude Sonnet 5 launcher. Put the absolute run path and generated
   `TEST_AGENT_PROMPT.md` in the task message. Require all tool workdirs to be the run directory
   and the first command to print/verify the current path. Explicitly forbid `$change-loop` and
   `$plan-changes`; they are unavailable to the fresh-experiment test agent. Immediately persist
   the returned identity:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py bind-agent <run-dir> `
     --agent-id <agent-id> --task-name <canonical-task-name> `
     --model <gpt-5.6-luna-or-claude-sonnet-5>
   ```
5. **Let the agent converge, wait for a lease, or checkpoint.** Do not pull routine firmware failures back to the main model. The
   agent keeps editing, building, flashing through live plan/permission gates, observing, and
   retesting until it emits a terminal result. If its build completes before HIL is eligible, it
   records the immutable build handoff and returns at `BUILT_WAITING_FOR_LEASE`. During a repair
   barrier, a server/HIL consumer may instead return at the requested safe checkpoint without
   changing `RUN_STATE.json` to a terminal status.
6. **Validate the claim.** Run:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py verify <run-dir>
   ```

7. **Adversarial evidence review.** For every `PASS` claim that passed structural validation,
   resume the recorded sealed-spec reviewer through `subagent exec`; do not create a new reviewer.
   Give it the absolute run directory containing `SPEC.md`, `SPEC_AMENDMENTS.md` if present,
   `RESULT.json`, `TEST_REPORT.md`, and all evidence paths. It must independently reassess the
   evidence without deferring to its earlier spec approval. It must not open or
   read anything under `BYO-Firmware-MCP`, including server source, tests, documentation, runtime
   state, or Git history. It must not operate hardware, invoke destructive tools, alter the run, or
   edit the server. Require it to write
   `.agent-workspace/ADVERSARIAL_REVIEW.md` and report numbered criticisms. Each criticism must
   name the supporting evidence, the expected observable server behavior, why the observed behavior
   indicates a server defect rather than an agent/fixture issue, and a minimal observable
   regression and label itself `ACTIONABLE` or `ADVISORY`. It must explicitly report
   `NO_ACTIONABLE_SERVER_ISSUES` when it finds none. An
   inability to complete the workflow from the available MCP guidance/evidence is itself a
   communication or product-surface criticism, not permission to inspect the server.
8. **Judge the criticisms.** Independently compare the spec, diffs, exact build commands,
   artifacts, MCP evidence, applicable identity/behavioral oracles, final state, and each
   adversarial criticism. An
   agent's prose is not proof.
   - Reject criticisms not supported by the evidence or attributable to firmware, fixture, SDK,
     test-spec, or agent mistakes. Record the rationale in the main review note.
   - Record but do not fix or gate on advisory perfection/hardening findings. Do not add product
     complexity whose cost is disproportionate to the evidenced risk.
   - For every validated **production-code** server defect, record the criticism, evidence paths,
     accepted scope, and rejected criticisms/rationale in the server change request, then use the
     server repair loop.
   - Do not mark the run green while an actionable criticism is unresolved. Conversely, do not keep
     the review loop open after actionable findings are resolved and the objective gates pass.
9. **Record the verdict.** Only when no actionable criticism remains, record a successful
   independent review:

   ```powershell
   python .codex/skills/run-firmware-test-suite/scripts/fresh_test.py review <run-dir> `
     --verdict GREEN --note "All numbered requirements independently evidenced."
   ```

   Use `--verdict REJECTED` when proof is inadequate, then request only the missing/invalidated
   proof from the recorded agent session (or its formally recorded necessary replacement). Resume
   the reviewer once for that targeted evidence; it must not reopen already accepted requirements
   unless the new change directly invalidated them. For a sharded task, record the
   catalog ID green in `SUITE_COORDINATION.md` only after its one named doer has completed every
   required shard and the manager has checked the aggregate coverage map.
10. **Request missing proof.** If a claimed pass is incomplete or a claimed server defect is not
    isolated, resume the recorded agent through its recorded provider launcher with the precise
    missing checks.
    Use the model-change/session-recovery handoff only when its necessity criteria are met; do not
    create a disposable same-model session for an ordinary follow-up.
11. **Handle run status:**
   - `PASS`: mark green only after main-model review passes.
   - `SERVER_FAILURE`: verify it is reproducible and belongs to production server code rather than
     firmware, wiring, SDK, host, documentation, metadata, test specification, or misunderstanding.
     Queue and start a repair barrier only for the production-code case.
    - Reject `NEEDS_USER` or `INFRA_BLOCKED` from a main-catalog doer. Do not relay a user request.
      Apply delegated authorization, repair the environment, substitute an autonomous equivalent,
      or append a signed correction. If a resource is temporarily absent, checkpoint the exact
      session and record `WAITING_FOR_RESOURCE`/`WAITING_FOR_PROVIDER` only in the suite ledger
      while all unrelated lanes continue. If the action intrinsically needs human manipulation or
      unavailable special equipment, reclassify only that action into Appendix A and record
      `SKIPPED_AUTONOMY_REQUIRED`.
12. **Advance eligible phases.** Assign a dependency-ready catalog task to its roster doer and
    resume that persistent session when it is idle and the phase leases do not conflict. A doer
    may take its next assigned task only after its current task is terminal or at a manager-recorded
    handoff. Internal shards stay inside that doer's session; never launch another doing subagent
    for them. During a repair barrier, do not start server-consuming or HIL work; isolated
    board-free spec/build/review work may proceed under the selective-freeze rules.

## Server repair loop

Only the main model may initiate this loop, and only for a reviewed `SERVER_FAILURE` proven to
require a production-code change in `BYO-Firmware-MCP`. Do not use it for fresh-experiment work,
firmware/fixture/SDK failures, missing evidence, documentation-only or metadata-only issues, or
test-spec corrections.

Before entering the loop, the main model must:

1. add the independently validated defect to `SERVER_REPAIR_QUEUE.md`;
2. stop launching new server-consuming/HIL phases and write `PAUSE_REQUESTED.md` only in active
   runs that consume the server or hardware;
3. wait for those nonterminal consumers to return bounded `PARALLEL_CHECKPOINT.md`; a reporting
   agent that already returned a terminal result is already quiescent;
4. record those consumers `FROZEN` and verify no test/repair controller operates hardware or the
   server worktree; separately record any continuing board-free build/spec/review phase and prove
   that it does not invoke the server; and
5. order queued defects into small independent repair slices.

Treat `.codex/design_charter.md` as a live repair constraint. The main model rereads it before
specifying the repair, before authoring and validating the plan, before each distinct
implementation slice or feature, and before accepting the neutral tests and targeted HIL retest.
Every repair-role prompt requires that role to reread the charter at the same relevant boundaries
and to stop and report any conflict. A single read at suite startup is not sufficient for a server
edit.

Process queued repairs one at a time. Never run concurrent change-loops or production-code edits.
If a queued report is rejected during manager analysis, record the reason and resume its test
agent rather than manufacturing a repair.

The current main model must inspect `BYO-Firmware-MCP` and author the server-repair plan there
directly; it must not launch a planner agent. The doer, spec tester, and regression tester must all
use `gpt-5.6-terra` at high reasoning on `service_tier="priority"` and be launched with
`BYO-Firmware-MCP` as their workspace. Preserve the priority tier on every resume. The
fresh-experiment run remains
evidence-only input to the main model; it is never a change-loop role workspace.

1. Write the exact observed/expected behavior, minimal reproducer, evidence paths, affected
   server commit, and exclusions to
   `fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id>/request.md`. Never put
   experiment repair-control state in `BYO-Firmware-MCP`.
2. Use a unique runtime to prepare the request so an existing change-loop is not overwritten:

   ```bash
   cd BYO-Firmware-MCP
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     bash ../.codex/skills/plan-changes/scripts/plan.sh --prepare \
       ../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id>/request.md
   ```

   The current main model then reads the plan-authoring contract, inspects the server repository,
   writes the runtime's `plan.md` directly, and validates it:

   ```bash
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     bash ../.codex/skills/plan-changes/scripts/plan.sh --validate
   ```

   Never delegate this plan to a subagent, `codex exec` planner, doer, or tester.
3. Perform exactly one independent, read-only adversarial review of the main-authored plan using
   `gpt-5.6-terra`, `reasoning_effort="high"`, and `service_tier="priority"`. Record the reviewed
   plan SHA-256, reviewer identity, and numbered actionable risks/test targets plus nonblocking
   advisory notes in the runtime's `plan-review.md`. If execution proves a genuine plan mistake,
   record a minimal evidence-backed amendment and review only that amendment once; do not regenerate
   the whole plan or re-review unchanged items. The neutral tester gate and later evidence review
   are the correctness backstops.
4. Invoke `$change-loop` immediately:

   ```bash
   CL_RUNTIME_DIR=../fresh-experiments/<run>/.agent-workspace/server-repairs/<test-id> \
     DOER_MODEL=gpt-5.6-terra \
     SPEC_TESTER_MODEL=gpt-5.6-terra \
     REGRESSION_TESTER_MODEL=gpt-5.6-terra \
     CL_REASONING_EFFORT=high \
     CL_CODEX_FLAGS='--dangerously-bypass-approvals-and-sandbox --ignore-user-config --config approval_policy="never" --config approvals_reviewer="user" --config service_tier="priority"' \
     bash ../.codex/skills/change-loop/scripts/run_loop.sh
   ```

   Do not weaken or replace this full-access/no-approval configuration. Retain
   `--config service_tier="priority"` so every start and resume remains in Fast mode.

5. If either neutral spec or regression test fails, stop. The main model analyzes the failure and
   deploys/resumes the change-loop doer to fix the server; rerun the failed test and only
   regressions whose covered source/contracts changed. Retain the other gate's validated passing
   evidence through the change-loop pass cache. Accept server repair only when both gates have a
   current pass or validated unaffected-pass reuse. Do not commit.
6. Restart/reload an isolated MCP process for the reporting test so it does not exercise stale
   code. Keep every other server/HIL consumer frozen; board-free non-server phases may continue.
7. Resume only the **recorded reporting test-agent session** through its recorded provider
   launcher, identify only the new server commit/diff, and request a targeted retest: the minimal
   reproducer, every requirement and control directly touched by the accepted server change, and
   the relevant evidence capture. If a necessary model/session handoff was recorded, resume the
   replacement from the same durable evidence boundary. Do **not** rerun the whole expensive
   application test merely because the agent/model changed or unless the server change's scope
   reaches those requirements.
8. Record the queue item closed only after its targeted retest passes, then repeat serially until
   the queue is drained. Reload every checkpointed server-consuming run's MCP process from the same
   final snapshot, update the coordination ledger, remove pause requests, and resume affected
   recorded agents for targeted retests before unrelated checkpointed server/HIL work continues.
   Bind builds that completed during repair to that snapshot before they enter HIL. Use a
   replacement only under the continuity contract.

Do not let the test agent propose or make server edits. Do not use `$change-loop` for firmware,
fixture, SDK, infrastructure, documentation-only, metadata-only, evidence, or test-spec errors.

## Permission and safety boundary

- Record an explicit user delegation that authorizes the manager to continue all in-scope suite
  approvals. For each populated live plan, the manager reviews the exact board, artifact,
  operation, losses, and final state and may relay the recorded delegated permission without
  another chat pause when they are within that grant. Never invent a permission value or extend
  the grant beyond the assigned user-owned fixture.
- Follow every live MCP plan and permission gate. Preserve every destructive disclosure in
  evidence. Any action not already covered by the recorded delegation is ineligible for the main
  suite; move/keep it in non-gating Appendix A and skip it without asking the user.
- D35, R37, and R38 are autonomous try-last Appendix A experiments, not main release gates. Run
  them only when every fixture, backup, control, permission, and recovery step is already
  available without further operator intervention; otherwise record
  `SKIPPED_AUTONOMY_REQUIRED`. If attempted after main work cannot be delayed, keep D35/R38 with
  Delta and R37 with Cygnus as defined by the doer roster.
- Keep RF frequency, antenna, power, and duty cycle legal for the actual module/region.
- Never claim all-green while a required test is unreviewed or incomplete. A manual/external-only
  branch cannot remain required: replace it with an autonomous equivalent or move it to Appendix A.

## Completion

Finish the main suite only when every main-catalog test has a main-reviewed `PASS` and the
manager-owned Q40 nonduplicative corpus gate is complete, or the user explicitly narrows the
suite. Appendix A and future version-to-version regression policy are not release gates. Write a
final suite matrix with run directory, agent identity, server commit, firmware commit, result,
evidence path, repair loop (if any), Appendix A `PASS`/skip/gap outcomes, and unresolved
exclusions. Include the final reconciled lane table, harness config/hash, manager and monitor logs,
notification/ack record, exact PID-identity cleanup, and watcher terminal state. Stop the managed
watcher cooperatively or let a deliberately handed-off heartbeat lease remain active; never leave
an unowned background watcher. Never commit, push, deploy, or flash outside a live test plan.

<!-- END SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/SKILL.md -->
### Snapshot: `Firmware/Firmware resources/test-program/run-firmware-test-suite/references/execution-contract.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/references/execution-contract.md -->
# Fresh Firmware Test Execution Contract

## Contents

1. Suite state machine
2. Harness-assisted parallel coordination
3. Test specification rules
4. Isolation and allowed inputs
5. Test-agent model and continuity contract
6. Main-model review
7. Server-failure escalation
8. Recovery and resumption

## 1. Suite state machine

Use these durable states:

```text
CREATED -> SPEC_READY -> SPEC_REVIEWED -> AGENT_RUNNING
AGENT_RUNNING -> PASS_CLAIMED -> (ADVERSARIAL_EVIDENCE_REVIEW) -> MAIN_REVIEW -> GREEN
AGENT_RUNNING -> SERVER_FAILURE -> MAIN_VERIFIED_SERVER_FAILURE
MAIN_VERIFIED_SERVER_FAILURE -> REPAIR_BARRIER -> CHANGE_LOOP -> SERVER_FIXED -> AGENT_RUNNING
```

Never transition `PASS_CLAIMED` directly to `GREEN`. After sealing, one persistent read-only
reviewer first writes `SPEC_ADVERSARIAL_REVIEW.md`; the main model records the one resulting spec
approval before the test agent starts. Every structurally valid PASS then resumes that exact
reviewer for the evidence review in `ADVERSARIAL_REVIEW.md`; `RUN_STATE.json` remains
`PASS_CLAIMED` until main review records a verdict. Never create a replacement test agent to escape
a red state. Persist the test-agent and reviewer identities, canonical task names, and models in
the run state as soon as they are spawned. A test-agent replacement is allowed only under
`model-continuity-contract.md`, with a durable recorded handoff.

`AGENT_RUNNING` may be temporarily coordinated as `PAUSE_REQUESTED`, `CHECKPOINTED`, or `FROZEN`
in the suite ledger. Those are not `RUN_STATE.json` terminal statuses and do not create or alter
`RESULT.json`. The exact persistent agent resumes from the recorded checkpoint.

Temporary resource/provider absence is similarly recorded only as `WAITING_FOR_RESOURCE` or
`WAITING_FOR_PROVIDER` in the suite ledger. Main-catalog runs never terminate as `NEEDS_USER` or
`INFRA_BLOCKED`, never request physical/operator intervention, and never stop unrelated lanes.

Every main-catalog-required behavior remains a hard release gate; Appendix A, optional
recommendations, and catalog-unsupported spec prerequisites do not. On a non-intentional failure,
block that test, its dependency descendants, and conflicting resource leases. Every unrelated
dependency-ready phase continues. A verified production server defect opens a barrier for
server-consuming and HIL
phases, but isolated board-free work that does not invoke the server may continue. The main model uses
change-loop only for a verified production-code defect; it must not use it for firmware, fixture,
SDK, host, specification, evidence, documentation-only, or metadata-only work. Rerun the exact
failed behavior before its gate becomes green. An intentional refusal/negative case passes only
when its specified refusal behavior is observed.

## 2. Harness-assisted parallel coordination

The suite uses one authoritative main-model manager and a five-session roster-owned doer pool: Atlas,
Boreal, Cygnus, Delta, and Nova. These are execution lanes, not fixed STM/nRF/host resource lanes.
Concurrency is bounded by one active task per doer, satisfied dependencies, isolated workspaces,
launcher/host capacity, and exact phase resource leases. The physical board tokens are `STM-A`,
`STM-B`, `NRF-A`, and `NRF-B`; board-free work may overlap them.

Treat concurrency as an affirmative scheduling requirement. On every scheduling pass, evaluate all
five lanes and launch or resume every eligible non-conflicting lane in the same batch. Never wait
for a blocked lane before advancing unrelated work. A dependency wave is an eligibility map, not a
serial queue; its row number, row membership, and row completion are never prerequisites. Compute
readiness per phase from explicit prerequisite edges, selective server-repair state, and required
resource leases, including the isolated workspace and doer/provider/launcher execution slot.
Catalog section 11.1 is the authoritative cross-test edge list. A sealed run may refine a listed
edge down to the exact consumed artifact/evidence phase, but it may not add an unlisted whole-test,
whole-row, or unrelated-lane dependency.

Whenever roles overlap, or any HIL/server-consuming epoch is active, start exactly one
`orchestrator_harness` managed watcher from a fresh suite-epoch config whose `run_globs` cover
every run the epoch may activate. The watcher is read-only; the current high-level session is the
sole manager. Record the watcher/owner PID identities and creation times, config hash, output
paths, manager/monitor logs, and heartbeat lease below
`multi-agent-logs/orchestrator-harness/<epoch>/`.

The manager consumes one durable actionable notification at a time, inspects its named lane and
the compact whole-suite state, performs any exact relay/recovery/lease decision itself, and then
acknowledges the exact event ID. The same watcher self-arms after acknowledgement. During active
HIL, inspect every live doer normally every two to three minutes and renew the watcher heartbeat
before expiry during longer reviews. Never acknowledge a notification without reviewing it.
Never use the watcher to launch, stop, approve, relay, classify, or repair.

Derive controller lanes from exact doer/task/session facts. Scope request/helper/MCP record formats
that support it with the exact manager-assigned `declared_lane_id`; it overrides any reused
persistent session ID. Historical lifecycle
conditions are baselined on watcher startup, not replayed as current work, while persistent safety,
request, conflict, provider, and manager-signal conditions remain actionable.

The main model maintains:

- `.agent-workspace/SUITE_COORDINATION.md`, containing manager identity, optional informational
  eligibility group (never an advancement gate), server snapshot, catalog test, canonical doer
  name, provider agent/session and reviewer identities,
  build/HIL dependencies, internal shards, phase-specific leases, process/runtime identities, and
  phase states; and
- `.agent-workspace/SERVER_REPAIR_QUEUE.md`, containing only manager-validated production-server
  defects and their evidence, disposition, repair slice, and targeted retest state.

Before HIL starts or resumes, the manager writes the run-local
`.agent-workspace/RESOURCE_ASSIGNMENT.md` with catalog ID, internal shard/phase, canonical doer
name, `HIL_RUNNING`, assigned server snapshot, exact leases, assignment time, and manager identity.
The test owner treats it as
read-only. This run-local copy lets an isolated agent verify authority without reading suite-root
state. When a phase may reach a permission-bearing live plan, the assignment also binds the
applicable delegated-authorization artifact path and SHA-256. Without that exact binding, the
agent must not infer a grant.

Use the following prompt-driven protocol:

1. Record one authoritative manager. A doer name identifies one persistent session. Assign each
   catalog test to one doer from `doer-roster.md` and record the doer separately from its provider
   identity. A doer runs only one task at a time but may receive a later roster task after a
   terminal or manager-checkpointed handoff. On every resume, inspect live processes and the ledger.
   Never permit two doers on one task, two live sessions under one doer name, or duplicate
   controllers for a persistent role or `CL_RUNTIME_DIR`.
   Immediately after reconciliation, fill every eligible lane; do not leave a lane idle merely
   because another lane is waiting on a provider, board, fixture, review, or dependency.
2. Record one immutable server snapshot for every server-consuming phase: Git HEAD, dirty status,
   and a stable diff/tree fingerprint. Each HIL owner starts a separate MCP process and state root
   from that snapshot unless the sealed test explicitly evaluates shared-process behavior.
   For a Codex CLI role inheriting the configured `byo-firmware` server, set per-process
   `mcp_servers.byo-firmware.cwd` and
   `mcp_servers.byo-firmware.env.BYO_MCP_ARTIFACT_ROOT` overrides on its launcher. Confirm the
   effective config and first public artifact/event path; if either escapes the assigned root,
   checkpoint at the next safe boundary and correct the launcher before retesting.
3. Before each phase, lease all execution, physical, and host-global resources it may use or
   mutate: doer/provider/launcher execution slot, isolated workspace, friendly board, probe UID,
   serial endpoint, peer/radio, autonomous electronic control actually used,
   USB-enumeration or power scope actually affected, server lifecycle, and mutable
   artifact/cache/state roots. External lab instruments and manual controls are not prerequisites
   and are never requested. Exclusive leases may not overlap. Only the
   manager writes assignments; an agent never self-acquires hardware.
4. Track `SPEC_READY`, `BUILDING`, `BUILT_WAITING_FOR_LEASE`, `HIL_RUNNING`, `CHECKPOINTED`, and
   `PASS_CLAIMED` in the suite ledger, separately from terminal `RUN_STATE.json`. A build starts
   when build prerequisites and host leases are ready. HIL starts only after its HIL prerequisites,
   assigned server snapshot, and hardware leases are ready.
5. Future specs, read-only spec reviews, and isolated board-free builds may run while hardware
   tests run. A completed build records an immutable artifact/configuration handoff and stops at
   `BUILT_WAITING_FOR_LEASE`; it grants no hardware authority.
6. A catalog item may define independent board/family shards, but they are internal phases owned
   by that task's assigned lane doer. Each shard needs immutable scope, an isolated
   application/build tree, and unique leases. The doer may orchestrate concurrent processes but
   may not delegate a shard to a second doing subagent. The manager records one catalog verdict
   after verifying the aggregate coverage map. Sharding may not duplicate or omit coverage.
7. A verified production-server defect stops new server-consuming/HIL launches. The manager writes
   `PAUSE_REQUESTED.md` only into active server/HIL runs. Each affected agent checks for it between numbered
   requirements and bounded soak/repetition epochs. After any current atomic hardware operation
   reaches its declared finite completion/timeout, the agent flushes evidence, records board and
   cleanup state, writes `PARALLEL_CHECKPOINT.md`, and returns without a terminal result.
   Board-free spec/build/review phases may continue only if they do not invoke or depend on the
   live server and cannot transition into HIL.
8. Wait through agent/process completion events, managed-watcher notifications, or an ordinary
   blocking shell wait. Do not use repeated model turns to poll. Still perform the bounded
   supervision pass above so a missing notification, crash, repetition loop, or idle lease is
   caught promptly.
9. When every active server/HIL consumer is checkpointed, mark those consumers frozen. Process the
   validated repair queue serially with one main-authored plan/change-loop at a time. Concurrent
   production edits or repair loops are forbidden.
10. After the queue is drained, restart checkpointed MCP processes from the same new server
    snapshot. Remove each pause request, update the ledger, and resume the exact persistent agents.
    Bind builds completed during repair to this snapshot before HIL. Affected tests rerun the
    minimal reproducer and reached requirements; unrelated verified evidence is retained.
11. If a watcher defect is confirmed, stop new launches, checkpoint only affected live roles,
    stop exact watcher/controller/affected descendants, preserve all completed evidence, make the
    focused local harness repair, run its focused and ordinary host tests, and resume only
    incomplete work. Never restart the whole suite or passed lanes for a harness repair.
12. Before ending an epoch, renew and durably hand off watcher ownership or issue cooperative
    `watch stop`, confirm exact watcher/controller absence, and record pending state. Heartbeat
    expiry is the fail-closed cleanup path if the manager disappears.

`PARALLEL_CHECKPOINT.md` must state the optional informational eligibility group, server snapshot,
last completed requirement, evidence paths, in-flight operation (`none` at a safe checkpoint), board/session/serial state, cleanup
performed, remaining work, and the exact first action on resume. A long soak or repetition loop
must define bounded epochs and persist cumulative counters so pause latency is bounded rather than
the full soak duration.

## 3. Test specification rules

The main model writes one immutable `.agent-workspace/SPEC.md` before spawning. Each spec must
contain:

- catalog test ID/title and source server commit;
- canonical named doer from `doer-roster.md`;
- objective and explicitly excluded behavior;
- required boards and roles;
- exact truthfully established MCU/package identifiers;
- manager-declared fixed fixture wiring and autonomous oracle material to the selected case;
- execution model (custom scheduler, ThreadX, or Zephyr when applicable);
- setup/build/flash/debug/lifecycle actions to exercise;
- seeded fault, if any, hidden oracle key location, and disclosure rule;
- numbered requirements, each with an observable pass and failure condition;
- build prerequisites and HIL prerequisites as separate dependency sets;
- internal catalog-defined shard map, when applicable;
- phase-specific resource requests and the immutable build-to-HIL artifact handoff;
- required raw evidence and final board state;
- mutation/risk class, applicable recorded delegated authorization, and whether the live plan
  exceeds it;
- finite time/retry bounds derived from the protocol or test objective;
- dependency prerequisites and requested exclusive/shared resources;
- disruptive USB, server-lifecycle, power, or cross-board scope; and
- safe checkpoint boundaries, bounded long-run epochs, and maximum pause latency.

The spec translates the catalog; it may not add evaluator-only prerequisites or any new
operator/physical action. Never require a PCA number, printed PCB revision, photograph, direct
visual chip inspection, removable label, cable move, button press, repositioning, rewiring,
jumper/solder change, DMM, logic analyzer, BLE sniffer, camera, oscilloscope, external power
instrument, or operator-timed event. Use the declared fixed fixture, stable electronic identity,
software-controlled fault injection, UART/peer/debug evidence, and live server plans. One truthful,
adequately correlated source is enough; do not demand duplicate modalities. Build and HIL
dependency lists contain only behavior actually consumed by that phase, never a blanket completion
barrier.

Do not reveal a seeded bug's answer to the test agent. State only the symptom and acceptance
behavior. Keep the answer key outside the run directory.

The test agent may amend application design details, but not weaken the spec. Only the main model
may append a spec correction, with reason and timestamp, before the affected action is rerun.
Removing a catalog-unsupported prerequisite is a correction rather than weakening; preserve valid
evidence and do not restart unrelated work.

## 4. Isolation and allowed inputs

At seal time the run root may contain only:

```text
stm32L476rgt.pdf
Nano_BLE_MCU-nRF52840_PS_v1.1.pdf
.agent-workspace/
```

The canonical baseline source files live in the task-owned asset directories under
`fresh-experiments/S10_20260726-034312/.agent-workspace/assets/datasheets/` and
`fresh-experiments/S11_20260726-034313/.agent-workspace/assets/datasheets/`; the scaffold preserves the
legacy filenames above inside each run for sealed-manifest compatibility.

For A24/A25 only, the manager may also place hashed copies of
`60852689.DS_SX1261_2 V2-2.pdf`, `waveshare-lora-module.pdf`, and
`nrf-sx-pin-mappings.md` in the run root. Fixed fixture facts belong in the manager-supplied
`.agent-workspace/FIXTURE.md`. No other parent/root document is allowed.

Their canonical sources are
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/sx1261-sx1262-v2.2.pdf`,
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/datasheets/waveshare-lora-module.pdf`, and
`fresh-experiments/A24_20260726-052146/.agent-workspace/assets/board-mappings/nrf-sx1262-pin-mappings.md`;
retain the legacy run-local names above.

The workspace may contain the generated spec, prompt, manifests, state, result schema, and an empty
evidence directory. After the agent starts it creates the application repository and all build
state in the run root.

The test agent may use:

- the two supplied local PDFs;
- for A24/A25 only, the three manager-supplied hashed CoreSX1262 inputs listed above;
- the run-local manager-supplied `.agent-workspace/FIXTURE.md` when the selected case needs fixed
  wiring, antenna, or bridge-state facts;
- official internet sources it finds itself;
- ordinary SDK/toolchain/package acquisition;
- the live BYO firmware MCP tools;
- physical boards named by the spec;
- files it creates in its own run.

It may not read:

- the master experiment Markdown;
- another experiment directory;
- server source/tests/docs or `.firm` from another project;
- parent/root documents other than the two copied baseline PDFs and the explicit A24/A25 inputs;
- pre-existing firmware examples or generated board profiles.

It may not invoke, read, or use `$change-loop` or `$plan-changes`. Those workflows are reserved
for the main model's verified production-server repairs.

It must not use direct pyOCD/OpenOCD/nrfjprog/J-Link/ST-LINK operations as a substitute for the MCP.
An ordinary vendor build tool is allowed. Independent autonomous oracles are limited to the
declared fixture and software/electronic evidence available without external lab equipment:
host-side serial logging, peer-observed counters, firmware protocol traces, debug/register state,
artifact inspection, and electronic identity. A spec must not request a logic analyzer, BLE/RF
sniffer, oscilloscope, DMM, camera, or another operator/external-instrument action.

## 5. Test-agent model and continuity contract

Invoke ordinary tests through `subagent exec`, not the regular internal subagent tool, with:

```text
fork_turns: none
model: gpt-5.6-luna
reasoning_effort: high
service_tier: default
task_name: firmware_lane_<doer-name-lower>
```

`default` is the regular tier required for Luna doers. `priority` is Codex Fast mode and is
reserved for Terra reviewers and repair roles; neither is a model suffix.

A23 is the sole provider exception. Invoke Nova, its one persistent doer, with Claude Sonnet 5 through a
persistent unrestricted/no-command-approval Claude launcher with no inherited parent conversation. Record the
launcher's exact model identifier and settings. Do not apply Codex `service_tier` or reasoning
labels to Claude. After one bounded retry window, transparently bind A23 to a persistent `gpt-5.6-luna`
high-reasoning regular/default fallback if the Claude provider is unavailable; record the necessary
model change and loss of the provider-comparison datapoint. Never substitute silently. Q40 is
manager-owned corpus aggregation rather than another base-application test-agent assignment;
assign each missing branch to one idle Atlas/Boreal/Cygnus/Delta session rather than creating a
branch-specific doer.

The test-agent task message must:

1. give the absolute run directory;
2. point to `.agent-workspace/TEST_AGENT_PROMPT.md` and `SPEC.md`;
3. require the first command to verify the run directory;
4. forbid server-source access and edits;
5. require autonomous firmware/test iteration;
6. require one result-contract terminal state, except for a manager-requested parallel checkpoint;
7. require raw evidence before returning; and
8. require pause-file checks at the sealed spec's safe boundaries.

The agent owns firmware code and tests. It should remain in one turn as long as useful. If it
returns early with progress prose, resume the recorded session through its recorded provider launcher and tell it to
continue from its durable state. Do not accept â€œlooks good,â€ a build-only result, or a flash-only
result. A requested pause is valid only with a complete `PARALLEL_CHECKPOINT.md`; it is not a PASS
or other terminal result. Do not create sequential disposable same-model sessions.

Keep the original session unless a model change is necessary or the session is irrecoverable.
Follow `model-continuity-contract.md` for the allowed reasons, required old/new identity record,
verified evidence boundary, and no-unnecessary-redo rule. A run already active on another model is
grandfathered and must not restart merely to adopt the new default.

Before starting that test agent, launch one persistent read-only reviewer with
`fork_turns: none`, `model: gpt-5.6-terra`, `reasoning_effort: high`, and
`service_tier: priority`. Its first task points
to `REVIEWER_PROMPT.md`, requires it to write `SPEC_ADVERSARIAL_REVIEW.md`, and forbids hardware
operations, server access, firmware/server edits, and change-loop use. Bind it with
`fresh_test.py bind-reviewer`, then let the main model append a signed `SPEC_AMENDMENTS.md` only
for a genuine spec error and call `fresh_test.py approve-spec`. Resume this recorded reviewerâ€”not a
new reviewerâ€”with the same model, reasoning, and service tier after a PASS claim for the evidence
review.

## 6. Main-model review

Before the main-model review, resume the one recorded read-only adversarial reviewer through
`subagent exec` for every PASS claim. Do not use the regular internal subagent tool.
It receives only the run directory and reads the sealed spec, result, report, and raw evidence. It
must not open or read `BYO-Firmware-MCP` (including its source, tests, documentation, runtime
state, or Git history), operate hardware, or edit firmware/server files. It writes
`.agent-workspace/ADVERSARIAL_REVIEW.md`. Its report either states
`NO_ACTIONABLE_SERVER_ISSUES` or supplies numbered criticisms with evidence paths, expected
observable behavior, server-versus-fixture/firmware reasoning, and a minimal observable
regression. Label each criticism `ACTIONABLE` or `ADVISORY`. Actionable findings demonstrate an
accepted requirement violation, credible safety/data-loss/identity risk, reproducible failure, or
likely hang/orchestration collapse. Speculative hardening, style, vanishingly unlikely cases
without evidence, unrelated features, and disproportionate complexity are advisory. Missing or
inadequate MCP guidance that blocks the required workflow is actionable; it is never permission to
inspect the server.

For `PASS`, verify only evidence applicable to the selected requirements:

- the initial manifest proves a fresh start;
- every numbered requirement has raw evidence;
- exact build commands exit zero and artifacts match the flashed plan;
- behavioral evidence comes after flash/reset and from the intended board;
- peer counters or independent oracles reconcile where required; no particular lab instrument is
  implied;
- debug conclusions identify the seeded cause rather than only changing symptoms;
- queue/RTOS tests include full/wraparound/ISR/priority/stack evidence when specified;
- temporary instrumentation is either removed or explicitly retained by the spec;
- final source diff is coherent and final board state is stated;
- no direct hardware utility bypassed the MCP.
- every adversarial criticism was independently accepted or rejected with recorded rationale.

Retain every previously accepted requirement/evidence edge whose spec, artifact, server snapshot,
fixture identity, and relevant behavior are unchanged. A rejected review triggers only the missing
or invalidated proof and one targeted reviewer follow-up; it never restarts the whole test or
reopens unrelated accepted requirements. When actionable findings are resolved and objective gates
pass, stop reviewing. Advisory findings are recorded but do not block delivery.

Resume the recorded test-agent session through its recorded provider launcher for gaps. If the continuity contract
requires a replacement, the replacement becomes the recorded owner and resumes the durable
evidence boundary without redoing already verified requirements merely because its model changed.
The main model may rerun host-only verification commands, inspect files, and compare evidence, but
it must not replace the agent as firmware implementer/tester outside that recorded exception.

For `SERVER_FAILURE`, require at least:

- exact MCP call sequence and complete response/error;
- expected behavior tied to the spec/server contract;
- target/server commit and run state;
- proof the correct artifact, board, and applicable wiring/SDK/preconditions were used;
- a minimal repeatable reproducer;
- a second observation or a strong explanation why repetition is unsafe;
- proof the failure remains when firmware/test mistakes are corrected.

## 7. Server-failure escalation

The main model independently reads the server contract and relevant code. Only if the defect is a
real production-code server defect, create a narrow change request and run `$change-loop` with a
test-specific `CL_RUNTIME_DIR`. Do not use change-loop for documentation-only/metadata-only,
firmware, fixture, SDK, host, test-spec, or evidence work.

Before editing the server, add the validated defect to `SERVER_REPAIR_QUEUE.md`, stop new
server-consuming/HIL launches, request and receive bounded checkpoints from all active server/HIL
consumers, and record those consumers `FROZEN`. Isolated board-free non-server phases may continue.
Do not hold a model turn open to poll; wait on role/process completion. Only the main model may
drain the queue, and it does so serially with one production repair/change-loop at a time.

The current main/orchestrating model directly authors the one plan; never delegate plan authorship
to a subagent, Codex exec planner, doer, or tester. Conduct one read-only adversarial plan review.
Record the reviewed plan SHA-256,
reviewer identity, and its numbered risks/test targets in `plan-review.md`, then begin the
change-loop immediately. If execution proves a genuine plan mistake, the main model records a
minimal evidence-backed amendment and obtains one targeted review of that amendment only; it does
not regenerate the whole plan or re-review unchanged items. The neutral gate and the subsequent
targeted retest remain the correctness backstops.

The repair must:

- be general rather than board-specific;
- preserve live plan/permission gates;
- include spec and regression tests owned by change-loop tester roles;
- rerun only failed or invalidated checks and affected regressions; retain unchanged passing gate
  evidence rather than restarting expensive tests or experiments from scratch;
- avoid editing the fresh firmware run;
- avoid changing the test to make the failure disappear;
- pass the neutral change-loop gate before HIL retest.

After each repair passes its neutral gate, keep unrelated server/HIL consumers frozen, restart an isolated MCP
process for the reporting run, and resume only its recorded agent for the minimal reproducer and
requirements reached by that change. Close the queue item only after that targeted retest passes,
then process the next item serially. After the queue is drained, record one final server snapshot,
restart every checkpointed MCP process from it, remove pause requests, and resume the recorded sessions
through their recorded provider launchers (or their formally recorded necessary replacements). Unaffected agents
resume their exact checkpoint. Do not repeat unrelated expensive acceptance or soak work unless
change scope requires it.

## 8. Recovery and resumption

Durable truth lives in:

- root `.agent-workspace/SUITE_COORDINATION.md`
- root `.agent-workspace/SERVER_REPAIR_QUEUE.md`
- `.agent-workspace/RUN_STATE.json`
- `.agent-workspace/SPEC.md`
- `.agent-workspace/RESULT.json`
- `.agent-workspace/TEST_REPORT.md`
- `.agent-workspace/PARALLEL_CHECKPOINT.md` when paused
- `.agent-workspace/evidence/`

Before compaction or session exit, record every active test/shard, phase, leases, server snapshot, run path,
agent ID/task/model, pause/checkpoint state, queued repair, server change-loop runtime, last
verified evidence, and exact next follow-up. Never discard a session mapping merely because its
last turn failed.

<!-- END SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/references/execution-contract.md -->
### Snapshot: `Firmware/Firmware resources/test-program/run-firmware-test-suite/references/result-contract.md`

<!-- BEGIN SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/references/result-contract.md -->
# Test Result Contract

The test agent writes both:

- `.agent-workspace/RESULT.json` for deterministic validation
- `.agent-workspace/TEST_REPORT.md` for human evidence review

## Main-run terminal statuses

### `PASS`

All spec requirements were executed and passed on the required hardware. Build/flash alone is not
PASS. The result includes raw evidence paths and final board state.

### `SERVER_FAILURE`

The agent has corrected or ruled out firmware, SDK, fixture, identity, and precondition mistakes
and has a minimal reproducible MCP server defect. It must not edit the server.

### Prohibited main-run blocker statuses

`NEEDS_USER` and `INFRA_BLOCKED` are invalid for this suite's main-catalog runs. A doer must not
create a terminal result or ask the user to touch/inspect hardware, supply another approval
utterance, install equipment, or resolve routine infrastructure.

The manager instead applies recorded delegated authorization, repairs ordinary infrastructure,
uses an autonomous electronic/software oracle, or appends a signed spec correction. A temporarily
unavailable resource is a nonterminal `WAITING_FOR_RESOURCE` or `WAITING_FOR_PROVIDER` ledger state:
checkpoint the persistent session and continue every unrelated lane. An intrinsically
manual/special-equipment branch belongs only in non-gating Appendix A, where it receives
`SKIPPED_AUTONOMY_REQUIRED`.

There is intentionally no terminal `FIRMWARE_FAILURE`. Resume the recorded persistent test agent
while it remains usable. If a necessary model change or irrecoverable session requires replacement,
record the continuity handoff defined in `model-continuity-contract.md`; the replacement continues
from the verified evidence boundary rather than restarting the test.

A manager-requested harness-assisted parallel pause is also not a terminal result. At a sealed safe
boundary, write `PARALLEL_CHECKPOINT.md` and return without creating or changing `RESULT.json`.
Resume the same persistent agent after the repair barrier. Never encode a coordination pause as a
terminal result.

`SKIPPED_AUTONOMY_REQUIRED` is a suite-ledger disposition for non-gating Appendix A only. It is not
a main-run `RESULT.json` terminal status and never satisfies or blocks a main catalog gate.

## Required JSON fields

```json
{
  "schema_version": 1,
  "test_id": "A20",
  "status": "PASS",
  "summary": "One-sentence evidence-based outcome.",
  "run_directory": "absolute path",
  "server_commit": "git commit under test",
  "firmware_commit": "fresh repo commit or null with explanation",
  "hardware": [
    {
      "friendly_name": "name used through setup",
      "board": "NUCLEO-L476RG",
      "mcu": "STM32L476RGT6",
      "role": "controller",
      "identity_evidence": "relative evidence path"
    }
  ],
  "requirements": [
    {
      "id": "REQ-001",
      "status": "PASS",
      "evidence": ["relative/path.txt"]
    }
  ],
  "commands": [
    {
      "command": "exact argv or command",
      "cwd": "absolute or run-relative cwd",
      "exit_code": 0,
      "evidence": "relative/path.log"
    }
  ],
  "mcp_evidence": ["relative/path.json"],
  "oracle_evidence": ["relative/path.txt"],
  "final_board_state": "observed state and how it was observed",
  "server_failure": null,
  "blocking_request": null,
  "remaining_work": []
}
```

For `SERVER_FAILURE`, replace `server_failure: null` with:

```json
{
  "observed": "exact observed behavior",
  "expected": "contract/spec behavior",
  "minimal_reproducer": ["ordered exact calls"],
  "reproduced_count": 2,
  "evidence": ["relative/raw-output.json"],
  "ruled_out": ["firmware", "artifact", "board identity", "wiring", "SDK"],
  "suspected_server_scope": ["module or tool name if known"]
}
```

For every main-run result, `blocking_request` is `null`. Waiting work is recorded in
`SUITE_COORDINATION.md`, not `RESULT.json`.

## Report requirements

`TEST_REPORT.md` maps each spec requirement to:

1. action performed;
2. raw evidence path;
3. independent oracle, if required;
4. observed result;
5. verdict;
6. cleanup/final state.

Do not paste only summaries. Preserve exact commands, MCP outputs, artifact hashes, UART/peer
counters, and timestamps in evidence files.

<!-- END SNAPSHOT Firmware/Firmware resources/test-program/run-firmware-test-suite/references/result-contract.md -->
--- END-NORMATIVE-SNAPSHOTS ---

<!-- BEGIN-PRESERVED-HANDOFF-SUFFIX -->
# Firmware V2 Harness Handoff

## Goal and current status

Deliver the generalized harness promptly while preventing deployed production bugs. The governing
contract is `goal.md` and `plans/general-coding-harness/EXECUTION_PLAN_2.md`.

Execution is user-paused. Do not launch/resume workers, MCP, C3, hardware, or promotion until the
user explicitly resumes. The last inspection found no live controller, resource claim, MCP, or
hardware process.

## Completed, verified work

- Stable runner: `4699d27`; pinned immutable BYO Firmware MCP fixture: `f003f84`.
- Candidate baseline: `659dd03`, preserving 140 credited green IDs.
- C3 control-plane defects were repaired in bounded batches. Fresh C0-0014 at joined tip
  `b5753eb` passed with no admissible finding.
- Current-tip CP04 all-child-Fast smoke passed 1/1; remaining focused docs execution passed 2/2.
- All launched child roles use the required Fast/priority tier and prescribed model/effort.
- C3/hardware has never started; the MCP fixture remains unmodified.

## Resume topology and decisions

For production/material changes: form a frozen joined tip, run the shortest affected smoke, then
run complete C0 and remaining focused execution in parallel on that exact tip. Repair accepted
production findings as one serial batch and reconcile dependency map, registry, and aggregate
evidence once per accepted batch tip.

For a strict test-only fast lane, all conditions must be recorded: the diff is limited to synthetic
fixture/setup or test metadata; exact failed IDs are known; and production, policy, contract, locked
configuration, test oracle, assertion strength, expected outcome, stable ID, and coverage obligation
are unchanged. Continue in the same test-author lane and rerun exactly those IDs once before any
unrelated work. Do not create C0, ordinary review, or reconciliation. Failed or unproved eligibility
uses the material route. Administrative-only corrections remain in the same lane with no rerun.

## Immediate next step after explicit resume

ROOT first validates and archives the finished joined-tip evidence, then reconciles once before C1:

```powershell
Get-Content -LiteralPath 'plans/general-coding-harness/runtime/firmware-v2/final/lanes/F.C0.FR1-0014/.agent-workspace/RESULT.json' -Raw
Get-Content -LiteralPath 'plans/general-coding-harness/runtime/firmware-v2/implementation/lanes/S23.D2-C3-REMAINING-0004/.agent-workspace/RESULT.json' -Raw
```

If both artifacts and their exact-tip bindings are valid, build one `b5753eb` dependency map,
reconcile the passed registry and aggregate evidence once, then advance the reserved candidate and
create fresh C1/C2. Do not rerun green IDs unless their dependency fingerprint changed.

## Files in flight and checks not run

- Pending: ROOT admission/archive, one `b5753eb` reconciliation, candidate advance, fresh C1,
  dependency-invalidated C2, C3, C4, safeguard, promotion, and outer verification.
- No current C1/C2 is operative; historical locks are superseded.
- No full repository verifier was run for this documentation-only handoff refresh.

## Governing hashes

- `goal.md`: `e96969e0b16190d06603973bf15e24a79a8b5869f3caf2bcb22937618898e19d`
- `active_docs/GENERALIZATION_SPEC_2.md`: `4f922396a442e860969423394072e1ee953ed6191cd8ed7c8529dc2e6b8d1b07`
- `active_docs/IMPLEMENTATION_ROADMAP_2.md`: `d6d99bf0cdbc8020c320e7c5d997da4ebfb98549ef1e83addff35a7422455250`
- `active_docs/EXECUTION_READINESS_2.md`: `e4587d0e0339b496aadf6ffa0c6a6af5127f3c11643410182e53240304417c66`
- `plans/general-coding-harness/EXECUTION_PLAN_2.md`: `ba3b2c39594d5865902601408b3f57a28d215cd36bc9f273b56d55f39275b261`

<!-- END-PRESERVED-HANDOFF-SUFFIX -->
