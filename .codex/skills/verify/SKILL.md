---
name: harness-verify
description: Verify changed code first with the repository's change-aware Ruff, BasedPyright, compilation, and test gate after code changes or when asked to verify, test, lint, type-check, or check the harness. Use whole-repository verification only for a missing baseline, an explicit request, or a promotion/release gate.
---

# Verify changed code first

Always start verification with the same change-aware verifier as the project Stop hook. It selects
static checks and tests for changed code; it does not silently expand into the whole-repository
suite. If a changed code path has no targeted route, add the smallest appropriate route before
finishing.

The Stop hook is only a changed-code exit gate; it never replaces this skill. It may recover by
running the full verifier only when the verification baseline is missing, obsolete, or unreadable.

Run this exact command from the repository root:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify_changed.py
```

Report the failing step and actionable locations. Do not claim routine change verification unless the command prints `VERIFY_CHANGED: PASS`.

## Whole-repository verification

Run the broader gate manually only when the user explicitly asks for it or a promotion/release
contract requires it. Do not run it merely because ordinary code changed; the changed verifier
handles the no-baseline recovery case itself:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Use `--full` only when that broader gate is required and watcher retention or lifecycle behavior changed.
