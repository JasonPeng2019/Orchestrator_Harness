# Firmware Resources

This is a convenient **copy library** of shared firmware-testing inputs and documentation. The
original files remain in their existing repository locations and remain authoritative.

This folder contains no experiment status, build output, run evidence, runtime logs, watcher state,
or fresh-experiment project trees.

## Start here

1. Read `test-program/BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md` for the complete evaluation plan,
   fixture contract, experiment catalog, pass gates, and hardware references.
2. Read `test-program/run-firmware-test-suite/SKILL.md` and its `references/` for the suite execution
   procedure.
3. Use `datasheets/`, `device-packs/`, and `fixture-and-toolchain/` as immutable inputs. Verify the
   file hash against `SOURCE_MANIFEST.csv` before relying on a copy.
4. Use `server-guides/` for the BYO-Firmware-MCP interfaces and setup contracts.
5. Use `orchestration-guides/` for the native harness and diagnostic watcher.

## Contents

### `datasheets/`

- STM32L476RG device PDF.
- nRF52840 product specification.
- SX1261/SX1262 device PDF.
- Waveshare LoRa module PDF.

Only one hash-unique copy of each shared PDF is retained here even when many experiment folders
contain the same bytes.

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

- The master end-to-end experiment guide.
- A complete copy of the `run-firmware-test-suite` skill, including its execution contracts,
  roster, model-continuity rules, result contract, and reusable scripts.

### `sprint-documentation/`

- `current/`: current sprint specifications and checklist copies.
- `archive/`: completed sprint, logging, watcher, and harness repair-plan copies.

These are planning/reference snapshots, not live authority or proof that a sprint passed. Consult
the original active plan and actual retained evidence before making a live decision.

### `server-guides/`

Shared BYO-Firmware-MCP README, operator guide, architecture, client contract, plan-tool contract,
and CMSIS-Pack admission design.

### `orchestration-guides/`

Harness/watcher specifications and quick-use rules. These are documentation copies only; production
code remains in `orchestrator_harness/`, `harness_common/`, and
`harness_watcher_implementation/`.

## Copy policy

- Do not write runtime output here.
- Do not treat a copied plan as current authority.
- Do not edit a copy and assume the source changed.
- When intentionally refreshing a resource, copy from its authoritative source and regenerate
  `SOURCE_MANIFEST.csv`.
- Do not copy entire `fresh-experiments/` runs, `.agent-workspace/`, logs, evidence, build trees,
  caches, virtual environments, or hardware runtime state into this library.

`SOURCE_MANIFEST.csv` records the source path, destination path, byte count, and SHA-256 of every
copied resource. Authored index/reference documents such as this README and `CONNECTED_HARDWARE.md`
are not source-copy manifest entries.

