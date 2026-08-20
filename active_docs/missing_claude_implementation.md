# Missing / broken Claude Code support in `Firmware/target-harness`

**Last updated: 2026-08-20 — rewritten to reflect the phase 0–4 compatibility-testing results.**
The previous revision of this file described the pre-testing state (the 4 launch blockers listed
as "still broken"). That is now out of date: **all 4 original blockers are fixed** (in the
disposable clone, not yet merged), **Phase 4 built the real Claude host adapter** (closing the
30-row CX-GAP subsystem gap), and phases 1–4 surfaced a **new, smaller set of genuine gaps** that
are what "missing" now means. This file is the human-readable companion to
`active_docs/claude_listed_Features.md` (the 346-row inventory) and
`plans/compatibility-testing/evidence/FINDINGS.md` (per-finding evidence).

Scope: `orchestrator_harness`, tested read-only/detection-only against the real `claude` CLI
v2.1.233 (pointed at a local Ollama backend for live lanes) and against synthetic fixtures for the
provider-neutral logic. `Firmware/target-harness` itself was **never modified** — all source fixes
live in the disposable clone described below.

---

## TL;DR — what is actually missing now

| Bucket | Count | Status |
|---|---|---|
| Original launch blockers (§A) | 4 | **FIXED** in clone `compat-test-copy`; **not merged** to `Firmware/target-harness` |
| Host-adapter / delivery subsystem (§B, formerly the big "CX-GAP") | 30 rows | **IMPLEMENTED** in Phase 4 (real `ClaudeAdapter`) |
| Genuinely-absent features / divergences from intended design (§C) | 18 GAP rows | **RECORDED, not fixed** — detection-only phases record, they don't patch |
| Live rows not yet authentically reproduced on the weak Ollama backend (§D) | 8 rows | reachable by coaching / accepted synthetically per user decision |
| Firmware + MCP (§E) | — | **OUT OF SCOPE** per instruction (MCP later shown to work live, see §D note) |

The important correction versus the old version of this file: **there is no longer a "Claude lane
can't even launch" story.** A Claude lane launches, runs, commits, resumes, and is coached to a
valid committed result end-to-end. What remains are (a) source fixes not yet merged upstream and
(b) a set of *design-intent divergences* — most of which are the harness being **stricter/safer**
than the plan text, plus a few genuinely-absent capabilities.

---

## A. The 4 original launch blockers — now FIXED (clone only, unmerged)

All four were confirmed broken against the real CLI, then fixed and verified in the disposable
worktree. **None are merged into `Firmware/target-harness`** — they are uncommitted working-tree
state on branch `compat-test-copy`.

- **Repository:** the `harness-single` submodule (`origin https://github.com/JasonPeng2019/harness-single.git`).
- **Worktree with the fixes:** `harness-single-worktrees/compat-test`, created from
  `Firmware/target-harness` @ `dd673cb`, branch **`compat-test-copy`**.
- **Files touched (tracked-modified):** `provider.py` (+140/−7), `lane_controller.py` (+36),
  `invocation.py` (+11), `tests/test_s2_contract.py`, `.gitignore`.
- **Evidence:** `plans/compatibility-testing/evidence/0.1/`…`0.5/`; ledger
  `plans/compatibility-testing/evidence/COORDINATOR-LOG.md`.

| # | Original defect | Fix (step) |
|---|---|---|
| 1 | `ClaudeCodeProviderAdapter.build_argv` never emitted `--verbose`, so the real CLI hard-rejected `--print --output-format stream-json` (exit 1). Every Claude lane failed before the first turn. | `build_argv` now always appends `--verbose` in print/stream-json mode (0.1). Regression: `tests/test_compat_provider_argv.py`. |
| 2 | No automatic permission bypass → a lane with every tool blocked exited 0 and was mapped to **COMPLETED** (silent false-success). | Default `--permission-mode bypassPermissions` (explicit caller value still wins); `parse_transcript_line` now maps `system/permission_denied` and terminal `permission_denials` → **FAILED** (0.2). Regression: `tests/test_compat_transcript_parse.py`. |
| 3 | `config_overrides` / `service_tier` / `approval_policy` were accepted by the validator, then silently dropped for `claude-code` — including the `model_provider="ollama"` redirect the whole test rig depends on. | **Reject-loud + honor**: `config_overrides` honored via a child-env channel (`ProviderLaunchSpec.env_overrides`; `model_provider="ollama"` alias → `ANTHROPIC_BASE_URL`/`AUTH_TOKEN`/`API_KEY`), wired through `lane_controller` after isolation filtering; `service_tier`/`approval_policy` on claude-code now raise `InvocationValidationError` (0.3). Regression: `tests/test_compat_provider_allowlist.py`; live env-merge proof in `evidence/0.3/`. |
| 4 | No working Claude example/fixture existed anywhere (only Codex-shaped examples + one synthetic-binary test). | New `examples/coding.claude.invocation.example.json` (+`.md`) and `examples/disposable_claude_coding_fixture.py` — a real single-lane fixture that runs end-to-end on the local Ollama backend (0.4). Two live runs in `evidence/0.4/`. |

