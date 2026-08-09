# M5 Spec + Plan - Manager-Attention Validation

## Plain goal

Run real multi-agent E2E work and collect enough causal evidence to answer:

> Does the native harness reliably surface worker requests to a persistent orchestrator, or do
> otherwise-idle workers wait because the manager fails to notice them?

The experiment must also distinguish a genuinely inattentive manager from a manager that is busy
doing other orchestration work.

M5 validates whether the harness and diagnostic watcher can support a multi-agent system making
real progress through the documented E2E experiments. It does **not** require a flawless
orchestrator, flawless workers, successful firmware, or a cosmetically perfect sprint.

## Governing sources

Apply this document with:

- `active-working-spec/m5-sprint-checklist.md` as the mandatory per-attempt audit record;
- `$run-firmware-test-suite` for real E2E lane, model, resource, and safety contracts;
- `harness_watcher_implementation/ATTENTION_LOGGING.md` for the implemented six-stage request/wake
  contract;
- `AGENTS.md` for repository placement and unassisted capability-testing rules;
- `REPOSITORY_LAYOUT.md` for evidence ownership; and
- the accepted current-surface M4 readiness report at
  `multi-agent-logs/verification/phase4-host-readiness-current.md`.

This document is the source of truth for M5 acceptance and retry decisions. Supporting documents
must not impose a stricter clean-run standard.

Before each attempt, copy the checklist into that epoch's attention-validation run directory and
complete it through the post-sprint decision. A sprint cannot count when required checklist facts
are missing or unsupported by linked evidence.

## What is being tested

### Tested system

- the production orchestrator harness and its blocking actionable-event wait;
- the persistent root orchestrator's ability to receive, claim, decide, and respond;
- the deterministic watcher in diagnostic-only mode; and
- the resulting ability of real external workers to resume useful E2E work.

### Not being tested

- whether the root follows every operating step perfectly;
- whether every worker behaves perfectly;
- whether every firmware build or hardware test succeeds;
- crash recovery for a terminated manager; or
- a `codex exec` bridge that has not yet been justified.

Orchestrator and worker errors are observations. They are not automatic sprint failures.

## Unassisted runtime boundary

Allowed during a sprint:

1. one persistent root orchestrator;
2. real external E2E workers/controllers allowed by `$run-firmware-test-suite`;
3. one production managed harness;
4. bounded native `orchestrator_harness watch --until-actionable` calls made directly by root;
5. one standalone deterministic watcher in diagnostic-only mode; and
6. normal provider/MCP/toolchain processes required by the E2E work.

Forbidden during request discovery:

- watcher, reviewer, or relay subagents;
- `collaboration.wait_agent` or collaboration notifications;
- transcript inspection or user messages used to discover requests;
- sprint runners, wrappers, schedulers, retry controllers, automated event handlers, or other
  executable assistance around the harness; and
- watcher evaluators, model children, manager notifications, acknowledgements, or repairs.

Unexpected assistance contaminates that sprint. It does not erase earlier valid evidence unless a
relevant tested-surface change also makes those earlier runs incomparable.

## Root authority

The root is the only manager and final decision-maker. It owns:

- lane selection and resource safety;
- request handling;
- evidence classification;
- acceptance or rejection of reviewer findings;
- repair scope;
- run disposition; and
- the final architecture verdict.

Reviewers advise. They never block, decide disposition, or keep a loop open for advisory
perfection.

## Three independent sprint gates

Every counted sprint must record all three results. Do not collapse them into one generic pass.

### Gate 1 — `HARNESS_PASS` or `HARNESS_BUG`

`HARNESS_PASS` requires evidence that the native harness:

- observed genuine worker requests and selected the correct actionable event;
- returned the exact event/wake identity through the native blocking wait;
- preserved ordering and correlation through claim, response, and acknowledgement;
- did not crash, restart, lose an event, use stale identity, mis-handle its queue, or misreport wake
  transport; and
- supported continued truthful E2E progress.

