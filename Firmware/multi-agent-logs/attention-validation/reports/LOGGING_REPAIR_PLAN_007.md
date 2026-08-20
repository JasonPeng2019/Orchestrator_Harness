# Logging repair plan 007 — interruption-safe sprint records

## Goal

Make producer closing records reliable on Windows and make resumed-root invocation boundaries explicit, so an interrupted sprint cannot silently continue under an old invocation identity.

## Code change

1. Add `record-attention --metadata-file <path>` as a mutually exclusive alternative to inline `--metadata`.
2. Parse the file as one JSON object through the same allowlist/validation path as inline metadata. Reject missing, malformed, non-object, or conflicting inputs without writing a record.
3. Document a portable producer pattern: atomically write metadata JSON, invoke `--metadata-file`, verify exit 0, then remove only the temporary metadata file.
4. Document that every resumed root turn must use a new `manager_invocation_id` and write `MANAGER_INVOCATION_STARTED` before scanning or responding. Never infer or backfill the unknown interval.
5. Add CLI/unit tests for valid file input, mutual exclusion, malformed/non-object/missing file, disabled no-op, and byte-equivalent records versus inline metadata.

## Non-goals

- Do not infer IDE process liveness.
- Do not change causal classifications or deadlines.
- Do not build a codex-exec bridge.

## Verification

Run the watcher unit suite, focused CLI tests, compileall, Ruff F, focused Pyright, then a fresh host-only readiness correlation using only `--metadata-file` for lane endpoints and a fresh invocation marker.
