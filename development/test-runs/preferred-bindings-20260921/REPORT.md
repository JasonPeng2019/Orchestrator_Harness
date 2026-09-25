# Preferred-role live launch verification

Date: 2026-09-21. VERIFY: PASS (focused live launch/tool/result/cleanup scope).

All 13 launchable preferred roles completed through the native multi-agent harness.
ROOT is this existing assistant session and is not a launch target. No fallback
was launched; no benchmark, memory-product implementation or learned selector ran.

| Role | Exact requested model | Effort | Transport | Result |
| --- | --- | --- | --- | --- |
| reviewer | `gpt-5.6-terra` | max | codex | PASS |
| test_claude | `claude-sonnet-5` | high | claude-code | PASS |
| test_heavy | `gpt-5.6-terra` | high | codex | PASS |
| test_middle | `gpt-5.6-terra` | low | codex | PASS |
| test_reviewer | `gpt-5.6-terra` | low | codex | PASS |
| test_root | `gpt-5.6-terra` | high | codex | PASS |
| test_routine | `gpt-5.6-luna` | high | codex | PASS |
| apc_a | `deepseek-v4.1-flash:cloud` | max | Ollama → Codex | PASS |
| apc_b | `deepseek-v4.1-flash:cloud` | max | Ollama → Codex | PASS |
| complex_writer | `glm-5.3:cloud` | xhigh | Ollama → Codex | PASS |
| routine | `deepseek-v4.1-flash:cloud` | high | Ollama → Codex | PASS |
| test_author | `glm-5.3:cloud` | xhigh | Ollama → Codex | PASS |
| writer | `deepseek-v4.1-flash:cloud` | max | Ollama → Codex | PASS |

## What PASS means

Each role got its own task card, branch/worktree, invocation and native provider
session. A real local tool computed a role-specific arithmetic challenge and
wrote proof plus RESULT.json. The read-only audit independently checked the
answer, role, lane/run identity, canonical SHA256, native valid-result state,
recorded model/configuration, launch command, tool execution, zero provider exit
and proven process-tree cleanup. Both runtimes returned SHUTDOWN_OK/CLOSED;
all 13 lanes are retired with cleanup_proven=true.

Evidence: [audit-results.json](audit-results.json), [audit_results.py](audit_results.py),
[cards](cards/), and native records under each workspace's ignored .harness-runtime.
The audit command is `python -B audit_results.py` from this directory; it exits 0
only when every mapped launchable role has passing evidence.

This is launch smoke evidence, not coding/test-authoring quality, nested testing
ROOT behavior, APC adaptation, native resume, backend reasoning-token behavior,
or a full product/release gate. Exact effort/tier forwarding and CLI acceptance
were checked; this does not establish an Ollama backend's internal service-tier
or reasoning semantics.

## Failures encountered and corrections

1. Git initially refused a deeply nested Windows worktree path. Enabled
   `core.longpaths=true` locally in the disposable workspace clones, not globally.
   The original failed bootstrap created no worker invocation.
2. The previous mapping's logical `ollama` and `claude` IDs were not native
   adapter IDs. It also described an unimplemented argv-prefix resolver.
   The mapping now uses native `codex` / `claude-code` and explicit
   `launcher=ollama` for the six Ollama-backed roles.
