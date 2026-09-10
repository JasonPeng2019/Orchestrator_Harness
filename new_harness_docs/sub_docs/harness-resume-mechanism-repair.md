# Resume mechanism: current problem and proposed repair

Updated: 2026-08-29

> **Status: current detailed v2 target contract.** The current-path discussion
> is diagnosis; the one-lane resume protocol below is subject to the master
> planning decision index.

## Scope

This document describes the project-local v2 harness. `<harness-root>` is a child
of ROOT's project workspace; all generated lane state remains below that workspace's
`.harness-runtime/` tree or the lane worktree it contains.

## The current problem

The current resume path makes ROOT manually prove old and new task/prompt hashes
through an amendment-review file before it can ask a saved provider session to
continue. It also treats an old missing or malformed `RESULT.json` as a reason to
block a resume, even though the same session may be needed to repair that result.

That is too much machinery for the actual goal: continue one stopped, unaccepted
lane with the same worktree and provider session, using a new current task.

## Proposed replacement: `resume-lane`

Provide one public command and a small ROOT skill:

```text
operator_launch resume-lane \
  --lane-id <lane-id> \
  --resume-task-card <path-to-new-card> \
  --rationale <why-this-lane-should-continue> \
  --prompt <what-the-provider-should-do-now>
```

ROOT supplies only those four inputs. The command obtains the provider/session
identity, worktree, current artifact paths, and process state from `lane.json`.
ROOT never provides a PID, provider session ID, worktree path, or amendment-review
file.

The `resume-lane` command itself never touches the manager queue. When a rejected
lane is signalled by a `LANE_RESUME_REQUIRED` manager event, closing that event is
the ROOT skill's job, not the command's (see resolution R3 in `harness_single.md`):
the skill directs ROOT to `manager acknowledge` the event, run `resume-lane` with
the new card, then `manager close --outcome COMPLETE` with a summary naming the new
`run_id`. If ROOT decides not to resume, it still closes the event (`COMPLETE`,
summary "not resuming"). The event is closed once ROOT has issued the resume (or
declined), not when the resumed lane is eventually accepted — the resumed run
produces its own fresh completion-review event — so ROOT's Stop gate is never held
open for the duration of the redo.

### One lane; a fresh `run_id` for each provider run

A lane is the durable unit. It has one worktree and one saved provider session
while it remains resumable. There is no generation tree, history directory,
archive step, or formal lineage record. A retired worktree is not a runtime
dependency: the operator may remove it manually, and later setup/epoch/new-lane
work never scans or validates it.

Initial launch and every successful resume assign the lane a fresh opaque `run_id`.
`lane.json` stores the one current `run_id`, current task-card path, provider/session
identity, process identity, and lifecycle state. A current `RESULT.json` and either
completion artifact are valid only when their `{ lane_id, run_id }` matches that
record. This prevents an old result from being reviewed as the new run.

The harness intentionally does not preserve rejected task/result/review artifacts
as a full audit trail. The provider's native session may retain conversational
context, but old harness artifacts may be replaced. An already accepted lane is
terminal and still cannot resume.

### Mechanical behavior

1. Resolve `<lane-id>` only through the controlled epoch/lane records. Reject an
   unknown lane; never accept caller-provided runtime paths.
2. Check the exact controller/provider process identities. If the lane is still
   live, return `LANE_RUNNING`; do not launch a second provider.
3. If the lane is `ACCEPTED`, return `ALREADY_ACCEPTED`. A separate accepted work
   item needs a new lane.
4. Check that this stopped unaccepted lane's recorded worktree still exists and is
   safe. If an operator removed it, return `RESUME_WORKTREE_MISSING`; do not
   recreate a different worktree and claim that the old provider session was
   preserved. A new lane is the honest next action.
5. Read the saved provider session. If absent, return `NO_SAVED_SESSION_ID`.
6. Validate that the new task card is readable and structurally valid. It may differ
   freely from the prior task; no old/new hash comparison or semantic-change
   classification is required.
