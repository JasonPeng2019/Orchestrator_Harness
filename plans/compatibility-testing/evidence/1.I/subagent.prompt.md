# Task: Phase 1, Area 1.I — Provider adapter contract, non-argv (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated adapters / specs / argv**.
You do NOT launch any `claude`/provider subprocess, you do NOT modify any harness source module,
and you do NOT "fix to green" — a test that reveals a real gap is a valid, recorded outcome.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_provider_contract -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_provider_adapter_public_seams.py` — **your primary model**:
    registers a deterministic fake CLI adapter via `register_provider_adapter(...)`, exercises
    `redact_command`, `structured_handoff`, capabilities/unsupported ops, and **always cleans up
    with `unregister_provider_adapter("fake-cli")` in tearDown**. COPY THAT CLEANUP DISCIPLINE.
  - `orchestrator_harness/tests/test_provider_adapter_registry.py` — the versioned-registry
    contract model (`_validate_adapter_contract`, built-in Codex/Claude adapters).
  - `orchestrator_harness/tests/test_compat_provider_argv.py` / `test_compat_provider_allowlist.py`
    (phase-0 modules — argv/allowlist idioms).
- Code under test in `orchestrator_harness/provider.py` (grep bodies before asserting):
  `BaseProviderAdapter` (:170), `ProviderCapabilities` (:203), `ProviderOperationResult` (:258),
  `ProviderAdapterError` (:70), `_validate_adapter_contract` (:727), `register_provider_adapter`
  (:761) / `unregister_provider_adapter`, `classify_operation` (:863),
  `unsupported_operation_result` (:904), `provider_config_digest` (:927), `redact_command` (:965),
  `build_provider_evidence` (:1001), `structured_handoff` (:1042). Built-in adapter classes:
  `ClaudeCodeProviderAdapter`, `CodexProviderAdapter`.

## ⚠️ Registry hygiene (mandatory)

`register_provider_adapter` mutates a **process-global** registry shared with every other test
module. Any adapter you register in a test MUST be removed with `unregister_provider_adapter(...)`
in `tearDown` (or `addCleanup`), exactly as `test_provider_adapter_public_seams.py` does. A
leaked registration will break other suites and fail the regression check — do not skip this.

## What to build

Create ONE new test module:
`orchestrator_harness/tests/test_compat_provider_contract.py`

One test per item:

1. **U5** shared contract shape: for both registered built-in adapters (Codex, Claude Code),
   assert `.capabilities()` returns a `ProviderCapabilities` and an operation result is a
   `ProviderOperationResult` with the documented fields.
2. **U7** `_validate_adapter_contract` rejects an incomplete adapter: define a structurally
   incomplete fake adapter (missing a required method/attr) and assert
   `register_provider_adapter` / `_validate_adapter_contract` raises `ProviderAdapterError`
   (verify the real message). Register-and-cleanup only if registration succeeds.
3. **U8** unsupported-operation handling: `classify_operation(provider_id, "<unsupported-op>")`
   returns a `ProviderOperationResult` with `supported=False` (graceful, not a crash). ALSO note:
   `unsupported_operation_result(...)` itself **raises** `ProviderAdapterError` for an unknown op
   (this is the same latent behavior recorded as finding **F1A-C24-1** — cross-reference it, do
   not re-file a duplicate; just assert both the graceful `classify_operation` path and the raise).
4. **U9** `provider_config_digest`: identical `ProviderLaunchSpec` → identical digest; change one
   field → different digest (stable, deterministic).
5. **U10** `redact_command` (and adapter `redact_argv`): an argv containing a secret-looking value
   (token/api-key/password pattern) → the secret is redacted in the returned tokens before any
   logging/persist. Assert the raw secret does not survive.
6. **U11** `build_provider_evidence` / `structured_handoff`: assert the evidence record shape
   (identity/version/capabilities/digest/session/redacted provenance) AND that no secret appears
   anywhere in the record.

If a contract/redaction behaves differently than U5–U11 describe (a secret survives redaction —
**HIGHER severity, flag clearly**; a digest is unstable; a contract gap admits a bad adapter),
**do not invent behavior** — document ACTUAL behavior in a green test and record a FINDING
(feature ID, input, expected vs. observed, `provider.py:<line>`). Never edit source.

## Pass criterion

- New module green under the run command above.
- Re-run the model suites to confirm the shared registry is undisturbed (this catches a leaked
  registration):
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_provider_adapter_public_seams orchestrator_harness.tests.test_provider_adapter_registry -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.I/`:
- `test-run.log` — full `-v` output of your new module.
- `provider-regression.log` — `-v` output of re-running the two model suites.

## Final report (return as your last message)

A markdown table: one row per feature ID (U5, U7–U11), each `PASS` / `FINDING` (one-line
what-differed) / `BLOCKED` (why). Then the exact commands run, the test count, and the pass/fail
tally. Do not modify any file outside your new test module and the evidence dir.