> **Merge caveat:** the formal phase-0 gate (step 0.5) has **not** yet been re-run to green — it
> was blocked 2026-08-18 by the Ollama account's session usage limit — and nothing above is merged
> upstream. Until merged, `Firmware/target-harness` on `firmware/v2-candidate` still has all four
> defects.

---

## B. Host-adapter / S4 delivery subsystem — now IMPLEMENTED (Phase 4)

Previously the single largest gap: Claude got a `FutureHostFixture` honest-stub instead of a real
host adapter, so the entire owned-installer + delivery-coordinator stack existed only for Codex
(30 inventory rows tagged CX-GAP). This was **not** an argv bug — it was a missing subsystem.

**Phase 4 built the real `ClaudeAdapter`.** All 30 provider-neutral rows are now built-and-tested
or held as a green Codex regression reference:

- **Delivery / wake (4.A):** N1, N2, N3, N6, N8, A24, G17, G19 — real `ClaudeAdapter` replaces
  `FutureHostFixture`; idle-wake is `claude --resume <session_id>` cross-process re-entry (Claude
  Code has no in-session injection API, so resume-as-wake is the equivalent mechanism).
- **Owned installer (4.B):** B9–B14 (`adapter install/check/upgrade/uninstall/self-test/hook`).
- **Codex regression reference (4.C):** M1–M16 held green (`test_codex_bounded_policy.py` +
  `test_s4_contract.py` + `test_compat_host_adapters.py` → 45 passed).

Root re-ran `pytest test_compat_claude_adapter.py` → 14 passed / 3 subtests, and read
`claude_adapter.py` in full to confirm real seams (not mocks). Acceptance:
`evidence/PHASE4-ORCHESTRATOR_ACCEPTANCE.json` (`decision: ACCEPTED`, `rows_rejected: []`,
`gaps_opened: []`).

---

## C. The genuinely-missing features & design-intent divergences (18 GAP rows)

These are the *actual* "missing implementation" items as of the current testing. Phases 1–2 are
detection-only unit tests over the real Codex-era modules; a **GAP** means the test ran and pinned
the actual behavior, and that behavior diverges from what the Codex-era plan intended. Full
evidence per row: `plans/compatibility-testing/evidence/FINDINGS.md`. **Nothing here is a launch
blocker; nothing here was patched** (only phase 0 changed code).

Read the two sub-buckets differently — most of these are the harness being *safer* than the plan,
not a hole a Claude consumer falls into.

### C.1 — Capabilities genuinely absent (a real "product would have this" gap)

| Row | Finding | What's actually missing |
|---|---|---|
| **A34** | F2E-A34-1 | `release_assets.py` is **read-only manifest accessors only** (`release_manifest`, `manifest_asset_paths`, `read_package_asset`). There is **no packaging/digest engine** — no `build_package`, no archive builder, no content digest over the declared asset set. The packaging half of the intended "public release surface" simply does not exist. |
| **A39 / T3** | F2G-A39-1 | No ordered `STOP_ASSIGNING → … → RESOLVED` **recovery ledger**. `watcher_recovery_projection` is a stateless open/acknowledged/resolved filter+label pass with **no ordering guard**; a lone `resolved` record (never `open`) is admitted unchanged, and `STOP_ASSIGNING` isn't even in `WATCHER_RECOVERY_STATES` (those records are silently dropped). The ordered-admission state machine the plan describes is absent. |
| **G18** | F1F-G18-1 | `HARNESS_SCAN_COMMITTED` is a declared taxonomy kind but **no producer in this worktree emits it**. The "exactly once per scan commit" marker is observable only at the record-contract level (`make_source_record` → one record); the emission path likely lives in the out-of-worktree watcher runtime. |
| **B2** | F1B-B2-1 | `scan --no-write` is **parsed but ignored** — a pure no-op (`scan_command` has no `no_write` parameter and never persists in any mode). Harmless (scan never writes) but misleading: a user could believe the flag is what makes scan safe. |
| **C24** | F1A-C24-1 | The unsupported-operation *record* branch in `_classify_provider_operations` is **dead code** — `unsupported_operation_result` raises `ProviderAdapterError` first. Latent only: `_requested_provider_operations` only ever emits validated operations, so the dead path can't fire from real input today. |
| **F24** | F1E-F24-1 | The result-validation memo (`_RESULT_VALIDATION_CACHE`) covers the **coding-result path only**; the task-result path (`_validate_task_result_cached`) is not memoized and re-validates every pass. A missing optimization, not a correctness gap. |

