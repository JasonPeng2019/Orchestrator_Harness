# M5 Sprint Checklist

Use this Markdown checklist for every M5 attempt. Copy it to:

`multi-agent-logs/attention-validation/runs/<epoch>/M5_SPRINT_CHECKLIST.md`

Fill fields from evidence; never infer missing facts. This checklist adds no runtime component and
does not replace `m5-three-sprint-wake-test.md`.

## Sprint identity

- [x] Epoch: `20260802-m5-s3-101953Z`
- [x] Start UTC: `2026-08-02T10:19:53Z`
- [x] Root manager session/invocation: `019fbbc1-63ba-7140-ab1d-46bf412596e9` / `root-20260802-m5-s3-101953Z-001`
- [x] Comparable-set fingerprint: Python exact 112-file match; policy `89bb18cb67282fe4e71c198d9a3b4a279c6cb1412710a98b9a0a720316ec0f04`
- [x] Current qualifying count before sprint: `1/3`

## Before workers launch

### Safe starting boundary

- [x] Any interrupted epoch is stopped, drained, and preserved.
- [x] Current worker sessions, processes, leases, hardware, and dependencies are reconciled.
- [x] No ownership or safety ambiguity remains.

Evidence: `PREFLIGHT.json`, `PYTHON_CODE_FINGERPRINT_BEFORE.json`,
`CONFIG_POLICY_FINGERPRINT.json`, `GIT_STATUS.txt`, and the then-current process inventory.

### Frozen tested surface

- [x] Git status recorded.
- [x] Relevant harness/watcher/logging **Python source only** is hashed.
- [x] Relevant config-policy fingerprint is recorded.
- [x] The surface matches the current comparable set, or the count has been reset.

Evidence: `PYTHON_CODE_FINGERPRINT_BEFORE.json` (112 exact files, no changes),
`CONFIG_POLICY_FINGERPRINT.json` (policy SHA-256
`89bb18cb67282fe4e71c198d9a3b4a279c6cb1412710a98b9a0a720316ec0f04`), and `GIT_STATUS.txt`.

### Runtime allowlist

Record exact command, PID plus creation identity, owner, and output path after launch.

| Allowed role | Planned identity/command | Actual PID + creation identity | Evidence |
|---|---|---|---|
| Persistent root | session/invocation `019fbbc1-63ba-7140-ab1d-46bf412596e9` / `root-...-001` | owner PID `192592`, creation `windows-filetime:134300974063275151` | `INFRASTRUCTURE_START.json`, invocation attention records |
| Native managed harness | `python -m orchestrator_harness ... watch --managed` | launcher PID `192204`, creation `2026-08-02T10:21:25.8441004Z` | `INFRASTRUCTURE_START.json`, harness managed runtime/service logs |
| Diagnostic-only watcher | native `python -m harness_watcher_implementation ... watch` | PID `196480`, creation `windows-filetime:134301396864022301` | `INFRASTRUCTURE_START.json`, watcher service record |
| E2E worker/controller lanes | Atlas/A22, Boreal/D31, Cygnus/A24, Delta/A26; persistent Luna-high/default | controller PIDs `194848`, `176328`, `191088`, `99932` with creation times recorded | `WORKER_START_INITIAL.json`, `WORKER_START_DELTA.json`, `WORKER_INDEX.json` |
| Required provider/MCP/tool/hardware processes | none for the host-only sprint slice | none | `RESOURCE_CLEANUP.json`, `PROCESS_CLEANUP.json` |

- [x] Every AI worker is assigned only genuine documented E2E work.
- [x] Watcher evaluator is disabled and no model child or notification path exists.
- [x] No runner, wrapper, relay, scheduler, retry controller, automated event handler, watcher
      subagent, or other harness assistance exists.
- [x] Root will use only the native blocking harness wait to discover tested requests.
- [x] Collaboration notifications, transcript inspection, watcher output, and user messages will not
      be used for request discovery.
- [x] Recorder preflight used the watcher config, allowlisted `main-orchestrator` source, no-BOM
      UTF-8 metadata, and returned a real `record_id` whose source record exists on disk.
- [x] Waiting intervals use paired `MANAGER_WAIT_STARTED`/`MANAGER_WAIT_FINISHED`; busy work uses
      paired `MANAGER_TOOL_STARTED`/`MANAGER_TOOL_FINISHED` with one activity ID and
      `manager_state: RUNNING_TOOL`. No unsupported kind or state is used.