7. Under the lane-record lock, generate a fresh `run_id`, set the lane state to
   `RESUMING`, replace the current task/rationale/instruction fields, and clear the
   current `RESULT.json`, `COMPLETION_REVIEW.json`, and
   `ORCHESTRATOR_ACCEPTANCE.json`. For a managed lane, also empty the worker
   incoming `.agent-workspace/QUEUE.json` to a valid empty queue carrying the fresh
   `run_id`, so no assignment from the prior run survives into the resumed run (see
   resolution R8 in `harness_single.md`). The public harness route performs those writes;
   ROOT does not edit the files. Its atomic replacement temporary files are
   same-directory siblings; successful replacement consumes each sibling as its
   final file, while failure cleanup deletes an unconsumed sibling before the
   lane-record lock is released.
8. Build one native provider-resume message containing the rationale, the new current
   task card, and the new instructions. The saved provider session already contains
   the earlier conversation; the harness does not copy or archive it.
9. Invoke the provider's native resume command using the saved session. If Codex,
   Claude, or Qwen reports that the session is expired or unknown, return that
   provider error verbatim and mark the lane resumable again; do not fabricate a
   new session.
10. Record the new exact child-process identity in `lane.json`. After that controller
   is live, atomically replace this lane's entry in `active-lanes.json` with the
   same fresh `run_id`, then mark the lane `RUNNING`. The eventual result must carry
   the lane's fresh `run_id`.

An interrupted step 6 leaves the lane `RESUMING`, with no current valid result.
Health reconciliation removes only malformed current artifacts and leaves the lane
eligible for the same public resume command. It does not try to reconstruct or
archive an old attempt.

## What remains deliberately strict

| Condition | Deterministic result | Why it remains |
| --- | --- | --- |
| Lane is already accepted | `ALREADY_ACCEPTED` | Credited work is terminal. |
| Exact lane process is alive | `LANE_RUNNING` | A second provider could corrupt the same worktree/session. |
| Recorded resumable worktree was removed | `RESUME_WORKTREE_MISSING` | The harness will not fabricate a replacement worktree for an existing provider session. |
| No saved provider session | `NO_SAVED_SESSION_ID` | The harness has no native session to resume. |
| Provider rejects saved session | Provider error, recorded verbatim | Only the provider knows whether that session exists. |
| New card is invalid | `INVALID_RESUME_TASK_CARD` | The worker needs one usable current contract. |
| Lane-record/current-artifact update fails | `RESUME_LANE_WRITE_FAILED` | The new run must never be mistaken for the old one. |

## Result and acceptance after resume

The normal final-result route validates the new `RESULT.json` against both the
current task card and the lane's current `{ lane_id, run_id }`. A stale result is
rejected as `RESULT_STALE_RUN`; it never reaches ROOT review. A structurally valid
`PASS`, `FAIL`, or `BLOCKED` result produces a managed completion-review event in
the managed profile, or makes the same direct `lane completion-review --lane-id`
route available in the plain profile. Neither profile requires a historical
worktree to be present.

If ROOT rejects the work, the lane becomes resumable again. ROOT can submit another
resume card to the same lane and same provider session. No archive, new worktree,
or generation folder is created.

## Observable acceptance criteria

1. ROOT resumes an unaccepted, stopped lane using one lane ID, a rationale, a prompt,
   and a new task card.
2. Resume preserves that lane's worktree and saved provider session.
3. Resume assigns a fresh `run_id`, clears obsolete current result/review state
   (and, for a managed lane, empties the worker incoming queue), republishes the
   live lane's exact `active-lanes.json` entry, and accepts only artifacts that
   name that fresh lane/run pair.
4. A changed task card or prompt does not require an amendment-review record or
   hash-equivalence decision.
5. An accepted lane and a live lane refuse duplicate resume before provider launch.
6. A missing worktree or expired provider session is reported honestly; no
   replacement worktree, session, generation folder, or artifact archive is
   fabricated.