### C.2 — Present but *narrower / stricter / safer* than the plan text (divergence, not a hole)

These are recorded as GAPs (intended-vs-actual divergence) but in every case the harness is
**stricter, safer, or fail-closed** relative to the plan — a Claude consumer is protected, not
exposed.

| Row | Finding | Divergence (all fail-closed / safer) |
|---|---|---|
| **E19** | F1D-E19-1 | The RUNNING_CODEX/RUNNING_PROVIDER operational-state gate is scoped to conflict detection only; discovery-level result acceptance does **not** reject a valid result offered under `EXITED`/`PROVIDER_EXITED`. (Malformed results are still rejected.) |
| **E20** | F1D-E20-1 | No ">1 candidate result JSON" ambiguity rejection — only the canonical `RESULT.json` is read; a second result-shaped JSON is silently ignored (deterministic, canonical wins). |
| **F3** | F1E-F3-1 | Lane elevates to `WAITING_RELAY` only on `RELAY_READY`; a `RELAY_UNBOUND` request leaves the lane `RUNNING_CODEX` (the request itself is still classified `RELAY_UNBOUND`, so no state is lost). |
| **G1** | F1F-G1-1 | `REQUEST_EXPIRY_WARNING` is selectable only for `WARNING`/`CRITICAL` buckets; an `EXPIRED`-bucket request is emitted but never selected (it has already passed its warning window). |
| **G5** | F1F-G5-1 | `OBSERVATION_ERROR` is emitted for any error but actionable only when a lane/request is live; a lone malformed signal is emitted-but-unselected. |
| **K8** | F1G-K8-1 | Conflicting legacy `resume_thread_id` vs canonical `resume_identity.thread_id` **fail closed** with `InvocationValidationError`, not the plan's "canonical wins" precedence. |
| **Q1** | F1K-Q1-1 | Out-of-range config numbers are **rejected** with `ConfigError`, not silently clamped to bounds. |
| **Q17** | F1K-Q17-1 | `prompt.py` has **no template constants** — it is a pure re-export shim; `compose_prompt_bundle` concatenates component bytes verbatim with no placeholder substitution. |
| **I4** | F2A-I4-1 | `verify_overlay_receipt` is a structural/identity prelaunch check that never reads materialized worktree bytes; byte-integrity is enforced at `restore_worktree` (the destructive boundary), which reports `BLOCKED` "later edit detected". |
| **L4** | F2B-L4-1 | `CapabilityPermit` has **no** use-count field — bounded single-use is broker-enforced via terminal-result caching + `REPLAY_MISMATCH`/`APPROVAL_REPLAY` refusal (no mutable per-permit state to corrupt). |
| **L7** | F2B-L7-1 | An adapter's `CapabilityAdapterUnavailable` from `observe` is **caught** → `DENIED` (`SNAPSHOT_UNAVAILABLE`); the typed exception doesn't propagate to the caller. No permit constructed, `dispatch_calls` stays 0. |

(P7/P11, F2C-P7P11-1, are the same shape — retirement refuses fail-closed via an `outcome=="VISIBLE"`
blocked result rather than raising — but were accepted as TESTED-PASSED-with-note, not counted in
the 18.)

---

## D. Live rows not yet authentically reproduced on the weak Ollama backend

These depend on model *output content*, not CLI mechanics, so the fast/weak
`deepseek-v4-flash:0731-cloud` backend can't always drive them in a single cold turn. Per user
decision (2026-08-20), they are reachable by **orchestrator coaching** (`claude --resume
<session_id> "<corrective prompt>"` continues the same transcript with no committed-RESULT
precondition — see P3-INT-1) across multiple turns until the worker emits a valid committed
`RESULT.json`; the multi-turn run exercises the steady-state/relay/lifecycle/ack events as
byproducts. Rows: **F15, G8–G13, G15, G16, G32-live**. Coaching turns spend live Ollama quota, so
STOP-on-429 applies.

