# Subagent task — Phase 0, Step 0.3: config_overrides / service_tier / approval_policy silently dropped for claude-code (bug C17 / U4)

You are a subagent executing one step of the compatibility-testing plan. Work autonomously: reproduce, fix, re-test, add a regression test, save evidence. Report precisely.

## Working directory (disposable clone — the ONLY place you may write)
```
C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test
```
- Branch `compat-test-copy`. NEVER modify `Firmware/target-harness`. Do NOT commit.
- Steps 0.1 and 0.2 already landed in this clone (`--verbose` fix in `ClaudeCodeProviderAdapter.build_argv`, default `--permission-mode bypassPermissions`, permission_denied detection in `parse_transcript_line`, `test_compat_provider_argv.py` + `test_compat_transcript_parse.py`). Keep those; build on them.

## The bug
`invocation.py: _provider()` (line 380) applies the SAME optional-field allow-list to every provider.id — it accepts `config_overrides`, `service_tier`, `approval_policy` for `claude-code` but `ClaudeCodeProviderAdapter.build_argv` (`provider.py:505`) never reads any of the three → accepted then silently dropped. The Codex adapter (`provider.py:401`) honors all three (`-c approval_policy=...`, `-c service_tier=...`, `-c <override>` argv entries). The concrete harm: the mechanism the Codex/DeepSeek probe used to redirect a lane to an alternate endpoint (`config_overrides: ["model_provider=\"ollama\""]`) has no Claude equivalent — no per-invocation way to point a claude lane at `http://localhost:11434`.

## Decided contract for this run (honor + reject — NO silent drop)
1. **`config_overrides` — HONOR.** Claude Code has no `-c` config channel; the natural channel is the child process environment. Facts already verified for you:
   - `claude --help` (v2.1.235) has NO `--service-tier` / `--approval-policy` flags; it DOES support env redirects: `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY` (empty value), `ANTHROPIC_MODEL`.
   - The provider child is spawned at `lane_controller.py:2860` `subprocess.Popen(argv, ..., env=child_env, ...)`. `child_env` is either `isolated_coding_child_environment()` (`lane_controller.py:189`) — which STRIPS everything except `_CHILD_ENV_ALLOW` (line ~170) — or built from `invocation.runtime_profile.provider_needs` (~line 2830). `ANTHROPIC_*` is currently NOT in `_CHILD_ENV_ALLOW`.
   - `ProviderLaunchSpec` is defined at `provider.py:75`; the launch spec is built by `_provider_launch_spec(invocation, thread)` (called at `lane_controller.py:2126`).
   - Design the minimal mechanism: extend `ProviderLaunchSpec` with an env-override channel (e.g. `env_overrides: Mapping[str, str]`); `ClaudeCodeProviderAdapter.build_argv` translates `config_overrides` into env entries; the controller merges them into `child_env` AFTER the isolation/allow-list filtering (so no inherited secret can leak — only explicitly declared keys pass). Alias the Codex spelling `model_provider="ollama"` → `ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama`, `ANTHROPIC_API_KEY=""`. Also accept explicit `ANTHROPIC_*` overrides verbatim (e.g. `ANTHROPIC_BASE_URL=...`). Reject (raise `ProviderAdapterError`/`InvocationValidationError`) any override entry that is neither a known alias nor an `ANTHROPIC_*` env var — fail loud, never drop.
   - Check whether other adapters/consumers construct `ProviderLaunchSpec` positionally (breaking change risk) and use a defaulted field so the change is backward-compatible.
2. **`service_tier`, `approval_policy` — REJECT for claude-code.** Make `_provider()` (`invocation.py:380`) per-provider aware: for `provider.id="claude-code"`, presence of `service_tier` or `approval_policy` raises `InvocationValidationError` naming the offending field(s) and explaining Claude Code has no equivalent. (`permission_mode`, `allowed_tools`, `disallowed_tools`, `mcp_config`, `command`, `model`, `notification`, `config_overrides` stay accepted for claude-code.)

## Step 1 — Reproduce (must fail first)
Write a small python snippet: build a canonical invocation (`orchestrator-worker-invocation/v1` — see `test_s2_contract.py` for the canonical claude-code shape) setting `config_overrides`, `service_tier`, `approval_policy`; load it; call `ClaudeCodeProviderAdapter().build_argv(spec)`; assert NONE of the three appear in the Claude argv (reproducing the silent drop). Same snippet shows the Codex adapter DOES carry all three. Save as `evidence/0.3/repro-silent-drop.txt`.

## Step 2 — Fix
Apply the contract above. Touch only: `orchestrator_harness/provider.py`, `orchestrator_harness/invocation.py`, `orchestrator_harness/lane_controller.py` (env merge), and the tests. Keep changes minimal and consistent with surrounding style.

## Step 3 — Re-test / pass
1. Claude argv now: `config_overrides` entries appear as env overrides (assert via the spec/mechanism you chose); service_tier/approval_policy on claude-code raise a clear `InvocationValidationError` naming the field(s).
2. Codex argv unchanged (still carries all three via `-c`).
3. Live proof of the redirect channel (if feasible): launch a real claude lane via the harness path with `config_overrides: ["model_provider=\"ollama\""]` (plus the env-scoped launcher env vars set process-wide for THIS run only) and confirm the lane actually talks to the Ollama backend and completes (a `system/subtype=init` + `result/subtype=success` appears). If the controller-level merge is hard to drive standalone, at minimum prove the merged `child_env` contains the three `ANTHROPIC_*` entries through the isolation function (unit-level assertion).
4. Save `evidence/0.3/claude-argv.txt` (claude argv + env override channel, for a spec with all three fields) and `evidence/0.3/codex-argv.txt` (codex argv, same spec) — the diff documents the fix.

## Step 4 — Regression test
Add `orchestrator_harness/tests/test_compat_provider_allowlist.py`:
- claude-code + `service_tier` → `InvocationValidationError`; claude-code + `approval_policy` → error; codex + same fields → accepted.
- claude-code `config_overrides` → env channel populated; unknown override key → error (no silent drop).
- existing tests still green: run `test_s2_contract.py`, `test_compat_provider_argv.py`, `test_compat_transcript_parse.py`, `test_lane_controller.py` (this touches the spawn path).
Run with:
```
cd "C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test"
PYTHONPATH="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test;C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees" python -m unittest <module> -v
```
Save outputs under `evidence/0.3/`.

## Hard constraints
- Claude CLI launches (if any) only via the env-scoped launcher; NEVER `~/.claude`, never `claude config set`, no settings outside the clone.
- Stdlib only. Work only in the clone + evidence dir.

## Report
(1) reproduction output; (2) design of the env channel (what you extended and where merged); (3) the reject behavior; (4) re-test results incl. live/lane proof; (5) regression results; (6) evidence file list.
