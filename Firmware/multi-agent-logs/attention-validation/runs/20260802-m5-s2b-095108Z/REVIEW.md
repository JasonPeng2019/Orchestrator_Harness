# Post-sprint advisory review — 20260802-m5-s2b-095108Z

**Scope:** read-only post-sprint assessment against `active-working-spec/m5-three-sprint-wake-test.md` and `active-working-spec/m5-sprint-checklist.md`.  This is advice to root, not a disposition.

## Recommendation

| Gate | Advisory result | Basis |
|---|---|---|
| Harness | `HARNESS_PASS` | No verified native-harness defect. The harness continuously committed scans 1–28, returned exact native blocking-wait wake identities, and recorded successful acknowledgement for each returned event. The five genuine lane signals were observed/actioned and their native `blocking_harness_wait_stdout` wake deliveries were recorded. |
| Watcher | `WATCHER_PASS` | No verified deterministic-watcher defect. It was diagnostic-only (`evaluator_enabled: false`), started READY, stopped on a recorded request, has `cursor_drained: true`, and its report conservatively classifies all 25 events as `INSUFFICIENT_EVIDENCE` rather than fabricating a causal result. The missing stages reported by the watcher match the raw timeline. |
| Manager evidence | `MANAGER_EVIDENCE_INSUFFICIENT` | Required durable manager wait/activity coverage and canonical terminal chains are absent. The attempt **must not count** and cannot support an architecture inference. Recommended disposition: `EVIDENCE_INSUFFICIENT`, with comparable-set count unchanged. |

## Raw-evidence findings

### Native harness

`multi-agent-logs/orchestrator-harness/20260802-m5-s2b-095108Z/attention-events.jsonl` records the following genuine lane signals and native wake attempts/deliveries: Atlas (09:54:24Z), Boreal (09:55:08Z), Cygnus (09:56:56Z), Delta gate 1 (10:01:29Z), and Delta gate 2 (10:07:17Z). The matching worker input journals under `harness_watcher/.../inputs/subagent/` record creation, wait, response receipt, and work resume. There is no raw evidence of a lost event, stale wake identity, failed delivery, queue failure, or harness crash.

The numerous additional returned checkpoint/status events do not establish a harness bug; they are additional workload and many lack the required agent-origin causal chain. Their presence makes the manager procedure harder, but not the harness defective.

### Deterministic watcher

`harness_watcher/20260802-m5-s2b-095108Z/watcher/service.json` records a READY diagnostic-only service from 09:51:23Z to an intentional stop at 10:09:29Z. Its cursor names all configured harness, root, and four subagent sources and has no partial bytes; `attention-report.json` says `cursor_drained: true`.

The report’s 25 `INSUFFICIENT_EVIDENCE` classifications are supported, not erroneous: it repeatedly identifies missing wake-source stages, matching stage deadline/late endpoint, and/or incomplete manager chains. The watcher did not notify, acknowledge, decide, repair, or become a discovery path. No watcher defect is verified merely because the report cannot classify evidence that the manager procedure did not record.

### Manager-evidence failure and operator/procedure errors

1. The copied `M5_SPRINT_CHECKLIST.md` is wholly uncompleted: no identity/allowlist completion, request rows, gate results, or final disposition. The required facts therefore cannot be supplied by inference.
2. The canonical timeline contains **zero** `MANAGER_WAIT_STARTED`, `MANAGER_WAIT_FINISHED`, `MANAGER_ACTIVITY_STARTED`, or `MANAGER_ACTIVITY_FINISHED` records. The 14 `waiting-wake-*-meta.json` and busy metadata artifacts are not canonical recorder records and do not carry durable interval boundaries. `ATTENTION_LOGGING.md` expressly forbids inferring manager state from silence and requires paired explicit intervals.
3. There are five worker-origin gate chains across four lanes, but only **one** canonical `MANAGER_RESPONSE_PUBLISHED` (Delta gate 2). The first four gate responses may exist as response files and worker receipt/resume records, but their root response publication is not present in the canonical timeline. None has the required complete manager wait/activity coverage; they are unclassifiable for the M5 causal gate.
4. For every returned wake, the required matching `MANAGER_WAIT_FINISHED` before claim is absent. This invalidates use of the receipt/claim times as evidence of waiting-manager availability or idle-manager inattention.
5. The only durable busy audits (`BUSY_WORK_AUDIT.json` and `_2.json`) describe real work, but their start/finish values were not emitted as canonical manager activity records. They cannot cover the Delta gate-2 delay or distinguish busy contention from an otherwise-idle manager for the causal decision.
6. `ISOLATION.json` truthfully records that the user redirected work to prerequisite completion and that the epoch is non-counting. This late handoff/interruption is an operator/procedure observation, not a harness or watcher defect. It also leaves no acceptable completed manager-attention sample.

## Safety, isolation, and progress

The closeout evidence supports a safe boundary: `PROCESS_CLEANUP.json` reports no live relevant processes and verified absence of declared PIDs; `RESOURCE_CLEANUP.json` reports all controllers exited, no leases/tokens/MCP servers, and no hardware actions; `ISOLATION.json` records native harness-only discovery with watcher evaluator disabled and no relay/wrapper/runner. Workers made host-only checkpoint progress and their terminal state was preserved. These facts do not repair the missing causal evidence.

## Smallest justified correction

Do **not** change harness, watcher, or logging code on this evidence. Before another attempt, correct only the manual procedure: complete the checklist contemporaneously; record invocation, paired native wait start/finish, paired real busy activity start/finish, bridges where required, exact claim, response publication, worker receipt/resume, and final safe-boundary records. If another handoff interrupts, preserve it as an `EVIDENCE_INSUFFICIENT` attempt rather than backfilling intervals. Reuse neither this attempt’s missing records nor its timing for architecture conclusions.
