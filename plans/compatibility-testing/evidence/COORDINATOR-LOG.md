# Coordinator log — Phase 0 (compatibility-testing plan)

Each row = one subagent launched via the native `claude` CLI on the local Ollama backend
(`deepseek-v4-flash:0731-cloud`), env-scoped launcher (ANTHROPIC_BASE_URL/AUTH_TOKEN/
API_KEY= + CLAUDE_CONFIG_DIR into the clone). All work in disposable worktree
`harness-single-worktrees/compat-test` (branch `compat-test-copy`, HEAD `dd673cb`).

| Step | Subagent | Launched | Exit | Evidence | Verification | Status |
|---|---|---|---|---|---|---|
| Baseline suite (clone) | — (direct run) | 2026-08-18 | 0 | task begublxqb | 496 tests OK (1 skipped) | ✅ done |
| 0.1 | missing `--verbose` | 2026-08-18 | 0 | evidence/0.1/ | ✅ fix verified in provider.py:508; 23 tests OK (indep. re-run); s2 pinning-bug expectation updated | ✅ done |
| 0.2 | false-COMPLETED / permission | 2026-08-18 | 0 | evidence/0.2/ | ✅ default bypass + permission_denied→FAILED (stateless result-line check); 28 tests OK; live denial + bypass proofs | ✅ done |
| 0.3 | dropped overrides | 2026-08-18 | 0 | evidence/0.3/ | ✅ env-override channel merged after isolation; fail-loud translation (model_provider="ollama" alias → ANTHROPIC_*); service_tier/approval_policy rejected for claude-code; codex unchanged; live lane proof (no inherited-secret leak); 18 compat + 29 s2/lane-controller tests OK (indep. re-run) | ✅ done |
| 0.4 | Claude example/fixture | 2026-08-18 | 0 | evidence/0.4/ | ✅ `examples/coding.claude.invocation.example.json` (canonical v1, claude-code, ollama alias via config_overrides, no service_tier/approval_policy) loads via `load_invocation` (LOAD_VALIDATION=PASS, indep. re-run); `examples/disposable_claude_coding_fixture.py` (stdlib, public launch path, terminal state PROVIDER_EXITED discovered) ran live twice — normal + scrubbed-ambient-env — exit 0, COMPLETED, real session_id ea14fa65…/e082a04d…, HELLO.txt committed; redirect proven via config_overrides channel alone | ✅ done |
| 0.5 | unblock confirmation | 2026-08-18 | 0* | evidence/0.5/ | ❌ attempt 1 **BLOCKED by Ollama usage limit** — subagent burned 764 thinking events / 55 assistant turns then ended with `result` envelope = `API Error: Request rejected (429) · jasonpeng2019 reached session usage limit (ref 940aa3e2…)`. No report produced; gate NOT met. Archived as `subagent.stdout.r1.jsonl` etc. | ⛔ blocked → rerun |
| 0.5 (r2) | unblock confirmation (retry) | 2026-08-19 | 0 | evidence/0.5/ | ✅ all six behaviors PASS + gate PASS (indep. verification): 2-lane concurrency (lane/alpha + lane/beta branches, each lane's own artifact, no cross-lane commits); PROVIDER_STARTED/EXITED ×2 real pids + real session UUIDs, COMPLETED/exit 0; real-adapter transcript parse → STARTED/COMPLETED both lanes; result_validation MISSING both lanes; `--resume 7288e624-…` recalled "HELLO FROM LANE A" (rc 0); `watch` → exit 3 + WATCH_TIMEOUT; gate: `--verbose` + `--permission-mode bypassPermissions` in argv, redirect via config_overrides alone (env stripped first), no 429s this run | ✅ done — **phase-0 gate MET** |

Decisions (user did not answer the plan's open questions before directing to proceed;
coordinator took the plan's recommended options, documented for veto):
- **0.2:** default `permission_mode=bypassPermissions` for headless claude lanes +
  `permission_denied` detection → non-COMPLETED.
- **0.3:** honor `config_overrides` via child env / supported flags (incl.
  ANTHROPIC_BASE_URL redirect) + reject unhonorable fields with InvocationValidationError.

Constraint: subagent launches and their nested claude subprocesses are process-scoped
(env vars + CLAUDE_CONFIG_DIR); no global Claude Code settings are ever touched.
