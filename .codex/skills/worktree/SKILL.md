---
name: harness-worktree
description: Create, list, or close isolated Git worktrees for parallel Codex development tasks in this repository.
---

# Manage task worktrees

Use the project helper from the repository root:

```powershell
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py create <task> --owner <agent>
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py list
uv run --project .codex/dev --locked python .codex/scripts/worktree_task.py close <task>
```

Assign disjoint file ownership. Never close a dirty worktree. The main agent remains responsible for integration and final verification.
