# Canary sprint target - `20260731-s1-clean-k`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent alarm: `75 seconds`; optional watcher poll: `180 seconds`

## Benchmark

Clean-K is the first fresh epoch after the independently accepted primary epoch/request/lifecycle repair. It is valid for counting only if all four bounded catalog endpoints below complete in one fresh lifetime/paired attempt each, the primary harness and optional watcher produce no validated defect, manager cadence/relay handling and shutdown are clean, and the same persistent Terra-medium auditor accepts it issue-free. Preserve all accepted prior evidence; never reuse a consumed Clean-I request, relay, PID, lifetime, or output root.

## Concurrent host-correction phase

Resume all four persistent Luna sessions concurrently, without board/provider/MCP leases, to prove only these run-local corrections:

- **Atlas/A22:** the fresh adapter must perform the required all-NULL `board_setup-plan` initialization before any populated plan.
- **Boreal/D31:** the fresh route parser must accept truthful terminal `setup_completed` without requiring another redirect, then expose the next RST01 planning boundary.
- **Cygnus/A24:** the dynamic loader must register the module in `sys.modules` before executing dataclass definitions.
- **Delta/A26:** reuse the already repaired normalized runtime-path guard and prove the exact fresh launcher; do not redo accepted counter preparation.

Each doer writes one `CLEAN_J_PREPARED.md`, focused host proof, checkpoint/progress record, and no terminal result. No doer starts MCP/provider/hardware in this phase.

## Counting endpoints

1. **Atlas/A22/STM-A:** one fresh Clean-K lifetime completes B14 or reaches its first truthful populated manager-reviewed read-only request after correct null-first initialization. Preserve B12/B15/B35/B36. B34 starts only after B14 acceptance.
2. **Boreal/D31/STM-B:** one fresh Clean-K lifetime follows current setup/validation routing, executes exactly one reviewed RST01 `reset_and_run`, persists post-action state, and stops before APP-1 breakpoint work.
3. **Cygnus/A24/NRF-A+NRF-B:** one paired attempt with two isolated per-board lifetimes reaches the first truthful post-flash identity/UART checkpoint for both retained PING/PONG artifacts. Stop before RF.
4. **Delta/A26/STM-A:** after Atlas releases STM-A, one fresh Clean-K lifetime performs the prepared `+8/+1/+1/+0` counter/version measurement. Preserve R16 and all accepted prep.

## Scheduling and stop rule

Launch all four host corrections together. Serialize only the short provider-enumeration windows: Atlas first; Boreal after Atlas's first public artifact or safe stop; Cygnus after Boreal's first public artifact or safe stop. Their disjoint HIL lifetimes may overlap. Release STM-A to Delta immediately when Atlas stops. A waiting/failing lane never stops unrelated work.

Valid `manager-signal/v1.kind` values are only `HELP`, `FEEDBACK`, `INSTRUCTION`, `PASS`, and `CHECKPOINT`. Every live request is hash-bound and manager-reviewed before its exact call. A lane uses one fresh live attempt only; on a run-local failure it checkpoints without retry while unrelated lanes continue.

Count only if all four endpoints are reached with no duplicate controller/lifetime, missed current request, stale actionable history, lease conflict, supervision gap, harness/watcher defect, manager-procedure defect, or unclean shutdown. Otherwise preserve useful evidence, audit as non-counting, repair only independently validated harness/watcher defects, and start a fresh successor without rerunning accepted work.
