# Firmware suite rules

This directory is a self-contained firmware-evaluation package. Do not read files above
`Firmware/` when planning, launching, reviewing, or resuming the suite. Official internet sources
and installed provider/toolchain executables remain allowed.

- Start with `README.md`, `PROVIDER_ADAPTER.md`, then `.codex/skills/run-firmware-test-suite/SKILL.md`
  and the selected section of `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`.
- Treat `target-harness/` as the only product harness under test. It must be prepared by the external
  run owner before the test orchestrator starts. Never substitute a parent or stable-development
  harness.
- Treat `multi-agent-logs/` as imported historical progress/evidence, not live process, lease,
  authorization, configuration, or watcher state. Never launch Q11; live continuation requires the
  new authority described in `.agent-workspace/SUITE_COORDINATION.md`.
- For a possible BYO-Firmware-MCP defect, first preserve and classify the reproducer under
  `run-firmware-test-suite`. Only a manager-verified production-code defect may enter the direct
  `$plan-changes` then `$change-loop` repair route. Do not use that route for firmware, fixture,
  SDK, host, evidence, documentation, or metadata work.
- Fresh firmware doers may inspect only their assigned `fresh-experiments/<run>/` worktree and its
  explicitly copied inputs. They may not inspect the catalog, product harness, server source, or
  another run.
- Do not operate hardware without a current user instruction authorizing hardware testing and a
  matching recorded scope in `.agent-workspace/USER_DELEGATED_AUTHORIZATION.md`.
- Use the WIP target's bounded `watch --until-actionable` command and separate owner-bound
  `harness_watcher_implementation` process. The stable-only managed-watcher/heartbeat interface is
  not part of the product target.
- Keep runtime state in the paths declared by the skill and `.gitignore`; do not write runtime state
  into `Firmware resources/` or `multi-agent-logs/`.
