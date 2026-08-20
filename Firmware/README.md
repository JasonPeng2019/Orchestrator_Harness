# Firmware evaluation package

This directory contains the firmware experiment catalog, the BYO-Firmware-MCP server, package-local
Codex skills, shared firmware inputs, orchestration helpers, and imported progress records. A test
orchestrator launched from this directory does not need filesystem access above `Firmware/`.
Official internet references and installed provider, SDK, compiler, and hardware-tool executables
remain available when the selected test permits them.

## Start with the right authority

Use one live authority for each question:

| Need | Read or use |
|---|---|
| Run or resume the evaluation | `.codex/skills/run-firmware-test-suite/SKILL.md`, then the selected section of `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` |
| Understand the current MCP server and its client workflow | `BYO-Firmware-MCP/README.md`, then `BYO-Firmware-MCP/SERVER_GUIDE.md` and its linked contracts |
| Repair a verified production-server defect | `Firmware resources/test-program/design_charter.md`, then `$plan-changes` and `$change-loop` under `.codex/skills/` |
| Find the current suite position and permitted next action | `.agent-workspace/SUITE_COORDINATION.md`; use `multi-agent-logs/` only as imported historical evidence |

The server documents in `Firmware resources/server-guides/` are checked mirrors for package-local
reference. They are not a second live authority; edit the matching document in `BYO-Firmware-MCP/`
first and keep the mirror identical.

## Live layout

- `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`: experiment catalog and acceptance contract.
- `.codex/skills/run-firmware-test-suite/`: canonical execution skill and contracts.
- `.codex/skills/plan-changes/` and `.codex/skills/change-loop/`: production-server repair workflow.
- `BYO-Firmware-MCP/`: production server under test.
- `Firmware resources/`: package-local datasheets, packs, fixture facts, guides, and repair charter.
- `scripts/orchestration/`: current package helpers.
- `multi-agent-logs/`: imported historical progress and evidence; never a live runtime root.
- `.agent-workspace/`: current campaign policy and coordination state.
- `fresh-experiments/`: runtime-created isolated firmware worktrees.
- `target-harness/`: runtime-supplied exact WIP product worktree under test.
- `runtime/`: package-level harness observations.

## Prepare a run

The external run owner creates or selects the exact WIP product worktree at `target-harness/`, then
launches the test orchestrator with `Firmware/` as its working directory. Before launching any role,
the orchestrator reads `.codex/skills/run-firmware-test-suite/SKILL.md` and runs its package audit
with `--require-target`.

If an experiment reports a possible MCP-server issue, do not patch the server from a firmware doer
or from a hunch. Preserve the reproducer, classify it under the suite skill, and use the repair
route above only after the manager verifies a production-code defect. Firmware, fixture, SDK,
host, evidence, documentation, and metadata issues stay outside that route.

The WIP product does not launch the high-level test orchestrator. Its lane controller launches
provider roles inside already prepared worktrees. Its bounded `watch --until-actionable` command
provides deterministic manager waits, while its separate owner-bound
`harness_watcher_implementation` process provides diagnostics. Do not use the stable harness's old
managed-watcher or heartbeat interface.

## External-plan-owner boundary

The external plan owner admits a selected scenario, supplies `target-harness/`, and later classifies
the suite's terminal handoff. The test orchestrator owns suite scheduling, doers, leases, MCP and
hardware actions, evidence, and any server-repair workflow. It must not accept the generic harness,
change the external plan, or promote a release; the external plan owner must not replace the suite
manager or run those campaign actions directly.

For provider/model/effort/tier allocation, adapter status, and launch-route rules, use the
[provider-adapter contract](PROVIDER_ADAPTER.md). Its Qwen Code/Ollama route is package-local under
`.qwen/`; it has passed no-hardware MCP probes but does not authorize a sprint. Terra's ROOT-only
evidence review remains outside Firmware suite state.

After a terminal sprint handoff, ROOT may independently run a root-only evidence reviewer to look
for a possible general-harness defect. That review is outside the Firmware suite: the test
orchestrator must not read, schedule, store, or act on its report. It remains responsible only for
firmware sprint execution and verified BYO-Firmware-MCP repairs.

## Current resume boundary

The imported `multi-agent-logs/` Q10 boundary is historical: Q10's manager evidence was insufficient
because wake records were ordered incorrectly and responses omitted lane IDs, while its evidence
showed no harness/watcher defect. Never launch Q11. This boundary must not override the current Plan
2 state. The operative position is
`.agent-workspace/SUITE_COORDINATION.md`: suites 003-008 are stopped, their durable evidence is
retained, and no old manager/provider identity, plan, permission, lease, claim, or hardware
authority is live.

ROOT has bound the clean package target at
`dd673cb304501bfc2228b8c44f41df45a0c8608f`. Plan 2 may continue at `EDGE-010R` through its one
focused repair and four-case no-hardware `CHECK-SPRINT-CONTINUATION`; it must not launch a live
manager first. After that check and affected exact-target M08 pass, ROOT may dispatch the prepared
continuation-aware manager input with exact selected sprint IDs/indices and fresh invocation
authority. Verified checkpoints may continue; stopped runtime authority may not.
