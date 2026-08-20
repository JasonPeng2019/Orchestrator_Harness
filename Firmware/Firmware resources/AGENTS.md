# Firmware resource-library rules

This directory is the package-local input/reference library, not a runtime root.

- Read `README.md` before using or refreshing resources.
- Use the top-level `Firmware/` catalog and `.codex/skills/run-firmware-test-suite/` as live
  authority.
- Treat `SOURCE_MANIFEST.csv` as provenance only; do not require access to a recorded source path.
- Never put logs, run evidence, build output, checkpoints, caches, installed packs, virtual
  environments, or live state here.
- Never copy an entire fresh experiment into this directory.
- `test-program/design_charter.md` is the live production-server repair charter. Other copied
  sprint and `test-program/` documents are historical snapshots only; they do not grant
  authorization or override the root catalog, canonical `.codex` skill, or current suite ledger.
- `server-guides/` is an exact checked reference mirror. The matching document under
  `../BYO-Firmware-MCP/` is the live server-document source; update it first and keep the mirror
  identical in the same change.
- Keep every runtime file and refreshed input inside `Firmware/`.
