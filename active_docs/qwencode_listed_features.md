# Qwen Code feature inventory — tested against the WIP target harness

> **Active compatibility follow-through.** This inventory and its related Qwen work remain active
> until their source changes are merged into `firmware-v2-harness-runner`. They do not reopen the
> closed Firmware hardware campaign. The delivered WIP surface and its limits are stated in
> [`final_v2-firmware_harness_overview.md`](../firmware-v2-harness-runner/final_v2-firmware_harness_overview.md).

Scope: `orchestrator_harness` at commit `055a5bd` (branch `firmware/v2-candidate`),
copied to `harness-single-worktrees/qwencode-test` (branch `qwencode-test-copy`).
The exact commit being actively developed was **never edited** — all execution
happened in the copy and sibling disposable lane worktrees. The qwen adapter is
loaded from the Firmware bootstrap (`Firmware/scripts/orchestration/qwen_provider_bootstrap.py`)
by file path and registered in-process, exactly as production does.

This file lists **every** functionality feature of the WIP harness, mirroring the
structure of `claude_listed_features.md`. The feature taxonomy follows
`QWENCODE_FEATURE_INVENTORY.md` (F1.x–F10.x), which is the source of truth for
the multi-agent test suite. Every row is tagged with its test status.

Status tags (same convention as `claude_listed_features.md`):
- **TESTED-PASSED** — actually executed and observed to work in the qwen multi-agent scenario.
- **TESTED-FAILED** — actually executed and observed to fail (a real qwen-vs-codex gap).
- **GAP — REAL** — a genuine qwen-vs-codex behavioral defect: the qwen adapter does *less than or differently from* codex on the **same code path** codex exercises. There is exactly **one** such row in this inventory (F1.2.7 — the silent-drop of override fields), confirmed by a passing test that asserts the current (defective) behavior. **A second real gap** (the terminal `CANCELLED` outcome collapsed to `FAILED`) is tracked as a cross-check finding rather than a distinct numbered row — see "Second real gap" below — so the row count of GAP — REAL is 1 while the total count of real gaps is **2**.
- **DESIGN-REC** — a *design recommendation*, **not** a qwen gap. The mechanism is either provider-neutral shared code or a codex-only host-adapter subsystem that is **unbuilt/unbound identically for claude and qwen** in this worktree (both get `FutureHostFixture`; there is no `claude()`/`qwen()` `AdapterCapabilities` factory, only `codex()` and `future_fixture()`). Recommending a qwen host adapter be built (via qwen's `Stop`/`Notification`/`idle_prompt` hooks) is not the same as finding a qwen-vs-codex compatibility gap — codex is the *only* provider that has this subsystem, so its absence is not a qwen regression. Mirrors `missing_claude_implementation.md` §C.
- **COVERED-GENERIC** — the mechanism is provider-neutral; it is verified by a named non-qwen suite that is confirmed green (cited inline, with the run date). A qwen-shaped invocation of the same code path would add no information. This counts as tested evidence, not a deferral.
- **N/A-QWEN — CX** — codex/claude-only mechanism (its own host adapter internals); there is no qwen equivalent to exercise, and the qwen analog (or the documented absence) is tested elsewhere. Not a qwen gap.
- **NOT-TESTED** — not executed; reason in parentheses:
  - **OOS** — explicit firmware/MCP/legacy-watcher exclusion per instruction. The only remaining genuinely-untested category.

**2026-08-21 gap correction.** An earlier pass over-listed gaps: it tagged 9 rows
"GAP — CONFIRMED BY TEST," but 8 of those (F5.2.1–6, F5.3.1–2 — the push-wake /
delivery / host-adapter subsystem) are **not qwen-vs-codex gaps at all**. They are
codex-only subsystem rows that are **identically absent for claude** in this
worktree (both providers get `FutureHostFixture`), so they are **DESIGN-REC**, not
gaps — exactly the reclassification `missing_claude_implementation.md` §C applied
to the claude side. The 9th (F1.1.6) asserts a *registration guard working
correctly* and is a plain **TESTED-PASSED**. After correction there are **two real
qwen gaps**: **(1) F1.2.7** (override fields silently dropped instead of
reject-loud — the qwen-side of claude's blocker #3, still unfixed for qwen — the
one GAP — REAL *row*); and **(2)** the terminal **`CANCELLED` outcome collapsed to
`FAILED`** (codex records a distinct `CANCELLED` on the same cancel path; qwen does
not), a low-severity but closeable divergence tracked as a cross-check finding, not
a numbered row. Both are documented in full below.

## Summary counts

| Metric | Count |
|---|---:|
| Total features inventoried | **112** |
| Rows tagged TESTED-PASSED | 52 |
| Rows tagged **GAP — REAL** (numbered-row defect: F1.2.7) | **1** |
| Rows tagged DESIGN-REC (codex-only subsystem, identically absent for claude — not a qwen gap) | 8 |
| Rows tagged TESTED-FAILED | 0 |
| Rows tagged COVERED-GENERIC (named green suite) | 43 |
| Rows tagged N/A-QWEN (codex-only, analog tested) | 4 |
| Rows tagged NOT-TESTED — OOS (firmware/MCP, excluded by instruction) | 4 |
| — every other NOT-TESTED category | 0 |

> **Real gaps total = 2**, not 1. The GAP — REAL *row* count is 1 (F1.2.7). The
> second real gap — the terminal `CANCELLED` outcome collapsed to `FAILED` — is a
> defect in the terminal-outcome mechanism (row F2.1.6 passes its own narrower
> assertion), tracked as a cross-check finding under "Second real gap" rather than
> as a distinct numbered row, so it does not change the 112-row tally.

> **The 8 DESIGN-REC rows** (F5.2.1–6, F5.3.1–2) are the push-wake / delivery /
> host-adapter subsystem. They were previously mislabeled "GAP." They are **one
> recommendation** — "build a qwen host adapter" — not 8 gaps, and codex is the
> only provider that has this subsystem (claude gets the same `FutureHostFixture`
> stub here). See `missing_claude_implementation.md` §C for the identical claude
> reclassification.

**2026-08-20 full completion pass.** The full inventory was driven to a
disposition with test evidence for every non-OOS row (the four F9.x firmware/MCP
rows are the only untested rows, excluded by instruction):

- **24 qwen-specific tests** in `test_qwen_multi_agent.py` (15 original + 4 TB-W
  + 4 completion-pass + 1 failure-branch), all green (`Ran 24 tests … OK`). The
  failure-branch test (`test_qwen_parse_and_terminal_map_failure_branch`) pins the
  qwen-specific FAILED mapping in `parse_transcript_line`/`terminal_outcome` that
  the success-only integration tests left uncovered. The completion-pass
  tests add F1.6.3 (wake-text mutation fail-closed), F1.1.6 (registration guard
  rejects a false `notification=True` — TESTED-PASSED, the guard works) + F5.2.x/
  F5.3.x (the unbuilt push-wake/host-adapter subsystem — DESIGN-REC, not a qwen
  gap; codex-only, identically absent for claude), and I5/I8/F3.3 (overlay
  collision atomic rejection in a qwen worktree).
- **178-test provider-neutral battery** green (`test_provider_adapter_registry`,
  `test_provider_adapter_public_seams`, `test_resource_locks`, `test_finding_gate`,
  `test_s5_capability_broker`, `test_events_cli`, `test_reconcile`, `test_discovery`,
  `test_processes`, exit 0) plus a lifecycle/CLI battery
  (`test_s4_contract`, `test_s4_repair`, `test_coding_lane_controller`,
  `test_git_results`, `test_handoff_preflight`) — these back the COVERED-GENERIC
  rows, each cited inline.
- Binding GAP-vs-PASSED rule held throughout: a completed-but-divergent test is
  recorded as GAP (confirmed by test), never laundered into TESTED-PASSED.

Run the qwen suite with
`python -m unittest orchestrator_harness.tests.test_qwen_multi_agent`
(24 tests, ~120s). A single real test action often confirms several rows at once.

### Disposition of rows not listed here (vs. `claude_listed_features.md`)

`claude_listed_features.md` inventories 346 rows at flag/rule/state granularity
(A–V sections); this doc lists 112 rows at feature granularity (F1.x–F10.x).
The rows from the claude doc **not** listed here are omitted deliberately, not
lost: they carry the claude doc's own provider-neutral tags — **PA** (already
validated end-to-end in the Codex/DeepSeek session), **CX** (codex-only
mechanism), **OOS** (firmware/MCP/legacy-watcher exclusion), and **TB-NS**
(trivially covered by Codex evidence). None of those tags differ for qwen: the
code path is identical regardless of provider, so a qwen-shaped invocation
would test the harness, not qwen support. This doc lists only rows with a
qwen-specific status (TESTED-PASSED, GAP) or a never-tested-anywhere status
(TB / TB-W) — i.e., the rows that carry mirroring information. For the goal of
"codex behavior mirrored into qwen," the omitted rows are mirrored by
construction; the TB-W section below is the actionable remainder.

