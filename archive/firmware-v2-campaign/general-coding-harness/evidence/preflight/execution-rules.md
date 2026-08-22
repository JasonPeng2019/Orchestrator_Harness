# Execution Rules

- Maximum concurrency is four active agents: this writer-manager plus at most three workers.
- Planning, product code, shared files, repair, integration, and merge decisions are serialized.
- Workers launch with full access and approval policy `never`, from their assigned candidate, test, evidence, target, or watcher directory.
- Workers must not read, list, search, execute, or modify `frozen-harness-to-use`.
- The writer-manager records the frozen checkout HEAD, porcelain status, and binary diff before and after every worker wave. Any change rejects the wave and stops execution without automatically reverting it.
- Product branches and worktrees are created serially from the accepted candidate commit.
- Green test IDs remain locked. Ordinary repairs rerun only failing or behaviorally implicated tests.
- The frozen harness is the outside observer during development and is stopped before candidate acceptance.

Worker launch equivalent:

```text
codex exec --dangerously-bypass-approvals-and-sandbox -c approval_policy="never" --cd <assigned-directory> ...
```

Initial worktree map:

| Step | Product branch | Product worktree |
|---|---|---|
| S1 | `impl/01-general-worker` | `harness-single-worktrees/01-general-worker` |
| S2 | `impl/02-git-safe-completion` | `harness-single-worktrees/02-git-safe-completion` |
| S3 | `impl/03-coordination-recovery` | `harness-single-worktrees/03-coordination-recovery` |
| S4 | `impl/04-general-use-delivery` | `harness-single-worktrees/04-general-use-delivery` |

