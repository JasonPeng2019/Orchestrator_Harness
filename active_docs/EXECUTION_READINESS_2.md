# EXECUTION_READINESS_2: Firmware V2 Launch Boundary

Status: **PAUSED FOR NEXT-RUN PREPARATION; RESUME REQUIRES EXPLICIT USER DIRECTION**  
Observed: 2026-08-06, America/Los_Angeles

This record originally closed static launch ambiguities for `goal.md` and `EXECUTION_PLAN_2`.
Execution has completed preflight, S1-S3, and the bounded S30 retained-session repair through joined
tip `6649cf201ded9782c2cb3bc56983f4a560728ea8`. Its focused four-ID execution is green, but ROOT has
not yet archived/admitted that tip to the reserved candidate. The user paused execution while the
topology, two S4 candidate features, the four immediately-following S5 efficiency/evidence features,
and external C3 support layer were prepared. The external
support/helper source, 16 focused tests, eight-check smoke, independent Luna practical, and full
repository gate are green; preparation no longer blocks resume. This record is not
hardware evidence or permission to skip S4/S5 or the dependency-scoped final gates. On explicit resume,
ROOT preserves valid S30 evidence, admits the joined tip if its fingerprint is unchanged, completes
S4 and S5, then runs fresh C0/C1 and only dependency-invalidated C2 work.

## 1. Reserved clean coordinates

The following locations and branches are reserved for this plan:

| Purpose | Path | Branch / base |
|---|---|---|
| Harness candidate | `plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/` | clean `firmware/v2-candidate` at `c6999d173c344b317a918df91619308fd9f93f63` before admission of tested S30 joined tip `6649cf201ded9782c2cb3bc56983f4a560728ea8` |
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
- The retained harness Git common store currently reports 137 registered worktrees. This includes
  the protected completed-project set, reserved candidate/MCP state, and accumulated V2
  implementation/final lanes. It is never a broad cleanup target. Before S5, all remain untouched;
  after S5 acceptance, only individually proven terminal V2 lanes satisfying C75 may retire. The 13
  protected historical worktrees, dirty/ambiguous state, live paths, unretained revisions, and
  unpreserved evidence remain excluded.
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

For C3, `ROOT-IM` uses this launch shape to start `F.C3.O` and, only when useful, optional
supplemental reviewer `F.C3.W`. ROOT starts the required deterministic observer directly as a
non-agent process by composing `.codex/scripts/c3_outer_support.py` with
`.codex/scripts/c3_watcher_helper.py`.
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
and requires the live set to be covered by the operative C1 plus valid append-only change
dispositions. It binds the live set into dispatch admission and dispatch/result. An unclassified
mismatch expires pending calls, refuses dispatch, emits `GOVERNING_INPUT_CHANGED`, and invokes
live-goal handling. ROOT classifies changed domains, refreshes C1 if needed, and preserves all
non-consuming green gates. A ROOT-owned read-only watcher monitors during in-flight mutation;
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

The fault boundary admits ordinary coordinator/orchestrator/worker and support-layer mistakes as
recoverable test work. A bad assignment, command, ordering choice, target edit, invalid call, result
envelope, helper record, launch, report, or cleanup step is returned to its owner and selectively
corrected. It does not reset the candidate, implementation steps, C1, or unaffected green tests.
When an immutable C3 attempt cannot close, only the attempt namespace rolls unless exact evidence
shows a changed product dependency, incorrect candidate behavior, or an untrustworthy candidate
result.

Before target work, ROOT directly launches the deterministic helper, records exact process identity,
and waits for ready evidence. The helper writes heartbeat/cursor and terminal-service evidence.
Ordinary findings are pooled through the complete assigned surface. Only exact evidence of an
unauthorized/wrong-resource operation, loss of live-process containment/cleanup, or irreversible
acceptance-evidence corruption requests immediate stop. A safety stop preserves product credit and
is classified after containment.

