# Logging and diagnostics: what the harness actually proves

## Short answer

The harness leaves useful, durable evidence for the main lane lifecycle. It is good
enough to investigate many concrete lane failures: provider exit, invalid result,
cleanup failure, lease ownership, queue state, review decision, and hook execution.

It is **not** enough to prove that every feature works, to discover unimplemented
features automatically, or to guarantee that every internal monitor failure is visible.
Logs can show what an implemented path recorded; they cannot prove that a path which
never ran is implemented or provider-native functional. The separate live integration
campaign is still needed for that proof.

This document states the actual evidence written by the current code. It does not add
new logging requirements merely because more logs could be convenient.

## Durable evidence that exists

| Evidence | What it actually records | Where it is written |
| --- | --- | --- |
| Controller status snapshot | Current controller/provider state, result state, cleanup proof, terminal status, process boundary, and copied acceptance advancement | `<lane-worktree>/.agent-workspace/controller.status.json` |
| Controller event log | Timestamped controller lifecycle facts such as provider start/exit, lease acquisition/release, cleanup proof/failure, result validation, acceptance, and shutdown stop | `<lane-worktree>/.agent-workspace/controller.events.jsonl` |
| Provider outputs | Raw provider stdout/transcript stream, stderr, and final parsed message when present | `<lane-worktree>/.agent-workspace/provider-transcript.jsonl`, `provider-stderr.txt`, `last-message.txt` |
| Authoritative lane record | Lane/run identity, paths, lifecycle, provider session, controller identity, and last reported actionable status | `<runtime>/epochs/<epoch>/lanes/<lane>/lane.json` |
| Manager queue | Each manager event, state-transition history, close summary, and any delivery-history receipt that was actually recorded | `<runtime>/manager/QUEUE.json` |
| Worker inbox/outbox | ROOT-to-worker assignment state and unprocessed/processed worker escalation files | `<lane-worktree>/.agent-workspace/QUEUE.json`, `manager-notifications/`, `processed-notifications/` |
| Lease record | Current resource holder's resource, lane/run, exact process identity, and acquisition time | `<runtime>/resources/leases/*.lease` |
| Monitor record | Monitor PID/creation identity, health, heartbeat timestamp, and requested-stop state | `<runtime>/monitor/MONITOR.json` |
| ROOT-hook evidence | One liveness line for each wrapper invocation and, only when one is actually written, a delivery receipt line | ROOT workspace `.agent-workspace/root-hook-liveness.jsonl` and `root-hook-delivery.jsonl` |
| Review/acceptance decision | ROOT's review finding, acceptance/rejection decision, hashes, evidence references, and commit | `<runtime>/epochs/<epoch>/lanes/<lane>/COMPLETION_REVIEW.json` and `ORCHESTRATOR_ACCEPTANCE.json` |

The controller event log is append-only. Most JSON state records are written through
the repository's lock-and-atomic-replacement helpers, so a reader sees an old complete
record or a new complete record rather than a normally half-written replacement.

## What an operator can diagnose from those records

For an active or recently finished lane, a person can normally answer these questions
from the runtime files:

- Did the controller start? The lane record and controller event log show its identity
  and `controller_started` event.
- Did the provider start, exit, or fail to start? The controller event log, status
  snapshot, transcript, and stderr show this.
- Was a result valid? The status snapshot records `valid` or `invalid`, and the actual
  `RESULT.json` is available for inspection.
- Did cleanup finish before resource release? `cleanup_proven`, the process-boundary
  record, controller events, and lease file presence show the answer.
- What did the monitor surface to ROOT? The manager queue records the event and its
  history. It also preserves the close summary supplied by ROOT.
- What did ROOT decide at review? The review/acceptance pair contains the explicit
  finding and approval decision.
- Which exact process a lease refers to? The lease record stores PID plus creation time,
  rather than a broad provider process name.

## What the records cannot truthfully prove

### They cannot prove an unexecuted feature exists or works

No runtime log can prove that every supported provider discovered its native hook,
honored the hook's output, resumed a real session, or completed a real coding lane if
that path was never run. Static/unit tests and fixture tests validate code structure;
they are not durable native-provider evidence.

The existing uncompleted live integration/M09 work is therefore an **evidence gap**.
It must be reported as unverified, not silently inferred from the presence of hook files
or from a passing mocked test.

### A fresh monitor heartbeat is not proof that every lane was processed correctly

`monitor._monitor_pass()` catches an exception while reading an individual lane and
continues. The outer monitor loop also catches arbitrary pass exceptions and continues.
Neither path writes an error record. `_heartbeat()` can subsequently write a fresh
healthy heartbeat.

This means an operator can see a live monitor with a current heartbeat while one lane
was silently skipped because its record could not be read or an unexpected exception
occurred.

In normal harness operation, this is unlikely to be a practical lane-record problem.
`lane.json` is written through a temporary sibling file, flushed, and atomically renamed
into place. Normal concurrent harness reads therefore see the old complete record or the
new complete record, not a half-written JSON record. A read failure would normally need
external/manual runtime-file modification, an unusual filesystem/permission/antivirus/
sync-client failure, pre-existing corruption, or a future bad writer.

Accordingly, this is recorded as an unlikely diagnostic limitation, **not** as a planned
correctness fix. It remains distinct from the master-spec-required watched-lane-count gap
recorded in the master-spec comparison document.

### Queue delivery evidence is currently incomplete

The code only appends an event-level `DELIVERED` history entry when the ROOT hook receives
`HARNESS_EVENT_ID`. The normal harness route does not set that variable. A liveness line
can therefore prove that a hook wrapper ran while the manager queue still has no delivery
receipt for its pending event. This is an implementation gap, documented separately in
`../code_intended_vs_real_gaps/MASTER-SPEC-VS-REAL-IMPLEMENTATION.md`.

### Some public recovery actions have no separate durable audit trail

Normal controller lease acquisition/release is recorded in `controller.events.jsonl`.
The public `lease force-release` command validates, removes, and read-backs one lease,
then returns a structured CLI response. It does not append a separate operation record to
the runtime. Afterward, the absence of the lease proves it is gone, but the harness does
not independently record who invoked the command or why. This is an actual limit of the
current evidence, not labeled here as a master-spec defect because the master spec does
not require a separate force-release audit log.

## Practical conclusion

For a specific lane that has used the controller path, the harness retains enough files
to perform a useful forensic investigation. For the broader question, "is the harness
fully implemented and working on every supported CLI?", the answer is no: the current
logs alone cannot establish that. Use the records above together with the explicit live
integration test results, and treat absent native-provider evidence as unverified rather
than as success.

## Source basis

- `harness-single/orchestrator_harness/controller.py`
- `harness-single/orchestrator_harness/monitor.py`
- `harness-single/orchestrator_harness/manager_queue.py`
- `harness-single/orchestrator_harness/root_hook_wrapper.py`
- `harness-single/orchestrator_harness/review.py`
- `harness-single/orchestrator_harness/leases.py`
- `new_harness_docs/master_docs/harness-master-spec.md`, Parts VIII–XII
