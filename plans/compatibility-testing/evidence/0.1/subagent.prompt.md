# Subagent task — Phase 0, Step 0.1: Claude lane launch missing `--verbose` (bugs A1 / U1 / U2)

You are a subagent executing one step of the compatibility-testing plan. Work autonomously: reproduce, fix, re-test, add a regression test, and save evidence. Report back what you did and what passed.

## Working directory (disposable clone — the ONLY place you may write)
```
C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test
```
- Branch `compat-test-copy`, commit `dd673cb`. You are in this directory.
- NEVER modify `C:\Users\Jason\Documents\Jason\Orchestrator_Harness\Firmware\target-harness` (the source worktree) — work only in the clone.
- Do NOT commit anything.

## The bug
`ClaudeCodeProviderAdapter.build_argv` (`orchestrator_harness/provider.py`, class starts at line 500, `build_argv` at line 505) builds:
`['claude', '--print', '--output-format', 'stream-json', ...]` and never adds `--verbose`. The real Claude CLI hard-rejects this exact combination with `Error: When using --print, --output-format=stream-json requires --verbose` and exit code 1 — so every claude-code lane dies before running a single turn.

## Step 1 — Reproduce (must fail first)
1. Run this exact command and capture the output (expect exit 1 with the flag error):
   ```
   echo "hi" | ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
     CLAUDE_CONFIG_DIR="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test\.subagent-scratch-01" \
     claude --print --output-format stream-json --model deepseek-v4-flash:0731-cloud --permission-mode bypassPermissions
   ```
   Save the output as `evidence/0.1/repro-flag-error.txt` (evidence dir: `C:\Users\Jason\Documents\Jason\Orchestrator_Harness\plans\compatibility-testing\evidence\0.1\`).
2. Write a tiny python snippet that calls `ClaudeCodeProviderAdapter().build_argv(spec)` with a `start` spec (see `test_s2_contract.py` for the canonical shape; `ProviderLaunchSpec` is in `provider.py:75`) and assert `"--verbose"` is ABSENT from the argv. Run it and capture output as `evidence/0.1/repro-argv-absent.txt`. This reproduces the defect in the harness itself.

## Step 2 — Fix
In `orchestrator_harness/provider.py`, `ClaudeCodeProviderAdapter.build_argv` (line 508): emit `--verbose` right after `"--output-format", "stream-json"` (i.e. whenever `--print`/stream-json mode is used). Minimal change, match surrounding style.

## Step 3 — Re-test / pass
1. Re-run your python snippet: argv must now contain `"--verbose"` after `stream-json`. Save as `evidence/0.1/argv.txt` (show the full fixed argv for a start spec).
2. Run the REAL CLI with the fixed argv shape (the same env-scoped launcher as above, but now WITH `--verbose`):
   ```
   echo "hi" | ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
     CLAUDE_CONFIG_DIR="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test\.subagent-scratch-01" \
     claude --print --output-format stream-json --verbose --model deepseek-v4-flash:0731-cloud --permission-mode bypassPermissions
   ```
   Save the RAW stream-json stdout as `evidence/0.1/cli-transcript.jsonl`. Pass = exit code 0, NO flag error, and a `{"type":"system","subtype":"init",...}` line appears in the transcript.

## Step 4 — Regression test
Add `orchestrator_harness/tests/test_compat_provider_argv.py` with at least `test_claude_start_argv_has_verbose` (build a start spec, assert `--verbose` present right after stream-json; also assert a resume spec keeps `--resume` + `--verbose`). Run it:
```
cd "C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test"
PYTHONPATH="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test;C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees" python -m unittest orchestrator_harness.tests.test_compat_provider_argv -v
```
Also run the existing `test_s2_contract.py` to prove no regression:
```
PYTHONPATH=... python -m unittest orchestrator_harness.tests.test_s2_contract -v
```
Save both outputs under `evidence/0.1/` (e.g. `unittest-compat-provider-argv.txt`, `unittest-s2-contract.txt`).

## Hard constraints
- The only Claude CLI launches allowed are the env-scoped form above (env vars scoped to that one process + CLAUDE_CONFIG_DIR inside the clone). NEVER touch `~/.claude`, never run `claude config set`, never write any settings file outside the clone.
- No third-party Python deps; stdlib only.
- Work only in the clone + the evidence dir.

## Report (your final text)
State: (1) reproduced? exact error observed; (2) the fix (one-line summary + diff); (3) re-test results (exit code, init line present?); (4) regression test results (pass/fail counts); (5) list of evidence files written. Be precise and factual — no fluff.
