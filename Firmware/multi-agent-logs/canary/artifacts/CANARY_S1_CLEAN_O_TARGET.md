# Canary sprint target — `20260731-s1-clean-o`

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent supervision: `75 seconds`; optional watcher
poll: `180 seconds`

## Purpose and counting benchmark

Clean-O is the first successor after the independently accepted Clean-N temporal/coalescing
repair. It resumes the four persistent Luna-high/default lanes from their preserved Clean-N
host-ready checkpoints and advances their bounded live catalog endpoints without repeating
accepted evidence. It counts as sprint 1 only if the endpoint work reaches truthful bounded
checkpoints, exact manager-review acknowledgements advance the baseline, the harness/watcher/
manager/subagents exhibit no validated issue, and cooperative exact cleanup leaves no relevant
process. A truthful endpoint failure may remain useful catalog evidence, but any harness,
watcher, orchestration, looping, lease, or subagent-control defect makes the sprint noncounting.

## Fresh-epoch preparation

Each lane may make only the mechanical Clean-N-to-Clean-O adaptation needed for new epoch names,
runtime roots, server names, assignments, releases, and evidence paths. It must retain the green
Clean-N host correction and rerun only its focused host gate before live start. No accepted flash,
RST01, R16, setup ordering, post-flash identity, or other expensive evidence is repeated.

All four persistent sessions start concurrently with only doer/workspace/launcher leases. They
must not start a provider or public MCP operation until their fresh manager-owned assignment and
exact provider-release gate permit it.

## Bounded live endpoints

1. **Atlas/A22/STM-A:** one fresh O lifetime completes B14 or reaches one truthful populated,
   manager-reviewed B14 read-only request after the accepted NULL-first setup. B34 may follow only
   after B14 is accepted and within the same bounded turn.
2. **Boreal/D31/STM-B:** one fresh O lifetime starts APP-1 without repeating RST01, sets the
   plan-bound `app_dispatch_command` breakpoint, triggers `status\r\n`, records halt/PC/R0-R3,
   performs exactly one step, and stops before resume/removal, APP-3, or under-reset work.
3. **Cygnus/A24/NRF-A+NRF-B:** one fresh paired no-flash/no-RF O lifetime records reset/BUSY
   timing and coherent `GetStatus`/`GetDeviceErrors` checkpoints on both retained CoreSX1262
   paths. Do not flash and do not transmit RF.
4. **Delta/A26/STM-A:** immediately after Atlas's exact STM-A release, one fresh O lifetime
   completes the retained `+8/+1/+1/+0` counter/version measurement without repeating R16.

Each endpoint has one fresh live lifetime/paired attempt. There is no same-epoch retry. A lane
that reaches a manager request writes the immutable request, stops at its declared safe boundary,
and waits for exact hash-bound relay review while unrelated lanes continue.

## Scheduling and leases

- Launch all four persistent doer turns concurrently.
- Serialize only provider-enumeration startup windows. Once one provider's exact ancestry is
  captured and its enumeration window closes, release the next eligible provider while already
  started disjoint-board work continues.
- Atlas owns STM-A until exact checkpoint/release; Boreal owns STM-B; Cygnus owns NRF-A+NRF-B.
  Delta receives STM-A only after Atlas's release. Board/probe/serial/runtime/evidence roots are
  mutually exclusive.
- A waiting or failed lane never stops unrelated work. No production-server repair begins without
  an independently validated production-code defect.

## Manager procedure and benchmark

Use the fresh Clean-O primary harness state and optional watcher. Check current pending state and
inspect each live lane at every 75-second supervision alarm, never less frequently than every
two-to-three minutes. For each exact `MANAGER_REVIEW_DUE`, write the whole-suite review record
first, invoke canonical exact-ID acknowledgement, verify `review_baseline_utc` advanced, heartbeat,
and rescan eligibility. Review every request/relay against exact lifetime, assignment, hash,
operation, board, loss, and final-state scope before relaying delegated authorization.

Stop at the first truthful bounded endpoint/checkpoint for every lane, or once all nonblocked
lanes have reached their endpoint and any blocked lane is safely checkpointed. Stop lane/controller
descendants exactly, optional watcher cooperatively, and primary owner/watcher cooperatively;
prove exact absence. Write the manager report and send the complete sprint to the same persistent
Terra-medium auditor. The counter advances only on an independent issue-free verdict.