Use `HARNESS_BUG` only for a verified in-scope native defect. An orchestrator command mistake,
worker failure, firmware failure, or insufficient sample is not a harness bug.

### Gate 2 — `WATCHER_PASS` or `WATCHER_BUG`

`WATCHER_PASS` requires evidence that the deterministic watcher:

- remained live for the tested interval and observed the configured sources;
- stayed diagnostic-only with no evaluator, notification, acknowledgement, decision, or repair;
- correlated identities and source timestamps correctly;
- produced accurate, non-misleading diagnostics with no material cursor or coverage gap; and
- drained and stopped with known state.

Use `WATCHER_BUG` only for a verified in-scope watcher defect. A root logging-order mistake is not a
watcher bug when the watcher reports it correctly.

### Gate 3 — `MANAGER_EVIDENCE_SUFFICIENT` or `MANAGER_EVIDENCE_INSUFFICIENT`

`MANAGER_EVIDENCE_SUFFICIENT` requires enough genuine request chains and activity coverage to
distinguish healthy wake, harness delay, otherwise-idle manager inattention, busy-manager
contention, and downstream response failure. This gate decides whether the persistent manager is
sufficient or `codex exec` is justified; it does not grade orchestrator perfection.

A sprint is qualifying only when it records `HARNESS_PASS`, `WATCHER_PASS`, and
`MANAGER_EVIDENCE_SUFFICIENT`.

### Ninety-second target and valid overruns

The worker's 90-second delivery target is diagnostic, not a universal sprint-failure threshold.
A request may exceed it and remain part of a clean qualifying sprint only when canonical evidence
fully covers the actual overrun window from the delivery deadline through actionability and
attributes it to genuine bounded manager work or handling an earlier genuine request. Record that
request as `BUSY_MANAGER_CONTENTION`.

Do not excuse an overrun when the harness first observed the request after the target, the manager
was otherwise idle, the manager was waiting for the native harness to return, activity coverage is
partial/overlapping/contradictory, or the cause is unknown. Those cases remain
`HARNESS_DELAY_OR_FAILURE`, `IDLE_MANAGER_INATTENTION`, or `UNCLASSIFIABLE`. The deterministic
watcher must fail closed rather than invent a valid reason.

In this specification, a **clean sprint** is one that passes all three independent gates with
sufficient truthful causal evidence. It does not require every request to finish within 90 seconds.

### Per counted request

A request is classifiable only when durable evidence establishes:

1. worker request creation;
2. harness observation;
3. wake attempt, component, and transport;
4. wake delivery or explicit delivery failure;
5. manager receipt/notice;
6. manager claim/start of handling;
7. manager activity state covering the relevant interval; and
8. worker response receipt and useful-work resume, or a truthful terminal reason it could not
   resume.

The first six stages use the IDs and ordering defined by
`harness_watcher_implementation/ATTENTION_LOGGING.md`. Missing or contradictory evidence makes that
request `UNCLASSIFIABLE`; it does not automatically invalidate the entire sprint.

An observed manager signal that native liveness rules intentionally exclude carries passive
`HARNESS_EVENT_INELIGIBLE` evidence with one truthful bounded reason: `ALREADY_ANSWERED`,
`INVALID_LANE_ID`, or `LANE_NOT_LIVE`. It is explanatory evidence only, never request discovery or
a wake path. The watcher accepts it only when exactly one record matches the exact signal and
harness event, follows observation, and has no actionable contradiction. All other cases fail
closed without suppressing a supported harness-delay diagnosis.

### Per manager-evidence-sufficient sprint

A sprint has `MANAGER_EVIDENCE_SUFFICIENT` when all of these are true:

- at least three classifiable, genuine requests exist from at least three external worker lanes;
- the sprint contains waiting-manager evidence and busy-manager activity evidence sufficient to
  distinguish idle delay from single-threaded contention;
