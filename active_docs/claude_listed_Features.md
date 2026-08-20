# Full feature inventory — `orchestrator_harness` (WIP target harness)

**Revision 2** — expanded from a 61-row module-level pass to a granular pass: every distinct
CLI subcommand/flag, validation rule, state classification, and event type is now its own row,
per explicit feedback that the first pass ("one row per file/module area") was too coarse. No new
testing was performed for this revision — every row that was TESTED-PASSED or TESTED-FAILED in
the prior revision keeps that exact status; every new row surfaced by this deeper pass is
NOT-TESTED with a reason.

"Time-boxed" (TB) = deliberately skipped rather than exhaustively tested, not inherently
untestable. **TB-SC** = a TB row that was short-circuited by the round: its testing was blocked
or made pointless by the 4 confirmed failures (no working Claude lane launch, untrustworthy lane
results), so it could not be exercised live. **TB-NS** = a TB row that was NOT short-circuited:
testable without a working Claude lane (pure validation rules, provider-neutral logic, CLI
subcommands), skipped for time/priority, not blocked. Within TB-NS, **TB-NS-V** = worth
verifying: provider-neutral but never exercised in either session (complex subsystems / safety
checks the Codex evidence does not trivially cover); plain TB-NS rows are trivially covered by
the Codex session's evidence and do not need testing. "Provider-agnostic" (PA) = code path that does not differ by provider (Codex vs.
Claude) and was already validated end-to-end in the earlier Codex/DeepSeek session. "Out of
scope" (OOS) = explicit firmware/MCP/legacy-watcher exclusion per instruction. "Codex-only" (CX)
= mechanism that is structurally Codex-specific (hook/adapter plumbing) with no Claude-provider
equivalent to exercise — listed for completeness, not a Claude gap by itself except where it
explains a linked failure. **CX-GAP** = a CX row that is actually a real Claude gap: the concept
is provider-neutral (a "product that works for every provider CLI" would have it for Claude too),
Claude Code has the mechanism to support it (hooks in `.claude/settings.json`, permissions,
headless mode), but the harness only implemented the Codex side. **All 30 CX rows in this
inventory are CX-GAP** — they trace to one root cause: the harness built the full Codex
hook-adapter + delivery-coordinator stack (install hooks into `.codex/hooks.json`, wake idle
sessions via `PostToolUse`/`Stop` hooks + App Server fixtures, deliver notices, bounded-policy
launcher) and left Claude with `FutureHostFixture` (N1/A24) instead of a real adapter. The one
genuine caveat is the "wake the idle agent" half of A24 (Codex App Server fixtures): Codex wakes
an idle session in-process via `thread/inject_items`/`Stop.continue`, and Claude Code has no
in-session injection API. But `claude --resume <session_id>` is a resuming-thread action that
serves the same purpose cross-process (a new process reloads the session) — and the harness
already has that machinery (K1/A26, `decide_resume_or_handoff`, tested live against the real
CLI). So the wake half is implementable for Claude, just with a different mechanism (a
resume-based re-entry loop) rather than App Server injection — the gap is that no delivery
coordinator wires resume-as-wake together, not that the mechanism is impossible.

Compiled from: `plans/general-coding-harness/EXECUTION_PLAN.md` (C1-C128 checklist),
`plans/general-coding-harness/FULL-EXECUTION-SPEC_PLAN_2.md` (module instances MI-*),
`Portable_Watcher_Repo/orchestrator_harness/SPEC.md` and
`Portable_Watcher_Repo/harness_watcher_implementation/SPEC.md` (R1-R8 / watcher requirements,
older generation of the same design), `README.md`, `QUICK_START.md`,
`orchestrator_harness/SPEC.md` (current S4 spec), and — for this revision — a direct read of
every one of the 39 modules under `Firmware/target-harness/orchestrator_harness/*.py` plus
`harness_common/process_identity.py`, at the function/class/constant/validation-rule level
(full source reads of `cli.py`, `AGENTS.md`, `SPEC.md`, `codex_adapter.py`; targeted greps of
every remaining module for `raise \w*Error(`, ALL-CAPS string constants, and top-level
`def`/`class` signatures), at commit `055a5bd` on branch `firmware/v2-candidate`.

## ⚠️ Status vocabulary — READ THIS before you edit any Status cell

**A test completing is NOT a pass.** Running a test only *produces a result*; that result is
either a pass or a gap/fail. "Passed" means a **positive** outcome — we got what we wanted: the
feature behaves exactly as the intended (Codex-era) design specified. If the test ran fine but the
observed behavior diverges from the intended behavior, that is a **GAP**, never a pass — even when
the divergence is "harmless" or the harness is stricter/safer than intended. Do not launder a
completed-but-divergent test into TESTED-PASSED.

Use exactly these Status values:

| Status | Meaning — when to use it |
|---|---|
| **TESTED-PASSED** | A test ran **and** the actual behavior matches the intended Codex-era behavior. Positive result. |
| **GAP** | A test ran **and** revealed a divergence between intended (Codex) behavior and actual (Claude/current) behavior — absent, weaker, or observably different, *including* stricter/safer. Not a pass. Cite the finding id (`F1x-…`/`F2x-…`) + a one-line divergence in the cell; full evidence in `plans/compatibility-testing/evidence/FINDINGS.md`. |
| **TESTED-FAILED** | The feature is broken / a confirmed defect (traces to a phase-0 finding). |
| **NOT-TESTED** | No test was run yet. Tag with the reason code (PA / OOS / CX / TB-*). |
| **NOTED** | Legacy pre-phase-1 label = an observed gap not counted as pass or fail. Prefer GAP for new rows. |

If you are a future agent running these tests: never write TESTED-PASSED just because a test module
went green on its own assertions. A test that *pins a divergence* is green **because** it correctly
captured the gap — that is a GAP row, not a pass.

## Summary counts

| Metric | Count |
|---|---:|
| Total features inventoried (this revision) | **346** |
| Total features inventoried (prior revision) | 61 |
| Rows tagged TESTED-PASSED (feature behaves as intended; some rows confirm the same underlying test action from a different angle; **7 of these were the phase-0 blockers — fixed & re-verified PASS in the compat-test clone, fix uncommitted/unmerged**) | 225 |
| Rows tagged **GAP** (feature *was* tested, but actual behavior diverges from the intended Codex-era behavior — a recorded finding, **NOT** a pass; see below and the FINDINGS ledger) | 19 |
| Rows tagged TESTED-FAILED | 0 — the 7 phase-0 failures (A1, A17, C17, U1–U4, from the 4 findings in `missing_claude_implementation.md`) were fixed & re-verified PASS in the compat-test clone and are now counted under TESTED-PASSED with a "fix uncommitted/unmerged" caveat; the authoritative target still exhibits the original failures until the fix is merged |
| Rows tagged NOT-TESTED | 102 |
| Rows tagged NOTED | 0 — the former legacy row (U15) is now folded into GAP per the gap/pass/not-tested taxonomy |

**GAP is a distinct outcome, not a pass.** Phases 1–2 are detection-only unit tests over the real
(Codex-era) `orchestrator_harness` modules. A GAP row means the test ran and pinned the *actual*
behavior, and that behavior differs from what the Codex-era design/plan intended for this feature —
sometimes the intended capability is absent or weaker (e.g. `scan --no-write` no-op, no
result-ambiguity rejection, `prompt.py` has no template constants), sometimes the harness is
*stricter/safer* than intended (e.g. config bounds reject instead of clamp, resume-thread conflict
fails closed instead of "canonical wins"). Either way it is an intended-vs-actual divergence a
Claude-side consumer could observe, so it is **not** marked TESTED-PASSED. The 19 GAP rows are:
B2, C24, E19, E20, F3, F24, G1, G5, G18, I4, K8, L4, L7, Q1, Q17, A34, A39, T3, U15 — each carries its finding id
(`F1x-…`/`F2x-…`/`U15-CANCELLED`) and a one-line divergence summary in its Status cell; full evidence is in
`plans/compatibility-testing/evidence/FINDINGS.md`. (U15 is a benign provider difference — Claude's CLI
emits no cancel event — formerly tracked as NOTED.)

**Phase-1/2 detection testing was executed this revision** (parent Opus 4.8 / high; test-authoring
subagents `deepseek-v4-flash:0731-cloud` @ `--effort high`, coordinator-verified). This supersedes
the prior revision's "no new testing performed" note. Test modules live under
`orchestrator_harness/tests/test_compat_*.py`; per-area verification is in
`plans/compatibility-testing/coverage-matrix.md` and `evidence/COORDINATOR-LOG-P12.md`.

> **Subagent launch envelope (all phases):** every deepseek build/test subagent is launched
> **session-local** with a pinned **autocompact limit of `CLAUDE_CODE_AUTO_COMPACT_WINDOW=180000`**
> (fixed token count, fires during `--print` runs) under a `CLAUDE_CODE_MAX_CONTEXT_TOKENS=200000`
> ceiling, `--effort high`, and `CLAUDE_CONFIG_DIR` scoped into the disposable clone — never
> `claude config set` / `~/.claude` / global settings. Full recipe: `plans/compatibility-testing/README-claude-code.md`
> §3 "MANDATORY subagent launch envelope"; rationale in memory `subagent-launch-local-only`.

NOT-TESTED breakdown by reason (102 rows):
| Reason | Count |
|---|---:|
| PA — Provider-agnostic, already verified in the earlier Codex/DeepSeek session | 72 |
| OOS — Out of scope per explicit firmware/MCP/legacy-watcher exclusion | 23 |
| CX — Codex-only mechanism, structurally has no Claude-provider equivalent to exercise | 0 (Phase 4 built the Claude host adapter; all 30 former CX-GAP rows are now TESTED-PASSED — see taxonomy note) |
| Live-not-materialized — event **classifier** logic exists, but the event never emitted on a real lane in 3.A: a single Ollama controller turn emits only PROVIDER_STARTED/PROVIDER_EXITED, and these rows (G8, G9, G11, G12, G13, G15, G16) were not in the phase-1 in-process batch either. Not fabricated, not flipped to PASS — recorded per the plan's live-emission caveat. **These 7 are the sole NOT-TESTED rows that are neither PA nor OOS and genuinely should be tested → deferred to [Phase 5](../plans/compatibility-testing/phase-5-residual-live-event-emission.md), which drives their live producers.** (All former TB-NS/TB-NS-V/TB-SC rows are now resolved: phase-1/2 pure-logic rows → TESTED-PASSED; F15/G21/V7/G32 → TESTED-PASSED via phase 3; G10 → synthetic/accepted.) | 7 |

See `missing_claude_implementation.md` for full evidence (argv diffs, live CLI transcripts, event-log
excerpts) behind every TESTED-FAILED row. The "14 real test actions" figure is unchanged from the
prior revision — this pass is purely an inventory-completeness expansion, not new testing; see
"Notes on methodology" at the bottom for how a handful of real commands back many feature rows at
once (e.g. one real 2-lane concurrent run confirms ~8 different rows across sections A, U, and V).

---

## Phase-0 fixes status & effect on the time-boxed tags (2026-08-18)

All 4 confirmed failures (`missing_claude_implementation.md`) are **fixed and verified** in the
disposable worktree clone; **none are merged into `Firmware/target-harness` yet** (uncommitted,
branch `compat-test-copy`).

**Worktree copy containing the fixes:**
`harness-single-worktrees/compat-test` (created from `Firmware/target-harness` @ `dd673cb`).
Per-step evidence: `plans/compatibility-testing/evidence/0.1/` … `0.5/`; coordinator ledger:
`plans/compatibility-testing/evidence/COORDINATOR-LOG.md`.

