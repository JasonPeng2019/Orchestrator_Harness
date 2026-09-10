# Harness v2 Addendum 3 execution handoff

## Objective

Execute Addendum 3 through EDGE-007: implement all eight operational tweaks, complete repeated independent source-review loops, run the exhaustive applicable Windows feature/provider/profile matrix, and retain native macOS and native-storage Linux as explicit nonblocking gaps.

## Status

STEP-001 through STEP-005 are accepted at clean candidate `a29e5682161c9b261bf7ffa50bcd52cd4b6c79a0`. STEP-006 disposable readiness passed 38/38 and ROOT accepted `MI-NORMAL-LIVE-READINESS`; EDGE-006 remains active at `MI-NORMAL-LIVE-MATRIX`. `ATTEMPT-LIVE-MATRIX-WINDOWS-001` is intentionally halted at a safe checkpoint at the user's request. No real provider scenario or feature cell completed. The first live probe exposed `FINDING-LIVE-SETUP-001`; its repair is committed and ROOT-verified at `4b349691faa8bd88cd33a1ed0d6241f6eeca06bc`, but it has not yet passed independent review or integration and is therefore not yet the accepted candidate.

## Completed

- Admitted target `harness-single@f4328b177177a3aa71bf5f064b88ad6033b3d903` and frozen control plane `frozen-harness@4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`.
- Accepted DEL-001 at `73b9be572637b36a42886f9157b91adc12be7bad`, DEL-002 at `058cb40aea70ef96bbb6fff7ec1074deffc5479f`, and their initial integration at `f949d386873c546c588e1b2c720aba466f9579df`.
- Initial STEP-005 CHECKER passed U1-U5 (15/15), product discovery (234/236 with two named environment skips), watcher discovery (100/100), compile/import/diff checks.
- Initial P11 audit found FINAL-REV-001 through FINAL-REV-005: managed dual-source watch wake, early native-session capture, validated-result monitor precedence, serialized inbox append, and truthful resume-to-launch state.
- PRODUCT_WRITER repaired all five in commit `a29e5682161c9b261bf7ffa50bcd52cd4b6c79a0`; producer evidence passed 20 focused tests, 57 affected tests, and 245 product tests with two environment skips.
- Independent mapped Claude Opus review closed all five findings with no new finding; handoff SHA-256 `5238395bfc343c249cc16585780bfe75cb6a3221481116c3ba16daacdca751c3`.
- Mapped INTEGRATOR fast-forwarded the exact reviewed tip and produced frozen-valid result SHA-256 `85b4880f676d3e33b74d44223290052d2dbc7e8ffb0ab639222f1085cec95cca`; integration handoff SHA-256 `5ae00101750a417785d737ba851532722604ed4ffcc899a08af002e92b8b836b`.
- Recorded one non-reproduced Windows teardown race: a provider test briefly retained `stderr.txt`; the exact isolated retry passed and the complete 37-test affected set then passed. No matching process remained and no product bytes changed.
- Series 2 CHECKER passed U1-U5 15/15, product discovery 243/245 with two named skips, compile, 13 imports, three provider-binding parses, diff/tip/status, and preserved 100/100 watcher credit. Frozen result SHA-256 is `495cdd33f4001e450b1c530b9b26ef3ca9fabc0558620b3cc28f1f9fb631ed32`.
- Mandatory mapped Claude Opus P11 follow-up re-derived all five closures from actual source and returned PASS with zero findings at handoff SHA-256 `3ceae342626c190ef625cfdde15b9e8ff7060b6478e0c0d267363c9ae0a4d0cf`. ROOT dispositioned its three nonmaterial observations and joined the pool once.
- The mapped Series 2 verdict-evidence CHECKER validated six exact hashes, two pool members, ten safeguard units, five closures, zero findings, and three ROOT dispositions with no discrepancy. Frozen result SHA-256 is `0b7085386cb350ffbbda3a3c9010a43e457b946e324591abb2324407a241334a`.
- ROOT published `RESULT-STATIC-ACCEPTANCE-RECONCILED-002.json=ACCEPTED`, cleared REQ-021, retained native macOS/Linux qualification gaps, and activated EDGE-006.
- Mapped CHECKER ran the local-fake-only disposable readiness profile once and passed all 38 identity, checkpoint, binding, abort, recovery, containment, and cleanup properties. Frozen result SHA-256 is `6cb0bea00102f3504574a94ff80b01cd89a6b41957c10393ea9c17a508774090`; handoff SHA-256 is `007deb4ea5d2157697e51bc9c14efc94be47b65aaa197c02bb570c5c0e7b70e1`.
- ROOT accepted `MI-NORMAL-LIVE-READINESS`. Recorded fake child PIDs 31220 and 41456 and frozen controller/provider PIDs 42856 and 28864 were absent after completion; the exact candidate remained clean. This readiness proof is synthetic and does not satisfy REQ-017.
- ROOT recorded `M09-WINDOWS-ADMISSION-001.json` for Codex, Claude Code, and Qwen Code in managed and plain profiles on the current Windows runner. The admitted target versions/configuration hashes and 96-cell scope are durable in that record.
- The first mapped executor was interrupted before real execution when its observer exited. The recovery executor then entered a repeated `tick_tock` compute loop and produced no scenario, manifest, result, or handoff; both executor process identities are absent and `EXECUTOR-COMPUTE-FAILURE-002.json` records the terminal agent failure.
- A ROOT-prepared, source-external target runner now compiles at `w/addendum-3-epoch-001/live-execution/.agent-workspace/run-live-target.py`. It creates a fresh candidate-bound harness root and Git workspace, exercises public setup/health/bootstrap/launch/assignment/review/retire/shutdown routes, runs a real provider without a timeout, and retains provider/result/hook/queue/process evidence before retirement. `finish-target-probe.py` validates the first target and emits the frozen result contract.
- Two mapped-primary Claude Opus observer launches terminated without a readiness/result artifact and are recorded in `OBSERVER-FAILURE-003.json` and `OBSERVER-FAILURE-004.json`. BOUND-005 therefore permitted the mapped Terra fallback for that launch. It created a valid detached observer marker and handoff for PID 33624 before the first target probe.
- The first real-target orchestration probe reached public setup but launched no provider: first setup returned `SETUP_OK`; the immediate unchanged second setup returned `SETUP_ADAPTER_COLLISION` for `.claude/orchestrator-harness-binding.json`. ROOT shut the target down, verified monitor PID 32096 absent, retained the target, recorded `RESULT-LIVE-PROBE-003.json`, and classified `FINDING-LIVE-SETUP-001` as a product behavior failure against the master spec's setup-idempotence requirement.
- The mapped PRODUCT_WRITER repaired only `FINDING-LIVE-SETUP-001` and committed exact clean tip `4b349691faa8bd88cd33a1ed0d6241f6eeca06bc` on `tier4-addendum3/live-setup-idempotence-patch-001`. The repair accepts byte-identical installed payloads and exact current-runtime materialized bindings on an unchanged rerun while retaining collision refusal for changed or foreign destinations. It adds focused unchanged-rerun, changed-payload, and foreign-binding regressions.
- ROOT independently verified the repair: 13 focused materialization tests passed, 29 affected setup/monitor/root-hook tests passed, full product discovery ran 248 tests successfully with the two documented environment skips, diff hygiene passed, and the repair worktree is clean. Durable evidence is `ROOT-VERIFICATION-LIVE-SETUP-PATCH-001.json` (SHA-256 `ec7790d3064ebd6ba88f2754b0342a2382ef38062b0747598ceccbf80fed7893`).
- The initial PRODUCT_WRITER provider entered a repeated compute loop after committing and never wrote the result contract; `PRODUCT-WRITER-COMPUTE-FAILURE-001.json` records that terminal failure. A deliberately narrow same-primary recovery then exited 0 at the controller level but its helper resolved the repository root one parent too high and failed to find the ROOT verification record, so it produced no handoff/result. The recovery controller and provider PIDs 33556 and 3092 are absent and no claim remains. This is an evidence-finalization defect only; product bytes and the verified commit are intact.

