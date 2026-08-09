# Manager-attention logging additions specification

## Goal

Record enough timing and activity evidence to determine why a manager response was late.

The logs must distinguish among:

1. the manager was absent or idle and needed to be woken;
2. the manager was busy with other work;
3. the harness delivered the event late or not at all;
4. the manager responded on time but acknowledged the event late; and
5. no agent was actually blocked, so the delay had no operational effect.

This specification adds observation only. It does not authorize waking the manager, controlling agents, acknowledging events, operating hardware, or changing orchestration decisions.

## Component ownership

The logging is distributed across the existing components; neither the harness nor the optional watcher can produce the complete timeline alone.

- **Agents/lane controllers** record signal creation, blocked/waiting state, response receipt, and resumed work.
- **`orchestrator_harness`** records objective signal observation, actionability, deferral, pending delivery, exact acknowledgement, and formal-review baseline changes.
- **Manager or manager-controller wrapper** records manager invocation/activity boundaries, event claim, tool waits, decisions, responses, checkpoints, and intentional waiting/idle boundaries.
- **Optional Harness Watcher** consumes those records, independently measures delays, classifies the evidenced failure mode, and alerts on a real attention or orchestration problem. It must not manufacture missing manager state.

The primary harness remains the source of truth for event delivery. The optional watcher remains a second-order auditor, not a second delivery queue.

## Mandatory optional-watcher gate

**Reminder: every optional Harness Watcher feature described here must remain conditional.** All watcher-specific tailing, state derivation, delay measurement, evaluation, alerting, log mirroring, cursor updates, and acknowledgement integration must check the existing watcher feature flag/runtime availability.

When the optional watcher is disabled, not configured, or not installed:

- all watcher-specific code paths are no-ops;
- no watcher process, evaluator, polling, alert, watcher log, cursor, or state file is created;
- no watcher-owned manager or agent instrumentation is required to run;
- the primary `orchestrator_harness` and normal suite workflow continue unchanged; and
- the absence of watcher output must not itself create an error, warning, manager event, or changed harness result.

Watcher-disabled behavior must not depend on importing the optional watcher package. Shared producers may continue writing their normal manager, harness, and agent lifecycle records, but watcher-only enrichment and consumption must disappear cleanly when the gate is off.

## Proving manager idle or waiting

The watcher cannot determine that a model is idle merely because no new log line appears. A live IDE or Codex process is also not proof that a model turn is active.

The optional watcher should continuously tail the manager's bounded structured log. When the manager runs through `codex exec --json`, an external wrapper should preserve the structured Codex event stream and translate the relevant turn/tool/process boundaries into the manager-attention timeline. For an IDE-managed conversation, an explicit manager logger or hook must publish equivalent boundaries; transcript silence is not a substitute.

The watcher may derive current manager state only from matched structured transitions:

- `MANAGER_WAIT_STARTED` without a matching `MANAGER_WAIT_FINISHED` means deliberately waiting;
- `MANAGER_TOOL_STARTED` without a matching `MANAGER_TOOL_FINISHED` means a tool operation is outstanding;
- `MANAGER_EVENT_CLAIMED` identifies which event currently has the manager's attention;
- `MANAGER_INVOCATION_FINISHED` plus exact process absence means no manager invocation is active; and
- incomplete, missing, buffered, or contradictory lifecycle evidence means `UNKNOWN`.

No-log silence must never be classified as idle. It may represent model reasoning, a running or blocked tool, provider/network delay, buffered output, a stuck process, or a completed turn whose terminal record was lost.

To prove an idle/waiting interval, the manager or its external controller must record explicit boundaries:

- `MANAGER_WAIT_STARTED`: the manager has finished its current work and deliberately entered a bounded wait;
- `MANAGER_WAIT_FINISHED`: that wait returned, including the event or timeout that ended it;
- `MANAGER_INVOCATION_FINISHED`: the manager turn/process ended and no manager invocation remains active; and
- `MANAGER_ACTIVITY_HEARTBEAT`: process/session liveness only, never proof that an event was reviewed.

An external wrapper should also record exact manager PID plus creation time and Codex invocation start/exit when available. If no explicit wait boundary or trustworthy invocation evidence exists, the watcher must classify the interval as `UNKNOWN`, not idle.

The watcher may then measure:

```text
manager wait/absence begins
  -> agent creates a blocking signal
  -> harness makes it pending
  -> manager wait ends or a new invocation starts
  -> manager claims the signal
```

