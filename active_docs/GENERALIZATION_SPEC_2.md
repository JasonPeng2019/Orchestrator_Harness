# GENERALIZATION_SPEC_2: Physical Firmware Compatibility and Acceptance

Status: paused for next-run preparation; S1-S3 and S30 are implemented/tested, S4/S5 and final gates remain  
Date: 2026-08-06  
Primary product baseline: detached `stable-general-harness-runner` at `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`  
Firmware MCP source baseline: `Firmware/BYO-Firmware-MCP` at `f003f84a7df51cd8595a3203c62e225b21da2a22`
Launch-readiness contract: `active_docs/EXECUTION_READINESS_2.md`

The exact accepted-but-not-yet-admitted S30 joined tip is
`6649cf201ded9782c2cb3bc56983f4a560728ea8`. The stable runner and candidate remain frozen while the
governing topology and external C3 support layer are prepared. That external support layer is now
independently tested and ready. No C3, MCP, target-repository,
watcher-helper, or hardware process starts until explicit user resumption.

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
8. A ROOT-launched deterministic helper supplies required observation evidence, pools ordinary
   findings, and requests an immediate controlled stop only for the three exact safety/containment/
   evidence-corruption conditions; an optional AI watcher is supplemental and non-blocking.
9. The final target firmware behaves correctly, all exact managed processes are gone, all resource claims are released, and the one final accumulated safeguard is green.
10. One worker thread serves one logical task; accepted threads are terminal and unrelated later work starts from a new bounded task card.
11. Accepted terminal lanes leave active discovery after their evidence is preserved; clean worktrees close safely, transcripts become archive-only, and disposable caches do not accumulate.
12. Static read-only work uses an exact immutable source view and separate result root without creating a full linked worktree; a full worktree remains available when mutation or source-local execution requires it.
13. Concurrent controllers cannot interleave or lose shared event-log records because every append waits on the same cross-process lock.

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
7. Add the bounded S4 task-card/semantic-acceptance feature and one report-only result-repair retry
   exactly as specified by top-level `task-card-spec.md`. These are coding-lane control features, not
   a scheduler or semantic planning engine.
8. Add one bounded S5 efficiency/evidence-integrity stage immediately after S4: enforce logical
   task/thread termination, retire accepted lanes from active discovery, support no-worktree static
   read-only lanes, and serialize each shared event-log append with one cross-process lock.

## 6. Agent and topology contract

The model assignments below govern subagents launched headlessly with `codex exec`; they do not
govern the current outside root session. The collaboration picker is not an availability oracle.

- Launched orchestrator subagents, including `F.C3.O`: GPT-5.6 Sol, high reasoning, Fast (`service_tier="priority"`).
- Coders that edit harness, MCP, test-medium, or firmware application source: GPT-5.6 Terra, medium reasoning, Fast (`service_tier="priority"`).
- Reviewers and test writers: GPT-5.6 Terra, medium reasoning, Fast (`service_tier="priority"`).
- Doers and test executors: GPT-5.6 Luna, high reasoning, Fast (`service_tier="priority"`).
- Optional supplemental watcher-reviewer `F.C3.W`: GPT-5.6 Terra, medium reasoning, Fast
  (`service_tier="priority"`), launched only when its independent review is worth the cost. The
  deterministic non-agent helper is the required observer.

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
- `F.C3.O` serially coordinates target test writing, target coding, target execution, and target
  review through `C3-HARNESS` while the deterministic helper supplies required observation;
  optional `F.C3.W` liveness is not a gate.

Gates and evidence must use `ROOT-IM`, `F.C3.O`, `F.C3.W`, or `C3-HARNESS`; an unqualified
"orchestrator" or "manager" is not sufficient where ownership, launch authority, or a model
requirement could be confused.

At most three fan-out lanes are allowed for any role pool. The default is one. A pool of two or three is used only for genuinely independent review, test-writing, or test-execution slices. Production coding is singular and serial.

### 6.1 Efficient lane lifecycle