## Safe stopping checkpoint

- The live experiment is halted. `EXPERIMENT_HALTED.json` (SHA-256 `fda0d8184e86c4b3051b9ed4439d096afa91fff0f88dbea7e4a6e02e18d59a8e`) records zero completed real-provider scenarios/cells and the retained failed `codex-managed` target.
- The observer is contained. PID 33624 is absent and `CONTAINMENT_SIGNAL.json` (SHA-256 `9e297c5daccaa3a5d568e51628c3eb99d9e167a7259a7670d902054e72ffe21e`) prevents an accidental observer-loop restart from resuming the old attempt.
- Every PID found in current execution, observation, patch-controller, target-monitor, and test-target evidence was checked and is absent: 3092, 7772, 13716, 14940, 16792, 18680, 22952, 26484, 26868, 29468, 32096, 33556, 33624, and 35128.
- The retained target monitor says `health=STOPPED` and `stop_requested=true`. The coding resource-lock directory contains zero claims. The live-execution, live-observation, and repair worktrees are tracked-clean; ignored evidence is intentionally retained.

## Verification

- `python -m py_compile orchestrator_harness/scan_watch.py orchestrator_harness/controller.py orchestrator_harness/monitor.py orchestrator_harness/manager_queue.py orchestrator_harness/resume.py orchestrator_harness/launch.py orchestrator_harness/tests/test_addendum3_product.py` — PASS.
- `python -m unittest orchestrator_harness.tests.test_addendum3_product` — 20 PASS.
- Eight directly affected neighbor modules — 37 PASS in the terminal integration run.
- Exact isolated Windows job-boundary retry — 1 PASS in 1.052s.
- `git diff --check f949d386873c546c588e1b2c720aba466f9579df..HEAD` — PASS.
- Candidate HEAD equals `a29e5682161c9b261bf7ffa50bcd52cd4b6c79a0`; worktree clean; controller/provider PIDs absent.
- Repair HEAD equals `4b349691faa8bd88cd33a1ed0d6241f6eeca06bc`; repair worktree clean.
- `python -m unittest orchestrator_harness.tests.test_v2_materialization -v` at the repair tip — 13 PASS.
- Five affected setup/monitor/root-hook modules at the repair tip — 29 PASS.
- Full product discovery at the repair tip — 248 successful with two documented environment skips.
- `git diff --check a29e5682161c9b261bf7ffa50bcd52cd4b6c79a0..4b349691faa8bd88cd33a1ed0d6241f6eeca06bc` — PASS.
- Halt audit — all 14 evidence-derived PIDs absent; zero coding claims; retained monitor STOPPED.

