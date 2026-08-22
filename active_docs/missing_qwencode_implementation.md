# Missing / broken Qwen Code support in the WIP target harness

> **Active compatibility follow-through.** The documented Qwen fixes and gaps remain active until
> their source changes are merged into `firmware-v2-harness-runner`. They do not reopen the closed
> Firmware hardware campaign.

Scope: `orchestrator_harness` at commit `055a5bd` (branch `firmware/v2-candidate`),
copied to `harness-single-worktrees/qwencode-test` (branch `qwencode-test-copy`).
The exact commit being actively developed was **never edited** — all execution
happened in the copy and sibling disposable lane worktrees. The qwen adapter is
loaded from the Firmware bootstrap (`Firmware/scripts/orchestration/qwen_provider_bootstrap.py`)
by file path and registered in-process, exactly as production does.

Only items that were **actually executed and observed to fail** are listed under
"Failed". Everything else that was executed is listed under "Passed" for
completeness; nothing below is inferred without a real run backing it up.

> **2026-08-21 correction — the goal was a qwen-code CLI mirror of the codex
> implementation, and an earlier pass over-listed "gaps."** Tracing the actual code
> in `harness-single-worktrees/qwencode-test` shows most of the listed "gaps" are
> **not qwen-vs-codex gaps at all**: they are a **codex-only host-adapter / delivery
> subsystem** that is *identically unbuilt for claude* in this worktree
> (`AdapterCapabilities` in `host_adapters.py` has only `codex()` and
> `future_fixture()` factories — no `claude()`, no `qwen()`; both non-codex
> providers get `FutureHostFixture`). Those are **design recommendations**, mirroring
> `missing_claude_implementation.md` §C — not compatibility gaps. After correction
> there are **two genuine qwen-vs-codex defects**: (1) the generic override channel
> silently dropped (§Real defect below), and (2) the terminal `CANCELLED` outcome
> collapsed to `FAILED` (§Second real defect below — low severity but closeable, and
> a real audit divergence from codex). The rest are design-recs and one missing
> convenience file.

## Explicit scope exclusion (per instruction)

Firmware-specific functionality (`firmware_campaign.py`, `firmware_adapter.py`,
`FirmwareCampaignPack`/`FirmwareAction`/`FirmwareHardwareAdapter`, the legacy
policy-bound firmware invocation path) and anything MCP-server-related
(`--mcp-config`, the broker-compatible MCP traffic in the firmware seam) were
**not tested at all**. This is a real gap in this report's coverage, not a
finding that they work — they were out of scope per instruction. The user may
simtest on the MCP server; that is noted as a gap, not a pass.

## Real defect #1 — generic override channel silently dropped (C17/U4 → F1.2.7)

### Generic override channel silently dropped for qwen-code (C17/U4 → F1.2.7)
`invocation.py`'s `_provider()` validator (`invocation.py:380-420`) applies the
same optional-field allow-list to every `provider.id` — it never checks whether
a field is meaningful for the selected provider. A qwen invocation that sets
`config_overrides`/`service_tier`/`approval_policy`/`permission_mode`/
`allowed_tools`/`disallowed_tools`/`mcp_config` passes validation with zero
error or warning, then the qwen adapter's `build_argv`
(`qwen_provider_bootstrap.py`) silently drops them all — it only uses
`command`/`model`/`action`/`session_id`. **This is a divergence on the exact code
path codex exercises**: codex's `build_argv` honors `config_overrides` via
`-c <override>` (`provider.py:426`); qwen's ignores them. Confirmed by direct
execution:

```
QWEN argv: ['qwen', 'exec', '--approval-mode=yolo', '--model',
  'deepseek-v4-flash:0731-cloud', '--output-format', 'stream-json',
  '--auth-type', 'openai', '--openai-api-key', 'ollama',
  '--openai-base-url', 'http://localhost:11434/v1', '--mcp-config', '{...}']
  # config_overrides, service_tier, approval_policy, permission_mode,
  # allowed_tools, disallowed_tools, and the invocation-provided mcp_config
  # are all silently dropped
```

**Fix = reject-loud** (the qwen-side of claude's blocker #3). Raise
`InvocationValidationError` for the fields qwen cannot honor: qwen-code has **no
`-c` equivalent** (its config is settings.json-based), and the Ollama redirect the
earlier probe achieved with `config_overrides: ["model_provider=\"ollama\""]` is
**already delivered** by the adapter's own `_route_argv` (`--openai-base-url` from
package-local settings). So there is nothing for qwen to *honor* — the correct
behavior is to reject the fields loudly instead of accepting-then-dropping them.
Asserted (current defective behavior) in
`test_qwen_build_argv_silently_drops_override_fields` and
`test_qwen_invocation_validator_accepts_override_fields`.

