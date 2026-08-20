# M5 checkpoint — pre-count RESET

- Epoch: `20260802-m5-s1-015559Z`
- Disposition: `RESET`; consecutive count remains `0/3`.
- The run stopped before external-worker launch. It is not a counted sprint and contains no manager-wake verdict.
- Quiet control failed because the separate blocking process tried to join the managed scanner's authoritative scan chain and correctly hit a process-identity mismatch.
- The fresh post-sprint reviewer also verified a primary-identity writer/schema mismatch that caused a false diagnostic `PRIMARY_HARNESS_LOST`.
- Root accepted both findings and rejected no material finding. Cleanup proved every captured process absent.

## Repair and verification

The smallest repair makes `watch --until-actionable` a read-only consumer whenever a live managed owner exists, while preserving standalone scan/select mode and fail-closed identity/lease checks. A canonical `scripts/orchestration/primary_harness_owner.ps1` now publishes wrapper, managed-owner, and managed-watcher exact identities.

- Independent final Terra review: no remaining actionable issue.
- Luna real topology smoke: PASS at `multi-agent-logs/verification/m5-managed-consumer-luna/REPORT.md`.
- Root full harness suite: 194 passed, 1 skipped.
- Root full watcher suite: 88 passed.
- Pyright: 0 errors; compileall: PASS.
- Post-change M4: PASS at `multi-agent-logs/verification/phase4-wake-evidence-post-managed-consumer/`; wake `4caaecec-f83b-4f8f-b203-fb93228a4681`, analyzer `COMPLETE`, quiet `WATCH_TIMEOUT`.

The count restarts at zero with wholly fresh configs, output roots, processes, and source hashes.
