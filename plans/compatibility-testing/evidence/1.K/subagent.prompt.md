# Task: Phase 1, Area 1.K — Config / prompt-bundle contract (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing
plan. You write and run **pure-Python `unittest` tests over fabricated config files and
prompt-bundle records**. You do NOT launch any `claude`/provider subprocess, you do NOT modify
any harness source module, and you do NOT "fix to green" — a test that reveals a real gap is a
valid, recorded outcome. Two of these items have a KNOWN plan-vs-reality divergence (see below);
your job is to pin the ACTUAL behavior in a green test and record the FINDING.

## Where you are

- Working dir (disposable clone, carries phase-0 fixes):
  `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run tests:
  ```bash
  cd "C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test"
  PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_config_bundle -v
  ```
- Model fixtures on the EXISTING suite — read FIRST to copy idioms exactly:
  - `orchestrator_harness/tests/test_config_store.py` — how `load_config` is driven from a
    temp JSON config file.
  - `orchestrator_harness/tests/test_s2_contract.py` — how `compose_prompt_bundle` /
    `bundle_from_record` / `prompt_bundle_record_from_paths` are used with real files under a
    run root.
  - `orchestrator_harness/tests/support.py`.

## Code under test (grep the bodies before asserting)

### `orchestrator_harness/config.py`
- `_number(raw, key, default, *, minimum)` (:62): non-numeric or bool → `ConfigError("{key} must
  be numeric")`; non-finite → error; **`value < minimum` → `ConfigError("{key} must be >=
  {minimum}")`** (it REJECTS, does not clamp).
- `_integer(raw, key, default, *, minimum)` (:74): bool or non-int → `ConfigError("{key} must be
  an integer")`; `value < minimum` → REJECTS.
- `_declared_relative_paths(raw, key, aliases)` (:83): a list containing any absolute path, any
  path with `".."` in its parts, any non-str, or any blank → `ConfigError("{key} must be a list
  of safe relative paths")`. `None`/absent → `()`; aliases consulted when key absent.
- `load_config(path, *, harness_root=None)` (:105): reads JSON; non-dict root → error; validates
  `suite_root`/`run_globs`/`workspace_relpath` (absolute or `..` rejected); cross-field rules:
  `request_critical_seconds >= request_warning_seconds` → error;
  `process_start_tolerance_seconds > 2` → error; removed policy keys emit
  `legacy_config_diagnostics` strings (no runtime effect).

### `orchestrator_harness/prompt_bundle.py`
- `_safe_component_path(path, root)` (:51): symlink → `PromptBundleError("...cannot be a
  symlink")`; resolved path not under `root` → `PromptBundleError("...escapes run root")`;
  not an existing regular file → `PromptBundleError("...must be an existing regular file")`.
- `compose_prompt_bundle(*, workflow_id, task_card_id, profile_id, components)` (:176): components
  are `PromptComponent` or `(id, bytes)` pairs; concatenates in order → `final_bytes`; computes
  `final_sha256` and `bundle_sha256`(=manifest digest). `PromptBundle.__post_init__` (:115) re-checks
  every binding (composed==final_bytes, sha matches, bundle_sha256==manifest_sha256, unique IDs).
- `prompt_bundle_record_from_paths(*, workflow_id, task_card_id, profile_id, paths, run_root)`
  (:285): builds a path-bound record from real files under `run_root` → `to_record()`.
- `bundle_from_record(record, *, run_root)` (:211): CLOSED shape — `set(record)` must equal the
  9-key required set, each component a 5-key closed shape with contiguous `ordinal`, a **path-bound**
  source under `run_root` whose bytes match `size` and `sha256`; reconstructs via
  `compose_prompt_bundle` and finally requires `bundle.to_record() == dict(record)` else
  `PromptBundleError("...manifest is stale or tampered")`.

### `orchestrator_harness/prompt.py`
- A **compatibility re-export shim only**: it re-exports `PROMPT_BUNDLE_SCHEMA`, `PromptBundle`,
  `PromptBundleError`, `PromptComponent`, `bundle_from_record`, `compose_prompt_bundle`,
  `prompt_bundle_record_from_paths` and declares `__all__`. **There are NO prompt template
  constants / template strings in this module.**

## What to build

Create ONE new test module: `orchestrator_harness/tests/test_compat_config_bundle.py`. One test
per feature ID:

1. **Q1** `load_config` numeric bounds. Write temp config JSONs and assert **ACTUAL** behavior:
   an out-of-range `poll_interval_seconds` (e.g. `0.0`, below the `0.05` minimum) and an
   out-of-range integer (e.g. `stable_read_retries: 0`) each raise `ConfigError("must be >= ...")`
   — the harness **REJECTS out-of-range, it does NOT clamp**. A non-numeric value → the "must be
   numeric"/"must be an integer" error. A valid in-range config loads and carries the exact value.
   > **PLAN-VS-REALITY DIVERGENCE — record as a FINDING.** The plan's Q1 text says "out-of-range
   > numbers clamp to bounds". Source `_number`/`_integer` (`config.py:62,74`) raise `ConfigError`
   > instead. This is *stricter/safer* (reject vs silently clamp) — note-severity. Do NOT try to
   > make a clamp pass; test the raise and file the finding.
2. **Q2** `_declared_relative_paths` / `load_config` path validation. Assert an absolute path and
   a `..`-traversal path in a declared-relative list (`record_paths` / `run_globs` /
   `workspace_relpath`) each raise `ConfigError`; a clean relative list loads. Cover the alias path
   (`observation_paths` → `record_paths`).
3. **Q14** `_safe_component_path` enforcement. Build a `run_root` temp dir; assert (a) a component
   path resolving OUTSIDE the root (e.g. `../escape.txt`) raises "escapes run root"; (b) a symlink
   component raises "cannot be a symlink" (skip that sub-case with `self.skipTest` if the OS/user
   cannot create a symlink — do NOT fail); (c) a non-existent / non-regular file raises "must be an
   existing regular file"; (d) a real in-root file resolves and returns the resolved path.
4. **Q15** `bundle_from_record` round-trip. Write ≥2 real component files under a temp `run_root`,
   build a record via `prompt_bundle_record_from_paths`, then `bundle_from_record(record,
   run_root=...)` → assert the reconstructed bundle's components are **byte-identical**, each
   `sha256`/`size` matches, `final_sha256` and `bundle_sha256` match, and `to_record()` equals the
   original record. Then tamper one component's on-disk bytes (or a digest in the record) → assert
   `PromptBundleError`.
5. **Q17** `prompt.py` surface. Assert **ACTUAL** behavior: `prompt.py` re-exports exactly its
   documented `__all__`, each exported name is the *same object* as in `prompt_bundle` (identity),
   and "composes without unresolved placeholders" is satisfied by `compose_prompt_bundle` producing
   a bundle whose `final_bytes` is the exact ordered concatenation of the component bytes (no
   template/placeholder substitution occurs — there are no templates). 
   > **PLAN-VS-REALITY DIVERGENCE — record as a FINDING.** The plan's Q17 text says to assert
   > "documented template constants / templates". `prompt.py` contains **no template constants** —
   > it is a pure compatibility re-export shim. Pin the re-export contract (this is the real Q17
   > surface) and file the finding. Note-severity.

Never edit source. If any OTHER behavior differs from the descriptions above (a fail-open —
out-of-root path accepted, tampered manifest accepted, out-of-range value silently accepted), that
is HIGHER severity — flag it clearly.

## Pass criterion

- New module green under the run command above.
- Re-run the model suite to confirm nothing shared is disturbed:
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_config_store -v`

## Evidence to leave behind

Into `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/plans/compatibility-testing/evidence/1.K/`:
- `test-run.log` — full `-v` output of your new module.
- `config-regression.log` — `-v` output of `test_config_store`.

## Final report (return as your last message)

A markdown table: one row per feature ID (Q1, Q2, Q14, Q15, Q17), each `PASS` / `FINDING`
(one-line what-differed) / `BLOCKED` (why) — Q1 and Q17 are EXPECTED to be `FINDING` rows. Then
the exact commands run, the test count, and the pass/fail tally. Do not modify any file outside
your new test module and the evidence dir.
