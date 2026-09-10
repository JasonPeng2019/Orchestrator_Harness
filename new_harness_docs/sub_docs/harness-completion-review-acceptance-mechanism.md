# Harness defect: no executable completion-review or acceptance mechanism

Observed: 2026-08-24.

> **Status: current detailed v2 target contract.** Current-reader observations
> explain the candidate defect; the proposed public completion route is the v2
> target and is subject to the master planning decision index.

## Scope

This document describes the pointed-at neutral harness:

```text
<root-workspace>/<harness-root>
```

It is a recommendation for a future neutral-harness repair. It is not present in
that checkout, is not present in the frozen firmware campaign runner, and has not
been implemented by this document.

## Current implementation: the files are read, but no product code creates them

The current canonical task-advancement reader expects this fixed chain in the
canonical workspace:

```text
TASK CARD
  -> RESULT.json
  -> COMPLETION_REVIEW.json
  -> ORCHESTRATOR_ACCEPTANCE.json
```

`RESULT.json` is a worker result. `COMPLETION_REVIEW.json` is a review record.
`ORCHESTRATOR_ACCEPTANCE.json` contains the final `ACCEPTED` or `REJECTED`
verdict. The reader checks that the card/result/review/acceptance hashes and IDs
refer to the same task and commit. If both review files are absent, the task is
still `ACCEPTANCE_PENDING`; if only one exists, the chain is an error.

The controller can then copy a valid `ACCEPTED` advancement into its own status.
On a later canonical resume, that status/advancement prevents another resume.

The problem is how those two review files appear. In the non-test neutral-harness
code:

- `task.py` reads and validates them; it does not write either file.
- `lane_controller.py` reserves their names, reads the validated chain, and writes
  `ACCEPTED` only into controller status; it does not write either review file.
- The public CLI has no `review`, `accept`, or equivalent command that creates the
  files.
- `lane retire --acceptance-ref <file>` accepts a reference to an already-existing
  file for retirement/archive work. It does not create acceptance.
- No controller event, manager-queue event, provider hook, monitor condition, or
  generated ROOT prompt says that review is now required.

Therefore the literal current flow is:

```text
worker finishes
  -> controller validates or rejects RESULT.json
  -> nothing tells ROOT that review is required
  -> some outside process must somehow create both review files
  -> controller can later read them and mark its status ACCEPTED
```

ROOT is only the intended author by convention. The current parser merely requires
`accepted_by` to be a non-empty string. It does not require `ROOT`, authenticate a
ROOT session, require a controller-owned command, restrict write access, or prove
which process wrote the file. A worker or any other process with workspace write
access could write a correctly linked pair of records. The controller would not know
that the wrong process made the verdict.

The worker cannot make itself accepted merely by setting `acceptance_state` in
`RESULT.json`; the separate review and acceptance records are still required. But
the missing writer/ownership boundary still means the harness has no actual way to
make its intended ROOT decision happen.

## Required replacement: one public review path for both lane profiles

For v2, the two harness-written decision files have fixed lane-record paths:

```text
<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/COMPLETION_REVIEW.json
<runtime-root>/epochs/<epoch-id>/lanes/<lane-id>/ORCHESTRATOR_ACCEPTANCE.json
```

They belong to the lane's current `run_id` recorded in `lane.json`; the public
completion command replaces them only after validating the managed event's
lane/run pair or the plain lane record's current lane/run pair.

The review and acceptance mechanism is deliberately still complete when the
optional managed-coordination package is disabled:

| Lane profile | How ROOT learns/reviews | What is deliberately absent |
| --- | --- | --- |
| Managed | The controller records `review_pending` (or `result_invalid`) status in its worktree records. The persistent monitor, the sole producer of ROOT events, promotes that status change to a `COMPLETION_REVIEW_REQUIRED` (or `LANE_RESULT_INVALID`) event in the fixed manager queue. ROOT acknowledges it and runs the review command with `--event-id`. | Nothing; this is the full manager workflow. |
| Plain | The controller records terminal result validation in `lane.json` and its normal worktree records. ROOT invokes the same public review command with `--lane-id`; it reads only the controlled lane record and current artifacts. | No manager event, queue, hook notice/Stop gate, delivery receipt, or `LANE_RESUME_REQUIRED` event. A declared hardware lease, when requested, remains normal controller behavior. |

