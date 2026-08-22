# Candidate Harness Acceptance V2 Watcher Report

## Outcome

`CLEAN`. The isolated read-only watcher found no candidate-harness defect and did not interact with the candidate orchestrator or target workers.

## Independent Findings

- `ACCEPTANCE_COMPLETE.json` records `PASS` for target commit `86daa9901f46b41c14e26b45135fa553503021ef`.
- An independent run of all 77 target tests passed; target `main` remained clean.
- The serialized ancestry `P1 -> P2 -> P3 -> P4 -> P5 -> A1 -> A2 -> D1 -> D2 -> M` is complete, and `main == lane/m`.
- Every current lane result matches its branch tip. The deliberate stale P1 result and malformed D2 result were rejected before valid retries.
- P3 resumed thread `019fc7b4-d325-75e1-a728-5b0fc3eab7a5` using the same output and status paths.
- Native evidence contains exactly 13 start/exit pairs across 26 events. The 19 observer acknowledgements are unique, reference existing events, and leave no pending or deferred notification.
- The contention fixture serialized Codex execution, rejected its stale result, passed its checks, and left zero claims.
- All 26 exact managed controller/worker PIDs were absent at shutdown; claim directories contained no active claim files.
- Launch evidence resolves to declared V2 worktrees with approval policy `never`, `danger-full-access`, and the bypass flag.
- The watcher sent no messages, edited no files, acknowledged no events, attempted no repair, and took no control action.

## Boundary

Candidate-source cleanliness, frozen-source non-use, and orchestrator-side watcher-isolation statements were outside the watcher's permitted filesystem boundary. The outside writer-manager separately verified the candidate and frozen checkouts were clean at their pinned commits.

This report records the final result returned by the isolated V2 watcher before the prior Codex session crashed.