### TB disposition (why the TB rows were not tested)

The TB rows were not tested because the qwen pass prioritized the multi-agent
coordination scenario (F10.x) and the Claude-gap cross-check; the rest were
marked TB without attempting them. Re-examined against `claude_listed_features.md`
(which flags its own TB-NS-V rows — provider-neutral but never exercised in
either session), the TB rows break down as:

- **18 worth testing (TB-W)** — see the "Worth testing" section below. These are
  the rows a qwen pass should still add: qwen-relevant behavior (F6.4, F2.1.2,
  F1.6.3), provider-neutral safety checks never exercised in either session
  (F3.4, F4.3, F5.1.4, I5, I8), and the two heavier subsystems (F2.3.1–F2.3.4
  lane lifecycle, F8.1–F8.6 capability broker).
- **6 trivially knowable from code** — F1.1.3, F1.1.4, F1.1.5, F1.1.7, F1.2.2,
  F1.2.7. All visible by reading the ~150-line qwen bootstrap: the adapter
  implements all 5 contract methods, `redact_argv` is explicit, `provider_id`
  matches the registration key, capabilities validation passed at registration
  (every launch test registered successfully), `encode_prompt` is a pass-through,
  and `configuration=True` is a no-op already covered by the C17/U4 gap tests.
- **21 generic provider-neutral code** — F1.1.2, F1.1.8, F1.4.3, F2.1.4, F2.1.7,
  F3.3, F4.2, F5.1.5, F5.1.6, F6.1, F6.2, F6.3, F6.5, F6.7, F6.8, plus the
  remaining overlay/queue/CLI rows. Same code path regardless of provider; a
  qwen-shaped invocation would test the harness, not qwen support. Caveat:
  these were not tested on codex either (that is why they are TB, not PA) — if
  they are untested at all, that is a harness test-coverage gap, and the right
  fix is a provider-agnostic test, not a qwen-specific one.
- **Operational note (F2.1.2)** — the unregistered-provider path has a
  qwen-specific angle: the registry is process-local, so a detached controller
  subprocess that skips the Firmware bootstrap gets
  `PROVIDER_OPERATION_UNSUPPORTED` for qwen (unlike built-in codex). The code
  path is generic, so it does not need a test, but it is a real operational risk
  worth remembering when launching qwen lanes from a detached controller.

### Worth testing (TB-W) — features a qwen pass should still add

Cross-referenced against `claude_listed_features.md` (346 rows, sections A–V).
These are the features that are **worth testing and nontrivial** — not trivially
knowable from code, not already covered by the 15 tests, and not provider-neutral
code that a qwen-shaped invocation would add no information about. Tier 1+2 are
focused unit tests in the existing file; Tier 3 is heavier subsystem work.

**Tier 1 — qwen-relevant, cheap, clearly worth it**

| # | Feature | Why worth testing |
|---|---|---|
| F6.4 | `watch --until-actionable` against a genuinely completed qwen lane | Operational proof of the polling workaround for qwen's `SAFE_BOUNDARY_ONLY` notification mode: the manager's polling path actually observing a finished qwen lane end-to-end. Only the registration-level `SAFE_BOUNDARY_ONLY` is asserted today, never the live polling behavior. |
| F2.1.2 | Unregistered provider → `PROVIDER_OPERATION_UNSUPPORTED` | Directly qwen-relevant: qwen is a foreign adapter in a process-local registry, so a detached controller that skips the Firmware bootstrap fails closed. Proves the fail-closed path for the exact operational risk noted above. |
| F1.6.3 | Post-registration wake-text mutation fails closed to `SAFE_BOUNDARY_ONLY` | qwen is a SAFE_BOUNDARY_ONLY provider; this proves the guard that keeps a mutated qwen adapter from silently becoming a WAKE provider. |

**Tier 2 — provider-neutral, never exercised in either session (claude TB-NS-V)**

| # | Feature | Why worth testing |
|---|---|---|
| F3.4 | `restore_worktree` exact-byte reversal on retirement | Claude tested it PASSED; qwen pass only tested ingest + prepare + receipt. The reversal path is untested. |
| I5 | Overlay collision detection (`OverlayCollisionError`) — append-only copy plan rejection | Safety check, never induced. |
| I8 | Receipt rollback on partial-apply failure | Receipt *rejection before launch* is tested; *rollback mid-apply* is not. |
| F4.3 | `active_declaration_conflicts` — duplicate branch/worktree detection | Safety check, never exercised. |
| F5.1.4 | `rebuild_state` crash recovery from the durable queue | admit/next/ack tested; crash-rebuild path is not. |

**Tier 3 — heavier subsystems (claude TB-NS-V)**

| # | Feature | Why worth testing |
|---|---|---|
| F2.3.1–F2.3.4 | Lane lifecycle: immutable source view allocation + read-only enforcement + archive-first retirement with hash-bound evidence | Safety-critical, completely unexercised. |
| F8.1–F8.6 | Capability broker full cycle: request → snapshot → approval → permit → result → cleanup, plus fail-closed paths (`CapabilityDenied`, `CapabilityAdapterUnavailable`) | Complex subsystem, never exercised. (Core request→permit cycle only; the firmware adapters stay OOS.) |