Plain does not mean auto-accept. ROOT still makes the same factual
`PASS`/`FAIL`/`BLOCKED` review and separate `ACCEPTED`/`REJECTED` decision through
the harness-owned command; it simply reaches that command directly instead of
through a queue notification.

After the provider has reached a terminal state, the lane controller already knows
the lane ID, current `run_id`, task card, result path, result-validation outcome,
and controller evidence paths. In both modes it records the terminal
result-validation outcome and sets the actionable status (`review_pending` or
`result_invalid`) in `lane.json` and its worktree records; it never writes the
manager queue. In managed mode the persistent monitor promotes that status change
to the ROOT-targeted manager event on its next pass; in plain mode ROOT reaches
the same recorded state directly. It must not accept its own work in either mode.

The decision tree is:

```text
provider ends
  -> controller validates RESULT.json for this lane run
     |
     +-- result missing, malformed, wrong-task, or contradictory
     |     -> controller sets result_invalid status in its worktree records
     |        managed: monitor promotes the status change to one ROOT
     |                 LANE_RESULT_INVALID event on its next pass
     |        plain: the recorded invalid state is read directly
     |     -> do not offer completion review or acceptance
     |
     +-- result is structurally valid
           -> controller sets review_pending status in its worktree records
              managed: monitor promotes the status change to one ROOT
                       COMPLETION_REVIEW_REQUIRED event on its next pass
              plain: the lane is ready for direct completion review
```

"Structurally valid" means the result belongs to the exact lane/task and has the
required valid record shape. It does **not** mean the task passed. A valid result can
say `PASS`, `FAIL`, or `BLOCKED`.

- A valid `PASS` is a candidate ROOT may accept after review.
- A valid `FAIL` or `BLOCKED` is still a coherent report. ROOT must review it and
  normally record `REJECTED`, or take the separately documented recovery action.
- An invalid result is not a review candidate. ROOT receives the concrete failure
  event instead and must repair, relaunch, or otherwise investigate.

The controller is never a queue producer. It writes only its own worktree records
and sets the actionable status; the persistent monitor is the single producer of
all ROOT events, promoting the completion-review status change on the same
status-driven path it already uses for lane-health events and consuming
worker-outbox escalations by moving them to `processed-notifications/`. Because
one component owns promotion, there is no controller/monitor duplication to
reconcile: the lane event log stays a permanent worktree audit record and is
never drained into the inbox. In plain mode the monitor has no queue route and
the controller's recorded `review_pending`/`result_invalid` state is read
directly.

### One controller terminal transition, one review event

For a managed lane, the controller sets the terminal `review_pending` status once
when its provider run reaches a terminal result-validation outcome. The monitor
promotes that status change to exactly one event, deduped by the lane's
`last_reported_actionable_status`: while the status is unchanged it is not
re-promoted, and it writes the resulting completion-review event ID into that
lane's record. A later resumed or newly launched run is a new controller terminal
transition and produces its own status change, which the monitor promotes as a
new event.

For a plain lane, the equivalent one-time fact is the lane record's terminal
validation and `review_pending` state. It has no event ID, delivery receipt, or
queue state. Later monitor passes may report the controller/lane health, but they
must not create a synthetic manager event for a profile that explicitly disabled
event delivery.

### Lightweight crash recovery for a lost review event

This harness is not mission-critical and does not promise exactly-once event
publication. A startup health check may discard a malformed temporary record or
reset a malformed manager queue. That is allowed to
lose an in-flight notification, but it must not permanently strand a valid
finished lane.

