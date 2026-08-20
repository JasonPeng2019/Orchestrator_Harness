# M5 Sprint Checklist

Use this Markdown checklist for every M5 attempt. Copy it to:

`multi-agent-logs/attention-validation/runs/<epoch>/M5_SPRINT_CHECKLIST.md`

Fill fields from evidence; never infer missing facts. This checklist adds no runtime component and
does not replace `m5-three-sprint-wake-test.md`.

## Sprint identity

- [ ] Epoch: `<epoch>`
- [ ] Start UTC: `<timestamp>`
- [ ] Root manager session/invocation: `<identity>`
- [ ] Comparable-set fingerprint: `<fingerprint or RESET>`
- [ ] Current qualifying count before sprint: `<0-3>/3`
- [ ] Active-goal attempt: `<1-10>/10` (do not launch attempt 11)

## Before workers launch

### Safe starting boundary

- [ ] Any interrupted epoch is stopped, drained, and preserved.
- [ ] Current worker sessions, processes, leases, hardware, and dependencies are reconciled.
- [ ] No ownership or safety ambiguity remains.

Evidence: `<paths>`

### Frozen tested surface

- [ ] Git status recorded.
- [ ] Relevant harness/watcher/logging **Python source only** is hashed.
- [ ] Python selection is exactly `harness_common/**/*.py`,
      `harness_watcher_implementation/**/*.py`, `orchestrator_harness/**/*.py`, and
      `scripts/orchestration/**/*.py`, excluding `**/__pycache__/**` and
      `harness_watcher_implementation/test_results/**`.
- [ ] Runtime logs, generated evidence, temporary workspaces, and whole runtime directories are
      excluded from the fingerprint.
- [ ] Relevant config-policy fingerprint is recorded.
- [ ] The surface matches the current comparable set, or the count has been reset.

Evidence: `<paths and hashes>`

### Runtime allowlist

Record exact command, PID plus creation identity, owner, and output path after launch.

| Allowed role | Planned identity/command | Actual PID + creation identity | Evidence |
|---|---|---|---|
| Persistent root | `<value>` | `<value>` | `<path>` |
| Native managed harness | `<value>` | `<value>` | `<path>` |
| Diagnostic-only watcher | `<value>` | `<value>` | `<path>` |
| E2E worker/controller lanes | `<lanes/models>` | `<value>` | `<path>` |
| Required provider/MCP/tool/hardware processes | `<value>` | `<value>` | `<path>` |

- [ ] Every AI worker is assigned only genuine documented E2E work.
- [ ] Watcher evaluator is disabled and no model child or notification path exists.
- [ ] No runner, wrapper, relay, scheduler, retry controller, automated event handler, watcher
      subagent, or other harness assistance exists.
- [ ] Root will use only the native blocking harness wait to discover tested requests.
- [ ] Collaboration notifications, transcript inspection, watcher output, and user messages will not
      be used for request discovery.
- [ ] Recorder preflight used the watcher config, allowlisted `main-orchestrator` source, no-BOM
      UTF-8 metadata, and returned a real `record_id` whose source record exists on disk.
- [ ] Waiting intervals use paired `MANAGER_WAIT_STARTED`/`MANAGER_WAIT_FINISHED`; busy work uses
      paired `MANAGER_TOOL_STARTED`/`MANAGER_TOOL_FINISHED` with one activity ID and
      `manager_state: RUNNING_TOOL`. No unsupported kind or state is used.
- [ ] On a successful wake, `MANAGER_WAIT_FINISHED.event_id` is the returned worker signal ID
      (not the synthetic wait ID), and the claim's `continuous_from_record_id` names that exact
      wait-finish record. Only a timeout keeps the synthetic wait event ID.
- [ ] Hidden/`*.tmp.json` manager-signal staging files are not admitted as native events; only the
      final ordinary JSON is eligible.
- [ ] `MANAGER_WAKE_DELIVERED` (stdout emission) and `MANAGER_WAKE_RECEIVED` (root notice) remain
      distinct timestamps; no reviewer or operator treats the former as model receipt.

Evidence: `<paths>`

### Ready to launch

- [ ] Setup completed before genuine workers launch.
- [ ] Any pre-worker setup failure was classified `SETUP_RETRY`, corrected, and recorded.
- [ ] Root explicitly approves starting the sprint under the frozen setup.

Root pre-sprint decision: `<START / DO NOT START>`  
UTC and rationale: `<value>`

## During the live sprint

- [ ] Quiet native blocking-wait control recorded.
- [ ] Every dependency-ready, resource-compatible lane was launched/resumed.
- [ ] Existing sessions, leases, completed work, and accepted evidence were preserved.
- [ ] Requests were genuine; none were manufactured to meet a quota.
- [ ] Root waiting and genuine busy-work boundaries were durably recorded.
- [ ] No tested code, config policy, runtime topology, or procedure changed mid-sprint.
- [ ] The sprint continued to a safe natural boundary despite ordinary mistakes or E2E failures.

Early stop, deviation, or unusable sample details: `<none or exact facts/evidence>`

## Request evidence

Add one row for every genuine request. Use `UNCLASSIFIABLE` when required facts are missing.

