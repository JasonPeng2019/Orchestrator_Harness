# Task: Phase 2, Area 2.H — Profile-scoped child environment construction (detection-only)

You are a **test-authoring subagent** for the `orchestrator_harness` compatibility-testing plan.
You write and run **pure-Python `unittest` tests** over the real `orchestrator_harness.profile`
module. No subprocess, no source edits, no "fix to green". Pin ACTUAL behavior.

## Where you are

- Working dir: `C:/Users/Jason/Documents/Jason/Orchestrator_Harness/harness-single-worktrees/compat-test`
- Run: `cd` there, then
  `PYTHONPATH="$PWD:$PWD/.." python -m unittest orchestrator_harness.tests.test_compat_profile -v`

## Code under test — `orchestrator_harness/profile.py` (read the WHOLE module)

- `RuntimeProfile` is a frozen dataclass; construct it directly OR via
  `RuntimeProfile.from_mapping({...})`. `__post_init__` requires `provider in provider_registry()`
  — so pick a REAL provider name. **Grep it:** `python -c "from orchestrator_harness.provider import
  provider_registry; print(sorted(provider_registry()))"` and use one of those (e.g. the first).
  `provider_needs` must be UPPERCASE env names matching `^[A-Z][A-Z0-9_]*$` and MUST NOT be denied
  names (construction rejects a denied grant with `ProfileError`).
- `build_child_environment(profile, inherited=None) -> (allowed: dict[str,str], cleared: list[str])`:
  `allowed_names = _BASE_ENV_ALLOW | set(profile.provider_needs) | {g in workflow_grants matching
  ^[A-Z][A-Z0-9_]*$}`. For each key in `inherited`: keep it iff `key.upper() in allowed_names AND
  not _denied_name(key.upper())`, else add key to `cleared`. Returns `(allowed, sorted(cleared))`.
- `_BASE_ENV_ALLOW` includes `PATH, PATHEXT, SYSTEMROOT, COMSPEC, WINDIR, TEMP, TMP, USERPROFILE,
  APPDATA, LOCALAPPDATA, LANG, LC_ALL, PYTHONUTF8, PYTHONIOENCODING, SSL_CERT_FILE, SSL_CERT_DIR,
  HTTP_PROXY, HTTPS_PROXY, NO_PROXY`.
- `_denied_name(v)` → True if `v` startswith any of `_DENIED_PREFIXES`
  (`MCP_, BYO_MCP_, PYOCD_, FIRMWARE_, DEVICE_, USB_, JTAG_, SWD_, GPIO_, PROBE_, TARGET_, SERIAL_,
  OPENOCD_, JLINK_, CREDENTIAL_, SECRET_, TOKEN_, AWS_, ANTHROPIC_API_KEY, OPENAI_API_KEY`) OR
  contains any of `_DENIED_MARKERS` (`API_KEY, ACCESS_KEY, PRIVATE_KEY, PASSWORD, SECRET, TOKEN,
  CREDENTIAL`).

## What to build — ONE module `orchestrator_harness/tests/test_compat_profile.py` (Q4)

1. **Q4 declared vars pass, denied/undeclared stripped:** build a `RuntimeProfile` with a valid
   registered `provider`, and `provider_needs=("MY_SAFE_VAR",)` (uppercase, not denied). Call
   `build_child_environment(profile, inherited={...})` with a fabricated `inherited` dict
   containing:
   - `"PATH": "/usr/bin"` (base-allowed) → **kept**.
   - `"MY_SAFE_VAR": "ok"` (declared) → **kept**.
   - undeclared plain var `"RANDOM_APP_VAR": "x"` → **cleared**.
   - inherited secrets that must be stripped: `"ANTHROPIC_API_KEY"`, `"AWS_SECRET_ACCESS_KEY"`,
     `"MY_PASSWORD"`, `"SOME_TOKEN"`, `"MCP_SERVER_URL"`, `"DEVICE_PORT"` → **all cleared**.
   Assert: `set(allowed) == {"PATH", "MY_SAFE_VAR"}`, `allowed["MY_SAFE_VAR"] == "ok"`, and every
   secret/undeclared key above is in `cleared`, and `cleared` is sorted.
2. **Belt-and-suspenders denied-guard:** show that even a name that reaches `allowed_names` cannot
   survive if it is denied. Since `provider_needs`/`workflow_grants` reject denied names at
   construction, demonstrate the second guard by: constructing a profile whose `provider_needs`
   contains a SAFE name that happens to be a **prefix** of nothing denied, then feed inherited keys
   that share a denied marker — confirm the `_denied_name` check at the keep-decision drops them
   even though `_BASE_ENV_ALLOW` membership is by `.upper()`. (E.g. inherited `"path_TOKEN"` →
   upper `"PATH_TOKEN"` is not in allow-list anyway → cleared; and directly assert
   `profile.build`-independent: `from orchestrator_harness.profile import _denied_name;
   self.assertTrue(_denied_name("AWS_REGION")); self.assertTrue(_denied_name("X_API_KEY"));
   self.assertFalse(_denied_name("PATH"))`.)
3. **Construction guard (fail-closed):** assert `RuntimeProfile(..., provider_needs=("SECRET_KEY",))`
   raises `ProfileError` (a denied grant is refused at construction), and that a profile with an
   unregistered `provider="does-not-exist"` raises `ProfileError`.

Never edit source. If a denied/secret inherited variable ever appears in `allowed`, or an
undeclared variable leaks through, that is a FAIL-OPEN isolation breach, HIGHER severity — flag it
loudly.

## Pass criterion & regression

- New module green under the run command above.
- Regression: `PYTHONPATH="$PWD:$PWD/.." python -c "import orchestrator_harness.profile"` clean
  import. If you find a sibling suite referencing `build_child_environment`/`RuntimeProfile`, run it.

## Evidence into `.../evidence/2.H/`

- `test-run.log` — `-v` of your new module.

## Final report

Markdown table with a **Q4** row = PASS (declared kept, denied+undeclared+inherited-secrets
cleared; construction guards fail closed) or FINDING if anything differs. Then exact commands, test
count, pass/fail tally. Do not modify any file outside your new test module and the evidence dir.