---

## 1. Provider Adapter System (`provider.py`)

### 1.1 Registry (`register_provider_adapter`, `unregister_provider_adapter`, `provider_registry`, `provider_adapter`)

| # | Feature | Status |
|---|---|---|
| F1.1.1 | Register a foreign external CLI adapter without generic-core edits | TESTED-PASSED (the qwen adapter is registered in-process via `register_provider_adapter` in `_register_qwen`) |
| F1.1.2 | Built-ins (`codex`, `claude-code`) cannot be unregistered; foreign can | COVERED-GENERIC (`test_provider_adapter_registry.py`, green in the 178-test provider-neutral battery 2026-08-20; the qwen side is exercised directly — `unregister_provider_adapter("qwen-code")` succeeds in `test_qwen_unregistered_provider_fails_closed_before_launch`) |
| F1.1.3 | Registration validates the adapter contract: `build_argv`, `encode_prompt`, `parse_transcript_line`, `terminal_outcome`, `redact_argv` all callable | COVERED-GENERIC (`test_provider_adapter_registry.py` contract-validation cases, green in the 178-battery; the qwen adapter passes this exact validation on every `_register_qwen()` in the suite) |
| F1.1.4 | `redact_argv` must be explicitly implemented (inherited base fallback rejected) | COVERED-GENERIC (`test_provider_adapter_registry.py`, green in the 178-battery; qwen's `redact_argv` is explicit — exercised in `test_qwen_provider_evidence_and_redaction`) |
| F1.1.5 | `provider_id` declared on adapter must match registration key | COVERED-GENERIC (`test_provider_adapter_registry.py`, green in the 178-battery; qwen registers under matching key `qwen-code` in every suite run) |
| F1.1.6 | `notification=True` requires exact `NOTIFICATION_WAKE_TEXT` and a real `deliver_notification` safe-boundary binding (base default rejected) | TESTED-PASSED (`test_qwen_notification_true_without_real_binding_is_rejected`: a qwen-shaped adapter declaring `notification=True` with the base no-op `deliver_notification` is rejected at registration with `ProviderAdapterError`. This asserts the **registration guard working correctly** — the same guard that protects codex/claude — so it is a pass, not a gap. qwen correctly registers `notification=False`; that it has no push-wake host adapter built is a DESIGN-REC, tracked at F5.3, identical to claude's state in this worktree.) |
| F1.1.7 | `ProviderCapabilities` validates all 8 booleans; `supports()`/`as_record()` | COVERED-GENERIC (`test_provider_adapter_registry.py` / `test_provider_adapter_public_seams.py`, green in the 178-battery; qwen constructs a full 8-boolean `ProviderCapabilities` in `_register_qwen`) |
| F1.1.8 | `classify_operation` returns actionable classified results for supported, unsupported, and unregistered operations | TESTED-PASSED (`test_qwen_no_push_wake_delivery_path_exists` calls `classify_operation("qwen-code","notification")` and asserts `supported=False`; supported/unregistered branches covered generically by `test_provider_adapter_public_seams.py`, green in the 178-battery) |

### 1.2 Capability dimensions (8)

| # | Feature | Status |
|---|---|---|
| F1.2.1 | `launch` — adapter can build a launch argv | TESTED-PASSED (qwen `build_argv` exercised in `test_qwen_build_argv_uses_stream_json` and the parallel-launch tests) |
| F1.2.2 | `prompt` — adapter can encode a prompt | COVERED-GENERIC (qwen `encode_prompt` is a pass-through exercised on every lane launch in the parallel-launch tests; generic contract in `test_provider_adapter_registry.py`, green in the 178-battery) |
| F1.2.3 | `event_result` — adapter can parse transcript lines into events | TESTED-PASSED (qwen `parse_transcript_line` handles `system/init` → STARTED and `result/subtype:success` → COMPLETED in the parallel-launch tests) |
| F1.2.4 | `session` — adapter tracks session identity | TESTED-PASSED (qwen `session_id` recorded in the parallel-launch tests) |
| F1.2.5 | `resume` — adapter supports `--resume <session_id>` | TESTED-PASSED (qwen declares `resume=True`; `decide_resume_or_handoff` returns RESUME on match in `test_qwen_resume_handoff_on_identity_mismatch`) |
| F1.2.6 | `permission` — adapter maps permission mode | TESTED-PASSED (qwen hardcodes `--approval-mode=yolo` unconditionally in `test_qwen_build_argv_hardcodes_approval_mode_yolo`) |
| F1.2.7 | `configuration` — adapter accepts configuration | **GAP — REAL (the one genuine qwen-vs-codex defect).** qwen declares `configuration=True`, and the shared `invocation.py` `_provider()` validator accepts `config_overrides`/`service_tier`/`approval_policy`/`permission_mode`/`allowed_tools`/`disallowed_tools`/`mcp_config` for a qwen invocation with **no error or warning** — then qwen's `build_argv` **silently drops every one of them** (unlike codex's `build_argv`, which honors `config_overrides` via `-c <override>` at `provider.py:426`). This is a divergence on the exact code path codex exercises. The fix mirrors claude's blocker #3: **reject-loud** the fields qwen cannot honor (there is no `-c` equivalent in qwen-code, and the Ollama redirect is already delivered by the adapter's own `_route_argv` → `--openai-base-url`, so `config_overrides` has no honoring path). Asserted (current defective behavior) in `test_qwen_build_argv_silently_drops_override_fields` + `test_qwen_invocation_validator_accepts_override_fields`. |
| F1.2.8 | `notification` — adapter supports immediate wake (codex=TRUE, claude-code=FALSE, **qwen-code=FALSE**) | TESTED-PASSED (`notification_mode("qwen-code")` → `SAFE_BOUNDARY_ONLY` in `test_qwen_adapter_registers_with_notification_false`). This is a **design difference that qwen shares with claude-code**, not a defect — codex is the only provider with `notification=True`. Building qwen a push-wake host adapter is a DESIGN-REC (F5.3), not a gap. |

### 1.3 Built-in adapters