## Design recommendations (NOT qwen-vs-codex gaps — codex-only subsystem or provider-neutral)

These were previously listed as "failed / gaps." Tracing the code shows each is a
**recommendation**, not a compatibility gap — identical to how
`missing_claude_implementation.md` §C reclassified the claude side.

### D1. No push "finish" notification / host adapter — build one (implementable, not a gap)
The qwen adapter registers `notification=False`, so `notification_mode("qwen-code")`
resolves to `SAFE_BOUNDARY_ONLY` with no wake text
(`test_qwen_adapter_registers_with_notification_false`), and qwen gets the
`FutureHostFixture` stub (all `AdapterCapabilities` False). A finishing qwen lane
produces no push wake; the manager must poll (`watch --until-actionable` /
`--until-event`).

**But this is not a qwen-vs-codex gap** — it is a **codex-only subsystem that is
identically unbuilt for claude** in this worktree. `host_adapters.py` exposes only
`AdapterCapabilities.codex()` (all True) and `.future_fixture()` (all False); there
is **no `claude()` and no `qwen()`**. So on the entire push-wake surface claude and
qwen are byte-identical. The claude side of this subsystem was later built in
Phase 4 in a *separate* clone (`compat-test-copy`); it is **not present or merged
here**. Recommendation: build a qwen host adapter the same way — qwen-code has a
full hooks mechanism (`qwen hooks`; `Stop`, `SessionEnd`, `SubagentStop`,
`Notification`/`idle_prompt`) that can wake the orchestrator's idle session. Until
then, any manager relying on codex's push wake must poll qwen lanes. (Inventory
rows F1.2.8, F5.2.1–6, F5.3.1–2 — DESIGN-REC.)

### D2. Overlay control data dirties the worktree (provider-neutral, identical for codex)
When a super-cache overlay is materialized into a subagent worktree
(`prepare_worktree(role="subagent")`), the materialized files (`instructions.md`,
`config/settings.txt`) are untracked and make the worktree dirty, so the result
gate (`validate_task_result_repository`) rejects it with `CODING_RESULT_INVALID`.
The test had to git-ignore + commit those paths for a clean tree. This is
**provider-neutral** — codex behaves identically — so it is a shared-code footgun
worth documenting, **not a qwen defect**.