After that health check, managed monitor reconciliation may create one
**replacement** `COMPLETION_REVIEW_REQUIRED` event only when all of these facts
hold: the lane has a terminal, structurally valid `RESULT.json`; neither a
complete linked review/acceptance pair nor an open matching review event exists;
and the lane record identifies that same `run_id`. The replacement is recorded
in the lane record as recovery evidence. It is a new request for ROOT to review
the same finished work, not a replay that claims the lost event was acknowledged
or handled. Plain reconciliation merely preserves or restores the direct
`review_pending` lane state after removing a broken artifact; it creates no queue
record.

If an interrupted review publication leaves a malformed or incomplete
`COMPLETION_REVIEW.json` / `ORCHESTRATOR_ACCEPTANCE.json` pair at the known
harness-owned paths, health recovery removes that broken pair and leaves the
lane acceptance pending. It writes no replacement acceptance and never infers
`ACCEPTED` from one surviving file. In managed mode ROOT receives a replacement
review event; in plain mode ROOT uses the direct review command again. No replay
service, distributed transaction, or attempt to reconstruct partial ROOT
reasoning is required.

## Exact managed ROOT event contents

The event must contain a generated, literal ROOT instruction block. It must not ask
ROOT to reconstruct the task from a vague lane label or a provider transcript.

The durable event payload contains:

```text
event ID
kind: COMPLETION_REVIEW_REQUIRED
target: ROOT
lane ID and current `run_id`
provider ID and provider terminal outcome

task card:
  exact original task-card text
  recorded task-card identity/hash
  source path for reference

worker result:
  exact RESULT.json text
  recorded result identity/hash
  source path for reference

controller evidence:
  exact status/event-log/transcript/stderr/last-message paths
  result-validation state and detail

review criteria:
  the original task-card completion criteria and required checks,
  copied verbatim from the task card
```

The event's ROOT-facing text is a deterministic template populated from that bundle,
for example:

```text
Completion review is required for lane <lane-id>, run <run-id>.

Review the verbatim task card and RESULT.json stored in this event. Do not accept
the work merely because the provider exited successfully. Check every completion
criterion and required check in the copied task card against the result and listed
evidence paths.

When the review is complete, run:

  operator_launch lane completion-review --event-id <event-id> \
    --review-outcome PASS|FAIL|BLOCKED \
    --approval ACCEPTED|REJECTED \
    --review-summary "<ROOT's actual reasoning>" \
    --evidence <path> [--evidence <path> ...]

`--review-outcome` and `--approval` are two independent, both-required fields on
this one command — a factual finding AND a separate decision. They are not two
names for one thing and not alternatives to pick between. `--review-outcome` is the
finding (did the work pass?): `PASS`, `FAIL`, or `BLOCKED`, recorded in
`COMPLETION_REVIEW.json`. `--approval` is ROOT's accept/reject decision: `ACCEPTED`
or `REJECTED`, recorded in `ORCHESTRATOR_ACCEPTANCE.json`. One rule links them:
`ACCEPTED` requires a `PASS` finding; `REJECTED` may accompany any finding. Neither
field is `manager close --outcome COMPLETE|BLOCKED` — that is a different command
that closes a manager-queue event, and its `BLOCKED` is an event-close state, not
this review's `BLOCKED` finding. Do not hand-write either artifact.
```

The normal ROOT queue rules still apply: a delivery receipt or the idle watch returning
does not acknowledge the event. ROOT finishes its current ROOT task first, then
explicitly acknowledges this event, performs the review, and closes it.

## New public ROOT action: `lane completion-review`

The neutral harness needs one public ROOT-facing command with two mutually
exclusive, profile-matched sources:

```text
operator_launch lane completion-review \
  --event-id <completion-review-event-id> \
  --review-outcome PASS|FAIL|BLOCKED \
  --approval ACCEPTED|REJECTED \
  --review-summary "<reasoning>" \
  --evidence <path> [--evidence <path> ...]
```

