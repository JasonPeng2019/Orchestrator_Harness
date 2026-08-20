# Task: Phase 2, Area 2.E — Release-manifest asset accessors (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** over the real `orchestrator_harness.release_assets`
module. No subprocess, no source edits, no "fix to green". Pin ACTUAL behavior.

> **READ THIS FIRST — PLAN-VS-REALITY DIVERGENCE (you MUST record it as a FINDING).**
> The plan item **A34** describes "build a release manifest + **package** the declared assets …
> each with a matching **content digest** … packaging is **deterministic** (re-run → identical
> bytes/digests)." **The real `release_assets.py` implements NO packaging step and NO digest.**
> It is a **read-only accessor**: it reads the manifest shipped inside the package and validates
> that each declared asset path resolves to a real file, with a path-traversal guard. Your job is
> to pin what the code ACTUALLY does and file the divergence as **F2E-A34-1 (note)** — do NOT
> invent a packaging/digest API or import symbols that do not exist.

## Where you are

- Working dir: `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run: `cd` there, then
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_release_assets -v`

## Code under test — `orchestrator_harness/release_assets.py` (the WHOLE module; read it)

- `release_manifest()` → dict; reads `orchestrator_harness/assets/release/manifest.json` via
  `importlib.resources`; raises `RuntimeError` if unreadable/invalid-JSON or if
  `schema != "orchestrator-release-assets/v1"`. The shipped manifest has keys incl. `schema`,
  `examples` (2), `release_evidence_templates` (7), plus others.
- `read_package_asset(relative_path)` → str; splits on `/`, refuses empty result or any `..`
  segment with `ValueError("package asset path must be relative")`, refuses a non-file with
  `FileNotFoundError`, else returns the file text.
- `manifest_asset_paths()` → tuple[str, ...]; collects `examples` + `release_evidence_templates`,
  raises `RuntimeError` if either field is not a list-of-str, raises on duplicate canonical paths,
  and calls `read_package_asset(path)` for each (so every declared path MUST resolve to a real
  file). Returns the validated tuple.

## What to build — ONE module `orchestrator_harness/tests/test_compat_release_assets.py`

1. **A34 actual-behavior (PASS rows):**
   - `release_manifest()` returns a dict whose `schema == "orchestrator-release-assets/v1"` and
     that contains `examples` and `release_evidence_templates` lists.
   - `manifest_asset_paths()` returns a non-empty tuple; assert it equals `examples +
     release_evidence_templates` from the manifest (exact declared set, in that order), contains
     no duplicates, and every entry resolves (`read_package_asset` returns a str for each). This is
     the "manifest lists exactly the declared assets, each present" property.
   - **Determinism (as far as the code supports it):** call `manifest_asset_paths()` twice and
     assert identical tuples; `read_package_asset(path)` twice for one path and assert identical
     bytes/text (idempotent read). NOTE in the row that there is **no digest field** to compare —
     that is the A34 gap, see the FINDING below.
   - **Path-traversal guard (fail-closed):** `read_package_asset("../secret")`,
     `read_package_asset("a/../../b")`, and an absolute-style `"/etc/passwd"` each raise
     `ValueError`; a bogus-but-relative `"assets/release/does-not-exist.json"` raises
     `FileNotFoundError`.
   - **Schema fail-closed:** monkeypatch is not needed — instead assert the schema guard by
     constructing the failure via a temp resource is hard; INSTEAD just assert that the real
     manifest passes and document that a wrong schema raises `RuntimeError` by reading the code.
     (If you can cleanly force a bad manifest via `unittest.mock.patch` on
     `orchestrator_harness.release_assets.resources.files` returning a fake object whose
     `.read_text` yields `'{"schema":"wrong"}'`, do so and assert `RuntimeError`; if that is
     fiddly, SKIP that sub-leg and say so — do not fail.)

2. **F2E-A34-1 (the FINDING, record clearly in your report):** the module exposes no
   packaging/tar/zip builder and no content-digest for declared assets; A34's "package … with a
   matching content digest … deterministic identical bytes/digests" is **not implemented here**.
   What IS enforced: read-only manifest access, exact declared-path set, no duplicates, every path
   resolves, and a `..`/absolute path-traversal guard. Assert `not hasattr(release_assets, "package")`
   and that no public name in `release_assets.__all__` produces a digest, to pin the absence.

Never edit source. If a `..` path is NOT rejected, or a declared asset path silently resolves to a
file OUTSIDE the package, that is FAIL-OPEN, HIGHER severity — flag it loudly.

## Pass criterion & regression

- New module green (with the F2E-A34-1 FINDING documented) under the run command above.
- Regression: `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_s6_public_release -v`
  **IMPORTANT:** `test_s6_public_release` has ~6 PRE-EXISTING, environment-dependent ERRORS in
  this clone (baseline). Those are NOT caused by you. Report the S6 tally but do not try to fix
  S6 and do not count its pre-existing errors as your regressions — just note "6 pre-existing
  errors, unchanged" (or the actual count you observe) in your log.

## Evidence into `.../evidence/2.E/`

- `test-run.log` — `-v` of your new module.
- `s6-regression.log` — `-v` of `test_s6_public_release` (baseline errors expected).

## Final report

Markdown table with an **A34** row = PASS (read-only accessor behavior pinned) plus an explicit
**F2E-A34-1** FINDING row (no packaging/digest engine; what IS enforced instead). Then exact
commands, test count, pass/fail tally, and the observed S6 error count. Do not modify any file
outside your new test module and the evidence dir.
