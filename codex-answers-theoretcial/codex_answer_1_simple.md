# Simple Generalization Answer

Keep the existing firmware feature and add normal coding support beside it.

The two paths should be separated by a small versioned contract:

- Existing firmware invocations keep their policy, server, MCP, relay, and hardware behavior.
- New coding invocations use Git branches and worktrees, merge-ready results, and generic named locks.
- Both paths share the reliable controller, process tracking, events, checkpoints, acknowledgements, and recovery code.

Do not build a large adapter or profile framework.

## Testing Cost

Keep the firmware tests required because firmware remains supported.

- The current orchestrator suite has 208 tests and takes about 28 seconds.
- The tests are synthetic and use no physical hardware.
- Preserving the firmware test path should add roughly 1–3 agent-hours during the conversion.
- Real hardware testing is needed only for releases or hardware-specific changes.

This is cheaper and safer than deleting the firmware code and untangling its extensive reconciliation and test coverage.