For a plain lane the command is identical except that it receives the controlled
lane identity directly:

```text
operator_launch lane completion-review \
  --lane-id <lane-id> \
  --review-outcome PASS|FAIL|BLOCKED \
  --approval ACCEPTED|REJECTED \
  --review-summary "<reasoning>" \
  --evidence <path> [--evidence <path> ...]
```

In managed mode, `event-id`, not a free-form worktree path or lane path, is the
command's source of truth. The event already fixes the exact lane, `run_id`,
fixed decision-file paths, card, result, and review request. In plain mode,
`lane-id` resolves only through the controlled current epoch/lane directory; the
command then requires `lane_mode: plain`, an unaccepted terminal lane, and a
current `review_pending` record. `--event-id` and `--lane-id` cannot be combined,
and neither form accepts a caller-supplied worktree or artifact path.

Distinct from that source choice (`--event-id` vs `--lane-id`), every call also
carries **two independent, both-required fields** — a finding and a decision, given
together, never chosen between: `--review-outcome` is the factual finding
(`PASS`/`FAIL`/`BLOCKED`, written to `COMPLETION_REVIEW.json`) and `--approval` is
ROOT's separate accept/reject decision (`ACCEPTED`/`REJECTED`, written to
`ORCHESTRATOR_ACCEPTANCE.json`), linked only by the rule that `ACCEPTED` requires a
`PASS` finding. Neither is the `manager close --outcome COMPLETE|BLOCKED`
event-close vocabulary, which belongs to a different command.

The command is backed by one product-owned generic Python entry point in the
harness source. It is not adapter code and is not a script ROOT copies or writes
at runtime. The selected provider adapter only installs the ROOT skill that tells
ROOT to invoke this public command.

### What the command does

1. In managed mode, opens the fixed `<runtime-root>/manager/QUEUE.json` under the
   normal short queue-file lock and requires an existing ROOT-targeted
   `COMPLETION_REVIEW_REQUIRED` event in state `ACKNOWLEDGED`. It rejects unknown,
   already-closed, wrong-type, or unacknowledged events. In plain mode, opens the
   authoritative `lane.json` under its lane-record lock and requires the direct
   review-pending state; it never opens a queue.
2. Reads the task/result snapshot from the managed event or the exact current
   task/result references in the plain lane record, then makes one narrow current
   identity check of the task card and `RESULT.json` before publication. This is
   not a general evidence sweep: it compares only those two current records with
   the snapshot identities ROOT reviewed.
3. Validates its direct user input: a permitted `review-outcome`, a permitted
   `approval`, a non-empty review summary, and the stated evidence references.
   `ACCEPTED` requires `review-outcome PASS`; `REJECTED` may accompany any of the
   three factual review outcomes.
4. Constructs the exact current-format `COMPLETION_REVIEW.json` and
   `ORCHESTRATOR_ACCEPTANCE.json` content from the managed event bundle or plain
   lane bundle, plus ROOT's separate factual review outcome, approval decision,
   summary, and evidence.
5. Writes those two files through the public harness route to the fixed lane-record
   paths above. ROOT never opens the worker worktree or writes the files itself.
6. For a managed lane, records the output paths, review outcome, and approval in
   the same queue event's history, writes the approval state to the lane record,
   then changes the review event to `COMPLETE` for a successful command. For a
   plain lane, it writes the same approval state and output paths to `lane.json`
   under the lane lock, with no queue update.
7. For `REJECTED` only, a managed lane writes one new `LANE_RESUME_REQUIRED` event to the same
   ROOT manager `QUEUE.json`. That event contains the exact lane ID/current `run_id`,
   the saved provider/session reference, ROOT's review rationale, and a literal
   instruction to use the `resume-lane` skill with a new resume card. It does not
   launch a provider or resume the lane automatically. A plain lane writes no
   event; its structured command result says `resume_required: true`, and ROOT
   may directly use `resume-lane` with the same lane ID.

