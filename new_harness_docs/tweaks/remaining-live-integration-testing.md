# Remaining live integration testing

## Status

Static/product tests and the disposable readiness rehearsal are accepted. The
remaining work is real-provider integration testing. No product feature is
currently identified as broken by this gap.

## Where execution stopped

Execution stopped at **M09 live provider/platform admission**, before any real
provider lane was launched. The earlier disposable rehearsal completed 38/38
synthetic control properties, but it used fake local processes and cannot prove
provider CLI or native-hook behavior.

## Required runner prerequisites

Before allocating a live test attempt, provide both of these workspace-confined
identities:

- A native macOS runner and workspace.
- A native Linux runner and workspace stored on native Linux storage.

The current WSL workspace is mounted through Windows `v9fs`; it is not valid
evidence for native Linux storage/process semantics.

Provider authorization is already recorded. Codex and Claude Code are
authenticated, and Qwen Code has a successful safe-mode authentication probe.

## Required pre-live implementation-audit gate

Before M09 begins, complete the repeated independent implementation audit defined in
`pre-live-run-repeated-implementation-audit.md`. ROOT must disposition every finding,
implement and verify the valid ones, then obtain a follow-up pass with no remaining
undispositioned valid gaps. This is a prerequisite to live testing, not a replacement
for it.

## Required test standard: exhaustive, not scoped

M09 must not be reduced to a small "provider started and edited one file"
smoke test. It is an end-to-end harness acceptance campaign. The campaign must
exercise every implemented managed/plain lifecycle feature, every public
command, every recovery route, every provider adapter, and every observable
failure condition that can be created safely in a disposable workspace.

The campaign may use multiple disposable lanes, worktrees, and epochs. It does
not need to force unrelated failures into one lane lifetime. However, it must
produce one durable coverage map from every implemented master-spec requirement
and public command to a real-run scenario and its retained evidence. No feature
may be marked covered merely because a unit test, mock, static source check, or
similar-looking happy-path scenario exists.

### Mandatory exhaustive scenario families

- **Runtime and monitor:** fresh setup, idempotent setup, single-monitor
  ownership, live monitor heartbeat, dead-monitor recovery, hung-monitor exact
  replacement, deliberately stopped monitor, monitor shutdown, and plain-mode
  recovery refusal.
- **Providers and adapters:** actual headless launch, streamed transcript,
  session capture, worker hooks, ROOT hooks, Stop behavior, provider exit,
  cleanup, and resume behavior for Codex, Claude Code, and Qwen Code.
- **Profiles and worktrees:** managed and plain bootstrap, selected-payload
  isolation, real Git worktree/branch creation, immutable source preservation,
  lane/run identity, and epoch turnover.
- **Normal worker completion:** a provider writes real code and tests in a
  disposable Git repository, writes a valid result, ROOT performs review and
  acceptance, the controller observes acceptance, and the lane retires.
- **Invalid-result correction:** every retry outcome in
  `bounded-invalid-result-correction.md`: invalid/missing results on attempts
  one through five, valid recovery on a later attempt, sixth-attempt
  exhaustion, attempt-ledger evidence, cleanup, lease handling, and ROOT's
  terminal event response.
- **Worker-to-ROOT notifications:** `manager-notify` skill, worker outbox,
  monitor promotion, queue persistence, ROOT PostToolUse notice, read-only
  queue inspection, acknowledgement, manual handling, close, delivery
  receipt, promotion failure retention, and retry after repair.
- **ROOT-to-worker assignments:** send a running managed lane an assignment,
  worker acknowledgement/completion/blocking, invalid/terminal assignment
  behavior, and absence of this feature in plain mode.
- **Manager events:** every implemented event type and state transition,
  duplicate/at-least-once handling, required close summary, completion-review
  event ownership, and the rule that closing an event never repairs a lane by
  itself.
- **Failure and recovery conditions:** controller exited, provider exited with
  no result, status/transcript contradiction, cleanup unproven, orphaned lease,
  invalid result, rejected review, missing worktree/session, and the prescribed
  ROOT response for each.
- **Leases and processes:** declared-resource contention, all-or-nothing lease
  acquisition, exact PID-plus-creation-time identity, provider child-process
  boundary cleanup, force-stop, orphaned lease recovery, live-holder refusal,
  and no broad process-name kill.
- **Review and lifecycle commands:** completion review pass/fail/blocked,
  acceptance/rejection/forced acceptance, resume-lane, force-stop, retirement,
  shutdown, cleanup proof, and public-command failure/result shapes.
- **Unsupported providers:** managed bootstrap refusal and plain launch refusal
  before arbitrary external execution.
- **Concurrency and durability:** concurrent lane/lease/queue operations,
  atomic record replacement, queue/header replacement detection, crash/retry
  behavior, and no lost notification or corrupted record.
- **Platform matrix:** all applicable scenario families run on Windows, native
  macOS, and native-storage Linux, with platform-specific process and
  filesystem evidence retained.

### Mandatory agent-behavior observation and adverse-behavior testing

The campaign must test the real agent's behavior, not merely whether the
harness can process ideal records that look as though an agent behaved
correctly. Provider/model instructions, skills, hooks, and task prompts express
expected behavior; they do not guarantee that a real agent will follow them.

For every real-provider scenario, preserve the actual prompt, provider/model
identity, transcript, tool activity where available, files changed, result,
hook/queue records, and ROOT response. Classify each expectation as:

- **Observed:** the agent actually did the expected thing;
- **Not observed:** the scenario did not exercise that expectation; or
- **Deviation:** the agent did something different, incomplete, malformed, or
  unsafe.

At minimum, observe whether the agent:

- stays inside its assigned lane worktree and task scope;
- uses `manager-notify` when it needs a ROOT decision rather than relying only
  on prose in its final response;
- uses and completes ROOT-to-worker assignments through the lane queue;
- writes a valid `RESULT.json` rather than only describing a result in chat;
- follows an invalid-result corrective prompt and repairs the result;
- obeys provider PostToolUse and Stop hook behavior; and
- behaves correctly after interruption, resume, rejection, and a blocked
  resource condition.

The campaign must also deliberately test safe adverse cases: no result file,
malformed result, incorrect lane/run identity, ignored correction request,
ordinary prose instead of a result, worker escalation, stopped provider,
provider/tool failure, and a response that leaves cleanup or lease state
unproven. For each deviation, retain what the agent actually did and prove the
harness takes its prescribed fail-closed path. Do not replace a deviation with a
mocked success, silently repair the agent's record, or count the intended
behavior as observed merely because the prompt asked for it.

## Tests still required

### 1. Real lane lifecycle, once for each selected supported provider

Use a new disposable Git repository inside the project workspace. Give the
worker a small objective coding task, such as adding one function and one unit
test. Prove this full sequence:

```text
harness setup
-> lane bootstrap creates a real worktree
-> lane launch starts the real provider CLI
-> provider edits the lane worktree
-> provider runs the focused test
-> provider writes RESULT.json
-> controller records the session/transcript and proves cleanup
-> ROOT performs completion review
-> lane is accepted or rejected and retired safely
```

The test must retain the exact provider/model, command provenance, session
identity, worktree, result, review, acceptance, process-boundary, and cleanup
records.

### 2. Real worker notification path

During a real managed lane run, require the worker to use its `manager-notify`
skill. Prove:

```text
worker manager-notify
-> worktree manager-notifications/notice-*.json
-> monitor promotion into runtime manager/QUEUE.json
-> ROOT's next native PostToolUse hook reports an unresolved notice
-> ROOT reads the queue read-only
-> ROOT acknowledges the top-level event_id
-> ROOT handles the underlying issue
-> ROOT closes the event with COMPLETE or BLOCKED and a summary
```

Also test the reliability tweak separately: force queue promotion to fail,
confirm that the worker source notice remains in its outbox, then confirm a
later successful monitor pass promotes and archives it.

### 3. Real ROOT and worker hook invocation

For Codex, Claude Code, and Qwen Code, prove from native provider output and
harness records that:

- the installed worker PostToolUse hook runs;
- the worker Stop hook accepts a valid result and blocks an invalid result;
- the installed ROOT PostToolUse hook produces an unresolved-queue notice; and
- the ROOT Stop hook blocks while a manager obligation is unresolved and allows
  normal completion once all obligations are terminal.

Do not count direct Python wrapper calls as this proof. The actual provider CLI
must invoke the hook declaration it was given.

### 4. Real interruption and resume

Start a real lane, stop it using the exact recorded identity, then resume the
same stopped unaccepted lane. Prove the new run ID, provider-session behavior,
fresh result validation, queue integrity, and cleanup of both process
boundaries.

### 5. Unsupported-provider refusal

Use an intentionally unknown provider ID and prove that:

- managed bootstrap refuses it because no worker payload exists; and
- plain launch refuses it before an external provider process starts because no
  registered launcher binding exists.

No generic command execution or provider fallback is permitted.

### 6. Platform matrix

Run the relevant live scenarios on Windows, native macOS, and native-storage
Linux. Retain per-platform evidence for process identity, process cleanup,
filesystem behavior, and the real provider run. A successful Windows-only run
is useful evidence but does not complete the required matrix.

## Acceptance rule

The work is complete only when the recorded live evidence proves the real
provider/hook/launcher lifecycle on all required platforms. Synthetic fixtures,
mocked subprocesses, wrapper unit tests, and authentication probes remain
supporting evidence only.

## Why existing logs cannot prove the harness fully works

The harness records useful evidence for a lane path that actually ran: controller
state/events, provider transcript and stderr, result validation, process cleanup,
leases, manager-event history, review/acceptance records, and hook liveness. That is
enough to investigate many specific lane failures.

It cannot by itself prove that every supported native CLI discovered its generated
hook configuration, honored a hook response, resumed a real session, or completed a
real lane. A record cannot prove an unexecuted integration path exists or works. The
static/unit and disposable-fixture results therefore do not replace the M09 campaign.

There are also known evidence blind spots in the current code:

- The monitor can catch an exception while processing an individual lane and continue
  without persisting that exception; it can later write a fresh healthy heartbeat.
- A normal ROOT hook currently lacks the harness-provided event identity needed to
  append the specified event-level `DELIVERED` receipt. A hook-liveness line can exist
  while the manager event has no delivery evidence.
- Public orphan-lease force release returns structured command evidence but does not
  append a separate durable operation audit record.

Therefore absence of a visible error is not proof that the whole harness is working.
Treat native-provider functionality as **unverified** until the retained M09 evidence
shows the specific provider, platform, scenario, and observed agent behavior.