- the native harness was the only tested request-discovery path;
- harness and deterministic-watcher records are sufficient to diagnose their own operation;
- the E2E checkpoint truthfully records useful progress, failures, and preserved state; and
- process/resource ownership is brought to a safe, known boundary before the next sprint.

The run need not be cosmetically clean. Additional unclassifiable requests, operator mistakes,
worker mistakes, firmware failures, stale non-causal diagnostics, or later cleanup corrections do
not defeat an otherwise sufficient causal sample.

### Three-run set

M5 completes after **three clean comparable qualifying sprints (3/3)** under the same relevant
harness, watcher, wake-logging logic, and config policy. They do not need to be consecutive in wall
clock history. Insufficient attempts between them do not erase valid evidence.

If relevant harness/watcher/logging code or config policy changes, earlier runs from the old tested
surface remain historical evidence but do not count toward the new comparable three-run set.

Count every live sprint launched under the active M5 goal against its bounded attempt budget,
whether it qualifies or not. The budget is **10 attempts**: after attempt 10, stop and report the
evidence and remaining defect rather than launching attempt 11. Historical runs from before this
goal do not consume this budget.

## Causal classifications

Classify every usable request as exactly one of:

1. **Healthy:** detection, delivery, manager handling, and worker resume occur without unexplained
   delay. This normally meets the target; a proven busy overrun uses classification 4 instead.
2. **Harness delay/failure:** observation is late, delivery fails, or actionability/delivery is late
   without a complete valid manager-work explanation.
3. **Idle-manager inattention:** delivery succeeds, manager activity evidence shows no genuine busy
   work, and receipt or claim is materially late.
4. **Busy-manager contention:** the delay, including an overrun beyond 90 seconds, is fully covered
   by a genuine bounded manager-work interval or handling of an earlier genuine request. This is
   valid architecture evidence and does not by itself fail a sprint.
5. **Downstream response failure:** manager handles the request, but response delivery or worker
   resume fails.
6. **Unclassifiable:** required evidence is missing, contradictory, or cannot establish manager
   activity state.

The deterministic watcher uses implementation labels. Map them without reinterpretation:
`NO_BLOCKING_IMPACT` → Healthy; `HARNESS_DELIVERY_DELAY` → Harness delay/failure;
`IDLE_OR_ABSENT_MANAGER_DELAY` → Idle-manager inattention; `BUSY_MANAGER_DELAY` → Busy-manager
contention; and `INSUFFICIENT_EVIDENCE` → Unclassifiable. Preserve
`ACKNOWLEDGEMENT_ONLY_DELAY` as a distinct downstream/acknowledgement finding.

Do not infer manager state from silence. Use durable activity/wait boundaries.

## Preconditions

The completed M1-M4 work remains valid. Before resuming M5:

1. Query and cleanly close any interrupted epoch by verified process identity.
2. Preserve its records and E2E progress.
3. Confirm no worker, harness, watcher, provider, MCP, lease, or hardware lifetime is ambiguously
   owned.
4. Verify current harness/watcher/logging code and config-policy fingerprints. The Python baseline
   includes only `harness_common/**/*.py`, `harness_watcher_implementation/**/*.py`,
   `orchestrator_harness/**/*.py`, and `scripts/orchestration/**/*.py`, excluding
   `**/__pycache__/**` and `harness_watcher_implementation/test_results/**`. Never hash runtime
   logs, generated evidence, temporary workspaces, or whole runtime directories.
5. Reconcile dependency-ready E2E lanes and leases without repeating accepted expensive work.
6. Audit preserved M5 attempts against this evidence standard before deciding how many additional
   sprints are needed.

## Sprint procedure

This is a manual procedure for root. Do not translate it into an executable runner.

### 1. Establish the epoch

- Create fresh owner-approved harness, watcher, and attention-validation paths.
- Record the active-goal attempt number (maximum 10), exact Python-source manifest and fingerprint,
  config-policy fingerprint, Git status, epoch, lane set, process identities, leases, and
  forbidden-assistance declaration.
