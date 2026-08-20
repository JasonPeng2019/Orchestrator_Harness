# Subagent task — Phase 0, Step 0.4: No working Claude example/fixture (bug A17)

You are a subagent executing one step of the compatibility-testing plan. Work autonomously: author, run, verify, save evidence. Report precisely.

## Working directory (disposable clone — the ONLY place you may write)
```
C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test
```
- Branch `compat-test-copy`. NEVER modify `Firmware/target-harness`. Do NOT commit.
- Steps 0.1–0.3 have landed in this clone: `ClaudeCodeProviderAdapter.build_argv` emits `--verbose` and defaults `--permission-mode bypassPermissions`; `parse_transcript_line` detects permission_denied; **`config_overrides` for claude-code now populate a child-env channel** (incl. the alias `model_provider="ollama"` → `ANTHROPIC_BASE_URL=http://localhost:11434`, `ANTHROPIC_AUTH_TOKEN=ollama`, `ANTHROPIC_API_KEY=""`), and `service_tier`/`approval_policy` on claude-code raise `InvocationValidationError`. Verify these exist before relying on them (`git diff --stat` / grep). If 0.3's channel is NOT present, STOP and report that 0.3 is missing.

## The gap
The only examples/fixtures are Codex-only: `examples/disposable_coding_fixture.py` and `examples/coding.invocation.example.json` use the legacy `orchestrator-coding-invocation/v1` schema with a `codex` block and a fake worker (`_fake_worker`), no `claude` anywhere in `examples/`. A new caller has no copy-paste path to a working claude-code lane.

## Your deliverables (both are required)

### 1. `examples/coding.claude.invocation.example.json`
A **valid canonical `orchestrator-worker-invocation/v1`** for `provider.id="claude-code"`:
- Study the canonical schema: `orchestrator_harness/invocation.py` (`parse_canonical_invocation`, required fields at the top of the function) and the ONLY existing claude-code canonical shape in `orchestrator_harness/tests/test_s2_contract.py` (grep for `"claude-code"`).
- Model the non-provider parts (run_root, repository, profile, prompt_bundle, output_paths, event_log_path, resources, task_card, etc.) on test_s2_contract's canonical invocation, generalized to a real path layout with clear comments.
- Provider block: `id: "claude-code"`, a model that maps to a real Ollama model, `config_overrides: ["model_provider=\"ollama\""]` (demonstrates the 0.3 redirect channel), and NO `service_tier`/`approval_policy` (those now raise for claude-code). `permission_mode` omitted → the 0.2 default bypass applies; add a comment saying so.
- Comment every non-obvious field. The file must be loadable end-to-end by `load_invocation` from `invocation.py` (validate with a snippet; save the validation output as `evidence/0.4/invocation-load.txt`).

### 2. `examples/disposable_claude_coding_fixture.py`
A single real Claude lane, end-to-end, on the Ollama backend:
- Model on `examples/disposable_coding_fixture.py` (same style, same helpers you can reuse: `_run`/`_git`/`_write_json`/`_wait_for_status`/`_finish_controller` pattern) but SIMPLER: one worktree, one lane, real `claude` as the provider binary.
- Create a temp project (git init, one commit, one trivial file), add a worktree, write the canonical invocation (same shape as deliverable 1, pointing at the real worktree + a real prompt that asks the model to do one concrete trivial thing, e.g. create `HELLO.txt` with fixed content and commit it — keep it tiny so the model reliably completes).
- Provider `command` = the path to the real claude CLI (resolve via `shutil.which("claude")`; on Windows it is `C:\Users\Jason\.local\bin\claude.exe`), and let the env channel carry the Ollama redirect via `config_overrides` (model_provider alias). The lane controller spawns the provider with an isolated env; the 0.3 fix merges the ANTHROPIC_* overrides AFTER isolation — verify the child actually gets them (if the run reaches api.anthropic.com and fails auth, the merge is broken: debug the merge before concluding).
- Launch via the same `launch_lane_controller` public path the existing fixture uses (`orchestrator_harness/public_launch.py`). Wait for the controller to reach the terminal state and assert: `PROVIDER_STARTED` and `PROVIDER_EXITED` rows present in the shared `LANE_EVENTS.jsonl`, a real non-empty `session_id` recorded, provider terminal outcome `COMPLETED`, exit code 0. NOTE: the terminal state name for a claude-code lane may differ from `CODEX_EXITED` — discover the actual state name from `lane_controller.py`/status output rather than assuming.
- `main()` like the existing fixture: `--keep DIRECTORY` support, JSON result summary printed, exit 0/1. Keep runtime bounded (~2–4 min max).

### 3. Live run + evidence
Run the new fixture from the clone root (it must pass on the Ollama backend — this is the real proof):
```
cd "C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test"
PYTHONPATH="C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test;C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees" python examples/disposable_claude_coding_fixture.py --keep <temp-root> 2>&1 | tee evidence/0.4/fixture-run.log
```
Capture:
- `evidence/0.4/fixture-run.log` — full run output + the printed JSON result.
- `evidence/0.4/LANE_EVENTS.jsonl` — copy the lane event log from the kept fixture root (keep the temp root via `--keep`, then copy the file; the fixture may leave it in `<temp-root>/runtime/LANE_EVENTS.jsonl`).
- `evidence/0.4/invocation-load.txt` — canonical-invocation validation proof (deliverable 1).
- `evidence/0.4/example-json.txt` — the rendered `coding.claude.invocation.example.json` if it aids review (optional).

Pass = fixture runs, real claude subprocess launches, `PROVIDER_STARTED`/`PROVIDER_EXITED` + real `session_id` in `LANE_EVENTS.jsonl`, exit 0.

## Hard constraints
- The fixture's claude lane must reach the Ollama backend ONLY via the invocation's `config_overrides` env channel (0.3) — do NOT set process-level ANTHROPIC_* env vars in the fixture itself (that would bypass the very mechanism under test). For YOUR OWN direct claude CLI calls (debugging), use the env-scoped launcher and never touch `~/.claude`/global settings.
- Stdlib only. Work only in the clone + evidence dir.

## Report
(1) canonical invocation written — load validated?; (2) fixture design summary + terminal state name discovered; (3) live run result (exit code, event rows, session_id, outcome); (4) any issues found (esp. env-channel/merge behavior); (5) evidence file list.