The command is the only supported writer of the two acceptance artifacts. Each atomic
write uses a same-directory temporary sibling of its final lane-record path and
consumes that temporary sibling by renaming it to the final path on success. Its
failure cleanup removes any unconsumed sibling before releasing the record lock.
There is no temporary registry, generic staging directory, or claim that two
File replacements are one operating-system atomic transaction.

### One final source identity check, not a general hash sweep

The command deliberately does not run another general hash sweep. The task-card and
result identities captured at event creation identify exactly what ROOT reviewed.
Immediately before publication, it compares only those two current records with the
snapshot. If they still match, the public command writes the linked pair normally.
It does not re-hash every evidence path or provider transcript.

This prevents a successful command from publishing acceptance for records that changed
while the event waited. The normal reader continues to validate the fixed artifact
chain later as its own independent protection.

### Failure behavior

- `RESULT.json` invalid or missing: a managed controller creates
  `LANE_RESULT_INVALID`; a plain controller records that state in `lane.json`.
  Neither form may publish a review/acceptance pair until the result is repaired.
- Managed event not acknowledged: ROOT must first read/acknowledge it through the
  ordinary manager queue route. Plain review has no acknowledgement step.
- Invalid command input or output failure: do not change the verdict or close the
  event. Leave it `ACKNOWLEDGED` with a recorded command failure so ROOT can correct
  the input or classify it `BLOCKED`.
- Current task/result identity differs from the queued snapshot: return
  `COMPLETION_REVIEW_STALE_SOURCE`, leave the event `ACKNOWLEDGED`, and record a
  warning that names the changed paths. ROOT normally resumes the lane so it can
  publish a new result. If ROOT has inspected the difference and judges it harmless,
  it may retry with `--force-accept --force-reason "<why the change is harmless>"`.
  A forced approval still requires a structurally valid *current* task/result chain,
  writes the current identities into the artifacts, includes the force reason in the
  permitted review summary and event history, and never accepts a malformed or
  unrelated result.
- Existing review/acceptance artifacts conflicting with this event: fail closed;
  do not overwrite an unrecognized file. ROOT receives/records the conflict as an
  actionable problem.
- A malformed manager queue (managed only), malformed temporary record, or
  incomplete harness-owned review/acceptance pair is handled by the lightweight
  health recovery above: remove the broken record(s), leave the lane unaccepted,
  and let normal managed reconciliation issue a replacement review event or
  plain reconciliation restore direct review-pending state when the terminal
  result remains valid.
- A `REJECTED` verdict does not turn the lane into a pass. It marks the lane
  `REJECTED`; managed mode creates the separate `LANE_RESUME_REQUIRED` ROOT queue
  event, while plain mode returns direct resume-required output. ROOT decides the
  new resume task; the command does not restart a provider.

### ROOT skill: `review-lane-completion`

Setup installs a ROOT-only skill named `review-lane-completion`. It tells ROOT to:

1. in managed mode, finish the current ROOT task, read the queued
   `COMPLETION_REVIEW_REQUIRED` event, and acknowledge its top-level event ID;
   in plain mode, identify the terminal `review_pending` lane through its
   controlled lane record;
2. compare the copied task criteria, `RESULT.json`, and cited evidence;
3. run the public command with the factual `PASS`, `FAIL`, or `BLOCKED` review
   outcome, the separate `ACCEPTED` or `REJECTED` ROOT approval, and a truthful
   review summary; and
4. never hand-edit `COMPLETION_REVIEW.json`, `ORCHESTRATOR_ACCEPTANCE.json`, a
   lane record, or `QUEUE.json`.

When ROOT chooses `REJECTED`, this skill ends after the review command. Managed
mode receives the new `LANE_RESUME_REQUIRED` event; plain mode receives the
command's direct resume-required result. In both cases the existing `resume-lane`
skill supplies the new resume card, rationale, and instructions. Keeping the two
skills separate prevents a review decision from silently becoming an automatic
provider relaunch.

