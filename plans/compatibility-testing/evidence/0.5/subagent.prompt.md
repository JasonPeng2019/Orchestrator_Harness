# Subagent task — Phase 0, Step 0.5: Confirm the unblock (gate for Phase 3)

You are a subagent executing the final step of phase 0. Work autonomously, then report precisely. This is the GATE for Phase 3: if any item below fails, report exactly what failed and why.

## Working directory (disposable clone — the ONLY place you may write)
```
C:\Users\Jason\Documents\Jason\Orchestrator_Harness\harness-single-worktrees\compat-test
```
- Branch `compat-test-copy`. NEVER modify `Firmware/target-harness`. Do NOT commit.
- Steps 0.1–0.4 have landed in this clone (verified before you start): `--verbose` + default `--permission-mode bypassPermissions` in `ClaudeCodeProviderAdapter.build_argv`, permission_denied detection in `parse_transcript_line`, config_overrides → child-env channel (`model_provider="ollama"` alias), per-provider rejection of service_tier/approval_policy, `examples/coding.claude.invocation.example.json`, `examples/disposable_claude_coding_fixture.py`. `git diff --stat` to confirm.

## Task — re-run the originally-passing live set, now on genuinely-launching Claude lanes
The prior round proved these behaviors with the REAL claude CLI (findings doc "Passed" section); your job is to prove they all STILL hold after the 0.1–0.4 fixes, and that the phase-0 gate is met. Drive REAL `claude` lanes against the local Ollama backend. The Ollama redirect must flow through the invocation's `config_overrides` env channel (0.3) — that is the mechanism under test.

### The six original behaviors (all must pass)
1. **2-lane concurrency with genuine claude subprocesses** — two lanes, each its own git worktree, launched simultaneously via `launch_lane_controller` (public path). Each lane asks the model to do one trivial distinct thing (create+commit a file named after the lane). Assert: each lane touched only its own file, committed only on its own branch; no cross-lane contamination.
2. **Provider event/evidence logging** — `PROVIDER_STARTED`/`PROVIDER_EXITED` in the shared `LANE_EVENTS.jsonl` for both lanes, with real non-empty `session_id`/`thread_id`, correct `provider_id` ("claude-code"), and `provider_terminal_outcome: COMPLETED`.
3. **Transcript parsing (STARTED/COMPLETED path)** — `system/subtype=init` → STARTED and `result/subtype=success` → COMPLETED correctly classified from the real transcript.
4. **`MISSING` result detection** — with no RESULT.json written, result validation reports `state: MISSING`.
5. **`--resume <session_id>`** — after lane A completes, launch a resume lane with the captured real session_id; the resumed process must recall prior turn content (ask the resume prompt to state what the original prompt asked; assert the reply reflects the original content — model on the prior round's "HELLO FROM LANE A" proof).
6. **`watch --until-actionable` → `WATCH_TIMEOUT`** — for a genuinely completed claude lane, `python -m orchestrator_harness watch --until-actionable` (with a short watch timeout config) returns WATCH_TIMEOUT (no push signal — known behavior, SAFE_BOUNDARY_ONLY; not a regression).

### Phase-0 gate (the point of all this)
- A claude lane launches with **no flag error** (the `--verbose` fix) and is **not** a false-COMPLETED: if the model's tools are denied, outcome ≠ COMPLETED; when the lane actually completes its work, outcome = COMPLETED and the expected file exists. Assert the happy path here (file exists + COMPLETED); the denied path was proven in 0.2.

### Mechanics
- Write your probe under `scratch/0.5/` in the clone (a python script driving temp project + worktrees + canonical invocations, modeled on `orchestrator_harness/tests/test_claude_code_compat.py` — the prior round's live tests — and `examples/disposable_claude_coding_fixture.py`). You may copy the env-scoped launcher pattern for any direct claude calls.
- Provider `command` = real claude CLI path (`shutil.which("claude")`, on this machine `C:\Users\Jason\.local\bin\claude.exe`).
- Prompts must be tiny and deterministic so the model reliably completes (single file create+commit).
- Save evidence to `C:\Users\Jason\Documents\Jason\Orchestrator_Harness\plans\compatibility-testing\evidence\0.5\`:
  - `probe.py` (the script), `probe-run.log` (full run output incl. JSON summary), `LANE_EVENTS.jsonl` (copy from the kept fixture root), `resume-proof.txt` (the resume reply excerpt), `watch-result.txt` (the watch command output), `gate-proof.txt` (file-exists + outcome assertions output).
- Keep the whole probe bounded: ~5–10 min max.

## Hard constraints
- No process-level ANTHROPIC_* env vars in the probe itself — the redirect must come from the invocation's config_overrides channel. Your own direct claude calls: env-scoped launcher only; NEVER `~/.claude`, never `claude config set`.
- Stdlib only. Work only in the clone + evidence dir.

## Report
Per-behavior result table (1–6: PASS/FAIL + one-line evidence pointer), the phase-0 gate verdict, any new findings (record honestly — a new gap is a valid recorded outcome), and the evidence file list.
