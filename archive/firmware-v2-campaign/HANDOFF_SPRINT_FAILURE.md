# Sprint failure investigation - why no firmware sprint has completed (Plan 2)

> **Archived at closure (2026-08-21).** The Firmware campaign was ended by user decision and the
> WIP harness was published. This investigation is retained for history only; it cannot authorize
> a resumed sprint. See the current [`HANDOFF.md`](../../HANDOFF.md).

Status: working investigation record. This file documents every interrupted sprint epoch, the
exact reason each one stopped, why the system could not recover, and what recovery should have
looked like. It preserves the documentation-error audit and the user's explicit requirement.
Historical sources are the archived `active-docs/goal.md`,
`general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md`, and
`firmware-docs/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`; this file is analysis, not authority.

## 1. Verdict

- The blocking pattern across all 8 epochs is the orchestration state lifecycle: an interrupted
  run leaves claims, sessions, and identities that no later epoch may legally clear, extend, or
  revive. Every interruption is therefore terminal and forces a full cold start.
- The only canonical plan-level blocker is spec-plan-2, but not because it bans resume: it has a
  resume route (EXC-SUITE-CHECKPOINT) and EDGE-012 says interruptions "follow the suite checkpoint
  route." The structural problem is the gate: the checkpoint must prove "target, resource leases,
  and required runtime identities remain valid," and every other path requires amendment or
  `INCOMPLETE`. After a forced stop the controller is killed before publishing complete boundary
  evidence, claims come back `MAY_EXIST_INCOMPLETE` / `INVENTORY_UNKNOWN`, the checkpoint can never
  prove validity, and `INCOMPLETE` (terminal) is the only legal outcome.
- So the failure is a gap, not a wrong rule: the plan specified a fail-closed model but never
  specified the disposition path that model requires (how to legally close or adopt ambiguous
  claims so a sprint can resume). That gap made every interruption terminal.
- Contributing layers (worse, not root): the agent-authored HANDOFF.md over-generalized into
  "do not revive anything" and dropped the checkpoint route; the orchestrator never exercised the
  checkpoint route and cold-started instead.
- Only 2 of the 8 epochs had a genuine harness defect (a21-002 watcher `CREATE_BREAKAWAY_FROM_JOB`,
  suite-003 Boreal pre-provider exits). Both were repaired. None of the other six was a harness
  failure; each died on an authority/resource/boundary mechanism.

## 2. What the user wants fixed

- Fix the lifecycle so sprints continue to completion and recover from whatever errors are needed:
  do not treat an interruption as the end of the sprint. Resume or recover in place: adopt and
  continue, close or reassign stale claims, replace a bad session, and keep the lane going until
  its work is genuinely complete.
- Review at the end: the sprint completes first; any harness issues observed during the run are
  pooled (collected as a batch) and fixed; the completed sprint is then reviewed and validated.
  Do not stop a sprint mid-run to fix harness issues.
- Stop condition: 3 consecutive no-harness-error, complete sprints.
- Plan 2 v3.9.23, `goal.md`, and `HANDOFF.md` now make this the operative requirement: three
  index-ordered completed/accepted sprints with no harness finding, with findings pooled only after
  the affected sprint completes.

## 3. Failure inventory - every epoch, why it failed, what recovery should have been

### 3.1 `20260815-plan2-a21-001` - INCOMPLETE_NOT_PASSED (product + hardware)

What happened:
- Sealed dual-STM32 I2C spec, distinct controller/responder firmware, STM-A electronic validation
  completed. STM-B was absent (not connected). The server refused the first STM-A flash before
  writing because the initial stack pointer was outside verified writable RAM: SRAM1 was declared
  128 KiB, actual verified writable RAM is 96 KiB.
- The doer corrected SRAM1 to 96 KiB and rebuilt, but the attempt stopped before that correction
  was committed or republished. No flash/reset/serial/debug mutation completed, no RESULT.json.

Why it failed:
- Product-side spec error (wrong SRAM extent) plus hardware availability (STM-B absent). The
  server's pre-flash validation correctly caught the unsafe image. The lane stopped before the
  corrected build could be republished, and there was no legal way to continue the same attempt.

Recovery that should have happened:
- Adopt the corrected 96 KiB build and the sealed spec; re-validate the image; wait for or verify
  STM-B (it later appeared on COM17 probe `0668FF514988525067213913`); continue the two-board
  proof in the same sprint. STM-A evidence was preserved and reusable. No new spec needed.

### 3.2 `20260816-plan2-a21-002` - stopped at SPEC_REVIEWED (harness defect)