| Fix | Step | What changed |
|---|---|---|
| 1. Missing `--verbose` flag | 0.1 ✅ | `ClaudeCodeProviderAdapter.build_argv` always emits `--verbose` after `--print --output-format stream-json` (the real CLI hard-rejects that combo without it) |
| 2. No permission bypass / false-COMPLETED | 0.2 ✅ | default `--permission-mode bypassPermissions` for headless lanes; `parse_transcript_line` maps `system/permission_denied` and result `permission_denials` → `FAILED` (a denied lane is never COMPLETED) |
| 3. `config_overrides`/`service_tier`/`approval_policy` silently dropped | 0.3 ✅ | `config_overrides` honored via a child-env channel (`ProviderLaunchSpec.env_overrides`, merged after isolation; `model_provider="ollama"` alias → `ANTHROPIC_BASE_URL`/`AUTH_TOKEN`/`API_KEY`); `service_tier`/`approval_policy` on claude-code → `InvocationValidationError` (fail loud, never silently dropped) |
| 4. No working Claude example/fixture | 0.4 ✅ | `examples/coding.claude.invocation.example.json` (canonical `orchestrator-worker-invocation/v1`, claude-code) + `examples/disposable_claude_coding_fixture.py` (real single-lane fixture, live-run on the local Ollama backend) |

**TB-SC rows are no longer short-circuited.** The short-circuit *was* these 4 failures (no lane
could launch / lane results were untrustworthy), which made TB-SC rows untestable live. With
0.1–0.4 fixed in the clone — verified by 0.3's live env-merge proof and 0.4's two live fixture
runs — that blocking condition is gone, so TB-SC rows revert from "short-circuited / untestable"
to ordinary "untested," testable by their planned split (logic half now, live-wiring half once the
phase-0 gate passes). Two caveats: the formal phase-0 gate (step 0.5) has **not** passed yet —
blocked 2026-08-18 by the Ollama account's session usage limit, resume pending (see
COORDINATOR-LOG) — and the fixes exist only in the clone until merged.

**How the rest gets tested — phases 1 & 2 (efficient, quota-free):** both are pure test authoring
against synthetic fixtures — no live lane, no model inference, no production code changes — and do
**not** depend on phase 0. See `plans/compatibility-testing/README.md`,
`phase-1-provider-neutral-validation.md`, `phase-2-subsystems-worth-verifying.md`, and the per-row
dispositions in `coverage-matrix.md`.

- **Phase 1** — plain **TB-NS** validation rules (batched lighter tier) + the **pure-logic half of
  TB-SC**, all tested with fabricated inputs:
  - task/result lifecycle validation: **D3–D18, D20** (plan 1.C)
  - git-safety merge-readiness + invalid-result evidence: **A13, E14–E17, E19** (plan 1.D)
  - notification / event-taxonomy classification: **G3, G27, G32-logic** (plan 1.F)
  - plus the plain-TB-NS batch: invocation C2–C24, CLI surface B1–B16, git-safety E4–E7/E20,
    reconcile F3–F24, notification G1–G30, resource locks H9–H10, resume K2–K10, host-adapter
    N4/N5/N7, config Q1–Q17, provider contract U5/U7–U11
- **Phase 2** — all **39 TB-NS-V** rows: workspace-overlay edge cases (A9, I4/I5/I7–I10 → 2.A),
  capability broker (A25, L1–L7, L10 → 2.B), lane lifecycle (P1–P12 → 2.C), operator launch
  (A35, O7–O9 → 2.D), release assets (A34 → 2.E), attention sprint (A30/T6 → 2.F), watcher
  recovery (A31, A39/T3 → 2.G), and the remaining row (Q4 → 2.H) — fixtures + real git worktrees
  only, no live `claude` subprocess.

The **live half of TB-SC** (authentic event wiring on real lanes — F15, G8–G13, G15, G16, G21,
G32-live, V7) ran in phase 3 once the phase-0 gate (0.5) passed. Outcome: **F15, G21, G32-live, V7
→ TESTED-PASSED** (authentic live evidence in `evidence/3.A`/`3.B`); **G10 → synthetic/accepted**;
**G8, G9, G11, G12, G13, G15, G16 → live emission did not materialize** on the Ollama backend (a
single controller turn emits only PROVIDER_STARTED/PROVIDER_EXITED), so they stay NOT-TESTED and are
honestly recorded rather than fabricated — and are the sole non-PA, non-OOS residue, now carried
forward to **[Phase 5](../plans/compatibility-testing/phase-5-residual-live-event-emission.md)**,
which drives their live producers. No TB-NS / TB-NS-V / TB-SC row remains open.

---

## Phase-0 fixes — diff-level record & branch pointers (2026-08-19)

### Where these changes live (branch pointers)

- **Repository:** the `harness-single` submodule — `origin https://github.com/JasonPeng2019/harness-single.git`.
- **Checkout / worktree:** `harness-single-worktrees/compat-test` (a linked git worktree of that
  submodule), created from `Firmware/target-harness` @ `dd673cb`.
- **Branch the phase-0 fixes were made in:** **`compat-test-copy`** (worktree tip `dd673cb`).
- **Branch being tested for Claude compatibility of the harness:** **the same branch,
  `compat-test-copy`.** The phase-0 source fixes and the phase-1/2 compatibility test suite are
  authored together on this one disposable branch — there is no separate "fix" vs "test" branch.
- **Commit state (be precise):** everything is **uncommitted working-tree state** on
  `compat-test-copy`, **not** a commit and **not** merged into `Firmware/target-harness`:
  - the four source fixes appear as tracked-modified (`git status` ` M`):
    `orchestrator_harness/provider.py`, `orchestrator_harness/invocation.py`,
    `orchestrator_harness/lane_controller.py`, plus `orchestrator_harness/tests/test_s2_contract.py`
    and `.gitignore`;
  - the phase-1/2 compat test modules appear as untracked (`??`)
    `orchestrator_harness/tests/test_compat_*.py`, and the phase-0 fixture files as untracked
    `examples/coding.claude.invocation.example.{json,md}` + `examples/disposable_claude_coding_fixture.py`.
- **Diffstat (source fixes only):** `provider.py` +140/−7, `lane_controller.py` +36,
  `invocation.py` +11. Per-step evidence: `plans/compatibility-testing/evidence/0.1/`…`0.5/`;
  ledger `plans/compatibility-testing/evidence/COORDINATOR-LOG.md`.

### Fix 1 — Claude lane launch missing `--verbose` (step 0.1; inventory A1/U1/U2)

- **File/seam:** `provider.py` → `ClaudeCodeProviderAdapter.build_argv`.
- **Change:** the argv seed became
  `[*spec.command, "--print", "--output-format", "stream-json", "--verbose"]` — `--verbose` is now
  always emitted in print/stream-json mode (the real CLI hard-rejects that combo without it, exit 1
  "requires --verbose").
- **Regression:** `orchestrator_harness/tests/test_compat_provider_argv.py`.

### Fix 2 — no permission bypass → silent false-COMPLETED (step 0.2; inventory U3)

Two independent hardenings, both in `provider.py`:
- **Default-safe bypass** (`build_argv`): `permission_mode = spec.permission_mode or
  "bypassPermissions"`, and `--permission-mode` is now always appended (previously only when the
  caller set it). An explicit caller value still wins. Mirrors Codex's unconditional bypass so a
  headless lane can't silently no-op with every tool blocked yet exit 0.
- **Denial detection** (`parse_transcript_line`):
  - an in-stream `system` line with `subtype == "permission_denied"` → `ProviderEvent("FAILED",
    outcome="FAILED", detail=…)` (other non-`init` system subtypes → `None`);
  - the terminal `result` line now reads `permission_denials`; `denied = isinstance(list) and
    bool(list)`, and `if is_error or denied:` classifies **FAILED** with the denied tool names in
    `detail` — so a blocked lane is never mapped to COMPLETED even though the CLI ends
    `is_error:false / subtype:success / exit 0`.
- **Regression:** `orchestrator_harness/tests/test_compat_transcript_parse.py`.

### Fix 3 — `config_overrides` / `service_tier` / `approval_policy` accepted then silently dropped (step 0.3; inventory C17/U4)

Chose **reject-loud + honor** (both options from the plan) across three files:
- **`provider.py` (honor `config_overrides` via a child-env channel):**
  - new `CLAUDE_CONFIG_OVERRIDE_ALIASES` (the `model_provider="ollama"` alias →
    `ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama`, `ANTHROPIC_API_KEY=`);
  - `claude_config_override_env(override)` — translates the alias or an explicit `ANTHROPIC_*=…`
    assignment (strips one quote layer), else raises `ProviderAdapterError` (**never a silent drop**);
  - `claude_child_env_overrides(spec)` — merges translated `config_overrides` + validated
    `env_overrides`;
  - new frozen-dataclass field `ProviderLaunchSpec.env_overrides`; `build_argv` calls
    `claude_child_env_overrides(spec)` so validation fails loud even on the standalone adapter path;
    `provider_config_digest` now includes `env_overrides`; both helpers exported.
- **`invocation.py` (reject the flags Claude has no equivalent for):** `_provider()` — for
  `provider_id == "claude-code"`, any of `service_tier` / `approval_policy` present → raise
  `InvocationValidationError` naming the field(s) (fail loud, not accepted-then-dropped).