- Start from a reconciled baseline. A setup mistake before genuine workers launch is a
  `SETUP_RETRY`, not an experimental sprint and not a reason to erase previous evidence.

### 2. Start native infrastructure

- Start exactly one managed harness through its documented module entry point.
- Start exactly one diagnostic-only deterministic watcher through its documented module entry
  point.
- Record PID plus creation identity, exact command, parent/owner, config hash, and output paths.
- Prove the watcher has no evaluator/model child and no notification path.
- Run a quiet native blocking wait. Record its timeout honestly; a bad quiet control makes that
  control unusable but does not by itself erase other causal samples.

### 3. Run real E2E work

- Launch/resume every dependency-ready, resource-compatible external lane allowed by
  `$run-firmware-test-suite`.
- Preserve persistent model/session contracts and hardware leases.
- Let workers perform genuine documented E2E work and create truthful blocking requests.
- Do not manufacture requests or repeat accepted expensive work to satisfy a quota.

### 4. Handle waiting-manager requests

- Root records `MANAGER_WAIT_STARTED`, then enters the native blocking harness wait with the
  current manager session and invocation IDs.
- On return, root records `MANAGER_WAKE_RECEIVED`, then `MANAGER_WAIT_FINISHED` with the returned
  wake ID/transport and matching wait activity ID, then records `MANAGER_EVENT_CLAIMED` for the
  exact event before responding.
- Keep the two returned event identities separate. `data.signal_id` is the source event ID for the
  manager attention/decision/response chain and worker receipt/resume. The envelope's top-level
  `event_id` is the native harness event ID for exact acknowledgement. Copy the returned `wake_id`
  exactly. Do not substitute either event identity for the other.
- Every manager claim, including a setup or stale-status claim, has a complete snapshot selecting
  its own source event with `selection_reason: SELECT_ACTIONABLE`.
- Root publishes the response and returns to a fresh wait when appropriate.
- Before atomic response publication, validate `manager-response/v1` and require exact non-empty
  epoch, source event, lane, manager session, and invocation identities. Never publish a malformed
  response and then repair it in place.
- Manager-signal discovery accepts only final ordinary JSON. Hidden JSON and `*.tmp.json` staging
  files are ignored and must never become separate native events.
- A worker prepares the payload only at a hidden or `*.tmp.json` staging path, durably records
  `AGENT_SIGNAL_CREATED`, and verifies the returned `record_id`. Immediately before atomically
  renaming the staged payload to final ordinary JSON, it captures the exact UTC publication time.
  It then durably records `AGENT_SIGNAL_PUBLISHED` using that captured time and records
  `AGENT_WAIT_STARTED`, verifying both returned IDs. This separates worker preparation time from
  native harness observation latency without adding any runtime helper or wake path.
- Workers record response receipt and useful-work resume.
- Treat native `MANAGER_WAKE_DELIVERED` as successful stdout emission and root
  `MANAGER_WAKE_RECEIVED` as actual manager notice; never collapse or backfill these stages.
- Every `record-attention` call must include the watcher config and the allowlisted source ID
  `main-orchestrator`. Write metadata as UTF-8 **without a BOM** (for example with Python
  `Path.write_text(..., encoding="utf-8")`), and require a returned `record_id`; a disabled/error
  result is not evidence.
- Root mistakes in this procedure must be logged, not hidden. If enough timestamps remain, use the
  mistake to classify the request rather than discarding it.

### 5. Capture busy-manager behavior

- Allow at least one real request to arise while root is doing genuine bounded manager work.
- Record exact activity boundaries with the implemented vocabulary: `MANAGER_TOOL_STARTED` and
  `MANAGER_TOOL_FINISHED`, the same `activity_id`, and `manager_state: RUNNING_TOOL`. Do not invent
  unsupported kinds such as `MANAGER_ACTIVITY_STARTED`/`MANAGER_ACTIVITY_FINISHED` or unsupported
  states such as `ACTIVE_MANAGEMENT`.