P4 ordering is candidate-managed shutdown; ROOT helper stop/reap; create-once
`WATCHER_OBSERVATION_CLOSE.json`; then O manifest closure. The close record resolves helper identity,
ready, heartbeat, abort disposition, terminal service, and exit using the normal source or the
predeclared independent fallback matrix. Missing facts with no complete fallback make only the
affected attempt incomplete. O validates the record through the reusable support validator rather
than a historical sealer. Optional AI-watcher report/exit evidence is supplemental.

Termination first requests controller-managed shutdown. Only if the exact registered controller is
unavailable/unresponsive may ROOT host-terminate/reap its pre-registered identities. Cleanup never
signals an unverified PID: already-gone/identity-uncertain children are recorded, and cleanup
continues for every other registered child. No MCP/hardware/broad-kill authority is granted.

ROOT separately monitors O's exact process and `topology/ORCHESTRATOR_HEARTBEATS.jsonl` at the same
30/90-second cadence through result commitment and normal exit. Manifest creation starts an absolute
90-second result deadline. Unexpected O exit, lost/stale heartbeat, deadline without valid result,
or exit without result is `ORCHESTRATOR_LOST`: stop/reap registered topology, preserve the partial
attempt, write `topology/ORCHESTRATOR_LOST.json`, and classify under the support-failure boundary.
Use a fresh attempt only when the required product result cannot be reconstructed honestly. Partial
manifest/result files are never completed or reused.
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

### S4 candidate-feature readiness

S4 is a required product stage, not an outer-support hot patch. Its authoritative contract is
`task-card-spec.md`. The candidate must validate and bind task cards, render focused prompts from
their structured context, publish the fixed entrypoint scoring scale, and emit a durable
`LANE_RESULT_READY_FOR_SEMANTIC_ACCEPTANCE` event with exact task-card/result paths and hashes. No
dependent lane starts until ROOT writes a hash-bound verdict. `ACCEPT-WITHIN-TOLERANCE` may apply
only to criteria explicitly marked `orchestrator_judgment`; strict criteria remain mandatory.

The same stage adds one report-only recovery attempt after a missing or structurally invalid terminal
artifact. The exact validator error returns to the same retained thread. That continuation cannot
edit code/tests, rerun execution, or invent evidence; absent evidence yields `INCOMPLETE`. A second
invalid artifact stops. Focused units and one disposable fake-Codex smoke must prove these boundaries
before S4 can unlock S5.

### S5 candidate-feature readiness

S5 is mandatory immediately after accepted S4 and before the first fresh C0. It is a candidate
feature stage, not permission to edit the frozen stable runner or to start external work. ROOT first
writes a focused feature plan for C74-C77 on the exact S4 tip. One Terra-medium-Fast coder implements
the bounded change; one Terra-medium-Fast reviewer and one disjoint Luna-high-Fast doer review and
test it; ROOT pools their results once.

S5 must prove four behaviors with focused units and disposable practical tests: an accepted logical
task thread cannot be reused for unrelated work; terminal accepted lanes leave active discovery only
after evidence/revision preservation and safe worktree closure; static read-only lanes use an exact
immutable source view and separate writable result root without allocating a linked worktree; and
concurrent event-log writers wait on one cross-process lock and never interleave, corrupt, or lose a
record. The retirement practical may touch only proven terminal V2 lanes and disposable fixtures;
protected historical, dirty, ambiguous, live, or unpreserved state remains untouched.

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

Every post-C1 governing hash change pauses new admission until ROOT records its append-only change
classification and refreshes C1 when current hashes must be rebound. A hardware-authority or
in-flight-mutation-domain change revokes affected calls immediately. Byte-only changes may use the
C1-rooted editorial chain after independent review/no-impact decision. Semantic changes invalidate
only consuming gates; uncertain classification uses the conservative fallback.
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

### C3 watcher closure clarification

The deterministic watcher helper, rather than an AI watcher turn, is the required observer. ROOT
uses `.codex/scripts/c3_outer_support.py` to launch `.codex/scripts/c3_watcher_helper.py` directly,
classify findings, resolve primary or
approved fallback evidence, write `topology/WATCHER_OBSERVATION_CLOSE.json`, classify outer support
failures, and continue safe cleanup past already-gone/identity-uncertain children. The helper must be
green in the host-only support smoke before C3 allocation. Optional AI-watcher evidence is
supplemental; its absence or early exit never invalidates an attempt.