| # | Feature | Status |
|---|---|---|
| F1.3.1 | `CodexProviderAdapter` — `codex exec ... --json --output-last-message`, parses `thread.started`/`turn.completed`/`turn.failed`/`turn.cancelled`, owns `last_message_path`, `notification_wake_text`, `deliver_notification` | N/A-QWEN — CX (codex's own adapter; there is no qwen equivalent to test. The qwen analog — `build_argv`, `parse_transcript_line`, `terminal_outcome` — IS tested: `build_argv` in `test_qwen_build_argv_uses_stream_json`, the COMPLETED parse in the parallel-launch tests, and — closing the previously-thin spot — the **failure/cancel branch** in `test_qwen_parse_and_terminal_map_failure_branch` (qwen collapses codex's distinct `turn.failed`/`turn.cancelled` into one `result` event with `is_error is True OR subtype != "success"` → FAILED; `terminal_outcome` honours a FAILED event even on exit 0). The live codex lane in the parallel demo confirms `CodexProviderAdapter` itself launches.) |
| F1.3.2 | `ClaudeCodeProviderAdapter` — `--print --output-format stream-json`, parses `system/init` + `result/subtype`, no wake (SAFE_BOUNDARY_ONLY) | N/A-QWEN — CX (claude's own adapter; the qwen analog stream-json parsing IS tested — both the COMPLETED path (parallel-launch tests) and the FAILED path (`test_qwen_parse_and_terminal_map_failure_branch`). Not a qwen gap.) |

### 1.4 Evidence & provenance

| # | Feature | Status |
|---|---|---|
| F1.4.1 | `build_provider_evidence` binds identity/version/capabilities/digest/session/redacted provenance | TESTED-PASSED (`test_qwen_provider_evidence_and_redaction`) |
| F1.4.2 | `redact_command` deterministically redacts credential-shaped tokens | TESTED-PASSED (`test_qwen_provider_evidence_and_redaction`) |
| F1.4.3 | `provider_config_digest` deterministic digest of effective config | COVERED-GENERIC (`provider_config_digest` binds the qwen effective config into `build_provider_evidence`, asserted in `test_qwen_provider_evidence_and_redaction`; deterministic-digest contract in `test_provider_adapter_public_seams.py`, green in the 178-battery) |
| F1.4.4 | `ProviderEvidence.command_provenance` and `launcher_settings.argv` use the same redacted value | TESTED-PASSED (`test_qwen_provider_evidence_and_redaction` asserts the redacted provenance) |

### 1.5 Resume / handoff

| # | Feature | Status |
|---|---|---|
| F1.5.1 | `decide_resume_or_handoff` — RESUME when supported + identity matches; else declared HANDOFF | TESTED-PASSED (`test_qwen_resume_handoff_on_identity_mismatch`) |
| F1.5.2 | `structured_handoff` never fabricates continuity (`fabricated_continuity=False`) | TESTED-PASSED (`test_qwen_resume_handoff_on_identity_mismatch` asserts `fabricated_continuity=False`) |
| F1.5.3 | Identity mismatch, session mismatch, unsupported resume → HANDOFF | TESTED-PASSED (`test_qwen_resume_handoff_on_identity_mismatch` asserts HANDOFF on identity mismatch) |

### 1.6 Notification mode

| # | Feature | Status |
|---|---|---|
| F1.6.1 | `notification_mode(provider_id)` → `WAKE` (codex) or `SAFE_BOUNDARY_ONLY` (claude, qwen) | TESTED-PASSED (`test_qwen_adapter_registers_with_notification_false` asserts `SAFE_BOUNDARY_ONLY`) |
| F1.6.2 | `WAKE` only for adapters with real `deliver_notification` binding | TESTED-PASSED (qwen has no wake text; `wake_text` is `None` in `test_qwen_adapter_registers_with_notification_false`) |
| F1.6.3 | Post-registration wake-text mutation fails closed to SAFE_BOUNDARY_ONLY | TESTED-PASSED (`test_qwen_wake_text_mutation_fails_closed_to_safe_boundary`: the live qwen adapter is mutated post-registration to return the exact `NOTIFICATION_WAKE_TEXT`, yet `notification_mode("qwen-code")` still resolves `SAFE_BOUNDARY_ONLY` with `wake_text=None` because the capability is `notification=False` — a mutated qwen adapter can never silently become a WAKE provider) |

---

## 2. Lane Controller (`lane_controller.py`)

### 2.1 Invocation validation & launch

| # | Feature | Status |
|---|---|---|
| F2.1.1 | Parse canonical `orchestrator-worker-invocation/v1` / `orchestrator-coding-invocation/v1` | TESTED-PASSED (canonical invocations built and parsed in every `_canonical`-driven test) |
| F2.1.2 | Validate provider is registered; unsupported → `PROVIDER_OPERATION_UNSUPPORTED` | TESTED-PASSED (`test_qwen_unregistered_provider_fails_closed_before_launch`: with qwen-code unregistered, a controller run exits 2 with "is not a registered provider" and launches no provider process; registry restored after) |
| F2.1.3 | Build argv via selected adapter; launch via `subprocess.Popen` with process boundary | TESTED-PASSED (qwen lanes launched via the adapter in the parallel-launch tests) |
| F2.1.4 | Write prompt via `adapter.encode_prompt`; close stdin | COVERED-GENERIC (`test_lane_controller.py` prompt-write/stdin-close path, green in the 178-battery; the qwen fake CLI reads stdin to EOF on every parallel-launch test, proving the controller closes it) |
| F2.1.5 | Drain stdout/stderr in threads; parse transcript lines; record session identity | TESTED-PASSED (qwen `system/init`/`result` lines parsed in the parallel-launch tests) |
| F2.1.6 | `terminal_outcome` from adapter; publish `PROVIDER_EXITED`/`CODEX_EXITED` only for closed vocabulary | TESTED-PASSED for the narrow assertion (qwen lanes reach `PROVIDER_EXITED` with `COMPLETED`/`FAILED`, both in the closed vocabulary, in the parallel-launch and failure-branch tests). **But note:** qwen's `terminal_outcome` never returns `CANCELLED`, collapsing cancellation into `FAILED` — a real gap vs codex's distinct `turn.cancelled → CANCELLED`. See "Second real gap" below. |
| F2.1.7 | Unknown terminal outcome → controller failure (fail closed) | COVERED-GENERIC (`test_lane_controller.py` / `test_coding_lane_controller.py` closed-vocabulary outcome gate, green in the 178-battery; provider-neutral — qwen `terminal_outcome` returns only the closed set) |
| F2.1.8 | Child environment isolation (cleared variables, profile grants) | COVERED-GENERIC — PA (`test_lane_controller.py` / `test_real_agent_isolation.py` env-isolation cases, green in the 178-battery / real-agent suite; OS-process behavior, provider-neutral) |
| F2.1.9 | Process boundary (windows-job) attach, inventory, cleanup, final reap | COVERED-GENERIC — PA (`test_process_supervisor.py` / `test_processes.py` / `test_integration_processes.py`, green in the 178-battery; the live qwen parallel-launch demo exercises real windows-job attach/reap incidentally) |
| F2.1.10 | Overlay receipt verification before subagent launch | TESTED-PASSED (both the success path in `test_overlay_super_cache_into_subagent_worktree` and the fail-closed path in `test_overlay_receipt_rejected_before_launch`) |

### 2.2 Resource claims (`resource_locks.py`)

| # | Feature | Status |
|---|---|---|
| F2.2.1 | `ResourceClaims.acquire_all` — named exclusive claims, kernel-locked | TESTED-PASSED (two qwen lanes serialize on `service:qwen-db` in `test_resource_contention_serializes_two_qwen_lanes`) |
| F2.2.2 | `arm_boundary` — durable fail-closed marker before provider launch | COVERED-GENERIC — PA (`test_resource_locks.py` boundary-arming cases, green in the 178-battery; provider-neutral kernel-lock mechanism, qwen lanes serialize through it in `test_resource_contention_serializes_two_qwen_lanes`) |
| F2.2.3 | `retain_boundary` — persist exact unresolved boundary identities | COVERED-GENERIC — PA (`test_resource_locks.py`, green in the 178-battery; provider-neutral) |
| F2.2.4 | `release_all` — exact-byte CAS release | TESTED-PASSED (the second qwen lane proceeds after the first releases the claim in `test_resource_contention_serializes_two_qwen_lanes`) |
| F2.2.5 | Stale reclaim revalidation under kernel lock; `PROVEN_STALE` only | COVERED-GENERIC — PA (`test_resource_locks.py` / `test_controller_lock_cleanup.py` stale-reclaim cases, green in the 178-battery; provider-neutral) |
| F2.2.6 | Owner identity (PID + creation identity) reuse detection | COVERED-GENERIC — PA (`test_resource_locks.py` / `test_controller_lock_cleanup.py`, green in the 178-battery; provider-neutral) |

### 2.3 Lifecycle registry (`lane_lifecycle.py`)

| # | Feature | Status |
|---|---|---|
| F2.3.1 | `allocate_immutable_source_view` — exact full-commit read-only source view | COVERED-GENERIC (`test_s4_contract.py` / `test_coding_lane_controller.py` immutable-source-view cases, green in the 129-test lifecycle/broker battery 2026-08-20; `lane_lifecycle` is provider-neutral — a qwen lane allocates the same view) |
| F2.3.2 | `retire_terminal_lane` — archive-first retirement (copy + hash-bound evidence) | COVERED-GENERIC (`test_s4_contract.py` / `test_s4_repair.py` archive-first retirement cases, green in the 129-test battery 2026-08-20; provider-neutral) |
| F2.3.3 | Lifecycle registry admission coordinate (canonical Git identity) | COVERED-GENERIC (`test_s4_contract.py` / `test_coding_lane_controller.py` admission-coordinate cases, green in the 129-test battery 2026-08-20; the canonical Git identity is the same one qwen lanes admit under) |
| F2.3.4 | `ImmutableSourceView` / `RetirementResult` records | COVERED-GENERIC (`test_s4_contract.py`, green in the 129-test battery 2026-08-20; provider-neutral record types) |

---

## 3. Workspace Overlay (`workspace_overlay.py`)

| # | Feature | Status |
|---|---|---|
| F3.1 | `ingest_super_cache` — contents-only refresh, staged mirror + byte-verify + swap | TESTED-PASSED (`test_overlay_super_cache_into_subagent_worktree`) |
| F3.2 | `prepare_worktree` — preflight-before-mutation; create/merge/exact-append; collision rejection | TESTED-PASSED (`test_overlay_super_cache_into_subagent_worktree`) |
| F3.3 | `.super-cache.json` `append_text` declaration (control data, never copied) | TESTED-PASSED (`test_qwen_overlay_collision_rejected_atomically` asserts the `.super-cache.json` control declaration is never materialized into the qwen subagent worktree; append_text list parsing also covered generically by `test_workspace_overlay.py`) |
| F3.4 | `restore_worktree` — exact-byte restoration on retirement | TESTED-PASSED (`test_qwen_overlay_receipt_restores_on_retirement`: ingest→prepare overlays files into a qwen subagent worktree, then `restore_worktree` returns outcome RESTORED and the overlaid files are gone; byte-level mechanics also covered generically by test_workspace_overlay.py) |
| F3.5 | `verify_overlay_receipt` — receipt validation | TESTED-PASSED (wrong-role receipt fails closed in `test_overlay_receipt_rejected_before_launch`) |
| F3.6 | Reparse/symlink rejection throughout | COVERED-GENERIC — PA (`test_workspace_overlay.py` reparse-rejection cases, green in the 178-test provider-neutral battery 2026-08-20) |
| I5 | Overlay collision detection (`OverlayCollisionError`) — append-only copy plan rejection | TESTED-PASSED (`test_qwen_overlay_collision_rejected_atomically`: a create-collision is induced in a qwen subagent worktree and `OverlayCollisionError` is raised before any mutation) |
| I8 | Receipt rollback on partial-apply failure | TESTED-PASSED (`test_qwen_overlay_collision_rejected_atomically` asserts the atomic no-partial-apply guarantee: on collision the colliding file is byte-unchanged, the non-colliding create was never applied, and no receipt was published) |

---

## 4. Git Safety (`git_safety.py`)

| # | Feature | Status |
|---|---|---|
| F4.1 | `inspect_repository` — worktree root, common dir, branch, base/head commit validation | TESTED-PASSED (each qwen lane's repository is validated before launch in the parallel-launch tests) |
| F4.2 | `validate_coding_result` — branch/tip/clean-worktree gate; checks shape | COVERED-GENERIC (`test_git_results.py` / `test_coding_lane_controller.py` result-gate cases, green in the 178-battery; the qwen side asserts the same gate on real qwen results in `test_stale_result_rejected_for_qwen_lane` and the parallel-launch tests) |
| F4.3 | `active_declaration_conflicts` — duplicate branch/worktree detection | COVERED-GENERIC (`test_git_results.py` / `test_s4_repair.py`, green in the 178-battery; provider-neutral safety check — a qwen-local reproduction needs two genuinely-live sibling processes and is racy on Windows, so it is verified in the generic suite rather than duplicated) |
| F4.4 | `validate_findings` — finding gate (closed schema, outcome/count match) | COVERED-GENERIC (`test_finding_gate.py`, green in the 178-battery; provider-neutral finding schema/outcome-count gate) |
| F4.5 | `validate_task_result_repository` — canonical result + branch/tip/clean gate | TESTED-PASSED (stale result rejected in `test_stale_result_rejected_for_qwen_lane`; valid results accepted in the parallel-launch tests) |

---

## 5. Notifications & Manager Queue (`notifications.py`, `host_adapters.py`)

### 5.1 ManagerEventRouter

| # | Feature | Status |
|---|---|---|
| F5.1.1 | `admit` — durable queue record with binding validation | TESTED-PASSED (`test_s3_manager_queue_admit_and_ack`) |
| F5.1.2 | `next_event` / `pending_events` — queue cursor | TESTED-PASSED (`test_s3_manager_queue_admit_and_ack`) |
| F5.1.3 | `acknowledge` — exact event ID ack; only manager action may ack | TESTED-PASSED (`test_s3_manager_queue_admit_and_ack`) |
| F5.1.4 | `rebuild_state` — crash recovery from durable queue | TESTED-PASSED (`test_qwen_manager_queue_rebuild_state_recovers_from_journal`: after deleting STATE.json/WAKE.json a fresh `ManagerEventRouter.rebuild_state()` reconstructs the pending event from QUEUE.jsonl alone and the queue is fully operable — ack drains it) |
| F5.1.5 | Event dispositions: `WAKING_MANAGER_EVENT` / `OBSERVED_STATE` / `SUPERSESSION` | COVERED-GENERIC (`test_manager_notifications_adversarial.py` / `test_s3_contract.py` disposition cases, green in the 178-battery; the qwen queue admit/next/ack path is exercised in `test_s3_manager_queue_admit_and_ack`) |
| F5.1.6 | `_WAKING_EVENT_TYPES` — the exhaustive waking set | COVERED-GENERIC (`test_manager_notifications_adversarial.py` / `test_s3_contract.py`, green in the 178-battery; provider-neutral) |

### 5.2 DeliveryCoordinator

| # | Feature | Status |
|---|---|---|
| F5.2.1 | `deliver_at_boundary` — bounded notice at a safe boundary | DESIGN-REC (**not a qwen gap**). `test_qwen_no_push_wake_delivery_path_exists` confirms qwen resolves `SAFE_BOUNDARY_ONLY` with no wake text and `classify_operation("qwen-code","notification")` reports `supported=False` — but this whole delivery subsystem is **codex-only** and **identically unbound for claude** in this worktree (both get `FutureHostFixture`). The `DeliveryCoordinator` types are provider-neutral and not broken, merely unbound absent a host adapter. Recommendation: build a qwen host adapter via qwen's `Stop`/`SessionEnd`/`Notification`(`idle_prompt`) hooks. |
| F5.2.2 | `DeliveryNotice` — payload-free wake edge | DESIGN-REC (not a qwen gap; `test_qwen_no_push_wake_delivery_path_exists` — codex-only subsystem, unbound identically for claude) |
| F5.2.3 | `DeliveryReceipt` — transport evidence only (never an ack) | DESIGN-REC (not a qwen gap; same — build a qwen host adapter to bind it) |
| F5.2.4 | `ManagerEventAck` — the only typed ack object | DESIGN-REC (not a qwen gap; the queue-side ack IS exercised generically in `test_s3_manager_queue_admit_and_ack` — the push-wake producer is the codex-only unbuilt piece) |
| F5.2.5 | Bounded retry with backoff; `DeliveryRetryExhausted` | DESIGN-REC (not a qwen gap; codex-only delivery subsystem, unbound identically for claude) |
| F5.2.6 | Exact-binding validation (run/queue/session/thread/registration) | DESIGN-REC (not a qwen gap; codex-only delivery subsystem, unbound identically for claude) |

### 5.3 Host adapters

| # | Feature | Status |
|---|---|---|
| F5.3.1 | `AdapterCapabilities` — active_turn_notice, idle_wake, next_input_injection, finalization_gate | DESIGN-REC (**not a qwen gap**). `AdapterCapabilities` has exactly two factories in `host_adapters.py` — `codex()` (all True) and `future_fixture()` (all False). There is **no `claude()` and no `qwen()`**, so qwen and claude are byte-identical here: both get `future_fixture()`. Recommendation: add a `qwen()` factory backed by qwen's `Notification`/`idle_prompt` hook for `idle_wake`. |
| F5.3.2 | `HostProfile` / `FutureHostFixture` — contract-only future host | DESIGN-REC (not a qwen gap; `test_qwen_no_push_wake_delivery_path_exists` — qwen gets the **same** `FutureHostFixture` as claude in this worktree. The claude side of this exact subsystem was later built in Phase 4 in a different clone; the qwen equivalent is the recommended follow-up, not a compatibility gap.) |
| F5.3.3 | `CodexAdapter` (in `codex_adapter.py`) — installed hook routes, `synthetic_wake_self_test` | N/A-QWEN — CX (codex-only host adapter; qwen has no host adapter — that absence is the documented GAP confirmed in `test_qwen_no_push_wake_delivery_path_exists`, so the qwen-relevant fact IS tested) |

---

## 6. CLI (`cli.py`)

| # | Feature | Status |
|---|---|---|
| F6.1 | `scan` — one reconciled snapshot JSON | COVERED-GENERIC (`test_events_cli.py` / `test_reconcile.py` scan-snapshot cases, green in the 178-battery; provider-neutral CLI over the watcher) |
| F6.2 | `watch --once` — diff vs persisted cursor, emit changed events | COVERED-GENERIC (`test_events_cli.py` diff-vs-cursor cases, green in the 178-battery; provider-neutral) |
| F6.3 | `watch --until-event` — poll without model, return on first material event | COVERED-GENERIC (`test_events_cli.py` until-event cases, green in the 178-battery; the qwen-specific sibling `watch --until-actionable` is directly tested in `test_qwen_watch_until_actionable_observes_actionable_condition`) |
| F6.4 | `watch --until-actionable` — block on diagnostic facts | TESTED-PASSED (`test_qwen_watch_until_actionable_observes_actionable_condition`: `watch_until_actionable` returns EXIT_OK on a MANAGER_SIGNAL actionable condition, and the test ties the polling requirement back to qwen's `SAFE_BOUNDARY_ONLY` notification mode — the polling workaround for the notification design difference) |
| F6.5 | `handoff-preflight` — preflight task-card/invocation/result/dependency-map/worktree/evidence | COVERED-GENERIC (`test_handoff_preflight.py`, green 2026-08-20; provider-neutral preflight over the canonical invocation/result schema qwen also uses) |
| F6.6 | `adapter install/check/upgrade/uninstall/self-test/hook` — codex host adapter | N/A-QWEN — CX (these CLI verbs manage the codex host adapter; qwen has no host adapter to install — that absence is the GAP confirmed in `test_qwen_no_push_wake_delivery_path_exists`) |
| F6.7 | `view`/`source allocate` — immutable source view | COVERED-GENERIC (`test_s4_contract.py` / `test_coding_lane_controller.py` immutable-source-view cases, green 2026-08-20; provider-neutral CLI over `lane_lifecycle.allocate_immutable_source_view`) |
| F6.8 | `lane retire` — terminal lane retirement | COVERED-GENERIC (`test_s4_contract.py` / `test_s4_repair.py` archive-first retirement cases, green 2026-08-20; provider-neutral CLI over `lane_lifecycle.retire_terminal_lane`) |
| F6.9 | `workspace super-cache ingest` / `workspace prepare` — overlay lifecycle | TESTED-PASSED (via direct calls to `ingest_super_cache`/`prepare_worktree` in the overlay tests; CLI wrapper itself not separately invoked) |
| F6.10 | Exit codes: `EXIT_OK=0`, `EXIT_ERROR=1`, `EXIT_TIMEOUT=3` | TESTED-PASSED (partial — exit code 2 observed for stale-result rejection, exit code 1 for overlay-receipt rejection) |

---

## 7. Watcher / Observation (`reconcile.py`, `events.py`, `discovery.py`, `processes.py`)

| # | Feature | Status |
|---|---|---|
| F7.1 | `discover_suite` — discover controller status files under run workspaces | COVERED-GENERIC — PA (`test_discovery.py`, green in the 178-battery; discovers the same controller status files a qwen lane writes) |
| F7.2 | `reconcile` — one OS process snapshot per scan; derive operational states | COVERED-GENERIC — PA (`test_reconcile.py`, green in the 178-battery; provider-neutral) |
| F7.3 | `diff_conditions` — stable deterministic event IDs; at-least-once crash consistency | COVERED-GENERIC — PA (`test_reconcile.py` diff/event-id cases, green in the 178-battery) |
| F7.4 | `conditions_from_snapshot` / `select_actionable` — actionable selection | COVERED-GENERIC — PA (`test_reconcile.py`; the qwen actionable-selection path is also exercised end-to-end in `test_qwen_watch_until_actionable_observes_actionable_condition`) |
| F7.5 | `process_snapshot` — Windows/CIM + Linux `/proc` discovery | COVERED-GENERIC — PA (`test_processes.py` / `test_integration_processes.py`, green in the 178-battery; the live qwen parallel demo drives real Windows CIM discovery) |
| F7.6 | `merge_watcher_conditions` — diagnostic conditions | COVERED-GENERIC — PA (`test_reconcile.py` merge-conditions cases, green in the 178-battery) |

---

## 8. Capability Broker (`capability_broker.py`)

| # | Feature | Status |
|---|---|---|
| F8.1 | `CapabilityRequest` — closed canonical request, no endpoint-bearing fields | COVERED-GENERIC (`test_s5_capability_broker.py` request-schema cases, green in the 129-test lifecycle/broker battery 2026-08-20; `capability_broker` is provider-neutral — the firmware adapters stay OOS) |
| F8.2 | `CapabilitySnapshot` — verified current observation | COVERED-GENERIC (`test_s5_capability_broker.py` snapshot cases, green in the 129-test battery 2026-08-20) |
| F8.3 | `CapabilityApproval` — signed approval bound to request + snapshot | COVERED-GENERIC (`test_s5_capability_broker.py` approval-binding cases, green in the 129-test battery 2026-08-20) |
| F8.4 | `CapabilityPermit` — immutable in-memory handoff | COVERED-GENERIC (`test_s5_capability_broker.py` permit cases, green in the 129-test battery 2026-08-20) |
| F8.5 | `CapabilityBroker` — request → snapshot → approval → permit → result → cleanup | COVERED-GENERIC (`test_s5_capability_broker.py` full request→permit→cleanup cycle + `CapabilityDenied`/`CapabilityAdapterUnavailable` fail-closed cases, green in the 129-test battery 2026-08-20) |
| F8.6 | `_public_json` — rejects private capability material (tokens, credentials) | COVERED-GENERIC (`test_s5_capability_broker.py` private-material-rejection cases, green in the 129-test battery 2026-08-20) |

---

## 9. Firmware (out of scope for qwen testing)

| # | Feature | Status |
|---|---|---|
| F9.1 | `firmware_campaign.py` — `FirmwareCampaignPack`, `FirmwareAction`, `FirmwareOperation` | NOT-TESTED — OOS |
| F9.2 | `firmware_adapter.py` — `FirmwareHardwareAdapter`, `HardwareCapabilityAdapter` | NOT-TESTED — OOS |
| F9.3 | Legacy policy-bound firmware invocation path | NOT-TESTED — OOS |
| F9.4 | MCP-server-related traffic (`--mcp-config`, broker-compatible MCP in firmware seam) | NOT-TESTED — OOS |

> **Per instruction:** firmware and MCP-server functionality are **not tested** in the
> qwen multi-agent suite. This is a documented gap, not a finding they work.

---

## 10. Multi-Agent / Coordination Features (the qwen focus)

| # | Feature | Test | Status |
|---|---|---|---|
| F10.1 | Spawn **multiple** deepseek agents via headless qwen-code exec processes | `test_two_qwen_agents_launch_in_parallel_worktrees` | TESTED-PASSED |
| F10.2 | Each agent in its own git worktree (parallel lanes) | `test_two_qwen_agents_launch_in_parallel_worktrees` | TESTED-PASSED |
| F10.3 | Resource contention — named exclusive claims serialize contention | `test_resource_contention_serializes_two_qwen_lanes` | TESTED-PASSED |
| F10.4 | Stale result rejection — a lane with a stale RESULT.json is rejected | `test_stale_result_rejected_for_qwen_lane` | TESTED-PASSED |
| F10.5 | Merge lane — launch a merge lane, run project checks, accept/promote candidate | `test_merge_lane_and_integration_merge` | TESTED-PASSED |
| F10.6 | Integration merges — merge alpha + beta branches into an integration branch | `test_merge_lane_and_integration_merge` | TESTED-PASSED |
| F10.7 | Subagent coordination — overlay super-cache into subagent worktrees | `test_overlay_super_cache_into_subagent_worktree` | TESTED-PASSED |
| F10.8 | Stable states — `PROVIDER_EXITED`/`CODEX_EXITED` with valid result | `test_two_qwen_agents_launch_in_parallel_worktrees` | TESTED-PASSED |
| F10.9 | Hook notification when agents finish — qwen adapter has `notification=False` (design difference shared with claude) | `test_qwen_adapter_registers_with_notification_false` | TESTED-PASSED (no push wake, manager polls; building a qwen host adapter is a DESIGN-REC at F5.3, not a gap) |
| F10.10 | S3 manager queue — admit/next/acknowledge events | `test_s3_manager_queue_admit_and_ack` | TESTED-PASSED |

---

## Claude-gap cross-check (qwen-relevant findings from `claude_listed_features.md`)

Claude's `claude_listed_features.md` recorded four TESTED-FAILED findings. Each
was re-examined against the qwen adapter. Three of the four are **not** qwen
failures (qwen's argv is correct and the bypass is unconditional). **Only one —
C17/U4 — is a genuine qwen-vs-codex defect** (the single GAP — REAL in this
inventory, F1.2.7). A17 is a *missing convenience artifact*, not a behavioral
defect, and is downgraded accordingly.

| Claude row | Feature | qwen result | Test | Status |
|---|---|---|---|---|
| U1/U2 | `ProviderLaunchSpec` → `build_argv` translation; stream-json flag correctness | qwen's `build_argv` emits `--output-format stream-json` correctly. **No missing-flag failure** (unlike claude's `--print`+`stream-json` without `--verbose`). The argv is complete and launchable as built. | `test_qwen_build_argv_uses_stream_json` | PASSED (no qwen defect) |
| U3 | Permission-mode / sandbox-bypass propagation into provider argv | qwen **hardcodes `--approval-mode=yolo` unconditionally**, so the bypass is always on. **No silent-false-COMPLETED risk** from an omitted optional field (unlike claude, which only emits a bypass when `provider.permission_mode` is explicitly set). | `test_qwen_build_argv_hardcodes_approval_mode_yolo` | PASSED (no qwen defect) |
| C17/U4 | `config_overrides`/`service_tier`/`approval_policy` generic override channel | **GAP — REAL (F1.2.7): the one genuine qwen defect.** The shared `invocation.py` `_provider()` validator accepts `config_overrides`/`service_tier`/`approval_policy`/`permission_mode`/`allowed_tools`/`disallowed_tools`/`mcp_config` for a qwen invocation with zero error or warning, then qwen's `build_argv` **silently drops them all** — whereas codex's `build_argv` honors `config_overrides` via `-c` (`provider.py:426`). Fix = reject-loud (claude's blocker #3 applied to qwen). | `test_qwen_build_argv_silently_drops_override_fields` + `test_qwen_invocation_validator_accepts_override_fields` | **GAP — REAL** (asserts the current defect) |
| A17 | Disposable two-worktree integration fixture | **Not a defect — a missing convenience file.** `examples/disposable_coding_fixture.py` is codex-only; no `examples/*qwen*` file exists (claude lacked one too until one was authored). Building a qwen invocation works today via the canonical `orchestrator-worker-invocation/v1` schema — the fixture is a nicety, not a capability gap. | `test_no_qwen_example_fixture_exists` | MINOR (missing example artifact; low priority) |

---

## The real qwen gaps (two)

| Gap | Detail |
|---|---|
| **1. Generic override channel silently dropped (C17/U4 → F1.2.7)** | The shared `invocation.py` `_provider()` validator accepts `config_overrides`/`service_tier`/`approval_policy`/`permission_mode`/`allowed_tools`/`disallowed_tools`/invocation `mcp_config` for a qwen invocation with no error or warning, then qwen's `build_argv` **silently drops them** — whereas codex honors `config_overrides` (`-c`, `provider.py:426`). A qwen-vs-codex divergence on a shared code path. **Fix = reject-loud** (the qwen-side of claude's blocker #3): raise `InvocationValidationError` for the fields qwen cannot honor, since qwen-code has no `-c` equivalent and the Ollama redirect is already delivered by the adapter's own `_route_argv`. |
| **2. Terminal `CANCELLED` collapsed to `FAILED`** | Codex records a distinct `CANCELLED` on cancellation (`turn.cancelled → CANCELLED`, `provider.py:447,458,465`); qwen's `parse_transcript_line`/`terminal_outcome` collapse it into `FAILED` and never emit `CANCELLED`. Since the aim is to mirror codex, this is a real divergence on a path codex exercises. **Low severity** (every downstream branch treats FAILED==CANCELLED — `lane_controller.py:3208`, `notifications.py:1762`, `reconcile.py:191-206`), but it produces a real audit/state-fidelity divergence: a cancelled qwen lane persists as `provider_failed` where codex persists `provider_cancelled`. **Closeable** (unlike claude's U15): qwen-code exits **130** on SIGINT and has an `interrupt` control subtype. **Fix** = map exit-130 / `interrupt` → `CANCELLED` in `terminal_outcome`. See "Second real gap" section for the full write-up. |

## Design recommendations (NOT gaps — codex-only subsystem or provider-neutral, identical to claude)

These were previously mislabeled "gaps." Each is a **recommendation to build a qwen
host adapter**, not a qwen-vs-codex compatibility gap — codex is the only provider
that has this subsystem, and claude is in the exact same unbuilt state here.

| Item | Detail |
|---|---|
| No push "finish" notification / host adapter (F1.2.8, F5.2.1–6, F5.3.1–2) | qwen registers `notification=False` → `SAFE_BOUNDARY_ONLY`, and gets `FutureHostFixture` (all capabilities False). A finishing qwen lane produces no push wake; the manager must poll. **Implementable, not a design constraint**: qwen-code has a hooks mechanism (`Stop`, `SessionEnd`, `SubagentStop`, `Notification`/`idle_prompt`) that could back a push-wake host adapter. **Identical to claude-code's state in this worktree** (`AdapterCapabilities` has only `codex()` and `future_fixture()` factories — no `claude()`, no `qwen()`). The claude side of this subsystem was later built in Phase 4 in a separate clone; the qwen equivalent is the recommended follow-up. |
| Overlay control data dirties the worktree | Materialized overlay files are untracked and fail the result gate unless git-ignored + committed. **Provider-neutral** footgun (identical for codex), surfaced in the multi-agent overlay scenario — not a qwen defect. |
| No qwen example/fixture (A17) | `examples/` contains only the codex-only `disposable_coding_fixture.py`. A **missing convenience file**, not a capability gap — a qwen invocation works today via the canonical `orchestrator-worker-invocation/v1` schema. |

## Second real gap (low severity, closeable) — terminal `CANCELLED` outcome collapsed to `FAILED`

qwen's `parse_transcript_line` maps a cancelled/interrupted run to **FAILED**
(no result line + non-zero exit → `terminal_outcome` returns FAILED), and never
returns `CANCELLED`. **Codex, on the same cancel path, records a distinct
`CANCELLED`**: `turn.cancelled` → `ProviderEvent(kind="CANCELLED")` →
`terminal_outcome` returns `"CANCELLED"` (`provider.py:447,458,465`). Since the
goal is to mirror codex, this divergence on a path codex exercises **is a real
gap**, not a design-rec. It is **closeable**: qwen-code's own bundled
`structured-output.md` says a SIGINT/interrupt exits **130** and normally emits no
result line ("treat the exit code as the source of truth"), and qwen-code carries
an `interrupt` control subtype — so mapping exit-130 / `interrupt` → `CANCELLED`
is implementable. (This is precisely what makes it *unlike* claude's unclosable
U15, where the CLI emits no cancellation signal at all.)

**Why it is low severity, not moot:** every downstream *branch decision* already
treats `FAILED` and `CANCELLED` identically — same controller exit code
(`lane_controller.py:3208`), same notification priority (`notifications.py:1762`),
same reconcile grouping (`reconcile.py:191-206`) — so there is no control-flow or
behavioral consequence today. But the **recorded terminal identity diverges**: the
whole stack models CANCELLED as first-class (`lane_controller` closed vocabulary
`3143-3153`; `reconcile.py` distinct `provider_cancelled` `194`; `notifications.py`
distinct `cancelled` `1760`), so a cancelled qwen lane is persisted as
`provider_failed` where codex would persist `provider_cancelled` — an audit /
state-fidelity divergence from codex. Fix: map qwen exit-130 (or the `interrupt`
subtype) → `CANCELLED` in `terminal_outcome`. Both the success and the current
FAILED-collapse branches are covered by
`test_qwen_parse_and_terminal_map_failure_branch`; a corrected mapping would need a
new assertion that exit-130 yields `CANCELLED`.

## Explicitly out of scope (per instruction)

| Feature | Reason |
|---|---|
| Firmware (`firmware_campaign.py`, `firmware_adapter.py`, legacy policy-bound path) | Not tested per instruction. |
| MCP-server functionality (`--mcp-config`, broker-compatible MCP in firmware seam) | Not tested per instruction. May be simtested on the MCP server; noted as a gap, not a pass. |

## How to run

```text
cd harness-single-worktrees/qwencode-test
python -m unittest orchestrator_harness.tests.test_qwen_multi_agent -v
```

All 24 tests pass (~120s). The COVERED-GENERIC rows are additionally backed by
the provider-neutral suites cited inline (run them with
`python -m unittest orchestrator_harness.tests.test_provider_adapter_registry
orchestrator_harness.tests.test_s4_contract
orchestrator_harness.tests.test_s5_capability_broker` etc.). See
`missing_qwencode_implementation.md` for the full evidence behind the documented
qwen-vs-codex gaps.
