# Subagent task — Phase 0, Step 0.2: No permission bypass → silent false-COMPLETED (bug U3)

You are a subagent executing one step of the compatibility-testing plan. Work autonomously: reproduce, fix, re-test, add a regression test, and save evidence. Report back precisely.

## Working directory (disposable clone — the ONLY place you may write)
```
C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test
```
- Branch `compat-test-copy`. You are in this directory. NEVER modify `Firmware/target-harness`. Do NOT commit.
- **Step 0.1 already landed in this clone**: `ClaudeCodeProviderAdapter.build_argv` now emits `--verbose` after `--output-format stream-json` (line ~508), and `orchestrator_harness/tests/test_compat_provider_argv.py` exists. Keep that fix; build on it.

## The bug
Two-part defect (both must be fixed):
1. **No default bypass.** Codex's adapter unconditionally emits `--dangerously-bypass-approvals-and-sandbox`. Claude's adapter (`provider.py:515`) only emits `--permission-mode` when the caller sets `provider.permission_mode` — an optional field absent from every example. Result: a caller following the documented shapes gets a lane that silently does nothing.
2. **Permission denial is invisible.** `ClaudeCodeProviderAdapter.parse_transcript_line` (`provider.py:535`) classifies a final `result` line as COMPLETED unless `is_error`/error-subtypes — it ignores `{"type":"system","subtype":"permission_denied",...}` lines. When the CLI blocks a tool (Write etc.), the turn still ends `is_error:false, subtype:"success", EXIT 0` but the work never happened → the harness reports a false COMPLETED.

## Step 1 — Reproduce (must produce the false positive first)
Run against the REAL CLI on the Ollama backend (env-scoped launcher; the env vars and CLAUDE_CONFIG_DIR are scoped to this one process — never touch `~/.claude`):
```
echo "Create a file named default_perm_test.txt with content HI" | \
  ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
  CLAUDE_CONFIG_DIR="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test\.subagent-scratch-02" \
  claude --print --output-format stream-json --verbose --model deepseek-v4-flash:0731-cloud
```
(NOTE: NO `--permission-mode` — that is the buggy default path.) Run it from a throwaway directory (e.g. `scratch/0.2-repro/` under the clone) so the Write attempt targets a real file path. Capture the raw stream-json as `evidence/0.2/denied-transcript.jsonl`.
- Expected observations to record: a `system/subtype=permission_denied` line for Write; final `result` line with `is_error:false`/`subtype:success`; process exit code 0; the file does NOT exist afterward (`ls` it — record that).
- If the Ollama model happens to be granted permissions (no denial occurs), record exactly what happened instead and still proceed — the harness-side reproduction below is what matters.
Then prove the harness maps that transcript to COMPLETED: small python snippet calling `parse_transcript_line` on each line of `evidence/0.2/denied-transcript.jsonl` (or a synthetic permission-denied transcript if the live one didn't deny) → final event kind is COMPLETED. Save snippet output as `evidence/0.2/repro-false-completed.txt`.

## Step 2 — Fix (two independent hardenings; do BOTH)
1. **Default-safe bypass (decision: default bypass, mirroring Codex):** in `ClaudeCodeProviderAdapter.build_argv` (`provider.py:505`), when `spec.permission_mode` is None (not set by caller), emit `--permission-mode bypassPermissions`. Explicit caller value still wins. (This is the documented product decision for this run.)
2. **Detect permission denial:** in `parse_transcript_line` (`provider.py:535`), treat a transcript containing `system/subtype=permission_denied` as not-clean. Concretely: emit a provider event that will never map to COMPLETED — e.g. return a `ProviderEvent("FAILED", ..., detail="permission_denied ...")` when the init/start has been seen and a permission_denied line arrives; and/or track "denied" state so the final `result` line maps to FAILED (or a distinct BLOCKED kind) instead of COMPLETED. Match the existing event taxonomy: `terminal_outcome` (line 564) already maps FAILED/CANCELLED non-COMPLETED; keep the fix consistent with it. Choose the minimal clean implementation; document your choice in the final report.

## Step 3 — Re-test / pass
1. **With default bypass:** run the same prompt WITH the fixed harness path (no `permission_mode` in spec → adapter emits bypass). Now `default_perm_test.txt` is actually created AND the lane's terminal outcome is COMPLETED. Save transcript as `evidence/0.2/bypass-success.jsonl`; record `ls default_perm_test.txt` output and parse_transcript_line classification.
2. **Forced denial:** with permission bypass deliberately removed (e.g. spec sets `permission_mode` to something restrictive, or construct a synthetic denied transcript) → `parse_transcript_line` now yields FAILED (non-COMPLETED). Save as `evidence/0.2/denied-classified.txt`.

## Step 4 — Regression test
Extend `orchestrator_harness/tests/test_compat_transcript_parse.py` (new file):
- Feed a captured/synthetic permission-denied transcript → assert the final classification is NOT COMPLETED (FAILED/BLOCKED per your implementation).
- Assert default spec (permission_mode=None) → build_argv contains `--permission-mode bypassPermissions`; explicit `permission_mode="default"` (or whatever value) → caller value used.
Run:
```
cd "C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test"
PYTHONPATH="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test;C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees" python -m unittest orchestrator_harness.tests.test_compat_transcript_parse -v
```
Also re-run `orchestrator_harness.tests.test_compat_provider_argv` and `orchestrator_harness.tests.test_s2_contract` (no regression). Save outputs under `evidence/0.2/`.

## Hard constraints
- Only the env-scoped claude launcher; NEVER `~/.claude`, never `claude config set`, no settings files outside the clone.
- Stdlib only. Work only in the clone + evidence dir.

## Report
(1) live reproduction: did the real CLI deny? exact lines + exit code; (2) harness false-COMPLETED reproduction; (3) the two fixes (summary + diff); (4) re-test results (file created? classification?); (5) regression test results; (6) evidence file list. Precise, factual.