### D3. No qwen example/fixture (A17) — a missing convenience file, not a capability gap
`examples/disposable_coding_fixture.py` is codex-only (`codex_command`,
`fixture_codex.jsonl`; no `qwen` hits under `examples/`). There is no
`examples/*qwen*` file. But a working qwen invocation is fully achievable **today**
via the canonical `orchestrator-worker-invocation/v1` schema from `invocation.py`
(the qwen suite builds exactly that). So the fixture is a **nicety**, not a missing
capability. (Claude also lacked one until a fixture was authored as its blocker #4.)
Asserted in `test_no_qwen_example_fixture_exists`. Low priority.

## Second real defect (low severity, closeable) — terminal `CANCELLED` collapsed to `FAILED`

qwen's `parse_transcript_line`/`terminal_outcome` map a cancelled/interrupted run
to **FAILED** (no terminating result line + non-zero exit → FAILED) and never emit
`CANCELLED`. **Codex, on the same cancel path, records a distinct `CANCELLED`**:
`turn.cancelled` → `ProviderEvent(kind="CANCELLED")` → `terminal_outcome` returns
`"CANCELLED"` (`provider.py:447,458,465`). Since the goal is to mirror codex, this
divergence on a path codex exercises **is a real gap**, not a design-rec — an
earlier draft wrongly filed it as "not a gap" by treating downstream mootness as if
it erased the divergence, which is exactly the completed-but-divergent laundering
the GAP-vs-PASSED rule forbids.

- **Closeable** (unlike claude's unclosable U15): qwen-code's own bundled
  `structured-output.md` states a SIGINT/interrupt exits **130** and normally emits
  **no result line** ("treat the exit code as the source of truth"); qwen-code's
  protocol vocabulary also includes an `interrupt` control subtype (and an exit-53
  max-turns path). So qwen **has** a distinguishable cancellation signal — the
  Claude CLI emits none at all, which is what makes U15 genuinely unclosable. Fix:
  map exit-130 / `interrupt` → `CANCELLED` in `terminal_outcome`.
- **Low severity, not moot.** Every downstream *branch decision* already treats
  `FAILED` and `CANCELLED` identically — same controller exit code
  (`lane_controller.py:3208`), same notification priority (`notifications.py:1762`),
  same reconcile grouping (`reconcile.py:191-206`) — so there is no control-flow
  consequence today. But the stack models CANCELLED as first-class
  (`lane_controller` closed vocabulary `3143-3153`; `reconcile.py` distinct
  `provider_cancelled` `194`; `notifications.py` distinct `cancelled` `1760`), so a
  cancelled qwen lane persists as `provider_failed` where codex persists
  `provider_cancelled` — a real audit / state-fidelity divergence from codex.

The success and current FAILED-collapse branches are both covered by
`test_qwen_parse_and_terminal_map_failure_branch`; a corrected mapping needs a new
assertion that exit-130 yields `CANCELLED`.

## Passed (tested, worked correctly)

- **Multiple deepseek agents spawn via headless qwen-code exec processes** — two
  lanes (`alpha`, `beta`), each its own git worktree, launched in parallel via
  `lane_controller.run` with a fake CLI emitting the exact qwen stream-json
  protocol (`system/init` → STARTED, `result/subtype:success` → COMPLETED). Both
  reached `PROVIDER_EXITED` with `provider_terminal_outcome=COMPLETED` and
  `result_valid=true`. Each lane committed only on its own branch
  (`lane/alpha`, `lane/beta`); no cross-lane contamination.
- **Resource contention serializes two qwen lanes** — two lanes claiming the same
  named exclusive resource (`service:qwen-db`) serialize: the second enters
  `WAITING_RESOURCE` while the first holds the claim, then proceeds after release.
- **Stale result rejection** — a pre-seeded canonical-shaped `RESULT.json` with a
  mismatched `worker_invocation_id` is rejected at start time (exit code 2,
  "task result task/card identity does not match") before the provider launches.
- **Merge lane and integration merge** — alpha + beta branches merged into an
  `integration/merge` worktree, a merge lane ran project checks
  (`python -m unittest -v`), and the merged tree passed with both features
  present.
- **S3 manager queue admit/ack** — `ManagerEventRouter.admit` → `next_event` →
  `acknowledge` → `pending_events` empty, with exact event-ID ack.
- **Overlay super-cache into a subagent worktree** — `ingest_super_cache` →
  `prepare_worktree(role="subagent")` materialized `instructions.md` and
  `config/settings.txt` into the alpha worktree; the lane verified the overlay
  receipt (`overlay_receipt_verified=true`) before the provider started and
  produced a valid result.
- **Overlay receipt rejection before launch** — a wrong-role (`orchestrator`)
  overlay receipt fails closed: `LAUNCH_FAILED`, no provider PID, error
  "overlay receipt is not completed for this subagent worktree".
- **Resume / handoff** — `decide_resume_or_handoff("qwen-code", ...)` returns
  `RESUME` when identity matches (qwen declares `resume=True`), and `HANDOFF`
  with `fabricated_continuity=False` on identity mismatch.
- **Provider evidence & redaction** — `build_provider_evidence` binds
  identity/version/capabilities/attempt/session and redacted provenance;
  `redact_command` deterministically redacts credential-shaped tokens.
- **Terminal-outcome parsing, success AND failure branches** — the qwen adapter's
  `parse_transcript_line`/`terminal_outcome` map both terminal states correctly.
  qwen has **no** distinct `turn.failed`/`turn.cancelled` events (unlike codex);
  it collapses every terminal `result` into one event and decides failure via
  `is_error is True OR subtype != "success"`. Asserted in
  `test_qwen_parse_and_terminal_map_failure_branch`: `subtype:"success"` →
  COMPLETED; `is_error:true` (even with `subtype:"success"`) → FAILED; any
  non-success subtype (`error`/`cancelled`/`error_max_turns`) → FAILED with the
  raw subtype preserved; and `terminal_outcome` honours a FAILED event even on a
  clean `exit_code==0` (a provider that reports failure then exits 0 is **not**
  laundered into COMPLETED). This closes the previously-thin spot where only the
  success path was exercised (the FAILED branch is qwen-specific adapter logic,
  not provider-neutral, so generic suites did not cover it).

## Noted but not counted as a failure

The qwen adapter's `notification=False` resolves to `SAFE_BOUNDARY_ONLY`, the
same mode claude-code uses. The code is not broken — but this is a **missing
capability, not a design constraint**: qwen-code has a hooks mechanism that
could back a push-wake host adapter, and none is built. It is the defining
qwen-vs-codex difference and the reason managers must poll. Documented as a
gap, not a defect.

## Not otherwise tested (time-boxed, lower priority given findings above)

Release-check selection, `watch --until-actionable` against a genuinely completed
qwen lane, and the full `ResumeAdmission` identity-matching path were not
independently re-run against qwen-authored commits in this session — that
machinery is provider-neutral and was already validated end-to-end in the earlier
Codex/DeepSeek session; nothing found here suggests it would behave differently
once a qwen lane actually reaches a committed, valid state.
