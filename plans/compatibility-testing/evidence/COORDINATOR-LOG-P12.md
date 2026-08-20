# Coordinator log — Phases 1 & 2 (compatibility-testing plan)

Detection-only test suite (TB-NS-V + TB-SC-logic + plain-TB-NS). Each row = one subagent
that authors a `test_compat_<area>.py` unit module in the clone and runs it. **No live
`claude` lanes** — pure Python over fabricated inputs. Subagents launched via the native
`claude` CLI on the local Ollama backend (`deepseek-v4-flash:0731-cloud`), `--effort high`,
env-scoped launcher + `CLAUDE_CONFIG_DIR` into the clone (per `subagent-launch-local-only`).
Convention: a mutation that is NOT rejected as the plan expects is a **FINDING** (recorded in
`evidence/FINDINGS.md`), never fixed to green. Coordinator independently re-runs each module
+ checks `git status` (only the new test module may appear) before accepting.

Clone: `harness-single-worktrees/compat-test` (branch `compat-test-copy`), carries phase-0 fixes.
Run cmd: `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.<module> -v`

| Area | Features | Module | Tests | Findings | Verification | Status |
|---|---|---|---|---|---|---|
| 1.A | C2–C24 invocation validation | test_compat_invocation_rules | 19 | F1A-C24-1 (note) | ✅ indep. re-run 19/19 OK; git shows only new module; finding confirmed in source (provider.py:908 raises, lane_controller.py:1692 branch dead) | ✅ done |
| 1.B | B1–B8,B15,B16 CLI subcommands | test_compat_cli_subcommands | 10 | F1B-B2-1 (note) | ✅ indep. re-run 10/10 OK; git shows only new module; B2 finding confirmed (cli.py:439 scan dispatch ignores --no-write, :82 no param); B16 archive-first ordering observed via _before_git_close seam | ✅ done |
| 1.C | D3–D20 task/result lifecycle | test_compat_task_lifecycle | 18 | none | ✅ indep. re-run 18/18 OK; git shows only new module; D15 REJECTED-non-terminal observation confirmed at task.py:600 | ✅ done |
| 1.D | E4–E20 git safety/result-merge | test_compat_git_safety | 13 | F1D-E19-1, F1D-E20-1 (both note) | ✅ indep. re-run 13/13 OK; git shows only new module; both findings confirmed in source (git_safety.py:370 gate scope, :415 only >256 bound) | ✅ done |
| 1.E | F3–F24 reconcile classification | test_compat_reconcile_classify | 13 | F1E-F3-1, F1E-F24-1 (both note) | ✅ indep. re-run 13/13 OK; git shows only new module; both findings confirmed in source (reconcile.py:1355 elevates only on RELAY_READY; discovery.py:566 coding-result memoized, :611 task-result not) | ✅ done |
| 1.F | G1–G32 notification/event taxonomy | test_compat_notification_taxonomy | 16 | F1F-G18-1, F1F-G1-1, F1F-G5-1 (all note) | ✅ indep. re-run 16/16 OK; git shows only new module; G1/G5 findings confirmed in source (notifications.py:1697 expiry WARNING/CRITICAL-only, :1727 OBSERVATION_ERROR active-lane gate); G18 declaration confirmed at :115 | ✅ done |
| 1.G | K2–K10 resume/handoff admission | test_compat_resume_admission | 11 | F1G-K8-1 (note) | ✅ indep. re-run 11/11 OK; regression test_s2_contract+test_handoff_preflight 27/27 OK; git shows only new module; K8 conflict-rejection confirmed in source (invocation.py:716-722). ⚠️ subagent 429'd mid-task (authored module, never ran it); coordinator repaired 2 fixture-authoring bugs to match actual behavior (continuation_start_commit constant; K5 digest-consistent tamper) — see evidence/1.G/COORDINATOR-NOTE.md | ✅ done |
| 1.H | H9,H10 resource-lock semantics | test_compat_resource_locks | 4 | none | ✅ indep. re-run 4/4 OK; regression test_resource_locks+test_reconcile 87/87 OK; git shows only new module; tests genuinely exercise acquire_all/on_wait CONTENDED blocking, claim-file persistence, resource_release_possible flag + RESOURCE_RELEASE_POSSIBLE emission, fail-closed STALE_STATUS contrast | ✅ done |
| 1.I | U5–U11 provider adapter (non-argv) | test_compat_provider_contract | 6 | none | ✅ indep. re-run 6/6 OK; regression public_seams+registry 40/40 OK (no leaked registration); git shows only new module; U10/U11 redaction verified (no secret survives any token or json.dumps(record)); U8 cross-refs F1A-C24-1 + confirms graceful classify_operation path. ⚠️ subagent killed at regression step (authoring done, self-verified green); coordinator finished acceptance — see evidence/1.I/COORDINATOR-NOTE.md | ✅ done |
| 1.J | N4,N5,N7 host adapter records | test_compat_host_adapters | 3 | none | ✅ indep. re-run 3/3 OK; regression test_s4_contract+test_s4_repair 68/68 OK (1 skipped); git shows only new module (host_adapters.py unmodified); tests build a live DeliveryCoordinator and drive real admit/deliver/block/declare/stop transitions; N5 gate confirmed in source (record_notification_final_response raises unless provided==expected exact actor/action set; stop constants imported not hardcoded); subagent completed cleanly (result envelope present, no external kill) | ✅ done |
| 1.K | Q1,Q2,Q14,Q15,Q17 config/prompt bundle | test_compat_config_bundle | 9 (1 skip) | F1K-Q1-1, F1K-Q17-1 (both note) | ✅ indep. re-run 8 pass/1 skip OK; regression test_config_store 12/12 OK; git shows only new module (config.py/prompt_bundle.py/prompt.py unmodified); both findings confirmed in source (config.py:62,74 raise-not-clamp; prompt.py is a 7-name re-export shim with no templates); Q15 has 4 fail-closed tamper gates (size/sha256/component-digest/manifest), Q17 pins verbatim concatenation with placeholder literals surviving; Q14 symlink sub-case skipped (WinError 1314, no privilege). ⚠️ first launch (b29kj1bvr) killed mid-probe with no module; re-launched fresh scratch (bejhxm8ye) → clean completion — see evidence/1.K/COORDINATOR-NOTE.md | ✅ done |
| 2.A | I4–I10 workspace overlay edges | test_compat_workspace_overlay | 19 | F2A-I4-1 (note) | ✅ indep. re-run 19/19 OK; regression test_workspace_overlay 30/30 OK; git shows only new module (workspace_overlay.py unmodified); tests drive real prepare/restore/verify seams over temp cache/target/receipt fixtures; I4 pins both actual behaviors (verify stays verified:True after byte corruption; restore catches it BLOCKED "later edit detected"); I8 injects a mid-apply MutationError via mock.patch on the imported mutation_replace and asserts byte-identical rollback + no receipt; I5 asserts no-partial-write on undeclared collision; I7 junction/reparse rejection runs (not skipped) on this host | ✅ done |
| 2.B | L1–L10, A25 capability broker | test_compat_capability_broker | 8 | F2B-L4-1, F2B-L7-1 (both note) | ✅ indep. re-run 8/8 OK; regression test_s5_capability_broker 27/27 OK; git shows only new module (capability_broker.py unmodified); tests drive the real default-deny request→approval→permit→adapter→cleanup pipeline over in-memory fixtures copied from test_s5; L2 frozen-snapshot/MappingProxy immutability + byte-stable round trip, L5 authority-alias fail-closed on AdapterResult/CleanupEvidence, L6/A25 claim→arm→cleanup→release ordering + no authority leak, L10 fail_dispatch→FAIL+release & cleanup_proved=False→UNCERTAIN+retain; both findings pin source-stricter-than-plan behavior (L4 no per-permit counter/replay refusal; L7 CapabilityAdapterUnavailable→DENIED SNAPSHOT_UNAVAILABLE). Subagent bz3njg6p9 (deepseek --effort high, scratch .subagent-scratch-2B) completed cleanly | ✅ done |
| 2.C | P1–P12 lane lifecycle | test_compat_lane_lifecycle (13 tests) | 13/13 OK | F2C-P7P11-1 (note) | coordinator re-ran 13/13 OK; regression test_s4_contract 21/21 OK (subagent's reported 1 "error" was a transient CIM/process-snapshot flake — passed on coordinator re-run); git status source-clean (lane_lifecycle.py untouched); module drives real seams, only process_snapshot patched for proof injection (same as model) | done |
| 2.D | O7–O9 operator launch/supervision | test_compat_operator_launch (5 tests) | 5/5 OK (2 skipped) | none | coordinator re-ran 5/5 OK; 2 skips are legitimate host-capability gaps (CIM full-inventory snapshot unavailable on this host; Windows exact-handle termination is internal to launch_process); git status source-clean (operator_launch.py untouched); module drives real seams (launch_process, detached_owner_snapshot, process_snapshot, targeted_process_query); decoy-protection O9 verified — wrong created_utc never signals | done |
| 2.E | A34 release-manifest assets | 10 | 10 | 0 | 0 | done — GAP F2E-A34-1; module green, release_assets.py source-clean, imports real seams |
| 2.F | A30/T6 attention sprint | 22 | 22 | 0 | 0 | done — PASS (no finding); module green, attention_sprint.py source-clean, imports real seam |
| 2.G | A31,A39/T3 watcher recovery | 19 | 19 | 0 | 0 | done — A31 PASS, A39/T3 GAP F2G-A39-1; module green, watcher_integration.py source-clean, imports real seams |
| 2.H | Q4 profile child environment | 5 | 5 | 0 | 0 | done — PASS (no finding); module green, profile.py source-clean, imports real seams |

## Findings summary
- **F1A-C24-1** (note): `_classify_provider_operations` unsupported-op record branch is dead
  code — `unsupported_operation_result` raises on the same condition. Cannot fire from a
  validated invocation.
- **F1D-E19-1** (note): the `RUNNING_CODEX`/`RUNNING_PROVIDER` gate (`git_safety.py:370`) is
  scoped to conflict detection; discovery-level result acceptance does NOT reject a valid
  result offered under `EXITED`/`PROVIDER_EXITED`.
- **F1D-E20-1** (note): no ">1 candidate result JSON" ambiguity rejection; `RESULT.json` is
  canonical and a second result-shaped JSON is silently ignored (only the >256 bound fires).
- **F1E-F3-1** (note): lane elevates to `WAITING_RELAY` only on a `RELAY_READY` request; a
  `RELAY_UNBOUND` request leaves the lane in `RUNNING_CODEX` (`reconcile.py:1355`).
- **F1E-F24-1** (note): validation memo covers only the coding-result path
  (`_validate_coding_result_cached`); the task-result path is not memoized.
- **F1F-G18-1** (note): `HARNESS_SCAN_COMMITTED` is a declared taxonomy/watcher kind but has no
  in-repo emitter; "once per scan commit" is observable only at the record-contract level.
- **F1F-G1-1** (note): `REQUEST_EXPIRY_WARNING` is selectable only for buckets WARNING/CRITICAL;
  an EXPIRED-bucket request is emitted but never selected (`notifications.py:1697`).
- **F1F-G5-1** (note): `OBSERVATION_ERROR` is emitted always but actionable only when a lane/
  request is live (`notifications.py:1727`).
- **F1B-B2-1** (note): `scan --no-write` flag is parsed but never read by the scan dispatch
  (`cli.py:439`); one-shot scan never persists anyway, so the flag is a harmless no-op.
- **F1G-K8-1** (note): the coding-v1 adapter fails *closed* on conflicting resume thread IDs
  (`invocation.py:716-722` raises `"conflicting requested resume thread IDs"`) rather than
  "canonical wins" as the plan described — safer than the plan text.
- **F1K-Q1-1** (note): out-of-range config numbers are *rejected* (`config.py:62,74` raise
  `ConfigError "must be >= …"`), not clamped as the plan Q1 text says — safer (fail-closed).
- **F1K-Q17-1** (note): `prompt.py` has no template constants; it is a 7-name re-export shim
  and `compose_prompt_bundle` concatenates verbatim (no placeholder substitution) — the plan
  Q17 "template constants" premise does not match the module.
- **F2A-I4-1** (note): `verify_overlay_receipt` is a structural/identity prelaunch check
  (REQ-O41) that never reads materialized worktree bytes — it returns `verified:True` even
  after a materialized byte is corrupted; byte-integrity is enforced only at `restore_worktree`
  (`workspace_overlay.py:789-795`, outcome `BLOCKED` "later edit detected"). The plan I4
  "re-verify → verification fails" premise overpromised the verify seam; both real behaviors
  are safe.
- **F2B-L4-1** (note): bounded single-use is broker-enforced, not a per-permit counter —
  `CapabilityPermit` has no `use_count`/`uses_remaining`; an exact retry reuses the cached
  terminal result (`dispatch_calls` stays 1) and reuse under changed semantics is refused
  (`REPLAY_MISMATCH`, durable `APPROVAL_REPLAY` via `_used_approvals`).
- **F2B-L7-1** (note): the broker catches an adapter's `CapabilityAdapterUnavailable` from
  `observe` and returns DENIED `SNAPSHOT_UNAVAILABLE` (`capability_broker.py:1400-1406`) rather
  than propagating; every fail-closed path constructs no permit and dispatches 0 times.
- All recorded in `evidence/FINDINGS.md`.

## Baseline
Clone full `unittest discover` = **533 tests, 6 errors, 1 skipped**. All 6 errors are in
`test_s6_public_release` (S6 public-release safeguard/selector — environment-dependent,
pre-existing in the clone, unrelated to any phase 1–2 module). Full log:
scratchpad `baseline-full.txt`. The per-module targeted runs are the acceptance signal, not
the whole-suite discover. NOTE: 2.E (release assets) is adjacent to S6 — verify carefully.
