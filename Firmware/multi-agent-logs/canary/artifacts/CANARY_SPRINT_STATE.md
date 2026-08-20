# Harness/watcher canary sprint state

Consecutive issue-free sprints: `0 / 3`  
Restart authority: root `HANDOFF.md` and `.agent-workspace/CURRENT_SUITE_STATE.json`

## Attempt ledger

- `20260731-long-canary-sprint-1`: non-counting; watcher self-observation and primary lane/cadence
  defects.
- `20260731-long-canary-sprint-1-success-a`: non-counting; useful progress, but cadence and
  redundant-helper problems.
- `20260731-s1-clean-b`: audited non-counting; stale scan/cadence. Audit:
  `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_B.md`.
- `20260731-s1-clean-c`: audited non-counting; useful progress and clean shutdown, but 185.4-second
  supervision gap. Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_C.md`.
- `20260731-s1-clean-d`: audited non-counting; benchmarks missed, one relay deadline missed,
  run-local helper defects, and optional-watcher pre-request false positives. Audit:
  `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_D.md`.
- `20260731-s1-clean-e`: audited **ACCEPTED_NONCOUNTING**. Useful lane evidence and exact clean
  shutdown were accepted, but cadence/request/manager-procedure issues plus two monitor defects
  prevented counting. Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_E.md`.
- `20260731-s1-clean-f`: audited **ACCEPTED_NONCOUNTING**. Four lanes overlapped, the manager
  serviced three exact D31 setup relays, cadence and shutdown were clean, and no production-server
  defect was found. It did not count because primary discovery omitted current
  `manager-requests`/`manager-relays`, D31 stopped at a run-local redirect-handling gap, and A24
  rendered a nonexistent server root. Audit:
  `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_F.md`.
- `20260731-s1-clean-g`: audited **ACCEPTED_NONCOUNTING**. Four persistent Luna lanes completed
  their fresh board-free rebind/preflight checkpoints once, cadence and shutdown were clean, and
  the optional watcher correctly caught a regression. It did not count because the primary
  harness treated closed historical MCP lifetime records as actionable when their numeric PIDs
  were reused. Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_G.md`.
- `20260731-s1-clean-h`: audited **ACCEPTED_NONCOUNTING**. All four persistent lanes reached
  truthful bounded endpoints, but all four declared counting benchmarks were missed because of
  run-local launcher/parser/controller defects. The manager also issued invalid signal-kind
  instructions that were preserved and normalized. Final scan/process inventory are clean. The
  audit validated one optional-watcher startup epoch/cursor defect and no primary/server/hardware
  defect. Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_H.md`.


- `20260731-s1-clean-i`: audited **ACCEPTED_NONCOUNTING**. Four one-shot lanes stopped at run-local defects; manager serviced four exact D31 setup relays and shutdown was clean. The optional watcher passed its repaired startup baseline and eight evaluations. The audit validated three primary epoch/request/lifecycle correlation defects; the narrow repair passed plan review, 114 focused coder tests, 151 pass/1 skip ordinary discovery, 11 manager controls, retained-data scan, and independent repair audit. Audit: `.agent-workspace/CANARY_AUDIT_20260731_S1_CLEAN_I.md`.

## Latest clean-F boundaries

- A22: clean-F adapter and focused self-test pass with zero hardware calls; prepared for a fresh
  STM-A assignment. B14/B34 remain open.
- D31: one fresh STM-B lifetime consumed three exact reviewed setup relays, then stopped truthfully
  at a run-local `board_fix_setup`/load-validation routing gap. No RST01 or retry.
- A24: UV resolution/preflight passed, but the generated pair launchers pointed at a nonexistent
  run-local server project. No MCP/provider/flash/RF action.
- A26: assignment-gated counter wrapper/config and four focused tests pass; no MCP/board action.

Accepted experiment evidence stays locked through every non-counting attempt.

## Clean-G disposition and next

Clean-G is stopped and audited. Its four board-free checkpoints are accepted and locked:

- A22 focused self-test passed;
- D31 six focused route/binding tests passed;
- A24 six launcher/preflight tests plus compile/syntax checks passed; and
- A26 four assignment/root tests plus compile/syntax checks passed.

No clean-G HIL was started after the manager validated the primary regression. Final scan and
process inventory prove exact clean shutdown with no leases, conflicts, observation errors, or
process errors.

The primary historical-lifetime classification repair under
`.agent-workspace/CANARY_CLEAN_G_FIX_PLAN.md` is complete and verified: focused coder checks passed
83 tests, the complete ordinary primary suite passed 136 tests once, and the manager's five
focused controls plus a fresh no-write scan are green. Verification:
`.agent-workspace/CANARY_CLEAN_G_REPAIR_VERIFICATION.md`. The optional watcher, finalization
transient, production server, and experiment evidence needed no repair. Create a wholly fresh
Clean-H epoch and continue directly from the locked prep checkpoints without rerunning them.
Three consecutive auditor-accepted issue-free sprints are still required.

## Current audit boundary

Clean-I is fully stopped, audited non-counting, and its validated primary repair is accepted. Counter remains `0/3`. All suite-owned processes and leases are absent; canonical current scan/process/state sidecars are refreshed. Clean-J is authored but not yet launched. Start from `.agent-workspace/CANARY_S1_CLEAN_J_TARGET.md`; retain all prior evidence and use fresh authority only.
