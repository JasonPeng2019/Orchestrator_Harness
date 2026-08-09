---
name: harness-verify
description: Run the repository's enforced Ruff, BasedPyright, compilation, and test gate after code changes or when asked to verify, test, lint, type-check, or check the harness.
---

# Verify the harness at final completion

This skill is the authoritative full end-of-implementation gate. The project Stop hook uses the separate change-aware `.codex/scripts/verify_changed.py` for fast incremental checks; that incremental result never replaces this skill before final completion or promotion.

Run this exact command from the repository root:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/verify.py
```

Do not substitute individual checks for the complete final gate. Report the failing step and actionable locations. Do not claim completion unless the command prints `VERIFY: PASS`.

Use `--full` when watcher retention or lifecycle behavior changed.