- A worker thread is bound to one task-card objective. Resume it only for exact `CONTINUE` gaps, the
  one report-only repair, the strict fast lane, or another correction within that same unaccepted
  logical task. `ACCEPTED` and `ACCEPT-WITHIN-TOLERANCE` make it terminal; unrelated work uses a new
  bounded card and thread.
- Each lane declaration names `linked-worktree` or `immutable-read-only-view`. Use a full linked
  worktree only for source mutation or source-local execution state. The read-only mode binds an
  exact source commit and gives the worker a separate writable result root.
- After semantic acceptance and evidence hashing, remove the lane from active discovery. Close a
  linked worktree only after proving it clean, its revision retained, and no live process uses it.
  Preserve required results/transcripts under an archive-only root and remove only disposable caches.
- Every controller appending to one shared event log acquires the same cross-process lock, waits its
  turn, writes and flushes one complete record, then releases the lock. A concurrent-process test must
  prove that no record is malformed, interleaved, or lost.

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
always `NOT_CERTIFIED`, no direct hardware bypass is allowed, and protected original harness tests
are ineligible for substitution.

`ROOT-IM` records the non-authorizing preflight draft at
`plans/general-coding-harness/evidence/firmware-v2/preflight/DELEGATED_HARDWARE_AUTHORIZATION.draft.json`.
At C1 `ROOT-IM` mechanically creates
`plans/general-coding-harness/evidence/firmware-v2/final/c1/{C1_LOCK_ID}/DELEGATED_HARDWARE_AUTHORIZATION.json` by copying
the user-issued scope and any explicit user expiry exactly, then adding only derived lock, identity,
pin, RF, and exclusion bindings. This is validation/attestation rather than issuance; `ROOT-IM` cannot alter or expand the
scope. Sibling `C1_LOCK.json` records its canonical path and SHA-256.

One candidate-owned controller holds one board claim and one MCP process/transport for a complete,
finite Server Run. Before launch, `C3-HARNESS` creates immutable
`hil/{lane-id}/sessions/{SESSION_ID}/SESSION_REQUEST.json` for a fresh opaque UUID, binding the exact
attempt/lane/board/resource, stable probe/target/profile/route, C1/delegated reference, pinned
server/schema/policy, five governing documents, target/seed/topology identities, user-allowed action
classes, and session deadline. The locked method policy--not caller data--defines allowed session
roles/transitions. The record authorizes lifecycle only, never a hardware action.

After exact claim acquisition and fixed MCP initialize/initialized plus the side-effect-free empty-
argument `initialization_handshake`, the controller records create-once `SESSION_OPEN.json` with the
request path/hash, exact controller/server process identities, Server Run ID, bootstrap transcript/
hash, and initial phase. It retains that exact process, transport, roots, claim, and Server Run for
the session. Every later `tools/call`, read-only or mutating, is a separately authorized call whose
request/proposal/decision/authorization/admission/result chain binds the session/open path/hash,
consecutive sequence number, exact prior result path/hash or first-call null, and policy transition.
Only the next exact transition is accepted. Server-returned plans, permissions, exposed actions, or
fallbacks must enter a new exact call proposal and signed O decision; a response never authorizes
its successor.

Normal close requires O's create-once signed
`session-close-decisions/{SESSION_ID}.json`, bound to the exact open record, last result/phase,
expected returning state, rationale, and time. Only `C3-HARNESS` closes stdin/server state, drains,
terminates if necessary, reaps, releases the claim, and writes `SESSION_CLOSED.json`, and only after
all policy-required returning-state calls have separately passed. Failure, expiry, revocation,
governing-input change, watcher abort, invalid sequence, or O loss uses bounded controller cleanup
and `SESSION_ABORTED.json`; it cannot invent a cleanup hardware call or claim a clean successful
return. A closed/aborted session is terminal and cannot be resumed or reused.

