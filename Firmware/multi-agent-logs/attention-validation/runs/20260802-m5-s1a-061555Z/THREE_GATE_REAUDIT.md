# S1a Three-Gate Re-audit

Date: 2026-08-02  
Authority: current `active-working-spec/m5-three-sprint-wake-test.md`  
Root decision: **QUALIFYING (1/3)**

This re-audit supersedes only the old all-or-nothing `RESET` disposition in
`SPRINT_CHECKPOINT.md`. The original facts and criticisms remain preserved.

## Sample

- Four genuine requests from four external lanes.
- Atlas is excluded because the operator acknowledged before the valid claim/response records,
  producing contradictory ordering.
- Boreal, Cygnus, and Delta remain classifiable, satisfying the minimum three requests from three
  lanes.
- Quiet control is valid.
- The busy activity interval is valid, but Delta was observed after it ended; therefore S1a does
  not supply a busy-manager-delay sample. The final three-run set must obtain that control elsewhere.

## Gate decisions

### `HARNESS_PASS`

The native harness observed, selected, delivered, correlated, and acknowledged all genuine
requests without a crash, restart, loss, stale identity, or verified queue/transport defect.
Boreal and Cygnus were deferred behind earlier pending events and missed their delivery deadlines;
that delay is retained as real harness-path behavior, but the evidence does not establish a broken
queue implementation. Delivery-to-manager receipt was approximately 2.3-2.5 seconds.

Evidence: `CHALLENGES.json`, `FINALIZE_VALIDATION.json`,
`../../../orchestrator-harness/20260802-m5-s1a-061555Z/attention-events.jsonl`.

### `WATCHER_PASS`

The watcher remained diagnostic-only with evaluator disabled, 379 evaluator skips, zero route
rejects, zero attention errors, a drained cursor, accurate source-time causal metrics, and a clean
stop. No verified watcher defect occurred.

Evidence: `WATCHER_HEALTH.json`,
`../../../../harness_watcher/20260802-m5-s1a-061555Z/watcher/attention-report.json`.

### `MANAGER_EVIDENCE_SUFFICIENT`

Three usable lanes retain complete six-stage chains, manager waiting/activity boundaries,
response/acknowledgement/resume facts, and enough causal timing to distinguish harness admission
delay from manager receipt and claim delay. Native blocking wait was the only discovery path.

Evidence: `CHALLENGES.json`, `ISOLATION.json`, and the `waiting-wake-*` records.

## Imperfections that do not defeat the gates

- Atlas is excluded rather than repaired or hidden.
- The unacknowledged final `MANAGER_REVIEW_DUE` control was an operator drain mistake. It did not
  corrupt the three usable request chains, watcher cursor, process cleanup, or resource safety.
- The busy control limitation is carried forward as a requirement for the final comparable set.

## Comparability and cleanup

- `CURRENT_COMPARABILITY_AUDIT.json` confirms all 112 frozen Python files still match current code.
- `PROCESS_CLEANUP.json` proves all 12 registered sprint processes absent.
- `RESOURCE_CLEANUP.json` proves empty leases, board tokens, and MCP servers.
- `FREEZE_AUDIT.json` proves the tested surface and sealed inputs did not change during the sprint.
- `ISOLATION.json` records no forbidden assistance.

Root therefore records S1a as the first qualifying sprint under the current evidence standard.
