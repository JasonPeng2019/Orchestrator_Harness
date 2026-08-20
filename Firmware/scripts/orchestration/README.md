# Orchestration helpers

These are package-local helpers for the firmware suite:

- `build_server_snapshot.py` records the common server state used by concurrent test roles.
- `prompt_policy.py` validates the package's delegated-launch prompt policy.

No script in this directory launches a provider session. When the user later implements the
adapter described in [`../../PROVIDER_ADAPTER.md`](../../PROVIDER_ADAPTER.md), it must use the WIP
product in `target-harness/`. The imported `run_persistent_lane_r9.ps1` launcher is retained only
as a historical artifact under `Firmware resources/test-program/scripts/orchestration/`; it bypasses
the WIP lane controller and is not an accepted live-suite launcher.