Each authorized call separately requires a fresh opaque UUID `CALL_ID` and this immutable order:
`C3-HARNESS` atomically creates `hil/{lane-id}/call-proposals/{CALL_ID}.json` with exact
C1/delegated path/hash, attempt/lane/logical-board, stable probe UID, reviewed target/profile,
rediscovered route or canonical null, session/open path/hash, consecutive sequence/predecessor/
transition, create-once board-identity/claim-acquisition paths/hashes, MCP
method/version, pinned server revision/schema hash, locked policy path/hash, exact arguments,
canonical policy-evaluation object/hash, live plan path/hash, required
`max_operation_duration_seconds`, and permission; after reading
it, `F.C3.O` independently atomically creates attempt-evidence
`authorization-decisions/{CALL_ID}.json` with proposal path/hash, matching fields, exact O
process/thread identity, approve/deny/rationale/time/expiry; only an approval lets `C3-HARNESS`
atomically create `hil/{lane-id}/authorizations/{CALL_ID}.json` binding both prior path/hashes. The
authorization also copies the same exact call/board/probe/target/route/identity/claim/method/server/
schema/policy/evaluation/argument/plan/duration fields. The
decision directory is O-owned and harness-read-only. Before launch ROOT creates nonce/keypair and
create-once launch intent, then spawns O with nonce but no private key over a bidirectional inherited
pipe. Post-spawn ROOT writes exact identity, sends its hash, receives O's nonce/hash acknowledgment,
writes create-once `topology/ORCHESTRATOR_KEY_RELEASE.json`, then sends the private key and discards
its copy. O may sign ready/work/decision only after reading key-release; every signature binds its
hash and has time >= release. Harness rejects earlier/unbound decisions. Failure forces fresh attempt
and no intent/identity/key-release file is rewritten. The private key never enters file/env/prompt/log/target/harness
state. O signs canonical decision JSON; harness verifies before dispatch and C4 verifies provenance.
All use create-new/no-overwrite; IDs are never reused. After validation, the harness samples its
monotonic clock and creates immutable `hil/{lane-id}/dispatch-admissions/{CALL_ID}.json`, binding the
authorization path/hash, fresh five governing hashes, all revalidated fields, clock identity, start,
and deadline = start + declared duration. Dispatch/result reference all four paths/hashes;
authorization is never rewritten and creation-to-submission time counts.
Immediately before submitting the MCP call, `C3-HARNESS` validates every field and refuses dispatch
or a success record for missing, expired, mismatched, or out-of-scope evidence. A post-dispatch
record cannot authorize a call; only the user can expand scope. Actual dispatch method/version,
server revision/schema, policy path/hash, normalized parameters, recomputed evaluation hash, plan/
duration, probe/target/route, and live identity/claim paths/hashes must exactly equal proposal, O
decision, and authorization. Result validation rediscovers identity/route and revalidates claim;
mismatch forbids success/forces cleanup. Dispatch/result retain all fields for C4.

At every actual mutating dispatch boundary, the harness independently rehashes all five governing
documents and requires the live set to be covered by the operative C1 plus valid append-only change
dispositions. It binds the live hash set in dispatch admission and dispatch/result. An unclassified
mismatch expires pending calls, refuses dispatch, emits `GOVERNING_INPUT_CHANGED`, and invokes the
live-goal protocol. ROOT classifies the smallest changed lock-input domain and refreshes C1 when
current hashes must be rebound, preserving all non-consuming green gates. A ROOT-owned read-only file watcher
observes them while mutation is in flight; a mid-call mismatch is revocation and uses the
`INDETERMINATE_EXPIRED` path.
It is a registered non-agent helper evidenced at `topology/GOVERNING_INPUT_WATCHER.json` with exact
process identity/current hashes/heartbeat, no authority beyond its own evidence, and mandatory
exit/reap in the topology shutdown inventory.

The delegated `expires_at_utc` is copied exactly when explicitly user-supplied and otherwise is
`null`; it always expires on user revocation/scope change, C1 invalidation/replacement, or completion.
All call records expire when their attempt exits/aborts. A one-shot call authorization otherwise
expires at the earlier of the delegated time (if any) and five UTC minutes after creation, and on any
bound-field change. At dispatch the remaining window must cover the live plan maximum plus a fixed
60-second result/cleanup margin, and validity must persist through result commitment. Mid-call
expiry/revocation requests safe MCP cancellation where supported, retains raw outcome as
`INDETERMINATE_EXPIRED`, performs bounded cleanup, forbids success, and releases claims only after
exact exit/reap. Retry uses a new call ID. Only an
explicit later user directive can set/extend delegated time, requiring a fresh C1.
The harness enforces the admission's monotonic deadline: at maximum it requests safe cancellation
and, if still running, exact bounded MCP/controller termination/cleanup. Result records start/
deadline/end/elapsed and cancellation/termination; end after deadline is
`INDETERMINATE_TIMEOUT`, never success, with claims retained through exact exit/reap/cleanup.