| Lane/request | Created | Harness detected | Wake attempted | Wake delivered/failed | Manager noticed | Manager claimed | Waiting/busy evidence | Response/resume | Classification | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| `<value>` | `<time>` | `<time>` | `<time/component/transport>` | `<time/result>` | `<time>` | `<time>` | `<state/path>` | `<time/result>` | `<class>` | `<paths>` |

Classifications: `HEALTHY`, `HARNESS_DELAY_OR_FAILURE`, `IDLE_MANAGER_INATTENTION`,
`BUSY_MANAGER_CONTENTION`, `DOWNSTREAM_RESPONSE_FAILURE`, or `UNCLASSIFIABLE`.

Watcher-label mapping: `NO_BLOCKING_IMPACT` → `HEALTHY`; `HARNESS_DELIVERY_DELAY` →
`HARNESS_DELAY_OR_FAILURE`; `IDLE_OR_ABSENT_MANAGER_DELAY` → `IDLE_MANAGER_INATTENTION`;
`BUSY_MANAGER_DELAY` → `BUSY_MANAGER_CONTENTION`; `INSUFFICIENT_EVIDENCE` → `UNCLASSIFIABLE`.
Retain `ACKNOWLEDGEMENT_ONLY_DELAY` explicitly as downstream acknowledgement evidence.

For every request exceeding 90 seconds:

- [ ] Exact `delivery_deadline_utc`, actionability/delivery endpoint, and overrun are recorded;
      later worker receipt/resume time was not substituted for the delivery endpoint.
- [ ] A gap-free canonical interval proves genuine manager work or handling of an earlier genuine
      request, **or** the row is classified as harness delay, idle inattention, or unclassifiable.
- [ ] Native harness waiting, late harness observation, silence, and partial/overlapping activity
      were not accepted as valid reasons.

## Safe sprint boundary

- [ ] New work stopped at a safe natural boundary.
- [ ] Actual E2E progress and failures were preserved.
- [ ] Harness logs were drained.
- [ ] Watcher logs/cursor were drained and terminal state recorded.
- [ ] Sprint-owned processes were stopped/checkpointed through documented interfaces.
- [ ] Exact PID plus creation-identity cleanup was verified.
- [ ] Leases, hardware, MCP/provider processes, and temporary state are safe and known.
- [ ] No post-sprint reviewer or repair agent launched before runtime shutdown and drain.

Evidence: `<paths>`

## Post-sprint review

- [ ] Fresh Terra-medium reviewer launched after the safe boundary.
- [ ] Reviewer identity and report recorded.
- [ ] Root checked every finding against raw evidence.
- [ ] Root accepted or rejected every finding with rationale.

Reviewer/report: `<identity/path>`  
Root adjudication: `<path>`

## Three independent gates

`Clean` means all three gates pass with sufficient truthful causal evidence; it does not mean every
request is under 90 seconds.

| Gate | Root result | Evidence and rationale |
|---|---|---|
| Harness | `<HARNESS_PASS / HARNESS_BUG>` | `<paths/reason>` |
| Watcher | `<WATCHER_PASS / WATCHER_BUG>` | `<paths/reason>` |
| Manager evidence | `<MANAGER_EVIDENCE_SUFFICIENT / MANAGER_EVIDENCE_INSUFFICIENT>` | `<paths/reason>` |

- [ ] At least three classifiable genuine requests exist from at least three worker lanes.
- [ ] Combined evidence covers waiting-manager and genuine busy-manager behavior as required by the
      current three-run set.
- [ ] Forbidden assistance did not influence request discovery.
- [ ] Any request over 90 seconds has a complete valid-cause chain; no overrun was excused by
      inference or merely to make the sprint pass.

## Insufficient evidence or defect handling

Complete when any gate does not pass:

- Exact cause: `<value>`
- Owner: `<sample/setup/operator/worker/harness/watcher/required-logging>`
- [ ] Cause is supported by raw evidence rather than assumption.
- [ ] Sample/setup/operator/worker cause: correct only setup or procedure; no component edit.
- [ ] Verified harness/watcher/logging gap: smallest plan written; persistent Terra coded;
      independent Terra reviewed; root adjudicated; Luna smoke-tested.
- [ ] Any accepted smoke failure completed the targeted code/review/retest loop.
- [ ] Watcher remains passive and no assistance layer was added.
- [ ] Relevant code/config change triggered refreeze and qualifying-count reset.

Evidence/repair paths: `<value>`

## Final sprint disposition

- Disposition: `<QUALIFYING / EVIDENCE_INSUFFICIENT / SETUP_RETRY / HARNESS_BUG / WATCHER_BUG / SYSTEM_DEFECT>`
- Qualifying count after decision: `<0-3>/3`
- Comparable-set status: `<unchanged / reset, with reason>`
- Next action: `<value>`
- Durable checkpoint: `<path>`

- [ ] Root confirms the sprint is counted only if all three gates pass.
- [ ] Root confirms missing checklist evidence was not filled by inference.
- [ ] Root confirms the active-goal attempt count is truthful and no attempt beyond 10 will launch.

Root final decision, UTC, and rationale: `<value>`
