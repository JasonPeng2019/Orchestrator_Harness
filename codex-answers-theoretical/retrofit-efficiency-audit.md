# Retrofit Efficiency Audit

Date: 2026-08-06

## Scope

This audit asks which inefficiencies remain after accounting for the changes already made to task cards, fast lanes, pooled testing and review, support-failure isolation, rehearsal, and scoped revalidation.

The finalized topology and new skill were written after the last recorded lane run. The logs therefore prove the old behavior, while the current files show whether a preventive rule or mechanism now exists.

## Confirmed remaining inefficiencies

### 1. Excessive micro-dispatch and oversized thread reuse

This is the largest remaining compute issue.

Evidence from the recorded run:

- 395 Codex starts represented only 151 worker IDs.
- 243 starts were additional starts or resumes.
- 98 resumes completed in under one minute.
- Resume processes consumed 477.7 agent-minutes.
- Scoped transcripts recorded 421 completed turns, 2.102 billion input tokens, 84.2 million uncached input tokens, and 10.58 million output tokens.
- S2.P alone recorded 68 turns and 744.6 million input tokens.
- Some late, narrow continuations processed 20–26 million input tokens each.

Cached input is cheaper, and not every continuation was waste. However, repeatedly resuming a very large thread for small corrections clearly reprocessed much more context than the correction required.

The original task-card rule reduced initial reading but did not explicitly require the orchestrator to:

- batch compatible continuation instructions;
- let one dispatch finish its complete logical task;
- close the thread after that task is accepted;
- start a compact, fresh task card when later work no longer needs the old conversation.

Strict fast-lane correction and the single report-only retry should remain in the same thread. Unrelated later work should not.

Resolution: the active task-card contract and topology skill now bind one thread to one logical task.
Only unfinished same-task work, the report-only retry, and the strict fast lane may resume it before
acceptance; an accepted thread is terminal. C74 and mandatory post-S4 stage S5 implement and test the
candidate enforcement before final C0.

### 2. No active/archive lifecycle for lanes

The runtime keeps scanning and retaining completed lanes as though they were still active.

Observed state:

- 123 registered runtime Git worktrees remain.
- Runtime state contains about 49,000 files and occupies about 972 MB.
- Worktrees occupy about 440 MB.
- Raw worker transcripts occupy about 136.6 MB.
- Retained Python caches occupy about 58.8 MB.
- A read-only implementation-suite scan took 12.96 seconds.
- A read-only final-suite scan took 4.62 seconds.

The implementation and final configurations still use broad lane globs, and discovery revisits every matching lane on each scan. Neither the active plan nor the new skill explicitly requires the system to:

- move accepted terminal lanes outside the active scan set;
- close their Git worktrees after preserving evidence;
- retain transcripts as archive-only data;
- remove disposable bytecode and caches.

This directly increases later filesystem scans, Git worktree operations, and audits.

Resolution: C75 and S5 add evidence-first terminal-lane retirement, active-scan exclusion, safe Git
worktree closure, archive-only transcript/result retention, and disposable-cache removal. One audited
retirement pass applies only to individually proven eligible V2 lanes; protected historical,
dirty/ambiguous, live, unretained, or unpreserved state remains untouched.

Relevant files:

- [`implementation-harness.json`](../plans/general-coding-harness/runtime/firmware-v2/implementation-harness.json)
- [`discovery.py`](../stable-general-harness-runner/orchestrator_harness/discovery.py)

### 3. Read-only workers still receive full worktrees

Of 58 recent candidate-worktree prompts, 46 explicitly described read-only work, yet each lane received a complete registered worktree.

A static reviewer generally needs an immutable view of the exact source commit plus a separate result directory, not a writable checkout. A test executor needs isolated output and temporary storage, but does not always need another complete source worktree.

The topology format permits a run root and worktree but does not state the narrower rule: allocate a worktree only when source mutation or source-local isolation actually requires one.

This differs from the archival problem: this rule prevents unnecessary worktrees from being created; the lifecycle rule removes necessary worktrees once they are finished.

Resolution: C76 and S5 add an `immutable-read-only-view` mode with exact source identity and a
separate result root. Full linked worktrees remain for mutation or source-local execution. The
topology skill now requires every lane to state its source-allocation mode and reason.

### 4. Concurrent event-log writing corrupted evidence

The shared lane event log contains a malformed record at line 745, and the corresponding concurrent reviewer-start event is missing. The corruption occurred during two concurrent C0 launches.

The stable and candidate lane controllers append to the same file without cross-process serialization:

- [`stable lane_controller.py`](../stable-general-harness-runner/orchestrator_harness/lane_controller.py)
- [`candidate lane_controller.py`](../plans/general-coding-harness/runtime/firmware-v2/worktrees/harness-candidate/orchestrator_harness/lane_controller.py)
- [`LANE_EVENTS.jsonl`](../plans/general-coding-harness/runtime/firmware-v2/events/LANE_EVENTS.jsonl)

This did not cause a documented multi-hour delay, but it is a confirmed evidence-integrity defect. A missing start or exit record can force manual reconstruction or invalidate evidence.

The harness should put a cross-process lock around each append. If another Codex process is writing,
it must wait until the lock is released before writing its complete log record. Add a concurrent-write
regression test that proves records remain complete and ordered safely; separate per-controller logs
are unnecessary for this fix.

Resolution: C77 and S5 require exactly that lock and a real concurrent-process regression test.
The frozen stable runner is not modified; the feature is implemented and certified in the
dogfooded candidate before final release gates.

## Compute accounting and compaction

Token accounting is useful for deciding whether a long-running thread needs compaction, but it is not
waste by itself. The worker transcript contains usage details while central lane artifacts do not
aggregate them. Record at least cached and uncached input tokens so a future controller can use
uncached usage as the compaction signal; cached usage is cheaper and should not trigger compaction by
itself.

The installed Codex CLI has automatic `remote_compaction_v2` enabled. However, the current headless
lane controller launches `codex exec`, writes one prompt to stdin, and closes stdin. `codex exec`
does not expose an interactive `/compact` control in its command-line interface, so the orchestrator
cannot currently send `/compact` to a running headless worker. Manual threshold-triggered compaction
would require a runner change that maintains a bidirectional interactive/app-server session; it is
not a documentation-only rule. Until then, record the token counts and rely on the CLI's automatic
compaction rather than claiming that the harness enforces `/compact`.

## Rules that remain only partly explicit

### Pooling

The active plan is strong, but the reusable topology rule should say explicitly:

1. Freeze one candidate tip.
2. Finish all compatible review, test, and observer lanes against that tip.
3. Join and deduplicate their findings once.
4. Repair once.
5. Do not repair between compatible lanes unless immediate containment is required.

### Scoped locks

The active plan contains a concrete scoped-lock matrix, but the reusable skill rule is less explicit. It should state:

- editorial changes invalidate no product evidence;
- an evidence-envelope refresh does not rerun the underlying test;
- unchanged dependency fingerprints preserve prior evidence;
- a full relock is an exceptional fallback, not the default response to any document change.

## Conclusion

The major historical review/test looping is covered by the new topology. The four concrete gaps in
this audit are now explicit C74-C77 requirements and mandatory post-S4 S5 candidate work before final
C0. They remain implementation work until S5 passes; they are no longer omitted from the governing
topology.