### Pooled finding rule

Every review, selected test set, and observer/watch lane completes its assigned affected surface or
selection, records the complete finding set, and sends it to one triage gate. Triage deduplicates and
authorizes one bounded repair batch; ordinary findings do not stop peer checks, restart review, or
trigger repair/rerun during the gate. Observers record non-critical violations for post-gate pooling.

Immediate stop is reserved for exact evidence of an unauthorized/wrong-resource operation, loss of
containment or cleanup of a live process, or irreversible corruption of evidence required to judge
later work. ROOT owns the stop and preserves evidence. Safely contained defects and non-critical
evidence gaps are recorded and pooled.

### Outer C3 failure isolation

Treat errors in outer C3 setup, launch, monitoring, report handling, evidence validation, and
emergency cleanup as outer-attempt procedure failures, not candidate failures. Correct harmless
procedure/paperwork errors in place. If an error prevents honest immutable-attempt closure, close only
that attempt and use a fresh namespace, preserving every candidate/test result with immutable valid
evidence and an unchanged dependency fingerprint. Do not reopen candidate implementation, C0/C1/C2,
or green candidate tests solely due to an outer procedure failure.

Escalate to candidate repair/relock only if exact evidence shows a changed C1-locked candidate input,
incorrect candidate behavior, or an untrustworthy candidate result. ROOT records the classification
before rerunning work.

Before the one logical safeguard run, an environment-admission gate executes no safeguard source
check or test and may be repaired/repeated. Once `SAFEGUARD_RUN_ID` exists, an environment-only
interruption resumes that same ID and only incomplete/dependency-invalidated components. A locked-
input change requires a new C1 lock and new run ID.

After candidate-managed shutdown and helper observation closure, at a quiescent checkpoint O inventories every regular
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
`goal.md`, the spec, roadmap, plan, `HANDOFF.md`, `test-cleanup.md`, `task-card-spec.md`, and
`PARALLEL_CHECKPOINT.md` agree; stable runner/rollback/MCP identities are exact; the reserved
candidate is clean at `c6999d1`; joined S30 tip `6649cf2` and its evidence are exact; the external
support focused tests, practical smoke, Luna execution evidence, plan validation, and repository
verification are green; and no managed worker/process/claim is live.

On explicit resume, classify the governing diff by lock-input domain and preserve unaffected credit.
Independently archive/admit exact S30 tip `6649cf2` without rerunning its four green affected IDs when
their fingerprint is unchanged. Then complete S4's two candidate features and S5's four candidate
features through their bounded implementation/review/test topologies. Run the shortest affected
S4/S5 smoke, fresh C0, C1, and only dependency-invalidated C2 IDs. Only the exact resulting candidate
may enter the host-only C3 rehearsal. A green
rehearsal unlocks the next fresh physical attempt. Do not begin C3, a safeguard, MCP, or hardware work
before those prerequisites are green.

Before any expensive selected executor set with custom inner-process evidence, readiness requires a
same-lane recordability preflight with no real product, MCP, or hardware action. It must validate a
complete sample record for stable ID, exact inputs, worker/process creation identity, timing, command,
outputs, and exit outcome. Bind the green preflight to the exact runner/procedure/configuration/
environment fingerprint and reuse it until that fingerprint changes. A preflight or reconstructable report procedure defect is same-lane only;
if raw identity evidence cannot be reconstructed, rerun only the affected ID on the same lock. Batch
all classified fixture, mock, and executor-environment corrections from one selected run before
rerunning that selection once. Before a C3 attempt pair, O/helper, target repository, MCP process, or
hardware claim is allocated, run an exact-C1/C2 host-only rehearsal against disposable local fakes for
launch admission, retained-session authorization, identity binding, duplicate refusal, watcher
correlation, recovery/idempotence, cleanup, and terminal closure. A green rehearsal is mandatory C3
admission evidence, but never physical certification.
