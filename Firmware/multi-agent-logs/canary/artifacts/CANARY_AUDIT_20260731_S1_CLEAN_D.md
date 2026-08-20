# Canary sprint audit - 20260731-s1-clean-d

Verdict: `ACCEPTED_NONCOUNTING`
Auditor: persistent `/root/canary_sprint_auditor` (`gpt-5.6-terra`, medium)
Counter after audit: `0 / 3`

## Benchmark

The declared benchmark in `.agent-workspace/CANARY_S1_CLEAN_D_TARGET.md` was not reached. All four
lanes stopped safely and preserved evidence, but none reached its requested experiment endpoint.

- A22: expected live-route issue; setup enumeration exposed no current debug connection and no B14
  or B34 action ran.
- D31: run-local doer issue; `continue_setup` omitted required `board_id`, so no RST01 ran.
- A24: manager procedure issue; the second setup-repair request did not receive a matching relay
  before its deadline, so no flash/post-flash checkpoint ran.
- A26: run-local doer issue; runtime-root/command handling stopped before setup/action.

Each lane used one bounded attempt and did not loop, duplicate, or mutate unsafely.

## Manager and scheduler

Initial A22/D31/A24 work was concurrent. Delta launched about 61 seconds after A22 released STM-A.
The prelaunch 90-second supervision loop produced fresh scans through shutdown. The manager failed
to service A24's later relay deadline and did not dispose of optional-watcher alerts. Classification:
`ORCHESTRATOR_PROCEDURE`; independently non-counting.

## Primary harness

The primary harness reconciled transitional states, delivered durable observations, and stopped
cooperatively. Final state has zero controllers, Codex workers, helpers, MCP lifetimes, leases,
requests, conflicts, observation errors, or process errors. No primary-harness code change is
justified.

## Optional watcher

The optional watcher stayed diagnostic and stopped cooperatively after real five-minute polls, but
created two false-positive alerts. It treated ordinary pre-request setup as unauditable merely
because request identity was absent, including a controller that had not yet started its declared
MCP lifetime. Classification: `WATCHER_CODE`.

Narrow correction: a missing request identity is not a defect during normal pre-request setup. The
watcher may diagnose ownership failure only when evidence explicitly says the lane is awaiting a
permission relay and the lane-correlated active lifetime and request evidence are absent or
inconsistent. Do not broaden or refactor.

Evidence:

- `harness_watcher/runs/20260731-s1-clean-d/watcher/alerts.json`
- `harness_watcher/runs/20260731-s1-clean-d/watcher/events.jsonl`
- `orchestrator_harness/canary-20260731-s1-clean-d-state/`
- `.agent-workspace/ORCHESTRATOR_HARNESS/{MANAGER_LOG,MONITOR_LOG,LANE_EVENTS}.jsonl`
- current A22/D31/A24/A26 `STATUS.md` and `PARALLEL_CHECKPOINT.md`
- `.agent-workspace/CURRENT_CANARY_READONLY_SCAN.json`
- `.agent-workspace/CURRENT_RELEVANT_PROCESS_INVENTORY.json`

## Disposition

Preserve all experiment evidence. Repair only the narrow watcher false-positive contract, verify it
with focused tests and a recorded-pre-request replay, then begin a fresh epoch. The canary counter
remains `0 / 3`.
