# M5 Q2 pending-priority repair report

Validated: `2026-08-02T13:14:46Z`  
Verdict: **REPAIR ACCEPTED**

## Verified defect

During Q2, an already-pending routine `CHECKPOINT_UPDATED` notification prevented four later
blocked HELP requests from becoming actionable. The harness observed the HELP requests, but its
single pending slot kept the lower-priority event until acknowledgement. This invalidated the
harness gate and left the manager-causality evidence insufficient.

## Minimal repair

The native harness now records the priority admitted with each pending notification. A newly
actionable event may preempt only when its durable admitted priority is strictly higher. The
displaced pending event moves to durable deferred state and is restored after the urgent event is
acknowledged. Equal- and lower-priority events do not preempt. Deferred promotion, coalescing, and
non-live re-gating preserve the admitted priority.

Changed production files:

- `orchestrator_harness/notifications.py`
- `orchestrator_harness/cli.py`

Changed regression tests:

- `orchestrator_harness/tests/test_clean_m_handoffs.py`
- `orchestrator_harness/tests/test_clean_n.py`

## Review loop

The independent Terra reviewer found two valid edge cases. Root accepted both:

1. a non-live pending event must be re-gated without guessing a missing legacy priority;
2. deferred coalescing must not drop the stored admitted priority.

Both received focused fixes and regression coverage. The final independent re-review reported no
remaining accepted-scope defect. Reviewer findings remained advisory; root made every decision.

## Verification

- Full native harness suite: **208 passed, 1 skipped**.
- Full deterministic watcher suite: **95 passed**.
- Host-only attention practical: **PASS**.
- Luna-authored native priority smoke, after root removed unrelated faulty fixture conditions:
  **PASS**.
- Autonomy-policy audit: **PASS** across 10 evidence runs.
- Compileall: **PASS**.
- No hardware, provider, MCP server, AI evaluator, watcher subagent, runner, wrapper, commit, push,
  or deploy was used.

The tested Python surface is frozen in
`multi-agent-logs/current-state/M5_PYTHON_BASELINE.json`: 68 active Python source files, baseline-file
SHA-256 `b22152516ef20f2d7f2bcb1ade5e316517810e16494d96203268bd03bf311d60`.
Runtime logs, generated evidence, temporary workspaces, `__pycache__`, and the copied
`harness_watcher_implementation/test_results/` workspace are explicitly excluded.
