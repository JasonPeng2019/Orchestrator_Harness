# Canary sprint target ? 20260731-s1-clean-h

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent alarm: `75 seconds`; optional watcher poll: `180 seconds`

## Why this is a valid counting benchmark

Clean-G locked all four board-free preparations and its sole primary historical-lifetime defect is
verified repaired. Clean-H therefore starts from those exact checkpoints and exercises live setup,
request/relay delivery, disjoint STM/nRF HIL overlap, STM-A lease turnover, current PID/lifetime
classification, optional watcher reporting, active manager supervision, and exact shutdown. It
must advance real catalog endpoints; host-only prep is not enough.

## Counting endpoints

1. **Atlas/A22/STM-A:** in one fresh Clean-H lifetime, complete B14 or reach its first truthful
   manager-reviewed populated read-only request if another bounded server gate is required. Preserve
   B12/B15/B35/B36. Start B34 only after B14 is accepted.
2. **Boreal/D31/STM-B:** in one fresh Clean-H lifetime, follow every live setup/fix/load route and
   execute exactly one reviewed RST01 `reset_and_run`; persist post-action state and stop before
   APP-1 breakpoint work.
3. **Cygnus/A24/NRF-A+NRF-B:** in two isolated per-board lifetimes under one paired attempt, reach
   the first truthful post-flash identity/UART checkpoint for both retained PING/PONG artifacts.
   Do not start RF.
4. **Delta/A26/STM-A:** after Atlas releases STM-A, use one new Clean-H lifetime for the prepared
   `+8/+1/+1/+0` counter/version measurement. Preserve R16 and do not rerun prep.

## Parallel schedule

Launch Atlas, Boreal, Cygnus, and Delta's Clean-H binding turn in one batch. Atlas owns the first
provider-enumeration window. Boreal waits for a manager release until Atlas records its first public
artifact; Cygnus waits until Boreal records its first public artifact. Their subsequent disjoint HIL
lifetimes may overlap. Delta checkpoints its H binding board-free, then resumes with an STM-A lease
immediately after Atlas releases it. A waiting lane never stops unrelated work.

## Counting and stop rule

Count only if all four endpoints are reached without redundant live attempts, expired current
requests, duplicate controllers, lease conflicts, stale actionable history, missed supervision,
watcher/harness defect, or unclean shutdown, and the same persistent Terra-medium auditor accepts
the epoch issue-free. A real bounded problem makes the epoch useful but non-counting; preserve its
evidence, finish unrelated endpoints, stop cooperatively, and audit before deciding whether a
harness/watcher repair is justified.