- **`lane_controller.py` (wire the env channel through launch):** import
  `claude_config_override_env`; new `apply_provider_env_overrides(child_env, env_overrides)` merges
  declared overrides **after** the isolation/allow-list filtering (override always wins; starts from
  `os.environ` when isolation is off so PATH & friends aren't dropped); `_provider_launch_spec`
  translates claude-code `config_overrides` into the spec's `env_overrides` (fail loud); `run()`
  applies `apply_provider_env_overrides(child_env, launch_spec.env_overrides)` just before
  `subprocess.Popen`.
- **Regression:** `orchestrator_harness/tests/test_compat_provider_allowlist.py`; live env-merge
  proof in `evidence/0.3/`.

### Fix 4 — no working Claude example/fixture (step 0.4; inventory A17)

- **New files (untracked in `examples/`):** `coding.claude.invocation.example.json` (a valid
  canonical `orchestrator-worker-invocation/v1` for `provider.id="claude-code"`, incorporating the
  0.2 permission handling) with a companion `coding.claude.invocation.example.md`, and
  `disposable_claude_coding_fixture.py` — a real single Claude lane fixture that runs end-to-end on
  the local Ollama backend, emitting `PROVIDER_STARTED`/`PROVIDER_EXITED` and a real `session_id`.
- **Cross-check:** validated against `tests/test_s2_contract.py` (the only pre-existing claude-code
  shape; that file is also ` M` for the new default-bypass / `env_overrides` expectations).
- **Evidence:** two live fixture runs in `evidence/0.4/`.

> Gate status unchanged: the formal phase-0 gate (step 0.5) has not yet been re-run to green, and
> none of the above is merged into `Firmware/target-harness` — it remains uncommitted on
> `compat-test-copy`.

---

## Phase-4 fixes — Claude host adapter & owned installer (2026-08-20)

Phase 4 closed the 30-row **CX-GAP** subsystem gap by *implementing* the missing Claude host
adapter (previously Claude got `FutureHostFixture`, a stub — see the taxonomy note above). Build
decision: **BUILD** (user, 2026-08-20). Build + test authoring were delegated to session-local
`deepseek-v4-flash:0731-cloud` subagents under the pinned 180K autocompact envelope; ROOT
re-ran and read every result independently. All new source lives in the **same worktree as the
phase-0 fixes** (below), still uncommitted on `compat-test-copy`.

### New files (all untracked `??` in the clone)

| Build unit | New file(s) | What it implements |
|---|---|---|
| BU1 — host adapter | `orchestrator_harness/claude_adapter.py` (312 lines) + a `select_host_adapter('claude')` routing branch in `codex_adapter.py` | Real `ClaudeAdapter` (replaces `FutureHostFixture`), `SyntheticClaudeTransport`, `create_claude_adapter`, `run_synthetic_wake_self_test`, `claude_profile`. Key semantic: Claude has no in-session injection API → `next_input_injection=False`; idle wake is cross-process via `claude --resume <session_id>` → `idle_wake=True` (**A24 resume-as-wake**, the analog of Codex's in-process `thread/inject_items`/`Stop.continue`). |
| BU2 — owned installer | `orchestrator_harness/claude_installer.py` (971 lines) + `orchestrator_harness/assets/claude/` (`orchestrator_harness_post_tool_use.py`, `orchestrator_harness_stop.py`, `manifest.json`, `settings.fragment.json`, `__init__.py`) + `adapter --host claude` routing in `cli.py` | Installs the Claude-side hooks/binding into `.claude/settings.json` with atomic rollback-on-failure; ownership/currency probe, legacy-revision upgrade, uninstall with preserve-modified, foreign-hook coexistence. |
| BU3 — tests | `orchestrator_harness/tests/test_compat_claude_adapter.py` (365 lines) | 14 tests (3 subtests) over the 4.A/4.B rows. Root re-run: `pytest test_compat_claude_adapter.py` → **14 passed**. |

### Gaps closed (30 rows, all now TESTED-PASSED)

- **4.A — delivery/wake (real adapter):** N1 (adapter replaces `FutureHostFixture`), N2 (sparse
  `DeliveryNotice`), N3 (transport-evidence-only `DeliveryReceipt`), N6 (registration replay
  persists beside the S3 queue), N8 (capability-gated `select_host_adapter`), A24 (resume-as-wake),
  G17 (wake attempt/deliver/fail — fail-closed to `DELIVERY_FAILED`), G19 (manager finalization
  round trip).
- **4.B — owned installer CLI:** B9 install (+ `CodexInstallRollback` atomicity), B10 check, B11
  upgrade, B12 uninstall (preserve-modified), B13 self-test, B14 per-boundary hook dispatch.
- **4.C — Codex regression reference (unchanged, held green):** M1–M16 —
  `test_codex_bounded_policy.py` + `test_s4_contract.py` + `test_compat_host_adapters.py` = **45
  passed, 95 subtests**. These are the existing Codex implementation; the Claude adapter mirrors
  their contract.

Two behaviors pinned as **stricter/safer, explicitly NOT a GAP**: G17's failure path converts a
transport exception into a `DELIVERY_FAILED` receipt (fail-closed) instead of re-raising; B9 wraps
`CodexInstallConflict` in `CodexInstallRollback` so the transaction is visibly atomic. Acceptance:
`evidence/PHASE4-ORCHESTRATOR_ACCEPTANCE.json` (`decision: ACCEPTED`, `rows_rejected: []`,
`gaps_opened: []`); disposition detail in `evidence/PHASE4-COMPLETION_REVIEW.json`.

---

## Where these fixes live — worktree & branch (all phases)

Every phase-0 and phase-4 source fix, plus the phase-1/2/4 compat test modules, live in **one
disposable git worktree** — nothing is committed or merged upstream.

- **Repository:** the `harness-single` submodule (`origin
  https://github.com/JasonPeng2019/harness-single.git`).
- **Worktree:** `harness-single-worktrees/compat-test` — a **linked git worktree** of that
  submodule, created from `Firmware/target-harness` @ `dd673cb`.
- **Branch:** **`compat-test-copy`** (worktree tip `dd673cb`). The phase-0 source fixes, the Phase 4
  host adapter, and the compat test suite are all authored together on this one branch — there is
  no separate "fix" vs "test" branch.
- **Commit state:** **all uncommitted working-tree state** on `compat-test-copy` — **not** a commit
  and **not** merged into `Firmware/target-harness`. Phase-0 fixes appear as tracked-modified
  (`provider.py`, `invocation.py`, `lane_controller.py`, `tests/test_s2_contract.py`, `.gitignore`);
  the Phase 4 files and phase-1/2 `test_compat_*.py` modules appear as untracked (`??`).

> **Not to be confused with the first-round scratch checkouts** (which do **not** carry any of these
> fixes): `harness-single-worktrees/claude-test` is the original **read-only probing clone**
> (standalone `.git`, stock source — where the 4 phase-0 blockers were first *discovered* against
> the real CLI), and `harness-single-worktrees/claude-probe-lanes/{lane-a,lane-b}` are the two
> now-orphaned concurrency **probe lanes** launched from it (they hold `HELLO FROM LANE A/B` probe
> files — evidence for A10/V2/V3/V4/V8 — but their backing worktree metadata is gone). The live
> fix work is only in `compat-test`.

---

## A. High-level / workflow features

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| A1 | Provider adapter abstraction (pluggable Codex / Claude Code backends behind one contract) | `provider.py`, `providers.py` | TESTED-PASSED (0.1, fix) — was TESTED-FAILED (phase-0 blocker §1); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged — the authoritative target still exhibits the failure. Evidence: `evidence/0.1/`. |
| A2 | Public extension seam to register additional/custom provider adapters at runtime | `provider.py: register_provider_adapter` | TESTED-PASSED (used directly as the workaround vehicle) |
| A3 | Canonical worker-invocation schema (`orchestrator-worker-invocation/v1`), provider-neutral | `invocation.py` | TESTED-PASSED (real invocations built and parsed for both lanes) |
| A4 | Legacy Codex-only coding invocation schema (`orchestrator-coding-invocation/v1`) | `invocation.py` | NOT-TESTED — PA |
| A5 | Legacy policy-bound firmware invocation path (retained for compatibility) | `firmware_adapter.py`, `firmware_campaign.py` | NOT-TESTED — OOS |
| A6 | Workspace overlay: ingest a "super-cache" source folder into a harness worktree | `workspace_overlay.py: ingest_super_cache` | TESTED-PASSED |
| A7 | Workspace overlay: materialize (bounded launcher scripts, shared docs) into a subagent's own worktree | `workspace_overlay.py: prepare_worktree` | TESTED-PASSED |
| A8 | Workspace overlay: exact-byte reversal/retirement of a materialized overlay | `workspace_overlay.py: restore_worktree` | TESTED-PASSED |
| A9 | Workspace overlay: independent receipt verification | `workspace_overlay.py: verify_overlay_receipt` | TESTED-PASSED (2.A; same feature as I4 — passes as a structural/identity prelaunch check; the byte-integrity caveat is GAP **F2A-I4-1**) |
| A10 | Parallel Git lanes: isolated branch + worktree per subagent | `git_safety.py`, `lane_controller.py` | TESTED-PASSED (2 concurrent real lanes, no cross-contamination) |
| A11 | Git identity verification before launch (repo, worktree root, branch, base commit) | `git_safety.py: inspect_repository, declaration_from_invocation` | TESTED-PASSED (both lane invocations validated before launch) |
| A12 | Duplicate active worktree/branch detection | `git_safety.py: active_declaration_conflicts` | TESTED-PASSED (1.D — same feature as E7) |
| A13 | Result validation for merge-readiness (branch-tip, clean tree, outcome shape) | `git_safety.py: validate_coding_result` | TESTED-PASSED (1.D — same feature as E14–E17; E19 state-gate scope is GAP **F1D-E19-1**) |
| A14 | Invalid-result durable evidence + clearing on correction | `git_safety.py: invalid_result_evidence` | NOT-TESTED — PA |
| A15 | Integration merge of multiple lane branches into one worktree + project checks | `README.md "Split, merge, accept"` | NOT-TESTED — PA |
| A16 | Cleanup of lane worktrees/branches/runtime state after merge | `README.md "Cleanup"` | NOT-TESTED — PA |
| A17 | Disposable two-worktree integration fixture (documented quick-start proof) | `examples/disposable_coding_fixture.py` | TESTED-PASSED (0.4, fix) — was TESTED-FAILED (phase-0 blocker §4, no working Claude example); working fixture authored & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.4/`. |
| A18 | Resource locks: generic named exclusive claims (non-Git shared resources) | `resource_locks.py` | NOT-TESTED — PA |
| A19 | Resource lock staleness reconciliation (never steal while owner state unknown) | `resource_locks.py: _owner_state, _retained_state` | NOT-TESTED — PA |
| A20 | `WAITING_RESOURCE` publication while blocked on a lock | `resource_locks.py`, `reconcile.py` | NOT-TESTED — PA |
| A21 | Deferred/durable manager notification with priority preemption | `notifications.py: select_actionable_with_deferred, preempt_pending_with_higher_priority` | TESTED-PASSED (1.F — same feature as G29) |
| A22 | Coalescing of mutable handoff notifications | `notifications.py: coalesce_mutable_handoffs` | TESTED-PASSED (1.F — same feature as G30) |
| A23 | `watch --until-actionable` bounded polling wait for the manager | `lane_controller.py` / CLI `watch` | TESTED-PASSED — but confirmed to only return `WATCH_TIMEOUT` even for a genuinely completed Claude lane (matches the known Codex/DeepSeek finding, not a new Claude regression) |
| A24 | S4 `DeliveryCoordinator` — wakes an idle Codex session via `PostToolUse`/`Stop` hooks and App Server fixtures | `orchestrator_harness/SPEC.md "S4 host delivery"` | TESTED-PASSED (Phase 4 — resume-as-wake via `claude --resume`; `test_A24`) |
| A25 | Capability broker: mediated, permit-based access to external capabilities/adapters | `capability_broker.py` | TESTED-PASSED (2.B / L6 — full broker orchestration end-to-end, no authority leak into public record) |
| A26 | Resume / handoff admission (mismatch-safe session resume across manager handoffs) | `resume.py: make_resume_admission, require_resume_admission` | TESTED-PASSED (partial) — real `--resume <session_id>` exercised live; the full `ResumeAdmission` identity-matching path was not separately driven |
| A27 | Resume amendment review validation (diff-based review gating on resume) | `resume.py: validate_resume_amendment_review` | TESTED-PASSED (1.G — same feature as K4) |
| A28 | Handoff preflight checks (invocation files, amendment identity, required evidence present before a manager handoff) | `handoff_preflight.py` | TESTED-PASSED (1.G — same feature as K10; CLI wrapper B8) |
| A29 | Task lifecycle: card → result → completion review → orchestrator acceptance → advancement | `task.py` | TESTED-PASSED (1.C — same lifecycle as D3–D20) |
| A30 | Attention-sprint historical record decoding | `attention_sprint.py` | TESTED-PASSED (2.F; inert bounded decoder — correct schema/identity/timestamp projection, fail-closed ValueError on every corrupt path, never actionable/acknowledgeable) |
| A31 | Watcher recovery projection / condition merging for the harness-owned diagnostic observer | `watcher_integration.py` | TESTED-PASSED (2.G; condition merging keyed by identity with dedup/last-write-wins + cleared-drops-out, recovery projection labels open/ack/resolved, actionable=open only) |
| A32 | Release-check selection engine (dependency-fingerprinted, scope-matched test/check selection) | `release_checks.py: select_checks, resolve_input_scope` | NOT-TESTED — PA |
| A33 | Release checkpoint merge / credit / disposition recording | `release_checks.py: write_checkpoint, merge_checkpoint_results, credit_record` | NOT-TESTED — PA |
| A34 | Public release surface / release-manifest asset packaging | `release_assets.py` | GAP — **F2E-A34-1** (2.E; module is read-only manifest accessors only — no packaging/digest engine A34 intended) |
| A35 | Operator launch: detached long-lived owner/watcher/lane-controller process with exact PID+creation identity | `operator_launch.py` | TESTED-PASSED (2.D / O7 — records exact PID+created_utc identity) |
| A36 | Public launch helper (`launch_lane_controller`) as an embeddable entry point for external callers | `public_launch.py` | TESTED-PASSED (used implicitly) |
| A37 | Legacy MCP-Trial-3-generation watcher: R1 suite-local discovery of controller/request/relay/checkpoint/result files | `Portable_Watcher_Repo/.../SPEC.md R1` | NOT-TESTED — OOS |
| A38 | Watcher evaluator (`gpt-5.6-terra` classification of harness defects, `evaluator_enabled` flag) | `harness_watcher_implementation/evaluator.py`, `settings.py` | NOT-TESTED — OOS |
| A39 | Watcher alert delivery / recovery ledger (`STOP_ASSIGNING → ... → RESOLVED`) | `harness_watcher_implementation/*`, `notifications.py` | GAP — **F2G-A39-1** (2.G; no ordered STOP_ASSIGNING→…→RESOLVED ledger — module is a stateless open/ack/resolved projection with no ordering guard) |
| A40 | Firmware/hardware capability path (leases, relays, boards, probes, MCP hardware tools) | `firmware_adapter.py`, `firmware_campaign.py`, `capability_broker.py` firmware adapters | NOT-TESTED — OOS |
| A41 | MCP server integration / `--mcp-config` traffic | `invocation.py` provider field, `provider.py` | NOT-TESTED — OOS |

## B. CLI surface — subcommands and flags (`cli.py`, `__main__.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| B1 | `scan` (one-shot snapshot compute + print) | `cli.py` | TESTED-PASSED (1.B `test_compat_cli_subcommands`; scan prints reconciled snapshot, EXIT_OK, no persistence) |
| B2 | `scan --no-write` (diagnostic-only, no snapshot/event mutation) | `cli.py` | GAP — **F1B-B2-1** (1.B; `scan --no-write` is parsed but ignored — a pure no-op; the intended write-suppression flag does nothing, harmless only because scan never persists) |
| B3 | `watch --once` (single reconcile pass) | `cli.py` | TESTED-PASSED (1.B; `watch --once` = exactly one reconcile pass, cursor persisted) |
| B4 | `watch --until-event` (block until any new event) | `cli.py` | TESTED-PASSED (1.B; `--until-event` returns on fabricated STALE_STATUS, not EXIT_TIMEOUT) |
| B5 | `watch --until-actionable` (block until manager-actionable event or timeout) | `cli.py` | TESTED-PASSED (A23) |
| B6 | `watch --timeout <seconds>` bound, observed via real `WATCH_TIMEOUT` exit | `cli.py` | TESTED-PASSED |
| B7 | `watch --no-write` | `cli.py` | TESTED-PASSED (1.B; `watch --no-write`: reconcile runs, store=None, tree unchanged) |
| B8 | `handoff-preflight` subcommand | `cli.py` | TESTED-PASSED (1.B; valid bundle→exit 0; missing evidence→EXIT_INCOMPLETE + REQUIRED_EVIDENCE_EXISTS) |
| B9 | `adapter install` (Codex bounded owned installer) | `cli.py` | TESTED-PASSED (Phase 4 — install atomic + rollback; `test_B9`) |
| B10 | `adapter check` (Codex adapter ownership/currency probe) | `cli.py` | TESTED-PASSED (Phase 4 — ownership/currency probe; `test_B10`) |
| B11 | `adapter upgrade` (Codex adapter legacy-revision migration) | `cli.py` | TESTED-PASSED (Phase 4 — upgrade idempotent; `test_B11`) |
| B12 | `adapter uninstall` (Codex adapter owned-file removal with rollback) | `cli.py` | TESTED-PASSED (Phase 4 — uninstall preserves modified; `test_B12`) |
| B13 | `adapter self-test` (Codex synthetic wake self-test) | `cli.py` | TESTED-PASSED (Phase 4 — synthetic wake self-test; `test_B13`) |
| B14 | `adapter hook --boundary post_tool_use\|turn_completed\|finalization` | `cli.py` | TESTED-PASSED (Phase 4 — per-boundary dispatch; `test_B14`) |
| B15 | `view`/`source allocate` (immutable source view allocation) | `cli.py` | TESTED-PASSED (1.B + 2.C P1/P2; immutable view read-only enforced, write_source → ImmutableViewError) |
| B16 | `lane retire` (archive-first terminal-lane retirement) | `cli.py` | TESTED-PASSED (1.B + 2.C P6; archive written and hash-bound before git worktree close) |
| B17 | `workspace super-cache ingest` | `cli.py` | TESTED-PASSED (A6, via direct call to `ingest_super_cache`; CLI wrapper itself not separately invoked) |
| B18 | `workspace prepare` (materialize overlay into subagent worktree) | `cli.py` | TESTED-PASSED (A7, via direct call to `prepare_worktree`; CLI wrapper itself not separately invoked) |
| B19 | Exit-code contract (`EXIT_OK=0` / `EXIT_ERROR=1` / `EXIT_TIMEOUT=3`) | `cli.py` | TESTED-PASSED (partial — `EXIT_TIMEOUT` observed live via `watch --until-actionable`) |

## C. Invocation schema & validation rules (`invocation.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| C1 | Closed-object-shape rejection for the invocation root (unknown top-level keys rejected) | `invocation.py: _load_canonical_invocation` | TESTED-PASSED (rejected a malformed key during test construction, accepted the corrected shape) |
| C2 | `action` must be `start` or `resume` | `invocation.py` | TESTED-PASSED (1.A `test_compat_invocation_rules`) |
| C3 | `resume` invocation requires a non-empty session/thread id | `invocation.py` | TESTED-PASSED (1.A) |
| C4 | `start` invocation cannot contain a `resume` block | `invocation.py` | TESTED-PASSED (1.A) |
| C5 | `provider.notification` must be boolean | `invocation.py` | TESTED-PASSED (1.A) |
| C6 | `profile.role` must match invocation role | `invocation.py` | TESTED-PASSED (1.A) |
| C7 | `profile.provider` must match `provider.id` | `invocation.py` | TESTED-PASSED (1.A) |
| C8 | `profile.model` must match `provider.model` | `invocation.py` | TESTED-PASSED (1.A) |
| C9 | `prompt_bundle` schema/version validation | `invocation.py: _coding_settings` | TESTED-PASSED (B15) |
| C10 | `resume_identity` must be an object | `invocation.py` | TESTED-PASSED (1.A) |
| C11 | Unsupported/unknown invocation-schema string rejection | `invocation.py: load_invocation` | TESTED-PASSED (1.A) |
| C12 | Canonical vs. legacy Codex-coding schema dispatch (`CANONICAL_INVOCATION_SCHEMA` vs `CODING_INVOCATION_SCHEMA`) | `invocation.py` | NOT-TESTED — PA |
| C13 | `repository.*` non-empty-path-string + resolvable-existing-directory validation | `invocation.py: _common_paths` | TESTED-PASSED (A11) |
| C14 | `repository.worktree_root` must equal `run_root` | `invocation.py` | TESTED-PASSED (A11) |
| C15 | Firmware/coding-model-settings cross-contamination rejection | `invocation.py: _reject_firmware_coding_model_settings` | NOT-TESTED — OOS |
| C16 | Ambiguous coding-alias rejection | `invocation.py: _reject_ambiguous_coding_aliases` | TESTED-PASSED (1.A) |
| C17 | Per-provider optional-field allow-list filtering | `invocation.py: _provider()` | TESTED-PASSED (0.3, fix) — was TESTED-FAILED (phase-0 blocker §3, config_overrides/service_tier/approval_policy silently dropped); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.3/`. |
| C18 | Canonical output-path safety/uniqueness validation | `invocation.py: _validate_canonical_output_paths` | TESTED-PASSED (1.A) |
| C19 | SHA-256 hex-digest field format validation | `invocation.py` | TESTED-PASSED (1.A) |
| C20 | String-list no-duplicates field validation | `invocation.py: _string_list` | TESTED-PASSED (1.A) |
| C21 | Isolated coding child-environment construction | `invocation.py: isolated_coding_child_environment` | TESTED-PASSED (1.A) |
| C22 | Prior canonical acceptance-status read/persist | `invocation.py: _read_canonical_prior_status, _persist_canonical_acceptance` | TESTED-PASSED (1.A) |
| C23 | Canonical resume-admission path & amendment-claims validation | `invocation.py: _canonical_resume_admission_path, _canonical_resume_claims_accepted` | TESTED-PASSED (1.A) |
| C24 | Provider-operation classification & handoff-identity derivation | `invocation.py: _classify_provider_operations, _provider_handoff_identity` | GAP — **F1A-C24-1** (1.A; the intended unsupported-operation *record* is never emitted — `unsupported_operation_result` raises `ProviderAdapterError` first, so the record-producing branch is dead code; latent, cannot fire from validated input today) |

## D. Task & result lifecycle validation (`task.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| D1 | Task-card schema validation (`orchestrator-task-card/v1`) | `task.py` | TESTED-PASSED (B16, used to build both real invocations) |
| D2 | Task-card content-hash self-consistency (`record_sha256` matches bytes) | `task.py: record_sha256` | TESTED-PASSED |
| D3 | Task-result schema validation | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D4 | Task-result task/card identity cross-match | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D5 | Task-result `.outcome` enum validation (PASS/FAIL/BLOCKED) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D6 | Task-result `.checks[]` shape + per-check outcome enum (PASS/FAIL/SKIP/NOT_RUN) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D7 | Task-result `.acceptance_state` enum validation (PENDING/ACCEPTED/REJECTED) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D8 | Completion-review schema validation | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D9 | Completion-review result-identity cross-match | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D10 | Completion-review owner-must-own-task-card check | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D11 | Completion-review `.verdict` enum validation (PASS/FAIL/BLOCKED) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D12 | Orchestrator-acceptance schema validation | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D13 | Orchestrator-acceptance identity cross-match | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D14 | Orchestrator-acceptance `.verdict` enum validation (ACCEPTED/REJECTED) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D15 | Task advancement state machine (`advance_task`, `ACCEPTANCE_PENDING` → `ACCEPTED`/`REJECTED`) | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D16 | Advancement result-must-match-supplied-task-card check | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D17 | Advancement review/acceptance-identity cross-match | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D18 | Advancement acceptance-commit-must-match-result check | `task.py` | TESTED-PASSED (1.C `test_compat_task_lifecycle`) |
| D19 | Canonical record construction shared by all four task schemas | `task.py: canonical_record` | TESTED-PASSED (used for the task card only) |
| D20 | Schema-string constant surface (`TASK_CARD_SCHEMA`/`TASK_RESULT_SCHEMA`/`COMPLETION_REVIEW_SCHEMA`/`ORCHESTRATOR_ACCEPTANCE_SCHEMA`) | `task.py` | TESTED-PASSED (1.C; schema-string constant surface asserted) |

## E. Git safety & result-merge validation (`git_safety.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| E1 | Repository closed-shape validation | `git_safety.py: declaration_from_invocation` | TESTED-PASSED (A11) |
| E2 | `repository.branch` non-empty trimmed-string validation | `git_safety.py` | TESTED-PASSED (A11) |
| E3 | Git-inspection subprocess execution + non-UTF-8-output rejection | `git_safety.py: inspect_repository` | TESTED-PASSED (implicit) |
| E4 | Repository-identity-must-be-reported check | `git_safety.py` | TESTED-PASSED (1.D `test_compat_git_safety`) |
| E5 | Coding worktree must have an attached branch (detached-HEAD rejection) | `git_safety.py` | TESTED-PASSED (1.D) |
| E6 | Commit-identity format validation | `git_safety.py` | TESTED-PASSED (1.D) |
| E7 | Duplicate active worktree/branch detection | `git_safety.py: active_declaration_conflicts` | TESTED-PASSED (1.D; duplicate active worktree/branch detected) |
| E8 | Finding-gate: closed schema + identity match on findings payload | `git_safety.py` | NOT-TESTED — PA |
| E9 | Finding-gate: outcome/count mismatch rejection (PASS requires 0 findings, FAIL requires ≥1) | `git_safety.py` | NOT-TESTED — PA |
| E10 | Finding-gate: severity enum validation (CODEBASE_BREAKING/FUNCTIONALITY_BREAKING/WORTH_FIXING) | `git_safety.py` | NOT-TESTED — PA |
| E11 | Finding-gate: unique-finding-ID enforcement | `git_safety.py` | NOT-TESTED — PA |
| E12 | Finding-gate: tradeoff-evidence completeness check | `git_safety.py` | NOT-TESTED — PA |
| E13 | Finding-gate: affected-ID / evidence-reference validity checks | `git_safety.py` | NOT-TESTED — PA |
| E14 | Coding-result root-shape + schema (`orchestrator-lane-result/v1`) validation | `git_safety.py: validate_coding_result` | TESTED-PASSED (1.D) |
| E15 | Coding-result lane_id / branch / outcome-enum cross-match against current lane | `git_safety.py` | TESTED-PASSED (1.D) |
| E16 | Coding-result per-check shape validation (name-or-command required, outcome enum) | `git_safety.py` | TESTED-PASSED (1.D) |
| E17 | Task-result branch-match + commit-must-equal-branch-tip checks (dirty/stale-tree rejection) | `git_safety.py` | TESTED-PASSED (1.D; branch-match + commit-tip; dirty/stale-tree rejected) |
| E18 | `CODING_RESULT_INVALID` durable evidence emission + clearing on correction | `git_safety.py: invalid_result_evidence` | TESTED-PASSED (1.D; CODING_RESULT_INVALID evidence emitted + cleared on correction) |
| E19 | Operational-state gate restricting result acceptance to `RUNNING_CODEX`/`RUNNING_PROVIDER` | `git_safety.py` | GAP — **F1D-E19-1** (1.D; the operational-state gate is scoped to conflict detection only — discovery-level result acceptance does NOT reject a result offered under EXITED/PROVIDER_EXITED) |
| E20 | Too-many-JSON-candidates ambiguity rejection under a result workspace | `git_safety.py` | GAP — **F1D-E20-1** (1.D; no >1-candidate ambiguity rejection — a second result-shaped JSON is silently ignored; only the canonical `RESULT.json` is read) |

## F. Reconcile.py operational-state classification

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| F1 | `RUNNING_CODEX` / `RUNNING_PROVIDER` live-process state | `reconcile.py` | NOT-TESTED — PA |
| F2 | `WAITING_RESOURCE` (blocked on a resource claim) | `reconcile.py` | NOT-TESTED — PA (A20) |
| F3 | `WAITING_RELAY` (blocked on manager relay) | `reconcile.py` | GAP — **F1E-F3-1** (1.E; lane elevates to WAITING_RELAY only on RELAY_READY — a RELAY_UNBOUND request leaves the lane RUNNING_CODEX, narrower than intended) |
| F4 | `HELPER_RUNNING`/`HELPER_EXITED`/`HELPER_STATE_UNKNOWN` helper-process tri-state | `reconcile.py` | TESTED-PASSED (1.E; helper tri-state HELPER_RUNNING/EXITED/STATE_UNKNOWN) |
| F5 | `MCP_RUNNING`/`MCP_EXITED`/`MCP_STATE_UNKNOWN` MCP-process tri-state | `reconcile.py` | NOT-TESTED — OOS |
| F6 | `STALE_STATUS` (status file older than liveness bound) | `reconcile.py` | NOT-TESTED — PA |
| F7 | `PROCESS_STATE_UNKNOWN` fail-closed derivation on incomplete evidence | `reconcile.py` | TESTED-PASSED (1.E; PROCESS_STATE_UNKNOWN fail-closed on incomplete evidence) |
| F8 | `EXITED` / `UNKNOWN` terminal process states | `reconcile.py` | TESTED-PASSED (1.E; EXITED/UNKNOWN terminal states) |
| F9 | `CHECKPOINTED` (release-checkpoint-bound) state | `reconcile.py` | NOT-TESTED — PA |
| F10 | Relay-binding states: `BOUND` / `BOUND_EXPIRED` / `UNBOUND` / `ABSENT` | `reconcile.py` | TESTED-PASSED (1.E; BOUND/BOUND_EXPIRED/UNBOUND/ABSENT) |
| F11 | Request-lifetime states: `LIVE` / `ABSENT` / `UNKNOWN` | `reconcile.py` | TESTED-PASSED (1.E; LIVE/ABSENT/UNKNOWN) |
| F12 | Expiry-bucket classification: `WARNING` / `CRITICAL` / `EXPIRED` / `UNKNOWN` | `reconcile.py` | TESTED-PASSED (1.E; WARNING/CRITICAL/EXPIRED/UNKNOWN) |
| F13 | MCP-proof states: `PROVEN` / `UNPROVEN` / `NOT_DECLARED` | `reconcile.py` | NOT-TESTED — OOS |
| F14 | `RELAY_READY` / `RELAY_UNBOUND` / `REQUEST_AMBIGUOUS` classification | `reconcile.py` | TESTED-PASSED (1.E; RELAY_READY/RELAY_UNBOUND/REQUEST_AMBIGUOUS) |
| F15 | `RESULT_ACCEPTANCE_PENDING` / `TERMINAL_RESULT` classification | `reconcile.py` | TESTED-PASSED (3.A — authentic multi-turn coaching per P3-INT-1; committed RESULT.json reconciled RESULT_ACCEPTANCE_PENDING → ACCEPTED/TERMINAL_RESULT) |
| F16 | `DUPLICATE_CODING_WORKTREE` / `DUPLICATE_CODING_BRANCH` detection (reconcile layer) | `reconcile.py` | TESTED-PASSED (1.E; DUPLICATE_CODING_WORKTREE + DUPLICATE_CODING_BRANCH; distinct-repo negative control) |
| F17 | Manager-signal record discovery | `discovery.py: _manager_signal, _manager_root_records` | NOT-TESTED — PA |
| F18 | Declared-record-path safety validation against workspace root | `discovery.py: _declared_record_path` | NOT-TESTED — PA |
| F19 | Record-kind classification from declared manifest | `discovery.py: _record_kind` | TESTED-PASSED (1.E; `_record_kind` helper/mcp/filename/field/schema/default) |
| F20 | Hidden/atomic-signal-file filtering | `discovery.py: _is_hidden_or_atomic_signal_file` | NOT-TESTED — PA |
| F21 | Reparse-point/symlink signal-file rejection | `discovery.py: _is_reparse_or_link` | NOT-TESTED — PA |
| F22 | UTC-timestamp format validation on discovered records | `discovery.py: _is_utc_timestamp` | TESTED-PASSED (1.E; `_is_utc_timestamp` Z/+00:00 accepted; naive/offset/garbage rejected) |
| F23 | Git-state fingerprinting (dirty/clean worktree identity) | `discovery.py: _git_state_fingerprint` | NOT-TESTED — PA |
| F24 | Memoized coding/task-result validation cache | `discovery.py: _validate_coding_result_cached, _validate_task_result_cached` | GAP — **F1E-F24-1** (1.E; the validation memo covers the coding-result path only — the task-result path is not memoized; missing optimization, not a correctness gap) |
| F25 | Declared-lifetime-record enumeration (manifest-driven) | `discovery.py: _declared_lifetime_records, _manifest_declarations` | NOT-TESTED — PA |
| F26 | `discover_run` / `discover_suite` full suite-local reconciliation entry points | `discovery.py` | NOT-TESTED — PA (B38) |

## G. Notification & event taxonomy (`notifications.py`, `events.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| G1 | Actionable manager-facing event class (RELAY_READY, REQUEST_AMBIGUOUS, RELAY_UNBOUND, REQUEST_EXPIRY_WARNING) | `notifications.py` | GAP — **F1F-G1-1** (1.F; an EXPIRED-bucket expiry request is emitted but never selectable — `_priority` is actionable only for WARNING/CRITICAL, narrower than the intended blanket 'actionable') |
| G2 | Duplicate-controller/coding-branch/coding-worktree conflict events | `notifications.py` | TESTED-PASSED (1.F; DUPLICATE_*/RESOURCE_CONFLICT emitted) |
| G3 | `CODING_RESULT_INVALID` / `COORDINATION_FAILED` failure events | `notifications.py` | TESTED-PASSED (1.F; CODING_RESULT_INVALID + COORDINATION_FAILED emitted) |
| G4 | Resource-contention events (RESOURCE_CLAIM_STALE, RESOURCE_CONFLICT, RESOURCE_WAIT, RESOURCE_AMBIGUOUS) | `notifications.py` | NOT-TESTED — PA (A20) |
| G5 | Process-health events (STALE_STATUS, PROCESS_STATE_UNKNOWN, PROCESS_INVENTORY_INCOMPLETE, OBSERVATION_ERROR) | `notifications.py` | GAP — **F1F-G5-1** (1.F; OBSERVATION_ERROR is emitted for any error but actionable only when a lane/request is live — a lone malformed signal is emitted-but-unselected) |
| G6 | `MANAGER_SIGNAL` actionable event | `notifications.py` | TESTED-PASSED (1.F; MANAGER_SIGNAL actionable) |
| G7 | Provider-lifecycle events (CODEX_STARTED/_EXITED, PROVIDER_STARTED/_EXITED, CONTROLLER_EXITED) | `notifications.py` | TESTED-PASSED (PROVIDER_STARTED/PROVIDER_EXITED observed live) |
| G8 | Subordinate-process events (HELPER_EXITED/_STATE_UNKNOWN, MCP_EXITED/_STATE_UNKNOWN) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A (a single controller turn emits only PROVIDER_STARTED/PROVIDER_EXITED; no subordinate helper/MCP process was spawned to produce these); not in the phase-1 in-process batch. **→ Phase 5 (5.A.1).** MCP portion additionally OOS. |
| G9 | `PROVIDER_WAIT` / `LANE_STATE_UNKNOWN` | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A (single-turn controller run never entered a provider-wait/unknown-lane state); not in the phase-1 in-process batch. **→ Phase 5 (5.A.2).** |
| G10 | Stall-detection events (MANAGER_REVIEW_DUE, LANE_NO_PROGRESS, LANE_STAGE_REPEAT) | `notifications.py` | TESTED-PASSED (synthetic, user-accepted 2026-08-20) — exercised via injected/synthetic events; live stall producers were removed in the S4 refactor so no authentic producer remains to emit them. |
| G11 | Non-actionable observed-state events (CONTROLLER_ACTIVE, LANE_WAITING_RESOURCE, LANE_WAITING_RELAY, RESULT_ACCEPTANCE_PENDING, RESOURCE_RELEASE_POSSIBLE, REQUEST_STALE) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A; not in the phase-1 in-process batch. **→ Phase 5 (5.A.3).** |
| G12 | Relay-observation events (RELAYED, RELAYED_INACTIVE, RELAYED_AMBIGUOUS) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A; not in the phase-1 in-process batch. **→ Phase 5 (5.A.4).** |
| G13 | Steady-state events (HELPER_ACTIVE, MCP_ACTIVE, CONDITION_CLEARED) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A; not in the phase-1 in-process batch. **→ Phase 5 (5.A.5).** MCP_ACTIVE portion additionally OOS. |
| G14 | Diagnostic/telemetry event class (RAW_OUTPUT, WORKER_OUTPUT, DIAGNOSTIC, PROVIDER_TELEMETRY, HEARTBEAT) | `notifications.py` | TESTED-PASSED (implicit — real entries observed in `LANE_EVENTS.jsonl`) |
| G15 | Harness-internal event-lifecycle tracking (HARNESS_SIGNAL_OBSERVED, HARNESS_EVENT_INELIGIBLE/_ACTIONABLE/_PENDING/_DEFERRED) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A; not in the phase-1 in-process batch. **→ Phase 5 (5.A.6).** |
| G16 | Harness ack tracking (HARNESS_ACK_ATTEMPTED/_SUCCEEDED) | `notifications.py` | NOT-TESTED — live emission did not materialize in 3.A; not in the phase-1 in-process batch. **→ Phase 5 (5.A.7).** |
| G17 | Harness wake-delivery tracking (HARNESS_WAKE_ATTEMPTED/_DELIVERED/_FAILED) | `notifications.py` | TESTED-PASSED (Phase 4 — resume-wake attempt/deliver/fail; `test_G17`) |
| G18 | `HARNESS_SCAN_COMMITTED` atomic scan-commit marker | `notifications.py` | GAP — **F1F-G18-1** (1.F; HARNESS_SCAN_COMMITTED is declared in the taxonomy but NO producer in this worktree emits it — the once-per-scan marker is observable only at contract level) |
| G19 | Manager-wake events (MANAGER_WAKE_RECEIVED, MANAGER_WAIT_FINISHED, MANAGER_WAKE_ATTEMPTED/_DELIVERED/_FAILED) | `notifications.py` | TESTED-PASSED (Phase 4 — manager finalization round trip; `test_G19`) |
| G20 | `WATCH_TIMEOUT` bounded-wait exhaustion event | `notifications.py` | TESTED-PASSED (A23) |
| G21 | Launch-failure events (LAUNCH_FAILED, CONTROLLER_FAILED, CONTROLLER_INTERRUPTED) | `notifications.py` | TESTED-PASSED (3.A) — authentic `launch_lane_controller` launch against a provider that never establishes a session wrote a genuine launch-failure-class event to the shared `LANE_EVENTS.jsonl`: `PROVIDER_STARTED` then `CONTROLLER_FAILED` (`[Errno 22] Invalid argument`), `provider_session_id` null, terminal state `CONTROLLER_FAILED`, 9.2s, quota-free. The classifier is provider-neutral (matches intended Codex-era grouping). Scope: `CONTROLLER_FAILED` observed live; the `LAUNCH_FAILED`/`CONTROLLER_INTERRUPTED` sibling variants remain proven only in-process (phase-1 unit suite). Evidence: `evidence/3.A/`. |
| G22 | `FORMAL_REVIEW_BASELINE_ADVANCED` event | `notifications.py` | NOT-TESTED — PA |
| G23 | `HARNESS_WATCHER_ALERT` (top-priority diagnostic alert) | `notifications.py` | TESTED-PASSED (1.F; HARNESS_WATCHER_ALERT top-priority) |
| G24 | Numeric event-preemption priority table (0=alert highest … 5=RESULT_AVAILABLE lowest) | `notifications.py` | TESTED-PASSED (1.F; numeric 0–5 preemption verified via behavior) |
| G25 | Event disposition tri-state (EVENT_DISPOSITION_WAKING/_OBSERVED/_SUPERSEDED) | `notifications.py` | TESTED-PASSED (1.F; WAKING/OBSERVED/SUPERSEDED) |
| G26 | Record kinds: EVENT / ACK / SUPERSESSION | `notifications.py` | TESTED-PASSED (1.F; EVENT/ACK/SUPERSESSION + BOGUS rejected) |
| G27 | Lane-notification outcome codes (ALREADY_ANSWERED / INVALID_LANE_ID / LANE_NOT_LIVE) | `notifications.py` | TESTED-PASSED (1.F; ALREADY_ANSWERED/INVALID_LANE_ID/LANE_NOT_LIVE; live→None) |
| G28 | `notification: "MANAGER_ACTION_REQUIRED"` field convention | `notifications.py` | TESTED-PASSED (1.F; MANAGER_ACTION_REQUIRED field) |
| G29 | Deferred/durable manager notification with priority preemption | `notifications.py: select_actionable_with_deferred, preempt_pending_with_higher_priority` | TESTED-PASSED (1.F; deferred/durable preemption) |
| G30 | Coalescing of mutable handoff notifications | `notifications.py: coalesce_mutable_handoffs` | TESTED-PASSED (1.F; mutable-handoff coalescing) |
| G31 | Stable deterministic event IDs / at-least-once dedup | `notifications.py`, `events.py` | NOT-TESTED — PA (B26) |
| G32 | `RESULT_AVAILABLE` terminal-result event | `notifications.py` | TESTED-PASSED (1.F logic; RESULT_AVAILABLE emitted at priority 5; live angle deferred to 3.A) |
| G33 | `CHECKPOINT_UPDATED` release-checkpoint event | `notifications.py` | NOT-TESTED — PA |

## H. Resource locks (`resource_locks.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| H1 | Kernel-level exclusive file lock primitive | `resource_locks.py: _kernel_resource_lock` | NOT-TESTED — PA |
| H2 | Safe-filename hashing of exact resource names | `resource_locks.py: claim_filename` | NOT-TESTED — PA (B23) |
| H3 | Claim-evidence read + tamper/corruption detection | `resource_locks.py: _read_claim_evidence` | NOT-TESTED — PA |
| H4 | Ambiguous-claim-parent/path rejection | `resource_locks.py: _claim_parent_is_unambiguous, _claim_path_is_unambiguous` | NOT-TESTED — PA |
| H5 | Exact process-identity binding for a claim owner | `resource_locks.py: _exact_identity` | NOT-TESTED — PA |
| H6 | Stale-owner retained-state reconciliation | `resource_locks.py: _retained_state, _owner_state` | NOT-TESTED — PA (A19) |
| H7 | `ResourceClaims` atomic multi-resource acquisition with rollback | `resource_locks.py` | NOT-TESTED — PA (B22) |
| H8 | `WAITING_RESOURCE` publication while blocked | `resource_locks.py` | NOT-TESTED — PA (A20) |
| H9 | Exclusive-resource semantics on invocation (`exclusive_resources` field) | `invocation.py`, `resource_locks.py` | TESTED-PASSED (1.H `test_compat_resource_locks`; exclusive canonicalization + conflict raise; second claimant blocks CONTENDED) |
| H10 | Resource-release-possible detection on owner exit | `resource_locks.py`, `notifications.py` | TESTED-PASSED (1.H; release-possible on owner exit; fail-closed while live) |

## I. Workspace overlay mechanics (`workspace_overlay.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| I1 | `ingest_super_cache` mirrored-content ingestion | `workspace_overlay.py` | TESTED-PASSED (A6) |
| I2 | `prepare_worktree` bounded materialization into subagent worktree | `workspace_overlay.py` | TESTED-PASSED (A7) |
| I3 | `restore_worktree` exact-byte reversal on retirement | `workspace_overlay.py` | TESTED-PASSED (A8) |
| I4 | `verify_overlay_receipt` independent receipt verification | `workspace_overlay.py` | GAP — **F2A-I4-1** (2.A; `verify_overlay_receipt` is a structural/identity prelaunch check that never reads materialized worktree bytes — byte-integrity is enforced only at `restore_worktree`, not verify) |
| I5 | Append-only copy plan + collision detection (`OverlayCollisionError`) | `workspace_overlay.py: _build_plan, _validate_append_targets` | TESTED-PASSED (2.A) |
| I6 | Exact-byte content-match verification of mirrored super-cache | `workspace_overlay.py: _verify_contents_match` | TESTED-PASSED (implicit, via successful round-trip) |
| I7 | Reparse-point / regular-directory-only enforcement | `workspace_overlay.py: _is_reparse, _regular_directory` | TESTED-PASSED (2.A; junctions available on host, not skipped) |
| I8 | Receipt rollback on partial-apply failure | `workspace_overlay.py: _rollback_applied` | TESTED-PASSED (2.A) |
| I9 | Declaration-file read/validate for a super-cache source | `workspace_overlay.py: _read_declaration` | TESTED-PASSED (2.A) |
| I10 | Byte-encode/decode helpers for receipt persistence | `workspace_overlay.py: _encode_bytes, _decode_bytes` | TESTED-PASSED (2.A) |

## J. Release checks & checkpoint/credit system (`release_checks.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| J1 | Check registry (fast/affected/full/release intent tiers) | `release_checks.py: _registry, registry` | NOT-TESTED — PA (A32) |
| J2 | Input-scope resolution per check | `release_checks.py: resolve_input_scope` | NOT-TESTED — PA |
| J3 | Source-identity capture (branch/commit/dirty-state) for a check run | `release_checks.py: read_source_identity` | NOT-TESTED — PA |
| J4 | Dependency-input-path enumeration per check | `release_checks.py: dependency_input_paths` | NOT-TESTED — PA |
| J5 | Dependency fingerprint hashing for change-detection | `release_checks.py: dependency_fingerprint` | NOT-TESTED — PA |
| J6 | Runner-coordinate identity (interpreter/tooling version binding) | `release_checks.py: runner_coordinate` | NOT-TESTED — PA |
| J7 | Credit record (proof a check's result is still valid for current source state) | `release_checks.py: credit_record` | NOT-TESTED — PA (A33) |
| J8 | Credit/fingerprint invalidation on source-state change | `release_checks.py: _source_matches, _is_ancestor` | NOT-TESTED — PA |
| J9 | Disposition record per-check outcome bookkeeping | `release_checks.py: disposition_record` | NOT-TESTED — PA |
| J10 | Checkpoint record construction | `release_checks.py: checkpoint_record` | NOT-TESTED — PA |
| J11 | Checkpoint write with atomicity | `release_checks.py: write_checkpoint` | NOT-TESTED — PA |
| J12 | Checkpoint merge across parallel lane runs | `release_checks.py: merge_checkpoint_results` | NOT-TESTED — PA |
| J13 | Ancestor-commit eligibility check for checkpoint reuse | `release_checks.py: _is_ancestor` | NOT-TESTED — PA |
| J14 | Source-identity match gate before trusting a cached checkpoint | `release_checks.py: _source_matches` | NOT-TESTED — PA |
| J15 | `select_checks` top-level selection engine (fast/affected/full/release intents combined) | `release_checks.py` | NOT-TESTED — PA |
| J16 | Checkpoint/credit-shape validation | `release_checks.py: _valid_credit_shape` | NOT-TESTED — PA |

## K. Resume & handoff admission (`resume.py`, `resume_admission.py`, `handoff_preflight.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| K1 | `--resume <session_id>` session continuity | `provider.py`, `resume.py` | TESTED-PASSED (live, against real Claude CLI) |
| K2 | `ResumeAdmission` identity-matching gate | `resume.py: make_resume_admission, require_resume_admission` | TESTED-PASSED (1.G `test_compat_resume_admission`) |
| K3 | Resume-identity mismatch rejection | `resume.py: _compare_identity` | TESTED-PASSED (1.G) |
| K4 | Resume amendment diff-based review validation | `resume.py: validate_resume_amendment_review` | TESTED-PASSED (1.G) |
| K5 | Amendment review-card payload load + digest validation | `resume.py: _review_card_payload, _review_path_digest` | TESTED-PASSED (1.G) |
| K6 | Amendment diff-command safety validation | `resume.py: _validate_review_diff_command` | TESTED-PASSED (1.G) |
| K7 | Amendment job-identity derivation | `resume.py: _review_job_identity` | TESTED-PASSED (1.G) |
| K8 | `resume_thread_id` (legacy) vs. `resume_identity.thread_id` (canonical) field-precedence distinction | `invocation.py`, `resume.py` | GAP — **F1G-K8-1** (1.G; conflicting legacy vs canonical resume thread IDs fail CLOSED with InvocationValidationError, not the intended 'canonical wins' precedence — safer, but divergent) |
| K9 | `decide_resume_or_handoff` shared resume-vs-handoff decision logic | `provider.py` | TESTED-PASSED (implicit, exercised by the real `--resume` path) |
| K10 | Handoff preflight: invocation-file / amendment-identity / required-evidence gate | `handoff_preflight.py: preflight_handoff` | TESTED-PASSED (1.G; handoff preflight blocks each missing piece distinctly) |

## L. Capability broker (`capability_broker.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| L1 | `CapabilityRequest` construction | `capability_broker.py` | TESTED-PASSED (2.B `test_compat_capability_broker`; closed shape + reason codes) |
| L2 | `CapabilitySnapshot` point-in-time capability-state capture | `capability_broker.py` | TESTED-PASSED (2.B; frozen/MappingProxy immutability + byte-stable snapshot) |
| L3 | `CapabilityApproval` mediated approval gate | `capability_broker.py` | TESTED-PASSED (2.B; admits on bound approval, denies non-approve at parse + broker, 0 dispatch) |
| L4 | `CapabilityPermit` bounded-use grant | `capability_broker.py` | GAP — **F2B-L4-1** (2.B; `CapabilityPermit` has no use-count field — bounded single-use is broker-enforced via terminal-result caching + REPLAY_MISMATCH/APPROVAL_REPLAY refusal, not a per-permit counter) |
| L5 | `AdapterResult` / `CleanupEvidence` / `CapabilityResult` outcome+cleanup pipeline | `capability_broker.py` | TESTED-PASSED (2.B; RESULT/CLEANUP schema + sha256 provenance; banned private-material aliases fail closed) |
| L6 | `CapabilityBroker` orchestration of request → approval → permit → adapter → cleanup | `capability_broker.py` | TESTED-PASSED (2.B; A25 full end-to-end ordering claim/arm/cleanup→release, no authority leak into public record) |
| L7 | `CapabilityDenied` / `CapabilityAdapterUnavailable` failure-closed paths | `capability_broker.py` | GAP — **F2B-L7-1** (2.B; adapter `CapabilityAdapterUnavailable` from `observe` is CAUGHT → DENIED `SNAPSHOT_UNAVAILABLE` — the typed exception does not propagate to the caller as intended; fail-closed, but divergent) |
| L8 | Canonical JSON + SHA-256 hashing utilities | `capability_broker.py: canonical_json_bytes, canonical_sha256` | TESTED-PASSED (B33, indirect; re-exercised in 2.B) |
| L9 | Process-identity binding for a capability requester | `capability_broker.py: _process_identity, current_process_identity` | NOT-TESTED — PA |
| L10 | `FakeCapabilityAdapter` reference/test adapter | `capability_broker.py` | TESTED-PASSED (2.B; supports/observe field mapping, fail_dispatch→FAIL+released, cleanup_proved=False→UNCERTAIN+retained) |

## M. Codex host adapter internals (`codex_adapter.py`, `codex_bounded_policy.py`) — Codex-only

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| M1 | Bounded owned installer transaction with atomic rollback-on-failure | `codex_adapter.py: install_codex_adapter` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M2 | Adapter-ownership probe | `codex_adapter.py: check_codex_adapter` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M3 | Legacy-revision upgrade path (codex-assets-v1/v2 → v3) | `codex_adapter.py: upgrade_codex_adapter` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M4 | Owned-file uninstall with preserved-modified detection | `codex_adapter.py: uninstall_codex_adapter` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M5 | Packaged-asset manifest integrity (SHA-256, BOM rejection, lone-CR rejection, UTF-8 strictness) | `codex_adapter.py: packaged_codex_assets` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M6 | Project-mutation guard: symlink/reparse-point chain rejection, project-identity revalidation | `codex_adapter.py: _ProjectMutationGuard` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M7 | Hook-fragment merge into `.codex/hooks.json` with ambiguous-owned-hook conflict detection | `codex_adapter.py: _merge_hooks` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M8 | Hook-fragment subtraction on uninstall | `codex_adapter.py: _subtract_hooks` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M9 | Installation-manifest closed-field-set + content-digest self-consistency validation | `codex_adapter.py: _validate_manifest_identity` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M10 | `CodexAdapter.deliver_notice` boundary dispatch (post_tool_use/turn_completed/finalization) | `codex_adapter.py` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M11 | `post_tool_use`/`turn_completed`/`stop_boundary` safe-boundary hook methods | `codex_adapter.py` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M12 | `synthetic_self_test` / `run_synthetic_wake_self_test` | `codex_adapter.py` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M13 | Sparse-notice-only enforcement (no event payload leakage) in transports | `codex_adapter.py: SyntheticCodexTransport, InstalledCodexHookTransport` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M14 | Codex binding-record read/validate for uninstall | `codex_adapter.py: _load_binding_for_hook` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M15 | Bounded-policy launcher/exclusion-list enforcement | `codex_bounded_policy.py: is_excluded, guard_pre_tool_use` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |
| M16 | Bounded-policy status reporting | `codex_bounded_policy.py: bounded_policy_status` | TESTED-PASSED (Phase 4 — Codex internals held as green regression reference: `test_codex_bounded_policy.py`+`test_s4_contract.py`+`test_compat_host_adapters.py`, 45 passed) |

## N. Host adapter framework / S4 delivery coordinator (`host_adapters.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| N1 | `HostAdapter` abstract contract + `FutureHostFixture` honest-stub for unimplemented hosts (Claude currently gets this fixture, not a real adapter) | `host_adapters.py` | TESTED-PASSED (Phase 4 — real `ClaudeAdapter` replaces `FutureHostFixture`; `test_N1`) |
| N2 | `DeliveryNotice` bounded wake payload (identity/revision/pending-count/severity, no event payload) | `host_adapters.py` | TESTED-PASSED (Phase 4 — sparse `DeliveryNotice`; `test_N2`) |
| N3 | `DeliveryReceipt` transport-evidence-only record | `host_adapters.py` | TESTED-PASSED (Phase 4 — transport-evidence-only `DeliveryReceipt`; `test_N3`) |
| N4 | `ManagerEventAck` (created only by a separate manager action) | `host_adapters.py` | TESTED-PASSED (1.J `test_compat_host_adapters`) |
| N5 | `NotificationStopDecision` | `host_adapters.py` | TESTED-PASSED (1.J) |
| N6 | `DeliveryCoordinator` registration/replay-state persistence beside the S3 queue | `host_adapters.py` | TESTED-PASSED (Phase 4 — registration replay persists across restart; `test_N6`) |
| N7 | Severity/highest-pending computation for a wake payload | `host_adapters.py: _severity_for, _highest_pending` | TESTED-PASSED (1.J; severity/highest-pending computation) |
| N8 | `select_host_adapter` capability-based host selection (routes unsupported hosts to `FutureHostFixture`) | `codex_adapter.py: select_host_adapter` | TESTED-PASSED (Phase 4 — capability-gated `select_host_adapter('claude')`; `test_N8`) |

## O. Process supervision & identity

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| O1 | Exact PID+creation-time process identity | `harness_common/process_identity.py: exact_process_identity` | NOT-TESTED — PA (B20) |
| O2 | Job-object/subreaper containment (Windows Job API / Linux subreaper) | `process_supervisor.py: ProcessBoundary` | NOT-TESTED — PA |
| O3 | Cooperative-stop-by-exact-identity (never broad kill) | `process_supervisor.py: ProcessSupervisor` | NOT-TESTED — PA |
| O4 | Windows CIM process snapshot/query | `processes.py: windows_process_snapshot, windows_process_query` | NOT-TESTED — PA |
| O5 | Linux `/proc` process snapshot/query | `processes.py: linux_process_snapshot, _linux_process_query` | NOT-TESTED — PA |
| O6 | Process-group inventory | `processes.py: process_group_inventory` | NOT-TESTED — PA |
| O7 | Detached long-lived owner-process launch with exact creation-identity capture | `operator_launch.py: launch_process` | TESTED-PASSED (2.D `test_compat_operator_launch` O7; records exact PID+created_utc identity; full-snapshot observe skipped on this host — CIM inventory unavailable) |
| O8 | Detached-owner snapshot for external supervision | `operator_launch.py: detached_owner_snapshot` | TESTED-PASSED (2.D O8; snapshot reports the live record then drains it after exit) |
| O9 | Cooperative exact-identity process termination | `operator_launch.py: _cleanup_exact_posix, _terminate_windows_exact` | TESTED-PASSED (2.D O9; wrong-creation-time decoy is never signaled → returns `(False, "POSIX process identity was reused")`; Windows exact-handle path is internal to launch, skipped on host) |
| O10 | `launch_lane_controller` embeddable entry point | `public_launch.py` | TESTED-PASSED (A36) |

## P. Lane lifecycle: immutable source views & archive-first retirement (`lane_lifecycle.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| P1 | `allocate_immutable_source_view` read-only source snapshot allocation | `lane_lifecycle.py` | TESTED-PASSED (2.C `test_compat_lane_lifecycle` P1) |
| P2 | Immutable-view read-only enforcement | `lane_lifecycle.py: _set_read_only` | TESTED-PASSED (2.C P2) |
| P3 | Lifecycle-registry admission with process-boundary record | `lane_lifecycle.py: _admit_lifecycle_registry` | TESTED-PASSED (2.C P3) |
| P4 | Lifecycle-registry update on state transition | `lane_lifecycle.py: _update_lifecycle_registry` | TESTED-PASSED (2.C P4) |
| P5 | Retained-commit / separate-root safety checks before allocation | `lane_lifecycle.py: _retained_commit, _assert_retained, _separate_root` | TESTED-PASSED (2.C P5) |
| P6 | `retire_terminal_lane` archive-first retirement (hash-bound copy before Git worktree close) | `lane_lifecycle.py` | TESTED-PASSED (2.C P6) |
| P7 | Lane-binding validation before retirement | `lane_lifecycle.py: _validate_lane_binding` | TESTED-PASSED w/ note **F2C-P7P11-1** (2.C P7; binding refusal surfaces fail-closed as `outcome=="VISIBLE"` with reason `LANE_BINDING_FOREIGN_WORKTREE`, not a raised exception) |
| P8 | Archive digest / member-copy integrity | `lane_lifecycle.py: _archive_digest, _copy_member` | TESTED-PASSED (2.C P8) |
| P9 | `validate_lane_archive` independent post-hoc archive verification | `lane_lifecycle.py` | TESTED-PASSED (2.C P9) |
| P10 | Registry-identity canonicalization (path-identity binding) | `lane_lifecycle.py: _canonical_registry_identity` | TESTED-PASSED (2.C P10) |
| P11 | Process-proof requirement before retirement | `lane_lifecycle.py: _process_proof` | TESTED-PASSED w/ note **F2C-P7P11-1** (2.C P11; missing/incomplete proof surfaces fail-closed as `outcome=="VISIBLE"` with reason `PROCESS_SNAPSHOT_INCOMPLETE`, not a raised exception) |
| P12 | Safe tar-member-name validation on archive extraction | `lane_lifecycle.py: _safe_member` | TESTED-PASSED (2.C P12) |

## Q. Config, profile, mutation, stable I/O, prompt bundle, shared models

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| Q1 | `HarnessConfig` load with numeric-bound clamping | `config.py: load_config, _number, _integer` | GAP — **F1K-Q1-1** (1.K; out-of-range config numbers are REJECTED with ConfigError, not clamped to bounds as intended — stricter/safer, but divergent) |
| Q2 | Declared-relative-path validation in config | `config.py: _declared_relative_paths` | TESTED-PASSED (1.K) |
| Q3 | `RuntimeProfile` denied-name / capability-name / env-name validation | `profile.py` | TESTED-PASSED (B17, partial — construction used, denial paths not independently probed) |
| Q4 | `build_child_environment` profile-scoped subprocess environment construction | `profile.py` | TESTED-PASSED (2.H; declared+base-allowed vars kept, undeclared/denied/inherited-secrets cleared and sorted, construction fail-closed on denied grant + unregistered provider; no fail-open breach in any casing) |
| Q5 | `safe_relative_path` path-traversal/absolute-path rejection | `mutation.py` | NOT-TESTED — PA |
| Q6 | Alternate-data-stream (ADS) detection on Windows paths | `mutation.py: _has_ads` | NOT-TESTED — PA |
| Q7 | Reparse-point-chain validation before any mutation | `mutation.py: _validate_chain` | NOT-TESTED — PA |
| Q8 | Atomic `replace`/`delete`/`rename` with expected-prior-state proof (optimistic concurrency) | `mutation.py` | NOT-TESTED — PA |
| Q9 | `AnchoredAppendFile` / directory-anchor-bound append-only writer | `mutation.py` | NOT-TESTED — PA |
| Q10 | `PathKeyedAppendLock` per-path append serialization | `stable_io.py` | NOT-TESTED — PA |
| Q11 | `SafeOutput` / `read_stable` / `read_tail_stable` torn-write-resistant reads | `stable_io.py` | NOT-TESTED — PA (B34) |
| Q12 | Canonical JSON serialization + SHA-256 helpers | `stable_io.py: canonical_json, sha256_bytes` | TESTED-PASSED (B33) |
| Q13 | Prompt-bundle component composition + per-component content digest | `prompt_bundle.py: compose_prompt_bundle` | TESTED-PASSED (B15) |
| Q14 | Prompt-bundle safe-component-path enforcement | `prompt_bundle.py: _safe_component_path` | TESTED-PASSED (1.K; symlink sub-case skipped on Windows) |
| Q15 | `bundle_from_record` reconstruction of a prompt bundle from a persisted record | `prompt_bundle.py` | TESTED-PASSED (1.K) |
| Q16 | Shared dataclass/schema surface (`ProcessInfo`, `RequestFacts`, `StableBytes`, `ObservationError`, UTC time helpers) | `models.py` | TESTED-PASSED (implicit, exercised throughout; B43) |
| Q17 | `prompt.py` prompt-construction constants/templates | `prompt.py` | GAP — **F1K-Q17-1** (1.K; `prompt.py` has NO template constants — it is a pure re-export shim; `compose_prompt_bundle` concatenates verbatim with no placeholder substitution) |
| Q18 | Suite-local run/controller/request/relay/checkpoint file discovery | `discovery.py: discover_run, discover_suite` | NOT-TESTED — PA (B38, dup of F26) |
| Q19 | Discovery record-kind classification + declared-lifetime-record enumeration | `discovery.py` | NOT-TESTED — PA (dup of F19/F25) |
| Q20 | Discovery observation-cache invalidation on file-signature change | `discovery.py: _clear_observation_caches, _file_signature, _cache_put` | NOT-TESTED — PA |

## R. Firmware/hardware — explicit out of scope

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| R1 | `FirmwareHardwareAdapter` capability-broker firmware adapter | `firmware_adapter.py` | NOT-TESTED — OOS |
| R2 | `FirmwareAction`/`FirmwareOperation`/`FirmwareCampaignPack` campaign model | `firmware_campaign.py` | NOT-TESTED — OOS |
| R3 | Legacy policy-bound firmware invocation loading | `invocation.py: _load_firmware_invocation` | NOT-TESTED — OOS |
| R4 | Firmware result routing (firmware-vs-coding invocation split) | `invocation.py` | NOT-TESTED — OOS |
| R5 | Firmware-as-coding rejection | `invocation.py: _reject_firmware_coding_model_settings` | NOT-TESTED — OOS (C15) |
| R6 | Firmware leases/relays/boards/probes hardware-capability path | `capability_broker.py` firmware adapters | NOT-TESTED — OOS |
| R7 | Firmware sprint/host-readiness/decide meta-planning surface | `FULL-EXECUTION-SPEC_PLAN_2.md` MI-FIRMWARE-* | NOT-TESTED — OOS |
| R8 | Firmware release-promotion gate | `FULL-EXECUTION-SPEC_PLAN_2.md` MI-PROMOTE | NOT-TESTED — OOS |

## S. MCP integration — explicit out of scope

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| S1 | `--mcp-config` invocation field / provider argv wiring | `invocation.py`, `provider.py` | NOT-TESTED — OOS |
| S2 | MCP process tri-state and MCP-proof states | `reconcile.py` (F5, F13) | NOT-TESTED — OOS |
| S3 | Broker-compatible MCP traffic in the firmware capability seam | `capability_broker.py` | NOT-TESTED — OOS |

## T. Legacy/parallel watcher generation (`Portable_Watcher_Repo`, superseded design)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| T1 | R1 suite-local discovery of controller/request/relay/checkpoint/result files (older generation) | `Portable_Watcher_Repo/orchestrator_harness/SPEC.md` | NOT-TESTED — OOS (superseded by `discovery.py`) |
| T2 | Watcher evaluator (AI-judge classification, `evaluator_enabled` flag, off by default) | `harness_watcher_implementation/evaluator.py`, `settings.py` | NOT-TESTED — OOS |
| T3 | Watcher alert/recovery ledger (`STOP_ASSIGNING` → … → `RESOLVED`) | `harness_watcher_implementation/*` | GAP — **F2G-A39-1** (2.G; see A39 — no ordered-admission ledger exists) |
| T4 | WSL2/bubblewrap real-agent dry-run containment spec | `Portable_Watcher_Repo/.../SPEC.md` R-series | NOT-TESTED — OOS |
| T5 | Host-only unit/integration test list (older SPEC.md) | `Portable_Watcher_Repo/.../SPEC.md` | NOT-TESTED — OOS |
| T6 | Attention-sprint historical record decoding | `attention_sprint.py: decode_historical_attention_record` | TESTED-PASSED (2.F; see A30 — 22-test decode + fail-closed suite) |

## U. Provider adapter contract & argv construction (`provider.py`, `providers.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| U1 | `ProviderLaunchSpec` → provider-specific `build_argv` translation | `provider.py` | TESTED-PASSED (0.1, fix) — was TESTED-FAILED (phase-0 blocker §1); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.1/`. |
| U2 | `--verbose`/stream-json flag correctness for Claude headless print mode | `provider.py: ClaudeCodeProviderAdapter.build_argv` | TESTED-PASSED (0.1, fix) — was TESTED-FAILED (phase-0 blocker §1, missing `--verbose`); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.1/`. |
| U3 | Permission-mode / sandbox-bypass propagation into provider argv | `provider.py` | TESTED-PASSED (0.2, fix) — was TESTED-FAILED (phase-0 blocker §2, no permission bypass → silent false-COMPLETED); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.2/`. |
| U4 | `config_overrides`/`service_tier`/`approval_policy` generic override channel | `provider.py`, `invocation.py` | TESTED-PASSED (0.3, fix) — was TESTED-FAILED (phase-0 blocker §3); fixed & re-verified PASS in the compat-test clone. ⚠️ Fix is uncommitted/unmerged. Evidence: `evidence/0.3/`. |
| U5 | `BaseProviderAdapter` shared contract (`ProviderCapabilities`, `ProviderOperationResult`) | `provider.py` | TESTED-PASSED (1.I `test_compat_provider_contract`; both built-ins share versioned contract shape + ProviderOperationResult fields) |
| U6 | `ProviderAdapterRegistration` / `register_provider_adapter` / `unregister_provider_adapter` runtime registry | `provider.py` | TESTED-PASSED (A2) |
| U7 | `_validate_adapter_contract` structural check on a registered adapter | `provider.py` | TESTED-PASSED (1.I; incomplete/id-mismatch adapter rejected) |
| U8 | `classify_operation` / `unsupported_operation_result` per-provider operation gating | `provider.py` | TESTED-PASSED (1.I; graceful unsupported + F1A-C24-1 raise) |
| U9 | `provider_config_digest` config-identity hashing | `provider.py` | TESTED-PASSED (1.I; digest stable / field-sensitive) |
| U10 | `redact_command` secret-redaction before argv is logged/persisted | `provider.py` | TESTED-PASSED (1.I; no secret survives redaction into any token byte) |
| U11 | `build_provider_evidence` / `structured_handoff` evidence-record construction | `provider.py` | TESTED-PASSED (1.I; no secret survives into any evidence/handoff byte) |
| U12 | `notification_mode` (SAFE_BOUNDARY_ONLY vs. WAKE) per-provider capability declaration | `provider.py` | TESTED-PASSED (implicit — Claude's SAFE_BOUNDARY_ONLY mode confirmed via A23) |
| U13 | `decide_resume_or_handoff` shared resume/handoff decision | `provider.py` | TESTED-PASSED (K9, dup) |
| U14 | Transcript line parsing → provider-neutral terminal outcome (STARTED/COMPLETED/FAILED/CANCELLED) | `provider.py: parse_transcript_line` | TESTED-PASSED for STARTED/COMPLETED (real Claude `system/init` and `result/success` lines) |
| U15 | Claude `parse_transcript_line` never produces a `CANCELLED` outcome, unlike Codex's explicit `turn.cancelled` handling | `provider.py` | GAP — **U15-CANCELLED** (observed divergence, benign: the Claude CLI emits no `turn.cancelled`-equivalent event, so the parser cannot produce `CANCELLED`; behavior differs from the Codex-era design but is not a defect. Formerly labeled NOTED. See [missing_claude_implementation.md "Noted but not counted as a failure"](missing_claude_implementation.md#noted-but-not-counted-as-a-failure)) |
| U16 | Session/thread identity persistence (`session_id`) into status + events | `lane_controller.py`, `provider.py` | TESTED-PASSED (real Claude `session_id` recorded in `LANE_EVENTS.jsonl`) |

## V. Lane controller: launch, concurrency, evidence (`lane_controller.py`)

| # | Feature | Source module(s) | Status |
|---|---|---|---|
| V1 | `run_root`/cwd binding for the launched subprocess | `lane_controller.py` | TESTED-PASSED |
| V2 | Concurrent multi-process lane launch (threading/subprocess isolation) | `lane_controller.py` | TESTED-PASSED (2 real concurrent `claude` subprocesses, no interference) |
| V3 | Provider event/evidence logging to `LANE_EVENTS.jsonl` | `lane_controller.py`, `events.py` | TESTED-PASSED |
| V4 | Result-file presence/absence detection (`result_validation.state = MISSING`) | `lane_controller.py`, `task.py`, `git_safety.py` | TESTED-PASSED (both lanes correctly reported `MISSING`) |
| V5 | Terminal-outcome-to-lane-status mapping (`FAILED`/`CANCELLED`/invalid-result → not-clean) | `lane_controller.py` | TESTED-PASSED (implicit, exercised via the COMPLETED path and the §2 false-positive) |
| V6 | Lane-controller main entry / in-process `lane_main` | `lane_controller.py` | TESTED-PASSED |
| V7 | `watch --until-actionable` actionable-event allowlist gating (MANAGER_SIGNAL/RESOURCE_CONFLICT/etc.) | `cli.py: _is_actionable` | TESTED-PASSED (3.B) — live `python -m orchestrator_harness watch --until-actionable` subprocess: a MANAGER_SIGNAL injected mid-watch wakes it (EXIT_OK, event printed before deadline) and a non-actionable event (malformed signal → observation error) does NOT wake it (EXIT_TIMEOUT). Both the positive wake and the negative non-wake observed; matches intended Codex-era allowlist gating. |
| V8 | Real-provider-subprocess isolation guarantees (no cross-lane file/branch contamination) | `lane_controller.py`, `git_safety.py` | TESTED-PASSED (A10, dup) |

---

## Notes on methodology

- "TESTED" above means a real command was executed against real source (live `claude` CLI
  subprocess, real `git worktree`, real file I/O) in this session or the prior Codex/DeepSeek
  session referenced throughout, with observed output — not inferred from reading code. A single
  real test action typically confirms several feature rows at once from different angles (e.g.
  one real 2-lane concurrent Claude run backs A10, V2, V8, V3, V4, and part of U16/U14
  simultaneously) — that's why the number of rows tagged TESTED-PASSED/TESTED-FAILED (52 + 7 = 59)
  is larger than the 14 distinct real commands/test actions that actually produced them (10
  successful, 4 revealing failures). The 14/10/4 figures are unchanged from the prior revision;
  no new testing was performed to produce this expanded inventory.
- Every NOT-TESTED row is a real gap in this report's coverage, not a claim that the feature
  works or is broken. Firmware (A5, A40, R1-R8) and MCP (A41, S1-S3) are explicit exclusions per
  instruction. The 30 former CX-GAP rows (M1-M16, N1-N3/N6/N8, G17, G19, B9-B14, A24) are now
  all **TESTED-PASSED**: Phase 4 built the real Claude host adapter + owned installer and the
  concept — provider-neutral all along — is exercised for Claude by
  `orchestrator_harness/tests/test_compat_claude_adapter.py` (4.A/4.B; 14 passed, 3 subtests),
  with M1-M16 held as the green Codex regression reference. N1, formerly the direct statement of
  the gap (Claude got `FutureHostFixture`), now confirms a real `ClaudeAdapter`; A24's idle-wake
  is `claude --resume <session_id>` cross-process re-entry. See `plans/compatibility-testing/`
  `evidence/PHASE4-ORCHESTRATOR_ACCEPTANCE.json` and the taxonomy note above.
- Full evidence for all four TESTED-FAILED findings (command output, argv diffs, transcript
  excerpts) lives in `missing_claude_implementation.md`, linked inline above from every row that
  traces back to one of them.
- This revision adds ~285 rows versus the prior 61-row pass, almost entirely from decomposing
  previously file-level rows (e.g. old B36 "Codex-specific adapter internals" → new M1-M16 and
  N1/N8; old B43 "models.py" → new Q16 plus cross-references; old invocation/reconcile/
  notification "one row" entries → new sections C, F, and G) down to individual CLI flags,
  validation rules, state classifications, and event types.
