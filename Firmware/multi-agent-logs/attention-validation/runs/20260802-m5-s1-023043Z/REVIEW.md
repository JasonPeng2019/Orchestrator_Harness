# M5 S1 Post-Sprint Review — 20260802-m5-s1-023043Z

Scope: durable artifacts only in the three requested epoch roots. This is advisory; no sprint disposition is made.

## Findings

1. **CRITICAL — diagnostic watcher did not remain live or cover the tested work.** `harness_watcher/.../owner-identity.json` says `exit_reason: owner-script-error`, `error: optional watcher exited before cooperative stop`, ending `02:33:13Z`. `watcher/service.json` records `service-error` at `02:33:09Z` with `stop_requested: false`; `watcher/events.jsonl` records `SERVICE_ERROR: 'str' object has no attribute 'get'`. The worker challenges/wakes occur later (e.g., Boreal harness observation `02:39:14Z`; further scans/wakes continue to cleanup about `02:51Z`). Thus its claimed diagnostic coverage is interrupted before the challenges and cannot validate the full sprint.

2. **HIGH — watcher evidence is additionally integrity-defective.** `watcher/attention-observation-errors.jsonl` records five Boreal rows whose `canonical source_record_sha256 does not bind source bytes`, including the Boreal challenge and completion. This prevents treating the watcher timeline/report as independently reconstructable for that source. No `ValueError` is evidenced in the requested roots: the durable service failure is the quoted `AttributeError`, not a poll `ValueError`.

3. **HIGH — required durable sprint evidence set is incomplete.** The specified `SPRINT_CHECKPOINT.md`, `CHALLENGES.json`, `PROCESS_REGISTRY.json`, and `ISOLATION.json` are absent from `multi-agent-logs/attention-validation/runs/20260802-m5-s1-023043Z`. Existing scattered metadata cannot replace the required complete challenge table, infrastructure identities/creation checks, forbidden-path audit, or root audit/cleanup narrative.

4. **HIGH — six-stage challenge reconstruction is insufficient as a complete set.** Harness attention records show four observed/actionable/attempted/delivered/acknowledged events and the manager metadata contains several receipt/claim/decision/response sidecars. But no durable challenge table correlates each event through worker-created blocked state, exact wait start/finish, receipt-first manager action, response receipt, useful-work resume, and one wake ID. The watcher report itself classifies 37 events as `INSUFFICIENT_EVIDENCE`. This is especially material for Boreal because the watcher's source-integrity errors cover it.

5. **MEDIUM — quiet control is evidenced; busy control validity is not fully demonstrated.** `QUIET_CONTROL.json` records `WATCH_TIMEOUT`, null wake ID, and `valid: true`, with matching quiet manager wait sidecars. `BUSY_WORK_AUDIT.json` records a real frozen-file audit from `02:45:37Z` to `02:46:23Z`, and busy start/finish sidecars exist. However, without a challenge table/interval correlation, the durable evidence does not show a genuine request created during that exact busy interval and later received by the production wait, as Stage 5 requires.

6. **MEDIUM — harness execution and cooperative cleanup have positive but incomplete evidence.** The managed harness shows a continuous 31-scan chain, `cursor_complete: true`, four delivered wakes and four successful acknowledgements; `managed-watch-runtime.json` records `stop-requested` at `02:50:57Z`. `CLEANUP_PROCESS_CHECK.json` records listed PIDs not alive. But process cleanup is PID-only in the retained check (no creation-identity matching), and there is no final process registry/isolation record proving every controller/helper/provider/MCP/lease scope or that no forbidden discovery path influenced the manager.

7. **LOW/POSITIVE — diagnostic-only evaluator isolation is supported only for its short live interval.** Watcher config sets `evaluator_enabled: false` with a must-not-run evaluator command; its events repeatedly record `EVALUATOR_SKIPPED` and no evaluator invocation appears in these roots. The sealed manifest declares AI evaluator, watcher subagent, collaboration notification, user message, and transcript inspection forbidden. This supports no evaluator use while the watcher was alive, but does not establish the absent full-sprint forbidden-path/isolation proof.

## Smallest evidence-oriented correction

Preserve this epoch, then repair/revalidate watcher owner/poll failure and source-hash binding before another counted invocation. For a new epoch, retain the required checkpoint, challenge table, process registry, and isolation/creation-identity cleanup proof; correlate quiet/busy and every worker challenge end-to-end without relying on post-hoc inference.