Evidence: `INFRASTRUCTURE_START.json`, `WORKER_START_INITIAL.json`,
`WORKER_START_DELTA.json`, `WORKER_INDEX.json`, `RECORDER_PREFLIGHT.json`,
`RECORDER_PREFLIGHT.stdout.json`, `ISOLATION.json`, and the native harness/watcher service records.

### Ready to launch

- [x] Setup completed before genuine workers launch.
- [x] Any pre-worker setup failure was classified `SETUP_RETRY`, corrected, and recorded. (none; only the post-launch parser used the wrong encoding for a valid stdout capture)
- [x] Root explicitly approves starting the sprint under the frozen setup.

Root pre-sprint decision: `START`  
UTC and rationale: `2026-08-02T10:22:25Z; native infrastructure ready, recorder record verified, quiet control passed, frozen surface matched.`

## During the live sprint

- [x] Quiet native blocking-wait control recorded.
- [x] Every dependency-ready, resource-compatible lane was launched/resumed.
- [x] Existing sessions, leases, completed work, and accepted evidence were preserved.
- [x] Requests were genuine; none were manufactured to meet a quota.
- [x] Root waiting and genuine busy-work boundaries were durably recorded.
- [x] No tested code, config policy, runtime topology, or procedure changed mid-sprint.
- [x] The sprint continued to a safe natural boundary despite the observed delivery defect.

Early stop, deviation, or unusable sample details: none. The live sprint completed before review or
repair. Evidence: `QUIET_CONTROL.stdout.json`, `WORKER_INDEX.json`,
`BUSY_MANAGER_RESOURCE_AUDIT.json`, `NEXT_LIVE_AUTHORITY_REQUIREMENTS.md`, and the wait metadata.

## Request evidence

Add one row for every genuine request. Use `UNCLASSIFIABLE` when required facts are missing.

| Lane/request | Created | Harness detected | Wake attempted | Wake delivered/failed | Manager noticed | Manager claimed | Waiting/busy evidence | Response/resume | Classification | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Atlas / `sig-...-atlas-a22-gate-001` | `10:24:31.172768Z` | `10:24:45.165594Z` | `10:24:49.728049Z` / native blocking wait | `10:24:49.728049Z` / success | `10:25:14.315472Z` | `10:25:15.131569Z` | waiting / `wait-002-*` | publish `10:25:15.547569Z`; resume `10:25:51.761035Z` | `HEALTHY` | `REQUEST_ANALYSIS.json`, harness/watcher timelines |
| Boreal / `sig-...-boreal-d31-gate-001` | `10:25:17.917311Z` | `10:25:31.522116Z` | `10:26:18.057849Z` / native blocking wait | `10:26:18.057849Z` / success | `10:26:37.786853Z` | `10:26:38.409585Z` | waiting / `wait-004-*` | publish `10:26:38.749716Z`; resume `10:27:50.427109Z` | `HEALTHY` | `REQUEST_ANALYSIS.json`, harness/watcher timelines |
| Cygnus / `sig-...-cygnus-a24-gate-001` | `10:24:31.365277Z` | `10:25:31.522116Z` | `10:25:35.666772Z` / native blocking wait | `10:25:35.666772Z` / success | `10:25:56.170376Z` | `10:25:56.845027Z` | waiting / `wait-003-*` | publish `10:25:57.156337Z`; resume `10:26:11.396453Z` | `HEALTHY` | `REQUEST_ANALYSIS.json`, harness/watcher timelines |
| Delta / `sig-...-delta-a26-gate-001` | `10:27:59.835149Z` | `10:29:05.723786Z` | `10:30:11.712615Z` / native blocking wait | `10:30:11.712615Z` / success, 44.100780 s late | `10:30:34.665990Z` | `10:30:35.411989Z` | created during busy `10:27:04.304481Z`-`10:28:35.938693Z`; root waiting from `10:28:45.633763Z` | publish `10:30:35.744990Z`; resume `10:31:14.962705Z` | `HARNESS_DELAY_OR_FAILURE` | `REQUEST_ANALYSIS.json`, `BUSY_MANAGER_RESOURCE_AUDIT.json`, harness/watcher timelines |

