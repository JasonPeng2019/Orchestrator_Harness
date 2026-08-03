# Development rules

This file governs development of the harness. It is not part of the harness runtime protocol.

- Read `HANDOFF.md` before changing the product; it records current status and agreed design direction.
- Treat `GENERALIZATION_SPEC.md` as the proposed target product contract for the Python-focused generalized harness.
- No external workflow framework is active. The audited reference checkout was removed after the useful pieces were ported into `.codex/`.
- Before finishing a code change, run `uv run --project .codex/dev --locked python .codex/scripts/verify.py`.
- Run `uv run --project .codex/dev --locked python .codex/scripts/verify.py --full` when changing watcher retention or lifecycle behavior.
- Treat new Ruff, BasedPyright, compilation, or unit-test failures as blocking.
- Existing BasedPyright findings are recorded in `.codex/dev/basedpyright-baseline.json`; do not expand the baseline.
- Give parallel agents disjoint file ownership. Use `uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py` when isolated branches are useful.
- The main agent owns integration and final verification.
- Project Codex hooks block selected destructive commands, restore handoff context, and verify changed repository state before Codex stops.
