---
name: harness-test-first
description: Explicit test-first workflow for implementing a harness feature or reproducing a bug; use only when the user invokes this skill.
---

# Test-first harness change

1. Identify the smallest observable contract.
2. Add or run a focused test that fails for the intended reason.
3. Make the smallest production change that passes it.
4. Refactor without weakening the test.
5. Run `uv run --project .codex/dev --locked python .codex/scripts/verify_changed.py` before completion.
   It may recover with `verify.py` only when the verification baseline is unavailable. Run
   `verify.py` manually only for an explicitly requested whole-repository audit or a promotion/release gate.

For timing, concurrency, or process-lifecycle behavior, test identities and state transitions rather than sleeps alone.