- Record the real work being performed in a separate durable audit artifact.
- Handle the request at the next legitimate attention boundary through the native harness path.
- Attribute the delay to busy work only when the activity interval durably covers it.

Across the three-run set, evidence must include both waiting/idle opportunities and genuine busy
manager intervals. Prefer both in each sprint, but do not reject an otherwise rich sprint merely
because one control is supplied more clearly by another comparable sprint.

### 6. Reach a safe boundary

- Preserve every worker's actual progress and failure state.
- Do not abandon hardware/server actions in an unsafe or ambiguous state.
- Stop launching new work and record final worker/controller state.
- Drain logs enough to preserve causal records.
- Stop/checkpoint sprint-owned processes through documented interfaces and verify identity.
- Correct cleanup mistakes before starting the next sprint. Cleanup is a safety gate, not a demand
  that the preceding orchestrator made no mistakes.

### 7. Post-sprint review

Only after runtime work has stopped and safety is known, launch one fresh Terra-medium result
reviewer. It receives read-only evidence and reports:

1. number of genuine requests and number classifiable;
2. classification and timing for each usable request;
3. recommended `HARNESS_PASS`/`HARNESS_BUG` result with evidence;
4. recommended `WATCHER_PASS`/`WATCHER_BUG` result with evidence;
5. recommended `MANAGER_EVIDENCE_SUFFICIENT`/`MANAGER_EVIDENCE_INSUFFICIENT` result;
6. verified harness/watcher/logging defects, separated from operator, worker, firmware, provider,
   and downstream failures;
7. whether E2E workers made and preserved useful progress;
8. isolation and process/resource cleanup findings; and
9. the smallest justified correction, if any.

Root audits every finding against raw evidence and writes `SPRINT_CHECKPOINT.md`. Reviewer labels,
including `BLOCK`, are advisory only.

## Sprint dispositions

### `QUALIFYING`

The sprint records `HARNESS_PASS`, `WATCHER_PASS`, and `MANAGER_EVIDENCE_SUFFICIENT`. Add it to the
current comparable three-run set.

### `EVIDENCE_INSUFFICIENT`

The sprint ran real work but lacks enough classifiable requests or activity coverage to answer the
causal question. Preserve its progress and evidence, then identify the exact cause before another
sprint:

- If request volume was too low or an operator/worker mistake damaged the sample, correct only the
  setup or manual procedure. Do not change component code.
- If a verified harness, watcher, or required-logging diagnostic gap prevented classification,
  write the smallest instrumentation plan, implement it between sprints, and run focused smoke
  tests before resuming. The watcher must remain diagnostic-only; added logging must not become a
  notification or assistance path.

Do not erase previously sufficient comparable runs unless the remedy changes the relevant tested
code or config policy. A relevant change requires refreezing and a new comparable three-run set.

### `SETUP_RETRY`

The attempt failed before a genuine sprint sample began—for example, a malformed command or stale
preflight state. Correct it and retry. It is not a harness verdict and does not reset evidence.

### `HARNESS_BUG`, `WATCHER_BUG`, or `SYSTEM_DEFECT`

Use the component-specific result when raw evidence verifies a defect in the native harness or
deterministic watcher. Use `SYSTEM_DEFECT` for required wake-logging defects that make the evidence
untrustworthy.
Preserve the sprint, repair between sprints, rerun readiness when relevant, refreeze the surface,
and begin a new comparable three-run set.

Forbidden assistance makes only the contaminated sprint unusable. A code/config-policy change made
to address it starts a new comparable set; an operator simply refraining from the forbidden action
does not erase earlier uncontaminated evidence.

## Repair loop

Repairs occur only after the sprint and only for verified native harness, deterministic-watcher, or
wake-logging defects, including a verified component-owned diagnostic gap that caused insufficient
evidence:

