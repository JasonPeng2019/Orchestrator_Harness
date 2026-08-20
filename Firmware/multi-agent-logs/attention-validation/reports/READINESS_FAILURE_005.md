# READINESS FAILURE 005 — R4 producer bound to stale runtime

R4 is noncounting and the consecutive sprint counter remains **0/3**.

Atlas created the real deadline-bearing R4 HELP signal, but its producer command named `canary-20260801-attention-r3.json`. Both R4-tagged producer records therefore landed under the R3 runtime instead of R4. The R4 watcher could not observe or wake the manager for the exact event before its `2026-08-01T17:47:34.5645506Z` response deadline. This is an execution-authority/configuration error, not evidence of manager idleness.

The error is fully observable from the Atlas Codex JSONL command/output, the absent Atlas R4 producer input, and the two R4 records present under the R3 input. No provider, MCP, board, flash, RF, request, relay, or RESULT action occurred. All four host-only controllers exited code 0.

Next readiness attempt must use a fresh epoch and an absolute exact-epoch watcher config path, and must verify the producer output path before arming the blocking signal.