3. The requested naive Ollama prefix would forward Codex's duplicate `-m`,
   which Ollama rejects. The master Codex adapter now handles the selected
   transport, passes the model to Ollama once, preserves other Codex arguments
   and resume identity, and adds noninteractive `--yes`. Direct Codex's full
   argument vector is regression-tested as unchanged. This uses the existing
   adapter; there is no extra runner, scheduler or fallback controller.
   See the [Ollama integration docs](https://docs.ollama.com/integrations/codex)
   and [v0.34.0 argument validation](https://raw.githubusercontent.com/ollama/ollama/v0.34.0/cmd/launch/codex.go).
4. DeepSeek writer/max initially struggled with shell quoting and RESULT hashing.
   ROOT sent one corrective assignment through native send-lane-notification;
   the worker acknowledged it, executed the supplied command, and completed.
   Later Ollama cards included a deterministic command up front. Thus writer's
   PASS is supervised completion, not an unassisted quality claim.

Models, efforts, normal tiers, fallback selections/order/triggers and reset-per-new-
launch rules did not change. Only native transport metadata was corrected.

## Master fix and synchronization

Authoritative edits are in references/harness-single (upstream HEAD remains
d679c1f792bd46e78a0bfcefc0e4991e43dfb409; repair is uncommitted):
two Codex launcher-binding copies, adapters/codex/README.md, and
orchestrator_harness/tests/test_codex_ollama_launch.py.
The same repair was synchronized into development/product/worktree_example/harness;
REUSE_MANIFEST.md records the exception. Existing product refresh edits were
preserved. No product runtime was upgraded or launched.

The tested disposable binding, master binding and product binding have identical
LF-normalized source SHA256:
98029e341f2a803cefe52ed4091a4031e2a820479aeaec66b412ac4578a053e8.
Their platform line endings differ. Catalog/registered copies match within each tree.

## Checks

- Test-first red: six new tests, two expected errors rejecting launcher=ollama.
- Master relevant regression suite: 100 tests PASS; [master-tests.log](master-tests.log).
  Command from references/harness-single:
  `python -B -m unittest -q orchestrator_harness.tests.test_codex_ollama_launch orchestrator_harness.tests.test_product_adapters_catalog orchestrator_harness.tests.test_v2_materialization orchestrator_harness.tests.test_operator_launch orchestrator_harness.tests.test_general_coding_docs.GeneralCodingDocumentationTests orchestrator_harness.tests.test_package_metadata.PackageMetadataStaticTests orchestrator_harness.tests.test_real_agent_isolation.RealAgentIsolationTests orchestrator_harness.tests.test_addendum3_product orchestrator_harness.tests.test_launch_lifecycle`.
  The emitted argparse usage error is an expected negative-test fixture; suite exit is 0.
- Product synchronized copy: first four modules in that command, 54 tests PASS.
- Fresh native read-only review: SHIP, no confirmed defects. Its coverage suggestion
  was vetted and used to strengthen the exact direct-Codex argv assertion.
- Formal compiler check: PASS, source hash unchanged
  b81317479f7c2f9bc7f00555fecb8e96f015bd662d9a4558b79987c637ea9fc4,
  no changed units/review candidates. Canonical plan validator PASS.
- Master and product git diff --check: PASS.
- Optional WSL/live-isolation and full release gates were not run; they are not
  credited by these native Windows launch checks.

## Retained state and limits

Runtime artifacts/worktrees are retained as evidence. Both monitors/providers
were stopped by native shutdown, not by broad process-name killing.

The final complex-writer completion notice
935761eaccd2447aa154769ea13363a0 remains pending in the *closed* epoch's retained
queue: ROOT recorded acceptance by lane ID and shut down before acknowledging
that notice. Post-shutdown acknowledgement correctly returned MANAGER_QUEUE_NO_EPOCH.
This is archival bookkeeping, not an active process or unfinished worker;
its acceptance, result and cleanup evidence are present. No queue file was edited.

Ollama launches shared the existing user provider home and were serialized.
The CLI refreshed its dedicated Codex Ollama profile/catalog. The user-level
config.toml SHA256 also changed during the first Ollama launch
(8dfe1a140585c3874900da8dac8192fb4ffa62e3d40838d8245feed5ddbb0696 to
c2ca4579edc55fca62f7355c42bc6be5900c5accec61c24aee3bbc83a526922b); no prelaunch content snapshot was taken,
so no exact semantic-diff claim is made. Provider-managed settings were left
intact. Recheck provider-home isolation before concurrent implementation dispatch.
