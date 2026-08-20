# 1.K coordinator note — first launch killed mid-probe, re-launch succeeded

The first `deepseek-v4-flash:0731-cloud` launch (task `b29kj1bvr`, `--effort high`, local Ollama,
env-scoped launcher, scratch `.subagent-scratch-1K`) was **externally terminated mid-probe**: 132
stdout lines, no module written, no `result` envelope. The only stderr line was the benign
cosmetic `[claude-code:unrecognized_model] … generate_session_title` (the session-title helper
does not recognize the Ollama model name — harmless, unrelated to the task). This is the same
external-kill pattern seen on the first 1.H launch and on 1.I.

Per the established handling (kill mid-probe with no module → re-launch fresh), a second launch
(task `bejhxm8ye`, scratch `.subagent-scratch-1K-r2`) ran to a clean `result` envelope
(`subtype: success`, 23 turns) and authored `test_compat_config_bundle.py`.

## Coordinator acceptance (independent)

- `test_compat_config_bundle` → **8 passed / 1 skipped OK** (`test-run.log`). The single skip is
  the Q14 symlink sub-case: this Windows session cannot create file symlinks (WinError 1314, "a
  required privilege is not held") — the test `skipTest`s it per the prompt rather than failing.
- Regression `test_config_store` → **12/12 OK** (`config-regression.log`).
- `git status` → only the pre-existing phase-0 `M` files + the new untracked module.
  `config.py`, `prompt_bundle.py`, `prompt.py` are unmodified — no source edit, no leak.

## Findings (2, both note-severity — actual behavior is STRICTER than the plan text)

- **F1K-Q1-1** — `load_config` numeric bounds **reject** out-of-range values
  (`config.py:62,74` raise `ConfigError "must be >= …"`); the plan's Q1 "clamp to bounds" premise
  does not hold. Fail-closed rejection beats silent clamping. Confirmed in source by the
  coordinator.
- **F1K-Q17-1** — `prompt.py` is a pure 7-name re-export shim with **no** template constants; the
  plan's Q17 "template constants / templates" premise does not match. `compose_prompt_bundle`
  concatenates component bytes verbatim (placeholder-looking literals survive byte-for-byte — no
  substitution). Confirmed in source by the coordinator.

Both filed in `evidence/FINDINGS.md` (ledger + detail). The subagent flagged both correctly but
noted `FINDINGS.md` was outside its allowed write scope; the coordinator filed them.

## Genuineness spot-check

The module drives the real seams (temp JSON configs through `load_config`; real path-bound files
through `prompt_bundle_record_from_paths` → `bundle_from_record`). Q15 exercises **four**
fail-closed tamper gates (length→size gate, same-length byte→sha256 gate, component-digest→sha256
gate, manifest-digest→"stale or tampered"). No fail-open was observed in any tested seam.