## Ownership boundaries

```text
Worker
  writes RESULT.json and worker evidence only.

Lane controller
  validates the result and writes one completion-review request event.
  It never writes ACCEPTED or REJECTED.

ROOT
  receives the managed event or directly selects a plain lane, makes the actual
  review decision, and invokes the public `lane completion-review` command.

Public `lane completion-review` command
  is the only supported writer of COMPLETION_REVIEW.json and
  ORCHESTRATOR_ACCEPTANCE.json. It writes ROOT's factual review outcome and separate
  approval decision; it does not decide either one. On rejection it writes the
  resume-required event only in managed mode; plain mode returns the same next
  action directly without creating a queue event.
```

This is an operational ownership boundary. The v2 MVP explicitly uses
**cooperative local trust**: ROOT and workers are expected to follow the public
harness routes, and the harness detects malformed or contradictory artifacts but
does not defend against a malicious local process deliberately forging acceptance
files. `ACCEPTED` therefore means a ROOT workflow decision recorded through the
public command, not a cryptographic or operating-system security guarantee.

No permissions, separate operating-system identities, or signatures are part of
this MVP. If a future product must prevent a worker or another local process from
forging approval, that is a separate security feature requiring an enforced
identity/write-permission boundary.

## Observable acceptance criteria for the repair

1. A disposable managed lane with a valid `PASS` result creates exactly one
   ROOT-targeted `COMPLETION_REVIEW_REQUIRED` event containing the exact task card,
   result, criteria, and evidence paths. A disposable plain lane records the same
   valid terminal facts as direct review-pending state and creates no event.
2. Managed ROOT idle watch returns for that event; its static hook reminder may
   report it while ROOT is busy, but neither mechanism acknowledges it. Plain
   watch returns a changed lane status without opening a queue.
3. A valid `FAIL` and a valid `BLOCKED` result each create the matching managed
   review event or plain direct review-pending state. Neither is auto-accepted.
4. A missing, malformed, wrong-task, or contradictory result creates an actionable
   managed `LANE_RESULT_INVALID` event or plain recorded invalid state, and no
   completion-review artifact.
5. Re-reading the same terminal lane/result creates neither a second managed
   event nor a second plain review state during a healthy run. A recorded health
   recovery may reissue one managed review event or restore the existing plain
   review-pending state after a malformed queue/artifact was removed. A resumed
   or later lane run has its own terminal transition.
6. Managed `lane completion-review --event-id ... --review-outcome PASS --approval
   ACCEPTED ...` can operate only on the acknowledged matching event. Plain
   `lane completion-review --lane-id ...` can operate only on its controlled
   review-pending lane. Both forms write a linked `PASS` review plus `ACCEPTED`
   approval pair through the public route; only the managed form records/closes
   a queue event.
7. Before ordinary publication, the review command compares the current task/result
   identities with the reviewed snapshot. A mismatch remains actionable; a forced
   approval requires ROOT's recorded reason and still validates the current chain.
8. `REJECTED` records a completed ROOT review but never becomes a lane or campaign
   pass. It marks the lane `REJECTED`, writes one `LANE_RESUME_REQUIRED` event
   only for a managed lane, and returns direct resume-required output for a plain
   lane; no provider is restarted until ROOT uses `resume-lane` with a new resume
   card.
9. No controller code path can write an `ACCEPTED` verdict; no worker command is
   offered a path to write either review artifact.
10. A failed review command, existing conflicting artifact, or invalid result leaves
    no false acceptance and remains actionable for ROOT.
11. A malformed temporary, managed queue, or review record is removed by health
    recovery. If the terminal result remains valid and unaccepted, normal managed
    reconciliation creates one replacement `COMPLETION_REVIEW_REQUIRED` event and
    plain reconciliation restores direct review-pending state; no lost event or
    partial approval is claimed handled or accepted.