C1 serialization is non-circular: `ROOT-IM` first allocates a fresh opaque UUID `C1_LOCK_ID` that is
not content-derived, creates the authorization artifact in that ID's canonical directory, hashes it,
then writes sibling `C1_LOCK.json` containing the ID, canonical authorization path/hash, and all
other locked-input hashes. Its hash is computed last into sibling `C1_LOCK.sha256` and is never an
authorization input. A replacement C1 uses a fresh UUID/directory and repeats this order; consumers
may use only the operative C1 paths/hashes.

## 9. Acceptance medium

The final test project is the **Four-Board Dual-Family Firmware Lab**. It is created fresh in a disposable repository by agents launched through the candidate harness. It has two physically independent subsystems because the fixture contains no authorized STM-to-nRF data wiring.

S2 produces `TARGET_SEED_MANIFEST.json`, which enumerates and hashes exactly
`TARGET_CHARTER.md`, `PINNED_INPUTS.json`, `TEST_CONTRACT.json`, and `EVIDENCE_SCHEMA.json`; C1
records the manifest's own hash. Those five read-only files are the entire initial C3 repository and
are C1-locked. Target application source, tests, build files, and target-repository-local
configuration created afterward are target-local and versioned in the target dependency fingerprint.
Target workers may not edit seed files; a required seed change invalidates C1.

### 9.1 STM32 subsystem

Build a dual-image controller/responder application:

- STM-A is a deterministic command generator and status CLI.
- STM-B is an I2C2 responder with deterministic request, response, checksum, sequence, timeout, and error counters.
- Both expose machine-readable UART evidence.
- The acceptance run proves normal exchange, bounded error recovery, reset/reconnect, debugger observability, and sustained ordered traffic.

### 9.2 nRF52 subsystem

Build one small codebase with two bounded acceptance modes:

- BLE mode: one DK is the peripheral and the other is the central; a deterministic GATT command/acknowledgement exchange proves the BLE path.
- LoRa mode: the two DK/CoreSX1262 assemblies perform deterministic ping/pong with sequence, checksum, retry, RSSI/SNR, and timeout evidence.
- Mode and board role are build-time or configuration-time selections, not a general dynamic radio framework.

### 9.3 Concurrent campaign

Run the STM32 I2C subsystem and nRF52 LoRa subsystem concurrently. Prove that:

- exactly one target doer agent remains active while its single `C3-HARNESS` assignment requests two concurrent non-agent physical lane process groups, `P3.STM` for STM-A/STM-B and `P3.NRF` for NRF-A/NRF-B;
- during normal operation only `C3-HARNESS` creates, starts, stops, and reaps those groups and owns both lane records, controller/process identities, claims, events, and cleanup, while each lane has distinct MCP processes, `.firm`, artifact, and log roots; `F.C3.P1` may request and operate them only through its assigned harness interfaces and may not spawn them; ROOT's emergency host-process exception below applies only when the controller cannot shut down;
- two independent hardware lanes can make progress without cross-contaminating probes, serial ports, MCP roots, artifacts, relays, or claims;
- same-resource contention queues rather than double-owns;
- one predeclared intentional, source-controlled, non-destructive target-code defect produces its recorded expected behavioral failure through the normal target test path, is classified as target work, and is repaired and selectively retested; it may not alter the harness, MCP server, fixture, authorization, or hardware configuration;
- a checkpointed lane resumes with the same thread/path identity;
- all application-level protocols complete and all exact managed process identities terminate.

### 9.4 MCP use

