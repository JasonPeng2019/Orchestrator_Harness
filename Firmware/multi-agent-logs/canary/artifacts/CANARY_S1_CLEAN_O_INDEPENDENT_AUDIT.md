# Clean-O independent audit

**Verdict: BLOCK NONCOUNTING**  
**Counter recommendation:** remain **`0/3`**.

## Validated issues

### 1. Optional watcher published two false durable `manager_failure` alerts

This is a validated optional-watcher orchestration defect. The two retained alerts are:

- `hwa-366be5445b484c7f526251cf` (Cygnus), and
- `hwa-88d5260ebbdcfb4701273cea` (Atlas).

Their alert summaries call normal endpoint shutdown a manager failure: the controller still
declared `RUNNING_CODEX` during the short interval after its Codex child had gone. Primary events
then show the normal resolution to `CONTROLLER_EXITED`, exit code 0, with exact identities absent:
Cygnus stale at `23:18:43Z` → exited at `23:19:04Z`; Atlas stale at `23:19:04Z` → exited at
`23:19:29Z`. Later optional evaluations are `defect=false`.

The alert state nevertheless retains both as `acknowledged:false`, `recovery_state:null`, with no
truthful invalid-alert disposition. The manager correctly did not invent a real recovery
lifecycle. A durable false manager-failure alert is a real orchestration/supervision defect under
the counting target, not speculative hardening.

**Narrow repair:** make optional evaluation distinguish the bounded controller-exit/final-status
transition from a persistent manager failure, or add an evidence-bound
`DISMISSED_INVALID` disposition that preserves alert history but removes a reviewed false alert
from active defect state. Test both the normal transient and a genuine unresolved stale condition.

### 2. Later `MANAGER_REVIEW_DUE` was not formally delivered/acknowledged

This is a **manager-procedure supervision gap**, not yet enough evidence for a separate primary
harness code defect. After the acknowledged baseline `23:22:48.878263Z`, the same exact
`MANAGER_REVIEW_DUE` condition (`ce8ae49d…`) is recorded at `23:24:52Z` and again at `23:26:36Z`
while Boreal remained live. It cleared only when the lane exited. It is absent from the durable
acknowledged IDs and there is no second formal review/baseline advance.

The target requires a whole-suite record and canonical ack at *each* exact due review; higher
priority transition draining does not substitute. The manager should have completed the formal
review while Boreal was still live. Preserve this as an operational defect/gate failure. A harness
repair is warranted only if a focused reproduction shows a live, unacknowledged review due cannot
be selected after higher-priority pending work clears; the current evidence alone establishes the
manager lapse.

## Verified nonissues and progress

- Lane results are truthful bounded run-local failures, not BYO-Firmware-MCP defects: Atlas and
  Boreal rejected plain-text guidance locally, Cygnus invoked its explicit local stub before
  provider start, and Delta indexed an empty local route list. All four stopped once, generated
  checkpoints, and did not reach a permission request, board action, flash, RF, UART, breakpoint,
  or counter measurement. No `RESULT.json` was created.
- Primary `STALE_STATUS` transitions are conservative normal exit/status ordering and resolve to
  `CONTROLLER_EXITED`; no primary-harness defect is established from them.
- Optional watcher otherwise ran eight evaluation cycles, six `defect=false`, and stopped
  cooperatively (`STOP_REQUESTED` then `SERVICE_STOPPED`). Its failure is false-alert semantics,
  not topology/cleanup.
- The primary runtime records cooperative `stop-requested`; final state has `pending:null`, no
  deferred entries, and 22 acknowledged IDs. The first formal review was correctly preceded by
  review evidence and advanced baseline from `23:14:53.001268Z` to `23:22:48.878263Z`.
- No duplicate/retry/lease-conflict evidence was found. The server recheck reports all 81
  production files and HEAD equal the Clean-M manifest (`all_match:true`).

## Cleanup and autonomy

Final manager inventory is empty; primary owner/watcher and optional owner/watcher both record
cooperative stop. Endpoint/controller identities referenced in the state are absent in final
supervision scans. The report's autonomy audit passed for all ten active run roots; no broad kill,
commit, deployment, production-server mutation, or live endpoint rerun occurred.

## Required disposition

Do not count Clean-O. Repair optional-watcher false-alert/dismissal semantics and enforce the
manager formal-review gate before a successor. Preserve Clean-O's useful checkpoints and start a
fresh epoch only after independent repair review.