## Remaining

- Correct the ignored `finalize-result.py` root calculation from `WORKTREE.parents[3]` to `WORKTREE.parents[2]`, rerun the mapped PRODUCT_WRITER primary recovery to create a frozen-valid producer result/handoff, and record its exact hashes. Do not change or recommit product files.
- Independently review exact repair tip `4b349691faa8bd88cd33a1ed0d6241f6eeca06bc`, disposition any finding, integrate the reviewed tip, and run affected readiness before restarting live work.
- Allocate a fresh observer-first Windows live attempt. Remove the old containment marker only as part of that deliberate restart, update the runner to the newly accepted candidate, retain the failed target, and use a fresh target suffix when rerunning `codex-managed` from CHECK-LIVE-5.
- Execute every applicable real Windows provider/profile matrix cell with observer-first practical lanes and complete artifacts.
- Record `GAP-NATIVE-MACOS` and `GAP-NATIVE-LINUX`; keep `cross_platform_qualification=INCOMPLETE` without blocking Windows completion or EDGE-007.
- Complete final live verdict, requirement-by-requirement acceptance audit, exact process/claim/worktree cleanup, and goal closure.

## Important assumptions

- Use frozen-harness as the only agent control plane; re-read `master_planning/SUBAGENT_ROLE_MODEL_MAPPING.json` before every lane/module/launch. Every mapped DeepSeek invocation includes `model_auto_compact_token_limit=280000`.
- User authorization covers workspace-local worktrees, branches, commits, integration, agents, applicable real Windows provider runs, review, and cleanup. It excludes push/publication/deployment/external communication, edits to frozen-harness, edits to the user-owned role map, and credential disclosure.
- `.agent/bounded-commands.txt` selects no commands. Never route agent sessions through the bounded wrapper.

## Relevant files

- `goal.md`
- `master_planning/harness-v2-tier4/addendum-3/steps/STEP-005.md`
- `master_planning/harness-v2-tier4/addendum-3/modules/M07.md`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-MI-FL2-S1-FINAL-PRODUCT-INTEGRATE.json`
- `w/addendum-3-epoch-001/final-product-integrate/.agent-workspace/HANDOFF-FL2-S1-FINAL-PRODUCT-INTEGRATE.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/DECISION-MI-NORMAL-LIVE-READINESS.json`
- `w/addendum-3-epoch-001/live-readiness/.agent-workspace/HANDOFF-LIVE-READINESS.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/FINDING-LIVE-SETUP-001.json`
- `.agent-runtime/harness-v2-tier4-addendum-3-epoch-001/ROOT-VERIFICATION-LIVE-SETUP-PATCH-001.json`
- `w/addendum-3-epoch-001/live-setup-idempotence-patch/.agent-workspace/finalize-result.py`
- `w/addendum-3-epoch-001/live-execution/.agent-workspace/EXPERIMENT_HALTED.json`
- `w/addendum-3-epoch-001/live-observation/.agent-workspace/CONTAINMENT_SIGNAL.json`

## Next action

Resume only when requested. First fix the ignored recovery helper's repository-root calculation, re-read `master_planning/SUBAGENT_ROLE_MODEL_MAPPING.json`, and launch the mapped PRODUCT_WRITER primary on the narrow result-finalization recovery. Once the frozen-valid producer result exists, update this handoff and begin an independent review of exact repair tip `4b349691faa8bd88cd33a1ed0d6241f6eeca06bc`. Do not restart an observer or real-provider target before the repair is reviewed, integrated, and readiness-checked.