Each hardware lane's candidate controller owns its MCP process, project-local `.firm` state, artifact root, logs, board assignments, launch capability, and stdio endpoint. Firmware builds may use the server's native-build/artifact tools or the pinned compiler directly, but every physical interaction is brokered by that controller through the MCP server. O/target workers submit structured requests and receive results; they cannot launch/address the physical server. The controller rejects forwarding without valid proposal, signed decision, authorization, and dispatch admission. Direct `pyocd`, direct serial control, direct physical-MCP access, or ad hoc probe scripts are not acceptance evidence; C4 audits environments/handles and ledgers for bypass.

## 10. Gating test set

The core release gate adapts the supplied experiment catalog rather than executing all of it:

- host and protocol: the applicable H00, H01, H02, and H05 contracts;
- setup and routing: S10 through S13 for all four boards;
- applications: the dual-STM intent of A21, the dual-nRF BLE intent of A23, and the dual-nRF CoreSX1262 intent of A24;
- operations: representative D30 through D36 cases covering inspect, control, flash, UART, concurrency, plans, permissions, and cleanup;
- one bounded, predeclared target failure and repair case;
- one concurrent four-board run.

The exhaustive A20-A26 application matrix, the entire B01-B39/Q40 seeded-bug corpus, eight-hour Q41 soaks, and destructive or try-last appendices are extended qualification, not release gates for this harness retrofit. They may be run later without changing this completion decision.

## 11. Required observation and support-failure contract

This section is the operative contract. It supersedes the archived watcher text below and every
other sentence in this specification that makes an AI watcher terminal report/exit mandatory,
promotes an ordinary observation directly to abort, or invalidates product credit solely because
outer test-support code failed.

ROOT directly launches the deterministic non-agent helper from the reusable external support
layer, records its exact PID/creation identity and launch hash, and waits for helper-authored ready
evidence before target work. The helper continues through candidate-managed shutdown and writes its
heartbeat/cursor, pooled findings, and terminal-service records. ROOT stops/reaps it and writes
create-once `topology/WATCHER_OBSERVATION_CLOSE.json` before manifest closure. Optional `F.C3.W`
review evidence is retained when available but never gates the attempt.

Each required observer fact has a primary source and predeclared independent backups in the C3
evidence-fallback matrix. ROOT validates hashes, attempt/process identities, correlation fields, and
time bounds. A missing helper record is acceptable only when those backups completely prove the same
fact. Otherwise only the affected attempt/work is `INCOMPLETE`; no candidate gate is reopened merely
because support evidence was unavailable.

All non-critical observer/reviewer/test findings are collected through the end of the assigned
surface, deduplicated once, and repaired in one bounded batch. Immediate live stop is limited to
exact evidence of: an unauthorized or wrong-resource operation; loss of containment/cleanup of a
live process; or irreversible corruption of evidence needed to judge later work. The stop protects
the live system but does not itself prove a product defect.

An outer allocation, launch, monitoring, helper, report, schema, validation, supervision, or cleanup
failure is `OUTER_ATTEMPT_PROCEDURE_FAILURE`. Correct it in place when the outcome remains
determinable. Otherwise roll only the incomplete support/physical attempt and preserve every valid
immutable product/test result. Product repair/relock is allowed only on exact evidence of a changed
product dependency, incorrect candidate behavior, or an untrustworthy candidate result. Cleanup
must record an already-gone or identity-unverified child without signalling it and continue through
the remaining registered identities.

### Orchestrator liveness and finding attribution

ROOT also monitors O's exact process and `topology/ORCHESTRATOR_HEARTBEATS.jsonl` through result
commitment and normal exit. Manifest creation starts a bounded result deadline. Unexpected O exit,
stale/lost liveness, deadline without a valid result, or normal exit without a valid result is
`ORCHESTRATOR_LOST`: stop new work, clean only registered topology, preserve the partial attempt, and
classify it under the support-failure contract above. Partial manifest/result files are never
completed or reused. Normal and abnormal exit records bind all available exact identity and result
evidence without claiming events that were not observed.

