# Firmware Resources

This is the package-local library of shared firmware-testing inputs and background documentation.
The canonical live catalog and skill are the sibling files under the `Firmware/` root; no parent
repository is required.

This folder contains no experiment status, build output, run evidence, runtime logs, watcher state,
or fresh-experiment project trees.

## Start here

1. Read `../BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` for the complete evaluation plan, fixture
   contract, experiment catalog, pass gates, and hardware references.
2. Read `../.codex/skills/run-firmware-test-suite/SKILL.md` and its `references/` for the suite
   execution procedure.
3. Use `datasheets/`, `device-packs/`, and `fixture-and-toolchain/` as package-local inputs.
4. Read `../BYO-Firmware-MCP/README.md` and `../BYO-Firmware-MCP/SERVER_GUIDE.md` for the live
   BYO-Firmware-MCP interfaces and setup contracts. `server-guides/` is an exact checked mirror for
   package-local reference, not a second authority.
5. Use `../scripts/orchestration/` for current package helpers.

## Contents

### `datasheets/`

- STM32L476RG device PDF.
- nRF52840 product specification.
- SX1261/SX1262 device PDF.
- Waveshare LoRa module PDF.

Only one package copy of each shared PDF is retained here even when many experiments use it.

### `device-packs/`

- Keil STM32L4 device-family pack used by the STM32 setup work.
- Nordic nRF device-family pack used by the nRF setup work.

These are copied package inputs, not installed package state or a package cache.

### `fixture-and-toolchain/`

- `CONNECTED_HARDWARE.md`: four-board topology, stable identities, I2C wiring, and nRF/CoreSX1262 pin mapping.
- Fixed nRF/SX126x pin mapping.
- ARM toolchain lock declaration.
- nRF Connect SDK lock declaration.

### `test-program/`

`design_charter.md` is the live package-local constraint for production-server repairs. The other
catalog, skill, and orchestration-script files in this directory are historical import copies
retained for comparison; use the root catalog, `.codex/skills/`, and `scripts/orchestration/`
named in **Start here** for suite execution.

### `sprint-documentation/`

- `current/`: imported M5-era sprint specifications and checklist copies; the directory name is
  retained for provenance, not as a current-authority claim.
- `archive/`: completed sprint, logging, watcher, and harness repair-plan copies.

These are planning/reference snapshots, not live suite authority or proof that a sprint passed.

### `server-guides/`

Exact checked copies of the BYO-Firmware-MCP README, operator guide, architecture, client contract,
plan-tool contract, and CMSIS-Pack admission design. Edit the corresponding file under
`../BYO-Firmware-MCP/` first, then refresh this mirror in the same change. The package audit rejects
a stale or independently edited mirror.

## Copy policy

- Do not write runtime output here.
- Do not treat a historical copied plan as current authority.
- Update the root catalog or the canonical skill under `../.codex/skills/`, not the historical
  `test-program/` copies.
- Update a live server document under `../BYO-Firmware-MCP/` first, then keep its
  `server-guides/` mirror identical. Never use the mirror as an independent source of behavior.
- When intentionally refreshing an imported resource, update `SOURCE_MANIFEST.csv` as provenance.
- Do not copy entire `fresh-experiments/` runs, `.agent-workspace/`, logs, evidence, build trees,
  caches, virtual environments, or hardware runtime state into this library.

`SOURCE_MANIFEST.csv` is retained provenance for imported resources. Runtime use does not require
access to any source path recorded there.