That interval directly tests whether an otherwise idle or absent manager failed to attend to a blocked agent promptly.

## Core requirement

For every manager-relevant agent signal or formal-review deadline, preserve a correlated timeline from creation through agent recovery:

```text
agent creates signal
  -> harness observes signal
  -> harness makes signal actionable
  -> manager first notices signal
  -> manager begins review
  -> manager decides and responds
  -> agent receives response and resumes
  -> manager acknowledges exact harness event
```

Every stage must use stable identifiers so records from different writers can be joined without guessing.

## Required identifiers

Each applicable record must contain:

- `schema`
- `timestamp_utc`
- `epoch_id`
- `event_id`
- `lane_id`, when lane-specific
- `agent_session_id`, when known
- `manager_session_id`, when known
- `manager_invocation_id`, when a manager turn is active
- recorder identity
- relevant process identity as PID plus creation time, when process evidence is available

Missing identity information must remain explicitly unknown. Records must not correlate events by PID, filename, or timestamp proximity alone.

## Required observations

### 1. Agent signal

Record:

- signal creation time;
- signal kind and stable ID;
- whether the agent declares itself blocked;
- what response it needs;
- response deadline, if any;
- whether it can continue useful work without the manager;
- when it begins waiting;
- when it receives the response; and
- when it resumes useful work or reaches its next checkpoint.

### 2. Harness delivery

Record when the harness:

- first observes the stable signal;
- classifies it as actionable or non-actionable;
- selects it as the pending manager notification;
- exposes/delivers that notification;
- defers it behind a higher-priority event;
- receives its exact acknowledgement; and
- advances the applicable formal-review baseline.

When attention logging is enabled, the harness must also emit `HARNESS_SCAN_COMMITTED` after each successful underlying scan commit. It identifies the epoch, stable scan sequence/ID, prior committed-scan record, coverage start/end, exact harness process identity, snapshot/condition generations, and output-root identity. This committed chain is the only evidence that may support a claim that the harness continuously operated through a deadline yet never observed/delivered a matching signal. Any gap, identity change, malformed record, backlog, or missing chain yields `INSUFFICIENT_EVIDENCE`.

Deferral records must identify the selected higher-priority event. The harness must not claim that the manager read an event merely because it was pending.

### 3. Manager lifecycle and activity

Record:

- manager session and invocation start/end;
- exact process identity when externally observable;
- first claim/read of each event;
- start and completion of event review;
- decision completion;
- instruction/response publication;
- exact acknowledgement attempt and result;
- checkpoint completion; and
- start and completion of any long-running tool operation relevant to a delayed response.

Manager activity may use only these conservative states:

- `ABSENT`
- `READING_EVENT`
- `REASONING`
- `RUNNING_TOOL`
- `WAITING_ON_TOOL`
- `HANDLING_OTHER_EVENT`
- `CHECKPOINTING`
- `UNKNOWN`

A live process alone is not proof of useful activity. If the available evidence cannot distinguish working, waiting, or stuck, record `UNKNOWN`.

### 4. Pending-work snapshot

At manager invocation start, event selection, formal-review completion, and invocation end, record:

- every pending event ID;
- event type, priority, and age;
- whether its agent is blocked;
- its response or lease deadline;
- which event was selected; and
- the selection reason.

This snapshot must remain bounded and contain metadata only, not unbounded evidence or transcript content.

### 5. Formal-review deadline

For each formal review, record:

- previous acknowledged baseline;
- configured interval;
- exact next deadline;
- when the due condition was created;
- when it became pending;
- when the manager first noticed it;
- when the review was authored;
- when the exact acknowledgement succeeded;
- the new baseline; and
- the manager's evidenced activity during any late period.

## Event vocabulary

The append-only timeline should support at least:

- `AGENT_SIGNAL_CREATED`
- `AGENT_WAIT_STARTED`
- `HARNESS_SIGNAL_OBSERVED`
- `HARNESS_SCAN_COMMITTED`
- `HARNESS_EVENT_ACTIONABLE`
- `HARNESS_EVENT_DEFERRED`
- `HARNESS_EVENT_PENDING`
- `MANAGER_INVOCATION_STARTED`
- `MANAGER_WAIT_STARTED`
- `MANAGER_WAIT_FINISHED`
- `MANAGER_ACTIVITY_HEARTBEAT`
- `MANAGER_EVENT_CLAIMED`
- `MANAGER_REVIEW_STARTED`
- `MANAGER_TOOL_STARTED`
- `MANAGER_TOOL_FINISHED`
- `MANAGER_DECISION_RECORDED`
- `MANAGER_RESPONSE_PUBLISHED`
- `AGENT_RESPONSE_RECEIVED`
- `AGENT_WORK_RESUMED`
- `HARNESS_ACK_ATTEMPTED`
- `HARNESS_ACK_SUCCEEDED`
- `FORMAL_REVIEW_BASELINE_ADVANCED`
- `MANAGER_CHECKPOINT_COMPLETED`
- `MANAGER_INVOCATION_FINISHED`