An orchestrator/operator mistake is target-project work unless exact evidence shows that the
candidate incorrectly accepted, rejected, contained, reported, resumed, or cleaned it. The
deterministic helper records such evidence and pools the finding; only one of the three explicit
live-safety conditions requests immediate containment. Repair and retest follow the smallest
dependency-invalidated route.

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
- Before an expensive selected test set that requires custom inner-process evidence, the executor
  runs one local recordability preflight with no real product, MCP, or hardware work. It proves one
  complete record can be written and validated for stable ID, exact inputs, worker/process creation
  identity, timing, command, output paths, and exit outcome. A preflight or reconstructable report
  defect stays in the same lane and does not invalidate product credit; if raw identity evidence is
  irrecoverable, rerun only that stable ID on the same lock.
- If a selected run yields only fixture/mock/executor-environment defects, ROOT batches the complete
  classified test-only set and reruns the selection once after the batch. It does not rerun the broad
  selection after each individual fixture correction. A candidate finding remains material.
- Before any C3 attempt directory, watcher, target repository, MCP process, or hardware claim is
  allocated, run a host-only rehearsal against the exact green C1/C2 candidate with disposable local
  fakes. It proves launch admission, retained-session authorization, process/identity binding,
  duplicate-assignment refusal, watcher correlation, recovery/idempotence, cleanup, and terminal
  closure. Only a green rehearsal unlocks the first physical attempt; failures are classified before
  an attempt exists and follow the material or same-lane route accordingly.

C1 locks the operative goal/spec/roadmap/plan/readiness hashes, candidate revision, server
pin/configuration, acceptance-kit and lane/MCP launch templates, fixture bindings, five-file target
seed, test/evidence contracts, authorization, and other implementation inputs used by C2/C3. Target
application source and target-repository-local configuration created later by `C3-HARNESS` are
excluded and versioned in the target dependency fingerprint. Any repair after C1 that changes a
locked domain expires the old C1 admission and requires a current C1 plus only the gates that consume
that domain before C3. Production, policy, behavioral-contract, coverage-obligation, or other operative changes
return to the owning step and full fresh C0. Only a qualifying strict test-only fast lane correction
may avoid fresh C0 before the new C1, after recording its checklist and exact failed-ID rerun. Every
post-C1 governing hash change pauses new admission until ROOT writes the append-only change
classification. Hardware-authority or in-flight-mutation changes revoke affected calls immediately.
Byte-only changes may use `EDITORIAL_SUPERSESSION.jsonl` after an independent review/no-impact
decision. Semantic changes name changed domains and invalidate only their consuming gates; ROOT may
then issue a current C1 that reuses all preserved evidence. Uncertain classification uses the
documented conservative fallback.
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

C4 and safeguard do not create a second lock. A governing change uses the append-only domain
classification and invalidates only gates that consume the changed lock-input domain; an
unclassifiable change uses the documented conservative fallback. Candidate revision changes and
other product-material input changes still follow their applicable repair/re-lock route.

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
2. Clean exact source-allocation and runtime provenance: linked worktree where required, otherwise
   immutable read-only source identity plus separate result root.
3. Green compatibility, lifecycle, relay, MCP, resource, cleanup, dual-route, and protected original general-harness unit tests, with no unjustified deletion, skip, expected failure, or weakened assertion.
4. Fresh final reviewer decision on the frozen joined candidate, after a complete sweep rather than
   first-finding return, with no unresolved production-relevant in-scope gap.
5. Fresh `F.C3.O` identity/key-release, ROOT-owned deterministic-helper launch/observation-close,
   and `C3-HARNESS` launch records proving every target agent was candidate-launched with the
   required model/tier and was not launched directly by `F.C3.O`; optional W evidence is supplemental.
