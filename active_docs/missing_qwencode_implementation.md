# Missing / broken Qwen Code support in the WIP target harness

Scope: `orchestrator_harness` at commit `055a5bd` (branch `firmware/v2-candidate`),
copied to `harness-single-worktrees/qwencode-test` (branch `qwencode-test-copy`).
The exact commit being actively developed was **never edited** — all execution
happened in the copy and sibling disposable lane worktrees. The qwen adapter is
loaded from the Firmware bootstrap (`Firmware/scripts/orchestration/qwen_provider_bootstrap.py`)
by file path and registered in-process, exactly as production does.

Only items that were **actually executed and observed to fail** are listed under
"Failed". Everything else that was executed is listed under "Passed" for
completeness; nothing below is inferred without a real run backing it up.

## Explicit scope exclusion (per instruction)

Firmware-specific functionality (`firmware_campaign.py`, `firmware_adapter.py`,
`FirmwareCampaignPack`/`FirmwareAction`/`FirmwareHardwareAdapter`, the legacy
policy-bound firmware invocation path) and anything MCP-server-related
(`--mcp-config`, the broker-compatible MCP traffic in the firmware seam) were
**not tested at all**. This is a real gap in this report's coverage, not a
finding that they work — they were out of scope per instruction. The user may
simtest on the MCP server; that is noted as a gap, not a pass.

## Failed (tested, and broken / a real qwen-vs-codex gap)

### 1. No push "finish" notification reaches the manager — qwen must poll (KEY gap)
The qwen adapter registers with `notification=False` (see
`qwen_provider_bootstrap.py`), so `notification_mode("qwen-code")` resolves to
`SAFE_BOUNDARY_ONLY` with no wake text. This is asserted deterministically in
`test_qwen_adapter_registers_with_notification_false`. Unlike codex (which
registers `notification=True` → `WAKE`), a qwen lane that finishes produces **no
push "finish" signal** to the manager. The manager must poll
(`watch --until-actionable` / `--until-event`) rather than receive an immediate
wake. This is the single most important qwen-vs-codex behavioral difference.

**This is an implementable gap, not a design constraint.** qwen-code has a full
hooks mechanism (`qwen hooks`; events `Stop`, `SessionEnd`, `SubagentStop`,
`Notification` with matcher type `idle_prompt`, etc.) that could back a
push-wake host adapter — the wake target is the orchestrator agent's idle
session, which qwen can wake via its `Notification`/`idle_prompt` hook. The
harness simply has **no qwen host adapter / hook binding built** (qwen gets the
same `FutureHostFixture` stub as claude). So the gap is a missing capability,
not a structural impossibility. Any manager that relies on codex's push wake
will silently stall on qwen lanes unless it polls.

### 2. Overlay control data dirties the worktree and fails the result gate unless ignored
When a super-cache overlay is materialized into a subagent worktree
(`prepare_worktree(role="subagent")`), the materialized files
(`instructions.md`, `config/settings.txt`) are **untracked** and make the
worktree dirty. The result gate (`validate_task_result_repository`) rejects a
dirty tree with `CODING_RESULT_INVALID` ("task result requires a clean project
worktree"). This is provider-neutral behavior, but it is a real footgun for qwen
lanes that use overlays: the overlay files must be git-ignored (and the ignore
rule committed) before the lane can produce a valid result. The test
`test_overlay_super_cache_into_subagent_worktree` had to append
`instructions.md`/`config/` to the worktree `.gitignore` and commit it to get a
clean tree. This is not a qwen-specific defect, but it is a coordination gap that
surfaced in the multi-agent overlay scenario and is worth documenting.

### 3. Generic override channel silently dropped for qwen-code (C17/U4 — same gap as claude)
`invocation.py`'s `_provider()` validator (`invocation.py:380-420`) applies the
same optional-field allow-list to every `provider.id` — it never checks whether
a field is meaningful for the selected provider. A qwen invocation that sets
`config_overrides`/`service_tier`/`approval_policy`/`permission_mode`/
`allowed_tools`/`disallowed_tools`/`mcp_config` passes validation with zero
error or warning, then the qwen adapter's `build_argv`
(`qwen_provider_bootstrap.py`) silently drops them all — it only uses
`command`/`model`/`action`/`session_id`. Confirmed by direct execution:

```
QWEN argv: ['qwen', 'exec', '--approval-mode=yolo', '--model',
  'deepseek-v4-flash:0731-cloud', '--output-format', 'stream-json',
  '--auth-type', 'openai', '--openai-api-key', 'ollama',
  '--openai-base-url', 'http://localhost:11434/v1', '--mcp-config', '{...}']
  # config_overrides, service_tier, approval_policy, permission_mode,
  # allowed_tools, disallowed_tools, and the invocation-provided mcp_config
  # are all silently dropped
```

This is the exact same generic-override-channel gap claude-code has (Claude's
finding §3). Concretely, the mechanism the earlier Codex/DeepSeek probe used to
redirect a lane to an alternate model endpoint
(`config_overrides: ["model_provider=\"ollama\""]`) has **no qwen equivalent** —
there is no generic-override channel into qwen's argv at all. Asserted in
`test_qwen_build_argv_silently_drops_override_fields` and
`test_qwen_invocation_validator_accepts_override_fields`.

### 4. No working example/fixture exists for a qwen-provider lane (A17 — same gap as claude)
The one "complete local example" advertised by the README/QUICK_START,
`examples/disposable_coding_fixture.py`, is hardcoded to the legacy Codex-only
`"codex": {...}` invocation shape (`codex_command`, `fixture_codex.jsonl`, etc.
— grepped, no `qwen` hits anywhere under `examples/`). There is no
`examples/*qwen*` file in the package. Building a working qwen-code invocation
requires the separate, more complex canonical
`orchestrator-worker-invocation/v1` schema directly from `invocation.py`. This
is the same gap claude-code has (Claude's finding §4). Asserted in
`test_no_qwen_example_fixture_exists`.

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
