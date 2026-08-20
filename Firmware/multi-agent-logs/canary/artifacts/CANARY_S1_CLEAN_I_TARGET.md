# Canary sprint target — 20260731-s1-clean-i

Counter before sprint: `0/3`  
Manager: current root session, sole scheduler/relay/evidence authority  
Primary review interval: `120 seconds`; independent alarm: `75 seconds`; optional watcher poll:
`180 seconds`

## Why this is a valid counting benchmark

Clean-H retained four useful live-route checkpoints and isolated four run-local execution gaps.
The optional watcher's one startup defect is now repaired and independently accepted. Clean-I
therefore tests the repaired epoch boundary plus the primary harness, manager cadence, same-session
Luna continuations, serialized provider windows, disjoint STM/nRF lifetimes, live request relays,
and real catalog advancement. No locked prep or terminal test is repeated.

## Required run-local corrections before each single live attempt

- **Atlas/A22:** correct the generated hook indentation and prove the exact launcher parses/runs to
  its bounded pre-initialization self-test before starting one fresh A22 lifetime.
- **Boreal/D31:** bind the underlying D31 launcher rather than the helper wrapper itself and prove a
  nonrecursive dry launch before starting one fresh D31 lifetime.
- **Cygnus/A24:** replay the retained `continue_setup` response host-only and prove that
  `redirect: board_fix_setup` routes to the next action before starting the fresh paired lifetimes.
- **Delta/A26:** use the retained live tool/setup evidence to complete the bounded controller path
  through the actual counter plan; do not stop merely because the next call is permission-bearing.

These are run-local corrections owned by the existing persistent doers. They do not authorize a
production-server edit and do not invalidate Clean-H evidence.

## Counting endpoints

1. **Atlas/A22/STM-A:** in one fresh Clean-I lifetime, complete B14 or reach its first truthful,
   populated, manager-reviewed read-only request if another bounded server gate is required.
   Preserve B12/B15/B35/B36. Start B34 only after B14 is accepted.
2. **Boreal/D31/STM-B:** in one fresh Clean-I lifetime, follow every live setup/fix/load route and
   execute exactly one reviewed RST01 `reset_and_run`; persist post-action state and stop before
   APP-1 breakpoint work.
3. **Cygnus/A24/NRF-A+NRF-B:** in two isolated per-board lifetimes under one paired attempt, reach
   the first truthful post-flash identity/UART checkpoint for both retained PING/PONG artifacts.
   Do not start RF.
4. **Delta/A26/STM-A:** after Atlas releases STM-A, use one fresh Clean-I lifetime for the prepared
   `+8/+1/+1/+0` counter/version measurement. Preserve R16 and do not rerun prep.

## Parallel schedule and manager vocabulary

Launch all four same-session correction/binding turns in one batch. Atlas owns the first
provider-enumeration window. Boreal may enter its provider window after Atlas reaches a safe public
artifact or terminal checkpoint; Cygnus may enter after Boreal's first public artifact or safe
terminal checkpoint. Their disjoint HIL lifetimes may then overlap. Delta completes its board-free
correction/binding work immediately and receives STM-A as soon as Atlas releases it. A waiting or
failed lane never stops unrelated eligible work.

`manager-signal/v1.kind` is **only** one of `HELP`, `FEEDBACK`, `INSTRUCTION`, `PASS`, or
`CHECKPOINT`. Waiting states such as `WAITING_FOR_PROVIDER` are phase/status text, never signal
kinds. A doer requests manager action with `HELP`, records a safe endpoint with `CHECKPOINT`, and
uses `PASS` only for a fully evidenced declared endpoint.

## Counting and stop rule

Count only if all four endpoints are reached without redundant live attempts, expired current
requests, duplicate controllers, lease conflicts, stale actionable history, missed supervision,
watcher/harness defect, manager-procedure defect, or unclean shutdown, and the same persistent
Terra-medium auditor accepts the epoch issue-free. A bounded problem makes the epoch useful but
non-counting: preserve its evidence, continue unrelated endpoints, stop cooperatively, and audit
before deciding whether any harness/watcher repair is justified.
