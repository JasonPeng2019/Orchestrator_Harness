# Orchestrator Harness workspace

The runnable Harness v2 product lives in [`harness-single/`](harness-single/). Run every
operator command from that directory; the repository root is only a container for the product
and its supporting submodules.

Start with [`harness-single/QUICK_START.md`](harness-single/QUICK_START.md). In particular, copy
the two tracked examples from `harness-single/examples/` into the ignored
`harness-single/local-config/` directory and replace the example workspace path before running
setup. The repository root intentionally contains no runnable harness configuration.

The other top-level submodules are supporting projects, not alternate Harness v2 entry points:

- `Codex_Claude_Setup/` contains the portable agent-workspace source.
- `BYO-Firmware-MCP/` contains the separate firmware MCP project.

No command in this directory automatically selects either supporting project.