1. Root verifies the exact failed boundary and writes the smallest repair plan.
2. A persistent GPT-5.6-terra **medium-reasoning** coder implements the accepted repair.
3. An independent GPT-5.6-terra **medium-reasoning** reviewer critiques the change.
4. Root audits every finding. Evidence-backed, worthwhile fixes return to the same coder;
   speculative, non-breaking, or disproportionately risky suggestions are rejected with rationale.
5. Repeat the coder/reviewer loop only while root has an accepted unresolved finding. The reviewer
   advises and never decides whether the repair is sufficient or whether work advances.
6. GPT-5.6-luna **high-reasoning** writes/runs the smallest practical smoke tests.
7. Root audits every smoke failure. Accepted failures return to the coder, followed by the smallest
   necessary targeted review and smoke retest; irrelevant or invalid failures are rejected with
   rationale.
8. Run affected full checks and M4 readiness when the production wake path changed.
9. When root determines all accepted issues are resolved and required checks are green, refreeze
   and start a new comparable three-run set.

Do not repair worker firmware, orchestration technique, or unrelated code merely to make an M5
sprint look cleaner. BYO production-server defects follow their own `$change-loop` outside the M5
control-plane repair loop.

## Checkpoint contents

Each checkpoint records:

- epoch, tested fingerprints, lane/session identities, and process/resource identities;
- genuine and classifiable request counts;
- for each usable request: worker, event/wake IDs, six-stage times, manager activity state,
  response/resume times, deadline, and causal classification;
- excluded requests and exact missing/contradictory evidence;
- quiet and busy evidence;
- harness and watcher health;
- forbidden-path isolation;
- actual E2E progress/failures and preserved state;
- cleanup/safety state and any corrected operator mistakes;
- reviewer findings with root acceptance/rejection rationale;
- disposition; and
- current count of comparable evidence-sufficient runs.

Never fill missing fields by inference.

## Final analysis

After three clean comparable qualifying sprints (3/3), root audits all usable request rows and chooses
exactly one verdict:

1. **Persistent manager sufficient** — the native wake path reliably surfaces work and idle
   handling is timely enough for real deadlines.
2. **`codex exec` bridge justified** — wake delivery succeeds, but otherwise-idle manager receipt
   or claim is repeatedly late or absent.
3. **Busy-manager contention** — delays are covered by genuine manager work; prioritize attention
   or divide work before assuming a wake bridge will help.
4. **Focused implementation repair required** — a native harness, watcher, logging, response, or
   worker-resume boundary remains defective or too uncertain for an architecture verdict.

The final report lives under `multi-agent-logs/attention-validation/reports/` and links all three
checkpoints and raw causal evidence. It must also state whether the harness supported real E2E
progress rather than only transporting synthetic signals.

## Definition of done

- three clean comparable sprints (3/3) durably record `HARNESS_PASS`, `WATCHER_PASS`, and
  `MANAGER_EVIDENCE_SUFFICIENT`;
- overruns beyond 90 seconds are accepted only with complete causal busy/prior-request evidence;
- the combined sample distinguishes harness delay, idle-manager inattention, busy-manager
  contention, and healthy operation;
- no forbidden assistance influenced counted request discovery;
- real E2E work made and preserved truthful progress;
- verified harness/watcher/logging defects are repaired and rebaselined;
- resource/process safety is known before completion;
- reviewer findings are independently adjudicated;
- final verdict, `PLAN.md`, `HANDOFF.md`, and durable report agree; and
- no commit or push is performed.

## Bounded execution result

The authorized execution exhausted its 10-attempt budget at Q10 without reaching 3/3. Q10's root
gates are `HARNESS_PASS`, `WATCHER_PASS`, and `MANAGER_EVIDENCE_INSUFFICIENT`; the comparable count
is `0/3`. Root reversed receipt/wait-finish records and published empty response lane IDs, so all
four genuine requests are unclassifiable even though the native harness surfaced them and the
watcher correctly failed closed. Q11 is forbidden. The final category is **Focused implementation
repair required because evidence remains inadequate**, but Q10 verifies no new component-code
defect and authorizes no production repair or further live sprint.