Two items cannot be provoked authentically on this backend and are accepted **synthetically**
(explicitly labeled fake) per user decision:
- **G10** stall events (`MANAGER_REVIEW_DUE`/`LANE_NO_PROGRESS`/`LANE_STAGE_REPEAT`) — S4 removed
  the live stall producers; only the classifier survives (P3-OBS-4).
- A realistic long-running **stall state** the fast model never sits in.

Live rows that *were* authentically observed this round: G21 launch-failure family
(`CONTROLLER_FAILED`/`LAUNCH_FAILED`/`CONTROLLER_INTERRUPTED`, 3.A/P3-OBS-6), V7 actionable-event
gating (3.B), cross-provider shared event log (3.C/P3-OBS-2), and — notably — **MCP works live**:
a claude+Ollama lane completed a full `--mcp-config` round-trip against a local stdio server with
exactly one `mcp__marker__record_marker` tool_use (3.D/P3-OBS-5).

---

## E. Explicit scope exclusions (per instruction)

Firmware-specific functionality (`firmware_campaign.py`, `firmware_adapter.py`,
`FirmwareCampaignPack`/`FirmwareAction`/`FirmwareHardwareAdapter`, the legacy policy-bound firmware
invocation path) was **not tested at all** (rows A5, A40, R1–R8). This is a genuine coverage gap,
not a finding that it works.

MCP-server integration was originally scoped out (rows A41, S1–S3) — but note §D above: Claude
Code + Ollama was subsequently shown to complete a real `--mcp-config` round-trip live in 3.D, so
the "unknown whether Claude+Ollama can do MCP" question is answered **yes** for the stdio path.
(Codex+Ollama still can't do MCP, so it remains excluded from that portion by construction.)

---

## Reference: launching Claude Code against an Ollama backend

Requires Ollama v0.14.0+ (native Anthropic Messages API) with a model pulled. Two working paths:

**(a) Environment redirect + the adapter's own argv** (fix #1 patched so `--verbose` is present):

```
ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
  claude --print --output-format stream-json --verbose --model deepseek-v4-flash:0731-cloud \
  --permission-mode bypassPermissions
```
- `ANTHROPIC_BASE_URL` redirects every request to the local Ollama server.
- `ANTHROPIC_AUTH_TOKEN` = any non-empty value (Ollama doesn't check it); leave `ANTHROPIC_API_KEY`
  empty so the CLI doesn't validate a real key.
- With fix #3 in place, the harness now sets these from `config_overrides:
  ["model_provider=\"ollama\""]` via the `env_overrides` child-env channel; on unpatched
  `Firmware/target-harness` you must still set them as process-level env vars before launch.

**(b) The `ollama launch` helper:**
```
ollama launch claude --model deepseek-v4-flash:0731-cloud -- --dangerously-skip-permissions
```

Both work; use whichever fits the launcher wiring.

**Why fixing against Ollama transfers to real Claude:** all four §A defects lived in argv
construction + stream-json parsing (`ClaudeCodeProviderAdapter` in `provider.py`) and the
per-provider allow-list (`invocation.py: _provider()`). Neither layer inspects which model
answered — they build a command line and parse the CLI's own output envelope, which is identical
whether the CLI talks to Anthropic or to an Anthropic-Messages-API-compatible Ollama endpoint. The
one caveat (§C/§D): a backend weaker/quirkier than real Claude can produce non-standard tool-call
or permission-request shapes that trip a *content-dependent* row real Claude wouldn't — orthogonal
to the four CLI-mechanic fixes, but worth watching in any model-output-dependent row.

---

## Historical note — the U15 `CANCELLED` observation (still not a failure)

Claude's `parse_transcript_line` never produces a `CANCELLED` provider event (only
`STARTED`/`COMPLETED`/`FAILED`), unlike Codex's explicit `turn.cancelled` handling. The only
consumer (`lane_controller.py`) treats `FAILED` and `CANCELLED` identically, so this has no
observed functional effect for Claude lanes — it only reduces the precision of a human reading raw
evidence after the fact. Recorded (inventory U15, NOTED), not counted as a failure.