## Suggested record shape

```json
{
  "schema": "manager-attention-timeline/v1",
  "timestamp_utc": "2026-08-01T00:00:00.000000Z",
  "epoch_id": "20260731-s1-clean-q-successor",
  "event_id": "stable-event-id",
  "lane_id": "epoch:Atlas:A22",
  "agent_session_id": "agent-session-id",
  "manager_session_id": "manager-session-id",
  "manager_invocation_id": "manager-turn-id",
  "kind": "MANAGER_EVENT_CLAIMED",
  "manager_state": "HANDLING_OTHER_EVENT",
  "agent_blocked": true,
  "recorder": "manager-controller"
}
```

Optional fields must be omitted or explicitly unknown rather than invented.

## Derived timings

The report must calculate, where evidence exists:

- signal creation to harness observation;
- harness observation to actionable selection;
- actionable selection to manager first attention;
- manager first attention to decision;
- decision to agent receipt;
- agent receipt to resumed progress;
- total agent-blocked duration;
- formal-review deadline lateness;
- review-authored to acknowledgement delay; and
- time an actionable event spent deferred behind other work.

## Diagnostic classifications

### `IDLE_OR_ABSENT_MANAGER_DELAY`

Use only when an actionable event was pending, an agent was blocked, the manager was provably absent or had no active invocation, and the response exceeded its required interval.

This classification supports considering a wake-up mechanism.

### `BUSY_MANAGER_DELAY`

Use only when the manager was evidentially handling another event or tool operation throughout the relevant delay.

This points to prioritization, operation length, or concurrency design—not a wake-up problem.

### `HARNESS_DELIVERY_DELAY`

Use when the source signal was stably persisted but the harness did not observe or expose it within the required interval.

### `ACKNOWLEDGEMENT_ONLY_DELAY`

Use when the manager reviewed and responded in time but the exact harness acknowledgement or baseline advance was late.

### `NO_BLOCKING_IMPACT`

Use when no agent required manager feedback to continue and no safety, lease, or review deadline was operationally affected.

### `INSUFFICIENT_EVIDENCE`

Use whenever process, activity, correlation, or timing evidence is incomplete. Do not infer manager idleness from silence or from a live process with no activity record.

## Output and safety requirements

- Use append-only JSONL for the canonical timeline.
- Keep logs in a dedicated observer-owned output directory.
- Do not modify agent signals, experiment evidence, server files, requests, relays, or leases.
- Use stable bounded reads for externally produced records.
- Use UTC timestamps with sufficient precision; preserve source timestamps separately from observer timestamps.
- Prefer host-observed timestamps for cross-process latency calculations.
- Flush durable records before advancing any derived cursor.
- Deduplicate using stable record/event identities.
- Record malformed, missing, or ambiguous evidence as an observation error.
- Do not store model reasoning, credentials, raw tokens, or unnecessary transcript contents.

## Acceptance criteria

The added logging is sufficient only if a synthetic test can independently distinguish all five cases:

1. manager absent while a blocked agent waits;
2. manager busy with another recorded operation;
3. harness delays delivery;
4. manager responds promptly but acknowledges late; and
5. informational event with no blocked agent or operational impact.

At the end of a real sprint, an auditor must be able to classify each late response from durable evidence without inferring manager state from missing logs.

## Decision enabled by this evidence

After at least one representative sprint, use the timeline to answer:

- If late responses are primarily `IDLE_OR_ABSENT_MANAGER_DELAY`, evaluate an external wake-up system such as `codex exec resume`.
- If they are primarily `BUSY_MANAGER_DELAY`, improve prioritization, shorten manager operations, or separate review responsibility.
- If they are `HARNESS_DELIVERY_DELAY`, repair the observation/delivery path.
- If they are `ACKNOWLEDGEMENT_ONLY_DELAY`, repair the acknowledgement lifecycle rather than changing manager wake-up architecture.