What happened:
- Fresh retry reached `SPEC_REVIEWED` with a Qwen-approved contract and no findings. ROOT stopped
  the A21-only manager before any doer, lease, MCP action, or hardware action because the normal
  watcher `start` path failed inside the lane controller's Windows Job Object: Windows requested
  `CREATE_BREAKAWAY_FROM_JOB` even though the owner-bound watcher should remain in the lane.

Why it failed:
- Genuine harness defect in the lane controller and watcher launch path. A two-file repair was
  produced, Terra xhigh returned zero findings, and a separate doer proved native
  `start -> READY -> status -> cooperative stop` inside the Job Object; all 52 affected watcher
  tests passed.

Recovery that should have happened:
- Record the harness defect permanently, preserve the sealed `SPEC_REVIEWED` checkpoint, isolate
  only the affected action, and continue every other feasible unit under replacement runtime and
  fresh live authority. The sprint then publishes `COMPLETED_WITH_FINDINGS`; ROOT repairs the
  pooled harness batch afterward. The sprint earns no clean credit.

### 3.3 `suite-003` - BLOCKED_FOR_ROOT_TARGET_REPAIR_CLEANED (harness defect)

What happened:
- Three distinct Boreal invocations exited before status publication, claim acquisition, or
  provider start (pre-provider exits). Four exact resource claims were held and released safely.
  No hardware plan, permission, lease, action, or result was created. Terminal state was clean.

Why it failed:
- Provider-launch defect in the suite's Qwen route (launch shape or pre-provider exit), not the
  target product. This was a real harness defect.

Recovery that should have happened:
- Preserve and pool the launch defect, record the affected unit truthfully, continue all other
  feasible units, and complete the same logical sprint as `COMPLETED_WITH_FINDINGS` rather than
  retiring it. ROOT repairs the pooled harness batch only after that terminal handoff; the sprint
  earns no clean credit.

### 3.4 `suite-004` - ROOT barrier (stale claim plus unassigned adapter)

What happened:
- A21 controller (PID 168480) was externally stopped at a file-edit boundary; the controller did
  not publish complete retained-boundary cleanup; its exact `board:STM-A` claim remained armed as
  `MAY_EXIST_INCOMPLETE`. A fresh controller waited on that exact claim and never launched.
- The accepted target correctly refuses to reclaim that claim, and the suite rules forbid manual
  delete or edit of the claim or revival of the stopped session. Deadlock.
- A25: both Nordic identities were validated and exact role images were flashed under fresh plans;
  Delta later attempted an unassigned host Intel Bluetooth adapter; ROOT stopped the lane safely.
- D30 waited on A20 debug-trampoline input; dependent lanes were not launched because their
  declared edges did not become terminally satisfied.

Why it failed:
- No legal disposition path for an incomplete retained-boundary claim: the claim could not be
  deleted, edited, reclaimed, or consulted as current authority, and its owning controller was
  absent. A doer also touched hardware it was not assigned, so ROOT stopped the lane.

Recovery that should have happened:
- Formal claim disposition: after verifying the owning controller and provider are absent and no
  live hardware operation exists, allow a ROOT-adopted disposition record to close the stale claim
  and relaunch A21. For A25: grant explicit host-BLE authority or accept a spec-valid fixture-only
  BLE stimulus topology, then continue the same lane. Only the affected lanes pause.

### 3.5 `suite-005` - ROOT launch-authority barrier (identity cannot be extended)

What happened:
- A21's canonical persistent provider identity had only provider, workspace, cache, and artifact
  resources; canonical resume cannot add the required STM boards, probes, serial endpoints,
  MCP, or server claims. ROOT instruction `root-a21-missing-hardware-claims-001`; no doer
  launched, no HIL. D30 and D34 completed board-free work and left `BUILT_WAITING_FOR_LEASE.md`.

Why:
- The identity and claim model cannot be extended on resume. The lane was stopped because
  continuing would violate the fresh plan, permission, lease, and identity boundary. This was an
  identity-design gap, not a harness error.

Recovery that should have happened:
- Create the identity with a complete canonical claim set from the start (hardware claims bound at
  identity creation), or provide a formal claim-extension route before launch. A21 then launches
  with a fully-claimed fresh identity; D30 and D34 resume from their checkpoints.

### 3.6 `suite-006` - continuation and retained-boundary barrier

What happened:
- A21: ROOT required the next exact-session continuation to carry the PLLM and PLLR correction in
  the active prompt. The persisted `task_card_sha256` was the assembled-markdown digest rather
  than the digest of an existing readable JSON artifact; the reviewed-amendment validator requires
  an old JSON artifact with that exact raw digest. A truthful reviewed amendment therefore cannot
  be admitted. A21 stopped; no post-instruction edit, rebuild, plan, or flash occurred.