6. Green STM32 I2C, nRF52 BLE, nRF52 LoRa, and concurrent four-board behavioral evidence.
7. Correct handling of controlled target failure, selective repair, checkpoint/resume, contention, exact acknowledgement, and shutdown.
8. Zero unresolved actionable events, zero live exact managed child identities, zero owned resource claims, and no unclosed serial/MCP session.
9. After candidate-managed shutdown, ROOT stops/reaps the deterministic helper and writes
   `WATCHER_OBSERVATION_CLOSE.json`; then O atomically creates manifest and result. The manifest
   inventories/hashes every regular file under both attempt roots, including the attempt registry and
   adverse evidence, except itself, result, and reserved topology; locked external inputs are
   canonical path/hash references verified directly by C4. Symlink/reparse/temp/later writes are
   forbidden; C4 independently enumerates. Result follows within 90 seconds. After O exit ROOT writes
   `ORCHESTRATOR_EXIT.json` and separately closes topology.
10. `topology/TOPOLOGY_SHUTDOWN.json` inventories/hashes every other regular topology file but excludes itself; symlink/reparse/temp entries are forbidden, and C4 independently enumerates that domain and separately hashes/verifies shutdown.
11. A final nested static audit proving requirement, topology, evidence, and original general-harness unit-regression coverage, including a baseline-to-candidate test-manifest comparison.
12. One terminal green logical `SAFEGUARD_RUN_ID` covers the complete accumulated safeguard after the practical gate, with no incomplete component.
13. A completion summary and out-of-scope ledger explicitly distinguish harness certification from extended MCP/firmware qualification.
14. A candidate-root safeguard result that cannot be confused with the outer verifier's fixed
    `stable-general-harness-runner` target, followed by outer verification only after the green candidate is
    staged on a distinct promotion branch.
15. Green S5 unit and disposable smoke evidence for terminal task/thread enforcement, accepted-lane
    retirement, immutable no-worktree review mode, and locked concurrent event appends.

Any required product test failure, ambiguous product identity, missing authorization, unresolved
`P.05` mapping needed by a test, or evidence gap that prevents determining a required product result
prevents promotion. A support artifact failure alone does not, when approved independent evidence
fully proves the same result.

### C3 watcher clarification

For C3, required observation is provided by the ROOT-launched deterministic helper. ROOT uses the
reusable external support layer for exact launch, finding classification, evidence fallback,
observation closure, procedure-failure isolation, and safe cleanup. Optional AI review is
supplemental and non-gating. `WATCHER_OBSERVATION_CLOSE.json` binds every required fact to its primary
or two-class independent backup evidence; an unresolved fact makes only the affected attempt
incomplete.

### Pooled finding rule

Every review, selected test set, and observer/watch lane completes its assigned affected surface or
selection, records its complete finding set, and hands it to one triage gate. Triage deduplicates
the set and authorizes one bounded repair batch; no ordinary finding stops peer checks, restarts a
review, or triggers repair/rerun during that gate. Observers record non-critical violations for
post-gate pooling.

Immediate stop is limited to exact evidence that continuing risks an unauthorized or wrong-resource
operation, loss of containment/cleanup of a live process, or irreversible corruption of evidence
needed to judge later work. ROOT owns the stop and preserves evidence. A safely contained behavior
defect, failed assertion, incomplete non-critical evidence, or target/test defect is recorded and
pooled instead.

### Outer C3 failure isolation

An error in outer C3 setup, launch, monitoring, report handling, evidence validation, or emergency
cleanup is an outer-attempt procedure failure, not a candidate failure. Correct a harmless procedure
or paperwork error in place and continue. If it prevents honest closure of the immutable attempt,
close that attempt and use a fresh namespace while preserving every candidate/test result whose
immutable evidence and dependency fingerprint remain valid. Do not reopen candidate implementation,
C0/C1/C2, or a green candidate test solely because an outer procedure failed.

Candidate repair/relock is allowed only on exact evidence that the outer failure changed a C1-locked
candidate input, caused incorrect candidate behavior, or made the candidate result untrustworthy.
ROOT records that classification before rerunning work.

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

Implementation is complete only after C1-C77 and the roadmap/execution plan have been followed end to end,
the separate acceptance orchestrator has completed the practical project under the isolated
deterministic observer, every accepted production-relevant failure has been minimally repaired and selectively
retested, the final full safeguard is green once, promotion evidence is written, and the new runtime
is left inactive and clean for general use. Cosmetic, unreachable, behavior-neutral, and speculative
non-findings may remain deferred.