Classifications: `HEALTHY`, `HARNESS_DELAY_OR_FAILURE`, `IDLE_MANAGER_INATTENTION`,
`BUSY_MANAGER_CONTENTION`, `DOWNSTREAM_RESPONSE_FAILURE`, or `UNCLASSIFIABLE`.

## Safe sprint boundary

- [x] New work stopped at a safe natural boundary.
- [x] Actual E2E progress and failures were preserved.
- [x] Harness logs were drained.
- [x] Watcher logs/cursor were drained and terminal state recorded.
- [x] Sprint-owned processes were stopped/checkpointed through documented interfaces.
- [x] Exact PID plus creation-identity cleanup was verified.
- [x] Leases, hardware, MCP/provider processes, and temporary state are safe and known.
- [x] No post-sprint reviewer or repair agent launched before runtime shutdown and drain.

Evidence: `PROCESS_CLEANUP.json`, `RESOURCE_CLEANUP.json`, `ISOLATION.json`, harness runtime output,
watcher service/report/cursor, and the four worker checkpoints listed in `WORKER_INDEX.json`.

## Post-sprint review

- [x] Fresh Terra-medium reviewer launched after the safe boundary.
- [x] Reviewer identity and report recorded.
- [x] Root checked every finding against raw evidence.
- [x] Root accepted or rejected every finding with rationale.

Reviewer/report: `/root/m5_s3_review`; `REVIEW.md`  
Root adjudication: `SPRINT_CHECKPOINT.md`

## Three independent gates

| Gate | Root result | Evidence and rationale |
|---|---|---|
| Harness | `HARNESS_BUG` | Delta was observed before its delivery deadline while root waited, but stale status was selected first and Delta was delivered 44.100780 s late. See `SPRINT_CHECKPOINT.md`, `REVIEW.md`, and raw harness records. |
| Watcher | `WATCHER_PASS` | Diagnostic-only, evaluator disabled, zero observation errors, correct causal report, drained cursor, clean stop. |
| Manager evidence | `MANAGER_EVIDENCE_SUFFICIENT` | Four complete multi-lane chains cover healthy waiting and a genuine paired busy sample, and isolate the late interval to the harness. |

- [x] At least three classifiable genuine requests exist from at least three worker lanes.
- [x] Combined evidence covers waiting-manager and genuine busy-manager behavior as required by the
      current three-run set.
- [x] Forbidden assistance did not influence request discovery.

## Insufficient evidence or defect handling

Complete when any gate does not pass:

- Exact cause: reconciliation discarded the signal's delivery metadata, so native selection ranked
  routine stale-status work ahead of a blocked HELP request whose delivery deadline was approaching.
- Owner: `harness`
- [x] Cause is supported by raw evidence rather than assumption.
- [x] Sample/setup/operator/worker-only correction is not applicable; component repair is warranted.
- [x] Verified harness/watcher/logging gap: smallest plan written; persistent Terra coded;
      independent Terra reviewed; root adjudicated; Luna smoke-tested.
- [x] No accepted smoke failure remained; the practical smoke passed 5/5 controls.
- [x] Watcher remains passive and no assistance layer was added.
- [x] Relevant code/config change triggered refreeze and qualifying-count reset.

Evidence/repair paths: `SPRINT_CHECKPOINT.md`, `REVIEW.md`,
`archive docs/active-working-spec/m5-harness-deadline-repair.md`,
`multi-agent-logs/verification/m5-deadline-repair-report.md`,
`multi-agent-logs/verification/m5-deadline-repair-luna-smoke.md`, and
`multi-agent-logs/verification/phase4-host-readiness-current.md`.

## Final sprint disposition

- Disposition: `HARNESS_BUG`
- Qualifying count after decision: `0/3` after the relevant harness repair
- Comparable-set status: reset because native harness selection behavior changes
- Next action: finish the focused repair/review/smoke/M4 loop, refreeze, then start a fresh sprint
- Durable checkpoint: `SPRINT_CHECKPOINT.md`

- [x] Root confirms the sprint is counted only if all three gates pass.
- [x] Root confirms missing checklist evidence was not filled by inference.

Root final decision, `2026-08-02`: accept the reviewer advisory. The watcher and manager-evidence
gates pass, but the verified native harness deadline-selection defect makes this sprint
nonqualifying and requires a between-sprint repair.