- A25: the first wrapper receipt was a false positive - nested quoting stripped PowerShell
  variable sigils. A later escaped inline launch acquired all 22 exact claims and resumed a
  session, but did not satisfy ROOT's newly required task-local `.ps1` launch shape. Before its
  exact stop completed, the provider accepted and dispatched one planned, authorized,
  non-destructive board-setup action (no flash, serial, radio, erase, or power action observed).
  The exact controller stop closed its job descendants but prevented the controller from
  publishing complete retained-boundary evidence. The corrected launch receipt then stopped at
  `WAITING_RESOURCE`; 22 fail-closed claims all `INVENTORY_UNKNOWN`, owned by absent controller
  PID 191680. The resource boundary is intentionally not empty - fail-closed claims cannot be
  cleared manually.

Why it failed:
- Tooling bugs (PowerShell quoting in the wrapper), launch-shape drift (a new `.ps1` requirement
  mid-run), and a stop protocol that prevented the controller from publishing boundary evidence,
  leaving stale claims with no disposition path. The validator digest mismatch blocked the
  amendment.

Recovery that should have happened:
- Fix the wrapper quoting; fix or register the validator so a truthful reviewed amendment is
  admitted (or store the exact JSON artifact); require the controller to publish boundary
  evidence before stop completes; then dispose the fail-closed claims via a ROOT-adopted
  reconcile-after-verify-absent route and relaunch A25.

### 3.7 `suite-007` - ROOT-owned scope barrier, forced containment (ROOT error)

What happened:
- Epoch-level `ROOT_A21_CLOCK_DIAGNOSIS.md` admitted only the three-line
  `firmware/common/clock.c` correction, one rebuild per role, disassembly proof, and flashes to
  the already assigned boards. A21 commit `4a888b6` changes exactly those three lines; rebuilt
  images and both flashes were within ROOT's intended scope.
- The run-local `ROOT_DIAGNOSIS.md` still required a pause at the safe boundary, and
  `PAUSE_REQUESTED.md` remained present. ROOT failed to remove or replace those stricter live
  signals after admitting continuation. A25 also continued while its pause marker remained
  present, with an interrupted flash outcome (a one-file UUID construction/copy/compare
  correction, temporary only). The manager correctly enforced the pause and force-contained both
  provider trees.
- Classification: ROOT-owned orchestration error, not a target or server defect.

Why:
- Contradictory ROOT sidecars (epoch-level admit vs run-local pause) confused the manager and
  the doers. The manager was right to contain; ROOT was wrong to leave the live signals.

Recovery that should have happened:
- ROOT removes or expires run-local pause markers atomically when it authorizes continuation.
  The A21 clock commit and its flashes are source evidence that a fresh authority can adopt;
  A25's one-file UUID correction is evidence for a fresh doer to independently read back, commit,
  rebuild, and prove. Electronic state is revalidated before any flash.

### 3.8 `suite-008` - stopped by lane authority violations (fresh parallel runtime)

What happened:
- Watcher READY; A21 (Boreal) and A25 (Delta) overlapped with disjoint complete claim sets (18
  and 22 claims) - the desired parallel shape worked. D30 and D34 read-only reviewer continuity.
- A21: a stale resumed session was stopped; a fresh replacement launched with an exact contract;
  then at 15:36 `A21_FRESH_REPLACEMENT_ORDER_VIOLATION_STOP_REQUESTED` - source diff exact, pre-
  gate validations passed, but `responder_byte_identity_gate_complete` was false when the doer
  proceeded; stop before further MCP or flash.
- A25: the first live `setup_overview` call was malformed (first-call-malformed, 3 attempts);
  `A25_ONE_CALL_ROUTE_GATE_VIOLATION_STOP_REQUESTED` at 15:37 - no flash, no hardware mutation.
- Manager log ended with both lanes waiting on ROOT; no terminal handoff was published for the
  epoch (the ledger remains at `PREPARING_FRESH_PARALLEL_RUNTIME`).

Why it failed:
- A doer order violation (flash attempt before the responder byte-identity gate completed) and a
  malformed first MCP call. These are lane-level doer mistakes - the correct response is to pause
  that lane, not end the whole suite.

Recovery that should have happened:
- A21: hold until the byte-identity gate completes, then flash; do not pre-empt.
- A25: allow one corrected invocation shape (the malformed call is a wrapper or schema bug) and
  continue with one `setup_overview` call.
- Keep the unaffected lanes running; pool the two lane defects as harness fixes; then finish both
  sprints and review at the end.

## 4. Why every interruption became terminal - the causal chain

1. Interruption triggers: doer errors, 2 real harness defects, ROOT churn - none is a sprint-
   failed signal.
2. The plan's only legal resume route is EXC-SUITE-CHECKPOINT, gated on proof that the target,
   leases, and identities are still valid.
3. Forced stops prevent the controller from publishing complete boundary evidence; claims come
   back `MAY_EXIST_INCOMPLETE` or `INVENTORY_UNKNOWN`.
4. The gate then fails; the only remaining legal outcome is `INCOMPLETE` (terminal).
5. No claim-disposition / retained-boundary recovery interface exists (spec gap).
6. The agent HANDOFF over-generalized the scoped no-revival rules; the orchestrator cold-started
   every epoch instead of exercising the checkpoint route.
7. Net result: 0 accepted sprints out of 8 epochs despite 6 with no harness error - the sprints
   never got a chance to finish.

## 5. Documentation audit - language that blocks interrupted-sprint resume

(Full detail is preserved in `active_docs/for-jason.md`; summary here.)

- `plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` - STRUCTURAL BLOCKER:
  resumption rule "Use only EXC-SUITE-CHECKPOINT; every other new graph or authority route
  requires amendment or `INCOMPLETE`"; EXC-SUITE-CHECKPOINT validity gate; BOUND-001 "fresh suite
  epoch" and "without reviving imported processes, leases, or a broad unrecorded permission".
- `HANDOFF.md` (repo root) - agent-authored blanket: "Do not reset, clean, or revive an imported
  process, lease, session, stopped A21 attempt, or Q11 run." (user did not write this).
- `active_docs/goal.md` - one scoped sentence "Do not revive that attempt" (a21-001 only) and
  "acquire new authority for every live action"; goal.md also has supporting recovery language
  ("administrative launch recovery", "provider-session continuity is preferred").
- `Firmware/target-harness/.agent-workspace/PLAN2_*_MANAGER_PROMPT_*.md` - literal per-run bans
  ("Never revive the prior manager...", "Do not revive any controller, provider session, watcher,
  MCP lifetime, plan, permission, lease, validation stamp, or resource claim from it.").

Docs that ALREADY permit resume (do NOT need changing):
- `Firmware/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`: "Eagerly launch or resume every doer
  whose next phase is dependency-ready"; "resume only incomplete work after the controller issue
  is corrected. Do not restart the whole suite or already-passed lanes."
- `Firmware/.codex/skills/run-firmware-test-suite/SKILL.md`: reconcile evidence before deciding
  what can be resumed; if an imported checkpoint is not materialized, create a fresh affected run
  with an explicit continuity handoff.
- `Firmware/.agent-workspace/SUITE_COORDINATION.md` and `Firmware/AGENTS.md`: "do not revive"
  scoped to imported historical records only.
- `Firmware/PROVIDER_ADAPTER.md`: "preserve the named session across normal resume".

## 6. Applied correction

The fix is a workflow-contract correction, not a new recovery subsystem:

1. The test orchestrator retains ownership of every logical lane and sprint until completion,
   replacing failed runtime/provider identities while preserving verified semantic progress.
2. Correctable execution faults are handled inside the sprint. ROOT receives only a completed
   terminal pool, never an intermediate request to terminate or repair the sprint.
3. Confirmed harness defects are repaired by ROOT between completed sprints. The affected sprint
   resets/no-counts; the next sprint runs on the accepted repaired target.
4. Plan 2 completes only after three consecutive completed, accepted, harness-clean sprints.

For every possible harness error, the test orchestrator records a suspected finding with the
affected lane/unit, evidence, observed and expected behavior, containment, whether other work
continued, and cleanup/uncertainty. It never declares the defect or requests a mid-sprint ROOT
decision. ROOT reviews the complete terminal pool, confirms or rejects each suspicion, authorizes
only justified between-sprint repairs, and resets the streak only for a confirmed harness defect.

## 7. Resolution status - Plan 2 v3.9.25

- The accepted target remains `dd673cb...`, tree `c18ccd0...`; M07 and M08 credit remain valid.
- No product-code change or special no-hardware recovery check is required before live resumption.
- The unaccepted continuation-repair implementation, test asset, worktrees, branches, temporary
  decision state, and bounded-test receipts were deleted rather than preserved as a second system.
- Plan 2 resumes directly at `EDGE-011 -> MI-FIRMWARE-SPRINT` through prepared prompt 009.
- The unfinished suite-008 logical sprint keeps its verified A21, A25, D30, and D34 progress under
  fresh runtime authority. Only affected or uncertain units are revalidated.
- Normal terminal states are `COMPLETED_CLEAN` and `COMPLETED_WITH_FINDINGS`. `INCOMPLETE` remains
  limited to explicit user cancellation or withdrawn authority.
